# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the ps7413/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
"""Pepper Stove (PS7413) - a pattern-reproduction click game.

The player clicks burner cells of a stove mesh. Each click cycles that
burner's spice color forward by one. Match the working mesh to the recipe
card to win. No avatar; the player edits board cells directly.
"""

import copy

BG_COLOR = 0

COLORS = {
    "border": 3,      # dark-gray burner border
    "divider": 2,     # gray panel divider
    "card_ring": 7,   # light-pink recipe ring
    "bar_full": 14,   # green budget bar
    "bar_used": 8,    # red used budget
    "token": 13,      # maroon pepper token
    "pip": 5,         # black center pip
    "lock_pin": 15,   # purple corner pin on a locked burner
}

def _geom(cols):
    """Return drawing geometry for a mesh with `cols` columns.

    3x3 meshes keep the original generous 5x5 burner boxes; larger meshes
    (4x4, 5x5) use tighter 4x4 boxes so the working panel and recipe panel
    both fit inside 32 columns.
    """
    if cols <= 3:
        return {
            "wrow0": 5, "wcol0": 3, "wcell": 6, "wbox": 5, "wint": 3,
            "crow0": 6, "ccol0": 20, "ccell": 4, "cbox": 3,
            "divider": 18,
        }
    if cols == 4:
        return {
            "wrow0": 2, "wcol0": 0, "wcell": 4, "wbox": 4, "wint": 2,
            "crow0": 2, "ccol0": 19, "ccell": 3, "cbox": 3,
            "divider": 18,
        }
    # 5x5 (or larger) mesh: compact 3x3 boxes so both panels fit in 32 cols.
    return {
        "wrow0": 2, "wcol0": 0, "wcell": 3, "wbox": 3, "wint": 1,
        "crow0": 2, "ccol0": 16, "ccell": 3, "cbox": 3,
        "divider": 15,
    }

