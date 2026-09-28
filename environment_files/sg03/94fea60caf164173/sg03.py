"""SG03: one impact travels through the facing edges of a sparse domino chain."""
from __future__ import annotations

import numpy as np
from arcengine import ARCBaseGame, Camera, GameAction, Level, Sprite

# Direction order is clockwise: east, south, west, north.
DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))
FIXED_LEVELS = (
    {"start": (1, 3), "goal": (5, 3),
     "pieces": ((2, 3, 0), (3, 3, 0), (4, 3, 0))},
    {"start": (1, 4), "goal": (5, 4),
     "pieces": ((2, 4, 0), (3, 4, 3), (4, 4, 0))},
    {"start": (1, 5), "goal": (5, 3),
     "pieces": ((2, 5, 0), (3, 5, 2), (3, 4, 3), (3, 3, 0), (4, 3, 0))},
    {"start": (1, 4), "goal": (6, 4),
     "pieces": ((2, 4, 0), (3, 4, 3), (3, 3, 3), (4, 3, 0),
                (4, 4, 0), (5, 4, 0), (3, 2, 2))},
    {"start": (1, 5), "goal": (6, 4),
     "pieces": ((2, 5, 0), (3, 5, 2), (3, 4, 3), (3, 3, 3),
                (3, 2, 0), (4, 2, 0), (5, 2, 0), (5, 3, 1), (5, 4, 0))},
    {"start": (1, 6), "goal": (6, 2),
     "pieces": ((2, 6, 0), (3, 6, 2), (3, 5, 3), (3, 4, 3),
                (4, 4, 0), (5, 4, 2), (5, 3, 3), (5, 2, 0))},
    {"start": (1, 6), "goal": (6, 1),
     "pieces": ((2, 6, 0), (3, 6, 2), (3, 5, 3), (3, 4, 0),
                (4, 4, 2), (4, 3, 0), (5, 3, 2), (5, 2, 0),
                (6, 2, 2))},
)


def _make_level(index, spec):
    return Level(
        sprites=[Sprite(pixels=np.zeros((64, 64), dtype=np.int64),
                        name="board", x=0, y=0, layer=0)],
        grid_size=(64, 64), data={"spec": spec}, name=str(index + 1),
    )


