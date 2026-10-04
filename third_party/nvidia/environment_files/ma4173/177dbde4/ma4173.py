# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the ma4173/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
"""Magnet Audit (MA4173) - ARC-AGI-3 falling/packing game.

Level 0 only. Fully deterministic. Mixed input:
  - LEFT/RIGHT steer the active crate's aim column (free, no budget cost).
  - DOWN / USE drop the aimed crate into its column (consumes a crate).
  - CLICK fires a magnetic pull: snap to the clicked column and drop.
Goal: pack falling crates so every glowing target slot is covered (an audit
that must match exactly).
"""
import copy
BG_COLOR = 4
COLORS = {'bg': 4, 'active': 8, 'core': 0, 'settled': 12, 'target': 11, 'auditor': 13, 'hud': 12}
CELL = 3
ROWS = 5
COLS = 5
LEVELS = {0: {'rows': 5, 'cols': 5, 'spawn_col': 2, 'num_crates': 4, 'targets': [[4, 0], [4, 1], [4, 3], [4, 4]], 'budget': 36, 'active_tags': [], 'goal_requirements': {'covered': 4}, 'design_contract': {'success_trigger': 'board_matches_target', 'state_key': 'audit_complete', 'state_keys': ['audit_complete'], 'primary_blocker': 'four target slots sit in four distinct columns and only four crates exist; each must be routed to a different column', 'dependencies': ['route a crate to column 0', 'route a crate to column 1', 'route a crate to column 3', 'route a crate to column 4'], 'feedback': 'a covered target turns from a yellow ring into a solid orange crate with a yellow center dot; HUD budget shrinks', 'bypass_guard': 'audit_complete only becomes true when all four target cells are covered, so dropping a crate in the wrong column leaves a target uncovered and blocks completion'}}, 1: {'rows': 5, 'cols': 5, 'spawn_col': 2, 'num_crates': 6, 'targets': [[4, 0], [4, 1], [4, 3], [4, 4], [3, 2]], 'budget': 36, 'active_tags': ['stack'], 'goal_requirements': {'covered': 5}, 'design_contract': {'success_trigger': 'board_matches_target', 'state_key': 'audit_complete', 'state_keys': ['audit_complete'], 'primary_blocker': 'the [3,2] target floats one row above the floor; a crate falls to the lowest free cell so a filler crate must occupy [4,2] first before another crate can stack onto the floating target', 'dependencies': ['cover [4,0]', 'cover [4,4]', 'drop a filler crate into [4,2] (non-target)', 'stack a crate onto the floating target [3,2]'], 'feedback': 'the floating yellow ring at [3,2] becomes a solid orange crate only after a filler crate sits below it; HUD shrinks', 'bypass_guard': 'with exactly 4 crates and a wasted filler needed under [3,2], a crate spent in the wrong column leaves a target uncovered and makes audit_complete unreachable'}}, 2: {'rows': 5, 'cols': 5, 'spawn_col': 2, 'num_crates': 7, 'targets': [[4, 0], [3, 0], [4, 1], [4, 4], [2, 2]], 'budget': 34, 'active_tags': ['stack'], 'goal_requirements': {'covered': 5}, 'design_contract': {'success_trigger': 'board_matches_target', 'state_key': 'audit_complete', 'state_keys': ['audit_complete'], 'primary_blocker': 'the [2,2] target floats two rows above the floor, so two filler crates must be stacked in column 2 before a third crate lands on the target; column 0 also requires two stacked crates in the correct vertical order', 'dependencies': ['cover [4,0] then stack [3,0] above it', 'cover [4,1]', 'cover [4,4]', 'drop two fillers into [4,2] and [3,2]', 'land the final crate onto floating target [2,2]'], 'feedback': 'each covered ring turns into a solid orange crate; the two-high stacks visibly build upward; HUD shrinks', 'bypass_guard': 'with exactly 7 crates and two fillers spent under [2,2], any crate dropped in a wrong column leaves a target uncovered and makes audit_complete unreachable'}}, 3: {'rows': 5, 'cols': 5, 'spawn_col': 2, 'num_crates': 6, 'targets': [[4, 0], [3, 0], [4, 2], [4, 4], [3, 4]], 'budget': 30, 'active_tags': ['stack', 'cascade'], 'goal_requirements': {'covered': 5}, 'design_contract': {'success_trigger': 'board_matches_target', 'state_key': 'audit_complete', 'state_keys': ['audit_complete'], 'primary_blocker': 'two-high stacks must be built at columns 0 and 4 while columns 1 and 3 stay empty; if both gap columns are ever filled, row 4 becomes complete and a cascade clears the whole row, destroying every covered target', 'dependencies': ['stack [4,0] then [3,0]', 'cover [4,2]', 'stack [4,4] then [3,4]', 'never fill both gap columns 1 and 3 on the floor row'], 'feedback': 'covered rings turn solid orange and the stacks build upward; completing the floor row visibly clears it (cascade) as a failure', 'bypass_guard': 'audit_complete requires all five targets covered, but completing the floor row cascades them away, so a careless drop in the gap columns makes completion unreachable'}}, 4: {'rows': 5, 'cols': 5, 'spawn_col': 2, 'num_crates': 7, 'targets': [[4, 0], [3, 0], [4, 2], [3, 2], [2, 2], [4, 4], [3, 4]], 'budget': 30, 'active_tags': ['stack', 'cascade'], 'goal_requirements': {'covered': 7}, 'design_contract': {'success_trigger': 'board_matches_target', 'state_key': 'audit_complete', 'state_keys': ['audit_complete'], 'primary_blocker': 'a three-high tower must be built at column 2 and two-high towers at columns 0 and 4, all while gap columns 1 and 3 stay empty so the floor row never completes and cascades away the towers', 'dependencies': ['stack [4,0] then [3,0]', 'stack [4,2], [3,2], then [2,2]', 'stack [4,4] then [3,4]', 'never fill both gap columns 1 and 3 on the floor row'], 'feedback': 'covered rings turn solid orange and three towers build upward at different heights; completing the floor row clears it (cascade) as a failure', 'bypass_guard': 'audit_complete requires all seven targets covered, but completing the floor row cascades them away, so any drop in the gap columns makes completion unreachable'}}, 5: {'rows': 5, 'cols': 5, 'spawn_col': 2, 'num_crates': 8, 'targets': [[4, 0], [3, 0], [4, 2], [4, 4], [3, 4]], 'budget': 26, 'active_tags': ['stack', 'patrol'], 'goal_requirements': {'covered': 5}, 'design_contract': {'success_trigger': 'board_matches_target', 'state_key': 'audit_complete', 'state_keys': ['audit_complete'], 'primary_blocker': 'a maroon auditor patrols the floor row in a fixed back-and-forth route advancing one cell per crate dropped; a crate dropped onto the floor cell the auditor currently occupies is rejected and wasted, so floor targets [4,0],[4,2],[4,4] must be filled in an order that never coincides with the patrol', 'dependencies': ['drop floor targets when the auditor is elsewhere', 'cover [4,0],[4,2],[4,4] in a patrol-safe order', 'stack [3,0] and [3,4] above their floor crates'], 'feedback': 'the maroon cross moves one floor cell per drop; a rejected crate leaves its target still a yellow ring; covered targets turn solid orange', 'bypass_guard': 'audit_complete requires every target covered, but a crate dropped on the auditor is wasted, so an ill-timed floor drop leaves a target uncovered and consumes a crate'}}, 6: {'rows': 5, 'cols': 5, 'spawn_col': 2, 'num_crates': 8, 'targets': [[4, 0], [3, 0], [4, 2], [3, 2], [2, 2], [4, 4], [3, 4]], 'budget': 24, 'active_tags': ['stack', 'patrol', 'cascade'], 'goal_requirements': {'covered': 7}, 'design_contract': {'success_trigger': 'board_matches_target', 'state_key': 'audit_complete', 'state_keys': ['audit_complete'], 'primary_blocker': 'the floor auditor patrols while a cascade lurks: floor targets must be dropped when the auditor is elsewhere, AND gap columns 1 and 3 must stay empty so the floor row never completes and cascades away the two towers', 'dependencies': ['drop floor targets [4,0],[4,2],[4,4] in a patrol-safe order', 'stack [3,0] and [3,4] above their floor crates', 'never fill both gap columns 1 and 3'], 'feedback': 'the maroon cross steps across the floor; covered rings turn solid orange; completing the floor row clears it (cascade) as a failure', 'bypass_guard': 'audit_complete requires all five targets covered; a wasted patrol drop or a cascade-triggering gap drop leaves a target uncovered and makes completion unreachable'}}, 7: {'rows': 5, 'cols': 5, 'spawn_col': 2, 'num_crates': 8, 'targets': [[4, 0], [3, 0], [2, 0], [4, 2], [4, 4], [3, 4], [2, 4]], 'budget': 26, 'active_tags': ['stack', 'patrol', 'cascade'], 'goal_requirements': {'covered': 7}, 'design_contract': {'success_trigger': 'board_matches_target', 'state_key': 'audit_complete', 'state_keys': ['audit_complete'], 'primary_blocker': 'final audit: two three-high towers at columns 0 and 4 plus a single floor target at column 2 must all be filled with only one spare crate, while the floor auditor patrols (floor drops must dodge it) and the cascade lurks (gap columns 1 and 3 must stay empty so the floor row never clears)', 'dependencies': ['drop the three floor targets [4,0],[4,2],[4,4] in a patrol-safe order', 'stack [3,0],[2,0] above column 0 and [3,4],[2,4] above column 4', 'never fill both gap columns 1 and 3'], 'feedback': 'two tall towers rise while the maroon auditor steps across the floor; each covered ring turns solid orange; completing the floor row clears it (cascade) as failure', 'bypass_guard': 'with only one spare crate, any wasted patrol drop, cascade-triggering gap drop, or wrong column leaves a target uncovered and makes audit_complete unreachable'}}}

