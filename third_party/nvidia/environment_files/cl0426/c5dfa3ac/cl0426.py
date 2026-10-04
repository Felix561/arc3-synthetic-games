# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the cl0426/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy

BG_COLOR = 0
EMPTY = -1
CELL = 7
TILE = 4
BOARD_TOP = 7
BOARD_LEFT = 5

COLORS = {
    "bg": 0,
    "pink": 6,
    "purple": 15,
    "light_blue": 10,
    "yellow": 11,
    "green": 14,
    "light_pink": 7,
    "blue": 9,
    "orange": 12,
    "target": 11,
    "target_alt": 9,
    "select": 6,
}

LEVELS = {
    0: {
        "name": "Four Cream Orders",
        "rows": 5,
        "cols": 5,
        "board": [
            [6, 6, 14, 15, 12],
            [15, 12, 6, 7, 9],
            [14, 7, 15, 11, 9],
            [14, 10, 11, 9, 12],
            [7, 14, 11, 11, 10],
        ],
        "targets": [(0, 1), (2, 4), (3, 0), (4, 3)],
        "budget": 18,
        "active_tags": [],
        "goal_requirements": {"all_targets_clear": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "all_targets_clear",
            "primary_blocker": "four target rings are occupied by cream tiles until each is included in a local match",
            "dependencies": ["clear pink row target", "clear blue column target", "clear green column target", "clear yellow column target"],
            "feedback": "matched tiles vanish, leaving empty target-ring pockets with green confirmation marks",
            "bypass_guard": "the all_targets_clear state key becomes true only when every visible target coordinate is empty after a valid match",
        },
    },
    1: {
        "name": "Locked Cotton Lift",
        "rows": 5,
        "cols": 6,
        "board": [
            [10, 6, 6, 14, 15, 12],
            [7, 15, 12, 6, 14, 9],
            [9, 14, 14, 15, 11, 9],
            [12, 14, 10, 11, 9, 12],
            [15, 7, 14, 11, 11, 10],
        ],
        "targets": [(0, 2), (1, 4), (2, 5), (3, 1), (4, 4)],
        "locked_cells": [(2, 2)],
        "unlock_targets": [(0, 2)],
        "budget": 20,
        "active_tags": ["locks"],
        "goal_requirements": {"all_targets_clear": True, "locks_open": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "all_targets_clear",
            "state_keys": ["all_targets_clear", "locks_open"],
            "primary_blocker": "one required cream is locked until the first order ring is cleared",
            "dependencies": ["clear the pink unlock order", "use the released cream to make the green row order", "clear blue, green, and yellow target orders"],
            "feedback": "the purple lock frame disappears once the unlock target is empty; target pips turn green as rings clear",
            "bypass_guard": "the locked cream cannot be selected or swapped before the unlock target is cleared, so all target rings cannot be emptied early",
        },
    },
    2: {
        "name": "Elevator Cascade Field",
        "rows": 6,
        "cols": 6,
        "board": [
            [10, 6, 15, 14, 7, 12],
            [9, 14, 10, 6, 15, 9],
            [9, 7, 12, 11, 14, 9],
            [12, 12, 6, 15, 9, 7],
            [9, 15, 14, 11, 11, 10],
            [15, 10, 7, 14, 6, 11],
        ],
        "targets": [(3, 1), (4, 0), (1, 5), (2, 5), (4, 4)],
        "cascade_columns": [0, 1, 2, 3, 4, 5],
        "budget": 18,
        "active_tags": ["cascade"],
        "goal_requirements": {"all_targets_clear": True, "cascade_done": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "all_targets_clear",
            "state_keys": ["all_targets_clear", "cascade_done"],
            "primary_blocker": "one blue order can only clear after a first row match opens an elevator-gap cascade",
            "dependencies": ["make the orange row match", "let gravity cascade clear the blue column order", "finish the right-side blue and yellow orders"],
            "feedback": "orange elevator arrows mark cascade columns; cascade counter and target pips light green after chain clears",
            "bypass_guard": "completion requires the visible cascade_done state as well as all target pips, so ordinary direct matches alone cannot finish",
        },
    },
    3: {
        "name": "Blocked Cascade Attitude",
        "rows": 6,
        "cols": 7,
        "board": [
            [10, 7, 6, 6, 14, 12, 9],
            [15, 10, 14, 7, 6, 14, 12],
            [9, 12, 15, 10, 14, 12, 9],
            [7, 6, 10, 15, 7, 9, 10],
            [15, 14, 7, 11, 11, 12, 9],
            [14, 12, 14, 10, 15, 11, 12],
        ],
        "targets": [(0, 2), (5, 1), (2, 6), (4, 4), (4, 5)],
        "locked_cells": [(5, 1)],
        "unlock_targets": [(0, 2)],
        "cascade_columns": [0, 1, 2, 3, 4, 5, 6],
        "budget": 20,
        "active_tags": ["locks", "cascade"],
        "goal_requirements": {"all_targets_clear": True, "locks_open": True, "cascade_done": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "all_targets_clear",
            "state_keys": ["all_targets_clear", "locks_open", "cascade_done"],
            "primary_blocker": "a required green target is locked, and another order must be cleared by an elevator cascade",
            "dependencies": ["clear the pink unlock order", "use the released locked green tile in a row match", "make the orange cascade setup", "finish blue and yellow target orders"],
            "feedback": "the purple lock frame disappears; orange arrows show falling columns; cascade counter and target pips confirm progress",
            "bypass_guard": "the locked target cannot be selected before the unlock order, and completion also requires a visible cascade clear",
        },
    },
    4: {
        "name": "Lives in the Cream Field",
        "rows": 7,
        "cols": 7,
        "board": [
            [6, 6, 14, 10, 15, 12, 7],
            [15, 12, 6, 7, 14, 10, 9],
            [10, 7, 15, 12, 15, 11, 9],
            [14, 10, 15, 15, 10, 9, 12],
            [14, 7, 10, 6, 12, 15, 7],
            [7, 14, 12, 10, 6, 11, 15],
            [15, 12, 7, 11, 11, 10, 14],
        ],
        "targets": [(0, 1), (2, 6), (5, 0), (6, 4), (3, 3)],
        "budget": 17,
        "lives": 3,
        "active_tags": ["lives"],
        "goal_requirements": {"all_targets_clear": True, "lives_positive": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "all_targets_clear",
            "state_keys": ["all_targets_clear", "lives_positive"],
            "primary_blocker": "five separated target rings require correct local swaps while wrong swaps spend limited lives",
            "dependencies": ["clear pink top order", "clear blue side order", "clear green lower-left order", "clear yellow bottom order", "clear purple center order without exhausting lives"],
            "feedback": "matched target pips turn green; pink heart pips disappear when a no-match swap is attempted",
            "bypass_guard": "completion requires every visible target to have been cleared and at least one life remaining; invalid swaps can make the level unwinnable",
        },
    },
    5: {
        "name": "Cream Bus Cascade Lives",
        "rows": 7,
        "cols": 7,
        "board": [
            [6, 6, 14, 11, 12, 11, 9],
            [15, 15, 6, 7, 11, 9, 12],
            [10, 7, 15, 15, 10, 12, 9],
            [14, 10, 7, 12, 15, 14, 9],
            [7, 12, 10, 6, 14, 15, 7],
            [10, 14, 12, 7, 6, 11, 15],
            [15, 12, 14, 11, 11, 10, 14],
        ],
        "targets": [(0, 1), (2, 6), (0, 4), (1, 1), (6, 4)],
        "cascade_columns": [0, 1, 2, 3, 4, 5, 6],
        "budget": 18,
        "lives": 2,
        "active_tags": ["cascade", "lives"],
        "goal_requirements": {"all_targets_clear": True, "cascade_done": True, "lives_positive": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "all_targets_clear",
            "state_keys": ["all_targets_clear", "cascade_done", "lives_positive"],
            "primary_blocker": "a wider field mixes cascade gravity with only two spare lives for wrong swaps",
            "dependencies": ["clear the top pink order", "clear the blue side order", "clear the yellow upper order", "clear the purple left order", "make the bottom yellow order trigger a fall"],
            "feedback": "target pips turn green, hearts show remaining lives, and orange elevator arrows/cascade counter show falling columns",
            "bypass_guard": "every target must be visibly cleared, at least one life must remain, and a cascade fall must have occurred before completion",
        },
    },
    6: {
        "name": "Foggy Similar Cream Field",
        "rows": 8,
        "cols": 8,
        "board": [
            [6, 6, 14, 10, 11, 12, 11, 7],
            [15, 15, 6, 15, 10, 11, 9, 12],
            [10, 7, 14, 10, 15, 12, 9, 9],
            [14, 10, 7, 12, 11, 14, 12, 9],
            [7, 12, 10, 6, 14, 15, 11, 7],
            [10, 14, 12, 7, 6, 11, 15, 14],
            [15, 12, 14, 11, 11, 10, 14, 15],
            [7, 10, 15, 14, 12, 11, 6, 10],
        ],
        "targets": [(0, 1), (0, 5), (1, 1), (2, 7), (6, 4)],
        "cascade_columns": [0, 1, 2, 3, 4, 5, 6, 7],
        "budget": 17,
        "lives": 2,
        "fog_radius": 5,
        "active_tags": ["cascade", "lives", "fog"],
        "goal_requirements": {"all_targets_clear": True, "cascade_done": True, "lives_positive": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "all_targets_clear",
            "state_keys": ["all_targets_clear", "cascade_done", "lives_positive"],
            "primary_blocker": "an 8x8 field is partially masked after play, so the player must remember separated match setups while preserving lives",
            "dependencies": ["clear two top orders before fog narrows context", "use remembered left purple row setup", "clear the right blue column with a fall", "finish the lower yellow order"],
            "feedback": "the last-click neighborhood remains visible, target pips/heart pips stay in HUD, and cascade arrows remain visible around the active area",
            "bypass_guard": "all visible target pips, cascade_done, and a positive life state are required; fog never hides the HUD requirements",
        },
    },
    7: {
        "name": "Final Cream Elevator Chain",
        "rows": 8,
        "cols": 8,
        "board": [
            [6, 6, 14, 10, 11, 12, 11, 7],
            [15, 15, 6, 15, 10, 11, 9, 12],
            [10, 7, 14, 10, 15, 12, 9, 9],
            [14, 10, 7, 12, 11, 14, 12, 9],
            [7, 12, 10, 6, 14, 15, 11, 7],
            [10, 14, 12, 7, 6, 11, 15, 14],
            [15, 12, 14, 11, 11, 10, 14, 15],
            [14, 14, 7, 14, 12, 11, 6, 10],
        ],
        "targets": [(0, 1), (0, 5), (1, 1), (2, 7), (6, 4), (7, 2)],
        "cascade_columns": [0, 1, 2, 3, 4, 5, 6, 7],
        "budget": 19,
        "lives": 2,
        "fog_radius": 4,
        "min_cascades": 3,
        "active_tags": ["cascade", "lives", "fog"],
        "goal_requirements": {"all_targets_clear": True, "cascade_done": True, "lives_positive": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "all_targets_clear",
            "state_keys": ["all_targets_clear", "cascade_done", "lives_positive"],
            "primary_blocker": "six separated target rings must be cleared while achieving three visible elevator falls under fog and life pressure",
            "dependencies": ["clear two top orders", "clear the remembered purple order", "trigger the right-side fall", "trigger the lower yellow fall", "finish with the bottom green fall"],
            "feedback": "target pips, hearts, fog window, and cascade arrows/counter show all requirements before final completion",
            "bypass_guard": "all target pips and three cascade events are required, so early target clearing without the final falls cannot complete the level",
        },
    }
}

