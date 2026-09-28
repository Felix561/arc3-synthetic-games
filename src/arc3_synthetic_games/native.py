"""Small native engine player. This executes only the installed curated game files."""

import importlib.util
import json
import sys
from threading import RLock

from arcengine import ActionInput, ARCBaseGame, GameAction, GameState

from .dataset import dataset_root, find_game

_classes = {}
_class_lock = RLock()


def game_class(entry):
    identity = entry["game_id"]
    with _class_lock:
        if identity not in _classes:
            folder = dataset_root() / entry["environment_path"]
            metadata = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
            name = metadata["class_name"]
            spec = importlib.util.spec_from_file_location(
                "native_" + identity.replace("-", "_"), folder / (name.lower() + ".py")
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            cls = getattr(module, name)
            if not issubclass(cls, ARCBaseGame) or cls.perform_action is not ARCBaseGame.perform_action:
                raise ValueError("Unexpected native game lifecycle")
            _classes[identity] = cls
        return _classes[identity]


class NativeGame:
    def __init__(self, identity, level=0):
        self.entry = find_game(identity)
        self.game = game_class(self.entry)(seed=0)
        self.observation = None
        self.lock = RLock()
        self.select_level(level)

    def select_level(self, level):
        if type(level) is not int or not 0 <= level < 7:
            raise ValueError("Choose a level from 1 through 7")
        with self.lock:
            self.game.full_reset()
            self.game.set_level(level)
            # Set the pinned engine's progression cursor for direct level browsing.
            # This is not evidence that the earlier levels were played or solved.
            self.game._score = level
            self.game._state = GameState.NOT_FINISHED
            self.game._next_level = False
            self.game._action_count = 1
            return self.act(0)

    def act(self, action_id, data=None):
        with self.lock:
            allowed = (
                self.observation["available_actions"] if self.observation else self.game._available_actions
            )
            if (
                type(action_id) is not int
                or action_id not in range(8)
                or (action_id and action_id not in allowed)
            ):
                raise ValueError("This action is unavailable")
            if self.observation and self.observation["state"] in ("WIN", "GAME_OVER") and action_id:
                raise ValueError("Reset this level or choose another level")
            data = {} if data is None else data
            if not isinstance(data, dict):
                raise TypeError("Invalid action data")
            if action_id == 6:
                if set(data) != {"x", "y"} or any(
                    type(data[k]) is not int or not 0 <= data[k] < 64 for k in data
                ):
                    raise ValueError("Click coordinates must lie inside the 64×64 grid")
            elif data:
                raise ValueError("Only click actions take coordinates")
            native = self.game.perform_action(ActionInput(id=GameAction.from_id(action_id), data=data))
            frames = native.frame
            if not frames or len(frames) > 128:
                raise ValueError("Unexpected animation response")
            for frame in frames:
                if len(frame) != 64 or any(
                    len(row) != 64 or any(type(v) is not int or not 0 <= v < 16 for v in row) for row in frame
                ):
                    raise ValueError("Unexpected native palette frame")
            self.observation = {
                "frames": frames,
                "state": native.state.value,
                "level_index": self.game.level_index,
                "available_actions": list(native.available_actions),
                "full_reset": bool(native.full_reset),
            }
            return self.observation

    def reset(self):
        with self.lock:
            return self.select_level(self.game.level_index)

    def restart(self):
        with self.lock:
            self.game = game_class(self.entry)(seed=0)
            self.observation = None
            return self.select_level(0)
