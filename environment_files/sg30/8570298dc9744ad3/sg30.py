FIXED_LEVELS = [{'top': {'fixed': [1, 1], 'sliders': [[1, -1]]}, 'lower': None}, {'top': {'fixed': [2, 3], 'sliders': [[3, 0]]}, 'lower': None}, {'top': {'fixed': [1, 1], 'sliders': [[1, 1], [2, 2]]}, 'lower': None}, {'top': {'fixed': [2, 1], 'sliders': [[1, -2], [2, -1]]}, 'lower': None}, {'top': {'fixed': [2, 1], 'sliders': [[1, 0]]}, 'lower': {'fixed': [1, 1], 'sliders': [[2, 2]]}}, {'top': {'fixed': [3, 1], 'sliders': [[1, 0], [2, 2]]}, 'lower': {'fixed': [1, 2], 'sliders': [[3, 0]]}}, {'top': {'fixed': [3, 1], 'sliders': [[1, 0], [2, 2]]}, 'lower': {'fixed': [2, 1], 'sliders': [[1, 0], [2, -2]]}}]


import numpy as np
from arcengine import ARCBaseGame,Camera,Level,Sprite,GameAction

HOOKS=(-2,-1,0,1,2)

def pieces(cfg):
    return list(cfg['top']['sliders'])+(list(cfg['lower']['sliders']) if cfg['lower'] else [])

def beam_of(cfg,index):
    return 0 if index<len(cfg['top']['sliders']) else 1

def initial(cfg):
    return (tuple(p for m,p in pieces(cfg)),0)

def child_mass(cfg):
    if cfg['lower'] is None:return 0
    lower=cfg['lower']
    return 1+sum(lower['fixed'])+sum(m for m,p in lower['sliders'])

def torque(cfg,state,beam):
    info=cfg['top'] if beam==0 else cfg['lower']
    if info is None:return 0
    left,right=info['fixed']
    total=3*(right-left)
    if beam==0:total+=child_mass(cfg)
    for i,(mass,start) in enumerate(pieces(cfg)):
        if beam_of(cfg,i)==beam:total+=mass*state[0][i]
    return total

def solved(cfg,state):
    return torque(cfg,state,0)==0 and (cfg['lower'] is None or torque(cfg,state,1)==0)

def advance(cfg,state,command):
    positions,selected=state
    kind,a,b=command
    if kind=='select':
        if 0<=a<len(positions):return (positions,a)
        return state
    if kind=='place':
        beam,target=a,b
        allowed=HOOKS if beam==1 or cfg['lower'] is None else (-2,-1,0,2)
        if beam_of(cfg,selected)!=beam or target not in allowed:return state
        if any(i!=selected and beam_of(cfg,i)==beam and position==target for i,position in enumerate(positions)):return state
        moved=list(positions);moved[selected]=target
        return (tuple(moved),selected)
    return state

