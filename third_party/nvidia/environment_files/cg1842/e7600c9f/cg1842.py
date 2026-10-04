# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the cg1842/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy

BG_COLOR = 0
GRID_SIZE = 64
CELL = 5
BOARD_R0 = 2
BOARD_C0 = 2

COLORS = {
    "bg": 0,
    "wall": 2,
    "seal": 2,
    "fog": 2,
    "player": 5,
    "exit": 5,
    "core": 8,
    "blast": 8,
}

LEVELS = {
    0: {
        "layout": [
            "############",
            "#..........#",
            "#.######...#",
            "#.#....#..E#",
            "#.#S##.#.#.#",
            "#.#.cS.....#",
            "###..S.#.#.#",
            "#.C.########",
            "#.#.##.###.#",
            "#P#.......##",
            "#.########.#",
            "############",
        ],
        "player_start": (9, 1),
        "core_start": (7, 2),
        "cores": [(7, 2)],
        "exit": (3, 10),
        "seals": [(4, 3), (5, 5), (6, 5)],
        "blast_centers": [(5, 4)],
        "blast_groups": [
            {"center": (5, 4), "seals": [(4, 3), (5, 5), (6, 5)]},
        ],
        "budget": 25,
        "active_tags": [],
        "goal_requirements": {
            "cleared_seals": [(4, 3), (5, 5), (6, 5)],
            "core_used": True,
        },
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "three gray pattern seals block the only passage to the exit lane",
            "dependencies": ["collect slam core", "stand at the 3x3 blast center matching all seals", "cross the cleared seal passage"],
            "feedback": "matched seals disappear and a red 3x3 blast outline remains around the slam center",
            "bypass_guard": "walls force every route to the exit through the seal passage, which is solid until cleared",
        },
    },
    1: {
        "layout": [
            "############",
            "#########.E#",
            "#########..#",
            "########S.##",
            "########cS##",
            "#######..S##",
            "######S.####",
            "#....cS.C###",
            "#..C..S.####",
            "#.###c######",
            "#P##########",
            "############",
        ],
        "player_start": (10, 1),
        "core_start": (8, 3),
        "cores": [(8, 3), (7, 8)],
        "exit": (1, 10),
        "seals": [(6, 6), (7, 6), (8, 6), (3, 8), (4, 9), (5, 9)],
        "blast_centers": [(7, 5), (4, 8)],
        "blast_groups": [
            {"center": (7, 5), "seals": [(6, 6), (7, 6), (8, 6)]},
            {"center": (4, 8), "seals": [(3, 8), (4, 9), (5, 9)]},
        ],
        "budget": 30,
        "active_tags": ["multi_core"],
        "goal_requirements": {
            "cleared_seals": [(3, 8), (4, 9), (5, 9), (6, 6), (7, 6), (8, 6)],
            "core_used": True,
        },
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "two separated gray seal curtains block the only route to the exit",
            "dependencies": ["collect first core", "match first vertical seal pattern", "collect second core beyond the first curtain", "match second bent seal pattern", "enter exit"],
            "feedback": "each matched group vanishes and leaves a red 3x3 blast outline; a decoy center remains visible but does not clear the curtain",
            "bypass_guard": "the second core and the exit corridor are physically behind the first and second uncleared seal curtains",
        },
    },
    2: {
        "layout": [
            "############",
            "#EG#########",
            "##.#########",
            "##.SS#######",
            "####cS######",
            "###C.#######",
            "####.S######",
            "####.Sc.####",
            "#####S#.C..#",
            "##########.#",
            "##########P#",
            "############",
        ],
        "player_start": (10, 10),
        "core_start": (8, 8),
        "cores": [(8, 8), (5, 3)],
        "exit": (1, 1),
        "gates": [(1, 2)],
        "seals": [(6, 5), (7, 5), (8, 5), (3, 3), (3, 4), (4, 5)],
        "blast_centers": [(7, 6), (4, 4)],
        "blast_groups": [
            {"center": (7, 6), "seals": [(6, 5), (7, 5), (8, 5)]},
            {"center": (4, 4), "seals": [(3, 3), (3, 4), (4, 5)]},
        ],
        "budget": 30,
        "active_tags": ["multi_core", "gate"],
        "goal_requirements": {
            "cleared_seals": [(3, 3), (3, 4), (4, 5), (6, 5), (7, 5), (8, 5)],
            "core_used": True,
            "gate_open": True,
        },
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "a gray gate seals the exit and two seal curtains block the route to that gate",
            "dependencies": ["collect first core", "match the lower vertical seal pattern", "collect second core", "match the upper bent seal pattern", "open the gate", "enter exit"],
            "feedback": "each seal group vanishes after the correct red 3x3 slam; the gate disappears only after all seals are gone",
            "bypass_guard": "the exit tile is enclosed behind the gate, and the gate tile rejects movement until every declared seal is cleared",
        },
    },
    3: {
        "layout": [
            "############",
            "#########GE#",
            "#########..#",
            "########S.##",
            "########cS##",
            "#######..S##",
            "######.C####",
            "####S..#####",
            "###HcS######",
            "###..S######",
            "#P.C########",
            "############",
        ],
        "player_start": (10, 1),
        "core_start": (10, 3),
        "cores": [(10, 3), (6, 7)],
        "exit": (1, 10),
        "gates": [(1, 9)],
        "hazards": [(8, 3)],
        "seals": [(7, 4), (8, 5), (9, 5), (3, 8), (4, 9), (5, 9)],
        "blast_centers": [(8, 4), (4, 8)],
        "blast_groups": [
            {"center": (8, 4), "seals": [(7, 4), (8, 5), (9, 5)]},
            {"center": (4, 8), "seals": [(3, 8), (4, 9), (5, 9)]},
        ],
        "budget": 26,
        "active_tags": ["multi_core", "gate", "hazard"],
        "goal_requirements": {
            "cleared_seals": [(3, 8), (4, 9), (5, 9), (7, 4), (8, 5), (9, 5)],
            "core_used": True,
            "gate_open": True,
        },
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "two pattern seal curtains and a final gate block the gallery exit while a red hazard branch punishes the wrong center-side move",
            "dependencies": ["collect lower core", "match the lower 3x3 seal pattern while avoiding the hazard", "collect upper core", "match the upper seal pattern", "open gate", "enter exit"],
            "feedback": "correct slam centers erase their gray seals; stepping into the red hazard ends the run; the exit gate opens after both patterns clear",
            "bypass_guard": "the only route to the exit crosses cleared seal cells and then the closed gate, so the exit cannot be occupied early",
        },
    },
    4: {
        "layout": [
            "############",
            "#########GE#",
            "#######..S##",
            "#######.cS##",
            "#####....S##",
            "#####.##C.##",
            "#####.##.###",
            "####S...####",
            "####.cS.####",
            "####..S.####",
            "#P..C..H####",
            "############",
        ],
        "player_start": (10, 1),
        "core_start": (10, 4),
        "cores": [(10, 4), (5, 8)],
        "exit": (1, 10),
        "gates": [(1, 9)],
        "hazards": [(10, 7)],
        "seals": [(7, 4), (8, 6), (9, 6), (2, 9), (3, 9), (4, 9)],
        "blast_centers": [(8, 5), (3, 8)],
        "blast_groups": [
            {"center": (8, 5), "seals": [(7, 4), (8, 6), (9, 6)]},
            {"center": (3, 8), "seals": [(2, 9), (3, 9), (4, 9)]},
        ],
        "budget": 28,
        "fog_radius": 4,
        "active_tags": ["multi_core", "gate", "hazard", "fog"],
        "goal_requirements": {
            "cleared_seals": [(2, 9), (3, 9), (4, 9), (7, 4), (8, 6), (9, 6)],
            "core_used": True,
            "gate_open": True,
        },
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "fog hides the upper seal pattern until the player advances, while two curtains and a gate still block the exit",
            "dependencies": ["carry lower core to the visible local pattern center", "remember the corridor under fog", "collect upper core", "match the fog-revealed upper pattern", "open gate", "enter exit"],
            "feedback": "nearby seals and slam centers appear through the fog; each correct slam removes a curtain and finally the gate",
            "bypass_guard": "the exit is behind a gate that stays closed until both fogged seal groups are cleared",
        },
    },
    5: {
        "layout": [
            "############",
            "############",
            "####SSG..E##",
            "#####cS#####",
            "#####..#####",
            "######C.S.##",
            "########cS##",
            "#####S...S##",
            "####cS.C####",
            "###..S######",
            "#P.C.H######",
            "############",
        ],
        "player_start": (10, 1),
        "core_start": (10, 3),
        "cores": [(10, 3), (8, 7), (5, 6)],
        "exit": (2, 9),
        "gates": [(2, 6)],
        "hazards": [(10, 5)],
        "seals": [(7, 5), (8, 5), (9, 5), (5, 8), (6, 9), (7, 9), (2, 4), (2, 5), (3, 6)],
        "blast_centers": [(8, 4), (6, 8), (3, 5)],
        "blast_groups": [
            {"center": (8, 4), "seals": [(7, 5), (8, 5), (9, 5)]},
            {"center": (6, 8), "seals": [(5, 8), (6, 9), (7, 9)]},
            {"center": (3, 5), "seals": [(2, 4), (2, 5), (3, 6)]},
        ],
        "budget": 32,
        "fog_radius": 4,
        "active_tags": ["multi_core", "gate", "hazard", "fog"],
        "goal_requirements": {
            "cleared_seals": [(2, 4), (2, 5), (3, 6), (5, 8), (6, 9), (7, 5), (7, 9), (8, 5), (9, 5)],
            "core_used": True,
            "gate_open": True,
        },
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "three ordered fogged seal patterns and a final gate divide the arena into chained territories",
            "dependencies": ["collect first core", "match first vertical seal curtain", "collect second core", "match second offset seal pattern", "collect third core", "match top lock pattern", "open gate", "enter exit"],
            "feedback": "each correct red slam removes exactly one three-seal curtain; the last cleared pattern opens the gray gate",
            "bypass_guard": "each later core and the exit route sit beyond the previous uncleared seal curtain, and the exit is also locked by the gate",
        },
    },
    6: {
        "layout": [
            "############",
            "############",
            "####SSG..E##",
            "#####cS#####",
            "#####..#####",
            "######C.S.##",
            "########cS##",
            "#####S...S##",
            "####cS.C####",
            "###..S######",
            "#P.CxH######",
            "############",
        ],
        "player_start": (10, 1),
        "core_start": (10, 3),
        "cores": [(10, 3), (8, 7), (5, 6)],
        "exit": (2, 9),
        "gates": [(2, 6)],
        "hazards": [(10, 5)],
        "trap_centers": [(10, 4)],
        "decoy_seals": [(9, 4), (10, 5)],
        "seals": [(7, 5), (8, 5), (9, 5), (5, 8), (6, 9), (7, 9), (2, 4), (2, 5), (3, 6)],
        "blast_centers": [(8, 4), (6, 8), (3, 5)],
        "blast_groups": [
            {"center": (8, 4), "seals": [(7, 5), (8, 5), (9, 5)]},
            {"center": (6, 8), "seals": [(5, 8), (6, 9), (7, 9)]},
            {"center": (3, 5), "seals": [(2, 4), (2, 5), (3, 6)]},
        ],
        "budget": 32,
        "fog_radius": 3,
        "active_tags": ["multi_core", "gate", "hazard", "fog", "decoy"],
        "goal_requirements": {
            "cleared_seals": [(2, 4), (2, 5), (3, 6), (5, 8), (6, 9), (7, 5), (7, 9), (8, 5), (9, 5)],
            "core_used": True,
            "gate_open": True,
        },
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "fog plus a false red slam center near the first core can consume the run; three real pattern curtains and a gate still block the exit",
            "dependencies": ["ignore the decoy center whose nearby seals do not match the 3x3 target pattern", "clear lower curtain", "clear right curtain", "clear top gate curtain", "enter exit"],
            "feedback": "a trap-center slam immediately fails, while true centers remove exactly their matching gray seal triplets and open the gate after all true groups clear",
            "bypass_guard": "the exit corridor remains behind the declared gate and all traversed seal curtains until every real seal group is cleared",
        },
    },
    7: {
        "layout": [
            "############",
            "#EG##S######",
            "##..Sc######",
            "####S.C#####",
            "######..S###",
            "#######Sc###",
            "#######S.C##",
            "#######S..##",
            "###S##.cS.##",
            "###cS#..S###",
            "#PC.S.CxH###",
            "############",
        ],
        "player_start": (10, 1),
        "core_start": (10, 2),
        "cores": [(10, 2), (10, 6), (6, 9), (3, 6)],
        "exit": (1, 1),
        "gates": [(1, 2)],
        "hazards": [(10, 8)],
        "trap_centers": [(10, 7)],
        "decoy_seals": [(9, 7), (10, 8)],
        "seals": [(8, 3), (9, 4), (10, 4), (7, 7), (8, 8), (9, 8), (4, 8), (5, 7), (6, 7), (1, 5), (2, 4), (3, 4)],
        "blast_centers": [(9, 3), (8, 7), (5, 8), (2, 5)],
        "blast_groups": [
            {"center": (9, 3), "seals": [(8, 3), (9, 4), (10, 4)]},
            {"center": (8, 7), "seals": [(7, 7), (8, 8), (9, 8)]},
            {"center": (5, 8), "seals": [(4, 8), (5, 7), (6, 7)]},
            {"center": (2, 5), "seals": [(1, 5), (2, 4), (3, 4)]},
        ],
        "budget": 38,
        "fog_radius": 3,
        "active_tags": ["multi_core", "gate", "hazard", "fog", "decoy"],
        "goal_requirements": {
            "cleared_seals": [(1, 5), (2, 4), (3, 4), (4, 8), (5, 7), (6, 7), (7, 7), (8, 3), (8, 8), (9, 4), (9, 8), (10, 4)],
            "core_used": True,
            "gate_open": True,
        },
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "four fogged 3x3 seal constellations, one decoy slam branch, and a final gate segment the arena into chained territories",
            "dependencies": ["collect each core in order", "match the lower-left pattern", "avoid the decoy branch after the second core", "match the middle pattern", "match the upper-right pattern", "match the top lock pattern", "open gate", "enter exit"],
            "feedback": "each correct slam erases a triplet of gray seals and leaves a red 3x3 outline; the false red branch fails immediately; the gate opens only after all four triplets clear",
            "bypass_guard": "every route to the exit crosses the still-closed gate, and that gate remains closed until all four visible pattern groups are cleared",
        },
    },
}

