"""Shadow Casting: original seven-level finite point-source section.

The optical section consists only of zero-thickness opaque vertical intervals.
Material mounts have disjoint depth bounds, preserving order through all moves.
Grips and mounting hardware are diagrammatic, nonoccluding fixtures. Straight
rays from a zero-extent point source produce binary shadows, not full 3D optics.
Native rows sample exact rational half-open intervals at their pixel centers.
"""
from copy import deepcopy
from fractions import Fraction

SOURCE_X = 6
DISTANCE = 48
RECEIVER_X = 54
RECEIVER_LO = 2
RECEIVER_HI = 62

LEVELS = {
    0: {"active_tags": ["point_source", "lateral"], "source": 32,
        "source_range": [32, 32], "selected": 0, "target": [[26, 38]],
        "masks": [{"d": 24, "c": 28, "h": 6, "depth": [24, 24], "lateral": [28, 36]}]},
    1: {"active_tags": ["point_source", "depth_scale"], "source": 32,
        "source_range": [32, 32], "selected": 0, "target": [[20, 44]],
        "masks": [{"d": 32, "c": 32, "h": 8, "depth": [16, 40], "lateral": [32, 32]}]},
    2: {"active_tags": ["point_source", "source_motion", "fixed_mount"], "source": 28,
        "source_range": [28, 36], "selected": -1, "target": [[20, 36]],
        "masks": [{"d": 24, "c": 32, "h": 8, "depth": [24, 24], "lateral": [32, 32]}]},
    3: {"active_tags": ["lateral", "depth_scale", "boolean_union"], "source": 32,
        "source_range": [32, 32], "selected": 0, "target": [[16, 38]],
        "masks": [{"d": 24, "c": 26, "h": 8, "depth": [24, 24], "lateral": [26, 38]},
                  {"d": 32, "c": 40, "h": 8, "depth": [32, 32], "lateral": [28, 40]}]},
    4: {"active_tags": ["lateral", "depth_scale", "off_axis"], "source": 28,
        "source_range": [28, 28], "selected": 0, "target": [[36, 52]],
        "masks": [{"d": 40, "c": 30, "h": 8, "depth": [24, 40], "lateral": [28, 36]}]},
    5: {"active_tags": ["source_motion", "fixed_mount", "unequal_depth", "boolean_union"], "source": 32,
        "source_range": [24, 36], "source_step": 4, "selected": -1, "target": [[14, 26], [40, 52]],
        "masks": [{"d": 24, "c": 24, "h": 6, "depth": [24, 24], "lateral": [24, 24]},
                  {"d": 32, "c": 36, "h": 8, "depth": [32, 32], "lateral": [32, 44], "lateral_step": 4}]},
    6: {"active_tags": ["source_motion", "fixed_mount", "depth_scale", "boolean_union", "band_decomposition"], "source": 34,
        "source_range": [26, 34], "source_step": 4, "selected": -1, "target": [[12, 30], [36, 54]],
        "masks": [{"d": 24, "c": 24, "h": 6, "depth": [24, 24], "lateral": [24, 24]},
                  {"d": 20, "c": 32, "h": 4, "depth": [12, 20], "lateral": [28, 32], "lateral_step": 4},
                  {"d": 40, "c": 36, "h": 12, "depth": [32, 40], "lateral": [36, 44], "lateral_step": 4}]},
}


def projected_interval(source, d, c, height, x=RECEIVER_X):
    """Exact boundary rays evaluated at a plane x >= the thin material."""
    ratio = Fraction(x - SOURCE_X, d)
    center = source + ratio * (c - source)
    half = ratio * Fraction(height, 2)
    return center - half, center + half


def sampled_rows(intervals):
    """One authoritative pixel-center, lower-inclusive/upper-exclusive rule."""
    return tuple(any(lo <= Fraction(2 * y + 1, 2) < hi for lo, hi in intervals)
                 for y in range(64))


def current_intervals(h_t):
    level = LEVELS[h_t["level"]]
    return [projected_interval(h_t["source"], pose[0], pose[1], spec["h"])
            for pose, spec in zip(h_t["poses"], level["masks"])]


