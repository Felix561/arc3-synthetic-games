# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the ll4821/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy
import json
import math
import random

BG_COLOR = 5
CELL_SIZE = 4
BOARD_SIZE = 16
GRID_SIZE = 64
MINE_FUSE = 2
POWERUP_DURATION = 18

COLORS = {
    "wall": 13,
    "wall_highlight": 0,
    "player": 8,
    "player_core": 11,
    "hive": 12,
    "hive_core": 11,
    "mine": 15,
    "mine_core": 6,
    "enemy": 9,
    "enemy_highlight": 10,
    "powerup": 14,
    "powerup_core": 10,
    "blast": 11,
    "blast_core": 12,
    "hud": 0,
    "hud_alt": 10,
    "hud_warn": 7,
}

LEVELS = {
    0: {
        "name": "First Bloom",
        "layout": [
            "################",
            "#..............#",
            "#..............#",
            "#..P...........#",
            "#..............#",
            "#..............#",
            "#......H.......#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#..............#",
            "################",
        ],
        "active_tags": [],
        "fog_radius": None,
        "budget": 40,
        "stochastic": [],
    },
    1: {
        "name": "Pillar Sting",
        "layout": [
            "################",
            "#..............#",
            "#....##........#",
            "#..P.##........#",
            "#........E.....#",
            "#..............#",
            "#......H.......#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#..............#",
            "################",
        ],
        "active_tags": [],
        "fog_radius": None,
        "budget": 44,
        "stochastic": [],
    },
    2: {
        "name": "Timed Aisle",
        "layout": [
            "################",
            "#..............#",
            "#...##.....H...#",
            "#..P##.........#",
            "#..............#",
            "#......##......#",
            "#......##..E...#",
            "#..............#",
            "#...H..........#",
            "#..............#",
            "#......##......#",
            "#......##......#",
            "#..............#",
            "#..............#",
            "#..............#",
            "################",
        ],
        "active_tags": ["timer"],
        "fog_radius": None,
        "budget": 38,
        "stochastic": [],
    },
    3: {
        "name": "West Loop Sweep",
        "layout": [
            "################",
            "#..............#",
            "#..####........#",
            "#..#..#....E...#",
            "#P.#..#.........#",
            "#..####........#",
            "#..............#",
            "#.....H....H...#",
            "#..............#",
            "#....E.....##..#",
            "#..........##..#",
            "#..H...........#",
            "#..............#",
            "#..............#",
            "#..............#",
            "################",
        ],
        "active_tags": ["timer"],
        "fog_radius": None,
        "budget": 36,
        "stochastic": [],
    },
    4: {
        "name": "Breach Charge",
        "layout": [
            "################",
            "#P.............#",
            "#....###.......#",
            "#....#H#.......#",
            "#....###.......#",
            "#..U...........#",
            "#..............#",
            "#.......###....#",
            "#.......#H#....#",
            "#.......###....#",
            "#......E.......#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#..............#",
            "################",
        ],
        "active_tags": ["timer", "powerup"],
        "fog_radius": None,
        "budget": 36,
        "stochastic": [],
    },
    5: {
        "name": "Jittered Patrols",
        "layout": [
            "################",
            "#P.......###...#",
            "#.U......#E#...#",
            "#...###..###...#",
            "#...#H#........#",
            "#...###........#",
            "#..............#",
            "#...###........#",
            "#...#H#........#",
            "#...###........#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#..............#",
            "#..............#",
            "################"
        ],
        "active_tags": ["timer", "powerup"],
        "fog_radius": None,
        "budget": 36,
        "stochastic": ["enemy_jitter"],
    },
    6: {
        "name": "Double Breach",
        "layout": [
            "################",
            "#P.......###...#",
            "#.U......#E#...#",
            "#...###..###...#",
            "#...#H#........#",
            "#...###........#",
            "#..............#",
            "#...###........#",
            "#...#H#........#",
            "#...###........#",
            "#.....U..###...#",
            "#...###..#E#...#",
            "#...#H#..###...#",
            "#...###........#",
            "#..............#",
            "################"
        ],
        "active_tags": ["timer", "powerup"],
        "fog_radius": None,
        "budget": 35,
        "stochastic": ["enemy_jitter"],
    },
    7: {
        "name": "Lunar West Core",
        "layout": [
            "################",
            "#P.......###...#",
            "#.U......#E#...#",
            "#...###..###...#",
            "#...#H#........#",
            "#...###........#",
            "#..............#",
            "#...###........#",
            "#...#H#........#",
            "#...###........#",
            "#.....U..###...#",
            "#...###..#E#...#",
            "#...#H#..###...#",
            "#...###........#",
            "#............E.#",
            "################"
        ],
        "active_tags": ["timer", "powerup"],
        "fog_radius": None,
        "budget": 34,
        "stochastic": ["enemy_jitter"],
    },
}

