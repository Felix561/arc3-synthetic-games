FIXED_LEVELS = [{'map': ['        ', '  ####  ', '  #..#  ', '  #..#  ', '  #..#  ', '  #..#  ', '  ####  ', '        '], 'shapes': [[[0, 0]]], 'start': [[3, 2]], 'goal': [[3, 5]], 'gate': [[4, 4]], 'open': True, 'gravity': 1, 'colors': [12]}, {'map': ['        ', '  ####  ', '  #..#  ', '  #..#  ', '  ##.#  ', '  #..#  ', '  ####  ', '        '], 'shapes': [[[0, 0]]], 'start': [[3, 2]], 'goal': [[4, 5]], 'gate': [[4, 4]], 'open': True, 'gravity': 1, 'colors': [12]}, {'map': ['        ', '  ####  ', '  #..#  ', '  #..#  ', '  #..#  ', '  #..#  ', '  ####  ', '        '], 'shapes': [[[0, 0]]], 'start': [[4, 2]], 'goal': [[4, 5]], 'gate': [[4, 4]], 'open': False, 'gravity': 1, 'colors': [12]}, {'map': ['  ##### ', '  #...# ', '###...##', '#......#', '#......#', '###..###', '  ####  ', '        '], 'shapes': [[[0, 0]], [[0, 0]]], 'start': [[3, 1], [5, 3]], 'goal': [[3, 4], [5, 1]], 'gate': [[3, 3]], 'open': False, 'gravity': 1, 'colors': [12, 9]}, {'map': ['  ##### ', '  #...# ', '###...##', '#......#', '#..#...#', '#..#..##', '####### ', '        '], 'shapes': [[[0, 0]], [[0, 0]]], 'start': [[3, 1], [5, 3]], 'goal': [[4, 3], [1, 3]], 'gate': [[3, 3]], 'open': False, 'gravity': 1, 'colors': [12, 9]}, {'map': ['  ####  ', '  #..###', '###....#', '#...#..#', '#......#', '###..###', '  ####  ', '        '], 'shapes': [[[0, 0], [1, 0]], [[0, 0]]], 'start': [[3, 1], [5, 3]], 'goal': [[5, 2], [3, 4]], 'gate': [[3, 3]], 'open': False, 'gravity': 1, 'colors': [12, 9]}, {'map': ['  ####  ', '  #..###', '###....#', '#...#..#', '#......#', '###..###', '  ####  ', '        '], 'shapes': [[[0, 0]], [[0, 0]], [[0, 0]]], 'start': [[3, 1], [5, 3], [1, 3]], 'goal': [[3, 4], [1, 3], [4, 4]], 'gate': [[3, 3]], 'open': False, 'gravity': 1, 'colors': [12, 9, 14]}]

# Fixed native puzzle mechanics.
DIRS = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}


def footprint(spec, positions, index):
    x, y = positions[index]
    return {(x + dx, y + dy) for dx, dy in spec['shapes'][index]}


def floor_cells(spec):
    return {(x, y) for y, row in enumerate(spec['map'])
            for x, char in enumerate(row) if char == '.'}


def initial(spec):
    return tuple(tuple(p) for p in spec['start']), spec['open'], spec['gravity']


def settle(spec, positions, opened, gravity):
    dx, dy = DIRS[gravity]
    free = floor_cells(spec)
    if not opened:
        free -= set(tuple(p) for p in spec['gate'])
    trace = []
    positions = tuple(positions)
    for _ in range(8):
        occupied = [footprint(spec, positions, i) for i in range(len(positions))]
        moving = {i for i, cells in enumerate(occupied)
                  if {(x + dx, y + dy) for x, y in cells} <= free}
        while True:
            blocked = {i for i in moving
                       if any({(x + dx, y + dy) for x, y in occupied[i]} & occupied[j]
                              for j in range(len(positions)) if j != i and j not in moving)}
            if not blocked:
                break
            moving -= blocked
        if not moving:
            break
        positions = tuple((x + dx, y + dy) if i in moving else (x, y)
                          for i, (x, y) in enumerate(positions))
        trace.append(positions)
    return positions, trace


def advance_trace(spec, state, action):
    positions, opened, gravity = state
    if action in DIRS:
        gravity = action
    elif action == 5:
        if opened and any(footprint(spec, positions, i) & set(tuple(p) for p in spec['gate'])
                          for i in range(len(positions))):
            return state, [], True
        opened = not opened
    else:
        return state, [], False
    settled, trace = settle(spec, positions, opened, gravity)
    return (settled, opened, gravity), trace, False


def advance(spec, state, action):
    return advance_trace(spec, state, action)[0]


def solved(spec, state):
    return state[0] == tuple(tuple(p) for p in spec['goal'])


def valid_state(spec, state):
    positions, opened, _ = state
    free = floor_cells(spec) - (set() if opened else set(tuple(p) for p in spec['gate']))
    seen = set()
    for i in range(len(positions)):
        body = footprint(spec, positions, i)
        if not body <= free or seen & body:
            return False
        seen |= body
    return True

"""SG25: guide conserved rigid grains through a gated gravity vessel."""
import numpy as np
from arcengine import ARCBaseGame, Camera, GameAction, Level, Sprite

PITCH = 7
ORIGIN = 4


def _level(index, spec):
    return Level(sprites=[Sprite(pixels=np.zeros((64,64),dtype=np.int64),
                                name='vessel',x=0,y=0,layer=0)],
                 grid_size=(64,64),data={'spec':spec},name=str(index+1))


