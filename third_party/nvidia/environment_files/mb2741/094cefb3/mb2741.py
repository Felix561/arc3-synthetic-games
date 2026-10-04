# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the mb2741/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy

BG_COLOR = 0
CELL = 5
BOARD_TOP = 1
BOARD_LEFT = 1
GRID_SIZE = 32

COLORS = {
    "bg": 0,
    "floor": 10,
    "player": 6,
    "player_mark": 7,
    "wall": 15,
    "cracked": 12,
    "pylon": 11,
    "pylon_core": 6,
    "pulse": 7,
    "exit": 9,
    "spent": 14,
    "key": 14,
}

# 6x6 tile arena. # wall, . floor, C cracked front, P pylon, E exit, S start.
LEVELS = {
    0: {
        "layout": [
            "######",
            "#S.P.#",
            "#C#.##",
            "#...##",
            "#.PCE#",
            "######",
        ],
        "player_start": (1, 1),
        "exit": (4, 4),
        "pylons": {"A": (1, 3), "B": (4, 2)},
        "pylon_order": ["A", "B"],
        "cracked": [(2, 1), (4, 3)],
        "pulse_targets": {
            "A": [(2, 1)],
            "B": [(4, 3)],
        },
        "pulse_shapes": {
            "A": [(1, 3), (1, 4), (2, 1)],
            "B": [(4, 2), (4, 3), (3, 2)],
        },
        "budget": 22,
        "active_tags": [],
        "goal_requirements": {"triggered_pylons": ["A", "B"], "cleared_cracks": 2},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "two cracked brick fronts block the only route to the exit",
            "dependencies": ["trigger north clap pylon", "route to south clap pylon", "clear both cracked fronts", "enter exit"],
            "feedback": "each pylon turns green and its targeted cracked front disappears; a light-pink pulse is shown briefly",
            "bypass_guard": "the exit corridor is physically sealed until both cracked fronts are removed",
        },
    },
    1: {
        "layout": [
            "######",
            "#S..P#",
            "#.##K#",
            "#P..C#",
            "####E#",
            "######",
        ],
        "player_start": (1, 1),
        "exit": (4, 4),
        "pylons": {"A": (1, 4), "B": (3, 1)},
        "pylon_order": ["A", "B"],
        "cracked": [(2, 1), (2, 4), (3, 4)],
        "keys": {"moon": (2, 4)},
        "pulse_targets": {
            "A": [(2, 1), (2, 4)],
            "B": [(3, 4)],
        },
        "pulse_shapes": {
            "A": [(1, 3), (1, 4), (2, 1), (2, 4)],
            "B": [(3, 1), (3, 2), (3, 3), (3, 4), (2, 1), (4, 1)],
        },
        "budget": 25,
        "active_tags": ["keys"],
        "goal_requirements": {"triggered_pylons": ["A", "B"], "cleared_cracks": 3, "key_collected": True},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "cracked fronts seal the lower pylon approach, the moon key, and the exit lane",
            "dependencies": ["trigger upper clap pylon to open the key and lower approach", "collect moon key from the opened front", "backtrack to lower clap pylon", "clear exit front", "enter exit"],
            "feedback": "the key appears on the opened front, collected state is shown by its disappearance, pylons turn green, and cracks disappear",
            "bypass_guard": "the lower pylon and exit lane are both physically sealed by cracked fronts until the upper pylon opens the prerequisite route and the lower pylon clears the final front",
        },
    },
    2: {
        "layout": [
            "######",
            "#S.P.#",
            "#.#C.#",
            "#.CP##",
            "###CE#",
            "######",
        ],
        "player_start": (1, 1),
        "exit": (4, 4),
        "pylons": {"A": (1, 3), "B": (3, 3)},
        "pylon_order": ["A", "B"],
        "cracked": [(2, 3), (3, 2), (4, 3)],
        "pulse_targets": {
            "A": [(2, 3), (3, 2)],
            "B": [(4, 3)],
        },
        "pulse_shapes": {
            "A": [(2, 3), (3, 2)],
            "B": [(3, 2), (4, 3)],
        },
        "spread_steps": {
            "A": [[(2, 3)], [(3, 2)]],
            "B": [[(3, 2)], [(4, 3)]],
        },
        "budget": 24,
        "active_tags": ["spread"],
        "goal_requirements": {"triggered_pylons": ["A", "B"], "cleared_cracks": 3},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "spread pulses must travel over two committed moves before the approach and exit fronts open",
            "dependencies": ["trigger upper spread pylon", "route around while spread opens lower approach", "trigger lower spread pylon", "step aside while spread opens final front", "enter exit"],
            "feedback": "light-pink spread cells appear one wave-step at a time; cracked fronts vanish only when the wave reaches them",
            "bypass_guard": "the lower pylon approach and the exit approach are physically blocked by cracked fronts until their spread waves arrive",
        },
    },
    3: {
        "layout": [
            "######",
            "#ECP.#",
            "####C#",
            "#P#.P#",
            "#S.C.#",
            "######",
        ],
        "player_start": (4, 1),
        "exit": (1, 1),
        "pylons": {"A": (3, 1), "B": (3, 4), "C": (1, 3)},
        "pylon_order": ["A", "B", "C"],
        "cracked": [(4, 3), (2, 4), (1, 2)],
        "pulse_targets": {
            "A": [(4, 3)],
            "B": [(3, 2), (2, 4)],
            "C": [(1, 2)],
        },
        "pulse_shapes": {
            "A": [(4, 3)],
            "B": [(3, 2), (2, 4)],
            "C": [(1, 2)],
        },
        "spread_steps": {
            "A": [[(4, 3)]],
            "B": [[(3, 2), (2, 4)]],
            "C": [[(1, 2)]],
        },
        "budget": 42,
        "active_tags": ["spread"],
        "goal_requirements": {"triggered_pylons": ["A", "B", "C"], "cleared_cracks": 3},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "three opposing spread fronts seal the bottom crossing, the upper climb, and the exit lip",
            "dependencies": ["trigger left pylon to open the bottom crossing", "route to the right pylon to open the upper climb", "route to the upper pylon to open the exit lip", "enter exit"],
            "feedback": "each spread wave appears as a light-pink cell, removes one cracked front, and turns its pylon green",
            "bypass_guard": "the exit is only reachable through the final cracked lip at row 1 column 2, which only the upper pylon can clear after the first two routes are opened",
        },
    },
    4: {
        "layout": [
            "######",
            "#S.P##",
            "#C#.P#",
            "#..C##",
            "#P#GE#",
            "######",
        ],
        "player_start": (1, 1),
        "exit": (4, 4),
        "pylons": {"A": (1, 3), "B": (4, 1), "C": (2, 4)},
        "pylon_order": ["A", "B", "C"],
        "cracked": [(2, 1), (3, 3), (4, 3)],
        "keys": {"moon": (2, 1)},
        "gates": {"moon_gate": (4, 3)},
        "pulse_targets": {
            "A": [(2, 1)],
            "B": [(3, 3)],
            "C": [(4, 3)],
        },
        "pulse_shapes": {
            "A": [(1, 3), (2, 1)],
            "B": [(4, 1), (3, 3)],
            "C": [(2, 4), (4, 3)],
        },
        "budget": 29,
        "active_tags": ["keys", "gate"],
        "goal_requirements": {"triggered_pylons": ["A", "B", "C"], "cleared_cracks": 3, "key_collected": True, "gate_open": True},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "a keyed moon gate and three cracked fronts form an ordered route to the exit",
            "dependencies": ["trigger pylon A to uncover the key", "collect the moon key to unlock the gate", "trigger pylon B to open the central turn", "trigger pylon C to clear the gate cell", "enter the exit"],
            "feedback": "the key disappears, the gate changes from closed to open, pylons turn green, and cracked fronts vanish",
            "bypass_guard": "the exit is only reachable through the gate cell at row 4 column 3; it is blocked by both the key gate and a crack until the declared subgoals are complete",
        },
    },
    5: {
        "layout": [
            "######",
            "#S.PE#",
            "#C#C##",
            "#..P.#",
            "#P.CK#",
            "######",
        ],
        "player_start": (1, 1),
        "exit": (1, 4),
        "pylons": {"A": (1, 3), "B": (4, 1), "C": (3, 3)},
        "pylon_order": ["A", "B", "C"],
        "cracked": [(2, 1), (3, 2), (4, 3), (2, 3), (1, 4)],
        "keys": {"moon": (4, 4)},
        "pulse_targets": {
            "A": [(2, 1), (4, 3)],
            "B": [(3, 2), (2, 3)],
            "C": [(1, 4)],
        },
        "pulse_shapes": {
            "A": [(2, 1), (4, 3)],
            "B": [(3, 2), (2, 3)],
            "C": [(1, 4)],
        },
        "spread_steps": {
            "A": [[(2, 1)], [(4, 3)]],
            "B": [[(3, 2), (2, 3)]],
            "C": [[(1, 4)]],
        },
        "budget": 28,
        "active_tags": ["spread", "keys"],
        "goal_requirements": {"triggered_pylons": ["A", "B", "C"], "cleared_cracks": 5, "key_collected": True},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "two-step spread opens the lower arena and key route, then later pylons open the upper climb and exit portal",
            "dependencies": ["trigger pylon A and route while its spread opens two fronts", "trigger pylon B to open the upper climb", "collect the moon key", "trigger pylon C to clear the exit portal", "enter exit"],
            "feedback": "spread cells appear one wave at a time, each cracked front vanishes when touched, the key disappears when collected, and spent pylons turn green",
            "bypass_guard": "the exit tile itself is cracked and key-locked, while the only upper approach remains cracked until pylon B has fired",
        },
    },
    6: {
        "layout": [
            "######",
            "#S.PE#",
            "#C##G#",
            "#..P.#",
            "#P.CK#",
            "######",
        ],
        "player_start": (1, 1),
        "exit": (1, 4),
        "pylons": {"A": (1, 3), "B": (4, 1), "C": (3, 3)},
        "pylon_order": ["A", "B", "C"],
        "cracked": [(2, 1), (3, 2), (4, 3), (2, 4), (1, 4)],
        "keys": {"moon": (4, 4)},
        "gates": {"moon_gate": (2, 4)},
        "pulse_targets": {
            "A": [(2, 1), (4, 3)],
            "B": [(3, 2), (2, 4)],
            "C": [(1, 4)],
        },
        "pulse_shapes": {
            "A": [(2, 1), (4, 3)],
            "B": [(3, 2), (2, 4)],
            "C": [(1, 4)],
        },
        "spread_steps": {
            "A": [[(2, 1)], [(4, 3)]],
            "B": [[(3, 2), (2, 4)]],
            "C": [[(1, 4)]],
        },
        "budget": 29,
        "active_tags": ["spread", "keys", "gate"],
        "goal_requirements": {"triggered_pylons": ["A", "B", "C"], "cleared_cracks": 5, "key_collected": True, "gate_open": True},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "a spread-cleared moon gate and cracked exit require an ordered lower-loop route",
            "dependencies": ["trigger pylon A so its spread opens the lower lane and key lane", "trigger pylon B to clear the gated climb", "collect the moon key to open the gate", "trigger pylon C to clear the exit tile", "enter exit through the opened gate"],
            "feedback": "two-step spread from A visibly opens two fronts, the key disappears and opens the gate, and later spread waves clear the climb and exit",
            "bypass_guard": "the only route to the exit passes the gated cell at row 2 column 4 and the cracked exit tile, so the key, B wave, and C wave are physically required",
        },
    },
    7: {
        "layout": [
            "######",
            "#S.PE#",
            "#C##G#",
            "#.P#P#",
            "#P.CK#",
            "######",
        ],
        "player_start": (1, 1),
        "exit": (1, 4),
        "pylons": {"A": (1, 3), "B": (4, 1), "C": (3, 2), "D": (3, 4)},
        "pylon_order": ["A", "B", "C", "D"],
        "cracked": [(2, 1), (4, 3), (2, 4), (1, 4)],
        "keys": {"moon": (4, 4)},
        "gates": {"moon_gate": (2, 4)},
        "pulse_targets": {
            "A": [(2, 1)],
            "B": [(2, 4)],
            "C": [(4, 3)],
            "D": [(1, 4)],
        },
        "pulse_shapes": {
            "A": [(1, 3), (2, 1)],
            "B": [(4, 1), (2, 4)],
            "C": [(3, 2), (4, 3)],
            "D": [(3, 4), (1, 4)],
        },
        "spread_steps": {
            "A": [[(1, 3)], [(2, 1)]],
            "B": [[(2, 4)]],
            "C": [[(3, 2)], [(4, 3)]],
            "D": [[(1, 4)]],
        },
        "budget": 30,
        "active_tags": ["spread", "keys", "gate"],
        "goal_requirements": {"triggered_pylons": ["A", "B", "C", "D"], "cleared_cracks": 4, "key_collected": True, "gate_open": True},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "four ordered spread pylons, a moon key, a gate, and a cracked exit create a serial arena-control chain",
            "dependencies": ["trigger A and step away while spread opens the descent", "trigger B to clear the gate front", "trigger C and route one step while spread opens the key front", "collect the key to open the gate", "trigger D from the key side to clear the exit", "enter the exit through the opened gate"],
            "feedback": "each spread wave is shown in light-pink, each cracked front vanishes when the wave reaches it, the key disappears, the gate opens, and every spent pylon turns green",
            "bypass_guard": "the only route to the blue exit requires the A descent, the B-cleared gate front, the C-cleared key front, the collected key, and the D-cleared exit tile; each blocker physically prevents early entry",
        },
    }
}