def _normalize_row(row):
    if len(row) < BOARD_SIZE:
        if row.startswith("#") and row.endswith("#"):
            return row[:-1] + "." * (BOARD_SIZE - len(row)) + "#"
        return row + "." * (BOARD_SIZE - len(row))
    if len(row) > BOARD_SIZE:
        if row.startswith("#"):
            return row[: BOARD_SIZE - 1] + "#"
        return row[:BOARD_SIZE]
    return row


for _lvl in LEVELS:
    LEVELS[_lvl]["layout"] = [_normalize_row(r) for r in LEVELS[_lvl]["layout"][:BOARD_SIZE]]
    if len(LEVELS[_lvl]["layout"]) < BOARD_SIZE:
        filler = "#" + "." * (BOARD_SIZE - 2) + "#"
        LEVELS[_lvl]["layout"] += [filler for _ in range(BOARD_SIZE - len(LEVELS[_lvl]["layout"]))]


DIRS = {
    1: (-1, 0),
    2: (1, 0),
    3: (0, -1),
    4: (0, 1),
}

for _lvl, _cfg in LEVELS.items():
    walls = []
    hives = []
    enemies = []
    powerups = []
    player_start = (1, 1)
    for r, row in enumerate(_cfg["layout"]):
        for c, ch in enumerate(row):
            if ch == "#":
                walls.append((r, c))
            elif ch == "P":
                player_start = (r, c)
            elif ch == "H":
                hives.append((r, c))
            elif ch == "E":
                enemies.append((r, c))
            elif ch == "U":
                powerups.append((r, c))
    _cfg["walls"] = walls
    _cfg["wall_set"] = set(walls)
    _cfg["player_start"] = player_start
    _cfg["hive_starts"] = hives
    _cfg["enemy_starts"] = enemies
    _cfg["powerup_starts"] = powerups


def _inside(r, c):
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE


def _to_set(pairs):
    return {(item[0], item[1]) for item in pairs}


def _draw_entity(grid, row, col, entity_type):
    base_r = row * CELL_SIZE
    base_c = col * CELL_SIZE
    if entity_type == "wall":
        pattern = [
            [13, 13, 13, 13],
            [13, 0, 0, 13],
            [13, 0, 0, 13],
            [13, 13, 13, 13],
        ]
    elif entity_type == "player":
        pattern = [
            [5, 8, 8, 5],
            [8, 11, 11, 8],
            [8, 11, 11, 8],
            [5, 8, 8, 5],
        ]
    elif entity_type == "hive":
        pattern = [
            [12, 12, 12, 12],
            [12, 11, 11, 12],
            [12, 11, 11, 12],
            [12, 12, 12, 12],
        ]
    elif entity_type == "mine":
        pattern = [
            [5, 15, 15, 5],
            [15, 6, 6, 15],
            [15, 6, 6, 15],
            [5, 15, 15, 5],
        ]
    elif entity_type == "enemy":
        pattern = [
            [5, 9, 5, 5],
            [9, 10, 9, 5],
            [5, 9, 10, 9],
            [5, 5, 9, 5],
        ]
    elif entity_type == "powerup":
        pattern = [
            [14, 14, 14, 14],
            [14, 10, 10, 14],
            [14, 10, 10, 14],
            [14, 14, 14, 14],
        ]
    elif entity_type == "blast":
        pattern = [
            [5, 11, 11, 5],
            [11, 12, 12, 11],
            [11, 12, 12, 11],
            [5, 11, 11, 5],
        ]
    else:
        pattern = [[BG_COLOR] * CELL_SIZE for _ in range(CELL_SIZE)]
    for dr in range(CELL_SIZE):
        for dc in range(CELL_SIZE):
            rr = base_r + dr
            cc = base_c + dc
            if 0 <= rr < GRID_SIZE and 0 <= cc < GRID_SIZE:
                grid[rr][cc] = pattern[dr][dc]