def current_rows(h_t):
    return sampled_rows(current_intervals(h_t))


def target_rows(level_index):
    return sampled_rows(LEVELS[level_index]["target"])


def get_initial_state(level):
    spec = LEVELS[level]
    return {"level": level, "source": spec["source"],
            "poses": [[m["d"], m["c"]] for m in spec["masks"]],
            "selected": spec["selected"], "feedback": [0, 0, 0], "history": []}, {}


def get_available_actions():
    return [1, 2, 3, 4, 6, 7]


def predict(h_t, seed=0):
    return {}


def movable_mask(spec):
    return spec["depth"][0] != spec["depth"][1] or spec["lateral"][0] != spec["lateral"][1]


def grip_centers(h_t):
    level = LEVELS[h_t["level"]]
    grips = []
    if level["source_range"][0] != level["source_range"][1]:
        grips.append((-1, SOURCE_X, h_t["source"]))
    for index, (pose, spec) in enumerate(zip(h_t["poses"], level["masks"])):
        if movable_mask(spec):
            grips.append((index, SOURCE_X + pose[0] - 4, pose[1]))
    return grips


def snapshot(h_t):
    return {key: deepcopy(value) for key, value in h_t.items() if key != "history"}


def transition(h_t, z_t, a_t):
    state = deepcopy(h_t)
    number = a_t[0] if isinstance(a_t, (tuple, list)) else a_t
    if number == 7:
        if state["history"]:
            history = state["history"]
            state = history[-1]
            state["history"] = history[:-1]
        return state
    state["history"].append(snapshot(h_t))
    state["feedback"] = [0, 0, 0]
    level = LEVELS[state["level"]]
    if number == 6:
        x, y = a_t[1], a_t[2]
        for index, gx, gy in grip_centers(state):
            if gx - 2 <= x <= gx + 2 and gy - 2 <= y <= gy + 2:
                state["selected"] = index
                state["feedback"] = [1, gx, gy]
                return state
        state["feedback"] = [3, x, y]
        return state
    selected = state["selected"]
    gx, gy = next((gx, gy) for i, gx, gy in grip_centers(state) if i == selected)
    moved = False
    if selected == -1:
        step = level.get("source_step", 2)
        delta = -step if number == 1 else step if number == 2 else 0
        proposed = state["source"] + delta
        if delta and level["source_range"][0] <= proposed <= level["source_range"][1]:
            state["source"] = proposed
            moved = True
    else:
        pose = state["poses"][selected]
        spec = level["masks"][selected]
        axis = 1 if number in (1, 2) else 0
        vertical = spec.get("lateral_step", 2)
        delta = {1: -vertical, 2: vertical, 3: -8, 4: 8}.get(number, 0)
        bounds = spec["lateral"] if axis == 1 else spec["depth"]
        proposed = pose[axis] + delta
        if delta and bounds[0] <= proposed <= bounds[1]:
            pose[axis] = proposed
            moved = True
    if not moved:
        state["feedback"] = [2, gx, gy]
    return state


def check_level_complete(h_t, z_t, level):
    return current_rows(h_t) == target_rows(level)


def paint_rect(frame, x0, y0, x1, y1, color):
    for y in range(max(0, y0), min(64, y1)):
        for x in range(max(0, x0), min(64, x1)):
            frame[y][x] = color


def paint_grip(frame, x, y, selected, blocked):
    if selected:
        paint_rect(frame, x - 3, y - 3, x + 4, y + 4, 8 if blocked else 14)
    paint_rect(frame, x - 2, y - 2, x + 3, y + 3, 5)
    paint_rect(frame, x - 1, y - 1, x + 2, y + 2, 0)


