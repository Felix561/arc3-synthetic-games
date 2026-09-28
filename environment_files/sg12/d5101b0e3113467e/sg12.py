FIXED_LEVELS = [{'rows': ['.....', '.....', '.....', '.....', '.....'], 'start': 11, 'blocks': [[12, 0]], 'goals': [[13, 1]], 'devices': [[7, 1, 'col']]}, {'rows': ['.....', '...#.', '...W.', '...#.', '.....'], 'start': 11, 'blocks': [[12, 0]], 'goals': [[13, -1]], 'devices': [[7, -1, 'col']]}, {'rows': ['.....', '.....', '...I.', '.....', '.....'], 'start': 11, 'blocks': [[12, 0]], 'goals': [[14, 0]], 'devices': [[7, 1, 'col'], [14, -1, 'row']]}, {'rows': ['#####', '#....', '#.IB.', '#..##', '#..##'], 'start': 16, 'blocks': [[17, 0]], 'goals': [[14, 2]], 'devices': [[16, 1, 'row'], [9, 1, 'col']]}, {'rows': ['#####', '#...#', '#...#', '#...#', '#...#'], 'start': 21, 'blocks': [[12, 0], [17, 0]], 'goals': [[16, 1], [18, -1]], 'devices': [[6, 1, 'col'], [8, -1, 'col']]}, {'rows': ['#####', '..#.I', '..W..', '..W..', '###..'], 'start': 15, 'blocks': [[11, 0], [19, 0]], 'goals': [[11, -1], [9, 1]], 'devices': [[16, -1, 'col'], [18, 1, 'row']]}, {'rows': ['#####', '..#.I', '..WB.', '..W..', '###..'], 'start': 15, 'blocks': [[11, 0], [19, 0]], 'goals': [[14, -1], [9, 0]], 'devices': [[16, -1, 'col'], [18, 1, 'row'], [9, -1, 'col']]}]

import numpy as np
from arcengine import ARCBaseGame,Camera,Level,Sprite,GameAction

COLORS={-2:9,-1:10,0:1,1:12,2:8}
DIRECTIONS={1:(0,-1),2:(0,1),3:(-1,0),4:(1,0)}

