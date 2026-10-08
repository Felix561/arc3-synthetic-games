"""Room Stitch: coherent local floors transported between real edge contacts."""
import copy
import numpy as np

DIRS = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}
TYPES = {
    'west': {'cells': [(0,0),(1,0),(0,1),(1,1),(2,1),(0,2),(1,2)], 'ports': [(2,1,1,0)], 'grip': None},
    'east': {'cells': [(1,0),(2,0),(0,1),(1,1),(2,1),(1,2),(2,2)], 'ports': [(0,1,-1,0)], 'grip': None},
    'south': {'cells': [(1,0),(0,1),(1,1),(2,1),(0,2),(1,2),(2,2)], 'ports': [(1,0,0,-1)], 'grip': None},
    'bar': {'cells': [(0,0),(1,0),(0,1),(1,1),(2,1),(1,2),(2,2)], 'ports': [(0,1,-1,0),(2,1,1,0)], 'grip': (1,1)},
    'bend': {'cells': [(0,0),(1,0),(0,1),(1,1),(2,1),(1,2),(2,2)], 'ports': [(0,1,-1,0),(1,2,0,1)], 'grip': (1,1)},
    'rise': {'cells': [(1,0),(2,0),(0,1),(1,1),(2,1),(0,2),(1,2)], 'ports': [(1,0,0,-1),(2,1,1,0)], 'grip': (1,1)},
}

# Every stage declares present geometry and goals. No route or win-history state.
LEVELS = {
    0: {'rooms': [('bar',(1,3)),('east',(6,3))], 'walkers': [(0,2,1)], 'goals': [(1,1,1)], 'rocks': []},
    1: {'rooms': [('bar',(6,3)),('west',(1,3))], 'walkers': [(0,0,1)], 'goals': [(1,1,1)], 'rocks': []},
    2: {'rooms': [('bend',(4,2)),('west',(0,0)),('south',(6,6))], 'walkers': [(0,0,1)], 'goals': [(2,1,1)], 'rocks': []},
    3: {'rooms': [('west',(0,0)),('bend',(3,0)),('rise',(0,6)),('east',(7,6))], 'walkers': [(0,2,1)], 'goals': [(3,1,1)], 'rocks': []},
    4: {'rooms': [('west',(0,0)),('bend',(3,0)),('rise',(4,6)),('east',(7,6))], 'walkers': [(1,1,1),(2,1,1)], 'goals': [(3,1,1),(0,1,1)], 'rocks': [(6,3),(7,3),(6,4),(7,4),(6,5)]},
    5: {'rooms': [('west',(0,0)),('bend',(3,0)),('rise',(0,6)),('east',(7,6)),('bar',(3,3))], 'walkers': [(1,1,1),(4,1,1)], 'goals': [(3,1,1),(0,1,1)], 'rocks': []},
    6: {'rooms': [('west',(0,0)),('bend',(0,3)),('rise',(4,6)),('east',(7,6))], 'walkers': [(1,1,1),(2,1,1),(0,2,1)], 'goals': [(3,1,1),(0,1,1),(3,1,2)], 'rocks': [(6,3),(7,3),(6,4),(7,4),(6,5)]},
}


def _cfg(h):
    return LEVELS[h['level']]


def _kind(h, room):
    return TYPES[_cfg(h)['rooms'][room][0]]


def _world(h, body):
    room, x, y = body
    ox, oy = h['poses'][room]
    return ox + x, oy + y


def _room_cells(h, room, pose=None):
    ox, oy = h['poses'][room] if pose is None else pose
    return {(ox+x, oy+y) for x, y in _kind(h, room)['cells']}


def _ports(h, room):
    ox, oy = h['poses'][room]
    return [(ox+x, oy+y, dx, dy) for x, y, dx, dy in _kind(h, room)['ports']]


def _free_pose(h, room, pose):
    cells = _room_cells(h, room, pose)
    if any(not (0 <= x < 10 and 0 <= y < 10) for x, y in cells):
        return False
    occupied = set(_cfg(h)['rocks'])
    for other in range(len(h['poses'])):
        if other != room:
            occupied.update(_room_cells(h, other))
    return not bool(cells & occupied)


def _placement(h, room, receiver, port):
    """Align opposing physical edge cells; never map a label to a remote exit."""
    if room == receiver or _kind(h, room)['grip'] is None:
        return None
    x, y, dx, dy = _ports(h, receiver)[port]
    local = [p for p in _kind(h, room)['ports'] if p[2:] == (-dx,-dy)]
    if len(local) != 1:
        return None
    lx, ly, _, _ = local[0]
    return x + dx - lx, y + dy - ly


