"""Original contact-changing closed-path process; execute only in secured Docker."""
import copy
import math
import numpy as np

LEVELS = {0: {'gates': [(31, 29)], 'phase': [1], 'bodies': [('g', 0, 'E')], 'paths': [(0, 'L', 0, 'L', [(19, 29), (13, 41), (31, 41)]), (0, 'T', 0, 'B', [(43, 17), (49, 29), (43, 41)]), (0, 'B', 0, 'T', [(43, 41), (49, 29), (43, 17)])], 'pockets': []}, 1: {'gates': [(31, 29)], 'phase': [0], 'bodies': [('g', 0, 'F')], 'paths': [(0, 'L', 0, 'L', [(19, 29), (13, 17), (31, 17)]), (0, 'T', 0, 'B', [(43, 23), (49, 35), (31, 41)]), (0, 'B', 0, 'T', [(31, 41), (49, 35), (43, 23)])], 'pockets': []}, 2: {'gates': [(17, 28), (47, 28)], 'phase': [1, 0], 'bodies': [('g', 0, 'E'), ('g', 1, 'F')], 'paths': [(0, 'L', 0, 'L', [(11, 28), (5, 28), (5, 34), (5, 40), (11, 40), (17, 40), (17, 34)]), (0, 'T', 0, 'B', [(17, 22), (17, 16), (23, 16), (23, 22), (23, 28), (23, 34)]), (0, 'B', 0, 'T', [(23, 34), (23, 28), (23, 22), (23, 16), (17, 16), (17, 22)]), (1, 'L', 1, 'L', [(41, 28), (35, 28), (35, 34), (35, 40), (41, 40), (47, 40), (47, 34)]), (1, 'T', 1, 'B', [(47, 22), (47, 16), (53, 16), (59, 16), (59, 22), (59, 28), (59, 34), (53, 34)]), (1, 'B', 1, 'T', [(53, 34), (59, 34), (59, 28), (59, 22), (59, 16), (53, 16), (47, 16), (47, 22)])], 'pockets': []}, 3: {'gates': [(31, 29)], 'phase': [1], 'bodies': [('g', 0, 'E'), ('p', 0, 0, 4)], 'paths': [(0, 'L', 0, 'L', [(25, 29), (19, 29), (13, 29), (13, 35), (13, 41), (19, 41), (25, 41), (31, 41), (31, 47), (31, 35)]), (0, 'T', 0, 'B', [(31, 23), (31, 17), (37, 17), (43, 17), (49, 17), (49, 23), (49, 29), (49, 35), (43, 35), (37, 35)]), (0, 'B', 0, 'T', [(37, 35), (43, 35), (49, 35), (49, 29), (49, 23), (49, 17), (43, 17), (37, 17), (31, 17), (31, 23)])], 'pockets': [(0, 4, False, 7, 41)]}, 4: {'gates': [[17, 22], [47, 22], [32, 43]], 'phase': [0, 0, 0], 'bodies': [['r', 7, 2], ['r', 2, 4]], 'paths': [[0, 'L', 2, 'T', [[17, 29], [17, 35], [26, 35]]], [0, 'T', 0, 'B', [[17, 16], [11, 10], [5, 10], [5, 16], [5, 22], [5, 28], [11, 28]]], [0, 'B', 0, 'T', [[11, 28], [5, 28], [5, 22], [5, 16], [5, 10], [11, 10], [17, 16]]], [1, 'L', 2, 'B', [[47, 29], [47, 35], [44, 43], [44, 49]]], [1, 'T', 1, 'B', [[53, 16], [59, 16], [59, 22], [59, 28], [53, 34], [47, 34]]], [1, 'B', 1, 'T', [[47, 34], [53, 34], [59, 28], [59, 22], [59, 16], [53, 16]]], [2, 'L', 2, 'L', [[26, 43], [20, 49], [20, 55], [26, 55], [32, 55], [32, 49]]], [2, 'T', 1, 'L', [[32, 37], [38, 31], [41, 28]]], [2, 'B', 0, 'L', [[26, 49], [20, 43], [11, 34], [11, 28]]]], 'pockets': [(1, 3, True, 11, 16), (4, 3, False, 53, 28), (6, 3, False, 26, 61)]}, 5: {'gates': [[17, 22], [47, 22], [32, 43], (9, 45)], 'phase': [0, 1, 0, 1], 'bodies': [('r', 1, 1), ('r', 4, 1)], 'paths': [[0, 'L', 2, 'T', [[17, 29], [17, 35], [26, 35]]], [0, 'T', 0, 'B', [[17, 16], [11, 10], [5, 10], [5, 16], [5, 22], [5, 28], [11, 28]]], [0, 'B', 0, 'T', [[11, 28], [5, 28], [5, 22], [5, 16], [5, 10], [11, 10], [17, 16]]], [1, 'L', 2, 'B', [[47, 29], [47, 35], [44, 43], [44, 49]]], [1, 'T', 1, 'B', [[53, 16], [59, 16], [59, 22], [59, 28], [53, 34], [47, 34]]], [1, 'B', 1, 'T', [[47, 34], [53, 34], [59, 28], [59, 22], [59, 16], [53, 16]]], [2, 'L', 2, 'L', [[26, 43], [20, 49], [20, 55], [26, 55], [32, 55], [32, 49]]], [2, 'T', 1, 'L', [[32, 37], [38, 31], [41, 28]]], (2, 'B', 3, 'T', [(26, 49), (20, 43), (14, 40)]), (3, 'L', 3, 'L', [(3, 45), (3, 51), (3, 57), (9, 57), (15, 57), (15, 51)]), (3, 'T', 0, 'L', [(9, 39), (9, 33), (11, 28)]), (3, 'B', 1, 'L', [(15, 51), (21, 57), (39, 57), (45, 51), (41, 34), (41, 28)])], 'pockets': [(1, 3, False, 11, 16), (4, 3, False, 53, 28), (6, 3, False, 26, 61), (9, 1, False, 9, 51)]}, 6: {'gates': [[17, 22], [47, 22], [32, 43]], 'phase': [0, 0, 0], 'bodies': [('r', 1, 3), ('r', 1, 5), ('r', 1, 0), ('p', 0, 1, 3)], 'paths': [[0, 'L', 2, 'T', [[17, 29], [17, 35], [26, 35]]], [0, 'T', 0, 'B', [[17, 16], [11, 10], [5, 10], [5, 16], [5, 22], [5, 28], [11, 28]]], [0, 'B', 0, 'T', [[11, 28], [5, 28], [5, 22], [5, 16], [5, 10], [11, 10], [17, 16]]], [1, 'L', 2, 'B', [[47, 29], [47, 35], [44, 43], [44, 49]]], [1, 'T', 1, 'B', [[53, 16], [59, 16], [59, 22], [59, 28], [53, 34], [47, 34]]], [1, 'B', 1, 'T', [[47, 34], [53, 34], [59, 28], [59, 22], [59, 16], [53, 16]]], [2, 'L', 2, 'L', [[26, 43], [20, 49], [20, 55], [26, 55], [32, 55], [32, 49]]], [2, 'T', 1, 'L', [[32, 37], [38, 31], [41, 28]]], [2, 'B', 0, 'L', [[26, 49], [20, 43], [11, 34], [11, 28]]]], 'pockets': [(1, 3, False, 11, 16), (4, 3, False, 53, 28), (6, 3, True, 26, 61)]}}

