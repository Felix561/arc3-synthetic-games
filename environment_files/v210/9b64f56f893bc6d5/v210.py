"""Equal Company: persistent countable units and present group correspondence."""
from copy import deepcopy

LEVELS = {
    0: {"atoms": [(0, [(10, 32)]), (1, [(54, 32)])], "seams": [], "paired": []},
    1: {"atoms": [(0, [(10, 24), (10, 32), (10, 40)]), (1, [(49, 25), (56, 32), (49, 39)])], "seams": [], "paired": []},
    2: {"atoms": [(0, [(10, 21), (10, 27)]), (0, [(10, 43)]), (1, [(49, 25), (56, 32), (49, 39)])], "seams": [(0, 1, (10, 27), (10, 43), (10, 35), False)], "paired": []},
    3: {"atoms": [(0, [(10, 12)]), (0, [(10, 24)]), (0, [(10, 40), (10, 47)]), (1, [(54, 17), (54, 24)]), (1, [(54, 43), (54, 50)])], "seams": [(0, 1, (10, 12), (10, 24), (10, 18), True), (1, 2, (10, 24), (10, 40), (10, 32), True)], "paired": []},
    4: {"atoms": [(0, [(10, 9), (10, 16)]), (0, [(10, 31)]), (0, [(10, 47), (10, 54)]), (1, [(54, 9), (54, 16)]), (1, [(54, 36), (54, 44), (54, 52)])], "seams": [(0, 1, (10, 16), (10, 31), (10, 23), False)], "paired": []},
    5: {"atoms": [(0, [(9, 8), (16, 8)]), (0, [(10, 20)]), (0, [(10, 32), (17, 32), (17, 39)]), (0, [(10, 47), (17, 47)]), (0, [(10, 60), (17, 60)]), (1, [(54, 8), (54, 14)]), (1, [(49, 24), (56, 24), (49, 31), (56, 31)]), (1, [(54, 40), (54, 45)]), (1, [(54, 58), (60, 58)])], "seams": [(1, 2, (10, 20), (10, 32), (10, 26), False), (7, 8, (54, 45), (54, 58), (54, 51), True)], "paired": [((0,), (5,))]},
    6: {"atoms": [(0, [(9, 8), (16, 8)]), (0, [(10, 20)]), (0, [(10, 32), (17, 32), (17, 39)]), (0, [(10, 47), (17, 47)]), (0, [(10, 60), (17, 60)]), (1, [(54, 8), (54, 14)]), (1, [(49, 24), (56, 24), (49, 31), (56, 31)]), (1, [(54, 43), (54, 49)]), (1, [(54, 57), (60, 57)])], "seams": [(1, 2, (10, 20), (10, 32), (10, 26), False), (3, 4, (10, 47), (10, 60), (10, 54), True)], "paired": [((3, 4), (6,))]},
}


def get_initial_state(level_index):
    spec = LEVELS[level_index]
    return {"level": level_index, "closed": [s[5] for s in spec["seams"]],
            "pairs": deepcopy(spec["paired"]), "selected": None, "history": []}, {}


def predict(h_t, seed):
    return {}


def groups(h):
    spec = LEVELS[h["level"]]
    result = []
    unseen = set(range(len(spec["atoms"])))
    while unseen:
        todo = [min(unseen)]
        group = set()
        while todo:
            atom = todo.pop()
            if atom in group:
                continue
            group.add(atom)
            for active, seam in zip(h["closed"], spec["seams"]):
                if active and atom in seam[:2]:
                    todo.append(seam[1] if atom == seam[0] else seam[0])
        unseen -= group
        result.append(tuple(sorted(group)))
    return result


def units(h, group):
    spec = LEVELS[h["level"]]
    return sorted([(a, i, p) for a in group for i, p in enumerate(spec["atoms"][a][1])],
                  key=lambda u: (u[2][1], u[2][0], u[0], u[1]))


def side(h, group):
    return LEVELS[h["level"]]["atoms"][group[0]][0]


def grip(h, group):
    points = units(h, group)
    return (22 if side(h, group) == 0 else 41,
            round(sum(u[2][1] for u in points) / len(points)))


def _touch(point, x, y, radius):
    return abs(point[0] - x) <= radius and abs(point[1] - y) <= radius


def hit(h, x, y):
    spec = LEVELS[h["level"]]
    for index, seam in enumerate(spec["seams"]):
        if _touch(seam[4], x, y, 3):
            return ("seam", index)
    for group in groups(h):
        if _touch(grip(h, group), x, y, 3):
            return ("group", group)
        if any(_touch(u[2], x, y, 2) for u in units(h, group)):
            return ("group", group)
    return None


def _unpair(h, members):
    members = set(members)
    h["pairs"] = [pair for pair in h["pairs"] if not members.intersection(pair[0] + pair[1])]


