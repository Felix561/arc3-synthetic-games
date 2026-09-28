FIXED_LEVELS = [{'capacities': [3, 3, 3], 'start': [2, 0, 0], 'goal': [0, 1, 1]}, {'capacities': [4, 3, 3], 'start': [4, 0, 0], 'goal': [2, 0, 2]}, {'capacities': [3, 2, 3, 3], 'start': [1, 1, 0, 3], 'goal': [1, 0, 2, 2]}, {'capacities': [3, 4, 2, 4], 'start': [0, 2, 2, 4], 'goal': [2, 4, 2, 0]}, {'capacities': [4, 4, 4, 4, 5], 'start': [0, 3, 2, 3, 5], 'goal': [4, 3, 3, 0, 3]}, {'capacities': [4, 5, 5, 4, 2, 1], 'start': [0, 5, 4, 3, 1, 0], 'goal': [3, 4, 2, 3, 0, 1]}, {'capacities': [1, 5, 5, 2, 1, 1], 'start': [1, 3, 0, 1, 1, 1], 'goal': [0, 0, 5, 2, 0, 0]}]

def initial(cfg):return tuple(cfg['start'])

def solved(cfg,state):return state==tuple(cfg['goal'])

def sow(cfg,state,index,unbounded=False):
    if type(index) is not int or not 0<=index<len(state) or state[index]==0:return state,()
    out=list(state);amount=out[index];out[index]=0;cursor=index;skipped=[]
    for _ in range(amount):
        cursor=(cursor+1)%len(out)
        while not unbounded and out[cursor]>=cfg['capacities'][cursor]:
            skipped.append(cursor);cursor=(cursor+1)%len(out)
        out[cursor]+=1
    return tuple(out),tuple(skipped)

def advance(cfg,state,index):return sow(cfg,state,index)[0]

def centers(cfg):
    return {3:((14,18),(50,18),(32,46)),4:((16,16),(48,16),(48,46),(16,46)),5:((32,13),(51,27),(44,49),(20,49),(13,27)),6:((12,17),(32,17),(52,17),(52,45),(32,45),(12,45))}[len(cfg['start'])]

import numpy as np
from arcengine import ARCBaseGame,Camera,Level,Sprite,GameAction

class Sg19(ARCBaseGame):
    def __init__(self,seed=0):
        self.cfg=None;self.state=None;self.history=[];self.selected=None;self.skipped=()
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='sowing')],grid_size=(64,64),data={'layout':c},name='Sowing %d'%(i+1)) for i,c in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg19-v1',levels=levels,camera=Camera(background=5,letter_box=5),available_actions=[6,7],seed=seed)

    def on_set_level(self,level):
        self.cfg=level.get_data('layout');self.state=initial(self.cfg);self.history=[];self.selected=None;self.skipped=();self._paint()

    def step(self):
        a=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1]);self.selected=None;self.skipped=()
        if a==7 and self.history:self.state=self.history.pop()
        elif a==6:
            d=self.action.data or {};x,y=d.get('x',-99),d.get('y',-99)
            if type(x) is int and type(y) is int:
                for i,(cx,cy) in enumerate(centers(self.cfg)):
                    if cx-6<=x<=cx+6 and cy-10<=y<=cy+10:
                        self.selected=i;n,self.skipped=sow(self.cfg,self.state,i)
                        if n!=self.state:self.history.append(self.state);self.state=n
                        break
        self._paint()
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    def _paint(self):
        c=np.full((64,64),5,dtype=np.int64);points=centers(self.cfg)
        for i,(x,y) in enumerate(points):
            tx,ty=points[(i+1)%len(points)];distance=max(abs(tx-x),abs(ty-y))
            for k in range(distance+1):c[round(y+(ty-y)*k/distance),round(x+(tx-x)*k/distance)]=4
            mx,my=(x+tx)/2,(y+ty)/2;length=((tx-x)**2+(ty-y)**2)**0.5;dx,dy=(tx-x)/length,(ty-y)/length
            triangle=((mx+3*dx,my+3*dy),(mx-2*dx-2*dy,my-2*dy+2*dx),(mx-2*dx+2*dy,my-2*dy-2*dx))
            for py in range(int(my)-4,int(my)+5):
                for px in range(int(mx)-4,int(mx)+5):
                    signs=[]
                    for j,(ax,ay) in enumerate(triangle):
                        bx,by=triangle[(j+1)%3];signs.append((px-ax)*(by-ay)-(py-ay)*(bx-ax))
                    if all(v>=0 for v in signs) or all(v<=0 for v in signs):c[py,px]=1
        for i,(x,y) in enumerate(points):
            c[y-10:y+11,x-6:x+7]=5;col=0 if self.selected==i else 6 if i in self.skipped else 3
            c[y-10,x-6:x+7]=col;c[y+10,x-6:x+7]=col;c[y-10:y+11,x-6]=col;c[y-10:y+11,x+6]=col
            for k in range(self.cfg['capacities'][i]):
                sx=x-5+(k%2)*6;sy=y-8+(k//2)*6;target=11 if k<self.cfg['goal'][i] else 3
                c[sy:sy+5,sx:sx+5]=target;c[sy+1:sy+4,sx+1:sx+4]=12 if k<self.state[i] else 5
        self.current_level.remove_all_sprites();self.current_level.add_sprite(Sprite(pixels=c,name='capacity-ring',x=0,y=0,layer=0))
