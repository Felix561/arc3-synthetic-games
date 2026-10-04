# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the ps1842/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy

BG_COLOR = 0

COLORS = {
    "bg": 0,
    "ui_empty": 1,
    "frame": 5,
    "pin": 13,
    "switch": 15,
    "complete": 14,
    "budget": 9,
    "bad": 8,
    "blue": 9,
    "red": 8,
    "green": 14,
    "yellow": 11,
    "purple": 15,
    "pink": 6,
    "orange": 12,
    "light_blue": 10,
}

ORBIT_MARK_COLORS = [15, 10, 11, 6, 12]
ORBIT_MARK_SLOTS = [
    [(0, 2), (0, 3), (0, 4)],
    [(2, 6), (3, 6), (4, 6)],
    [(6, 2), (6, 3), (6, 4)],
    [(2, 0), (3, 0), (4, 0)],
]

TILE = 7
BOARD_ROW = 7
BOARD_COL = 2

LEVELS = {
    0: {
        "rows": 1,
        "cols": 3,
        "palette": [9, 8],
        "initial": [0, 0, 0],
        "target_indices": [1, 0, 1],
        "switches": {},
        "locked": [],
        "budget": 8,
        "active_tags": [],
        "goal_requirements": {
            "matches_target": True,
            "current": [1, 0, 1],
        },
        "solution_indices": [0, 2],
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "matches_target",
            "primary_blocker": "two live prism cores begin with the wrong signal color",
            "dependencies": ["compare each archive ring to its live core", "cycle only the mismatched tiles"],
            "feedback": "the clicked core color changes locally; the bottom row turns green when all cores match",
            "bypass_guard": "completion is the visible exact equality of every core and its target ring",
        },
    },
    1: {
        "rows": 2,
        "cols": 3,
        "palette": [9, 8, 14],
        "initial": [0, 0, 0, 0, 0, 0],
        "target_indices": [0, 1, 2, 2, 1, 0],
        "switches": {},
        "locked": [],
        "budget": 13,
        "active_tags": [],
        "goal_requirements": {
            "matches_target": True,
            "current": [0, 1, 2, 2, 1, 0],
        },
        "solution_indices": [1, 2, 2, 3, 3, 4],
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "matches_target",
            "primary_blocker": "the archive forms a mirrored three-color pattern that the blank board lacks",
            "dependencies": ["identify one-step red targets", "identify two-step green targets"],
            "feedback": "each clicked free tile advances its live core through the prism palette",
            "bypass_guard": "no terminal button exists; success only appears when the displayed pattern is exact",
        },
    },
    2: {
        "rows": 2,
        "cols": 3,
        "palette": [9, 8, 14],
        "initial": [0, 0, 0, 0, 0, 0],
        "target_indices": [1, 1, 1, 0, 1, 0],
        "switches": {0: [0, 1, 2]},
        "locked": [0, 1, 2],
        "budget": 8,
        "active_tags": ["switch"],
        "goal_requirements": {
            "matches_target": True,
            "current": [1, 1, 1, 0, 1, 0],
        },
        "solution_indices": [0, 4],
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "matches_target",
            "primary_blocker": "the top archive row is locked and cannot be cycled tile by tile",
            "dependencies": ["activate the purple switch tile to advance the locked row", "cycle the remaining free red tile"],
            "feedback": "switch-marked tile advances every locked tile in its orbit together",
            "bypass_guard": "locked top-row cores ignore direct non-switch cycling, so the target row requires the switch",
        },
    },
    3: {
        "rows": 2,
        "cols": 4,
        "palette": [9, 8, 14],
        "initial": [0, 0, 0, 0, 0, 0, 0, 0],
        "target_indices": [2, 2, 1, 0, 0, 2, 1, 1],
        "switches": {0: [0, 1], 7: [6, 7]},
        "locked": [0, 1, 6, 7],
        "budget": 13,
        "active_tags": ["switch"],
        "goal_requirements": {
            "matches_target": True,
            "current": [2, 2, 1, 0, 0, 2, 1, 1],
        },
        "solution_indices": [0, 0, 2, 5, 5, 7],
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "matches_target",
            "primary_blocker": "two separate locked mirror pairs require different switch counts",
            "dependencies": ["set the left mirror pair to green", "set the right mirror pair to red", "repair free singleton mismatches"],
            "feedback": "each switch orbit changes as a pair while free cores change individually",
            "bypass_guard": "the locked pairs cannot be matched by clicking their partner tiles directly",
        },
    },
    4: {
        "rows": 3,
        "cols": 4,
        "palette": [9, 8, 14, 11],
        "initial": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "target_indices": [1, 2, 3, 2, 1, 0, 2, 2, 1, 3, 0, 2],
        "switches": {0: [0, 4, 8], 3: [3, 7, 11]},
        "locked": [0, 4, 8, 3, 7, 11],
        "budget": 21,
        "active_tags": ["switch"],
        "goal_requirements": {
            "matches_target": True,
            "current": [1, 2, 3, 2, 1, 0, 2, 2, 1, 3, 0, 2],
        },
        "solution_indices": [0, 3, 3, 1, 1, 2, 2, 2, 6, 6, 9, 9, 9],
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "matches_target",
            "primary_blocker": "both outer columns are switch-locked at different target depths",
            "dependencies": ["set left column once", "set right column twice", "then fill interior target colors"],
            "feedback": "locked columns visibly rotate together while interior cores remain independently editable",
            "bypass_guard": "outer-column targets are unreachable without their column switches",
        },
    },
    5: {
        "rows": 3,
        "cols": 4,
        "palette": [9, 8, 14, 11],
        "initial": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "target_indices": [3, 2, 1, 2, 1, 2, 1, 3, 2, 2, 1, 3],
        "switches": {0: [0, 11], 5: [1, 5, 9], 10: [2, 6, 10]},
        "locked": [0, 11, 1, 5, 9, 2, 6, 10],
        "budget": 21,
        "active_tags": ["switch"],
        "goal_requirements": {
            "matches_target": True,
            "current": [3, 2, 1, 2, 1, 2, 1, 3, 2, 2, 1, 3],
        },
        "solution_indices": [0, 0, 0, 5, 5, 10, 3, 3, 4, 7, 7, 7, 8, 8],
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "matches_target",
            "primary_blocker": "mirror corners and two vertical signal columns are all switch-linked",
            "dependencies": ["set amber mirror corners", "set green center column orbit", "set red right-column orbit", "cycle remaining free tiles"],
            "feedback": "each purple switch changes a distinct visible orbit shape",
            "bypass_guard": "mirror and column locked cells cannot be directly adjusted outside their switch orbits",
        },
    },
    6: {
        "rows": 3,
        "cols": 4,
        "palette": [9, 8, 14, 11, 15],
        "initial": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "target_indices": [1, 1, 3, 4, 1, 2, 3, 2, 2, 1, 3, 2],
        "switches": {0: [0, 1, 4], 6: [2, 6, 10], 11: [7, 8, 11]},
        "locked": [0, 1, 4, 2, 6, 10, 7, 8, 11],
        "budget": 20,
        "active_tags": ["switch"],
        "goal_requirements": {
            "matches_target": True,
            "current": [1, 1, 3, 4, 1, 2, 3, 2, 2, 1, 3, 2],
        },
        "solution_indices": [0, 6, 6, 6, 11, 11, 3, 3, 3, 3, 5, 5, 9],
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "matches_target",
            "primary_blocker": "five-color palette makes switch counts wrap if chosen carelessly",
            "dependencies": ["set red L-orbit", "set yellow column orbit", "set green lower orbit", "finish purple, green, and red free cores"],
            "feedback": "locked orbits advance through five visibly distinct prism colors",
            "bypass_guard": "most targets are pinned to switch orbits, so free cycling cannot bypass switch planning",
        },
    },
    7: {
        "rows": 3,
        "cols": 4,
        "palette": [9, 8, 14, 11, 15],
        "initial": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "target_indices": [1, 1, 2, 2, 4, 1, 2, 3, 3, 3, 1, 1],
        "switches": {0: [0, 1, 4, 5], 3: [2, 3, 6, 7], 8: [4, 8, 9], 11: [7, 10, 11]},
        "locked": [0, 1, 4, 5, 2, 3, 6, 7, 8, 9, 10, 11],
        "budget": 13,
        "active_tags": ["switch"],
        "goal_requirements": {
            "matches_target": True,
            "current": [1, 1, 2, 2, 4, 1, 2, 3, 3, 3, 1, 1],
        },
        "solution_indices": [0, 3, 3, 8, 8, 8, 11],
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "matches_target",
            "primary_blocker": "every prism is locked into one of four switch-orbit equations",
            "dependencies": ["apply the left block switch once", "apply the right block switch twice", "apply the lower-left switch three times", "apply the lower-right switch once"],
            "feedback": "overlap cells reveal combined switch effects by changing to later palette colors",
            "bypass_guard": "all cells are locked; the board can only reach the visible terminal pattern through switch activations",
        },
    },
}


