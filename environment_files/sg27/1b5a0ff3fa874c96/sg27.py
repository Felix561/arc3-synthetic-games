FIXED_LEVELS = [{'floor': [[0, 2], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 2], [4, 2], [5, 2]], 'start': [1, 2], 'axis': 0, 'crates': [[3, 2]], 'goal': [[4, 2]]}, {'floor': [[1, 1], [1, 2], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [3, 1], [3, 2]], 'start': [2, 1], 'axis': 1, 'crates': [[2, 3]], 'goal': [[2, 4]]}, {'floor': [[0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [5, 2]], 'start': [2, 2], 'axis': 0, 'crates': [[1, 2], [3, 2]], 'goal': [[0, 2], [5, 2]]}, {'floor': [[0, 1], [0, 2], [0, 3], [1, 1], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 3], [4, 1], [4, 3], [5, 1], [5, 2], [5, 3]], 'start': [2, 2], 'axis': 0, 'crates': [[1, 1], [3, 1]], 'goal': [[1, 1], [2, 1]]}, {'floor': [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [5, 0], [5, 1], [5, 2], [5, 3], [5, 4]], 'start': [2, 2], 'axis': 1, 'crates': [[1, 1], [3, 1]], 'goal': [[0, 0], [3, 0]]}, {'floor': [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5]], 'start': [1, 2], 'axis': 0, 'crates': [[1, 1], [4, 1]], 'goal': [[0, 0], [5, 0]]}, {'floor': [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5]], 'start': [2, 2], 'axis': 0, 'crates': [[1, 1], [3, 1]], 'goal': [[1, 0], [0, 0]]}]

from collections import deque

DIRS={1:(0,-1),2:(0,1),3:(-1,0),4:(1,0)}
AXES=((1,0),(0,1))

def initial(cfg):
    return (tuple(cfg['start']),cfg.get('axis',0),False,tuple(tuple(p) for p in cfg['crates']))

def footprint(state):
    p,axis,opened,crates=state
    if not opened:return (p,)
    dx,dy=AXES[axis]
    return (p,(p[0]-dx,p[1]-dy),(p[0]+dx,p[1]+dy))

def solved(cfg,state):return state[3]==tuple(tuple(p) for p in cfg['goal'])

def advance(cfg,state,action,allow_multiple=True,allow_retract=True,freeze_correct=False):
    p,axis,opened,crates=state
    floor=set(tuple(p) for p in cfg['floor'])
    if action in DIRS:
        dx,dy=DIRS[action]
        n=(p[0]+dx,p[1]+dy)
        facing=axis if opened else (1 if dy else 0)
        out=(n,facing,opened,crates)
        if all(q in floor and q not in crates for q in footprint(out)):return out
        return (p,facing,opened,crates)
    if action==5:
        if opened:return (p,axis,False,crates) if allow_retract else state
        dx,dy=AXES[axis]
        arms=((p[0]-dx,p[1]-dy),(p[0]+dx,p[1]+dy))
        if any(q not in floor for q in arms):return state
        moved=list(crates);count=0
        for sign,q in zip((-1,1),arms):
            if q not in crates:continue
            i=crates.index(q);target=(q[0]+sign*dx,q[1]+sign*dy)
            if target not in floor or target in crates:return state
            if freeze_correct and q==tuple(cfg['goal'][i]):return state
            moved[i]=target;count+=1
        if count>1 and not allow_multiple:return state
        return p,axis,True,tuple(moved)
    return state

def explore(cfg,allow_multiple=True,allow_retract=True,freeze_correct=False,cap=200000):
    start=initial(cfg);q=deque([start]);parents={start:None};actions={}
    while q:
        s=q.popleft()
        for a in (1,2,3,4,5):
            n=advance(cfg,s,a,allow_multiple,allow_retract,freeze_correct)
            if n not in parents:
                if len(parents)>=cap:raise ValueError('state cap exceeded')
                parents[n]=s;actions[n]=a;q.append(n)
    return parents,actions

