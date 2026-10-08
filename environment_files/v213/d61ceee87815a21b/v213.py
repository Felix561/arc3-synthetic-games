"""Selection Boundary: current filled region, loose markers and solid posts."""
import numpy as np

LEVELS = {
    0: {'corners': [(12,12),(36,12),(36,52),(12,52)], 'inside': [(40,22)], 'outside': [], 'posts': [], 'step': 4, 'active_tags': ['inside_outside']},
    1: {'corners': [(12,12),(48,12),(48,48),(12,48)], 'inside': [(20,51)], 'outside': [], 'posts': [], 'step': 4, 'active_tags': ['inside_outside','adjacent_edges']},
    2: {'corners': [(12,12),(36,12),(36,48),(12,48)], 'inside': [(40,40)], 'outside': [(44,22)], 'posts': [], 'step': 4, 'active_tags': ['inside_outside','exclusion']},
    3: {'corners': [(10,10),(50,10),(50,50),(10,50),(30,36),(30,24)], 'inside': [(20,20)], 'outside': [], 'posts': [(20,28,24,32)], 'step': 4, 'active_tags': ['inside_outside','solid_sweep']},
    4: {'corners': [(10,10),(50,10),(50,50),(10,50),(10,30)], 'inside': [(20,16),(20,44)], 'outside': [(22,30)], 'posts': [], 'step': 4, 'active_tags': ['inside_outside','exclusion','concavity']},
    5: {'corners': [(10,10),(50,10),(50,50),(10,50),(30,38),(30,22)], 'inside': [(20,18),(20,42)], 'outside': [(22,30)], 'posts': [], 'step': 4, 'active_tags': ['inside_outside','exclusion','concavity','shared_access']},
    6: {'corners': [(10,10),(50,10),(50,50),(10,50),(26,38),(26,22)], 'inside': [(24,14),(24,46),(44,30)], 'outside': [(30,30)], 'posts': [(36,28,40,32)], 'step': 4, 'active_tags': ['inside_outside','exclusion','concavity','solid_sweep']},
}

EPS = 1e-8
DIRECTIONS = {1:(0,-1),2:(0,1),3:(-1,0),4:(1,0)}

def _cross(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def _on(a,b,p):
    return abs(_cross(a,b,p)) <= EPS and min(a[0],b[0])-EPS <= p[0] <= max(a[0],b[0])+EPS and min(a[1],b[1])-EPS <= p[1] <= max(a[1],b[1])+EPS

def _intersect(a,b,c,d):
    s,t,u,v = _cross(a,b,c),_cross(a,b,d),_cross(c,d,a),_cross(c,d,b)
    if ((s > EPS and t < -EPS) or (s < -EPS and t > EPS)) and ((u > EPS and v < -EPS) or (u < -EPS and v > EPS)):
        return True
    return (abs(s)<=EPS and _on(a,b,c)) or (abs(t)<=EPS and _on(a,b,d)) or (abs(u)<=EPS and _on(c,d,a)) or (abs(v)<=EPS and _on(c,d,b))

def _contains(poly,p):
    """Pixel-center membership, including the actual closed boundary."""
    inside=False
    for i,a in enumerate(poly):
        b=poly[(i+1)%len(poly)]
        if _on(a,b,p):
            return True
        if (a[1]>p[1]) != (b[1]>p[1]):
            x=a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
            if x>p[0]:
                inside=not inside
    return inside

def _simple(poly):
    n=len(poly)
    area=sum(poly[i][0]*poly[(i+1)%n][1]-poly[(i+1)%n][0]*poly[i][1] for i in range(n))
    if abs(area)<=EPS:
        return False
    for i,a in enumerate(poly):
        b=poly[(i+1)%n]
        if abs(a[0]-b[0])+abs(a[1]-b[1])<=EPS:
            return False
        c=poly[(i+2)%n]
        if abs(_cross(a,b,c))<=EPS and (a[0]-b[0])*(c[0]-b[0])+(a[1]-b[1])*(c[1]-b[1])>EPS:
            return False
        for j in range(i+1,n):
            if j==i+1 or (i==0 and j==n-1):
                continue
            if _intersect(a,b,poly[j],poly[(j+1)%n]):
                return False
    return True

def _rect_poly(rect,padding=0):
    x1,y1,x2,y2=rect
    return [(x1-.5-padding,y1-.5-padding),(x2+.5+padding,y1-.5-padding),(x2+.5+padding,y2+.5+padding),(x1-.5-padding,y2+.5+padding)]

def _poly_hits_rect(poly,rect,padding=0):
    box=_rect_poly(rect,padding)
    if any(_contains(box,p) for p in poly) or (len(poly)>2 and any(_contains(poly,p) for p in box)):
        return True
    return any(_intersect(poly[i],poly[(i+1)%len(poly)],box[j],box[(j+1)%4]) for i in range(len(poly)) for j in range(4))

def _distance(a,b,p):
    dx,dy=b[0]-a[0],b[1]-a[1]
    den=dx*dx+dy*dy
    t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/den)) if den else 0
    return ((p[0]-a[0]-t*dx)**2+(p[1]-a[1]-t*dy)**2)**.5