def _matches_target_for_level(level, current):
    cfg = LEVELS[level]
    return list(current) == list(cfg["target_indices"])


def _refresh_goal_state(h_t):
    level = h_t["level"]
    h_t["matches_target"] = _matches_target_for_level(level, h_t.get("current", []))
    return h_t


def _orbit_memberships(cfg):
    memberships = {idx: [] for idx in range(cfg["rows"] * cfg["cols"])}
    for group_number, switch_idx in enumerate(sorted(cfg.get("switches", {}))):
        for controlled_idx in cfg["switches"][switch_idx]:
            memberships.setdefault(controlled_idx, []).append(group_number)
        memberships.setdefault(switch_idx, []).append(group_number)
    return memberships


def _draw_orbit_markers(grid, row, col, group_numbers):
    seen = []
    for group_number in group_numbers:
        if group_number not in seen:
            seen.append(group_number)
    for slot_index, group_number in enumerate(seen[:len(ORBIT_MARK_SLOTS)]):
        color = ORBIT_MARK_COLORS[group_number % len(ORBIT_MARK_COLORS)]
        for dr, dc in ORBIT_MARK_SLOTS[slot_index]:
            rr = row + dr
            cc = col + dc
            if 0 <= rr < 32 and 0 <= cc < 32:
                grid[rr][cc] = color


