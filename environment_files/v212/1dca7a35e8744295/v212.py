"""Repair Crew: current opportunities drive deterministic constructive workers.

The player changes material orientation/availability, never commands a worker or
places material into a goal. Space advances one meaningful pickup/install phase.
This is an abstract two-phase construction toy, not a realistic social model.
"""
from copy import deepcopy
from collections import deque

LEVELS = {
    0: {"floor": [[4, 6, 59, 59]],
        "slots": [{"x": 32, "y": 19, "axis": 0, "gap": 8, "bay": 12, "owner": 0, "bridge": False}],
        "workers": [[32, 29]],
        "parts": [{"x": 32, "y": 47, "length": 12, "axis": 0, "closed": True, "slot": None}]},
    1: {"floor": [[4, 6, 59, 59]],
        "slots": [{"x": 32, "y": 19, "axis": 0, "gap": 8, "bay": 12, "owner": 0, "bridge": False}],
        "workers": [[32, 29]],
        "parts": [{"x": 32, "y": 47, "length": 12, "axis": 1, "closed": False, "slot": None}]},
    2: {"floor": [[4, 6, 59, 59]],
        "slots": [{"x": 22, "y": 15, "axis": 0, "gap": 4, "bay": 8, "owner": 0, "bridge": False},
                  {"x": 22, "y": 27, "axis": 0, "gap": 8, "bay": 12, "owner": 0, "bridge": False}],
        "workers": [[22, 36]],
        "parts": [{"x": 10, "y": 48, "length": 8, "axis": 0, "closed": False, "slot": 0},
                  {"x": 31, "y": 43, "length": 8, "axis": 0, "closed": False, "slot": None},
                  {"x": 49, "y": 43, "length": 12, "axis": 1, "closed": False, "slot": None}]},
    3: {"floor": [[4, 6, 59, 59]],
        "slots": [{"x": 18, "y": 18, "axis": 0, "gap": 4, "bay": 12, "owner": 0, "bridge": False},
                  {"x": 46, "y": 20, "axis": 1, "gap": 8, "bay": 12, "owner": 1, "bridge": False}],
        "workers": [[18, 29], [54, 20]],
        "parts": [{"x": 27, "y": 41, "length": 12, "axis": 0, "closed": False, "slot": None},
                  {"x": 11, "y": 47, "length": 8, "axis": 0, "closed": True, "slot": None}]},
    4: {"floor": [[4, 8, 27, 58], [33, 8, 59, 58]],
        "slots": [{"x": 30, "y": 20, "axis": 0, "gap": 8, "bay": 12, "owner": 0, "bridge": True},
                  {"x": 14, "y": 40, "axis": 1, "gap": 8, "bay": 12, "owner": 1, "bridge": False}],
        "workers": [[18, 28], [20, 47]],
        "parts": [{"x": 12, "y": 14, "length": 12, "axis": 0, "closed": False, "slot": None},
                  {"x": 45, "y": 42, "length": 12, "axis": 0, "closed": True, "slot": None}]},
    5: {"floor": [[4, 6, 59, 59]],
        "slots": [{"x": 18, "y": 18, "axis": 0, "gap": 4, "bay": 12, "owner": 0, "bridge": False},
                  {"x": 46, "y": 18, "axis": 0, "gap": 8, "bay": 12, "owner": 1, "bridge": False}],
        "workers": [[18, 29], [46, 29]],
        "parts": [{"x": 11, "y": 47, "length": 8, "axis": 0, "closed": False, "slot": 0},
                  {"x": 27, "y": 41, "length": 12, "axis": 1, "closed": False, "slot": None}]},
    6: {"floor": [[4, 6, 59, 59]],
        "slots": [{"x": 18, "y": 18, "axis": 0, "gap": 4, "bay": 12, "owner": 0, "bridge": False},
                  {"x": 46, "y": 18, "axis": 0, "gap": 8, "bay": 12, "owner": 1, "bridge": False}],
        "workers": [[18, 29], [46, 29]],
        "parts": [{"x": 27, "y": 41, "length": 12, "axis": 0, "closed": False, "slot": 0},
                  {"x": 11, "y": 47, "length": 8, "axis": 1, "closed": True, "slot": None}]},
}


