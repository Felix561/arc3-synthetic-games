# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the fl5273/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
"""Floodlight Lockdown (FL5273) - a Sokoban game.

Push generator crates (yellow) onto anchor pads (green ring) so the whole
urban block is lit and "held" under lockdown. Directional game: UP/DOWN/
LEFT/RIGHT. Win depends on object arrangement, not player position.
Fully deterministic.
"""

import copy

# ----------------------------------------------------------------------------
# Module-level constants
# ----------------------------------------------------------------------------
BG_COLOR = 4          # near-black plaza / floor
CELL = 5              # each board cell is a 5x5 pixel block
OFFSET = 1            # 1-pixel margin so a 6x6 board fits in 30px (rows 1..30)

COLORS = {
    "wall": 2,        # gray building
    "floor": BG_COLOR,
    "floor_dot": 3,   # dark-gray center dot on floor
    "player": 12,     # orange warden (cross)
    "crate": 11,      # yellow generator crate (hollow)
    "pad": 14,        # green anchor pad (ring)
    "barricade": 13,  # maroon brittle barricade
    "barricade_stripe": 8,  # red stripe accent
    "spark": 6,       # pink spark tile (impassable until ignited)
    "spark_core": 15, # purple core accent
    "crate_on_pad": 11,  # lit crate interior (green border + yellow core)
    "hud": 10,        # light-blue budget bar
}

