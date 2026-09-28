import numpy as np
from arcengine import ARCBaseGame, Camera, Level, Sprite, GameAction


BG = 0
FLOOR = 1
WALL = 2
CUR_R = 3
CUR_L = 4
CUR_U = 5
CUR_D = 6
KEY_A = 7
GATE_A = 8
KEY_B = 9
GATE_B = 10
TARGET = 11
TARGET_DONE = 12
EXIT_OFF = 13
EXIT_ON = 14
CURSOR = 15
PROBE = 8

DIRS = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, 1),
}
MOVE_ACTIONS = {
    1: (0, -1),
    2: (0, 1),
    3: (-1, 0),
    4: (1, 0),
}
CURRENT_COLORS = {"R": CUR_R, "L": CUR_L, "U": CUR_U, "D": CUR_D}
KEY_COLORS = {"A": KEY_A, "B": KEY_B}
GATE_COLORS = {"A": GATE_A, "B": GATE_B}


FIXED_LEVELS = [
    {'name': 'sg01-0', 'start': [20, 32], 'floor_rects': [[20, 32, 28, 32]], 'walls': [], 'currents': [[25, 32, 'R'], [26, 32, 'R'], [27, 32, 'R']], 'keys': [[21, 32, 'A']], 'gates': [[23, 32, 'A']], 'targets': [], 'exit': [28, 32]},
    {
        "name": "sg01-1",
        "start": [7, 43],
        "floor_rects": [[7, 43, 17, 43], [17, 34, 17, 43], [17, 34, 36, 34], [36, 28, 36, 34], [24, 35, 26, 35]],
        "walls": [[25, 34]],
        "currents": [[17, 39, "U"], [17, 40, "U"], [17, 41, "U"], [17, 42, "U"], [20, 34, "R"], [21, 34, "R"], [22, 34, "R"], [23, 34, "R"], [24, 34, "R"]],
        "keys": [],
        "gates": [],
        "targets": [],
        "exit": [36, 28],
    },
    {
        "name": "sg01-2",
        "start": [8, 32],
        "floor_rects": [[8, 32, 48, 32], [22, 27, 22, 32], [48, 28, 48, 32]],
        "walls": [],
        "currents": [[12, 32, "R"], [13, 32, "R"], [14, 32, "R"], [15, 32, "R"]],
        "keys": [[22, 27, "A"]],
        "gates": [[34, 32, "A"]],
        "targets": [],
        "exit": [48, 28],
    },
    {
        "name": "sg01-3",
        "start": [9, 50],
        "floor_rects": [[9, 50, 22, 50], [22, 42, 22, 50], [22, 42, 41, 42], [41, 32, 41, 42], [41, 32, 52, 32], [52, 27, 52, 32]],
        "walls": [],
        "currents": [[22, 45, "U"], [22, 46, "U"], [22, 47, "U"], [22, 48, "U"], [22, 49, "U"], [28, 42, "R"], [29, 42, "R"], [30, 42, "R"], [31, 42, "R"], [32, 42, "R"], [33, 42, "R"], [34, 42, "R"], [35, 42, "R"]],
        "keys": [],
        "gates": [],
        "targets": [[22, 42], [41, 32]],
        "exit": [52, 27],
    },
    {
        "name": "sg01-4",
        "start": [9, 36],
        "floor_rects": [[9, 36, 23, 36], [23, 29, 23, 44], [23, 29, 43, 29], [43, 29, 43, 44], [24, 44, 43, 44], [43, 44, 52, 44]],
        "walls": [],
        "currents": [[23, 32, "U"], [23, 33, "U"], [23, 34, "U"], [23, 35, "U"], [26, 29, "R"], [27, 29, "R"], [28, 29, "R"], [29, 29, "R"], [30, 29, "R"], [31, 29, "R"], [32, 29, "R"], [33, 29, "R"], [34, 29, "R"], [35, 29, "R"], [36, 29, "R"], [43, 33, "D"], [43, 34, "D"], [43, 35, "D"], [43, 36, "D"], [43, 37, "D"], [43, 38, "D"], [43, 39, "D"], [43, 40, "D"], [43, 41, "D"], [43, 42, "D"]],
        "keys": [],
        "gates": [],
        "targets": [[43, 44]],
        "exit": [52, 44],
    },
    {
        "name": "sg01-5",
        "start": [8, 38],
        "floor_rects": [[8, 38, 49, 38], [16, 32, 16, 38], [30, 32, 30, 38], [49, 31, 49, 38], [49, 31, 55, 31], [18, 46, 30, 46], [30, 39, 30, 46]],
        "walls": [],
        "currents": [[10, 38, "R"], [11, 38, "R"], [12, 38, "R"]],
        "keys": [[16, 32, "A"], [30, 46, "B"]],
        "gates": [[24, 38, "A"], [41, 38, "B"], [22, 46, "B"]],
        "targets": [[49, 31]],
        "exit": [55, 31],
    },
    {
        "name": "sg01-6",
        "start": [6, 54],
        "floor_rects": [[6, 54, 18, 54], [18, 44, 18, 54], [18, 44, 34, 44], [34, 36, 34, 44], [34, 36, 50, 36], [50, 26, 50, 36], [40, 26, 50, 26], [40, 20, 40, 26], [40, 20, 56, 20]],
        "walls": [],
        "currents": [[18, 48, "U"], [18, 49, "U"], [18, 50, "U"], [18, 51, "U"], [18, 52, "U"], [18, 53, "U"], [22, 44, "R"], [23, 44, "R"], [24, 44, "R"], [25, 44, "R"], [26, 44, "R"], [27, 44, "R"], [28, 44, "R"], [50, 29, "U"], [50, 30, "U"], [50, 31, "U"], [50, 32, "U"], [50, 33, "U"], [50, 34, "U"], [50, 35, "U"]],
        "keys": [[34, 42, 'A'], [49, 26, 'B']],
        "gates": [[34, 40, "A"], [47, 26, "B"]],
        "targets": [[34, 44], [50, 36], [40, 20]],
        "exit": [56, 20],
    },
]