def _draw_entity(grid, row, col, entity_type):
    kind = entity_type[0] if isinstance(entity_type, tuple) else entity_type

    if kind == "lamp":
        target_color = entity_type[1]
        current_color = entity_type[2]
        is_switch = entity_type[3]
        is_locked = entity_type[4]
        matched = entity_type[5]

        for rr in range(row, row + TILE):
            for cc in range(col, col + TILE):
                if 0 <= rr < 32 and 0 <= cc < 32:
                    grid[rr][cc] = COLORS["frame"]

        for rr in range(row + 1, row + TILE - 1):
            for cc in range(col + 1, col + TILE - 1):
                if 0 <= rr < 32 and 0 <= cc < 32:
                    if rr == row + 1 or rr == row + TILE - 2 or cc == col + 1 or cc == col + TILE - 2:
                        grid[rr][cc] = target_color
                    else:
                        grid[rr][cc] = BG_COLOR

        for rr in range(row + 3, row + 6):
            for cc in range(col + 3, col + 6):
                if 0 <= rr < 32 and 0 <= cc < 32 and rr < row + TILE - 1 and cc < col + TILE - 1:
                    grid[rr][cc] = current_color

        if matched and 0 <= row + 3 < 32 and 0 <= col + 3 < 32:
            grid[row + 3][col + 3] = current_color

        if is_locked:
            pins = [
                (row, col),
                (row, col + TILE - 1),
                (row + TILE - 1, col),
                (row + TILE - 1, col + TILE - 1),
            ]
            for rr, cc in pins:
                if 0 <= rr < 32 and 0 <= cc < 32:
                    grid[rr][cc] = COLORS["pin"]

        if is_switch:
            s = COLORS["switch"]
            marks = [
                (1, 1), (1, 5), (2, 2), (2, 4),
                (4, 2), (4, 4), (5, 1), (5, 5),
            ]
            for dr, dc in marks:
                rr = row + dr
                cc = col + dc
                if 0 <= rr < 32 and 0 <= cc < 32:
                    grid[rr][cc] = s

    elif kind == "budget":
        color = entity_type[1]
        width = entity_type[2]
        for cc in range(col, min(32, col + width)):
            if 0 <= row < 32:
                grid[row][cc] = color


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    new_h = copy.deepcopy(h_t)
    level = new_h["level"]

    if a_t == 0:
        return get_initial_state(level)[0]

    if new_h.get("budget_left", 0) <= 0:
        return _refresh_goal_state(new_h)

    is_click = isinstance(a_t, tuple) and len(a_t) == 3 and a_t[0] == 6
    if not is_click:
        return _refresh_goal_state(new_h)

    x = a_t[1]
    y = a_t[2]
    cfg = LEVELS[level]
    rows = cfg["rows"]
    cols = cfg["cols"]
    palette_len = len(cfg["palette"])

    clicked_idx = None
    for r in range(rows):
        for c in range(cols):
            top = BOARD_ROW + r * TILE
            left = BOARD_COL + c * TILE
            if left <= x < left + TILE and top <= y < top + TILE:
                clicked_idx = r * cols + c

    if clicked_idx is not None:
        switches = cfg.get("switches", {}) if "switch" in cfg.get("active_tags", []) else {}
        locked = set(cfg.get("locked", [])) if "switch" in cfg.get("active_tags", []) else set()

        if clicked_idx in switches:
            for idx in switches[clicked_idx]:
                new_h["current"][idx] = (new_h["current"][idx] + 1) % palette_len
            if "switch_counts" in new_h:
                current_count = new_h["switch_counts"].get(clicked_idx, 0)
                new_h["switch_counts"][clicked_idx] = current_count + 1
        elif clicked_idx not in locked:
            new_h["current"][clicked_idx] = (new_h["current"][clicked_idx] + 1) % palette_len

    new_h["step"] = new_h.get("step", 0) + 1
    new_h["budget_left"] = max(0, new_h.get("budget_left", 0) - 1)
    return _refresh_goal_state(new_h)


