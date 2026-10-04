# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the mt4926/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy

BG_COLOR = 1
GRID_SIZE = 32
CELL_SIZE = 6

COLORS = {
    "bg": 1,
    "slot": 2,
    "idea": 10,
    "truth": 0,
    "flag": 9,
    "ink": 5,
    "select": 5,
    "patrol": 7,
    "fog": 2,
    "charge": 15,
}

LEVELS = {
    0: {
        "rows": 3,
        "cols": 4,
        "origin": (10, 2),
        "gap": 1,
        "target_columns": ["idea", "truth", "idea", "truth"],
        "initial_tokens": [
            ["truth", "idea", "idea", "truth"],
            ["idea", "idea", "truth", "truth"],
            ["truth", "truth", "idea", "idea"],
        ],
        "budget": 22,
        "active_tags": [],
        "fog_radius": None,
        "goal_requirements": {
            "sorted": True,
        },
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "sorted",
            "primary_blocker": "truth and idea tokens begin in the wrong flagged columns",
            "dependencies": [
                "repair the first-row left pair",
                "move the second-row middle token into the truth column",
                "route the bottom-right idea token across adjacent slots before the last truth can settle",
            ],
            "feedback": "clicked tokens visibly swap; columns become uniformly matched to their flag headers",
            "bypass_guard": "sorted is true only when every filled tray token matches its column flag",
        },
    },
    1: {
        "rows": 3,
        "cols": 4,
        "origin": (10, 2),
        "gap": 1,
        "target_columns": ["idea", "truth", "idea", "truth"],
        "target_empty": [[2, 3]],
        "initial_tokens": [
            ["idea", "idea", "truth", "truth"],
            ["idea", "truth", "truth", "truth"],
            ["idea", None, "idea", "idea"],
        ],
        "budget": 42,
        "active_tags": ["buffer"],
        "fog_radius": None,
        "goal_requirements": {
            "sorted": True,
            "buffer_empty": True,
            "used_buffer": True,
        },
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["sorted", "buffer_empty", "used_buffer"],
            "primary_blocker": "level 1 is slide-only: occupied tokens cannot swap directly, so the empty buffer must be routed beside each blocker",
            "dependencies": [
                "move the empty buffer beside the top-row wrong pair",
                "slide the idea/truth blockers through the buffer corridor",
                "return the empty buffer to its marked bottom-right dock"
            ],
            "feedback": "the purple buffer dock is empty/filled visibly, and every legal buffer slide moves the blank square",
            "bypass_guard": "the board is not complete unless all non-buffer trays match their column flags and the marked buffer dock is empty after at least one buffer slide",
        },
    },
    2: {
        "rows": 3,
        "cols": 4,
        "origin": (10, 2),
        "gap": 1,
        "target_columns": ["idea", "truth", "charge", "idea"],
        "initial_tokens": [
            ["charge", "idea", "truth", "idea"],
            ["truth", "charge", "idea", "idea"],
            ["idea", "truth", "idea", "charge"],
        ],
        "budget": 24,
        "active_tags": ["charge"],
        "fog_radius": None,
        "goal_requirements": {
            "sorted": True,
        },
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "sorted",
            "primary_blocker": "a third charge-token class must be routed into its own flagged column without disturbing already-correct idea/truth columns",
            "dependencies": [
                "recognize the new purple charge target column",
                "repair top-row idea/truth/charge ordering",
                "repair middle-row charge blocker",
                "finish the bottom-row charge/idea inversion"
            ],
            "feedback": "purple charge rings line up under the purple-marked flag column when sorted",
            "bypass_guard": "completion requires every tray, including every charge token, to match the visible column flag",
        },
    },
    3: {
        "rows": 3,
        "cols": 4,
        "origin": (10, 2),
        "gap": 1,
        "target_columns": ["idea", "truth", "charge", "idea"],
        "initial_tokens": [
            ["truth", "idea", "charge", "idea"],
            ["idea", "charge", "truth", "idea"],
            ["idea", "truth", "idea", "charge"],
        ],
        "budget": 28,
        "active_tags": ["charge", "patrol"],
        "fog_radius": None,
        "patrol_route": [[0, 1], [1, 1], [1, 2], [2, 2]],
        "goal_requirements": {
            "sorted": True,
            "patrol_respected": True,
        },
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["sorted", "patrol_respected"],
            "primary_blocker": "a light-pink auditor patrols the middle trays and any click on its current tray is blocked",
            "dependencies": [
                "time the first top-row repair around the auditor",
                "wait until the middle charge/truth pair is not under audit before swapping",
                "finish the bottom charge/idea inversion on a safe patrol phase"
            ],
            "feedback": "the auditor eye is drawn on the currently locked tray and advances after each click",
            "bypass_guard": "locked trays ignore clicks, so the board cannot be matched unless the patrol timing constraint is respected",
        },
    },
    4: {
        "rows": 3,
        "cols": 4,
        "origin": (10, 2),
        "gap": 1,
        "target_columns": ["idea", "truth", "charge", "idea"],
        "initial_tokens": [
            ["truth", "idea", "charge", "idea"],
            ["idea", "charge", "truth", "idea"],
            ["charge", "truth", "idea", "idea"],
        ],
        "budget": 30,
        "active_tags": ["charge", "patrol", "dual_patrol"],
        "fog_radius": None,
        "patrol_routes": [
            [[0, 1], [1, 0], [0, 2], [1, 3]],
            [[0, 3], [2, 3], [1, 3], [2, 0]]
        ],
        "goal_requirements": {
            "sorted": True,
            "patrol_respected": True,
        },
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["sorted", "patrol_respected"],
            "primary_blocker": "two auditors patrol different trays, so several tempting direct swaps are sometimes locked",
            "dependencies": [
                "repair the top truth/idea inversion while both auditors are elsewhere",
                "repair the middle charge/truth inversion on a safe phase",
                "bubble the bottom charge token through two adjacent swaps without clicking an audited tray"
            ],
            "feedback": "two light-pink auditor eyes are visible on their locked trays and advance after each click",
            "bypass_guard": "any clicked locked tray is ignored and flips patrol_respected false; completion requires the matched board and respected patrol state",
        },
    },
    5: {
        "rows": 4,
        "cols": 4,
        "origin": (7, 2),
        "gap": 0,
        "target_columns": ["idea", "truth", "charge", "idea"],
        "initial_tokens": [
            ["truth", "idea", "charge", "idea"],
            ["idea", "charge", "truth", "idea"],
            ["idea", "truth", "idea", "charge"],
            ["charge", "idea", "truth", "idea"],
        ],
        "budget": 30,
        "active_tags": ["charge", "fog"],
        "fog_radius": 1,
        "initial_revealed": [[0, 0], [0, 1], [1, 1], [1, 2]],
        "goal_requirements": {
            "sorted": True,
        },
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "sorted",
            "primary_blocker": "gray fog veils most trays, so the player must remember token classes revealed by local clicks while sorting the same column pattern",
            "dependencies": [
                "use the visible clue trays to identify the flag pattern",
                "click into fogged local trays to reveal misplaced tokens",
                "complete top, middle, lower, and bottom inversions without losing the remembered positions"
            ],
            "feedback": "clicked fogged trays become clear and tokens remain visible afterward",
            "bypass_guard": "the terminal sorted state requires every token under every flag to match; fog never marks a column complete by itself",
        },
    },
    6: {
        "rows": 4,
        "cols": 4,
        "origin": (7, 2),
        "gap": 0,
        "target_columns": ["idea", "truth", "charge", "idea"],
        "initial_tokens": [
            ["truth", "idea", "charge", "idea"],
            ["idea", "charge", "truth", "idea"],
            ["charge", "truth", "idea", "idea"],
            ["idea", "truth", "idea", "charge"],
        ],
        "budget": 34,
        "active_tags": ["charge", "fog", "patrol", "dual_patrol"],
        "fog_radius": 1,
        "initial_revealed": [[0, 0], [0, 1], [1, 1], [1, 2]],
        "patrol_routes": [
            [[0, 2], [0, 3], [1, 0], [1, 3]],
            [[2, 3], [3, 0], [3, 1], [0, 3]]
        ],
        "goal_requirements": {
            "sorted": True,
            "patrol_respected": True,
        },
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["sorted", "patrol_respected"],
            "primary_blocker": "fog hides most of a larger board while two auditors visibly lock trays on a patrol cycle",
            "dependencies": [
                "reveal and repair the top inversion",
                "reveal and repair the middle charge/truth inversion",
                "route the lower charge through two adjacent swaps while avoiding auditor cells",
                "finish the bottom charge/idea inversion from memory"
            ],
            "feedback": "fog clears on clicked local trays; two auditor eyes advance and show which trays are unsafe",
            "bypass_guard": "success requires the full board to match the flag columns and any audited click invalidates patrol_respected",
        },
    },
    7: {
        "rows": 4,
        "cols": 4,
        "origin": (7, 2),
        "gap": 0,
        "target_columns": ["charge", "truth", "idea", "idea"],
        "initial_tokens": [
            ["charge", "truth", "idea", "idea"],
            ["charge", "truth", "idea", "idea"],
            ["idea", "truth", "charge", "idea"],
            ["charge", "idea", "truth", "idea"],
        ],
        "budget": 46,
        "active_tags": ["charge", "fog", "patrol", "dual_patrol", "reveal_all"],
        "fog_radius": 1,
        "initial_revealed": [[0, 0], [0, 1], [1, 1], [1, 2]],
        "patrol_routes": [
            [[0, 0]],
            [[0, 1]]
        ],
        "goal_requirements": {
            "sorted": True,
            "patrol_respected": True,
            "all_revealed": True,
        },
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["sorted", "patrol_respected", "all_revealed"],
            "primary_blocker": "the final archive is fogged, watched by two patrol auditors, and cannot complete until every tray has been inspected",
            "dependencies": [
                "reveal the hidden lower trays to satisfy the inspection requirement",
                "repair the top charge/truth inversion under patrol timing",
                "repair the second-row idea/truth inversion",
                "route lower charge tokens through staged adjacent swaps while retaining the revealed map"
            ],
            "feedback": "each clicked fog tray becomes permanently visible; the all_revealed state becomes true only when no fog covers remain",
            "bypass_guard": "the matched target columns are not sufficient until every tray has been revealed and no patrol click has been made",
        },
    }
}


