# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the sf2048/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy
BG_COLOR = 5
CELL = 4
ORIGIN_R = 10
ORIGIN_C = 8
BOARD_H = 12
BOARD_W = 12
COLORS = {'floor': 3, 'wall': 2, 'wall_edge': 4, 'frost': 10, 'frost_core': 9, 'ember': 8, 'warm': 12, 'heat_core': 11, 'target': 14, 'target_core': 0, 'hud': 11, 'hud_used': 13, 'fog': 4, 'ice': 9, 'crack': 7, 'nest': 15, 'nest_core': 6, 'amp': 11, 'amp_core': 8}
LEVELS = {0: {'layout': ['############', '#...#...T..#', '#.#.#.#.##.#', '#.#...#....#', '#F###.###F.#', '#..F...F...#', '###.#.#.####', '#...#.#....#', '#.##F###.#.#', '#T...F...#.#', '#....#.....#', '############'], 'targets': [(1, 8), (9, 1)], 'initial_frost': [(4, 1), (4, 9), (5, 3), (5, 7), (8, 4), (9, 5)], 'budget': 22, 'active_tags': ['spread'], 'fog_radius': None, 'goal_requirements': {'all_targets_warm': True, 'frost_cleared': True}, 'design_contract': {'success_trigger': 'board_matches_target', 'state_keys': ['all_targets_warm', 'frost_cleared'], 'primary_blocker': 'six frost cells occupy separate branches and will spread into useful corridors if ignored', 'dependencies': ['clear central frost', 'warm upper scale branch', 'warm lower scale branch', 'extinguish all remaining frost'], 'feedback': 'frost tiles turn orange/yellow when heated and target rings fill with yellow centers', 'bypass_guard': 'completion requires visible warm target cells and zero visible frost cells, not a hidden click counter'}}, 1: {'layout': ['############', '#T..F..B...#', '#.##.##.##.#', '#....#.....#', '###F.#.F####', '#....#.....#', '#.####B###.#', '#.....F....#', '#F###.###F.#', '#...#.....T#', '#..B....F..#', '############'], 'targets': [(1, 1), (9, 10)], 'initial_frost': [(1, 4), (4, 3), (4, 7), (7, 6), (8, 1), (8, 9), (10, 8)], 'initial_ice': [(1, 7), (6, 6), (10, 3)], 'budget': 24, 'active_tags': ['spread', 'ice'], 'fog_radius': None, 'goal_requirements': {'all_targets_warm': True, 'frost_cleared': True, 'ice_cleared': True}, 'design_contract': {'success_trigger': 'board_matches_target', 'state_keys': ['all_targets_warm', 'frost_cleared', 'ice_cleared'], 'primary_blocker': 'broken ice cells block heat corridors and must be cracked before the final stabilization can hold', 'dependencies': ['crack upper ice', 'clear frost pockets', 'crack central ice bridge', 'crack lower ice', 'warm both scale targets'], 'feedback': 'blue cracked blocks disappear into orange warmth, frost clears, and the two target rings fill yellow', 'bypass_guard': 'completion requires every visible ice block gone, all frost gone, and both visible targets warmed'}}, 2: {'layout': ['############', '#..T..F....#', '#.##.##B##.#', '#....N.....#', '###F.#.F##.#', '#....#.....#', '#.B###.###T#', '#.....N....#', '#F###.###F.#', '#...#..B...#', '#T...F....N#', '############'], 'targets': [(1, 3), (6, 10), (10, 1)], 'initial_frost': [(1, 6), (4, 3), (4, 7), (8, 1), (8, 9), (10, 5)], 'initial_ice': [(2, 7), (6, 2), (9, 7)], 'initial_nests': [(3, 5), (7, 6), (10, 10)], 'budget': 28, 'active_tags': ['spread', 'ice', 'nests'], 'fog_radius': None, 'goal_requirements': {'all_targets_warm': True, 'frost_cleared': True, 'ice_cleared': True, 'nests_cleared': True}, 'design_contract': {'success_trigger': 'board_matches_target', 'state_keys': ['all_targets_warm', 'frost_cleared', 'ice_cleared', 'nests_cleared'], 'primary_blocker': 'purple frost nests ignore nearby heat and keep reseeding cold branches until clicked directly', 'dependencies': ['crack ice gates', 'click each frost nest directly', 'clear ordinary frost', 'warm all three scale targets'], 'feedback': 'purple nest cells vanish only on direct sun clicks, then surrounding frost can be melted normally', 'bypass_guard': 'completion requires zero visible nests, zero frost, zero ice, and all three targets visibly warm'}}, 3: {'layout': ['############', '#T...F...B.#', '#.##.##.##.#', '#...N......#', '##F###F##..#', '#....#...T.#', '#.B..#..B#.#', '#....N.....#', '#F###.###F.#', '#...#..F...#', '#T...B...N.#', '############'], 'targets': [(1, 1), (5, 9), (10, 1)], 'initial_frost': [(1, 5), (4, 2), (4, 6), (8, 1), (8, 9), (9, 7)], 'initial_ice': [(1, 9), (6, 2), (6, 8), (10, 5)], 'initial_nests': [(3, 4), (7, 5), (10, 9)], 'budget': 30, 'active_tags': ['spread', 'ice', 'nests', 'fog'], 'fog_radius': 4, 'goal_requirements': {'all_targets_warm': True, 'frost_cleared': True, 'ice_cleared': True, 'nests_cleared': True}, 'design_contract': {'success_trigger': 'board_matches_target', 'state_keys': ['all_targets_warm', 'frost_cleared', 'ice_cleared', 'nests_cleared'], 'primary_blocker': 'fog hides cold side branches until warmth is seeded, while ice and nests must still be handled in separate regions', 'dependencies': ['reveal and warm the upper target area', 'clear central nest and frost pair', 'open the lower ice route', 'clear final nest before warming the lower target'], 'feedback': 'warmed cells push back the fog mask; cleared blue ice and purple nests leave orange warm cells behind', 'bypass_guard': 'all visible target lamps require target warmth plus zero remaining frost, ice, or nest cells'}}, 4: {'layout': ['############', '#T.F...B..T#', '#.##.##.##.#', '#..A.N.....#', '##F###F##B.#', '#....#.....#', '#.B..A..B#.#', '#....N.....#', '#F###.###F.#', '#..B#..F.A.#', '#T...B...N.#', '############'], 'targets': [(1, 1), (1, 10), (10, 1)], 'initial_frost': [(1, 3), (4, 2), (4, 6), (8, 1), (8, 9), (9, 7)], 'initial_ice': [(1, 7), (4, 9), (6, 2), (6, 8), (9, 3), (10, 5)], 'initial_nests': [(3, 5), (7, 5), (10, 9)], 'initial_amps': [(3, 3), (6, 5), (9, 9)], 'budget': 32, 'active_tags': ['spread', 'ice', 'nests', 'fog', 'amplifier'], 'fog_radius': 3, 'goal_requirements': {'all_targets_warm': True, 'frost_cleared': True, 'ice_cleared': True, 'nests_cleared': True, 'amps_used': True}, 'design_contract': {'success_trigger': 'board_matches_target', 'state_keys': ['all_targets_warm', 'frost_cleared', 'ice_cleared', 'nests_cleared', 'amps_used'], 'primary_blocker': 'three yellow sun-scale amplifiers must be deliberately triggered to reveal and heat branches efficiently under tighter fog', 'dependencies': ['trigger upper amplifier after clearing its nearby frost', 'open and use central amplifier bridge', 'trigger lower amplifier before final nest cleanup', 'warm all three targets'], 'feedback': 'clicked amplifiers turn into red/yellow embers and cast a longer cross-shaped heat flare through corridors', 'bypass_guard': 'completion requires every visible amplifier used plus all frost, ice, nests cleared and targets warmed'}}, 5: {'layout': ['############', '#T..F.B..NT#', '#.##.##A##.#', '#..N....F..#', '##F###B##..#', '#....#..A..#', '#.B..N..B#.#', '#....F.....#', '#F###.###F.#', '#..A#..F...#', '#T..B...N.T#', '############'], 'targets': [(1, 1), (1, 10), (10, 1), (10, 10)], 'initial_frost': [(1, 4), (3, 8), (4, 2), (7, 5), (8, 1), (8, 9), (9, 7)], 'initial_ice': [(1, 6), (4, 6), (6, 2), (6, 8), (10, 4)], 'initial_nests': [(1, 9), (3, 3), (6, 5), (10, 8)], 'initial_amps': [(2, 7), (5, 8), (9, 3)], 'budget': 36, 'active_tags': ['spread', 'ice', 'nests', 'fog', 'amplifier'], 'fog_radius': 2, 'goal_requirements': {'all_targets_warm': True, 'frost_cleared': True, 'ice_cleared': True, 'nests_cleared': True, 'amps_used': True}, 'design_contract': {'success_trigger': 'board_matches_target', 'state_keys': ['all_targets_warm', 'frost_cleared', 'ice_cleared', 'nests_cleared', 'amps_used'], 'primary_blocker': 'dense fog and four separated scale targets force the player to stabilize quadrants in an efficient order', 'dependencies': ['clear and warm the upper pair', 'use the top amplifier to reveal the right branch', 'open central ice before the middle nest', 'use the lower amplifier before the final target pair'], 'feedback': 'each quadrant becomes visible only after local warming, amplifiers turn to embers, and target rings fill yellow', 'bypass_guard': 'the board is not complete until all four targets are warm and every visible frost, ice, nest, and amplifier objective is gone'}}, 6: {'layout': ['############', '#T.FB.A.N.T#', '#.##.##.##.#', '#..N..F..B.#', '##F###B##F.#', '#..A.#..A..#', '#.B..N..B#.#', '#F...F..N..#', '#.###.###F.#', '#..A#B.F...#', '#T..N...B.T#', '############'], 'targets': [(1, 1), (1, 10), (10, 1), (10, 10)], 'initial_frost': [(1, 3), (3, 6), (4, 2), (4, 9), (7, 1), (7, 5), (8, 9), (9, 7)], 'initial_ice': [(1, 4), (3, 9), (4, 6), (6, 2), (6, 8), (9, 5), (10, 8)], 'initial_nests': [(1, 8), (3, 3), (6, 5), (7, 8), (10, 4)], 'initial_amps': [(1, 6), (5, 3), (5, 8), (9, 3)], 'budget': 42, 'active_tags': ['spread', 'ice', 'nests', 'fog', 'amplifier'], 'fog_radius': 2, 'goal_requirements': {'all_targets_warm': True, 'frost_cleared': True, 'ice_cleared': True, 'nests_cleared': True, 'amps_used': True}, 'design_contract': {'success_trigger': 'board_matches_target', 'state_keys': ['all_targets_warm', 'frost_cleared', 'ice_cleared', 'nests_cleared', 'amps_used'], 'primary_blocker': 'four-quadrant fog and interleaved nests, ice, and amplifiers create critical ordering pressure across the whole field', 'dependencies': ['stabilize top-left before top amplifier', 'clear upper-right nest and frost before target warming', 'open both central ice gates before lower spread', 'use lower amplifiers before final target pair'], 'feedback': 'each used amplifier becomes an ember flare, blue ice and purple nests disappear, and fog retracts around warm corridors', 'bypass_guard': 'all four targets, every amplifier, every nest, every ice block, and every frost cell are visible board requirements'}}, 7: {'layout': ['############', '#T.FB.A.N.T#', '#.##.##B##.#', '#N.F..F..B.#', '##F###A##F.#', '#..A.#..N..#', '#.B..N..B#.#', '#F..BF..N..#', '#.###A###F.#', '#..N#B.F.A.#', '#T..F.N.B.T#', '############'], 'targets': [(1, 1), (1, 10), (10, 1), (10, 10)], 'initial_frost': [(1, 3), (3, 3), (3, 6), (4, 2), (4, 9), (7, 1), (7, 5), (8, 9), (9, 7), (10, 4)], 'initial_ice': [(1, 4), (2, 7), (3, 9), (6, 2), (6, 8), (7, 4), (9, 5), (10, 8)], 'initial_nests': [(1, 8), (3, 1), (5, 8), (6, 5), (7, 8), (9, 3), (10, 6)], 'initial_amps': [(1, 6), (4, 6), (5, 3), (8, 5), (9, 9)], 'budget': 50, 'active_tags': ['spread', 'ice', 'nests', 'fog', 'amplifier'], 'fog_radius': 1, 'goal_requirements': {'all_targets_warm': True, 'frost_cleared': True, 'ice_cleared': True, 'nests_cleared': True, 'amps_used': True}, 'design_contract': {'success_trigger': 'board_matches_target', 'state_keys': ['all_targets_warm', 'frost_cleared', 'ice_cleared', 'nests_cleared', 'amps_used'], 'primary_blocker': 'near-black fog leaves only local warm islands visible while every quadrant contains interlocked frost, ice, nests, and amplifier timing choices', 'dependencies': ['secure top-left before spending the first amplifier', 'clear both upper nests before top-right target', 'open the central amplifier chain', 'stabilize lower-left before crossing to the final right branch', 'use the final amplifier before warming the last target'], 'feedback': 'each local click retracts fog around the warmed island; amplifiers flare red/yellow and all blockers visibly disappear when solved', 'bypass_guard': 'final completion requires the entire visible cellular field stabilized: four warm targets, no frost, no ice, no nests, and no unused amplifiers'}}}
NEIGHBORS4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def _cell_at_pixel(y, x):
    r = (y - ORIGIN_R) // CELL
    c = (x - ORIGIN_C) // CELL
    if 0 <= r < BOARD_H and 0 <= c < BOARD_W:
        return (int(r), int(c))
    return None

