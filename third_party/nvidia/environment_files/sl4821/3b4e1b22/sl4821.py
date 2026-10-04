# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the sl4821/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy
import random

BG_COLOR = 4
GRID_SIZE = 64
CELL_SIZE = 4
BOARD_CELLS = GRID_SIZE // CELL_SIZE

COLORS = {
    "socket": 0,
    "wall": 13,
    "source": 15,
    "lamp": 11,
    "pipe": 9,
    "loose": 6,
    "patrol": 13,
    "highlight": 0,
}

LEVELS = {
    0: {
        "rows": 5,
        "cols": 5,
        "source": {"r": 2, "c": 0, "side": "E"},
        "lamps": [{"r": 2, "c": 4, "side": "W"}],
        "walls": [],
        "patrols": [],
        "pieces": [
            {"r": 2, "c": 1, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 2, "c": 2, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 2, "c": 3, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
        ],
        "solve_order": [0, 1, 2],
        "wait_cell": (0, 0),
        "active_tags": [],
        "fog_radius": None,
        "budget": 20,
        "stochastic": ["flicker"],
    },
    1: {
        "rows": 6,
        "cols": 6,
        "source": {"r": 4, "c": 0, "side": "E"},
        "lamps": [{"r": 1, "c": 5, "side": "W"}],
        "walls": [],
        "patrols": [],
        "pieces": [
            {"r": 4, "c": 1, "kind": "elbow", "rot": 1, "loose": False, "target_rot": 3},
            {"r": 3, "c": 1, "kind": "straight", "rot": 1, "loose": False, "target_rot": 0},
            {"r": 2, "c": 1, "kind": "straight", "rot": 1, "loose": False, "target_rot": 0},
            {"r": 1, "c": 1, "kind": "elbow", "rot": 3, "loose": False, "target_rot": 1},
            {"r": 1, "c": 2, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 1, "c": 3, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 1, "c": 4, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
        ],
        "solve_order": [0, 1, 2, 3, 4, 5, 6],
        "wait_cell": (0, 0),
        "active_tags": [],
        "fog_radius": None,
        "budget": 19,
        "stochastic": ["flicker"],
    },
    2: {
        "rows": 7,
        "cols": 6,
        "source": {"r": 3, "c": 0, "side": "E"},
        "lamps": [
            {"r": 1, "c": 3, "side": "S"},
            {"r": 3, "c": 5, "side": "W"},
        ],
        "walls": [],
        "patrols": [],
        "pieces": [
            {"r": 3, "c": 1, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 3, "c": 2, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 3, "c": 3, "kind": "tee", "rot": 3, "loose": False, "target_rot": 0},
            {"r": 2, "c": 3, "kind": "straight", "rot": 1, "loose": False, "target_rot": 0},
            {"r": 3, "c": 4, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
        ],
        "solve_order": [2, 0, 1, 3, 4],
        "wait_cell": (0, 0),
        "active_tags": [],
        "fog_radius": None,
        "budget": 18,
        "stochastic": ["flicker"],
    },
    3: {
        "rows": 7,
        "cols": 7,
        "source": {"r": 4, "c": 0, "side": "E"},
        "lamps": [{"r": 4, "c": 6, "side": "W"}],
        "walls": [(5, 3)],
        "patrols": [],
        "pieces": [
            {"r": 4, "c": 1, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 4, "c": 2, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 1, "c": 3, "kind": "straight", "rot": 0, "loose": True, "target_rot": 1, "target_r": 4},
            {"r": 4, "c": 4, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 4, "c": 5, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
        ],
        "solve_order": [0, 1, 3, 4, 2],
        "wait_cell": (0, 0),
        "active_tags": ["gravity"],
        "fog_radius": None,
        "budget": 17,
        "stochastic": ["flicker"],
    },
    4: {
        "rows": 8,
        "cols": 8,
        "source": {"r": 5, "c": 0, "side": "E"},
        "lamps": [{"r": 3, "c": 6, "side": "S"}],
        "walls": [(6, 2), (6, 5)],
        "patrols": [],
        "pieces": [
            {"r": 5, "c": 1, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 1, "c": 2, "kind": "straight", "rot": 0, "loose": True, "target_rot": 1, "target_r": 5},
            {"r": 5, "c": 3, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 5, "c": 4, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 0, "c": 5, "kind": "straight", "rot": 0, "loose": True, "target_rot": 1, "target_r": 5},
            {"r": 5, "c": 6, "kind": "elbow", "rot": 1, "loose": False, "target_rot": 3},
            {"r": 4, "c": 6, "kind": "straight", "rot": 1, "loose": False, "target_rot": 0},
        ],
        "solve_order": [0, 2, 3, 6, 1, 4, 5],
        "wait_cell": (0, 0),
        "active_tags": ["gravity"],
        "fog_radius": None,
        "budget": 16,
        "stochastic": ["flicker"],
    },
    5: {
        "rows": 8,
        "cols": 8,
        "source": {"r": 3, "c": 0, "side": "E"},
        "lamps": [{"r": 3, "c": 6, "side": "W"}],
        "walls": [],
        "patrols": [
            {"path": [(2, 3), (3, 3), (4, 3)], "phase": 0},
        ],
        "pieces": [
            {"r": 3, "c": 1, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 3, "c": 2, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 3, "c": 3, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 3, "c": 4, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 3, "c": 5, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
        ],
        "solve_order": [0, 1, 3, 4, 2],
        "wait_cell": (0, 0),
        "active_tags": ["patrol"],
        "fog_radius": None,
        "budget": 15,
        "stochastic": ["flicker", "patrol_glint"],
    },
    6: {
        "rows": 9,
        "cols": 8,
        "source": {"r": 3, "c": 0, "side": "E"},
        "lamps": [
            {"r": 3, "c": 7, "side": "W"},
            {"r": 6, "c": 3, "side": "N"},
        ],
        "walls": [],
        "patrols": [
            {"path": [(2, 4), (3, 4), (4, 4)], "phase": 0},
            {"path": [(4, 2), (4, 3), (4, 4)], "phase": 1},
        ],
        "pieces": [
            {"r": 3, "c": 1, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 3, "c": 2, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 3, "c": 3, "kind": "tee", "rot": 1, "loose": False, "target_rot": 2},
            {"r": 3, "c": 4, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 3, "c": 5, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 3, "c": 6, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 4, "c": 3, "kind": "straight", "rot": 1, "loose": False, "target_rot": 0},
            {"r": 5, "c": 3, "kind": "straight", "rot": 1, "loose": False, "target_rot": 0},
        ],
        "solve_order": [2, 0, 1, 5, 4, 3, 7, 6],
        "wait_cell": (0, 0),
        "active_tags": ["patrol"],
        "fog_radius": None,
        "budget": 14,
        "stochastic": ["flicker", "patrol_glint"],
    },
    7: {
        "rows": 10,
        "cols": 10,
        "source": {"r": 5, "c": 0, "side": "E"},
        "lamps": [{"r": 2, "c": 6, "side": "S"}],
        "walls": [(6, 2), (6, 5)],
        "patrols": [
            {"path": [(3, 5), (3, 6), (3, 7)], "phase": 0},
        ],
        "pieces": [
            {"r": 5, "c": 1, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 0, "c": 2, "kind": "straight", "rot": 0, "loose": True, "target_rot": 1, "target_r": 5},
            {"r": 5, "c": 3, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 5, "c": 4, "kind": "straight", "rot": 0, "loose": False, "target_rot": 1},
            {"r": 1, "c": 5, "kind": "straight", "rot": 0, "loose": True, "target_rot": 1, "target_r": 5},
            {"r": 5, "c": 6, "kind": "elbow", "rot": 1, "loose": False, "target_rot": 3},
            {"r": 4, "c": 6, "kind": "straight", "rot": 1, "loose": False, "target_rot": 0},
            {"r": 3, "c": 6, "kind": "straight", "rot": 1, "loose": False, "target_rot": 0},
        ],
        "solve_order": [0, 2, 3, 6, 7, 1, 4, 5],
        "wait_cell": (0, 0),
        "active_tags": ["gravity", "patrol"],
        "fog_radius": None,
        "budget": 13,
        "stochastic": ["flicker", "patrol_glint"],
    },
}

DIR_VECTORS = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}
OPPOSITE = {"N": "S", "E": "W", "S": "N", "W": "E"}


def _board_offset(level):
    cfg = LEVELS[level]
    return (BOARD_CELLS - cfg["rows"]) // 2, (BOARD_CELLS - cfg["cols"]) // 2


def _cell_to_click(level, r, c):
    off_r, off_c = _board_offset(level)
    x = (off_c + c) * CELL_SIZE + 2
    y = (off_r + r) * CELL_SIZE + 2
    return (6, x, y)


def _piece_connections(kind, rot):
    rot = rot % 4
    if kind == "straight":
        return {"N", "S"} if rot % 2 == 0 else {"E", "W"}
    if kind == "elbow":
        return [{"N", "E"}, {"E", "S"}, {"S", "W"}, {"W", "N"}][rot]
    if kind == "tee":
        return [{"N", "E", "W"}, {"N", "E", "S"}, {"E", "S", "W"}, {"N", "S", "W"}][rot]
    return set()


def _endpoint_connections(endpoint):
    side = endpoint.get("side")
    if isinstance(side, list):
        return set(side)
    return {side}


def _piece_at(h_t, r, c):
    for idx, piece in enumerate(h_t["pieces"]):
        if piece["r"] == r and piece["c"] == c:
            return idx
    return None


def _static_occupied(level):
    cfg = LEVELS[level]
    occupied = set(tuple(pos) for pos in cfg.get("walls", []))
    occupied.add((cfg["source"]["r"], cfg["source"]["c"]))
    for lamp in cfg["lamps"]:
        occupied.add((lamp["r"], lamp["c"]))
    return occupied


def _patrol_positions(level, step):
    positions = []
    for patrol in LEVELS[level].get("patrols", []):
        path = patrol["path"]
        idx = (step + patrol.get("phase", 0)) % len(path)
        positions.append(tuple(path[idx]))
    return positions


def _blocked_cells(h_t, level):
    if "patrol" not in LEVELS[level].get("active_tags", []):
        return set()
    return set(_patrol_positions(level, h_t["step"]))


def _apply_gravity(new_h):
    level = new_h["level"]
    cfg = LEVELS[level]
    if "gravity" not in cfg.get("active_tags", []):
        return
    static_occ = _static_occupied(level)
    current_occ = {(p["r"], p["c"]): i for i, p in enumerate(new_h["pieces"])}
    can_fall = []
    for idx, state in enumerate(new_h["pieces"]):
        spec = cfg["pieces"][idx]
        if not spec.get("loose", False):
            continue
        below = (state["r"] + 1, state["c"])
        if state["r"] + 1 >= cfg["rows"]:
            continue
        if below in static_occ:
            continue
        blocker = current_occ.get(below)
        if blocker is not None:
            continue
        can_fall.append(idx)
    for idx in can_fall:
        new_h["pieces"][idx]["r"] += 1


def _draw_entity(grid, row, col, entity_type):
    def paint(dr, dc, color):
        rr = row + dr
        cc = col + dc
        if 0 <= rr < GRID_SIZE and 0 <= cc < GRID_SIZE and color is not None:
            grid[rr][cc] = color

    def draw_connector(base, directions, loose=False):
        for dr in (1, 2):
            for dc in (1, 2):
                paint(dr, dc, base)
        if "N" in directions:
            paint(0, 1, base)
            paint(0, 2, base)
            paint(1, 1, base)
            paint(1, 2, base)
            paint(0, 1, COLORS["highlight"])
        if "S" in directions:
            paint(3, 1, base)
            paint(3, 2, base)
            paint(2, 1, base)
            paint(2, 2, base)
            paint(3, 2, COLORS["highlight"])
        if "W" in directions:
            paint(1, 0, base)
            paint(2, 0, base)
            paint(1, 1, base)
            paint(2, 1, base)
            paint(2, 0, COLORS["highlight"])
        if "E" in directions:
            paint(1, 3, base)
            paint(2, 3, base)
            paint(1, 2, base)
            paint(2, 2, base)
            paint(1, 3, COLORS["highlight"])
        if loose:
            paint(1, 1, COLORS["highlight"])
            paint(2, 2, COLORS["highlight"])
        else:
            paint(1, 1, COLORS["highlight"])

    if entity_type == "socket":
        for i in range(4):
            paint(0, i, COLORS["socket"])
            paint(3, i, COLORS["socket"])
            paint(i, 0, COLORS["socket"])
            paint(i, 3, COLORS["socket"])
        for dr in (1, 2):
            for dc in (1, 2):
                paint(dr, dc, BG_COLOR)
        return

    if entity_type == "wall":
        for dr in range(4):
            for dc in range(4):
                paint(dr, dc, COLORS["wall"])
        for dr in (1, 2):
            for dc in (1, 2):
                paint(dr, dc, BG_COLOR)
        return

    if entity_type.startswith("source:"):
        side = entity_type.split(":")[1]
        for dr in range(4):
            for dc in range(4):
                paint(dr, dc, COLORS["source"] if dr in (0, 3) or dc in (0, 3) else COLORS["source"])
        paint(1, 1, COLORS["highlight"])
        paint(2, 2, COLORS["highlight"])
        if side == "N":
            paint(0, 1, COLORS["highlight"])
            paint(0, 2, COLORS["source"])
        elif side == "S":
            paint(3, 1, COLORS["source"])
            paint(3, 2, COLORS["highlight"])
        elif side == "W":
            paint(1, 0, COLORS["highlight"])
            paint(2, 0, COLORS["source"])
        elif side == "E":
            paint(1, 3, COLORS["source"])
            paint(2, 3, COLORS["highlight"])
        return

    if entity_type.startswith("lamp:"):
        side = entity_type.split(":")[1]
        for i in range(4):
            paint(0, i, COLORS["lamp"])
            paint(3, i, COLORS["lamp"])
            paint(i, 0, COLORS["lamp"])
            paint(i, 3, COLORS["lamp"])
        paint(1, 1, COLORS["highlight"])
        paint(1, 2, COLORS["highlight"])
        paint(2, 1, COLORS["lamp"])
        paint(2, 2, COLORS["highlight"])
        if side == "N":
            paint(0, 1, COLORS["highlight"])
        elif side == "S":
            paint(3, 2, COLORS["highlight"])
        elif side == "W":
            paint(2, 0, COLORS["highlight"])
        elif side == "E":
            paint(1, 3, COLORS["highlight"])
        return

    if entity_type == "patrol":
        for pos in [(0, 0), (0, 3), (1, 1), (1, 2), (2, 1), (2, 2), (3, 0), (3, 3)]:
            paint(pos[0], pos[1], COLORS["patrol"])
        paint(1, 1, COLORS["highlight"])
        paint(2, 2, COLORS["highlight"])
        return

    if entity_type.startswith("piece:"):
        _, weight, kind, rot_text = entity_type.split(":")
        rot = int(rot_text)
        base = COLORS["loose"] if weight == "loose" else COLORS["pipe"]
        draw_connector(base, _piece_connections(kind, rot), loose=(weight == "loose"))


def _connection_map(h_t, level):
    cfg = LEVELS[level]
    blocked = _blocked_cells(h_t, level)
    mapping = {}
    src = cfg["source"]
    if (src["r"], src["c"]) not in blocked:
        mapping[(src["r"], src["c"])] = _endpoint_connections(src)
    for lamp in cfg["lamps"]:
        if (lamp["r"], lamp["c"]) not in blocked:
            mapping[(lamp["r"], lamp["c"])] = _endpoint_connections(lamp)
    for idx, state in enumerate(h_t["pieces"]):
        if (state["r"], state["c"]) in blocked:
            continue
        spec = cfg["pieces"][idx]
        mapping[(state["r"], state["c"])] = _piece_connections(spec["kind"], state["rot"])
    return mapping


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    """Deterministic history state update (DreamerV3 sequence model).

    Uses both h_t and z_t to compute the next state. z_t may contain
    stochastic elements (enemy positions, spawns) that affect transitions.
    For deterministic games, z_t is {} and can be ignored.

    Read level constants from LEVELS[h_t["level"]]. Check active_tags
    to decide which mechanics apply. Apply the action:
    1. Dispatch: which entity does this action target?
    2. Apply effect: movement, toggle, cycle, collection
    3. Check collisions: blocked by walls? overlapping items?
    4. Resolve interactions: collection, switching, triggering
    5. Update globals: budget, step counter

    Args:
        h_t: Current history state dict.
        z_t: Current latent state dict (stochastic elements).
        a_t: Action value. Use bare ints for non-click actions, or `(6, x, y)` for CLICK.
    Returns:
        New history state dict (must deepcopy first).
    """
    level = h_t["level"]
    cfg = LEVELS[level]

    if a_t == 0:
        reset_h, _ = get_initial_state(level)
        return reset_h

    new_h = copy.deepcopy(h_t)

    if a_t == 7:
        if new_h["undo"]:
            prev = new_h["undo"].pop()
            new_h["pieces"] = copy.deepcopy(prev["pieces"])
            new_h["step"] = prev["step"]
            new_h["budget"] = prev["budget"]
        return new_h

    if new_h["budget"] <= 0:
        return new_h

    snapshot = {
        "pieces": copy.deepcopy(new_h["pieces"]),
        "step": new_h["step"],
        "budget": new_h["budget"],
    }
    new_h["undo"].append(snapshot)
    if len(new_h["undo"]) > 50:
        new_h["undo"] = new_h["undo"][-50:]

    if isinstance(a_t, tuple) and len(a_t) == 3 and a_t[0] == 6:
        x = int(a_t[1])
        y = int(a_t[2])
        cell_r = y // CELL_SIZE
        cell_c = x // CELL_SIZE
        off_r, off_c = _board_offset(level)
        local_r = cell_r - off_r
        local_c = cell_c - off_c
        if 0 <= local_r < cfg["rows"] and 0 <= local_c < cfg["cols"]:
            blocked = _blocked_cells(h_t, level)
            idx = _piece_at(new_h, local_r, local_c)
            if idx is not None and (local_r, local_c) not in blocked:
                new_h["pieces"][idx]["rot"] = (new_h["pieces"][idx]["rot"] + 1) % 4

    _apply_gravity(new_h)
    pulse = z_t.get("source_pulse", 0)
    new_h["step"] += 1 + 0 * pulse
    new_h["budget"] = max(0, new_h["budget"] - 1)
    return new_h


def predict(h_t: dict, seed: int) -> dict:
    """Generate latent state from history.

    Check LEVELS[h_t["level"]]["stochastic"] to decide what to sample.
    For deterministic levels: return minimal/empty z_t.
    For stochastic levels: use the seed to sample random elements.

    Args:
        h_t: Current history state dict.
        seed: Random seed for reproducibility.
    Returns:
        Latent state dict (z_t).
    """
    level = h_t["level"]
    cfg = LEVELS[level]
    if not cfg.get("stochastic"):
        return {}
    rng = random.Random((seed + 1) * 997 + level * 131 + h_t["step"] * 17)
    lamp_flicker = [rng.randint(0, 1) for _ in cfg["lamps"]]
    patrol_glint = [rng.randint(0, 1) for _ in cfg.get("patrols", [])]
    sparkle = (rng.randint(0, cfg["rows"] - 1), rng.randint(0, cfg["cols"] - 1))
    return {
        "lamp_flicker": lamp_flicker,
        "patrol_glint": patrol_glint,
        "source_pulse": rng.randint(0, 2),
        "sparkle": sparkle,
    }


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    """Check if the current level's goal has been achieved.

    Use RELATIONAL checks against LEVELS[level] goal config.
    Example: player at LEVELS[level]["exit"] AND all keys collected.

    Args:
        h_t: Current history state.
        z_t: Current latent state.
        level: Level number (0-indexed).
    Returns:
        True if level is complete.
    """
    cfg = LEVELS[level]
    connections = _connection_map(h_t, level)
    source_pos = (cfg["source"]["r"], cfg["source"]["c"])
    if source_pos not in connections:
        return False

    visited = {source_pos}
    frontier = [source_pos]
    while frontier:
        r, c = frontier.pop()
        for direction in connections.get((r, c), set()):
            dr, dc = DIR_VECTORS[direction]
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            if neighbor not in connections:
                continue
            if OPPOSITE[direction] not in connections[neighbor]:
                continue
            if neighbor not in visited:
                visited.add(neighbor)
                frontier.append(neighbor)

    for lamp in cfg["lamps"]:
        if (lamp["r"], lamp["c"]) not in visited:
            return False
    return True


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    """Render the current state as a 64x64 grid.

    Use layered compositing:
    1. Fill with BG_COLOR
    2. Draw static elements from LEVELS constants
    3. Draw dynamic entities from h_t
    4. Draw UI overlays (budget bar, score) from h_t scalars


    Args:
        h_t: Current history state.
        z_t: Current latent state.
    Returns:
        64x64 list of lists, values 0-15.
    """
    level = h_t["level"]
    cfg = LEVELS[level]
    grid = [[BG_COLOR for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    off_r, off_c = _board_offset(level)

    for r in range(cfg["rows"]):
        for c in range(cfg["cols"]):
            top = (off_r + r) * CELL_SIZE
            left = (off_c + c) * CELL_SIZE
            _draw_entity(grid, top, left, "socket")

    for wr, wc in cfg.get("walls", []):
        top = (off_r + wr) * CELL_SIZE
        left = (off_c + wc) * CELL_SIZE
        _draw_entity(grid, top, left, "wall")

    src = cfg["source"]
    top = (off_r + src["r"]) * CELL_SIZE
    left = (off_c + src["c"]) * CELL_SIZE
    _draw_entity(grid, top, left, "source:" + src["side"])
    if z_t.get("source_pulse", 0) % 2 == 1:
        grid[top + 1][left + 2] = COLORS["highlight"]

    for i, lamp in enumerate(cfg["lamps"]):
        top = (off_r + lamp["r"]) * CELL_SIZE
        left = (off_c + lamp["c"]) * CELL_SIZE
        _draw_entity(grid, top, left, "lamp:" + lamp["side"])
        if i < len(z_t.get("lamp_flicker", [])) and z_t["lamp_flicker"][i]:
            grid[top + 2][left + 1] = COLORS["highlight"]
        else:
            grid[top + 2][left + 1] = COLORS["lamp"]

    for idx, state in enumerate(h_t["pieces"]):
        spec = cfg["pieces"][idx]
        top = (off_r + state["r"]) * CELL_SIZE
        left = (off_c + state["c"]) * CELL_SIZE
        weight = "loose" if spec.get("loose", False) else "stable"
        _draw_entity(grid, top, left, "piece:%s:%s:%d" % (weight, spec["kind"], state["rot"]))

    patrol_positions = _patrol_positions(level, h_t["step"])
    for i, (pr, pc) in enumerate(patrol_positions):
        top = (off_r + pr) * CELL_SIZE
        left = (off_c + pc) * CELL_SIZE
        _draw_entity(grid, top, left, "patrol")
        if i < len(z_t.get("patrol_glint", [])) and z_t["patrol_glint"][i]:
            grid[top + 1][left + 2] = COLORS["highlight"]

    max_budget = max(1, cfg["budget"])
    fill = int((60 * h_t["budget"]) / max_budget)
    for c in range(2, 62):
        grid[62][c] = COLORS["highlight"]
        grid[63][c] = COLORS["wall"]
        if c - 2 < fill:
            grid[63][c] = COLORS["lamp"]
    spark = z_t.get("sparkle")
    if spark:
        sr, sc = spark
        top = (off_r + sr) * CELL_SIZE
        left = (off_c + sc) * CELL_SIZE
        if 0 <= top < GRID_SIZE and 0 <= left < GRID_SIZE:
            grid[top][left] = COLORS["highlight"]
    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    """Get the initial (h_t, z_t) for a given level.

    Read from LEVELS[level] to set starting positions and parameters.

    Args:
        level: Level number (0-indexed, 0 to 7).
    Returns:
        Tuple of (h_t, z_t).
    """
    cfg = LEVELS[level]
    h_t = {
        "level": level,
        "step": 0,
        "budget": cfg["budget"],
        "pieces": [{"r": p["r"], "c": p["c"], "rot": p["rot"]} for p in cfg["pieces"]],
        "undo": [],
    }
    z_t = predict(h_t, seed=level + 1)
    return h_t, z_t


def get_available_actions() -> list[int]:
    """Return available action integers for this game.

    Returns:
        List of available base action ints.
        Possible values: 0=RESET, 1=UP, 2=DOWN, 3=LEFT, 4=RIGHT, 5=USE, 6=CLICK, 7=UNDO.
        Example: [0, 6] for RESET + spatial clicks. When action 6 is used, `transition()` receives `(6, x, y)`.
    """
    return [0, 6, 7]


def _orientation_matches(spec, rot):
    return _piece_connections(spec["kind"], rot) == _piece_connections(spec["kind"], spec["target_rot"])



def solve_level(level: int, h_t: dict, z_t: dict):
    """Programmatic policy that solves any level given current state.

    This function has access to the full internal state (h_t and z_t)
    and returns the best action for the current situation. It is called
    in a loop until check_level_complete returns True.

    Args:
        level: Level number.
        h_t: Current history state.
        z_t: Current latent state.
    Returns:
        Single action to take next.
        Return a bare int for non-click actions, or `(6, x, y)` for CLICK.
    """
    cfg = LEVELS[level]
    blocked = _blocked_cells(h_t, level)

    for idx in cfg["solve_order"]:
        spec = cfg["pieces"][idx]
        state = h_t["pieces"][idx]
        if not _orientation_matches(spec, state["rot"]):
            if (state["r"], state["c"]) not in blocked:
                return _cell_to_click(level, state["r"], state["c"])

    return _cell_to_click(level, cfg["wait_cell"][0], cfg["wait_cell"][1])


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Sl4821(_FunctionalArcGame):
    GAME_ID = "sl4821-3b4e1b22"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
