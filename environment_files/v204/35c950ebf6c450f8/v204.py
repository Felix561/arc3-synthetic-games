"""Original private V2 environment: rigid contact assemblies and local peeling.

Execute only inside the secured native runtime. Validation helpers are separate.
"""
from copy import deepcopy


LEVELS = {
    0: {"poses": [(2, 4), (5, 4)], "walls": [], "receiver": (7, 2, 10, 7), "jaws": [], "departure": None, "goal": "arrival", "tags": ["contact", "shared_translation"]},
    1: {"poses": [(2, 4), (3, 2)], "walls": [(5, 2)], "receiver": (7, 0, 10, 2), "jaws": [], "departure": None, "goal": "arrival", "tags": ["attachment_side", "shared_collision"]},
    2: {"poses": [(2, 4), (5, 4)], "walls": [], "receiver": (9, 1, 10, 8), "jaws": [(9, 4, -1, 0)], "departure": (0, 4), "goal": "separate_return", "tags": ["local_peel", "carrier_return"]},
    3: {"poses": [(1, 4), (4, 4), (7, 4)], "walls": [(5, 0), (5, 1), (5, 2), (5, 3), (5, 6), (5, 7), (5, 8), (5, 9)], "receiver": (9, 1, 10, 8), "jaws": [(10, 4, -1, 0), (9, 7, -1, 0)], "departure": (0, 4), "goal": "separate_return", "tags": ["aperture", "staged_peeling", "parking"]},
    4: {"poses": [(1, 4), (4, 4), (6, 4), (8, 4)], "walls": [(4, 0), (4, 1), (4, 2), (4, 3), (4, 6), (4, 7), (4, 8), (4, 9)], "receiver": (9, 0, 10, 8), "jaws": [(10, 4, -1, 0), (9, 7, -1, 0), (9, 1, -1, 0)], "departure": (0, 4), "goal": "separate_return", "tags": ["successive_partition", "clearance", "receiver_access"]},
    5: {"poses": [(0, 5), (3, 5), (5, 5), (7, 2)], "walls": [(5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3)], "receiver": (9, 4, 10, 9), "jaws": [(10, 5, -1, 0), (9, 8, -1, 0), (9, 4, -1, 0)], "departure": (0, 5), "goal": "separate_return", "tags": ["assembled_reach", "retraction", "reuse"]},
    6: {"poses": [(0, 6), (3, 6), (5, 6), (7, 2), (8, 6)], "walls": [(5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3)], "receiver": (9, 4, 10, 9), "jaws": [(10, 6, -1, 0), (10, 8, -1, 0), (9, 4, -1, 0), (9, 7, -1, 0)], "departure": (0, 6), "goal": "separate_return", "tags": ["assembled_reach", "recruitment", "parking_order"]},
}

WIDTH, HEIGHT, UNIT, ORIGIN_X, ORIGIN_Y = 11, 10, 5, 4, 7
DIRECTIONS = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}


def get_available_actions():
    return [1, 2, 3, 4, 5, 7]


def predict(h_t, seed=0):
    return {}


def _cells(poses, index):
    x, y = poses[index]
    if index == 0:
        return {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}
    return {(x, y)}


def _touching(poses, a, b):
    right = _cells(poses, b)
    return any((x + dx, y + dy) in right for x, y in _cells(poses, a)
               for dx, dy in DIRECTIONS.values())


def _component(bonds, start):
    found = {start}
    while True:
        grown = found | {b for a, b in bonds if a in found} | {a for a, b in bonds if b in found}
        if grown == found:
            return found
        found = grown


def _contacts(h, moved):
    bonds = {tuple(edge) for edge in h["bonds"]}
    active = set(moved)
    additions = []
    while True:
        changed = False
        for a in range(len(h["poses"])):
            for b in range(a + 1, len(h["poses"])):
                if (a in active or b in active) and _touching(h["poses"], a, b):
                    if (a, b) not in bonds:
                        bonds.add((a, b))
                        additions.append((a, b))
                        changed = True
                    active |= _component(bonds, a)
                    active |= _component(bonds, b)
        if not changed:
            break
    h["bonds"] = sorted(bonds)
    return additions


