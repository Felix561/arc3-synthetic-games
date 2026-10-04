# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the cc2048/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy

BG_COLOR = 3
TILE = 4
GRID_SIZE = 32

COLORS = {
    "bg": 3,
    "floor": 2,
    "wall": 1,
    "wall_edge": 5,
    "player": 5,
    "egg": 0,
    "mark": 12,
    "zone": 12,
    "pad": 1,
    "exit": 0,
    "closed": 5,
}

LEVELS = {
    0: {
        "layout": [
            "########",
            "#......#",
            "#..#...#",
            "#..#...#",
            "#..#...#",
            "#......#",
            "#......#",
            "########",
        ],
        "player_start": (3, 1),
        "eggs": {
            "plain": {"pos": (4, 1), "mark": "gray", "zone": (6, 1), "pad": (5, 1)},
            "gold": {"pos": (1, 4), "mark": "orange", "zone": (1, 6), "pad": (2, 6)},
        },
        "zones": {"plain": (6, 1), "gold": (1, 6)},
        "pads": {"plain": (5, 1), "gold": (2, 6)},
        "exit": (6, 6),
        "budget": 32,
        "active_tags": [],
        "fog_radius": None,
        "goal_requirements": {"required_items": ["plain", "gold"]},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "exit hatch is physically closed until both sorted eggs are crunched by their matching zones",
            "dependencies": ["push plain egg to lower-left crunch zone", "step on lower detector pad", "push gold-marked egg to upper-right crunch zone", "step on upper detector pad"],
            "feedback": "each egg disappears from its orange crunch zone after the matching detector pad is stepped on; the hatch changes from barred black to white ring",
            "bypass_guard": "transition blocks movement onto the exit tile until every required item/egg is crunched",
        },
    },
    1: {
        "layout": [
            "########",
            "#......#",
            "#......#",
            "#......#",
            "#......#",
            "#......#",
            "#......#",
            "########",
        ],
        "player_start": (4, 3),
        "eggs": {
            "plain": {"pos": (5, 1), "mark": "gray", "zone": (6, 1), "pad": (5, 2)},
            "gold": {"pos": (1, 2), "mark": "orange", "zone": (1, 6), "pad": (2, 6)},
            "heavy": {"pos": (3, 6), "mark": "black", "zone": (6, 6), "pad": (5, 6)},
        },
        "zones": {"plain": (6, 1), "gold": (1, 6), "heavy": (6, 6)},
        "pads": {"plain": (5, 2), "gold": (2, 6), "heavy": (5, 6)},
        "exit": (6, 5),
        "budget": 35,
        "active_tags": ["extra_egg"],
        "fog_radius": None,
        "goal_requirements": {"required_items": ["plain", "gold", "heavy"]},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "exit hatch is closed until three differently marked eggs are sorted and crunched",
            "dependencies": ["sort plain egg into the lower-left crunch zone", "trigger the plain detector", "sort gold egg across the upper lane", "trigger the gold detector", "push heavy egg down into the lower-right crunch zone", "trigger the heavy detector"],
            "feedback": "each correctly sorted egg disappears when its matching detector is stepped on; the exit ring opens only after all three are gone",
            "bypass_guard": "movement onto the exit tile is blocked until inventory contains all three crunched egg ids",
        },
    },
    2: {
        "layout": [
            "########",
            "#......#",
            "#..#...#",
            "#..#...#",
            "#......#",
            "#...#..#",
            "#......#",
            "########",
        ],
        "player_start": (4, 4),
        "eggs": {
            "plain": {"pos": (5, 2), "mark": "gray", "zone": (6, 2), "pad": (5, 1)},
            "gold": {"pos": (1, 3), "mark": "orange", "zone": (1, 6), "pad": (2, 6)},
            "heavy": {"pos": (3, 5), "mark": "black", "zone": (6, 5), "pad": (5, 5)},
        },
        "zones": {"plain": (6, 2), "gold": (1, 6), "heavy": (6, 5)},
        "pads": {"plain": (5, 1), "gold": (2, 6), "heavy": (5, 5)},
        "exit": (6, 6),
        "budget": 30,
        "active_tags": ["extra_egg", "branch_walls"],
        "fog_radius": None,
        "goal_requirements": {"required_items": ["plain", "gold", "heavy"]},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "internal wall islands split the arena so the three eggs must be sorted from three different approach sides",
            "dependencies": ["clear the lower-left plain egg before the left lane becomes a dead end", "route to the upper lane and push the gold egg right", "trigger the gold detector", "return to the center line to push the heavy egg downward", "trigger the heavy detector and enter the opened exit"],
            "feedback": "each matching detector crunches its egg away; the opened hatch is visible after all three egg ids are in inventory",
            "bypass_guard": "the exit tile rejects movement until all three required_items have been visibly crunched",
        },
    },
    3: {
        "layout": [
            "########",
            "#......#",
            "#..#...#",
            "#..#...#",
            "#..##..#",
            "#...#..#",
            "#......#",
            "########",
        ],
        "player_start": (4, 2),
        "eggs": {
            "plain": {"pos": (5, 2), "mark": "gray", "zone": (6, 2), "pad": (5, 1)},
            "drop": {"pos": (4, 1), "mark": "split", "zone": (1, 1), "pad": (2, 2)},
            "gold": {"pos": (1, 2), "mark": "orange", "zone": (1, 6), "pad": (2, 6)},
            "heavy": {"pos": (3, 6), "mark": "black", "zone": (6, 6), "pad": (5, 5)},
        },
        "zones": {"plain": (6, 2), "drop": (1, 1), "gold": (1, 6), "heavy": (6, 6)},
        "pads": {"plain": (5, 1), "drop": (2, 2), "gold": (2, 6), "heavy": (5, 5)},
        "exit": (6, 5),
        "budget": 31,
        "active_tags": ["extra_egg", "one_way_sort_order"],
        "fog_radius": None,
        "goal_requirements": {"required_items": ["plain", "drop", "gold", "heavy"]},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "four eggs occupy irreversible push lanes around a central wall island, and the exit is closed until all four are sorted",
            "dependencies": ["crunch the lower plain egg to open the left lane", "push the drop egg upward before leaving that lane", "use the cleared corner to push the gold egg across the top", "push the heavy egg down from the gold detector side", "trigger the heavy detector and enter the opened hatch"],
            "feedback": "each zone visibly empties when its matching detector is stepped on; the final hatch changes from barred to open after all four ids are in inventory",
            "bypass_guard": "the exit tile is adjacent but rejects movement until plain, drop, gold, and heavy have all been crunched",
        },
    },
    4: {
        "layout": [
            "########",
            "#......#",
            "#......#",
            "#..#...#",
            "#...#..#",
            "#......#",
            "#..#...#",
            "########",
        ],
        "player_start": (4, 3),
        "eggs": {
            "plain": {"pos": (5, 1), "mark": "gray", "zone": (6, 1), "pad": (5, 2)},
            "gold": {"pos": (1, 2), "mark": "orange", "zone": (1, 6), "pad": (2, 6)},
            "heavy": {"pos": (3, 6), "mark": "black", "zone": (6, 6), "pad": (5, 6)},
        },
        "zones": {"plain": (6, 1), "gold": (1, 6), "heavy": (6, 6)},
        "pads": {"plain": (5, 2), "gold": (2, 6), "heavy": (5, 6)},
        "keys": {"copper_key": (4, 1)},
        "gates": {"copper_gate": {"pos": (6, 5), "key": "copper_key"}},
        "exit": (6, 4),
        "budget": 33,
        "active_tags": ["keys", "extra_egg", "gate_route"],
        "fog_radius": None,
        "goal_requirements": {"required_items": ["plain", "gold", "heavy", "copper_key"]},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "a locked gate and closed hatch protect the final lane while three eggs still need sorting",
            "dependencies": ["collect the copper key from the left carpet lane", "sort and trigger the plain egg beside that lane", "sort and trigger the gold egg in the upper-right zone", "push and trigger the heavy egg downward", "walk through the opened gate to the exit hatch"],
            "feedback": "the key disappears into inventory, the gate becomes a pale open frame, each sorted egg vanishes from its crunch zone, and the hatch opens after all required items are visible in inventory",
            "bypass_guard": "the gate blocks its tile until copper_key is collected, and the exit rejects entry until the key and all three crunched egg ids are in inventory",
        },
    },
    5: {
        "layout": [
            "########",
            "#......#",
            "#......#",
            "#..#...#",
            "#......#",
            "#...#..#",
            "#......#",
            "########",
        ],
        "player_start": (4, 3),
        "eggs": {
            "plain": {"pos": (5, 1), "mark": "gray", "zone": (6, 1), "pad": (5, 2)},
            "gold": {"pos": (1, 2), "mark": "orange", "zone": (1, 6), "pad": (2, 6)},
            "heavy": {"pos": (3, 6), "mark": "black", "zone": (6, 6), "pad": (5, 6)},
        },
        "zones": {"plain": (6, 1), "gold": (1, 6), "heavy": (6, 6)},
        "pads": {"plain": (5, 2), "gold": (2, 6), "heavy": (5, 6)},
        "keys": {"copper_key": (4, 1), "silver_key": (2, 2)},
        "gates": {
            "silver_gate": {"pos": (2, 5), "key": "silver_key"},
            "copper_gate": {"pos": (6, 5), "key": "copper_key"}
        },
        "exit": (6, 4),
        "budget": 32,
        "active_tags": ["keys", "fog", "dual_gates"],
        "fog_radius": 4,
        "goal_requirements": {"required_items": ["plain", "gold", "heavy", "copper_key", "silver_key"]},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "two locked gates split the arena while fog hides far crunch zones until approached",
            "dependencies": ["collect copper_key while entering the left sorting lane", "crunch the plain egg", "collect silver_key on the upper approach", "pass the silver gate to trigger the gold crunch zone", "crunch the heavy egg", "pass the copper gate to reach the exit"],
            "feedback": "keys disappear into inventory, their matching gates render as open frames, and sorted eggs vanish from zones; fog reveals objects as the player approaches",
            "bypass_guard": "silver_gate blocks the gold detector route, copper_gate blocks the final exit route, and the exit rejects movement until both keys and all three egg ids are in inventory",
        },
    },
    6: {
        "layout": [
            "########",
            "#......#",
            "#..#...#",
            "#..#...#",
            "#..##..#",
            "#...#..#",
            "#......#",
            "########",
        ],
        "player_start": (4, 2),
        "eggs": {
            "plain": {"pos": (5, 2), "mark": "gray", "zone": (6, 2), "pad": (5, 1)},
            "drop": {"pos": (4, 1), "mark": "split", "zone": (1, 1), "pad": (2, 2)},
            "gold": {"pos": (1, 2), "mark": "orange", "zone": (1, 6), "pad": (2, 6)},
            "heavy": {"pos": (3, 6), "mark": "black", "zone": (6, 6), "pad": (5, 5)},
        },
        "zones": {"plain": (6, 2), "drop": (1, 1), "gold": (1, 6), "heavy": (6, 6)},
        "pads": {"plain": (5, 1), "drop": (2, 2), "gold": (2, 6), "heavy": (5, 5)},
        "keys": {"copper_key": (2, 1), "silver_key": (5, 6)},
        "gates": {
            "copper_gate": {"pos": (6, 4), "key": "copper_key"},
            "silver_gate": {"pos": (6, 5), "key": "silver_key"}
        },
        "exit": (6, 4),
        "budget": 38,
        "active_tags": ["keys", "fog", "four_eggs", "gate_chain"],
        "fog_radius": 4,
        "goal_requirements": {"required_items": ["plain", "drop", "gold", "heavy", "copper_key", "silver_key"]},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "four sorted crunches and two key-gated floor cells must be resolved before the terminal hatch can be entered",
            "dependencies": ["sort the plain egg first to clear the lower-left lane", "push the drop egg upward and collect copper_key on the return route", "sort the gold egg across the top lane", "push the heavy egg into its lower-right zone", "collect silver_key at the heavy detector route", "cross both opened gates to enter the hatch"],
            "feedback": "fog reveals each lane locally, eggs vanish when crunched, keys vanish when collected, and gate bars become open frames after their keys are carried",
            "bypass_guard": "copper_gate and silver_gate occupy the only final approach and the exit rejects entry until all four egg ids plus both keys are in inventory",
        },
    },
    7: {
        "layout": [
            "########",
            "#......#",
            "#...#..#",
            "#...#..#",
            "#..##..#",
            "#..#...#",
            "#......#",
            "########",
        ],
        "player_start": (4, 5),
        "eggs": {
            "plain": {"pos": (5, 5), "mark": "gray", "zone": (6, 5), "pad": (5, 6)},
            "drop": {"pos": (4, 6), "mark": "split", "zone": (1, 6), "pad": (2, 5)},
            "gold": {"pos": (1, 5), "mark": "orange", "zone": (1, 1), "pad": (2, 1)},
            "heavy": {"pos": (3, 1), "mark": "black", "zone": (6, 1), "pad": (5, 2)},
        },
        "zones": {"plain": (6, 5), "drop": (1, 6), "gold": (1, 1), "heavy": (6, 1)},
        "pads": {"plain": (5, 6), "drop": (2, 5), "gold": (2, 1), "heavy": (5, 2)},
        "keys": {"iron_key": (2, 5), "copper_key": (2, 6), "silver_key": (5, 1)},
        "gates": {
            "silver_gate": {"pos": (6, 2), "key": "silver_key"},
            "copper_gate": {"pos": (6, 3), "key": "copper_key"},
            "iron_gate": {"pos": (6, 4), "key": "iron_key"}
        },
        "exit": (6, 4),
        "budget": 34,
        "active_tags": ["keys", "fog", "four_eggs", "triple_gate_chain"],
        "fog_radius": 4,
        "goal_requirements": {"required_items": ["plain", "drop", "gold", "heavy", "iron_key", "copper_key", "silver_key"]},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "three keyed gates occupy the only final corridor and four egg variants must be sorted under fog before those gates matter",
            "dependencies": ["push the plain egg into the lower-right zone and trigger its pad", "drive the drop egg upward and collect the iron key on its detector pad", "collect copper_key while returning from the drop lane", "push the gold egg left into its matching zone and trigger it", "push the heavy egg down into its zone and collect silver_key", "cross the silver, copper, and iron gates to enter the exit"],
            "feedback": "each sorted egg disappears from its ring, keys vanish into inventory, each matching gate renders open once its key is carried, and fog reveals the final corridor only near the end",
            "bypass_guard": "the final corridor is blocked by all three gates, and the exit tile itself rejects entry until every required egg id and key id is in inventory",
        },
    }
}

