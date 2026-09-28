FIXED_LEVELS = [{'rooms': [[16, 34], [48, 34]], 'edges': [[0, 1, [0], []]], 'start': 0, 'coins': [1, 0, 0], 'seals': [], 'exit': 1, 'target': [0, 0, 0]}, {'rooms': [[10, 17], [54, 17], [10, 48], [54, 48]], 'edges': [[0, 1, [0], [1]], [0, 2, [0], [2]], [1, 3, [2], [0]], [2, 3, [2], [1]]], 'start': 0, 'coins': [1, 0, 0], 'seals': [1], 'exit': 3, 'target': [0, 1, 0]}, {'rooms': [[10, 17], [32, 17], [54, 17], [10, 48], [32, 48], [54, 48]], 'edges': [[0, 1, [0], [1]], [1, 2, [1], [2]], [0, 3, [0], [2]], [3, 4, [2], [1]], [4, 5, [1], [0]], [2, 5, [2], [0]], [1, 4, [0], [2]]], 'start': 0, 'coins': [1, 1, 0], 'seals': [3], 'exit': 5, 'target': [0, 1, 1]}, {'rooms': [[10, 17], [32, 17], [54, 17], [10, 34], [32, 34], [54, 34], [10, 48], [32, 48], [54, 48]], 'edges': [[0, 1, [0], [1]], [1, 2, [1], [2]], [0, 3, [0], [2]], [3, 4, [2], [1]], [4, 5, [1], [0]], [2, 5, [2], [0]], [3, 6, [2], [0]], [6, 7, [0], [1]], [7, 8, [1], [2]], [5, 8, [0], [2]]], 'start': 0, 'coins': [1, 0, 0], 'seals': [2, 4, 6], 'exit': 8, 'target': [0, 0, 1]}, {'rooms': [[10, 17], [32, 17], [54, 17], [10, 34], [32, 34], [54, 34], [10, 48], [32, 48], [54, 48]], 'edges': [[0, 1, [0], [1, 1]], [1, 2, [1, 1], [2]], [0, 3, [0], [2]], [3, 4, [2], [1]], [4, 5, [1], [0]], [2, 5, [2], [0]], [3, 6, [2], [0]], [6, 7, [0], [1, 1]], [7, 8, [1], [2]], [5, 8, [0], [2]], [1, 4, [1], [2]]], 'start': 0, 'coins': [1, 0, 0], 'seals': [2, 6], 'exit': 8, 'target': [0, 0, 2]}, {'rooms': [[10, 17], [32, 17], [54, 17], [10, 34], [32, 34], [54, 34], [10, 48], [32, 48], [54, 48]], 'edges': [[0, 1, [0], [1, 1]], [1, 2, [1], [2]], [0, 3, [0], [2]], [3, 4, [2], [0, 1]], [4, 5, [0], [2]], [2, 5, [2], [0]], [3, 6, [2], [0]], [6, 7, [0], [1, 1]], [7, 8, [1, 2], [0]], [5, 8, [0], [1]], [1, 4, [1], [2]], [4, 7, [1], [2]]], 'start': 0, 'coins': [1, 1, 0], 'seals': [2, 6], 'exit': 8, 'target': [2, 0, 0]}, {'rooms': [[10, 17], [32, 17], [54, 17], [10, 34], [32, 34], [54, 34], [10, 48], [32, 48], [54, 48]], 'edges': [[0, 1, [0], [1, 1]], [1, 2, [1], [2]], [0, 3, [0], [2]], [3, 4, [2], [0, 1]], [4, 5, [0, 1], [2, 2]], [3, 6, [2], [0]], [6, 7, [0], [1, 1]], [7, 8, [1, 2], [0]], [1, 4, [1], [2]], [4, 7, [1], [2]]], 'start': 0, 'coins': [1, 1, 0], 'seals': [2, 6, 8], 'exit': 5, 'target': [0, 1, 2]}]

