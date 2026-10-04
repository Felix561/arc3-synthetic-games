# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the ne4172/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy

BG_COLOR = 4
COLORS = {
    "bg": 4,
    "player": 15,
    "collectible": 11,
    "wall": 9,
    "exit": 9,
    "white": 0,
    "chaser": 13,
    "warning": 6,
}
CELL = 3
ORIGIN_R = 3
ORIGIN_C = 1
DIRS = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}

LEVELS = {
    0: {
        "layout": [
            "##########",
            "#...S..E.#",
            "#.####...#",
            "#....#...#",
            "#.##.#.#.#",
            "#....#...#",
            "#P.s.#..C#",
            "##########",
        ],
        "player_start": (6, 1),
        "chasers": [(6, 8)],
        "collectibles": [((6, 3), "lower_phrase"), ((1, 4), "upper_phrase")],
        "exit": (1, 7),
        "budget": 25,
        "echo_interval": 3,
        "active_tags": ["chase", "collectible"],
        "goal_requirements": {"required_items": ["lower_phrase", "upper_phrase"]},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "the permit exit is a locked maroon-blue barrier until both phrase shards are collected",
            "dependencies": ["collect lower phrase shard", "detour up the west corridor", "collect upper phrase shard", "enter opened permit exit"],
            "feedback": "collected shards disappear; the exit changes from a maroon-locked ring to a white-centered open ring",
            "bypass_guard": "transition blocks movement onto the exit cell while any required shard remains, so the player cannot stand on the success tile early",
        },
    },
    1: {
        "layout": [
            "##########",
            "#..S..E..#",
            "#.####.#.#",
            "#....#.#.#",
            "#.##.#...#",
            "#S...#.#.#",
            "#.##..S#.#",
            "#P.s....C#",
            "##########",
        ],
        "player_start": (7, 1),
        "chasers": [(7, 8)],
        "collectibles": [((7, 3), "lower_phrase"), ((5, 1), "side_permit"), ((6, 6), "east_phrase"), ((1, 3), "north_phrase")],
        "exit": (1, 6),
        "budget": 42,
        "echo_interval": 4,
        "active_tags": ["chase", "collectible"],
        "goal_requirements": {"required_items": ["lower_phrase", "side_permit", "east_phrase", "north_phrase"]},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "the permit exit is locked until four phrase shards are collected; one shard sits in an east branch that must be entered and left before the echo closes",
            "dependencies": ["collect lower phrase", "time the east branch phrase", "retreat west to side permit", "collect north phrase", "enter opened permit exit"],
            "feedback": "each shard disappears; the exit changes from locked maroon cross to open white center only after all four named items are held",
            "bypass_guard": "transition blocks movement onto the exit cell until every required_items entry is in inventory",
        },
    },
    2: {
        "layout": [
            "##########",
            "#..S..E..#",
            "#.####.#.#",
            "#....#.#.#",
            "#.##.#...#",
            "#S...#.#.#",
            "#.##..S#.#",
            "#P.s....C#",
            "##########",
        ],
        "player_start": (7, 1),
        "chasers": [(7, 8)],
        "collectibles": [((7, 3), "lower_phrase"), ((5, 1), "side_permit"), ((6, 6), "memory_phrase"), ((1, 3), "north_phrase")],
        "exit": (1, 6),
        "budget": 48,
        "echo_interval": 4,
        "memory_ttl": 5,
        "active_tags": ["chase", "collectible", "memory"],
        "goal_requirements": {"required_items": ["lower_phrase", "side_permit", "memory_phrase", "north_phrase"]},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "the exit is locked by four phrase shards, and echo memory marks temporarily make recently occupied echo cells unsafe",
            "dependencies": ["collect lower phrase", "avoid the first echo memory trail", "collect memory phrase in the east branch", "retreat west to side permit", "collect north phrase", "enter opened permit exit"],
            "feedback": "pink memory marks appear behind the echo and fade; shards vanish; the exit opens when all required item names are held",
            "bypass_guard": "movement onto the exit cell is blocked until every required_items entry is in inventory, and stepping on active memory marks causes capture rather than silent success",
        },
    },
    3: {
        "layout": [
            "##########",
            "#..S..E.C#",
            "#.####.#.#",
            "#....#.#.#",
            "#.##.#...#",
            "#S...#.#.#",
            "#.##..S#.#",
            "#P.s....C#",
            "##########",
        ],
        "player_start": (7, 1),
        "chasers": [(7, 8), (1, 8)],
        "collectibles": [((7, 3), "lower_phrase"), ((5, 1), "side_permit"), ((6, 6), "east_phrase"), ((4, 8), "harsh_phrase"), ((1, 3), "north_phrase")],
        "exit": (1, 6),
        "budget": 62,
        "echo_interval": 4,
        "memory_ttl": 4,
        "active_tags": ["chase", "collectible", "memory"],
        "goal_requirements": {"required_items": ["lower_phrase", "side_permit", "east_phrase", "harsh_phrase", "north_phrase"]},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "two echo faces narrow both corridors while five shards, including an upper east pocket shard, lock the exit",
            "dependencies": ["collect lower phrase", "time the east branch", "detour to harsh_phrase", "retreat around lower echo", "avoid upper echo face", "collect north phrase", "enter exit"],
            "feedback": "two maroon faces move on the same echo beat and leave pink memory marks; exit opens after all five shards vanish",
            "bypass_guard": "exit entry is physically blocked until every required item is in inventory",
        },
    },
    4: {
        "layout": [
            "##########",
            "#..S..E.C#",
            "#.####.#.#",
            "#....#.#.#",
            "#.##.#...#",
            "#K...#.#.#",
            "#.##..S#.#",
            "#P.sG...C#",
            "##########",
        ],
        "player_start": (7, 1),
        "chasers": [(7, 8), (1, 8)],
        "collectibles": [((7, 3), "lower_phrase"), ((5, 1), "side_permit"), ((6, 6), "east_phrase"), ((1, 3), "north_phrase")],
        "gates": [{"pos": (7, 4), "requires": "side_permit", "name": "east_gate"}],
        "exit": (1, 6),
        "budget": 64,
        "echo_interval": 5,
        "memory_ttl": 4,
        "active_tags": ["chase", "collectible", "memory", "keys"],
        "goal_requirements": {"required_items": ["lower_phrase", "side_permit", "east_phrase", "north_phrase"], "opened_gates": ["east_gate"]},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "a locked lower gate blocks the direct east branch until the side permit is collected, while two echoes leave dangerous memory marks",
            "dependencies": ["go north first to collect side permit", "collect north phrase", "return to lower phrase", "open east_gate with side permit", "collect east phrase", "enter opened exit"],
            "feedback": "the gate changes from maroon locked bars to a white-blue open frame after the side_permit is held and the gate is entered; memory marks fade visibly",
            "bypass_guard": "the gate cell is physically blocked until its permit is held, and completion requires opened_gates so the east branch cannot be bypassed by hidden state",
        },
    },
    5: {
        "layout": [
            "##########",
            "#..S.GE.C#",
            "#.####.#.#",
            "#....#.#.#",
            "#.##.#...#",
            "#K...#.#.#",
            "#.##..S#.#",
            "#P.sG...C#",
            "##########",
        ],
        "player_start": (7, 1),
        "chasers": [(7, 8), (1, 8)],
        "collectibles": [((7, 3), "lower_phrase"), ((5, 1), "side_permit"), ((6, 6), "east_phrase"), ((1, 3), "north_phrase")],
        "gates": [{"pos": (7, 4), "requires": "side_permit", "name": "lower_gate"}, {"pos": (1, 5), "requires": "east_phrase", "name": "north_gate"}],
        "exit": (1, 6),
        "budget": 74,
        "echo_interval": 5,
        "memory_ttl": 4,
        "active_tags": ["chase", "collectible", "memory", "keys"],
        "goal_requirements": {"required_items": ["lower_phrase", "side_permit", "east_phrase", "north_phrase"], "opened_gates": ["lower_gate", "north_gate"]},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "two sequential permit gates force the player to fetch side_permit before the lower gate and east_phrase before the north gate, while echoes press both corridors",
            "dependencies": ["collect side_permit", "return to lower corridor", "open lower_gate", "collect east_phrase", "collect north_phrase", "open north_gate", "enter exit"],
            "feedback": "each gate changes from maroon lock bars to a white-blue frame only after entering it with the named permit; echoes leave fading pink memory marks",
            "bypass_guard": "the exit is behind north_gate and completion also requires both opened_gates plus all items, so neither gate can be skipped",
        },
    },
    6: {
        "layout": [
            "##########",
            "#..S.GE.C#",
            "#.####.#.#",
            "#..SG#...#",
            "#.##.#...#",
            "#K...#.#.#",
            "#.##..S#.#",
            "#P.sG...C#",
            "##########",
        ],
        "player_start": (7, 1),
        "chasers": [(7, 8), (1, 8), (3, 8)],
        "collectibles": [((7, 3), "lower_phrase"), ((5, 1), "side_permit"), ((6, 6), "east_phrase"), ((3, 3), "face_permit"), ((1, 3), "north_phrase")],
        "gates": [{"pos": (7, 4), "requires": "side_permit", "name": "lower_gate"}, {"pos": (3, 4), "requires": "east_phrase", "name": "face_gate"}, {"pos": (1, 5), "requires": "face_permit", "name": "north_gate"}],
        "exit": (1, 6),
        "budget": 78,
        "echo_interval": 5,
        "memory_ttl": 4,
        "active_tags": ["chase", "collectible", "memory", "keys"],
        "goal_requirements": {"required_items": ["lower_phrase", "side_permit", "east_phrase", "face_permit", "north_phrase"], "opened_gates": ["lower_gate", "face_gate", "north_gate"]},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "a three-gate permit relay blocks the exit: side_permit opens the lower gate, east_phrase opens the face gate, and face_permit opens the north gate while three echoes patrol",
            "dependencies": ["collect side_permit", "open lower_gate", "collect east_phrase", "open face_gate", "collect face_permit", "collect north_phrase", "open north_gate", "enter exit"],
            "feedback": "each gate changes from maroon lock bars to a white-blue open frame only after the correct permit is carried into it; three echo faces leave fading pink memory marks",
            "bypass_guard": "the exit is physically behind north_gate and check_level_complete requires all five named items and all three opened gates",
        },
    },
    7: {
        "layout": [
            "##########",
            "#..S.GE.C#",
            "#.####.#.#",
            "#..SG#...#",
            "#.##.#..S#",
            "#K...#.#.#",
            "#.##..S#.#",
            "#P.sG...C#",
            "##########",
        ],
        "player_start": (7, 1),
        "chasers": [(7, 8), (1, 8), (3, 8)],
        "collectibles": [((7, 3), "lower_phrase"), ((5, 1), "side_permit"), ((6, 6), "east_phrase"), ((3, 3), "face_permit"), ((4, 8), "harsh_phrase"), ((1, 3), "north_phrase")],
        "gates": [{"pos": (7, 4), "requires": "side_permit", "name": "lower_gate"}, {"pos": (3, 4), "requires": "east_phrase", "name": "face_gate"}, {"pos": (1, 5), "requires": "face_permit", "name": "north_gate"}],
        "exit": (1, 6),
        "budget": 90,
        "echo_interval": 7,
        "memory_ttl": 4,
        "active_tags": ["chase", "collectible", "memory", "keys"],
        "goal_requirements": {"required_items": ["lower_phrase", "side_permit", "east_phrase", "face_permit", "harsh_phrase", "north_phrase"], "opened_gates": ["lower_gate", "face_gate", "north_gate"]},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "three-gate permit relay plus a harsh phrase in the upper east pocket force a detour under three echoes",
            "dependencies": ["collect side_permit", "open lower_gate", "collect east_phrase", "detour to harsh_phrase before memory marks close the pocket", "open face_gate", "collect face_permit", "collect north_phrase", "open north_gate", "enter exit"],
            "feedback": "six shards disappear, gates open as white-blue frames, and three echoes leave fading pink memory marks",
            "bypass_guard": "exit is behind north_gate and completion requires all six items plus all three opened gates",
        },
    }
}