def _lowest_free_row(settled, col, rows):
    """Lowest empty row in a column (crate falls to it). None if column full."""
    occ = {r for r, c in settled if c == col}
    for r in range(rows - 1, -1, -1):
        if r not in occ:
            return r
    return None

def _count_covered(settled, targets):
    s = [list(x) for x in settled]
    return sum((1 for t in targets if list(t) in s))

def _patrol_col(k, cols):
    """Deterministic triangle-wave patrol position over crate-drop count k."""
    period = 2 * (cols - 1)
    phase = k % period
    return phase if phase <= cols - 1 else period - phase

def _drop(h, col):
    """Drop the active crate into a column; advance to the next crate."""
    lvl = LEVELS[h['level']]
    if h['crate_idx'] >= lvl['num_crates'] or h['budget'] <= 0:
        return
    tags = lvl.get('active_tags', [])
    r = _lowest_free_row(h['settled'], col, lvl['rows'])
    if r is not None:
        rejected = False
        if 'patrol' in tags:
            if r == lvl['rows'] - 1 and col == _patrol_col(h['crate_idx'], lvl['cols']):
                rejected = True
        if not rejected:
            h['settled'].append([r, col])
            h['settled'].sort()
            if 'cascade' in tags:
                _apply_cascade(h, lvl)
    h['crate_idx'] += 1
    h['budget'] -= 1
    h['aim_col'] = lvl['spawn_col']
    h['covered'] = _count_covered(h['settled'], lvl['targets'])
    h['audit_complete'] = h['covered'] >= lvl['goal_requirements']['covered'] and all((list(t) in [list(s) for s in h['settled']] for t in lvl['targets']))

