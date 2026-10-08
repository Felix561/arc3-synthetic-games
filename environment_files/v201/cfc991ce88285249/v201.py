"""Fold and Pierce: deterministic material contact, not image reflection."""
from copy import deepcopy

LEVELS = {
    0: {"size": (4, 4), "folds": [("x", 2, "high")], "target": [(1, 1), (2, 1)], "punches": 1, "features": ["vertical contact"]},
    1: {"size": (4, 4), "folds": [("y", 2, "high")], "target": [(2, 0), (2, 3)], "punches": 1, "features": ["horizontal contact"]},
    2: {"size": (4, 4), "folds": [("x", 2, "high"), ("y", 2, "high")], "target": [(0, 0), (3, 0), (0, 3), (3, 3)], "punches": 1, "features": ["two axes"]},
    3: {"size": (6, 4), "folds": [("x", 2, "low"), ("x", 3, "high")], "target": [(0, 1), (3, 1)], "punches": 1, "features": ["asymmetric crease choice"]},
    4: {"size": (6, 6), "folds": [("x", 2, "low"), ("x", 3, "high"), ("y", 3, "high")], "target": [(1, 1), (2, 1), (1, 4), (2, 4)], "punches": 1, "features": ["asymmetric two axes"]},
    5: {"size": (6, 4), "folds": [("x", 2, "low"), ("x", 3, "high")], "target": [(0, 0), (3, 0), (1, 2), (4, 2)], "punches": 2, "features": ["different contact groups", "unfold and prepare"]},
    6: {"size": (6, 6), "folds": [("x", 2, "low"), ("x", 3, "high"), ("y", 3, "high")], "target": [(0, 0), (1, 0), (2, 0), (3, 0), (0, 5), (1, 5), (2, 5), (3, 5), (1, 2), (4, 2), (5, 3)], "punches": 3, "features": ["parallel crease order", "mixed contact groups", "singleton"]},
}


def get_available_actions():
    return [5, 6, 7]


def get_initial_state(level):
    w, h = LEVELS[level]["size"]
    return {"level": level, "locations": [[x, y] for y in range(h) for x in range(w)],
            "holes": [], "remaining": LEVELS[level]["punches"], "folded": [], "history": []}, {}


def predict(h_t, seed=0):
    return {}


def _geometry(level):
    w, h = LEVELS[level]["size"]
    c = 10 if w == 4 else 7
    return (64 - w * c) // 2, 12, c, w, h


def _handle(level, fold):
    ox, oy, c, w, h = _geometry(level)
    axis, k, side = fold
    return (ox + k*c, 6) if axis == "x" else (5, oy + k*c)


def _snapshot(state):
    return {k: deepcopy(v) for k, v in state.items() if k != "history"}


def _save(state):
    state["history"].append(_snapshot(state))