def _connected(h, a, b):
    """True only for adjacent, opposing open edges in the current drawing."""
    ar, ax, ay = a
    br, bx, by = b
    if ar == br:
        return True
    aw = _world(h, a)
    bw = _world(h, b)
    delta = bw[0]-aw[0], bw[1]-aw[1]
    return (ax,ay,delta[0],delta[1]) in _kind(h, ar)['ports'] and (bx,by,-delta[0],-delta[1]) in _kind(h, br)['ports']


def _destination(h, walker, direction):
    wx, wy = _world(h, h['walkers'][walker])
    dx, dy = DIRS[direction]
    target = wx+dx, wy+dy
    if any(i != walker and _world(h, body) == target for i, body in enumerate(h['walkers'])):
        return None
    for room in range(len(h['poses'])):
        ox, oy = h['poses'][room]
        local = target[0]-ox, target[1]-oy
        if local in _kind(h, room)['cells']:
            body = (room,local[0],local[1])
            return body if _connected(h, h['walkers'][walker], body) else None
    return None


def _snapshot(h):
    return {key: copy.deepcopy(value) for key, value in h.items() if key != 'history'}


def get_initial_state(level):
    level = int(level)
    cfg = LEVELS[level]
    h = {'level': level, 'poses': [tuple(pose) for _, pose in cfg['rooms']],
         'walkers': [tuple(body) for body in cfg['walkers']], 'active': 0,
         'selected': None, 'feedback': None, 'history': []}
    return h, {}


def predict(h_t, seed):
    return {}


def get_available_actions():
    return [1, 2, 3, 4, 6, 7]


def _center(cell):
    return 5 + 6*cell[0], 5 + 6*cell[1]


def _mouth_rect(port):
    x, y, dx, dy = port
    cx, cy = _center((x,y))
    # A substantial visible lip, with the exact same paint and hit footprint.
    if dx < 0:
        return cx-3,cy-2,cx,cy+1
    if dx > 0:
        return cx-1,cy-2,cx+2,cy+1
    if dy < 0:
        return cx-2,cy-3,cx+1,cy
    return cx-2,cy-1,cx+1,cy+2


def _inside(point, rect):
    x, y = point
    x0, y0, x1, y1 = rect
    return x0 <= x <= x1 and y0 <= y <= y1


def transition(h_t, z_t, action):
    h = copy.deepcopy(h_t)
    number = action[0] if isinstance(action, (tuple,list)) else action
    if number == 7:
        if h['history']:
            old = h['history'].pop()
            old['history'] = h['history']
            return old
        return h
    if number not in get_available_actions():
        return h
    old = _snapshot(h)
    h['feedback'] = None
    if number in DIRS:
        body = _destination(h, h['active'], number)
        if body is not None:
            h['walkers'][h['active']] = body
        else:
            h['feedback'] = _world(h, h['walkers'][h['active']])
    elif number == 6:
        if not isinstance(action, (tuple,list)) or len(action) != 3:
            return h_t
        point = int(action[1]),int(action[2])
        handled = False
        selected = h['selected']
        # The whole visibly painted body always controls that walker. A body
        # occluding a mouth never secretly becomes a room-placement control.
        for walker, body in enumerate(h['walkers']):
            cx, cy = _center(_world(h, body))
            if (point[0]-cx,point[1]-cy) in _shape_cells(walker):
                h['active'] = walker
                h['selected'] = None
                handled = True
                break
        if not handled and selected is not None:
            for receiver in range(len(h['poses'])):
                if receiver == selected:
                    continue
                for port, edge in enumerate(_ports(h, receiver)):
                    if _inside(point, _mouth_rect(edge)):
                        pose = _placement(h, selected, receiver, port)
                        if pose is not None and _free_pose(h, selected, pose):
                            h['poses'][selected] = pose
                            h['selected'] = None
                        else:
                            h['feedback'] = edge[:2]
                        handled = True
                        break
                if handled:
                    break
        if not handled:
            for room in range(len(h['poses'])):
                grip = _kind(h, room)['grip']
                if grip is None:
                    continue
                ox, oy = h['poses'][room]
                cx, cy = _center((ox+grip[0],oy+grip[1]))
                if _inside(point,(cx-3,cy-3,cx+2,cy+2)):
                    h['selected'] = None if selected == room else room
                    handled = True
                    break
        if not handled:
            h['selected'] = None
    if _snapshot(h) != old:
        h['history'].append(old)
        h['history'] = h['history'][-256:]
    return h


