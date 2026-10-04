# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the dl4827/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy

BG_COLOR = 5
GRID_SIZE = 16
COLORS = {
    "wall": 4,
    "player": 14,
    "pad": 14,
    "goal": 11,
    "stud": 11,
    "hazard": 8,
    "fog": 4,
}

LEVELS = {
    0: {
        "layout": [
            "################",
            "#.....#........#",
            "#.....#........#",
            "#.....#........#",
            "#..............#",
            "#..XXXX........#",
            "#..............#",
            "#........##....#",
            "#..............#",
            "#.......XXX....#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#..............#",
            "################",
        ],
        "player_start": (1, 5),
        "goal": (13, 11),
        "studs": {
            "upper": {"coord": (2, 2), "pads": [(5, 5), (5, 6)]},
            "lower": {"coord": (7, 12), "pads": [(9, 8), (9, 9), (9, 10)]},
        },
        "budget": 22,
        "active_tags": [],
        "fog_radius": None,
        "goal_requirements": {"activated_studs": ["upper", "lower"]},
        "design_contract": {
            "success_trigger": "land_on_diamond_socket",
            "primary_blocker": "two red danger rows are only safely crossed after drawing the matching lawn pads",
            "dependencies": ["click upper draw-stud", "steer across upper ledge", "click lower draw-stud", "cross lower ledge", "land on diamond socket"],
            "feedback": "clicked studs turn on green lawn pads over the red danger cells",
            "bypass_guard": "without the upper pad the shell must hit the first danger row; without the lower pad the row-7 wall prevents crossing before the second danger row",
        },
    },
    1: {
        "layout": [
            "################",
            "#..............#",
            "#..............#",
            "#..............#",
            "#XXXXXXXXXX....#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#....XXXXXXXXXX#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#..XXXXXXXX....#",
            "#..............#",
            "#..............#",
            "################",
        ],
        "player_start": (1, 3),
        "goal": (13, 11),
        "studs": {
            "upper": {"coord": (2, 2), "pads": [(4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10)]},
            "middle": {"coord": (6, 13), "pads": [(8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14)]},
            "lower": {"coord": (10, 2), "pads": [(12, 3), (12, 4), (12, 5), (12, 6), (12, 7), (12, 8), (12, 9), (12, 10)]},
        },
        "budget": 42,
        "active_tags": ["dependency"],
        "fog_radius": None,
        "goal_requirements": {"activated_studs": ["upper", "middle", "lower"]},
        "design_contract": {
            "success_trigger": "land_on_diamond_socket",
            "primary_blocker": "three danger bands force a right-left-right zigzag over drawn lawn supports",
            "dependencies": ["click upper draw-stud", "cross right over the first support", "click middle draw-stud", "cross left over the second support", "click lower draw-stud", "cross right over the final support", "land on diamond socket"],
            "feedback": "each clicked stud visibly converts its matching red danger band cells into green support pads",
            "bypass_guard": "the shell cannot cross any danger band before its matching support is drawn; the goal is below all three bands",
        },
    },
    2: {
        "layout": [
            "################",
            "#..............#",
            "#..............#",
            "#..............#",
            "#......XXXXXXXX#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#.XXXXXXXXX....#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#....XXXXXXXXX.#",
            "#..............#",
            "#..............#",
            "################",
        ],
        "player_start": (1, 12),
        "goal": (13, 4),
        "studs": {
            "upper": {"coord": (2, 13), "pads": [(4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13)]},
            "middle": {"coord": (6, 2), "pads": [(8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10)]},
            "lower": {"coord": (10, 13), "pads": [(12, 5), (12, 6), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12), (12, 13)]},
            "decoy": {"coord": (10, 4), "pads": [(11, 4), (11, 5)]},
        },
        "budget": 40,
        "active_tags": ["dependency", "branch"],
        "fog_radius": None,
        "goal_requirements": {"activated_studs": ["upper", "middle", "lower"]},
        "design_contract": {
            "success_trigger": "land_on_diamond_socket",
            "primary_blocker": "three offset danger bands require a left-right-left route and one visible decoy stud can block the final exit lane",
            "dependencies": ["click upper draw-stud", "exit the upper support on the left safe gap", "click middle draw-stud", "exit the middle support on the right safe gap", "click lower draw-stud", "avoid the decoy blocker", "drop into the left diamond socket"],
            "feedback": "required studs turn long red bands into green lawn supports; the decoy draws a short green blocker in the lower exit lane",
            "bypass_guard": "the diamond is below all three danger bands, and the final left socket is unreachable if the decoy blocker is drawn",
        },
    },
    3: {
        "layout": [
            "################",
            "#..............#",
            "#..............#",
            "#..............#",
            "#..XXXXXXXXX...#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#....XXXXXXXXX.#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#...XXXXXXX....#",
            "#..............#",
            "#..............#",
            "################",
        ],
        "player_start": (1, 4),
        "goal": (13, 11),
        "studs": {
            "upper": {"coord": (2, 13), "pads": [(4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11)]},
            "middle": {"coord": (6, 2), "pads": [(8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12)]},
            "lower": {"coord": (10, 13), "pads": [(12, 4), (12, 5), (12, 6), (12, 7), (12, 8), (12, 9), (12, 10)]},
        },
        "spawn_wells": [(1, 8)],
        "spawn_period": 6,
        "spawn_phase": 0,
        "initial_spawns": [],
        "budget": 42,
        "active_tags": ["dependency", "spawn"],
        "fog_radius": None,
        "goal_requirements": {"activated_studs": ["upper", "middle", "lower"]},
        "design_contract": {
            "success_trigger": "land_on_diamond_socket",
            "primary_blocker": "a central spawn well drops red seeds while three offset danger bands still require drawn supports",
            "dependencies": ["click upper draw-stud", "cross the top band before the spawned seed reaches the lane", "click middle draw-stud", "route left while tracking the falling seed column", "click lower draw-stud", "cross right below the seed stream", "land on diamond socket"],
            "feedback": "the red well at the top repeatedly emits falling red seeds; required studs still turn danger bands into green supports",
            "bypass_guard": "the goal lies below every danger band and the central spawn column can kill late or mistimed crossings",
        },
    },
    4: {
        "layout": [
            "################",
            "#..............#",
            "#.#............#",
            "#..............#",
            "#..XXXXXXXXX...#",
            "#..............#",
            "#..........#...#",
            "#..............#",
            "#....XXXXXXXXX.#",
            "#.#............#",
            "#..............#",
            "#............#.#",
            "#...XXXXXXXX...#",
            "#..............#",
            "#..............#",
            "################",
        ],
        "player_start": (1, 4),
        "goal": (13, 12),
        "studs": {
            "upper_pair": {"coord": (2, 13), "pads": [(4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11)]},
            "middle_pair": {"coord": (6, 2), "pads": [(8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12)]},
            "lower_pair": {"coord": (10, 13), "pads": [(12, 4), (12, 5), (12, 6), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11)]},
            "tail": {"coord": (11, 2), "pads": [(14, 11), (14, 12)]},
        },
        "spawn_wells": [(1, 9)],
        "spawn_period": 50,
        "spawn_phase": 0,
        "initial_spawns": [],
        "budget": 44,
        "active_tags": ["dependency", "spawn", "fog"],
        "fog_radius": 7,
        "goal_requirements": {"activated_studs": ["upper_pair", "tail", "middle_pair", "lower_pair"]},
        "design_contract": {
            "success_trigger": "land_on_diamond_socket",
            "primary_blocker": "fog masks the lower half until approached while four studs must be selected in the right order",
            "dependencies": ["click upper paired stud", "cross right over the first support", "click tail support while safely held by the upper pad", "click middle paired stud", "route left through the fog edge", "click lower paired stud", "cross right to the socket"],
            "feedback": "nearby fog clears around the falling shell; clicked studs draw green paired supports, and the red top well marks the spawn lane",
            "bypass_guard": "the diamond is below every danger band and all required supports are visibly drawn before the final drop",
        },
    },
    5: {
        "layout": [
            "################",
            "#..............#",
            "#..........#...#",
            "#..............#",
            "#.....XXXXXXXX.#",
            "#..............#",
            "#.#............#",
            "#..............#",
            "#..XXXXXXXX....#",
            "#..............#",
            "#............#.#",
            "#..............#",
            "#...XXXXXXXX...#",
            "#..............#",
            "#..............#",
            "################",
        ],
        "player_start": (1, 12),
        "goal": (13, 3),
        "studs": {
            "upper": {"coord": (2, 2), "pads": [(4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13)]},
            "middle": {"coord": (6, 13), "pads": [(8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10)]},
            "lower": {"coord": (10, 2), "pads": [(12, 4), (12, 5), (12, 6), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11)]},
            "tail": {"coord": (11, 13), "pads": [(14, 3), (14, 4)]},
        },
        "spawn_wells": [(1, 1), (1, 14)],
        "spawn_period": 50,
        "spawn_phase": 0,
        "initial_spawns": [],
        "budget": 46,
        "active_tags": ["dependency", "spawn", "fog", "branch"],
        "fog_radius": 6,
        "goal_requirements": {"activated_studs": ["upper", "middle", "lower", "tail"]},
        "design_contract": {
            "success_trigger": "land_on_diamond_socket",
            "primary_blocker": "three staggered danger bands and two side spawn streams punish choosing the outside lanes while fog hides the final left exit until approached",
            "dependencies": ["click upper draw-stud", "cross left off the upper support", "click middle draw-stud", "cross right through the central basin", "click lower draw-stud", "click tail marker while held on the lower support", "cross left to the diamond socket"],
            "feedback": "clicked studs draw green supports over red bands; two red spawn wells mark unsafe side lanes; fog clears around the shell",
            "bypass_guard": "the socket sits below all three danger bands and all four declared supports must be visibly drawn before the final drop",
        },
    },
    6: {
        "layout": [
            "################",
            "#..............#",
            "#....#.........#",
            "#..............#",
            "#..XXXXXXXXX...#",
            "#..............#",
            "#.#........#...#",
            "#..............#",
            "#....XXXXXXXXX.#",
            "#..............#",
            "#..........#...#",
            "#..............#",
            "#...XXXXXXXX...#",
            "#..............#",
            "#..............#",
            "################",
        ],
        "player_start": (1, 4),
        "goal": (13, 12),
        "studs": {
            "upper": {"coord": (2, 13), "pads": [(4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11)]},
            "gate": {"coord": (2, 2), "pads": [(3, 13), (4, 13)]},
            "tail": {"coord": (11, 2), "pads": [(14, 11), (14, 12)]},
            "middle": {"coord": (6, 2), "pads": [(8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12)]},
            "lower": {"coord": (10, 13), "pads": [(12, 4), (12, 5), (12, 6), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11)]},
        },
        "spawn_wells": [(1, 7), (1, 14)],
        "spawn_period": 50,
        "spawn_phase": 0,
        "initial_spawns": [],
        "budget": 50,
        "active_tags": ["dependency", "spawn", "fog", "branch"],
        "fog_radius": 5,
        "goal_requirements": {"activated_studs": ["upper", "gate", "tail", "middle", "lower"]},
        "design_contract": {
            "success_trigger": "land_on_diamond_socket",
            "primary_blocker": "five required studs create a support chain under fog; the gate and tail clicks must be made while the shell is safely held on the upper support",
            "dependencies": ["click upper support", "cross right", "click gate support", "click tail support", "click middle support", "route left under fog", "click lower support", "cross right to the socket"],
            "feedback": "each dependency adds visible green support cells, including small gate/tail markers and two red spawn wells marking unsafe lanes",
            "bypass_guard": "the final socket lies under three danger bands and all required gate, tail, and band supports are visibly drawn before the final descent",
        },
    },
    7: {
        "layout": [
            "################",
            "#..............#",
            "#.........#....#",
            "#..............#",
            "#.....XXXXXXXX.#",
            "#..............#",
            "#.#............#",
            "#..............#",
            "#..XXXXXXXX....#",
            "#..............#",
            "#............#.#",
            "#..............#",
            "#....XXXXXXXXX.#",
            "#..............#",
            "#..............#",
            "################",
        ],
        "player_start": (1, 12),
        "goal": (13, 3),
        "studs": {
            "upper": {"coord": (2, 2), "pads": [(4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13)]},
            "gate": {"coord": (2, 13), "pads": [(3, 2), (4, 2)]},
            "middle": {"coord": (6, 13), "pads": [(8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10)]},
            "tail": {"coord": (11, 13), "pads": [(14, 3), (14, 4)]},
            "lower": {"coord": (10, 2), "pads": [(12, 5), (12, 6), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12), (12, 13)]},
        },
        "spawn_wells": [(1, 1), (1, 8), (1, 14)],
        "spawn_period": 50,
        "spawn_phase": 0,
        "initial_spawns": [],
        "budget": 50,
        "active_tags": ["dependency", "spawn", "fog", "branch"],
        "fog_radius": 4,
        "goal_requirements": {"activated_studs": ["upper", "gate", "middle", "tail", "lower"]},
        "design_contract": {
            "success_trigger": "land_on_diamond_socket",
            "primary_blocker": "three spawn wells and heavy fog frame a final leftward route; five supports must be clicked in a planned order while the shell is held on safe ledges",
            "dependencies": ["click upper support", "click gate marker before leaving the upper support", "cross left", "click middle support", "cross right", "click tail marker while held", "click lower support", "cross left to the socket"],
            "feedback": "fog clears locally, red spawn wells mark danger columns, and each clicked stud draws green supports over the required bands",
            "bypass_guard": "the socket is below every danger band and completion requires all five visible support groups to be active",
        },
    }


}

