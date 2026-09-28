FIXED_LEVELS = [{'start': [[1, 1], [1, 2]], 'goal': [[2, 3]]}, {'start': [[2, 2], [2, 1], [0, 1]], 'goal': [[1, 4]]}, {'start': [[0, 1], [0, 1], [0, 1], [0, 1], [1, 2]], 'goal': [[2, 4], [1, 2]]}, {'start': [[0, 2], [0, 1], [1, 1], [1, 2], [1, 1], [1, 1]], 'goal': [[0, 2], [1, 6]]}, {'start': [[0, 1], [0, 1], [2, 2], [2, 2], [2, 1], [2, 1]], 'goal': [[2, 8]]}, {'start': [[0, 1], [0, 1], [0, 1], [0, 1], [2, 1], [2, 1], [2, 2], [2, 1]], 'goal': [[2, 4], [1, 5]]}, {'start': [[2, 4], [2, 2], [1, 1], [1, 2], [2, 1], [2, 1], [0, 1], [1, 1], [1, 1]], 'goal': [[2, 14]]}]

def initial(cfg):return tuple(tuple(t) for t in cfg['start'])
def solved(cfg,state):return state==tuple(tuple(t) for t in cfg['goal'])

def advance(cfg,state,index):
    if type(index) is not int or not 0<=index<len(state)-1:return state
    a,b=state[index:index+2]
    if a[0]!=b[0]:return state
    return state[:index]+(((a[0]+1)%3,a[1]+b[1]),)+state[index+2:]

def geometry(cfg):
    total=sum(w for c,w in cfg['start']);unit=56//total
    return (64-total*unit)//2,unit

def boundaries(cfg,state):
    left,unit=geometry(cfg);positions=[];used=0
    for c,w in state[:-1]:
        used+=w;positions.append(left+used*unit-1)
    return positions

import numpy as np
from arcengine import ARCBaseGame,Camera,Level,Sprite,GameAction

COLORS=(10,6,12)

class Sg15(ARCBaseGame):
    def __init__(self,seed=0):
        self.cfg=None;self.state=None;self.history=[];self.selected=0;self.rejected=False
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='fusion')],grid_size=(64,64),data={'layout':c},name='Fusion %d'%(i+1)) for i,c in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg15-v1',levels=levels,camera=Camera(background=5,letter_box=5),available_actions=[3,4,5,6,7],seed=seed)

    def on_set_level(self,level):
        self.cfg=level.get_data('layout');self.state=initial(self.cfg);self.history=[];self.selected=0;self.rejected=False;self._paint()

    def step(self):
        a=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1]);self.rejected=False;choice=None
        if a==7:
            if self.history:self.state=self.history.pop()
            self.selected=0
        elif a in (3,4) and len(self.state)>1:self.selected=(self.selected+(1 if a==4 else -1))%(len(self.state)-1)
        elif a==5:choice=self.selected
        elif a==6:
            d=self.action.data or {};x,y=d.get('x',-99),d.get('y',-99)
            if type(x) is int and type(y) is int and 32<=y<=59:
                gaps=boundaries(self.cfg,self.state)
                if gaps:
                    i=min(range(len(gaps)),key=lambda j:abs(gaps[j]-x))
                    if abs(gaps[i]-x)<=2:choice=i;self.selected=i
        if choice is not None:
            nxt=advance(self.cfg,self.state,choice)
            if nxt!=self.state:self.history.append(self.state);self.state=nxt
            else:self.rejected=True
            self.selected=min(self.selected,max(0,len(self.state)-2))
        self._paint()
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    def _paint(self):
        c=np.full((64,64),5,dtype=np.int64);left,unit=geometry(self.cfg)
        for state,y,height in ((self.cfg['goal'],10,8),(self.state,35,15)):
            x=left
            for color,width in state:
                right=x+width*unit-1;c[y:y+height,x:right]=COLORS[color]
                # Unit ticks make conserved lengths readable without numerals.
                for k in range(width):c[y+height-1,x+k*unit]=4
                x+=width*unit
        total=sum(w for color,w in self.state)*unit
        c[20,left:left+total]=3
        for i,x in enumerate(boundaries(self.cfg,self.state)):
            legal=self.state[i][0]==self.state[i+1][0]
            col=0 if legal else 3
            c[52,x-1:x+2]=col;c[53,x]=col
            if i==self.selected:
                c[56,x-2:x+3]=8 if self.rejected else 11;c[55,x]=8 if self.rejected else 11
        for i in range(7):c[63,5+i*8:11+i*8]=14 if i<self.level_index else 4
        self.current_level.remove_all_sprites();self.current_level.add_sprite(Sprite(pixels=c,name='fusion-ribbon',x=0,y=0,layer=0))