LEVELS = {
    0: {
        "rows": 3,
        "cols": 3,
        "cycle": [6, 10, 11],  # pink, light-blue, yellow
        # working mesh starting color indices (flat row-major)
        "start": [0, 1, 2, 1, 2, 0, 2, 0, 1],
        # recipe card target color indices (flat row-major)
        "target": [1, 1, 0, 0, 2, 2, 2, 1, 2],
        "budget": 14,
        "active_tags": [],
        "goal_requirements": {},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "primary_blocker": "every burner starts on the wrong spice color",
            "dependencies": [
                "cycle each mismatched burner the exact number of clicks",
            ],
            "feedback": "each clicked burner's interior color advances visibly",
            "bypass_guard": "win only when all 9 interiors equal the recipe",
            "state_key": "matches_target",
        },
    },
    1: {
        "rows": 3,
        "cols": 3,
        # Full 5-color spice cycle: pink, light-blue, yellow, green, orange.
        "cycle": [6, 10, 11, 14, 12],
        "start": [0, 2, 4, 1, 3, 0, 4, 2, 3],
        "target": [3, 0, 1, 4, 3, 2, 1, 0, 4],
        # Exact clicks needed = 26; small headroom to discourage free tapping.
        "budget": 34,
        "active_tags": [],
        "goal_requirements": {},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "primary_blocker": "five-color cycle wraps, so overshoot is costly",
            "dependencies": [
                "count exact forward cycle distance for each burner",
            ],
            "feedback": "each clicked burner advances one step through 5 colors",
            "bypass_guard": "win only when all 9 interiors equal the recipe",
            "state_key": "matches_target",
        },
    },
    2: {
        "rows": 4,
        "cols": 4,
        # 4-color cycle on a larger 4x4 mesh (16 burners).
        "cycle": [6, 10, 11, 14],
        "start": [0, 1, 2, 3,
                  3, 2, 1, 0,
                  1, 3, 0, 2,
                  2, 0, 3, 1],
        "target": [2, 3, 0, 1,
                   1, 0, 3, 2,
                   3, 1, 2, 0,
                   0, 2, 1, 3],
        # Exact clicks = 16 cells * 2 = 32; headroom for exploration.
        "budget": 46,
        "active_tags": [],
        "goal_requirements": {},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "primary_blocker": "16 burners each need their own cycle distance",
            "dependencies": [
                "count exact forward distance for each of 16 burners",
            ],
            "feedback": "each clicked burner advances one step through 4 colors",
            "bypass_guard": "win only when all 16 interiors equal the recipe",
            "state_key": "matches_target",
        },
    },
    3: {
        "rows": 4,
        "cols": 4,
        "cycle": [6, 10, 11, 14],
        "start": [1, 0, 3, 2,
                  2, 3, 0, 1,
                  0, 2, 1, 3,
                  3, 1, 2, 0],
        "target": [3, 2, 0, 1,
                   0, 1, 2, 3,
                   2, 0, 3, 1,
                   1, 3, 0, 2],
        # One pepper token gates burner index 10; it must be collected first.
        "tokens": [
            {"r": 23, "c": 6, "unlocks": 10, "item": "pepper"},
        ],
        "budget": 50,
        "active_tags": ["collectible"],
        "goal_requirements": {"required_items": ["pepper"]},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "primary_blocker": "burner 10 is locked until the pepper token is collected",
            "dependencies": [
                "click the pepper token to collect it",
                "then cycle every burner (incl. the unlocked one) to target",
            ],
            "feedback": "lock pins disappear from burner 10 once token is taken",
            "bypass_guard": "locked burner cannot be cycled, so the recipe "
                            "cannot match until the token is collected",
            "state_key": "matches_target",
        },
    },
    4: {
        "rows": 4,
        "cols": 4,
        "cycle": [6, 10, 11, 14, 12],
        "start": [2, 4, 1, 3,
                  0, 3, 2, 4,
                  4, 1, 3, 0,
                  3, 0, 4, 2],
        "target": [0, 2, 3, 1,
                   4, 1, 0, 2,
                   1, 3, 2, 4,
                   2, 4, 1, 0],
        # Two pepper tokens lock two separate burners (indices 5 and 11).
        "tokens": [
            {"r": 22, "c": 4, "unlocks": 5, "item": "red_pepper"},
            {"r": 22, "c": 11, "unlocks": 11, "item": "green_pepper"},
        ],
        "budget": 70,
        "active_tags": ["collectible"],
        "goal_requirements": {"required_items": ["red_pepper", "green_pepper"]},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "primary_blocker": "two burners (5 and 11) are locked by two tokens",
            "dependencies": [
                "collect both pepper tokens",
                "cycle every burner including the two unlocked ones",
            ],
            "feedback": "lock pins clear from each burner as its token is taken",
            "bypass_guard": "neither locked burner can be cycled until its "
                            "matching pepper token is collected",
            "state_key": "matches_target",
        },
    },
    5: {
        "rows": 4,
        "cols": 4,
        "cycle": [6, 10, 11, 14, 12],
        "start": [0, 1, 2, 3,
                  4, 0, 1, 2,
                  3, 4, 0, 1,
                  2, 3, 4, 0],
        "target": [2, 3, 4, 0,
                   1, 2, 3, 4,
                   0, 1, 2, 3,
                   4, 0, 1, 2],
        # No tokens; fog hides the recipe cards until each is clicked.
        "budget": 78,
        "active_tags": ["fog"],
        "goal_requirements": {"reveal_all_cards": True},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "primary_blocker": "every recipe card is hidden under a fog veil",
            "dependencies": [
                "click each covered recipe card to reveal its target color",
                "cycle each burner to the revealed target",
            ],
            "feedback": "a clicked card's fog clears to show the spice color",
            "bypass_guard": "the recipe is unreadable under fog and completion "
                            "requires every card revealed, so matching requires "
                            "revealing the cards first",
            "state_key": "matches_target",
        },
    },
    6: {
        "rows": 5,
        "cols": 5,
        "cycle": [6, 10, 11, 14, 12],
        "start": [0, 1, 2, 3, 4,
                  4, 0, 1, 2, 3,
                  3, 4, 0, 1, 2,
                  2, 3, 4, 0, 1,
                  1, 2, 3, 4, 0],
        "target": [1, 2, 3, 4, 0,
                   2, 3, 4, 0, 1,
                   3, 4, 0, 1, 2,
                   4, 0, 1, 2, 3,
                   0, 1, 2, 3, 4],
        # One pepper token locks burner 12 (center); fog hides the recipe.
        "tokens": [
            {"r": 20, "c": 4, "unlocks": 12, "item": "pepper"},
        ],
        "budget": 104,
        "active_tags": ["fog", "collectible"],
        "goal_requirements": {
            "required_items": ["pepper"],
            "reveal_all_cards": True,
        },
        "design_contract": {
            "success_trigger": "board_matches_target",
            "primary_blocker": "recipe hidden by fog AND center burner locked",
            "dependencies": [
                "reveal every recipe card from under fog",
                "collect the pepper token to unlock the center burner",
                "cycle all 25 burners to their revealed targets",
            ],
            "feedback": "fog clears per clicked card; lock pins clear on collect",
            "bypass_guard": "the recipe is unreadable and the center burner "
                            "cannot be cycled until both are resolved",
            "state_key": "matches_target",
        },
    },
    7: {
        "rows": 5,
        "cols": 5,
        "cycle": [6, 10, 11, 14, 12],
        "start": [2, 0, 3, 1, 4,
                  1, 4, 2, 0, 3,
                  0, 3, 1, 4, 2,
                  4, 2, 0, 3, 1,
                  3, 1, 4, 2, 0],
        "target": [0, 1, 2, 3, 4,
                   3, 4, 0, 1, 2,
                   1, 2, 3, 4, 0,
                   4, 0, 1, 2, 3,
                   2, 3, 4, 0, 1],
        # Three pepper tokens lock three scattered burners.
        "tokens": [
            {"r": 19, "c": 1, "unlocks": 6, "item": "red_pepper"},
            {"r": 19, "c": 6, "unlocks": 12, "item": "green_pepper"},
            {"r": 19, "c": 11, "unlocks": 18, "item": "gold_pepper"},
        ],
        "budget": 120,
        "active_tags": ["fog", "collectible"],
        "goal_requirements": {
            "required_items": ["red_pepper", "green_pepper", "gold_pepper"],
            "reveal_all_cards": True,
        },
        "design_contract": {
            "success_trigger": "board_matches_target",
            "primary_blocker": "full fog hides the recipe and three burners are locked",
            "dependencies": [
                "reveal all 25 recipe cards from under fog",
                "collect all three pepper tokens to unlock burners 6, 12, 18",
                "cycle every burner to its revealed target color",
            ],
            "feedback": "fog clears per card; lock pins clear as each token is taken",
            "bypass_guard": "the recipe is unreadable and the three locked "
                            "burners cannot be cycled until every token is collected",
            "state_key": "matches_target",
        },
    },
}


