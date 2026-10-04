# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the gc4721/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
"""Gorilla Clinic Merge (GC4721) - a click-based merge puzzle.

Players click pens to fuse equal-tier creatures into the next tier:
Nut(1) -> Hen(2) -> Tuna(3) -> Gorilla(4). Deterministic, click-only.
"""
import copy
BG_COLOR = 5
COLORS = {'frame': 1, 'nut': 11, 'hen': 12, 'tuna': 9, 'gorilla': 8, 'pad': 14, 'wall': 3, 'covered': 2, 'decoy': 13, 'hud': 10, 'face': 4}
OFF_R = 1
OFF_C = 1
CELL = 6
MAX_TIER = 4
DECOY = 7
_NEIGHBORS = [(-1, 0), (0, -1), (0, 1), (1, 0)]
LEVELS = {0: {'tiers': [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]], 'rows': 4, 'cols': 4, 'budget': 28, 'active_tags': [], 'goal_requirements': {'gorilla_count': 2}, 'design_contract': {'success_trigger': 'two Gorillas (tier 4) have been assembled on the board', 'state_key': 'gorilla_count', 'primary_blocker': 'no tier-4 tile exists; tiers only rise by fusing equal neighbors, and two separate chains must each be completed', 'dependencies': ['fuse Nut pairs into Hens', 'fuse Hens into Tunas', 'complete one Gorilla, then build a second full chain into another Gorilla'], 'feedback': "the clicked pen's creature shape/color upgrades one tier and the consumed neighbor empties", 'bypass_guard': 'the start board has only tier-1 nuts, so two tier-4 pens cannot exist until both merge chains are built'}}, 1: {'tiers': [[1, 1, -1, 1, 1], [1, 1, -1, 1, 1], [1, 1, -1, 1, 1], [1, 1, -1, 1, 1]], 'rows': 4, 'cols': 5, 'pad': (1, 0), 'budget': 28, 'active_tags': ['walls'], 'goal_requirements': {'gorilla_count': 2, 'pad_tier': 4}, 'design_contract': {'success_trigger': 'two Gorillas exist and the clinic pad cell holds a Gorilla (tier 4)', 'state_keys': ['gorilla_count', 'pad_tier'], 'primary_blocker': 'the wall column isolates the halves, so each Gorilla needs its own full chain, and one must finish on the pad cell', 'dependencies': ['build the left chain so its Gorilla lands on the pad cell', 'build the right chain into a second Gorilla'], 'feedback': 'the clicked pen upgrades one tier; the green pad shows the discharged Gorilla when complete', 'bypass_guard': 'only tier-1 nuts exist at start; two Gorillas with one on the pad cannot occur until both wall-separated chains finish correctly'}}, 2: {'tiers': [[3, 1, 1, 3, 1], [1, 2, 1, 2, 1], [1, 1, 1, 1, 1], [3, 1, 1, 3, 1], [1, 1, 1, 1, 1]], 'rows': 5, 'cols': 5, 'budget': 30, 'active_tags': ['mixed_tiers'], 'goal_requirements': {'gorilla_count': 3}, 'design_contract': {'success_trigger': 'three Gorillas (tier 4) have been assembled on the board', 'state_key': 'gorilla_count', 'primary_blocker': 'pre-placed Tunas and Hens must be combined with the right nut-grown tiers; a wrong survivor choice strands a high tier with no equal partner', 'dependencies': ['grow nuts into hens/tunas adjacent to the pre-placed high tiers', 'fuse matching tiers into three separate Gorillas'], 'feedback': 'the clicked pen upgrades one tier and the consumed neighbor empties', 'bypass_guard': 'no tier-4 pen exists at start; three Gorillas require completing three full merge chains using the mixed tiers'}}, 3: {'tiers': [[3, 3, 1, 3, 3], [1, 1, 1, 1, 1], [2, 1, 3, 1, 2], [1, 1, 1, 1, 1], [3, 3, 1, 3, 3]], 'rows': 5, 'cols': 5, 'budget': 25, 'active_tags': ['mixed_tiers', 'timer'], 'goal_requirements': {'gorilla_count': 5}, 'design_contract': {'success_trigger': 'five Gorillas (tier 4) have been assembled before the move timer runs out', 'state_key': 'gorilla_count', 'primary_blocker': 'the move budget barely covers the optimal merge plan; wasted or wrong clicks make five Gorillas impossible in time', 'dependencies': ["merge each quadrant's Tunas/Hens/Nuts into a Gorilla efficiently", 'reuse leftover tiles for the fifth Gorilla without wasting clicks', 'avoid no-op clicks so the timer is not exhausted'], 'feedback': 'the HUD budget bar shrinks each click; the clicked pen upgrades a tier', 'bypass_guard': 'five Gorillas cannot exist without five completed chains, and the timer caps total clicks below any brute-force approach'}}, 4: {'tiers': [[1, 1, 7, 1, 1], [1, 1, 7, 1, 1], [1, 1, 7, 1, 1], [1, 1, 7, 1, 1], [3, 3, 7, 3, 3]], 'rows': 5, 'cols': 5, 'budget': 29, 'active_tags': ['mixed_tiers', 'timer', 'decoys'], 'goal_requirements': {'gorilla_count': 4}, 'design_contract': {'success_trigger': 'four Gorillas (tier 4) have been assembled before the move timer runs out', 'state_key': 'gorilla_count', 'primary_blocker': 'decoy specimens block adjacency and waste clicks if touched; chains must route around them within the timer', 'dependencies': ['grow each Nut column into a Gorilla without clicking decoys', 'fuse the bottom Tuna pairs into the last two Gorillas', 'avoid no-op decoy clicks so the timer is not exhausted'], 'feedback': 'decoys render as maroon X tiles; the clicked pen upgrades a tier; HUD bar shrinks', 'bypass_guard': 'four Gorillas require four completed chains; decoys cannot merge so they can never become a Gorilla'}}, 5: {'tiers': [[1, 1, 7, 1, 1], [1, 1, 7, 1, 1], [1, 1, 7, 1, 1], [1, 1, 7, 1, 1], [3, 3, 7, 3, 3]], 'covered': [(1, 0), (3, 0), (1, 3), (3, 3)], 'rows': 5, 'cols': 5, 'budget': 34, 'active_tags': ['mixed_tiers', 'decoys', 'hidden'], 'goal_requirements': {'gorilla_count': 4}, 'design_contract': {'success_trigger': 'four Gorillas (tier 4) have been assembled', 'state_key': 'gorilla_count', 'primary_blocker': 'covered pens hide a tier and cannot merge or be merged through until a click reveals them; they must be uncovered in the right order', 'dependencies': ['reveal the covered pens inside each Nut column', 'grow each column into a Gorilla once its lids are open', 'fuse the bottom Tuna pairs into the last two Gorillas'], 'feedback': 'covered pens render as gray lids; revealing one shows the hidden creature; HUD bar shrinks', 'bypass_guard': 'a covered pen cannot merge, so four Gorillas are impossible until the hidden pens are revealed and chained'}}, 6: {'tiers': [[1, 1, 7, 1, 1], [1, 1, 7, 1, 1], [1, 1, 7, 1, 1], [1, 1, 7, 1, 1], [3, 3, 7, 3, 3]], 'covered': [(1, 0), (3, 0), (1, 3), (3, 3), (4, 4)], 'pad': (1, 0), 'rows': 5, 'cols': 5, 'budget': 34, 'active_tags': ['mixed_tiers', 'decoys', 'hidden', 'timer'], 'goal_requirements': {'gorilla_count': 4, 'pad_tier': 4}, 'design_contract': {'success_trigger': 'four Gorillas exist and the clinic pad holds a Gorilla, all before the timer runs out', 'state_keys': ['gorilla_count', 'pad_tier'], 'primary_blocker': 'hidden lids must be revealed in order and a Gorilla must land on the pad, all within a tight move budget', 'dependencies': ['reveal the lids inside each Nut column', 'grow the left column so its Gorilla lands on the pad cell', 'grow the right column and fuse the bottom Tuna pairs', 'reveal the stray lid blocking a Tuna pair before fusing it'], 'feedback': 'lids show as gray; the green pad shows the discharged Gorilla; HUD bar shrinks each click', 'bypass_guard': 'covered pens cannot merge and the timer caps clicks, so the pad Gorilla plus four total cannot occur without the correct reveal-and-merge order'}}}

