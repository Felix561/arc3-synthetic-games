# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the td4826/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy

BG_COLOR = 5
CELL_SIZE = 4
GRID_SIZE = 32
BOARD_SIZE = 8

COLORS = {
    "bg": 5,
    "floor": 4,
    "floor_dot": 1,
    "wall": 2,
    "wall_shadow": 3,
    "player": 8,
    "player_tail": 0,
    "exit": 11,
    "exit_core": 0,
    "shark": 12,
    "shark_teeth": 13,
    "switch": 14,
    "switch_core": 0,
    "gate": 15,
    "link": 6,
    "fog": 10,
    "fog_core": 7,
    "hud": 10,
    "hud_empty": 3,
}

LEVELS = {
    0: {
        "layout": [
            "########",
            "#...#..#",
            "#.##.#E#",
            "#....#.#",
            "###.##.#",
            "#......#",
            "#..###.#",
            "########",
        ],
        "player_start": (1, 1),
        "shark_start": (1, 2),
        "exit": (2, 6),
        "budget": 20,
        "lives": 1,
        "active_tags": ["chase"],
        "goal_requirements": {"lives": 1, "failed": False},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "a fever shark pursues through the lower corridor and catches direct or poorly timed routes",
            "dependencies": ["avoid shark contact", "bait shark down the long corridor", "turn up the right lane", "enter exit before shark recovers"],
            "feedback": "the orange shark visibly moves after each committed dolphin step",
            "bypass_guard": "no extra requirements exist; the exit is physically reachable only by navigating the chase maze",
        },
    },
    1: {
        "layout": [
            "########",
            "#..#...#",
            "#..#.#E#",
            "#..#.#.#",
            "#....#G#",
            "#S#....#",
            "#......#",
            "########",
        ],
        "player_start": (1, 1),
        "shark_start": (1, 2),
        "exit": (2, 6),
        "switches": [(5, 1)],
        "gates": [(1, 4), (4, 6)],
        "switch_groups": [{"id": "A", "switch": (5, 1), "gates": [(1, 4), (4, 6)]}],
        "budget": 26,
        "lives": 1,
        "active_tags": ["chase", "switch"],
        "goal_requirements": {"gate_open": True, "lives": 1, "failed": False},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "the paired purple scissors gates block both passages into the exit lane",
            "dependencies": ["step on the green lucky switch", "confirm the linked purple gate opens", "bait the shark away from the upper lane", "enter the exit"],
            "feedback": "the switch gains a white center and the linked gate changes from a purple X to an open pink-edged floor marker",
            "bypass_guard": "both upper and lower routes to the exit are physically sealed by closed gates until gate_open is true",
        },
    },
    2: {
        "layout": [
            "########",
            "#..#..E#",
            "#..#.#.#",
            "#....#.#",
            "#.##.#.#",
            "#S.....#",
            "#..#G..#",
            "########",
        ],
        "player_start": (1, 1),
        "shark_start": (1, 2),
        "shark_starts": [(1, 2), (6, 5)],
        "exit": (1, 6),
        "switches": [(5, 1)],
        "gates": [(6, 4), (5, 6), (1, 5)],
        "switch_groups": [{"id": "A", "switch": (5, 1), "gates": [(6, 4), (5, 6), (1, 5)]}],
        "budget": 32,
        "lives": 1,
        "active_tags": ["chase", "switch"],
        "goal_requirements": {"gate_open": True, "lives": 1, "failed": False},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "two fever sharks cover different lanes while paired scissors gates block the return route and the exit approach",
            "dependencies": ["reach the lower switch before the second shark closes", "open both linked gates", "route around the lower shark", "thread the upper exit lane before interception"],
            "feedback": "both orange sharks move every committed step; the green switch opens both pink-marked gate cells",
            "bypass_guard": "closed gates at the lower turn, right-column approach, and upper shortcut physically prevent reaching the exit before the switch is stepped on",
        },
    },
    3: {
        "layout": [
            "########",
            "#..#..E#",
            "#..#.#.#",
            "#S...#.#",
            "#.##...#",
            "#..#G#.#",
            "#......#",
            "########",
        ],
        "player_start": (1, 1),
        "shark_start": (1, 2),
        "shark_starts": [(1, 2), (6, 5)],
        "exit": (1, 6),
        "switches": [(3, 1)],
        "gates": [(5, 4), (4, 6), (1, 5)],
        "switch_groups": [{"id": "A", "switch": (3, 1), "gates": [(5, 4), (4, 6), (1, 5)]}],
        "fog": [(4, 4), (4, 5)],
        "budget": 38,
        "lives": 1,
        "active_tags": ["chase", "switch", "fog"],
        "goal_requirements": {"gate_open": True, "lives": 1, "failed": False},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "a visible fog bank and offset switch force the dolphin to delay a pursuing shark before using the opened right corridor",
            "dependencies": ["reach the left-side switch", "open the linked gates", "draw the shark across the light-blue fog delay strip", "escape through the right corridor to the exit"],
            "feedback": "fog is drawn as pale diagonal mist and sharks pause one turn after entering it; gates visibly open from the switch",
            "bypass_guard": "closed gates block the switch return, right corridor, and upper shortcut until the switch is reached",
        },
    },
    4: {
        "layout": [
            "########",
            "#EG...##",
            "#G#....#",
            "#...#..#",
            "#.#S#..#",
            "#...#..#",
            "#.....##",
            "########",
        ],
        "player_start": (6, 1),
        "shark_start": (5, 1),
        "shark_starts": [(5, 1), (2, 6)],
        "exit": (1, 1),
        "switches": [(4, 3)],
        "gates": [(1, 2), (2, 1)],
        "switch_groups": [{"id": "A", "switch": (4, 3), "gates": [(1, 2), (2, 1)]}],
        "fog": [(5, 3)],
        "budget": 34,
        "lives": 1,
        "active_tags": ["chase", "switch", "toggle", "fog"],
        "goal_requirements": {"gate_open": True, "lives": 1, "failed": False},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "toggle gates seal both cells adjacent to the exit until the central switch is stepped on",
            "dependencies": ["reach the central toggle switch", "leave it without stepping on it again", "bait sharks through the lower bend and fog", "enter the opened exit pocket"],
            "feedback": "the switch fills green and both pink-linked gates open while sharks continue to move",
            "bypass_guard": "both neighbors of the exit are closed gates before the switch, so the exit is physically unavailable early",
        },
    },

    5: {
        "layout": [
            "########",
            "#EG...##",
            "#G#....#",
            "#...#..#",
            "#.#S#..#",
            "#...#..#",
            "#.....##",
            "########",
        ],
        "player_start": (6, 1),
        "shark_start": (6, 5),
        "shark_starts": [(6, 5), (1, 5), (3, 6)],
        "exit": (1, 1),
        "switches": [(4, 3)],
        "gates": [(1, 2), (2, 1), (6, 3)],
        "switch_groups": [{"id": "A", "switch": (4, 3), "gates": [(1, 2), (2, 1), (6, 3)]}],
        "fog": [(5, 3), (5, 4), (3, 3)],
        "budget": 52,
        "lives": 1,
        "active_tags": ["chase", "switch", "fog"],
        "goal_requirements": {"gate_open": True, "lives": 1, "failed": False},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "three fever sharks and linked scissors gates force a fog-assisted return route",
            "dependencies": ["reach the central switch", "open all linked gates", "draw a shark across visible fog", "time the upper-left crossing", "enter the guarded exit pocket"],
            "feedback": "the switch fills and every pink-linked gate opens while fog slows sharks for one turn",
            "bypass_guard": "two closed gates border the exit pocket and a third blocks the lower shortcut before the switch is activated",
        },
    },

    6: {
        "layout": [
            "########",
            "#EG...##",
            "#G#....#",
            "#...#..#",
            "#.#S#..#",
            "#..S#..#",
            "#.....##",
            "########",
        ],
        "player_start": (6, 1),
        "shark_start": (6, 5),
        "shark_starts": [(6, 5), (1, 5), (3, 6)],
        "exit": (1, 1),
        "switches": [(5, 3), (4, 3)],
        "required_switches": 2,
        "gates": [(1, 2), (2, 1), (6, 3)],
        "switch_groups": [{"id": "A", "switch": (5, 3), "gates": [(1, 2), (2, 1), (6, 3)]}, {"id": "A", "switch": (4, 3), "gates": [(1, 2), (2, 1), (6, 3)]}],
        "fog": [(5, 4), (3, 3)],
        "budget": 38,
        "lives": 1,
        "active_tags": ["chase", "switch", "multi_switch", "fog"],
        "goal_requirements": {"gate_open": True, "switch_count": 2, "lives": 1, "failed": False},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "two ordered lucky switches must both be stepped on before the exit pocket gates open under three-shark chase pressure",
            "dependencies": ["bait the lower shark in the left lane", "step on the lower switch", "step on the upper switch without backtracking onto danger", "use the opened gate pair to enter the exit pocket"],
            "feedback": "each visited switch fills green; after the second switch all pink-linked gate cells open",
            "bypass_guard": "both neighbors of the exit are closed gates until both switches are active",
        },
    },

    7: {
        "layout": [
            "########",
            "#EG..S##",
            "#G#....#",
            "#...#..#",
            "#.#S#..#",
            "#..S...#",
            "#......#",
            "########",
        ],
        "player_start": (6, 1),
        "shark_start": (6, 5),
        "shark_starts": [(6, 5), (1, 4), (3, 6)],
        "exit": (1, 1),
        "switches": [(5, 3), (4, 3), (1, 5)],
        "required_switches": 3,
        "gates": [(1, 2), (2, 1), (6, 3)],
        "switch_groups": [{"id": "A", "switch": (5, 3), "gates": [(1, 2), (2, 1), (6, 3)]}, {"id": "A", "switch": (4, 3), "gates": [(1, 2), (2, 1), (6, 3)]}, {"id": "A", "switch": (1, 5), "gates": [(1, 2), (2, 1), (6, 3)]}],
        "fog": [(5, 4), (3, 3), (4, 6)],
        "budget": 56,
        "lives": 1,
        "active_tags": ["chase", "switch", "multi_switch", "fog"],
        "goal_requirements": {"gate_open": True, "switch_count": 3, "lives": 1, "failed": False},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "three lucky switches must all be visited before the exit gates open while three sharks compress the arena",
            "dependencies": ["activate the lower switch", "activate the middle switch", "activate the upper switch", "use fog delays to break pursuit", "enter the opened exit pocket"],
            "feedback": "each switch fills independently; after the third switch, every linked purple gate opens",
            "bypass_guard": "closed gates block both neighbors of the exit and the lower shortcut until all three switches are active",
        },
    },
}

