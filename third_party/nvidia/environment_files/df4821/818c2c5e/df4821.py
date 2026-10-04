# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the df4821/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy
import math
from collections import deque

# ═══════════════════════════════════════════════════════════════
# MODULE CONSTANTS
# ═══════════════════════════════════════════════════════════════

BG_COLOR = 3  # dark-gray background

COLORS = {
    "wall": 5,        # black - tube walls
    "yellow": 11,     # yellow flow blocks
    "orange": 12,     # orange flow blocks
    "red": 8,         # red flow blocks
    "green": 14,      # green flow blocks
    "maroon": 13,     # maroon flow blocks
    "highlight": 0,   # white - selection highlight
    "complete": 0,    # white - completion indicator
}

# Tube rendering constants
TUBE_INTERIOR_W = 6   # width of tube interior in pixels
BLOCK_SIZE = 6        # block size (square)
SLOT_H = 8            # vertical spacing between slot tops

# Tube vertical layout
MARKER_TOP_Y = 3      # y of source marker top
MARKER_H = 5          # marker height
TUBE_TOP_Y = 10       # y of tube top wall

# Tube X positions per tube count
TUBE_X_MAP = {
    4: [6, 20, 34, 48],
    5: [4, 16, 28, 40, 52],
}


def _tube_bot_y(capacity):
    """Compute tube bottom y based on capacity."""
    bot = TUBE_TOP_Y + 2 + capacity * SLOT_H
    return min(bot, 55)


