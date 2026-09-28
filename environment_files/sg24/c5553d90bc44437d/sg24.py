FIXED_LEVELS = [{'floors': [8, 8, 8, 8, 8, 8, 8, 8, 8, 11, 11, 8, 8, 8, 8, 8, 8, 8, 8, 8], 'walker': [3, 7], 'bridge': [4, 7], 'length': 4, 'goal': [13, 7], 'ladders': [], 'blocks': []}, {'floors': [8, 8, 8, 8, 8, 8, 8, 8, 8, 11, 11, 8, 8, 8, 8, 8, 8, 8, 8, 8], 'walker': [17, 7], 'bridge': [13, 7], 'length': 4, 'goal': [6, 7], 'ladders': [], 'blocks': []}, {'floors': [7, 7, 7, 7, 7, 11, 11, 7, 7, 7, 7, 7, 7, 11, 11, 7, 7, 7, 7, 7], 'walker': [0, 6], 'bridge': [1, 6], 'length': 4, 'goal': [17, 6], 'ladders': [], 'blocks': []}, {'floors': [10, 10, 10, 10, 10, 10, 10, 10, 6, 6, 6, 6, 6, 6, 11, 11, 6, 6, 6, 6], 'walker': [5, 9], 'bridge': [1, 9], 'length': 4, 'goal': [18, 5], 'ladders': [[7, 5], [7, 6], [7, 7], [7, 8], [7, 9]], 'blocks': []}, {'floors': [7, 7, 7, 7, 11, 7, 7, 7, 7, 7, 11, 7, 7, 7, 7, 7, 11, 7, 7, 7], 'walker': [0, 6], 'bridge': [1, 6], 'length': 3, 'goal': [18, 6], 'ladders': [], 'blocks': []}, {'floors': [7, 7, 7, 7, 7, 7, 7, 7, 7, 4, 4, 4, 7, 7, 7, 11, 7, 7, 7, 7], 'walker': [8, 6], 'bridge': [5, 6], 'length': 3, 'goal': [18, 6], 'ladders': [[8, 3], [8, 4], [8, 5], [8, 6], [12, 3], [12, 4], [12, 5], [12, 6]], 'blocks': []}, {'floors': [7, 7, 7, 7, 11, 7, 7, 7, 7, 4, 4, 4, 7, 7, 7, 11, 7, 7, 7, 7], 'walker': [0, 6], 'bridge': [1, 6], 'length': 3, 'goal': [18, 6], 'ladders': [[8, 3], [8, 4], [8, 5], [8, 6], [12, 3], [12, 4], [12, 5], [12, 6]], 'blocks': []}]

from collections import deque

W = 20
H = 12
DIRS = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}


def initial(cfg):
    return tuple(cfg['walker']) + tuple(cfg['bridge']) + (0,)


def terrain(cfg):
    out = {(x, y) for x, floor in enumerate(cfg['floors']) for y in range(floor, H)}
    out.update(tuple(p) for p in cfg.get('blocks', []))
    return out


def ladders(cfg):
    return {tuple(p) for p in cfg['ladders']}


def bridge_cells(cfg, state):
    x, y, bx, by, side = state
    if side:
        bx, by = x + 1 if side > 0 else x - cfg['length'], y - 1
    return {(bx + i, by) for i in range(cfg['length'])}


def occupied(cfg, state, bridge_support=True):
    solid = terrain(cfg)
    if not state[4] and bridge_support:
        solid |= bridge_cells(cfg, state)
    return solid


def carried_clear(cfg, x, y, side):
    bx, by = x + 1 if side > 0 else x - cfg['length'], y - 1
    if bx < 0 or bx + cfg['length'] > W or not 0 <= by < H:
        return False
    return all((xx, by) not in terrain(cfg) for xx in range(bx, bx + cfg['length']))


def solved(cfg, state):
    return state[:2] == tuple(cfg['goal'])


def advance(cfg, state, action, bridge_support=True, allow_left_grab=True, allow_right_grab=True):
    x, y, bx, by, side = state
    solid = occupied(cfg, state, bridge_support)
    ladder = ladders(cfg)
    if action == 5:
        if side:
            nx = x + 1 if side > 0 else x - cfg['length']
            ny = y
            cells = {(nx + i, ny) for i in range(cfg['length'])}
            ground = terrain(cfg)
            # A horizontal bridge can be put down only with its two ends
            # supported. The rejected attempt changes neither object.
            if not cells & ground and (nx, ny + 1) in ground and (nx + cfg['length'] - 1, ny + 1) in ground:
                return x, y, nx, ny, 0
        elif y == by:
            if x == bx - 1 and allow_right_grab and carried_clear(cfg, x, y, 1):
                return x, y, bx, by, 1
            if x == bx + cfg['length'] and allow_left_grab and carried_clear(cfg, x, y, -1):
                return x, y, bx, by, -1
        return state
    if action not in DIRS:
        return state
    dx, dy = DIRS[action]
    nx, ny = x + dx, y + dy
    if not 0 <= nx < W or not 0 <= ny < H:
        return state
    if dy < 0 and (x, y) not in ladder and (nx, ny) not in ladder:
        return state
    if (nx, ny) in solid:
        if not dx or ny == 0 or (nx, ny - 1) in solid:
            return state
        ny -= 1  # One high edge can be stepped onto; a cliff cannot.
    if dy > 0 and (x, y) not in ladder and (nx, ny) in solid:
        return state
    while ny + 1 < H and (nx, ny + 1) not in solid and (nx, ny) not in ladder:
        ny += 1
    if side and not carried_clear(cfg, nx, ny, side):
        return state
    return nx, ny, bx, by, side