LEVELS[7] = {
    "tiers": [
        [1, 1, -1, 3, 3],
        [1, 1, -1, 7, 3],
        [1, 1, -1, 3, 3],
        [1, 1, 7, 3, 3],
        [3, 3, 3, 7, 3],
    ],
    "covered": [(1, 0), (3, 0), (0, 3), (2, 3), (3, 3), (4, 0)],
    "pad": (1, 0),
    "rows": 5,
    "cols": 5,
    "budget": 28,
    "active_tags": ["mixed_tiers", "walls", "decoys", "hidden", "timer"],
    "goal_requirements": {"gorilla_count": 5, "pad_tier": 4},
    "design_contract": {
        "success_trigger": "five Gorillas exist and the clinic pad holds a Gorilla, all before the timer runs out",
        "state_keys": ["gorilla_count", "pad_tier"],
        "primary_blocker": "walls split the board, decoys and hidden lids waste clicks if mishandled, and the pad Gorilla plus four others must all finish within the timer",
        "dependencies": [
            "reveal the left Nut-column lids and build the pad Gorilla",
            "reveal the right Tuna lids in order and fuse three Tuna-pair Gorillas",
            "reveal the bottom lid and fuse the final Tuna pair",
        ],
        "feedback": "walls render as solid blocks, decoys as maroon X, lids as gray; the pad shows the discharged Gorilla; HUD bar shrinks",
        "bypass_guard": "covered pens and decoys cannot merge and the wall blocks adjacency, so five Gorillas with one on the pad require the exact reveal-and-merge plan within the timer",
    },
}


