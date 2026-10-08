"""Original finite, quasistatic spring/pawl toy. Native execution only in isolation.

Every output coordinate is material travel. A drive/holder lever enables a light
follower; bearing depends on actual contour-flank contact, not lever posture.
The held crosshead's coordinate is prescribed. Its off-axis slotted follower
stems are ideal kinematic guides. Contacts between the two late outputs use the
same planar convex material parts as rendering. No real-time dynamics occur.
"""
import copy
import math

LEVELS = {
    0: {"name": "Drive and overrun", "orthogonal": False, "rows": [26], "limit": [16], "target": [4], "driver_teeth": [[0, 8, 16]], "holder_teeth": [[0, 8, 16]], "initial_q": [0], "initial_c": 0},
    1: {"name": "Retained finite input", "orthogonal": False, "rows": [26], "limit": [20], "target": [12], "driver_teeth": [[0, 8, 16]], "holder_teeth": [[0, 8, 16]], "initial_q": [0], "initial_c": 0},
    2: {"name": "Enabled and seated", "orthogonal": False, "rows": [26], "limit": [20], "target": [12], "driver_teeth": [[0, 8, 16]], "holder_teeth": [[0, 8, 16]], "initial_q": [4], "initial_c": 4},
    3: {"name": "Selective shared handoff", "orthogonal": False, "rows": [18, 42], "limit": [20, 20], "target": [8, 16], "driver_teeth": [[0, 8, 16], [0, 8, 16]], "holder_teeth": [[0, 8, 16], [0, 8, 16]], "initial_q": [0, 0], "initial_c": 0},
    4: {"name": "Cross the lip, receive the load", "orthogonal": True, "rows": [8, 16], "limit": [16, 12], "target": [12, 12], "driver_teeth": [[0, 8, 16], [0, 8]], "holder_teeth": [[0, 8, 16], [0, 8, 12]], "initial_q": [0, 0], "initial_c": 0},
    5: {"name": "A real stop jams the common input", "orthogonal": False, "rows": [18, 42], "limit": [8, 20], "target": [8, 16], "driver_teeth": [[0, 8, 16], [0, 8, 16]], "holder_teeth": [[0, 8], [0, 8, 16]], "initial_q": [0, 0], "initial_c": 0},
    6: {"name": "The held driver bears both springs", "orthogonal": True, "rows": [8, 16], "limit": [16, 12], "target": [12, 12], "driver_teeth": [[0, 8, 16], [0, 8]], "holder_teeth": [[0, 8, 16], [0, 8]], "initial_q": [0, 0], "initial_c": 0}
}


def get_initial_state(level):
    cfg = LEVELS[level]
    n = len(cfg["initial_q"])
    return {"level": level, "q": list(cfg["initial_q"]), "c": cfg["initial_c"], "driver": [True] * n, "holder": [True] * n, "feedback": None, "history": []}, {}


def predict(h_t, seed=0):
    return {}


def get_available_actions():
    return [3, 4, 6, 7]


