"""Original finite-body clearance toy; execute only in the secured runtime."""
from copy import deepcopy
from math import sin, cos, pi, sqrt

LEVELS = {0: {'stops': (24, 40),
     'wall': ((0, 24, 8, 30),),
     'leaves': ((20, 34, 16, 4, 0, -90),),
     'initial': (0, (0,)),
     'doors': ((25, 32, 35, 36),)},
 1: {'stops': (16, 32),
     'wall': ((0, 24, 8, 30),),
     'leaves': ((44, 34, 16, 4, 180, 270),),
     'initial': (1, (0,)),
     'doors': ((29, 32, 39, 36),)},
 2: {'stops': (24, 40),
     'wall': ((0, 24, 8, 30),),
     'leaves': ((20, 34, 16, 4, 0, -90),),
     'initial': (0, (0,)),
     'doors': ((25, 32, 35, 36), (40, 23, 48, 31))},
 3: {'stops': (24, 31, 38),
     'wall': ((0, 24, 6, 29),),
     'leaves': ((20, 34, 16, 4, 0, -90), (44, 18, 12, 4, 180, 90)),
     'initial': (0, (0, 0)),
     'doors': ((25, 32, 35, 36), (29, 16, 39, 20), (36, 23, 41, 30))},
 4: {'stops': (9, 17, 25, 33),
     'wall': ((6, 31, 14, 37), (-4, 14, 0, 36), (22, 24, 26, 36), (-4, 32, 26, 36), (8, 32, 12, 48)),
     'leaves': ((42, 16, 14, 4, 180, 90), (24, 54, 14, 4, 180, 360)),
     'initial': (2, (1, 0)),
     'doors': ((29, 21, 45, 30), (10, 51, 18, 57))},
 5: {'stops': (9, 17, 25, 33),
     'wall': ((6, 31, 14, 37), (-4, 14, 0, 36), (22, 24, 26, 36), (-4, 32, 26, 36), (8, 32, 12, 48)),
     'leaves': ((42, 16, 14, 4, 180, 90), (24, 54, 14, 4, 180, 360)),
     'initial': (2, (0, 0)),
     'doors': ((29, 21, 45, 30), (10, 51, 18, 57))},
 6: {'stops': (9, 17, 25, 33),
     'wall': ((6, 31, 14, 37), (-4, 14, 0, 36), (22, 24, 26, 36), (-4, 32, 26, 36), (8, 32, 12, 48)),
     'leaves': ((42, 16, 14, 4, 180, 90), (24, 54, 14, 4, 180, 360)),
     'initial': (0, (0, 0)),
     'doors': ((29, 21, 45, 30), (10, 51, 18, 57))}}

def rectangle(r):
    a,b,c,d = r
    return ((a,b),(c,b),(c,d),(a,d))

def leaf_polygon(config, angle):
    x,y,length,width,a,b = config
    t = angle*pi/180
    u,v = (cos(t),sin(t)), (-sin(t),cos(t))
    return tuple((x+s*u[0]+q*v[0], y+s*u[1]+q*v[1]) for s,q in ((0,-width/2),(length,-width/2),(length,width/2),(0,width/2)))

def hinge(config):
    x,y = config[:2]
    return rectangle((x-3,y-3,x+3,y+3))

def wall_polygons(config, x):
    return tuple(rectangle((a+x,b,c+x,d)) for a,b,c,d in config['wall'])

def overlap(a,b, margin=0):
    # Closed polygons: contact blocks. Margin bounds the small arc sagitta.
    for poly in (a,b):
        for k in range(len(poly)):
            p,q = poly[k],poly[(k+1)%len(poly)]
            nx,ny = q[1]-p[1], p[0]-q[0]
            scale = sqrt(nx*nx+ny*ny)
            av = [nx*x+ny*y for x,y in a]
            bv = [nx*x+ny*y for x,y in b]
            if max(av)+margin*scale < min(bv)-1e-8 or max(bv)+margin*scale < min(av)-1e-8:
                return False
    return True

