"""Original last-seen pursuit toy. Native execution only in secured Docker."""
import copy

LEVELS = {
    0: {"destination": [34, 30], "bodies": [[26, 30]], "memories": [[34, 30]], "rests": [[28, 26]], "walls": []},
    1: {"destination": [30, 10], "bodies": [[14, 38]], "memories": [[30, 10]], "rests": [[18, 30]], "walls": [[26, 22, 45, 45]]},
    2: {"destination": [14, 14], "bodies": [[10, 34]], "memories": [[14, 14]], "rests": [[30, 18]], "walls": [[22, 22, 37, 45]]},
    3: {"destination": [14, 14], "bodies": [[14, 26]], "memories": [[14, 14]], "rests": [[42, 34]], "walls": [[22, 18, 37, 41]]},
    4: {"destination": [10, 14], "bodies": [[10, 46]], "memories": [[10, 14]], "rests": [[30, 30]], "walls": [[18, 22, 26, 41], [34, 22, 45, 41]]},
    5: {"destination": [10, 10], "bodies": [[10, 50]], "memories": [[10, 10]], "rests": [[34, 30]], "walls": [[18, 18, 30, 37], [38, 30, 49, 49]]},
    6: {"destination": [10, 14], "bodies": [[10, 42], [50, 42]], "memories": [[10, 14], [50, 14]], "rests": [[30, 30], [26, 50]], "walls": [[18, 22, 26, 41], [34, 22, 45, 41]]},
}

DIRECTIONS = {1: (0, -4), 2: (0, 4), 3: (-4, 0), 4: (4, 0)}

def _material(dx, dy, radius, shape=0):
    if radius == 4:
        return max(abs(dx), abs(dy)) >= 3
    return abs(dx)+abs(dy) <= radius if shape == 0 else (abs(dx) <= 1 or abs(dy) <= 1)

def _fits(p, radius, walls, shape=0):
    x, y = p
    if x-radius < 2 or y-radius < 2 or x+radius > 61 or y+radius > 61:
        return False
    for oy in range(-radius, radius+1):
        for ox in range(-radius, radius+1):
            if _material(ox, oy, radius, shape) and any(a <= x+ox <= c and b <= y+oy <= d for a,b,c,d in walls):
                return False
    return True

