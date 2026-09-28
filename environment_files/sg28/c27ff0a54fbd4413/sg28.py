FIXED_LEVELS = [{'start': [3, 4], 'heading': [1, -1], 'bumpers': [], 'active': [], 'goal': [2, 5], 'goal_heading': [-1, 1]}, {'start': [1, 5], 'heading': [1, -1], 'bumpers': [], 'active': [], 'goal': [2, 4], 'goal_heading': [-1, 1]}, {'start': [2, 5], 'heading': [1, -1], 'bumpers': [2], 'active': [True], 'goal': [3, 4], 'goal_heading': [-1, 1]}, {'start': [1, 6], 'heading': [1, -1], 'bumpers': [2, 5], 'active': [False, False], 'goal': [3, 5], 'goal_heading': [1, 1]}, {'start': [0, 7], 'heading': [1, -1], 'bumpers': [1, 4], 'active': [False, True], 'goal': [2, 4], 'goal_heading': [-1, -1]}, {'start': [2, 5], 'heading': [1, -1], 'bumpers': [2, 6], 'active': [True, True], 'goal': [1, 2], 'goal_heading': [-1, 1]}, {'start': [1, 5], 'heading': [1, -1], 'bumpers': [1, 5, 6], 'active': [False, False, True], 'goal': [3, 5], 'goal_heading': [-1, -1]}]

"""Two equal-mass runners on a lane with timed, retractable bumpers."""

N = 8


def initial(cfg):
    return tuple(cfg['start']), tuple(cfg['heading']), tuple(cfg['active'])


def goal_projection(state):
    return state[0], state[1]


def solved(cfg, state):
    return goal_projection(state) == (tuple(cfg['goal']), tuple(cfg['goal_heading']))


def pulse(cfg, state):
    positions, headings, active = state
    proposals = []
    next_headings = []
    for pos, direction in zip(positions, headings):
        nxt = pos + direction
        gap = pos if direction > 0 else pos - 1
        wall = nxt < 0 or nxt >= N
        bumper = gap in cfg['bumpers'] and active[cfg['bumpers'].index(gap)]
        if wall or bumper:
            proposals.append(pos)
            next_headings.append(-direction)
        else:
            proposals.append(nxt)
            next_headings.append(direction)
    impact = proposals[0] == proposals[1] or (
        proposals[0] == positions[1] and proposals[1] == positions[0]
    )
    if impact:
        # First apply any spring reflection, then the contact reflection.
        return (positions, tuple(-d for d in next_headings), active), True
    return (tuple(proposals), tuple(next_headings), active), False


def advance(cfg, state, action):
    if action == 'pulse':
        return pulse(cfg, state)[0]
    if type(action) is int and 0 <= action < len(cfg['bumpers']):
        pos, heading, active = state
        out = list(active)
        out[action] = not out[action]
        return pos, heading, tuple(out)
    return state


def center(position):
    return 8 + 7 * position, 28


def bumper_center(gap):
    return 11 + 7 * gap, 39

import numpy as np
from arcengine import ARCBaseGame,Camera,Level,Sprite,GameAction


