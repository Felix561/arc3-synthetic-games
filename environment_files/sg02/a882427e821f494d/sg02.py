from arcengine import ARCBaseGame, Camera, Level, Sprite, GameAction
import numpy as np

CELL = 8
BOARD = 8
SIZE = CELL * BOARD
EMPTY = 0
BLOCK = 8
PATH_BLANK = 9
EDGE = 10
SOURCE_EDGE = 11
SINK_BODY = 12
MIXER_BODY = 13
CURSOR = 14
HOT = 15

FIXED_LEVELS = (
    {
        'cursor': (1, 3),
        'sources': (((1, 3), 1),),
        'sinks': (((3, 3), 1),),
        'paths': ((2, 3),),
        'blockers': (),
        'mixers': (),
        'cycle': (1, 2, 3, 4, 5, 6),
        'initial': (),
    },
    {
        # L2 continues the L1 relay: one new cursor move extends the line.
        'cursor': (1, 4),
        'sources': (((1, 4), 2),),
        'sinks': (((4, 4), 2),),
        'paths': ((2, 4), (3, 4)),
        'blockers': (),
        'mixers': (),
        'cycle': (1, 2, 3, 4, 5, 6),
        'initial': (),
    },
    {
        'cursor': (1, 1),
        'sources': (((1, 1), 1), ((1, 6), 2)),
        'sinks': (((6, 1), 1), ((6, 6), 2)),
        'paths': ((2, 1), (3, 1), (4, 1), (5, 1), (2, 6), (3, 6), (4, 6), (5, 6)),
        'blockers': ((3, 3), (4, 3), (3, 4), (4, 4), (2, 3), (5, 4)),
        'mixers': (),
        'cycle': (1, 2, 3, 4, 5, 6),
        'initial': (),
    },
    {
        'cursor': (1, 3),
        'sources': (((1, 3), 1),),
        'sinks': (((6, 3), 3),),
        'paths': ((3, 3), (4, 3), (5, 3)),
        'blockers': ((2, 2), (2, 4), (4, 1), (4, 5)),
        'mixers': ((2, 3),),
        'cycle': (1, 3, 2, 4, 5, 6),
        'initial': (),
    },
    {
        'cursor': (1, 2),
        'sources': (((1, 2), 2),),
        'sinks': (((6, 2), 2), ((6, 4), 2)),
        'paths': ((2, 2), (3, 2), (4, 2), (5, 2), (5, 3), (5, 4)),
        'blockers': ((3, 3), (4, 3), (2, 4), (4, 5)),
        'mixers': (),
        'cycle': (1, 2, 3, 4, 5, 6),
        'initial': ((2, 2, 2), (3, 2, 1), (4, 2, 2), (5, 2, 2), (5, 3, 2), (5, 4, 2)),
    },
    {
        'cursor': (1, 5),
        'sources': (((1, 5), 4),),
        'sinks': (((6, 1), 4),),
        'paths': ((2, 5), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (5, 2), (5, 1)),
        'blockers': ((1, 4), (3, 5), (3, 3), (5, 4), (4, 1), (6, 2), (1, 3), (5, 3)),
        'mixers': (),
        'cycle': (1, 2, 3, 4, 5, 6),
        'initial': (),
    },
    {
        'cursor': (1, 3),
        'sources': (((1, 3), 5), ((1, 6), 1)),
        'sinks': (((6, 2), 5), ((6, 4), 5), ((6, 6), 6)),
        'paths': ((2, 3), (3, 3), (4, 3), (5, 3), (5, 2), (5, 4), (3, 6), (4, 6), (5, 6)),
        'blockers': ((3, 1), (4, 1), (2, 5), (3, 5), (4, 5), (6, 3), (6, 5), (0, 6), (2, 2), (2, 4), (7, 3)),
        'mixers': ((2, 6),),
        'cycle': (1, 6, 2, 3, 4, 5),
        'initial': (),
    },
)


def _blank_pixels():
    return np.zeros((SIZE, SIZE), dtype=int)


def _make_level(index, spec):
    return Level(
        sprites=[Sprite(pixels=_blank_pixels(), name='board', x=0, y=0, layer=0)],
        grid_size=(SIZE, SIZE),
        data={'spec': spec},
        name=str(index),
    )


