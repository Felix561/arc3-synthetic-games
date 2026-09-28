FIXED_LEVELS = [{'walls': [], 'pads': [7], 'start': [7], 'headings': [3], 'goal': [9]}, {'walls': [], 'pads': [7, 9], 'start': [7], 'headings': [3], 'goal': [21]}, {'walls': [10, 26], 'pads': [7, 8, 19, 25], 'start': [7, 25], 'headings': [3, 3], 'goal': [9, 13]}, {'walls': [5, 8, 9, 16, 19, 21, 32, 35], 'pads': [12, 14, 22, 23, 34], 'start': [12, 23], 'headings': [3, 2], 'goal': [26, 17]}, {'walls': [0, 1, 2, 3, 4, 8, 10, 22, 24, 26, 27, 31, 34], 'pads': [7, 13, 15, 25], 'start': [7, 15], 'headings': [3, 2], 'goal': [19, 6]}, {'walls': [1, 2, 15, 19, 25, 27, 30, 35], 'pads': [4, 5, 16, 17, 28], 'start': [4, 17], 'headings': [3, 2], 'goal': [10, 28]}, {'walls': [2, 7, 9, 11, 12, 15, 17, 18, 22, 23, 26, 32, 34], 'pads': [1, 13, 19, 21, 25], 'start': [13, 25], 'headings': [3, 2], 'goal': [27, 33]}]

N=6
DIRS=((0,-1),(0,1),(-1,0),(1,0))

def initial(cfg):return tuple(cfg['start']),tuple(cfg['headings'])

def solved(cfg,state):return state[0]==tuple(cfg['goal'])

def advance(cfg,state,action):
    positions,headings=state
    if action in (1,2,3,4):
        return positions,tuple(action-1 if p in cfg['pads'] else h for p,h in zip(positions,headings))
    if action!=5:return state
    walls=set(cfg['walls']);dest=[]
    for p,h in zip(positions,headings):
        dx,dy=DIRS[h];x,y=p%N+dx,p//N+dy
        q=y*N+x
        dest.append(q if 0<=x<N and 0<=y<N and q not in walls else p)
    # Contested destinations and head-on swaps stop both; trains can advance.
    blocked={i for i,q in enumerate(dest) if q==positions[i] or dest.count(q)>1}
    for i,q in enumerate(dest):
        for j,r in enumerate(dest):
            if i!=j and q==positions[j] and r==positions[i]:blocked.update((i,j))
    changed=True
    while changed:
        changed=False
        for i,q in enumerate(dest):
            if i not in blocked and any(q==positions[j] for j in blocked):blocked.add(i);changed=True
    return tuple(p if i in blocked else dest[i] for i,p in enumerate(positions)),headings

import numpy as np
from arcengine import ARCBaseGame,Camera,Level,Sprite,GameAction
COLORS=(12,10)

class Sg17(ARCBaseGame):
    def __init__(self,seed=0):
        self.cfg=None;self.state=None;self.history=[];self.flash=0
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='memory')],grid_size=(64,64),data={'layout':c},name='Memory %d'%(i+1)) for i,c in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg17-v1',levels=levels,camera=Camera(background=5,letter_box=5),available_actions=[1,2,3,4,5,7],seed=seed)

    def on_set_level(self,level):
        self.cfg=level.get_data('layout');self.state=initial(self.cfg);self.history=[];self.flash=0;self._paint()

    def step(self):
        a=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1]);self.flash=a
        if a==7:
            if self.history:self.state=self.history.pop()
        elif a in (1,2,3,4,5):
            nxt=advance(self.cfg,self.state,a)
            if nxt!=self.state:self.history.append(self.state);self.state=nxt
        self._paint()
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    def _paint(self):
        c=np.full((64,64),5,dtype=np.int64)
        for p in range(36):
            x,y=8+p%6*8,6+p//6*8
            if p in self.cfg['walls']:c[y:y+7,x:x+7]=3
            else:c[y+3,x+3]=4
            if p in self.cfg['pads']:
                col=7 if self.flash in (1,2,3,4) and p in self.state[0] else 15
                for yy,xx in ((y,x),(y,x+6),(y+6,x),(y+6,x+6)):c[yy:yy+2,xx:xx+2]=col
        for i,p in enumerate(self.cfg['goal']):
            x,y=8+p%6*8,6+p//6*8;col=COLORS[i]
            c[y,x:x+7]=col;c[y+6,x:x+7]=col;c[y:y+7,x]=col;c[y:y+7,x+6]=col
        for i,(p,h) in enumerate(zip(*self.state)):
            x,y=8+p%6*8+1,6+p//6*8+1;c[y:y+5,x:x+5]=COLORS[i]
            # Explicit solid arrowhead inside each substantial colored piece.
            for px,py in ((0,2),(1,2),(2,2),(3,1),(3,2),(3,3),(4,2)):
                if h==2:px=4-px
                elif h==1:px,py=py,px
                elif h==0:px,py=py,4-px
                c[y+py,x+px]=5
        # A single advance glyph emphasizes the separate pulse action.
        col=0 if self.flash==5 else 3
        for x in (29,34):
            c[56:61,x]=col;c[57:60,x+1]=col;c[58,x+2]=col
        self.current_level.remove_all_sprites();self.current_level.add_sprite(Sprite(pixels=c,name='programmed-pieces',x=0,y=0,layer=0))
