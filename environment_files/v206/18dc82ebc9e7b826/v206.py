"""Original local-field game. Execute only in the secured native runtime."""
from copy import deepcopy

# Literal level constants; all centers lie on the same 8-pixel movement lattice.
# Field triples are x, y, age. L2 alone has disclosed initial field; later fields start empty.
LEVELS = {
    0: {"emitter": (24, 20), "creature": (24, 28), "goal": (32, 28), "on": True,
        "walls": (), "field": ()},
    1: {"emitter": (24, 20), "creature": (16, 28), "goal": (32, 28), "on": False,
        "walls": (), "field": ((24, 28, 3), (32, 28, 0))},
    2: {"emitter": (16, 20), "creature": (16, 36), "goal": (24, 44), "on": True,
        "walls": ((28, 32, 30, 40), (20, 40, 22, 42), (27, 40, 30, 42)), "field": ()},
    3: {"emitter": (24, 28), "creature": (24, 44), "goal": (40, 36), "on": True,
        "walls": ((12, 32, 21, 34), (28, 32, 30, 34), (35, 32, 38, 34),
                  (43, 32, 46, 34), (28, 24, 46, 25), (44, 24, 46, 40)), "field": ()},
    4: {"emitter": (8, 20), "creature": (16, 28), "goal": (32, 44), "on": True,
        "walls": ((36, 28, 38, 40), (28, 40, 30, 42), (35, 40, 38, 42)), "field": ()},
    5: {"emitter": (24, 12), "creature": (24, 28), "goal": (24, 36), "on": True,
        "walls": ((20, 24, 21, 34), (20, 32, 22, 34), (27, 32, 30, 34)), "field": ()},
    6: {"emitter": (8, 20), "creature": (16, 28), "goal": (40, 44), "on": True,
        "walls": ((20, 32, 22, 34), (27, 32, 30, 34), (35, 32, 37, 34),
                  (44, 32, 46, 34), (44, 28, 46, 40), (36, 40, 38, 42),
                  (43, 40, 46, 42)), "field": ()},
}

MOVES = {1: (0, -8), 2: (0, 8), 3: (-8, 0), 4: (8, 0)}


def tier(age):
    """This exact quantized value drives both render and creature policy."""
    if age is None or age >= 9:
        return 0
    if age <= 2:
        return 3
    return 2 if age <= 5 else 1


def walls(level):
    # Each rectangle is the actual drawn solid; access is solely full footprint.
    return [(3, 7, 61, 9), (3, 55, 61, 57), (3, 9, 5, 55), (59, 9, 61, 55)] + list(LEVELS[level]["walls"])


def body_clear(level, position, radius):
    x, y = position
    for x0, y0, x1, y1 in walls(level):
        if x - radius < x1 and x + radius >= x0 and y - radius < y1 and y + radius >= y0:
            return False
    return 5 <= x - radius and x + radius < 59 and 9 <= y - radius and y + radius < 55


def overlap(a, ar, b, br):
    return abs(a[0] - b[0]) <= ar + br and abs(a[1] - b[1]) <= ar + br