DIRS = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}


def _inside(r, c):
    return 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE


def _active_pad_cells(h_t):
    level = LEVELS[h_t["level"]]
    cells = set()
    for sid in h_t.get("activated_studs", []):
        if sid in level.get("studs", {}):
            cells.update(tuple(p) for p in level["studs"][sid]["pads"])
    return cells


def _cell_char(level, r, c):
    if not _inside(r, c):
        return "#"
    return LEVELS[level]["layout"][r][c]


def _is_solid(h_t, r, c):
    if not _inside(r, c):
        return True
    if (r, c) in _active_pad_cells(h_t):
        return True
    return _cell_char(h_t["level"], r, c) == "#"


def _is_hazard(h_t, r, c):
    if (r, c) in _active_pad_cells(h_t):
        return False
    if (r, c) in set(tuple(p) for p in h_t.get("spawned", [])):
        return True
    return _cell_char(h_t["level"], r, c) == "X"


def _advance_spawns(h_t):
    level = LEVELS[h_t["level"]]
    if "spawn" not in level.get("active_tags", []):
        return
    moved = []
    for r, c in h_t.get("spawned", []):
        nr, nc = r + 1, c
        if _inside(nr, nc) and not _is_solid(h_t, nr, nc):
            moved.append((nr, nc))
    period = level.get("spawn_period", 6)
    phase = level.get("spawn_phase", 0)
    if period > 0 and h_t.get("step", 0) % period == phase:
        for wr, wc in level.get("spawn_wells", []):
            if not _is_solid(h_t, wr, wc):
                moved.append((wr, wc))
    h_t["spawned"] = moved