def predict(h_t: dict, seed: int) -> dict:
    return {}


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    if h_t.get("level") != level:
        return False

    cfg = LEVELS[level]
    req = cfg.get("goal_requirements", {})

    for key, expected in req.items():
        if key == "matches_target":
            actual = _matches_target_for_level(level, h_t.get("current", []))
        else:
            actual = h_t.get(key)
        if actual != expected:
            return False

    return _matches_target_for_level(level, h_t.get("current", []))


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    grid = [[BG_COLOR for _ in range(32)] for _ in range(32)]
    level = h_t["level"]
    cfg = LEVELS[level]
    budget = cfg["budget"]
    budget_left = h_t.get("budget_left", budget)

    for c in range(32):
        grid[0][c] = COLORS["ui_empty"]

    filled = 0
    if budget > 0:
        filled = int((budget_left * 32) // budget)
    _draw_entity(grid, 0, 0, ("budget", COLORS["budget"], filled))

    rows = cfg["rows"]
    cols = cfg["cols"]
    palette = cfg["palette"]
    targets = cfg["target_indices"]
    current = h_t.get("current", cfg["initial"])
    switches = cfg.get("switches", {}) if "switch" in cfg.get("active_tags", []) else {}
    locked = set(cfg.get("locked", [])) if "switch" in cfg.get("active_tags", []) else set()
    orbit_memberships = _orbit_memberships(cfg) if switches else {}

    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            top = BOARD_ROW + r * TILE
            left = BOARD_COL + c * TILE
            target_color = palette[targets[idx]]
            current_color = palette[current[idx] % len(palette)]
            is_switch = idx in switches
            is_locked = idx in locked
            matched = current[idx] == targets[idx]
            _draw_entity(grid, top, left, ("lamp", target_color, current_color, is_switch, is_locked, matched))

    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            groups = orbit_memberships.get(idx, [])
            if groups:
                top = BOARD_ROW + r * TILE
                left = BOARD_COL + c * TILE
                _draw_orbit_markers(grid, top, left, groups)

    if check_level_complete(h_t, {}, level):
        for c in range(32):
            grid[31][c] = COLORS["complete"]
    elif budget_left <= 0:
        for c in range(32):
            grid[31][c] = COLORS["bad"]

    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    cfg = LEVELS[level]
    h_t = {
        "level": level,
        "step": 0,
        "budget_left": cfg["budget"],
        "current": copy.deepcopy(cfg["initial"]),
        "switch_counts": {},
        "matches_target": False,
    }

    for switch_idx in cfg.get("switches", {}):
        h_t["switch_counts"][switch_idx] = 0

    _refresh_goal_state(h_t)
    z_t = {}
    return h_t, z_t


def get_available_actions() -> list[int]:
    return [0, 6]


def solve_level(level: int) -> list:
    cfg = LEVELS[level]
    cols = cfg["cols"]
    actions = []

    for idx in cfg["solution_indices"]:
        r = idx // cols
        c = idx % cols
        x = BOARD_COL + c * TILE + TILE // 2
        y = BOARD_ROW + r * TILE + TILE // 2
        actions.append((6, x, y))

    return actions


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Ps1842(_FunctionalArcGame):
    GAME_ID = "ps1842-539e99d4"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