def _sweep_fits(old, new, radius, walls, shape=0):
    dx, dy = new[0]-old[0], new[1]-old[1]
    size = max(abs(dx), abs(dy))
    return all(_fits([old[0]+dx*i//size, old[1]+dy*i//size], radius, walls, shape)
               for i in range(1, size+1)) if size else True

def _sight(a, b, walls):
    # Exact closed segment/axis-aligned rectangle intersection, including edges.
    for left, top, right, bottom in walls:
        low, high = 0.0, 1.0
        for start, change, minimum, maximum in ((a[0], b[0]-a[0], left, right),
                                                (a[1], b[1]-a[1], top, bottom)):
            if change == 0:
                if start < minimum or start > maximum:
                    low, high = 1.0, 0.0
                    break
            else:
                u, v = (minimum-start)/change, (maximum-start)/change
                low, high = max(low, min(u, v)), min(high, max(u, v))
        if low <= high:
            return False
    return True

def _choices(position, remembered):
    dx, dy = remembered[0]-position[0], remembered[1]-position[1]
    axes = (0, 1) if abs(dx) >= abs(dy) else (1, 0)
    result = []
    for axis in axes:
        delta = (dx, dy)[axis]
        if delta:
            step = [0, 0]
            step[axis] = 2 if delta > 0 else -2
            result.append([position[0]+step[0], position[1]+step[1]])
    return result

def _overlap(a, shape_a, b, shape_b):
    if abs(a[0]-b[0]) > 4 or abs(a[1]-b[1]) > 4:
        return False
    for oy in range(-2,3):
        for ox in range(-2,3):
            rx, ry = a[0]+ox-b[0], a[1]+oy-b[1]
            if _material(ox,oy,2,shape_a) and -2 <= rx <= 2 and -2 <= ry <= 2 and _material(rx,ry,2,shape_b):
                return True
    return False

def _advance(destination, bodies, memories, rests, walls):
    new_bodies, new_memories, headings = [], [], []
    for i, (body, memory, rest) in enumerate(zip(bodies, memories, rests)):
        # A seated body currently rests; this rule has no latch/history flag.
        if body == rest:
            new_bodies.append(list(body)); new_memories.append(list(memory)); headings.append([0, 0])
            continue
        remembered = list(destination) if _sight(body, destination, walls) else list(memory)
        moved = next((p for p in _choices(body, remembered) if _sweep_fits(body, p, 2, walls, i)), list(body))
        new_bodies.append(moved); new_memories.append(remembered)
        headings.append([(moved[0]-body[0])//2, (moved[1]-body[1])//2])
    # Simultaneous physical-body occupancy, independent of iteration order.
    # The movable destination is an observation marker, not a second body.
    blocked = set()
    for i in range(len(bodies)):
        for j in range(i+1,len(bodies)):
            if _overlap(new_bodies[i],i,new_bodies[j],j):
                blocked.update((i,j))
        dx,dy=new_bodies[i][0]-bodies[i][0],new_bodies[i][1]-bodies[i][1]
        size=max(abs(dx),abs(dy))
        for step in range(1,size+1):
            p=[bodies[i][0]+dx*step//size,bodies[i][1]+dy*step//size]
            if any(j!=i and _overlap(p,i,old,j) for j,old in enumerate(bodies)):
                blocked.add(i)
    for i in blocked:
        new_bodies[i]=list(bodies[i]);headings[i]=[0,0]
    return new_bodies, new_memories, headings

def get_initial_state(level_index):
    c = LEVELS[level_index]
    h = {"level": level_index, "destination": list(c["destination"]),
         "bodies": copy.deepcopy(c["bodies"]), "memories": copy.deepcopy(c["memories"]),
         "headings": [[0, 0] for _ in c["bodies"]], "blocked": False, "history": []}
    return h, predict(h, 0)

def transition(h_t, z_t, action):
    h = copy.deepcopy(h_t)
    if action == 7:
        if h["history"]:
            old = h["history"].pop()
            h.update(old)
        return h
    if action not in DIRECTIONS:
        return h
    c = LEVELS[h["level"]]
    previous = {k: copy.deepcopy(v) for k, v in h.items() if k != "history"}
    h["history"].append(previous)
    dx, dy = DIRECTIONS[action]
    dest = [h["destination"][0]+dx, h["destination"][1]+dy]
    if not _sweep_fits(h["destination"], dest, 4, c["walls"]):
        h["blocked"] = True
        return h
    h["blocked"] = False
    h["destination"] = dest
    h["bodies"], h["memories"], h["headings"] = _advance(dest, h["bodies"], h["memories"], c["rests"], c["walls"])
    return h

def predict(h_t, seed):
    c = LEVELS[h_t["level"]]
    return {"visible": [_sight(p, h_t["destination"], c["walls"]) for p in h_t["bodies"]],
            "route_candidates": [[] if p == rest else _choices(p, m)
                                 for p, m, rest in zip(h_t["bodies"], h_t["memories"], c["rests"])]}

def check_level_complete(h_t, z_t, level_index):
    return h_t["level"] == level_index and h_t["bodies"] == LEVELS[level_index]["rests"]

def render(h_t, z_t):
    c = LEVELS[h_t["level"]]
    pixels = [[0]*64 for _ in range(64)]
    def rectangle(a, b, c, d, color):
        for y in range(max(0, b), min(64, d+1)):
            for x in range(max(0, a), min(64, c+1)):
                pixels[y][x] = color
    rectangle(0, 0, 63, 1, 1); rectangle(0, 62, 63, 63, 1)
    rectangle(0, 0, 1, 63, 1); rectangle(62, 0, 63, 63, 1)
    for a, b, d, e in c["walls"]:
        rectangle(a, b, d, e, 3)
    x, y = h_t["destination"]
    rectangle(x-4, y-4, x+4, y+4, 14)
    rectangle(x-2, y-2, x+2, y+2, 0)
    if h_t["blocked"]:
        rectangle(x-2, y-4, x+2, y-3, 11)
    # Fixed rests remain whole above all moving paint; distinct diamond/plus contours.
    for i, (x, y) in enumerate(c["rests"]):
        color = (12, 15)[i]
        for oy in range(-3, 4):
            for ox in range(-3, 4):
                edge = abs(ox)+abs(oy) == 3 if i == 0 else (_material(ox,oy,3,i) and any(not (-3 <= ox+dx <= 3 and -3 <= oy+dy <= 3 and _material(ox+dx,oy+dy,3,i)) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))))
                if edge:
                    pixels[y+oy][x+ox] = color
    for i, (x, y) in enumerate(h_t["bodies"]):
        color = (12, 15)[i]
        for oy in range(-2, 3):
            for ox in range(-2, 3):
                if _material(ox,oy,2,i):
                    pixels[y+oy][x+ox] = color
    return pixels

def get_available_actions():
    return [1, 2, 3, 4, 7]


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


class V218(FunctionalGame):
    GAME_ID = 'v218-917a3aaf08b0e772'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