class Sg02(ARCBaseGame):
    def __init__(self, seed=0):
        self._spec = None
        self._cursor = (0, 0)
        self._held = 0
        self._paths = set()
        self._blockers = set()
        self._sources = {}
        self._sinks = {}
        self._mixers = set()
        self._cycle = (1, 2, 3, 4, 5, 6)
        self._painted = {}
        self._mixer_outputs = {}
        self._lit = set()
        self._hot = set()
        self._undo = []
        levels = [_make_level(i, spec) for i, spec in enumerate(FIXED_LEVELS)]
        super().__init__(
            game_id='sg02-v1',
            levels=levels,
            camera=Camera(background=0, letter_box=0),
            available_actions=[1, 2, 3, 4, 5, 6, 7],
            seed=seed,
        )

    def on_set_level(self, level):
        self._load_spec(level.get_data('spec'))

    def _load_spec(self, spec):
        self._spec = spec
        self._cursor = tuple(spec['cursor'])
        self._held = 0
        self._paths = {tuple(pos) for pos in spec.get('paths', ())}
        self._blockers = {tuple(pos) for pos in spec.get('blockers', ())}
        self._sources = {tuple(pos): color for pos, color in spec.get('sources', ())}
        self._sinks = {tuple(pos): color for pos, color in spec.get('sinks', ())}
        self._mixers = {tuple(pos) for pos in spec.get('mixers', ())}
        self._cycle = tuple(spec.get('cycle', (1, 2, 3, 4, 5, 6)))
        self._painted = {(x, y): color for x, y, color in spec.get('initial', ())}
        self._mixer_outputs = {pos: 0 for pos in self._mixers}
        self._undo = []
        self._update_lit()
        self._redraw()

    def step(self):
        action_id = self._action_number()
        if action_id == -1:
            self.complete_action()
            return
        if action_id == 7:
            self._undo_one()
            self.complete_action()
            return
        self._push_undo()
        if action_id == 1:
            self._move(0, -1)
        elif action_id == 2:
            self._move(0, 1)
        elif action_id == 3:
            self._move(-1, 0)
        elif action_id == 4:
            self._move(1, 0)
        elif action_id == 5:
            self._interact()
        elif action_id == 6:
            self._paint_click()
        self._update_lit()
        self._redraw()
        if self._all_sinks_lit():
            self.next_level()
        self.complete_action()

    def _action_number(self):
        raw = self.action.id
        value = getattr(raw, 'value', raw)
        parsed = self._parse_action_value(value)
        if parsed is not None:
            return parsed
        return self._parse_action_value(getattr(raw, 'name', raw))

    def _parse_action_value(self, value):
        if isinstance(value, str):
            text = value.upper()
            if text == 'RESET':
                return -1
            if text.startswith('ACTION'):
                try:
                    return int(text[6:])
                except ValueError:
                    return None
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def _push_undo(self):
        self._undo.append((self._cursor, self._held, dict(self._painted), dict(self._mixer_outputs)))
        if len(self._undo) > 64:
            self._undo.pop(0)

    def _undo_one(self):
        if not self._undo:
            self._redraw()
            return
        cursor, held, painted, mixer_outputs = self._undo.pop()
        self._cursor = cursor
        self._held = held
        self._painted = painted
        self._mixer_outputs = mixer_outputs
        self._update_lit()
        self._redraw()

    def _move(self, dx, dy):
        x, y = self._cursor
        dest = (x + dx, y + dy)
        if 0 <= dest[0] < BOARD and 0 <= dest[1] < BOARD and dest not in self._blockers:
            self._cursor = dest

    def _interact(self):
        pos = self._cursor
        if pos in self._sources:
            color = self._sources[pos]
            self._held = 0 if self._held == color else color
        elif pos in self._mixers and self._held:
            self._held = self._next_cycle_color(self._held)
            self._mixer_outputs[pos] = self._held
        elif pos in self._sinks:
            required = self._sinks[pos]
            if pos in self._lit and self._held == required:
                self._held = 0
            elif pos in self._lit and self._held == 0:
                self._held = required

    def _next_cycle_color(self, color):
        if not self._cycle:
            return color
        if color not in self._cycle:
            return self._cycle[0]
        index = self._cycle.index(color)
        return self._cycle[(index + 1) % len(self._cycle)]

    def _paint_click(self):
        data = getattr(self.action, 'data', None) or {}
        try:
            cell = (int(data.get('x', -100)) // CELL, int(data.get('y', -100)) // CELL)
        except (TypeError, ValueError):
            return
        if not (0 <= cell[0] < BOARD and 0 <= cell[1] < BOARD):
            return
        # Clicking the source underneath the cursor is the same physical pickup
        # as ACTION5. Remote sources remain non-interactive; the cursor never jumps.
        if cell == self._cursor and cell in self._sources:
            self._interact()
            return
        if cell not in self._paths:
            return
        if abs(cell[0] - self._cursor[0]) + abs(cell[1] - self._cursor[1]) != 1:
            return
        if self._held:
            self._painted[cell] = self._held
        else:
            self._painted.pop(cell, None)

    def _neighbors(self, pos):
        x, y = pos
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nxt = (x + dx, y + dy)
            if 0 <= nxt[0] < BOARD and 0 <= nxt[1] < BOARD:
                yield nxt

    def _update_lit(self):
        colors = set(self._sinks.values()) | set(self._sources.values()) | {c for c in self._mixer_outputs.values() if c}
        reachable_by_color = {color: self._reachable_cells(color) for color in colors}
        self._hot = set()
        for cells in reachable_by_color.values():
            self._hot.update(cells)
        lit = set()
        for sink, required in self._sinks.items():
            reachable = reachable_by_color.get(required, set())
            if any(neighbor in reachable for neighbor in self._neighbors(sink)):
                lit.add(sink)
        self._lit = lit

    def _reachable_cells(self, color):
        starts = []
        for pos, source_color in self._sources.items():
            if source_color == color:
                starts.append(pos)
        for pos, output_color in self._mixer_outputs.items():
            if output_color == color:
                starts.append(pos)
        seen = set()
        frontier = []
        for start in starts:
            for neighbor in self._neighbors(start):
                if neighbor in self._paths and self._painted.get(neighbor) == color and neighbor not in seen:
                    seen.add(neighbor)
                    frontier.append(neighbor)
        index = 0
        while index < len(frontier):
            pos = frontier[index]
            index += 1
            for neighbor in self._neighbors(pos):
                if neighbor in self._paths and self._painted.get(neighbor) == color and neighbor not in seen:
                    seen.add(neighbor)
                    frontier.append(neighbor)
        return seen

    def _all_sinks_lit(self):
        return bool(self._sinks) and len(self._lit) == len(self._sinks)

    def _redraw(self):
        pixels = self._render_pixels()
        level = self.current_level
        level.remove_all_sprites()
        level.add_sprite(Sprite(pixels=pixels, name='board', x=0, y=0, layer=0))

    def _render_pixels(self):
        pixels=np.full((64,64),5,dtype=np.int64)
        palette={0:4,1:10,2:12,3:6,4:14,5:15,6:11}
        def color(v):return palette.get(v,v)
        active=set(self._paths)|set(self._sources)|set(self._sinks)|set(self._mixers)
        for px,py in active:
            for qx,qy in self._neighbors((px,py)):
                if (qx,qy) in active:
                    pixels[min(py,qy)*8+3:max(py,qy)*8+5,min(px,qx)*8+3:max(px,qx)*8+5]=3
        for pos in self._paths:
            x,y=pos[0]*8,pos[1]*8;v=self._painted.get(pos,0)
            pixels[y+1:y+7,x+1:x+7]=color(v)
            if pos in self._hot:pixels[y+3:y+5,x:x+8]=color(v)
            if not v:pixels[y+3:y+5,x+3:x+5]=5
        for pos in self._blockers:
            x,y=pos[0]*8,pos[1]*8;pixels[y+1:y+7,x+1:x+7]=2
        for pos,v in self._sources.items():
            x,y=pos[0]*8,pos[1]*8;pixels[y+1:y+7,x+1:x+7]=color(v);pixels[y+2:y+6,x+2:x+6]=5;pixels[y+3:y+5,x+3:x+5]=color(v)
        for pos,v in self._sinks.items():
            x,y=pos[0]*8,pos[1]*8;pixels[y:y+8,x:x+8]=color(v);pixels[y+1:y+7,x+1:x+7]=5
            if pos in self._lit:pixels[y+2:y+6,x+2:x+6]=color(v)
        for pos in self._mixers:
            x,y=pos[0]*8,pos[1]*8
            for k,v in enumerate(self._cycle[:3]):pixels[y+1+k*2:y+3+k*2,x+2:x+6]=color(v)
        x,y=self._cursor[0]*8,self._cursor[1]*8
        for yy,xx in ((y,x),(y,x+7),(y+7,x),(y+7,x+7)):pixels[yy,xx]=0
        if self._held:
            pixels[y+2:y+6,x+2:x+6]=color(self._held)
        else:
            pixels[y+3:y+5,x+3:x+5]=0
        return pixels

    def _draw_cell(self, pixels, pos, fill, border):
        x, y = pos[0] * CELL, pos[1] * CELL
        pixels[y:y + CELL, x:x + CELL] = border
        pixels[y + 1:y + CELL - 1, x + 1:x + CELL - 1] = fill

    def _draw_center(self, pixels, pos, color):
        x, y = pos[0] * CELL, pos[1] * CELL
        pixels[y + 3:y + 5, x + 3:x + 5] = color

    def _draw_cycle_ticks(self, pixels, pos):
        x, y = pos[0] * CELL, pos[1] * CELL
        for i, color in enumerate(self._cycle[:4]):
            pixels[y + 2:y + 6, x + 2 + i:x + 3 + i] = color

    def _draw_blocker(self, pixels, pos):
        self._draw_cell(pixels, pos, BLOCK, BLOCK)
        x, y = pos[0] * CELL, pos[1] * CELL
        for i in range(CELL):
            pixels[y + i, x + i] = EDGE
            pixels[y + i, x + CELL - 1 - i] = EDGE

    def _draw_cursor(self, pixels):
        x, y = self._cursor[0] * CELL, self._cursor[1] * CELL
        pixels[y, x:x + CELL] = CURSOR
        pixels[y + CELL - 1, x:x + CELL] = CURSOR
        pixels[y:y + CELL, x] = CURSOR
        pixels[y:y + CELL, x + CELL - 1] = CURSOR
        if self._held:
            pixels[y + 2:y + 6, x + 2:x + 6] = self._held
        else:
            pixels[y + 3:y + 5, x + 3:x + 5] = CURSOR
