"""Private original functional displacement ferry. Execute only in secured Docker."""
from copy import deepcopy
import numpy as np

# Pier (x, top); block (owner, width, height, initially immersed).
LEVELS = {
 0: {'piers': [(19,39),(55,35)], 'blocks': [(0,10,20,False)], 'capacity':[1,0], 'goal':1, 'start':0, 'side':1, 'tags':['one immersion','actual delivery']},
 1: {'piers': [(19,35),(55,39)], 'blocks': [(0,10,20,True)], 'capacity':[1,0], 'goal':1, 'start':0, 'side':1, 'tags':['retrieval reverses displacement']},
 2: {'piers': [(19,39),(55,34)], 'blocks': [(0,10,10,False),(0,10,20,False)], 'capacity':[2,0], 'goal':1, 'start':0, 'side':1, 'tags':['two visible quantities']},
 3: {'piers': [(19,39),(55,35)], 'blocks': [(0,10,10,False),(0,10,20,False)], 'capacity':[1,0], 'goal':1, 'start':0, 'side':1, 'tags':['one receiving pocket','exchange']},
 4: {'piers': [(19,35),(39,35),(59,32)], 'blocks': [(0,10,20,False),(2,10,20,True)], 'capacity':[1,0,1], 'goal':1, 'goal_side':1, 'start':0, 'side':1, 'tags':['middle depot','return delivery','local retrieval']},
 5: {'piers': [(16,35),(34,39),(54,35),(59,32)], 'blocks': [(1,10,20,False),(0,10,20,False),(2,10,10,False)], 'capacity':[1,1,1,0], 'goal':3, 'start':1, 'side':1, 'tags':['two feasible depots','different supply','recoverable branch']},
 6: {'piers': [(19,33),(39,35),(59,30)], 'blocks': [(0,10,10,True),(0,10,20,False),(1,10,20,True),(1,15,20,False)], 'capacity':[1,1,0], 'goal':2, 'start':0, 'side':1, 'tags':['capacity','necessary return','exchange before delivery']},
}

LEFT, RIGHT, FLOOR = 3, 61, 62
FLOAT_W, DRAFT, LOAD_H = 10, 3, 4

def _fluid_space(level, surface):
    c = LEVELS[level]
    return (RIGHT-LEFT)*(FLOOR-surface) - sum(2*max(0, FLOOR-max(surface, top)) for x,top in c['piers'])

def _surface(h):
    level=h['level']
    displaced=sum(w*t for on,(owner,w,t,initial) in zip(h['immersed'],LEVELS[level]['blocks']) if on)
    water=_fluid_space(level,39)-FLOAT_W*DRAFT
    lo,hi=20.0,39.0
    for _ in range(36):
        mid=(lo+hi)/2
        if _fluid_space(level,mid)-displaced-FLOAT_W*DRAFT > water: lo=mid
        else: hi=mid
    return (lo+hi)/2

def _deck(h):
    return int(round(_surface(h)))

def _boat_x(h):
    return LEVELS[h['level']]['piers'][h['station']][0]+(7 if h['side']>0 else -6)

def _snapshot(h):
    return {k:deepcopy(v) for k,v in h.items() if k!='history'}

def get_initial_state(level):
    c=LEVELS[level]
    h={'level':level,'station':c['start'],'side':c['side'],'immersed':[b[3] for b in c['blocks']], 'selected':None,'feedback':None,'delivered':False,'history':[]}
    return h,predict(h)

def get_available_actions():
    return [5,6,7]

def predict(h_t, seed=0):
    return {'surface':_surface(h_t),'deck':_deck(h_t),'boat_x':_boat_x(h_t)}

def _rack_rect(level,index):
    owner,w,t,initial=LEVELS[level]['blocks'][index]
    x=3+index*14
    return (x,3,x+w,3+t)

def _seat_rect(level,index):
    owner,w,t,initial=LEVELS[level]['blocks'][index]
    px=LEVELS[level]['piers'][owner][0]
    order=sum(1 for b in LEVELS[level]['blocks'][:index] if b[0]==owner)
    x=px-w-3 if LEVELS[level]['capacity'][owner]==1 or order==0 else px+4
    return (x,FLOOR-t,x+w,FLOOR)

def _block_hit(h,x,y):
    for i,on in enumerate(h['immersed']):
        owner,w,t,initial=LEVELS[h['level']]['blocks'][i]
        if owner!=h['station']: continue
        if on:
            r=_seat_rect(h['level'],i)
        else: r=_rack_rect(h['level'],i)
        if r[0]<=x<r[2] and r[1]<=y<r[3]: return i
    return None

def _travel(h,dest):
    c=LEVELS[h['level']]
    px,top=c['piers'][dest]
    if _deck(h)!=top: return None,('berth',dest)
    start=_boat_x(h)
    side=-1 if px>start else 1
    end=px+(7 if side>0 else -6)
    # Actual float/cargo sweep; destination pier is contacted at its facing side.
    a,b=sorted((start,end))
    bottom=_surface(h)+DRAFT
    for j,(x,y) in enumerate(c['piers']):
        if j==dest: continue
        if a-5<x+2 and b+5>x and bottom>y+0.01:
            return None,('pier',j)
    return side,None