class Sg25(ARCBaseGame):
    def __init__(self,seed=0):
        self._spec=None
        self._matter=None
        self._history=[]
        self._phases=[]
        self._blocked=False
        super().__init__(game_id='sg25-v1',levels=[_level(i,spec) for i,spec in enumerate(FIXED_LEVELS)],
                         camera=Camera(background=5,letter_box=5),
                         available_actions=[1,2,3,4,5,7],seed=seed)

    def on_set_level(self,level):
        self._spec=level.get_data('spec')
        self._matter=initial(self._spec)
        self._history=[]
        self._phases=[]
        self._blocked=False
        self._paint()

    def _finish_phase(self):
        self._matter=self._phases.pop(0)
        self._paint()
        if self._phases:
            return
        if solved(self._spec,self._matter):
            self.next_level()
        self.complete_action()

    def step(self):
        if self._phases:
            self._finish_phase()
            return
        action=self.action.id
        self._blocked=False
        if action==GameAction.RESET:
            self.complete_action()
            return
        if action==GameAction.ACTION7:
            if self._history:
                self._matter=self._history.pop()
            self._paint()
            self.complete_action()
            return
        action_id={GameAction.ACTION1:1,GameAction.ACTION2:2,GameAction.ACTION3:3,
                   GameAction.ACTION4:4,GameAction.ACTION5:5}.get(action)
        if action_id in (1,2,3,4,5):
            before=self._matter
            after,trace,self._blocked=advance_trace(self._spec,before,action_id)
            if after!=before:
                self._history.append(before)
                # The gate or gravity changes first; movement remains visible in
                # native intermediate frames before the final settled state.
                self._phases=[(before[0],after[1],after[2])]
                self._phases.extend((positions,after[1],after[2]) for positions in trace)
                if self._phases[-1]!=after:
                    self._phases.append(after)
                self._finish_phase()
                return
        # No ACTION6 handler: forced clicks cannot change state or history.
        self._paint()
        self.complete_action()

    @staticmethod
    def _rect(canvas,x,y,w,h,color):
        canvas[max(0,y):min(64,y+h),max(0,x):min(64,x+w)]=color

    def _body(self,canvas,cells,color,outline=False):
        cells=set(cells)
        for gx,gy in cells:
            x=ORIGIN+gx*PITCH;y=ORIGIN+gy*PITCH
            if outline:
                # Continuous target contour, including a domino's full footprint.
                for dx,dy in ((0,-1),(0,1),(-1,0),(1,0)):
                    if (gx+dx,gy+dy) not in cells:
                        if dx==-1:self._rect(canvas,x,y,1,PITCH,color)
                        elif dx==1:self._rect(canvas,x+PITCH-1,y,1,PITCH,color)
                        elif dy==-1:self._rect(canvas,x,y,PITCH,1,color)
                        else:self._rect(canvas,x,y+PITCH-1,PITCH,1,color)
            else:
                self._rect(canvas,x+1,y+1,PITCH-2,PITCH-2,color)
                if (gx+1,gy) in cells:self._rect(canvas,x+PITCH-1,y+1,2,PITCH-2,color)
                if (gx,gy+1) in cells:self._rect(canvas,x+1,y+PITCH-1,PITCH-2,2,color)

    def _paint(self):
        canvas=np.full((64,64),5,dtype=np.int64)
        positions,opened,gravity=self._matter
        free=floor_cells(self._spec)
        for gy,row in enumerate(self._spec['map']):
            for gx,char in enumerate(row):
                if char=='#':
                    x=ORIGIN+gx*PITCH;y=ORIGIN+gy*PITCH
                    self._rect(canvas,x,y,PITCH,PITCH,3)
                    # Edges beside actual interior space emphasize physical walls,
                    # never the otherwise invisible logical grid.
                    if (gx+1,gy) in free:self._rect(canvas,x+PITCH-1,y,1,PITCH,2)
                    if (gx-1,gy) in free:self._rect(canvas,x,y,1,PITCH,2)
                    if (gx,gy+1) in free:self._rect(canvas,x,y+PITCH-1,PITCH,1,2)
                    if (gx,gy-1) in free:self._rect(canvas,x,y,PITCH,1,2)
        for i,color in enumerate(self._spec['colors']):
            self._body(canvas,footprint(self._spec,self._spec['goal'],i),color,outline=True)
        for gx,gy in self._spec['gate']:
            x=ORIGIN+gx*PITCH;y=ORIGIN+gy*PITCH
            gate_color=0 if self._blocked else 11
            if opened:
                self._rect(canvas,x,y+2,1,3,gate_color)
                self._rect(canvas,x+PITCH-1,y+2,1,3,gate_color)
                self._rect(canvas,x,y,2,1,0)
            else:
                self._rect(canvas,x,y+2,PITCH,3,gate_color)
                self._rect(canvas,x,y+2,2,1,0)
        for i,color in enumerate(self._spec['colors']):
            self._body(canvas,footprint(self._spec,positions,i),color)
        # A small arrow outside the vessel shows the current global force. It
        # is not a progress meter and does not look like a clickable button.
        dx,dy=DIRS[gravity]
        cx=7;cy=7
        for distance in range(-2,3):
            self._rect(canvas,cx+dx*distance,cy+dy*distance,1,1,0)
        for spread in range(-2,3):
            distance=2-abs(spread)
            self._rect(canvas,cx+dx*distance-dy*spread,cy+dy*distance+dx*spread,1,1,0)
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=canvas,name='vessel',x=0,y=0,layer=0))