def _is_wall(level, r, c):
    return LEVELS[level]['layout'][r][c] == '#'

def _in_bounds(r, c):
    return 0 <= r < BOARD_H and 0 <= c < BOARD_W

def _parse_cells(value):
    return set((tuple(p) for p in value))

def _pack_cells(cells):
    return sorted([tuple(p) for p in cells])

def _draw_entity(grid, row, col, entity_type):
    y0 = ORIGIN_R + row * CELL
    x0 = ORIGIN_C + col * CELL
    if entity_type == 'floor':
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                grid[y][x] = COLORS['floor']
    elif entity_type == 'wall':
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                edge = y in (y0, y0 + CELL - 1) or x in (x0, x0 + CELL - 1)
                grid[y][x] = COLORS['wall_edge'] if edge else COLORS['wall']
    elif entity_type == 'frost':
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                grid[y][x] = COLORS['frost'] if (y + x) % 2 == 0 else COLORS['frost_core']
    elif entity_type == 'warm':
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                grid[y][x] = COLORS['warm']
        grid[y0 + 1][x0 + 1] = COLORS['heat_core']
        grid[y0 + 1][x0 + 2] = COLORS['heat_core']
        grid[y0 + 2][x0 + 1] = COLORS['heat_core']
        grid[y0 + 2][x0 + 2] = COLORS['heat_core']
    elif entity_type == 'ember':
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                grid[y][x] = COLORS['warm']
        for i in range(CELL):
            grid[y0 + 1][x0 + i] = COLORS['ember']
            grid[y0 + 2][x0 + i] = COLORS['ember']
            grid[y0 + i][x0 + 1] = COLORS['ember']
            grid[y0 + i][x0 + 2] = COLORS['ember']
        grid[y0 + 1][x0 + 1] = COLORS['heat_core']
        grid[y0 + 2][x0 + 2] = COLORS['heat_core']
    elif entity_type == 'target':
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                edge = y in (y0, y0 + CELL - 1) or x in (x0, x0 + CELL - 1)
                grid[y][x] = COLORS['target'] if edge else BG_COLOR
        grid[y0 + 1][x0 + 1] = COLORS['target_core']
        grid[y0 + 1][x0 + 2] = COLORS['target_core']
        grid[y0 + 2][x0 + 1] = COLORS['target_core']
        grid[y0 + 2][x0 + 2] = COLORS['target_core']
    elif entity_type == 'target_warm':
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                edge = y in (y0, y0 + CELL - 1) or x in (x0, x0 + CELL - 1)
                grid[y][x] = COLORS['target'] if edge else COLORS['heat_core']
    elif entity_type == 'ice':
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                edge = y in (y0, y0 + CELL - 1) or x in (x0, x0 + CELL - 1)
                grid[y][x] = COLORS['ice'] if edge else BG_COLOR
        grid[y0 + 1][x0 + 1] = COLORS['crack']
        grid[y0 + 2][x0 + 2] = COLORS['crack']
        grid[y0 + 1][x0 + 2] = COLORS['crack']
    elif entity_type == 'nest':
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                grid[y][x] = COLORS['nest'] if x in (x0, x0 + CELL - 1) or y in (y0, y0 + CELL - 1) else COLORS['frost']
        grid[y0 + 1][x0 + 1] = COLORS['nest_core']
        grid[y0 + 1][x0 + 2] = COLORS['nest_core']
        grid[y0 + 2][x0 + 1] = COLORS['nest_core']
        grid[y0 + 2][x0 + 2] = COLORS['nest_core']
    elif entity_type == 'amp':
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                edge = y in (y0, y0 + CELL - 1) or x in (x0, x0 + CELL - 1)
                grid[y][x] = COLORS['amp'] if edge else COLORS['floor']
        grid[y0 + 1][x0 + 1] = COLORS['amp_core']
        grid[y0 + 1][x0 + 2] = COLORS['amp_core']
        grid[y0 + 2][x0 + 1] = COLORS['amp_core']
        grid[y0 + 2][x0 + 2] = COLORS['amp_core']

