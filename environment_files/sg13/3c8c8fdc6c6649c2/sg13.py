FIXED_LEVELS = [{'capacity': [2, 2], 'start': [[0], []], 'goal': [[], [1]]}, {'capacity': [2, 2], 'start': [[0, 2], []], 'goal': [[3, 1], []]}, {'capacity': [2, 2, 2], 'goal': [[0, 2], [1], []], 'start': [[], [0, 2], [0]]}, {'capacity': [3, 2, 2], 'start': [[0, 2, 1], [], [2, 2]], 'goal': [[0, 0, 2], [2, 2], []]}, {'capacity': [3, 3, 2], 'start': [[3, 3], [1, 1], [2]], 'goal': [[0, 0, 2], [2, 2], []]}, {'capacity': [3, 3, 3], 'start': [[3, 3, 1], [1, 1, 3], []], 'goal': [[0, 0, 2], [2, 2, 0], []]}, {'capacity': [3, 3, 3], 'start': [[0, 3], [2, 0], [3, 1, 1]], 'goal': [[0, 0, 2], [2, 2, 0], [0]]}]

import numpy as np
from arcengine import ARCBaseGame,Camera,Level,Sprite,GameAction

COLORS=(10,12,6,14)

def initial(cfg):return tuple(tuple(x) for x in cfg['start'])
def solved(cfg,state):return state==tuple(tuple(x) for x in cfg['goal'])
def packet(stack):
    if not stack:return 0
    n=1
    while n<len(stack) and stack[-n-1]==stack[-1]:n+=1
    return n

def advance(cfg,state,action):
    kind,a,b=action
    if a not in range(len(state)):return state
    stacks=list(state)
    if kind=='flip':
        stacks[a]=tuple(x^1 for x in reversed(state[a]))
    elif kind=='move':
        if b not in range(len(state)) or a==b:return state
        n=packet(state[a])
        if not n or len(state[b])+n>cfg['capacity'][b]:return state
        stacks[a]=state[a][:-n]
        stacks[b]=state[b]+tuple(x^1 for x in reversed(state[a][-n:]))
    else:return state
    return tuple(stacks)

class Sg13(ARCBaseGame):
    def __init__(self,seed=0):
        self.cfg=None;self.state=None;self.history=[];self.selected=None;self.rejected=None;self.transition=None
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='trays')],grid_size=(64,64),data={'layout':c},name='Turnover %d'%(i+1)) for i,c in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg13-v1',levels=levels,camera=Camera(background=5,letter_box=5),available_actions=[3,4,5,6,7],seed=seed)

    def on_set_level(self,level):
        self.cfg=level.get_data('layout');self.state=initial(self.cfg);self.history=[];self.selected=None;self.rejected=None;self.transition=None;self._paint()

    def step(self):
        if self.transition is not None:
            operation,nxt=self.transition
            self.transition=None;self.state=nxt;self._paint()
            if solved(self.cfg,self.state):self.next_level()
            self.complete_action();return
        n=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1]);self.rejected=None
        operation=None
        if n==7:
            if self.history:self.state=self.history.pop()
            self.selected=None
        elif n in (3,4):
            self.selected=((self.selected if self.selected is not None else (-1 if n==4 else 0))+(1 if n==4 else -1))%len(self.state)
        elif n==5 and self.selected is not None:operation=('flip',self.selected,-1)
        elif n==6:
            d=self.action.data or {};x,y=d.get('x',-99),d.get('y',-99)
            if type(x) is int and type(y) is int:
                if 16<=y<=48:
                    hit=next((i for i,center in enumerate(self.centers()) if abs(x-center)<=7),None)
                    if hit is not None:
                        if self.selected is None:self.selected=hit
                        elif self.selected==hit:operation=('flip',hit,-1)
                        else:operation=('move',self.selected,hit)
        if operation:
            nxt=advance(self.cfg,self.state,operation)
            if nxt!=self.state:
                self.history.append(self.state);self.transition=(operation,nxt)
            else:self.rejected=operation[2] if operation[0]=='move' else operation[1]
            self.selected=None
        self._paint()
        if self.transition is not None:return
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    def centers(self):
        n=len(self.state)
        return [16,47] if n==2 else ([11,32,53] if n==3 else [8,24,40,56])

    @staticmethod
    def rect(c,x,y,w,h,col):c[max(0,y):min(64,y+h),max(0,x):min(64,x+w)]=col

    def _paint(self):
        c=np.full((64,64),5,dtype=np.int64)
        for i,x in enumerate(self.centers()):
            capacity=self.cfg['capacity'][i];top=43-capacity*9
            can_receive=(self.selected is not None and i!=self.selected and
                         len(self.state[i])+packet(self.state[self.selected])<=capacity)
            rim=0 if self.selected==i else (1 if can_receive else 3)
            c[top:47,x-8]=rim;c[top:47,x+8]=rim;c[46,x-8:x+9]=rim
            goal=self.cfg['goal'][i]
            for j in range(capacity):
                y=36-j*9
                # Hollow full-size targets sit exactly where their objects belong.
                edge=COLORS[goal[j]] if j<len(goal) else 4
                c[y:y+8,x-6]=edge;c[y:y+8,x+6]=edge
                c[y,x-6:x+7]=edge;c[y+7,x-6:x+7]=edge
                if j<len(goal):c[y+6,x-4:x+5]=COLORS[goal[j]^1]
            for j,t in enumerate(self.state[i]):
                y=36-j*9
                # Main face and substantial underside stay visible together.
                self.rect(c,x-5,y+1,11,4,COLORS[t])
                self.rect(c,x-4,y+5,9,2,COLORS[t^1])
                if j and self.state[i][j-1]==t:c[y+8:y+10,x-1:x+2]=COLORS[t]
            if self.selected==i:
                # Brackets pick out precisely the packet that would move.
                n=packet(self.state[i])
                if n:
                    low=36-(len(self.state[i])-n)*9
                    high=36-(len(self.state[i])-1)*9
                    c[high-1:low+8,x-7]=0;c[high-1:low+8,x+7]=0
                    c[high-1,x-7:x-4]=0;c[high-1,x+5:x+8]=0
                else:c[top-3:top,x-2:x+3]=0
            if self.rejected==i:
                c[48,x-6:x+7]=1;c[49,x-6]=1;c[49,x+6]=1
        if self.transition is not None:
            # A native intermediate frame makes the packet's movement and
            # turning visible before the destination state appears.
            (kind,a,b),nxt=self.transition
            x0=self.centers()[a]
            x1=self.centers()[b] if kind=='move' else x0
            left,right=sorted((x0,x1))
            c[11,left:right+1]=1
            mid=(x0+x1)//2
            face=self.state[a][-1]
            self.rect(c,mid-5,7,11,4,COLORS[face])
            self.rect(c,mid-5,11,11,4,COLORS[face^1])
            c[6,mid-6:mid+7]=0
        self.current_level.remove_all_sprites();self.current_level.add_sprite(Sprite(pixels=c,name='turnover-trays',x=0,y=0,layer=0))