def _edge_sweep_hits_post(poly,rect):
    """Exact distance from a segment/swept triangle to full solid material."""
    if _poly_hits_rect(poly,rect):
        return True
    box=_rect_poly(rect)
    for i,a in enumerate(poly):
        b=poly[(i+1)%len(poly)]
        for j,c in enumerate(box):
            d=box[(j+1)%4]
            if min(_distance(a,b,c),_distance(a,b,d),_distance(c,d,a),_distance(c,d,b))<=.75+EPS:
                return True
    return False

def _legal_shape(poly,posts):
    if not _simple(poly) or any(not(6<=x<=58 and 6<=y<=58) for x,y in poly):
        return False
    for i,p in enumerate(poly):
        if any(abs(p[0]-q[0])<=5 and abs(p[1]-q[1])<=5 for q in poly[i+1:]):
            return False
        for rect in posts:
            if _edge_sweep_hits_post([p,poly[(i+1)%len(poly)]],rect):
                return False
            if _poly_hits_rect([p],rect,2.5):
                return False
    return True

def _legal_move(poly,index,new,posts):
    """Continuous sweep, not endpoint sampling. Event roots cover simplicity."""
    old=poly[index]
    candidate=list(poly)
    candidate[index]=new
    if not _legal_shape(candidate,posts):
        return False
    for rect in posts:
        if _poly_hits_rect([old,new],rect,2.5):
            return False
        for neighbor in (poly[(index-1)%len(poly)],poly[(index+1)%len(poly)]):
            triangle=[neighbor,old,new]
            if _edge_sweep_hits_post(triangle,rect):
                return False
    # A moving square handle must not pass through any other square handle.
    for j,p in enumerate(poly):
        if j!=index and _poly_hits_rect([old,new],(p[0]-2,p[1]-2,p[0]+2,p[1]+2),2.5):
            return False
    # Every orientation involving the single moving vertex is affine in t.
    # Intersection truth can change only at these exact event roots.
    roots={0.0,1.0}
    n=len(poly)
    for a in range(n):
        for b in range(a+1,n):
            for c in range(b+1,n):
                if index not in (a,b,c):
                    continue
                u=_cross(poly[a],poly[b],poly[c])
                v=_cross(candidate[a],candidate[b],candidate[c])
                if abs(v-u)>EPS:
                    t=-u/(v-u)
                    if EPS<t<1-EPS:
                        roots.add(t)
    times=sorted(roots)
    times+= [(a+b)/2 for a,b in zip(times,times[1:])]
    for t in times:
        shape=list(poly)
        shape[index]=(old[0]+t*(new[0]-old[0]),old[1]+t*(new[1]-old[1]))
        if not _simple(shape):
            return False
    return True

def _marker_pixels(center,kind):
    x,y=center
    return [(x+dx,y+dy) for dy in range(-2,3) for dx in range(-2,3) if (dx*dx+dy*dy<=4 if kind=='inside' else dx==0 or dy==0)]

