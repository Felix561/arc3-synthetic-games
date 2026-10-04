# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the os1842/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy

TITLE = "Orbit Signal Loom"
SHORT_NAME = "OS1842"

BG_COLOR = 0
CELL = 5
TARGET_ORIGIN = (7, 1)
EDIT_ORIGIN = (7, 16)

COLORS = {
    "bg": 0,
    "frame": 5,
    "soft_frame": 2,
    "locked": 13,
    "locked_mark": 4,
    "row_switch": 15,
    "col_switch": 12,
    "orbit_switch": 6,
    "connector": 1,
    "hud": 10,
    "hud_warn": 8,
    "blank": 3,
}

VALUE_COLORS = [9, 8, 14, 11, 15]

LEVELS = {
    0: {
        "n": 2,
        "palette_count": 3,
        "initial": [[0, 0], [0, 0]],
        "target": [[1, 2], [0, 1]],
        "locked": [],
        "switches": [],
        "budget": 14,
        "active_tags": [],
        "goal_requirements": {"board_matches_target": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["board_matches_target"],
            "primary_blocker": "editable prism colors start different from the proof pattern",
            "dependencies": ["cycle three different prism tiles until their colors match the proof"],
            "feedback": "each clicked tile visibly cycles blue-red-green",
            "bypass_guard": "completion is the exact visible board-to-target equality check",
        },
    },
    1: {
        "n": 3,
        "palette_count": 3,
        "initial": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        "target": [[2, 1, 0], [1, 2, 1], [0, 1, 2]],
        "locked": [],
        "switches": [],
        "budget": 20,
        "active_tags": [],
        "goal_requirements": {"board_matches_target": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["board_matches_target"],
            "primary_blocker": "nine-cell proof contains mixed colors",
            "dependencies": ["compare each live tile against its proof tile", "cycle only mismatched cells"],
            "feedback": "every corrected tile visibly matches its left-side counterpart",
            "bypass_guard": "there is no finish button; only exact pattern equality wins",
        },
    },
    2: {
        "n": 3,
        "palette_count": 3,
        "initial": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        "target": [[2, 0, 1], [1, 1, 1], [0, 2, 0]],
        "locked": [(1, 0), (1, 1), (1, 2)],
        "switches": [{"kind": "row", "index": 1, "delta": 1}],
        "budget": 15,
        "active_tags": ["switch"],
        "goal_requirements": {"board_matches_target": True, "locked_cells_matched": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["board_matches_target", "locked_cells_matched"],
            "primary_blocker": "middle row is locked and cannot be cycled directly",
            "dependencies": ["use the purple row switch once", "then directly repair remaining unlocked cells"],
            "feedback": "the connected locked row changes color when its switch is clicked",
            "bypass_guard": "locked row cells ignore direct tile clicks, so the visible target row is unreachable without the switch",
        },
    },
    3: {
        "n": 3,
        "palette_count": 3,
        "initial": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        "target": [[1, 0, 2], [0, 2, 2], [1, 1, 2]],
        "locked": [(0, 2), (1, 2), (2, 2)],
        "switches": [{"kind": "col", "index": 2, "delta": 1}],
        "budget": 15,
        "active_tags": ["switch"],
        "goal_requirements": {"board_matches_target": True, "locked_cells_matched": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["board_matches_target", "locked_cells_matched"],
            "primary_blocker": "right column is locked and must become color value two",
            "dependencies": ["click orange column switch twice", "fix four remaining unlocked cells"],
            "feedback": "the marked column changes after each switch activation",
            "bypass_guard": "locked column cells cannot be directly edited, preventing early exact match",
        },
    },
    4: {
        "n": 3,
        "palette_count": 4,
        "initial": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        "target": [[1, 3, 1], [2, 2, 0], [0, 2, 3]],
        "locked": [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
        "switches": [{"kind": "row", "index": 0, "delta": 1}, {"kind": "col", "index": 1, "delta": 1}],
        "budget": 17,
        "active_tags": ["switch"],
        "goal_requirements": {"board_matches_target": True, "locked_cells_matched": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["board_matches_target", "locked_cells_matched"],
            "primary_blocker": "locked top row and locked center column require two different switches",
            "dependencies": ["activate row switch once", "activate column switch twice", "repair two unlocked endpoints"],
            "feedback": "row and column connectors show exactly which cells each switch controls",
            "bypass_guard": "the locked cross cannot be matched by direct clicks",
        },
    },
    5: {
        "n": 3,
        "palette_count": 4,
        "initial": [[1, 2, 0], [3, 0, 0], [0, 0, 0]],
        "target": [[3, 1, 0], [0, 2, 2], [1, 3, 0]],
        "locked": [(0, 0), (0, 1), (1, 0), (1, 1)],
        "switches": [{"kind": "orbit", "block": (0, 0)}],
        "budget": 16,
        "active_tags": ["switch"],
        "goal_requirements": {"board_matches_target": True, "locked_cells_matched": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["board_matches_target", "locked_cells_matched"],
            "primary_blocker": "locked 2x2 archive block has correct colors in wrong orbit order",
            "dependencies": ["click pink orbit switch once", "cycle three unlocked support tiles"],
            "feedback": "pink corner marks outline the rotating 2x2 block",
            "bypass_guard": "direct clicks cannot alter the locked archive block arrangement",
        },
    },
    6: {
        "n": 3,
        "palette_count": 4,
        "initial": [[0, 1, 0], [2, 0, 0], [0, 0, 3]],
        "target": [[1, 0, 2], [3, 1, 2], [3, 2, 0]],
        "locked": [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)],
        "switches": [
            {"kind": "col", "index": 2, "delta": 1},
            {"kind": "row", "index": 0, "delta": 1},
            {"kind": "orbit", "block": (0, 1)},
        ],
        "budget": 18,
        "active_tags": ["switch"],
        "goal_requirements": {"board_matches_target": True, "locked_cells_matched": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["board_matches_target", "locked_cells_matched"],
            "primary_blocker": "locked cells need a chained column charge, row charge, then orbit rearrangement",
            "dependencies": ["charge column two", "charge row zero", "orbit the upper-right 2x2", "repair three unlocked cells"],
            "feedback": "each switch has a visible connector and the orbit block has pink corners",
            "bypass_guard": "the locked dependency chain cannot be reproduced with direct cycling",
        },
    },
    7: {
        "n": 3,
        "palette_count": 5,
        "initial": [[0, 1, 2], [3, 0, 1], [2, 3, 4]],
        "target": [[1, 4, 4], [3, 1, 3], [3, 2, 0]],
        "locked": [(0, 0), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1)],
        "switches": [
            {"kind": "row", "index": 1, "delta": 1},
            {"kind": "col", "index": 0, "delta": 1},
            {"kind": "orbit", "block": (1, 0)},
        ],
        "budget": 20,
        "active_tags": ["switch"],
        "goal_requirements": {"board_matches_target": True, "locked_cells_matched": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["board_matches_target", "locked_cells_matched"],
            "primary_blocker": "six locked cells require row cycling, column cycling, and a lower orbit rotation before direct tile work",
            "dependencies": [
                "activate row one twice",
                "activate column zero once",
                "orbit the lower-left 2x2 block",
                "repair the three unlocked top/right tiles",
            ],
            "feedback": "row, column, and orbit markings all remain visible around affected regions",
            "bypass_guard": "final equality is impossible by direct clicks because most required cells are locked behind switches",
        },
    },
}