DIRS = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}


def _is_wall(level_data, r, c):
    if r < 0 or c < 0 or r >= BOARD_SIZE or c >= BOARD_SIZE:
        return True
    return level_data["layout"][r][c] == "#"


def _gate_closed(h_t, r, c):
    return (r, c) in LEVELS[h_t["level"]].get("gates", []) and not h_t.get("gate_open", False)


def _passable(level_data, r, c, h_t=None):
    if _is_wall(level_data, r, c):
        return False
    if h_t is not None and (r, c) in level_data.get("gates", []) and not h_t.get("gate_open", False):
        return False
    return True


def _draw_entity(grid, row, col, entity_type):
    base_r = row * CELL_SIZE
    base_c = col * CELL_SIZE
    if entity_type == "floor":
        for rr in range(base_r, base_r + CELL_SIZE):
            for cc in range(base_c, base_c + CELL_SIZE):
                grid[rr][cc] = COLORS["floor"]
        grid[base_r + 2][base_c + 2] = COLORS["floor_dot"]
    elif entity_type == "wall":
        for rr in range(base_r, base_r + CELL_SIZE):
            for cc in range(base_c, base_c + CELL_SIZE):
                grid[rr][cc] = COLORS["wall"]
        for cc in range(base_c, base_c + CELL_SIZE):
            grid[base_r + 3][cc] = COLORS["wall_shadow"]
    elif entity_type == "exit":
        for rr in range(base_r, base_r + CELL_SIZE):
            for cc in range(base_c, base_c + CELL_SIZE):
                if rr in (base_r, base_r + 3) or cc in (base_c, base_c + 3):
                    grid[rr][cc] = COLORS["exit"]
                else:
                    grid[rr][cc] = COLORS["exit_core"]
    elif entity_type == "player":
        pts = [(1, 1), (1, 2), (0, 1), (2, 1), (2, 2), (3, 0)]
        for dr, dc in pts:
            grid[base_r + dr][base_c + dc] = COLORS["player"]
        grid[base_r + 1][base_c + 3] = COLORS["player_tail"]
    elif entity_type == "shark":
        pts = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2), (3, 3)]
        for dr, dc in pts:
            grid[base_r + dr][base_c + dc] = COLORS["shark"]
        grid[base_r + 1][base_c + 3] = COLORS["shark_teeth"]
        grid[base_r + 2][base_c + 3] = COLORS["shark_teeth"]
    elif entity_type == "switch_off":
        for rr in range(base_r, base_r + CELL_SIZE):
            for cc in range(base_c, base_c + CELL_SIZE):
                grid[rr][cc] = COLORS["floor"]
        for i in range(CELL_SIZE):
            grid[base_r + i][base_c + i] = COLORS["switch"]
            grid[base_r + i][base_c + CELL_SIZE - 1 - i] = COLORS["switch"]
        grid[base_r][base_c] = COLORS["link"]
        grid[base_r][base_c + 3] = COLORS["link"]
    elif entity_type == "switch_on":
        for rr in range(base_r, base_r + CELL_SIZE):
            for cc in range(base_c, base_c + CELL_SIZE):
                grid[rr][cc] = COLORS["switch"]
        grid[base_r + 1][base_c + 1] = COLORS["switch_core"]
        grid[base_r + 1][base_c + 2] = COLORS["switch_core"]
        grid[base_r][base_c] = COLORS["link"]
        grid[base_r][base_c + 3] = COLORS["link"]
    elif entity_type == "gate_closed":
        for rr in range(base_r, base_r + CELL_SIZE):
            for cc in range(base_c, base_c + CELL_SIZE):
                grid[rr][cc] = COLORS["floor"]
        for i in range(CELL_SIZE):
            grid[base_r + i][base_c + i] = COLORS["gate"]
            grid[base_r + i][base_c + CELL_SIZE - 1 - i] = COLORS["gate"]
        grid[base_r][base_c] = COLORS["link"]
        grid[base_r][base_c + 3] = COLORS["link"]
    elif entity_type == "gate_open":
        for rr in range(base_r, base_r + CELL_SIZE):
            for cc in range(base_c, base_c + CELL_SIZE):
                grid[rr][cc] = COLORS["floor"]
        for cc in range(base_c, base_c + CELL_SIZE):
            grid[base_r][cc] = COLORS["link"]
        grid[base_r + 2][base_c + 2] = COLORS["floor_dot"]
    elif entity_type == "fog":
        for rr in range(base_r, base_r + CELL_SIZE):
            for cc in range(base_c, base_c + CELL_SIZE):
                grid[rr][cc] = COLORS["floor"]
        for i in range(CELL_SIZE):
            grid[base_r + i][base_c + i] = COLORS["fog"]
            grid[base_r + i][base_c + ((i + 1) % CELL_SIZE)] = COLORS["fog_core"]


