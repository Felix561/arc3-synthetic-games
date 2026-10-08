"""Contact Cancellation: deterministic unranked material and temporary seams."""
from copy import deepcopy
import numpy as np

# id, left, top, width, height, exposed keyed face, contour family
LEVELS = {
    0: {"size": (6, 6), "units": [(0, 0, 2, 1, 2, "R", 0), (1, 3, 2, 1, 2, "L", 0)], "walls": []},
    1: {"size": (6, 6), "units": [(0, 2, 2, 1, 2, "R", 0), (1, 5, 2, 1, 2, "L", 0)], "walls": []},
    2: {"size": (6, 6), "units": [(0, 0, 2, 1, 2, "R", 0), (1, 2, 0, 1, 2, "L", 0), (2, 4, 3, 2, 1, "D", 1), (3, 2, 4, 2, 1, "U", 1)], "walls": []},
    3: {"size": (6, 6), "units": [(0, 0, 4, 1, 2, "R", 0), (1, 3, 1, 1, 2, "L", 0), (2, 0, 2, 2, 1, "D", 1), (3, 4, 0, 2, 1, "U", 1)], "walls": []},
    4: {"size": (6, 6), "units": [(0, 0, 4, 1, 2, "R", 0), (1, 2, 4, 1, 2, "L", 0), (2, 0, 2, 2, 1, "D", 1), (3, 4, 0, 2, 1, "U", 1)], "walls": []},
    5: {"size": (6, 6), "units": [(0, 0, 4, 1, 2, "R", 0), (1, 3, 4, 1, 2, "L", 0), (2, 0, 2, 2, 1, "D", 1), (3, 4, 0, 2, 1, "U", 1), (4, 3, 0, 1, 2, "R", 1), (5, 4, 2, 1, 2, "L", 1)], "walls": []},
    6: {"size": (6, 6), "units": [(0, 0, 4, 1, 2, "R", 0), (1, 3, 4, 1, 2, "L", 0), (2, 0, 2, 2, 1, "D", 1), (3, 4, 0, 2, 1, "U", 1), (4, 3, 0, 1, 2, "D", 0), (5, 4, 2, 1, 2, "U", 0)], "walls": []},
}
DIRS = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}
OPPOSITE = {"L": "R", "R": "L", "U": "D", "D": "U"}


def get_available_actions():
    return [1, 2, 3, 4, 5, 7]


def get_initial_state(level_index):
    spec = LEVELS[int(level_index)]
    units = {u[0]: {"x": u[1], "y": u[2], "w": u[3], "h": u[4], "face": u[5], "contour": u[6]} for u in spec["units"]}
    return {"level": int(level_index), "size": spec["size"], "units": units, "original_ids": tuple(sorted(units)), "bonds": [], "released": [], "walls": list(spec["walls"]), "history": [], "event": None}, {}


def predict(h_t, seed):
    return {}


def _cells(u, dx=0, dy=0):
    return {(x + dx, y + dy) for x in range(u["x"], u["x"] + u["w"]) for y in range(u["y"], u["y"] + u["h"])}


def _contact(a, b):
    if a["x"] + a["w"] == b["x"] and max(a["y"], b["y"]) < min(a["y"] + a["h"], b["y"] + b["h"]):
        return "R"
    if b["x"] + b["w"] == a["x"] and max(a["y"], b["y"]) < min(a["y"] + a["h"], b["y"] + b["h"]):
        return "L"
    if a["y"] + a["h"] == b["y"] and max(a["x"], b["x"]) < min(a["x"] + a["w"], b["x"] + b["w"]):
        return "D"
    if b["y"] + b["h"] == a["y"] and max(a["x"], b["x"]) < min(a["x"] + a["w"], b["x"] + b["w"]):
        return "U"
    return None


def _complement(a, b, side):
    if side is None or a["face"] != side or b["face"] != OPPOSITE[side] or a["contour"] != b["contour"]:
        return False
    return (a["y"], a["h"]) == (b["y"], b["h"]) if side in ("L", "R") else (a["x"], a["w"]) == (b["x"], b["w"])


def _groups(h):
    units = h["units"]
    unseen = set(units)
    groups = []
    while unseen:
        component = {min(unseen)}
        changed = True
        while changed:
            changed = False
            for a, b in h["bonds"]:
                if a in units and b in units and (a in component or b in component) and not {a, b} <= component:
                    component.update((a, b))
                    changed = True
        unseen.difference_update(component)
        groups.append(component)
    return groups


def _snapshot(h):
    return {k: deepcopy(v) for k, v in h.items() if k != "history"}