def _draw_entity(grid, row, col, entity_type):
    """Draw one chunky 5x5 entity with a distinctive pixel identity."""
    if isinstance(entity_type, tuple):
        kind, value, locked = entity_type
        value_color = VALUE_COLORS[value % len(VALUE_COLORS)]

        if kind == "target_tile":
            for r in range(CELL):
                for c in range(CELL):
                    rr = row + r
                    cc = col + c
                    if 0 <= rr < 32 and 0 <= cc < 32:
                        if r == 0 or c == 0 or r == CELL - 1 or c == CELL - 1:
                            grid[rr][cc] = COLORS["frame"]
                        elif r == 2 and c == 2:
                            grid[rr][cc] = COLORS["bg"]
                        else:
                            grid[rr][cc] = value_color
            return

        if kind == "edit_tile":
            border = COLORS["locked"] if locked else COLORS["soft_frame"]
            for r in range(CELL):
                for c in range(CELL):
                    rr = row + r
                    cc = col + c
                    if 0 <= rr < 32 and 0 <= cc < 32:
                        if r == 0 or c == 0 or r == CELL - 1 or c == CELL - 1:
                            grid[rr][cc] = border
                        elif locked and (r == c or r + c == CELL - 1):
                            grid[rr][cc] = COLORS["locked_mark"]
                        else:
                            grid[rr][cc] = value_color
            return

    if entity_type == "row_switch":
        for r in range(CELL):
            for c in range(CELL):
                rr = row + r
                cc = col + c
                if 0 <= rr < 32 and 0 <= cc < 32:
                    if r == 2 or c in (1, 3):
                        grid[rr][cc] = COLORS["row_switch"]
                    elif r in (0, 4) or c in (0, 4):
                        grid[rr][cc] = COLORS["frame"]
                    else:
                        grid[rr][cc] = COLORS["bg"]
        return

    if entity_type == "col_switch":
        for r in range(CELL):
            for c in range(CELL):
                rr = row + r
                cc = col + c
                if 0 <= rr < 32 and 0 <= cc < 32:
                    if c == 2 or r in (1, 3):
                        grid[rr][cc] = COLORS["col_switch"]
                    elif r in (0, 4) or c in (0, 4):
                        grid[rr][cc] = COLORS["frame"]
                    else:
                        grid[rr][cc] = COLORS["bg"]
        return

    if entity_type == "orbit_switch":
        for r in range(CELL):
            for c in range(CELL):
                rr = row + r
                cc = col + c
                if 0 <= rr < 32 and 0 <= cc < 32:
                    if (r in (0, 4) and c in (1, 2, 3)) or (c in (0, 4) and r in (1, 2, 3)):
                        grid[rr][cc] = COLORS["orbit_switch"]
                    elif (r, c) in ((1, 3), (2, 4), (3, 3)):
                        grid[rr][cc] = COLORS["frame"]
                    else:
                        grid[rr][cc] = COLORS["bg"]


