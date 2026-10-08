"""Original Body Relay. Native/generated execution belongs in secured Docker."""
import copy
from functools import lru_cache
import numpy as np

CELL = 4
OFFSET = 4
SIZE = 14
DIRECTIONS = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}
SHAPES = {
    0: ((0, 0), (1, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2)),
    1: ((0, 0), (0, 1), (0, 2)),
    2: ((0, 0), (1, 0), (0, 1), (1, 1)),
}
IDENTITY = {0: 9, 1: 12, 2: 14}
LEVELS = {
    0: {"bodies": (0, 1), "poses": ((4, 5), (7, 5)), "goals": ((4, 5), (7, 4)), "active": 0, "walls": (), "active_tags": ("contact_transfer", "undo")},
    1: {"bodies": (0, 1), "poses": ((5, 5), (4, 5)), "goals": ((5, 4), (4, 3)), "active": 0, "walls": (), "active_tags": ("contact_transfer", "opposite_side", "undo")},
    2: {"bodies": (0, 1), "poses": ((2, 2), (5, 2)), "goals": ((4, 0), (7, 9)), "active": 0, "walls": ((0, 6, 7, 1), (8, 6, 6, 1)), "active_tags": ("contact_transfer", "clearance", "staging", "undo")},
    3: {"bodies": (0, 1), "poses": ((2, 4), (7, 4)), "goals": ((4, 4), (10, 8)), "active": 0, "walls": ((6, 0, 1, 5), (6, 6, 1, 8)), "active_tags": ("contact_transfer", "partition_contact", "undo")},
    4: {"bodies": (0, 1, 2), "poses": ((2, 2), (5, 3), (7, 8)), "goals": ((4, 0), (6, 8), (10, 9)), "active": 1, "walls": ((0, 6, 6, 1), (7, 6, 7, 1)), "active_tags": ("contact_transfer", "return_access", "three_bodies", "undo")},
    5: {"bodies": (0, 1, 2), "poses": ((2, 4), (6, 6), (7, 8)), "goals": ((4, 1), (6, 6), (10, 9)), "active": 2, "walls": ((0, 7, 6, 1), (7, 7, 7, 1)), "active_tags": ("contact_transfer", "temporary_unseating", "three_bodies", "undo")},
    6: {"bodies": (0, 1, 2), "poses": ((2, 2), (5, 3), (6, 8)), "goals": ((4, 0), (8, 9), (6, 8)), "active": 0, "walls": ((0, 6, 6, 1), (7, 6, 7, 1)), "active_tags": ("contact_transfer", "temporary_unseating", "relay_order", "three_bodies", "undo")},
}


@lru_cache(maxsize=4096)
def _pixels(body_id, pose):
    x, y = pose
    return frozenset((OFFSET + CELL * (x + sx) + dx, OFFSET + CELL * (y + sy) + dy)
                     for sx, sy in SHAPES[body_id]
                     for dx in range(CELL) for dy in range(CELL))


@lru_cache(maxsize=7)
def _wall_pixels(level):
    return frozenset((OFFSET + CELL * cx + dx, OFFSET + CELL * cy + dy)
                     for x, y, w, h in LEVELS[level]["walls"]
                     for cx in range(x, x + w) for cy in range(y, y + h)
                     for dx in range(CELL) for dy in range(CELL))


def _rim(pixels):
    return {(x + dx, y + dy) for x, y in pixels for dx, dy in DIRECTIONS.values()} - pixels


def _edge(pixels):
    return {(x, y) for x, y in pixels if any((x + dx, y + dy) not in pixels for dx, dy in DIRECTIONS.values())}


def _footprints(h_t):
    return [_pixels(body, tuple(pose)) for body, pose in zip(LEVELS[h_t["level"]]["bodies"], h_t["poses"])]


def _contacts(h_t):
    footprints = _footprints(h_t)
    active = h_t["active"]
    near = _rim(footprints[active])
    return [i for i, footprint in enumerate(footprints) if i != active and near & footprint]


def _legal_state(h_t):
    footprints = _footprints(h_t)
    walls = _wall_pixels(h_t["level"])
    for i, pixels in enumerate(footprints):
        if any(not OFFSET <= x < OFFSET + CELL * SIZE or not OFFSET <= y < OFFSET + CELL * SIZE for x, y in pixels):
            return False
        if pixels & walls or any(pixels & other for other in footprints[i + 1:]):
            return False
    return True


def _sweep(h_t, direction):
    dx, dy = direction
    footprints = _footprints(h_t)
    active = h_t["active"]
    pixels = footprints[active]
    other = _wall_pixels(h_t["level"]) | frozenset().union(*(p for i, p in enumerate(footprints) if i != active))
    for step in range(1, CELL + 1):
        moved = {(x + step * dx, y + step * dy) for x, y in pixels}
        blocked = moved & other
        blocked |= {(x, y) for x, y in moved if not OFFSET <= x < OFFSET + CELL * SIZE or not OFFSET <= y < OFFSET + CELL * SIZE}
        if blocked:
            return False, sorted(blocked)
    return True, []


def get_initial_state(level):
    cfg = LEVELS[level]
    return {"level": level, "poses": [tuple(p) for p in cfg["poses"]], "active": cfg["active"], "feedback": None, "history": []}, {}


