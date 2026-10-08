"""Winding Anchor: original finite polygonal cable toy; secured execution only.

All geometry uses one load-to-hand ordered route. Reserve is stored in the
hand's attached spool; it has no separate reel control. No solution helper.
"""
import copy
import math


LEVELS = {
    0: {"load": [20, 30], "hand": [24, 18], "pegs": [[29, 27, 37, 35]], "length": 19.0, "goal": [24, 27], "home": None, "tags": ["route", "redirected_pull"]},
    1: {"load": [20, 34], "hand": [24, 46], "pegs": [[29, 29, 37, 37]], "length": 19.0, "goal": [24, 37], "home": None, "tags": ["route", "reflected_contact"]},
    2: {"load": [20, 30], "hand": [24, 18], "pegs": [[29, 27, 37, 35]], "length": 23.0, "goal": [24, 27], "home": [24, 42], "tags": ["temporary_wrap", "dock_then_return"]},
    3: {"load": [20, 30], "hand": [24, 18], "pegs": [[33, 27, 41, 35], [15, 39, 23, 47]], "length": 30.0, "goal": [24, 27], "home": [28, 50], "tags": ["competing_contacts", "return_clearance"]},
    4: {"load": [8, 31], "hand": [8, 14], "pegs": [[13, 22, 27, 38]], "length": 28.0, "goal": [12, 18], "home": [8, 42], "tags": ["pocket_retrieval", "contact_reallocation"]},
    5: {"load": [8, 33], "hand": [8, 12], "pegs": [[13, 24, 27, 42], [35, 8, 43, 16], [37, 35, 45, 43]], "length": 32.0, "goal": [12, 20], "home": [8, 48], "tags": ["upper_transit", "reserve_allocation", "return"]},
    6: {"load": [8, 33], "hand": [8, 12], "pegs": [[13, 24, 27, 42], [33, 8, 41, 16], [38, 36, 46, 44]], "length": 40.0, "goal": [12, 20], "home": [24, 48], "tags": ["asymmetric_return", "contact_reallocation", "reserve_allocation"]},
}

EPS = 1e-7
CORD_OFFSET = 2.5
CONTACT_LIMIT = 16
HISTORY_LIMIT = 256


