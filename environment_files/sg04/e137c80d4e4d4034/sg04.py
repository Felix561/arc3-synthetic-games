import numpy as np
from collections import deque
from arcengine import ARCBaseGame, Camera, Level, Sprite, GameAction

FIXED_LEVELS = [
    {'emitters': [[0, 3, 1, 0]], 'receivers': [[3, 0, 0]], 'forbidden': [[3, 7]], 'mirrors': [[3, 3, 1]], 'splitters': [], 'absorbers': [], 'relays': [], 'relay_links': []},
    {'emitters': [[0, 6, 1, 0]], 'receivers': [[6, 2, 0]], 'forbidden': [[2, 7], [0, 2]], 'mirrors': [[2, 6, 1], [2, 2, 1]], 'splitters': [], 'absorbers': [[7, 2]], 'relays': [], 'relay_links': []},
    {'emitters': [[0, 3, 1, 0]], 'receivers': [[3, 7, 1]], 'forbidden': [[3, 0]], 'mirrors': [[3, 3, 0]], 'splitters': [], 'absorbers': [], 'relays': [], 'relay_links': []},
    {'emitters': [[0, 3, 1, 0]], 'receivers': [[7, 3, 0], [3, 7, 1]], 'forbidden': [[3, 0]], 'mirrors': [], 'splitters': [[3, 3, 0]], 'absorbers': [], 'relays': [], 'relay_links': []},
    {'emitters': [[0, 6, 1, 0], [7, 5, 3, 1]], 'receivers': [[3, 2, 0], [6, 2, 1], [6, 6, 1], [4, 1, 0]], 'forbidden': [[3, 7], [4, 7]], 'mirrors': [[3, 6, 1], [4, 5, 1]], 'splitters': [], 'absorbers': [[4, 0], [6, 7]], 'relays': [[3, 2, 0, 1, 0], [6, 2, 1, 2, 0]], 'relay_links': [[0, 1]]},
    {'emitters': [[0, 3, 1, 0]], 'receivers': [[7, 3, 0], [5, 6, 1], [5, 2, 0], [1, 2, 0]], 'forbidden': [[2, 0], [0, 6]], 'mirrors': [[2, 6, 0]], 'splitters': [[2, 3, 0]], 'absorbers': [[0, 2]], 'relays': [[5, 6, 1, 3, 0], [5, 2, 0, 3, 1]], 'relay_links': [[0, 1]]},
    {'emitters': [[0, 4, 1, 0], [7, 7, 3, 0], [7, 1, 3, 1]], 'receivers': [[1, 1, 0], [4, 1, 0], [6, 5, 0], [6, 6, 0], [3, 5, 1], [3, 0, 0]], 'forbidden': [[1, 7], [1, 0], [6, 0], [7, 5], [3, 7]], 'mirrors': [[1, 4, 1], [6, 1, 1], [5, 7, 0], [5, 5, 0]], 'splitters': [], 'absorbers': [[5, 1]], 'relays': [[1, 1, 0, 0, 0], [6, 5, 0, 2, 0], [3, 5, 1, 2, 0]], 'relay_links': [[0, 2], [1, 2]]}
]