def search(cfg, limit=150000, **variants):
    start = initial(cfg)
    queue = deque([start])
    seen = {start: None}
    found = None
    while queue:
        s = queue.popleft()
        if solved(cfg, s):
            found = s
            break
        for a in (1, 2, 3, 4, 5):
            n = advance(cfg, s, a, **variants)
            if n not in seen:
                if len(seen) >= limit:
                    return {'solved': False, 'exhausted': False, 'states': len(seen), 'limit': limit}
                seen[n] = s, a
                queue.append(n)
    path = []
    if found is not None:
        cur = found
        while seen[cur] is not None:
            prev, a = seen[cur]
            path.append(a)
            cur = prev
        path.reverse()
    return {'solved': found is not None, 'exhausted': found is None and not queue,
            'states': len(seen), 'limit': limit, 'path': path}

import numpy as np
from arcengine import ARCBaseGame, Camera, Level, Sprite, GameAction


class Sg24(ARCBaseGame):
    def __init__(self, seed=0):
        self.cfg = None
        self.state = None
        self.history = []
        self.release_feedback = ()
        levels = [Level(sprites=[Sprite(pixels=np.full((64, 64), 5, dtype=np.int64), name='canyon')],
                        grid_size=(64, 64), data={'layout': cfg}, name='Span %d' % (i + 1))
                  for i, cfg in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg24-borrowed-span', levels=levels,
                         camera=Camera(background=5, letter_box=5), available_actions=[1, 2, 3, 4, 5, 7], seed=seed)

    def on_set_level(self, level):
        self.cfg = level.get_data('layout')
        self.state = initial(self.cfg)
        self.history = []
        self.release_feedback = ()
        self._paint()

    def step(self):
        a = 0 if self.action.id == GameAction.RESET else int(self.action.id.name[-1])
        if a == 7 and self.history:
            self.state, self.release_feedback = self.history.pop()
        elif a in (1, 2, 3, 4, 5):
            previous = (self.state, self.release_feedback)
            self.release_feedback = ()
            n = advance(self.cfg, self.state, a)
            if a == 5 and self.state[4] and n == self.state:
                x, y, _, _, side = self.state
                bx = x + 1 if side > 0 else x - self.cfg['length']
                ends = (bx, bx + self.cfg['length'] - 1)
                ground = terrain(self.cfg)
                missing = [xx for xx in ends if (xx, y + 1) not in ground]
                collided = [xx for xx in range(bx, bx + self.cfg['length']) if (xx, y) in ground]
                self.release_feedback = tuple(sorted(set(missing + collided)))
            if n != previous[0] or self.release_feedback != previous[1]:
                self.history.append(previous)
            self.state = n
        self._paint()
        if solved(self.cfg, self.state):
            self.next_level()
        self.complete_action()

    def _paint(self):
        c = np.full((64, 64), 5, dtype=np.int64)
        ox, oy, sx, sy = 2, 8, 3, 4
        # Continuous banks, not a board of cells. Their top edges make support
        # and the depth of each canyon visible at native resolution.
        for x, y in terrain(self.cfg):
            px, py = ox + sx * x, oy + sy * y
            c[py:py + sy, px:px + sx] = 4
            if (x, y - 1) not in terrain(self.cfg):
                c[py, px:px + sx] = 2
        # The ladder is attached to the adjacent cliff. No remote glyph is
        # needed to explain why the walker can go up here and not in midair.
        for x, y in ladders(self.cfg):
            px, py = ox + sx * x, oy + sy * y
            c[py:py + sy, px] = 3
            c[py:py + sy, px + 2] = 3
            c[py + 2, px:px + sx] = 2
        gx, gy = self.cfg['goal']
        px, foot = ox + sx * gx + 1, oy + sy * gy + sy - 1
        c[foot - 7:foot + 1, px - 2] = 10
        c[foot - 7:foot + 1, px + 2] = 10
        c[foot - 7, px - 2:px + 3] = 10
        # One coherent plank: a substantial beam with two contrasting end
        # faces. Picking an end lifts it into the walker's hand; putting it
        # down changes the physical surface that the walker can cross.
        cells = bridge_cells(self.cfg, self.state)
        bx = min(p[0] for p in cells)
        by = next(iter(cells))[1]
        px, py = ox + sx * bx, oy + sy * by
        width = sx * self.cfg['length']
        c[py:py + sy - 1, px:px + width] = 11
        c[py + sy - 1, px:px + width] = 12
        c[py:py + sy, px] = 12
        c[py:py + sy, px + width - 1] = 12
        # A rejected release marks only the end lacking support (or the
        # directly colliding part). The beam never teleports or pretends to
        # fall. Undo restores the exact previous stable drawing.
        for xx in self.release_feedback:
            fx = ox + sx * xx
            c[py:py + sy - 1, fx:fx + sx] = 8
        x, y, _, _, side = self.state
        px, foot = ox + sx * x + 1, oy + sy * y + sy - 1
        # A single connected, substantial body. Its feet touch the terrain;
        # its hand touches the carried end, making contact the action site.
        c[foot - 6:foot - 3, px - 1:px + 2] = 9
        c[foot - 3:foot, px] = 9
        c[foot, px - 1:px + 2] = 9
        c[foot - 5, px] = 10
        if side:
            hand_y = oy + sy * (y - 1) + 2
            c[hand_y:foot - 2, px + side] = 9
            if side > 0:
                c[hand_y, px:px + 3] = 9
            else:
                c[hand_y, px - 2:px + 1] = 9
        elif y == by and x == bx - 1:
            c[foot - 2, px:px + 3] = 9
        elif y == by and x == bx + self.cfg['length']:
            c[foot - 2, px - 2:px + 1] = 9
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=c, name='walker-and-borrowed-span', x=0, y=0, layer=0))