class Sg30(ARCBaseGame):
    def __init__(self,seed=0):
        self.cfg=None;self.state=None;self.history=[];self.rejected=False
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='mobile')],
                      grid_size=(64,64),data={'layout':cfg},name='Mobile %d'%(i+1))
                for i,cfg in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg30-v1',levels=levels,camera=Camera(background=5,letter_box=5),
                         available_actions=[6,7],seed=seed)

    def on_set_level(self,level):
        self.cfg=level.get_data('layout')
        self.state=initial(self.cfg)
        self.history=[];self.rejected=False
        self._paint()

    def _geometry(self,beam):
        return (32,16,8) if beam==0 else (40,39,6)

    def _height(self,beam,x):
        cx,cy,unit=self._geometry(beam)
        moment=torque(self.cfg,self.state,beam)
        slope=0 if moment==0 else (3 if moment>0 else -3)
        return cy+int(round(slope*(x-cx)/(3*unit)))

    def _decode_click(self,x,y):
        items=pieces(self.cfg)
        for i,(mass,start) in enumerate(items):
            beam=beam_of(self.cfg,i);cx,cy,unit=self._geometry(beam)
            bx=cx+unit*self.state[0][i];by=self._height(beam,bx)+10
            if abs(x-bx)<=4 and abs(y-by)<=4:return ('select',i,0)
        for beam in range(2 if self.cfg['lower'] else 1):
            cx,cy,unit=self._geometry(beam)
            if abs(y-(cy-3))>5 and abs(y-(cy+5))>2:continue
            allowed=HOOKS if beam==1 or self.cfg['lower'] is None else (-2,-1,0,2)
            for target in allowed:
                if target==0:
                    # The support carries a visible U-shaped hook below the pivot.
                    # Click inside that ring, not the gray pivot above the beam.
                    if abs(x-cx)<=3 and abs(y-(cy+5))<=2:return ('place',beam,target)
                elif abs(x-(cx+unit*target))<=3:return ('place',beam,target)
        return ('none',-1,-1)

    def step(self):
        n=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1])
        self.rejected=False
        if n==7:
            if self.history:self.state=self.history.pop()
        elif n==6:
            data=self.action.data or {}
            x,y=data.get('x',-99),data.get('y',-99)
            command=self._decode_click(x,y) if type(x) is int and type(y) is int else ('none',-1,-1)
            next_state=advance(self.cfg,self.state,command)
            if next_state!=self.state:
                self.history.append(self.state);self.state=next_state
            elif command[0]=='select' and command[1]==self.state[1]:
                pass
            elif command[0]=='place' and command[1]==beam_of(self.cfg,self.state[1]) and command[2]==self.state[0][self.state[1]]:
                pass
            else:self.rejected=True
        self._paint()
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    @staticmethod
    def rect(c,x,y,w,h,col):
        c[max(0,y):min(64,y+h),max(0,x):min(64,x+w)]=col

    def _bob(self,c,x,y,mass,color,selected=False):
        size=3+2*mass
        self.rect(c,x-size//2,y-size//2,size,size,color)
        c[y,x]=0
        if selected:
            radius=size//2+2
            for dx in (-radius,radius):
                for dy in (-radius,radius):
                    px,py=x+dx,y+dy
                    if 0<=px<64 and 0<=py<64:c[py,px]=0
                    if 0<=px-1<64 and 0<=py<64:c[py,px-1]=2

    def _paint(self):
        c=np.full((64,64),5,dtype=np.int64)
        self.rect(c,30,2,5,2,2)
        self.rect(c,32,4,1,12,2)
        if self.cfg['lower']:
            attach=40;upper_y=self._height(0,attach)
            self.rect(c,attach,upper_y+2,1,37-upper_y,2)
        for beam in range(2 if self.cfg['lower'] else 1):
            cx,cy,unit=self._geometry(beam)
            lo,hi=cx-3*unit,cx+3*unit
            for x in range(lo,hi+1,4):c[cy,x]=3
            moment=torque(self.cfg,self.state,beam)
            beam_color=11 if moment==0 else 12
            for x in range(lo,hi+1):
                y=self._height(beam,x)
                c[y,x]=beam_color
                if y+1<64:c[y+1,x]=3
            self.rect(c,cx-2,cy-3,5,5,2)
            c[cy,cx]=5
            allowed=HOOKS if beam==1 or self.cfg['lower'] is None else (-2,-1,0,2)
            for p in allowed:
                x=cx+unit*p;y=self._height(beam,x)
                if p==0:
                    # A white U hangs under the gray support: its dark opening
                    # is the exact click target, separated from any bob below.
                    self.rect(c,x-3,cy+3,7,5,5)
                    c[cy+3,x]=2
                    c[cy+4:cy+6,x-3]=2
                    c[cy+4:cy+6,x+3]=2
                    c[cy+6,x-2:x+3]=2
                else:
                    self.rect(c,x-1,y-4,3,2,2)
                    c[y-3,x]=0
            info=self.cfg['top'] if beam==0 else self.cfg['lower']
            for p,mass in ((-3,info['fixed'][0]),(3,info['fixed'][1])):
                x=cx+unit*p;y=self._height(beam,x)
                self.rect(c,x,y+2,1,6,2)
                self._bob(c,x,y+10,mass,12)
            for i,(mass,start) in enumerate(pieces(self.cfg)):
                if beam_of(self.cfg,i)!=beam:continue
                x=cx+unit*self.state[0][i];y=self._height(beam,x)
                self.rect(c,x,y+2,1,6,2)
                color=10 if i%2==0 else 6
                self._bob(c,x,y+10,mass,color,i==self.state[1])
        if self.rejected:
            i=self.state[1];beam=beam_of(self.cfg,i);cx,cy,unit=self._geometry(beam)
            x=cx+unit*self.state[0][i];y=self._height(beam,x)+4
            c[y,x-2:x+3]=8
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=c,name='mobile',x=0,y=0,layer=0))
