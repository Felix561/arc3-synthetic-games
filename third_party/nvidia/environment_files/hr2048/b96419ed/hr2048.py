# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the hr2048/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy

BG_COLOR = 5
COLORS = {
    "owned": 8,
    "spark": 6,
    "phone": 12,
    "heart": 14,
    "heart_inner": 10,
    "cache": 11,
    "wall": 2,
    "wall_dark": 3,
    "thick": 15,
    "white": 0,
    "maroon": 13,
    "echo": 7,
}

CELL = 6
ORIGIN_R = 10
ORIGIN_C = 10

LEVELS = {
    0: {
        "board_h": 7,
        "board_w": 7,
        "budget": 16,
        "start_credits": 8,
        "claim_quota": 9,
        "phone": (3, 1),
        "hearts": [(1, 5), (5, 5)],
        "caches": {(2, 3): 4},
        "thick": {(3, 3): 3, (4, 3): 3},
        "walls": [(0, 0), (0, 1), (0, 2), (0, 6), (6, 0), (6, 1), (6, 6),
                  (1, 1), (5, 1)],
        "fog_radius": None,
        "active_tags": [],
        "goal_requirements": {"controlled_hearts": 2, "claimed_count": 11},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "complete",
            "primary_blocker": "hearts are separated by unclaimed void and limited signal credits",
            "dependencies": ["extend from phone", "claim emotion cache", "route around thick void", "claim both hearts"],
            "feedback": "claimed cells turn red, cache becomes owned, hearts fill red when controlled",
            "bypass_guard": "a heart click is only valid when adjacent to already owned territory",
        },
    },
    1: {
        "board_h": 8,
        "board_w": 8,
        "budget": 22,
        "start_credits": 9,
        "claim_quota": 14,
        "phone": (4, 1),
        "hearts": [(1, 6), (6, 6)],
        "caches": {(5, 3): 6, (2, 4): 3},
        "thick": {(4, 3): 4, (3, 4): 4, (4, 4): 4, (5, 5): 4},
        "walls": [(0, 0), (0, 1), (0, 2), (0, 7), (1, 1), (1, 3), (2, 1),
                  (3, 1), (3, 3), (5, 1), (6, 1), (7, 0), (7, 1), (7, 7)],
        "fog_radius": None,
        "active_tags": ["energy"],
        "goal_requirements": {"controlled_hearts": 2, "claimed_count": 16, "collected_caches_count": 2},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "complete",
            "primary_blocker": "the direct fork crosses expensive thick void and runs out of credits before both hearts",
            "dependencies": ["take lower cache first", "use the cache to fund the upper branch", "claim second cache", "control both hearts"],
            "feedback": "yellow caches vanish into red owned cells and the HUD credit ticks increase",
            "bypass_guard": "both hearts require connected claimed routes and the required cache count is visible in claimed cache cells",
        },
    },
    2: {
        "board_h": 8,
        "board_w": 9,
        "budget": 27,
        "start_credits": 10,
        "claim_quota": 17,
        "phone": (4, 1),
        "hearts": [(1, 7), (6, 7)],
        "caches": {(6, 3): 6, (2, 5): 4},
        "thick": {(4, 3): 8, (3, 3): 5, (2, 3): 5, (5, 5): 4, (5, 6): 4},
        "walls": [(0, 0), (0, 1), (0, 2), (0, 8), (1, 1), (1, 3), (2, 1),
                  (3, 1), (3, 5), (4, 5), (5, 1), (5, 3), (7, 0), (7, 1), (7, 8)],
        "fog_radius": None,
        "active_tags": ["energy", "undo"],
        "goal_requirements": {"controlled_hearts": 2, "claimed_count": 17, "collected_caches_count": 2},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "complete",
            "primary_blocker": "a visible expensive purple branch can consume the signal reserve before any cache is reached",
            "dependencies": ["test or avoid the costly branch", "use undo to recover from the costly claim", "collect lower cache", "collect upper cache", "control both hearts"],
            "feedback": "undo restores the previous red territory and credits; caches refill the HUD credit ticks",
            "bypass_guard": "both hearts and the cache requirement require connected claimed routes; early heart control without both caches does not satisfy visible cache indicators",
        },
    },
    3: {
        "board_h": 9,
        "board_w": 9,
        "budget": 30,
        "start_credits": 10,
        "claim_quota": 19,
        "phone": (4, 1),
        "relay_phones": [(4, 6)],
        "hearts": [(1, 7), (7, 7)],
        "caches": {(6, 3): 5, (2, 3): 4},
        "thick": {(3, 3): 4, (5, 3): 4, (3, 5): 5, (5, 5): 5},
        "walls": [(0, 0), (0, 1), (0, 2), (0, 8), (1, 1), (1, 5), (2, 1), (2, 5),
                  (3, 1), (3, 6), (4, 3), (5, 1), (5, 6), (6, 1), (6, 5),
                  (7, 1), (8, 0), (8, 1), (8, 8)],
        "fog_radius": None,
        "active_tags": ["energy", "undo", "relay"],
        "goal_requirements": {"controlled_hearts": 2, "claimed_count": 20, "collected_caches_count": 2, "relay_phones_opened": 1},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "complete",
            "primary_blocker": "the far hearts are too costly unless the orange relay phone is connected and reopened",
            "dependencies": ["collect one cache to fund the crossing", "claim the relay phone", "use the relay as a new adjacency source", "collect second cache", "control both hearts"],
            "feedback": "the relay phone changes from orange outline to red-owned phone and a new red branch can grow from it",
            "bypass_guard": "far hearts remain unreachable through walls unless the connected relay corridor is claimed first",
        },
    },
    4: {
        "board_h": 9,
        "board_w": 9,
        "budget": 22,
        "start_credits": 9,
        "claim_quota": 22,
        "phone": (4, 1),
        "relay_phones": [(4, 6)],
        "hearts": [(1, 7), (7, 7)],
        "caches": {(6, 3): 4, (2, 3): 4},
        "thick": {(3, 2): 4, (3, 5): 4, (5, 5): 4, (4, 7): 4},
        "flood": {
            (5, 4): [(6, 4), (6, 5)],
            (3, 4): [(2, 4), (2, 3)],
            (3, 6): [(2, 6), (2, 7)]
        },
        "walls": [(0, 0), (0, 1), (0, 2), (0, 8), (1, 1), (1, 4), (2, 1),
                  (3, 1), (4, 3), (5, 1), (6, 1), (7, 1), (8, 0), (8, 1), (8, 8)],
        "fog_radius": None,
        "active_tags": ["energy", "undo", "relay", "flood"],
        "goal_requirements": {"controlled_hearts": 2, "claimed_count": 22, "collected_caches_count": 2, "relay_phones_opened": 1, "flood_cells_claimed": 9},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "complete",
            "primary_blocker": "manual claiming cannot cover both hearts, relay, caches, and quota inside the signal budget unless flood arrows are used",
            "dependencies": ["collect lower cache", "trigger lower flood arrow", "open relay phone", "trigger upper cache flood", "trigger upper heart flood", "control both hearts"],
            "feedback": "light-blue flood arrows turn red and extend red territory along their marked channel in one click",
            "bypass_guard": "the exact visible flood-channel cells, relay phone, caches, and hearts must all be owned; walls block direct shortcuts",
        },
    },
    5: {
        "board_h": 9,
        "board_w": 9,
        "budget": 22,
        "start_credits": 9,
        "claim_quota": 19,
        "phone": (7, 1),
        "relay_phones": [(3, 6)],
        "hearts": [(1, 7), (7, 7)],
        "caches": {(5, 2): 4, (2, 4): 3},
        "thick": {(7, 3): 5, (6, 3): 4, (4, 5): 4, (2, 5): 4, (6, 7): 3},
        "flood": {
            (5, 3): [(5, 4), (4, 4)],
            (3, 7): [(2, 7)]
        },
        "walls": [(0, 0), (0, 1), (0, 8), (1, 1), (2, 1), (2, 6), (3, 1),
                  (3, 3), (4, 3), (5, 5), (6, 1), (6, 5), (8, 0), (8, 1), (8, 8)],
        "fog_radius": 2,
        "active_tags": ["energy", "undo", "relay", "flood", "fog"],
        "goal_requirements": {"controlled_hearts": 2, "claimed_count": 19, "collected_caches_count": 2, "relay_phones_opened": 1, "flood_cells_claimed": 5},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "complete",
            "primary_blocker": "fog hides the relay and top cache until the player spends credits extending a remembered branch",
            "dependencies": ["secure the visible lower cache", "trigger the visible lower flood channel", "push into fog toward the upper cache", "open the relay phone", "split from relay to both hearts"],
            "feedback": "new district cells emerge from gray fog as red territory approaches; cache and flood markers become visible before use",
            "bypass_guard": "hearts, relay, caches, and all marked flood-channel cells must be visibly owned; fog does not create hidden completion",
        },
    },
    6: {
        "board_h": 9,
        "board_w": 9,
        "budget": 27,
        "start_credits": 10,
        "claim_quota": 24,
        "phone": (7, 1),
        "relay_phones": [(4, 4), (2, 6)],
        "hearts": [(1, 7), (7, 7), (1, 3)],
        "caches": {(6, 2): 3, (4, 2): 4, (2, 4): 4},
        "thick": {(5, 3): 4, (4, 5): 4, (3, 6): 4, (6, 7): 4, (2, 2): 4},
        "flood": {
            (5, 4): [(5, 5), (5, 6)],
            (3, 4): [(2, 4), (2, 5)],
            (2, 6): [(2, 7), (1, 7)],
            (2, 3): [(1, 3)]
        },
        "walls": [(0, 0), (0, 1), (0, 8), (1, 1), (2, 1), (3, 1),
                  (3, 3), (4, 3), (5, 1), (6, 1), (6, 5), (8, 0), (8, 1), (8, 8)],
        "fog_radius": 2,
        "active_tags": ["energy", "undo", "relay", "flood", "fog", "multiheart"],
        "goal_requirements": {"controlled_hearts": 3, "claimed_count": 24, "collected_caches_count": 3, "relay_phones_opened": 2, "flood_cells_claimed": 11},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "complete",
            "primary_blocker": "three hearts sit behind different resource branches; opening only one relay leaves the final heart unfunded",
            "dependencies": ["claim lower cache", "detour to left cache", "open central relay", "collect upper cache by flood", "open upper relay", "use both heart floods and finish bottom heart"],
            "feedback": "two orange relay phones become owned phone anchors; three heart HUD pips fill as branches are controlled",
            "bypass_guard": "all three hearts, three caches, two relay phones, and marked flood cells must be owned through adjacency; fog only hides future choices",
        },
    },
    7: {
        "board_h": 9,
        "board_w": 9,
        "budget": 31,
        "start_credits": 11,
        "claim_quota": 27,
        "phone": (1, 1),
        "relay_phones": [(4, 4), (6, 6)],
        "hearts": [(1, 7), (7, 7), (7, 2)],
        "caches": {(2, 3): 4, (5, 4): 4, (6, 2): 5},
        "thick": {(1, 3): 5, (3, 3): 4, (4, 5): 4, (5, 6): 4, (7, 5): 4, (5, 2): 4},
        "flood": {
            (2, 4): [(3, 4), (4, 4)],
            (5, 4): [(5, 5), (5, 6)],
            (6, 6): [(6, 7), (7, 7)],
            (6, 3): [(7, 3), (7, 2)]
        },
        "walls": [(0, 0), (0, 1), (0, 8), (1, 5), (2, 1), (2, 6), (3, 1),
                  (3, 6), (4, 1), (4, 3), (5, 1), (6, 5), (8, 0), (8, 1), (8, 8)],
        "fog_radius": 2,
        "active_tags": ["energy", "undo", "relay", "flood", "fog", "multiheart", "final"],
        "goal_requirements": {"controlled_hearts": 3, "claimed_count": 27, "collected_caches_count": 3, "relay_phones_opened": 2, "flood_cells_claimed": 12},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "complete",
            "primary_blocker": "the final city has three heart districts and two relay phones; spending on the tempting thick top road leaves too few credits for the lower hearts",
            "dependencies": ["take the cheap cache route", "trigger the central flood to open the first relay", "fund and open the lower relay", "use the relay flood for the far heart", "detour to the lower cache and heart flood", "finish the top heart"],
            "feedback": "fog peels back around each claimed branch, relay phones turn red, and three heart pips fill on the HUD",
            "bypass_guard": "all three hearts, all three caches, both relay phones, and every marked flood channel must be visibly owned through connected territory",
        },
    }
}


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    """Deterministic history state update (DreamerV3 sequence model)."""
    if isinstance(a_t, tuple):
        base = a_t[0] if a_t else None
    else:
        base = a_t
    if base not in get_available_actions():
        return copy.deepcopy(h_t)

    level = h_t["level"]
    cfg = LEVELS[level]

    if base == 0:
        fresh, _ = get_initial_state(level)
        return fresh

    if base == 7:
        if "undo" not in cfg.get("active_tags", []) or not h_t.get("undo_stack"):
            return copy.deepcopy(h_t)
        prev = copy.deepcopy(h_t["undo_stack"][-1])
        prev["undo_stack"] = copy.deepcopy(h_t["undo_stack"][:-1])
        prev["last_click"] = None
        return prev

    if base != 6 or not isinstance(a_t, tuple) or len(a_t) != 3:
        return copy.deepcopy(h_t)

    x, y = int(a_t[1]), int(a_t[2])
    r = (y - ORIGIN_R) // CELL
    c = (x - ORIGIN_C) // CELL
    if not (0 <= r < cfg["board_h"] and 0 <= c < cfg["board_w"]):
        return copy.deepcopy(h_t)
    cell = (r, c)
    if cell in cfg["walls"] or cell in h_t["claimed"]:
        return copy.deepcopy(h_t)

    claimed = set(tuple(p) for p in h_t["claimed"])
    adjacent = False
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if (r + dr, c + dc) in claimed:
            adjacent = True
            break
    if not adjacent:
        return copy.deepcopy(h_t)

    cost = cfg["thick"].get(cell, 1)
    if h_t["credits"] < cost or h_t["budget_left"] <= 0:
        return copy.deepcopy(h_t)

    n = copy.deepcopy(h_t)
    if "undo" in cfg.get("active_tags", []):
        snap = copy.deepcopy(h_t)
        snap["undo_stack"] = []
        n["undo_stack"] = (copy.deepcopy(h_t.get("undo_stack", [])) + [snap])[-50:]
    n["claimed"].append(cell)
    n["credits"] -= cost
    if cell in cfg["caches"]:
        n["credits"] += cfg["caches"][cell]
        if cell not in n["collected_caches"]:
            n["collected_caches"].append(cell)
    if "flood" in cfg.get("active_tags", []) and cell in cfg.get("flood", {}):
        for fcell in cfg.get("flood", {}).get(cell, []):
            if fcell not in set(tuple(p) for p in n["claimed"]) and fcell not in cfg["walls"]:
                n["claimed"].append(fcell)
                if fcell in cfg["caches"]:
                    n["credits"] += cfg["caches"][fcell]
                    if fcell not in n["collected_caches"]:
                        n["collected_caches"].append(fcell)
    claimed_after = set(tuple(p) for p in n["claimed"])
    n["controlled_hearts"] = sum(1 for h in cfg["hearts"] if h in claimed_after)
    n["claimed_count"] = len(n["claimed"])
    n["collected_caches_count"] = len(n.get("collected_caches", []))
    n["relay_phones_opened"] = sum(1 for p in cfg.get("relay_phones", []) if p in claimed_after)
    flood_cells = set(cfg.get("flood", {}).keys())
    for vals in cfg.get("flood", {}).values():
        for p in vals:
            flood_cells.add(p)
    n["flood_cells_claimed"] = sum(1 for p in flood_cells if p in claimed_after)
    n["budget_left"] -= 1
    n["step"] += 1
    n["last_click"] = cell
    n["complete"] = check_level_complete(n, {}, level)
    return n