DIRS = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}


def _requirements_met(h_t, level):
    req = LEVELS[level].get("goal_requirements", {})
    crunched = set(h_t.get("crunched", []))
    for egg_id in req.get("required_crunched", []):
        if egg_id not in crunched:
            return False
    inv = set(h_t.get("inventory", []))
    for item_id in req.get("required_items", []):
        if item_id not in inv:
            return False
    return True


def _in_bounds(r, c, level):
    layout = LEVELS[level]["layout"]
    return 0 <= r < len(layout) and 0 <= c < len(layout[0])


def _egg_at(h_t, r, c):
    for egg_id, pos in h_t.get("eggs", {}).items():
        if pos is not None and tuple(pos) == (r, c):
            return egg_id
    return None


def _is_wall(level, r, c):
    return (not _in_bounds(r, c, level)) or LEVELS[level]["layout"][r][c] == "#"


def _is_open_for_move(h_t, r, c):
    level = h_t["level"]
    if _is_wall(level, r, c):
        return False
    for gate in LEVELS[level].get("gates", {}).values():
        if (r, c) == tuple(gate["pos"]) and gate.get("key") not in h_t.get("inventory", []):
            return False
    if (r, c) == tuple(LEVELS[level]["exit"]) and not _requirements_met(h_t, level):
        return False
    return True