def _move_shark(level_data, sr, sc, pr, pc, h_t=None):
    choices = []
    if abs(pc - sc) >= abs(pr - sr):
        if pc > sc:
            choices.append((0, 1))
        elif pc < sc:
            choices.append((0, -1))
        if pr > sr:
            choices.append((1, 0))
        elif pr < sr:
            choices.append((-1, 0))
    else:
        if pr > sr:
            choices.append((1, 0))
        elif pr < sr:
            choices.append((-1, 0))
        if pc > sc:
            choices.append((0, 1))
        elif pc < sc:
            choices.append((0, -1))
    for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        if d not in choices:
            choices.append(d)
    for dr, dc in choices:
        nr, nc = sr + dr, sc + dc
        if _passable(level_data, nr, nc, h_t):
            return nr, nc
    return sr, sc


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    """Deterministic history state update (DreamerV3 sequence model)."""
    if isinstance(a_t, tuple):
        base_action = a_t[0] if a_t else None
    else:
        base_action = a_t
    if base_action not in get_available_actions():
        return copy.deepcopy(h_t)

    level = h_t["level"]
    level_data = LEVELS[level]
    if base_action == 0:
        fresh, _ = get_initial_state(level)
        return fresh
    if h_t.get("complete") or h_t.get("failed"):
        return copy.deepcopy(h_t)
    if base_action not in DIRS:
        return copy.deepcopy(h_t)

    dr, dc = DIRS[base_action]
    nr, nc = h_t["player_r"] + dr, h_t["player_c"] + dc
    if not _passable(level_data, nr, nc, h_t):
        return copy.deepcopy(h_t)

    n = copy.deepcopy(h_t)
    n["player_r"], n["player_c"] = nr, nc
    if "switch" in level_data.get("active_tags", []) and (nr, nc) in level_data.get("switches", []):
        if "multi_switch" in level_data.get("active_tags", []):
            seen_switches = list(n.get("switches_on", []))
            if (nr, nc) not in seen_switches:
                seen_switches.append((nr, nc))
            n["switches_on"] = seen_switches
            n["switch_count"] = len(seen_switches)
            n["gate_open"] = n["switch_count"] >= level_data.get("required_switches", len(level_data.get("switches", [])))
        elif "toggle" in level_data.get("active_tags", []):
            n["gate_open"] = not n.get("gate_open", False)
        else:
            n["gate_open"] = True
    n["step"] += 1
    n["budget_left"] -= 1

    if check_level_complete(n, {}, level):
        n["complete"] = True
        return n

    if "chase" in level_data.get("active_tags", []):
        current_sharks = n.get("sharks", [(n["shark_r"], n["shark_c"])])
        for sr, sc in current_sharks:
            if (sr, sc) == (nr, nc):
                n["lives"] -= 1
                n["failed"] = True
                return n
        moved_sharks = []
        old_cooldowns = n.get("shark_cooldowns", [0 for _ in current_sharks])
        new_cooldowns = []
        for idx, (sr, sc) in enumerate(current_sharks):
            if idx < len(old_cooldowns) and old_cooldowns[idx] > 0:
                nsr, nsc = sr, sc
                new_cooldowns.append(0)
            else:
                nsr, nsc = _move_shark(level_data, sr, sc, nr, nc, n)
                new_cooldowns.append(1 if (nsr, nsc) in level_data.get("fog", []) else 0)
            moved_sharks.append((nsr, nsc))
            if (nsr, nsc) == (nr, nc):
                n["lives"] -= 1
                n["failed"] = True
                n["sharks"] = moved_sharks + current_sharks[len(moved_sharks):]
                n["shark_cooldowns"] = new_cooldowns
                n["shark_r"], n["shark_c"] = nsr, nsc
                return n
        n["sharks"] = moved_sharks
        n["shark_cooldowns"] = new_cooldowns
        if moved_sharks:
            n["shark_r"], n["shark_c"] = moved_sharks[0]

    if n["budget_left"] < 0:
        n["failed"] = True
    return n


