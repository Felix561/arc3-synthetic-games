# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the fw4821/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy

# ─── Module Constants ───────────────────────────────────────────────────────

BG_COLOR = 5  # black
COLORS = {
    "empty": 5,       # black - unwoven
    "woven": 14,      # green - claimed territory
    "target": 11,     # yellow - target markers
    "obstacle": 4,    # near-black - walls/blockers
    "highlight": 8,   # red - last click feedback
}

CELL_SIZE = 3
PLAY_OFFSET_R = 1  # row 0 is budget bar
PLAY_OFFSET_C = 0

LEVELS = {
    0: {
        "grid_size": 5,
        "targets": [(0, 3), (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 4), (4, 3)],
        "obstacles": [],
        "pattern_type": "cross",
        "wrap": False,
        "budget": 18,
        "active_tags": [],
        "goal_requirements": {"targets_matched": 9},
        "design_contract": {
            "success_trigger": "targets_matched",
            "primary_blocker": "cross patterns overlap; must reason about XOR cancellation across 8 clicks",
            "dependencies": ["identify all 8 required click positions", "each click interacts with neighbors"],
            "feedback": "cells visibly toggle green/black on each click",
            "bypass_guard": "targets_matched only reaches 9 when exact board pattern achieved; no extra woven cells allowed",
            "state_key": "targets_matched",
        },
        "solution": [(0, 3), (1, 2), (1, 4), (2, 4), (3, 1), (4, 0), (4, 1), (4, 2)],
    },
    1: {
        "grid_size": 5,
        "targets": [(1, 0), (1, 2), (1, 4), (2, 4), (3, 0), (3, 1), (3, 4), (4, 0), (4, 3)],
        "obstacles": [(0, 0), (2, 0), (4, 4)],
        "pattern_type": "cross",
        "wrap": False,
        "budget": 20,
        "active_tags": ["obstacles"],
        "goal_requirements": {"targets_matched": 9},
        "design_contract": {
            "success_trigger": "targets_matched",
            "primary_blocker": "obstacles block cross pattern propagation; partial patterns require new reasoning",
            "dependencies": ["reason about blocked adjacency", "find 10 click positions accounting for obstacles"],
            "feedback": "cells toggle but obstacles remain static",
            "bypass_guard": "targets_matched only reaches 9 when exact pattern achieved with no extras",
            "state_key": "targets_matched",
        },
        "solution": [(0, 1), (0, 2), (0, 4), (1, 0), (1, 4), (2, 3), (2, 4), (3, 2), (4, 0), (4, 2)],
    },
    2: {
        "grid_size": 5,
        "targets": [(0, 3), (1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 4), (3, 0), (3, 1), (3, 3), (3, 4), (4, 0), (4, 1), (4, 4)],
        "obstacles": [],
        "pattern_type": "L",
        "wrap": False,
        "budget": 18,
        "active_tags": [],
        "goal_requirements": {"targets_matched": 14},
        "design_contract": {
            "success_trigger": "targets_matched",
            "primary_blocker": "L-shaped pattern is asymmetric; overlaps are harder to reason about",
            "dependencies": ["mentally simulate L-shape toggles", "find 9 click positions"],
            "feedback": "cells toggle in L-shape from click point",
            "bypass_guard": "targets_matched only reaches 14 when exact pattern achieved",
            "state_key": "targets_matched",
        },
        "solution": [(0, 3), (0, 4), (1, 1), (2, 4), (3, 0), (3, 3), (3, 4), (4, 1), (4, 2)],
    },
    3: {
        "grid_size": 5,
        "targets": [(0, 0), (0, 1), (0, 4), (1, 1), (1, 2), (1, 4), (2, 1), (2, 2), (3, 0), (3, 2), (3, 4), (4, 2)],
        "obstacles": [],
        "pattern_type": "cross",
        "wrap": True,
        "budget": 18,
        "active_tags": ["wrap"],
        "goal_requirements": {"targets_matched": 12},
        "design_contract": {
            "success_trigger": "targets_matched",
            "primary_blocker": "wrap causes cross patterns to affect opposite edges; must reason toroidally",
            "dependencies": ["understand wrap mechanics", "find 8 click positions with toroidal effects"],
            "feedback": "cells on opposite edges toggle when pattern wraps",
            "bypass_guard": "targets_matched only reaches 12 when exact pattern achieved",
            "state_key": "targets_matched",
        },
        "solution": [(0, 0), (0, 2), (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (3, 0)],
    },
    4: {
        "grid_size": 5,
        "targets": [(0, 2), (1, 1), (2, 0), (2, 1), (3, 3), (4, 0), (4, 2), (4, 4)],
        "obstacles": [],
        "pattern_type": "ring",
        "wrap": True,
        "budget": 20,
        "active_tags": ["wrap"],
        "goal_requirements": {"targets_matched": 8},
        "design_contract": {
            "success_trigger": "targets_matched",
            "primary_blocker": "ring pattern toggles 8 neighbors; large overlap regions require careful planning",
            "dependencies": ["reason about 8-neighbor ring with wrap", "find 11 click positions"],
            "feedback": "ring of cells toggles around clicked point",
            "bypass_guard": "targets_matched only reaches 8 when exact pattern achieved",
            "state_key": "targets_matched",
        },
        "solution": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 4), (2, 0), (2, 1), (2, 2), (3, 0)],
    },
    5: {
        "grid_size": 5,
        "targets": [(0, 3), (1, 0), (1, 2), (2, 0), (2, 3), (3, 1), (3, 4), (4, 3)],
        "obstacles": [(1, 1), (3, 3)],
        "pattern_type": "cross",
        "wrap": True,
        "budget": 20,
        "active_tags": ["wrap", "obstacles"],
        "goal_requirements": {"targets_matched": 8},
        "design_contract": {
            "success_trigger": "targets_matched",
            "primary_blocker": "wrap + obstacles combine; patterns wrap around but stop at obstacles",
            "dependencies": ["reason about wrap + obstacle interaction", "find 11 click positions"],
            "feedback": "cells toggle with wrap but obstacles block",
            "bypass_guard": "targets_matched only reaches 8 when exact pattern achieved",
            "state_key": "targets_matched",
        },
        "solution": [(0, 0), (0, 1), (0, 3), (0, 4), (1, 3), (1, 4), (2, 0), (2, 1), (2, 3), (2, 4), (4, 0)],
    },
    6: {
        "grid_size": 5,
        "targets": [(0, 1), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 4), (3, 0), (3, 1), (3, 2), (4, 1), (4, 2), (4, 3), (4, 4)],
        "obstacles": [],
        "pattern_type": "L",
        "wrap": True,
        "budget": 22,
        "active_tags": ["wrap"],
        "goal_requirements": {"targets_matched": 17},
        "design_contract": {
            "success_trigger": "targets_matched",
            "primary_blocker": "L-pattern with wrap creates asymmetric toroidal effects; 13 clicks needed",
            "dependencies": ["reason about L-shape wrapping at edges", "find 13 click positions"],
            "feedback": "L-pattern wraps around grid edges",
            "bypass_guard": "targets_matched only reaches 17 when exact pattern achieved",
            "state_key": "targets_matched",
        },
        "solution": [(0, 0), (0, 2), (0, 4), (1, 0), (1, 3), (1, 4), (2, 0), (2, 3), (2, 4), (3, 1), (3, 3), (4, 2), (4, 3)],
    },
    7: {
        "grid_size": 5,
        "targets": [(0, 0), (2, 0), (2, 1), (3, 0), (3, 2), (4, 0), (4, 2), (4, 3), (4, 4)],
        "obstacles": [],
        "pattern_type": "L",
        "wrap": True,
        "budget": 22,
        "active_tags": ["wrap"],
        "goal_requirements": {"targets_matched": 9},
        "design_contract": {
            "success_trigger": "targets_matched",
            "primary_blocker": "15 clicks needed with L+wrap; maximum planning depth required",
            "dependencies": ["find exact 15-click L+wrap solution", "reason about complex toroidal L overlaps"],
            "feedback": "cells toggle; budget bar shows extreme pressure",
            "bypass_guard": "targets_matched only reaches 9 when exact pattern achieved; 15 of 25 cells clicked",
            "state_key": "targets_matched",
        },
        "solution": [(0, 1), (0, 3), (1, 1), (1, 2), (2, 0), (2, 1), (3, 0), (3, 2), (3, 3), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)],
    },
}