class Sg03(ARCBaseGame):
    def __init__(self, seed=0):
        self._spec = None
        self._dirs = {}
        self._fallen = set()
        self._history = []
        self._pending = None
        self._pressed = False
        levels = [_make_level(i, spec) for i, spec in enumerate(FIXED_LEVELS)]
        super().__init__(
            game_id="sg03-v1", levels=levels,
            camera=Camera(background=5, letter_box=5),
            available_actions=[5, 6, 7], seed=seed,
        )

    def on_set_level(self, level):
        self._spec = level.get_data("spec")
        self._dirs = {(x, y): direction for x, y, direction in self._spec["pieces"]}
        occupied = list(self._dirs) + [self._spec["start"], self._spec["goal"]]
        self._min_x = min(x for x, y in occupied)
        self._min_y = min(y for x, y in occupied)
        self._max_x = max(x for x, y in occupied)
        self._max_y = max(y for x, y in occupied)
        width = self._max_x - self._min_x + 1
        height = self._max_y - self._min_y + 1
        self._pitch = min(10, 56 // max(width, height))
        self._origin_x = (64 - width * self._pitch) // 2
        self._origin_y = (64 - height * self._pitch) // 2
        self._fallen = set()
        self._history = []
        self._pending = None
        self._pressed = False
        self._draw()

    def _snapshot(self):
        return (dict(self._dirs), set(self._fallen), self._pressed)

    def _restore(self, state):
        self._dirs, self._fallen, self._pressed = state
        self._pending = None
        self._draw()

    def _click_cell(self):
        data = self.action.data or {}
        x, y = data.get("x"), data.get("y")
        if type(x) is not int or type(y) is not int or not (0 <= x < 64 and 0 <= y < 64):
            return None
        bx = (x - self._origin_x) // self._pitch + self._min_x
        by = (y - self._origin_y) // self._pitch + self._min_y
        if not (self._min_x <= bx <= self._max_x and self._min_y <= by <= self._max_y):
            return None
        return (bx, by)

    def _trace(self):
        start = self._spec["start"]
        pos = (start[0] + 1, start[1])
        visited = set()
        order = []
        while len(order) <= len(self._dirs):
            if pos == self._spec["goal"]:
                return order, True
            if pos not in self._dirs or pos in visited:
                return order, False
            order.append(pos)
            visited.add(pos)
            dx, dy = DIRS[self._dirs[pos]]
            pos = (pos[0] + dx, pos[1] + dy)
        return order, False

    def _launch_or_reset(self):
        if self._fallen:
            self._history.append(self._snapshot())
            self._fallen = set()
            self._pressed = False
            self._draw()
            self.complete_action()
            return
        order, success = self._trace()
        if not order:
            self._draw()
            self.complete_action()
            return
        self._history.append(self._snapshot())
        self._pending = {"order": order, "success": success}
        self._pressed = True
        self._draw()
        # Another native step shows each domino falling along the path.

    def step(self):
        if self._pending is not None:
            pending = self._pending
            if pending["order"]:
                pos = pending["order"].pop(0)
                self._fallen.add(pos)
                self._draw()
                if pending["order"]:
                    return
            success = pending["success"]
            self._pending = None
            self._pressed = False
            if success:
                self.next_level()
            self.complete_action()
            return

        action = self.action.id
        if action == GameAction.RESET:
            self.on_set_level(self.current_level)
            self.complete_action()
            return
        if action == GameAction.ACTION7:
            if self._history:
                self._restore(self._history.pop())
            self.complete_action()
            return
        if action == GameAction.ACTION5:
            self._launch_or_reset()
            return
        if action == GameAction.ACTION6:
            cell = self._click_cell()
            if cell == self._spec["start"]:
                self._launch_or_reset()
                return
            if cell in self._dirs and not self._fallen:
                self._history.append(self._snapshot())
                self._dirs[cell] = (self._dirs[cell] + 1) % 4
                self._draw()
            self.complete_action()
            return
        self.complete_action()

    def _point(self, cell):
        return (self._origin_x + (cell[0] - self._min_x) * self._pitch,
                self._origin_y + (cell[1] - self._min_y) * self._pitch)

    def _attached_face(self, pixels, x, y, direction, thickness=2):
        p = self._pitch
        mid = p // 2
        if direction == 0:
            pixels[y + mid - thickness // 2:y + mid + 1,
                   x + p - 2:x + p + 2] = 11
        elif direction == 1:
            pixels[y + p - 2:y + p + 2,
                   x + mid - thickness // 2:x + mid + 1] = 11
        elif direction == 2:
            pixels[y + mid - thickness // 2:y + mid + 1,
                   x - 1:x + 3] = 11
        else:
            pixels[y - 1:y + 3,
                   x + mid - thickness // 2:x + mid + 1] = 11

    def _draw(self):
        pixels = np.full((64, 64), 5, dtype=np.int64)
        p = self._pitch
        mid = p // 2
        # The yellow contact face touches the next cell. The physical shape
        # changes from upright hollow tile to a low bar when it falls.
        for cell, direction in self._dirs.items():
            x, y = self._point(cell)
            if cell in self._fallen:
                pixels[y + mid - 1:y + mid + 2, x + mid - 1:x + mid + 2] = 2
                if direction == 0:
                    pixels[y + mid - 1:y + mid + 2, x + mid:x + p + 2] = 11
                elif direction == 1:
                    pixels[y + mid:y + p + 2, x + mid - 1:x + mid + 2] = 11
                elif direction == 2:
                    pixels[y + mid - 1:y + mid + 2, x - 1:x + mid + 1] = 11
                else:
                    pixels[y - 1:y + mid + 1, x + mid - 1:x + mid + 2] = 11
            else:
                pixels[y + 1:y + p, x + 1:x + p] = 2
                pixels[y + 2:y + p - 1, x + 2:x + p - 1] = 5
                self._attached_face(pixels, x, y, direction)
        x, y = self._point(self._spec["start"])
        pixels[y + 1:y + p, x + 1:x + p] = 10
        pixels[y + 2:y + p - 1, x + 2:x + p - 1] = 5
        pixels[y + mid - 1:y + mid + 2, x + p - 2:x + p + 2] = 10
        if self._pressed:
            pixels[y + 2:y + p - 1, x + 2:x + mid + 1] = 10
        x, y = self._point(self._spec["goal"])
        pixels[y + 1:y + p, x + 1:x + p] = 11
        pixels[y + 2:y + p - 1, x + 2:x + p - 1] = 5
        level = self.current_level
        level.remove_all_sprites()
        level.add_sprite(Sprite(pixels=pixels, name="board", x=0, y=0, layer=0))