# Each LEVELS entry: static layout ('#'=wall, '.'=floor) + dynamic seeds.
LEVELS = {
    0: {
        "layout": [
            "######",
            "#....#",
            "#....#",
            "#....#",
            "#....#",
            "######",
        ],
        "player_start": (1, 1),
        "crates": [(2, 1), (3, 3)],
        "pads": [(4, 1), (4, 4)],
        "budget": 18,
        "active_tags": [],
        "goal_requirements": {},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "all_pads_covered",
            "primary_blocker": "both anchor pads start empty; crates are far from them",
            "dependencies": [
                "push left crate down two cells onto its pad",
                "reposition warden around to approach the second crate from above",
                "push second crate down then shove it right onto its pad",
            ],
            "feedback": "a covered pad renders as a lit crate (green border, yellow core)",
            "bypass_guard": "completion requires every pad covered, not the warden standing anywhere",
        },
    },
    1: {
        "layout": [
            "######",
            "#....#",
            "#.cc.#",
            "#.#..#",
            "#p..p#",
            "######",
        ],
        "player_start": (1, 1),
        "crates": [(2, 2), (2, 3)],
        "pads": [(4, 1), (4, 4)],
        "budget": 28,
        "active_tags": [],
        "goal_requirements": {},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "all_pads_covered",
            "primary_blocker": "a wall pillar splits the lower room; the two pads sit in opposite bottom corners",
            "dependencies": [
                "push one crate toward the left pad along a lane that clears the pillar",
                "route the warden across the top without trapping the second crate",
                "push the second crate down the right lane onto the right pad",
            ],
            "feedback": "each covered pad renders as a lit crate (green border, yellow core)",
            "bypass_guard": "the pillar forces a push order; a wrong first push corners a crate so a pad cannot be covered",
        },
    },
    2: {
        "layout": [
            "######",
            "#...p#",
            "#cc#.#",
            "#.c..#",
            "#p..p#",
            "######",
        ],
        "player_start": (1, 1),
        "crates": [(2, 1), (2, 2), (3, 2)],
        "pads": [(1, 4), (4, 1), (4, 4)],
        "budget": 30,
        "active_tags": [],
        "goal_requirements": {},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "all_pads_covered",
            "primary_blocker": "three crates packed in a narrow aisle; a wall pillar blocks the direct lane to the top pad",
            "dependencies": [
                "clear the lower crate down to a bottom-corner pad first to free the aisle",
                "route a crate up and around the pillar to the top-right pad",
                "stage the last crate to the remaining bottom pad without jamming the aisle",
            ],
            "feedback": "each covered pad renders as a lit crate (green border, yellow core)",
            "bypass_guard": "the packed aisle and pillar force an order; an early wrong push corners a crate so a pad cannot be covered",
        },
    },
    3: {
        "layout": [
            "######",
            "#p..p#",
            "#cmc.#",
            "#.c..#",
            "#..p.#",
            "######",
        ],
        "player_start": (1, 1),
        "crates": [(2, 1), (2, 3), (3, 2)],
        "pads": [(1, 1), (1, 4), (4, 3)],
        "barricades": [(2, 2)],
        "budget": 25,
        "active_tags": ["destructible"],
        "goal_requirements": {"barricades_cleared": 1},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "all_pads_covered",
            "primary_blocker": "a brittle barricade blocks the only lane connecting the left and right halves",
            "dependencies": [
                "push a crate into the barricade to destroy it and open the central lane",
                "stage crates through the cleared lane to the far pads",
                "cover all three pads without cornering a crate against a wall",
            ],
            "feedback": "the maroon striped barricade disappears once a crate is shoved into it; covered pads light up",
            "bypass_guard": "with the barricade intact the right-side pads are unreachable, so it must be destroyed first",
        },
    },
    4: {
        "layout": [
            "######",
            "#pc.p#",
            "#.m#.#",
            "#.cm.#",
            "#pc..#",
            "######",
        ],
        "player_start": (1, 1),
        "crates": [(1, 2), (3, 2), (4, 2)],
        "pads": [(1, 1), (1, 4), (4, 1)],
        "barricades": [(2, 2), (3, 3)],
        "budget": 38,
        "active_tags": ["destructible"],
        "goal_requirements": {"barricades_cleared": 2},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "all_pads_covered",
            "primary_blocker": "two brittle barricades, with a wall pillar, gate the routes to the far pads",
            "dependencies": [
                "destroy the upper barricade so a crate can pass through the left column",
                "destroy the lower barricade to open the route to the right pad",
                "stage all three crates to their pads in an order that does not corner any crate",
            ],
            "feedback": "each maroon barricade vanishes when a crate is shoved into it; covered pads light up",
            "bypass_guard": "with either barricade intact a pad is unreachable, so both must be destroyed",
        },
    },
    5: {
        "layout": [
            "######",
            "#..p.#",
            "#.css#",
            "#pc..#",
            "#.cp.#",
            "######",
        ],
        "player_start": (1, 1),
        "crates": [(2, 2), (3, 2), (4, 2)],
        "pads": [(1, 3), (3, 1), (4, 3)],
        "sparks": [(2, 3), (2, 4)],
        "budget": 26,
        "active_tags": ["spread"],
        "goal_requirements": {"sparks_remaining": 0},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "all_pads_covered",
            "primary_blocker": "pink spark tiles wall off the top-right pad and cannot be entered or pushed through",
            "dependencies": [
                "cover the bottom pad adjacent to the spark cluster to ignite it",
                "the ignition spreads and clears the spark tiles, opening the corridor",
                "route the remaining crates to the now-reachable pads",
            ],
            "feedback": "the pink spark tiles vanish (burn away) once their adjacent pad is covered",
            "bypass_guard": "with sparks intact the far pad is unreachable; only covering the seed pad ignites and clears them",
        },
    },
    6: {
        "layout": [
            "######",
            "#p..p#",
            "#cmc.#",
            "#.css#",
            "#..p.#",
            "######",
        ],
        "player_start": (1, 1),
        "crates": [(2, 1), (2, 3), (3, 2)],
        "pads": [(1, 1), (1, 4), (4, 3)],
        "barricades": [(2, 2)],
        "sparks": [(3, 3), (3, 4)],
        "budget": 30,
        "active_tags": ["destructible", "spread"],
        "goal_requirements": {"barricades_cleared": 1, "sparks_remaining": 0},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "all_pads_covered",
            "primary_blocker": "a brittle barricade splits the room and a pink spark cluster walls off the bottom pad",
            "dependencies": [
                "shove a crate into the barricade to open the central lane",
                "cover the bottom pad's seed cell to ignite and clear the spark cluster",
                "stage all three crates to their pads in a non-cornering order",
            ],
            "feedback": "the maroon barricade and the pink sparks both disappear as they are cleared; covered pads light up",
            "bypass_guard": "with the barricade intact the right half is cut off and with sparks intact the bottom pad is unreachable, so both must be cleared",
        },
    },
    7: {
        "layout": [
            "######",
            "#....#",
            "#....#",
            "#....#",
            "#....#",
            "######",
        ],
        "player_start": (1, 2),
        "crates": [(2, 2), (2, 3), (3, 2)],
        "pads": [(1, 1), (1, 4), (4, 1)],
        "barricades": [(4, 3)],
        "sparks": [(2, 1), (3, 1)],
        "budget": 34,
        "active_tags": ["destructible", "spread"],
        "goal_requirements": {"barricades_cleared": 1, "sparks_remaining": 0},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "all_pads_covered",
            "primary_blocker": "a pink spark column seals the left lane and a brittle barricade blocks the bottom route; three crates must reach three corner pads",
            "dependencies": [
                "cover the top-left corner pad to ignite and clear the spark column",
                "shove a crate into the bottom barricade to open that route",
                "stage all three crates across the now-open board to the corner pads in a non-cornering order",
            ],
            "feedback": "the pink sparks burn away and the maroon barricade shatters as they are cleared; covered pads light up",
            "bypass_guard": "with sparks intact the left lane is closed and with the barricade intact the bottom route is sealed, so both must be cleared",
        },
    },
}

