import math
import numpy as np
from arcengine import ARCBaseGame, Camera, Level, Sprite, GameAction

SCALE_COLORS = (9, 12, 14, 13)

FIXED_LEVELS = [
    {
        'nodes': [[9, 20, 0], [20, 40, 0], [43, 20, 0], [54, 40, 0], [48, 55, 2]],
        'weights': [[2, 0], [1, 1]],
        'scales': [[[0, 1], [2, 3], 1, 27, 8]],
        'edges': [[0, 1, 0, -1], [1, 2, 0, -1], [2, 3, 0, -1], [3, 4, 3, 0]],
        'exit': 4,
        'lever': False,
        'lever_at': None
    },
    {
        'nodes': [[11, 18, 0], [11, 37, 0], [31, 51, 1], [50, 37, 0], [52, 18, 0], [9, 55, 2]],
        'weights': [[2, 4], [1, 3]],
        'scales': [[[0, 1], [3, 4], -1, 32, 8]],
        'edges': [[4, 3, 0, -1], [3, 2, 0, -1], [2, 1, 0, -1], [1, 0, 0, -1], [1, 5, 3, 0]],
        'exit': 5,
        'lever': False,
        'lever_at': None
    },
    {
        'nodes': [[10, 19, 0], [20, 38, 0], [45, 19, 0], [53, 38, 0], [31, 51, 1], [53, 55, 2]],
        'weights': [[3, 0], [1, 1], [1, 2]],
        'scales': [[[0, 1], [2, 3], 1, 27, 8]],
        'edges': [[0, 1, 0, -1], [1, 4, 0, -1], [4, 3, 0, -1], [2, 3, 0, -1], [2, 4, 0, -1], [3, 5, 3, 0]],
        'exit': 5,
        'lever': False,
        'lever_at': None
    },
    {
        'nodes': [[10, 17, 0], [19, 34, 0], [31, 46, 1], [43, 34, 0], [54, 17, 0], [53, 55, 2]],
        'weights': [[2, 0], [1, 1], [1, 4]],
        'scales': [[[0, 1], [3, 4], 1, 32, 8]],
        'edges': [[0, 1, 0, -1], [1, 2, 1, -1], [2, 3, 1, -1], [3, 4, 0, -1], [3, 5, 3, 0]],
        'exit': 5,
        'lever': False,
        'lever_at': None
    },
    {
        'nodes': [[7, 18, 0], [10, 38, 0], [31, 18, 0], [31, 38, 0], [57, 18, 0], [52, 38, 0], [52, 56, 2]],
        'weights': [[1, 0], [2, 1], [2, 4]],
        'scales': [[[0, 1], [2, 3], -3, 22, 8], [[4], [5], 0, 42, 8]],
        'edges': [[0, 3, 0, -1], [1, 0, 0, -1], [2, 3, 0, -1], [3, 5, 3, 0], [4, 5, 0, -1], [5, 6, 3, 1]],
        'exit': 6,
        'lever': False,
        'lever_at': None
    },
    {
        'nodes': [[7, 18, 0], [7, 38, 0], [57, 18, 0], [57, 38, 0], [31, 49, 1], [54, 52, 2]],
        'weights': [[1, 0], [1, 1]],
        'scales': [[[0, 1], [2, 3], -2, 22, 8], [[4], [3], 1, 40, 8]],
        'edges': [[0, 2, 2, -1], [1, 3, 2, -1], [3, 4, 3, 0], [5, 4, 4, 1]],
        'exit': 5,
        'lever': True,
        'lever_at': [57, 8]
    },
    {
        'nodes': [[10, 24, 0], [10, 42, 0], [27, 32, 0], [43, 24, 0], [54, 42, 0], [27, 55, 1], [54, 56, 2]],
        'weights': [[2, 0], [1, 1], [1, 2], [1, 4]],
        'scales': [[[0, 1], [2, 3], 0, 11, 8], [[2], [3], 0, 27, 8], [[3], [4], 0, 43, 8]],
        'edges': [[0, 1, 0, -1], [2, 3, 0, -1], [1, 5, 2, -1], [5, 3, 2, -1], [6, 4, 4, 2]],
        'exit': 6,
        'lever': True,
        'lever_at': [56, 8]
    }
]