def _burner_box(i, j, cols):
    """Return (top, left) of working burner (i, j) box."""
    g = _geom(cols)
    return g["wrow0"] + i * g["wcell"], g["wcol0"] + j * g["wcell"]


def _burner_center(i, j, cols):
    g = _geom(cols)
    top, left = _burner_box(i, j, cols)
    off = g["wbox"] // 2
    return top + off, left + off  # (row, col)


def _hit_burner(x, y, rows, cols):
    """Map a click (x=col, y=row) to a burner index, or None."""
    g = _geom(cols)
    b = g["wbox"]
    for i in range(rows):
        for j in range(cols):
            top, left = _burner_box(i, j, cols)
            if top <= y <= top + b - 1 and left <= x <= left + b - 1:
                return i * cols + j
    return None


def _hit_token(x, y, cfg):
    """Map a click to a pepper token index, or None. Tokens are 3x3 boxes."""
    for ti, tok in enumerate(cfg.get("tokens", [])):
        tr, tc = tok["r"], tok["c"]
        if tr <= y <= tr + 2 and tc <= x <= tc + 2:
            return ti
    return None


def _hit_card(x, y, rows, cols):
    """Map a click in the recipe panel to a card index, or None."""
    g = _geom(cols)
    cb = g["cbox"]
    for i in range(rows):
        for j in range(cols):
            top = g["crow0"] + i * g["ccell"]
            left = g["ccol0"] + j * g["ccell"]
            if top <= y <= top + cb - 1 and left <= x <= left + cb - 1:
                return i * cols + j
    return None