def _draw_entity(grid, row, col, entity_type):
    """Draw one medium tile/entity with a distinctive 4x4 pixel glyph."""
    top = BOARD_TOP + row * CELL
    left = BOARD_LEFT + col * CELL
    # faint slot corner ticks
    for dy, dx in [(0, 0), (0, TILE - 1), (TILE - 1, 0), (TILE - 1, TILE - 1)]:
        y = top + dy
        x = left + dx
        if 0 <= y < 64 and 0 <= x < 64:
            grid[y][x] = COLORS["light_blue"]
    if entity_type == EMPTY:
        return
    color = entity_type
    # base colored 4x4 tile
    for y in range(top, top + TILE):
        for x in range(left, left + TILE):
            if 0 <= y < 64 and 0 <= x < 64:
                grid[y][x] = color
    # color-specific readable glyphs using only palette colors
    if color == 6:  # pink dot-center
        grid[top + 1][left + 1] = 0
        grid[top + 2][left + 2] = 0
    elif color == 15:  # purple hollow/ring
        for y in range(top + 1, top + 3):
            for x in range(left + 1, left + 3):
                grid[y][x] = 0
    elif color == 10:  # light-blue diagonal
        for i in range(TILE):
            grid[top + i][left + i] = 0
    elif color == 11:  # yellow plus
        for i in range(TILE):
            grid[top + 1][left + i] = 0
            grid[top + i][left + 1] = 0
    elif color == 14:  # green split
        for x in range(left, left + TILE):
            grid[top + 2][x] = 0
    elif color == 7:  # light-pink corner mark
        grid[top][left] = 0
        grid[top][left + 1] = 0
        grid[top + 1][left] = 0
    elif color == 9:  # blue vertical bar
        for y in range(top, top + TILE):
            grid[y][left + 2] = 0
    elif color == 12:  # orange hollow square
        grid[top + 1][left + 1] = 0
        grid[top + 1][left + 2] = 0
        grid[top + 2][left + 1] = 0
        grid[top + 2][left + 2] = 0