def _cell_to_pixel_center(r, c):
    """Return (x, y) pixel center of logical cell (r, c)."""
    y = OFF_R + r * CELL + CELL // 2
    x = OFF_C + c * CELL + CELL // 2
    return (x, y)

def _pixel_to_cell(x, y, rows, cols):
    """Map a click pixel (x, y) to a logical cell, or None if outside board."""
    if x < OFF_C or y < OFF_R:
        return None
    c = (x - OFF_C) // CELL
    r = (y - OFF_R) // CELL
    if 0 <= r < rows and 0 <= c < cols:
        return (int(r), int(c))
    return None

def get_available_actions():
    return [6]

def get_initial_state(level):
    cfg = LEVELS[level]
    tiers = copy.deepcopy(cfg['tiers'])
    pad = cfg.get('pad')
    h_t = {'level': level, 'step': 0, 'budget': cfg['budget'], 'tiers': tiers, 'max_tier': max((max(row) for row in tiers)), 'pad_tier': tiers[pad[0]][pad[1]] if pad else 0, 'gorilla_count': sum((1 for row in tiers for v in row if v == MAX_TIER)), 'covered': [list(rc) for rc in cfg.get('covered', [])], 'undo': []}
    z_t = {}
    return (h_t, z_t)

def predict(h_t, seed):
    return {}

def transition(h_t, z_t, a_t):
    h = copy.deepcopy(h_t)
    cfg = LEVELS[h['level']]
    rows, cols = (cfg['rows'], cfg['cols'])
    if not (isinstance(a_t, (tuple, list)) and len(a_t) == 3 and (a_t[0] == 6)):
        return h
    _, x, y = a_t
    cell = _pixel_to_cell(x, y, rows, cols)
    h['step'] += 1
    if cell is None:
        return h
    r, c = cell
    tiers = h['tiers']
    covered = h.get('covered', [])
    if [r, c] in covered:
        covered.remove([r, c])
        return h
    t = tiers[r][c]
    if t == DECOY or t == -1:
        return h
    if t < 1 or t >= MAX_TIER:
        return h
    for dr, dc in _NEIGHBORS:
        nr, nc = (r + dr, c + dc)
        if 0 <= nr < rows and 0 <= nc < cols and ([nr, nc] not in covered) and (tiers[nr][nc] == t):
            if len(h['undo']) < 50:
                h['undo'].append(copy.deepcopy(tiers))
            tiers[r][c] = t + 1
            tiers[nr][nc] = 0
            if t + 1 > h['max_tier']:
                h['max_tier'] = t + 1
            break
    pad = cfg.get('pad')
    if pad:
        h['pad_tier'] = tiers[pad[0]][pad[1]]
    h['gorilla_count'] = sum((1 for row in tiers for v in row if v == MAX_TIER))
    return h

