"""Original stationary figures and actual foreground access; no solution helpers."""
import copy


LEVELS = {
    0: {
        "active_tags": ["object_continuity", "attached_query"],
        "figures": [{"path": [[10, 20], [28, 20], [28, 40], [53, 40]], "width": 7}],
        "collars": [[0, 6, 16, 8, 9], [0, 50, 36, 8, 9]],
        "screens": [],
    },
    1: {
        "active_tags": ["object_continuity", "attached_query", "figure_overlap"],
        "figures": [
            {"path": [[9, 17], [46, 17], [46, 43], [54, 43]], "width": 7},
            {"path": [[9, 43], [27, 43], [27, 29], [55, 29]], "width": 7},
        ],
        "collars": [[0, 5, 13, 8, 9], [0, 51, 39, 8, 9]],
        "screens": [],
    },
    2: {
        "active_tags": ["object_continuity", "attached_query", "foreground_access"],
        "figures": [
            {"path": [[22, 26], [33, 26], [33, 36], [42, 36]], "width": 7},
            {"path": [[8, 49], [53, 49]], "width": 7},
        ],
        "collars": [[0, 18, 22, 8, 9], [0, 39, 32, 8, 9]],
        "screens": [{"rect": [24, 18, 17, 25], "grip": [5, -7, 7, 8], "axis": "x", "bounds": [5, 44], "step": 8}],
    },
    3: {
        "active_tags": ["object_continuity", "attached_query", "foreground_access", "split_visible_parts"],
        "figures": [
            {"path": [[10, 15], [32, 15], [32, 44], [54, 44]], "width": 7},
            {"path": [[10, 44], [19, 44], [19, 30], [50, 30], [50, 15], [54, 15]], "width": 7},
        ],
        "collars": [[0, 6, 11, 8, 9], [0, 51, 40, 8, 9]],
        "screens": [{"rect": [25, 9, 14, 46], "grip": [4, -7, 7, 8], "axis": "x", "bounds": [5, 45], "step": 8}],
    },
    4: {
        "active_tags": ["object_continuity", "attached_query", "foreground_access", "occluded_turn"],
        "figures": [
            {"path": [[10, 30], [24, 30], [24, 14], [54, 14]], "width": 7},
            {"path": [[10, 14], [18, 14], [18, 48], [54, 48], [54, 30], [36, 30]], "width": 7},
        ],
        "collars": [[0, 6, 26, 8, 9], [0, 51, 10, 8, 9]],
        "screens": [{"rect": [17, 9, 27, 31], "grip": [10, -7, 7, 8], "axis": "y", "bounds": [9, 30], "step": 8}],
    },
    5: {
        "active_tags": ["object_continuity", "attached_query", "foreground_access", "layered_handle_access"],
        "figures": [
            {"path": [[22, 32], [43, 32]], "width": 7},
            {"path": [[8, 48], [52, 48], [52, 12], [8, 12]], "width": 7},
        ],
        "collars": [[0, 18, 28, 8, 9], [0, 40, 28, 8, 9]],
        "screens": [
            {"rect": [24, 24, 18, 15], "grip": [5, -7, 7, 8], "axis": "x", "bounds": [4, 44], "step": 8},
            {"rect": [18, 16, 27, 12], "grip": [-7, 6, 8, 8], "axis": "x", "bounds": [10, 34], "step": 8},
        ],
    },
    6: {
        "active_tags": ["object_continuity", "attached_query", "foreground_access", "orthogonal_foreground_union"],
        "figures": [
            {"path": [[20, 33], [32, 33], [32, 18], [36, 18], [36, 48], [45, 48]], "width": 7},
            {"path": [[10, 12], [10, 57], [54, 57], [54, 20], [24, 20]], "width": 7},
        ],
        "collars": [[0, 16, 29, 8, 9], [0, 42, 44, 8, 9]],
        "screens": [
            {"rect": [25, 10, 17, 43], "grip": [-7, 4, 8, 8], "axis": "x", "bounds": [9, 41], "step": 8},
            {"rect": [24, 27, 27, 13], "grip": [10, -7, 7, 8], "axis": "y", "bounds": [11, 43], "step": 8},
        ],
    },
}


def _rect_cells(rect):
    x, y, w, h = rect
    return {(px, py) for py in range(y, y + h) for px in range(x, x + w)}


def _figure_cells(figure):
    cells = set()
    r = figure["width"] // 2
    points = figure["path"]
    for a, b in zip(points, points[1:]):
        cells.update(_rect_cells([min(a[0], b[0]) - r, min(a[1], b[1]) - r,
                                  abs(a[0] - b[0]) + 2 * r + 1,
                                  abs(a[1] - b[1]) + 2 * r + 1]))
    return cells


def _screen_parts(h_t, index):
    spec = LEVELS[h_t["level"]]["screens"][index]
    x, y = h_t["poses"][index]
    _, _, w, height = spec["rect"]
    gx, gy, gw, gh = spec["grip"]
    return [x, y, w, height], [x + gx, y + gy, gw, gh]