def rectangle(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def slotted_rectangle(x0, y0, x1, y1, sx0, sy0, sx1, sy1):
    return [rectangle(x0, y0, x1, sy0), rectangle(x0, sy1, x1, y1), rectangle(x0, sy0, sx0, sy1), rectangle(sx1, sy0, x1, sy1)]


def parts(level, branch, q):
    cfg = LEVELS[level]
    if not cfg["orthogonal"]:
        y = cfg["rows"][branch]
        body = slotted_rectangle(4 + q, y, 40 + q, y + 8, 12 + q, y + 1, 22 + q, y + 7)
    elif branch == 0:
        body = slotted_rectangle(2 + q, 4, 42 + q, 10, 14 + q, 5, 26 + q, 9) + [
            rectangle(38 + q, 8, 42 + q, 33),
            [(21 + q, 29), (26 + q, 29), (22 + q, 33), (17 + q, 33)],
            rectangle(22 + q, 29, 42 + q, 33)]
    else:
        body = slotted_rectangle(8, 16 + q, 14, 50 + q, 9, 28 + q, 13, 40 + q) + [
            [(14, 16 + q), (34, 16 + q), (14, 36 + q)],
            rectangle(12, 24 + q, 33, 28 + q)]
    for role in ("holder", "driver"):
        for tooth in cfg[role + "_teeth"][branch]:
            if cfg["orthogonal"] and branch == 1:
                yy = 32 - tooth + q
                xx = 4 if role == "holder" else 6
                body.append([(xx, yy), (8, yy), (8, yy + 4)])
            else:
                yy = 4 if cfg["orthogonal"] else cfg["rows"][branch]
                xx = (24 if cfg["orthogonal"] else 32) - tooth + q
                if role == "holder":
                    body.append([(xx, yy), (xx, yy - 4), (xx + 5, yy)])
                else:
                    yy = 10 if cfg["orthogonal"] else yy + 8
                    body.append([(xx, yy), (xx, yy + 4), (xx + 5, yy)])
    return body


def polygon_overlap(a, b):
    # Separating-axis theorem: tangency is legal, penetration is not.
    for poly in (a, b):
        for i in range(len(poly)):
            p, r = poly[i], poly[(i + 1) % len(poly)]
            ax, ay = -(r[1] - p[1]), r[0] - p[0]
            aa = [x * ax + y * ay for x, y in a]
            bb = [x * ax + y * ay for x, y in b]
            if max(aa) <= min(bb) + 1e-9 or max(bb) <= min(aa) + 1e-9:
                return False
    return True


def obstruction(level, q):
    cfg = LEVELS[level]
    for i, x in enumerate(q):
        if x < 0 or x > cfg["limit"][i]:
            return ("stop", i)
    if cfg["orthogonal"]:
        for a in parts(level, 0, q[0]):
            for b in parts(level, 1, q[1]):
                if polygon_overlap(a, b):
                    return ("contact", 1)
    return None


def supports(h, branch):
    cfg, q, c = LEVELS[h["level"]], h["q"][branch], h["c"]
    available = [0]
    if h["holder"][branch]:
        available += [v for v in cfg["holder_teeth"][branch] if v <= q]
    if h["driver"][branch]:
        available += [c + v for v in cfg["driver_teeth"][branch] if 0 <= c + v <= q]
    return max(available)


def seated(h, branch, role):
    cfg = LEVELS[h["level"]]
    if not h[role][branch]:
        return False
    return h["q"][branch] in ([h["c"] + t for t in cfg["driver_teeth"][branch]] if role == "driver" else cfg["holder_teeth"][branch])


def settle(h):
    # The event bounds come from real flank locations below the present output.
    # Springs can only reduce coordinates; joint material constraints stop or
    # couple that retreat. Both negative springs participate, without flag priority.
    bounds = [supports(h, i) for i in range(len(h["q"]))]
    while True:
        moved = False
        for i in range(len(h["q"])):
            if h["q"][i] <= bounds[i]:
                continue
            candidate = list(h["q"])
            candidate[i] -= 1
            if obstruction(h["level"], candidate) is None:
                h["q"] = candidate
                moved = True
        if not moved:
            return h


def lever_boxes(h):
    cfg, c = LEVELS[h["level"]], h["c"]
    if cfg["orthogonal"]:
        return [("holder", 0, (20, 0, 28, 7)), ("driver", 0, (27 + c, 39, 35 + c, 46)),
                ("holder", 1, (0, 15, 7, 23)), ("driver", 1, (0, 34 + c, 7, 41 + c))]
    boxes = []
    for i, y in enumerate(cfg["rows"]):
        boxes += [("holder", i, (28, y - 13, 36, y - 6)), ("driver", i, (24 + c, y + 15, 32 + c, y + 22))]
    return boxes


def transition(h_t, z_t, action):
    h = copy.deepcopy(h_t)
    number = action[0] if isinstance(action, (tuple, list)) else action
    if number == 7:
        if not h["history"]:
            return h
        prior = h["history"].pop()
        return {**prior, "history": h["history"]}
    prior = {k: copy.deepcopy(v) for k, v in h.items() if k != "history"}
    h["feedback"] = None
    if number in (3, 4):
        target_c = h["c"] + (4 if number == 4 else -4)
        if not 0 <= target_c <= 8:
            h["feedback"] = ("carriage", -1)
        else:
            old = copy.deepcopy(h)
            direction = 1 if number == 4 else -1
            for _ in range(4):
                # A single prescribed coordinate drives every connected branch.
                # No branch can independently clip at its limit.
                previous_c = h["c"]
                h["c"] += direction
                if direction > 0:
                    for i in range(len(h["q"])):
                        if h["driver"][i]:
                            rear = [t for t in LEVELS[h["level"]]["driver_teeth"][i] if previous_c + t <= h["q"][i]]
                            if rear:
                                h["q"][i] = max(h["q"][i], h["c"] + max(rear))
                bad = obstruction(h["level"], h["q"])
                if bad is not None:
                    h = old
                    h["feedback"] = bad
                    break
                settle(h)
    elif number == 6 and isinstance(action, (tuple, list)) and len(action) == 3:
        _, x, y = action
        for role, branch, (x0, y0, x1, y1) in lever_boxes(h):
            if x0 <= x < x1 and y0 <= y < y1:
                h[role][branch] = not h[role][branch]
                settle(h)
                break
        else:
            h["feedback"] = ("miss", -1)
    else:
        return h_t
    h["history"].append(prior)
    return h


def apertures(level):
    cfg = LEVELS[level]
    if cfg["orthogonal"]:
        return [(29, 5, 35, 9), (9, 44, 13, 50)]
    return [(14 + q, y + 2, 20 + q, y + 6) for q, y in zip(cfg["target"], cfg["rows"])]


def check_level_complete(h_t, z_t, level):
    if h_t["level"] != level or obstruction(level, h_t["q"]) is not None:
        return False
    for i, box in enumerate(apertures(level)):
        if any(polygon_overlap(p, rectangle(*box)) for p in parts(level, i, h_t["q"][i])):
            return False
    return True


def fill_polygon(grid, poly, color):
    x0 = max(0, math.floor(min(x for x, y in poly)))
    x1 = min(64, math.ceil(max(x for x, y in poly)))
    y0 = max(0, math.floor(min(y for x, y in poly)))
    y1 = min(64, math.ceil(max(y for x, y in poly)))
    for y in range(y0, y1):
        for x in range(x0, x1):
            signs = []
            for i, (ax, ay) in enumerate(poly):
                bx, by = poly[(i + 1) % len(poly)]
                signs.append((bx - ax) * (y + .5 - ay) - (by - ay) * (x + .5 - ax))
            if all(v >= -1e-9 for v in signs) or all(v <= 1e-9 for v in signs):
                grid[y][x] = color


def paint_rect(grid, box, color):
    fill_polygon(grid, rectangle(*box), color)


def line(grid, a, b, color, width=1):
    x0, y0 = a
    x1, y1 = b
    n = max(1, int(max(abs(x1 - x0), abs(y1 - y0))))
    for k in range(n + 1):
        x, y = round(x0 + (x1 - x0) * k / n), round(y0 + (y1 - y0) * k / n)
        paint_rect(grid, (x, y, x + width, y + width), color)


def render(h_t, z_t):
    h, cfg = h_t, LEVELS[h_t["level"]]
    g = [[5] * 64 for _ in range(64)]
    # The frame and positively held common crosshead are material anchors,
    # not action counters. Driver stems occupy schematic guide channels.
    if cfg["orthogonal"]:
        c = h["c"]
        common = (43 + c, 49 + c, 51 + c, 55 + c)
        line(g, (47 + c, 52 + c), (47 + c, 42), 3, 2)
        line(g, (31 + c, 42), (47 + c, 42), 3, 2)
        line(g, (31 + c, 42), (24 + c, 19), 3, 2)
        line(g, (47 + c, 42), (5, 42 + c), 3)
        line(g, (5, 42 + c), (5, 32 + c), 3, 2)
        paint_rect(g, (58, 3, 64, 35), 2)
        paint_rect(g, (7, 61, 16, 64), 2)
    else:
        c = h["c"]
        common = (48 + c, 29, 56 + c, 35)
        paint_rect(g, (52 + c, 7, 54 + c, 61), 3)
        for i, y in enumerate(cfg["rows"]):
            line(g, (28 + c, y + 18), (52 + c, y + 18), 3, 2)
            paint_rect(g, (40 + cfg["limit"][i], y - 1, 42 + cfg["limit"][i], y + 10), 2)
    paint_rect(g, common, 10)
    paint_rect(g, (common[0] + 2, common[1] + 1, common[2] - 2, common[3] - 1), 0)
    # Aperture backing stays visible when output material actually clears it.
    for box in apertures(h["level"]):
        paint_rect(g, box, 0)
    for i, q in enumerate(h["q"]):
        for p in parts(h["level"], i, q):
            fill_polygon(g, p, 14 if i == 0 else 9)
        # Attached return spring: visible frame anchor, zigzag and rack end.
        if cfg["orthogonal"] and i == 1:
            line(g, (17, 15), (17, 16 + q), 2)
            for t in range(0, q, 3):
                line(g, (17, 16 + t), (19, 17 + t), 0)
                line(g, (19, 17 + t), (17, 18 + t), 0)
            paint_rect(g, (16, 12, 20, 16), 2)
        else:
            y = 6 if cfg["orthogonal"] else cfg["rows"][i] + 4
            start = 2 if cfg["orthogonal"] else 4
            paint_rect(g, (0, y - 2, 2, y + 3), 2)
            line(g, (2, y), (start + q, y), 2)
            for t in range(0, q, 3):
                line(g, (2 + t, y), (3 + t, y - 2), 0)
                line(g, (3 + t, y - 2), (4 + t, y), 0)
        # Few broad shoulders on distinct holding and driving contours.
        for role in ("holder", "driver"):
            for tooth in cfg[role + "_teeth"][i]:
                if cfg["orthogonal"] and i == 1:
                    yy = 32 - tooth + q
                    xx = 4 if role == "holder" else 6
                    fill_polygon(g, [(xx, yy), (8, yy), (8, yy + 4)], 9)
                else:
                    yy = 4 if cfg["orthogonal"] else cfg["rows"][i]
                    xx = 24 - tooth + q if cfg["orthogonal"] else 32 - tooth + q
                    if role == "holder":
                        fill_polygon(g, [(xx, yy), (xx, yy - 4), (xx + 5, yy)], 14 if i == 0 else 9)
                    else:
                        bottom = 10 if cfg["orthogonal"] else yy + 8
                        fill_polygon(g, [(xx, bottom), (xx, bottom + 4), (xx + 5, bottom)], 14 if i == 0 else 9)
    for role, i, box in lever_boxes(h):
        enabled, bearing = h[role][i], seated(h, i, role)
        paint_rect(g, box, 2 if role == "holder" else 10)
        # Broad in-material lever posture: an actual lifted diagonal gap.
        x0, y0, x1, y1 = box
        if enabled:
            paint_rect(g, (x0 + 2, y0 + 2, x1 - 2, y1 - 2), 0 if bearing else 3)
        else:
            line(g, (x0 + 1, y1 - 2), (x1 - 2, y0 + 1), 5, 2)
        if cfg["orthogonal"] and i == 1:
            head_y = 32 + (h["c"] if role == "driver" else 0)
            head_x = 4 if role == "holder" else 6
            if not enabled:
                head_x = 0
            paint_rect(g, (head_x, head_y - 4, head_x + 3, head_y), 0 if bearing else (2 if enabled else 4))
            line(g, ((x0 + x1) // 2, (y0 + y1) // 2), (head_x, head_y), 2 if role == "holder" else 10)
        else:
            yy = 4 if cfg["orthogonal"] else cfg["rows"][i]
            xx = (24 if cfg["orthogonal"] else 32) + (h["c"] if role == "driver" else 0)
            head_y = (yy - 4 if role == "holder" else (10 if cfg["orthogonal"] else yy + 8))
            if not enabled:
                head_y += -4 if role == "holder" else 4
            paint_rect(g, (xx - 3, head_y, xx, head_y + 4), 0 if bearing else (2 if enabled else 4))
            line(g, ((x0 + x1) // 2, (y0 + y1) // 2), (xx - 2, head_y + 2), 2 if role == "holder" else 10)
    # Fixed goal jambs border the actual empty-space relation, not target numbers.
    for x0, y0, x1, y1 in apertures(h["level"]):
        paint_rect(g, (x0 - 1, y0 - 1, x1 + 1, y0), 11)
        paint_rect(g, (x0 - 1, y1, x1 + 1, y1 + 1), 11)
        paint_rect(g, (x0 - 1, y0, x0, y1), 11)
        paint_rect(g, (x1, y0, x1 + 1, y1), 11)
    if h["feedback"]:
        kind, i = h["feedback"]
        if kind == "stop" and not cfg["orthogonal"]:
            yy = cfg["rows"][i]
            paint_rect(g, (39 + cfg["limit"][i], yy, 42 + cfg["limit"][i], yy + 8), 8)
        elif kind == "contact":
            paint_rect(g, (34, 27 + h["q"][1], 38, 31 + h["q"][1]), 8)
        elif kind == "carriage":
            paint_rect(g, (common[0], common[1], common[0] + 2, common[3]), 8)
    return g


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


class V208(FunctionalGame):
    GAME_ID = 'v208-92ef1a3ddcf74643'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
