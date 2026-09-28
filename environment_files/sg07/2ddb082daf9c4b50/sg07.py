FIXED_LEVELS = [{'tools': [{'shape': [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]], 'color': 10, 'uses': 1}], 'blocked': [], 'rotate_mask': False, 'initial': [], 'target': [[0, 0, 0, 0, 0], [0, 10, 0, 0, 0], [0, 10, 0, 0, 0], [0, 10, 10, 10, 0], [0, 0, 0, 0, 0]]}, {'tools': [{'shape': [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]], 'color': 10, 'uses': 1}, {'shape': [[0, 0], [1, 0], [2, 0], [1, 1]], 'color': 12, 'uses': 1}], 'blocked': [], 'rotate_mask': False, 'initial': [], 'target': [[0, 0, 0, 0, 0], [10, 10, 10, 12, 0], [10, 0, 12, 12, 12], [10, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}, {'tools': [{'shape': [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1], [0, 2], [1, 2], [2, 2]], 'color': 10, 'uses': 1}, {'shape': [[0, 0], [1, 0], [2, 0]], 'color': 12, 'uses': 1}], 'blocked': [[2, 2], [1, 0]], 'rotate_mask': False, 'initial': [], 'target': [[12, 0, 12, 0, 0], [0, 10, 10, 10, 0], [0, 10, 0, 10, 0], [0, 10, 10, 10, 0], [0, 0, 0, 0, 0]]}, {'tools': [{'shape': [[0, 0], [1, 0], [0, 1], [1, 1]], 'color': 10, 'uses': 1}, {'shape': [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1], [0, 2], [1, 2], [2, 2]], 'color': 12, 'uses': 1}, {'shape': [[0, 0], [1, 0], [2, 0]], 'color': 0, 'uses': 1}], 'blocked': [], 'rotate_mask': False, 'initial': [], 'target': [[0, 12, 12, 12, 0], [0, 10, 10, 0, 0], [0, 12, 12, 12, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}, {'tools': [{'shape': [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1], [0, 2], [1, 2], [2, 2]], 'color': 10, 'uses': 1}, {'shape': [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1], [0, 2], [1, 2], [2, 2]], 'color': 12, 'uses': 1}, {'shape': [[0, 0], [0, 1], [1, 1]], 'color': 0, 'uses': 1}], 'blocked': [[4, 1]], 'rotate_mask': False, 'initial': [], 'target': [[0, 0, 0, 0, 0], [10, 10, 10, 12, 0], [10, 10, 10, 0, 12], [10, 10, 12, 12, 12], [0, 0, 0, 0, 0]]}, {'tools': [{'shape': [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1], [0, 2], [1, 2], [2, 2]], 'color': 10, 'uses': 1}, {'shape': [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]], 'color': 12, 'uses': 1}, {'shape': [[0, 0], [1, 0], [1, 1], [2, 1]], 'color': 6, 'uses': 1}, {'shape': [[0, 0], [1, 0], [2, 0]], 'color': 0, 'uses': 1}], 'blocked': [[1, 1], [2, 3], [4, 0]], 'rotate_mask': True, 'initial': [], 'target': [[0, 0, 12, 12, 12], [10, 0, 10, 0, 12], [10, 10, 6, 0, 12], [10, 10, 6, 0, 0], [0, 0, 0, 0, 0]]}, {'tools': [{'shape': [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1], [0, 2], [1, 2], [2, 2]], 'color': 10, 'uses': 1}, {'shape': [[0, 0], [1, 0], [2, 0], [1, 1]], 'color': 12, 'uses': 2}, {'shape': [[0, 0], [1, 0], [1, 1], [2, 1]], 'color': 6, 'uses': 1}, {'shape': [[0, 0], [0, 1], [1, 1]], 'color': 0, 'uses': 2}], 'blocked': [[1, 1], [3, 2], [0, 4]], 'rotate_mask': True, 'initial': [], 'target': [[0, 12, 0, 0, 0], [12, 0, 12, 0, 0], [0, 12, 12, 12, 0], [0, 0, 10, 6, 0], [0, 0, 0, 0, 0]]}]

import numpy as np
from arcengine import ARCBaseGame, Camera, Level, Sprite, GameAction


def rotated(shape, count):
    points = [tuple(p) for p in shape]
    for _ in range(count % 4):
        points = [(-y, x) for x, y in points]
    min_x, min_y = min(x for x, y in points), min(y for x, y in points)
    return sorted((x-min_x, y-min_y) for x, y in points)