def _targets_warm(h_t, level):
    warm = _parse_cells(h_t.get('warm', []))
    frost = _parse_cells(h_t.get('frost', []))
    for t in LEVELS[level]['targets']:
        if tuple(t) not in warm or tuple(t) in frost:
            return False
    return True

def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    new_h = copy.deepcopy(h_t)
    level = h_t['level']
    cfg = LEVELS[level]
    base = a_t[0] if isinstance(a_t, tuple) else a_t
    if base not in get_available_actions():
        return new_h
    if base == 0:
        fresh, _ = get_initial_state(level)
        return fresh
    if base != 6 or not isinstance(a_t, tuple) or len(a_t) != 3:
        return new_h
    clicked = _cell_at_pixel(a_t[2], a_t[1])
    if clicked is None:
        return new_h
    r, c = clicked
    if _is_wall(level, r, c):
        return new_h
    if h_t.get('complete', False) or h_t.get('failed', False):
        return new_h
    if h_t['step'] >= cfg['budget']:
        new_h['failed'] = True
        return new_h
    warm = _parse_cells(h_t.get('warm', []))
    frost = _parse_cells(h_t.get('frost', []))
    embers = _parse_cells(h_t.get('embers', []))
    ice = _parse_cells(h_t.get('ice', []))
    nests = _parse_cells(h_t.get('nests', []))
    amps = _parse_cells(h_t.get('amps', []))
    used_amps = _parse_cells(h_t.get('used_amps', []))
    clicked_ice = (r, c) in ice
    if (r, c) in ice:
        ice.remove((r, c))
    if (r, c) in nests:
        nests.remove((r, c))
    clicked_amp = (r, c) in amps
    if clicked_amp:
        amps.remove((r, c))
        used_amps.add((r, c))
    embers.add((r, c))
    heat = set()
    for rr in range(r - 2, r + 3):
        for cc in range(c - 2, c + 3):
            if _in_bounds(rr, cc) and (not _is_wall(level, rr, cc)) and ((rr, cc) not in ice) and ((rr, cc) not in nests) and (abs(rr - r) + abs(cc - c) <= 2):
                heat.add((rr, cc))
    if clicked_amp and 'amplifier' in cfg.get('active_tags', []):
        for dr, dc in NEIGHBORS4:
            for dist in range(1, 5):
                nr, nc = (r + dr * dist, c + dc * dist)
                if not _in_bounds(nr, nc) or _is_wall(level, nr, nc) or (nr, nc) in ice or ((nr, nc) in nests):
                    break
                heat.add((nr, nc))
    for wr, wc in list(warm):
        near_burst = abs(wr - r) + abs(wc - c) <= 3
        if near_burst:
            for dr, dc in NEIGHBORS4:
                nr, nc = (wr + dr, wc + dc)
                if _in_bounds(nr, nc) and (not _is_wall(level, nr, nc)) and ((nr, nc) not in ice) and ((nr, nc) not in nests):
                    heat.add((nr, nc))
    warm |= heat
    frost -= heat
    if 'spread' in cfg.get('active_tags', []):
        spread = set()
        for fr, fc in frost:
            for dr, dc in NEIGHBORS4:
                nr, nc = (fr + dr, fc + dc)
                if _in_bounds(nr, nc) and (not _is_wall(level, nr, nc)) and ((nr, nc) not in warm) and ((nr, nc) not in ice) and ((nr, nc) not in nests):
                    spread.add((nr, nc))
        mature = set()
        for sr, sc in spread:
            cold_n = 0
            for dr, dc in NEIGHBORS4:
                nr, nc = (sr + dr, sc + dc)
                if _in_bounds(nr, nc) and (not _is_wall(level, nr, nc)) and ((nr, nc) not in warm) and ((nr, nc) not in ice) and ((nr, nc) not in nests):
                    cold_n += 1
            if cold_n >= 4:
                mature.add((sr, sc))
        frost |= mature
    new_h['warm'] = _pack_cells(warm)
    new_h['frost'] = _pack_cells(frost)
    new_h['embers'] = _pack_cells(embers)
    new_h['ice'] = _pack_cells(ice)
    new_h['nests'] = _pack_cells(nests)
    new_h['amps'] = _pack_cells(amps)
    new_h['used_amps'] = _pack_cells(used_amps)
    new_h['step'] = h_t['step'] + 1
    new_h['all_targets_warm'] = _targets_warm(new_h, level)
    new_h['frost_cleared'] = len(new_h['frost']) == 0
    new_h['ice_cleared'] = len(new_h['ice']) == 0
    new_h['nests_cleared'] = len(new_h['nests']) == 0
    new_h['amps_used'] = len(new_h['amps']) == 0
    new_h['complete'] = check_level_complete(new_h, {}, level)
    if new_h['step'] >= cfg['budget'] and (not new_h['complete']):
        new_h['failed'] = True
    return new_h