def predict(h_t: dict, seed: int) -> dict:
    """Return exactly {}. This game is fully deterministic."""
    return {}


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    """Check if the current level's goal has been achieved."""
    level_data = LEVELS[level]
    at_exit = (h_t.get("player_r"), h_t.get("player_c")) == level_data["exit"]
    requirements = level_data.get("goal_requirements", {})
    for key, needed in requirements.items():
        if h_t.get(key) != needed:
            return False
    return bool(at_exit)


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    """Render the current state as a 32x32 grid."""
    grid = [[BG_COLOR for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    level_data = LEVELS[h_t["level"]]
    for r, row in enumerate(level_data["layout"]):
        for c, ch in enumerate(row):
            _draw_entity(grid, r, c, "wall" if ch == "#" else "floor")
    er, ec = level_data["exit"]
    _draw_entity(grid, er, ec, "exit")
    for fr, fc in level_data.get("fog", []):
        _draw_entity(grid, fr, fc, "fog")
    for gr, gc in level_data.get("gates", []):
        _draw_entity(grid, gr, gc, "gate_open" if h_t.get("gate_open", False) else "gate_closed")
    for sr, sc in level_data.get("switches", []):
        if "multi_switch" in level_data.get("active_tags", []):
            is_on = (sr, sc) in h_t.get("switches_on", [])
        else:
            is_on = h_t.get("gate_open", False)
        _draw_entity(grid, sr, sc, "switch_on" if is_on else "switch_off")
    for shr, shc in h_t.get("sharks", [(h_t["shark_r"], h_t["shark_c"])]):
        _draw_entity(grid, shr, shc, "shark")
    _draw_entity(grid, h_t["player_r"], h_t["player_c"], "player")

    max_budget = max(1, level_data["budget"])
    lit = max(0, min(GRID_SIZE, (h_t.get("budget_left", 0) * GRID_SIZE) // max_budget))
    for c in range(GRID_SIZE):
        grid[31][c] = COLORS["hud"] if c < lit else COLORS["hud_empty"]
    if h_t.get("failed"):
        for i in range(4, 28):
            grid[i][i] = 8
            grid[i][31 - i] = 8
    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    """Get the initial (h_t, z_t) for a given level."""
    level_data = LEVELS[level]
    pr, pc = level_data["player_start"]
    shark_list = level_data.get("shark_starts", [level_data["shark_start"]])
    sr, sc = shark_list[0]
    h_t = {
        "level": level,
        "step": 0,
        "player_r": pr,
        "player_c": pc,
        "shark_r": sr,
        "shark_c": sc,
        "sharks": list(shark_list),
        "shark_cooldowns": [0 for _ in shark_list],
        "budget_left": level_data["budget"],
        "lives": level_data.get("lives", 1),
        "gate_open": False,
        "switches_on": [],
        "switch_count": 0,
        "complete": False,
        "failed": False,
    }
    return h_t, {}


def get_available_actions() -> list[int]:
    """Return available action integers for this game."""
    return [0, 1, 2, 3, 4]


def solve_level(level: int) -> list:
    """Return a fixed sequence of actions that solves this level."""
    if level == 0:
        return [2, 2, 4, 4, 2, 2, 4, 4, 4, 1, 1, 1]
    if level == 1:
        return [2, 2, 2, 2, 2, 4, 4, 1, 4, 4, 4, 1, 1, 1]
    if level == 2:
        return [2, 4, 3, 4, 3, 2, 4, 4, 4, 2, 2, 3, 3, 3, 1, 1, 4, 4, 4, 1, 1, 4, 4]
    if level == 3:
        return [2, 2, 4, 4, 4, 1, 1, 4, 4]
    if level == 4:
        return [4, 3, 4, 3, 4, 4, 4, 4, 1, 1, 1, 1, 3, 3, 2, 2, 2, 3, 3, 1, 1, 1, 1]
    if level == 5:
        return [1, 1, 1, 2, 1, 2, 2, 4, 4, 1, 1, 1, 1, 3, 3]
    if level == 6:
        return [1, 1, 1, 2, 1, 2, 2, 4, 4, 1, 1, 1, 1, 3, 3]
    if level == 7:
        return [1, 2, 1, 4, 2, 1, 3, 1, 1, 4, 4, 2, 2, 4, 4, 1, 1, 1, 1, 3, 3, 3, 3]
    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Td4826(_FunctionalArcGame):
    GAME_ID = "td4826-33bf03a4"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