DIRS = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}


def _base_tile(level, r, c):
    ch = LEVELS[level]["layout"][r][c]
    return ch


def _tile_in_bounds(level, r, c):
    layout = LEVELS[level]["layout"]
    return 0 <= r < len(layout) and 0 <= c < len(layout[0])


def _requirements_satisfied(h_t, cfg):
    req = cfg.get("goal_requirements", {})
    for pid in req.get("triggered_pylons", []):
        if pid not in h_t.get("triggered_pylons", h_t.get("triggered", [])):
            return False
    if h_t.get("cleared_cracks", len(cfg.get("cracked", [])) - len(h_t.get("cracked", []))) < req.get("cleared_cracks", 0):
        return False
    if req.get("key_collected", False) and not h_t.get("key_collected", False):
        return False
    if req.get("gate_open", False) and not h_t.get("gate_open", False):
        return False
    return not h_t.get("failed", False)


def _draw_entity(grid, row, col, entity_type):
    top = BOARD_TOP + row * CELL
    left = BOARD_LEFT + col * CELL
    if entity_type == "floor":
        for y in range(top, top + CELL):
            for x in range(left, left + CELL):
                grid[y][x] = COLORS["floor"] if y in (top, top + CELL - 1) or x in (left, left + CELL - 1) else BG_COLOR
    elif entity_type == "wall":
        for y in range(top, top + CELL):
            for x in range(left, left + CELL):
                grid[y][x] = COLORS["wall"]
    elif entity_type == "cracked":
        for y in range(top, top + CELL):
            for x in range(left, left + CELL):
                grid[y][x] = COLORS["cracked"] if (y - top + x - left) % 2 == 0 else BG_COLOR
    elif entity_type == "pylon":
        for y in range(top, top + CELL):
            for x in range(left, left + CELL):
                edge = y in (top, top + CELL - 1) or x in (left, left + CELL - 1)
                grid[y][x] = COLORS["pylon"] if edge else BG_COLOR
        grid[top + 2][left + 2] = COLORS["pylon_core"]
        grid[top + 1][left + 2] = COLORS["pylon_core"]
        grid[top + 3][left + 2] = COLORS["pylon_core"]
        grid[top + 2][left + 1] = COLORS["pylon_core"]
        grid[top + 2][left + 3] = COLORS["pylon_core"]
    elif entity_type == "spent_pylon":
        for y in range(top, top + CELL):
            for x in range(left, left + CELL):
                edge = y in (top, top + CELL - 1) or x in (left, left + CELL - 1)
                grid[y][x] = COLORS["spent"] if edge else BG_COLOR
        grid[top + 2][left + 2] = COLORS["spent"]
    elif entity_type == "pulse":
        for y in range(top, top + CELL):
            for x in range(left, left + CELL):
                if y == top + 2 or x == left + 2:
                    grid[y][x] = COLORS["pulse"]
    elif entity_type == "exit":
        for y in range(top, top + CELL):
            for x in range(left, left + CELL):
                edge = y in (top, top + CELL - 1) or x in (left, left + CELL - 1)
                grid[y][x] = COLORS["exit"] if edge else BG_COLOR
        grid[top + 2][left + 2] = COLORS["exit"]
    elif entity_type == "key":
        for y in range(top + 1, top + CELL - 1):
            for x in range(left + 1, left + CELL - 1):
                if y == top + 2 or x == left + 2:
                    grid[y][x] = COLORS["key"]
        grid[top + 2][left + 2] = BG_COLOR
    elif entity_type == "gate":
        for y in range(top, top + CELL):
            for x in range(left, left + CELL):
                edge = y in (top, top + CELL - 1) or x in (left, left + CELL - 1)
                bar = (x - left) in (1, 3)
                grid[y][x] = COLORS["wall"] if edge or bar else BG_COLOR
        grid[top + 2][left + 2] = COLORS["exit"]
    elif entity_type == "player":
        for y in range(top, top + CELL):
            for x in range(left, left + CELL):
                if y == top + 2 or x == left + 2:
                    grid[y][x] = COLORS["player"]
        grid[top + 1][left + 2] = COLORS["player_mark"]


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    """Deterministic history state update (DreamerV3 sequence model)."""
    if a_t not in get_available_actions():
        return copy.deepcopy(h_t)
    if a_t == 0:
        return get_initial_state(h_t["level"])[0]
    if a_t not in DIRS:
        return copy.deepcopy(h_t)

    level = h_t["level"]
    cfg = LEVELS[level]
    dr, dc = DIRS[a_t]
    nr, nc = h_t["player_r"] + dr, h_t["player_c"] + dc
    if not _tile_in_bounds(level, nr, nc):
        return copy.deepcopy(h_t)
    if _base_tile(level, nr, nc) == "#":
        return copy.deepcopy(h_t)
    if (nr, nc) in h_t["cracked"]:
        return copy.deepcopy(h_t)
    if (nr, nc) in cfg.get("gates", {}).values() and not h_t.get("gate_open", False):
        return copy.deepcopy(h_t)
    # The exit portal is visibly barred until all declared arena-control requirements are met.
    if (nr, nc) == cfg["exit"] and not _requirements_satisfied(h_t, cfg):
        return copy.deepcopy(h_t)
    # Keyed levels visibly require the moon key before the player may enter the blue exit portal.
    if (nr, nc) == cfg["exit"] and cfg.get("goal_requirements", {}).get("key_collected", False) and not h_t.get("key_collected", False):
        return copy.deepcopy(h_t)
    # Fresh pulse lanes deny space for one move, except the player may leave the pylon they just triggered.
    if h_t.get("pulse_timer", 0) > 0 and (nr, nc) in h_t.get("pulse_cells", []) and (nr, nc) != (h_t["player_r"], h_t["player_c"]):
        return copy.deepcopy(h_t)

    new_h = copy.deepcopy(h_t)
    new_h["undo"].append({k: copy.deepcopy(v) for k, v in h_t.items() if k != "undo"})
    if len(new_h["undo"]) > 50:
        new_h["undo"] = new_h["undo"][-50:]
    new_h["player_r"], new_h["player_c"] = nr, nc

    # Trigger an unspent pylon on entry. Its area effect clears its cracked brick target.
    for pid, pos in cfg["pylons"].items():
        if pos == (nr, nc) and pid not in new_h["triggered"]:
            new_h["triggered"].append(pid)
            new_h["triggered_pylons"].append(pid)
            new_h["triggered_pylons"] = [p for p in cfg.get("pylon_order", []) if p in new_h["triggered_pylons"]]
            new_h["last_pylon"] = pid
            if "spread" in cfg.get("active_tags", []):
                new_h["active_spreads"].append({"pid": pid, "idx": 0})
                new_h["pulse_cells"] = []
                new_h["pulse_timer"] = 0
            else:
                pulse = list(cfg["pulse_shapes"][pid])
                new_h["pulse_cells"] = pulse
                new_h["pulse_timer"] = 1
                for target in cfg["pulse_targets"][pid]:
                    if target in new_h["cracked"]:
                        new_h["cracked"].remove(target)
                        new_h["cleared_cracks"] += 1
            break

    if "keys" in cfg:
        for kid, pos in cfg["keys"].items():
            if pos == (nr, nc) and kid not in new_h["keys_collected"] and pos not in new_h["cracked"]:
                new_h["keys_collected"].append(kid)
                new_h["key_collected"] = True
                if "gates" in cfg:
                    new_h["gate_open"] = True

    if check_level_complete(new_h, {}, level):
        new_h["complete"] = True
        new_h["step"] += 1
        new_h["budget_left"] -= 1
        return new_h

    if "spread" in cfg.get("active_tags", []):
        new_cells = []
        remaining = []
        for wave in new_h.get("active_spreads", []):
            pid = wave["pid"]
            idx = wave["idx"]
            seq = cfg.get("spread_steps", {}).get(pid, [])
            if idx < len(seq):
                for cell in seq[idx]:
                    if cell not in new_cells:
                        new_cells.append(cell)
                wave["idx"] = idx + 1
            if wave["idx"] < len(seq):
                remaining.append(wave)
        for cell in new_cells:
            if cell in new_h["cracked"]:
                new_h["cracked"].remove(cell)
                new_h["cleared_cracks"] += 1
        new_h["active_spreads"] = remaining
        new_h["pulse_cells"] = new_cells
        new_h["pulse_timer"] = 1 if new_cells else 0
    else:
        if new_h.get("pulse_timer", 0) > 0:
            new_h["pulse_timer"] -= 1
        if new_h.get("pulse_timer", 0) <= 0:
            new_h["pulse_cells"] = []
    new_h["step"] += 1
    new_h["budget_left"] -= 1
    if new_h["budget_left"] < 0:
        new_h["failed"] = True
    return new_h