def _draw_entity(grid, row, col, entity_type):
    cr = ORIGIN_R + row * CELL + 1
    cc = ORIGIN_C + col * CELL + 1
    if entity_type == "wall":
        for rr in range(cr - 1, cr + 2):
            for cc2 in range(cc - 1, cc + 2):
                if 0 <= rr < 32 and 0 <= cc2 < 32:
                    grid[rr][cc2] = COLORS["wall"]
        if 0 <= cr < 32 and 0 <= cc < 32:
            grid[cr][cc] = COLORS["warning"]
    elif entity_type == "floor":
        if 0 <= cr < 32 and 0 <= cc < 32:
            grid[cr][cc] = COLORS["white"]
    elif entity_type == "collectible":
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            rr, cc2 = cr + dr, cc + dc
            if 0 <= rr < 32 and 0 <= cc2 < 32:
                grid[rr][cc2] = COLORS["collectible"]
        if 0 <= cr < 32 and 0 <= cc < 32:
            grid[cr][cc] = COLORS["white"]
    elif entity_type == "player":
        for d in range(-2, 3):
            if 0 <= cr + d < 32 and 0 <= cc < 32:
                grid[cr + d][cc] = COLORS["player"]
            if 0 <= cr < 32 and 0 <= cc + d < 32:
                grid[cr][cc + d] = COLORS["player"]
        if 0 <= cr - 1 < 32 and 0 <= cc + 1 < 32:
            grid[cr - 1][cc + 1] = COLORS["white"]
    elif entity_type == "chaser":
        for rr in range(cr - 1, cr + 3):
            for cc2 in range(cc - 1, cc + 3):
                if 0 <= rr < 32 and 0 <= cc2 < 32:
                    grid[rr][cc2] = COLORS["chaser"]
        for dc in [0, 2]:
            if 0 <= cr < 32 and 0 <= cc - 1 + dc < 32:
                grid[cr][cc - 1 + dc] = COLORS["warning"]
        if 0 <= cr + 2 < 32 and 0 <= cc < 32:
            grid[cr + 2][cc] = COLORS["warning"]
    elif entity_type == "gate_locked":
        for d in range(-1, 2):
            rr = cr + d
            for cc2 in [cc - 1, cc + 1]:
                if 0 <= rr < 32 and 0 <= cc2 < 32:
                    grid[rr][cc2] = COLORS["chaser"]
        for d in range(-1, 2):
            cc2 = cc + d
            if 0 <= cr < 32 and 0 <= cc2 < 32:
                grid[cr][cc2] = COLORS["exit"]
        if 0 <= cr < 32 and 0 <= cc < 32:
            grid[cr][cc] = COLORS["warning"]
    elif entity_type == "gate_open":
        for d in range(-1, 2):
            for rr, cc2 in [(cr - 1, cc + d), (cr + 1, cc + d), (cr + d, cc - 1), (cr + d, cc + 1)]:
                if 0 <= rr < 32 and 0 <= cc2 < 32:
                    grid[rr][cc2] = COLORS["exit"]
        if 0 <= cr < 32 and 0 <= cc < 32:
            grid[cr][cc] = COLORS["white"]
    elif entity_type == "exit_locked":
        for d in range(-2, 3):
            for rr, cc2 in [(cr - 2, cc + d), (cr + 2, cc + d), (cr + d, cc - 2), (cr + d, cc + 2)]:
                if 0 <= rr < 32 and 0 <= cc2 < 32:
                    grid[rr][cc2] = COLORS["exit"]
        for d in range(-1, 2):
            if 0 <= cr + d < 32 and 0 <= cc + d < 32:
                grid[cr + d][cc + d] = COLORS["chaser"]
            if 0 <= cr + d < 32 and 0 <= cc - d < 32:
                grid[cr + d][cc - d] = COLORS["chaser"]
    elif entity_type == "exit_open":
        for d in range(-2, 3):
            for rr, cc2 in [(cr - 2, cc + d), (cr + 2, cc + d), (cr + d, cc - 2), (cr + d, cc + 2)]:
                if 0 <= rr < 32 and 0 <= cc2 < 32:
                    grid[rr][cc2] = COLORS["exit"]
        for rr in range(cr - 1, cr + 2):
            for cc2 in range(cc - 1, cc + 2):
                if 0 <= rr < 32 and 0 <= cc2 < 32:
                    grid[rr][cc2] = COLORS["white"]
        if 0 <= cr < 32 and 0 <= cc < 32:
            grid[cr][cc] = COLORS["collectible"]
    elif entity_type == "memory":
        for d in range(-1, 2):
            if 0 <= cr + d < 32 and 0 <= cc < 32:
                grid[cr + d][cc] = COLORS["warning"]
            if 0 <= cr < 32 and 0 <= cc + d < 32:
                grid[cr][cc + d] = COLORS["warning"]
        if 0 <= cr < 32 and 0 <= cc < 32:
            grid[cr][cc] = COLORS["chaser"]
    elif entity_type == "caught":
        for d in range(-2, 3):
            if 0 <= cr + d < 32 and 0 <= cc < 32:
                grid[cr + d][cc] = COLORS["chaser"]
            if 0 <= cr < 32 and 0 <= cc + d < 32:
                grid[cr][cc + d] = COLORS["chaser"]


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    """Deterministic history state update (DreamerV3 sequence model)."""
    if a_t == 0:
        return get_initial_state(h_t["level"])[0]
    h = copy.deepcopy(h_t)
    level = h["level"]
    cfg = LEVELS[level]
    base_action = a_t[0] if isinstance(a_t, tuple) else a_t
    if base_action not in DIRS or h.get("caught", False) or h.get("complete", False) or h["budget_remaining"] <= 0:
        return h

    dr, dc = DIRS[base_action]
    nr, nc = h["player_r"] + dr, h["player_c"] + dc
    layout = cfg["layout"]
    blocked = False
    if nr < 0 or nr >= len(layout) or nc < 0 or nc >= len(layout[0]) or layout[nr][nc] == "#":
        blocked = True
    if (nr, nc) == tuple(cfg["exit"]) and "collectible" in cfg.get("active_tags", []):
        required_items = cfg["goal_requirements"].get("required_items", [])
        if any(name not in h.get("inventory", []) for name in required_items):
            blocked = True
    for gate in cfg.get("gates", []):
        if (nr, nc) == tuple(gate["pos"]) and gate.get("requires") not in h.get("inventory", []):
            blocked = True
    if not blocked:
        h["player_r"], h["player_c"] = nr, nc

    if "collectible" in cfg.get("active_tags", []):
        kept = []
        for item in h["collectibles"]:
            if h["player_r"] == item[0] and h["player_c"] == item[1]:
                h["collected"] += 1
                if len(item) > 2 and item[2] not in h["inventory"]:
                    h["inventory"].append(item[2])
            else:
                kept.append(item)
        h["collectibles"] = kept

    for gate in cfg.get("gates", []):
        if (h["player_r"], h["player_c"]) == tuple(gate["pos"]) and gate.get("requires") in h.get("inventory", []):
            if gate.get("name") not in h.setdefault("opened_gates", []):
                h["opened_gates"].append(gate.get("name"))

    for ch in h["chasers"]:
        if h["player_r"] == ch[0] and h["player_c"] == ch[1]:
            h["caught"] = True
    if "memory" in cfg.get("active_tags", []):
        for mark in h.get("memory_marks", []):
            if h["player_r"] == mark[0] and h["player_c"] == mark[1]:
                h["caught"] = True

    h["step"] += 1
    h["budget_remaining"] -= 1

    if "memory" in cfg.get("active_tags", []):
        h["memory_marks"] = [[r, c, ttl - 1] for r, c, ttl in h.get("memory_marks", []) if ttl - 1 > 0]

    if not h["caught"] and h["step"] % cfg.get("echo_interval", 1) == 0:
        moved = []
        for ch in h["chasers"]:
            er, ec = ch[0], ch[1]
            if "memory" in cfg.get("active_tags", []):
                h.setdefault("memory_marks", []).append([er, ec, cfg.get("memory_ttl", 4)])
            pr, pc = h["player_r"], h["player_c"]
            row_step = -1 if pr < er else (1 if pr > er else 0)
            col_step = -1 if pc < ec else (1 if pc > ec else 0)
            choices = []
            if abs(pc - ec) >= abs(pr - er):
                choices = [(0, col_step), (row_step, 0)]
            else:
                choices = [(row_step, 0), (0, col_step)]
            moved_this = False
            for mdr, mdc in choices:
                tr, tc = er + mdr, ec + mdc
                if (mdr != 0 or mdc != 0) and 0 <= tr < len(layout) and 0 <= tc < len(layout[0]) and layout[tr][tc] != "#":
                    er, ec = tr, tc
                    moved_this = True
                    break
            if not moved_this:
                er, ec = ch[0], ch[1]
            moved.append([er, ec])
            if er == h["player_r"] and ec == h["player_c"]:
                h["caught"] = True
        h["chasers"] = moved

    h["complete"] = check_level_complete(h, {}, level)
    return h


