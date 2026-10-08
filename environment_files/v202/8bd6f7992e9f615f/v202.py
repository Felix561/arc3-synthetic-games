"""Cam Lift: geometric contact with one guided, travelling carriage."""
from copy import deepcopy
from functools import lru_cache
from math import cos, sin, pi

LEVELS = {
    0: {"phase": 1, "windows": [[25, 33]], "bays": [None, None], "supply": None},
    1: {"phase": 6, "windows": [[24, 31]], "bays": [None, None], "supply": None},
    2: {"phase": 1, "windows": [[25, 32], [24, 30], [26, 32]], "bays": [None, None, None, None], "supply": None},
    3: {"phase": 1, "windows": [[26, 32], [24, 30], [26, 32]], "bays": [None, None, None, None], "supply": 6},
    4: {"phase": 2, "windows": [[26, 31], [25, 30]], "bays": [None, None, None], "supply": 3},
    5: {"phase": 2, "windows": [[26, 31], [26, 31], [25, 30]], "bays": [None, [26, 31], None, None], "supply": 3},
    6: {"phase": 2, "windows": [[26, 31], [26, 31], [25, 30], [27, 32]], "bays": [None, [26, 31], None, None, None], "supply": 5},
}

CAM = ((0, -10), (4, -9), (8, -4), (6, 5), (0, 7), (-6, 5), (-8, -4), (-4, -9))


@lru_cache(maxsize=256)
def _cam(phase):
    angle = phase*pi/6
    c, s = cos(angle), sin(angle)
    vertices = [(int(round(x*c-y*s)), int(round(x*s+y*c))) for x, y in CAM]
    cells = []
    for y in range(-11, 12):
        for x in range(-11, 12):
            crosses = [(b[0]-a[0])*(y-a[1])-(b[1]-a[1])*(x-a[0])
                       for a, b in zip(vertices, vertices[1:]+vertices[:1])]
            if all(v >= 0 for v in crosses) or all(v <= 0 for v in crosses):
                cells.append((x, y))
    return tuple(cells), tuple(vertices)


def _geometry(phase):
    cells, vertices = _cam(phase)
    # Broad flat shoe covers every x of the rotated solid. Its lower edge
    # touches the first occupied raster row; no detached radius lookup exists.
    contact = 49 + min(y for x, y in cells)
    shoe = contact-1
    return {"cells": cells, "vertices": vertices, "contact": contact, "shoe": shoe,
            "top": shoe-14, "bottom": shoe-9, "wheel_bottom": 49+max(y for x, y in cells)}


def _fits(geometry, interval):
    return interval is None or interval[0] <= geometry["top"] and geometry["bottom"] <= interval[1]


def _core(h):
    return {k: deepcopy(v) for k, v in h.items() if k != "history"}


def get_initial_state(level_index):
    spec = LEVELS[level_index]
    h = {"level": level_index, "phase": spec["phase"], "station": 0,
         "remaining": spec["supply"], "feedback": None, "history": []}
    return h, predict(h, 0)


def get_available_actions():
    return [3, 4, 5, 7]


def predict(h_t, seed):
    # The seed does not perturb this deliberately fixed geometric machine.
    return _geometry(h_t["phase"])


def transition(h_t, z_t, action):
    h = deepcopy(h_t)
    spec = LEVELS[h["level"]]
    if action == 7:
        if h["history"]:
            previous = h["history"].pop()
            h.update(previous)
        return h
    if h["station"] >= len(spec["windows"]):
        return h
    if action in (3, 4):
        direction = -1 if action == 3 else 1
        if h["remaining"] == 0:
            h["feedback"] = ["supply", 0]
            return h
        # Sample the same rotating solid through the complete 30 degree turn,
        # so an equal endpoint height can still collide during the sweep.
        for sample in range(1, 9):
            geometry = _geometry((h["phase"]+direction*sample/8) % 12)
            if not _fits(geometry, spec["bays"][h["station"]]) or geometry["wheel_bottom"] > 60:
                h["feedback"] = ["bay", geometry["top"]]
                return h
        h["history"].append(_core(h_t))
        h["phase"] = (h["phase"]+direction) % 12
        if h["remaining"] is not None:
            h["remaining"] -= 1
        h["feedback"] = None
        return h
    if action == 5:
        geometry = _geometry(h["phase"])
        # Horizontal travel holds the supported load at its current height.
        # Its swept x rectangle intersects the next actual wall/window.
        if not _fits(geometry, spec["windows"][h["station"]]):
            h["feedback"] = ["wall", h["station"]]
            return h
        if not _fits(geometry, spec["bays"][h["station"]+1]):
            h["feedback"] = ["bay", geometry["top"]]
            return h
        h["history"].append(_core(h_t))
        h["station"] += 1
        h["feedback"] = None
        return h
    return h