def get_available_actions():
    return [5,6,7]

def _key(h):
    return (tuple(tuple(b) for b in h['bodies']),tuple(h['phase']),tuple(h['open']),h.get('example',0))

def _main_key(h):
    return (tuple(tuple(b) for b in h['bodies']),tuple(h['phase']),tuple(h['open']))

def _snapshot(h):
    return {'level':h['level'],'bodies':copy.deepcopy(h['bodies']),'phase':list(h['phase']),'open':list(h['open']),'example':h.get('example',0)}

def get_initial_state(level):
    c=LEVELS[level]
    h={'level':level,'bodies':[list(b) for b in c['bodies']],'phase':list(c['phase']),
       'open':[p[2] for p in c['pockets']],'undo':[],'example':0,'notice':None}
    return h,predict(h,0)

def _xy(h,b):
    c=LEVELS[h['level']]
    if b[0]=='p':
        return tuple(c['pockets'][b[1]][3:5])
    if b[0]!='g':return tuple(c['paths'][b[1]][4][b[2]])
    return _port_xy(c,b[1],b[2])

def _port_xy(c,gate,port):
    x,y=c['gates'][gate]
    dx,dy={'L':(-6,0),'T':(0,-6),'B':(6,6),'E':(-5,7),'F':(-5,-7)}[port]
    return x+dx,y+dy