def transition(h_t,z_t,action):
    h=deepcopy(h_t)
    if action==7:
        if h['history']:
            old=h['history'].pop(); hist=h['history']; h=deepcopy(old); h['history']=hist
        return h
    if h['delivered']: return h
    before=_snapshot(h)
    if isinstance(action,(tuple,list)) and len(action)==3 and action[0]==6:
        x,y=action[1:]
        if not isinstance(x,int) or not isinstance(y,int) or not(0<=x<64 and 0<=y<64): return h
        i=_block_hit(h,x,y)
        if i is not None:
            owner=LEVELS[h['level']]['blocks'][i][0]
            used=sum(on for on,b in zip(h['immersed'],LEVELS[h['level']]['blocks']) if b[0]==owner)
            if not h['immersed'][i] and used>=LEVELS[h['level']]['capacity'][owner]:
                h['feedback']=('pocket',owner)
            else:
                h['immersed'][i]=not h['immersed'][i];h['feedback']=None
        else:
            found=None
            for j,(px,top) in enumerate(LEVELS[h['level']]['piers']):
                if px-3<=x<px+5 and top-2<=y<top+2: found=j; break
            if found is None:return h
            h['selected']=None if h['selected']==found else found;h['feedback']=None
    elif action==5:
        if h['selected'] is None or h['selected']==h['station']:
            h['feedback']=('berth',h['station'])
        else:
            side,error=_travel(h,h['selected'])
            if error:h['feedback']=error
            else:
                h['station']=h['selected'];h['side']=side;h['selected']=None;h['feedback']=None
                h['delivered']=h['station']==LEVELS[h['level']]['goal'] and h['side']==LEVELS[h['level']].get('goal_side',-1)
    else:return h
    if _snapshot(h)!=before:
        h['history'].append(before)
        h['history']=h['history'][-100:]
    return h

def check_level_complete(h_t,z_t,level):
    return h_t['level']==level and h_t['delivered'] and h_t['station']==LEVELS[level]['goal'] and _deck(h_t)==LEVELS[level]['piers'][h_t['station']][1] and h_t['side']==LEVELS[level].get('goal_side',-1)

def render(h_t,z_t):
    h=h_t;c=LEVELS[h['level']]
    g=np.full((64,64),5,dtype=np.int8)
    surface=int(round(_surface(h))); deck=_deck(h); bx=_boat_x(h)
    g[surface:FLOOR,LEFT:RIGHT]=1
    g[surface:surface+1,LEFT:RIGHT]=12
    g[20:FLOOR+2,LEFT-2:LEFT]=3;g[20:FLOOR+2,RIGHT:RIGHT+2]=3;g[FLOOR:FLOOR+2,LEFT-2:RIGHT+2]=3
    # Substantial retaining walls and solid internal piers have no leak holes.
    for j,(px,top) in enumerate(c['piers']):
        g[top:FLOOR,px:px+2]=3
        col=8 if h['feedback'] and h['feedback'][1]==j else (14 if h['selected']==j else 2)
        g[top-1:top+1,px-3:px+5]=col
        if j==c['goal']:
            # Visible receiving cradle adjacent to landing, never a separate switch.
            rx=px+5 if c.get('goal_side',-1)>0 else px-8
            g[top-4:top,rx:rx+4]=4;g[top-4:top-3,rx:rx+4]=9
            g[top-1:top,rx:rx+4]=9
        if c['capacity'][j]:
            maxw=max(b[1] for b in c['blocks'] if b[0]==j)
            sx=px-maxw-3
            g[FLOOR-21:FLOOR,sx:sx+1]=2;g[FLOOR-21:FLOOR,sx+maxw:sx+maxw+1]=2
            g[FLOOR-1:FLOOR,sx:sx+maxw+1]=2
            if c['capacity'][j]>1:
                tx=px+4
                g[FLOOR-21:FLOOR,tx:tx+1]=2;g[FLOOR-21:FLOOR,tx+maxw:tx+maxw+1]=2
                g[FLOOR-1:FLOOR,tx:tx+maxw+1]=2
            # Crane rail reaches only this local water bay; no remote control.
            g[2:25,px-1:px+1]=2
            for i,b in enumerate(c['blocks']):
                if b[0]==j:
                    rx,ry,rx2,ry2=_rack_rect(h['level'],i)
                    g[1:2,min(rx,px):max(rx2,px)+1]=2
            if j==h['station']:g[24:deck,px-1:px+1]=14
    for i,on in enumerate(h['immersed']):
        owner,w,t,initial=c['blocks'][i]
        if on:
            x,y,x2,y2=_seat_rect(h['level'],i)
            g[y:FLOOR,x:x+w]=11;g[y:y+1,x:x+w]=10
        else:
            x,y,x2,y2=_rack_rect(h['level'],i)
            g[y:y2,x:x2]=11;g[y:y+1,x:x2]=10
    # Constant load and fixed draft: same object persists on every crossing.
    g[deck:surface+DRAFT,bx-5:bx+5]=2
    g[deck-LOAD_H:deck,bx-2:bx+2]=9
    g[deck:deck+1,bx-5:bx+5]=4
    return g


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


class V203(FunctionalGame):
    GAME_ID = 'v203-a4d822d4642c9bb3'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