def check_level_complete(h_t, z_t, level):
    cfg = LEVELS[level]
    req = cfg.get('goal_requirements', {})
    if 'timer' in cfg.get('active_tags', []):
        if h_t.get('step', 0) > cfg.get('budget', 10 ** 9):
            return False
    if 'gorilla_count' in req and h_t.get('gorilla_count', 0) < req['gorilla_count']:
        return False
    if 'pad_tier' in req and h_t.get('pad_tier', 0) < req['pad_tier']:
        return False
    if 'max_tier' in req and h_t.get('max_tier', 0) < req['max_tier']:
        return False
    if not req:
        return h_t.get('max_tier', 0) >= MAX_TIER
    return True

def _draw_entity(grid, ir, ic, tier):
    """Draw a tier creature in the inner 4x4 block at top-left (ir, ic)."""
    if tier == DECOY:
        for k in range(4):
            grid[ir + k][ic + k] = COLORS['decoy']
            grid[ir + k][ic + 3 - k] = COLORS['decoy']
        return
    if tier == 1:
        for rr in range(ir + 1, ir + 3):
            for cc in range(ic + 1, ic + 3):
                grid[rr][cc] = COLORS['nut']
    elif tier == 2:
        for cc in range(ic, ic + 4):
            grid[ir][cc] = COLORS['hen']
            grid[ir + 1][cc] = COLORS['hen']
            grid[ir + 2][cc] = COLORS['nut']
            grid[ir + 3][cc] = COLORS['nut']
    elif tier == 3:
        for cc in range(ic, ic + 4):
            grid[ir + 1][cc] = COLORS['tuna']
            grid[ir + 2][cc] = COLORS['tuna']
        grid[ir][ic + 3] = COLORS['tuna']
        grid[ir + 3][ic + 3] = COLORS['tuna']
    elif tier >= 4:
        for rr in range(ir, ir + 4):
            for cc in range(ic, ic + 4):
                grid[rr][cc] = COLORS['gorilla']
        grid[ir + 1][ic + 1] = COLORS['face']
        grid[ir + 1][ic + 2] = COLORS['face']
        grid[ir + 2][ic + 1] = COLORS['face']
        grid[ir + 2][ic + 2] = COLORS['face']