def _membership(poly,center,kind):
    flags=[_contains(poly,p) for p in _marker_pixels(center,kind)]
    return all(flags) if kind=='inside' else not any(flags)

def get_initial_state(level_index):
    return {'level':level_index,'corners':list(LEVELS[level_index]['corners']),'selected':-1,'feedback':None,'history':[]},{}

def get_available_actions():
    return [1,2,3,4,6,7]

def _snapshot(h):
    return {k:(list(v) if k=='corners' else v) for k,v in h.items() if k!='history'}

def transition(h_t,z_t,a_t):
    h={**_snapshot(h_t),'history':list(h_t['history'])}
    number=a_t[0] if isinstance(a_t,tuple) else a_t
    if number==7:
        if h['history']:
            previous=h['history'].pop()
            return {**previous,'corners':list(previous['corners']),'history':h['history']}
        return h
    if number not in [1,2,3,4,6]:
        return h
    old=_snapshot(h)
    h['feedback']=None
    if number==6:
        x,y=a_t[1:]
        hit=next((i for i,p in enumerate(h['corners']) if abs(p[0]-x)<=2 and abs(p[1]-y)<=2),None)
        if hit is not None:
            h['selected']=hit
        else:
            h['feedback']=('miss',x,y)
    elif h['selected']!=-1:
        i=h['selected']
        x,y=h['corners'][i]
        dx,dy=DIRECTIONS[number]
        step=LEVELS[h['level']]['step']
        new=(x+dx*step,y+dy*step)
        if _legal_move(h['corners'],i,new,LEVELS[h['level']]['posts']):
            h['corners'][i]=new
        else:
            h['feedback']=('blocked',i)
    if _snapshot(h)!=old:
        h['history'].append(old)
    return h

def predict(h_t,seed):
    return {}

def check_level_complete(h_t,z_t,level_index):
    level=LEVELS[level_index]
    poly=h_t['corners']
    return _legal_shape(poly,level['posts']) and all(_membership(poly,p,'inside') for p in level['inside']) and all(_membership(poly,p,'outside') for p in level['outside'])

def render(h_t,z_t):
    canvas=np.full((64,64),1,dtype=np.int8)
    poly=h_t['corners']
    level=LEVELS[h_t['level']]
    for y in range(64):
        for x in range(64):
            if _contains(poly,(x,y)):
                canvas[y,x]=15
            if any(_distance(poly[i],poly[(i+1)%len(poly)],(x,y))<=.75 for i in range(len(poly))):
                canvas[y,x]=14
    for x1,y1,x2,y2 in level['posts']:
        canvas[y1:y2+1,x1:x2+1]=3
        canvas[y1+1:y2,x1+1:x2]=5
    for i,(x,y) in enumerate(poly):
        selected=h_t['selected']==i
        # The entire drawn frame stays inside the true 5x5 corner hit area.
        # A surviving perimeter distinguishes the control from marker material.
        canvas[y-2:y+3,x-2:x+3]=10 if selected else 3
        canvas[y-1:y+2,x-1:x+2]=5
        if h_t['feedback']==('blocked',i):
            # Keep selection across top/bottom, with distinct blocked side strips.
            canvas[y-1:y+2,x-2]=11
            canvas[y-1:y+2,x+2]=11
    if h_t['feedback'] and h_t['feedback'][0]=='miss':
        _,x,y=h_t['feedback']
        canvas[y,x]=8
    # Loose stationary markers are never erased by boundary/control/feedback paint.
    # Their colors are disjoint from selected yellow and blocked orange frames.
    for kind in ('inside','outside'):
        for p in level[kind]:
            good=_membership(poly,p,kind)
            for x,y in _marker_pixels(p,kind):
                canvas[y,x]=((13 if good else 0) if kind=='inside' else (12 if good else 8))
            canvas[p[1],p[0]]=0 if kind=='inside' else 3
    return canvas


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


class V213(FunctionalGame):
    GAME_ID = 'v213-d61ceee87815a21b'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