def _blast_cells(mine, wall_set):
    r, c, _, radius, pierce = mine
    cells = {(r, c)}
    for dr, dc in DIRS.values():
        used_pierce = 0
        for dist in range(1, radius + 1):
            nr = r + dr * dist
            nc = c + dc * dist
            if not _inside(nr, nc):
                break
            if (nr, nc) in wall_set:
                if used_pierce < pierce:
                    used_pierce += 1
                    continue
                break
            cells.add((nr, nc))
    return cells


def _mine_hits_target(cell, target, radius, pierce, wall_set):
    probe = [cell[0], cell[1], 1, radius, pierce]
    return target in _blast_cells(probe, wall_set)


def _enemy_axis_mode(index, h_t, z_t):
    modes = z_t.get("enemy_modes", []) if isinstance(z_t, dict) else []
    if index < len(modes):
        return modes[index]
    return (h_t.get("step", 0) + index) % 2


def _move_enemies(enemy_list, player_pos, hives, mines, level_cfg, z_t, step):
    wall_set = level_cfg["wall_set"]
    hive_set = _to_set(hives)
    mine_set = _to_set(mines)
    moved = []
    occupied = set()
    for idx, enemy in enumerate(enemy_list):
        r, c = enemy[0], enemy[1]
        dr = player_pos[0] - r
        dc = player_pos[1] - c
        v_step = 1 if dr > 0 else -1 if dr < 0 else 0
        h_step = 1 if dc > 0 else -1 if dc < 0 else 0
        mode = (step + idx) % 2
        modes = z_t.get("enemy_modes", []) if isinstance(z_t, dict) else []
        if idx < len(modes):
            mode = modes[idx]
        candidates = []
        if mode == 0:
            if v_step != 0:
                candidates.append((r + v_step, c))
            if h_step != 0:
                candidates.append((r, c + h_step))
        else:
            if h_step != 0:
                candidates.append((r, c + h_step))
            if v_step != 0:
                candidates.append((r + v_step, c))
        for action in [1, 4, 2, 3]:
            nr = r + DIRS[action][0]
            nc = c + DIRS[action][1]
            if (nr, nc) not in candidates:
                candidates.append((nr, nc))
        move = (r, c)
        for nr, nc in candidates:
            if not _inside(nr, nc):
                continue
            if (nr, nc) in wall_set or (nr, nc) in hive_set or (nr, nc) in mine_set or (nr, nc) in occupied:
                continue
            move = (nr, nc)
            break
        occupied.add(move)
        moved.append([move[0], move[1]])
    return moved


def _player_blocked(level_cfg, h_t):
    blocked = set(level_cfg["wall_set"])
    blocked |= _to_set(h_t["hives"])
    blocked |= _to_set(h_t["enemies"])
    return blocked


