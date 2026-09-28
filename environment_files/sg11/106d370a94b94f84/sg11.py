FIXED_LEVELS = [{'target': ['10'], 'phase': 0, 'knots': 0}, {'target': ['10', '01'], 'phase': 0, 'knots': 0}, {'target': ['11', '10'], 'phase': 1, 'knots': 2}, {'target': ['110', '001', '101'], 'phase': 0, 'knots': 0}, {'target': ['111', '010', '101'], 'phase': 0, 'knots': 2}, {'target': ['1101', '0110', '1010', '0101'], 'phase': 0, 'knots': 1}, {'target': ['1110', '1011', '0101', '1000'], 'phase': 1, 'knots': 2}]

import numpy as np
from arcengine import ARCBaseGame,Camera,Level,Sprite,GameAction

COLORS=(10,6,14,15)

def initial(cfg):
    n=len(cfg['target'])
    return (tuple([0]*n),0,cfg['phase'],cfg['knots'],-1,-1)

def advance(cfg,state,row):
    lengths,over,phase,knots,last,previous=state
    n=len(lengths);cols=len(cfg['target'][0])
    if row==-1:
        if knots==0 or last<0:return state
        return (lengths,over|(1<<last),previous,knots-1,-1,-1)
    if not (0<=row<n) or lengths[row]>=cols:return state
    col=lengths[row];idx=row*cols+col
    lengths=list(lengths);lengths[row]+=1
    if phase==0:over|=1<<idx
    return (tuple(lengths),over,1-phase,knots,idx,phase)

def target_mask(cfg):
    return sum(1<<(r*len(cfg['target'][0])+c) for r,row in enumerate(cfg['target']) for c,v in enumerate(row) if v=='1')

def solved(cfg,state):
    return all(n==len(cfg['target'][0]) for n in state[0]) and state[1]==target_mask(cfg)

def viable(cfg,state):
    lengths,over,phase,knots,last,previous=state;cols=len(cfg['target'][0]);target=target_mask(cfg)
    for r,used in enumerate(lengths):
        for c in range(used):
            idx=r*cols+c
            if bool(over&(1<<idx))!=bool(target&(1<<idx)):
                if idx!=last or not knots or not target&(1<<idx):return False
    return True

class Sg11(ARCBaseGame):
    def __init__(self,seed=0):
        self.cfg=None;self.state=None;self.history=[];self.rejected=False
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='weave')],grid_size=(64,64),data={'layout':c},name='Weave %d'%(i+1)) for i,c in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg11-v1',levels=levels,camera=Camera(background=5,letter_box=5),available_actions=[5,6,7],seed=seed)

    def on_set_level(self,level):
        self.cfg=level.get_data('layout');self.state=initial(self.cfg);self.history=[];self.rejected=False;self._paint()

    def centers(self):
        rows=len(self.cfg['target']);cols=len(self.cfg['target'][0])
        return ([22+i*32//max(1,cols-1) for i in range(cols)], [24+i*32//max(1,rows-1) for i in range(rows)])

    def step(self):
        n=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1]);self.rejected=False
        if n==7:
            if self.history:self.state=self.history.pop()
        elif n:
            row=-99
            if n==5:row=-1
            elif n==6:
                data=self.action.data or {};x,y=data.get('x',-99),data.get('y',-99)
                if type(x) is int and type(y) is int:
                    if 29<=x<=42 and 1<=y<=11:row=-1
                    # The last crossing itself is the visible knot affordance.
                    # This keeps the optional keyboard action without requiring
                    # a player to infer what a distant icon controls.
                    if self.state[4]>=0 and self.state[3]>0:
                        r,j=divmod(self.state[4],len(self.cfg['target'][0]))
                        cx,cy=self.centers()[0][j],self.centers()[1][r]
                        if abs(x-cx)<=4 and abs(y-cy)<=4:row=-1
                    for i,cy in enumerate(self.centers()[1]):
                        if 2<=x<=14 and abs(y-cy)<=4:row=i
            nxt=advance(self.cfg,self.state,row)
            if nxt!=self.state:self.history.append(self.state);self.state=nxt
            else:self.rejected=True
        self._paint()
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    @staticmethod
    def rect(c,x,y,w,h,col):c[max(0,y):min(64,y+h),max(0,x):min(64,x+w)]=col

    def _paint(self):
        c=np.full((64,64),5,dtype=np.int64)
        lengths,over,phase,knots,last,previous=self.state;xs,ys=self.centers();cols=len(xs)
        # The reference is the same geometry, rather than a separate bar code.
        c[1:22,42]=1;c[1:22,63]=1;c[1,42:64]=1;c[21,42:64]=1
        for r,row in enumerate(self.cfg['target']):
            for j,value in enumerate(row):
                xx,yy=44+j*5,3+r*5
                c[yy:yy+5,xx+2]=12
                c[yy+2,xx:xx+5]=COLORS[r]
                c[yy+2,xx+2]=COLORS[r] if value=='1' else 12
        for x in xs:
            self.rect(c,x-1,20,3,41,3)
            c[20:61,x]=2
        for r,y in enumerate(ys):
            color=COLORS[r];tip=xs[lengths[r]-1]+3 if lengths[r] else 15
            self.rect(c,12,y-2,max(0,tip-11),5,color)
            # Draw actual crossings as overlapping physical strips.
            for j in range(lengths[r]):
                x=xs[j];idx=r*cols+j
                self.rect(c,x-1,y-4,3,9,12)
                if over&(1<<idx):self.rect(c,x-4,y-2,9,5,color)
                else:
                    self.rect(c,x-4,y-2,9,5,color)
                    self.rect(c,x-1,y-4,3,9,12)
                    c[y-4:y+5,x]=11
            self.rect(c,2,y-4,11,9,color if lengths[r]<cols else 3)
            self.rect(c,4,y-2,5,5,5)
            if lengths[r]<cols:
                # The next crossing shows exactly which strip would pass on top.
                nx=xs[lengths[r]]
                c[y-5,nx-5:nx+6]=3;c[y+5,nx-5:nx+6]=3
                c[y-5:y+6,nx-5]=3;c[y-5:y+6,nx+5]=3
                self.rect(c,nx-1,y-3,3,7,12)
                self.rect(c,nx-3,y-1,7,3,color)
                c[y,nx]=color if phase==0 else 12
            if lengths[r]==cols:c[y-1:y+2,61]=0
        if last>=0:
            r,j=divmod(last,cols);x,y=xs[j],ys[r]
            if knots:
                # Clicking this white loop ties the latest crossing over.
                c[y-5,x-5:x+6]=0;c[y+5,x-5:x+6]=0
                c[y-5:y+6,x-5]=0;c[y-5:y+6,x+5]=0
                c[y-6,x-1:x+2]=0
        # Persistent knots are recovered from history of skipped clock events.
        for before,after in zip(self.history,self.history[1:]+[self.state]):
            if after[3]<before[3] and before[4]>=0:
                r,j=divmod(before[4],cols);x,y=xs[j],ys[r]
                c[y-2,x-2]=0;c[y+2,x+2]=0
        # Remaining white loops in a compact bank beside the shared clock.
        for i in range(self.cfg['knots']):
            x=24+i*7;self.rect(c,x,5,5,5,0 if i<knots else 3)
            self.rect(c,x+1,6,3,3,5)
        if self.rejected:c[13,3:14]=8
        self.current_level.remove_all_sprites();self.current_level.add_sprite(Sprite(pixels=c,name='simple-loom',x=0,y=0,layer=0))