def predict(h_t: dict) -> dict:
    """Return minimal/empty z_t. This game is fully deterministic."""
    return {}


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    """Check if the current level's goal has been achieved."""
    cfg = LEVELS[level]
    req = cfg.get("goal_requirements", {})
    if (h_t.get("player_r"), h_t.get("player_c")) != cfg["exit"]:
        return False
    return _requirements_satisfied(h_t, cfg)


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    """Render the current state as a 32x32 grid."""
    level = h_t["level"]
    cfg = LEVELS[level]
    grid = [[BG_COLOR for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for r, row in enumerate(cfg["layout"]):
        for c, ch in enumerate(row):
            if ch == "#":
                _draw_entity(grid, r, c, "wall")
            else:
                _draw_entity(grid, r, c, "floor")
    for cell in h_t.get("pulse_cells", []):
        if cell not in h_t.get("cracked", []):
            _draw_entity(grid, cell[0], cell[1], "pulse")
    for cell in h_t.get("cracked", []):
        _draw_entity(grid, cell[0], cell[1], "cracked")
    for kid, pos in cfg.get("keys", {}).items():
        if kid not in h_t.get("keys_collected", []):
            _draw_entity(grid, pos[0], pos[1], "key")
    if not h_t.get("gate_open", False):
        for gid, pos in cfg.get("gates", {}).items():
            _draw_entity(grid, pos[0], pos[1], "gate")
    er, ec = cfg["exit"]
    _draw_entity(grid, er, ec, "exit")
    if not _requirements_satisfied(h_t, cfg):
        _draw_entity(grid, er, ec, "gate")
    for pid, (r, c) in cfg["pylons"].items():
        _draw_entity(grid, r, c, "spent_pylon" if pid in h_t.get("triggered", []) else "pylon")
    _draw_entity(grid, h_t["player_r"], h_t["player_c"], "player")
    # Budget bar HUD on row 0.
    budget = cfg["budget"]
    left = max(0, h_t.get("budget_left", budget))
    fill = min(30, int(30 * left / budget))
    for x in range(1, 31):
        grid[0][x] = COLORS["spent"] if x <= fill else COLORS["wall"]
    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    """Get the initial (h_t, z_t) for a given level."""
    cfg = LEVELS[level]
    sr, sc = cfg["player_start"]
    h_t = {
        "level": level,
        "step": 0,
        "player_r": sr,
        "player_c": sc,
        "cracked": list(cfg.get("cracked", [])),
        "triggered": [],
        "triggered_pylons": [],
        "cleared_cracks": 0,
        "keys_collected": [],
        "key_collected": False,
        "gate_open": False,
        "last_pylon": None,
        "pulse_cells": [],
        "pulse_timer": 0,
        "active_spreads": [],
        "budget_left": cfg["budget"],
        "complete": False,
        "failed": False,
        "undo": [],
    }
    return h_t, predict(h_t)


def get_available_actions() -> list[int]:
    """Return available action integers for this game."""
    return [0, 1, 2, 3, 4]


def solve_level(level: int) -> list:
    """Return a fixed sequence of actions that solves this level."""
    if level == 0:
        # Right, right to north pylon; backtrack and route down to south pylon; cross opened fronts to exit.
        return [4, 4, 3, 3, 2, 2, 2, 4, 4, 4]
    if level == 1:
        # Trigger A, collect the key from the opened front, backtrack to B, then cross the newly cleared exit front.
        return [4, 4, 4, 2, 1, 3, 3, 3, 2, 2, 4, 4, 4, 2]
    if level == 2:
        # Trigger spread A, route while it opens B, trigger spread B, step aside, then enter the opened exit.
        return [4, 4, 3, 3, 2, 2, 4, 4, 1, 2, 2, 4]
    if level == 3:
        # Open the bottom crossing, open the upper climb, then step aside from the final spread before entering.
        return [1, 2, 4, 4, 4, 1, 2, 1, 1, 1, 3, 4, 3, 3, 3]
    if level == 4:
        # A uncovers key, key opens gate, B opens center, C clears the gate cell, then enter.
        return [4, 4, 3, 3, 2, 2, 2, 1, 4, 4, 1, 4, 3, 2, 2, 4]
    if level == 5:
        # A's two-step spread opens lower/key route; B opens upper climb; key then C opens exit.
        return [4, 4, 3, 3, 2, 2, 2, 4, 4, 4, 1, 3, 1, 1, 4]
    if level == 6:
        # A opens lower/key lanes over time, B clears gated climb, key opens gate, C clears exit.
        return [4, 4, 3, 3, 2, 2, 2, 4, 4, 4, 3, 1, 4, 1, 1]
    if level == 7:
        # Four-pylon finale: A descent, B gate crack, delayed C key front, key, D exit crack, then gate-to-exit.
        return [4, 4, 3, 3, 2, 2, 2, 4, 1, 2, 1, 2, 4, 4, 1, 1, 1]
    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Mb2741(_FunctionalArcGame):
    GAME_ID = "mb2741-094cefb3"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