def predict(h_t: dict, seed: int) -> dict:
    """Return exactly {}. This game is fully deterministic."""
    return {}


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    """Check if the current level's goal has been achieved."""
    cfg = LEVELS[level]
    req = cfg.get("goal_requirements", {})
    required_items = req.get("required_items", [])
    has_items = all(name in h_t.get("inventory", []) for name in required_items)
    required_gates = req.get("opened_gates", [])
    has_gates = all(name in h_t.get("opened_gates", []) for name in required_gates)
    at_exit = (h_t.get("player_r"), h_t.get("player_c")) == tuple(cfg["exit"])
    return bool(at_exit and has_items and has_gates and not h_t.get("caught", False))


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    """Render the current state as a 32x32 grid."""
    grid = [[BG_COLOR for _ in range(32)] for _ in range(32)]
    cfg = LEVELS[h_t["level"]]
    for r, row in enumerate(cfg["layout"]):
        for c, ch in enumerate(row):
            if ch == "#":
                _draw_entity(grid, r, c, "wall")
            else:
                _draw_entity(grid, r, c, "floor")
    required_items = cfg["goal_requirements"].get("required_items", [])
    exit_type = "exit_open" if all(name in h_t.get("inventory", []) for name in required_items) else "exit_locked"
    _draw_entity(grid, cfg["exit"][0], cfg["exit"][1], exit_type)
    for gate in cfg.get("gates", []):
        gate_type = "gate_open" if gate.get("requires") in h_t.get("inventory", []) else "gate_locked"
        _draw_entity(grid, gate["pos"][0], gate["pos"][1], gate_type)
    for item in h_t.get("collectibles", []):
        _draw_entity(grid, item[0], item[1], "collectible")
    for mark in h_t.get("memory_marks", []):
        _draw_entity(grid, mark[0], mark[1], "memory")
    for ch in h_t.get("chasers", []):
        _draw_entity(grid, ch[0], ch[1], "chaser")
    _draw_entity(grid, h_t["player_r"], h_t["player_c"], "caught" if h_t.get("caught", False) else "player")

    budget = cfg["budget"]
    remaining = max(0, h_t.get("budget_remaining", 0))
    bar = int((remaining * 32) / budget) if budget else 0
    for c in range(32):
        grid[0][c] = COLORS["collectible"] if c < bar else COLORS["chaser"]
    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    """Get the initial (h_t, z_t) for a given level."""
    cfg = LEVELS[level]
    h_t = {
        "level": level,
        "step": 0,
        "budget_remaining": cfg["budget"],
        "player_r": cfg["player_start"][0],
        "player_c": cfg["player_start"][1],
        "chasers": [[r, c] for r, c in cfg.get("chasers", [])],
        "collectibles": [[pos[0], pos[1], name] for pos, name in cfg.get("collectibles", [])],
        "collected": 0,
        "inventory": [],
        "caught": False,
        "complete": False,
        "memory_marks": [],
        "opened_gates": [],
    }
    return h_t, {}