def _draw_entity(grid, row, col, entity_type):
    def put(r, c, color):
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            grid[r][c] = color

    if entity_type == "wall":
        put(row, col, COLORS["wall"])
    elif entity_type == "hazard":
        put(row, col, COLORS["hazard"])
        put(row - 1, col - 1, COLORS["hazard"])
        put(row + 1, col + 1, COLORS["hazard"])
    elif entity_type == "pad":
        put(row, col, COLORS["pad"])
        put(row, col - 1, COLORS["pad"])
        put(row, col + 1, COLORS["pad"])
    elif entity_type == "stud":
        put(row, col, COLORS["stud"])
        put(row - 1, col, COLORS["stud"])
        put(row + 1, col, COLORS["stud"])
        put(row, col - 1, COLORS["stud"])
        put(row, col + 1, COLORS["stud"])
    elif entity_type == "goal":
        put(row - 1, col, COLORS["goal"])
        put(row, col - 1, COLORS["goal"])
        put(row, col + 1, COLORS["goal"])
        put(row + 1, col, COLORS["goal"])
    elif entity_type == "spawn":
        put(row, col, COLORS["hazard"])
        put(row, col - 1, COLORS["hazard"])
        put(row, col + 1, COLORS["hazard"])
        put(row + 1, col, COLORS["hazard"])
    elif entity_type == "player":
        put(row, col, COLORS["player"])
        put(row - 1, col, COLORS["player"])
        put(row + 1, col, COLORS["player"])
        put(row, col - 1, COLORS["player"])
        put(row, col + 1, COLORS["player"])


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    """Deterministic history state update (DreamerV3 sequence model)."""
    base = a_t[0] if isinstance(a_t, tuple) and len(a_t) > 0 else a_t
    if base not in get_available_actions():
        return copy.deepcopy(h_t)
    if base == 0:
        return get_initial_state(h_t.get("level", 0))[0]
    if h_t.get("status") in ("complete", "broken"):
        return copy.deepcopy(h_t)

    n = copy.deepcopy(h_t)
    level = LEVELS[n["level"]]
    committed = False
    r, c = n["player"]

    if base == 6:
        if not (isinstance(a_t, tuple) and len(a_t) == 3):
            return copy.deepcopy(h_t)
        x, y = a_t[1], a_t[2]
        target = None
        for sid, spec in level.get("studs", {}).items():
            if spec["coord"] == (y, x):
                target = sid
                break
        if target is None:
            return copy.deepcopy(h_t)
        acts = list(n.get("activated_studs", []))
        if target in acts:
            acts.remove(target)
        else:
            acts.append(target)
        n["activated_studs"] = acts
        committed = True
    elif base in DIRS:
        dr, dc = DIRS[base]
        nr, nc = r + dr, c + dc
        if _is_solid(n, nr, nc):
            return copy.deepcopy(h_t)
        n["player"] = (nr, nc)
        committed = True

    if not committed:
        return copy.deepcopy(h_t)

    n["step"] += 1
    n["budget_remaining"] -= 1

    pr, pc = n["player"]
    if _is_hazard(n, pr, pc):
        n["status"] = "broken"
        n["budget_remaining"] = 0
        return n
    if check_level_complete(n, {}, n["level"]):
        n["status"] = "complete"
        return n

    # Gravity: every committed action advances the falling shell one row unless a drawn pad or wall supports it.
    gr, gc = pr + 1, pc
    if not _is_solid(n, gr, gc):
        n["player"] = (gr, gc)
        if _is_hazard(n, gr, gc):
            n["status"] = "broken"
            n["budget_remaining"] = 0
            return n

    if check_level_complete(n, {}, n["level"]):
        n["status"] = "complete"
        return n
    if "spawn" in level.get("active_tags", []):
        _advance_spawns(n)
        if tuple(n["player"]) in set(tuple(p) for p in n.get("spawned", [])):
            n["status"] = "broken"
            n["budget_remaining"] = 0
            return n
    if n["budget_remaining"] < 0:
        n["status"] = "broken"
    return n


