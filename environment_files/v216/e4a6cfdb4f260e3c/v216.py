"""Consumable Path: current material, reciprocal contact, and complete recovery."""
import copy
import numpy as np


LEVELS = {
    0: {
        "name": "One crossing spends one link",
        "bounds": (1, 1, 5, 5), "walls": (),
        "maker": (2, 3), "lay": False,
        "followers": ((2, 4),), "goals": ((3, 4),),
        "links": (((2, 4), (3, 4)),),
    },
    1: {
        "name": "Closed gap and open retrace",
        "bounds": (1, 1, 5, 5), "walls": (),
        "maker": (2, 3), "lay": False,
        "followers": ((2, 3),), "goals": ((4, 3),),
        "links": (((3, 3), (4, 3)),),
    },
    2: {
        "name": "A bend carries the same body",
        "bounds": (1, 1, 5, 5), "walls": ((3, 3), (3, 4), (3, 5)),
        "maker": (1, 3), "lay": True,
        "followers": ((1, 4),), "goals": ((5, 4),),
        "links": (((1, 4), (1, 3)),),
    },
    3: {
        "name": "Repair a fork and reuse a neck",
        "bounds": (1, 1, 5, 5), "walls": ((3, 1), (3, 2), (3, 4), (3, 5)),
        "maker": (1, 1), "lay": False,
        "followers": ((1, 2), (1, 4)), "goals": ((5, 2), (5, 4)),
        "links": (((1, 1), (1, 2)), ((1, 2), (2, 2))),
    },
    4: {
        "name": "Withhold the second branch",
        "bounds": (1, 1, 5, 5), "walls": ((3, 1), (3, 2), (3, 4), (3, 5)),
        "maker": (4, 3), "lay": False,
        "followers": ((1, 2), (1, 5)), "goals": ((5, 2), (5, 5)),
        "links": (((1, 2), (2, 2)), ((2, 2), (2, 3)), ((2, 3), (3, 3)),
                  ((3, 3), (4, 3)), ((4, 3), (4, 2)), ((4, 2), (5, 2)),
                  ((4, 3), (4, 4)), ((4, 4), (5, 4)), ((5, 4), (5, 5))),
    },
    5: {
        "name": "Divert, rebuild from the right, and return",
        "bounds": (1, 1, 5, 5), "walls": ((3, 1), (3, 2), (3, 4), (3, 5)),
        "maker": (4, 3), "lay": False,
        "followers": ((1, 2), (5, 2)), "goals": ((5, 4), (1, 4)),
        "links": (((1, 2), (2, 2)), ((2, 2), (2, 3)), ((2, 3), (3, 3)),
                  ((3, 3), (4, 3)), ((4, 3), (4, 2)), ((4, 2), (5, 2))),
    },
    6: {
        "name": "Three bodies compete for rebuilt access",
        "bounds": (1, 1, 5, 5), "walls": ((3, 1), (3, 2), (3, 4), (3, 5)),
        "maker": (4, 4), "lay": False,
        "followers": ((2, 3), (4, 3), (2, 4)),
        "goals": ((5, 4), (1, 4), (5, 2)),
        "links": (((2, 3), (2, 4)), ((2, 3), (3, 3)), ((3, 3), (4, 3)),
                  ((4, 3), (4, 2)), ((4, 2), (5, 2)),
                  ((4, 3), (4, 4)), ((4, 4), (5, 4))),
    },
}

DIRECTIONS = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}
BODY_COLORS = (8, 14, 12)


def _edge(a, b):
    return tuple(sorted((tuple(a), tuple(b))))


def _legal(level, p):
    x0, y0, x1, y1 = level["bounds"]
    return x0 <= p[0] <= x1 and y0 <= p[1] <= y1 and tuple(p) not in level["walls"]


def _neighbors(links, p):
    p = tuple(p)
    return sorted(b if a == p else a for a, b in links if a == p or b == p)


def _snapshot(h):
    return copy.deepcopy({k: v for k, v in h.items() if k != "undo"})


def get_initial_state(level_index):
    level = LEVELS[int(level_index)]
    h = {"level": int(level_index), "maker": tuple(level["maker"]),
         "lay": bool(level["lay"]), "followers": list(level["followers"]),
         "links": sorted(_edge(a, b) for a, b in level["links"]), "undo": []}
    return h, predict(h, 0)