def action_id_value(action_id):
    if hasattr(action_id, "value"):
        return action_id.value
    return action_id


def expand_rects(rects):
    cells = []
    seen = set()
    for rect in rects:
        x0, y0, x1, y1 = rect
        left = min(x0, x1)
        right = max(x0, x1)
        top = min(y0, y1)
        bottom = max(y0, y1)
        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                pos = (x, y)
                if pos not in seen:
                    seen.add(pos)
                    cells.append(pos)
    return cells


def make_data(spec):
    return {
        "start": tuple(spec["start"]),
        "floor": expand_rects(spec["floor_rects"]),
        "walls": [tuple(p) for p in spec["walls"]],
        "currents": {(item[0], item[1]): item[2] for item in spec["currents"]},
        "keys": {(item[0], item[1]): item[2] for item in spec["keys"]},
        "gates": {(item[0], item[1]): item[2] for item in spec["gates"]},
        "targets": [tuple(p) for p in spec["targets"]],
        "exit": tuple(spec["exit"]),
    }


def make_level(spec):
    return Level(sprites=[], grid_size=(64, 64), data=make_data(spec), name=spec["name"])


class Sg01(ARCBaseGame):
    def __init__(self, seed=0):
        self.phase = 0
        self.nav_state = None
        self.undo_stack = []
        self.probe = None
        levels = [make_level(spec) for spec in FIXED_LEVELS]
        super().__init__(
            game_id="sg01-v1",
            levels=levels,
            camera=Camera(background=BG, letter_box=BG),
            available_actions=[1, 2, 3, 4, 5, 6, 7],
            seed=seed,
        )

    def on_set_level(self, level):
        self.nav_state = {
            "pos": tuple(level.get_data("start")),
            "keys": {"A": 0, "B": 0},
            "open": set(),
            "collected": set(),
            "visited": set(),
        }
        self.undo_stack = []
        self.probe = None
        self.phase = 0
        self._touch_current_cell()
        self._redraw()

    def step(self):
        raw_aid = self.action.id
        aid = action_id_value(raw_aid)
        if raw_aid == GameAction.RESET or aid == 0:
            self.complete_action()
            return
        if aid == 7:
            if self.undo_stack:
                self.nav_state = self.undo_stack.pop()
                self.probe = None
                self._redraw()
            self.complete_action()
            return
        if aid == 6:
            data = self.action.data or {}
            x = int(data.get("x", -1))
            y = int(data.get("y", -1))
            if 0 <= x < 64 and 0 <= y < 64:
                self.probe = (x, y)
                self._redraw()
            self.complete_action()
            return
        if aid in MOVE_ACTIONS:
            self._save_undo()
            self.probe = None
            dx, dy = MOVE_ACTIONS[aid]
            self._try_move(dx, dy)
            self._resolve_current()
            self._touch_current_cell()
            self._redraw()
            if self._is_complete():
                self.next_level()
            self.complete_action()
            return
        if aid == 5:
            self._save_undo()
            self.probe = None
            if not self._try_open_adjacent_gate():
                self._resolve_current()
            self._touch_current_cell()
            self._redraw()
            if self._is_complete():
                self.next_level()
            self.complete_action()
            return
        self.complete_action()

    def _data(self):
        return {
            "floor": [tuple(p) for p in self.current_level.get_data("floor")],
            "walls": set(tuple(p) for p in (self.current_level.get_data("walls") or [])),
            "currents": {tuple(k): v for k, v in (self.current_level.get_data("currents") or {}).items()},
            "keys": {tuple(k): v for k, v in (self.current_level.get_data("keys") or {}).items()},
            "gates": {tuple(k): v for k, v in (self.current_level.get_data("gates") or {}).items()},
            "targets": [tuple(p) for p in (self.current_level.get_data("targets") or [])],
            "exit": tuple(self.current_level.get_data("exit")),
        }

    def _save_undo(self):
        state = {
            "pos": self.nav_state["pos"],
            "keys": dict(self.nav_state["keys"]),
            "open": set(self.nav_state["open"]),
            "collected": set(self.nav_state["collected"]),
            "visited": set(self.nav_state["visited"]),
        }
        self.undo_stack.append(state)
        if len(self.undo_stack) > 24:
            self.undo_stack.pop(0)

    def _walkable(self, pos):
        d = self._data()
        if pos in d["walls"]:
            return False
        if pos in d["gates"] and pos not in self.nav_state["open"]:
            return False
        return pos in set(d["floor"])

    def _try_move(self, dx, dy):
        x, y = self.nav_state["pos"]
        nxt = (x + dx, y + dy)
        if self._walkable(nxt):
            self.nav_state["pos"] = nxt
            return True
        return False

    def _resolve_current(self):
        d = self._data()
        guard = 0
        while self.nav_state["pos"] in d["currents"] and guard < 64:
            direction = d["currents"][self.nav_state["pos"]]
            dx, dy = DIRS[direction]
            x, y = self.nav_state["pos"]
            nxt = (x + dx, y + dy)
            if not self._walkable(nxt):
                break
            self.nav_state["pos"] = nxt
            guard += 1
            if self.nav_state["pos"] not in d["currents"]:
                break
        return guard

    def _try_open_adjacent_gate(self):
        d = self._data()
        x, y = self.nav_state["pos"]
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            pos = (x + dx, y + dy)
            color = d["gates"].get(pos)
            if color and pos not in self.nav_state["open"] and self.nav_state["keys"].get(color, 0) > 0:
                self.nav_state["keys"][color] -= 1
                self.nav_state["open"].add(pos)
                return True
        return False

    def _touch_current_cell(self):
        d = self._data()
        pos = self.nav_state["pos"]
        if pos in d["keys"] and pos not in self.nav_state["collected"]:
            color = d["keys"][pos]
            self.nav_state["keys"][color] = self.nav_state["keys"].get(color, 0) + 1
            self.nav_state["collected"].add(pos)
        if pos in d["targets"]:
            self.nav_state["visited"].add(pos)

    def _is_complete(self):
        d = self._data()
        return self.nav_state["pos"] == d["exit"] and set(d["targets"]).issubset(self.nav_state["visited"])

    def _view(self):
        floor=self._data()['floor'];xs=[p[0] for p in floor];ys=[p[1] for p in floor]
        sx=min(5 if self.level_index==0 else 2,52/max(1,max(xs)-min(xs)));sy=min(4,42/max(1,max(ys)-min(ys)))
        return min(xs),min(ys),(64-(max(xs)-min(xs))*sx)/2,(64-(max(ys)-min(ys))*sy)/2,sx,sy

    def _redraw(self):
        grid=np.full((64,64),5,dtype=np.int64);d=self._data();x0,y0,ox,oy,sx,sy=self._view()
        def point(p):return round(ox+(p[0]-x0)*sx),round(oy+(p[1]-y0)*sy)
        def square(p,col,r=1):
            x,y=point(p);grid[y-r:y+r+1,x-r:x+r+1]=col
        floor=set(d['floor'])
        for p in floor:
            x,y=point(p);square(p,3)
            for dx,dy in ((1,0),(0,1)):
                q=(p[0]+dx,p[1]+dy)
                if q in floor:
                    a,b=point(q);grid[min(y,b)-1:max(y,b)+2,min(x,a)-1:max(x,a)+2]=3
        for p in d['walls']:square(p,8)
        for p,direction in d['currents'].items():
            square(p,9)
            if (p[0]+p[1])%4==0 or (p[0]-DIRS[direction][0],p[1]-DIRS[direction][1]) not in d['currents']:
                x,y=point(p);dx,dy=DIRS[direction]
                grid[y-dy*2,x-dx*2]=0;grid[y-dy,x-dx]=0;grid[y,x]=0;grid[y+dy,x+dx]=0
                grid[y+dx,x-dy]=0;grid[y-dx,x+dy]=0
        for p in d['targets']:
            square(p,14 if p in self.nav_state['visited'] else 11,2);square(p,5,1)
        ready=set(d['targets']).issubset(self.nav_state['visited']);square(d['exit'],14 if ready else 3,2);square(d['exit'],5,1)
        keycolors={'A':12,'B':10}
        for p,color in d['keys'].items():
            if p not in self.nav_state['collected']:
                square(p,keycolors[color],2);x,y=point(p);grid[y,x]=5
        for p,color in d['gates'].items():
            if p not in self.nav_state['open']:
                square(p,keycolors[color],2);x,y=point(p);grid[y-1:y+2,x]=5
        x,y=point(self.nav_state['pos']);grid[y-1:y+2,x-1:x+2]=0;grid[y,x]=5
        for i,color in enumerate(('A','B')):
            for k in range(self.nav_state['keys'][color]):grid[4:7,5+i*12+k*4:8+i*12+k*4]=keycolors[color]
        if self.probe is not None:
            px,py=self.probe
            if 0<=px<64 and 0<=py<64:grid[py,px]=11
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=grid,name='current-causeways',x=0,y=0,layer=0))
