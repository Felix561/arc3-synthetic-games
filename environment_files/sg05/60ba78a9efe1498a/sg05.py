"""SG05: water adjacent sprouts until each flower fills its own petals."""
from __future__ import annotations

import numpy as np
from arcengine import ARCBaseGame, Camera, GameAction, Level, Sprite

MAX_PITCH = 12
FIXED_LEVELS = (
    {"wells": ((2, 2),), "plants": ((2, 3, 1),)},
    {"wells": ((1, 2), (4, 2)), "plants": ((1, 3, 1), (4, 3, 2))},
    {"wells": ((2, 1), (3, 2)), "plants": ((2, 2, 1), (4, 2, 2))},
    {"wells": ((2, 2), (3, 3), (1, 1), (4, 4)),
     "plants": ((1, 2, 1), (3, 2, 2), (3, 4, 1))},
    {"wells": ((2, 2), (2, 4), (1, 3), (3, 3)),
     "plants": ((1, 2, 1), (3, 2, 2), (1, 4, 1), (3, 4, 2))},
    {"wells": ((2, 2), (4, 2), (1, 1), (5, 1)),
     "plants": ((1, 2, 1), (3, 2, 2), (5, 2, 1))},
    {"wells": ((2, 1), (4, 1), (5, 2), (1, 2), (2, 2), (5, 4)),
     "plants": ((1, 1, 1), (3, 1, 2), (5, 1, 2), (2, 3, 2), (5, 3, 1))},
)


def _make_level(index, spec):
    return Level(
        sprites=[Sprite(pixels=np.zeros((64, 64), dtype=np.int64),
                        name="board", x=0, y=0, layer=0)],
        grid_size=(64, 64), data={"spec": spec}, name=str(index + 1),
    )


class Sg05(ARCBaseGame):
    def __init__(self, seed=0):
        self._spec = None
        self._wells = ()
        self._plants = {}
        self._history = []
        self._pending = None
        self._active_well = None
        levels = [_make_level(i, spec) for i, spec in enumerate(FIXED_LEVELS)]
        super().__init__(
            game_id="sg05-v1", levels=levels,
            camera=Camera(background=5, letter_box=5),
            available_actions=[6, 7], seed=seed,
        )

    def on_set_level(self, level):
        self._spec = level.get_data("spec")
        self._wells = tuple(tuple(cell) for cell in self._spec["wells"])
        self._plants = {(x, y): stage for x, y, stage in self._spec["plants"]}
        occupied = list(self._wells) + list(self._plants)
        self._min_x = min(x for x, y in occupied)
        self._max_x = max(x for x, y in occupied)
        self._min_y = min(y for x, y in occupied)
        self._max_y = max(y for x, y in occupied)
        width = self._max_x - self._min_x + 1
        height = self._max_y - self._min_y + 1
        self._pitch = min(MAX_PITCH, 54 // max(width, height))
        self._origin_x = (64 - width * self._pitch) // 2
        self._origin_y = (64 - height * self._pitch) // 2
        self._history = []
        self._pending = None
        self._active_well = None
        self._draw()

    @staticmethod
    def _adjacent(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1

    def _point(self, cell):
        return (self._origin_x + (cell[0] - self._min_x) * self._pitch,
                self._origin_y + (cell[1] - self._min_y) * self._pitch)

    def _clicked(self):
        data = self.action.data or {}
        x, y = data.get("x"), data.get("y")
        if type(x) is not int or type(y) is not int:
            return None
        bx = (x - self._origin_x) // self._pitch + self._min_x
        by = (y - self._origin_y) // self._pitch + self._min_y
        if not (self._min_x <= bx <= self._max_x and self._min_y <= by <= self._max_y):
            return None
        return (bx, by)

    def _water(self, well):
        if well not in self._wells:
            self.complete_action()
            return
        self._history.append(dict(self._plants))
        self._pending = well
        self._active_well = well
        self._draw()
        # The next native frame applies the visible well-to-sprout pulse.

    def step(self):
        if self._pending is not None:
            well = self._pending
            self._pending = None
            for plant in self._plants:
                if self._adjacent(well, plant):
                    self._plants[plant] = min(4, self._plants[plant] + 1)
            self._active_well = None
            self._draw()
            if self._plants and all(stage == 3 for stage in self._plants.values()):
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
                self._plants = self._history.pop()
                self._active_well = None
                self._draw()
            self.complete_action()
            return
        if action == GameAction.ACTION6:
            cell = self._clicked()
            if cell in self._wells:
                self._water(cell)
            else:
                self.complete_action()
            return
        self.complete_action()

    def _draw(self):
        pixels = np.full((64, 64), 5, dtype=np.int64)
        p = self._pitch
        mid = p // 2
        # Thin water paths depict exact local causality, not a circuit HUD.
        for well in self._wells:
            wx, wy = self._point(well)
            wcx, wcy = wx + mid, wy + mid
            for plant in self._plants:
                if not self._adjacent(well, plant):
                    continue
                px, py = self._point(plant)
                pcx, pcy = px + mid, py + mid
                color = 10 if well == self._active_well else 9
                if wx == px:
                    pixels[min(wcy, pcy):max(wcy, pcy) + 1, wcx] = color
                else:
                    pixels[wcy, min(wcx, pcx):max(wcx, pcx) + 1] = color
        for well in self._wells:
            x, y = self._point(well)
            color = 10 if well == self._active_well else 9
            cx, cy = x + mid, y + mid
            # Rounded water pool with one reflection, distinct from the
            # angular electrical sockets used in other games.
            pixels[cy - 3, cx - 1:cx + 2] = color
            pixels[cy - 2:cy + 2, cx - 3:cx + 4] = color
            pixels[cy + 2, cx - 2:cx + 3] = color
            pixels[cy - 2, cx - 1] = 0
        for plant, stage in self._plants.items():
            x, y = self._point(plant)
            cx, cy = x + mid, y + mid
            # An attached gray petal stencil gives the seed an observable
            # target shape. It fills yellow only when the flower is mature.
            petal = 11 if stage == 3 else 3
            pixels[cy - 4:cy - 2, cx - 1:cx + 2] = petal
            pixels[cy + 3:cy + 5, cx - 1:cx + 2] = petal
            pixels[cy - 1:cy + 2, cx - 4:cx - 2] = petal
            pixels[cy - 1:cy + 2, cx + 3:cx + 5] = petal
            pixels[cy:cy + 4, cx] = 14
            if stage == 1:
                pixels[cy - 1:cy + 1, cx - 1:cx + 2] = 14
            elif stage == 2:
                pixels[cy - 2:cy + 2, cx - 1:cx + 2] = 14
                pixels[cy:cy + 2, cx - 3:cx - 1] = 14
                pixels[cy:cy + 2, cx + 2:cx + 4] = 14
            elif stage == 3:
                pixels[cy - 2:cy + 3, cx - 2:cx + 3] = 11
                pixels[cy - 1:cy + 2, cx - 1:cx + 2] = 14
            else:
                pixels[cy - 3:cy + 4, cx - 3:cx + 4] = 13
                pixels[cy - 2:cy + 3, cx - 2:cx + 3] = 5
                pixels[cy - 1:cy + 2, cx - 1:cx + 2] = 13
        level = self.current_level
        level.remove_all_sprites()
        level.add_sprite(Sprite(pixels=pixels, name="board", x=0, y=0, layer=0))