def _cell_from_click(x, y, level_conf):
    cols = level_conf["cols"]
    rows = level_conf["rows"]
    c = (x - BOARD_LEFT) // CELL
    r = (y - BOARD_TOP) // CELL
    if 0 <= r < rows and 0 <= c < cols:
        lx = (x - BOARD_LEFT) % CELL
        ly = (y - BOARD_TOP) % CELL
        if 0 <= lx < TILE and 0 <= ly < TILE:
            return (r, c)
    return None


def _find_matches(board):
    rows = len(board)
    cols = len(board[0])
    matched = set()
    for r in range(rows):
        c = 0
        while c < cols:
            color = board[r][c]
            start = c
            while c < cols and board[r][c] == color:
                c += 1
            if color != EMPTY and c - start >= 3:
                for cc in range(start, c):
                    matched.add((r, cc))
    for c in range(cols):
        r = 0
        while r < rows:
            color = board[r][c]
            start = r
            while r < rows and board[r][c] == color:
                r += 1
            if color != EMPTY and r - start >= 3:
                for rr in range(start, r):
                    matched.add((rr, c))
    return matched


def _record_cleared_targets(state, matches):
    target_set = set(LEVELS[state["level"]].get("targets", []))
    cleared = set(tuple(p) for p in state.get("cleared_targets", []))
    for pos in matches:
        if pos in target_set:
            cleared.add(pos)
    state["cleared_targets"] = sorted(cleared)