def get_available_actions():
    return [6]


def get_initial_state(level):
    cfg = LEVELS[level]
    h_t = {
        "level": level,
        "step": 0,
        "moves_left": cfg["budget"],
        "grid_idx": list(cfg["start"]),
        "collected": [],   # indices of collected pepper tokens
        "inventory": [],   # item names of collected tokens
        "revealed": [],    # indices of recipe cards revealed from under fog
        "reveal_all_cards": ("fog" not in cfg.get("active_tags", [])),
    }
    z_t = {}
    return h_t, z_t


def predict(h_t, seed):
    return {}


def _locked_burner_idx(cfg, collected):
    """Return set of burner indices currently locked (token not yet taken)."""
    locked = set()
    for ti, tok in enumerate(cfg.get("tokens", [])):
        if ti not in collected:
            locked.add(tok["unlocks"])
    return locked


def transition(h_t, z_t, a_t):
    h = copy.deepcopy(h_t)
    cfg = LEVELS[h["level"]]
    rows, cols = cfg["rows"], cfg["cols"]
    cyc = len(cfg["cycle"])

    # Guard: only CLICK actions are valid.
    if not (isinstance(a_t, (tuple, list)) and len(a_t) == 3 and a_t[0] == 6):
        return h

    _, x, y = a_t
    if h["moves_left"] <= 0:
        return h

    # First, check pepper tokens (collectibles).
    ti = _hit_token(x, y, cfg)
    if ti is not None:
        if ti in h["collected"]:
            return h  # already collected -> rejected, no time advance
        h["collected"].append(ti)
        item = cfg["tokens"][ti].get("item")
        if item is not None and item not in h["inventory"]:
            h["inventory"].append(item)
        h["step"] += 1
        h["moves_left"] -= 1
        return h

    # Under fog, a click on a covered recipe card reveals it (memory peek).
    if "fog" in cfg.get("active_tags", []):
        ci = _hit_card(x, y, rows, cols)
        if ci is not None:
            if ci in h["revealed"]:
                return h  # already revealed -> rejected, no time advance
            h["revealed"].append(ci)
            total = rows * cols
            if len(set(h["revealed"])) >= total:
                h["reveal_all_cards"] = True
            h["step"] += 1
            h["moves_left"] -= 1
            return h

    # Otherwise, check burner cells.
    idx = _hit_burner(x, y, rows, cols)
    if idx is None:
        return h  # missed everything -> rejected input

    # Locked burner: refuse to cycle until its token is collected.
    if idx in _locked_burner_idx(cfg, h["collected"]):
        return h

    h["grid_idx"][idx] = (h["grid_idx"][idx] + 1) % cyc
    h["step"] += 1
    h["moves_left"] -= 1
    return h


def check_level_complete(h_t, z_t, level):
    cfg = LEVELS[level]
    req = cfg.get("goal_requirements", {})
    # Enforce explicit collectible requirements.
    for item in req.get("required_items", []):
        if item not in h_t.get("inventory", []):
            return False
    # Under fog, require every recipe card to have been revealed.
    if req.get("reveal_all_cards"):
        if not h_t.get("reveal_all_cards"):
            return False
    return list(h_t["grid_idx"]) == list(cfg["target"])


def _set_box(grid, top, left, size, color):
    for r in range(top, top + size):
        for c in range(left, left + size):
            if 0 <= r < 32 and 0 <= c < 32:
                grid[r][c] = color


