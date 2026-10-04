# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the rs0427/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy

BG_COLOR = 4
CELL = 3
ORIGIN_R = 2
ORIGIN_C = 1
COLORS = {
    "background": 4,
    "player": 12,
    "hazard": 8,
    "fuse": 11,
    "switch": 6,
    "one_way": 15,
    "wall": 13,
    "white": 0,
    "gate": 14,
    "exit": 9,
}
DIRS = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}

LEVELS = {
    0: {
        "layout": [
            "#########",
            "#P..F.###",
            "#.#...###",
            "#...G..E#",
            "#########",
        ],
        "player_start": (1, 1),
        "exit": (3, 7),
        "fuses": [(1, 4)],
        "gates": [(3, 4)],
        "patrol_route": [(3, 5), (2, 5), (1, 5), (2, 5)],
        "patrol_start_index": 0,
        "active_tags": ["patrol", "collectible"],
        "budget": 15,
        "fog_radius": None,
        "goal_requirements": {"required_fuses": 1},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "closed green gate blocks the only path to the exit until the fuse is collected",
            "dependencies": ["collect yellow fuse", "open green gate", "time crossing past red grinder", "enter blue exit hatch"],
            "feedback": "the yellow fuse disappears and the green gate changes from a solid blocker to an open marked floor",
            "bypass_guard": "all routes to the blue exit pass through the fuse-opened gate, so the exit tile cannot be reached early",
        },
    },
    1: {
        "layout": [
            "##########",
            "#P..S#.###",
            "#.##G#.###",
            "#.##.....#",
            "#.######E#",
            "##########",
        ],
        "player_start": (1, 1),
        "exit": (4, 8),
        "switches": [(1, 4)],
        "gates": [(2, 4)],
        "switch_links": [{"switch": (1, 4), "targets": [(2, 4)]}],
        "patrol_route": [(3, 6), (2, 6), (1, 6), (2, 6)],
        "patrol_start_index": 0,
        "active_tags": ["patrol", "switch"],
        "budget": 17,
        "fog_radius": None,
        "goal_requirements": {"switches_on": 1},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "a pink switch must open the only green gate before the lower hazard lane can be reached",
            "dependencies": ["step on pink switch", "observe linked gate open", "cross the grinder lane on the safe phase", "enter blue exit hatch"],
            "feedback": "the switch fills in and the linked gate gains pink corner markers while becoming passable",
            "bypass_guard": "walls isolate the exit corridor behind the gate, so the exit tile cannot be reached before the switch requirement is visibly satisfied",
        },
    },
    2: {
        "layout": [
            "##########",
            "#P..>...E#",
            "#.#.##.#.#",
            "#.#.##.#.#",
            "#...##...#",
            "##########",
        ],
        "player_start": (1, 1),
        "exit": (1, 8),
        "one_ways": {(1, 4): 4},
        "patrol_route": [(1, 6), (2, 6), (3, 6), (2, 6)],
        "patrol_start_index": 0,
        "active_tags": ["patrol", "one-way"],
        "budget": 24,
        "fog_radius": None,
        "goal_requirements": {"one_way_passes": 1},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "the only exit lane passes through a purple right-facing one-way flap and then a timed grinder crossing",
            "dependencies": ["use the pre-flap pocket to set grinder phase", "enter the one-way flap from the left", "cross the grinder lane before it returns", "enter blue exit hatch"],
            "feedback": "the purple arrow marks the irreversible direction and the red route shows the crossing cycle",
            "bypass_guard": "walls surround the exit lane; reaching the hatch requires passing the one-way tile in its shown direction",
        },
    },
    3: {
        "layout": [
            "##########",
            "#P..S#...#",
            "#.##G#.#E#",
            "#.##.##..#",
            "#...v....#",
            "##########",
        ],
        "player_start": (1, 1),
        "exit": (2, 8),
        "switches": [(1, 4)],
        "gates": [(2, 4)],
        "switch_links": [{"switch": (1, 4), "targets": [(2, 4)]}],
        "one_ways": {(4, 4): 2},
        "patrol_route": [(4, 6), (3, 6), (2, 6), (1, 6), (2, 6), (3, 6)],
        "patrol_start_index": 0,
        "active_tags": ["patrol", "switch", "one-way"],
        "budget": 22,
        "fog_radius": None,
        "goal_requirements": {"switches_on": 1, "one_way_passes": 1},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "the exit corridor is behind a switch-opened gate and a downward one-way flap that commits the player to the patrol lane",
            "dependencies": ["activate pink switch", "pass the linked green gate", "enter the purple one-way from above", "use the alcove to desynchronize the grinder", "enter blue exit hatch"],
            "feedback": "the switch fills, the gate shows pink open markers, and the purple down arrow marks the irreversible drop",
            "bypass_guard": "walls surround the exit approach; the player cannot reach the hatch without both opening the gate and passing the one-way tile",
        },
    },
    4: {
        "layout": [
            "##########",
            "#P..F#..E#",
            "#.##G#.#.#",
            "#S..v....#",
            "#.###....#",
            "######.###",
            "##########",
        ],
        "player_start": (1, 1),
        "exit": (1, 8),
        "fuses": [(1, 4)],
        "switches": [(3, 1)],
        "gates": [(2, 4)],
        "switch_links": [{"switch": (3, 1), "targets": [(2, 4)]}],
        "one_ways": {(3, 4): 2},
        "patrol_route": [(3, 6), (4, 6), (5, 6), (4, 6)],
        "patrol_start_index": 0,
        "active_tags": ["patrol", "collectible", "switch", "one-way"],
        "budget": 34,
        "fog_radius": None,
        "goal_requirements": {"required_fuses": 1, "switches_on": 1, "one_way_passes": 1},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "both a fuse and a distant switch must open the only gate before the downward one-way commits the player to the grinder lane",
            "dependencies": ["collect yellow fuse", "activate pink switch", "return to the green gate after both prerequisites", "drop through the purple one-way", "use the side pocket to time the red grinder", "enter blue exit hatch"],
            "feedback": "the fuse disappears, the switch fills, the gate opens with shared pink/green markers, and the purple arrow shows the forced drop",
            "bypass_guard": "walls and the closed gate isolate the exit lane; the player cannot reach the hatch without the visible fuse, switch, and one-way passage",
        },
    },
    5: {
        "layout": [
            "##########",
            "#P..F#####",
            "#.##.#####",
            "#S..G>..E#",
            "#.##.#####",
            "#...F#####",
            "##########",
        ],
        "player_start": (1, 1),
        "exit": (3, 8),
        "fuses": [(1, 4), (5, 4)],
        "switches": [(3, 1)],
        "gates": [(3, 4)],
        "switch_links": [{"switch": (3, 1), "targets": [(3, 4)]}],
        "one_ways": {(3, 5): 4},
        "patrol_route": [(3, 6), (2, 6), (1, 6), (2, 6)],
        "patrol_start_index": 0,
        "active_tags": ["patrol", "collectible", "switch", "one-way", "fog"],
        "budget": 42,
        "fog_radius": 12,
        "goal_requirements": {"required_fuses": 2, "switches_on": 1, "one_way_passes": 1},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "two fuses and a switch must open the only gate before a right-facing one-way and vertical grinder lane",
            "dependencies": ["collect upper fuse", "activate pink switch", "collect lower fuse", "return to the linked gate", "enter the purple one-way from the left", "time the red grinder", "enter blue exit hatch"],
            "feedback": "each fuse disappears, the switch fills, the linked gate opens, and fog still leaves the local grinder and purple arrow readable",
            "bypass_guard": "walls and the closed gate isolate the exit lane; every route to the hatch passes through the one-way tile",
        },
    },
    6: {
        "layout": [
            "##########",
            "#P..F#####",
            "#.##.#####",
            "#S..G>..E#",
            "#.##.#####",
            "#...S#####",
            "#.########",
            "##########",
        ],
        "player_start": (1, 1),
        "exit": (3, 8),
        "fuses": [(1, 4)],
        "switches": [(3, 1), (5, 4)],
        "gates": [(3, 4)],
        "switch_links": [{"switch": (3, 1), "targets": [(3, 4)]}, {"switch": (5, 4), "targets": [(3, 4)]}],
        "one_ways": {(3, 5): 4},
        "patrol_route": [(3, 6), (2, 6), (1, 6), (2, 6)],
        "patrol_start_index": 0,
        "active_tags": ["patrol", "collectible", "switch", "one-way", "fog"],
        "budget": 40,
        "fog_radius": 10,
        "goal_requirements": {"required_fuses": 1, "switches_on": 2, "one_way_passes": 1},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "two switches and a fuse are all required before the only green gate opens into the one-way grinder lane",
            "dependencies": ["collect the upper fuse", "activate the first pink switch", "activate the lower pink switch", "return to the linked gate", "enter the purple one-way from the left", "time the red grinder", "enter blue exit hatch"],
            "feedback": "the fuse disappears, both switches fill, and the linked gate opens only after both pink controls and the fuse are satisfied",
            "bypass_guard": "walls and the closed gate isolate the exit lane; every route to the hatch passes through the gate and the one-way tile",
        },
    },
    7: {
        "layout": [
            "##########",
            "#P..F#####",
            "#.##.#####",
            "#S..G>..E#",
            "#.##.#####",
            "#...S#####",
            "#.########",
            "#...F#####",
            "##########",
        ],
        "player_start": (1, 1),
        "exit": (3, 8),
        "fuses": [(1, 4), (7, 4)],
        "switches": [(3, 1), (5, 4)],
        "gates": [(3, 4)],
        "switch_links": [{"switch": (3, 1), "targets": [(3, 4)]}, {"switch": (5, 4), "targets": [(3, 4)]}],
        "one_ways": {(3, 5): 4},
        "patrol_route": [(3, 6), (2, 6), (1, 6), (2, 6)],
        "patrol_start_index": 0,
        "active_tags": ["patrol", "collectible", "switch", "one-way", "fog"],
        "budget": 52,
        "fog_radius": 9,
        "goal_requirements": {"required_fuses": 2, "switches_on": 2, "one_way_passes": 1},
        "design_contract": {
            "success_trigger": "enter_exit",
            "primary_blocker": "two fuses and two switches must all be handled before the final one-way grinder lane opens",
            "dependencies": ["collect upper fuse", "activate first switch", "activate lower switch", "collect deep fuse", "return to the linked gate", "enter one-way from the left", "time final grinder", "enter exit"],
            "feedback": "two fuses disappear, both switches fill, the gate opens, and the foggy one-way/grinder lane remains locally visible",
            "bypass_guard": "the closed gate and one-way tile form the only route to the hatch; all visible requirements must be complete before the gate opens",
        },
    },
}


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    """Deterministic history state update (DreamerV3 sequence model)."""
    base = a_t[0] if isinstance(a_t, tuple) else a_t
    if base not in get_available_actions():
        return copy.deepcopy(h_t)

    if base == 0:
        h0, _ = get_initial_state(h_t.get("level", 0))
        return h0

    if h_t.get("dead", False) or h_t.get("complete", False) or h_t.get("budget_remaining", 0) <= 0:
        return copy.deepcopy(h_t)

    if base not in DIRS:
        return copy.deepcopy(h_t)

    level = h_t["level"]
    cfg = LEVELS[level]
    tags = cfg.get("active_tags", [])
    layout = cfg["layout"]
    nr = h_t["player_r"] + DIRS[base][0]
    nc = h_t["player_c"] + DIRS[base][1]

    if nr < 0 or nr >= len(layout) or nc < 0 or nc >= len(layout[0]):
        return copy.deepcopy(h_t)

    tile = layout[nr][nc]
    if tile == "#":
        return copy.deepcopy(h_t)
    if tile == "G" and not h_t.get("gate_open", False):
        return copy.deepcopy(h_t)
    one_ways = cfg.get("one_ways", {})
    if (nr, nc) in one_ways and one_ways[(nr, nc)] != base:
        return copy.deepcopy(h_t)

    new_h = copy.deepcopy(h_t)
    new_h["player_r"] = nr
    new_h["player_c"] = nc
    new_h["step"] += 1
    new_h["budget_remaining"] -= 1
    new_h["last_action"] = base

    # Stepping into the current grinder is a real losing collision.
    route = cfg.get("patrol_route", [])
    if "patrol" in tags and route:
        current_patrol = route[new_h["patrol_idx"]]
        if (nr, nc) == current_patrol:
            new_h["dead"] = True
            return new_h

    if "collectible" in tags and (nr, nc) in cfg.get("fuses", []):
        if (nr, nc) not in new_h["collected_fuses"]:
            new_h["collected_fuses"].append((nr, nc))
        new_h["required_fuses"] = len(new_h["collected_fuses"])

    if "switch" in tags and (nr, nc) in cfg.get("switches", []):
        if (nr, nc) not in new_h["activated_switches"]:
            new_h["activated_switches"].append((nr, nc))
        new_h["switches_on"] = len(new_h["activated_switches"])

    if "one-way" in tags and (nr, nc) in cfg.get("one_ways", {}) and new_h.get("one_way_passes", 0) == 0:
        new_h["one_way_passes"] = 1

    req = cfg.get("goal_requirements", {})
    if cfg.get("gates", []):
        gate_ready = True
        if new_h.get("required_fuses", 0) < req.get("required_fuses", 0):
            gate_ready = False
        if new_h.get("switches_on", 0) < req.get("switches_on", 0):
            gate_ready = False
        if gate_ready:
            new_h["gate_open"] = True

    if check_level_complete(new_h, {}, level):
        new_h["complete"] = True
        return new_h

    if "patrol" in tags and route:
        new_h["patrol_idx"] = (new_h["patrol_idx"] + 1) % len(route)
        if route[new_h["patrol_idx"]] == (new_h["player_r"], new_h["player_c"]):
            new_h["dead"] = True

    if new_h["budget_remaining"] <= 0 and not new_h.get("complete", False):
        new_h["dead"] = True

    return new_h


