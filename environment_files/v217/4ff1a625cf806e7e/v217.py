"""Nested Access: current spatial containment, not a remembered assembly recipe."""
from copy import deepcopy
import math


LEVELS = {
    0: {
        "bodies": [("a", 19, 19, 8, 1, 20, 27), ("b", 7, 7, 12, 1, 44, 27)],
        "parents": {}, "walls": [],
        "goal": {"root": "a", "pose": [20, 47, 1], "chain": ["a", "b"], "sides": [1, 1]},
    },
    1: {
        "bodies": [("a", 19, 19, 8, 1, 39, 25), ("b", 7, 7, 12, 1, 15, 25)],
        "parents": {}, "walls": [(25, 14, 27, 34)],
        "goal": {"root": "a", "pose": [39, 48, -1], "chain": ["a", "b"], "sides": [-1, 1]},
    },
    2: {
        "bodies": [("a", 23, 23, 8, 1, 17, 13), ("b", 11, 11, 12, 1, 48, 47),
                   ("t", 17, 17, 10, -1, 45, 13)],
        "parents": {}, "walls": [(22, 26, 35, 29)],
        "goal": {"root": "a", "pose": [17, 47, 1], "chain": ["a", "b"], "sides": [1, 1]},
    },
    3: {
        "bodies": [("a", 23, 23, 8, 1, 17, 13), ("b", 17, 17, 12, -1, 22, 13),
                   ("c", 11, 11, 9, -1, 17, 13)],
        "parents": {"b": ["a", 5, 0], "c": ["b", -5, 0]},
        "walls": [(2, 26, 5, 29), (29, 26, 45, 29)],
        "goal": {"root": "a", "pose": [17, 47, 1], "chain": ["a", "b", "c"], "sides": [1, -1, -1]},
    },
    4: {
        "bodies": [("a", 23, 23, 8, 1, 17, 13), ("b", 17, 17, 12, -1, 43, 47),
                   ("c", 11, 11, 9, 1, 43, 13), ("d", 5, 5, 14, 1, 13, 47)],
        "parents": {}, "walls": [(2, 26, 5, 29), (29, 26, 45, 29)],
        "goal": {"root": "a", "pose": [17, 47, 1], "chain": ["a", "b", "c", "d"], "sides": [1, -1, -1, 1]},
    },
    5: {
        "bodies": [("a", 23, 23, 8, 1, 17, 13), ("b", 17, 17, 12, -1, 43, 13),
                   ("c", 11, 11, 9, 1, 33, 13), ("d", 5, 5, 14, 1, 38, 13)],
        "parents": {"d": ["c", 5, 0]}, "walls": [(2, 26, 5, 29), (29, 26, 45, 29)],
        "goal": {"root": "a", "pose": [17, 47, 1], "chain": ["a", "b", "c", "d"], "sides": [1, -1, -1, 1]},
    },
    6: {
        "bodies": [("a", 23, 23, 8, 1, 17, 13), ("b", 17, 17, 12, -1, 22, 13),
                   ("c", 11, 11, 9, -1, 17, 13), ("d", 5, 5, 14, 1, 12, 13)],
        "parents": {"b": ["a", 5, 0], "c": ["b", -5, 0], "d": ["c", -5, 0]},
        "walls": [(2, 26, 5, 29), (29, 26, 45, 29)],
        "goal": {"root": "a", "pose": [17, 47, 1], "chain": ["a", "b", "c", "d"], "sides": [1, -1, 1, 1]},
    },
}


def get_available_actions():
    return [6, 7]


def _body(h, name):
    return h["bodies"][name]


def _position(h, name):
    b = _body(h, name)
    if b["parent"] is None:
        return b["x"], b["y"]
    x, y = _position(h, b["parent"])
    return x + b["dx"], y + b["dy"]


def _family(h, name):
    result = {name}
    for other, b in h["bodies"].items():
        if b["parent"] == name:
            result.update(_family(h, other))
    return result


def _children(h, name):
    return [k for k, b in h["bodies"].items() if b["parent"] == name]


def _root(h, name):
    seen = set()
    while _body(h, name)["parent"] is not None:
        if name in seen:
            raise ValueError("Containment cycle")
        seen.add(name)
        name = _body(h, name)["parent"]
    return name