def render(h_t, z_t):
    frame = [[0] * 64 for _ in range(64)]
    level = LEVELS[h_t["level"]]
    source = h_t["source"]
    # Continuous illuminated section, with exact opaque wedges behind material.
    for x in range(SOURCE_X, RECEIVER_X):
        ratio = Fraction(x - SOURCE_X, DISTANCE)
        lit = (source + ratio * (RECEIVER_LO - source),
               source + ratio * (RECEIVER_HI - source))
        shadows = [projected_interval(source, d, c, spec["h"], x)
                   for (d, c), spec in zip(h_t["poses"], level["masks"])
                   if x >= SOURCE_X + d]
        for y, present in enumerate(sampled_rows([lit])):
            if present:
                frame[y][x] = 1
        for y, dark in enumerate(sampled_rows(shadows)):
            if dark:
                frame[y][x] = 3
    # The selected current boundary rays aid causal comparison, never a solution.
    selected = h_t["selected"]
    if selected >= 0:
        d, c = h_t["poses"][selected]
        height = level["masks"][selected]["h"]
        for x in range(SOURCE_X + 3, RECEIVER_X - 1):
            for edge in projected_interval(source, d, c, height, x):
                y = int(edge + Fraction(1, 2))
                if 0 <= y < 64:
                    frame[y][x] = 10
    # Passive receiver and desired bands are adjacent on the same ordinate.
    occupied = current_rows(h_t)
    wanted = target_rows(h_t["level"])
    for y in range(RECEIVER_LO, RECEIVER_HI):
        paint_rect(frame, 53, y, 57, y + 1, 5 if occupied[y] else 10)
        paint_rect(frame, 59, y, 62, y + 1, 7 if wanted[y] else 1)
    paint_rect(frame, 52, 1, 57, 2, 4)
    paint_rect(frame, 52, 62, 57, 63, 4)
    # Source: fixed radiant material differs from the movable black/white grip.
    lo, hi = level["source_range"]
    if lo != hi:
        paint_rect(frame, 6, lo - 3, 7, hi + 4, 2)
        paint_rect(frame, 3, lo - 3, 10, lo - 2, 4)
        paint_rect(frame, 3, hi + 3, 10, hi + 4, 4)
        paint_rect(frame, 8, source - 1, 11, source + 2, 10)
    else:
        paint_rect(frame, 4, source - 2, 9, source + 3, 10)
        paint_rect(frame, 3, source - 1, 10, source + 2, 10)
        paint_rect(frame, 1, source - 1, 3, source + 2, 4)
    # Each finite mounting guide is attached to its actual material pose.
    for index, ((d, c), spec) in enumerate(zip(h_t["poses"], level["masks"])):
        x = SOURCE_X + d
        gx = x - 4
        if movable_mask(spec):
            clo, chi = spec["lateral"]
            dlo, dhi = spec["depth"]
            if clo != chi:
                paint_rect(frame, gx, clo - 3, gx + 1, chi + 4, 2)
                paint_rect(frame, gx - 3, clo - 3, gx + 4, clo - 2, 4)
                paint_rect(frame, gx - 3, chi + 3, gx + 4, chi + 4, 4)
            if dlo != dhi:
                rail_y = c + spec["h"] // 2 + 4
                paint_rect(frame, SOURCE_X + dlo - 4, rail_y,
                           SOURCE_X + dhi - 3, rail_y + 1, 2)
                for stop in (SOURCE_X + dlo - 4, SOURCE_X + dhi - 4):
                    paint_rect(frame, stop, rail_y - 2, stop + 1, rail_y + 3, 4)
                paint_rect(frame, gx, c + 2, gx + 1, rail_y, 2)
            paint_rect(frame, gx + 2, c, x, c + 1, 4)
        else:
            paint_rect(frame, x + 2, c - 1, x + 6, c + 2, 4)
            paint_rect(frame, x + 5, c - 4, x + 7, c + 5, 2)
        half = spec["h"] // 2
        paint_rect(frame, x - 1, c - half, x + 2, c + half, 5)
    for index, gx, gy in grip_centers(h_t):
        blocked = h_t["feedback"][0] == 2 and index == h_t["selected"]
        paint_grip(frame, gx, gy, index == selected, blocked)
    if h_t["feedback"][0] == 3:
        _, x, y = h_t["feedback"]
        paint_rect(frame, x - 1, y, x + 2, y + 1, 8)
        paint_rect(frame, x, y - 1, x + 1, y + 2, 8)
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


class V209(FunctionalGame):
    GAME_ID = 'v209-e5d0d0141696c8b8'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