def predict(h_t: dict) -> dict:
    """Return minimal/empty z_t. This game is fully deterministic."""
    return {}


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    """Check if the current level's goal has been achieved."""
    cfg = LEVELS[level]
    req = cfg.get("goal_requirements", {})
    if h_t.get("dead", False):
        return False
    if h_t.get("budget_remaining", 0) < 0:
        return False
    for key, needed in req.items():
        if h_t.get(key, 0) < needed:
            return False
    return (h_t.get("player_r"), h_t.get("player_c")) == cfg["exit"]


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    """Render the current state as a 32x32 grid."""
    grid = [[BG_COLOR for _ in range(32)] for _ in range(32)]
    cfg = LEVELS[h_t["level"]]

    def _draw_entity(grid, row, col, entity_type):
        sr = ORIGIN_R + row * CELL
        sc = ORIGIN_C + col * CELL
        if sr < 0 or sc < 0 or sr + 2 >= 32 or sc + 2 >= 32:
            return
        if entity_type == "wall":
            for rr in range(3):
                for cc in range(3):
                    grid[sr + rr][sc + cc] = COLORS["wall"]
        elif entity_type == "route":
            for rr in range(3):
                grid[sr + rr][sc + 1] = COLORS["hazard"]
        elif entity_type == "exit":
            for rr in range(3):
                for cc in range(3):
                    if rr in (0, 2) or cc in (0, 2):
                        grid[sr + rr][sc + cc] = COLORS["exit"]
        elif entity_type == "fuse":
            for rr, cc in [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]:
                grid[sr + rr][sc + cc] = COLORS["fuse"]
            grid[sr + 1][sc + 1] = COLORS["white"]
        elif entity_type == "switch_off":
            for rr in range(3):
                for cc in range(3):
                    if rr in (0, 2) or cc in (0, 2):
                        grid[sr + rr][sc + cc] = COLORS["switch"]
            grid[sr + 1][sc + 1] = COLORS["background"]
        elif entity_type == "switch_on":
            for rr, cc in [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]:
                grid[sr + rr][sc + cc] = COLORS["switch"]
            grid[sr + 1][sc + 1] = COLORS["white"]
        elif entity_type == "gate_closed":
            for rr in range(3):
                for cc in range(3):
                    grid[sr + rr][sc + cc] = COLORS["gate"] if (rr in (0, 2) or cc in (0, 2)) else COLORS["wall"]
        elif entity_type == "gate_open":
            for rr, cc in [(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)]:
                grid[sr + rr][sc + cc] = COLORS["gate"]
        elif entity_type == "gate_switch_closed":
            for rr in range(3):
                for cc in range(3):
                    grid[sr + rr][sc + cc] = COLORS["gate"] if (rr in (0, 2) or cc in (0, 2)) else COLORS["wall"]
            grid[sr][sc + 1] = COLORS["switch"]
            grid[sr + 2][sc + 1] = COLORS["switch"]
        elif entity_type == "gate_switch_open":
            for rr, cc in [(0, 0), (0, 2), (2, 0), (2, 2), (1, 1), (0, 1), (2, 1)]:
                grid[sr + rr][sc + cc] = COLORS["switch"] if cc == 1 else COLORS["gate"]
        elif entity_type == "one_way_right":
            for rr, cc in [(0, 0), (1, 0), (2, 0), (1, 1), (0, 2), (1, 2), (2, 2)]:
                grid[sr + rr][sc + cc] = COLORS["one_way"]
            grid[sr + 1][sc + 2] = COLORS["white"]
        elif entity_type == "one_way_down":
            for rr, cc in [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (2, 2)]:
                grid[sr + rr][sc + cc] = COLORS["one_way"]
            grid[sr + 2][sc + 1] = COLORS["white"]
        elif entity_type == "patrol":
            for rr, cc in [(0, 0), (1, 1), (2, 2), (0, 2), (2, 0)]:
                grid[sr + rr][sc + cc] = COLORS["hazard"]
        elif entity_type == "player":
            for rr, cc in [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]:
                grid[sr + rr][sc + cc] = COLORS["player"]
            grid[sr + 1][sc + 1] = COLORS["white"]
        elif entity_type == "dead":
            for rr in range(3):
                for cc in range(3):
                    grid[sr + rr][sc + cc] = COLORS["hazard"]
            grid[sr + 1][sc + 1] = COLORS["white"]

    # Static board.
    for r, line in enumerate(cfg["layout"]):
        for c, ch in enumerate(line):
            if ch == "#":
                _draw_entity(grid, r, c, "wall")

    # Visible patrol rail as a connected line.
    for pos in cfg.get("patrol_route", []):
        _draw_entity(grid, pos[0], pos[1], "route")

    _draw_entity(grid, cfg["exit"][0], cfg["exit"][1], "exit")

    for sw in cfg.get("switches", []):
        _draw_entity(grid, sw[0], sw[1], "switch_on" if sw in h_t.get("activated_switches", []) else "switch_off")

    for ow, direction in cfg.get("one_ways", {}).items():
        _draw_entity(grid, ow[0], ow[1], "one_way_right" if direction == 4 else "one_way_down")

    for g in cfg.get("gates", []):
        if "switch" in cfg.get("active_tags", []):
            gate_type = "gate_switch_open" if h_t.get("gate_open", False) else "gate_switch_closed"
        else:
            gate_type = "gate_open" if h_t.get("gate_open", False) else "gate_closed"
        _draw_entity(grid, g[0], g[1], gate_type)

    for fuse in cfg.get("fuses", []):
        if fuse not in h_t.get("collected_fuses", []):
            _draw_entity(grid, fuse[0], fuse[1], "fuse")

    route = cfg.get("patrol_route", [])
    if "patrol" in cfg.get("active_tags", []) and route:
        pr, pc = route[h_t.get("patrol_idx", 0)]
        _draw_entity(grid, pr, pc, "patrol")

    _draw_entity(grid, h_t["player_r"], h_t["player_c"], "dead" if h_t.get("dead", False) else "player")

    # Budget HUD on row 0.
    max_budget = max(1, cfg["budget"])
    remaining = max(0, min(32, int((h_t.get("budget_remaining", 0) * 32) / max_budget)))
    hud_color = COLORS["hazard"] if h_t.get("dead", False) else COLORS["player"]
    for c in range(remaining):
        grid[0][c] = hud_color
    for c in range(remaining, 32):
        grid[0][c] = BG_COLOR

    fog_radius = cfg.get("fog_radius", None)
    if fog_radius is not None:
        pr = ORIGIN_R + h_t["player_r"] * CELL + 1
        pc = ORIGIN_C + h_t["player_c"] * CELL + 1
        for r in range(32):
            for c in range(32):
                if abs(r - pr) + abs(c - pc) > fog_radius:
                    grid[r][c] = BG_COLOR

    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    """Get the initial (h_t, z_t) for a given level."""
    cfg = LEVELS[level]
    start = cfg["player_start"]
    h_t = {
        "level": level,
        "step": 0,
        "player_r": start[0],
        "player_c": start[1],
        "patrol_idx": cfg.get("patrol_start_index", 0),
        "collected_fuses": [],
        "required_fuses": 0,
        "activated_switches": [],
        "switches_on": 0,
        "one_way_passes": 0,
        "gate_open": False if cfg.get("gates", []) else True,
        "budget_remaining": cfg["budget"],
        "dead": False,
        "complete": False,
        "last_action": None,
    }
    return h_t, predict(h_t)