def _apply_cascade(h, lvl):
    """Clear any fully filled row; shift crates above it down. Chains."""
    cols = lvl['cols']
    rows = lvl['rows']
    changed = True
    while changed:
        changed = False
        occ = {(s[0], s[1]) for s in h['settled']}
        for r in range(rows):
            if all(((r, c) in occ for c in range(cols))):
                kept = []
                for s in h['settled']:
                    if s[0] == r:
                        continue
                    if s[0] < r:
                        kept.append([s[0] + 1, s[1]])
                    else:
                        kept.append([s[0], s[1]])
                h['settled'] = sorted(kept)
                changed = True
                break

def get_initial_state(level):
    lvl = LEVELS[level]
    h_t = {'level': level, 'budget': lvl['budget'], 'aim_col': lvl['spawn_col'], 'settled': [], 'crate_idx': 0, 'covered': 0, 'audit_complete': False}
    return (h_t, {})

def get_available_actions():
    return [0, 2, 3, 4, 5, 6, 7]

def predict(h_t, seed):
    return {}

def transition(h_t, z_t, a_t):
    h = copy.deepcopy(h_t)
    level = h['level']
    lvl = LEVELS[level]
    cols = lvl['cols']
    if isinstance(a_t, (tuple, list)):
        act = a_t[0]
        cx = a_t[1] if len(a_t) > 1 else 0
    else:
        act = a_t
        cx = 0
    if act == 0:
        nh, _ = get_initial_state(level)
        return nh
    if act == 7:
        return h
    if h['crate_idx'] >= lvl['num_crates']:
        return h
    if act == 3:
        h['aim_col'] = max(0, h['aim_col'] - 1)
    elif act == 4:
        h['aim_col'] = min(cols - 1, h['aim_col'] + 1)
    elif act in (2, 5):
        _drop(h, h['aim_col'])
    elif act == 6:
        col = max(0, min(cols - 1, cx // CELL))
        h['aim_col'] = col
        _drop(h, col)
    return h

def check_level_complete(h_t, z_t, level):
    lvl = LEVELS[level]
    settled = [list(s) for s in h_t['settled']]
    targets_ok = all((list(t) in settled for t in lvl['targets']))
    req = lvl.get('goal_requirements', {})
    covered_ok = h_t.get('covered', 0) >= req.get('covered', len(lvl['targets']))
    return targets_ok and covered_ok

def _fill_cell(grid, br, bc, color):
    for dr in range(CELL):
        for dc in range(CELL):
            grid[br * CELL + dr][bc * CELL + dc] = color

def _ring_cell(grid, br, bc, color):
    for dr in range(CELL):
        for dc in range(CELL):
            if dr in (0, CELL - 1) or dc in (0, CELL - 1):
                grid[br * CELL + dr][bc * CELL + dc] = color

def _draw_entity(grid, br, bc, entity_type, on_target=False):
    if entity_type == 'target':
        _ring_cell(grid, br, bc, COLORS['target'])
    elif entity_type == 'settled':
        _fill_cell(grid, br, bc, COLORS['settled'])
        if on_target:
            grid[br * CELL + 1][bc * CELL + 1] = COLORS['target']
    elif entity_type == 'active':
        _fill_cell(grid, br, bc, COLORS['active'])
        grid[br * CELL + 1][bc * CELL + 1] = COLORS['core']
    elif entity_type == 'auditor':
        cr, cc = (br * CELL + 1, bc * CELL + 1)
        grid[cr][cc] = COLORS['auditor']
        grid[cr - 1][cc] = COLORS['auditor']
        grid[cr + 1][cc] = COLORS['auditor']
        grid[cr][cc - 1] = COLORS['auditor']
        grid[cr][cc + 1] = COLORS['auditor']

def render(h_t, z_t):
    grid = [[BG_COLOR for _ in range(16)] for _ in range(16)]
    level = h_t['level']
    lvl = LEVELS[level]
    targets = [list(t) for t in lvl['targets']]
    settled = [list(s) for s in h_t['settled']]
    for t in targets:
        if t not in settled:
            _draw_entity(grid, t[0], t[1], 'target')
    for s in settled:
        _draw_entity(grid, s[0], s[1], 'settled', on_target=s in targets)
    if h_t['crate_idx'] < lvl['num_crates']:
        _draw_entity(grid, 0, h_t['aim_col'], 'active')
    if 'patrol' in lvl.get('active_tags', []) and h_t['crate_idx'] < lvl['num_crates']:
        pc = _patrol_col(h_t['crate_idx'], lvl['cols'])
        floor = lvl['rows'] - 1
        if [floor, pc] not in settled:
            _draw_entity(grid, floor, pc, 'auditor')
    filled = max(0, min(15, h_t['budget']))
    for cc in range(filled):
        grid[15][cc] = COLORS['hud']
    return grid

def solve_level(level):
    if level == 0:
        return [3, 3, 5, (6, 12, 13), 3, 5, 4, 5]
    if level == 1:
        return [3, 3, 5, 3, 5, 4, 5, (6, 12, 13), 5, 5]
    if level == 2:
        return [3, 3, 5, 3, 3, 5, 3, 5, (6, 12, 13), 5, 5, 5]
    if level == 3:
        return [3, 3, 5, 3, 3, 5, 5, 4, 4, 5, 4, 4, 5]
    if level == 4:
        return [3, 3, 5, 3, 3, 5, 4, 4, 5, 4, 4, 5, 5, 5, 5]
    if level == 5:
        return [4, 4, 5, 3, 3, 5, 4, 4, 5, 3, 3, 5, 5]
    if level == 6:
        return [4, 4, 5, 3, 3, 5, 4, 4, 5, 5, 3, 3, 5, 5, 5]
    if level == 7:
        return [5, 4, 4, 5, 4, 4, 5, 4, 4, 5, 3, 3, 5, 3, 3, 5, 3, 3, 5]
    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Ma4173(_FunctionalArcGame):
    GAME_ID = "ma4173-177dbde4"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