def _update_flags(h_t):
    cfg = LEVELS[h_t["level"]]
    board = h_t["board"]
    target = cfg["target"]

    board_match = board == target
    locked_match = True
    for r, c in cfg.get("locked", []):
        if board[r][c] != target[r][c]:
            locked_match = False
            break

    h_t["board_matches_target"] = board_match
    h_t["locked_cells_matched"] = locked_match
    h_t["requirements_met"] = board_match and locked_match
    return h_t


def _click_to_tile(x, y, origin, n):
    row0, col0 = origin
    if col0 <= x < col0 + n * CELL and row0 <= y < row0 + n * CELL:
        r = (y - row0) // CELL
        c = (x - col0) // CELL
        return int(r), int(c)
    return None


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    """Deterministic history state update for the click-only pattern game."""
    new_h = copy.deepcopy(h_t)

    if a_t == 0:
        reset_h, _ = get_initial_state(h_t["level"])
        return reset_h

    if not (isinstance(a_t, tuple) and len(a_t) == 3 and a_t[0] == 6):
        return new_h

    cfg = LEVELS[new_h["level"]]
    if new_h.get("step", 0) >= cfg["budget"]:
        return new_h

    x = int(a_t[1])
    y = int(a_t[2])
    n = cfg["n"]
    palette_count = cfg["palette_count"]
    acted = False

    if "switch" in cfg.get("active_tags", []):
        for sw_index, sw in enumerate(cfg.get("switches", [])):
            if sw["kind"] == "row":
                r = sw["index"]
                sw_row = EDIT_ORIGIN[0] + r * CELL
                sw_col = EDIT_ORIGIN[1] - CELL
                if sw_col <= x < sw_col + CELL and sw_row <= y < sw_row + CELL:
                    for c in range(n):
                        new_h["board"][r][c] = (new_h["board"][r][c] + sw.get("delta", 1)) % palette_count
                    key = "s" + str(sw_index)
                    new_h["switch_counts"][key] = new_h["switch_counts"].get(key, 0) + 1
                    acted = True
                    break

            elif sw["kind"] == "col":
                c = sw["index"]
                sw_row = EDIT_ORIGIN[0] - CELL
                sw_col = EDIT_ORIGIN[1] + c * CELL
                if sw_col <= x < sw_col + CELL and sw_row <= y < sw_row + CELL:
                    for r in range(n):
                        new_h["board"][r][c] = (new_h["board"][r][c] + sw.get("delta", 1)) % palette_count
                    key = "s" + str(sw_index)
                    new_h["switch_counts"][key] = new_h["switch_counts"].get(key, 0) + 1
                    acted = True
                    break

            elif sw["kind"] == "orbit":
                br, bc = sw["block"]
                sw_row = EDIT_ORIGIN[0] + n * CELL
                sw_col = EDIT_ORIGIN[1] + bc * CELL
                if sw_col <= x < sw_col + CELL and sw_row <= y < sw_row + CELL:
                    if 0 <= br < n - 1 and 0 <= bc < n - 1:
                        a = new_h["board"][br][bc]
                        b = new_h["board"][br][bc + 1]
                        cval = new_h["board"][br + 1][bc + 1]
                        d = new_h["board"][br + 1][bc]
                        new_h["board"][br][bc] = d
                        new_h["board"][br][bc + 1] = a
                        new_h["board"][br + 1][bc + 1] = b
                        new_h["board"][br + 1][bc] = cval
                        key = "s" + str(sw_index)
                        new_h["switch_counts"][key] = new_h["switch_counts"].get(key, 0) + 1
                        acted = True
                    break

    if not acted:
        tile = _click_to_tile(x, y, EDIT_ORIGIN, n)
        if tile is not None:
            r, c = tile
            locked = set(tuple(p) for p in cfg.get("locked", []))
            if (r, c) not in locked:
                new_h["board"][r][c] = (new_h["board"][r][c] + 1) % palette_count
                acted = True

    if acted:
        new_h["step"] += 1
        _update_flags(new_h)

    return new_h