LEVELS = {
    0: {
        "num_tubes": 4,
        "tube_capacity": 3,
        "tube_colors": [11, 12, -1, -1],
        "initial_stacks": [
            [11, 12, 11],
            [12, 11, 12],
            [],
            [],
        ],
        "locked_count": [0, 0, 0, 0],
        "budget": 24,
        "active_tags": [],
        "goal_requirements": {"all_tubes_sorted": True},
        "design_contract": {
            "success_trigger": "all_tubes_sorted",
            "primary_blocker": "blocks scrambled across tubes",
            "dependencies": ["use workspace", "sort blocks"],
            "feedback": "completed tubes show white indicator",
            "bypass_guard": "interleaved colors require multiple moves",
        },
    },
    1: {
        "num_tubes": 4,
        "tube_capacity": 4,
        "tube_colors": [11, 12, -1, -1],
        "initial_stacks": [
            [11, 12, 11, 12],
            [12, 11, 12, 11],
            [],
            [],
        ],
        "locked_count": [0, 0, 0, 0],
        "budget": 32,
        "active_tags": [],
        "goal_requirements": {"all_tubes_sorted": True},
        "design_contract": {
            "success_trigger": "all_tubes_sorted",
            "primary_blocker": "deeper interleaved stacks require longer chains",
            "dependencies": ["empty to workspace", "rebuild sorted stacks"],
            "feedback": "completed tubes show white indicator",
            "bypass_guard": "fully interleaved 4-deep stacks need full disassembly",
        },
    },
    2: {
        "num_tubes": 5,
        "tube_capacity": 3,
        "tube_colors": [11, 12, 8, -1, -1],
        "initial_stacks": [
            [11, 8, 12],
            [12, 11, 8],
            [8, 12, 11],
            [],
            [],
        ],
        "locked_count": [0, 0, 0, 0, 0],
        "budget": 30,
        "active_tags": [],
        "goal_requirements": {"all_tubes_sorted": True},
        "design_contract": {
            "success_trigger": "all_tubes_sorted",
            "primary_blocker": "3 colors with cyclic scramble",
            "dependencies": ["free top blocks", "route colors to correct tubes"],
            "feedback": "completed tubes show white indicator",
            "bypass_guard": "cyclic color placement requires routing through workspace",
        },
    },
    3: {
        "num_tubes": 5,
        "tube_capacity": 3,
        "tube_colors": [11, 12, 8, -1, -1],
        "initial_stacks": [
            [11, 8, 11],
            [12, 12, 8],
            [8, 11, 12],
            [],
            [],
        ],
        "locked_count": [1, 1, 1, 0, 0],
        "budget": 28,
        "active_tags": ["gravity"],
        "goal_requirements": {"all_tubes_sorted": True},
        "design_contract": {
            "success_trigger": "all_tubes_sorted",
            "primary_blocker": "locked bottom blocks with gravity constraint",
            "dependencies": ["work around locks", "sort top blocks only"],
            "feedback": "locked blocks shown with stripes; completed tubes show indicator",
            "bypass_guard": "cannot move locked bottom blocks; must sort remaining above",
        },
    },
    4: {
        "num_tubes": 4,
        "tube_capacity": 3,
        "tube_colors": [11, 12, 8, -1],
        "initial_stacks": [
            [8, 11, 12],
            [11, 12, 8],
            [12, 8, 11],
            [],
        ],
        "locked_count": [0, 0, 0, 0],
        "budget": 48,
        "active_tags": ["gravity"],
        "goal_requirements": {"all_tubes_sorted": True},
        "design_contract": {
            "success_trigger": "all_tubes_sorted",
            "primary_blocker": "only 1 workspace tube forces careful planning",
            "dependencies": ["manage single workspace", "avoid deadlocks"],
            "feedback": "completed tubes show white indicator",
            "bypass_guard": "single workspace means wrong moves create dead states quickly",
        },
    },
    5: {
        "num_tubes": 4,
        "tube_capacity": 3,
        "tube_colors": [11, 12, 8, -1],
        "initial_stacks": [
            [11, 12, 11],
            [12, 8, 12],
            [8, 11, 8],
            [],
        ],
        "locked_count": [1, 1, 1, 0],
        "budget": 34,
        "active_tags": ["gravity"],
        "goal_requirements": {"all_tubes_sorted": True},
        "design_contract": {
            "success_trigger": "all_tubes_sorted",
            "primary_blocker": "locked bottoms + single workspace = very constrained",
            "dependencies": ["route blocks with minimal workspace", "avoid blocking needed colors"],
            "feedback": "locked blocks striped; completed tubes show indicator",
            "bypass_guard": "locked + 1 workspace makes random solving near impossible",
        },
    },
    6: {
        "num_tubes": 4,
        "tube_capacity": 4,
        "tube_colors": [11, 12, 8, -1],
        "initial_stacks": [
            [11, 8, 12, 8],
            [12, 11, 8, 11],
            [8, 12, 11, 12],
            [],
        ],
        "locked_count": [1, 1, 1, 0],
        "budget": 40,
        "active_tags": ["gravity"],
        "goal_requirements": {"all_tubes_sorted": True},
        "design_contract": {
            "success_trigger": "all_tubes_sorted",
            "primary_blocker": "deep stacks + locks + 1 workspace = complex dependency chains",
            "dependencies": ["plan multi-step extraction", "manage 3 free slots per tube"],
            "feedback": "locked blocks striped; completed tubes show indicator",
            "bypass_guard": "deep locked stacks with 1 workspace require precise move ordering",
        },
    },
    7: {
        "num_tubes": 4,
        "tube_capacity": 5,
        "tube_colors": [11, 12, 8, -1],
        "initial_stacks": [
            [11, 11, 8, 12, 8],
            [12, 12, 11, 8, 11],
            [8, 8, 12, 11, 12],
            [],
        ],
        "locked_count": [2, 2, 2, 0],
        "budget": 42,
        "active_tags": ["gravity"],
        "goal_requirements": {"all_tubes_sorted": True},
        "design_contract": {
            "success_trigger": "all_tubes_sorted",
            "primary_blocker": "tallest stacks + deep locks + 1 workspace = maximum difficulty",
            "dependencies": ["plan long extraction sequences", "critical workspace management"],
            "feedback": "locked blocks striped; completed tubes show indicator",
            "bypass_guard": "5-deep stacks with 2 locked + 1 workspace is the hardest configuration",
        },
    },
}


# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def _get_tube_x(num_tubes):
    """Get tube X positions for given number of tubes."""
    return TUBE_X_MAP[num_tubes]


def _get_tube_from_x(x, num_tubes):
    """Determine which tube index was clicked based on x coordinate."""
    positions = _get_tube_x(num_tubes)
    for i in range(num_tubes):
        tx = positions[i]
        if tx - 1 <= x <= tx + TUBE_INTERIOR_W:
            return i
    return -1


def _is_tube_sorted(stack, target_color, capacity):
    """Check if a tube is correctly sorted."""
    if target_color == -1:
        return len(stack) == 0
    return len(stack) == capacity and all(b == target_color for b in stack)