# ─── Helper Functions ───────────────────────────────────────────────────────

def _get_cross_pattern(r, c, grid_size, wrap=False):
    """Return list of cells toggled by cross pattern at (r, c)."""
    cells = [(r, c)]
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if wrap:
            nr, nc = nr % grid_size, nc % grid_size
            cells.append((nr, nc))
        else:
            if 0 <= nr < grid_size and 0 <= nc < grid_size:
                cells.append((nr, nc))
    return cells


def _get_l_pattern(r, c, grid_size, wrap=False):
    """Return list of cells toggled by L pattern at (r, c): center + right + down."""
    cells = [(r, c)]
    nc = (c + 1) % grid_size if wrap else c + 1
    if wrap or (0 <= nc < grid_size):
        cells.append((r, nc))
    nr = (r + 1) % grid_size if wrap else r + 1
    if wrap or (0 <= nr < grid_size):
        cells.append((nr, c))
    return cells


def _get_ring_pattern(r, c, grid_size, wrap=False):
    """Return list of cells toggled by ring pattern (8 neighbors, not center)."""
    cells = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if wrap:
                nr, nc = nr % grid_size, nc % grid_size
                cells.append((nr, nc))
            else:
                if 0 <= nr < grid_size and 0 <= nc < grid_size:
                    cells.append((nr, nc))
    return cells