class Sg06(ARCBaseGame):
    def __init__(self, seed=0):
        self.spec = {}
        self.positions = []
        self.selected = None
        self.unlocked = set()
        self.lever = False
        self.history = []
        levels = []
        for index, spec in enumerate(FIXED_LEVELS):
            blank = np.zeros((64, 64), dtype=np.int32)
            sprite = Sprite(pixels=blank, name='apparatus', x=0, y=0, layer=0)
            levels.append(Level(sprites=[sprite], grid_size=(64, 64), data={'spec': spec}, name='station_%d' % index))
        super().__init__(game_id='sg06-v1', levels=levels, camera=Camera(background=0, letter_box=0), available_actions=[6, 7], seed=seed)

    def on_set_level(self, level):
        self.spec = level.get_data('spec')
        self.positions = [weight[1] for weight in self.spec['weights']]
        self.selected = None
        self.unlocked = set()
        self.lever = bool(self.spec['lever'])
        self.history = []
        self._refresh_locks()
        self._render_board()

    def _snapshot(self):
        return (self.positions[:], self.selected, set(self.unlocked), self.lever)

    def _restore(self, state):
        positions, selected, unlocked, lever = state
        self.positions = positions[:]
        self.selected = selected
        self.unlocked = set(unlocked)
        self.lever = lever

    def _scale_totals(self, index):
        scale = self.spec['scales'][index]
        left_total = 0
        right_total = 0
        for node in scale[0]:
            for weight_index, position in enumerate(self.positions):
                if position == node:
                    left_total += self.spec['weights'][weight_index][0]
        for node in scale[1]:
            for weight_index, position in enumerate(self.positions):
                if position == node:
                    right_total += self.spec['weights'][weight_index][0]
        return left_total, right_total

    def _scale_difference(self, index):
        left_total, right_total = self._scale_totals(index)
        return left_total - right_total

    def _refresh_locks(self):
        for index, scale in enumerate(self.spec['scales']):
            if self._scale_difference(index) == scale[2]:
                self.unlocked.add(index)

    def _all_open(self):
        return len(self.unlocked) == len(self.spec['scales'])

    def _is_goal(self):
        return self._all_open() and self.selected is not None and self.positions[self.selected] == self.spec['exit']

    def _weight_at(self, node):
        for index, position in enumerate(self.positions):
            if position == node:
                return index
        return None

    def _edge_allowed(self, source, target):
        for edge in self.spec['edges']:
            u, v, kind, lock = edge
            if kind == 0:
                if (source == u and target == v) or (source == v and target == u):
                    return True
            elif kind == 1:
                if source == u and target == v:
                    return True
            elif kind == 2:
                if not self.lever and source == u and target == v:
                    return True
                if self.lever and source == v and target == u:
                    return True
            elif kind == 3:
                if lock in self.unlocked and ((source == u and target == v) or (source == v and target == u)):
                    return True
            elif kind == 4:
                if lock in self.unlocked and not self.lever and source == u and target == v:
                    return True
                if lock in self.unlocked and self.lever and source == v and target == u:
                    return True
        return False

    def _node_at(self, x, y):
        best = None
        best_distance = 10 ** 9
        for index, node in enumerate(self.spec['nodes']):
            dx = x - node[0]
            dy = y - node[1]
            if abs(dx) <= 8 and abs(dy) <= 8:
                distance = dx * dx + dy * dy
                if distance < best_distance:
                    best = index
                    best_distance = distance
        return best

    def _handle_click(self):
        data = getattr(self.action, 'data', {}) or {}
        x = data.get('x')
        y = data.get('y')
        if x is None or y is None:
            return False
        x = int(x)
        y = int(y)
        lever_at = self.spec['lever_at']
        if lever_at is not None and abs(x - lever_at[0]) <= 5 and abs(y - lever_at[1]) <= 5:
            self.history.append(self._snapshot())
            self.lever = not self.lever
            self._render_board()
            return False
        node = self._node_at(x, y)
        if node is None:
            return False
        before = self._snapshot()
        changed = False
        if self.selected is None:
            weight_index = self._weight_at(node)
            if weight_index is not None:
                self.selected = weight_index
                changed = True
        else:
            weight_index = self._weight_at(node)
            if weight_index == self.selected:
                self.selected = None
                changed = True
            elif weight_index is not None:
                self.selected = weight_index
                changed = True
            else:
                source = self.positions[self.selected]
                if self._edge_allowed(source, node):
                    self.history.append(before)
                    self.positions[self.selected] = node
                    self._refresh_locks()
                    self._render_board()
                    return self._is_goal()
        if changed:
            self.history.append(before)
            self._render_board()
            return self._is_goal()
        return False

    def _undo(self):
        if self.history:
            self._restore(self.history.pop())
            self._render_board()

    def step(self):
        if self.action.id == GameAction.RESET:
            self.complete_action()
            return
        if self.action.id == GameAction.ACTION6:
            if self._handle_click():
                self.next_level()
        elif self.action.id == GameAction.ACTION7:
            self._undo()
        self.complete_action()

    def _pixel(self, canvas, x, y, color):
        if 0 <= x < 64 and 0 <= y < 64:
            canvas[y, x] = color

    def _rect(self, canvas, x, y, width, height, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(64, x + width)
        y1 = min(64, y + height)
        if x0 < x1 and y0 < y1:
            canvas[y0:y1, x0:x1] = color

    def _line(self, canvas, x0, y0, x1, y1, color, width=1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        error = dx - dy
        radius = max(0, (width - 1) // 2)
        while True:
            for oy in range(-radius, radius + 1):
                for ox in range(-radius, radius + 1):
                    self._pixel(canvas, x0 + ox, y0 + oy, color)
            if x0 == x1 and y0 == y1:
                break
            twice = 2 * error
            if twice > -dy:
                error -= dy
                x0 += sx
            if twice < dx:
                error += dx
                y0 += sy

    def _outline(self, canvas, x, y, width, height, color):
        self._line(canvas, x, y, x + width - 1, y, color)
        self._line(canvas, x, y + height - 1, x + width - 1, y + height - 1, color)
        self._line(canvas, x, y, x, y + height - 1, color)
        self._line(canvas, x + width - 1, y, x + width - 1, y + height - 1, color)

    def _draw_arrow(self, canvas, start, end, color):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.sqrt(dx * dx + dy * dy)
        if length < 1:
            return
        ux = dx / length
        uy = dy / length
        px = -uy
        py = ux
        mx = (start[0] + end[0]) / 2.0
        my = (start[1] + end[1]) / 2.0
        tip = (int(round(mx + ux * 3)), int(round(my + uy * 3)))
        base_x = mx - ux * 2
        base_y = my - uy * 2
        wing_a = (int(round(base_x + px * 2)), int(round(base_y + py * 2)))
        wing_b = (int(round(base_x - px * 2)), int(round(base_y - py * 2)))
        self._line(canvas, tip[0], tip[1], wing_a[0], wing_a[1], color, 1)
        self._line(canvas, tip[0], tip[1], wing_b[0], wing_b[1], color, 1)

    def _draw_gate_bars(self, canvas, a, b, color):
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        length = max(1.0, math.sqrt(dx * dx + dy * dy))
        ux = dx / length
        uy = dy / length
        px = -uy
        py = ux
        mx = (a[0] + b[0]) / 2.0
        my = (a[1] + b[1]) / 2.0
        for offset in (-2, 2):
            cx = mx + ux * offset
            cy = my + uy * offset
            self._line(canvas, int(round(cx - px * 3)), int(round(cy - py * 3)), int(round(cx + px * 3)), int(round(cy + py * 3)), color, 2)

    def _scale_color(self, index):
        return SCALE_COLORS[index % len(SCALE_COLORS)]

    def _meter_cell_positions(self, mx, my, side):
        if side == 'left':
            return ((mx - 6, my + 2), (mx - 4, my + 2), (mx - 6, my + 4), (mx - 4, my + 4), (mx - 6, my + 6), (mx - 4, my + 6))
        return ((mx + 3, my + 2), (mx + 5, my + 2), (mx + 3, my + 4), (mx + 5, my + 4), (mx + 3, my + 6), (mx + 5, my + 6))

    def _meter_slots(self, total):
        amount = max(0, int(total))
        return min(6, amount), amount > 6

    def _overflow_marker_pos(self, mx, my, side):
        if side == 'left':
            return mx - 6, my + 6
        return mx + 6, my + 6

    def _draw_tally(self, canvas, mx, my, side, total, theme):
        shown, overflow = self._meter_slots(total)
        cells = self._meter_cell_positions(mx, my, side)
        active_color = theme if side == 'left' else 10
        for slot, point in enumerate(cells):
            color = active_color if slot < shown else 4
            self._pixel(canvas, point[0], point[1], color)
        if overflow:
            ox, oy = self._overflow_marker_pos(mx, my, side)
            self._pixel(canvas, ox, oy, 15)
            direction = 1 if side == 'left' else -1
            self._pixel(canvas, ox + direction, oy - 1, 15)

    def _balance_totals(self, index):
        left,right=self._scale_totals(index)
        target=self.spec['scales'][index][2]
        return left+max(0,-target),right+max(0,target)

    def _draw_meter(self, canvas, index, scale):
        mx,my=scale[3],scale[4];theme=self._scale_color(index)
        left,right=self._balance_totals(index)
        tilt=max(-2,min(2,left-right))
        # A horizontal pale outline is the balance position, never another meter.
        self._line(canvas,mx-6,my,mx+6,my,3)
        # Heavy side is lower, attached to a central fulcrum.
        self._line(canvas,mx,my-1,mx-2,my+4,2)
        self._line(canvas,mx-2,my+4,mx+2,my+4,2)
        self._line(canvas,mx+2,my+4,mx,my-1,2)
        self._line(canvas,mx-6,my+tilt,mx+6,my-tilt,0)
        for side,total,yy,fixed in ((-1,left,my+tilt,max(0,-scale[2])),(1,right,my-tilt,max(0,scale[2]))):
            xx=mx+side*5
            self._line(canvas,xx,yy,xx,yy+3,theme)
            self._line(canvas,xx-2,yy+3,xx+2,yy+3,theme)
            # Unit blocks match the movable weights; bolted units are fixed tare.
            for n in range(min(total,6)):
                ux=xx-2+(n%2)*3;uy=yy+2-(n//2)*2
                self._rect(canvas,ux,uy,2,2,12 if n>=fixed else 2)
                if n<fixed:self._pixel(canvas,ux,uy,0)
        # The goal is actual horizontal equilibrium; the gate itself shows its latch.

    def _draw_lever(self, canvas):
        lever_at=self.spec['lever_at']
        if lever_at is None:return
        cx,cy=lever_at
        self._rect(canvas,cx-5,cy-4,11,9,4)
        self._line(canvas,cx-4,cy+3,cx+4,cy+3,2)
        direction=-1 if self.lever else 1
        self._line(canvas,cx,cy+2,cx+direction*3,cy-2,0)
        self._rect(canvas,cx+direction*3-1,cy-3,3,3,12)

    def _draw_edges(self, canvas):
        nodes = self.spec['nodes']
        for edge in self.spec['edges']:
            u, v, kind, lock = edge
            a = (nodes[u][0], nodes[u][1])
            b = (nodes[v][0], nodes[v][1])
            is_gate = kind in (3, 4)
            is_open = not is_gate or lock in self.unlocked
            theme = self._scale_color(lock) if is_gate else 5
            if kind in (0, 3):
                if kind == 3 and not is_open:
                    inner = 10
                elif kind == 3:
                    inner = theme
                else:
                    inner = 4
                self._line(canvas, a[0], a[1], b[0], b[1], 3, 5)
                self._line(canvas, a[0], a[1], b[0], b[1], inner, 3)
                self._line(canvas, a[0], a[1], b[0], b[1], 5, 1)
            else:
                if is_gate and not is_open:
                    inner = 3
                else:
                    inner = 8
                self._line(canvas, a[0], a[1], b[0], b[1], 3, 5)
                self._line(canvas, a[0], a[1], b[0], b[1], inner, 2)
                if not is_gate or is_open:
                    if kind == 1:
                        direction = (a, b)
                    elif self.lever:
                        direction = (b, a)
                    else:
                        direction = (a, b)
                    self._draw_arrow(canvas, direction[0], direction[1], 0)
            if is_gate:
                gate_color = theme if is_open else 10
                if not is_open:self._draw_gate_bars(canvas,a,b,8)
                else:
                    self._pixel(canvas,(a[0]+b[0])//2+3,(a[1]+b[1])//2,theme)
                mx = int(round((a[0] + b[0]) / 2.0))
                my = int(round((a[1] + b[1]) / 2.0))
                self._pixel(canvas, mx, my, theme)

    def _draw_node(self, canvas, index, node):
        cx,cy,kind=node
        # Every transport stop is a tray; scale pans have suspension cables.
        self._rect(canvas,cx-6,cy-1,13,7,4)
        self._line(canvas,cx-6,cy-1,cx-4,cy+4,2)
        self._line(canvas,cx-4,cy+4,cx+4,cy+4,2)
        self._line(canvas,cx+4,cy+4,cx+6,cy-1,2)
        if kind==1:
            # A solid pedestal is an ordinary parking place, not a forbidden sign.
            self._rect(canvas,cx-4,cy+5,9,2,3)
        elif kind==2:
            # Receiving socket has the outline of a unit weight, not a colored badge.
            self._outline(canvas,cx-5,cy-6,11,12,0)
            self._outline(canvas,cx-2,cy-8,5,3,0)
            self._rect(canvas,cx-3,cy-4,7,8,5)

    def _draw_scale_badges(self, canvas, node_index, node):
        # No membership badges: actual cables join the pan to its scale endpoint.
        return

    def _draw_weight(self, canvas, index, node):
        cx,cy=self.spec['nodes'][node][:2]
        mass=self.spec['weights'][index][0]
        # Mass is a stack of equal substantial units, not arbitrary body colors.
        for unit in range(mass):
            self._rect(canvas,cx-3,cy+1-unit*3,7,3,12)
            self._line(canvas,cx-2,cy+1-unit*3,cx+2,cy+1-unit*3,11)
        top=cy+1-(mass-1)*3
        self._outline(canvas,cx-1,top-2,3,3,2)

    def _draw_selection(self, canvas, node):
        cx,cy=self.spec['nodes'][node][:2]
        for dx in (-1,1):
            self._line(canvas,cx+dx*7,cy-5,cx+dx*7,cy+5,0)
            self._line(canvas,cx+dx*7,cy+5,cx+dx*5,cy+5,0)

    def _render_board(self):
        canvas=np.full((64,64),5,dtype=np.int32)
        # Suspension circuits are thin, colored and terminate at a real pan.
        # Transport rails are thick neutral tracks, so these are not extra routes.
        for index,scale in enumerate(self.spec['scales']):
            mx,my=scale[3],scale[4];theme=self._scale_color(index)
            for side,nodes in ((-1,scale[0]),(1,scale[1])):
                for node in nodes:
                    x,y,_=self.spec['nodes'][node]
                    left,right=self._balance_totals(index)
                    tilt=max(-2,min(2,left-right))
                    self._line(canvas,mx+side*5,my-side*tilt+3,x,y+4,theme)
        self._draw_edges(canvas)
        for index,node in enumerate(self.spec['nodes']):self._draw_node(canvas,index,node)
        for weight_index,node in enumerate(self.positions):self._draw_weight(canvas,weight_index,node)
        if self.selected is not None:self._draw_selection(canvas,self.positions[self.selected])
        for index,scale in enumerate(self.spec['scales']):self._draw_meter(canvas,index,scale)
        self._draw_lever(canvas)
        level=self.current_level;level.remove_all_sprites()
        level.add_sprite(Sprite(pixels=canvas,name='apparatus',x=0,y=0,layer=0))