class Sg04(ARCBaseGame):
    DX = (0, 1, 0, -1)
    DY = (-1, 0, 1, 0)
    SLASH = (1, 0, 3, 2)
    BACKSLASH = (3, 2, 1, 0)

    def __init__(self, seed=0):
        self.cfg = None
        self._selected = None
        self._undo_stack = []
        self._mirrors = []
        self._splitters = []
        self._relays = []
        self._relay_links = []
        self._beams = {}
        self._hits = set()
        self._relay_lit = set()
        levels = self._build_levels()
        super().__init__(game_id='sg04-v1', levels=levels, camera=Camera(background=0, letter_box=0), available_actions=[4, 5, 6, 7], seed=seed)

    def _build_levels(self):
        levels = []
        for index, cfg in enumerate(FIXED_LEVELS):
            blank = Sprite(pixels=np.zeros((64, 64), dtype=np.int64), name='board', x=0, y=0, layer=0)
            levels.append(Level(sprites=[blank], grid_size=(64, 64), data={'cfg': cfg, 'index': index}, name='Optical field %d' % (index + 1)))
        return levels

    def on_set_level(self, level):
        self.cfg = level.get_data('cfg')
        self._mirrors = [item[:] for item in self.cfg['mirrors']]
        self._splitters = [item[:] for item in self.cfg['splitters']]
        self._relays = [item[:] for item in self.cfg['relays']]
        self._relay_links = [item[:] for item in self.cfg['relay_links']]
        self._selected = None
        self._undo_stack = []
        self._recompute()
        self._paint()

    def _remember(self):
        self._undo_stack.append((
            [item[:] for item in self._mirrors],
            [item[:] for item in self._splitters],
            [item[:] for item in self._relays],
            self._selected
        ))

    def _restore(self):
        if self._undo_stack:
            mirrors, splitters, relays, selected = self._undo_stack.pop()
            self._mirrors = [item[:] for item in mirrors]
            self._splitters = [item[:] for item in splitters]
            self._relays = [item[:] for item in relays]
            self._selected = selected
        self._recompute()
        self._paint()

    def _select_at(self, px, py):
        if px is None or py is None or px < 0 or py < 0 or px > 63 or py > 63:
            self._selected = None
            return
        cx, cy = px // 8, py // 8
        for index, mirror in enumerate(self._mirrors):
            if mirror[0] == cx and mirror[1] == cy:
                self._selected = ('mirror', index)
                return
        for index, splitter in enumerate(self._splitters):
            if splitter[0] == cx and splitter[1] == cy:
                self._selected = ('splitter', index)
                return
        for index, relay in enumerate(self._relays):
            if relay[0] == cx and relay[1] == cy:
                self._selected = ('relay', index)
                return
        self._selected = None

    def _adjust_clockwise(self):
        if self._selected is None:
            return
        kind, index = self._selected
        if kind == 'mirror':
            self._mirrors[index][2] = (self._mirrors[index][2] + 1) % 4
        elif kind == 'relay':
            self._relays[index][3] = (self._relays[index][3] + 1) % 4

    def _adjust_counterclockwise_or_phase(self):
        if self._selected is None:
            return
        kind, index = self._selected
        if kind == 'mirror':
            self._mirrors[index][2] = (self._mirrors[index][2] - 1) % 4
        elif kind == 'splitter':
            self._splitters[index][2] ^= 1
        elif kind == 'relay':
            self._relays[index][4] ^= 1

    def step(self):
        action_id = self.action.id
        if action_id == GameAction.RESET:
            self.complete_action()
            return
        if action_id == GameAction.ACTION7:
            self._restore()
            self.complete_action()
            return
        if action_id not in (GameAction.ACTION4, GameAction.ACTION5, GameAction.ACTION6):
            self.complete_action()
            return
        self._remember()
        if action_id == GameAction.ACTION6:
            data = self.action.data or {}
            self._select_at(data.get('x', -1), data.get('y', -1))
        elif action_id == GameAction.ACTION4:
            self._adjust_clockwise()
        else:
            self._adjust_counterclockwise_or_phase()
        self._recompute()
        self._paint()
        if self._goal_reached():
            self.next_level()
        self.complete_action()

    def _recompute(self):
        mirrors = {(item[0], item[1]): item[2] for item in self._mirrors}
        splitters = {(item[0], item[1]): item[2] for item in self._splitters}
        absorbers = {(item[0], item[1]) for item in self.cfg['absorbers']}
        relay_at = {(item[0], item[1]): index for index, item in enumerate(self._relays)}
        requirements = {}
        for source, target in self._relay_links:
            requirements.setdefault(target, []).append(source)
        queue = deque()
        for ex, ey, direction, polarity in self.cfg['emitters']:
            queue.append((ex + self.DX[direction], ey + self.DY[direction], direction, polarity))
        seen = set()
        beam_map = {}
        hits = set()
        pending_relays = set()
        active_relays = set()
        while True:
            while queue:
                x, y, direction, polarity = queue.popleft()
                if x < 0 or y < 0 or x > 7 or y > 7:
                    continue
                state = (x, y, direction, polarity)
                if state in seen:
                    continue
                seen.add(state)
                beam_map.setdefault((x, y), set()).add((direction, polarity))
                hits.add((x, y, polarity))
                if (x, y) in absorbers:
                    continue
                if (x, y) in relay_at:
                    relay_index = relay_at[(x, y)]
                    relay = self._relays[relay_index]
                    if polarity == relay[2]:
                        pending_relays.add(relay_index)
                    continue
                if (x, y) in mirrors:
                    orientation = mirrors[(x, y)]
                    turned = self.SLASH[direction] if orientation % 2 == 0 else self.BACKSLASH[direction]
                    output_polarity = polarity ^ (orientation // 2)
                    queue.append((x + self.DX[turned], y + self.DY[turned], turned, output_polarity))
                    continue
                if (x, y) in splitters:
                    phase = splitters[(x, y)]
                    side = (direction - 1) % 4 if phase == 0 else (direction + 1) % 4
                    queue.append((x + self.DX[direction], y + self.DY[direction], direction, polarity))
                    queue.append((x + self.DX[side], y + self.DY[side], side, polarity ^ 1))
                    continue
                queue.append((x + self.DX[direction], y + self.DY[direction], direction, polarity))
            activated = False
            for relay_index in sorted(pending_relays):
                if relay_index in active_relays:
                    continue
                needed = requirements.get(relay_index, [])
                if not all(source in active_relays for source in needed):
                    continue
                relay = self._relays[relay_index]
                active_relays.add(relay_index)
                direction = relay[3]
                output_polarity = relay[2] ^ relay[4]
                queue.append((relay[0] + self.DX[direction], relay[1] + self.DY[direction], direction, output_polarity))
                activated = True
            if not activated:
                break
        self._beams = beam_map
        self._hits = hits
        self._relay_lit = {(self._relays[index][0], self._relays[index][1]) for index in active_relays}

    def _goal_reached(self):
        for x, y, polarity in self.cfg['receivers']:
            if (x, y, polarity) not in self._hits:
                return False
        for x, y in self.cfg['forbidden']:
            if any(hit_x == x and hit_y == y for hit_x, hit_y, _ in self._hits):
                return False
        return True

    def _cell_box(self, canvas, x, y, color):
        x0, y0 = x * 8, y * 8
        canvas[y0 + 1:y0 + 7, x0:x0 + 8] = color
        canvas[y0 + 1, x0 + 1:x0 + 7] = 3
        canvas[y0 + 6, x0 + 1:x0 + 7] = 3
        canvas[y0 + 1:y0 + 7, x0 + 1] = 3
        canvas[y0 + 1:y0 + 7, x0 + 6] = 3

    def _draw_emitter(self, canvas, item):
        x, y, direction, polarity = item
        self._cell_box(canvas, x, y, 2)
        x0, y0 = x * 8, y * 8
        arrows = (
            [(3, 1), (2, 2), (3, 2), (4, 2), (3, 3), (3, 4)],
            [(6, 3), (5, 2), (5, 3), (5, 4), (3, 3), (4, 3)],
            [(3, 6), (2, 5), (3, 5), (4, 5), (3, 3), (3, 4)],
            [(1, 3), (2, 2), (2, 3), (2, 4), (3, 3), (4, 3)]
        )
        color = 10 if polarity == 0 else 14
        for ax, ay in arrows[direction]:
            canvas[y0 + ay, x0 + ax] = color
        if polarity == 0:
            canvas[y0 + 3, x0 + 3] = color
        else:
            canvas[y0 + 3, x0 + 2:x0 + 5] = color

    def _draw_receiver(self, canvas, x, y, polarity, forbidden=False, combined=False):
        x0, y0 = x * 8, y * 8
        if forbidden:
            lit = any(hx == x and hy == y for hx, hy, _ in self._hits)
            color = 15 if lit else 8
            for offset in range(1, 7):
                canvas[y0 + offset, x0 + offset] = color
                canvas[y0 + offset, x0 + 7 - offset] = color
            canvas[y0 + 3:y0 + 5, x0 + 3:x0 + 5] = 2
            return
        lit = (x, y, polarity) in self._hits
        color = (10 if polarity == 0 else 14) if lit else 5
        if combined:
            points = [(2, 1), (1, 2), (2, 2), (3, 2), (2, 3)]
            for lx, ly in points:
                canvas[y0 + ly, x0 + lx] = color
            center = (10 if polarity == 0 else 14) if lit else (6 if polarity == 0 else 9)
            canvas[y0 + 2, x0 + 2] = center
            return
        for ly in range(1, 7):
            for lx in range(1, 7):
                distance = abs(lx - 3) + abs(ly - 3)
                if distance in (2, 3):
                    canvas[y0 + ly, x0 + lx] = color
        center = (10 if polarity == 0 else 14) if lit else (6 if polarity == 0 else 9)
        if polarity == 0:
            canvas[y0 + 3, x0 + 3] = center
        else:
            canvas[y0 + 3, x0 + 2:x0 + 5] = center

    def _draw_mirror(self, canvas, item, selected):
        x, y, orientation = item
        self._cell_box(canvas, x, y, 2)
        x0, y0 = x * 8, y * 8
        for ly in range(1, 7):
            for lx in range(1, 7):
                distance = abs(lx + ly - 7) if orientation % 2 == 0 else abs(lx - ly)
                if distance <= 1:
                    canvas[y0 + ly, x0 + lx] = 9
        phase_color = 10 if orientation // 2 == 0 else 14
        if orientation // 2 == 0:
            canvas[y0 + 3, x0 + 3] = phase_color
        else:
            canvas[y0 + 3, x0 + 2:x0 + 5] = phase_color
        if selected:
            canvas[y0 + 1, x0 + 1:x0 + 7] = 15
            canvas[y0 + 6, x0 + 1:x0 + 7] = 15
            canvas[y0 + 1:y0 + 7, x0 + 1] = 15
            canvas[y0 + 1:y0 + 7, x0 + 6] = 15

    def _draw_splitter(self, canvas, item, selected):
        x, y, phase = item
        self._cell_box(canvas, x, y, 2)
        x0, y0 = x * 8, y * 8
        for ly in range(1, 7):
            for lx in range(1, 7):
                if abs(lx - 3) + abs(ly - 3) <= 3:
                    canvas[y0 + ly, x0 + lx] = 12
        marker_points = [(3, 2), (2, 3), (3, 3), (4, 3), (3, 4)] if phase == 0 else [(2, 2), (3, 2), (4, 2), (4, 3), (4, 4)]
        marker_color = 10 if phase == 0 else 14
        for lx, ly in marker_points:
            canvas[y0 + ly, x0 + lx] = marker_color
        if selected:
            canvas[y0 + 1, x0 + 1:x0 + 7] = 15
            canvas[y0 + 6, x0 + 1:x0 + 7] = 15
            canvas[y0 + 1:y0 + 7, x0 + 1] = 15
            canvas[y0 + 1:y0 + 7, x0 + 6] = 15

    def _draw_relay(self, canvas, item, selected, active):
        x, y, input_polarity, output_direction, flip = item
        x0, y0 = x * 8, y * 8
        self._cell_box(canvas, x, y, 2)
        input_color = 10 if input_polarity == 0 else 14
        for ly in range(1, 7):
            for lx in range(1, 7):
                distance = abs(lx - 3) + abs(ly - 3)
                if distance == 2 or (input_polarity == 1 and distance == 3):
                    canvas[y0 + ly, x0 + lx] = input_color
        center = 15 if active else 5
        canvas[y0 + 3:y0 + 5, x0 + 3:x0 + 5] = center
        output_polarity = input_polarity ^ flip
        output_color = 10 if output_polarity == 0 else 14
        if output_direction == 0:
            canvas[y0 + 1:y0 + 3, x0 + 3:x0 + 5] = output_color
        elif output_direction == 1:
            canvas[y0 + 3:y0 + 5, x0 + 4:x0 + 6] = output_color
        elif output_direction == 2:
            canvas[y0 + 4:y0 + 6, x0 + 3:x0 + 5] = output_color
        else:
            canvas[y0 + 3:y0 + 5, x0 + 1:x0 + 3] = output_color
        if flip == 0:
            canvas[y0 + 5, x0 + 2] = output_color
        else:
            canvas[y0 + 5, x0 + 1:x0 + 4] = output_color
        if selected:
            canvas[y0 + 1, x0 + 1:x0 + 7] = 15
            canvas[y0 + 6, x0 + 1:x0 + 7] = 15
            canvas[y0 + 1:y0 + 7, x0 + 1] = 15
            canvas[y0 + 1:y0 + 7, x0 + 6] = 15

    def _draw_absorber(self, canvas, x, y):
        x0, y0 = x * 8, y * 8
        canvas[y0 + 1:y0 + 7, x0 + 1:x0 + 7] = 8
        canvas[y0 + 2:y0 + 6, x0 + 2:x0 + 6] = 2
        canvas[y0 + 3:y0 + 5, x0 + 3:x0 + 5] = 8

    def _draw_relay_links(self, canvas):
        for source, target in self._relay_links:
            first = self._relays[source]
            second = self._relays[target]
            x1, y1 = first[0], first[1]
            x2, y2 = second[0], second[1]
            xstep = 1 if x2 >= x1 else -1
            ystep = 1 if y2 >= y1 else -1
            for cx in range(x1, x2 + xstep, xstep):
                canvas[y1 * 8 + 4, cx * 8 + 4] = 6
            for cy in range(y1, y2 + ystep, ystep):
                canvas[cy * 8 + 4, x2 * 8 + 4] = 6

    def _paint(self):
        canvas = np.full((64, 64), 5, dtype=np.int64)
        self._draw_relay_links(canvas)
        for (x, y), states in sorted(self._beams.items()):
            x0, y0 = x * 8, y * 8
            for direction, polarity in sorted(states):
                color = 10 if polarity == 0 else 14
                if direction in (1, 3):
                    canvas[y0 + 3:y0 + 5, x0:x0 + 8] = color
                else:
                    canvas[y0:y0 + 8, x0 + 3:x0 + 5] = color
            if len({polarity for _, polarity in states}) > 1 or len(states) > 1:
                canvas[y0 + 3:y0 + 5, x0 + 3:x0 + 5] = 15
        for item in self.cfg['emitters']:
            self._draw_emitter(canvas, item)
        for index, item in enumerate(self._mirrors):
            self._draw_mirror(canvas, item, self._selected == ('mirror', index))
        for index, item in enumerate(self._splitters):
            self._draw_splitter(canvas, item, self._selected == ('splitter', index))
        for index, item in enumerate(self._relays):
            self._draw_relay(canvas, item, self._selected == ('relay', index), (item[0], item[1]) in self._relay_lit)
        for x, y in self.cfg['absorbers']:
            self._draw_absorber(canvas, x, y)
        relay_cells = {(item[0], item[1]) for item in self._relays}
        for x, y, polarity in self.cfg['receivers']:
            self._draw_receiver(canvas, x, y, polarity, False, (x, y) in relay_cells)
        for x, y in self.cfg['forbidden']:
            self._draw_receiver(canvas, x, y, 0, True)
        self.current_level.remove_all_sprites()
        self.current_level.add_sprite(Sprite(pixels=canvas, name='board', x=0, y=0, layer=0))

    def _draw_mirror(self, canvas, item, selected):
        x,y,orientation=item;x*=8;y*=8
        canvas[y+1:y+7,x+1:x+7]=4
        col=10 if orientation//2==0 else 14
        for k in range(1,7):
            xx=7-k if orientation%2==0 else k
            canvas[y+k,x+xx]=col
            if xx<6:canvas[y+k,x+xx+1]=col
        if selected:canvas[y,x:x+8]=0

    def _draw_receiver(self, canvas, x, y, polarity, forbidden=False, combined=False):
        x*=8;y*=8
        if forbidden:
            canvas[y+1:y+7,x+1:x+7]=8
            canvas[y+2:y+6,x+2:x+6]=5
            return
        col=10 if polarity==0 else 14
        if combined:
            canvas[y,x:x+8]=col
            canvas[y,x+3:x+5]=col if (x//8,y//8,polarity) in self._hits else 5
            return
        canvas[y+1:y+7,x+1:x+7]=col
        canvas[y+2:y+6,x+2:x+6]=col if (x//8,y//8,polarity) in self._hits else 5

    def _draw_splitter(self, canvas, item, selected):
        x,y,phase=item;x*=8;y*=8;col=10 if phase==0 else 14
        canvas[y+1:y+7,x+1:x+7]=4
        canvas[y+3:y+5,x+1:x+7]=col;canvas[y+1:y+7,x+3:x+5]=col
        if selected:canvas[y,x:x+8]=0

    def _draw_relay(self, canvas, item, selected, active):
        x,y,polarity,direction,flip=item;x*=8;y*=8
        col=10 if polarity==0 else 14;out=10 if polarity^flip==0 else 14
        canvas[y+1:y+7,x+1:x+7]=col;canvas[y+2:y+6,x+2:x+6]=5
        canvas[y+3:y+5,x+3:x+5]=col if active else 4
        dx,dy=((0,-1),(1,0),(0,1),(-1,0))[direction]
        for k in (2,3):canvas[y+3+dy*k,x+3+dx*k]=out
        canvas[y+3+dy*2+dx,x+3+dx*2+dy]=out
        canvas[y+3+dy*2-dx,x+3+dx*2-dy]=out
        if selected:canvas[y,x:x+8]=0
