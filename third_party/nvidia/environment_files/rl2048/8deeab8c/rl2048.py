# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the rl2048/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy

BG_COLOR = 0
COLORS = {
    "tray": 15,
    "select": 7,
    "pink": 6,
    "silver": 10,
    "pulp": 11,
    "idea": 14,
    "hopper": 9,
    "pin": 12,
}
TOKEN_COLORS = {"P": 6, "S": 10, "Y": 11, "I": 14}
CELL = 4
BOARD_R = 5
BOARD_C = 8
TARGET_R = 21

LEVELS = {
    0: {
        "rows": 3,
        "cols": 3,
        "start": [
            ["S", "P", "Y"],
            ["P", "Y", "S"],
            ["Y", "S", "P"],
        ],
        "target": [
            ["P", "S", "Y"],
            ["P", "S", "Y"],
            ["P", "S", "Y"],
        ],
        "blocked_edges": [],
        "active_tags": [],
        "budget": 16,
        "goal_requirements": {"matched": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "matched",
            "primary_blocker": "mixed ingredient layers start in the wrong columns and rows",
            "dependencies": ["select a local pair", "swap misplaced layers", "match every visible recipe label"],
            "feedback": "tokens line up with the target labels and the selected token has a light-pink outline",
            "bypass_guard": "completion is exactly the visible board-to-target relation for all nine slots",
        },
    },
    1: {
        "rows": 3,
        "cols": 4,
        "start": [
            ["S", "P", "I", "Y"],
            ["P", "Y", "S", "I"],
            ["S", "P", "Y", "I"],
        ],
        "target": [
            ["P", "S", "Y", "I"],
            ["P", "S", "Y", "I"],
            ["P", "S", "Y", "I"],
        ],
        "blocked_edges": [(1, 1, 1, 2)],
        "active_tags": ["pins"],
        "budget": 22,
        "goal_requirements": {"matched": True, "pin_detour_used": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "matched",
            "primary_blocker": "an orange mixing pin blocks the obvious middle-row swap between silver and pulp",
            "dependencies": [
                "sort the unpinned top and bottom pairs",
                "route the middle-row silver/pulp conflict through the lower row",
                "restore the lower row after the detour",
                "match every visible recipe label",
            ],
            "feedback": "the orange pin is drawn between the blocked cells; detour_used becomes true after a legal swap touches that blocked pair's lower bypass",
            "bypass_guard": "the visible target cannot be reached without changing the pinned pair through adjacent bypass swaps, and completion requires matched plus pin_detour_used",
        },
    },
    2: {
        "rows": 3,
        "cols": 4,
        "start": [
            ["I", "P", "S", "Y"],
            ["S", "Y", "P", "I"],
            ["P", "S", "Y", "I"],
        ],
        "target": [
            ["P", "S", "Y", "I"],
            ["P", "S", "Y", "I"],
            ["P", "S", "Y", "I"],
        ],
        "blocked_edges": [(0, 2, 0, 3), (1, 1, 1, 2)],
        "active_tags": ["pins"],
        "budget": 30,
        "goal_requirements": {"matched": True, "pin_detour_used": True, "second_pin_detour_used": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "matched",
            "primary_blocker": "a top-row pin and a middle-row pin block two different direct corrections, requiring vertical staging",
            "dependencies": [
                "free the top idea/yellow order through the row below",
                "detour the middle pulp/pink conflict around its pin",
                "restore the staged row",
                "match all visible recipe labels",
            ],
            "feedback": "the two orange pins appear in different rows, so each bypass route is visually distinct",
            "bypass_guard": "completion requires the visible board match plus evidence that both pinned conflicts were routed by detours",
        },
    },
    3: {
        "rows": 3,
        "cols": 5,
        "start": [
            ["S", "P", "Y", "I", "P"],
            ["P", "Y", "S", "I", "P"],
            ["Y", "P", "S", "I", "P"],
        ],
        "target": [
            ["P", "S", "Y", "I", "P"],
            ["P", "S", "Y", "I", "P"],
            ["P", "S", "Y", "I", "P"],
        ],
        "hidden_cells": [(0, 2), (1, 2), (2, 2), (0, 4), (1, 4), (2, 4)],
        "blocked_edges": [],
        "active_tags": ["hidden"],
        "budget": 28,
        "goal_requirements": {"matched": True, "all_revealed": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["matched", "all_revealed"],
            "primary_blocker": "six target recipe labels are covered by light-pink hidden cards",
            "dependencies": [
                "click each covered target card to reveal the full recipe",
                "use the revealed constraints to solve the three left columns",
                "match all now-visible recipe labels",
            ],
            "feedback": "each clicked hidden card turns into its colored target glyph; all_revealed becomes true when no cards remain",
            "bypass_guard": "completion requires both the visible board match and all hidden target cards revealed",
        },
    },
    4: {
        "rows": 4,
        "cols": 4,
        "start": [
            ["I", "P", "S", "Y"],
            ["P", "Y", "I", "S"],
            ["S", "P", "Y", "I"],
            ["P", "S", "Y", "I"],
        ],
        "target": [
            ["P", "S", "Y", "I"],
            ["P", "S", "Y", "I"],
            ["P", "S", "Y", "I"],
            ["P", "S", "Y", "I"],
        ],
        "hidden_cells": [(0, 1), (0, 3), (1, 2), (2, 0), (2, 3), (3, 1)],
        "blocked_edges": [(0, 0, 1, 0), (1, 1, 1, 2)],
        "active_tags": ["hidden", "pins"],
        "budget": 40,
        "goal_requirements": {"matched": True, "all_revealed": True, "pin_detour_used": True, "second_pin_detour_used": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["matched", "all_revealed"],
            "primary_blocker": "some recipe labels are hidden while two pins forbid direct corrections in different orientations",
            "dependencies": [
                "reveal the covered target cards",
                "use the revealed pattern to stage the top-left token around the vertical pin",
                "route the middle row around the horizontal pin",
                "match all sixteen visible recipe slots",
            ],
            "feedback": "clicked hidden cards become colored targets, and both orange pins remain visible as no-swap constraints",
            "bypass_guard": "the terminal board relation is accepted only when all cards are revealed and both pin detours have been used",
        },
    },
    5: {
        "rows": 3,
        "cols": 5,
        "start": [
            ["S", "P", "Y", "I", "E"],
            ["P", "Y", "S", "I", "P"],
            ["E", "P", "S", "Y", "I"],
        ],
        "target": [
            ["P", "S", "Y", "I", "P"],
            ["P", "S", "Y", "I", "P"],
            ["P", "S", "Y", "I", "P"],
        ],
        "spawn_targets": {
            (0, 4): "P",
            (2, 0): "P",
        },
        "blocked_edges": [],
        "active_tags": ["spawn"],
        "budget": 34,
        "goal_requirements": {"matched": True, "spawn_a_done": True, "spawn_b_done": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["matched", "spawn_a_done", "spawn_b_done"],
            "primary_blocker": "two empty blue hopper trays must be spawned before the recipe has enough pink tokens",
            "dependencies": [
                "click the upper-right hopper tray to spawn its pink ingredient",
                "click the lower-left hopper tray to spawn its pink ingredient",
                "sort the expanded five-column board into visible recipe order",
            ],
            "feedback": "empty hopper trays show blue rings; after a spawn the ring becomes a normal pink token",
            "bypass_guard": "the visible board cannot match the full recipe until both spawned ingredients exist, and completion requires both spawn flags",
        },
    },
    6: {
        "rows": 3,
        "cols": 5,
        "start": [
            ["P", "S", "Y", "I", "E"],
            ["P", "Y", "S", "I", "P"],
            ["E", "S", "Y", "I", "P"],
        ],
        "target": [
            ["P", "S", "Y", "I", "P"],
            ["P", "S", "Y", "I", "P"],
            ["P", "S", "Y", "I", "P"],
        ],
        "hidden_cells": [(0, 0), (0, 4), (1, 1), (1, 2), (2, 0), (2, 4)],
        "spawn_targets": {
            (0, 4): "P",
            (2, 0): "P",
        },
        "blocked_edges": [(1, 1, 1, 2)],
        "active_tags": ["hidden", "spawn", "pins"],
        "budget": 32,
        "goal_requirements": {"matched": True, "all_revealed": True, "spawn_a_done": True, "spawn_b_done": True, "pin_detour_used": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["matched", "all_revealed", "spawn_a_done", "spawn_b_done"],
            "primary_blocker": "the middle silver/pulp correction is pinned, while hidden target cards and two empty hoppers must be resolved first",
            "dependencies": [
                "reveal the covered recipe labels",
                "spawn the two missing pink ingredients from blue hopper trays",
                "route the pinned middle-row pair through the row above",
                "match every visible recipe label",
            ],
            "feedback": "hidden cards flip to target glyphs, hopper rings become pink tokens, and the orange pin shows the forbidden direct swap",
            "bypass_guard": "completion requires the visible board match plus all reveal, spawn, and detour requirements",
        },
    },
    7: {
        "rows": 3,
        "cols": 5,
        "start": [
            ["S", "Y", "I", "P", "E"],
            ["P", "S", "P", "I", "I"],
            ["E", "Y", "Y", "S", "P"],
        ],
        "target": [
            ["P", "S", "Y", "I", "P"],
            ["P", "S", "Y", "I", "P"],
            ["P", "S", "Y", "I", "P"],
        ],
        "hidden_cells": [(0, 1), (0, 4), (1, 0), (1, 3), (2, 0), (2, 2)],
        "spawn_targets": {
            (0, 4): "P",
            (2, 0): "P",
        },
        "blocked_edges": [(1, 1, 1, 2), (2, 3, 2, 4)],
        "active_tags": ["hidden", "spawn", "pins"],
        "budget": 42,
        "goal_requirements": {"matched": True, "all_revealed": True, "spawn_a_done": True, "spawn_b_done": True, "pin_detour_used": True, "second_pin_detour_used": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_keys": ["matched", "all_revealed", "spawn_a_done", "spawn_b_done"],
            "primary_blocker": "two hoppers are empty, six recipe labels are hidden, and two horizontal pins forbid the tempting direct swaps",
            "dependencies": [
                "reveal all six covered recipe labels",
                "spawn both missing pink layers",
                "route around the middle-row pin using the top-row bypass",
                "route around the bottom-right pin using the middle-row bypass",
                "restore the displaced ingredients into all five target columns",
            ],
            "feedback": "cards reveal colored target glyphs, hoppers become pink tokens, and detour flags are satisfied by visible swaps beside each orange pin",
            "bypass_guard": "the final board relation is accepted only after all reveals, both spawns, and both distinct pin detours are complete",
        },
    },
}