def _route_points(c,path):
    # Route strokes meet actual transport ports, never a different hinge-center
    # endpoint. Centerlines are material continuity, not a future-route forecast.
    return [_port_xy(c,path[0],path[1])]+list(path[4])+[_port_xy(c,path[2],path[3])]

def _next(h,b):
    c=LEVELS[h['level']]
    if b[0]=='p':
        if not h['open'][b[1]]:return list(b),None
        path,index=b[2:4]
        return ['r',path,index],None
    if b[0]=='g':
        phase=h['phase'][b[1]]
        choices={'L':('T','B'),'T':('L',None),'B':(None,'L'),'E':('B',None),'F':(None,'T')}
        outlet=choices[b[2]][phase]
        if outlet is None:return list(b),None
        for i,p in enumerate(c['paths']):
            if p[0]==b[1] and p[1]==outlet:return ['r',i,0],b[1]
        return list(b),None
    p=c['paths'][b[1]]
    if b[2]+1<len(p[4]):
        for i,pocket in enumerate(c['pockets']):
            point=c['paths'][pocket[0]][4][pocket[1]]
            if tuple(p[4][b[2]+1])==tuple(point) and h['open'][i]:return ['p',i,b[1],b[2]+1],None
        return ['r',b[1],b[2]+1],None
    return ['g',p[2],p[3]],None

def _beat(h):
    out=_snapshot(h)
    out['example']=(out['example']+1)%8
    proposed=[_next(h,b) for b in h['bodies']]
    blocked=set()
    points=[_xy(h,p[0]) for p in proposed]
    old=[_xy(h,b) for b in h['bodies']]
    for i in range(len(points)):
        for j in range(i):
            if max(abs(points[i][0]-points[j][0]),abs(points[i][1]-points[j][1]))<5 or (points[i]==old[j] and points[j]==old[i]):
                blocked.update((i,j))
    # If a prevented move leaves an occupied footprint, no other body enters it.
    changed=True
    while changed:
        changed=False
        for i in range(len(points)):
            if i in blocked:continue
            for j in blocked:
                if max(abs(points[i][0]-old[j][0]),abs(points[i][1]-old[j][1]))<5:
                    blocked.add(i);changed=True;break
    moved=[]
    for i,(b,gate) in enumerate(proposed):
        good=i not in blocked and b!=h['bodies'][i]
        moved.append(good and points[i]!=old[i])
        if good:
            out['bodies'][i]=b
            if gate is not None:out['phase'][gate]^=1
    return out,moved

def _recurrence(h):
    c=LEVELS[h['level']]
    positions=sum(len(p[4]) for p in c['paths'])+5*len(c['gates'])
    for pocket in c['pockets']:
        point=tuple(c['paths'][pocket[0]][4][pocket[1]])
        positions+=sum(tuple(q)==point for p in c['paths'] for q in p[4])
    bound=(positions**len(h['bodies']))*(2**(len(c['gates'])+len(c['pockets'])))
    # Finite-state bound, not a period/action quota. Floyd keeps memory constant.
    slow=_beat(h)[0];fast=_beat(_beat(h)[0])[0]
    for _ in range(bound):
        if _main_key(slow)==_main_key(fast):break
        slow=_beat(slow)[0];fast=_beat(_beat(fast)[0])[0]
    else:raise ValueError('Finite state recurrence bound contradicted')
    start=_snapshot(h);begin=0
    while _main_key(start)!=_main_key(slow):
        start=_beat(start)[0];slow=_beat(slow)[0];begin+=1
    active=[False]*len(h['bodies']);period=0;cur=_snapshot(start)
    while True:
        cur,moved=_beat(cur);period+=1
        active=[a or b for a,b in zip(active,moved)]
        if _main_key(cur)==_main_key(start):break
    # Exemplar is a disjoint genuine 8-position body. Product recurrence exactly
    # returns its actual current pose too; factorization avoids empty simulation.
    full_period=math.lcm(period,8)
    return {'live':begin==0 and all(active),'period':full_period,'main_period':period,
            'transient':begin,'active':active,'exemplar_active':True,'state_bound':bound*8}