def _get_pattern(r, c, pattern_type, grid_size, wrap=False):
    """Get the list of cells affected by clicking (r,c) with given pattern."""
    if pattern_type == "cross":
        return _get_cross_pattern(r, c, grid_size, wrap)
    elif pattern_type == "L":
        return _get_l_pattern(r, c, grid_size, wrap)
    elif pattern_type == "ring":
        return _get_ring_pattern(r, c, grid_size, wrap)
    return [(r, c)]


def _pixel_to_grid(px_r, px_c, grid_size):
    """Convert pixel coordinate to logical grid coordinate. Returns None if out of bounds."""
    local_r = px_r - PLAY_OFFSET_R
    local_c = px_c - PLAY_OFFSET_C
    if local_r < 0 or local_c < 0:
        return None
    gr = local_r // CELL_SIZE
    gc = local_c // CELL_SIZE
    if 0 <= gr < grid_size and 0 <= gc < grid_size:
        return (gr, gc)
    return None


def _draw_entity(grid, row, col, entity_type):
    """Draw a 3x3 entity at pixel position (row, col)."""
    if entity_type == "empty":
        for dr in range(CELL_SIZE):
            for dc in range(CELL_SIZE):
                r, c = row + dr, col + dc
                if 0 <= r < 16 and 0 <= c < 16:
                    grid[r][c] = COLORS["empty"]
    elif entity_type == "woven":
        for dr in range(CELL_SIZE):
            for dc in range(CELL_SIZE):
                r, c = row + dr, col + dc
                if 0 <= r < 16 and 0 <= c < 16:
                    grid[r][c] = COLORS["woven"]
        cr, cc = row + 1, col + 1
        if 0 <= cr < 16 and 0 <= cc < 16:
            grid[cr][cc] = COLORS["target"]
    elif entity_type == "target":
        for dr in range(CELL_SIZE):
            for dc in range(CELL_SIZE):
                r, c = row + dr, col + dc
                if 0 <= r < 16 and 0 <= c < 16:
                    if dr == 0 or dr == CELL_SIZE - 1 or dc == 0 or dc == CELL_SIZE - 1:
                        grid[r][c] = COLORS["target"]
                    else:
                        grid[r][c] = COLORS["empty"]
    elif entity_type == "obstacle":
        for dr in range(CELL_SIZE):
            for dc in range(CELL_SIZE):
                r, c = row + dr, col + dc
                if 0 <= r < 16 and 0 <= c < 16:
                    if (dr + dc) % 2 == 0:
                        grid[r][c] = COLORS["obstacle"]
                    else:
                        grid[r][c] = COLORS["empty"]


# ─── Required Game Functions ────────────────────────────────────────────────

def get_available_actions():
    """Return available action integers for this game."""
    return [0, 6]


def get_initial_state(level):
    """Get the initial (h_t, z_t) for a given level."""
    lvl = LEVELS[level]
    grid_size = lvl["grid_size"]
    h_t = {
        "level": level,
        "step": 0,
        "grid_state": [[0] * grid_size for _ in range(grid_size)],
        "last_click": None,
        "complete": False,
        "targets_matched": 0,
    }
    z_t = {}
    return h_t, z_t