def path_to(parents,actions,state):
    path=[]
    while parents[state] is not None:path.append(actions[state]);state=parents[state]
    return path[::-1]

import numpy as np
from arcengine import ARCBaseGame,Camera,Level,Sprite,GameAction

class Sg27(ARCBaseGame):
    def __init__(self,seed=0):
        self.cfg=None;self.state=None;self.history=[];self.transition=None;self.blocked=False
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='press')],
                      grid_size=(64,64),data={'layout':cfg},name='Press %d'%(i+1))
                for i,cfg in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg27-v2',levels=levels,camera=Camera(background=1,letter_box=1),
                         available_actions=[1,2,3,4,5,7],seed=seed)

    def on_set_level(self,level):
        self.cfg=level.get_data('layout');self.state=initial(self.cfg);self.history=[]
        self.transition=None;self.blocked=False;self._paint()

    def step(self):
        if self.transition is not None:
            self.state=self.transition;self.transition=None;self._paint()
            if solved(self.cfg,self.state):self.next_level()
            self.complete_action();return
        a=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1])
        self.blocked=False
        if a==7:
            if self.history:self.state=self.history.pop()
        elif a in (1,2,3,4,5):
            n=advance(self.cfg,self.state,a)
            if n!=self.state:
                self.history.append(self.state)
                if a==5 and n[2]:self.transition=n
                else:self.state=n
            else:self.blocked=True
        self._paint()
        if self.transition is not None:return
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    @staticmethod
    def center(p):return 12+8*p[0],12+8*p[1]

    @staticmethod
    def rect(c,x,y,w,h,col):c[max(0,y):min(64,y+h),max(0,x):min(64,x+w)]=col

    def _paint(self):
        c=np.full((64,64),1,dtype=np.int64);r=self.rect
        # A light machine chamber and dark solid obstacles, without dotted cells.
        floor=set(tuple(p) for p in self.cfg['floor'])
        for p in floor:
            x,y=self.center(p);r(c,x-5,y-5,11,11,3)
        for p in floor:
            x,y=self.center(p);r(c,x-4,y-4,8,8,0)
        for i,p in enumerate(self.cfg['goal']):
            x,y=self.center(p);col=12 if i==0 else 10
            r(c,x-4,y-4,8,8,col);r(c,x-2,y-2,4,4,0)
        p,axis,opened,crates=self.state
        centers=[self.center(q) for q in crates]
        if self.transition is not None:
            centers=[((a[0]+b[0])//2,(a[1]+b[1])//2) for a,b in zip(centers,[self.center(q) for q in self.transition[3]])]
        for i,(x,y) in enumerate(centers):
            col=12 if i==0 else 10;r(c,x-3,y-3,6,6,col)
            # Substantial solid cargo differs from empty matching bay rims.
            r(c,x-1,y-1,2,2,5)
        x,y=self.center(p);dx,dy=AXES[axis]
        extent=8 if opened else 2
        if self.transition is not None:extent=5
        span=7 if opened or self.transition is not None else 5
        half=span//2
        r(c,x-dx*extent-1,y-dy*extent-1,2*dx*extent+3,2*dy*extent+3,3)
        for sign in (-1,1):
            qx,qy=x+sign*dx*extent,y+sign*dy*extent
            r(c,qx-1 if dx else qx-half,qy-half if dx else qy-1,3 if dx else span,span if dx else 3,6)
            r(c,qx if dx else qx-half+1,qy-half+1 if dx else qy,1 if dx else span-2,span-2 if dx else 1,13)
        r(c,x-2,y-2,5,5,6);r(c,x-1,y-1,3,3,0);r(c,x,y,1,1,5)
        if self.blocked:
            r(c,x-dx*2-dy,y-dy*2-dx,2,2,13)
            r(c,x+dx*2-dy,y+dy*2-dx,2,2,13)
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=c,name='opposed-jaw-press',x=0,y=0,layer=0))