def render(h_t, z_t):
    grid = [[BG_COLOR for _ in range(32)] for _ in range(32)]
    cfg = LEVELS[h_t['level']]
    rows, cols = (cfg['rows'], cfg['cols'])
    tiers = h_t['tiers']
    covered = h_t.get('covered', [])
    for r in range(rows):
        for c in range(cols):
            top = OFF_R + r * CELL
            left = OFF_C + c * CELL
            t = tiers[r][c]
            if t == -1:
                for rr in range(CELL):
                    for cc in range(CELL):
                        grid[top + rr][left + cc] = COLORS['wall']
                continue
            pad = cfg.get('pad')
            frame_col = COLORS['pad'] if pad and (r, c) == tuple(pad) else COLORS['frame']
            for k in range(CELL):
                grid[top][left + k] = frame_col
                grid[top + CELL - 1][left + k] = frame_col
                grid[top + k][left] = frame_col
                grid[top + k][left + CELL - 1] = frame_col
            if [r, c] in covered:
                for rr in range(top + 1, top + CELL - 1):
                    for cc in range(left + 1, left + CELL - 1):
                        grid[rr][cc] = COLORS['covered']
                grid[top + CELL // 2][left + CELL // 2] = COLORS['face']
                continue
            if t > 0:
                _draw_entity(grid, top + 1, left + 1, t)
    remaining = max(0, cfg['budget'] - h_t['step'])
    fill = min(32, int(round(32 * remaining / max(1, cfg['budget']))))
    for x in range(fill):
        grid[31][x] = COLORS['hud']
    return grid

def solve_level(level):
    if level == 0:
        seq_cells = [(0, 0), (1, 0), (1, 0), (2, 0), (3, 0), (2, 0), (1, 0), (0, 2), (1, 2), (1, 2), (2, 2), (3, 2), (2, 2), (1, 2)]
        actions = []
        for r, c in seq_cells:
            x, y = _cell_to_pixel_center(r, c)
            actions.append((6, x, y))
        return actions
    if level == 1:
        seq_cells = [(0, 0), (0, 3), (1, 0), (1, 0), (1, 3), (1, 3), (2, 0), (2, 3), (3, 0), (2, 0), (1, 0), (3, 3), (2, 3), (1, 3)]
        actions = []
        for r, c in seq_cells:
            x, y = _cell_to_pixel_center(r, c)
            actions.append((6, x, y))
        return actions
    if level == 2:
        seq_cells = [(0, 1), (0, 1), (0, 0), (0, 4), (1, 0), (1, 2), (1, 2), (2, 3), (3, 1), (4, 1), (3, 1), (3, 0), (4, 2), (4, 3), (4, 3), (3, 3)]
        actions = []
        for r, c in seq_cells:
            x, y = _cell_to_pixel_center(r, c)
            actions.append((6, x, y))
        return actions
    if level == 3:
        seq_cells = [(0, 0), (0, 2), (0, 3), (1, 0), (1, 0), (1, 3), (2, 1), (2, 3), (2, 3), (2, 2), (3, 2), (4, 0), (4, 3)]
        actions = []
        for r, c in seq_cells:
            x, y = _cell_to_pixel_center(r, c)
            actions.append((6, x, y))
        return actions
    if level == 4:
        seq_cells = [(0, 0), (1, 0), (1, 0), (2, 0), (3, 0), (2, 0), (1, 0), (0, 3), (1, 3), (1, 3), (2, 3), (3, 3), (2, 3), (1, 3), (4, 0), (4, 3)]
        actions = []
        for r, c in seq_cells:
            x, y = _cell_to_pixel_center(r, c)
            actions.append((6, x, y))
        return actions
    if level == 5:
        seq_cells = [(1, 0), (3, 0), (0, 0), (1, 0), (1, 0), (2, 0), (3, 0), (2, 0), (1, 0), (1, 3), (3, 3), (0, 3), (1, 3), (1, 3), (2, 3), (3, 3), (2, 3), (1, 3), (4, 0), (4, 3)]
        actions = []
        for r, c in seq_cells:
            x, y = _cell_to_pixel_center(r, c)
            actions.append((6, x, y))
        return actions
    if level == 6:
        seq_cells = [(1, 0), (3, 0), (0, 0), (1, 0), (1, 0), (2, 0), (3, 0), (2, 0), (1, 0), (1, 3), (3, 3), (0, 3), (1, 3), (1, 3), (2, 3), (3, 3), (2, 3), (1, 3), (4, 4), (4, 0), (4, 3)]
        actions = []
        for r, c in seq_cells:
            x, y = _cell_to_pixel_center(r, c)
            actions.append((6, x, y))
        return actions
    if level == 7:
        seq_cells = [
            (1, 0), (3, 0),                                          # reveal left lids
            (0, 0), (1, 0), (1, 0), (2, 0), (3, 0), (2, 0), (1, 0),  # left gorilla -> pad
            (0, 3), (2, 3), (3, 3),                                  # reveal right lids
            (0, 3), (2, 3), (3, 3),                                  # three tuna-pair gorillas
            (4, 0),                                                  # reveal bottom lid
            (4, 1),                                                  # final tuna pair -> gorilla
        ]
        actions = []
        for (r, c) in seq_cells:
            x, y = _cell_to_pixel_center(r, c)
            actions.append((6, x, y))
        return actions
    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Gc4721(_FunctionalArcGame):
    GAME_ID = "gc4721-78997285"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