def _draw_tile(grid, tr, tc, color):
    r0, c0 = tr * TILE, tc * TILE
    for rr in range(r0, r0 + TILE):
        for cc in range(c0, c0 + TILE):
            grid[rr][cc] = color


def _draw_entity(grid, row, col, entity_type):
    r0, c0 = row * TILE, col * TILE
    if entity_type == "floor":
        _draw_tile(grid, row, col, COLORS["floor"])
        grid[r0 + 1][c0 + 1] = BG_COLOR
        grid[r0 + 2][c0 + 2] = BG_COLOR
    elif entity_type == "wall":
        _draw_tile(grid, row, col, COLORS["wall"])
        for i in range(TILE):
            grid[r0][c0 + i] = COLORS["wall_edge"]
            grid[r0 + TILE - 1][c0 + i] = COLORS["wall_edge"]
            grid[r0 + i][c0] = COLORS["wall_edge"]
            grid[r0 + i][c0 + TILE - 1] = COLORS["wall_edge"]
    elif entity_type.startswith("zone"):
        for i in range(TILE):
            grid[r0][c0 + i] = COLORS["zone"]
            grid[r0 + TILE - 1][c0 + i] = COLORS["zone"]
            grid[r0 + i][c0] = COLORS["zone"]
            grid[r0 + i][c0 + TILE - 1] = COLORS["zone"]
        if entity_type == "zone_plain":
            grid[r0 + 1][c0 + 1] = COLORS["egg"]
        elif entity_type == "zone_drop":
            grid[r0 + 1][c0 + 1] = COLORS["egg"]
            grid[r0 + 1][c0 + 2] = COLORS["closed"]
            grid[r0 + 2][c0 + 1] = COLORS["closed"]
        elif entity_type == "zone_heavy":
            grid[r0 + 1][c0 + 1] = COLORS["closed"]
            grid[r0 + 2][c0 + 2] = COLORS["closed"]
        else:
            grid[r0 + 1][c0 + 2] = COLORS["mark"]
            grid[r0 + 2][c0 + 1] = COLORS["mark"]
    elif entity_type.startswith("pad"):
        for rr in range(r0, r0 + TILE):
            for cc in range(c0, c0 + TILE):
                if (rr + cc) % 2 == 0:
                    grid[rr][cc] = COLORS["pad"]
        grid[r0 + 1][c0 + 1] = COLORS["mark"]
        grid[r0 + 1][c0 + 2] = COLORS["mark"]
        grid[r0 + 2][c0 + 1] = COLORS["mark"]
        grid[r0 + 2][c0 + 2] = COLORS["mark"]
    elif entity_type == "exit_closed":
        for i in range(TILE):
            grid[r0][c0 + i] = COLORS["exit"]
            grid[r0 + TILE - 1][c0 + i] = COLORS["exit"]
            grid[r0 + i][c0] = COLORS["exit"]
            grid[r0 + i][c0 + TILE - 1] = COLORS["exit"]
            grid[r0 + i][c0 + i] = COLORS["closed"]
    elif entity_type == "exit_open":
        for i in range(TILE):
            grid[r0][c0 + i] = COLORS["exit"]
            grid[r0 + TILE - 1][c0 + i] = COLORS["exit"]
            grid[r0 + i][c0] = COLORS["exit"]
            grid[r0 + i][c0 + TILE - 1] = COLORS["exit"]
        grid[r0 + 1][c0 + 1] = COLORS["closed"]
        grid[r0 + 1][c0 + 2] = COLORS["closed"]
    elif entity_type.startswith("egg"):
        grid[r0 + 1][c0 + 1] = COLORS["egg"]
        grid[r0 + 1][c0 + 2] = COLORS["egg"]
        grid[r0 + 2][c0 + 1] = COLORS["egg"]
        grid[r0 + 2][c0 + 2] = COLORS["egg"]
        if entity_type == "egg_plain":
            grid[r0 + 2][c0 + 2] = COLORS["floor"]
        elif entity_type == "egg_drop":
            grid[r0 + 1][c0 + 1] = COLORS["closed"]
            grid[r0 + 1][c0 + 2] = COLORS["egg"]
            grid[r0 + 2][c0 + 1] = COLORS["egg"]
            grid[r0 + 2][c0 + 2] = COLORS["closed"]
        elif entity_type == "egg_heavy":
            grid[r0 + 1][c0 + 1] = COLORS["closed"]
            grid[r0 + 2][c0 + 2] = COLORS["closed"]
        else:
            grid[r0 + 1][c0 + 2] = COLORS["mark"]
            grid[r0 + 2][c0 + 1] = COLORS["mark"]
    elif entity_type == "key":
        grid[r0 + 1][c0 + 1] = COLORS["mark"]
        grid[r0 + 1][c0 + 2] = COLORS["mark"]
        grid[r0 + 2][c0 + 1] = COLORS["exit"]
        grid[r0 + 2][c0 + 2] = COLORS["mark"]
    elif entity_type == "gate_closed":
        for i in range(TILE):
            grid[r0 + i][c0] = COLORS["closed"]
            grid[r0 + i][c0 + 2] = COLORS["closed"]
            grid[r0 + i][c0 + 3] = COLORS["wall"]
        grid[r0 + 1][c0 + 1] = COLORS["mark"]
        grid[r0 + 2][c0 + 1] = COLORS["mark"]
    elif entity_type == "gate_open":
        for i in range(TILE):
            grid[r0][c0 + i] = COLORS["wall"]
            grid[r0 + TILE - 1][c0 + i] = COLORS["wall"]
        grid[r0 + 1][c0 + 1] = COLORS["floor"]
        grid[r0 + 2][c0 + 2] = COLORS["floor"]
    elif entity_type == "player":
        grid[r0 + 1][c0 + 1] = COLORS["player"]
        grid[r0 + 1][c0 + 2] = COLORS["player"]
        grid[r0 + 2][c0 + 1] = COLORS["player"]
        grid[r0 + 2][c0 + 2] = COLORS["player"]
        grid[r0 + 1][c0 + 1] = COLORS["exit"]
        grid[r0 + 2][c0 + 2] = COLORS["exit"]


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    """Deterministic history state update."""
    if isinstance(a_t, tuple):
        base = a_t[0]
    else:
        base = a_t
    if base not in get_available_actions():
        return copy.deepcopy(h_t)
    if base == 0:
        return get_initial_state(h_t.get("level", 0))[0]
    if base not in DIRS:
        return copy.deepcopy(h_t)

    h = copy.deepcopy(h_t)
    if h.get("complete") or h.get("budget", 0) <= 0:
        return h

    level = h["level"]
    active_tags = LEVELS[level].get("active_tags", [])
    dr, dc = DIRS[base]
    nr, nc = h["player_r"] + dr, h["player_c"] + dc
    if not _is_open_for_move(h, nr, nc):
        return h

    pushed = _egg_at(h, nr, nc)
    if pushed is not None:
        br, bc = nr + dr, nc + dc
        if (not _is_open_for_move(h, br, bc)) or _egg_at(h, br, bc) is not None:
            return h
        h["eggs"][pushed] = (br, bc)

    h["player_r"], h["player_c"] = nr, nc

    # Keys are progressive inventory items; only active on tagged levels.
    if "keys" in active_tags:
        for key_id, pos in list(h.get("keys", {}).items()):
            if pos is not None and (nr, nc) == tuple(pos):
                h["keys"][key_id] = None
                if key_id not in h["inventory"]:
                    h["inventory"].append(key_id)

    # Detector pads trigger their own area-effect crunch zone.
    for egg_id, pad in LEVELS[level]["pads"].items():
        if (nr, nc) == tuple(pad):
            zone = tuple(LEVELS[level]["zones"][egg_id])
            if h["eggs"].get(egg_id) is not None and tuple(h["eggs"][egg_id]) == zone:
                h["eggs"][egg_id] = None
                if egg_id not in h["crunched"]:
                    h["crunched"].append(egg_id)
                if egg_id not in h["inventory"]:
                    h["inventory"].append(egg_id)

    h["step"] += 1
    h["budget"] -= 1
    if check_level_complete(h, {}, level):
        h["complete"] = True
    return h


