FIXED_LEVELS = [{'nodes': [[12, 34], [50, 34]], 'edges': [[0, 1, 1, 0]], 'switches': [], 'batteries': [0], 'start': 0, 'flags': 0, 'lamps': [1], 'target_on': 1, 'exit': 1}, {'nodes': [[9, 20], [32, 20], [55, 20], [32, 51]], 'edges': [[0, 1, 0, 0], [1, 2, 1, 0], [1, 3, 1, 0]], 'switches': [[1, [1, 2]]], 'batteries': [0], 'start': 0, 'flags': 0, 'lamps': [3], 'target_on': 1, 'exit': 3}, {'nodes': [[8, 25], [30, 25], [54, 25], [30, 50]], 'edges': [[0, 1, 0, 0], [1, 2, 1, 0], [1, 3, 0, 0], [3, 2, 0, 1]], 'switches': [[1, [0, 1]]], 'batteries': [0], 'start': 0, 'flags': 0, 'lamps': [2, 3], 'target_on': 3, 'exit': 2}, {'nodes': [[8, 17], [30, 17], [54, 17], [8, 36], [30, 36], [54, 36], [8, 55], [30, 55], [54, 55]], 'edges': [[0, 1, 0, 0], [1, 2, 1, 0], [0, 3, 0, 1], [3, 4, 0, 0], [1, 4, 0, 0], [4, 5, 1, 0], [2, 5, 0, 1], [3, 6, 1, 0], [6, 7, 0, 0], [4, 7, 0, 0], [7, 8, 1, 0], [5, 8, 0, 0]], 'switches': [[1, [0, 1]], [4, [3, 5]], [7, [8, 10]]], 'batteries': [0], 'start': 3, 'flags': 3, 'lamps': [2, 5, 6, 8], 'target_on': 4, 'exit': 6}, {'nodes': [[8, 17], [30, 17], [54, 17], [8, 36], [30, 36], [54, 36], [8, 55], [30, 55], [54, 55]], 'edges': [[0, 1, 0, 0], [1, 2, 1, 0], [0, 3, 0, 1], [3, 4, 0, 0], [1, 4, 0, 0], [4, 5, 1, 0], [2, 5, 0, 1], [3, 6, 1, 0], [6, 7, 0, 0], [4, 7, 0, 0], [7, 8, 1, 0], [5, 8, 0, 0]], 'switches': [[1, [0, 1]], [4, [3, 5]], [7, [8, 10]], [3, [2, 7]]], 'batteries': [0], 'start': 3, 'flags': 2, 'lamps': [2, 4, 6, 8], 'target_on': 11, 'exit': 2}, {'nodes': [[8, 17], [30, 17], [54, 17], [8, 36], [30, 36], [54, 36], [8, 55], [30, 55], [54, 55]], 'edges': [[0, 1, 0, 0], [1, 2, 1, 0], [0, 3, 0, 1], [3, 4, 0, 0], [1, 4, 0, 0], [4, 5, 1, 0], [2, 5, 0, 1], [3, 6, 1, 0], [6, 7, 0, 0], [4, 7, 0, 0], [7, 8, 1, 0], [5, 8, 0, 0]], 'switches': [[1, [0, 1]], [4, [3, 5]], [7, [8, 10]], [3, [2, 7]], [5, [6, 11]]], 'batteries': [0], 'start': 0, 'flags': 0, 'lamps': [2, 3, 6, 8], 'target_on': 8, 'exit': 8}, {'nodes': [[8, 17], [30, 17], [54, 17], [8, 36], [30, 36], [54, 36], [8, 55], [30, 55], [54, 55]], 'edges': [[0, 1, 0, 0], [1, 2, 1, 0], [0, 3, 0, 1], [3, 4, 0, 0], [1, 4, 0, 0], [4, 5, 1, 0], [2, 5, 0, 1], [3, 6, 1, 0], [6, 7, 0, 0], [4, 7, 0, 0], [7, 8, 1, 0], [5, 8, 0, 0]], 'switches': [[1, [0, 1]], [4, [3, 5]], [7, [8, 10]], [3, [2, 7]], [5, [6, 11]]], 'batteries': [0, 8], 'start': 0, 'flags': 0, 'lamps': [1, 2, 3, 5, 6, 7], 'target_on': 41, 'exit': 6}]

import numpy as np
from arcengine import ARCBaseGame,Camera,Level,Sprite,GameAction

def active(cfg,flags,index):
    for i,switch in enumerate(cfg['switches']):
        choices=switch[1]
        if index in choices and index!=choices[(flags>>i)&1]:return False
    return True