def transition(h_t, z_t, action):
    h = deepcopy(h_t)
    if action == 7:
        if h["history"]:
            prior = h["history"].pop()
            return {**prior, "history": h["history"]}
        return h
    if not isinstance(action, tuple) or len(action) != 3 or action[0] != 6:
        return h
    target = hit(h, action[1], action[2])
    if target is None:
        return h
    prior = {key: deepcopy(value) for key, value in h.items() if key != "history"}
    if target[0] == "seam":
        index = target[1]
        first_atom, second_atom = LEVELS[h["level"]]["seams"][index][:2]
        touched = tuple(atom for group in groups(h) if first_atom in group or second_atom in group for atom in group)
        _unpair(h, touched)
        h["closed"][index] = not h["closed"][index]
        h["selected"] = None
    else:
        group = target[1]
        selected = h["selected"]
        if selected is None or side(h, selected) == side(h, group) and selected != group:
            h["selected"] = group
        elif selected == group:
            _unpair(h, group)
            h["selected"] = None
        else:
            _unpair(h, selected + group)
            pair = (selected, group) if side(h, selected) == 0 else (group, selected)
            h["pairs"].append(pair)
            h["selected"] = None
    h["history"].append(prior)
    return h


def correspondence(h):
    current = set(groups(h))
    links = []
    for left, right in h["pairs"]:
        if left in current and right in current and side(h, left) == 0 and side(h, right) == 1:
            links.extend(zip(units(h, left), units(h, right)))
    return links


def check_level_complete(h_t, z_t, level_index):
    spec = LEVELS[h_t["level"]]
    links = correspondence(h_t)
    left = [(u[0], u[1]) for u, v in links]
    right = [(v[0], v[1]) for u, v in links]
    population = [sum(len(points) for s, points in spec["atoms"] if s == side_id) for side_id in (0, 1)]
    return (population[0] == population[1] == len(links) and len(set(left)) == len(left)
            and len(set(right)) == len(right))


def _rect(frame, x0, y0, x1, y1, color):
    for y in range(max(0, y0), min(64, y1 + 1)):
        for x in range(max(0, x0), min(64, x1 + 1)):
            frame[y][x] = color


def _line(frame, p, q, color, width=1):
    distance = max(abs(q[0] - p[0]), abs(q[1] - p[1]))
    for t in range(distance + 1):
        x = round(p[0] + (q[0] - p[0]) * t / max(1, distance))
        y = round(p[1] + (q[1] - p[1]) * t / max(1, distance))
        r = width // 2
        _rect(frame, x-r, y-r, x+r, y+r, color)


def render(h_t, z_t):
    h = h_t
    spec = LEVELS[h["level"]]
    frame = [[5 for _ in range(64)] for _ in range(64)]
    linked = set()
    for left, right in correspondence(h):
        _line(frame, left[2], right[2], 1)
        linked.add((left[0], left[1]))
        linked.add((right[0], right[1]))
    # All connective material is beneath the separately countable bead bodies.
    for atom, (side_id, points) in enumerate(spec["atoms"]):
        for first, second in zip(points, points[1:]):
            _line(frame, first, second, 10, 3)
    # The reversible bridges keep their actual endpoints and broad joint grips.
    for active, seam in zip(h["closed"], spec["seams"]):
        p, q, center = seam[2:5]
        _line(frame, p, q, 1, 3)
        x, y = center
        _rect(frame, x-3, y-3, x+3, y+3, 0)
        _rect(frame, x-2, y-2, x+2, y+2, 5)
        if active:
            _rect(frame, x-1, y-3, x+1, y+3, 1)
        else:
            _rect(frame, x-1, y-3, x+1, y-2, 1)
            _rect(frame, x-1, y+2, x+1, y+3, 1)
    for group in groups(h):
        x, y = grip(h, group)
        _rect(frame, x-3, y-3, x+3, y+3, 0)
        _rect(frame, x-2, y-2, x+2, y+2, 5)
        if h["selected"] == group:
            _rect(frame, x-2, y-2, x+2, y+2, 7)
        else:
            _rect(frame, x, y-1, x, y+1, 0)
        for _, _, (ux, uy) in units(h, group):
            end = (ux+3, uy) if side(h, group) == 0 else (ux-3, uy)
            _line(frame, end, (x-4 if side(h, group) == 0 else x+4, y), 3)
    # A bead always owns its complete outline/interior above any bridge or trace.
    for atom, (side_id, points) in enumerate(spec["atoms"]):
        for i, (x, y) in enumerate(points):
            _rect(frame, x-2, y-2, x+2, y+2, 0)
            _rect(frame, x-1, y-1, x+1, y+1, 10)
            if (atom, i) in linked:
                _rect(frame, x-1, y-1, x+1, y+1, 0)
            else:
                frame[y][x] = 5
    if h["selected"] is not None:
        for _, _, (ux, uy) in units(h, h["selected"]):
            for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3)]:
                if 0 <= ux+dx < 64 and 0 <= uy+dy < 64:
                    frame[uy+dy][ux+dx] = 7
    return frame


def get_available_actions():
    return [6, 7]


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


class V210(FunctionalGame):
    GAME_ID = 'v210-9b64f56f893bc6d5'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