def hull(points):
    p = sorted(set(points))
    def cross(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    lower=[]
    for q in p:
        while len(lower)>=2 and cross(lower[-2],lower[-1],q)<=0:
            lower.pop()
        lower.append(q)
    upper=[]
    for q in reversed(p):
        while len(upper)>=2 and cross(upper[-2],upper[-1],q)<=0:
            upper.pop()
        upper.append(q)
    return tuple(lower[:-1]+upper[:-1])

def scene(config, wall_index, poses):
    x=config['stops'][wall_index]
    bodies=[leaf_polygon(c,c[4+poses[k]]) for k,c in enumerate(config['leaves'])]
    return wall_polygons(config,x), bodies

def valid(config, wall_index, poses):
    walls,bodies=scene(config,wall_index,poses)
    roots=[hinge(c) for c in config['leaves']]
    for poly in list(walls)+bodies+roots:
        if any(x<5 or x>59 or y<6 or y>58 for x,y in poly):
            return False
    if any(overlap(w,r) for w in walls for r in roots):
        return False
    if any(overlap(w,b) for w in walls for b in bodies):
        return False
    if any(overlap(bodies[i],bodies[j]) for i in range(len(bodies)) for j in range(i)):
        return False
    if any(overlap(bodies[i],roots[j]) for i in range(len(bodies)) for j in range(len(roots)) if i!=j):
        return False
    return True

def rotation_collision(config, wall_index, poses, index):
    walls,bodies=scene(config,wall_index,poses)
    c=config['leaves'][index]
    obstacles=list(walls)+[b for k,b in enumerate(bodies) if k!=index]+[hinge(q) for k,q in enumerate(config['leaves']) if k!=index]
    lo,hi=sorted((c[4],c[5]))
    count=max(1,int((hi-lo)/5))
    step=(hi-lo)/count
    radius=sqrt(c[2]*c[2]+(c[3]/2)**2)
    margin=radius*(1-cos(step*pi/360))+1e-7
    for k in range(count):
        swept=hull(leaf_polygon(c,lo+k*step)+leaf_polygon(c,lo+(k+1)*step))
        if any(x-margin<5 or x+margin>59 or y-margin<6 or y+margin>58 for x,y in swept):
            return ('bounds',)
        for obstacle in obstacles:
            if overlap(swept,obstacle,margin):
                return obstacle
    return None

def rotation_clear(config, wall_index, poses, index):
    return rotation_collision(config,wall_index,poses,index) is None

def translation_collision(config, wall_index, poses, destination):
    if not 0<=destination<len(config['stops']):
        return ('stop',)
    start,end=config['stops'][wall_index],config['stops'][destination]
    walls,bodies=scene(config,wall_index,poses)
    obstacles=bodies+[hinge(c) for c in config['leaves']]
    for a,b,c,d in config['wall']:
        sweep=rectangle((a+min(start,end),b,c+max(start,end),d))
        if any(x<5 or x>59 or y<6 or y>58 for x,y in sweep):
            return ('bounds',)
        for obstacle in obstacles:
            if overlap(sweep,obstacle):
                return obstacle
    return None

def translation_clear(config, wall_index, poses, destination):
    return translation_collision(config,wall_index,poses,destination) is None

def get_initial_state(level):
    config=LEVELS[level]
    wall_index,poses=config['initial']
    h={'level':level,'wall_index':wall_index,'poses':poses,'feedback':None,'history':[]}
    return h,{}

def core(h):
    return {k:deepcopy(v) for k,v in h.items() if k!='history'}

def transition(h_t,z_t,action):
    h=deepcopy(h_t)
    if action==7:
        if h['history']:
            past=h['history'].pop(); history=h['history']; h=past; h['history']=history
        return h
    config=LEVELS[h['level']]
    accepted=None
    contact=None
    move=None
    if action in (3,4):
        move=action
        destination=h['wall_index']+(-1 if action==3 else 1)
        contact=translation_collision(config,h['wall_index'],h['poses'],destination)
        accepted=contact is None
        feedback=('wall',0,contact)
    elif isinstance(action,tuple) and action[0]==6:
        _,x,y=action
        index=next((k for k,c in enumerate(config['leaves']) if c[0]-3<=x<c[0]+3 and c[1]-3<=y<c[1]+3),None)
        if index is None:
            a,b,c,d=config['wall'][0]
            wx=config['stops'][h['wall_index']]
            if not wx+a<=x<wx+c or not b<=y<d:
                return h
            move=3 if x<wx+(a+c)/2 else 4
            destination=h['wall_index']+(-1 if move==3 else 1)
            contact=translation_collision(config,h['wall_index'],h['poses'],destination)
            accepted=contact is None
            feedback=('wall',0,contact)
        else:
            contact=rotation_collision(config,h['wall_index'],h['poses'],index)
            accepted=contact is None
            feedback=('leaf',index,contact)
    else:
        return h
    h['history'].append(core(h))
    h['feedback']=None if accepted else feedback
    if accepted:
        if move in (3,4):
            h['wall_index']=destination
        else:
            p=list(h['poses']); p[index]=1-p[index]; h['poses']=tuple(p)
    return h

def predict(h_t,seed):
    return {}

def check_level_complete(h_t,z_t,level):
    config=LEVELS[level]
    walls,bodies=scene(config,h_t['wall_index'],h_t['poses'])
    roots=[hinge(c) for c in config['leaves']]
    return h_t['level']==level and valid(config,h_t['wall_index'],h_t['poses']) and all(not overlap(rectangle(d),p) for d in config['doors'] for p in list(walls)+bodies+roots)

def get_available_actions():
    return [3,4,6,7]

def inside(point,poly):
    x,y=point
    return all((poly[(k+1)%len(poly)][0]-p[0])*(y-p[1])-(poly[(k+1)%len(poly)][1]-p[1])*(x-p[0])>=-1e-8 for k,p in enumerate(poly))

def render(h_t,z_t):
    config=LEVELS[h_t['level']]
    image=[[0]*64 for _ in range(64)]
    def paint(poly,color):
        for y in range(64):
            for x in range(64):
                if inside((x+.5,y+.5),poly): image[y][x]=color
    # Doorways are real clearance regions, drawn with two substantial jambs.
    for a,b,c,d in config['doors']:
        paint(rectangle((a-2,b-2,a,d+2)),11)
        paint(rectangle((c,b-2,c+2,d+2)),11)
    # One horizontal guide and attached broad grip; no remote selector.
    left,right=min(config['stops'])+min(a for a,b,c,d in config['wall']),max(config['stops'])+max(c for a,b,c,d in config['wall'])
    paint(rectangle((left,38,right,39)),2)
    walls,bodies=scene(config,h_t['wall_index'],h_t['poses'])
    for poly in walls: paint(poly,4)
    for k,poly in enumerate(bodies): paint(poly,12 if k==0 else 14)
    for k,c in enumerate(config['leaves']):
        paint(hinge(c),12 if k==0 else 14)
        paint(rectangle((c[0]-1,c[1]-1,c[0]+1,c[1]+1)),1)
    x=config['stops'][h_t['wall_index']]
    # The broad grip is a surface patch inside the wall's actual material.
    a,b,c,d=config['wall'][0]
    paint(rectangle((x+a+1,b+1,x+c-1,d-1)),0)
    paint(rectangle((x+(a+c)/2-.5,b+1,x+(a+c)/2+.5,d-1)),4)
    if h_t['feedback']:
        kind,index,contact=h_t['feedback']
        if len(contact)>1:
            paint(contact,8)
        if kind=='leaf':
            c=config['leaves'][index]; paint(rectangle((c[0]-1,c[1]-1,c[0]+1,c[1]+1)),8)
        else: paint(rectangle((x+a+1,b+1,x+c-1,d-1)),8)
    return image


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


class V207(FunctionalGame):
    GAME_ID = 'v207-a8b53bd94a9471c7'
    NUM_LEVELS = 7
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions
    }