# Directional deltas
_DELTA = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def _walls(level):
    layout = LEVELS[level]["layout"]
    w = set()
    for r, row in enumerate(layout):
        for c, ch in enumerate(row):
            if ch == "#":
                w.add((r, c))
    return w


def _draw_entity(grid, r, c, kind):
    """Render one board cell as a distinctive 5x5 pixel shape."""
    top = OFFSET + r * CELL
    left = OFFSET + c * CELL

    def fill(color):
        for i in range(CELL):
            for j in range(CELL):
                grid[top + i][left + j] = color

    if kind == "wall":
        fill(COLORS["wall"])
    elif kind == "floor":
        fill(BG_COLOR)
        grid[top + 2][left + 2] = COLORS["floor_dot"]
    elif kind == "player":
        # orange plus/cross on dark body
        fill(BG_COLOR)
        for j in range(CELL):
            grid[top + 2][left + j] = COLORS["player"]
        for i in range(CELL):
            grid[top + i][left + 2] = COLORS["player"]
    elif kind == "crate":
        # yellow hollow box with a small core dot
        fill(COLORS["crate"])
        for i in range(1, CELL - 1):
            for j in range(1, CELL - 1):
                grid[top + i][left + j] = BG_COLOR
        grid[top + 2][left + 2] = COLORS["crate"]
    elif kind == "pad":
        # green ring / donut, hollow center
        fill(BG_COLOR)
        for i in range(CELL):
            grid[top + i][left] = COLORS["pad"]
            grid[top + i][left + CELL - 1] = COLORS["pad"]
        for j in range(CELL):
            grid[top][left + j] = COLORS["pad"]
            grid[top + CELL - 1][left + j] = COLORS["pad"]
    elif kind == "barricade":
        # maroon diagonal-striped breakable block
        fill(COLORS["barricade"])
        for i in range(CELL):
            for j in range(CELL):
                if (i + j) % 2 == 0:
                    grid[top + i][left + j] = COLORS["barricade_stripe"]
    elif kind == "spark":
        # pink ring with purple core - impassable spark tile
        fill(COLORS["spark"])
        for i in range(1, CELL - 1):
            for j in range(1, CELL - 1):
                grid[top + i][left + j] = COLORS["spark_core"]
        grid[top + 2][left + 2] = COLORS["spark"]
    elif kind == "crate_on_pad":
        # lit: green border, yellow interior
        fill(COLORS["pad"])
        for i in range(1, CELL - 1):
            for j in range(1, CELL - 1):
                grid[top + i][left + j] = COLORS["crate_on_pad"]