def check_level_complete(h_t, z_t, level):
    if h_t['level'] != level:
        return False
    return all(tuple(body) == tuple(goal) for body, goal in zip(h_t['walkers'], LEVELS[level]['goals']))


def _rect(frame, x0,y0,x1,y1,color):
    x0, x1 = max(0,x0), min(63,x1)
    y0, y1 = max(0,y0), min(63,y1)
    if x0 <= x1 and y0 <= y1:
        frame[y0:y1+1,x0:x1+1] = color


def _shape_cells(identity):
    if identity == 0:
        cells = [(x,y) for y in range(-2,3) for x in range(-2,3) if x*x+y*y <= 5]
    elif identity == 1:
        cells = [(x,y) for y in range(-2,3) for x in range(-2,3)]
    else:
        cells = [(x,y) for y in range(-2,3) for x in range(-2,3) if abs(x)+abs(y) <= 2]
    return cells


def _shape(frame, cx, cy, identity, color, outline=False):
    # Three visibly distinct compact bodies and matching fixed exit hollows.
    cells = _shape_cells(identity)
    for x,y in cells:
        if not outline or (x,y) not in {(0,0),(1,0),(-1,0),(0,1),(0,-1)}:
            if 0 <= cx+x < 64 and 0 <= cy+y < 64:
                frame[cy+y,cx+x] = color


def render(h_t, z_t):
    h = h_t
    frame = np.full((64,64),3,dtype=np.int8)
    for x,y in _cfg(h)['rocks']:
        cx,cy = _center((x,y))
        _rect(frame,cx-3,cy-3,cx+2,cy+2,2)
    for room in range(len(h['poses'])):
        cells = _room_cells(h,room)
        mobile = _kind(h,room)['grip'] is not None
        for x,y in cells:
            cx,cy = _center((x,y))
            _rect(frame,cx-3,cy-3,cx+2,cy+2,1 if mobile else 2)
        # Outlines enclose coherent floor masses; only actual mouths open them.
        for x,y in cells:
            cx,cy = _center((x,y))
            for dx,dy in ((0,-1),(0,1),(-1,0),(1,0)):
                if (x+dx,y+dy) in cells:
                    continue
                if dx:
                    ex = cx-3 if dx < 0 else cx+2
                    _rect(frame,ex,cy-3,ex,cy+2,0)
                else:
                    ey = cy-3 if dy < 0 else cy+2
                    _rect(frame,cx-3,ey,cx+2,ey,0)
        for edge in _ports(h,room):
            x,y,dx,dy = edge
            connected = False
            for other in range(len(h['poses'])):
                if other != room and (x+dx,y+dy,-dx,-dy) in _ports(h,other):
                    connected = True
            offer = h['selected'] is not None and h['selected'] != room
            color = 10 if offer or not connected else 1
            x0,y0,x1,y1 = _mouth_rect(edge)
            _rect(frame,x0,y0,x1,y1,color)
        grip = _kind(h,room)['grip']
        if grip is not None:
            ox,oy = h['poses'][room]
            cx,cy = _center((ox+grip[0],oy+grip[1]))
            color = 11 if h['selected'] == room else 0
            _rect(frame,cx-3,cy-3,cx+2,cy-3,color)
            _rect(frame,cx-3,cy+2,cx+2,cy+2,color)
            _rect(frame,cx-3,cy-3,cx-3,cy+2,color)
            _rect(frame,cx+2,cy-3,cx+2,cy+2,color)
    colors = (7,8,12)
    for walker,goal in enumerate(_cfg(h)['goals']):
        cx,cy = _center(_world(h,goal))
        _shape(frame,cx,cy,walker,colors[walker],outline=True)
    for walker,body in enumerate(h['walkers']):
        cx,cy = _center(_world(h,body))
        # White body perimeter retains the identity beside the exit hollow.
        _shape(frame,cx,cy,walker,0)
        _rect(frame,cx-1,cy-1,cx+1,cy+1,colors[walker])
        if walker == h['active']:
            frame[cy,cx] = 3
    if h['feedback'] is not None:
        cx,cy = _center(h['feedback'])
        _rect(frame,cx-2,cy-3,cx+1,cy-3,4)
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


class V215(FunctionalGame):
    GAME_ID = 'v215-b78be6f260e52882'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