def get_initial_state(level):
    cfg = LEVELS[level]
    parts = []
    for source in cfg["parts"]:
        p = deepcopy(source)
        p["home"] = [p["x"], p["y"]]
        p["carrier"] = None
        if p["slot"] is not None:
            slot = cfg["slots"][p["slot"]]
            p["x"], p["y"], p["axis"], p["closed"] = slot["x"], slot["y"], slot["axis"], True
        parts.append(p)
    workers = [{"x": xy[0], "y": xy[1], "home": list(xy), "carry": None, "aim": None}
               for xy in cfg["workers"]]
    h = {"level": level, "parts": parts, "workers": workers, "feedback": None, "history": []}
    return h, {}


def get_available_actions():
    return [5, 6, 7]


def predict(h_t, seed=0):
    return {}


def part_box(p):
    n = p["length"]
    if p["axis"] == 0:
        return (p["x"] - n//2, p["y"] - 2, p["x"] + n//2 - 1, p["y"] + 2)
    return (p["x"] - 2, p["y"] - n//2, p["x"] + 2, p["y"] + n//2 - 1)


def grip_box(p):
    if p["axis"] == 0:
        gx, gy = p["x"] + p["length"]//2 - 2, p["y"]
        return gx-1, gy-3, gx+2, gy+3
    else:
        gx, gy = p["x"], p["y"] + p["length"]//2 - 2
        return gx-3, gy-1, gx+3, gy+2


def inside(box, x, y):
    return box[0] <= x <= box[2] and box[1] <= y <= box[3]


def fits(p, slot):
    # Two cells of supported overlap at each end; outer shoulders limit length.
    return p["axis"] == slot["axis"] and slot["gap"] + 4 <= p["length"] <= slot["bay"]


def connected_part(h, slot_index):
    slot = LEVELS[h["level"]]["slots"][slot_index]
    for i, p in enumerate(h["parts"]):
        if (p["slot"] == slot_index and p["carrier"] is None and p["closed"]
                and p["x"] == slot["x"] and p["y"] == slot["y"] and fits(p, slot)):
            return i
    return None


def complete_worker(h, worker_index):
    return all(connected_part(h, i) is not None
               for i, s in enumerate(LEVELS[h["level"]]["slots"]) if s["owner"] == worker_index)


def floor_cells(h):
    cfg = LEVELS[h["level"]]
    cells = set()
    for x1, y1, x2, y2 in cfg["floor"]:
        cells.update((x, y) for y in range(y1, y2+1) for x in range(x1, x2+1))
    for i, slot in enumerate(cfg["slots"]):
        p_index = connected_part(h, i)
        if slot["bridge"] and p_index is not None:
            x1, y1, x2, y2 = part_box(h["parts"][p_index])
            cells.update((x, y) for y in range(y1, y2+1) for x in range(x1, x2+1))
    return cells


def navigation(h):
    cells = floor_cells(h)
    # Every point in the full 5x5 feet footprint must be supported. Unit lattice.
    return {(x, y) for x, y in cells
            if all((x+dx, y+dy) in cells for dy in range(-2, 3) for dx in range(-2, 3))}


def distances(start, valid):
    if tuple(start) not in valid:
        return {}
    result = {tuple(start): 0}
    queue = deque([tuple(start)])
    while queue:
        x, y = queue.popleft()
        for p in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
            if p in valid and p not in result:
                result[p] = result[(x, y)] + 1
                queue.append(p)
    return result


def pickup_point(p):
    return p["x"], p["y"] + 7


def options(h):
    cfg = LEVELS[h["level"]]
    valid = navigation(h)
    choices = []
    for wi, worker in enumerate(h["workers"]):
        if worker["carry"] is not None or complete_worker(h, wi):
            continue
        reach = distances((worker["x"], worker["y"]), valid)
        for pi, part in enumerate(h["parts"]):
            if part["closed"] or part["slot"] is not None or part["carrier"] is not None:
                continue
            point = pickup_point(part)
            if point not in reach:
                continue
            for si, slot in enumerate(cfg["slots"]):
                if slot["owner"] == wi and connected_part(h, si) is None and fits(part, slot):
                    choices.append((reach[point], worker["x"], worker["y"], part["x"], part["y"], wi, pi, si))
    return sorted(choices)


def rotate_clear(h, pi):
    p = h["parts"][pi]
    r = p["length"]//2 + 2
    swept = (p["x"]-r, p["y"]-r, p["x"]+r, p["y"]+r)
    if min(swept) < 2 or max(swept) > 61:
        return False
    for qi, q in enumerate(h["parts"]):
        if qi != pi and q["carrier"] is None:
            box = part_box(q)
            if not (swept[2] < box[0] or box[2] < swept[0] or swept[3] < box[1] or box[3] < swept[1]):
                return False
    return True


def saved_scene(h):
    return {key: deepcopy(value) for key, value in h.items() if key != "history"}


def transition(h_t, z_t, action):
    h = deepcopy(h_t)
    number = action[0] if isinstance(action, (tuple, list)) else action
    if number == 7:
        if h["history"]:
            old = h["history"].pop()
            return {**old, "history": h["history"]}
        return h
    before = saved_scene(h)
    h["feedback"] = None
    changed = False
    if number == 6:
        _, x, y = action
        for pi in reversed(range(len(h["parts"]))):
            p = h["parts"][pi]
            if not inside(grip_box(p), x, y) and not inside(part_box(p), x, y):
                continue
            if p["carrier"] is not None:
                h["feedback"] = [p["x"], p["y"], "held"]
            elif inside(grip_box(p), x, y):
                if p["slot"] is not None:
                    p["slot"] = None
                    p["x"], p["y"] = p["home"]
                    p["closed"] = False
                else:
                    p["closed"] = not p["closed"]
                changed = True
            elif p["slot"] is not None:
                h["feedback"] = [p["x"], p["y"], "pinned"]
            elif rotate_clear(h, pi):
                p["axis"] = 1 - p["axis"]
                changed = True
            else:
                h["feedback"] = [p["x"], p["y"], "blocked"]
            break
        else:
            h["feedback"] = [x, y, "miss"]
    elif number == 5:
        carrying = []
        valid = navigation(h)
        for wi, w in enumerate(h["workers"]):
            if w["carry"] is not None:
                reach = distances((w["x"], w["y"]), valid)
                destination = tuple(w["home"])
                if destination in reach:
                    carrying.append((reach[destination], w["x"], w["y"], wi))
        if carrying:
            wi = sorted(carrying)[0][-1]
            w = h["workers"][wi]
            p = h["parts"][w["carry"]]
            si = w["aim"]
            slot = LEVELS[h["level"]]["slots"][si]
            # The material pose is unchanged while held. Installation establishes
            # actual current pinned endpoint relations, not a serviced-job flag.
            if connected_part(h, si) is None and fits(p, slot):
                p["x"], p["y"], p["slot"] = slot["x"], slot["y"], si
                p["closed"], p["carrier"] = True, None
                w["x"], w["y"] = w["home"]
                w["carry"], w["aim"] = None, None
                changed = True
        else:
            choices = options(h)
            if choices:
                _, _, _, _, _, wi, pi, si = choices[0]
                w, p = h["workers"][wi], h["parts"][pi]
                w["x"], w["y"] = pickup_point(p)
                w["carry"], w["aim"], p["carrier"] = pi, si, wi
                changed = True
            else:
                for w in h["workers"]:
                    if not complete_worker(h, h["workers"].index(w)):
                        h["feedback"] = [w["x"], w["y"]-6, "no_usable_material"]
                        break
    if changed or h["feedback"] != before["feedback"]:
        h["history"].append(before)
    return h


def check_level_complete(h_t, z_t, level):
    return h_t["level"] == level and all(connected_part(h_t, i) is not None
                                        for i in range(len(LEVELS[level]["slots"])))


def render(h_t, z_t):
    h = h_t
    cfg = LEVELS[h["level"]]
    frame = [[0 for _ in range(64)] for _ in range(64)]

    def rect(x1, y1, x2, y2, color):
        for y in range(max(0, y1), min(63, y2)+1):
            for x in range(max(0, x1), min(63, x2)+1):
                frame[y][x] = color

    def line(x1, y1, x2, y2, color, width=1):
        if x1 == x2:
            rect(x1-width//2, min(y1, y2), x1+width//2, max(y1, y2), color)
        else:
            rect(min(x1, x2), y1-width//2, max(x1, x2), y1+width//2, color)

    for floor in cfg["floor"]:
        rect(*floor, 1)
    for i, s in enumerate(cfg["slots"]):
        x, y, gap, bay = s["x"], s["y"], s["gap"], s["bay"]
        if s["axis"] == 0:
            rect(x-bay//2-3, y-2, x-gap//2-1, y+2, 3)
            rect(x+gap//2, y-2, x+bay//2+2, y+2, 3)
            # Broad shoulders show the maximum usable length; stems form an
            # interrupted coherent structure, not a detached target board.
            rect(x-bay//2-2, y-4, x-bay//2-1, y+8, 3)
            rect(x+bay//2, y-4, x+bay//2+1, y+8, 3)
            if s["bridge"]:
                rect(x-bay//2-2, y+5, x-bay//2-1, y+8, 1)
                rect(x+bay//2, y+5, x+bay//2+1, y+8, 1)
        else:
            rect(x-2, y-bay//2-3, x+2, y-gap//2-1, 3)
            rect(x-2, y+gap//2, x+2, y+bay//2+2, 3)
            rect(x-4, y-bay//2-2, x+8, y-bay//2-1, 3)
            rect(x-4, y+bay//2, x+8, y+bay//2+1, 3)
    for p in h["parts"]:
        # A persistent small pivot marks the staging location after movement.
        hx, hy = p["home"]
        rect(hx-1, hy-1, hx+1, hy+1, 2)
    for wi, w in enumerate(h["workers"]):
        x, y = w["x"], w["y"]
        rect(x-2, y-6, x+2, y-3, 11)
        rect(x-3, y-2, x+3, y, 11)
        # Ground feet lie within the authoritative 5x5 navigation footprint;
        # raised shoulders/arms and carried material may overhang its boundary.
        rect(x-2, y+1, x-1, y+2, 3)
        rect(x+1, y+1, x+2, y+2, 3)
        if w["carry"] is None:
            if not complete_worker(h, wi):
                # Raised hands near its actual incomplete structure.
                aim = next(s for si, s in enumerate(cfg["slots"])
                           if s["owner"] == wi and connected_part(h, si) is None)
                dx, dy = aim["x"]-x, aim["y"]-y
                if abs(dy) >= abs(dx):
                    rect(x-4, y-5, x-3, y-1, 11)
                    rect(x+3, y-5, x+4, y-1, 11)
                elif dx > 0:
                    rect(x+3, y-4, x+6, y-1, 11)
                    rect(x-4, y, x-3, y+2, 11)
                else:
                    rect(x-6, y-2, x-3, y+1, 11)
                    rect(x+3, y, x+4, y+2, 11)
            else:
                rect(x-4, y, x-3, y+2, 11)
                rect(x+3, y, x+4, y+2, 11)
    for p in h["parts"]:
        rect(*part_box(p), 14)
        bx = grip_box(p)
        if p["carrier"] is not None:
            rect(bx[0], bx[1], bx[2], bx[3], 14)
            # Broad white hands visibly grasp the persistent blue material.
            rect(p["x"]-4, p["y"]+2, p["x"]-2, p["y"]+4, 0)
            rect(p["x"]+2, p["y"]+2, p["x"]+4, p["y"]+4, 0)
        elif p["closed"]:
            rect(*bx, 4)
            rect(bx[0]+1, bx[1]+1, bx[2]-1, bx[3]-1, 0)
        else:
            # Open jaws, same broad actual click box; no detached switch.
            rect(bx[0], bx[1], bx[0], bx[3], 4)
            rect(bx[2], bx[1], bx[2], bx[3], 4)
            rect(bx[0], bx[3], bx[2], bx[3], 4)
    if h["feedback"]:
        x, y, kind = h["feedback"]
        if kind == "miss":
            rect(x-1, y-1, x+1, y+1, 2)
        else:
            # Local broad contrasting contact response, no remote error HUD.
            rect(x-3, y-3, x+3, y-2, 8)
    return frame


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


class V212(FunctionalGame):
    GAME_ID = 'v212-1dca7a35e8744295'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