def swept_clear(h, start, end, radius, other, other_radius):
    dx, dy = end[0] - start[0], end[1] - start[1]
    for k in range(1, 9):
        pose = (start[0] + dx * k // 8, start[1] + dy * k // 8)
        if not body_clear(h["level"], pose, radius) or overlap(pose, radius, other, other_radius):
            return False
    return True


def nozzle_site(h):
    """One real downward nozzle, exactly one lattice step, never a remote selector."""
    x, y = h["emitter"]
    target = (x, y + 8)
    if not body_clear(h["level"], target, 2):
        return None
    for yy in range(y + 4, y + 9):
        for xx in range(x - 1, x + 2):
            if any(a <= xx < c and b <= yy < d for a, b, c, d in walls(h["level"])):
                return None
    return target


def get_initial_state(level):
    config = LEVELS[level]
    h = {"level": level, "emitter": config["emitter"], "creature": config["creature"],
         "on": config["on"], "field": {(x, y): age for x, y, age in config["field"]},
         "translations": 0, "feedback": None, "history": []}
    return h, predict(h, 0)


def core(h):
    return {key: deepcopy(value) for key, value in h.items() if key != "history"}


def local_response(h):
    current = tier(h["field"].get(h["creature"]))
    candidates = []
    cx, cy = h["creature"]
    for dx, dy in MOVES.values():
        pose = (cx + dx, cy + dy)
        if swept_clear(h, h["creature"], pose, 2, h["emitter"], 3):
            candidates.append((tier(h["field"].get(pose)), pose))
    strongest = max((value for value, pose in candidates), default=0)
    best = [pose for value, pose in candidates if value == strongest]
    if strongest > current and len(best) == 1:
        h["creature"] = best[0]


def transition(h_t, z_t, action):
    h = deepcopy(h_t)
    if action == 7:
        if h["history"]:
            previous = h["history"].pop()
            history = h["history"]
            h = previous
            h["history"] = history
        return h
    if action == 5:
        h["history"].append(core(h))
        h["on"] = not h["on"]
        h["feedback"] = None
        return h
    if action not in MOVES:
        return h
    dx, dy = MOVES[action]
    destination = (h["emitter"][0] + dx, h["emitter"][1] + dy)
    if not swept_clear(h, h["emitter"], destination, 3, h["creature"], 2):
        h["history"].append(core(h))
        h["feedback"] = (destination, "blocked")
        return h
    h["history"].append(core(h))
    h["emitter"] = destination
    h["feedback"] = None
    h["translations"] += 1
    # The sole tick: decay -> real local deposition -> one strictly local response.
    h["field"] = {pose: age + 1 for pose, age in h["field"].items() if age + 1 < 9}
    site = nozzle_site(h)
    if h["on"] and site is not None:
        h["field"][site] = 0
    local_response(h)
    return h


def predict(h_t, seed):
    return {"current_tier": tier(h_t["field"].get(h_t["creature"])),
            "nozzle_site": nozzle_site(h_t)}


def check_level_complete(h_t, z_t, level):
    return h_t["level"] == level and h_t["creature"] == LEVELS[level]["goal"]


def get_available_actions():
    return [1, 2, 3, 4, 5, 7]


def render(h_t, z_t):
    image = [[5 for _ in range(64)] for _ in range(64)]

    def rect(x0, y0, x1, y1, color):
        for yy in range(max(0, y0), min(64, y1)):
            for xx in range(max(0, x0), min(64, x1)):
                image[yy][xx] = color

    def patch(x, y, value):
        # Strength has both area and shape; no hidden finer score is compared.
        rect(x - 2, y - 2, x + 3, y + 3, 5)
        if value == 1:
            rect(x - 1, y, x + 2, y + 1, 6)
        elif value == 2:
            rect(x - 2, y - 2, x + 3, y + 3, 14)
            rect(x - 1, y - 1, x + 2, y + 2, 5)
        elif value == 3:
            rect(x - 2, y - 2, x + 3, y + 3, 10)

    # Compact single room, single open destination; no HUD, dots or decorative map.
    for rectangle in walls(h_t["level"]):
        rect(*rectangle, 4)
    gx, gy = LEVELS[h_t["level"]]["goal"]
    rect(gx - 3, gy - 3, gx + 4, gy + 4, 11)
    rect(gx - 2, gy - 2, gx + 3, gy + 3, 5)
    # Remove the receiver's top face: visibly open rather than another filled body.
    rect(gx - 2, gy - 3, gx + 3, gy - 2, 5)
    for (x, y), age in h_t["field"].items():
        patch(x, y, tier(age))
    # Redraw exact solid wall after patches so scent cannot conceal an obstruction.
    for rectangle in walls(h_t["level"]):
        rect(*rectangle, 4)
    ex, ey = h_t["emitter"]
    if nozzle_site(h_t) is not None:
        rect(ex - 1, ey + 3, ex + 2, ey + 9, 12 if h_t["on"] else 4)
    rect(ex - 3, ey - 3, ex + 4, ey + 4, 12)
    # Substantial 3x3 central nozzle-state window, not weak border pixels.
    rect(ex - 1, ey - 1, ex + 2, ey + 2, 10 if h_t["on"] else 4)
    cx, cy = h_t["creature"]
    rect(cx - 2, cy - 2, cx + 3, cy + 3, 1)
    # Ground-tier window is attached and always visible inside the persistent body.
    value = tier(h_t["field"].get(h_t["creature"]))
    rect(cx - 1, cy - 1, cx + 2, cy + 2, 5)
    if value == 1:
        rect(cx - 1, cy - 1, cx + 2, cy + 2, 6)
    elif value == 2:
        rect(cx - 1, cy - 1, cx + 2, cy + 2, 14)
        rect(cx, cy, cx + 1, cy + 1, 5)
    elif value == 3:
        rect(cx - 1, cy - 1, cx + 2, cy + 2, 10)
    if h_t["feedback"] is not None:
        rect(ex - 3, ey - 4, ex + 4, ey - 3, 8)
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


class V206(FunctionalGame):
    GAME_ID = 'v206-18dc82ebc9e7b826'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
