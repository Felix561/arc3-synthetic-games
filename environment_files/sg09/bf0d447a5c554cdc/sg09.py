FIXED_LEVELS = [{'rows': ['#######', '#######', '..bb...', '..bb...', '#######', '#######', '#######'], 'switches': [[0, 3], [5, 3]], 'start': [0, 2, 0, 0, 0], 'phases': 2, 'badges': [], 'dock': [[5, 2], [6, 2]]}, {'rows': ['..bb...', '..bb...', '#####..', '.....aa', '.....aa', '..#####', '..#####'], 'switches': [[0, 1], [5, 1], [1, 4]], 'start': [0, 0, 0, 0, 0], 'phases': 2, 'badges': [[0, 6]], 'dock': [[0, 5], [0, 6]]}, {'rows': ['..aaa..', '..###..', '.####..', 'b#####b', '..####b', '..##...', '..aaa..'], 'switches': [[0, 1], [6, 1], [5, 5], [0, 5]], 'start': [0, 0, 0, 1, 0], 'phases': 2, 'badges': [[6, 1], [5, 5], [0, 5]], 'dock': [[1, 0], [1, 1]]}, {'rows': ['..bbb..', '..###..', '.####..', 'a#####c', '..####c', '..##...', '..aaa..'], 'switches': [[0, 1], [6, 1], [0, 6]], 'start': [0, 0, 0, 0, 0], 'phases': 3, 'badges': [[6, 1], [5, 5], [0, 5]], 'dock': [[5, 0], [6, 0]]}, {'rows': ['..bbb..', '..###..', '.####..', 'a##...c', '..###.c', '..##...', '..aaa..'], 'switches': [[0, 1], [6, 1], [3, 3], [0, 6]], 'start': [0, 0, 0, 0, 0], 'phases': 3, 'badges': [[6, 1], [3, 3], [0, 5]], 'dock': [[0, 1], [1, 1]]}, {'rows': ['..bbb..', '..###..', 'a#####c', '...b...', '..###..', 'c#####a', '..bbb..'], 'switches': [[0, 0], [6, 1], [1, 3], [6, 6]], 'start': [0, 0, 0, 0, 0], 'phases': 3, 'badges': [[6, 0], [4, 3], [0, 6]], 'dock': [[1, 0], [1, 1]]}, {'rows': ['..bbb..', '..###..', 'a#...#c', '...c...', '..###..', 'b#####a', '..ccc..'], 'switches': [[0, 0], [6, 1], [3, 2], [6, 6]], 'start': [0, 0, 0, 0, 0], 'phases': 3, 'badges': [[6, 0], [6, 6]], 'dock': [[5, 3], [4, 3]]}]

import numpy as np
from arcengine import ARCBaseGame, Camera, Level, Sprite, GameAction

VECTORS=((1,0),(0,1),(-1,0),(0,-1))
COLORS=(10,6,11)

def body(state):
    x,y,d,_,_=state;dx,dy=VECTORS[d]
    return ((x,y),(x+dx,y+dy))

def solid(cfg,x,y,phase):
    if not (0<=x<7 and 0<=y<7):return False
    tile=cfg['rows'][y][x]
    return tile=='.' or tile==chr(97+phase)

def visible_switch(cfg,state,switch):
    if list(switch) not in cfg['switches']:return False
    u,v=switch
    for x,y in body(state):
        if x!=u and y!=v:continue
        dx=0 if x==u else (1 if u>x else -1)
        dy=0 if y==v else (1 if v>y else -1)
        px,py=x,y;clear=True
        while (px,py)!=(u,v):
            px+=dx;py+=dy
            if not solid(cfg,px,py,state[3]):clear=False;break
        if clear:return True
    return False

def advance(cfg,state,action):
    x,y,d,phase,badges=state
    number,tx,ty=action
    if number in (1,2,3,4):
        dx,dy={1:(0,-1),2:(0,1),3:(-1,0),4:(1,0)}[number];x+=dx;y+=dy
    elif number==5:d=(d+1)%4
    elif number==6:
        if not visible_switch(cfg,state,(tx,ty)):return state
        phase=(phase+1)%cfg['phases']
    else:return state
    nxt=(x,y,d,phase,badges)
    if not all(solid(cfg,u,v,phase) for u,v in body(nxt)):return state
    for i,gem in enumerate(cfg['badges']):
        if tuple(gem) in body(nxt):badges|=1<<i
    return (x,y,d,phase,badges)

def solved(cfg,state):
    return (set(body(state))==set(map(tuple,cfg['dock']))
            and state[4]==(1<<len(cfg['badges']))-1)