def predict(h_t: dict) -> dict:
    """Return minimal derived state for deterministic game."""
    return {}


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    """True when player enters exit after visible sorting requirements are met."""
    if h_t.get("level") != level:
        return False
    if (h_t.get("player_r"), h_t.get("player_c")) != tuple(LEVELS[level]["exit"]):
        return False
    return _requirements_met(h_t, level)


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    """Render the current state as a 32x32 grid."""
    level = h_t["level"]
    lev = LEVELS[level]
    grid = [[BG_COLOR for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    for r, row in enumerate(lev["layout"]):
        for c, ch in enumerate(row):
            if ch == "#":
                _draw_entity(grid, r, c, "wall")
            else:
                _draw_entity(grid, r, c, "floor")

    for egg_id, zpos in lev["zones"].items():
        _draw_entity(grid, zpos[0], zpos[1], "zone_" + egg_id)
    for egg_id, ppos in lev["pads"].items():
        _draw_entity(grid, ppos[0], ppos[1], "pad_" + egg_id)

    for gate in lev.get("gates", {}).values():
        gr, gc = gate["pos"]
        gtype = "gate_open" if gate.get("key") in h_t.get("inventory", []) else "gate_closed"
        _draw_entity(grid, gr, gc, gtype)

    if "keys" in lev.get("active_tags", []):
        for key_id, pos in h_t.get("keys", {}).items():
            if pos is not None:
                _draw_entity(grid, pos[0], pos[1], "key")

    exit_type = "exit_open" if _requirements_met(h_t, level) else "exit_closed"
    er, ec = lev["exit"]
    _draw_entity(grid, er, ec, exit_type)

    for egg_id, pos in h_t.get("eggs", {}).items():
        if pos is not None:
            _draw_entity(grid, pos[0], pos[1], "egg_" + egg_id)

    _draw_entity(grid, h_t["player_r"], h_t["player_c"], "player")

    max_budget = max(1, lev["budget"])
    lit = int((max(0, h_t.get("budget", 0)) * GRID_SIZE) / max_budget)
    for c in range(GRID_SIZE):
        if c < lit:
            grid[0][c] = COLORS["mark"]

    fog = lev.get("fog_radius")
    if fog is not None:
        pr, pc = h_t["player_r"] * TILE + TILE // 2, h_t["player_c"] * TILE + TILE // 2
        radius = fog * TILE
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if abs(r - pr) + abs(c - pc) > radius:
                    grid[r][c] = BG_COLOR
    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    """Get the initial state for a level."""
    lev = LEVELS[level]
    eggs = {egg_id: tuple(info["pos"]) for egg_id, info in lev["eggs"].items()}
    keys = {key_id: tuple(pos) for key_id, pos in lev.get("keys", {}).items()}
    pr, pc = lev["player_start"]
    h_t = {
        "level": level,
        "step": 0,
        "budget": lev["budget"],
        "player_r": pr,
        "player_c": pc,
        "eggs": eggs,
        "keys": keys,
        "crunched": [],
        "inventory": [],
        "complete": False,
    }
    return h_t, predict(h_t)


def get_available_actions() -> list[int]:
    """Return available action integers: reset and four directions."""
    return [0, 1, 2, 3, 4]


def solve_level(level: int) -> list:
    """Return a fixed action sequence that solves this level."""
    if level == 0:
        return [2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 2, 4, 2, 2, 2, 2]
    if level == 1:
        return [3, 3, 2, 4, 1, 1, 1, 3, 1, 4, 4, 4, 4, 2, 4, 2, 2, 2, 3, 2]
    if level == 2:
        return [3, 3, 2, 3, 1, 1, 1, 1, 4, 4, 4, 4, 2, 4, 3, 2, 2, 2, 2, 4]
    if level == 3:
        return [2, 3, 1, 1, 1, 4, 3, 1, 4, 4, 4, 4, 2, 4, 2, 2, 2, 3, 2]
    if level == 4:
        return [3, 3, 2, 4, 1, 1, 1, 3, 1, 4, 4, 4, 4, 2, 4, 2, 2, 2, 3, 2, 3]
    if level == 5:
        return [3, 3, 2, 4, 1, 1, 1, 3, 1, 4, 4, 4, 4, 2, 4, 2, 2, 2, 3, 2, 3]
    if level == 6:
        return [2, 3, 1, 1, 1, 4, 3, 1, 4, 4, 4, 4, 2, 4, 2, 2, 2, 3, 2, 3]
    if level == 7:
        return [2, 4, 1, 1, 1, 3, 4, 1, 3, 3, 3, 3, 2, 3, 2, 2, 2, 4, 2, 4, 4]
    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Cc2048(_FunctionalArcGame):
    GAME_ID = "cc2048-f080c4af"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