DIRS = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}


def _tile_origin(row, col):
    return BOARD_R0 + row * CELL, BOARD_C0 + col * CELL


def _put(grid, r, c, color):
    if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
        grid[r][c] = color


def _draw_entity(grid, row, col, entity_type):
    pr, pc = _tile_origin(row, col)
    if entity_type == "wall":
        for rr in range(pr, pr + CELL):
            for cc in range(pc, pc + CELL):
                _put(grid, rr, cc, COLORS["wall"])
    elif entity_type == "player":
        mid = 2
        for i in range(CELL):
            _put(grid, pr + mid, pc + i, COLORS["player"])
            _put(grid, pr + i, pc + mid, COLORS["player"])
        _put(grid, pr + mid, pc + mid, BG_COLOR)
    elif entity_type == "core":
        for i in range(4):
            _put(grid, pr + i, pc, COLORS["core"])
            _put(grid, pr + i, pc + 3, COLORS["core"])
            _put(grid, pr, pc + i, COLORS["core"])
            _put(grid, pr + 3, pc + i, COLORS["core"])
        _put(grid, pr + 1, pc + 1, COLORS["core"])
        _put(grid, pr + 2, pc + 2, COLORS["core"])
    elif entity_type == "seal":
        for i in range(4):
            _put(grid, pr, pc + i, COLORS["seal"])
            _put(grid, pr + 3, pc + i, COLORS["seal"])
            _put(grid, pr + i, pc, COLORS["seal"])
            _put(grid, pr + i, pc + 3, COLORS["seal"])
        _put(grid, pr + 1, pc + 1, COLORS["player"])
    elif entity_type == "center":
        _put(grid, pr + 2, pc + 1, COLORS["core"])
        _put(grid, pr + 2, pc + 2, COLORS["core"])
        _put(grid, pr + 2, pc + 3, COLORS["core"])
        _put(grid, pr + 1, pc + 2, COLORS["core"])
        _put(grid, pr + 3, pc + 2, COLORS["core"])
    elif entity_type == "exit":
        for i in range(6):
            _put(grid, pr - 1, pc - 1 + i, COLORS["exit"])
            _put(grid, pr + 4, pc - 1 + i, COLORS["exit"])
            _put(grid, pr - 1 + i, pc - 1, COLORS["exit"])
            _put(grid, pr - 1 + i, pc + 4, COLORS["exit"])
    elif entity_type == "gate":
        for i in range(CELL):
            _put(grid, pr + i, pc, COLORS["wall"])
            _put(grid, pr + i, pc + CELL - 1, COLORS["wall"])
            _put(grid, pr + i, pc + i, COLORS["player"])
            _put(grid, pr + i, pc + CELL - 1 - i, COLORS["player"])
    elif entity_type == "hazard":
        for i in range(CELL):
            _put(grid, pr + i, pc + i, COLORS["core"])
            _put(grid, pr + i, pc + CELL - 1 - i, COLORS["core"])
        _put(grid, pr + 2, pc + 2, COLORS["player"])
    elif entity_type == "blast":
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                br, bc = _tile_origin(row + dr, col + dc)
                _put(grid, br, bc, COLORS["blast"])
                _put(grid, br + CELL - 1, bc, COLORS["blast"])
                _put(grid, br, bc + CELL - 1, COLORS["blast"])
                _put(grid, br + CELL - 1, bc + CELL - 1, COLORS["blast"])