def transition(h,z,action):
    out=copy.deepcopy(h)
    number=action[0] if isinstance(action,(tuple,list)) else action
    if number==0:return get_initial_state(h['level'])[0]
    if number==7:
        if out['undo']:
            previous=out['undo'].pop(); history=out['undo'];out.update(previous);out['undo']=history
        return out
    old={**_snapshot(h),'example':h['example'],'notice':h['notice']}
    out['notice']=None
    if number==5:
        future,moved=_beat(h);out.update(future);out['example']=(h['example']+1)%8
        if not any(moved):out['notice']=('stop',)
    elif number==6:
        x,y=action[1:];c=LEVELS[h['level']];found=False
        for i,(gx,gy) in enumerate(c['gates']):
            if abs(x-gx)<=4 and abs(y-gy)<=4 and any(b[0]=='g' and b[1]==i for b in h['bodies']):
                out['phase'][i]^=1;found=True;break
        if not found:
            for i,pocket in enumerate(c['pockets']):
                path,index=pocket[:2]
                px,py=c['paths'][path][4][index]
                bx,by=pocket[3:5];mx,my=(px+bx)//2,(py+by)//2
                horizontal=abs(by-py)>=abs(bx-px)
                hit=abs(x-mx)<=(3 if horizontal else 1) and abs(y-my)<=(1 if horizontal else 3)
                if hit:
                    out['open'][i]=not out['open'][i];found=True;break
        if not found:return copy.deepcopy(h)
    else:return out
    out['undo'].append(old)
    if len(out['undo'])>180:out['undo']=out['undo'][-180:]
    return out

def predict(h,seed):
    future,moved=_beat(h)
    return {'moving':moved,'recurrence':_recurrence(h)}

def check_level_complete(h,z,level):
    return bool(h['level']==level and _recurrence(h)['live'])

def _line(a,p,q,color,width=3):
    x0,y0=p;x1,y1=q;n=max(abs(x1-x0),abs(y1-y0),1)
    for j in range(n+1):
        x=round(x0+(x1-x0)*j/n);y=round(y0+(y1-y0)*j/n);r=width//2
        a[max(0,y-r):min(64,y+r+1),max(0,x-r):min(64,x+r+1)]=color

