FIXED_LEVELS = [
    {'start': [4, 0], 'goal': [2, 2]},
    {'start': [4, 0, 0], 'goal': [2, 1, 1]},
    {'start': [0, 1, 6], 'goal': [1, 3, 3]},
    {'start': [6, 0, 6, 0], 'goal': [5, 3, 3, 1]},
    {'start': [0, 6, 0, 6], 'goal': [2, 2, 3, 5]},
    {'start': [6, 0, 1, 6, 0], 'goal': [4, 4, 2, 2, 1]},
    {'start': [0, 1, 4, 6, 6], 'goal': [2, 2, 4, 4, 5]},
]

import numpy as np
from arcengine import ARCBaseGame, Camera, GameAction, Level, Sprite


def initial(cfg):
    return tuple(cfg['start'])


def solved(cfg, state):
    return state == tuple(cfg['goal'])


def advance(cfg, state, valve):
    if type(valve) is not int or not 0 <= valve < len(state)-1:
        return state
    values = list(state)
    a, b = values[valve], values[valve+1]
    if abs(a-b) < 2:
        return state
    high, low = (a+b+1)//2, (a+b)//2
    values[valve], values[valve+1] = (high, low) if a > b else (low, high)
    return tuple(values)


class Sg26(ARCBaseGame):
    def __init__(self, seed=0):
        self.cfg=None;self.state=None;self.history=[];self.transition=None;self.rejected=False
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='basins')],
                      grid_size=(64,64),data={'layout':cfg},name='Basins %d'%(i+1))
                for i,cfg in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg26-v1',levels=levels,camera=Camera(background=5,letter_box=5),
                         available_actions=[6,7],seed=seed)

    def on_set_level(self, level):
        self.cfg=level.get_data('layout');self.state=initial(self.cfg);self.history=[]
        self.transition=None;self.rejected=False;self._paint()

    def geometry(self):
        n=len(self.state)
        width,gap={2:(12,10),3:(11,7),4:(10,5)}.get(n,(8,4))
        left=(64-(n*width+(n-1)*gap))//2
        xs=[left+i*(width+gap) for i in range(n)]
        centers=[(xs[i]+width+xs[i+1]-1)//2 for i in range(n-1)]
        return xs,width,centers

    def step(self):
        if self.transition is not None:
            valve,new=self.transition;self.state=new;self.transition=None;self._paint()
            if solved(self.cfg,self.state):self.next_level()
            self.complete_action();return
        action_id=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1])
        self.rejected=False
        if action_id==7:
            if self.history:self.state=self.history.pop()
        elif action_id==6:
            data=self.action.data or {};x,y=data.get('x',-99),data.get('y',-99)
            if type(x) is int and type(y) is int and 47<=y<=59:
                _,_,centers=self.geometry()
                hit=next((i for i,cx in enumerate(centers) if abs(x-cx)<=3),None)
                if hit is not None:
                    new=advance(self.cfg,self.state,hit)
                    if new!=self.state:
                        self.history.append(self.state);self.transition=(hit,new)
                        self._paint();return
                    self.rejected=True
        self._paint()
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    @staticmethod
    def rect(c,x,y,w,h,color):
        c[max(0,y):min(64,y+h),max(0,x):min(64,x+w)]=color

    def _paint(self):
        c=np.full((64,64),5,dtype=np.int64)
        xs,width,centers=self.geometry();bottom=53
        for i,(x,volume) in enumerate(zip(xs,self.state)):
            self.rect(c,x+1,20,width-2,34,4)
            self.rect(c,x,19,2,36,2);self.rect(c,x+width-2,19,2,36,2)
            self.rect(c,x,54,width,2,2)
            if volume:
                water_top=bottom-volume*5+1
                self.rect(c,x+2,water_top,width-4,bottom-water_top+1,10)
                self.rect(c,x+2,water_top,width-4,1,0)
            # A white physical fill line marks the intended water surface.
            mark=bottom-self.cfg['goal'][i]*5+1
            c[mark,x-2:x]=0;c[mark,x+width:x+width+2]=0
        for i,cx in enumerate(centers):
            left=xs[i]+width;right=xs[i+1]
            self.rect(c,left,51,right-left,3,3)
            color=0 if self.transition and self.transition[0]==i else (8 if self.rejected else 1)
            self.rect(c,cx-2,49,5,8,color)
            self.rect(c,cx-1,50,3,6,5)
            if self.transition and self.transition[0]==i:
                # The bright connection is a one-frame, local flow preview.
                c[52,left:right]=10;c[47,cx]=10
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=c,name='equalizing-basins',x=0,y=0,layer=0))