def get_initial_state(level):
    if level not in LEVELS:
        raise ValueError("Level must be 0 through 6")
    h = {"level": level, "poses": deepcopy(LEVELS[level]["poses"]), "bonds": [],
         "history": [], "feedback": {"kind": "quiet", "cells": []}}
    _contacts(h, set(range(len(h["poses"]))))
    return h, {}


def _snapshot(h):
    return {"poses": deepcopy(h["poses"]), "bonds": deepcopy(h["bonds"]),
            "feedback": deepcopy(h["feedback"])}


def _accepted(before, after):
    after["history"] = (deepcopy(before["history"]) + [_snapshot(before)])[-128:]
    return after


def _translation(h, moving, dx, dy):
    poses = deepcopy(h["poses"])
    occupied = set().union(*[_cells(poses, i) for i in range(len(poses)) if i not in moving]) if len(moving) < len(poses) else set()
    walls = set(LEVELS[h["level"]]["walls"])
    blocked = set()
    for i in moving:
        x, y = poses[i]
        poses[i] = (x + dx, y + dy)
        for cx, cy in _cells(poses, i):
            if not (0 <= cx < WIDTH and 0 <= cy < HEIGHT) or (cx, cy) in walls or (cx, cy) in occupied:
                blocked.add((max(0, min(WIDTH - 1, cx)), max(0, min(HEIGHT - 1, cy))))
    return poses, sorted(blocked)


def transition(h_t, z_t, action):
    h = deepcopy(h_t)
    if action == 7:
        if h["history"]:
            previous = h["history"].pop()
            h.update(previous)
        return h
    if action in DIRECTIONS:
        dx, dy = DIRECTIONS[action]
        moving = _component(h["bonds"], 0)
        poses, blocked = _translation(h, moving, dx, dy)
        if blocked:
            h["feedback"] = {"kind": "blocked", "cells": blocked}
            return h
        h["poses"] = poses
        additions = _contacts(h, moving)
        h["feedback"] = {"kind": "contact" if additions else "quiet", "cells": []}
        return _accepted(h_t, h)
    if action != 5:
        return h
    moving = _component(h["bonds"], 0)
    bonds = {tuple(edge) for edge in h["bonds"]}
    cuts, captured, mouths, pulls = set(), set(), [], set()
    for x, y, dx, dy in LEVELS[h["level"]]["jaws"]:
        plate = next((i for i in moving if i != 0 and h["poses"][i] == (x, y)), None)
        if plate is None:
            continue
        neighbor = next((i for i in moving if i != plate and (x + dx, y + dy) in _cells(h["poses"], i)), None)
        if neighbor is None:
            continue
        edge = tuple(sorted((plate, neighbor)))
        if edge in bonds:
            cuts.add(edge)
            captured.add(plate)
            mouths.append((x, y))
            pulls.add((dx, dy))
    if not cuts:
        h["feedback"] = {"kind": "miss", "cells": [h["poses"][0]]}
        return h
    remaining = sorted(bonds - cuts)
    departing = _component(remaining, 0)
    if len(pulls) != 1 or captured & departing:
        h["feedback"] = {"kind": "blocked", "cells": mouths}
        return h
    dx, dy = next(iter(pulls))
    poses, blocked = _translation(h, departing, dx, dy)
    if blocked:
        h["feedback"] = {"kind": "blocked", "cells": blocked}
        return h
    h["bonds"], h["poses"] = remaining, poses
    _contacts(h, departing)
    h["feedback"] = {"kind": "scrape", "cells": mouths}
    return _accepted(h_t, h)


def _geometry_valid(h):
    occupied, walls = set(), set(LEVELS[h["level"]]["walls"])
    for i in range(len(h["poses"])):
        footprint = _cells(h["poses"], i)
        if footprint & (occupied | walls) or any(not (0 <= x < WIDTH and 0 <= y < HEIGHT) for x, y in footprint):
            return False
        occupied |= footprint
    return all(0 <= a < b < len(h["poses"]) and _touching(h["poses"], a, b) for a, b in h["bonds"])


