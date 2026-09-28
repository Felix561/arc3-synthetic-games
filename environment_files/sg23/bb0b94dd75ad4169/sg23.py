FIXED_LEVELS = [{'gears': [12, 13], 'clutches': [], 'start': [0, 0], 'raised': [False, False], 'selected': 0, 'goal': [1, 3]}, {'gears': [11, 12, 13], 'clutches': [], 'start': [0, 0, 0], 'raised': [False, False, False], 'selected': 1, 'goal': [2, 2, 2]}, {'gears': [11, 12, 13], 'clutches': [1], 'start': [0, 0, 0], 'raised': [False, False, False], 'selected': 1, 'goal': [1, 0, 1]}, {'gears': [10, 11, 12, 13], 'clutches': [1], 'start': [0, 0, 0, 0], 'raised': [False, False, False, False], 'selected': 1, 'goal': [2, 0, 3, 1]}, {'gears': [6, 7, 8, 12], 'clutches': [1, 3], 'start': [0, 0, 0, 0], 'raised': [False, False, False, False], 'selected': 1, 'goal': [1, 3, 2, 1]}, {'gears': [10, 11, 12, 13, 17], 'clutches': [1, 2], 'start': [0, 0, 0, 0, 0], 'raised': [False, False, False, False, False], 'selected': 2, 'goal': [2, 0, 3, 1, 1]}, {'gears': [5, 6, 7, 12, 13, 14], 'clutches': [2, 3], 'start': [0, 0, 0, 0, 0, 0], 'raised': [False, False, False, False, False, False], 'selected': 2, 'goal': [1, 3, 3, 1, 0, 0]}]

from collections import deque
N=5

def cell(x,y):return y*N+x

def xy(p):return p%N,p//N

def initial(cfg):
    return tuple(cfg['start']),tuple(cfg['raised']),cfg['selected']

def connected(cfg,raised,index):
    positions=cfg['gears'];active={i for i in range(len(positions)) if not raised[i]}
    if index not in active:return {index:0}
    dist={index:0};q=deque([index])
    while q:
        i=q.popleft();x,y=xy(positions[i])
        for j in active:
            if j in dist:continue
            u,v=xy(positions[j])
            if abs(x-u)+abs(y-v)==1:
                dist[j]=dist[i]+1;q.append(j)
    return dist

def advance(cfg,state,action):
    ori,raised,selected=state
    if action==5:
        if selected not in cfg['clutches']:return state
        out=list(raised);out[selected]=not out[selected]
        return ori,tuple(out),selected
    if type(action) is not int or not 0<=action<len(ori):return state
    out=list(ori)
    for i,dist in connected(cfg,raised,action).items():
        out[i]=(out[i]+(1 if dist%2==0 else -1))%4
    return tuple(out),raised,action

def solved(cfg,state):return state[0]==tuple(cfg['goal'])

def geometry(cfg):
    coords=[xy(p) for p in cfg['gears']]
    xs=[x for x,y in coords];ys=[y for x,y in coords]
    span=max(max(xs)-min(xs),max(ys)-min(ys),1)
    step=min(20,44//span)
    midx=(min(xs)+max(xs))/2;midy=(min(ys)+max(ys))/2
    points=tuple((round(32+(x-midx)*step),round(32+(y-midy)*step)) for x,y in coords)
    return points,min(9,max(4,step//2-1))

def centers(cfg):return geometry(cfg)[0]


import numpy as np
from arcengine import ARCBaseGame,Camera,Level,Sprite,GameAction
VECTORS=((0,-1),(1,0),(0,1),(-1,0))


class Sg23(ARCBaseGame):
    def __init__(self,seed=0):
        self.cfg=None;self.state=None;self.history=[];self.last=()
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='gears')],
                      grid_size=(64,64),data={'layout':cfg},name='Gears %d'%(i+1))
                for i,cfg in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg23-v1',levels=levels,camera=Camera(background=5,letter_box=5),
                         available_actions=[5,6,7],seed=seed)

    def on_set_level(self,level):
        self.cfg=level.get_data('layout');self.state=initial(self.cfg);self.history=[];self.last=();self._paint()

    def step(self):
        a=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1]);self.last=()
        if a==7 and self.history:self.state=self.history.pop()
        elif a==5:
            nxt=advance(self.cfg,self.state,5)
            if nxt!=self.state:self.history.append(self.state);self.state=nxt
        elif a==6:
            d=self.action.data or {};x,y=d.get('x',-99),d.get('y',-99)
            if type(x) is int and type(y) is int:
                points,radius=geometry(self.cfg)
                for i,(cx,cy) in enumerate(points):
                    if abs(x-cx)<=radius and abs(y-cy)<=radius:
                        nxt=advance(self.cfg,self.state,i)
                        if nxt!=self.state:
                            self.last=tuple(connected(self.cfg,self.state[1],i))
                            self.history.append(self.state);self.state=nxt
                        break
        self._paint()
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    def _paint(self):
        c=np.full((64,64),5,dtype=np.int64);ori,raised,selected=self.state
        points,radius=geometry(self.cfg)
        for i,(cx,cy) in enumerate(points):
            col=4 if raised[i] else 12
            for dy in range(-radius,radius+1):
                for dx in range(-radius,radius+1):
                    d=dx*dx+dy*dy
                    if (radius-2)**2<=d<=radius*radius:c[cy+dy,cx+dx]=col
            for dx,dy in VECTORS:c[cy+(radius+1)*dy,cx+(radius+1)*dx]=col
            c[cy-1:cy+2,cx-1:cx+2]=3
            sx,sy=VECTORS[ori[i]]
            for k in range(1,radius):c[cy+sy*k,cx+sx*k]=0
            c[cy,cx]=0
            gx,gy=VECTORS[self.cfg['goal'][i]]
            c[cy+gy*(radius+2),cx+gx*(radius+2)]=11
            if i in self.cfg['clutches']:
                c[cy+radius+2,cx-radius-1:cx-radius+2]=9 if raised[i] else 14
            if i==selected:
                c[cy-radius,cx-radius]=0;c[cy-radius,cx+radius]=0
                c[cy+radius,cx-radius]=0;c[cy+radius,cx+radius]=0
            if i in self.last:c[cy-radius-1,cx-1:cx+2]=0
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=c,name='gear-field',x=0,y=0,layer=0))