def _is_uncleared_seal(level, h_t, pos):
    return tuple(pos) in {tuple(s) for s in level.get("seals", [])} and tuple(pos) not in {tuple(s) for s in h_t.get("cleared_seals", [])}


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    new_h = copy.deepcopy(h_t)
    base = a_t[0] if isinstance(a_t, tuple) else a_t
    if base not in get_available_actions():
        return new_h
    if base == 0:
        return get_initial_state(h_t["level"])[0]
    if new_h.get("complete") or new_h.get("failed"):
        return new_h
    if base not in DIRS:
        return new_h

    level = LEVELS[new_h["level"]]
    tags = level.get("active_tags", [])
    dr, dc = DIRS[base]
    nr, nc = new_h["player_r"] + dr, new_h["player_c"] + dc
    rows, cols = len(level["layout"]), len(level["layout"][0])
    if not (0 <= nr < rows and 0 <= nc < cols):
        return new_h
    if level["layout"][nr][nc] == "#":
        return new_h
    if _is_uncleared_seal(level, new_h, (nr, nc)):
        return new_h
    if tuple((nr, nc)) in {tuple(g) for g in level.get("gates", [])} and not new_h.get("gate_open", False):
        return new_h

    new_h["player_r"], new_h["player_c"] = nr, nc

    if "hazard" in tags and tuple((nr, nc)) in {tuple(h) for h in level.get("hazards", [])}:
        new_h["step"] += 1
        new_h["budget_left"] -= 1
        new_h["failed"] = True
        return new_h
    if "decoy" in tags and new_h.get("carrying") and tuple((nr, nc)) in {tuple(t) for t in level.get("trap_centers", [])}:
        new_h["step"] += 1
        new_h["budget_left"] -= 1
        new_h["failed"] = True
        return new_h

    cores = [tuple(c) for c in new_h.get("cores_remaining", [])]
    if not new_h.get("carrying") and (nr, nc) in cores:
        cores.remove((nr, nc))
        new_h["cores_remaining"] = cores
        new_h["core_present"] = len(cores) > 0
        new_h["carrying"] = True

    if new_h.get("carrying"):
        new_h["last_blast_center"] = (nr, nc)
        zone = {(nr + rr, nc + cc) for rr in (-1, 0, 1) for cc in (-1, 0, 1)}
        cleared = {tuple(s) for s in new_h.get("cleared_seals", [])}
        for group in level.get("blast_groups", []):
            center = tuple(group["center"])
            targets = {tuple(s) for s in group.get("seals", [])}
            # Level 1 explicitly uses multi_core groups; level 0 has one identical group.
            if ("multi_core" in tags or len(level.get("blast_groups", [])) == 1) and (nr, nc) == center and targets.issubset(zone):
                if not targets.issubset(cleared):
                    cleared |= targets
                    new_h["cleared_seals"] = sorted(list(cleared))
                    new_h["carrying"] = False
                    new_h["core_used"] = True
                    new_h["blast_count"] = new_h.get("blast_count", 0) + 1
                    required_all = {tuple(s) for s in level.get("goal_requirements", {}).get("cleared_seals", [])}
                    if required_all and required_all.issubset(cleared):
                        new_h["gate_open"] = True
                break

    new_h["step"] += 1
    new_h["budget_left"] -= 1
    if check_level_complete(new_h, {}, new_h["level"]):
        new_h["complete"] = True
        return new_h
    if new_h["budget_left"] <= 0:
        new_h["failed"] = True
    return new_h