def _draw_block(grid, x, y, color, highlighted=False, locked=False):
    """Draw a 6x6 block at pixel position (x, y)."""
    for dy in range(BLOCK_SIZE):
        for dx in range(BLOCK_SIZE):
            py = y + dy
            px = x + dx
            if 0 <= py < 64 and 0 <= px < 64:
                if dy == 0 or dy == BLOCK_SIZE - 1 or dx == 0 or dx == BLOCK_SIZE - 1:
                    if highlighted:
                        grid[py][px] = COLORS["highlight"]
                    else:
                        grid[py][px] = 5
                else:
                    if locked and (dx + dy) % 2 == 0:
                        grid[py][px] = 5
                    else:
                        grid[py][px] = color


def _draw_marker(grid, x, y, color):
    """Draw a 5x5 colored marker (ring shape)."""
    for dy in range(MARKER_H):
        for dx in range(MARKER_H):
            py = y + dy
            px = x + dx
            if 0 <= py < 64 and 0 <= px < 64:
                if dy == 0 or dy == MARKER_H - 1 or dx == 0 or dx == MARKER_H - 1:
                    grid[py][px] = 0
                else:
                    grid[py][px] = color


def _draw_tube_walls(grid, tube_idx, num_tubes, capacity):
    """Draw the walls of a tube."""
    positions = _get_tube_x(num_tubes)
    tx = positions[tube_idx]
    left_wall_x = tx - 1
    right_wall_x = tx + TUBE_INTERIOR_W
    tube_bot = _tube_bot_y(capacity)

    for y in range(TUBE_TOP_Y, tube_bot + 1):
        if 0 <= y < 64:
            if 0 <= left_wall_x < 64:
                grid[y][left_wall_x] = COLORS["wall"]
            if 0 <= right_wall_x < 64:
                grid[y][right_wall_x] = COLORS["wall"]

    for dx in range(-1, TUBE_INTERIOR_W + 1):
        px = tx + dx
        if 0 <= px < 64 and 0 <= tube_bot < 64:
            grid[tube_bot][px] = COLORS["wall"]


def _bfs_solve(initial_stacks, tube_colors, capacity, locked_count, max_states=200000):
    """BFS solver for tube sort puzzle. Returns list of (src, dst) moves."""
    num_tubes = len(initial_stacks)

    def state_key(stacks):
        return tuple(tuple(s) for s in stacks)

    def is_solved(stacks):
        for i in range(num_tubes):
            if not _is_tube_sorted(stacks[i], tube_colors[i], capacity):
                return False
        return True

    def get_moves(stacks):
        moves = []
        for src in range(num_tubes):
            if len(stacks[src]) <= locked_count[src]:
                continue
            for dst in range(num_tubes):
                if src == dst:
                    continue
                if len(stacks[dst]) >= capacity:
                    continue
                moves.append((src, dst))
        return moves

    def apply_move(stacks, src, dst):
        new_stacks = [list(s) for s in stacks]
        block = new_stacks[src].pop()
        new_stacks[dst].append(block)
        return new_stacks

    start = [list(s) for s in initial_stacks]
    if is_solved(start):
        return []

    start_key = state_key(start)
    queue = deque([(start, [])])
    visited = {start_key}

    while queue and len(visited) < max_states:
        current, path = queue.popleft()
        for move in get_moves(current):
            src, dst = move
            new_stacks = apply_move(current, src, dst)
            new_key = state_key(new_stacks)
            if new_key in visited:
                continue
            visited.add(new_key)
            new_path = path + [move]
            if is_solved(new_stacks):
                return new_path
            queue.append((new_stacks, new_path))

    return None


# ═══════════════════════════════════════════════════════════════
# GAME FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def get_available_actions():
    """Return available action integers for this game."""
    return [0, 6]