def predict(h_t: dict) -> dict:
    """Return minimal/empty z_t. This game is fully deterministic."""
    return {}


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    """Check if the current level's goal has been achieved."""
    if h_t.get("level") != level or h_t.get("status") == "broken":
        return False
    req = LEVELS[level].get("goal_requirements", {})
    active = set(h_t.get("activated_studs", []))
    for sid in req.get("activated_studs", []):
        if sid not in active:
            return False
    return tuple(h_t.get("player")) == tuple(LEVELS[level]["goal"])


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    """Render the current state as a 16x16 grid."""
    level = LEVELS[h_t["level"]]
    grid = [[BG_COLOR for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    active_pads = _active_pad_cells(h_t)

    for r, row in enumerate(level["layout"]):
        for c, ch in enumerate(row):
            if (r, c) in active_pads:
                continue
            if ch == "#":
                _draw_entity(grid, r, c, "wall")
            elif ch == "X":
                _draw_entity(grid, r, c, "hazard")

    for sr, sc in level.get("spawn_wells", []):
        _draw_entity(grid, sr, sc, "spawn")
    for sr, sc in h_t.get("spawned", []):
        _draw_entity(grid, sr, sc, "hazard")

    _draw_entity(grid, level["goal"][0], level["goal"][1], "goal")
    for sid, spec in level.get("studs", {}).items():
        _draw_entity(grid, spec["coord"][0], spec["coord"][1], "stud")
        if sid in h_t.get("activated_studs", []):
            for pr, pc in spec["pads"]:
                _draw_entity(grid, pr, pc, "pad")
        else:
            # tiny yellow remote markers at the controlled cells so click effects are visible before use
            for pr, pc in spec["pads"]:
                if 0 <= pr < GRID_SIZE and 0 <= pc < GRID_SIZE and grid[pr][pc] != COLORS["hazard"]:
                    grid[pr][pc] = COLORS["stud"]

    if h_t.get("status") != "broken":
        _draw_entity(grid, h_t["player"][0], h_t["player"][1], "player")

    # HUD budget pips on top row, after terrain: yellow remaining, red exhausted.
    budget = level.get("budget", 1)
    remaining = max(0, h_t.get("budget_remaining", budget))
    shown = min(GRID_SIZE, budget)
    for c in range(shown):
        grid[0][c] = COLORS["goal"] if c < remaining * shown // budget else COLORS["hazard"]

    radius = level.get("fog_radius")
    if radius is not None:
        pr, pc = h_t["player"]
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if abs(r - pr) + abs(c - pc) > radius:
                    grid[r][c] = COLORS["fog"]
    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    """Get the initial (h_t, z_t) for a given level."""
    cfg = LEVELS[level]
    h_t = {
        "level": level,
        "step": 0,
        "player": tuple(cfg["player_start"]),
        "activated_studs": [],
        "budget_remaining": cfg["budget"],
        "status": "playing",
        "spawned": [tuple(p) for p in cfg.get("initial_spawns", [])],
    }
    return h_t, predict(h_t)


def get_available_actions() -> list[int]:
    """Return available action integers for this game."""
    return [0, 1, 2, 3, 4, 6]


def solve_level(level: int) -> list:
    """Return a fixed sequence of actions that solves this level."""
    if level == 0:
        return [
            (6, 2, 2),  # draw upper lawn over first danger row
            2,          # dive to the upper fork
            4, 4,       # cross the upper ledge and drop into the right chute
            (6, 12, 7), # draw lower lawn ledge
            4,          # enter the lower ledge approach
            2,          # dive onto the supported row above the lower danger
            4, 4, 4,    # traverse the drawn lower ledge, then leave it
            2, 2,       # final descent into the diamond socket
        ]
    if level == 1:
        return [
            (6, 2, 2),
            2,
            4, 4, 4, 4, 4, 4, 4, 4,
            (6, 13, 6),
            2,
            3, 3, 3, 3, 3, 3, 3,
            (6, 2, 10),
            2,
            4, 4, 4, 4, 4, 4, 4,
            2,
        ]
    if level == 2:
        return [
            (6, 13, 2),
            2,
            3, 3, 3, 3, 3, 3,
            (6, 2, 6),
            2,
            4, 4, 4, 4, 4,
            (6, 13, 10),
            2,
            3, 3, 3, 3, 3, 3, 3,
            2,
        ]
    if level == 3:
        return [
            (6, 13, 2),
            2,
            4, 4, 4, 4, 4, 4, 4, 4,
            (6, 2, 6),
            2,
            3, 3, 3, 3, 3, 3, 3, 3,
            (6, 13, 10),
            2,
            4, 4, 4, 4, 4, 4, 4,
            2,
        ]
    if level == 4:
        return [
            (6, 13, 2),
            2,
            4, 4, 4, 4, 4, 4, 4,
            (6, 2, 11),
            4,
            (6, 2, 6),
            2,
            3, 3, 3, 3, 3, 3, 3, 3,
            (6, 13, 10),
            2,
            4, 4, 4, 4, 4, 4, 4, 4,
            2,
        ]
    if level == 5:
        return [
            (6, 2, 2),
            2,
            3, 3, 3, 3, 3, 3, 3,
            (6, 13, 6),
            2,
            4, 4, 4, 4, 4, 4,
            (6, 2, 10),
            (6, 13, 11),
            2,
            3, 3, 3, 3, 3, 3, 3, 3,
            2,
        ]
    if level == 6:
        return [
            (6, 13, 2),
            2,
            4, 4, 4, 4, 4, 4, 4,
            (6, 2, 2),
            (6, 2, 11),
            4,
            (6, 2, 6),
            2,
            3, 3, 3, 3, 3, 3, 3, 3,
            (6, 13, 10),
            2,
            4, 4, 4, 4, 4, 4, 4, 4,
            2,
        ]
    if level == 7:
        return [
            (6, 2, 2),
            (6, 13, 2),
            2,
            3, 3, 3, 3, 3, 3, 3,
            (6, 13, 6),
            2,
            4, 4, 4, 4, 4, 4,
            (6, 13, 11),
            (6, 2, 10),
            2,
            3, 3, 3, 3, 3, 3, 3, 3,
            2,
        ]
    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Dl4827(_FunctionalArcGame):
    GAME_ID = "dl4827-b8768101"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