def check_level_complete(h_t, z_t, level_index):
    return h_t["level"] == level_index and h_t["station"] == len(LEVELS[level_index]["windows"])


def render(h_t, z_t):
    grid = [[5 for _ in range(64)] for _ in range(64)]
    def rect(x0, y0, x1, y1, color):
        for y in range(max(0, y0), min(63, y1)+1):
            for x in range(max(0, x0), min(63, x1)+1):
                grid[y][x] = color
    spec = LEVELS[h_t["level"]]
    cx = 12+10*h_t["station"]
    geometry = _geometry(h_t["phase"])
    # The lower actuator lane is continuous beneath the cargo-plane walls.
    rect(1, 60, 62, 61, 3)
    rect(cx-8, 59, cx+8, 59, 2)
    for x, y in geometry["cells"]:
        if 0 <= cx+x < 64 and 0 <= 49+y < 64:
            grid[49+y][cx+x] = 9
    # A single dark spoke marks real angular pose, including equal lift poses.
    vx, vy = geometry["vertices"][0]
    for i in range(11):
        x, y = cx+int(round(vx*i/10)), 49+int(round(vy*i/10))
        if 0 <= x < 64 and 0 <= y < 64:
            grid[y][x] = 4
    rect(cx-1, 48, cx+1, 50, 2)
    shoe = geometry["shoe"]
    rect(cx-11, shoe-1, cx+11, shoe, 2)
    # One vertical guided follower joins shoe to the platform/cargo. It is
    # behind the cargo obstacle plane and is occluded by its lower wall panels.
    rect(cx, geometry["bottom"]+1, cx, shoe-2, 2)
    rect(cx-3, geometry["bottom"]+1, cx+3, geometry["bottom"]+2, 2)
    for i, window in enumerate(spec["windows"]):
        wx = 17+10*i
        rect(wx, 8, wx+1, window[0]-1, 3)
        rect(wx, window[1]+1, wx+1, 35, 3)
        rect(wx, window[0], wx+1, window[1], 1)
    for i, bay in enumerate(spec["bays"]):
        if bay is not None:
            left, right = 8+10*i, 15+10*i
            rect(left, bay[0]-2, right, bay[0]-1, 3)
            rect(left, bay[1]+1, right, bay[1]+2, 3)
    # Destination is an open receiving bay, spatially beyond all walls.
    end = 12+10*len(spec["windows"])
    rect(end-3, 21, end-3, 35, 11)
    rect(end+3, 21, end+3, 35, 11)
    rect(end-3, 35, end+3, 35, 11)
    rect(cx-2, geometry["top"], cx+2, geometry["bottom"], 12)
    rect(cx-1, geometry["top"]+1, cx+1, geometry["bottom"]-1, 0)
    # Separate, countable drive pins stay next to the travelling axle.
    if spec["supply"] is not None:
        for i in range(spec["supply"]):
            px = cx-8+3*i
            rect(px, 62, px+1, 63, 9 if i < h_t["remaining"] else 3)
    if h_t["feedback"]:
        kind, value = h_t["feedback"]
        if kind == "wall":
            wx = 17+10*value
            rect(wx, geometry["top"], wx+1, geometry["bottom"], 8)
        elif kind == "bay":
            bay = spec["bays"][h_t["station"]]
            if bay:
                yy = bay[0]-1 if value < bay[0] else bay[1]+1
                rect(cx-2, yy, cx+2, yy, 8)
        else:
            rect(cx-1, 48, cx+1, 50, 8)
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


class V202(FunctionalGame):
    GAME_ID = 'v202-8bd6f7992e9f615f'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