def predict(h_t: dict) -> dict:
    return {}

def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    cfg = LEVELS[level]
    req = cfg.get('goal_requirements', {})
    if req.get('all_targets_warm', False) and (not _targets_warm(h_t, level)):
        return False
    if req.get('frost_cleared', False) and len(_parse_cells(h_t.get('frost', []))) != 0:
        return False
    if req.get('ice_cleared', False) and len(_parse_cells(h_t.get('ice', []))) != 0:
        return False
    if req.get('nests_cleared', False) and len(_parse_cells(h_t.get('nests', []))) != 0:
        return False
    if req.get('amps_used', False) and len(_parse_cells(h_t.get('amps', []))) != 0:
        return False
    return True

def render(h_t: dict, z_t: dict) -> list[list[int]]:
    level = h_t['level']
    cfg = LEVELS[level]
    grid = [[BG_COLOR for _ in range(64)] for _ in range(64)]
    for r in range(BOARD_H):
        for c in range(BOARD_W):
            _draw_entity(grid, r, c, 'wall' if _is_wall(level, r, c) else 'floor')
    warm = _parse_cells(h_t.get('warm', []))
    frost = _parse_cells(h_t.get('frost', []))
    embers = _parse_cells(h_t.get('embers', []))
    ice = _parse_cells(h_t.get('ice', []))
    nests = _parse_cells(h_t.get('nests', []))
    amps = _parse_cells(h_t.get('amps', []))
    targets = set((tuple(t) for t in cfg['targets']))
    for r, c in sorted(warm):
        _draw_entity(grid, r, c, 'warm')
    for r, c in sorted(targets):
        _draw_entity(grid, r, c, 'target_warm' if (r, c) in warm else 'target')
    for r, c in sorted(frost):
        _draw_entity(grid, r, c, 'frost')
    for r, c in sorted(ice):
        _draw_entity(grid, r, c, 'ice')
    for r, c in sorted(nests):
        _draw_entity(grid, r, c, 'nest')
    for r, c in sorted(amps):
        _draw_entity(grid, r, c, 'amp')
    for r, c in sorted(embers):
        _draw_entity(grid, r, c, 'ember')
    budget = cfg['budget']
    used = min(h_t.get('step', 0), budget)
    for x in range(2, 2 + budget * 2):
        if 0 <= x < 64:
            grid[1][x] = COLORS['hud_used'] if x < 2 + used * 2 else COLORS['hud']
    lamp_color = COLORS['target'] if h_t.get('all_targets_warm', False) else COLORS['wall']
    clear_color = COLORS['heat_core'] if h_t.get('frost_cleared', False) else COLORS['frost']
    for y in range(1, 4):
        for x in range(44, 47):
            grid[y][x] = lamp_color
        for x in range(49, 52):
            grid[y][x] = clear_color
    fog_radius = cfg.get('fog_radius')
    if fog_radius is not None:
        visible = set(targets) | warm | embers
        mask_cells = set()
        for vr, vc in visible:
            for rr in range(BOARD_H):
                for cc in range(BOARD_W):
                    if abs(rr - vr) + abs(cc - vc) <= fog_radius:
                        mask_cells.add((rr, cc))
        for rr in range(BOARD_H):
            for cc in range(BOARD_W):
                if (rr, cc) not in mask_cells:
                    y0 = ORIGIN_R + rr * CELL
                    x0 = ORIGIN_C + cc * CELL
                    for y in range(y0, y0 + CELL):
                        for x in range(x0, x0 + CELL):
                            grid[y][x] = COLORS['fog'] if (x + y) % 2 == 0 else BG_COLOR
    return grid