def _slot_top(cfg, r, c):
    sr, sc = cfg["origin"]
    gap = cfg.get("gap", 1)
    return sr + r * (CELL_SIZE + gap), sc + c * (CELL_SIZE + gap)


def _patrol_locked_slots(h_t, cfg):
    routes = cfg.get("patrol_routes")
    if routes is None:
        route = cfg.get("patrol_route", [])
        routes = [route] if route else []
    locks = []
    phase = h_t.get("patrol_phase", 0)
    for route in routes:
        if route:
            locks.append(route[phase % len(route)])
    return locks


def _draw_entity(grid, row, col, entity_type):
    color = COLORS.get(entity_type, COLORS["ink"])
    if entity_type == "slot":
        for rr in range(row, row + CELL_SIZE):
            for cc in range(col, col + CELL_SIZE):
                if rr == row or rr == row + CELL_SIZE - 1 or cc == col or cc == col + CELL_SIZE - 1:
                    grid[rr][cc] = COLORS["slot"]
    elif entity_type == "flag_idea":
        for cc in range(col, col + CELL_SIZE - 1):
            grid[row][cc] = COLORS["flag"]
        for rr in range(row, row + 5):
            grid[rr][col] = COLORS["ink"]
        grid[row + 1][col + 1] = COLORS["idea"]
        grid[row + 1][col + 2] = COLORS["idea"]
        grid[row + 2][col + 1] = COLORS["idea"]
    elif entity_type == "flag_truth":
        for cc in range(col, col + CELL_SIZE - 1):
            grid[row][cc] = COLORS["flag"]
        for rr in range(row, row + 5):
            grid[rr][col] = COLORS["ink"]
        grid[row + 1][col + 2] = COLORS["truth"]
        grid[row + 2][col + 1] = COLORS["truth"]
        grid[row + 2][col + 3] = COLORS["truth"]
        grid[row + 3][col + 2] = COLORS["truth"]
    elif entity_type == "flag_charge":
        for cc in range(col, col + CELL_SIZE - 1):
            grid[row][cc] = COLORS["flag"]
        for rr in range(row, row + 5):
            grid[rr][col] = COLORS["ink"]
        for cc in range(col + 1, col + 4):
            grid[row + 1][cc] = COLORS["charge"]
            grid[row + 3][cc] = COLORS["charge"]
        grid[row + 2][col + 1] = COLORS["charge"]
        grid[row + 2][col + 3] = COLORS["charge"]
    elif entity_type == "idea":
        # chunky plus/star token
        for rr in range(row + 1, row + CELL_SIZE - 1):
            grid[rr][col + 2] = color
            grid[rr][col + 3] = color
        for cc in range(col + 1, col + CELL_SIZE - 1):
            grid[row + 2][cc] = color
            grid[row + 3][cc] = color
        grid[row + 2][col + 2] = COLORS["ink"]
        grid[row + 3][col + 3] = COLORS["ink"]
    elif entity_type == "truth":
        # white diamond with black center, readable on gray slot
        pts = [(1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3), (3, 4), (4, 2), (4, 3)]
        for dr, dc in pts:
            grid[row + dr][col + dc] = color
        grid[row + 2][col + 2] = COLORS["ink"]
        grid[row + 3][col + 3] = COLORS["ink"]
    elif entity_type == "charge":
        # purple ring / charged drum token
        for cc in range(col + 1, col + CELL_SIZE - 1):
            grid[row + 1][cc] = COLORS["charge"]
            grid[row + 4][cc] = COLORS["charge"]
        for rr in range(row + 1, row + CELL_SIZE - 1):
            grid[rr][col + 1] = COLORS["charge"]
            grid[rr][col + 4] = COLORS["charge"]
        grid[row + 2][col + 2] = COLORS["ink"]
        grid[row + 2][col + 3] = COLORS["ink"]
        grid[row + 3][col + 2] = COLORS["ink"]
        grid[row + 3][col + 3] = COLORS["ink"]
    elif entity_type == "patrol":
        # light-pink auditor eye/bar overlay
        for cc in range(col + 1, col + CELL_SIZE - 1):
            grid[row + 1][cc] = COLORS["patrol"]
            grid[row + 4][cc] = COLORS["patrol"]
        grid[row + 2][col + 1] = COLORS["patrol"]
        grid[row + 2][col + 4] = COLORS["patrol"]
        grid[row + 3][col + 2] = COLORS["ink"]
        grid[row + 3][col + 3] = COLORS["ink"]
    elif entity_type == "buffer":
        # purple/black dock marker for the empty buffer home
        for rr in range(row + 1, row + CELL_SIZE - 1):
            grid[rr][col + 1] = COLORS["charge"]
            grid[rr][col + 4] = COLORS["charge"]
        for cc in range(col + 1, col + CELL_SIZE - 1):
            grid[row + 1][cc] = COLORS["charge"]
            grid[row + 4][cc] = COLORS["charge"]
        grid[row + 2][col + 2] = COLORS["ink"]
        grid[row + 3][col + 3] = COLORS["ink"]
    elif entity_type == "selected":
        for cc in range(col, col + CELL_SIZE):
            grid[row][cc] = COLORS["select"]
            grid[row + CELL_SIZE - 1][cc] = COLORS["select"]
        for rr in range(row, row + CELL_SIZE):
            grid[rr][col] = COLORS["select"]
            grid[rr][col + CELL_SIZE - 1] = COLORS["select"]
        grid[row + 1][col + 1] = COLORS["select"]
        grid[row + 1][col + 4] = COLORS["select"]
        grid[row + 4][col + 2] = COLORS["select"]
        grid[row + 4][col + 3] = COLORS["select"]
    elif entity_type == "fog":
        for rr in range(row, row + CELL_SIZE):
            for cc in range(col, col + CELL_SIZE):
                if (rr + cc) % 2 == 0:
                    grid[rr][cc] = COLORS["fog"]
                else:
                    grid[rr][cc] = COLORS["ink"]


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    """Deterministic history state update (DreamerV3 sequence model)."""
    level = h_t["level"]
    cfg = LEVELS[level]
    new_h = copy.deepcopy(h_t)

    if a_t == 0:
        return get_initial_state(level)[0]

    if new_h.get("budget", 0) <= 0:
        return new_h

    tags = cfg.get("active_tags", [])
    if "patrol" in tags:
        if cfg.get("patrol_routes"):
            route_len = max([len(route) for route in cfg.get("patrol_routes", [])] + [4])
        else:
            route_len = len(cfg.get("patrol_route", [])) or 4
        new_h["patrol_phase"] = (new_h.get("patrol_phase", 0) + 1) % route_len

    clicked_slot = None
    if isinstance(a_t, tuple) and len(a_t) == 3 and a_t[0] == 6:
        x, y = a_t[1], a_t[2]
        for r in range(cfg["rows"]):
            for c in range(cfg["cols"]):
                top, left = _slot_top(cfg, r, c)
                if left <= x < left + CELL_SIZE and top <= y < top + CELL_SIZE:
                    clicked_slot = [r, c]
                    break
            if clicked_slot is not None:
                break

    if clicked_slot is not None and "patrol" in tags and clicked_slot in _patrol_locked_slots(new_h, cfg):
        clicked_slot = None
        new_h["selected"] = None
        new_h["patrol_respected"] = False

    if clicked_slot is not None:
        if "fog" in tags:
            if clicked_slot not in new_h.get("revealed", []):
                new_h.setdefault("revealed", []).append(clicked_slot[:])
            if "reveal_all" in tags:
                new_h["all_revealed"] = len(new_h.get("revealed", [])) >= cfg["rows"] * cfg["cols"]
        sel = new_h.get("selected")
        r, c = clicked_slot
        if sel is None:
            new_h["selected"] = [r, c]
        else:
            sr, sc = sel
            if sr == r and sc == c:
                new_h["selected"] = None
            elif abs(sr - r) + abs(sc - c) == 1:
                tokens = new_h["tokens"]
                if "buffer" in tags:
                    # Slide-only level: at least one endpoint must be empty.
                    if (tokens[sr][sc] is None) != (tokens[r][c] is None):
                        tokens[sr][sc], tokens[r][c] = tokens[r][c], tokens[sr][sc]
                        new_h["used_buffer"] = True
                        new_h["selected"] = None
                    else:
                        new_h["selected"] = [r, c]
                else:
                    tokens[sr][sc], tokens[r][c] = tokens[r][c], tokens[sr][sc]
                    new_h["selected"] = None
            else:
                new_h["selected"] = [r, c]

    new_h["step"] = new_h.get("step", 0) + 1
    new_h["budget"] = max(0, new_h.get("budget", 0) - 1)
    new_h["buffer_empty"] = _target_empty_clear(new_h, cfg)
    new_h["sorted"] = check_level_complete(new_h, {}, level)
    return new_h