def _bfs_first_action(start, goals, blocked, avoid=None):
    if avoid is None:
        avoid = set()
    goals = set(goals)
    if not goals:
        return None
    if start in goals:
        return None
    queue = [start]
    prev = {start: None}
    head = 0
    while head < len(queue):
        cur = queue[head]
        head += 1
        for action in [1, 4, 2, 3]:
            nr = cur[0] + DIRS[action][0]
            nc = cur[1] + DIRS[action][1]
            nxt = (nr, nc)
            if not _inside(nr, nc):
                continue
            if nxt in blocked or nxt in avoid or nxt in prev:
                continue
            prev[nxt] = (cur, action)
            if nxt in goals:
                step = nxt
                while prev[step][0] != start:
                    step = prev[step][0]
                return prev[step][1]
            queue.append(nxt)
    return None


def _distance_to_goals(start, goals, blocked):
    goals = set(goals)
    if not goals:
        return 0
    if start in goals:
        return 0
    queue = [start]
    dist = {start: 0}
    head = 0
    while head < len(queue):
        cur = queue[head]
        head += 1
        for action in [1, 4, 2, 3]:
            nr = cur[0] + DIRS[action][0]
            nc = cur[1] + DIRS[action][1]
            nxt = (nr, nc)
            if not _inside(nr, nc) or nxt in blocked or nxt in dist:
                continue
            dist[nxt] = dist[cur] + 1
            if nxt in goals:
                return dist[nxt]
            queue.append(nxt)
    return 999


def _candidate_fire_cells(hives, level_cfg, powered):
    wall_set = level_cfg["wall_set"]
    hive_set = set(hives)
    radius = 2 if powered else 1
    pierce = 1 if powered else 0
    cells = set()
    for hive in hive_set:
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if (r, c) in wall_set or (r, c) in hive_set:
                    continue
                if _mine_hits_target((r, c), hive, radius, pierce, wall_set):
                    cells.add((r, c))
    return cells


def _best_safe_move(level, h_t, z_t, preferred_goals):
    level_cfg = LEVELS[level]
    best_action = 1
    best_score = 10 ** 9
    for action in [1, 2, 3, 4]:
        nxt = transition(h_t, z_t, action)
        score = 0
        if nxt.get("expired") and len(nxt.get("hives", [])) > 0:
            score += 5000
        if nxt.get("stings", 0) > h_t.get("stings", 0):
            score += 3000
        blocked = set(level_cfg["wall_set"]) | _to_set(nxt["hives"]) | _to_set(nxt["enemies"])
        pos = (nxt["player_r"], nxt["player_c"])
        score += _distance_to_goals(pos, preferred_goals, blocked)
        if preferred_goals and pos in preferred_goals:
            score -= 20
        score += len(nxt["hives"]) * 50
        score += nxt.get("step", 0) * 0.01
        if score < best_score:
            best_score = score
            best_action = action
    return best_action


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    n = copy.deepcopy(h_t)
    level_cfg = LEVELS[n["level"]]
    if a_t == 0:
        return get_initial_state(n["level"])[0]
    if n.get("expired"):
        return n
    n["step"] += 1
    n["blasts"] = []

    current_powered = "powerup" in level_cfg["active_tags"] and n.get("power_timer", 0) > 0
    current_radius = 2 if current_powered else 1
    current_pierce = 1 if current_powered else 0

    blocked = _player_blocked(level_cfg, n)
    if a_t in DIRS:
        dr, dc = DIRS[a_t]
        nr = n["player_r"] + dr
        nc = n["player_c"] + dc
        if _inside(nr, nc) and (nr, nc) not in blocked:
            old_pos = (n["player_r"], n["player_c"])
            mine_positions = _to_set(n["mines"])
            if old_pos not in mine_positions:
                n["mines"].append([old_pos[0], old_pos[1], MINE_FUSE, current_radius, current_pierce])
            n["player_r"] = nr
            n["player_c"] = nc

    if "powerup" in level_cfg["active_tags"]:
        collected = None
        for idx, item in enumerate(n["powerups"]):
            if item[0] == n["player_r"] and item[1] == n["player_c"]:
                collected = idx
                break
        if collected is not None:
            n["powerups"].pop(collected)
            n["power_timer"] = POWERUP_DURATION
        elif n.get("power_timer", 0) > 0:
            n["power_timer"] -= 1
    else:
        n["power_timer"] = 0
    n["blast_radius"] = 2 if n.get("power_timer", 0) > 0 else 1
    n["pierce"] = 1 if n.get("power_timer", 0) > 0 else 0

    n["enemies"] = _move_enemies(
        n["enemies"],
        (n["player_r"], n["player_c"]),
        n["hives"],
        n["mines"],
        level_cfg,
        z_t if isinstance(z_t, dict) else {},
        n["step"],
    )

    exploding = []
    updated_mines = []
    for mine in n["mines"]:
        next_mine = [mine[0], mine[1], mine[2] - 1, mine[3], mine[4]]
        if next_mine[2] <= 0:
            exploding.append(next_mine)
        else:
            updated_mines.append(next_mine)
    n["mines"] = updated_mines

    blast_cells = set()
    for mine in exploding:
        blast_cells |= _blast_cells(mine, level_cfg["wall_set"])
    n["blasts"] = [[r, c] for (r, c) in sorted(blast_cells)]

    if blast_cells:
        n["hives"] = [h for h in n["hives"] if (h[0], h[1]) not in blast_cells]
        n["enemies"] = [e for e in n["enemies"] if (e[0], e[1]) not in blast_cells]

    stung = False
    for enemy in n["enemies"]:
        if enemy[0] == n["player_r"] and enemy[1] == n["player_c"]:
            stung = True
            break
    if stung:
        start_r, start_c = level_cfg["player_start"]
        n["player_r"] = start_r
        n["player_c"] = start_c
        n["power_timer"] = 0
        n["blast_radius"] = 1
        n["pierce"] = 0
        n["stings"] += 1
        if "timer" in level_cfg["active_tags"]:
            n["step"] += 2

    if "timer" in level_cfg["active_tags"] and n["step"] >= level_cfg["budget"] and len(n["hives"]) > 0:
        n["expired"] = True
    else:
        n["expired"] = False
    return n