def render(h,z):
    a=np.full((64,64),5,dtype=np.int8);c=LEVELS[h['level']]
    for p in c['paths']:
        points=_route_points(c,p)
        for x,y in zip(points,points[1:]):_line(a,x,y,2,5)
    # Paint all broad tracks first, then their actual centerlines. Shared points
    # remain shared: no false overpass, bridge gap or separate collision layer.
    for p in c['paths']:
        points=_route_points(c,p)
        for x,y in zip(points,points[1:]):_line(a,x,y,3,1)
    # Tiny genuine passive exemplar: one connected closed route, one moving body.
    ep=[(52,4),(55,4),(58,4),(58,7),(58,10),(55,10),(52,10),(52,7)]
    for p,q in zip(ep,ep[1:]+ep[:1]):_line(a,p,q,2,3)
    ex,ey=ep[h['example']];a[ey-1:ey+2,ex-1:ex+2]=12
    for i,(gx,gy) in enumerate(c['gates']):
        _line(a,(gx,gy+5),(gx-5,gy+5),2,5)
        seed_ports=[b[2] for b in c['bodies'] if b[0]=='g' and b[1]==i and b[2] in ('E','F')]
        for port in seed_ports:
            offset=7 if port=='E' else -7
            _line(a,(gx-5,gy),(gx-5,gy+offset),2,5)
        a[gy-4:gy+5,gx-4:gx+5]=0
        color=9 if any(b[0]=='g' and b[1]==i for b in h['bodies']) else 3
        if h['phase'][i]==0:_line(a,(gx-3,gy+2),(gx+2,gy-3),color,3)
        else:_line(a,(gx-3,gy-2),(gx+2,gy+3),color,3)
        a[gy-1:gy+2,gx-1:gx+2]=4
        for port in seed_ports:
            offset=5 if port=='E' else -5
            _line(a,(gx-3,gy),(gx-5,gy+offset),color,3)
    for i,pocket in enumerate(c['pockets']):
        path,index=pocket[:2]
        px,py=c['paths'][path][4][index]
        bx,by=pocket[3:5];mx,my=(px+bx)//2,(py+by)//2
        _line(a,(px,py),(bx,by),2,5)
        a[by-3:by+4,bx-3:bx+4]=2
        if abs(by-py)>=abs(bx-px):
            if not h['open'][i]:_line(a,(mx-3,my),(mx+3,my),9,3)
            else:
                a[my-1:my+2,mx-3:mx-1]=9;a[my-1:my+2,mx+2:mx+4]=9
        else:
            if not h['open'][i]:_line(a,(mx,my-3),(mx,my+3),9,3)
            else:
                a[my-3:my-1,mx-1:mx+2]=9;a[my+2:my+4,mx-1:mx+2]=9
    colors=(12,8,11,6)
    for i,b in enumerate(h['bodies']):
        x,y=_xy(h,b)
        a[y-2:y+3,x-2:x+3]=colors[i%len(colors)]
        # Body identity is a connected material form, with a small open center.
        a[y,x]=0
    return a


"""Seven-level functional bridge; execute in the secured ARC runtime only."""
import numpy as np
from arcengine import ARCBaseGame, Camera, GameAction, Level, Sprite


class FunctionalGame(ARCBaseGame):
    def __init__(self, seed=0):
        self.functions = self.FUNCTIONS
        self.tick = 0
        self.h_t, self.z_t = self.functions["get_initial_state"](0)
        levels = [Level(grid_size=(64, 64), name=f"Level {i+1}") for i in range(7)]
        super().__init__(game_id=self.GAME_ID, levels=levels,
                         camera=Camera(background=5, letter_box=5),
                         available_actions=self.functions["get_available_actions"](), seed=seed)

    def on_set_level(self, level):
        self.tick = 0
        self.h_t, self.z_t = self.functions["get_initial_state"](self.level_index)
        self.paint()

    def paint(self):
        pixels = np.asarray(self.functions["render"](self.h_t, self.z_t), dtype=np.int8)
        if pixels.shape != (64, 64) or pixels.min() < 0 or pixels.max() > 15:
            raise ValueError("Functional render must be native 64x64 palette indices")
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=pixels, name="viewport", collidable=False))

    def step(self):
        number = int(self.action.id.value)
        if self.action.id != GameAction.RESET:
            event = (number, int(self.action.data["x"]), int(self.action.data["y"])) if number == 6 else number
            self.h_t = self.functions["transition"](self.h_t, self.z_t, event)
            self.tick += 1
            self.z_t = self.functions["predict"](self.h_t, self._seed * 10000 + self.tick)
            self.paint()
            if self.functions["check_level_complete"](self.h_t, self.z_t, self.level_index):
                self.next_level()
        self.complete_action()


"""PROPOSED v219-only accepted-current-cycle presentation; not host executable.

Only exact genuine passive states are displayed. A long certified period is
walked in full internally; the response may omit beats, never interpolate them.
The received action changes authoritative state once. Its accepted current state
and Undo history do not advance with this separate presentation copy.
"""