# ----------------------------------------------------------------------------
# Required game functions
# ----------------------------------------------------------------------------
def get_available_actions():
    """Directional Sokoban: UP/DOWN/LEFT/RIGHT only."""
    return [1, 2, 3, 4]


def predict(h_t, seed):
    """Fully deterministic: no latent state."""
    return {}


def get_initial_state(level):
    L = LEVELS[level]
    pr, pc = L["player_start"]
    h_t = {
        "level": level,
        "step": 0,
        "player_r": pr,
        "player_c": pc,
        "crates": [list(crate) for crate in L["crates"]],
        "barricades": [list(b) for b in L.get("barricades", [])],
        "barricades_cleared": 0,
        "sparks": [list(s) for s in L.get("sparks", [])],
        "sparks_remaining": len(L.get("sparks", [])),
        "all_pads_covered": False,
    }
    _spread_sparks(h_t, level)
    h_t["sparks_remaining"] = len(h_t["sparks"])
    return h_t, {}


def transition(h_t, z_t, a_t):
    h = copy.deepcopy(h_t)

    # 1. Guard: only this game's directional actions are valid.
    if a_t not in _DELTA:
        return h

    level = h["level"]
    walls = _walls(level)
    dr, dc = _DELTA[a_t]
    pr, pc = h["player_r"], h["player_c"]
    tr, tc = pr + dr, pc + dc

    crate_set = {(cr, cc) for cr, cc in h["crates"]}
    bar_set = {(br, bc) for br, bc in h.get("barricades", [])}
    spark_set = {(sr, sc) for sr, sc in h.get("sparks", [])}
    has_barr = "destructible" in LEVELS[level].get("active_tags", [])
    has_spread = "spread" in LEVELS[level].get("active_tags", [])

    # 2/3. Blocked by wall -> rejected input, do not advance.
    if (tr, tc) in walls:
        return h

    # Walking directly into a barricade is blocked (must push a crate into it).
    if has_barr and (tr, tc) in bar_set:
        return h

    # Walking into an un-ignited spark tile is blocked.
    if has_spread and (tr, tc) in spark_set:
        return h

    # Pushing a crate?
    if (tr, tc) in crate_set:
        br, bc = tr + dr, tc + dc
        # crate blocked by wall, another crate, or a spark tile -> rejected.
        if (br, bc) in walls or (br, bc) in crate_set:
            return h
        if has_spread and (br, bc) in spark_set:
            return h
        # crate pushed into a barricade -> destroy barricade, crate & player stay.
        if has_barr and (br, bc) in bar_set:
            h["barricades"] = [list(b) for b in h["barricades"]
                               if not (b[0] == br and b[1] == bc)]
            h["barricades_cleared"] = h.get("barricades_cleared", 0) + 1
            h["step"] += 1
            _spread_sparks(h, level)
            h["all_pads_covered"] = _pads_covered(h, level)
            return h
        # commit push
        for crate in h["crates"]:
            if crate[0] == tr and crate[1] == tc:
                crate[0], crate[1] = br, bc
                break
        h["player_r"], h["player_c"] = tr, tc
        h["step"] += 1
        _spread_sparks(h, level)
        h["all_pads_covered"] = _pads_covered(h, level)
        return h

    # Plain move onto floor.
    h["player_r"], h["player_c"] = tr, tc
    h["step"] += 1
    _spread_sparks(h, level)
    h["all_pads_covered"] = _pads_covered(h, level)
    return h


def _spread_sparks(h, level):
    """Clear spark tiles 4-connected to any spark adjacent to a covered pad."""
    if "spread" not in LEVELS[level].get("active_tags", []):
        return
    sparks = {(sr, sc) for sr, sc in h.get("sparks", [])}
    if not sparks:
        return
    crate_set = {(cr, cc) for cr, cc in h["crates"]}
    pads = [tuple(p) for p in LEVELS[level]["pads"]]
    seeds = []
    for p in pads:
        if p in crate_set:
            for dr, dc in _DELTA.values():
                n = (p[0] + dr, p[1] + dc)
                if n in sparks:
                    seeds.append(n)
    stack = list(seeds)
    while stack:
        cell = stack.pop()
        if cell in sparks:
            sparks.discard(cell)
            for dr, dc in _DELTA.values():
                n = (cell[0] + dr, cell[1] + dc)
                if n in sparks:
                    stack.append(n)
    h["sparks"] = [list(s) for s in sparks]
    h["sparks_remaining"] = len(sparks)