def component(cfg,flags,start):
    seen={start};todo=[start]
    while todo:
        n=todo.pop()
        for i,(a,b,gate,wire) in enumerate(cfg['edges']):
            if not active(cfg,flags,i) or n not in (a,b):continue
            other=b if n==a else a
            if other not in seen:seen.add(other);todo.append(other)
    return seen

def advance(cfg,state,action):
    pos,flags,power=state;kind,target=action
    if kind=='pulse':
        connected=component(cfg,flags,pos)
        if not any(b in connected for b in cfg['batteries']):return state
        return (pos,flags,sum(1<<n for n in connected))
    if kind=='flip':
        for i,(node,choices) in enumerate(cfg['switches']):
            if pos==node:return (pos,flags^(1<<i),power)
        return state
    if kind=='move':
        for i,(a,b,gate,wire) in enumerate(cfg['edges']):
            if wire or not active(cfg,flags,i) or {pos,target}!={a,b}:continue
            if gate and not (power&(1<<a) and power&(1<<b)):return state
            return (target,flags,power)
    return state

def lights(cfg,power):
    return sum((1<<i) for i,n in enumerate(cfg['lamps']) if power&(1<<n))

def solved(cfg,state):return state[0]==cfg['exit'] and lights(cfg,state[2])==cfg['target_on']