class Sg28(ARCBaseGame):
    def __init__(self,seed=0):
        self.cfg=None;self.state=None;self.history=[];self.last_impact=False
        levels=[Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),name='runners')],
                      grid_size=(64,64),data={'layout':cfg},name='Impact %d'%(i+1))
                for i,cfg in enumerate(FIXED_LEVELS)]
        super().__init__(game_id='sg28-v1',levels=levels,camera=Camera(background=5,letter_box=5),
                         available_actions=[5,6,7],seed=seed)

    def on_set_level(self,level):
        self.cfg=level.get_data('layout');self.state=initial(self.cfg)
        self.history=[];self.last_impact=False;self._paint()

    def _bumper_at(self,x,y):
        # Runners are painted over plungers. A click on a runner must not
        # activate a bumper whose hidden shaft happens to be nearby.
        for pos in self.state[0]:
            px,py=center(pos);dx=abs(x-px);dy=abs(y-py)
            if (dx<=3 and dy<=2) or (dx<=2 and dy<=3):return None
        for i,gap in enumerate(self.cfg['bumpers']):
            bx,_=bumper_center(gap)
            dx=abs(x-bx)
            shaft=(self.state[2][i] and dx<=1 and 21<=y<=33)
            retracted=(not self.state[2][i] and dx<=1 and 34<=y<=38)
            stem=(dx==0 and 33<=y<=43)
            handle=(dx<=3 and 38<=y<=43)
            if shaft or retracted or stem or handle:return i
        return None

    def step(self):
        a=0 if self.action.id==GameAction.RESET else int(self.action.id.name[-1])
        self.last_impact=False
        if a==7:
            if self.history:self.state=self.history.pop()
        elif a==5:
            nxt,hit=pulse(self.cfg,self.state)
            if nxt!=self.state:
                self.history.append(self.state);self.state=nxt;self.last_impact=hit
        elif a==6:
            d=self.action.data or {};x,y=d.get('x',-99),d.get('y',-99)
            if type(x) is int and type(y) is int:
                if 2<=x<=14 and 48<=y<=60:
                    nxt,hit=pulse(self.cfg,self.state)
                    if nxt!=self.state:
                        self.history.append(self.state);self.state=nxt;self.last_impact=hit
                else:
                    i=self._bumper_at(x,y)
                    if i is not None:
                        self.history.append(self.state)
                        self.state=advance(self.cfg,self.state,i)
        self._paint()
        if solved(self.cfg,self.state):self.next_level()
        self.complete_action()

    def _paint(self):
        c=np.full((64,64),5,dtype=np.int64)
        # Thick rail and its regularly spaced physical sockets fill the native board.
        c[24:33,4:61]=3
        c[24,4:61]=4;c[32,4:61]=4
        for pos in range(N):
            x,_=center(pos)
            c[26:31,x]=4
            c[33:36,x]=4
        # Target bays above the same lane have colored identity and a direction notch.
        for i,(pos,direction) in enumerate(zip(self.cfg['goal'],self.cfg['goal_heading'])):
            x,_=center(pos);col=(12,9)[i]
            c[8,x-3:x+4]=col;c[17,x-3:x+4]=col
            c[9:17,x-3]=col;c[9:17,x+3]=col
            c[18:22,x]=4
            c[12,x-direction]=0;c[12,x]=0;c[12,x+direction]=0
            c[11,x+2*direction]=0;c[12,x+2*direction]=0;c[13,x+2*direction]=0
        positions,headings,active=self.state
        for i,gap in enumerate(self.cfg['bumpers']):
            x,y=bumper_center(gap)
            # The handle is physically connected to a plunger between two sockets.
            c[33:43,x]=4
            c[38:44,x-3:x+4]=3
            c[40:43,x-2:x+3]=0 if active[i] else 2
            if active[i]:
                c[21:34,x-1:x+2]=11
                c[23:32,x]=0
            else:
                c[34:39,x-1:x+2]=6
        if self.last_impact:
            x=(center(positions[0])[0]+center(positions[1])[0])//2
            c[19:23,x]=11;c[20:22,x-2:x+3]=11
        for i,(pos,direction) in enumerate(zip(positions,headings)):
            x,y=center(pos);col=(12,9)[i]
            c[y-2:y+3,x-3:x+4]=col
            c[y-3:y+4,x-2:x+3]=col
            c[y,x-direction]=0;c[y,x]=0;c[y,x+direction]=0
            c[y-1,x+2*direction]=0;c[y,x+2*direction]=0;c[y+1,x+2*direction]=0
        # The click-to-pulse crank is attached to the left rail by a visible stem.
        c[33:50,8]=4
        c[49:60,2:15]=3;c[50:59,3:14]=12
        c[53:56,5:10]=0;c[52:57,10:12]=0
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=c,name='impact-lane',x=0,y=0,layer=0))