def adjacent(a,b):return abs(a%5-b%5)+abs(a//5-b//5)==1

def terrain(cfg,p,melt,crumble):
    if not 0<=p<25:return '#'
    t=cfg['rows'][p//5][p%5]
    if t=='I' and melt&(1<<p):return '.'
    if t=='B' and crumble&(1<<p):return '#'
    return t

def react(cfg,blocks,melt,crumble):
    for p,t in blocks:
        for q in range(25):
            if not adjacent(p,q):continue
            tile=cfg['rows'][q//5][q%5]
            if t>=1 and tile=='I':melt|=1<<q
            if t==2 and tile=='B':crumble|=1<<q
    return melt,crumble

def supported(cfg,p,blocks,melt,crumble):
    tile=terrain(cfg,p,melt,crumble)
    if tile in ('#','I'):return False
    if tile=='W':return any(t<0 and (p==q or adjacent(p,q)) for q,t in blocks)
    return True

def initial(cfg):
    blocks=tuple(sorted(map(tuple,cfg['blocks'])));m,c=react(cfg,blocks,0,0)
    return (cfg['start'],blocks,m,c)

def advance(cfg,state,action):
    pos,blocks,melt,crumble=state;kind,value=action
    proposed=list(blocks);newpos=pos
    if kind=='move':
        dx,dy=DIRECTIONS[value];x,y=pos%5+dx,pos//5+dy
        if not (0<=x<5 and 0<=y<5):return state
        newpos=y*5+x
        index=next((i for i,(p,t) in enumerate(blocks) if p==newpos),None)
        if index is not None:
            u,v=x+dx,y+dy
            if not (0<=u<5 and 0<=v<5):return state
            destination=v*5+u
            if any(p==destination for p,t in blocks):return state
            proposed[index]=(destination,blocks[index][1])
    elif kind=='pulse':
        if value not in range(len(cfg['devices'])):return state
        source,delta,axis=cfg['devices'][value]
        if pos!=source and not adjacent(pos,source):return state
        affected=set()
        for p,t in blocks:
            if axis=='row' and p//5!=source//5:continue
            if axis=='col' and p%5!=source%5:continue
            step=(1 if p>source else -1)*(1 if axis=='row' else 5)
            ray=range(source+step,p+step,step) if p!=source else ()
            if all(terrain(cfg,q,melt,crumble) not in ('#','I') for q in ray):affected.add(p)
        proposed=[(p,max(-2,min(2,t+delta))) if p in affected else (p,t) for p,t in blocks]
    else:return state
    proposed=tuple(sorted(proposed));m,c=react(cfg,proposed,melt,crumble)
    if not supported(cfg,newpos,proposed,m,c):return state
    if any(not supported(cfg,p,proposed,m,c) for p,t in proposed):return state
    return (newpos,proposed,m,c)

def solved(cfg,state):return state[1]==tuple(sorted(map(tuple,cfg['goals'])))

class Sg12(ARCBaseGame):
    def __init__(self,seed=0):
        self.cfg=None;self.state=None;self.history=[];self.rejected=False
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='thermal')],grid_size=(64,64),data={'layout':c},name='Thermal %d'%(i+1)) for i,c in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg12-v1',levels=levels,camera=Camera(background=5,letter_box=5),available_actions=[1,2,3,4,5,6,7],seed=seed)

    def on_set_level(self,level):
        self.cfg=level.get_data('layout');self.state=initial(self.cfg);self.history=[];self.rejected=False;self._paint()

    def step(self):
        n=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1]);self.rejected=False
        if n==7:
            if self.history:self.state=self.history.pop()
        elif n:
            action=('none',-1)
            undone=False
            if n in DIRECTIONS:action=('move',n)
            elif n==5:
                choices=[i for i,(p,d,a) in enumerate(self.cfg['devices']) if p==self.state[0] or adjacent(p,self.state[0])]
                if len(choices)==1:action=('pulse',choices[0])
            elif n==6:
                data=self.action.data or {};x,y=data.get('x',-99),data.get('y',-99)
                if type(x) is int and type(y) is int:
                    gx,gy=(x-9)//9,(y-12)//9
                    if 0<=gx<5 and 0<=gy<5:
                        p=gy*5+gx
                        # The hollow echo at the previous avatar position is a
                        # direct, visible way to reverse a mistaken push.
                        if self.history and p==self.history[-1][0] and p!=self.state[0] and all(p!=q for q,d,a in self.cfg['devices']):
                            self.state=self.history.pop();undone=True
                        else:
                            for i,(q,d,a) in enumerate(self.cfg['devices']):
                                if p==q:action=('pulse',i)
            if not undone:
                nxt=advance(self.cfg,self.state,action)
                if nxt!=self.state:self.history.append(self.state);self.state=nxt
                else:self.rejected=True
        self._paint()
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    @staticmethod
    def rect(c,x,y,w,h,col):c[max(0,y):min(64,y+h),max(0,x):min(64,x+w)]=col

    def _paint(self):
        c=np.full((64,64),5,dtype=np.int64);pos,blocks,melt,crumble=self.state
        for p in range(25):
            x,y=9+(p%5)*9,12+(p//5)*9;tile=terrain(self.cfg,p,melt,crumble)
            if tile=='#':
                if crumble&(1<<p):c[y+1,x+1]=8;c[y+6,x+6]=8
                continue
            col=3 if tile not in ('I','W') else (10 if tile=='I' else 9)
            self.rect(c,x,y,8,8,col)
            if tile=='I':
                c[y+1:y+7,x+2]=0;c[y+2,x+2:x+7]=0
            elif tile=='W':
                if supported(self.cfg,p,blocks,melt,crumble):self.rect(c,x,y,8,8,10);c[y+6,x+1:x+7]=0
                else:c[y+2,x+1:x+4]=10;c[y+5,x+4:x+7]=10
            elif tile=='B':
                c[y,x:x+8]=13;c[y+7,x:x+8]=13;c[y+2,x+3]=2;c[y+3:y+5,x+4]=2
        # Device channels are physically laid into the floor; walls stop them.
        for source,delta,axis in self.cfg['devices']:
            for direction in (-1,1):
                q=source
                while True:
                    nx=q%5+(direction if axis=='row' else 0)
                    ny=q//5+(direction if axis=='col' else 0)
                    if not(0<=nx<5 and 0<=ny<5):break
                    q=ny*5+nx
                    if terrain(self.cfg,q,melt,crumble) in ('#','I'):break
                    xx,yy=9+nx*9,12+ny*9
                    channel=12 if delta>0 else 10
                    if axis=='row':c[yy+4,xx:xx+8]=channel
                    else:c[yy:yy+8,xx+4]=channel
        for p,t in self.cfg['goals']:
            x,y=9+(p%5)*9,12+(p//5)*9;col=COLORS[t]
            c[y,x:x+8]=col;c[y+7,x:x+8]=col;c[y:y+8,x]=col;c[y:y+8,x+7]=col
            # Socket bears the same temperature marks as its intended block.
            if t==0:c[y+3:y+5,x+3:x+5]=col
            else:
                for j in range(abs(t)):c[y+2+j*2,x+2:x+6]=col
        for i,(p,delta,axis) in enumerate(self.cfg['devices']):
            x,y=9+(p%5)*9,12+(p//5)*9
            self.rect(c,x+1,y+1,6,6,8 if delta>0 else 9)
            if axis=='row':c[y+3,x+1:x+7]=0
            else:c[y+1:y+7,x+3]=0
            if delta>0:c[y+2:y+5,x+4]=0;c[y+3,x+3:x+6]=0
            # Reachable controls have a raised white rim; distant controls stay recessed.
            rim=0 if pos==p or adjacent(pos,p) else 2
            c[y,x:x+8]=rim;c[y+7,x:x+8]=rim
            c[y:y+8,x]=rim;c[y:y+8,x+7]=rim
        for p,t in blocks:
            x,y=9+(p%5)*9,12+(p//5)*9
            self.rect(c,x+1,y+1,6,6,COLORS[t])
            if t==0:c[y+3:y+5,x+3:x+5]=5
            else:
                for j in range(abs(t)):c[y+2+j*2,x+2:x+6]=0
        if self.history and self.history[-1][0]!=pos and all(self.history[-1][0]!=q for q,d,a in self.cfg['devices']):
            old=self.history[-1][0];gx,gy=9+(old%5)*9,12+(old//5)*9
            c[gy+1,gx+1:gx+7]=1;c[gy+6,gx+1:gx+7]=1
            c[gy+1:gy+7,gx+1]=1;c[gy+1:gy+7,gx+6]=1
        x,y=9+(pos%5)*9,12+(pos//5)*9
        self.rect(c,x+2,y+1,4,6,0);self.rect(c,x+1,y+2,6,4,0);c[y+2,x+4]=5
        if self.rejected:c[y+7,x+1:x+7]=8
        self.current_level.remove_all_sprites();self.current_level.add_sprite(Sprite(pixels=c,name='plain-thermal',x=0,y=0,layer=0))