class Sg09(ARCBaseGame):
    def __init__(self,seed=0):
        self.cfg=None;self.state=None;self.history=[];self.rejected=False
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='hull')],grid_size=(64,64),data={'layout':c},name='Causeway %d'%(i+1)) for i,c in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg09-v1',levels=levels,camera=Camera(background=5,letter_box=5),available_actions=[1,2,3,4,5,6,7],seed=seed)

    def on_set_level(self,level):
        self.cfg=level.get_data('layout');self.state=tuple(self.cfg['start']);self.history=[];self.rejected=False;self._paint()

    def step(self):
        n=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1]);self.rejected=False
        if n==7:
            if self.history:self.state=self.history.pop()
        elif n:
            tx=ty=-99
            if n==6:
                data=self.action.data or {};px,py=data.get('x',-99),data.get('y',-99)
                if type(px) is int and type(py) is int:tx,ty=(px-7)//7,(py-11)//7
            nxt=advance(self.cfg,self.state,(n,tx,ty))
            if nxt!=self.state:self.history.append(self.state);self.state=nxt
            else:self.rejected=True
        self._paint()
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    @staticmethod
    def rect(c,x,y,w,h,col):c[max(0,y):min(64,y+h),max(0,x):min(64,x+w)]=col

    def _paint(self):
        c=np.full((64,64),5,dtype=np.int64)
        phase=self.state[3]
        # Sparse water streaks sit outside the logical platforms.
        for y in (17,31,45,57):c[y,1:4]=4;c[y-3,60:63]=4
        for i in range(self.cfg['phases']):
            x=8+i*12;self.rect(c,x,1,9,7,2 if i==phase else 4)
            self.rect(c,x+2,2,5,5,COLORS[i]);c[4,x+4]=0 if i==phase else 5
        for i in range(len(self.cfg['badges'])):
            sx=44+i*5
            self.rect(c,sx,2,4,5,2)
            self.rect(c,sx+1,3,2,3,14 if self.state[4]&(1<<i) else 5)
        for y,row in enumerate(self.cfg['rows']):
            for x,tile in enumerate(row):
                if tile=='#':continue
                px,py=7+x*7,11+y*7
                col=2 if tile=='.' else COLORS[ord(tile)-97]
                if solid(self.cfg,x,y,phase):
                    self.rect(c,px,py,6,6,col)
                    self.rect(c,px+1,py+1,4,4,3 if tile=='.' else col)
                    c[py+5,px:px+6]=4
                else:
                    c[py,px: px+2]=col;c[py+4,px+4:px+6]=col
                    c[py+1,px]=col;c[py+3,px+5]=col
                if [x,y] in self.cfg['dock']:
                    c[py+1,px+1:px+5]=0;c[py+4,px+1:px+5]=0
                    c[py+1:py+5,px+1]=0;c[py+1:py+5,px+4]=0
        # Thin sight beams terminate at crystals along the actual clear support.
        for sx,sy in self.cfg['switches']:
            if not visible_switch(self.cfg,self.state,(sx,sy)):continue
            for bx,by in body(self.state):
                if bx!=sx and by!=sy:continue
                dx=0 if bx==sx else (1 if sx>bx else -1)
                dy=0 if by==sy else (1 if sy>by else -1)
                cells=[];u,v=bx,by
                while (u,v)!=(sx,sy):
                    u+=dx;v+=dy;cells.append((u,v))
                if not all(solid(self.cfg,u,v,phase) for u,v in cells):continue
                px,py=10+bx*7,14+by*7;qx,qy=10+sx*7,14+sy*7
                if py==qy:c[py,min(px,qx):max(px,qx)+1]=1
                else:c[min(py,qy):max(py,qy)+1,px]=1
        for x,y in self.cfg['switches']:
            px,py=7+x*7,11+y*7
            col=0 if visible_switch(self.cfg,self.state,(x,y)) else 2
            self.rect(c,px+2,py,2,6,col);self.rect(c,px,py+2,6,2,col)
            self.rect(c,px+2,py+2,2,2,COLORS[(phase+1)%self.cfg['phases']])
        for i,(x,y) in enumerate(self.cfg['badges']):
            if not self.state[4]&(1<<i):
                px,py=7+x*7,11+y*7
                c[py+1,px+2:px+4]=14;c[py+4,px+2:px+4]=14
                c[py+2:py+4,px+1:px+5]=14
        (x,y),(u,v)=body(self.state)
        px,py=7+x*7,11+y*7;qx,qy=7+u*7,11+v*7
        self.rect(c,min(px,qx),min(py,qy),abs(px-qx)+6,abs(py-qy)+6,0)
        self.rect(c,px+1,py+1,4,4,COLORS[phase])
        c[py+2:py+4,px+2:px+4]=5
        # The circular hinge is at the actual fixed end, with a rotation cue.
        c[py,px+1:px+5]=COLORS[phase];c[py+1,px]=COLORS[phase]
        # A visible hinge distinguishes the pivot end from the trailing end.
        self.rect(c,qx+2,qy+2,2,2,2)
        if self.rejected:c[py+5,px:px+6]=8
        self.current_level.remove_all_sprites();self.current_level.add_sprite(Sprite(pixels=c,name='phase-hull',x=0,y=0,layer=0))