def check_level_complete(h_t, z_t, level):
    if level != h_t["level"] or len(h_t["poses"]) != len(LEVELS[level]["poses"]) or not _geometry_valid(h_t):
        return False
    config = LEVELS[level]
    x0, y0, x1, y1 = config["receiver"]
    if not all(x0 <= x <= x1 and y0 <= y <= y1 for x, y in h_t["poses"][1:]):
        return False
    if config["goal"] == "arrival":
        return True
    return not h_t["bonds"] and h_t["poses"][0] == config["departure"]


def _rect(grid, x, y, width, height, color):
    for row in range(max(0, y), min(64, y + height)):
        for col in range(max(0, x), min(64, x + width)):
            grid[row][col] = color


def _pixel_cell(x, y):
    return ORIGIN_X + x * UNIT, ORIGIN_Y + y * UNIT


def render(h_t, z_t):
    grid = [[1 for _ in range(64)] for _ in range(64)]
    config = LEVELS[h_t["level"]]
    _rect(grid, ORIGIN_X - 1, ORIGIN_Y - 1, WIDTH * UNIT + 2, HEIGHT * UNIT + 2, 3)
    _rect(grid, ORIGIN_X, ORIGIN_Y, WIDTH * UNIT, HEIGHT * UNIT, 1)
    x0, y0, x1, y1 = config["receiver"]
    px, py = _pixel_cell(x0, y0)
    _rect(grid, px, py, (x1 - x0 + 1) * UNIT, (y1 - y0 + 1) * UNIT, 0)
    # The receiving region is an open continuous tray, never per-piece sockets.
    _rect(grid, px + (x1 - x0 + 1) * UNIT - 1, py, 1, (y1 - y0 + 1) * UNIT, 3)
    for x, y in config["walls"]:
        px, py = _pixel_cell(x, y)
        _rect(grid, px, py, UNIT, UNIT, 4)
    if config["departure"] is not None:
        px, py = _pixel_cell(*config["departure"])
        _rect(grid, px - 1, py - 1, 12, 1, 14)
        _rect(grid, px - 1, py + 10, 12, 1, 14)
        _rect(grid, px - 1, py, 1, 10, 14)
    for i, (x, y) in enumerate(h_t["poses"]):
        px, py = _pixel_cell(x, y)
        if i == 0:
            _rect(grid, px, py, 10, 10, 14)
            for cx, cy in [(px, py), (px + 9, py), (px, py + 9), (px + 9, py + 9)]:
                grid[cy][cx] = 1
            _rect(grid, px + 4, py + 4, 2, 2, 0)
        else:
            _rect(grid, px, py, UNIT, UNIT, 11)
    for a, b in h_t["bonds"]:
        for x, y in _cells(h_t["poses"], a):
            for bx, by in _cells(h_t["poses"], b):
                if abs(x - bx) + abs(y - by) != 1:
                    continue
                if y == by:
                    px, py = _pixel_cell(max(x, bx), y)
                    _rect(grid, px, py + 1, 1, 3, 7)
                else:
                    px, py = _pixel_cell(x, max(y, by))
                    _rect(grid, px + 1, py, 3, 1, 7)
    for x, y, dx, dy in config["jaws"]:
        px, py = _pixel_cell(x, y)
        # All present levels use left-open jaws; the stored pull direction is causal.
        _rect(grid, px - 1, py - 1, 7, 1, 5)
        _rect(grid, px - 1, py + 5, 7, 1, 5)
        _rect(grid, px + 5, py, 1, 5, 5)
        _rect(grid, px - 1, py, 1, 1, 5)
        _rect(grid, px - 1, py + 4, 1, 1, 5)
    feedback = h_t["feedback"]
    if feedback["kind"] == "scrape":
        for x, y in feedback["cells"]:
            px, py = _pixel_cell(x, y)
            _rect(grid, px - 1, py + 1, 1, 3, 0)
    elif feedback["kind"] == "blocked":
        for x, y in feedback["cells"]:
            px, py = _pixel_cell(x, y)
            _rect(grid, px + 1, py + 1, 3, 3, 8)
    elif feedback["kind"] == "miss":
        px, py = _pixel_cell(*h_t["poses"][0])
        _rect(grid, px + 4, py + 4, 2, 2, 3)
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


class V204(FunctionalGame):
    GAME_ID = 'v204-35c950ebf6c450f8'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