def predict(h_t: dict) -> dict:
    return {}


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    cfg = LEVELS[level]
    if (h_t.get("player_r"), h_t.get("player_c")) != cfg["exit"]:
        return False
    req = cfg.get("goal_requirements", {})
    if req.get("core_used") and not h_t.get("core_used"):
        return False
    if req.get("gate_open") and not h_t.get("gate_open"):
        return False
    cleared = {tuple(x) for x in h_t.get("cleared_seals", [])}
    for seal in req.get("cleared_seals", []):
        if tuple(seal) not in cleared:
            return False
    return True


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    cfg = LEVELS[h_t["level"]]
    grid = [[BG_COLOR for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    for r, row in enumerate(cfg["layout"]):
        for c, ch in enumerate(row):
            if ch == "#":
                _draw_entity(grid, r, c, "wall")
            elif ch == "c":
                _draw_entity(grid, r, c, "center")
            elif ch == "x":
                _draw_entity(grid, r, c, "center")
                _draw_entity(grid, r, c, "hazard")

    if h_t.get("last_blast_center") is not None:
        br, bc = h_t["last_blast_center"]
        _draw_entity(grid, br, bc, "blast")

    cleared = {tuple(x) for x in h_t.get("cleared_seals", [])}
    for seal in cfg.get("seals", []):
        if tuple(seal) not in cleared:
            _draw_entity(grid, seal[0], seal[1], "seal")
    for seal in cfg.get("decoy_seals", []):
        _draw_entity(grid, seal[0], seal[1], "seal")

    if not h_t.get("gate_open", True):
        for gr, gc in cfg.get("gates", []):
            _draw_entity(grid, gr, gc, "gate")

    for hr, hc in cfg.get("hazards", []):
        _draw_entity(grid, hr, hc, "hazard")

    for cr, cc in h_t.get("cores_remaining", []):
        _draw_entity(grid, cr, cc, "core")
    _draw_entity(grid, cfg["exit"][0], cfg["exit"][1], "exit")
    _draw_entity(grid, h_t["player_r"], h_t["player_c"], "player")

    max_budget = max(1, cfg["budget"])
    filled = max(0, int((h_t.get("budget_left", 0) / max_budget) * GRID_SIZE))
    for c in range(GRID_SIZE):
        grid[0][c] = COLORS["player"] if c < filled else COLORS["wall"]
    if h_t.get("complete"):
        for c in range(0, GRID_SIZE, 2):
            grid[1][c] = COLORS["core"]

    fog_radius = cfg.get("fog_radius")
    if fog_radius is not None:
        pr, pc = h_t["player_r"], h_t["player_c"]
        for tr in range(len(cfg["layout"])):
            for tc in range(len(cfg["layout"][0])):
                if abs(tr - pr) + abs(tc - pc) > fog_radius:
                    rr, cc = _tile_origin(tr, tc)
                    for r in range(rr, min(rr + CELL, GRID_SIZE)):
                        for c in range(cc, min(cc + CELL, GRID_SIZE)):
                            grid[r][c] = COLORS["fog"]
    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    cfg = LEVELS[level]
    pr, pc = cfg["player_start"]
    cores = [tuple(c) for c in cfg.get("cores", [cfg.get("core_start")]) if c is not None]
    h_t = {
        "level": level,
        "step": 0,
        "budget_left": cfg["budget"],
        "player_r": pr,
        "player_c": pc,
        "core_present": len(cores) > 0,
        "cores_remaining": cores,
        "gate_open": len(cfg.get("gates", [])) == 0,
        "carrying": False,
        "core_used": False,
        "blast_count": 0,
        "cleared_seals": [],
        "last_blast_center": None,
        "complete": False,
        "failed": False,
    }
    return h_t, predict(h_t)


def get_available_actions() -> list[int]:
    return [0, 1, 2, 3, 4]


def solve_level(level: int) -> list:
    if level == 0:
        return [1, 1, 4, 4, 1, 1, 4, 4, 4, 4, 4, 4, 4, 1, 1]
    if level == 1:
        return [1, 1, 4, 4, 4, 4, 1, 4, 4, 4, 3, 1, 1, 4, 1, 4, 1, 1, 1, 4]
    if level == 2:
        return [1, 1, 3, 3, 3, 1, 3, 3, 3, 1, 1, 3, 4, 1, 1, 3, 3, 1, 1, 3]
    if level == 3:
        return [4, 4, 1, 4, 1, 1, 4, 4, 1, 4, 1, 4, 1, 1, 4, 1, 1, 4]
    if level == 4:
        return [4, 4, 4, 1, 1, 4, 1, 1, 1, 1, 4, 4, 4, 2, 1, 1, 4, 1, 1, 4]
    if level == 5:
        return [4, 4, 1, 4, 1, 4, 4, 4, 1, 4, 1, 1, 3, 3, 1, 3, 1, 4, 1, 4, 4, 4]
    if level == 6:
        return [4, 4, 1, 4, 1, 4, 4, 4, 1, 4, 1, 1, 3, 3, 1, 3, 1, 4, 1, 4, 4, 4]
    if level == 7:
        return [4, 4, 1, 2, 4, 4, 4, 1, 1, 4, 4, 4, 1, 1, 3, 1, 1, 3, 3, 1, 3, 1, 3, 3, 3, 1, 3]
    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Cg1842(_FunctionalArcGame):
    GAME_ID = "cg1842-e7600c9f"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