def _cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _distance(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


def _corners(rect):
    x0, y0, x1, y1 = rect
    r = CORD_OFFSET
    return [(x0-r, y0-r), (x1+r, y0-r), (x1+r, y1+r), (x0-r, y1+r)]


def _expanded(rect):
    x0, y0, x1, y1 = rect
    return (x0-CORD_OFFSET, y0-CORD_OFFSET, x1+CORD_OFFSET, y1+CORD_OFFSET)


def _interior_hit(a, b, rect):
    """Exact open-rectangle span intersection, with stable tangent tolerance."""
    x0, y0, x1, y1 = rect
    low, high = 0.0, 1.0
    for av, bv, lower, upper in ((a[0], b[0], x0+EPS, x1-EPS),
                                  (a[1], b[1], y0+EPS, y1-EPS)):
        dv = bv-av
        if abs(dv) < EPS:
            if av <= lower or av >= upper:
                return None
        else:
            enter, leave = sorted(((lower-av)/dv, (upper-av)/dv))
            low, high = max(low, enter), min(high, leave)
            if high-low <= EPS:
                return None
    if high <= EPS or low >= 1.0-EPS:
        return None
    return max(0.0, low)


def _first_block(a, b, pegs):
    hits = []
    for i, rect in enumerate(pegs):
        hit = _interior_hit(a, b, _expanded(rect))
        if hit is not None:
            hits.append((hit, i))
    return min(hits)[1] if hits else None


def _clear(a, b, pegs):
    return _first_block(a, b, pegs) is None


def route_vertices(h):
    pegs = LEVELS[h["level"]]["pegs"]
    return [tuple(h["load"])] + [_corners(pegs[p])[c] for p, c, turn in h["contacts"]] + [tuple(h["hand"])]


def routed_length(h):
    points = route_vertices(h)
    return sum(_distance(a, b) for a, b in zip(points, points[1:]))


def reserve(h):
    return max(0.0, h["length"] - routed_length(h))


def _detour(a, b, old_b, peg_index, pegs):
    """A local contour insertion on the side swept by this attachment.

    The minimum below is only among new detours of the actually hit contour.
    Existing contacts are never replaced by an endpoint-only shortest route.
    """
    vertices = _corners(pegs[peg_index])
    motion = _cross(a, old_b, b)
    required_turn = 1 if motion > EPS else -1 if motion < -EPS else 0
    options = []
    for start in range(4):
        for direction in (-1, 1):
            for count in range(1, 5):
                indices = [(start + direction*i) % 4 for i in range(count)]
                path = [a] + [vertices[i] for i in indices] + [b]
                if any(_interior_hit(x, y, _expanded(pegs[peg_index])) is not None
                       for x, y in zip(path, path[1:])):
                    continue
                # The last span may meet a subsequent peg: the update loop
                # handles that after this first encountered contour.
                if any(not _clear(x, y, pegs) for x, y in zip(path[:-2], path[1:-1])):
                    continue
                turns = [_cross(path[i], path[i+1], path[i+2]) for i in range(count)]
                if required_turn and any(t*required_turn < -EPS for t in turns):
                    continue
                nonzero = [1 if t > EPS else -1 for t in turns if abs(t) > EPS]
                if nonzero and min(nonzero) != max(nonzero):
                    continue
                sign = required_turn or (nonzero[0] if nonzero else 1)
                cost = sum(_distance(x, y) for x, y in zip(path, path[1:]))
                options.append((cost, tuple(indices), sign))
    if not options:
        raise ValueError("No continuous local contour insertion")
    cost, indices, sign = min(options)
    return [(peg_index, i, sign) for i in indices]


def _compact_contacts(contacts):
    """Drop only consecutive identical zero-length contact triplets.

    Nonconsecutive repeats and different oriented turns remain: those may
    encode genuine winding rather than redundant numerical corner insertion.
    """
    result = []
    for contact in contacts:
        if not result or contact != result[-1]:
            result.append(contact)
    return result


def _update_end(fixed, old_end, new_end, contacts, pegs):
    """Update only the moving end of an existing ordered route."""
    work = _compact_contacts(contacts)
    for iteration in range(CONTACT_LIMIT):
        if work:
            q = _corners(pegs[work[-1][0]])[work[-1][1]]
            p = _corners(pegs[work[-2][0]])[work[-2][1]] if len(work) > 1 else fixed
            turn = work[-1][2]
            if _cross(p, q, new_end)*turn <= EPS and _clear(p, new_end, pegs):
                work.pop()
                continue
        pivot = _corners(pegs[work[-1][0]])[work[-1][1]] if work else fixed
        hit = _first_block(pivot, new_end, pegs)
        if hit is None:
            points = [fixed] + [_corners(pegs[p])[c] for p, c, turn in work] + [new_end]
            if any(not _clear(a, b, pegs) for a, b in zip(points, points[1:])):
                raise ValueError("An existing span crossed a contour")
            return work
        additions = _detour(pivot, new_end, old_end, hit, pegs)
        work = _compact_contacts(work + additions)
        if len(work) > CONTACT_LIMIT:
            raise ValueError("Contact complexity exceeded finite bound")
    raise ValueError("Contact update did not settle")


def _body_clear(center, halfwidth, pegs):
    x, y = center
    if x-halfwidth < 3-EPS or x+halfwidth > 60+EPS or y-halfwidth < 3-EPS or y+halfwidth > 60+EPS:
        return False
    for x0, y0, x1, y1 in pegs:
        if x+halfwidth > x0+EPS and x-halfwidth < x1-EPS and y+halfwidth > y0+EPS and y-halfwidth < y1-EPS:
            return False
    return True


def _capture(h):
    if not h["docked"] and _distance(h["load"], LEVELS[h["level"]]["goal"]) <= 1.4:
        h["docked"] = True


def _resolve_tension(h):
    pegs = LEVELS[h["level"]]["pegs"]
    for iteration in range(128):
        shortage = routed_length(h) - h["length"]
        if shortage <= EPS:
            return None
        if h["docked"]:
            return ("taut", tuple(h["hand"]))
        points = route_vertices(h)
        target = points[1]
        gap = _distance(points[0], target)
        if gap <= EPS:
            if h["contacts"]:
                h["contacts"].pop(0)
                continue
            return ("cargo", tuple(h["load"]))
        amount = min(shortage, gap, 0.25)
        old_load = tuple(h["load"])
        new_load = (old_load[0] + amount*(target[0]-old_load[0])/gap,
                    old_load[1] + amount*(target[1]-old_load[1])/gap)
        if not _body_clear(new_load, 2, pegs):
            return ("cargo", new_load)
        reversed_contacts = [(p, c, -turn) for p, c, turn in reversed(h["contacts"])]
        updated = _update_end(tuple(h["hand"]), old_load, new_load, reversed_contacts, pegs)
        h["contacts"] = [(p, c, -turn) for p, c, turn in reversed(updated)]
        h["load"] = list(new_load)
    return ("taut", tuple(h["hand"]))


def _snapshot(h):
    return copy.deepcopy({k: v for k, v in h.items() if k != "history"})


def transition(h_t, z_t, action):
    h = copy.deepcopy(h_t)
    if action == 7:
        if h["history"]:
            prior = h["history"].pop()
            prior["history"] = h["history"]
            return prior
        return h
    delta = {1: (0, -0.5), 2: (0, 0.5), 3: (-0.5, 0), 4: (0.5, 0)}.get(action)
    if delta is None:
        return h
    prior = _snapshot(h)
    history = (h["history"] + [prior])[-HISTORY_LIMIT:]
    h["feedback"] = None
    pegs = LEVELS[h["level"]]["pegs"]
    failure = None
    try:
        for substep in range(8):
            old_hand = tuple(h["hand"])
            new_hand = (old_hand[0]+delta[0], old_hand[1]+delta[1])
            if not _body_clear(new_hand, 3, pegs):
                failure = ("hand", new_hand)
                break
            h["contacts"] = _update_end(tuple(h["load"]), old_hand, new_hand, h["contacts"], pegs)
            h["hand"] = list(new_hand)
            failure = _resolve_tension(h)
            if failure:
                break
    except ValueError:
        failure = ("contact", tuple(h["hand"]))
    if failure:
        h = copy.deepcopy(prior)
        h["feedback"] = [failure[0], list(failure[1])]
    else:
        _capture(h)
    h["history"] = history
    return h


def predict(h_t, seed=0):
    return {}


def check_level_complete(h_t, z_t, level):
    if level != h_t["level"] or not h_t["docked"] or _distance(h_t["load"], LEVELS[level]["goal"]) > 1.4:
        return False
    home = LEVELS[level]["home"]
    return home is None or _distance(h_t["hand"], home) <= 2.1


def get_initial_state(level):
    config = LEVELS[level]
    h = {"level": level, "load": list(config["load"]), "hand": list(config["hand"]),
         "contacts": [], "length": config["length"], "docked": False,
         "feedback": None, "history": []}
    return h, {}


def get_available_actions():
    return [1, 2, 3, 4, 7]


def _box(grid, x0, y0, x1, y1, color):
    for y in range(max(0, int(round(y0))), min(63, int(round(y1)))+1):
        for x in range(max(0, int(round(x0))), min(63, int(round(x1)))+1):
            grid[y][x] = color


def _stroke(grid, a, b, color, radius=2):
    count = max(1, int(math.ceil(_distance(a, b)*3)))
    for i in range(count+1):
        t = i/count
        x, y = a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t
        ix, iy = int(round(x)), int(round(y))
        _box(grid, ix-radius, iy-radius, ix+radius, iy+radius, color)


def _cradle(grid, point, color, radius, opening="left"):
    x, y = point
    _box(grid, x-radius, y-radius, x+radius, y+radius, color)
    _box(grid, x-radius+1, y-radius+1, x+radius-1, y+radius-1, 1)
    if opening == "left":
        _box(grid, x-radius, y-2, x-radius+1, y+2, 1)
    else:
        _box(grid, x-2, y-radius, x+2, y-radius+1, 1)


def render(h_t, z_t):
    h = h_t
    config = LEVELS[h["level"]]
    grid = [[1 for x in range(64)] for y in range(64)]
    _box(grid, 2, 2, 61, 61, 3)
    _box(grid, 3, 3, 60, 60, 1)
    _cradle(grid, config["goal"], 0, 4)
    if config["home"] is not None:
        _cradle(grid, config["home"], 14, 5, "up")
    points = route_vertices(h)
    color = 11 if reserve(h) < 0.35 else 10
    for a, b in zip(points, points[1:]):
        _stroke(grid, a, b, color)
    for rect in config["pegs"]:
        _box(grid, *rect, 4)
    lx, ly = h["load"]
    _box(grid, lx-2, ly-2, lx+2, ly+2, 11)
    # The local held/free state occupies the cargo's full 3x3 interior,
    # surrounded by its persistent orange body. It cannot merge with an
    # external white cradle/peg edge as the former bottom stripe did.
    cx, cy = int(round(lx)), int(round(ly))
    _box(grid, cx-1, cy-1, cx+1, cy+1, 0 if h["docked"] else 4)
    hx, hy = h["hand"]
    _box(grid, hx-3, hy-3, hx+3, hy+3, 14)
    _box(grid, hx-1, hy-1, hx+1, hy+1, 1)
    # Local stored-reserve cue, quantized by material fraction. It is inside
    # the physical hand body, and not an ignored deployed slack/sag curve.
    coil = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
    quantity = int(math.ceil(8*reserve(h)/h["length"]-EPS))
    for dx, dy in coil[:max(0, min(8, quantity))]:
        _box(grid, hx+dx, hy+dy, hx+dx, hy+dy, 10)
    if h["feedback"]:
        kind, location = h["feedback"]
        x, y = location
        radius = 4 if kind == "hand" else 3
        _box(grid, x-radius, y-radius, x+radius, y-radius, 8)
        _box(grid, x-radius, y+radius, x+radius, y+radius, 8)
        if kind in ("taut", "contact"):
            _box(grid, hx-1, hy-1, hx+1, hy+1, 8)
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


class V205(FunctionalGame):
    GAME_ID = 'v205-4aa913d479f6ec63'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