def render(h_t, z_t):
    grid = [[BG_COLOR for _ in range(32)] for _ in range(32)]
    cfg = LEVELS[h_t["level"]]
    rows, cols = cfg["rows"], cfg["cols"]
    cycle = cfg["cycle"]
    g = _geom(cols)

    # Vertical divider between working mesh and recipe panel.
    for r in range(2, 30):
        grid[r][g["divider"]] = COLORS["divider"]

    # Working burners: bordered box with interior color fill.
    wb, wi = g["wbox"], g["wint"]
    locked = _locked_burner_idx(cfg, h_t.get("collected", []))
    for i in range(rows):
        for j in range(cols):
            k = i * cols + j
            top, left = _burner_box(i, j, cols)
            _set_box(grid, top, left, wb, COLORS["border"])
            color = cycle[h_t["grid_idx"][k]]
            _set_box(grid, top + 1, left + 1, wi, color)
            # Locked burners show a purple corner pin until unlocked.
            if k in locked:
                grid[top][left] = COLORS["lock_pin"]
                grid[top][left + wb - 1] = COLORS["lock_pin"]
                grid[top + wb - 1][left] = COLORS["lock_pin"]
                grid[top + wb - 1][left + wb - 1] = COLORS["lock_pin"]

    # Pepper tokens: maroon 3x3 box. The center pip uses the purple lock
    # color so a token visibly shares its marker with the locked burner
    # (purple corner pins) it unlocks.
    for ti, tok in enumerate(cfg.get("tokens", [])):
        if ti in h_t.get("collected", []):
            continue
        tr, tc = tok["r"], tok["c"]
        _set_box(grid, tr, tc, 3, COLORS["token"])
        grid[tr + 1][tc + 1] = COLORS["lock_pin"]

    # Recipe cards: ring (light-pink) with target color center pip.
    # Under fog, unrevealed cards are covered with a black veil.
    cb = g["cbox"]
    fog = "fog" in cfg.get("active_tags", [])
    revealed = h_t.get("revealed", [])
    for i in range(rows):
        for j in range(cols):
            k = i * cols + j
            top = g["crow0"] + i * g["ccell"]
            left = g["ccol0"] + j * g["ccell"]
            if fog and k not in revealed:
                _set_box(grid, top, left, cb, 5)  # black fog veil
                continue
            _set_box(grid, top, left, cb, COLORS["card_ring"])
            grid[top + 1][left + 1] = cycle[cfg["target"][k]]

    # Budget bar on row 31.
    total = cfg["budget"]
    left_n = max(0, h_t["moves_left"])
    span = min(total, 32)
    for c in range(span):
        filled = c < int(round(left_n / total * span)) if total else False
        grid[31][c] = COLORS["bar_full"] if filled else COLORS["bar_used"]

    return grid


def solve_level(level):
    cfg = LEVELS[level]
    rows, cols = cfg["rows"], cfg["cols"]
    cyc = len(cfg["cycle"])
    start = cfg["start"]
    target = cfg["target"]
    actions = []
    # Under fog, reveal each covered recipe card first (read the recipe).
    if "fog" in cfg.get("active_tags", []):
        g = _geom(cols)
        cb = g["cbox"]
        for i in range(rows):
            for j in range(cols):
                top = g["crow0"] + i * g["ccell"]
                left = g["ccol0"] + j * g["ccell"]
                actions.append((6, left + cb // 2, top + cb // 2))
    # First collect every required pepper token (unlocks locked burners).
    for ti, tok in enumerate(cfg.get("tokens", [])):
        actions.append((6, tok["c"] + 1, tok["r"] + 1))
    # Then cycle each burner to its target color.
    for i in range(rows):
        for j in range(cols):
            k = i * cols + j
            dist = (target[k] - start[k]) % cyc
            if dist == 0:
                continue
            cr, cc = _burner_center(i, j, cols)
            for _ in range(dist):
                actions.append((6, cc, cr))  # (6, x=col, y=row)
    return actions


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Ps7413(_FunctionalArcGame):
    GAME_ID = "ps7413-3a14ed61"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
