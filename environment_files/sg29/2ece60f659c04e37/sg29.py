FIXED_LEVELS = [{'floor': [[0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [5, 2], [6, 2]], 'start': [[3, 2], [4, 2], [5, 2]], 'goal': [[0, 2], [2, 2]]}, {'floor': [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [2, 1], [3, 1], [4, 1], [5, 1]], 'start': [[3, 1], [4, 1], [5, 1]], 'goal': [[1, 3], [1, 1]]}, {'floor': [[0, 2], [1, 2], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [3, 2], [4, 2], [5, 2], [5, 3], [5, 4], [5, 5], [6, 2]], 'start': [[2, 2], [3, 2], [4, 2]], 'goal': [[3, 2], [1, 2]]}, {'floor': [[0, 1], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [2, 1], [2, 5], [3, 1], [3, 2], [3, 3], [3, 5], [4, 1], [4, 5], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [6, 1]], 'start': [[2, 1], [3, 1], [4, 1], [5, 1]], 'goal': [[1, 3], [0, 1]]}, {'floor': [[0, 1], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [2, 1], [2, 2], [2, 4], [3, 1], [3, 4], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [5, 1], [5, 4], [6, 1], [6, 4]], 'start': [[1, 2], [1, 3], [1, 4], [2, 4]], 'goal': [[4, 3], [6, 4]]}, {'floor': [[1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [2, 1], [2, 4], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [4, 1], [4, 4], [4, 5], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [6, 1], [6, 5]], 'start': [[3, 2], [3, 3], [3, 4], [4, 4], [5, 4]], 'goal': [[5, 4], [6, 5]]}, {'floor': [[0, 1], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [2, 1], [2, 3], [2, 5], [3, 1], [3, 2], [3, 3], [3, 5], [4, 1], [4, 3], [4, 4], [4, 5], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [6, 1], [6, 3], [6, 4], [6, 5]], 'start': [[1, 3], [2, 3], [3, 3], [4, 3], [4, 4]], 'goal': [[2, 1], [6, 1]]}]

from collections import deque

DIRS = {1:(0,-1), 2:(0,1), 3:(-1,0), 4:(1,0)}

def initial(cfg):
    return (tuple(tuple(p) for p in cfg['start']),0)

def solved(cfg,state):
    body,active=state
    return body[0]==tuple(cfg['goal'][0]) and body[-1]==tuple(cfg['goal'][1])

def advance(cfg,state,action):
    body,active=state
    if action==5:
        return body,1-active
    if action not in DIRS:
        return state
    dx,dy=DIRS[action]
    head=body[0] if active==0 else body[-1]
    target=(head[0]+dx,head[1]+dy)
    floor=set(tuple(p) for p in cfg['floor'])
    blocking=body[:-1] if active==0 else body[1:]
    if target not in floor or target in blocking:
        return state
    return ((target,)+body[:-1] if active==0 else body[1:]+(target,),active)

def explore(cfg,allow_switch=True,cap=150000):
    start=initial(cfg);q=deque([start]);parents={start:None};actions={}
    while q:
        s=q.popleft()
        for a in ((1,2,3,4,5) if allow_switch else (1,2,3,4)):
            n=advance(cfg,s,a)
            if n not in parents:
                if len(parents)>=cap:raise ValueError('state cap exceeded')
                parents[n]=s;actions[n]=a;q.append(n)
    return parents,actions

def path_to(parents,actions,state):
    path=[]
    while parents[state] is not None:
        path.append(actions[state]);state=parents[state]
    return path[::-1]

def min_switches(cfg,states):
    start=initial(cfg);dist={start:0};q=deque([start])
    while q:
        s=q.popleft()
        for a in (1,2,3,4,5):
            n=advance(cfg,s,a);d=dist[s]+(a==5)
            if n not in dist or d<dist[n]:
                dist[n]=d
                if a==5:q.append(n)
                else:q.appendleft(n)
    result={}
    for s,v in dist.items():
        key=(s[0][0],s[0][-1]);result[key]=min(v,result.get(key,999))
    return result

import numpy as np
from arcengine import ARCBaseGame, Camera, Level, Sprite, GameAction

class Sg29(ARCBaseGame):
    def __init__(self,seed=0):
        self.cfg=None;self.state=None;self.history=[];self.transition=None;self.blocked=None
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='convoy')],
                      grid_size=(64,64),data={'layout':cfg},name='Convoy %d'%(i+1))
                for i,cfg in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg29-v2',levels=levels,camera=Camera(background=5,letter_box=5),
                         available_actions=[1,2,3,4,5,7],seed=seed)

    def on_set_level(self,level):
        self.cfg=level.get_data('layout');self.state=initial(self.cfg);self.history=[]
        self.transition=None;self.blocked=None;self._paint()

    def step(self):
        if self.transition is not None:
            self.state=self.transition;self.transition=None;self._paint()
            if solved(self.cfg,self.state):self.next_level()
            self.complete_action();return
        a=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1])
        self.blocked=None
        if a==7:
            if self.history:self.state=self.history.pop()
        elif a in (1,2,3,4,5):
            n=advance(self.cfg,self.state,a)
            if n!=self.state:
                self.history.append(self.state)
                if a in DIRS:self.transition=n
                else:self.state=n
            elif a in DIRS:self.blocked=DIRS[a]
        self._paint()
        if self.transition is not None:return
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    @staticmethod
    def center(p):return 10+7*p[0],12+7*p[1]

    @staticmethod
    def rect(c,x,y,w,h,col):
        c[max(0,y):min(64,y+h),max(0,x):min(64,x+w)]=col

    def _paint(self):
        c=np.full((64,64),5,dtype=np.int64);r=self.rect
        # A continuous road has no cell marks, decorative ticks, or universal HUD.
        floor=set(tuple(p) for p in self.cfg['floor'])
        for p in floor:
            x,y=self.center(p);r(c,x-3,y-3,7,7,4)
            for dx,dy in ((1,0),(0,1)):
                if (p[0]+dx,p[1]+dy) in floor:r(c,x-3,y-3,7+7*dx,7+7*dy,4)
        for i,p in enumerate(self.cfg['goal']):
            x,y=self.center(p);col=12 if i==0 else 10
            r(c,x-4,y-4,9,9,col);r(c,x-2,y-2,5,5,5)
            # Endpoint shape is redundant with color: square and hollow-disc bays.
            if i==1:
                for sx,sy in ((-4,-4),(4,-4),(-4,4),(4,4)):r(c,x+sx,y+sy,1,1,5)
        body,active=self.state
        centers=[self.center(p) for p in body]
        if self.transition is not None:
            centers=[((a[0]+b[0])//2,(a[1]+b[1])//2) for a,b in zip(centers,[self.center(p) for p in self.transition[0]])]
        for (x1,y1),(x2,y2) in zip(centers,centers[1:]):
            r(c,min(x1,x2)-1,min(y1,y2)-1,abs(x2-x1)+3,abs(y2-y1)+3,1)
        for i,(x,y) in enumerate(centers):
            col=12 if i==0 else 10 if i==len(body)-1 else 3
            r(c,x-3,y-3,7,7,col)
            if i==len(body)-1:
                for sx,sy in ((-3,-3),(3,-3),(-3,3),(3,3)):r(c,x+sx,y+sy,1,1,4)
                r(c,x-1,y-1,3,3,5)
            elif i not in (0,len(body)-1):r(c,x-1,y-1,3,3,1)
        x,y=centers[0 if active==0 else -1]
        # White corner brackets attach selection to the endpoint that actually leads.
        for sx,sy in ((-4,-4),(3,-4),(-4,3),(3,3)):r(c,x+sx,y+sy,2,2,0)
        if self.blocked:
            dx,dy=self.blocked;r(c,x+dx*4-1,y+dy*4-1,3,3,6)
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=c,name='ordered-chain',x=0,y=0,layer=0))