def predict(h_t: dict, seed: int) -> dict:
    """Return exactly {}. This game is fully deterministic."""
    return {}


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    """Check exact visible pattern completion within budget and declared requirements."""
    if h_t.get("level") != level:
        return False

    cfg = LEVELS[level]
    if h_t.get("step", 0) > cfg["budget"]:
        return False

    board = h_t.get("board")
    target = cfg["target"]
    if board != target:
        return False

    locked_match = True
    for r, c in cfg.get("locked", []):
        if board[r][c] != target[r][c]:
            locked_match = False
            break

    computed = {
        "board_matches_target": board == target,
        "locked_cells_matched": locked_match,
    }

    for key, required_value in cfg.get("goal_requirements", {}).items():
        if computed.get(key) != required_value:
            return False

    return True


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    """Render the current state as a 32x32 grid."""
    grid = [[BG_COLOR for _ in range(32)] for _ in range(32)]

    cfg = LEVELS[h_t["level"]]
    n = cfg["n"]
    tr, tc = TARGET_ORIGIN
    er, ec = EDIT_ORIGIN

    budget = cfg["budget"]
    remaining = max(0, budget - h_t.get("step", 0))
    fill = int(remaining * 32 / budget) if budget > 0 else 0
    hud_color = COLORS["hud"] if remaining > 2 else COLORS["hud_warn"]

    for c in range(32):
        grid[0][c] = hud_color if c < fill else COLORS["soft_frame"]

    for r in range(1, 31):
        grid[r][0] = COLORS["soft_frame"] if r % 2 == 0 else BG_COLOR
        grid[r][31] = COLORS["soft_frame"] if r % 2 == 0 else BG_COLOR

    if "switch" in cfg.get("active_tags", []):
        for sw in cfg.get("switches", []):
            if sw["kind"] == "row":
                r = sw["index"]
                y = er + r * CELL + CELL // 2
                for x in range(ec, ec + n * CELL):
                    if 0 <= y < 32 and 0 <= x < 32:
                        grid[y][x] = COLORS["connector"]

            elif sw["kind"] == "col":
                c = sw["index"]
                x = ec + c * CELL + CELL // 2
                for y in range(er, er + n * CELL):
                    if 0 <= y < 32 and 0 <= x < 32:
                        grid[y][x] = COLORS["connector"]

            elif sw["kind"] == "orbit":
                br, bc = sw["block"]
                rr = er + br * CELL
                cc = ec + bc * CELL
                for i in range(2 * CELL):
                    for pr, pc in [
                        (rr, cc + i),
                        (rr + 2 * CELL - 1, cc + i),
                        (rr + i, cc),
                        (rr + i, cc + 2 * CELL - 1),
                    ]:
                        if 0 <= pr < 32 and 0 <= pc < 32:
                            grid[pr][pc] = COLORS["orbit_switch"]

    locked = set(tuple(p) for p in cfg.get("locked", []))

    for r in range(n):
        for c in range(n):
            _draw_entity(grid, tr + r * CELL, tc + c * CELL, ("target_tile", cfg["target"][r][c], False))
            is_locked = (r, c) in locked
            _draw_entity(grid, er + r * CELL, ec + c * CELL, ("edit_tile", h_t["board"][r][c], is_locked))

    if "switch" in cfg.get("active_tags", []):
        for sw in cfg.get("switches", []):
            if sw["kind"] == "row":
                _draw_entity(grid, er + sw["index"] * CELL, ec - CELL, "row_switch")
            elif sw["kind"] == "col":
                _draw_entity(grid, er - CELL, ec + sw["index"] * CELL, "col_switch")
            elif sw["kind"] == "orbit":
                _draw_entity(grid, er + n * CELL, ec + sw["block"][1] * CELL, "orbit_switch")

    solved = check_level_complete(h_t, {}, h_t["level"])
    for c in range(32):
        grid[31][c] = COLORS["hud"] if solved else COLORS["soft_frame"]

    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    """Get the initial deterministic state for a level."""
    cfg = LEVELS[level]
    board = copy.deepcopy(cfg["initial"])
    target = cfg["target"]

    board_match = board == target
    locked_match = True
    for r, c in cfg.get("locked", []):
        if board[r][c] != target[r][c]:
            locked_match = False
            break

    h_t = {
        "level": level,
        "step": 0,
        "board": board,
        "switch_counts": {},
        "board_matches_target": board_match,
        "locked_cells_matched": locked_match,
        "requirements_met": board_match and locked_match,
    }
    return h_t, {}