def _pads_covered(h, level):
    crate_set = {(cr, cc) for cr, cc in h["crates"]}
    pads = [tuple(p) for p in LEVELS[level]["pads"]]
    return all(p in crate_set for p in pads)


def check_level_complete(h_t, z_t, level):
    L = LEVELS[level]
    req = L.get("goal_requirements", {})
    if "barricades_cleared" in req:
        if h_t.get("barricades_cleared", 0) < req["barricades_cleared"]:
            return False
    if "sparks_remaining" in req:
        if h_t.get("sparks_remaining", len(h_t.get("sparks", []))) > req["sparks_remaining"]:
            return False
    return _pads_covered(h_t, level)


def render(h_t, z_t):
    level = h_t["level"]
    L = LEVELS[level]
    layout = L["layout"]
    grid = [[BG_COLOR] * 32 for _ in range(32)]

    # static terrain
    for r, row in enumerate(layout):
        for c, ch in enumerate(row):
            _draw_entity(grid, r, c, "wall" if ch == "#" else "floor")

    crate_set = {(cr, cc) for cr, cc in h_t["crates"]}
    pad_set = {tuple(p) for p in L["pads"]}

    # pads not yet covered
    for p in pad_set:
        if p not in crate_set:
            _draw_entity(grid, p[0], p[1], "pad")

    # destructible barricades
    for (br, bc) in h_t.get("barricades", []):
        _draw_entity(grid, br, bc, "barricade")

    # spark tiles (impassable until ignited by a covered adjacent pad)
    for (sr, sc) in h_t.get("sparks", []):
        _draw_entity(grid, sr, sc, "spark")

    # crates (lit if on a pad)
    for (cr, cc) in h_t["crates"]:
        kind = "crate_on_pad" if (cr, cc) in pad_set else "crate"
        _draw_entity(grid, cr, cc, kind)

    # player
    _draw_entity(grid, h_t["player_r"], h_t["player_c"], "player")

    # HUD: remaining budget bar across row 0
    remaining = max(0, L["budget"] - h_t["step"])
    for j in range(min(remaining, 32)):
        grid[0][j] = COLORS["hud"]

    return grid


def solve_level(level):
    if level == 0:
        # push left crate down x2; circle up and over; push right crate down then right
        return [2, 2, 1, 4, 4, 2, 3, 2, 4]
    if level == 1:
        return [4, 4, 2, 2, 1, 1, 3, 3, 2, 2, 2, 4, 4, 1, 1, 3, 1, 3, 2, 2]
    if level == 2:
        return [2, 2, 4, 4, 3, 3, 1, 1, 4, 4, 4, 2, 2, 3, 3, 1, 3, 1, 4, 4]
    if level == 3:
        return [4, 4, 2, 4, 2, 2, 3, 3, 1, 1, 3, 1, 4, 4, 2, 4, 1]
    if level == 4:
        return [2, 2, 4, 2, 4, 1, 1, 4, 4, 2, 3, 1, 4, 1, 1, 3, 3, 2, 3, 2, 4, 4, 2, 3, 4, 4, 1, 1]
    if level == 5:
        return [2, 2, 2, 4, 3, 1, 4, 1, 3, 1, 4, 2, 4, 4, 2, 3, 3]
    if level == 6:
        return [4, 4, 4, 2, 3, 1, 3, 3, 2, 2, 3, 1, 2, 2, 4, 1, 1, 4, 2, 4, 1]
    if level == 7:
        return [4, 2, 2, 2, 4, 2, 3, 3, 4, 1, 1, 3, 4, 2, 2, 3, 1, 3, 1, 4, 4, 2, 4, 1]
    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Fl5273(_FunctionalArcGame):
    GAME_ID = "fl5273-6a25a72a"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