def _step(h, action):
    """Resolve the maximal simultaneously movable set, then new face contacts."""
    dx, dy = DIRS[action]
    units = h["units"]
    groups = _groups(h)
    owner = {uid: i for i, group in enumerate(groups) for uid in group}
    occupied = [set().union(*(_cells(units[uid]) for uid in group)) for group in groups]
    proposed = [{(x + dx, y + dy) for x, y in cells} for cells in occupied]
    width, height = h["size"]
    walls = set(h["walls"])
    moving = {i for i, cells in enumerate(proposed) if not cells & walls and all(0 <= x < width and 0 <= y < height for x, y in cells)}
    changed = True
    while changed:
        remove = {i for i in moving if any(proposed[i] & occupied[j] for j in range(len(groups)) if j != i and j not in moving)}
        changed = bool(remove)
        moving.difference_update(remove)
    # Contacts form at the actual approached endpoint, without a confirmation.
    # A released abutment cannot attach until it separates and approaches anew.
    previous_contacts = {}
    previous_matches = {}
    ids = sorted(units)
    released = {tuple(p) for p in h["released"]}
    for pos, a in enumerate(ids):
        for b in ids[pos + 1:]:
            previous_contacts[(a, b)] = _contact(units[a], units[b])
            previous_matches[(a, b)] = _complement(units[a], units[b], previous_contacts[(a, b)])
    for uid, unit in units.items():
        if owner[uid] in moving:
            unit["x"] += dx
            unit["y"] += dy
    pressed = []
    for pos, a in enumerate(ids):
        for b in ids[pos + 1:]:
            side = _contact(units[a], units[b])
            new_seam = (a, b) not in released and previous_contacts[(a, b)] != side
            new_match = _complement(units[a], units[b], side) and not previous_matches[(a, b)]
            if owner[a] != owner[b] and side is not None and (new_seam or new_match):
                pressed.append((a, b, side))
    canceled = set()
    for a, b, side in pressed:
        if _complement(units[a], units[b], side):
            canceled.update((a, b))
    new_bonds = {tuple(p) for p in h["bonds"] if not set(p) & canceled}
    for a, b, side in pressed:
        if a not in canceled and b not in canceled:
            new_bonds.add((a, b))
    for uid in canceled:
        del units[uid]
    h["bonds"] = sorted(new_bonds)
    h["released"] = sorted(p for p in released if p[0] in units and p[1] in units and _contact(units[p[0]], units[p[1]]) is not None)
    h["event"] = {"kind": "cancel" if canceled else "join" if pressed else "move", "removed": sorted(canceled)}
    return h


def transition(h_t, z_t, action):
    action = int(action[0] if isinstance(action, (tuple, list)) else action)
    h = deepcopy(h_t)
    if action == 7:
        if h["history"]:
            past = h["history"].pop()
            history = h["history"]
            h = past
            h["history"] = history
        return h
    if action not in DIRS and action != 5:
        return h
    before = _snapshot(h)
    if action == 5:
        h["released"] = sorted({tuple(p) for p in h["released"] + h["bonds"]})
        h["bonds"] = []
        h["event"] = {"kind": "release", "removed": []}
    else:
        h = _step(h, action)
    if _snapshot(h) != before:
        h["history"].append(before)
    return h


def check_level_complete(h_t, z_t, level_index):
    return not (set(h_t["original_ids"]) & set(h_t["units"]))


def render(h_t, z_t):
    image = np.full((64, 64), 5, dtype=np.int8)
    # A broad undecorated square field. The only fixed material is its rim.
    image[6:58, 6:58] = 4
    image[8:56, 8:56] = 5
    for x, y in h_t["walls"]:
        image[8 + 8*y:16 + 8*y, 8 + 8*x:16 + 8*x] = 4
    units = h_t["units"]
    colors = {"R": 12, "L": 12, "D": 9, "U": 9}
    for uid in sorted(units):
        u = units[uid]
        x, y, w, height = 8 + 8*u["x"], 8 + 8*u["y"], 8*u["w"], 8*u["h"]
        image[y:y+height, x:x+w] = 0
        image[y+1:y+height-1, x+1:x+w-1] = colors[u["face"]]
        # Broad face-local complementary outline, never a ranked/color code.
        length = height if u["face"] in ("R", "L") else w
        for offset in range(2, length-2):
            depth = 1 + (2 if (offset < length//2) == (u["face"] in ("R", "D")) else 0)
            if u["contour"] == 1:
                depth = 1 + (2 if (offset//3) % 2 == (u["face"] in ("R", "D")) else 0)
            if u["face"] == "R":
                image[y+offset, x+w-1-depth:x+w] = 0
            elif u["face"] == "L":
                image[y+offset, x:x+depth+1] = 0
            elif u["face"] == "D":
                image[y+height-1-depth:y+height, x+offset] = 0
            else:
                image[y:y+depth+1, x+offset] = 0
    # Joins are short solid bars across an otherwise countable two-pixel seam.
    # Released seams retain the dark outline and gain a bright local split cue.
    for pairs, color in ((h_t["bonds"], 4), (h_t["released"], 1)):
        for a, b in pairs:
            if a not in units or b not in units:
                continue
            u, v = units[a], units[b]
            side = _contact(u, v)
            if side in ("L", "R"):
                edge = u["x"] + (u["w"] if side == "R" else 0)
                cy = 8 + 8*max(u["y"], v["y"]) + 4
                cx = 8 + 8*edge
                image[cy-1:cy+2, cx-1:cx+1] = color
            elif side in ("U", "D"):
                edge = u["y"] + (u["h"] if side == "D" else 0)
                cx = 8 + 8*max(u["x"], v["x"]) + 4
                cy = 8 + 8*edge
                image[cy-1:cy+1, cx-1:cx+2] = color
    return image


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


class V220(FunctionalGame):
    GAME_ID = 'v220-357dafa509cf0402'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