def predict(h_t: dict, seed: int) -> dict:
    level_cfg = LEVELS[h_t["level"]]
    if not level_cfg.get("stochastic"):
        return {}
    z_t = {}
    rng = random.Random(seed + 97 * h_t["level"] + 13 * h_t.get("step", 0) + len(h_t.get("enemies", [])))
    if "enemy_jitter" in level_cfg["stochastic"]:
        z_t["enemy_modes"] = [rng.randint(0, 1) for _ in h_t.get("enemies", [])]
    return z_t


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    return len(h_t.get("hives", [])) == 0


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    grid = [[BG_COLOR for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    level_cfg = LEVELS[h_t["level"]]

    for r, c in level_cfg["walls"]:
        _draw_entity(grid, r, c, "wall")

    for r, c in h_t.get("powerups", []):
        _draw_entity(grid, r, c, "powerup")
    for r, c in h_t.get("hives", []):
        _draw_entity(grid, r, c, "hive")
    for r, c, _, _, _ in h_t.get("mines", []):
        _draw_entity(grid, r, c, "mine")
    for r, c in h_t.get("enemies", []):
        _draw_entity(grid, r, c, "enemy")
    _draw_entity(grid, h_t["player_r"], h_t["player_c"], "player")
    for r, c in h_t.get("blasts", []):
        _draw_entity(grid, r, c, "blast")

    if "timer" in level_cfg["active_tags"]:
        remaining = max(0, level_cfg["budget"] - h_t.get("step", 0))
        fill = int((remaining / max(1, level_cfg["budget"])) * GRID_SIZE)
        for c in range(fill):
            grid[63][c] = COLORS["hud"]
        for c in range(fill, GRID_SIZE):
            grid[63][c] = COLORS["hud_warn"]
    else:
        for c in range(GRID_SIZE):
            grid[63][c] = COLORS["hud_warn"] if c % 2 == 0 else BG_COLOR

    power_fill = int((h_t.get("power_timer", 0) / max(1, POWERUP_DURATION)) * GRID_SIZE)
    for c in range(power_fill):
        grid[62][c] = COLORS["hud_alt"]

    hive_count = min(len(h_t.get("hives", [])), 15)
    for i in range(hive_count):
        grid[61][i * 4:(i * 4) + 3] = [COLORS["hive"]] * 3

    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    level_cfg = LEVELS[level]
    start_r, start_c = level_cfg["player_start"]
    h_t = {
        "level": level,
        "step": 0,
        "player_r": start_r,
        "player_c": start_c,
        "mines": [],
        "blasts": [],
        "hives": [[r, c] for r, c in level_cfg["hive_starts"]],
        "enemies": [[r, c] for r, c in level_cfg["enemy_starts"]],
        "powerups": [[r, c] for r, c in level_cfg["powerup_starts"]],
        "power_timer": 0,
        "blast_radius": 1,
        "pierce": 0,
        "expired": False,
        "stings": 0,
    }
    z_t = predict(h_t, 0)
    return h_t, z_t


def get_available_actions() -> list[int]:
    return [1, 2, 3, 4]


def solve_level(level: int, h_t: dict, z_t: dict):
    level_cfg = LEVELS[level]
    if check_level_complete(h_t, z_t, level):
        return 1

    player = (h_t["player_r"], h_t["player_c"])
    hives = [tuple(h) for h in h_t.get("hives", [])]
    powerups = [tuple(p) for p in h_t.get("powerups", [])]
    blocked = set(level_cfg["wall_set"]) | set(hives) | _to_set(h_t.get("enemies", []))
    powered = "powerup" in level_cfg["active_tags"] and h_t.get("power_timer", 0) > 0

    unpowered_goals = _candidate_fire_cells(hives, level_cfg, False)
    powered_goals = _candidate_fire_cells(hives, level_cfg, True)
    fire_cells = powered_goals if powered else unpowered_goals

    def _safe_path_action(goals):
        if not goals:
            return None
        action = _bfs_first_action(player, goals, blocked)
        if action is None:
            return None
        candidate = transition(h_t, z_t, action)
        if not candidate.get("expired") and candidate.get("stings", 0) == h_t.get("stings", 0):
            return action
        return None

    if "powerup" in level_cfg["active_tags"]:
        # Power-up-first policy for breach levels: sealed hives are the main curriculum.
        if not powered and powerups:
            action = _safe_path_action(set(powerups))
            if action is not None:
                return action
            return _best_safe_move(level, h_t, z_t, set(powerups))

        # If power is running short and a refresh exists, refresh before committing deeper.
        if powered and powerups and len(hives) > 1:
            dist_fire = _distance_to_goals(player, fire_cells, blocked)
            dist_pwr = _distance_to_goals(player, powerups, blocked)
            if h_t.get("power_timer", 0) <= dist_fire + 2 and dist_pwr <= dist_fire:
                action = _safe_path_action(set(powerups))
                if action is not None:
                    return action
                return _best_safe_move(level, h_t, z_t, set(powerups))

    if player in fire_cells:
        legal_goals = set()
        for action in [1, 2, 3, 4]:
            nr = player[0] + DIRS[action][0]
            nc = player[1] + DIRS[action][1]
            if _inside(nr, nc) and (nr, nc) not in blocked:
                legal_goals.add((nr, nc))
        if legal_goals:
            return _best_safe_move(level, h_t, z_t, legal_goals)

    action = _safe_path_action(fire_cells)
    if action is not None:
        return action
    if fire_cells:
        return _best_safe_move(level, h_t, z_t, fire_cells)

    if powerups and (not powered):
        action = _safe_path_action(set(powerups))
        if action is not None:
            return action
        return _best_safe_move(level, h_t, z_t, set(powerups))

    return _best_safe_move(level, h_t, z_t, {(level_cfg["player_start"][0], level_cfg["player_start"][1])})


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Ll4821(_FunctionalArcGame):
    GAME_ID = "ll4821-9da7c9ef"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