def predict(h_t: dict) -> dict:
    """Return minimal/empty z_t. This game is fully deterministic."""
    return {}


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    """Check if the current level's goal has been achieved."""
    cfg = LEVELS[level]
    req = cfg.get("goal_requirements", {})
    claimed = set(tuple(p) for p in h_t.get("claimed", []))
    hearts_controlled = sum(1 for h in cfg.get("hearts", []) if h in claimed)
    if hearts_controlled < req.get("controlled_hearts", 0):
        return False
    if len(claimed) < req.get("claimed_count", 0):
        return False
    if len(h_t.get("collected_caches", [])) < req.get("collected_caches_count", 0):
        return False
    relay_opened = sum(1 for p in cfg.get("relay_phones", []) if p in claimed)
    if relay_opened < req.get("relay_phones_opened", 0):
        return False
    flood_cells = set(cfg.get("flood", {}).keys())
    for vals in cfg.get("flood", {}).values():
        for p in vals:
            flood_cells.add(p)
    flood_claimed = sum(1 for p in flood_cells if p in claimed)
    if flood_claimed < req.get("flood_cells_claimed", 0):
        return False
    return True


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    """Render the current state as a 64x64 grid."""
    grid = [[BG_COLOR for _ in range(64)] for _ in range(64)]
    cfg = LEVELS[h_t["level"]]

    def _draw_entity(grid, row, col, entity_type):
        top = ORIGIN_R + row * CELL
        left = ORIGIN_C + col * CELL
        if entity_type == "cell":
            for rr in range(top + 1, top + CELL - 1):
                for cc in range(left + 1, left + CELL - 1):
                    grid[rr][cc] = 4
        elif entity_type == "wall":
            for rr in range(top, top + CELL):
                for cc in range(left, left + CELL):
                    grid[rr][cc] = COLORS["wall_dark"] if (rr + cc) % 2 else COLORS["wall"]
        elif entity_type == "thick":
            for rr in range(top + 1, top + CELL - 1):
                for cc in range(left + 1, left + CELL - 1):
                    grid[rr][cc] = COLORS["thick"] if (rr - top + cc - left) % 3 == 0 else 4
        elif entity_type == "owned":
            for rr in range(top + 1, top + CELL - 1):
                for cc in range(left + 1, left + CELL - 1):
                    grid[rr][cc] = COLORS["owned"]
            grid[top + CELL // 2][left + CELL // 2] = COLORS["spark"]
        elif entity_type == "phone":
            for i in range(CELL):
                grid[top + i][left] = COLORS["phone"]
                grid[top + i][left + CELL - 1] = COLORS["phone"]
                grid[top][left + i] = COLORS["phone"]
                grid[top + CELL - 1][left + i] = COLORS["phone"]
            grid[top + 2][left + 2] = COLORS["white"]
            grid[top + 3][left + 3] = COLORS["white"]
        elif entity_type == "cache":
            pts = [(2, 3), (3, 2), (3, 3), (3, 4), (4, 3)]
            for pr, pc in pts:
                grid[top + pr][left + pc] = COLORS["cache"]
        elif entity_type == "heart":
            pts = [(1, 2), (1, 4), (2, 1), (2, 3), (2, 5), (3, 1), (3, 5), (4, 2), (4, 4), (5, 3)]
            for pr, pc in pts:
                grid[top + pr][left + pc] = COLORS["heart"]
            grid[top + 3][left + 3] = COLORS["heart_inner"]
        elif entity_type == "echo":
            for i in range(1, CELL - 1):
                grid[top + 1][left + i] = COLORS["echo"]
                grid[top + CELL - 2][left + i] = COLORS["echo"]
                grid[top + i][left + 1] = COLORS["echo"]
                grid[top + i][left + CELL - 2] = COLORS["echo"]
        elif entity_type == "flood":
            for i in range(1, CELL - 1):
                grid[top + CELL // 2][left + i] = COLORS["heart_inner"]
            grid[top + 1][left + CELL - 2] = COLORS["heart_inner"]
            grid[top + CELL - 2][left + CELL - 2] = COLORS["heart_inner"]
        elif entity_type == "flood_path":
            grid[top + 2][left + 2] = COLORS["heart_inner"]
            grid[top + 3][left + 3] = COLORS["heart_inner"]
            grid[top + 2][left + 3] = COLORS["heart_inner"]
            grid[top + 3][left + 2] = COLORS["heart_inner"]

    # static board cells
    for r in range(cfg["board_h"]):
        for c in range(cfg["board_w"]):
            _draw_entity(grid, r, c, "cell")
    for cell in cfg["thick"]:
        _draw_entity(grid, cell[0], cell[1], "thick")
    flood_marks = set(cfg.get("flood", {}).keys())
    for vals in cfg.get("flood", {}).values():
        for p in vals:
            flood_marks.add(p)
    for cell in flood_marks:
        if cell not in set(tuple(p) for p in h_t.get("claimed", [])):
            _draw_entity(grid, cell[0], cell[1], "flood" if cell in cfg.get("flood", {}) else "flood_path")
    for cell in cfg["walls"]:
        _draw_entity(grid, cell[0], cell[1], "wall")
    for cell in cfg["hearts"]:
        _draw_entity(grid, cell[0], cell[1], "heart")
    for cell in cfg["caches"]:
        if cell not in set(tuple(p) for p in h_t.get("claimed", [])):
            _draw_entity(grid, cell[0], cell[1], "cache")
    _draw_entity(grid, cfg["phone"][0], cfg["phone"][1], "phone")
    for cell in cfg.get("relay_phones", []):
        _draw_entity(grid, cell[0], cell[1], "phone")

    for cell in h_t.get("claimed", []):
        _draw_entity(grid, cell[0], cell[1], "owned")
    _draw_entity(grid, cfg["phone"][0], cfg["phone"][1], "phone")
    for cell in cfg.get("relay_phones", []):
        _draw_entity(grid, cell[0], cell[1], "phone")
    for cell in cfg["hearts"]:
        if cell in set(tuple(p) for p in h_t.get("claimed", [])):
            _draw_entity(grid, cell[0], cell[1], "owned")
            _draw_entity(grid, cell[0], cell[1], "heart")
    if "undo" in cfg.get("active_tags", []) and h_t.get("last_click"):
        _draw_entity(grid, h_t["last_click"][0], h_t["last_click"][1], "echo")

    # HUD: budget row and credits ticks
    max_budget = cfg["budget"]
    budget_pixels = int(32 * max(0, h_t.get("budget_left", 0)) / max_budget)
    for c in range(32):
        grid[1][c + 1] = COLORS["heart"] if c < budget_pixels else COLORS["wall_dark"]
    for c in range(min(20, max(0, h_t.get("credits", 0)))):
        grid[3][c + 1] = COLORS["cache"]
    for c in range(h_t.get("controlled_hearts", 0)):
        grid[5][c + 1] = COLORS["heart"]
    for c in range(h_t.get("collected_caches_count", len(h_t.get("collected_caches", [])))):
        grid[7][c + 1] = COLORS["white"]

    fog = cfg.get("fog_radius")
    if fog is not None:
        visible = set()
        for cr, cc in h_t.get("claimed", []):
            for rr in range(cr - fog, cr + fog + 1):
                for cc2 in range(cc - fog, cc + fog + 1):
                    if abs(rr - cr) + abs(cc2 - cc) <= fog:
                        visible.add((rr, cc2))
        for rr in range(ORIGIN_R, ORIGIN_R + cfg["board_h"] * CELL):
            for cc in range(ORIGIN_C, ORIGIN_C + cfg["board_w"] * CELL):
                br = (rr - ORIGIN_R) // CELL
                bc = (cc - ORIGIN_C) // CELL
                if (br, bc) not in visible:
                    grid[rr][cc] = 3
    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    """Get the initial (h_t, z_t) for a given level."""
    cfg = LEVELS[level]
    h_t = {
        "level": level,
        "step": 0,
        "budget_left": cfg["budget"],
        "credits": cfg["start_credits"],
        "claimed": [cfg["phone"]],
        "collected_caches": [],
        "collected_caches_count": 0,
        "relay_phones_opened": 0,
        "flood_cells_claimed": 0,
        "controlled_hearts": 0,
        "claimed_count": 1,
        "last_click": None,
        "undo_stack": [],
        "complete": False,
    }
    return h_t, predict(h_t)


def get_available_actions() -> list[int]:
    """Return available action integers for this game."""
    return [0, 6, 7]


def solve_level(level: int) -> list:
    """Return a fixed sequence of actions that solves this level."""
    def click_cell(r, c):
        return (6, ORIGIN_C + c * CELL + CELL // 2, ORIGIN_R + r * CELL + CELL // 2)
    if level == 0:
        path = [(3, 2), (2, 2), (2, 3), (2, 4), (1, 4), (1, 5), (3, 4), (4, 4), (5, 4), (5, 5)]
        return [click_cell(r, c) for r, c in path]
    if level == 1:
        path = [(4, 2), (5, 2), (5, 3), (5, 4), (6, 4), (6, 5), (6, 6),
                (4, 3), (3, 2), (2, 2), (2, 3), (2, 4), (2, 5), (1, 5), (1, 6)]
        return [click_cell(r, c) for r, c in path]
    if level == 2:
        probe = [click_cell(4, 2), click_cell(4, 3), 7]
        path = [(5, 2), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7),
                (5, 4), (4, 4), (3, 4), (2, 4), (2, 5), (2, 6), (1, 6), (1, 7)]
        return probe + [click_cell(r, c) for r, c in path]
    if level == 3:
        path = [(4, 2), (5, 2), (6, 2), (6, 3), (6, 4), (5, 4), (4, 4), (4, 5), (4, 6),
                (3, 4), (2, 4), (2, 3),
                (4, 7), (3, 7), (2, 7), (1, 7),
                (5, 7), (6, 7), (7, 7)]
        return [click_cell(r, c) for r, c in path]
    if level == 4:
        path = [(4, 2), (5, 2), (6, 2), (6, 3), (5, 3), (5, 4),
                (6, 6), (7, 6), (7, 7),
                (4, 4), (4, 5), (4, 6),
                (3, 4), (3, 6), (1, 7)]
        return [click_cell(r, c) for r, c in path]
    if level == 5:
        path = [(7, 2), (6, 2), (5, 2), (5, 3),
                (3, 4), (2, 4), (3, 5), (3, 6), (3, 7), (1, 7),
                (4, 6), (5, 6), (6, 6), (7, 6), (7, 7)]
        return [click_cell(r, c) for r, c in path]
    if level == 6:
        path = [(7, 2), (6, 2), (5, 2), (4, 2), (5, 3), (5, 4),
                (4, 4), (3, 4), (2, 4), (2, 3),
                (2, 6), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (6, 7), (5, 7)]
        return [click_cell(r, c) for r, c in path]
    if level == 7:
        path = [(1, 2), (2, 2), (2, 3), (2, 4),
                (5, 4), (6, 4), (6, 3), (6, 2),
                (5, 2), (6, 6),
                (2, 5), (3, 5), (1, 4),
                (5, 7), (4, 7), (3, 7), (2, 7), (1, 7)]
        return [click_cell(r, c) for r, c in path]
    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Hr2048(_FunctionalArcGame):
    GAME_ID = "hr2048-b96419ed"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
