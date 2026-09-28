FIXED_LEVELS = [{'window': 6, 'beads': [14], 'walls': [], 'goals': [16]}, {'window': 6, 'beads': [14], 'walls': [16], 'goals': [24]}, {'window': 7, 'beads': [14, 15], 'walls': [16, 22], 'goals': [2, 1]}, {'window': 6, 'beads': [8, 14], 'walls': [10, 16, 20, 21], 'goals': [2, 17]}, {'window': 7, 'beads': [14, 15], 'walls': [4, 10, 16, 25, 26, 27], 'goals': [17, 2]}, {'window': 0, 'beads': [0, 1, 6], 'walls': [5, 11, 17, 23, 29, 30, 31, 32, 33, 34, 35, 9, 15, 20, 26, 28], 'goals': [1, 0, 24]}, {'window': 7, 'beads': [8, 9, 14], 'walls': [0, 1, 2, 3, 4, 5, 11, 17, 23, 29, 35, 10, 16, 19, 25, 27], 'goals': [32, 12, 6]}]

# Fixed native puzzle mechanics.
DIRS={1:(0,-1),2:(0,1),3:(-1,0),4:(1,0)}

def initial(cfg):return (cfg['window'],tuple(cfg['beads']))

def inside(window,p):
    wx,wy=window%5,window//5
    return wx<=p%6<wx+2 and wy<=p//6<wy+2

def advance(cfg,state,action):
    if action not in DIRS:return state
    window,beads=state;dx,dy=DIRS[action];wx,wy=window%5+dx,window//5+dy
    if not(0<=wx<5 and 0<=wy<5):return state
    walls=set(cfg['walls']);moving={i for i,p in enumerate(beads) if inside(window,p)}
    destinations={}
    for i in list(moving):
        p=beads[i];x,y=p%6+dx,p//6+dy
        if not(0<=x<6 and 0<=y<6) or y*6+x in walls:moving.remove(i)
        else:destinations[i]=y*6+x
    # A stationary bead blocks a train of carried beads; no pushing or overlap.
    changed=True
    while changed:
        changed=False
        stationary={p for i,p in enumerate(beads) if i not in moving}
        for i in list(moving):
            if destinations[i] in stationary:moving.remove(i);changed=True
    return (wy*5+wx,tuple(destinations[i] if i in moving else p for i,p in enumerate(beads)))

def solved(cfg,state):return state[1]==tuple(cfg['goals'])

import numpy as np
from arcengine import ARCBaseGame,Camera,Level,Sprite,GameAction

COLORS=(10,12,6)

class Sg14(ARCBaseGame):
    def __init__(self,seed=0):
        self.cfg=None;self.state=None;self.history=[];self.stranded=();self.rejected=False
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='window')],grid_size=(64,64),data={'layout':c},name='Window %d'%(i+1)) for i,c in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg14-v1',levels=levels,camera=Camera(background=5,letter_box=5),available_actions=[1,2,3,4,7],seed=seed)

    def on_set_level(self,level):
        self.cfg=level.get_data('layout');self.state=initial(self.cfg);self.history=[];self.stranded=();self.rejected=False;self._paint()

    def step(self):
        a=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1]);self.stranded=();self.rejected=False
        if a==7:
            if self.history:self.state=self.history.pop()
        elif a in DIRS:
            old=self.state;n=advance(self.cfg,old,a)
            if n!=old:
                self.stranded=tuple(i for i,p in enumerate(old[1]) if inside(old[0],p) and p==n[1][i])
                self.history.append(old);self.state=n
            else:self.rejected=True
        self._paint()
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    def _paint(self):
        c=np.full((64,64),5,dtype=np.int64);walls=set(self.cfg['walls'])
        for p in range(36):
            x,y=8+8*(p%6),8+8*(p//6)
            if p in walls:
                c[y:y+7,x:x+7]=3;c[y+1:y+6,x+1:x+6]=4
            else:c[y+3,x+3]=4
        for i,p in enumerate(self.cfg['goals']):
            x,y=8+8*(p%6),8+8*(p//6);col=COLORS[i]
            c[y,x:x+7]=col;c[y+6,x:x+7]=col;c[y:y+7,x]=col;c[y:y+7,x+6]=col
        for i,p in enumerate(self.state[1]):
            x,y=8+8*(p%6),8+8*(p//6);col=COLORS[i]
            c[y+1:y+6,x+1:x+6]=col;c[y+2,x+2]=0
            if i in self.stranded:c[y+4,x+2:x+5]=8
        window=self.state[0];x,y=7+8*(window%5),7+8*(window//5)
        col=8 if self.rejected else 0
        # Offset outline never erases bead centers; it can visibly cross terrain.
        c[y,x:x+17]=col;c[y+16,x:x+17]=col;c[y:y+17,x]=col;c[y:y+17,x+16]=col
        for i in range(7):c[63,5+i*8:11+i*8]=14 if i<self.level_index else 4
        self.current_level.remove_all_sprites();self.current_level.add_sprite(Sprite(pixels=c,name='carrying-window',x=0,y=0,layer=0))
