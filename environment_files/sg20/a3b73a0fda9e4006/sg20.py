FIXED_LEVELS = [{'start': [0, 0, 0], 'goal': [1, 0, 0]}, {'start': [0, 1, 1], 'goal': [1, 0, 0]}, {'start': [2, 1, 2, 1], 'goal': [1, 2, 0, 0]}, {'start': [1, 2, 1, 0, 0, 0], 'goal': [2, 1, 0, 0, 1, 1]}, {'start': [2, 0, 0, 0, 2, 0, 0], 'goal': [1, 1, 2, 1, 0, 0, 1]}, {'start': [2, 0, 0, 1, 0, 1, 2, 2, 0], 'goal': [1, 1, 2, 0, 1, 2, 2, 1, 2]}, {'start': [2, 1, 0, 0, 0, 2, 1, 1, 0], 'goal': [2, 2, 2, 1, 1, 0, 2, 2, 1]}]

def initial(cfg):return tuple(cfg['start'])

def solved(cfg,state):return state==tuple(cfg['goal'])

def advance(cfg,state,index):
    if type(index) is not int or not 0<=index<len(state):return state
    old=state[index];new=(old+1)%3
    return tuple(new if i==index else old if color==new else color for i,color in enumerate(state))

def centers(cfg):
    n=len(cfg['start'])
    if n==3:return ((15,32),(32,32),(49,32))
    if n==4:return ((22,22),(42,22),(22,42),(42,42))
    if n==6:return tuple((x,y) for y in (21,43) for x in (15,32,49))
    if n==7:return ((15,15),(32,15),(49,15),(32,32),(15,49),(32,49),(49,49))
    return tuple((x,y) for y in (15,32,49) for x in (15,32,49))

import numpy as np
from arcengine import ARCBaseGame,Camera,Level,Sprite,GameAction
COLORS=(10,12,6)

class Sg20(ARCBaseGame):
    def __init__(self,seed=0):
        self.cfg=None;self.state=None;self.history=[];self.selected=None;self.changed=()
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='borrowing')],grid_size=(64,64),data={'layout':c},name='Borrowing %d'%(i+1)) for i,c in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg20-v1',levels=levels,camera=Camera(background=5,letter_box=5),available_actions=[6,7],seed=seed)

    def on_set_level(self,level):
        self.cfg=level.get_data('layout');self.state=initial(self.cfg);self.history=[];self.selected=None;self.changed=();self._paint()

    def step(self):
        a=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1]);self.selected=None;self.changed=()
        if a==7 and self.history:self.state=self.history.pop()
        elif a==6:
            d=self.action.data or {};x,y=d.get('x',-99),d.get('y',-99)
            if type(x) is int and type(y) is int:
                for i,(cx,cy) in enumerate(centers(self.cfg)):
                    if cx-6<=x<=cx+6 and cy-6<=y<=cy+6:
                        self.selected=i;n=advance(self.cfg,self.state,i)
                        self.changed=tuple(k for k in range(len(n)) if n[k]!=self.state[k])
                        self.history.append(self.state);self.state=n;break
        self._paint()
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    def _paint(self):
        c=np.full((64,64),5,dtype=np.int64)
        for i,(x,y) in enumerate(centers(self.cfg)):
            goal=COLORS[self.cfg['goal'][i]];color=COLORS[self.state[i]]
            c[y-6,x-6:x+7]=goal;c[y+6,x-6:x+7]=goal;c[y-6:y+7,x-6]=goal;c[y-6:y+7,x+6]=goal
            c[y-4:y+5,x-4:x+5]=color
            if i==self.selected:c[y-1:y+2,x-1:x+2]=0
            elif i in self.changed:
                c[y-4,x-4:x-2]=0;c[y+4,x+3:x+5]=0
        self.current_level.remove_all_sprites();self.current_level.add_sprite(Sprite(pixels=c,name='borrowed-colors',x=0,y=0,layer=0))