class OngoingMotionPresentation(FunctionalGame):
    def _presentation_clear(self):
        self._presentation_states = None
        self._presentation_indices = None
        self._presentation_cursor = 0
        self._presentation_authority = None
        self._presentation_certificate = None

    def on_set_level(self, level):
        self._presentation_clear()
        super().on_set_level(level)

    def _presentation_plan(self, accepted, period):
        # 125 actual snapshots, one ordinary completion frame retaining closure,
        # and at most one setup frame fit under the unchanged 128-frame cap.
        # This is solely a display budget, never a goal.
        budget = 125
        if not isinstance(period, int) or isinstance(period, bool) or period < 1:
            raise ValueError('Invalid certified full-process period')
        origin = _snapshot(accepted)
        origin_xy = [tuple(_xy(origin, body)) for body in origin['bodies']]
        mandatory = {0, period}
        changed = [False] * len(origin_xy)
        example_changed = False
        uniform = {j * period // (budget - 1) for j in range(budget)}
        snapshots = {0: origin}
        cur = _snapshot(origin)
        for beat in range(1, period + 1):
            cur, _ = _beat(cur)
            required = False
            for index, body in enumerate(cur['bodies']):
                if not changed[index] and tuple(_xy(cur, body)) != origin_xy[index]:
                    changed[index] = True
                    required = True
            if not example_changed and cur['example'] != origin['example']:
                example_changed = True
                required = True
            if required:
                mandatory.add(beat)
            if required or beat in uniform:
                snapshots[beat] = _snapshot(cur)
        if _key(cur) != _key(origin) or cur['level'] != origin['level']:
            raise ValueError('Certified cycle did not close exactly')
        if not all(changed) or not example_changed:
            raise ValueError('Certified process lacks actual body activity')
        # At most 125 uniform + 4 main-body + 1 exemplar snapshots are stored.
        # Never discard a body-activity witness, accepted origin or exact closure.
        for beat in sorted(set(snapshots) - mandatory, reverse=True):
            if len(snapshots) <= budget:
                break
            del snapshots[beat]
        if len(snapshots) > budget:
            raise ValueError('Unexpected v219 population/display mismatch')
        indices = sorted(snapshots)
        states = [snapshots[beat] for beat in indices]
        certificate = {'period': period, 'walked_beats': period,
                       'snapshot_indices': indices,
                       'omitted_beats': period + 1 - len(indices),
                       'completion_closure_frames': 1,
                       'all_main_bodies_visible_in_motion': changed,
                       'exemplar_visible_in_motion': example_changed,
                       'exact_closure': True}
        return states, indices, certificate

    def _presentation_paint(self, display):
        pixels = np.asarray(self.functions['render'](display, self.z_t), dtype=np.int8)
        if pixels.shape != (64, 64) or pixels.min() < 0 or pixels.max() > 15:
            raise ValueError('Functional render must be native 64x64 palette indices')
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=pixels, name='viewport', collidable=False))

    def _presentation_continue(self):
        if (self.h_t, self.z_t, self.tick) != self._presentation_authority:
            raise ValueError('Presentation mutated authoritative action/history')
        if self._presentation_cursor == len(self._presentation_states) - 1:
            # A previous ordinary step already painted and emitted exact closure.
            # This completion iteration retains that same genuine closing pose;
            # engine progression/setup follows using ordinary public lifecycle.
            self._presentation_clear()
            self.next_level()
            self.complete_action()
            return
        self._presentation_cursor += 1
        self._presentation_paint(self._presentation_states[self._presentation_cursor])

    def step(self):
        if self._presentation_states is not None:
            self._presentation_continue()
            return
        if self.action.id == GameAction.RESET:
            self._presentation_clear()
            self.complete_action()
            return
        number = int(self.action.id.value)
        event = (number, int(self.action.data['x']), int(self.action.data['y'])) if number == 6 else number
        self.h_t = self.functions['transition'](self.h_t, self.z_t, event)
        self.tick += 1
        self.z_t = self.functions['predict'](self.h_t, self._seed * 10000 + self.tick)
        self.paint()
        if self.functions['check_level_complete'](self.h_t, self.z_t, self.level_index):
            self._presentation_authority = copy.deepcopy((self.h_t, self.z_t, self.tick))
            states, indices, certificate = self._presentation_plan(
                self.h_t, self.z_t['recurrence']['period'])
            self._presentation_states = states
            self._presentation_indices = indices
            self._presentation_certificate = certificate
            self._presentation_cursor = 0
            # Engine records the accepted origin now. Further ordinary step()
            # calls paint actual passive snapshots, then exact closure, before
            # public next_level/complete_action finish this same received action.
            return
        self.complete_action()


class V219(OngoingMotionPresentation):
    GAME_ID = 'v219-f70869827a8dd010'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