def _cell_origin(r, c):
    return BOARD_R + r * CELL, BOARD_C + c * CELL


def _target_origin(r, c, rows=3):
    base = 18 if rows >= 4 else TARGET_R
    return base + r * 3, BOARD_C + c * CELL


def _draw_entity(grid, row, col, entity_type, color=None):
    if entity_type == "tray":
        for dr in range(4):
            for dc in range(4):
                if dr in (0, 3) or dc in (0, 3):
                    grid[row + dr][col + dc] = COLORS["tray"]
    elif entity_type == "token":
        for dr in range(3):
            for dc in range(3):
                grid[row + dr][col + dc] = color
        grid[row + 1][col + 1] = BG_COLOR
    elif entity_type == "selected":
        for dc in range(4):
            grid[row][col + dc] = COLORS["select"]
            grid[row + 3][col + dc] = COLORS["select"]
        for dr in range(4):
            grid[row + dr][col] = COLORS["select"]
            grid[row + dr][col + 3] = COLORS["select"]
    elif entity_type == "target":
        for dr in range(3):
            for dc in range(3):
                if dr == 1 or dc == 1:
                    grid[row + dr][col + dc] = color
        grid[row + 1][col + 1] = COLORS["tray"]
    elif entity_type == "hidden":
        for dr in range(3):
            for dc in range(3):
                grid[row + dr][col + dc] = COLORS["select"]
        grid[row + 1][col + 1] = COLORS["tray"]
        grid[row][col] = COLORS["tray"]
        grid[row + 2][col + 2] = COLORS["tray"]
    elif entity_type == "spawn":
        for dr in range(3):
            for dc in range(3):
                if dr in (0, 2) or dc in (0, 2):
                    grid[row + dr][col + dc] = COLORS["hopper"]
        grid[row + 1][col + 1] = COLORS["pin"]
    elif entity_type == "pin_h":
        # Diagonal orange stitches between two horizontal neighbor cells.
        grid[row][col] = COLORS["pin"]
        grid[row + 1][col + 1] = COLORS["pin"]
        grid[row + 2][col] = COLORS["pin"]
        grid[row + 3][col + 1] = COLORS["pin"]
    elif entity_type == "pin_v":
        grid[row][col] = COLORS["pin"]
        grid[row + 1][col - 1] = COLORS["pin"]
        grid[row][col - 2] = COLORS["pin"]
        grid[row + 1][col - 3] = COLORS["pin"]
    elif entity_type == "budget":
        for dc in range(color):
            if 1 + dc < 31:
                grid[row][1 + dc] = COLORS["pin"]