def predict(h_t):
    """Return minimal/empty z_t. This game is fully deterministic."""
    return {}


def transition(h_t, z_t, a_t):
    """Deterministic history state update."""
    new_h = copy.deepcopy(h_t)
    level = new_h["level"]
    lvl = LEVELS[level]

    if isinstance(a_t, int):
        if a_t == 0:
            init_h, _ = get_initial_state(level)
            return init_h
        else:
            return new_h

    if not (isinstance(a_t, (list, tuple)) and len(a_t) == 3 and a_t[0] == 6):
        return new_h

    _, px_c, px_r = a_t

    if new_h["complete"]:
        return new_h
    if new_h["step"] >= lvl["budget"]:
        return new_h

    grid_size = lvl["grid_size"]
    grid_coord = _pixel_to_grid(px_r, px_c, grid_size)
    if grid_coord is None:
        return new_h

    gr, gc = grid_coord
    obstacle_set = set(tuple(o) for o in lvl["obstacles"])
    if (gr, gc) in obstacle_set:
        return new_h

    wrap = lvl.get("wrap", False)
    pattern_type = lvl["pattern_type"]
    affected = _get_pattern(gr, gc, pattern_type, grid_size, wrap)

    for (ar, ac) in affected:
        if (ar, ac) not in obstacle_set:
            new_h["grid_state"][ar][ac] = 1 - new_h["grid_state"][ar][ac]

    new_h["last_click"] = (gr, gc)
    new_h["step"] += 1

    target_set = set(tuple(t) for t in lvl["targets"])
    matched = 0
    for (tr, tc) in target_set:
        if new_h["grid_state"][tr][tc] == 1:
            matched += 1
    new_h["targets_matched"] = matched

    if _check_win(new_h, lvl):
        new_h["complete"] = True

    return new_h


def _check_win(h_t, lvl):
    """Check if current grid state matches target exactly."""
    grid_size = lvl["grid_size"]
    target_set = set(tuple(t) for t in lvl["targets"])
    for r in range(grid_size):
        for c in range(grid_size):
            is_woven = h_t["grid_state"][r][c] == 1
            should_be_woven = (r, c) in target_set
            if is_woven != should_be_woven:
                return False
    return True


def check_level_complete(h_t, z_t, level):
    """Check if the current level's goal has been achieved."""
    lvl = LEVELS[level]
    return _check_win(h_t, lvl)


def render(h_t, z_t):
    """Render the current state as a 16x16 grid."""
    grid = [[BG_COLOR] * 16 for _ in range(16)]
    level = h_t["level"]
    lvl = LEVELS[level]
    grid_size = lvl["grid_size"]
    target_set = set(tuple(t) for t in lvl["targets"])
    obstacle_set = set(tuple(o) for o in lvl["obstacles"])

    for gr in range(grid_size):
        for gc in range(grid_size):
            px_r = PLAY_OFFSET_R + gr * CELL_SIZE
            px_c = PLAY_OFFSET_C + gc * CELL_SIZE
            if (gr, gc) in obstacle_set:
                _draw_entity(grid, px_r, px_c, "obstacle")
            elif h_t["grid_state"][gr][gc] == 1:
                _draw_entity(grid, px_r, px_c, "woven")
            elif (gr, gc) in target_set:
                _draw_entity(grid, px_r, px_c, "target")
            else:
                _draw_entity(grid, px_r, px_c, "empty")

    budget = lvl["budget"]
    steps_used = h_t["step"]
    remaining = max(0, budget - steps_used)
    bar_length = min(16, int(16 * remaining / budget)) if budget > 0 else 0
    for c in range(16):
        if c < bar_length:
            grid[0][c] = COLORS["woven"]
        else:
            grid[0][c] = COLORS["highlight"]

    return grid


def solve_level(level):
    """Return a fixed sequence of actions that solves this level."""
    lvl = LEVELS[level]
    solution_coords = lvl["solution"]
    actions = []
    for (gr, gc) in solution_coords:
        px_r = PLAY_OFFSET_R + gr * CELL_SIZE + 1
        px_c = PLAY_OFFSET_C + gc * CELL_SIZE + 1
        actions.append((6, px_c, px_r))
    return actions


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Fw4821(_FunctionalArcGame):
    GAME_ID = "fw4821-98cb6b43"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
