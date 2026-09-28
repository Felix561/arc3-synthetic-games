FIXED_LEVELS = [{'start': [14, 12], 'walls': [], 'slack': 2, 'goal': [15, 13]}, {'start': [14, 12], 'walls': [], 'slack': 2, 'goal': [15, 20]}, {'start': [15, 13], 'walls': [16], 'slack': 2, 'goal': [19, 24]}, {'start': [20, 18], 'walls': [21, 27], 'slack': 2, 'goal': [15, 9]}, {'start': [9, 7], 'walls': [10, 20, 22], 'slack': 2, 'goal': [21, 27]}, {'start': [15, 12], 'walls': [2, 16, 27, 24], 'slack': 3, 'goal': [22, 34]}, {'start': [14, 12], 'walls': [4, 21, 27, 25, 29], 'slack': 2, 'goal': [33, 34]}]

from collections import deque
N=6
DIRS={1:(0,-1),2:(0,1),3:(-1,0),4:(1,0)}


def cell(x,y):return y*N+x

def pos(p):return p%N,p//N

def initial(cfg):return tuple(cfg['start'])

def solved(cfg,state):return tuple(state)==tuple(cfg['goal'])

def advance(cfg,state,active,action):
    if action not in DIRS or active not in (0,1):return state
    dx,dy=DIRS[action]
    moved=state[active];other=state[1-active]
    mx,my=pos(moved);ox,oy=pos(other)
    nx,ny=mx+dx,my+dy
    if not 0<=nx<N or not 0<=ny<N:return state
    n=cell(nx,ny);walls=set(cfg['walls'])
    if n in walls or n==other:return state
    pulled=abs(nx-ox)+abs(ny-oy)>cfg['slack']
    if pulled:
        fx,fy=ox+dx,oy+dy
        if not 0<=fx<N or not 0<=fy<N:return state
        follower=cell(fx,fy)
        if follower in walls or follower==n:return state
        other=follower
    out=list(state);out[active]=n;out[1-active]=other
    return tuple(out)


def centers():return tuple((8+8*(p%N)+4,8+8*(p//N)+4) for p in range(N*N))

import numpy as np
from arcengine import ARCBaseGame, Camera, Level, Sprite, GameAction
COLORS=(8,9)


class Sg22(ARCBaseGame):
    def __init__(self,seed=0):
        self.cfg=None;self.state=None;self.selected=0;self.history=[];self.last_pull=False;self.blocked=False
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='tether')],
                      grid_size=(64,64),data={'layout':cfg},name='Tether %d'%(i+1))
                for i,cfg in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg22-v1',levels=levels,camera=Camera(background=5,letter_box=5),
                         available_actions=[1,2,3,4,6,7],seed=seed)

    def on_set_level(self,level):
        self.cfg=level.get_data('layout');self.state=initial(self.cfg);self.selected=0
        self.history=[];self.last_pull=False;self.blocked=False;self._paint()

    def step(self):
        a=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1])
        self.last_pull=False;self.blocked=False
        if a==7 and self.history:
            self.state,self.selected=self.history.pop()
        elif a==6:
            d=self.action.data or {};x,y=d.get('x',-99),d.get('y',-99)
            if type(x) is int and type(y) is int and 8<=x<56 and 8<=y<56:
                p=cell((x-8)//8,(y-8)//8)
                if p in self.state:
                    n=self.state.index(p)
                    if n!=self.selected:self.history.append((self.state,self.selected));self.selected=n
        elif a in DIRS:
            n=advance(self.cfg,self.state,self.selected,a)
            if n!=self.state:
                self.last_pull=n[1-self.selected]!=self.state[1-self.selected]
                self.history.append((self.state,self.selected));self.state=n
            else:self.blocked=True
        self._paint()
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    def _paint(self):
        c=np.full((64,64),5,dtype=np.int64)
        c[6,6:58]=4;c[57,6:58]=4;c[6:58,6]=4;c[6:58,57]=4
        for p in range(36):
            x,y=8+8*(p%6),8+8*(p//6)
            c[y+3,x+3]=4
            if p in self.cfg['walls']:
                c[y:y+8,x:x+8]=3
                c[y+1:y+7,x+1:x+7]=4
        for i,p in enumerate(self.cfg['goal']):
            x,y=8+8*(p%6),8+8*(p//6);col=COLORS[i]
            c[y,x+1:x+7]=col;c[y+7,x+1:x+7]=col;c[y+1:y+7,x]=col;c[y+1:y+7,x+7]=col
        # The continuous cord is the central relation; the beads remain separate objects.
        x1,y1=centers()[self.state[0]];x2,y2=centers()[self.state[1]]
        for xx in range(min(x1,x2),max(x1,x2)+1):c[y1,xx]=0
        for yy in range(min(y1,y2),max(y1,y2)+1):c[yy,x2]=0
        for i,p in enumerate(self.state):
            x,y=8+8*(p%6),8+8*(p//6);col=COLORS[i]
            c[y+1:y+7,x+1:x+7]=col
            c[y+2:y+6,x:x+8]=col
            c[y+3:y+5,x+3:x+5]=5
            if i==self.selected:
                c[y,x]=0;c[y,x+7]=0;c[y+7,x]=0;c[y+7,x+7]=0
            if self.last_pull and i!=self.selected:
                c[y+7,x+2:x+6]=11
        if self.blocked:
            p=self.state[self.selected];x,y=8+8*(p%6),8+8*(p//6)
            c[y+1,x+1]=6;c[y+1,x+6]=6
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=c,name='two-bead-tether',x=0,y=0,layer=0))