def _local_pixels(b):
    w, v = b["w"] // 2, b["h"] // 2
    points = set()
    if b["w"] <= 7:
        for y in range(-v, v + 1):
            for x in range(-w, w + 1):
                if abs(x) + abs(y) <= w + v - 2:
                    points.add((b["side"] * x, b["side"] * y))
        return points
    for y in range(-v, v + 1):
        for x in range(-w, w + 1):
            spine = x <= -w + 3 and abs(y) < v - 1
            roof = y <= -v + 2 and -w + 2 <= x <= w - 2
            lower = y >= v - 2 and -w + 1 <= x <= w
            shoulder = x == -w + 1 and abs(y) <= v - 1
            if spine or roof or lower or shoulder:
                points.add((b["side"] * x, b["side"] * y))
    return points


def _pixels(h, name):
    x, y = _position(h, name)
    return {(x + dx, y + dy) for dx, dy in _local_pixels(_body(h, name))}


def _occupied(h, names=None):
    result = set()
    for name in h["bodies"] if names is None else names:
        result.update(_pixels(h, name))
    return result


def _walls(h):
    result = set()
    for x0, y0, x1, y1 in LEVELS[h["level"]]["walls"]:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                result.add((x, y))
    return result


def _mouth(h, name):
    b = _body(h, name)
    x, y = _position(h, name)
    return x + b["side"] * (b["w"] // 2 + 1), y


def _mouth_pixels(h, name):
    b = _body(h, name)
    if b["w"] <= 7:
        return set()
    x, y = _mouth(h, name)
    half = max(2, b["h"] // 2 - 4)
    return {(x + dx, y + dy) for dx in range(-1, 2) for dy in range(-half, half + 1)}


def _mouth_exposed(h, name):
    b = _body(h, name)
    if b["w"] <= 7:
        return False
    x, y = _mouth(h, name)
    own = _family(h, name)
    incoming = h["selected"]
    if incoming is not None and incoming not in own and _fits(h, incoming, name) and name not in _family(h, incoming):
        own = own | _family(h, incoming)
    solid = _occupied(h, set(h["bodies"]) - own) | _walls(h)
    root_name = _root(h, name)
    rx, ry = _position(h, root_name)
    reach = 3 if root_name == name else abs(rx - x) + _body(h, root_name)["w"] // 2 + 3
    for step in range(reach + 1):
        xx = x + b["side"] * step
        for yy in range(y - 2, y + 3):
            if (xx, yy) in solid:
                return False
    return True


def _snapshot(h):
    return {k: deepcopy(v) for k, v in h.items() if k != "history"}


def _push(old, new):
    new["history"] = old["history"] + [_snapshot(old)]
    new["history"] = new["history"][-128:]
    return new


def _cue(h, x, y, kind="blocked"):
    h["cue"] = [int(x), int(y), kind]
    return h


def _free_pixels(points, solid):
    return all(1 <= x <= 62 and 1 <= y <= 62 and (x, y) not in solid for x, y in points)


def _fits(h, child, host):
    a, b = _body(h, child), _body(h, host)
    return a["w"] <= b["w"] - 6 and a["h"] <= b["h"] - 6


def _inside(h, child, host):
    if not _fits(h, child, host):
        return False
    a, b = _body(h, child), _body(h, host)
    x, y = _position(h, child)
    hx, hy = _position(h, host)
    dx = (x - hx) * b["side"]
    return (dx - a["w"] // 2 >= -(b["w"] // 2) + 4
            and dx + a["w"] // 2 <= b["w"] // 2 + 2
            and abs(y - hy) + a["h"] // 2 <= b["h"] // 2 - 3)


def _dock(h, child, host):
    a, b = _body(h, child), _body(h, host)
    return b["side"] * (b["w"] // 2 - a["w"] // 2 + 2), 0


def _slide(h, name, target, attach=True):
    """Pixel sweep of the entire present subtree; empty cavities stay empty."""
    old_parent = _body(h, name)["parent"]
    if old_parent is not None and not _mouth_exposed(h, old_parent):
        return None
    x, y = _position(h, name)
    tx, ty = target
    own = _family(h, name)
    moving = _occupied(h, own)
    stationary = _occupied(h, set(h["bodies"]) - own) | _walls(h)
    steps = max(abs(tx - x), abs(ty - y), 1)
    for i in range(1, steps + 1):
        dx, dy = round((tx - x) * i / steps), round((ty - y) * i / steps)
        if not _free_pixels({(xx + dx, yy + dy) for xx, yy in moving}, stationary):
            return None
    n = deepcopy(h)
    n["bodies"][name].update(parent=None, x=tx, y=ty, dx=0, dy=0)
    if attach:
        hosts = [k for k in n["bodies"] if k not in own and _inside(n, name, k)]
        if hosts:
            host = min(hosts, key=lambda k: n["bodies"][k]["w"])
            if _children(n, host):
                return None
            hx, hy = _position(n, host)
            n["bodies"][name].update(parent=host, dx=tx - hx, dy=ty - hy)
        else:
            captured = [k for k, b in n["bodies"].items() if k not in own and b["parent"] is None and _inside(n, k, name)]
            if len(captured) > 1 or (captured and _children(n, name)):
                return None
            for child in captured:
                cx, cy = _position(n, child)
                n["bodies"][child].update(parent=name, dx=cx - tx, dy=cy - ty)
    n["cue"] = None
    return n


def _insert(h, child, host):
    if host in _family(h, child) or _children(h, host) or not _fits(h, child, host) or not _mouth_exposed(h, host):
        return None
    hx, hy = _position(h, host)
    dx, dy = _dock(h, child, host)
    n = _slide(h, child, (hx + dx, hy + dy), attach=False)
    if n is None:
        return None
    n["bodies"][child].update(parent=host, dx=dx, dy=dy)
    n["selected"] = None
    return n


def _withdraw(h, host):
    children = _children(h, host)
    if len(children) != 1 or not _mouth_exposed(h, host):
        return None
    child = children[0]
    b, c = _body(h, host), _body(h, child)
    x, y = _position(h, host)
    target = (x + b["side"] * (b["w"] // 2 + c["w"] // 2 + 1), y)
    n = _slide(h, child, target, attach=False)
    if n is not None:
        n["selected"] = child
    return n


def _turn(h, name):
    """Half-turn about the selected body, with its whole hierarchy attached."""
    x, y = _position(h, name)
    own = _family(h, name)
    moving = _occupied(h, own)
    stationary = _occupied(h, set(h["bodies"]) - own) | _walls(h)
    for i in range(1, 13):
        theta = math.pi * i / 12
        cosine, sine = math.cos(theta), math.sin(theta)
        rotated = {(x + round((xx - x) * cosine - (yy - y) * sine),
                    y + round((xx - x) * sine + (yy - y) * cosine)) for xx, yy in moving}
        if not _free_pixels(rotated, stationary):
            return None
    n = deepcopy(h)
    for item in own:
        n["bodies"][item]["side"] *= -1
        if item != name:
            n["bodies"][item]["dx"] *= -1
            n["bodies"][item]["dy"] *= -1
    n["cue"] = None
    return n


def get_initial_state(level):
    spec = LEVELS[level]
    bodies = {}
    for name, w, height, color, side, x, y in spec["bodies"]:
        bodies[name] = {"w": w, "h": height, "color": color, "side": side,
                        "x": x, "y": y, "parent": None, "dx": 0, "dy": 0}
    for child, (parent, dx, dy) in spec["parents"].items():
        bodies[child].update(parent=parent, dx=dx, dy=dy)
    h = {"level": level, "bodies": bodies, "selected": None, "cue": None, "history": []}
    return h, predict(h, 0)


def predict(h_t, seed):
    return {"mouths": {name: _mouth_exposed(h_t, name) for name in h_t["bodies"]}}


def transition(h_t, z_t, action):
    h = deepcopy(h_t)
    if action == 7:
        if not h["history"]:
            h["cue"] = None
            return h
        before = h["history"][-1]
        before["history"] = h["history"][:-1]
        return deepcopy(before)
    if not isinstance(action, tuple) or len(action) != 3 or action[0] != 6:
        return h
    x, y = action[1:]
    h["cue"] = None
    selected = h["selected"]
    mouths = [name for name in h["bodies"] if (x, y) in _mouth_pixels(h, name)]
    # Mouth controls are the physical foreground opening, not remote selectors.
    for host in sorted(mouths, key=lambda k: h["bodies"][k]["w"]):
        if not _mouth_exposed(h, host):
            continue
        if selected == host:
            n = _turn(h, host)
        elif selected is not None:
            n = _insert(h, selected, host)
        else:
            n = _withdraw(h, host)
        if n is not None:
            return _push(h_t, n)
        return _cue(h, x, y)
    # Descendants are painted first; the containing rim is foreground.
    order = sorted(h["bodies"], key=lambda k: len(_family(h, k)))
    hits = [name for name in order if (x, y) in _pixels(h, name)]
    if hits:
        name = hits[-1]
        h["selected"] = None if selected == name else name
        return h
    if mouths:
        return _cue(h, x, y, "covered")
    if selected is not None:
        n = _slide(h, selected, (x, y))
        return _push(h_t, n) if n is not None else _cue(h, x, y)
    return h


def _goal_state(h):
    n = deepcopy(h)
    goal = LEVELS[h["level"]]["goal"]
    chain = goal["chain"]
    for name in chain:
        n["bodies"][name]["parent"] = None
    x, y, side = goal["pose"]
    n["bodies"][chain[0]].update(x=x, y=y, side=side)
    for name, wanted_side in zip(chain, goal["sides"]):
        n["bodies"][name]["side"] = wanted_side
    for host, child in zip(chain, chain[1:]):
        dx, dy = _dock(n, child, host)
        n["bodies"][child].update(parent=host, dx=dx, dy=dy)
    return n


def check_level_complete(h_t, z_t, level):
    goal = LEVELS[level]["goal"]
    target = _goal_state(h_t)
    chain = goal["chain"]
    for name in chain:
        a, b = h_t["bodies"][name], target["bodies"][name]
        if a["parent"] != b["parent"] or (a["w"] > 7 and a["side"] != b["side"]) or _position(h_t, name) != _position(target, name):
            return False
    return _mouth_exposed(h_t, chain[0])


def render(h_t, z_t):
    h = h_t
    frame = [[0 for _ in range(64)] for _ in range(64)]
    def paint(points, color):
        for x, y in points:
            if 0 <= x < 64 and 0 <= y < 64:
                frame[y][x] = color
    paint(_walls(h), 3)
    # One whole anchored assembly is visible as broad pale material, not codes.
    wanted = _goal_state(h)
    chain = LEVELS[h["level"]]["goal"]["chain"]
    for name in reversed(chain):
        points = _pixels(wanted, name)
        paint(points, 1)
        edge = {p for p in points if any((p[0] + dx, p[1] + dy) not in points for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)])}
        paint(edge, h["bodies"][name]["color"])
    order = sorted(h["bodies"], key=lambda k: len(_family(h, k)))
    for name in order:
        points = _pixels(h, name)
        b = _body(h, name)
        paint(points, b["color"])
        edge = {p for p in points if any((p[0] + dx, p[1] + dy) not in points for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)])}
        paint(edge, 4)
        if h["selected"] == name:
            interior = points - edge
            paint(interior, 11)
    material_frame = [row[:] for row in frame]
    # Inactive faces stay behind every currently exposed foreground entry.
    for name in order:
        if _body(h, name)["w"] <= 7:
            continue
        if not _mouth_exposed(h, name):
            paint(_mouth_pixels(h, name) - _occupied(h) - _walls(h), 2)
    # Smaller exposed mouth faces are foreground, exactly as click priority.
    for name in sorted(h["bodies"], key=lambda k: h["bodies"][k]["w"], reverse=True):
        if _body(h, name)["w"] <= 7 or not _mouth_exposed(h, name):
            continue
        for xx, yy in _mouth_pixels(h, name):
            if 0 <= xx < 64 and 0 <= yy < 64:
                frame[yy][xx] = material_frame[yy][xx]
        x, y = _mouth(h, name)
        half = max(2, _body(h, name)["h"] // 2 - 4)
        rim = {p for p in _mouth_pixels(h, name) if p[0] in (x - 1, x + 1) or abs(p[1] - y) == half}
        paint(rim, _body(h, name)["color"])
    if h["cue"] is not None:
        x, y, kind = h["cue"]
        paint({(x+dx, y+dy) for dx in range(-2,3) for dy in range(-2,3) if max(abs(dx),abs(dy)) == 2}, 6)
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


class V217(FunctionalGame):
    GAME_ID = 'v217-4ff1a625cf806e7e'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