def get_available_actions() -> list[int]:
    """Return available action integers for this game."""
    return [0, 1, 2, 3, 4]


def solve_level(level: int) -> list:
    """Return a fixed sequence of actions that solves this level."""
    if level == 0:
        return [4, 4, 4, 2, 2, 4, 4, 4]
    if level == 1:
        return [4, 4, 4, 2, 2, 4, 4, 4, 4, 2]
    if level == 2:
        return [4, 4, 4, 3, 4, 4, 4, 4, 4]
    if level == 3:
        return [4, 4, 4, 2, 2, 2, 4, 4, 4, 1, 4, 1]
    if level == 4:
        return [4, 4, 4, 3, 3, 3, 2, 2, 1, 1, 4, 4, 4, 2, 2, 4, 2, 1, 4, 4, 4, 1, 1]
    if level == 5:
        return [4, 4, 4, 3, 3, 3, 2, 2, 2, 2, 4, 4, 4, 3, 3, 3, 1, 1, 4, 4, 4, 4, 4, 4, 4]
    if level == 6:
        return [2, 1, 4, 4, 4, 3, 3, 3, 2, 2, 2, 2, 4, 4, 4, 1, 1, 4, 4, 4, 4]
    if level == 7:
        return [4, 4, 4, 3, 3, 3, 2, 2, 2, 2, 4, 4, 4, 3, 3, 3, 2, 2, 4, 4, 4, 3, 3, 3, 1, 1, 1, 1, 4, 4, 4, 1, 2, 4, 4, 4, 4]
    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Rs0427(_FunctionalArcGame):
    GAME_ID = "rs0427-2c8b97d9"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