def _slot_from_click(x, y, cfg):
    # Runtime click action is (6, x, y); x is column, y is row.
    c = (x - BOARD_C) // CELL
    r = (y - BOARD_R) // CELL
    if 0 <= r < cfg["rows"] and 0 <= c < cfg["cols"]:
        rr, cc = _cell_origin(r, c)
        if rr <= y < rr + CELL and cc <= x < cc + CELL:
            return int(r), int(c)
    return None


def _target_from_click(x, y, cfg):
    c = (x - BOARD_C) // CELL
    if not (0 <= c < cfg["cols"]):
        return None
    for r in range(cfg["rows"]):
        rr, cc = _target_origin(r, c, cfg.get("rows", 3))
        if rr <= y < rr + 3 and cc <= x < cc + 3:
            return int(r), int(c)
    return None


def _is_adjacent(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1


def _edge_blocked(a, b, cfg):
    if "pins" not in cfg.get("active_tags", []):
        return False
    e1 = (a[0], a[1], b[0], b[1])
    e2 = (b[0], b[1], a[0], a[1])
    return e1 in cfg.get("blocked_edges", []) or e2 in cfg.get("blocked_edges", [])


def _matched(board, target):
    return board == target


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    new_h = copy.deepcopy(h_t)
    cfg = LEVELS[h_t["level"]]
    tags = cfg.get("active_tags", [])

    base = a_t[0] if isinstance(a_t, tuple) else a_t
    if base not in get_available_actions():
        return new_h

    if base == 0:
        reset_h, _ = get_initial_state(h_t["level"])
        return reset_h

    if not isinstance(a_t, tuple) or len(a_t) != 3 or a_t[0] != 6:
        return new_h

    if new_h.get("complete") or new_h.get("failed"):
        return new_h

    if "hidden" in tags:
        target_slot = _target_from_click(a_t[1], a_t[2], cfg)
        if target_slot in cfg.get("hidden_cells", []) and target_slot not in [tuple(x) for x in new_h.get("revealed", [])]:
            if new_h["budget_left"] <= 0:
                new_h["failed"] = True
                return new_h
            new_h["revealed"].append(target_slot)
            new_h["selected"] = None
            new_h["step"] += 1
            new_h["budget_left"] -= 1
            new_h["all_revealed"] = len(new_h["revealed"]) == len(cfg.get("hidden_cells", []))
            if check_level_complete(new_h, {}, new_h["level"]):
                new_h["complete"] = True
            elif new_h["budget_left"] <= 0:
                new_h["failed"] = True
            return new_h

    slot = _slot_from_click(a_t[1], a_t[2], cfg)
    if slot is None:
        return new_h

    if "spawn" in tags:
        spawn_targets = cfg.get("spawn_targets", {})
        if slot in spawn_targets and new_h["board"][slot[0]][slot[1]] == "E":
            if new_h["budget_left"] <= 0:
                new_h["failed"] = True
                return new_h
            board = copy.deepcopy(new_h["board"])
            board[slot[0]][slot[1]] = spawn_targets[slot]
            new_h["board"] = board
            new_h["selected"] = None
            new_h["step"] += 1
            new_h["budget_left"] -= 1
            if slot == (0, 4):
                new_h["spawn_a_done"] = True
            if slot == (2, 0):
                new_h["spawn_b_done"] = True
            new_h["matched"] = _matched(board, cfg["target"])
            if check_level_complete(new_h, {}, new_h["level"]):
                new_h["complete"] = True
            elif new_h["budget_left"] <= 0:
                new_h["failed"] = True
            return new_h

    sel = new_h.get("selected")
    if sel is None:
        if new_h["board"][slot[0]][slot[1]] == "E":
            return new_h
        new_h["selected"] = slot
        return new_h

    sel = tuple(sel)
    if sel == slot:
        new_h["selected"] = None
        return new_h

    if new_h["board"][slot[0]][slot[1]] == "E":
        new_h["selected"] = None
        return new_h

    if not _is_adjacent(sel, slot) or _edge_blocked(sel, slot, cfg):
        new_h["selected"] = slot
        return new_h

    if new_h["budget_left"] <= 0:
        new_h["failed"] = True
        new_h["selected"] = None
        return new_h

    board = copy.deepcopy(new_h["board"])
    ar, ac = sel
    br, bc = slot
    board[ar][ac], board[br][bc] = board[br][bc], board[ar][ac]
    new_h["board"] = board
    new_h["selected"] = None
    new_h["step"] += 1
    new_h["budget_left"] -= 1

    if "pins" in tags:
        # Detour evidence: a legal bypass swap adjacent to a pinned edge.
        pinned = cfg.get("blocked_edges", [])
        for idx, (pr1, pc1, pr2, pc2) in enumerate(pinned):
            candidates = []
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a = (pr1 + dr, pc1 + dc)
                b = (pr2 + dr, pc2 + dc)
                if 0 <= a[0] < cfg["rows"] and 0 <= a[1] < cfg["cols"]:
                    candidates.append(tuple(sorted([(pr1, pc1), a])))
                if 0 <= b[0] < cfg["rows"] and 0 <= b[1] < cfg["cols"]:
                    candidates.append(tuple(sorted([(pr2, pc2), b])))
                if 0 <= a[0] < cfg["rows"] and 0 <= a[1] < cfg["cols"] and 0 <= b[0] < cfg["rows"] and 0 <= b[1] < cfg["cols"] and _is_adjacent(a, b):
                    candidates.append(tuple(sorted([a, b])))
            if tuple(sorted([sel, slot])) in candidates:
                if idx == 0:
                    new_h["pin_detour_used"] = True
                else:
                    new_h["second_pin_detour_used"] = True

    new_h["matched"] = _matched(board, cfg["target"])
    if check_level_complete(new_h, {}, new_h["level"]):
        new_h["complete"] = True
    elif new_h["budget_left"] <= 0:
        new_h["failed"] = True
    return new_h


def predict(h_t: dict) -> dict:
    return {}


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    cfg = LEVELS[level]
    req = cfg.get("goal_requirements", {})
    if req.get("matched") and not h_t.get("matched", False):
        return False
    if req.get("pin_detour_used") and not h_t.get("pin_detour_used", False):
        return False
    if req.get("second_pin_detour_used") and not h_t.get("second_pin_detour_used", False):
        return False
    if req.get("all_revealed") and not h_t.get("all_revealed", False):
        return False
    if req.get("spawn_a_done") and not h_t.get("spawn_a_done", False):
        return False
    if req.get("spawn_b_done") and not h_t.get("spawn_b_done", False):
        return False
    return _matched(h_t.get("board", []), cfg["target"])


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    grid = [[BG_COLOR for _ in range(32)] for _ in range(32)]
    cfg = LEVELS[h_t["level"]]

    # Title stripe and budget bar.
    _draw_entity(grid, 0, 0, "budget", max(0, h_t.get("budget_left", 0)))

    for r in range(cfg["rows"]):
        for c in range(cfg["cols"]):
            rr, cc = _cell_origin(r, c)
            _draw_entity(grid, rr, cc, "tray")
            token = h_t["board"][r][c]
            if token == "E":
                if "spawn" in cfg.get("active_tags", []) and (r, c) in cfg.get("spawn_targets", {}):
                    _draw_entity(grid, rr + 1, cc + 1, "spawn")
            else:
                _draw_entity(grid, rr + 1, cc + 1, "token", TOKEN_COLORS[token])

    if "pins" in cfg.get("active_tags", []):
        for r1, c1, r2, c2 in cfg.get("blocked_edges", []):
            rr1, cc1 = _cell_origin(r1, c1)
            rr2, cc2 = _cell_origin(r2, c2)
            if r1 == r2:
                _draw_entity(grid, rr1, max(cc1, cc2) - 1, "pin_h")
            elif c1 == c2:
                _draw_entity(grid, max(rr1, rr2) - 1, cc1 + 3, "pin_v")

    sel = h_t.get("selected")
    if sel is not None:
        rr, cc = _cell_origin(sel[0], sel[1])
        _draw_entity(grid, rr, cc, "selected")

    # Draw target recipe labels under the board. Hidden cards are local clickable reveal targets.
    revealed = [tuple(x) for x in h_t.get("revealed", [])]
    for r in range(cfg["rows"]):
        for c in range(cfg["cols"]):
            rr, cc = _target_origin(r, c, cfg.get("rows", 3))
            if "hidden" in cfg.get("active_tags", []) and (r, c) in cfg.get("hidden_cells", []) and (r, c) not in revealed:
                _draw_entity(grid, rr, cc, "hidden")
            else:
                _draw_entity(grid, rr, cc, "target", TOKEN_COLORS[cfg["target"][r][c]])

    # A solved board gets green sparkles on the side.
    if check_level_complete(h_t, z_t, h_t["level"]):
        for i in range(3):
            grid[5 + i * 2][26] = COLORS["idea"]
            grid[6 + i * 2][27] = COLORS["idea"]
    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    cfg = LEVELS[level]
    h_t = {
        "level": level,
        "step": 0,
        "board": copy.deepcopy(cfg["start"]),
        "selected": None,
        "budget_left": cfg["budget"],
        "matched": _matched(cfg["start"], cfg["target"]),
        "pin_detour_used": False,
        "second_pin_detour_used": False,
        "revealed": [],
        "all_revealed": len(cfg.get("hidden_cells", [])) == 0,
        "spawn_a_done": False,
        "spawn_b_done": False,
        "complete": False,
        "failed": False,
    }
    return h_t, predict(h_t)


def get_available_actions() -> list[int]:
    return [0, 6]


def solve_level(level: int) -> list:
    if level == 0:
        # Five distinct adjacent swaps at different cells.
        return [
            (6, 10, 6), (6, 14, 6),    # top row: S,P,Y -> P,S,Y
            (6, 14, 10), (6, 18, 10),  # middle row: P,Y,S -> P,S,Y
            (6, 10, 14), (6, 14, 14),  # bottom row route 1: Y,S,P -> S,Y,P
            (6, 14, 14), (6, 18, 14),  # bottom row route 2: S,Y,P -> S,P,Y
            (6, 10, 14), (6, 14, 14),  # bottom row finish: S,P,Y -> P,S,Y
        ]
    if level == 1:
        # Six swaps; the middle row must route around the visible orange pin.
        return [
            (6, 10, 6), (6, 14, 6),    # top left pair
            (6, 18, 6), (6, 22, 6),    # top right pair
            (6, 10, 14), (6, 14, 14),  # prepare lower bypass row
            (6, 14, 10), (6, 14, 14),  # bypass pinned left side downward
            (6, 18, 10), (6, 18, 14),  # bypass pinned right side downward
            (6, 14, 14), (6, 18, 14),  # restore lower row
        ]
    if level == 2:
        # Distinct board: pins sit on top and middle rows; route through vertical staging.
        return [
            (6, 10, 6), (6, 14, 6),
            (6, 10, 6), (6, 10, 10),
            (6, 14, 6), (6, 18, 6),
            (6, 14, 6), (6, 14, 10),
            (6, 18, 6), (6, 18, 10),
            (6, 14, 6), (6, 18, 6),
            (6, 10, 6), (6, 14, 6),
            (6, 22, 6), (6, 22, 10),
            (6, 18, 10), (6, 22, 10),
        ]
    if level == 3:
        # Reveal six local hidden recipe cards, then solve the expanded five-column board.
        return [
            (6, 17, 22),
            (6, 17, 25),
            (6, 17, 28),
            (6, 25, 22),
            (6, 25, 25),
            (6, 25, 28),
            (6, 10, 6), (6, 14, 6),
            (6, 14, 10), (6, 18, 10),
            (6, 10, 14), (6, 14, 14),
            (6, 14, 14), (6, 18, 14),
        ]
    if level == 4:
        # Reveal six hidden targets, then solve a 4x4 pinned board.
        return [
            (6, 13, 19),
            (6, 21, 19),
            (6, 17, 22),
            (6, 9, 25),
            (6, 21, 25),
            (6, 13, 28),
            (6, 10, 6), (6, 14, 6),
            (6, 14, 6), (6, 18, 6),
            (6, 14, 6), (6, 14, 10),
            (6, 18, 6), (6, 22, 6),
            (6, 18, 10), (6, 22, 10),
            (6, 18, 6), (6, 18, 10),
            (6, 14, 6), (6, 18, 6),
            (6, 10, 14), (6, 14, 14),
        ]
    if level == 5:
        # Spawn two missing pink layers locally, then sort the five-column recipe.
        return [
            (6, 26, 6),
            (6, 10, 14),
            (6, 10, 6), (6, 14, 6),
            (6, 14, 10), (6, 18, 10),
            (6, 14, 14), (6, 18, 14),
            (6, 18, 14), (6, 22, 14),
            (6, 22, 14), (6, 26, 14),
        ]
    if level == 6:
        # Combined hidden+spawn+pin: reveal, spawn, then use a top-row bypass for the pinned middle pair.
        return [
            (6, 9, 22),
            (6, 25, 22),
            (6, 13, 25),
            (6, 17, 25),
            (6, 9, 28),
            (6, 25, 28),
            (6, 26, 6),
            (6, 10, 14),
            (6, 14, 6), (6, 14, 10),
            (6, 18, 6), (6, 18, 10),
            (6, 14, 6), (6, 18, 6),
        ]
    if level == 7:
        # Final combined puzzle: reveal, spawn, then satisfy two distinct pin detours while sorting.
        return [
            (6, 13, 22),
            (6, 25, 22),
            (6, 9, 25),
            (6, 21, 25),
            (6, 9, 28),
            (6, 17, 28),
            (6, 26, 6),
            (6, 10, 14),
            (6, 18, 6), (6, 18, 10),
            (6, 18, 10), (6, 18, 14),
            (6, 18, 14), (6, 22, 14),
            (6, 14, 14), (6, 18, 14),
            (6, 22, 6), (6, 22, 10),
            (6, 22, 10), (6, 26, 10),
            (6, 14, 6), (6, 18, 6),
            (6, 10, 6), (6, 14, 6),
        ]
    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Rl2048(_FunctionalArcGame):
    GAME_ID = "rl2048-8deeab8c"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