import numpy as np
from arcengine import ARCBaseGame, Camera, Level, Sprite, GameAction

COLORS = (12, 10, 6)


def initial(cfg):
    return (cfg['start'], tuple(cfg['coins']), 0, 0)


def cross(cfg, state, destination):
    pos, coins, flipped, seals = state
    for i, edge in enumerate(cfg['edges']):
        a, b, left, right = edge
        if {pos, destination} != {a, b}:
            continue
        cost, refund = (right, left) if flipped & (1 << i) else (left, right)
        pocket = list(coins)
        for color in cost:
            if pocket[color] == 0:
                return state
            pocket[color] -= 1
        for color in refund:
            pocket[color] += 1
        if destination in cfg['seals']:
            seals |= 1 << cfg['seals'].index(destination)
        return (destination, tuple(pocket), flipped ^ (1 << i), seals)
    return state


def solved(cfg, state):
    return (state[0] == cfg['exit'] and list(state[1]) == cfg['target']
            and state[3] == (1 << len(cfg['seals'])) - 1)


class Sg08(ARCBaseGame):
    def __init__(self, seed=0):
        self.cfg = None
        self.state = None
        self.history = []
        self.rejected = False
        levels = [Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='mint')],
                        grid_size=(64,64),data={'layout': c},name='Vault %d'%(i+1))
                  for i,c in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg08-v1',levels=levels,camera=Camera(background=5,letter_box=5),
                         available_actions=[1,2,3,4,6,7],seed=seed)

    def on_set_level(self, level):
        self.cfg = level.get_data('layout')
        self.state = initial(self.cfg)
        self.history = []
        self.rejected = False
        self._paint()

    def step(self):
        number = 0 if self.action.id == GameAction.RESET else int(self.action.id.name[-1])
        self.rejected = False
        if number == 7:
            if self.history:
                self.state = self.history.pop()
        elif number:
            destination = None
            px,py = self.cfg['rooms'][self.state[0]]
            if number == 6:
                data = self.action.data or {}
                x,y = data.get('x',-99),data.get('y',-99)
                if type(x) is int and type(y) is int:
                    for i,(cx,cy) in enumerate(self.cfg['rooms']):
                        if abs(x-cx)<=6 and abs(y-cy)<=6:
                            destination=i
            elif number in (1,2,3,4):
                dx,dy = {1:(0,-1),2:(0,1),3:(-1,0),4:(1,0)}[number]
                choices=[]
                for a,b,_,_ in self.cfg['edges']:
                    if self.state[0] not in (a,b): continue
                    other=b if a==self.state[0] else a
                    x,y=self.cfg['rooms'][other]
                    if (dx and y==py and (x-px)*dx>0) or (dy and x==px and (y-py)*dy>0):
                        choices.append((abs(x-px)+abs(y-py),other))
                if choices: destination=min(choices)[1]
            if destination is not None:
                nxt=cross(self.cfg,self.state,destination)
                if nxt!=self.state:
                    self.history.append(self.state)
                    self.state=nxt
                else: self.rejected=True
        self._paint()
        if solved(self.cfg,self.state): self.next_level()
        self.complete_action()

    @staticmethod
    def rect(c,x,y,w,h,color):
        c[max(0,y):min(64,y+h),max(0,x):min(64,x+w)] = color

    def coin(self,c,x,y,color,small=False):
        if small:
            self.rect(c,x,y,2,2,COLORS[color]); return
        self.rect(c,x+1,y,3,5,COLORS[color])
        self.rect(c,x,y+1,5,3,COLORS[color])
        c[y+2,x+2]=5

    def _paint(self):
        c=np.full((64,64),5,dtype=np.int64)
        pos,coins,flipped,seals=self.state
        # A physical purse above the chambers; exact exit cargo below it.
        self.rect(c,1,0,62,8,4)
        # Raised handle and the courier's white material identify carried cargo.
        c[0,2:9]=0;c[1:7,1]=0;c[7,1:63]=0;c[1:7,62]=0
        x=3
        for color,count in enumerate(coins):
            for j in range(count):
                if x<=57:self.coin(c,x,1,color)
                x+=6
        for a,b,_,_ in self.cfg['edges']:
            x,y=self.cfg['rooms'][a];u,v=self.cfg['rooms'][b]
            self.rect(c,min(x,u),min(y,v),abs(u-x)+1,abs(v-y)+1,2)
            if y==v:self.rect(c,min(x,u),y-1,abs(u-x)+1,3,3)
            else:self.rect(c,x-1,min(y,v),3,abs(v-y)+1,3)
        for i,(x,y) in enumerate(self.cfg['rooms']):
            radius=10 if len(self.cfg['rooms'])==2 else 6
            self.rect(c,x-radius,y-radius,radius*2+1,radius*2+1,3)
            self.rect(c,x-radius+1,y-radius+1,radius*2-1,radius*2-1,4)
            self.rect(c,x-3,y-radius+2,7,1,2)
            if i==self.cfg['exit']:
                self.rect(c,x-radius+1,y-radius+1,radius*2-1,radius*2-1,1)
                self.rect(c,x-radius+2,y-radius+2,radius*2-3,radius*2-3,5)
                c[y-radius+1,x]=14;c[y-radius+2,x]=14
            if i in self.cfg['seals']:
                taken=bool(seals & (1<<self.cfg['seals'].index(i)))
                color=3 if taken else 11
                self.rect(c,x-2,y-2,5,5,color);c[y,x]=5
            if i==pos:
                # Substantial courier carrying a handle, not a one-pixel marker.
                self.rect(c,x-2,y-2,5,5,0)
                self.rect(c,x-1,y-3,3,1,0)
                c[y-1,x+1]=5;c[y+2,x]=2
                if self.rejected:c[y+4,x-2:x+3]=8
        for i,(a,b,left,right) in enumerate(self.cfg['edges']):
            x,y=self.cfg['rooms'][a];u,v=self.cfg['rooms'][b]
            mx,my=(x+u)//2,(y+v)//2
            cost,refund=(right,left) if flipped&(1<<i) else (left,right)
            # Upper bank is the required deposit; lower bank is the payout.
            self.rect(c,mx-4,my-4,9,9,2)
            self.rect(c,mx-3,my-3,7,3,5)
            self.rect(c,mx-3,my+1,7,3,5)
            for j,color in enumerate(cost):self.coin(c,mx-3+j*3,my-3,color,True)
            for j,color in enumerate(refund):self.coin(c,mx-3+j*3,my+1,color,True)
            # Deposit physically feeds the lower payout: a downward chute.
            c[my-2:my+1,mx+3]=0;c[my+1,mx+2:mx+5]=0;c[my+2,mx+3]=0
            if not cost and not refund:c[my-2:my+3,mx]=3
        # Exit requirement sheet is tethered to the exit chamber at the right rim.
        ex,ey=self.cfg['rooms'][self.cfg['exit']]
        c[ey,ex+7:64]=1;c[ey:57,63]=1
        self.rect(c,1,56,62,8,1)
        self.rect(c,2,57,60,6,4)
        x=3
        for color,count in enumerate(self.cfg['target']):
            for j in range(count):
                self.coin(c,x,57,color);x+=6
        if not any(self.cfg['target']):
            # Empty cargo is visibly an empty receptacle, not a mysterious dash.
            c[58:62,3]=1;c[58:62,10]=1;c[61,3:11]=1
        for i in range(len(self.cfg['seals'])):
            sx=32+i*6
            self.rect(c,sx,58,5,5,11 if seals&(1<<i) else 2);c[60,sx+2]=5
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=c,name='toll-vault',x=0,y=0,layer=0))