def transition(h_t, z_t, action):
    number = int(action[0] if isinstance(action, (tuple, list)) else action)
    if number == 0:
        return get_initial_state(h_t["level"])[0]
    h = copy.deepcopy(h_t)
    if number == 7:
        if h["undo"]:
            previous = h["undo"].pop()
            return {**previous, "undo": h["undo"]}
        return h
    if number not in DIRECTIONS and number != 5:
        return h
    h["undo"].append(_snapshot(h))
    if number == 5:
        h["lay"] = not h["lay"]
        return h

    level = LEVELS[h["level"]]
    dx, dy = DIRECTIONS[number]
    a = tuple(h["maker"])
    b = (a[0] + dx, a[1] + dy)
    links = set(h["links"])
    if _legal(level, b):
        h["maker"] = b
        edge = _edge(a, b)
        if h["lay"]:
            links.add(edge)
        else:
            links.discard(edge)

    # All choices use one pre-response material/occupancy snapshot. A fork,
    # occupied contact, opposing swap, or same-destination contention stays put.
    occupied = set(tuple(p) for p in h["followers"])
    proposals = {}
    for i, p in enumerate(h["followers"]):
        if tuple(p) == level["goals"][i]:
            continue
        choices = _neighbors(links, p)
        if len(choices) == 1 and choices[0] not in occupied:
            proposals[i] = choices[0]
    counts = {}
    for p in proposals.values():
        counts[p] = counts.get(p, 0) + 1
    for i, p in proposals.items():
        if counts[p] == 1:
            links.remove(_edge(h["followers"][i], p))
            h["followers"][i] = p
    h["links"] = sorted(links)
    return h


def predict(h_t, seed):
    # The explicit seed is accepted; the process has no stochastic dynamics.
    level = LEVELS[h_t["level"]]
    occupied = set(tuple(p) for p in h_t["followers"])
    choices = [_neighbors(h_t["links"], p) for p in h_t["followers"]]
    proposed = {}
    for i, p in enumerate(h_t["followers"]):
        if tuple(p) != level["goals"][i] and len(choices[i]) == 1 and choices[i][0] not in occupied:
            target = choices[i][0]
            proposed[target] = proposed.get(target, 0) + 1
    status = []
    for i, p in enumerate(h_t["followers"]):
        if tuple(p) == level["goals"][i]:
            status.append("rest")
        elif len(choices[i]) > 1:
            status.append("fork")
        elif not choices[i]:
            status.append("gap")
        elif choices[i][0] in occupied:
            status.append("contact")
        elif proposed.get(choices[i][0], 0) > 1:
            status.append("contention")
        else:
            status.append("ready")
    return {"choices": choices, "status": status}


def check_level_complete(h_t, z_t, level_index):
    return h_t["level"] == int(level_index) and all(
        tuple(p) == goal for p, goal in zip(h_t["followers"], LEVELS[int(level_index)]["goals"])
    ) and len(h_t["followers"]) == len(LEVELS[int(level_index)]["goals"])


def _center(p):
    return -1 + 11 * p[0], -1 + 11 * p[1]


def _shape(kind, radius):
    pixels = []
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            inside = (abs(dx) + abs(dy) <= radius) if kind == 2 else (
                abs(dx) + abs(dy) <= radius + radius // 2 if kind == 0 else True)
            if inside:
                pixels.append((dx, dy))
    return pixels


def render(h_t, z_t):
    frame = np.full((64, 64), 1, dtype=np.int8)
    frame[4:61, 4:61] = 2
    level = LEVELS[h_t["level"]]
    for p in level["walls"]:
        x, y = _center(p)
        frame[y - 5:y + 6, x - 5:x + 6] = 5
    for a, b in h_t["links"]:
        x0, y0 = _center(a)
        x1, y1 = _center(b)
        frame[min(y0, y1) - 2:max(y0, y1) + 3,
              min(x0, x1) - 2:max(x0, x1) + 3] = 10
    # This outline marks the maker's current contact; it is not extra solid
    # collision material. At a rest it surrounds the whole unchanged rest rim.
    x, y = _center(h_t["maker"])
    radius = 7 if tuple(h_t["maker"]) in level["goals"] else 4
    for d in range(1 - radius, radius):
        frame[y - radius, x + d] = 0
        frame[y + d, x - radius] = 0
        frame[y + d, x + radius] = 0
        if not h_t["lay"] or abs(d) >= 3:
            frame[y + radius, x + d] = 0
    if not h_t["lay"]:
        frame[y + radius - 1, x - 2:x + 3] = 7
    # Goal rims retain paint priority over control annotations. Solid followers
    # are painted last, preserving both their contours and each outer goal rim.
    for i, p in enumerate(level["goals"]):
        x, y = _center(p)
        inner = set(_shape(i, 3))
        for dx, dy in _shape(i, 5):
            if (dx, dy) not in inner:
                frame[y + dy, x + dx] = BODY_COLORS[i]
    derived = predict(h_t, 0)
    for i, p in enumerate(h_t["followers"]):
        x, y = _center(p)
        for dx, dy in _shape(i, 3 if i == 2 else 2):
            frame[y + dy, x + dx] = BODY_COLORS[i]
        if derived["status"][i] in ("fork", "contact", "contention"):
            frame[y, x - 1:x + 2] = 5
        if derived["status"][i] == "rest":
            frame[y, x - 1:x + 2] = 0
    return frame


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


class V216(FunctionalGame):
    GAME_ID = 'v216-e4a6cfdb4f260e3c'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