def get_available_actions() -> list[int]:
    """Return available base actions: reset and spatial click."""
    return [0, 6]


def solve_level(level: int) -> list:
    """Return a fixed sequence of click actions that solves each level."""

    def tile(r, c):
        return (6, EDIT_ORIGIN[1] + c * CELL + CELL // 2, EDIT_ORIGIN[0] + r * CELL + CELL // 2)

    def row_sw(r):
        return (6, EDIT_ORIGIN[1] - CELL + CELL // 2, EDIT_ORIGIN[0] + r * CELL + CELL // 2)

    def col_sw(c):
        return (6, EDIT_ORIGIN[1] + c * CELL + CELL // 2, EDIT_ORIGIN[0] - CELL + CELL // 2)

    def orbit_sw(block_r, block_c, n=3):
        return (6, EDIT_ORIGIN[1] + block_c * CELL + CELL // 2, EDIT_ORIGIN[0] + n * CELL + CELL // 2)

    if level == 0:
        return [
            tile(0, 0),
            tile(0, 1),
            tile(0, 1),
            tile(1, 1),
        ]

    if level == 1:
        return [
            tile(0, 0),
            tile(0, 0),
            tile(0, 1),
            tile(1, 0),
            tile(1, 1),
            tile(1, 1),
            tile(1, 2),
            tile(2, 1),
            tile(2, 2),
            tile(2, 2),
        ]

    if level == 2:
        return [
            row_sw(1),
            tile(0, 0),
            tile(0, 0),
            tile(0, 2),
            tile(2, 1),
            tile(2, 1),
        ]

    if level == 3:
        return [
            col_sw(2),
            col_sw(2),
            tile(0, 0),
            tile(1, 1),
            tile(1, 1),
            tile(2, 0),
            tile(2, 1),
        ]

    if level == 4:
        return [
            row_sw(0),
            col_sw(1),
            col_sw(1),
            tile(1, 0),
            tile(1, 0),
            tile(2, 2),
            tile(2, 2),
            tile(2, 2),
        ]

    if level == 5:
        return [
            orbit_sw(0, 0),
            tile(1, 2),
            tile(1, 2),
            tile(2, 0),
            tile(2, 1),
            tile(2, 1),
            tile(2, 1),
        ]

    if level == 6:
        return [
            col_sw(2),
            row_sw(0),
            orbit_sw(0, 1),
            tile(2, 0),
            tile(2, 0),
            tile(2, 0),
            tile(2, 1),
            tile(2, 1),
            tile(1, 0),
        ]

    if level == 7:
        return [
            row_sw(1),
            row_sw(1),
            col_sw(0),
            orbit_sw(1, 0),
            tile(0, 1),
            tile(0, 1),
            tile(0, 1),
            tile(0, 2),
            tile(0, 2),
            tile(2, 2),
        ]

    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Os1842(_FunctionalArcGame):
    GAME_ID = "os1842-ca39ae90"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