def get_initial_state(level):
    """Get the initial (h_t, z_t) for a given level."""
    lvl = LEVELS[level]
    h_t = {
        "level": level,
        "step": 0,
        "stacks": copy.deepcopy(lvl["initial_stacks"]),
        "selected_tube": -1,
        "undo_stack": [],
        "all_tubes_sorted": False,
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

    # Handle RESET action
    if a_t == 0:
        reset_h, _ = get_initial_state(level)
        return reset_h

    # Only accept CLICK actions (tuple of (6, x, y))
    if not (isinstance(a_t, (list, tuple)) and len(a_t) == 3 and a_t[0] == 6):
        return new_h

    _, click_x, click_y = a_t

    # Check budget
    if new_h["step"] >= lvl["budget"]:
        return new_h

    num_tubes = lvl["num_tubes"]
    capacity = lvl["tube_capacity"]
    tube_colors = lvl["tube_colors"]
    locked_count = lvl.get("locked_count", [0] * num_tubes)
    active_tags = lvl.get("active_tags", [])

    # Determine which tube was clicked
    clicked_tube = _get_tube_from_x(click_x, num_tubes)

    if clicked_tube == -1:
        return new_h

    # Check vertical range
    tube_bot = _tube_bot_y(capacity)
    if not (MARKER_TOP_Y <= click_y <= tube_bot + MARKER_H + 5):
        return new_h

    selected = new_h["selected_tube"]

    if selected == -1:
        # No tube selected - try to select
        stack = new_h["stacks"][clicked_tube]
        min_blocks = locked_count[clicked_tube] if "gravity" in active_tags else 0
        if len(stack) > min_blocks:
            new_h["selected_tube"] = clicked_tube
            new_h["step"] += 1
    elif selected == clicked_tube:
        # Deselect
        new_h["selected_tube"] = -1
        new_h["step"] -= 1
    else:
        # Move top block from selected to clicked tube
        src_stack = new_h["stacks"][selected]
        dst_stack = new_h["stacks"][clicked_tube]

        if len(src_stack) > 0 and len(dst_stack) < capacity:
            # Save undo
            undo_entry = {
                "stacks": copy.deepcopy(h_t["stacks"]),
                "step": h_t["step"],
                "selected_tube": h_t["selected_tube"],
            }
            if len(new_h["undo_stack"]) >= 50:
                new_h["undo_stack"] = new_h["undo_stack"][-49:]
            new_h["undo_stack"].append(undo_entry)

            block = src_stack.pop()
            dst_stack.append(block)
            new_h["selected_tube"] = -1
            new_h["step"] += 1

            # Check completion
            all_sorted = True
            for ti in range(num_tubes):
                if not _is_tube_sorted(new_h["stacks"][ti], tube_colors[ti], capacity):
                    all_sorted = False
                    break
            new_h["all_tubes_sorted"] = all_sorted
        else:
            new_h["selected_tube"] = -1
            new_h["step"] -= 1

    return new_h


def check_level_complete(h_t, z_t, level):
    """Check if the current level goal has been achieved."""
    lvl = LEVELS[level]
    reqs = lvl.get("goal_requirements", {})
    if "all_tubes_sorted" in reqs:
        if not h_t.get("all_tubes_sorted", False):
            return False
    return h_t.get("all_tubes_sorted", False)


def render(h_t, z_t):
    """Render the current state as a 64x64 grid."""
    grid = [[BG_COLOR] * 64 for _ in range(64)]

    level = h_t["level"]
    lvl = LEVELS[level]
    num_tubes = lvl["num_tubes"]
    capacity = lvl["tube_capacity"]
    tube_colors = lvl["tube_colors"]
    stacks = h_t["stacks"]
    selected = h_t["selected_tube"]
    locked_count = lvl.get("locked_count", [0] * num_tubes)
    active_tags = lvl.get("active_tags", [])
    positions = _get_tube_x(num_tubes)
    tube_bot = _tube_bot_y(capacity)

    for i in range(num_tubes):
        tx = positions[i]

        # Draw tube walls
        _draw_tube_walls(grid, i, num_tubes, capacity)

        # Draw source/basin markers
        if tube_colors[i] != -1:
            _draw_marker(grid, tx, MARKER_TOP_Y, tube_colors[i])
            basin_y = tube_bot + 2
            if basin_y + MARKER_H < 62:
                _draw_marker(grid, tx, basin_y, tube_colors[i])

        # Draw blocks
        stack = stacks[i]
        local_bot_y = tube_bot - 1 - BLOCK_SIZE
        for slot_idx, block_color in enumerate(stack):
            bx = tx
            by = local_bot_y - slot_idx * SLOT_H
            is_top = (slot_idx == len(stack) - 1)
            highlighted = (i == selected and is_top)
            is_locked = ("gravity" in active_tags and slot_idx < locked_count[i])
            _draw_block(grid, bx, by, block_color, highlighted, is_locked)

        # Completion indicator
        if tube_colors[i] != -1 and _is_tube_sorted(stack, tube_colors[i], capacity):
            dot_x = tx + TUBE_INTERIOR_W // 2
            dot_y = TUBE_TOP_Y + 1
            if 0 <= dot_y < 64 and 0 <= dot_x < 64:
                grid[dot_y][dot_x] = COLORS["complete"]
                if dot_x + 1 < 64:
                    grid[dot_y][dot_x + 1] = COLORS["complete"]

    # Budget bar on row 62-63
    budget = lvl["budget"]
    step = h_t["step"]
    remaining_frac = max(0, (budget - step)) / budget
    bar_width = int(remaining_frac * 60)
    for dx in range(60):
        px = 2 + dx
        if dx < bar_width:
            grid[62][px] = 14
            grid[63][px] = 14
        else:
            grid[62][px] = 8
            grid[63][px] = 8

    return grid


def solve_level(level):
    """Return a pre-computed sequence of actions that solves this level."""
    SOLUTIONS = {
        0: [(6,9,30),(6,37,30),(6,9,30),(6,51,30),(6,23,30),(6,51,30),(6,23,30),(6,9,30),(6,37,30),(6,9,30),(6,51,30),(6,23,30),(6,51,30),(6,23,30)],
        1: [(6,9,30),(6,37,30),(6,9,30),(6,37,30),(6,9,30),(6,37,30),(6,23,30),(6,9,30),(6,23,30),(6,37,30),(6,23,30),(6,9,30),(6,37,30),(6,23,30),(6,37,30),(6,23,30),(6,37,30),(6,9,30),(6,37,30),(6,23,30)],
        2: [(6,7,30),(6,43,30),(6,7,30),(6,43,30),(6,19,30),(6,43,30),(6,19,30),(6,7,30),(6,31,30),(6,7,30),(6,31,30),(6,19,30),(6,43,30),(6,31,30),(6,43,30),(6,31,30),(6,43,30),(6,19,30)],
        3: [(6,7,30),(6,43,30),(6,7,30),(6,43,30),(6,19,30),(6,43,30),(6,31,30),(6,19,30),(6,31,30),(6,7,30),(6,43,30),(6,31,30),(6,43,30),(6,31,30),(6,43,30),(6,7,30)],
        4: [(6,9,30),(6,51,30),(6,9,30),(6,51,30),(6,9,30),(6,51,30),(6,37,30),(6,9,30),(6,37,30),(6,9,30),(6,37,30),(6,9,30),(6,23,30),(6,37,30),(6,51,30),(6,37,30),(6,23,30),(6,37,30),(6,23,30),(6,51,30),(6,9,30),(6,23,30),(6,37,30),(6,23,30),(6,9,30),(6,37,30),(6,51,30),(6,9,30),(6,51,30),(6,9,30),(6,51,30),(6,23,30)],
        5: [(6,9,30),(6,51,30),(6,9,30),(6,51,30),(6,23,30),(6,51,30),(6,37,30),(6,23,30),(6,37,30),(6,9,30),(6,23,30),(6,37,30),(6,23,30),(6,37,30),(6,51,30),(6,23,30),(6,51,30),(6,23,30),(6,51,30),(6,9,30)],
        6: [(6,9,30),(6,51,30),(6,9,30),(6,51,30),(6,9,30),(6,51,30),(6,23,30),(6,9,30),(6,23,30),(6,51,30),(6,23,30),(6,9,30),(6,37,30),(6,23,30),(6,37,30),(6,9,30),(6,37,30),(6,23,30),(6,51,30),(6,37,30),(6,51,30),(6,37,30),(6,51,30),(6,23,30),(6,51,30),(6,37,30)],
        7: [(6,9,30),(6,51,30),(6,9,30),(6,51,30),(6,9,30),(6,51,30),(6,23,30),(6,9,30),(6,23,30),(6,51,30),(6,23,30),(6,9,30),(6,37,30),(6,23,30),(6,37,30),(6,9,30),(6,37,30),(6,23,30),(6,51,30),(6,37,30),(6,51,30),(6,37,30),(6,51,30),(6,23,30),(6,51,30),(6,37,30)],
    }
    return SOLUTIONS.get(level, [])


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Df4821(_FunctionalArcGame):
    GAME_ID = "df4821-818c2c5e"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