def _apply_gravity(board):
    rows = len(board)
    cols = len(board[0])
    moved = False
    for c in range(cols):
        old_col = [board[r][c] for r in range(rows)]
        non_empty = [board[r][c] for r in range(rows) if board[r][c] != EMPTY]
        new_col = [EMPTY] * (rows - len(non_empty)) + non_empty
        if new_col != old_col:
            moved = True
        for r in range(rows):
            board[r][c] = new_col[r]
    return moved


def _update_target_flags(state):
    level_conf = LEVELS[state["level"]]
    targets = level_conf.get("targets", [])
    cleared_set = set(tuple(p) for p in state.get("cleared_targets", []))
    for r, c in targets:
        if state["board"][r][c] == EMPTY:
            cleared_set.add((r, c))
    state["cleared_targets"] = sorted(cleared_set)
    state["targets_cleared"] = sum(1 for pos in targets if pos in cleared_set)
    state["all_targets_clear"] = (len(targets) > 0 and state["targets_cleared"] == len(targets))
    if "locks" in level_conf.get("active_tags", []):
        unlock_targets = level_conf.get("unlock_targets", [])
        if unlock_targets and all((r, c) in cleared_set or state["board"][r][c] == EMPTY for r, c in unlock_targets):
            state["locks_open"] = True
    else:
        state["locks_open"] = True
    if "cascade" not in level_conf.get("active_tags", []):
        state["cascade_done"] = True
    elif level_conf.get("min_cascades", 1) > 1:
        state["cascade_done"] = state.get("cascade_count", 0) >= level_conf.get("min_cascades", 1)
    if "lives" in level_conf.get("active_tags", []):
        state["lives_positive"] = state.get("lives", 0) > 0
    else:
        state["lives_positive"] = True
    state["complete"] = state["all_targets_clear"] and all(
        (key == "all_targets_clear" or state.get(key) == expected)
        for key, expected in level_conf.get("goal_requirements", {}).items()
    )


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    """Deterministic history state update (DreamerV3 sequence model)."""
    if not h_t or h_t.get("level") not in LEVELS:
        return copy.deepcopy(h_t)
    level = h_t["level"]
    level_conf = LEVELS[level]
    base_action = a_t[0] if isinstance(a_t, tuple) and len(a_t) > 0 else a_t
    if base_action not in get_available_actions():
        return copy.deepcopy(h_t)
    if base_action == 0:
        return get_initial_state(level)[0]
    if base_action != 6 or not (isinstance(a_t, tuple) and len(a_t) == 3):
        return copy.deepcopy(h_t)

    new_h = copy.deepcopy(h_t)
    if new_h.get("complete") or new_h.get("budget", 0) <= 0:
        return new_h
    if "lives" in level_conf.get("active_tags", []) and new_h.get("lives", 0) <= 0:
        return new_h

    x, y = a_t[1], a_t[2]
    cell = _cell_from_click(x, y, level_conf)
    if cell is None:
        return new_h
    r, c = cell
    if "locks" in level_conf.get("active_tags", []) and not new_h.get("locks_open", False):
        if (r, c) in level_conf.get("locked_cells", []):
            new_h["last_click"] = (r, c)
            return new_h
    if new_h["board"][r][c] == EMPTY:
        new_h["selected"] = None
        new_h["last_click"] = (r, c)
        return new_h

    selected = new_h.get("selected")
    if selected is None:
        new_h["selected"] = (r, c)
        new_h["last_click"] = (r, c)
        return new_h
    sr, sc = selected
    if (sr, sc) == (r, c):
        new_h["selected"] = None
        new_h["last_click"] = (r, c)
        return new_h
    if abs(sr - r) + abs(sc - c) != 1:
        new_h["selected"] = (r, c)
        new_h["last_click"] = (r, c)
        return new_h

    board = new_h["board"]
    board[sr][sc], board[r][c] = board[r][c], board[sr][sc]
    matches = _find_matches(board)
    if not matches:
        board[sr][sc], board[r][c] = board[r][c], board[sr][sc]
        new_h["selected"] = None
        new_h["invalid_swaps"] = new_h.get("invalid_swaps", 0) + 1
        if "lives" in level_conf.get("active_tags", []):
            new_h["lives"] = max(0, new_h.get("lives", level_conf.get("lives", 0)) - 1)
            new_h["lives_positive"] = new_h["lives"] > 0
        new_h["last_click"] = (r, c)
        return new_h

    _record_cleared_targets(new_h, matches)
    for mr, mc in matches:
        board[mr][mc] = EMPTY

    cascade_steps = 0
    all_matches = set(matches)
    if "cascade" in level_conf.get("active_tags", []):
        gravity_moved = False
        while True:
            if _apply_gravity(board):
                gravity_moved = True
            cascade_matches = _find_matches(board)
            if not cascade_matches:
                break
            cascade_steps += 1
            all_matches.update(cascade_matches)
            _record_cleared_targets(new_h, cascade_matches)
            for mr, mc in cascade_matches:
                board[mr][mc] = EMPTY
        if cascade_steps > 0 or gravity_moved:
            new_h["cascade_done"] = True
            new_h["cascade_count"] = new_h.get("cascade_count", 0) + max(1, cascade_steps)

    new_h["selected"] = None
    new_h["step"] = new_h.get("step", 0) + 1
    new_h["budget"] = max(0, new_h.get("budget", level_conf["budget"]) - 1)
    new_h["matches_made"] = new_h.get("matches_made", 0) + 1
    new_h["cleared_tiles"] = new_h.get("cleared_tiles", 0) + len(all_matches)
    new_h["last_match"] = sorted(all_matches)
    new_h["last_click"] = (r, c)
    _update_target_flags(new_h)
    return new_h