def transition(h_t, z_t, a_t):
    action = a_t[0] if isinstance(a_t, (tuple, list)) else a_t
    if action == 0:
        return get_initial_state(h_t["level"])[0]
    result = copy.deepcopy(h_t)
    if action == 7:
        if result["history"]:
            previous = result["history"].pop()
            history = result["history"]
            result = previous
            result["history"] = history
        return result
    if action not in DIRECTIONS and action != 5:
        return result
    previous = {key: copy.deepcopy(value) for key, value in h_t.items() if key != "history"}
    result["history"].append(previous)
    result["feedback"] = None
    if action in DIRECTIONS:
        legal, blocked = _sweep(h_t, DIRECTIONS[action])
        if legal:
            i = result["active"]
            x, y = result["poses"][i]
            dx, dy = DIRECTIONS[action]
            result["poses"][i] = (x + dx, y + dy)
        else:
            result["feedback"] = {"kind": "blocked", "pixels": blocked}
    else:
        contacts = _contacts(h_t)
        if len(contacts) == 1:
            result["active"] = contacts[0]
        else:
            footprints = _footprints(h_t)
            seam = _rim(footprints[h_t["active"]])
            pixels = sorted(set().union(*(seam & footprints[i] for i in contacts))) if contacts else sorted(_edge(footprints[h_t["active"]]))
            result["feedback"] = {"kind": "ambiguous" if contacts else "no_contact", "pixels": pixels}
    return result


def predict(h_t, seed=0):
    # Fixed deterministic layouts; no private time, stochastic or history goal.
    return {}


def check_level_complete(h_t, z_t, level):
    return (h_t.get("level") == level and len(h_t["poses"]) == len(LEVELS[level]["goals"])
            and all(tuple(pose) == tuple(goal) for pose, goal in zip(h_t["poses"], LEVELS[level]["goals"])))


def render(h_t, z_t):
    canvas = np.full((64, 64), 1, dtype=np.int8)
    canvas[2:4, 2:62] = 3
    canvas[60:62, 2:62] = 3
    canvas[2:62, 2:4] = 3
    canvas[2:62, 60:62] = 3
    cfg = LEVELS[h_t["level"]]
    walls = _wall_pixels(h_t["level"])
    for x, y in walls:
        canvas[y, x] = 3
    # Empty matching material is rendered first; its exterior rim persists at seat.
    for body, goal in zip(cfg["bodies"], cfg["goals"]):
        footprint = _pixels(body, tuple(goal))
        rim = _rim(footprint)
        for x, y in footprint:
            canvas[y, x] = 0
        for x, y in rim:
            if 0 <= x < 64 and 0 <= y < 64 and (x, y) not in walls:
                canvas[y, x] = IDENTITY[body]
    for i, (body, pose) in enumerate(zip(cfg["bodies"], h_t["poses"])):
        pixels = _pixels(body, tuple(pose))
        edge = _edge(pixels)
        for x, y in pixels:
            canvas[y, x] = IDENTITY[body] if (x, y) in edge else (10 if i == h_t["active"] else 3)
    feedback = h_t["feedback"]
    if feedback:
        for x, y in feedback["pixels"]:
            if 0 <= x < 64 and 0 <= y < 64:
                canvas[y, x] = 8
    return canvas


def get_available_actions():
    return [1, 2, 3, 4, 5, 7]


"""Seven-level functional bridge; execute in the secured ARC runtime only."""
import numpy as np
from arcengine import ARCBaseGame, Camera, GameAction, Level, Sprite


class FunctionalGame(ARCBaseGame):
    def __init__(self, seed=0):
        self.functions = self.FUNCTIONS
        self.tick = 0
        self.h_t, self.z_t = self.functions["get_initial_state"](0)
        levels = [Level(grid_size=(64, 64), name=f"Level {i+1}") for i in range(7)]
        super().__init__(game_id=self.GAME_ID, levels=levels,
                         camera=Camera(background=5, letter_box=5),
                         available_actions=self.functions["get_available_actions"](), seed=seed)

    def on_set_level(self, level):
        self.tick = 0
        self.h_t, self.z_t = self.functions["get_initial_state"](self.level_index)
        self.paint()

    def paint(self):
        pixels = np.asarray(self.functions["render"](self.h_t, self.z_t), dtype=np.int8)
        if pixels.shape != (64, 64) or pixels.min() < 0 or pixels.max() > 15:
            raise ValueError("Functional render must be native 64x64 palette indices")
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=pixels, name="viewport", collidable=False))

    def step(self):
        number = int(self.action.id.value)
        if self.action.id != GameAction.RESET:
            event = (number, int(self.action.data["x"]), int(self.action.data["y"])) if number == 6 else number
            self.h_t = self.functions["transition"](self.h_t, self.z_t, event)
            self.tick += 1
            self.z_t = self.functions["predict"](self.h_t, self._seed * 10000 + self.tick)
            self.paint()
            if self.functions["check_level_complete"](self.h_t, self.z_t, self.level_index):
                self.next_level()
        self.complete_action()


class V214(FunctionalGame):
    GAME_ID = 'v214-40ec64554cdecd22'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