def transition(h_t, z_t, action):
    s = deepcopy(h_t)
    number = action[0] if isinstance(action, (tuple, list)) else action
    if number == 7:
        if s["history"]:
            previous = s["history"].pop()
            previous["history"] = s["history"]
            return previous
        return s
    if number == 5:
        if s["folded"]:
            _save(s)
            _, _, _, w, h = _geometry(s["level"])
            s["locations"] = [[x, y] for y in range(h) for x in range(w)]
            s["folded"] = []
        return s
    if number != 6 or not isinstance(action, (tuple, list)) or len(action) != 3:
        return s
    px, py = action[1:]
    if not isinstance(px, int) or not isinstance(py, int) or not (0 <= px < 64 and 0 <= py < 64):
        return s
    # The two drawn controls also accept clicks; keyboard Space and Undo agree.
    if 3 <= px <= 29 and 57 <= py <= 63:
        return transition(s, z_t, 5)
    if 33 <= px <= 48 and 57 <= py <= 63:
        return transition(s, z_t, 7)
    spec = LEVELS[s["level"]]
    for i, fold in enumerate(spec["folds"]):
        hx, hy = _handle(s["level"], fold)
        if abs(px-hx) <= 3 and abs(py-hy) <= 3:
            if i in s["folded"]:
                return s
            axis, k, side = fold
            dimension = 0 if axis == "x" else 1
            positions = deepcopy(s["locations"])
            for p in positions:
                moving = p[dimension] < k if side == "low" else p[dimension] >= k
                if moving:
                    p[dimension] = 2*k - 1 - p[dimension]
            if positions == s["locations"]:
                return s
            _save(s)
            s["locations"] = positions
            s["folded"].append(i)
            return s
    ox, oy, c, w, h = _geometry(s["level"])
    if not (ox <= px < ox+w*c and oy <= py < oy+h*c):
        return s
    point = [(px-ox)//c, (py-oy)//c]
    contacted = [i for i, location in enumerate(s["locations"]) if location == point]
    new_holes = set(contacted) - set(s["holes"])
    if not new_holes or s["remaining"] <= 0:
        return s
    _save(s)
    s["holes"] = sorted(set(s["holes"]) | set(contacted))
    s["remaining"] -= 1
    return s


def check_level_complete(h_t, z_t, level):
    if h_t["level"] != level or h_t["folded"]:
        return False
    w, h = LEVELS[level]["size"]
    originals = [[x, y] for y in range(h) for x in range(w)]
    wanted = {y*w+x for x, y in LEVELS[level]["target"]}
    return h_t["locations"] == originals and set(h_t["holes"]) == wanted


def _rect(grid, x0, y0, x1, y1, color):
    for y in range(max(0, y0), min(64, y1)):
        for x in range(max(0, x0), min(64, x1)):
            grid[y][x] = color


def _outline(grid, x0, y0, x1, y1, color):
    _rect(grid, x0, y0, x1, y0+1, color)
    _rect(grid, x0, y1-1, x1, y1, color)
    _rect(grid, x0, y0, x0+1, y1, color)
    _rect(grid, x1-1, y0, x1, y1, color)


def render(h_t, z_t):
    s = h_t
    spec = LEVELS[s["level"]]
    ox, oy, c, w, h = _geometry(s["level"])
    grid = [[1 for _ in range(64)] for _ in range(64)]
    # White backing is fixed in original material coordinates. Pink outlines
    # remain visible before, during, and after a fold; they are wanted apertures.
    _rect(grid, ox-1, oy-1, ox+w*c+1, oy+h*c+1, 2)
    _rect(grid, ox, oy, ox+w*c, oy+h*c, 0)
    groups = {}
    for identity, (x, y) in enumerate(s["locations"]):
        groups.setdefault((x, y), []).append(identity)
    holes = set(s["holes"])
    for (x, y), identities in groups.items():
        xx, yy = ox+x*c, oy+y*c
        _rect(grid, xx, yy, xx+c, yy+c, 10)
        # Thin seams retain a coherent sheet but make punch cells inspectable.
        _rect(grid, xx+c-1, yy, xx+c, yy+c, 11)
        _rect(grid, xx, yy+c-1, xx+c, yy+c, 11)
        if len(identities) > 1:
            _rect(grid, xx+c-2, yy+1, xx+c-1, yy+c-1, 12)
        punctured = sum(i in holes for i in identities)
        if punctured:
            color = 5 if punctured == len(identities) else 12
            _rect(grid, xx+2, yy+2, xx+c-2, yy+c-2, color)
    for x, y in spec["target"]:
        xx, yy = ox+x*c, oy+y*c
        _outline(grid, xx+1, yy+1, xx+c-1, yy+c-1, 6)
    for i, fold in enumerate(spec["folds"]):
        axis, k, side = fold
        hx, hy = _handle(s["level"], fold)
        color = 3 if i in s["folded"] else 15
        if axis == "x":
            _rect(grid, ox+k*c-1, oy, ox+k*c, oy+h*c, 2)
        else:
            _rect(grid, ox, oy+k*c-1, ox+w*c, oy+k*c, 2)
        _rect(grid, hx-3, hy-3, hx+4, hy+4, color)
        # Arrows describe the moving side's direction toward the crease.
        if axis == "x":
            direction = 1 if side == "low" else -1
            _rect(grid, hx-2, hy, hx+3, hy+1, 0)
            for dy in (-1, 1):
                grid[hy+dy][hx+direction] = 0
        else:
            direction = 1 if side == "low" else -1
            _rect(grid, hx, hy-2, hx+1, hy+3, 0)
            for dx in (-1, 1):
                grid[hy+direction][hx+dx] = 0
    # Contact thickness cross-section sits immediately beside the material.
    depth = max(len(ids) for ids in groups.values())
    for i in range(depth):
        _rect(grid, 56, 14+i*3, 63, 16+i*3, 10)
        _rect(grid, 56, 16+i*3, 63, 17+i*3, 11)
    # Drawn unfold key with a broad flat sheet; drawn undo key with return arrow.
    _rect(grid, 3, 57, 30, 64, 3)
    _rect(grid, 9, 59, 24, 62, 0)
    _rect(grid, 33, 57, 49, 64, 3)
    _rect(grid, 37, 59, 45, 60, 0)
    _rect(grid, 43, 60, 45, 62, 0)
    grid[58][38] = 0
    grid[60][38] = 0
    # Countable unused punch plugs beside the controls, not a progress bar.
    for i in range(spec["punches"]):
        xx = 51+i*4
        _outline(grid, xx, 58, xx+3, 63, 3)
        if i < s["remaining"]:
            _rect(grid, xx+1, 59, xx+2, 62, 5)
    return grid


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


class V201(FunctionalGame):
    GAME_ID = 'v201-cfc991ce88285249'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