def get_initial_state(level: int) -> tuple[dict, dict]:
    cfg = LEVELS[level]
    h_t = {'level': level, 'step': 0, 'warm': [], 'frost': _pack_cells(cfg['initial_frost']), 'ice': _pack_cells(cfg.get('initial_ice', [])), 'nests': _pack_cells(cfg.get('initial_nests', [])), 'amps': _pack_cells(cfg.get('initial_amps', [])), 'used_amps': [], 'embers': [], 'complete': False, 'failed': False, 'all_targets_warm': False, 'frost_cleared': False, 'ice_cleared': len(cfg.get('initial_ice', [])) == 0, 'nests_cleared': len(cfg.get('initial_nests', [])) == 0, 'amps_used': len(cfg.get('initial_amps', [])) == 0}
    return (h_t, predict(h_t))

def get_available_actions() -> list[int]:
    return [0, 6]

def solve_level(level: int) -> list:
    if level == 0:

        def click_cell(r, c):
            return (6, ORIGIN_C + c * CELL + CELL // 2, ORIGIN_R + r * CELL + CELL // 2)
        return [click_cell(5, 5), click_cell(5, 3), click_cell(4, 1), click_cell(9, 2), click_cell(9, 5), click_cell(8, 4), click_cell(4, 9), click_cell(1, 8), click_cell(9, 1)]
    if level == 1:

        def click_cell(r, c):
            return (6, ORIGIN_C + c * CELL + CELL // 2, ORIGIN_R + r * CELL + CELL // 2)
        return [click_cell(1, 7), click_cell(1, 4), click_cell(1, 1), click_cell(4, 3), click_cell(4, 7), click_cell(6, 6), click_cell(7, 6), click_cell(8, 1), click_cell(10, 3), click_cell(8, 9), click_cell(10, 8), click_cell(9, 10)]
    if level == 2:

        def click_cell(r, c):
            return (6, ORIGIN_C + c * CELL + CELL // 2, ORIGIN_R + r * CELL + CELL // 2)
        return [click_cell(2, 7), click_cell(3, 5), click_cell(1, 6), click_cell(1, 3), click_cell(4, 3), click_cell(4, 7), click_cell(6, 2), click_cell(7, 6), click_cell(8, 1), click_cell(9, 7), click_cell(8, 9), click_cell(10, 10), click_cell(10, 5), click_cell(10, 1), click_cell(6, 10)]
    if level == 3:

        def click_cell(r, c):
            return (6, ORIGIN_C + c * CELL + CELL // 2, ORIGIN_R + r * CELL + CELL // 2)
        return [click_cell(1, 5), click_cell(1, 9), click_cell(3, 4), click_cell(1, 1), click_cell(4, 2), click_cell(4, 6), click_cell(5, 9), click_cell(6, 2), click_cell(7, 5), click_cell(6, 8), click_cell(8, 1), click_cell(8, 9), click_cell(9, 7), click_cell(10, 5), click_cell(10, 9), click_cell(10, 1)]
    if level == 4:

        def click_cell(r, c):
            return (6, ORIGIN_C + c * CELL + CELL // 2, ORIGIN_R + r * CELL + CELL // 2)
        return [click_cell(1, 3), click_cell(3, 3), click_cell(3, 5), click_cell(1, 7), click_cell(1, 1), click_cell(1, 10), click_cell(4, 2), click_cell(4, 6), click_cell(4, 9), click_cell(6, 2), click_cell(6, 5), click_cell(7, 5), click_cell(6, 8), click_cell(8, 1), click_cell(8, 9), click_cell(9, 3), click_cell(9, 7), click_cell(9, 9), click_cell(10, 5), click_cell(10, 9), click_cell(10, 1)]
    if level == 5:

        def click_cell(r, c):
            return (6, ORIGIN_C + c * CELL + CELL // 2, ORIGIN_R + r * CELL + CELL // 2)
        return [
            click_cell(1, 4),   # top-left frost
            click_cell(1, 6),   # top ice
            click_cell(2, 7),   # top amplifier reveal
            click_cell(1, 1),   # top-left target
            click_cell(3, 3),   # upper-left nest
            click_cell(4, 2),   # central-left frost
            click_cell(1, 9),   # upper-right nest
            click_cell(3, 8),   # upper-right frost
            click_cell(1, 10),  # top-right target
            click_cell(4, 6),   # central ice
            click_cell(5, 8),   # middle-right amplifier
            click_cell(6, 5),   # central nest
            click_cell(6, 2),   # left lower ice
            click_cell(6, 8),   # right lower ice
            click_cell(7, 5),   # middle frost
            click_cell(8, 1),   # lower-left frost
            click_cell(8, 9),   # lower-right frost
            click_cell(9, 3),   # lower amplifier
            click_cell(9, 7),   # bottom connector frost
            click_cell(10, 4),  # lower ice
            click_cell(10, 8),  # lower-right nest
            click_cell(10, 1),  # lower-left target
            click_cell(10, 10), # lower-right target
        ]
    if level == 6:

        def click_cell(r, c):
            return (6, ORIGIN_C + c * CELL + CELL // 2, ORIGIN_R + r * CELL + CELL // 2)
        return [
            click_cell(1, 3),   # top-left frost
            click_cell(1, 4),   # top-left ice
            click_cell(1, 6),   # top amplifier
            click_cell(1, 1),   # top-left target
            click_cell(3, 3),   # upper-left nest
            click_cell(4, 2),   # central-left frost
            click_cell(1, 8),   # upper-right nest
            click_cell(3, 6),   # upper frost
            click_cell(3, 9),   # upper-right ice
            click_cell(4, 9),   # upper-right frost
            click_cell(1, 10),  # top-right target
            click_cell(4, 6),   # central ice gate
            click_cell(5, 3),   # left amplifier
            click_cell(5, 8),   # right amplifier
            click_cell(6, 5),   # central nest
            click_cell(6, 2),   # lower-left ice
            click_cell(6, 8),   # lower-right ice
            click_cell(7, 1),   # lower-left frost
            click_cell(7, 5),   # lower-middle frost
            click_cell(7, 8),   # lower-right nest
            click_cell(8, 9),   # right lower frost
            click_cell(9, 3),   # lower amplifier
            click_cell(9, 5),   # lower ice
            click_cell(9, 7),   # bottom connector frost
            click_cell(10, 4),  # bottom nest
            click_cell(10, 8),  # bottom-right ice
            click_cell(10, 1),  # lower-left target
            click_cell(10, 10), # lower-right target
        ]
    if level == 7:

        def click_cell(r, c):
            return (6, ORIGIN_C + c * CELL + CELL // 2, ORIGIN_R + r * CELL + CELL // 2)
        return [
            click_cell(1, 3),   # top-left frost
            click_cell(1, 4),   # top-left ice
            click_cell(1, 6),   # first amplifier
            click_cell(1, 1),   # warm top-left scale
            click_cell(3, 1),   # left hidden nest
            click_cell(3, 3),   # upper-left frost
            click_cell(4, 2),   # left-central frost
            click_cell(1, 8),   # upper-right nest
            click_cell(2, 6),   # top central ice
            click_cell(3, 6),   # upper connector frost
            click_cell(3, 9),   # upper-right ice
            click_cell(4, 6),   # central amplifier
            click_cell(4, 9),   # upper-right frost
            click_cell(1, 10),  # warm top-right scale
            click_cell(5, 3),   # left amplifier
            click_cell(5, 8),   # right middle nest
            click_cell(6, 5),   # central nest
            click_cell(6, 2),   # lower-left ice
            click_cell(6, 8),   # lower-right ice
            click_cell(7, 1),   # lower-left frost
            click_cell(7, 4),   # lower bridge ice
            click_cell(7, 5),   # lower bridge frost
            click_cell(7, 8),   # right lower nest
            click_cell(8, 5),   # lower central amplifier
            click_cell(8, 9),   # right lower frost
            click_cell(9, 3),   # bottom-left nest
            click_cell(9, 5),   # bottom bridge ice
            click_cell(9, 7),   # bottom connector frost
            click_cell(9, 9),   # final amplifier
            click_cell(10, 4),  # bottom-left frost
            click_cell(10, 6),  # bottom nest
            click_cell(10, 8),  # bottom-right ice
            click_cell(10, 1),  # warm lower-left scale
            click_cell(10, 10), # warm lower-right scale
            click_cell(2, 7),   # clear the last hidden upper ice seam
        ]
    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Sf2048(_FunctionalArcGame):
    GAME_ID = "sf2048-f3d334c1"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