def predict(h_t: dict) -> dict:
    """Return minimal/empty z_t. This game is fully deterministic."""
    return {}


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    """Check if the current level's visible target cells are all empty."""
    if level not in LEVELS or h_t.get("level") != level:
        return False
    req = LEVELS[level].get("goal_requirements", {})
    if req.get("all_targets_clear") is not True:
        return False
    targets = LEVELS[level].get("targets", [])
    if not targets:
        return False
    cleared_set = set(tuple(p) for p in h_t.get("cleared_targets", []))
    board = h_t.get("board", [])
    for r, c in targets:
        if (r, c) not in cleared_set:
            if r >= len(board) or c >= len(board[r]) or board[r][c] != EMPTY:
                return False
    for key, expected in req.items():
        if key == "all_targets_clear":
            continue
        if h_t.get(key) != expected:
            return False
    return True


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    """Render the current state as a 64x64 grid."""
    grid = [[BG_COLOR for _ in range(64)] for _ in range(64)]
    level_conf = LEVELS[h_t["level"]]
    rows = level_conf["rows"]
    cols = level_conf["cols"]

    # board frame and target rings
    for r in range(rows):
        for c in range(cols):
            top = BOARD_TOP + r * CELL
            left = BOARD_LEFT + c * CELL
            for y in range(top - 1, top + TILE + 1):
                for x in range(left - 1, left + TILE + 1):
                    if 0 <= y < 64 and 0 <= x < 64 and (y in (top - 1, top + TILE) or x in (left - 1, left + TILE)):
                        grid[y][x] = COLORS["light_blue"]
    for idx, (r, c) in enumerate(level_conf["targets"]):
        top = BOARD_TOP + r * CELL
        left = BOARD_LEFT + c * CELL
        ring_color = COLORS["target"] if idx % 2 == 0 else COLORS["target_alt"]
        for x in range(left - 2, left + TILE + 2):
            if 0 <= top - 2 < 64 and 0 <= x < 64:
                grid[top - 2][x] = ring_color
            if 0 <= top + TILE + 1 < 64 and 0 <= x < 64:
                grid[top + TILE + 1][x] = ring_color
        for y in range(top - 2, top + TILE + 2):
            if 0 <= y < 64 and 0 <= left - 2 < 64:
                grid[y][left - 2] = ring_color
            if 0 <= y < 64 and 0 <= left + TILE + 1 < 64:
                grid[y][left + TILE + 1] = ring_color
        if (r, c) in set(tuple(p) for p in h_t.get("cleared_targets", [])):
            grid[top + 1][left + 1] = COLORS["green"]
            grid[top + 1][left + 2] = COLORS["green"]
            grid[top + 2][left + 1] = COLORS["green"]
            grid[top + 2][left + 2] = COLORS["green"]

    # visible elevator cascade arrows
    if "cascade" in level_conf.get("active_tags", []):
        for c in level_conf.get("cascade_columns", []):
            x = BOARD_LEFT + c * CELL + TILE // 2
            for r in range(rows - 1):
                y = BOARD_TOP + r * CELL + TILE + 1
                if 0 <= y < 64 and 1 <= x < 63:
                    grid[y][x] = COLORS["orange"]
                    grid[y + 1][x - 1] = COLORS["orange"]
                    grid[y + 1][x + 1] = COLORS["orange"]

    # dynamic tiles
    for r in range(rows):
        for c in range(cols):
            _draw_entity(grid, r, c, h_t["board"][r][c])

    # locked creams and their visible unlock marker
    if "locks" in level_conf.get("active_tags", []) and not h_t.get("locks_open", False):
        for r, c in level_conf.get("locked_cells", []):
            top = BOARD_TOP + r * CELL
            left = BOARD_LEFT + c * CELL
            for x in range(left - 2, left + TILE + 2):
                if 0 <= x < 64:
                    grid[top - 2][x] = COLORS["purple"]
                    grid[top + TILE + 1][x] = COLORS["purple"]
            for y in range(top - 2, top + TILE + 2):
                if 0 <= y < 64:
                    grid[y][left - 2] = COLORS["purple"]
                    grid[y][left + TILE + 1] = COLORS["purple"]
            grid[top + 1][left + 1] = COLORS["orange"]
            grid[top + 2][left + 2] = COLORS["orange"]
        for r, c in level_conf.get("unlock_targets", []):
            top = BOARD_TOP + r * CELL
            left = BOARD_LEFT + c * CELL
            grid[top - 2][left - 2] = COLORS["purple"]
            grid[top + TILE + 1][left + TILE + 1] = COLORS["purple"]

    # selection bracket
    if h_t.get("selected") is not None:
        r, c = h_t["selected"]
        top = BOARD_TOP + r * CELL
        left = BOARD_LEFT + c * CELL
        for x in range(left - 3, left + TILE + 3):
            if 0 <= x < 64:
                if 0 <= top - 3 < 64:
                    grid[top - 3][x] = COLORS["select"]
                if 0 <= top + TILE + 2 < 64:
                    grid[top + TILE + 2][x] = COLORS["select"]
        for y in range(top - 3, top + TILE + 3):
            if 0 <= y < 64:
                if 0 <= left - 3 < 64:
                    grid[y][left - 3] = COLORS["select"]
                if 0 <= left + TILE + 2 < 64:
                    grid[y][left + TILE + 2] = COLORS["select"]

    # HUD: target progress pips and budget bar
    total = len(level_conf["targets"])
    cleared = h_t.get("targets_cleared", 0)
    for i in range(total):
        col = 2 + i * 4
        color = COLORS["green"] if i < cleared else COLORS["orange"]
        for y in range(2, 5):
            for x in range(col, col + 3):
                grid[y][x] = color
    if "lives" in level_conf.get("active_tags", []):
        max_lives = level_conf.get("lives", 0)
        lives = h_t.get("lives", max_lives)
        for i in range(max_lives):
            col = 46 + i * 5
            color = COLORS["pink"] if i < lives else COLORS["light_pink"]
            grid[2][col + 1] = color
            grid[2][col + 2] = color
            grid[3][col] = color
            grid[3][col + 1] = color
            grid[3][col + 2] = color
            grid[3][col + 3] = color
            grid[4][col + 1] = color
            grid[4][col + 2] = color
    budget_total = max(1, level_conf["budget"])
    rem = max(0, h_t.get("budget", budget_total))
    length = int(60 * rem / budget_total)
    for x in range(2, 62):
        grid[62][x] = COLORS["light_pink"]
    for x in range(2, 2 + length):
        grid[62][x] = COLORS["pink"]

    # Optional observability mask for future levels.
    fog_radius = level_conf.get("fog_radius")
    if fog_radius is not None and h_t.get("last_click") is not None:
        lr, lc = h_t["last_click"]
        cy = BOARD_TOP + lr * CELL + TILE // 2
        cx = BOARD_LEFT + lc * CELL + TILE // 2
        radius_px = fog_radius * CELL
        for y in range(64):
            for x in range(64):
                if abs(y - cy) + abs(x - cx) > radius_px:
                    grid[y][x] = BG_COLOR
    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    """Get the initial (h_t, z_t) for a given level."""
    conf = LEVELS[level]
    h_t = {
        "level": level,
        "step": 0,
        "budget": conf["budget"],
        "board": copy.deepcopy(conf["board"]),
        "selected": None,
        "targets_cleared": 0,
        "all_targets_clear": False,
        "complete": False,
        "matches_made": 0,
        "cleared_tiles": 0,
        "invalid_swaps": 0,
        "last_match": [],
        "last_click": None,
        "locks_open": "locks" not in conf.get("active_tags", []),
        "cascade_done": "cascade" not in conf.get("active_tags", []),
        "cascade_count": 0,
        "cleared_targets": [],
        "lives": conf.get("lives", 0),
        "lives_positive": True,
    }
    _update_target_flags(h_t)
    return h_t, predict(h_t)