class Sg10(ARCBaseGame):
    def __init__(self,seed=0):
        self.cfg=None;self.state=None;self.history=[];self.rejected=False
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='rail')],grid_size=(64,64),data={'layout':c},name='Yard %d'%(i+1)) for i,c in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg10-v1',levels=levels,camera=Camera(background=5,letter_box=5),available_actions=[1,2,3,4,5,6,7],seed=seed)

    def on_set_level(self,level):
        self.cfg=level.get_data('layout');self.state=(self.cfg['start'],self.cfg['flags'],0);self.history=[];self.rejected=False;self._paint()

    def step(self):
        n=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1]);self.rejected=False
        if n==7:
            if self.history:self.state=self.history.pop()
        elif n:
            action=('none',-1);pos=self.state[0];px,py=self.cfg['nodes'][pos]
            if n==5:action=('pulse',-1)
            elif n==6:
                data=self.action.data or {};x,y=data.get('x',-99),data.get('y',-99)
                if type(x) is int and type(y) is int:
                    if 1<=x<=14 and 1<=y<=9:action=('pulse',-1)
                    for i,(u,v) in enumerate(self.cfg['nodes']):
                        if abs(x-u)<=5 and abs(y-v)<=5:
                            action=('pulse',-1) if i==pos and i in self.cfg['batteries'] else (('flip',-1) if i==pos else ('move',i))
            elif n in (1,2,3,4):
                dx,dy={1:(0,-1),2:(0,1),3:(-1,0),4:(1,0)}[n];choices=[]
                for a,b,gate,wire in self.cfg['edges']:
                    if wire or pos not in (a,b):continue
                    other=b if pos==a else a;u,v=self.cfg['nodes'][other]
                    if (dx and (u-px)*dx>0 and v==py) or (dy and (v-py)*dy>0 and u==px):choices.append((abs(u-px)+abs(v-py),other))
                if choices:action=('move',min(choices)[1])
            nxt=advance(self.cfg,self.state,action)
            if nxt!=self.state:self.history.append(self.state);self.state=nxt
            else:self.rejected=True
        self._paint()
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    @staticmethod
    def rect(c,x,y,w,h,col):c[max(0,y):min(64,y+h),max(0,x):min(64,x+w)]=col

    def line(self,c,a,b,col,rail=False):
        x,y=a;u,v=b
        # Orthogonal elbow for electrical jumpers; rail endpoints are collinear.
        points=[(px,y) for px in range(min(x,u),max(x,u)+1)]+[(u,py) for py in range(min(y,v),max(y,v)+1)]
        for j,(px,py) in enumerate(points):
            c[py,px]=col
            if rail:
                if y==v:
                    c[py-1,px]=2;c[py+1,px]=2
                    if j%4==0:c[py-2:py+3,px]=3
                else:
                    c[py,px-1]=2;c[py,px+1]=2
                    if j%4==0:c[py,px-2:px+3]=3


    def _paint(self):
        c = np.full((64,64),5,dtype=np.int64)
        pos,flags,power = self.state
        connected = component(self.cfg,flags,pos)
        can_pulse = any(b in connected for b in self.cfg['batteries'])
        prospective = connected if can_pulse else set()

        # The only HUD control is a large clickable pulse button. Its lightning
        # icon repeats at batteries; a red foot means no connected supply.
        self.rect(c,1,1,14,9,3)
        self.rect(c,2,2,12,7,2)
        self.rect(c,4,3,8,5,11 if can_pulse else 4)
        c[4,7:10]=0;c[5,6:9]=0;c[6,8]=0
        if not can_pulse:c[8,3:13]=8

        def route(a,b):
            x,y=a;u,v=b
            if x==u:return [(x,py) for py in range(min(y,v),max(y,v)+1)]
            if y==v:return [(px,y) for px in range(min(x,u),max(x,u)+1)]
            return ([(px,y) for px in range(min(x,u),max(x,u)+1)]
                    +[(u,py) for py in range(min(y,v),max(y,v)+1)])

        # Off branches are ghosted and physically broken at their centre.
        for i,(a,b,gate,wire) in enumerate(self.cfg['edges']):
            if active(self.cfg,flags,i):continue
            pts=route(self.cfg['nodes'][a],self.cfg['nodes'][b])
            middle=len(pts)//2
            for j,(x,y) in enumerate(pts):
                if j%3==0 and abs(j-middle)>3:c[y,x]=4

        # Electrical jumpers are blue dotted lines; they carry a pulse but
        # cannot be travelled. A live rail is continuous, white or amber.
        for i,(a,b,gate,wire) in enumerate(self.cfg['edges']):
            if not active(self.cfg,flags,i):continue
            pts=route(self.cfg['nodes'][a],self.cfg['nodes'][b])
            charged=bool(power&(1<<a) and power&(1<<b))
            if wire:
                for j,(x,y) in enumerate(pts):
                    if j%2==0:c[y,x]=9
            else:
                for x,y in pts:
                    self.rect(c,x-1,y-1,3,3,3)
                    c[y,x]=11 if charged else 2

        # A closed gate interrupts even a visible rail; charging both endpoint
        # capacitors changes the red stop bar to a green open aperture.
        for i,(a,b,gate,wire) in enumerate(self.cfg['edges']):
            if not gate or not active(self.cfg,flags,i):continue
            pts=route(self.cfg['nodes'][a],self.cfg['nodes'][b])
            x,y=pts[len(pts)//2]
            charged=bool(power&(1<<a) and power&(1<<b))
            if charged:
                self.rect(c,x-2,y-2,5,5,14)
                c[y,x]=11
            else:
                self.rect(c,x-2,y-2,5,5,8)
                self.rect(c,x-1,y-1,3,3,5)

        # The small tile above each bulb is a fixed target exemplar, while the
        # bulb at its node shows the present state. The two never swap roles.
        for i,(x,y) in enumerate(self.cfg['nodes']):
            is_charged=bool(power&(1<<i))
            self.rect(c,x-3,y-3,7,7,2)
            self.rect(c,x-2,y-2,5,5,11 if is_charged else 4)
            if i in prospective:
                c[y-3,x-3]=10;c[y+3,x+3]=10
            if i in self.cfg['batteries']:
                self.rect(c,x-3,y-4,7,2,12)
                c[y-4,x]=0;c[y-5,x]=11
                c[y,x]=0;c[y-1,x]=0;c[y,x-1:x+2]=0
            if i in self.cfg['lamps']:
                index=self.cfg['lamps'].index(i)
                wanted=bool(self.cfg['target_on']&(1<<index))
                self.rect(c,x-3,y-10,7,4,2)
                self.rect(c,x-2,y-9,5,2,11 if wanted else 5)
                c[y,x]=11 if is_charged else 5
                c[y-1,x-1:x+2]=11 if is_charged else 4
            if i==self.cfg['exit']:
                c[y+5,x-4:x+5]=0;c[y+4,x-4]=0;c[y+4,x+4]=0

        # A short pointer leaves each switch toward the branch actually in
        # circuit. The cart is a separate orange outline, not a charge symbol.
        for j,(node,choices) in enumerate(self.cfg['switches']):
            x,y=self.cfg['nodes'][node]
            a,b,_,_=self.cfg['edges'][choices[(flags>>j)&1]]
            other=b if a==node else a
            u,v=self.cfg['nodes'][other]
            dx=0 if u==x else (1 if u>x else -1)
            dy=0 if v==y else (1 if v>y else -1)
            for k in range(4,7):
                px,py=x+dx*k,y+dy*k
                if 0<=px<64 and 0<=py<64:c[py,px]=0
            c[y,x]=0

        x,y=self.cfg['nodes'][pos]
        c[y-5,x-5:x-2]=12;c[y-5,x+3:x+6]=12
        c[y+5,x-5:x-2]=12;c[y+5,x+3:x+6]=12
        c[y-4:y-1,x-5]=12;c[y-4:y-1,x+5]=12
        c[y+2:y+5,x-5]=12;c[y+2:y+5,x+5]=12
        if self.rejected:c[y-5,x-2:x+3]=8
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=c,name='capacitor-yard',x=0,y=0,layer=0))
