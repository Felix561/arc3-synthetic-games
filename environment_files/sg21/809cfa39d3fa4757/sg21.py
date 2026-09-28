FIXED_LEVELS = [{'n': 3, 'goal': [2, 0, 1], 'cover': []}, {'n': 4, 'goal': [2, 3, 0, 1], 'cover': [1]}, {'n': 5, 'goal': [2, 0, 3, 4, 1], 'cover': [1, 3]}, {'n': 5, 'goal': [3, 0, 4, 2, 1], 'cover': [1, 2, 3]}, {'n': 6, 'goal': [3, 0, 2, 4, 5, 1], 'cover': [1, 2, 4]}, {'n': 6, 'goal': [3, 5, 2, 0, 4, 1], 'cover': [1, 2, 3, 4]}, {'n': 7, 'goal': [4, 3, 6, 2, 1, 0, 5], 'cover': [1, 2, 4, 5]}]

from collections import deque


def initial(cfg):
    return tuple(range(cfg['n']))


def advance(cfg, state, center):
    if type(center) is not int or not 1 <= center < cfg['n'] - 1:
        return state
    out = list(state)
    out[center - 1:center + 2] = [state[center + 1], state[center - 1], state[center]]
    return tuple(out)


def solved(cfg, state):
    return tuple(state) == tuple(cfg['goal'])


def centers(cfg):
    n = cfg['n']
    return tuple((32 - 4 * (n - 1) + 8 * i, 40) for i in range(n))


import numpy as np
from arcengine import ARCBaseGame, Camera, Level, Sprite, GameAction

COLORS = (8, 9, 11, 14, 12, 15, 6)


class Sg21(ARCBaseGame):
    def __init__(self, seed=0):
        self.cfg = None;self.state = None;self.history = [];self.peek = True;self.last = None
        levels = [Level(sprites=[Sprite(pixels=np.zeros((64, 64), dtype=np.int64), name='cups')],
                        grid_size=(64, 64), data={'layout': cfg}, name='Cups %d' % (i + 1))
                  for i, cfg in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg21-v1', levels=levels,
                         camera=Camera(background=5, letter_box=5),
                         available_actions=[5, 6, 7], seed=seed)

    def on_set_level(self, level):
        self.cfg = level.get_data('layout');self.state = initial(self.cfg)
        self.history = [];self.peek = True;self.last = None;self._paint()

    def step(self):
        a = 0 if self.action.id == GameAction.RESET else int(self.action.id.name[-1])
        if a == 7 and self.history:
            self.state, self.peek = self.history.pop();self.last = None
        elif a == 5:
            self.peek = True;self.last = None
        elif a == 6:
            d = self.action.data or {};x, y = d.get('x', -1), d.get('y', -1)
            if type(x) is int and type(y) is int:
                for i, (cx, _) in enumerate(centers(self.cfg)):
                    if abs(x-cx)>3:continue
                    if 21<=y<=34 and not self.peek and i in self.cfg['cover']:
                        self.peek=True;self.last=None;break
                    if 1<=i<self.cfg['n']-1 and (37<=y<=43 or 23<=y<=34):
                        self.history.append((self.state,self.peek))
                        self.state=advance(self.cfg,self.state,i)
                        self.peek=False;self.last=i;break
        self._paint()
        if solved(self.cfg, self.state):self.next_level()
        self.complete_action()

    def _paint(self):
        c = np.full((64, 64), 5, dtype=np.int64)
        for i, (cx, _) in enumerate(centers(self.cfg)):
            color = COLORS[self.cfg['goal'][i]]
            c[48, cx-3:cx+4] = color;c[56, cx-3:cx+4] = color
            c[48:57, cx-3] = color;c[48:57, cx+3] = color
            c[52:54, cx-1:cx+2] = 4
            if 0<i<self.cfg['n']-1:
                # The under-cup handle is the physical rotation control.
                c[39:41,cx-2:cx+3]=0;c[41,cx]=0
        for i, (cx, _) in enumerate(centers(self.cfg)):
            color = COLORS[self.state[i]]
            c[18, cx-3:cx+4] = 4;c[18:38, cx-4] = 4;c[18:38, cx+4] = 4
            c[36:38, cx-3:cx+4] = 3
            visible = self.peek or i not in self.cfg['cover']
            if visible:
                c[23:34, cx-3:cx+4] = color
                c[25:27, cx-1:cx+1] = 0
            else:
                c[22:34, cx-3:cx+4] = 3
                c[23, cx-2:cx+3] = 4;c[32, cx-2:cx+3] = 4
                c[27, cx] = 0
                # Lift tab is attached to the opaque cup; clicking its hood peeks.
                c[20,cx-2:cx+3]=0;c[21,cx-1:cx+2]=0
            if i == self.last or (self.last is not None and abs(i-self.last) == 1):
                c[19, cx-3:cx+4] = 0
        c[44, centers(self.cfg)[0][0]-4:centers(self.cfg)[-1][0]+5] = 4
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=c, name='occluded-cups', x=0, y=0, layer=0))