def _border(cells, point):
    x, y = point
    return any((x + dx, y + dy) not in cells for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


def _foreground_at(h_t, x, y):
    top = -1
    for index in range(len(LEVELS[h_t["level"]]["screens"])):
        if any((x, y) in _rect_cells(r) for r in _screen_parts(h_t, index)):
            top = index
    return top


def _scene(h_t, feedback=True):
    grid = [[0] * 64 for _ in range(64)]
    owners = [[-1] * 64 for _ in range(64)]
    controls = [[-1] * 64 for _ in range(64)]
    spec = LEVELS[h_t["level"]]
    for owner, figure in enumerate(spec["figures"]):
        cells = _figure_cells(figure)
        for x, y in cells:
            grid[y][x] = 4 if _border(cells, (x, y)) else 9
            owners[y][x] = owner
    for owner, x, y, w, height in spec["collars"]:
        cells = _rect_cells([x, y, w, height])
        for px, py in cells:
            grid[py][px] = 4 if _border(cells, (px, py)) else 0
            owners[py][px] = -1
    for index in range(len(spec["screens"])):
        body, grip = _screen_parts(h_t, index)
        for rect, is_grip in ((body, False), (grip, True)):
            cells = _rect_cells(rect)
            for x, y in cells:
                grid[y][x] = 4 if _border(cells, (x, y)) else (12 if h_t["selected"] == index else 7) if is_grip else 2
                owners[y][x] = -1
                controls[y][x] = index if is_grip else -1
        gx, gy, gw, gh = grip
        cx, cy = gx + gw // 2, gy + gh // 2
        if spec["screens"][index]["axis"] == "x":
            marks = [(cx + d, cy) for d in range(-2, 3)] + [(cx - 1, cy - 1), (cx - 1, cy + 1), (cx + 1, cy - 1), (cx + 1, cy + 1)]
        else:
            marks = [(cx, cy + d) for d in range(-2, 3)] + [(cx - 1, cy - 1), (cx + 1, cy - 1), (cx - 1, cy + 1), (cx + 1, cy + 1)]
        for x, y in marks:
            grid[y][x] = 4
    if feedback and h_t["feedback"] is not None:
        info = h_t["feedback"]
        if info["kind"] == "wrong":
            for y in range(64):
                for x in range(64):
                    if owners[y][x] == info["owner"]:
                        grid[y][x] = 8
        elif info["kind"] == "blocked" and info.get("screen") is not None:
            index = info["screen"]
            body, grip = _screen_parts(h_t, index)
            edge = _rect_cells(body) | _rect_cells(grip)
            for x, y in edge:
                if _border(edge, (x, y)) and _foreground_at(h_t, x, y) == index:
                    grid[y][x] = 8
        else:
            x, y = info["point"]
            for dx, dy in ((-3, -3), (-2, -3), (-1, -3), (0, -3), (1, -3), (2, -3), (3, -3),
                           (-3, 3), (-2, 3), (-1, 3), (0, 3), (1, 3), (2, 3), (3, 3),
                           (-3, -2), (-3, -1), (-3, 0), (-3, 1), (-3, 2),
                           (3, -2), (3, -1), (3, 0), (3, 1), (3, 2)):
                if 0 <= x + dx < 64 and 0 <= y + dy < 64:
                    grid[y + dy][x + dx] = 12 if info["kind"] == "collar" else 8
    return grid, owners, controls


def _snapshot(h_t):
    return copy.deepcopy({k: v for k, v in h_t.items() if k != "history"})


def get_initial_state(level):
    spec = LEVELS[level]
    return {"level": level, "poses": [s["rect"][:2] for s in spec["screens"]],
            "selected": None, "answer": None, "feedback": None, "history": []}, {}


def get_available_actions():
    return [1, 2, 3, 4, 6, 7]


def predict(h_t, seed=0):
    return {}


def check_level_complete(h_t, z_t, level):
    if h_t["level"] != level or h_t["answer"] is None:
        return False
    _, owners, _ = _scene(h_t, False)
    x, y = h_t["answer"]
    collar_owners = {collar[0] for collar in LEVELS[level]["collars"]}
    return len(collar_owners) == 1 and owners[y][x] in collar_owners


def transition(h_t, z_t, action):
    h = copy.deepcopy(h_t)
    number = action[0] if isinstance(action, (tuple, list)) else action
    if number == 7:
        if h["history"]:
            previous = h["history"].pop()
            previous["history"] = h["history"]
            return previous
        return h
    if number == 0:
        return get_initial_state(h["level"])[0]
    h["history"].append(_snapshot(h))
    h["feedback"] = None
    h["answer"] = None
    _, owners, controls = _scene(h, False)
    if number == 6:
        _, x, y = action
        control = controls[y][x]
        if control >= 0:
            h["selected"] = None if h["selected"] == control else control
        elif owners[y][x] >= 0:
            h["answer"] = [x, y]
            wanted = {c[0] for c in LEVELS[h["level"]]["collars"]}
            if owners[y][x] not in wanted:
                h["feedback"] = {"kind": "wrong", "owner": owners[y][x], "point": [x, y]}
        else:
            is_collar = any((x, y) in _rect_cells(c[1:]) for c in LEVELS[h["level"]]["collars"])
            h["feedback"] = {"kind": "collar" if is_collar else "empty", "point": [x, y]}
    elif number in (1, 2, 3, 4):
        index = h["selected"]
        if index is None:
            h["feedback"] = {"kind": "empty", "point": [32, 32]}
        else:
            spec = LEVELS[h["level"]]["screens"][index]
            accessible = any(index in row for row in controls)
            dx, dy = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}[number]
            axis = 0 if spec["axis"] == "x" else 1
            delta = (dx, dy)[axis] * spec["step"]
            proposed = h["poses"][index][axis] + delta
            if not accessible or delta == 0 or not spec["bounds"][0] <= proposed <= spec["bounds"][1]:
                h["feedback"] = {"kind": "blocked", "screen": index}
            else:
                h["poses"][index][axis] = proposed
    return h


def render(h_t, z_t):
    return _scene(h_t)[0]


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


class V211(FunctionalGame):
    GAME_ID = 'v211-81d4dbeea8d1234c'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
