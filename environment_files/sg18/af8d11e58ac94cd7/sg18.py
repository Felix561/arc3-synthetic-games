FIXED_LEVELS = [{'start': [14, 13], 'walls': [], 'goal': [14, 15]}, {'start': [14, 13, 8], 'walls': [], 'goal': [16, 15, 10]}, {'start': [32, 8, 13, 12], 'walls': [], 'goal': [32, 18, 5, 14]}, {'start': [2, 21, 8, 31], 'walls': [], 'goal': [0, 19, 32, 9]}, {'start': [5, 4, 7, 0], 'walls': [], 'goal': [1, 2, 7, 12]}, {'start': [32, 8, 21, 14], 'walls': [], 'goal': [6, 20, 19, 26]}, {'start': [22, 15, 4, 31], 'walls': [], 'goal': [10, 17, 2, 7]}]

N=6

def initial(cfg):return tuple(cfg['start'])

def solved(cfg,state):return state==tuple(cfg['goal'])

def advance(cfg,state,pivot):
    if type(pivot) is not int or not 0<=pivot<len(state):return state
    center=state[pivot];cx,cy=center%N,center//N;occupied=set(state);walls=set(cfg['walls']);out=[]
    for i,p in enumerate(state):
        if i==pivot:out.append(p);continue
        x,y=2*cx-p%N,2*cy-p//N;q=y*N+x
        out.append(q if 0<=x<N and 0<=y<N and q not in walls and q not in occupied else p)
    return tuple(out)

import numpy as np
from arcengine import ARCBaseGame,Camera,Level,Sprite,GameAction
COLORS=(10,12,6,14)

class Sg18(ARCBaseGame):
    def __init__(self,seed=0):
        self.cfg=None;self.state=None;self.history=[];self.pivot=None;self.changed=()
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='pivot')],grid_size=(64,64),data={'layout':c},name='Pivot %d'%(i+1)) for i,c in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg18-v1',levels=levels,camera=Camera(background=5,letter_box=5),available_actions=[6,7],seed=seed)

    def on_set_level(self,level):
        self.cfg=level.get_data('layout');self.state=initial(self.cfg);self.history=[];self.pivot=None;self.changed=();self._paint()

    def step(self):
        a=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1]);self.pivot=None;self.changed=()
        if a==7 and self.history:self.state=self.history.pop()
        elif a==6:
            d=self.action.data or {};x,y=d.get('x',-1),d.get('y',-1)
            if type(x) is int and type(y) is int and 8<=x<56 and 8<=y<56:
                p=((y-8)//8)*6+(x-8)//8
                if p in self.state and (x-8)%8<7 and (y-8)%8<7:
                    i=self.state.index(p);self.pivot=i;n=advance(self.cfg,self.state,i)
                    self.changed=tuple(k for k in range(len(n)) if n[k]!=self.state[k])
                    if n!=self.state:self.history.append(self.state);self.state=n
        self._paint()
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    def _paint(self):
        c=np.full((64,64),5,dtype=np.int64)
        c[6,6:58]=4;c[57,6:58]=4;c[6:58,6]=4;c[6:58,57]=4
        for p in range(36):
            x,y=8+p%6*8,8+p//6*8;c[y+3,x+3]=4
            if p in self.cfg['walls']:c[y:y+7,x:x+7]=3
        for i,p in enumerate(self.cfg['goal']):
            x,y=8+p%6*8,8+p//6*8;col=COLORS[i]
            c[y,x+1:x+6]=col;c[y+6,x+1:x+6]=col;c[y+1:y+6,x]=col;c[y+1:y+6,x+6]=col
        for i,p in enumerate(self.state):
            x,y=8+p%6*8,8+p//6*8;col=COLORS[i]
            c[y+1:y+6,x+1:x+6]=col;c[y+2:y+5,x:x+7]=col;c[y:y+7,x+2:x+5]=col
            if self.cfg['goal'][i]==p:c[y+2:y+5,x+2:x+5]=5
            if self.pivot==i:
                c[y,x]=0;c[y,x+6]=0;c[y+6,x]=0;c[y+6,x+6]=0
            elif i in self.changed:c[y+7,x+2:x+5]=0
        self.current_level.remove_all_sprites();self.current_level.add_sprite(Sprite(pixels=c,name='pivot-field',x=0,y=0,layer=0))