class Sg07(ARCBaseGame):
    # The two equal-size surfaces are the live print and the reference proof.
    LEFT, RIGHT, TOP, CELL = 3, 36, 21, 5

    def __init__(self, seed=0):
        self.cfg = None
        self.layers = []
        self.remaining = []
        self.selected = None
        self.anchor = (1, 1)
        self.orientation = 0
        self.mask_turn = 0
        self.history = []
        self.rejected = False
        levels = [Level(sprites=[Sprite(pixels=np.zeros((64,64), dtype=np.int64), name='press', x=0, y=0)],
                        grid_size=(64,64), data={'layout': cfg}, name='Proof %d' % (i+1))
                  for i,cfg in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg07-v1', levels=levels,
                         camera=Camera(background=5,letter_box=5),
                         available_actions=[1,2,4,5,6,7], seed=seed)

    def on_set_level(self, level):
        self.cfg = level.get_data('layout')
        self.layers = [[[] for _ in range(5)] for _ in range(5)]
        for x,y,colors in self.cfg['initial']:
            self.layers[y][x] = list(colors)
        self.remaining = [tool['uses'] for tool in self.cfg['tools']]
        self.selected = 0 if len(self.cfg['tools']) == 1 else None
        self.anchor = (1,1)
        self.orientation = self.mask_turn = 0
        self.history = []
        self.rejected = False
        self._paint()

    def _snapshot(self):
        return ([[s[:] for s in row] for row in self.layers], self.remaining[:],
                self.selected, self.anchor, self.orientation, self.mask_turn)

    def _restore(self, state):
        layers,remaining,self.selected,self.anchor,self.orientation,self.mask_turn = state
        self.layers = [[s[:] for s in row] for row in layers]
        self.remaining = remaining[:]

    def _holes(self):
        points = set(map(tuple,self.cfg['blocked']))
        for _ in range(self.mask_turn):
            points = {(4-y,x) for x,y in points}
        return points

    def _footprint(self):
        if self.selected is None:
            return []
        return [(self.anchor[0]+x,self.anchor[1]+y)
                for x,y in rotated(self.cfg['tools'][self.selected]['shape'], self.orientation)]

    def visible(self):
        return [[s[-1] if s else 0 for s in row] for row in self.layers]

    def _press(self):
        if self.selected is None or self.remaining[self.selected] <= 0:
            return False
        points = self._footprint()
        if any(not (0<=x<5 and 0<=y<5) for x,y in points):
            return False
        points = [(x,y) for x,y in points if (x,y) not in self._holes()]
        color = self.cfg['tools'][self.selected]['color']
        if not points or (color == 0 and not any(self.layers[y][x] for x,y in points)):
            return False
        for x,y in points:
            if color:
                self.layers[y][x].append(color)
            elif self.layers[y][x]:
                self.layers[y][x].pop()
        self.remaining[self.selected] -= 1
        return True

    def step(self):
        action = self.action.id
        if action == GameAction.RESET:
            self.complete_action()
            return
        self.rejected = False
        if action == GameAction.ACTION7:
            if self.history:
                self._restore(self.history.pop())
        else:
            before = self._snapshot()
            changed = False
            if action == GameAction.ACTION6:
                data = self.action.data or {}
                x,y = data.get('x',-1),data.get('y',-1)
                if type(x) is int and type(y) is int:
                    if 2<=y<=14 and 2<=x<62:
                        slot = (x-2)//15
                        if slot < len(self.cfg['tools']):
                            self.selected = slot
                            self.orientation = 0
                            changed = True
                    elif self.LEFT<=x<self.LEFT+25 and self.TOP<=y<self.TOP+25:
                        self.anchor = ((x-self.LEFT)//5, (y-self.TOP)//5)
                        changed = True
                    elif 3<=x<=27 and 51<=y<=60:
                        changed = self._press()
                        self.rejected = not changed
                    elif 29<=x<=34 and 20<=y<=46 and self.cfg['rotate_mask']:
                        self.mask_turn = (self.mask_turn+1)%4
                        changed = True
            elif action in (GameAction.ACTION1,GameAction.ACTION2) and self.selected is not None:
                self.orientation = (self.orientation + (1 if action==GameAction.ACTION2 else -1))%4
                changed = True
            elif action == GameAction.ACTION4 and self.cfg['rotate_mask']:
                self.mask_turn = (self.mask_turn+1)%4
                changed = True
            elif action == GameAction.ACTION5:
                changed = self._press()
                self.rejected = not changed
            if changed:
                self.history.append(before)
        self._paint()
        if self.visible() == self.cfg['target']:
            self.next_level()
        self.complete_action()

    @staticmethod
    def _rect(c,x,y,w,h,color):
        c[max(0,y):min(64,y+h),max(0,x):min(64,x+w)] = color

    def _outline(self,c,x,y,w,h,color):
        self._rect(c,x,y,w,1,color);self._rect(c,x,y+h-1,w,1,color)
        self._rect(c,x,y,1,h,color);self._rect(c,x+w-1,y,1,h,color)

    def _ink(self,c,x,y,color):
        # Adjacent cells fuse into substantial continuous silhouettes.
        self._rect(c,x,y,5,5,color)
        if color==10: c[y,x]=9
        elif color==12: c[y+3,x+3]=8
        elif color==6: c[y+1,x+1]=7

    def _paint(self):
        c = np.full((64,64),5,dtype=np.int64)
        self._rect(c,0,0,64,16,4)
        for index,tool in enumerate(self.cfg['tools']):
            bx=2+index*15
            available=self.remaining[index]>0
            self._rect(c,bx,2,13,12,3 if available else 4)
            self._outline(c,bx,2,13,12,0 if self.selected==index else 2)
            shape=rotated(tool['shape'], self.orientation if self.selected==index else 0)
            width=max(x for x,y in shape)+1
            height=max(y for x,y in shape)+1
            for x,y in shape:
                sx=bx+6-width+x*2;sy=4+(6-height*2)//2+y*2
                self._rect(c,sx,sy,2,2,(tool['color'] or 0) if available else 2)
                if not tool['color']:c[sy,sx]=3
            for unit in range(tool['uses']):
                self._rect(c,bx+4+unit*3,11,2,1,(tool['color'] or 0) if unit<self.remaining[index] else 5)

        # Same scale, borders and ink texture connect construction to reference.
        self._rect(c,1,18,29,30,3)
        self._rect(c,34,18,29,30,3)
        self._outline(c,1,18,29,30,2)
        self._outline(c,34,18,29,30,0)
        self._rect(c,12,17,7,2,2)
        self._rect(c,45,17,7,2,0)
        visible=self.visible()
        holes=self._holes()
        for y in range(5):
            for x in range(5):
                for origin,board in ((self.LEFT,visible),(self.RIGHT,self.cfg['target'])):
                    px,py=origin+x*5,self.TOP+y*5
                    self._rect(c,px,py,4,4,4)
                    if board[y][x]: self._ink(c,px,py,board[y][x])
                px,py=self.LEFT+x*5,self.TOP+y*5
                if (x,y) in holes:
                    # Stencil clips only the edge: underlying ink stays visible.
                    c[py,px]=2;c[py+1,px]=2;c[py,px+1]=2
                    c[py+3,px+3]=2
                stack=self.layers[y][x]
                if len(stack)>1:
                    c[py+4,px: px+min(4,len(stack)-1)]=stack[-2::-1][:4]
        # Preview outlines leave all central color and stack evidence unobscured.
        if self.selected is not None and self.remaining[self.selected]>0:
            for x,y in self._footprint():
                if 0<=x<5 and 0<=y<5:
                    px,py=self.LEFT+x*5,self.TOP+y*5
                    col=2 if (x,y) in holes else (self.cfg['tools'][self.selected]['color'] or 0)
                    c[py+4,px+3]=col;c[py+3,px+4]=col
            ax,ay=self.anchor
            c[self.TOP+ay*5,self.LEFT+ax*5]=0
        if self.cfg['blocked']:
            self._rect(c,30,27,3,13,4)
            for i in range(4):
                c[29+i*2,31]=0 if i==self.mask_turn else 2
            if self.cfg['rotate_mask']:
                c[25,30:34]=11;c[26,33]=11;c[27,32]=11
        # The machine is physically joined to the live paper, not the reference.
        self._rect(c,4,47,2,5,2);self._rect(c,25,47,2,5,2)
        # A fixed folded corner identifies the reference as a printed sheet.
        c[18:21,59:62]=0;c[19:21,60:62]=3
        # Physical press and layer cross-section, rather than explanatory prose.
        self._rect(c,3,51,25,10,3)
        self._outline(c,3,51,25,10,8 if self.rejected else 2)
        self._rect(c,8,53,15,2,0)
        self._rect(c,14,55,3,3,0)
        c[57,12:19]=0;c[58,13:18]=0;c[59,14:17]=0
        self._rect(c,7,59,17,1,2)
        ax,ay=self.anchor
        # Cross-section shares a thin leader with the selected sample location.
        c[49,29:49]=2;c[49:52,48]=2
        stack=self.layers[ay][ax]
        self._rect(c,35,51,27,10,4)
        for depth,color in enumerate(stack[-4:]):
            self._rect(c,38+depth*2,57-depth*2,12,2,color)
        if not stack:self._rect(c,38,58,12,1,2)
        # Segmented progress is native level progress, never a hidden rule hint.
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=c,name='palimpsest',x=0,y=0,layer=0))