def predict(h_t: dict, seed: int) -> dict:
    """Return exactly {}. This game is fully deterministic."""
    return {}


def _target_empty_clear(h_t, cfg):
    for pos in cfg.get("target_empty", []):
        r, c = pos
        if h_t.get("tokens", [[None]])[r][c] is not None:
            return False
    return True


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    """Check if the current level's goal has been achieved."""
    cfg = LEVELS[level]
    req = cfg.get("goal_requirements", {})
    target = cfg["target_columns"]
    tokens = h_t.get("tokens", [])
    filled = 0
    if len(tokens) != cfg["rows"]:
        return False
    target_empty = [tuple(pos) for pos in cfg.get("target_empty", [])]
    for r in range(cfg["rows"]):
        if len(tokens[r]) != cfg["cols"]:
            return False
        for c in range(cfg["cols"]):
            tok = tokens[r][c]
            if (r, c) in target_empty:
                if tok is not None:
                    return False
                continue
            if tok is None:
                return False
            filled += 1
            if tok != target[c]:
                return False
    if filled != cfg["rows"] * cfg["cols"] - len(target_empty):
        return False
    # Enforce simple validator-visible goal requirement state keys.
    for key, value in req.items():
        if key == "sorted":
            if value is not True:
                return False
        elif h_t.get(key) != value:
            return False
    return True


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    """Render the current state as a 32x32 grid."""
    level = h_t["level"]
    cfg = LEVELS[level]
    grid = [[BG_COLOR for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # Flag headers.
    for c, target in enumerate(cfg["target_columns"]):
        slot_top, slot_left = _slot_top(cfg, 0, c)
        _draw_entity(grid, 4, slot_left, "flag_" + target)

    # Slots and tokens.
    for r in range(cfg["rows"]):
        for c in range(cfg["cols"]):
            top, left = _slot_top(cfg, r, c)
            _draw_entity(grid, top, left, "slot")
            if [r, c] in cfg.get("target_empty", []):
                _draw_entity(grid, top, left, "buffer")
            tok = h_t["tokens"][r][c]
            if tok is not None:
                _draw_entity(grid, top, left, tok)

    # Patrol auditor overlay on currently locked slot.
    if "patrol" in cfg.get("active_tags", []):
        for r, c in _patrol_locked_slots(h_t, cfg):
            top, left = _slot_top(cfg, r, c)
            _draw_entity(grid, top, left, "patrol")

    # Selection mouse-stamp outline.
    if h_t.get("selected") is not None:
        r, c = h_t["selected"]
        top, left = _slot_top(cfg, r, c)
        _draw_entity(grid, top, left, "selected")

    # Budget bar along bottom row: blue spent-safe track, black low reserve.
    budget = h_t.get("budget", 0)
    max_budget = cfg.get("budget", 1)
    width = int((budget * GRID_SIZE) / max_budget) if max_budget else 0
    for c in range(GRID_SIZE):
        grid[31][c] = COLORS["flag"] if c < width else COLORS["ink"]

    # Observability masking for fog levels: only remembered/recent local trays are clear.
    fog_radius = cfg.get("fog_radius")
    if fog_radius is not None and "fog" in cfg.get("active_tags", []):
        visible = [list(pos) for pos in h_t.get("revealed", cfg.get("initial_revealed", []))]
        if h_t.get("selected") is not None:
            sr, sc = h_t["selected"]
            for rr in range(cfg["rows"]):
                for cc in range(cfg["cols"]):
                    if abs(sr - rr) + abs(sc - cc) <= fog_radius and [rr, cc] not in visible:
                        visible.append([rr, cc])
        for r in range(cfg["rows"]):
            for c in range(cfg["cols"]):
                if [r, c] not in visible:
                    top, left = _slot_top(cfg, r, c)
                    _draw_entity(grid, top, left, "fog")
    elif fog_radius is not None and h_t.get("selected") is not None:
        sr, sc = h_t["selected"]
        for r in range(cfg["rows"]):
            for c in range(cfg["cols"]):
                if abs(sr - r) + abs(sc - c) > fog_radius:
                    top, left = _slot_top(cfg, r, c)
                    _draw_entity(grid, top, left, "fog")

    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    """Get the initial (h_t, z_t) for a given level."""
    cfg = LEVELS[level]
    h_t = {
        "level": level,
        "step": 0,
        "budget": cfg["budget"],
        "tokens": copy.deepcopy(cfg["initial_tokens"]),
        "selected": None,
        "used_buffer": False,
        "buffer_empty": False,
        "patrol_phase": 0,
        "patrol_respected": True,
        "revealed": copy.deepcopy(cfg.get("initial_revealed", [])),
        "all_revealed": False,
        "sorted": False,
    }
    h_t["buffer_empty"] = _target_empty_clear(h_t, cfg)
    h_t["all_revealed"] = len(h_t.get("revealed", [])) >= cfg["rows"] * cfg["cols"]
    h_t["sorted"] = check_level_complete(h_t, {}, level)
    return h_t, {}


def get_available_actions() -> list[int]:
    """Return available action integers for this click game."""
    return [0, 6]


def solve_level(level: int) -> list:
    """Return a fixed sequence of actions that solves this level."""
    cfg = LEVELS[level]
    def center(r, c):
        top, left = _slot_top(cfg, r, c)
        return (6, left + CELL_SIZE // 2, top + CELL_SIZE // 2)
    if level == 0:
        return [
            center(0, 0), center(0, 1),  # row 0: T I I T -> I T I T
            center(1, 1), center(1, 2),  # row 1: I I T T -> I T I T
            center(2, 1), center(2, 2),  # route bottom row: T T I I -> T I T I
            center(2, 0), center(2, 1),  # -> I T T I
            center(2, 2), center(2, 3),  # -> I T I T
        ]
    if level == 1:
        return [
            center(2, 2), center(2, 1),
            center(1, 2), center(2, 2),
            center(0, 2), center(1, 2),
            center(0, 1), center(0, 2),
            center(1, 1), center(0, 1),
            center(1, 2), center(1, 1),
            center(2, 2), center(1, 2),
            center(2, 1), center(2, 2),
            center(1, 1), center(2, 1),
            center(1, 2), center(1, 1),
            center(2, 2), center(1, 2),
            center(2, 3), center(2, 2),
        ]
    if level == 2:
        return [
            center(0, 0), center(0, 1),
            center(0, 1), center(0, 2),
            center(1, 1), center(1, 2),
            center(1, 0), center(1, 1),
            center(2, 2), center(2, 3),
        ]
    if level == 3:
        return [
            center(0, 0), center(0, 1),
            center(1, 1), center(1, 2),
            center(2, 2), center(2, 3),
        ]
    if level == 4:
        return [
            center(0, 0), center(0, 1),
            center(1, 1), center(1, 2),
            center(2, 0), center(2, 1),
            center(2, 1), center(2, 2),
            center(2, 0), center(2, 1),
        ]
    if level == 5:
        return [
            center(0, 0), center(0, 1),
            center(1, 1), center(1, 2),
            center(2, 2), center(2, 3),
            center(3, 0), center(3, 1),
            center(3, 1), center(3, 2),
        ]
    if level == 6:
        return [
            center(0, 0), center(0, 1),
            center(1, 1), center(1, 2),
            center(2, 0), center(2, 1),
            center(2, 1), center(2, 2),
            center(2, 0), center(2, 1),
            center(3, 2), center(3, 3),
        ]
    if level == 7:
        # Inspect all non-initial fogged trays without touching the two audited top docks,
        # then make staged lower-row adjacent swaps.
        return [
            center(0, 2), center(0, 2),
            center(0, 3), center(0, 3),
            center(1, 0), center(1, 0),
            center(1, 3), center(1, 3),
            center(2, 0), center(2, 0),
            center(2, 1), center(2, 1),
            center(2, 2), center(2, 2),
            center(2, 3), center(2, 3),
            center(3, 0), center(3, 0),
            center(3, 1), center(3, 1),
            center(3, 2), center(3, 2),
            center(3, 3), center(3, 3),
            center(2, 1), center(2, 2),
            center(2, 0), center(2, 1),
            center(2, 1), center(2, 2),
            center(3, 1), center(3, 2),
        ]
    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Mt4926(_FunctionalArcGame):
    GAME_ID = "mt4926-66d0222a"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