def get_available_actions() -> list[int]:
    """Return available action integers for this game."""
    return [0, 6]


def solve_level(level: int) -> list:
    """Return a fixed sequence of actions that solves this level."""
    def click(r, c):
        return (6, BOARD_LEFT + c * CELL + 2, BOARD_TOP + r * CELL + 2)
    if level == 0:
        return [
            click(0, 2), click(1, 2),  # pink row target
            click(3, 3), click(3, 4),  # blue column target
            click(4, 0), click(4, 1),  # green column target
            click(3, 2), click(3, 3),  # yellow column target
        ]
    if level == 1:
        return [
            click(0, 3), click(1, 3),  # clear unlock target
            click(1, 2), click(2, 2),  # use released locked cream
            click(3, 4), click(3, 5),  # blue column target
            click(4, 1), click(4, 2),  # green column target
            click(3, 3), click(3, 4),  # yellow column target
        ]
    if level == 2:
        return [
            click(2, 2), click(3, 2),  # orange row match starts elevator cascade
            click(3, 4), click(3, 5),  # blue right-column order
            click(4, 5), click(5, 5),  # yellow row order after the drop
        ]
    if level == 3:
        return [
            click(0, 4), click(1, 4),  # unlock with pink target order
            click(5, 1), click(4, 1),  # clear released locked orange/green edge order
            click(3, 5), click(3, 6),  # blue right-column target
            click(4, 5), click(5, 5),  # yellow target order after cascade drops
        ]
    if level == 4:
        return [
            click(0, 2), click(1, 2),  # pink top target
            click(3, 5), click(3, 6),  # blue right-side target
            click(5, 0), click(5, 1),  # green lower-left target
            click(5, 5), click(6, 5),  # yellow bottom target
            click(2, 4), click(3, 4),  # purple center target
        ]
    if level == 5:
        return [
            click(0, 2), click(1, 2),  # pink top order
            click(1, 6), click(1, 5),  # blue right order
            click(0, 4), click(1, 4),  # yellow upper order
            click(1, 2), click(2, 2),  # purple left order after gaps
            click(6, 5), click(5, 5),  # bottom yellow order and cascade fall
        ]
    if level == 6:
        return [
            click(0, 2), click(1, 2),  # top pink order
            click(0, 5), click(1, 5),  # top yellow order
            click(1, 2), click(1, 3),  # remembered purple order
            click(1, 6), click(1, 7),  # right blue order with fall
            click(6, 5), click(5, 5),  # lower yellow order
        ]
    if level == 7:
        return [
            click(0, 2), click(1, 2),  # top pink order
            click(0, 5), click(1, 5),  # top yellow order
            click(1, 2), click(1, 3),  # remembered purple order
            click(1, 6), click(1, 7),  # right blue order, first fall
            click(6, 5), click(5, 5),  # lower yellow order, second fall
            click(7, 2), click(7, 3),  # bottom green order, third fall
        ]
    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Cl0426(_FunctionalArcGame):
    GAME_ID = "cl0426-c5dfa3ac"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