def get_available_actions() -> list[int]:
    """Return available action integers for this game."""
    return [0, 1, 2, 3, 4]


def solve_level(level: int) -> list:
    """Return a fixed sequence of actions that solves this level."""
    if level == 0:
        return [4, 4, 3, 3, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4]
    if level == 1:
        return [4, 4, 4, 1, 4, 4, 3, 3, 1, 3, 3, 3, 1, 1, 1, 1, 4, 4, 4, 4, 4]
    if level == 2:
        return [4, 4, 4, 1, 4, 4, 3, 3, 1, 3, 3, 3, 1, 1, 1, 1, 4, 4, 4, 4, 4]
    if level == 3:
        return [1, 1, 1, 2, 4, 4, 4, 2, 4, 4, 1, 1, 4, 4, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4]
    if level == 4:
        return [1, 1, 1, 1, 1, 1, 4, 4, 3, 3, 2, 2, 2, 2, 2, 2, 4, 4, 4, 1, 4, 4, 1, 1, 1, 1, 1]
    if level == 5:
        return [1, 1, 1, 2, 2, 2, 4, 4, 4, 1, 4, 4, 3, 3, 1, 1, 1, 3, 3, 3, 1, 1, 4, 4, 4, 4, 4]
    if level == 6:
        return [1, 1, 1, 2, 2, 2, 4, 4, 4, 1, 4, 4, 3, 3, 1, 1, 1, 3, 3, 3, 1, 1, 4, 4, 4, 4, 4]
    if level == 7:
        return [1, 1, 1, 2, 2, 2, 4, 4, 4, 1, 4, 4, 1, 1, 4, 4, 3, 3, 2, 2, 3, 3, 1, 1, 1, 3, 3, 3, 1, 1, 4, 4, 4, 4, 4]
    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Ne4172(_FunctionalArcGame):
    GAME_ID = "ne4172-fe2b50a3"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
