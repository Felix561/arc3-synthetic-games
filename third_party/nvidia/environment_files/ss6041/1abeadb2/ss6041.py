# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the ss6041/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy

BG_COLOR = 5
COLORS = {
    "stone": 9,
    "wall": 15,
    "floor": 10,
    "target": 11,
    "seal": 0,
    "void": 5,
}

LEVELS = {
    0: {
        "name": "Six Sink Survey",
        "active_tags": ["gravity"],
        "budget": 24,
        "basins": [
            {"id": 0, "rect": (3, 2, 13, 9), "target": 2, "capacity": 4, "click": (5, 6)},
            {"id": 1, "rect": (3, 12, 13, 19), "target": 3, "capacity": 4, "click": (15, 6)},
            {"id": 2, "rect": (3, 22, 13, 29), "target": 1, "capacity": 4, "click": (25, 6)},
            {"id": 3, "rect": (18, 2, 28, 9), "target": 4, "capacity": 4, "click": (5, 21)},
            {"id": 4, "rect": (18, 12, 28, 19), "target": 2, "capacity": 4, "click": (15, 21)},
            {"id": 5, "rect": (18, 22, 28, 29), "target": 3, "capacity": 4, "click": (25, 21)},
        ],
        "seal_rect": (14, 27, 17, 30),
        "goal_requirements": {"all_basin_targets": True, "no_overfill": True},
        "design_contract": {
            "success_trigger": "click_final_button",
            "state_key": "seal_clicked",
            "primary_blocker": "white ready seal stays closed until all six basin fill counts exactly match yellow target ticks",
            "dependencies": ["estimate target for each basin", "drop stones into six different basins", "click ready seal"],
            "feedback": "blue stones stack upward by gravity; the ready seal gains a white center when every target is met; overfill draws an X",
            "bypass_guard": "clicking the seal before exact fills is rejected and does not set seal_clicked",
        },
    },
    1: {
        "name": "Shallow Shelf Survey",
        "active_tags": ["gravity", "shelves"],
        "budget": 28,
        "basins": [
            {"id": 0, "rect": (2, 1, 13, 8), "target": 3, "capacity": 4, "click": (4, 6), "shelf": (9, 4, 7)},
            {"id": 1, "rect": (2, 11, 13, 18), "target": 2, "capacity": 4, "click": (14, 6)},
            {"id": 2, "rect": (2, 21, 13, 30), "target": 4, "capacity": 4, "click": (25, 6), "shelf": (7, 22, 26)},
            {"id": 3, "rect": (17, 1, 29, 8), "target": 2, "capacity": 4, "click": (4, 22), "shelf": (23, 2, 5)},
            {"id": 4, "rect": (17, 11, 29, 18), "target": 3, "capacity": 4, "click": (14, 22)},
            {"id": 5, "rect": (17, 21, 29, 30), "target": 4, "capacity": 4, "click": (25, 22), "shelf": (24, 26, 29)},
        ],
        "seal_rect": (14, 26, 17, 29),
        "goal_requirements": {"all_basin_targets": True, "no_overfill": True},
        "design_contract": {
            "success_trigger": "click_final_button",
            "state_key": "seal_clicked",
            "primary_blocker": "shallow light-blue shelves change the visible usable space, so the ready seal remains closed until shelf-adjusted targets are exact",
            "dependencies": ["read shelf-obstructed target ticks", "fill all six basins to different counts", "avoid overfilling shallow basins", "click ready seal"],
            "feedback": "shelf bars are light-blue obstacles; stones visibly settle against floors and shelves while target ticks remain yellow",
            "bypass_guard": "the final seal cannot be activated before all six exact fill counts are visible and no basin has an overfill X",
        },
    },
    2: {
        "name": "Void Lip Survey",
        "active_tags": ["gravity", "shelves", "voids"],
        "budget": 22,
        "basins": [
            {"id": 0, "rect": (2, 2, 12, 9), "target": 4, "capacity": 4, "start": 1, "click": (6, 6), "void": (4, 3, 2, 2)},
            {"id": 1, "rect": (3, 12, 14, 20), "target": 2, "capacity": 4, "start": 0, "click": (17, 7), "shelf": (10, 13, 16)},
            {"id": 2, "rect": (2, 23, 13, 30), "target": 3, "capacity": 4, "start": 1, "click": (25, 6), "void": (5, 27, 2, 2)},
            {"id": 3, "rect": (17, 1, 29, 7), "target": 1, "capacity": 4, "start": 0, "click": (6, 23), "void": (20, 2, 2, 2)},
            {"id": 4, "rect": (18, 10, 29, 18), "target": 4, "capacity": 4, "start": 2, "click": (14, 23), "shelf": (24, 14, 17)},
            {"id": 5, "rect": (17, 22, 29, 30), "target": 3, "capacity": 4, "start": 1, "click": (24, 24), "void": (19, 28, 2, 2)},
        ],
        "seal_rect": (14, 14, 16, 17),
        "goal_requirements": {"all_basin_targets": True, "no_overfill": True, "no_void_loss": True},
        "design_contract": {
            "success_trigger": "click_final_button",
            "state_key": "seal_clicked",
            "primary_blocker": "black void drains inside several basins destroy stones clicked too near their lips",
            "dependencies": ["estimate remaining stones after pre-set blue dirt", "choose safe local click spots away from void drains", "fill every basin to its yellow target", "click ready seal"],
            "feedback": "void mouths are black pockets with white rims; pre-set stones already occupy lower slots; falling stones settle normally when safe",
            "bypass_guard": "the seal rejects early activation and any void loss sets no_void_loss false with the run failed",
        },
    },
    3: {
        "name": "Dirt Plug Survey",
        "active_tags": ["gravity", "shelves", "voids", "plugs"],
        "budget": 30,
        "basins": [
            {"id": 0, "rect": (2, 1, 13, 8), "target": 2, "capacity": 4, "start": 0, "click": (6, 11), "plug": (4, 2), "shelf": (9, 5, 7)},
            {"id": 1, "rect": (3, 11, 14, 18), "target": 3, "capacity": 4, "start": 1, "click": (15, 8), "void": (5, 12, 2, 2)},
            {"id": 2, "rect": (2, 22, 12, 30), "target": 4, "capacity": 4, "start": 0, "click": (28, 10), "plug": (5, 24)},
            {"id": 3, "rect": (18, 2, 29, 9), "target": 3, "capacity": 4, "start": 1, "click": (6, 24), "void": (20, 3, 2, 2)},
            {"id": 4, "rect": (17, 12, 29, 20), "target": 4, "capacity": 4, "start": 0, "click": (18, 26), "plug": (20, 14), "shelf": (24, 16, 19)},
            {"id": 5, "rect": (19, 23, 29, 30), "target": 2, "capacity": 4, "start": 0, "click": (25, 25)},
        ],
        "seal_rect": (14, 27, 17, 30),
        "goal_requirements": {"all_basin_targets": True, "no_overfill": True, "no_void_loss": True, "plugs_ready": True},
        "design_contract": {
            "success_trigger": "click_final_button",
            "state_key": "seal_clicked",
            "primary_blocker": "white dirt plugs must be cleared before their basin receives stones; otherwise the plug collapses and ruins the estimate",
            "dependencies": ["identify plug-capped basins", "clear plugs while those basins are empty", "avoid visible void pockets", "estimate remaining stones after starts", "click ready seal"],
            "feedback": "uncleared plugs are white/yellow caps; each clicked plug disappears, and a wrong late plug click draws an X",
            "bypass_guard": "the final seal activates only when every plug is visibly gone and all basin targets are exact",
        },
    },
    4: {
        "name": "Fogged Memory Survey",
        "active_tags": ["gravity", "shelves", "voids", "plugs", "fog"],
        "budget": 31,
        "fog_radius": 6,
        "basins": [
            {"id": 0, "rect": (2, 2, 13, 10), "target": 4, "capacity": 4, "start": 1, "click": (7, 8), "void": (4, 3, 2, 2)},
            {"id": 1, "rect": (2, 13, 12, 20), "target": 2, "capacity": 4, "start": 0, "click": (17, 9), "plug": (5, 14), "shelf": (8, 17, 19)},
            {"id": 2, "rect": (3, 23, 14, 30), "target": 3, "capacity": 4, "start": 1, "click": (25, 9), "void": (6, 28, 2, 2)},
            {"id": 3, "rect": (17, 1, 29, 8), "target": 4, "capacity": 4, "start": 0, "click": (6, 25), "plug": (20, 2)},
            {"id": 4, "rect": (18, 11, 29, 19), "target": 3, "capacity": 4, "start": 1, "click": (16, 24), "shelf": (24, 14, 17)},
            {"id": 5, "rect": (17, 22, 28, 30), "target": 2, "capacity": 4, "start": 0, "click": (25, 23), "plug": (19, 25), "void": (24, 28, 2, 2)},
        ],
        "seal_rect": (14, 14, 16, 17),
        "goal_requirements": {"all_basin_targets": True, "no_overfill": True, "no_void_loss": True, "plugs_ready": True},
        "design_contract": {
            "success_trigger": "click_final_button",
            "state_key": "seal_clicked",
            "primary_blocker": "fog hides distant target ticks, forcing the player to estimate and remember counts while still clearing plugs first",
            "dependencies": ["clear visible plugs before filling those basins", "use partial fog windows to read target ticks", "avoid void pockets", "settle exact gravity stacks", "click ready seal"],
            "feedback": "clicked or pre-filled basins remain visible in a local light circle; unrevealed board areas stay black",
            "bypass_guard": "the seal only opens after visible exact fills, all plugs cleared, and no void loss or overfill has occurred",
        },
    },
    5: {
        "name": "Chute Estimate Survey",
        "active_tags": ["gravity", "shelves", "voids", "plugs", "chutes"],
        "budget": 28,
        "required_chute_uses": 3,
        "basins": [
            {"id": 0, "rect": (2, 1, 12, 8), "target": 2, "capacity": 4, "start": 0, "click": (6, 10), "chute": (4, 3, 3, 3), "chute_to": 2},
            {"id": 1, "rect": (3, 11, 14, 20), "target": 3, "capacity": 4, "start": 1, "click": (16, 8), "void": (5, 12, 2, 2), "shelf": (10, 16, 19)},
            {"id": 2, "rect": (2, 23, 13, 30), "target": 4, "capacity": 4, "start": 1, "click": (27, 9), "void": (4, 28, 2, 2)},
            {"id": 3, "rect": (18, 1, 29, 8), "target": 3, "capacity": 4, "start": 0, "click": (6, 25), "plug": (20, 2), "shelf": (24, 5, 7)},
            {"id": 4, "rect": (17, 12, 29, 19), "target": 2, "capacity": 4, "start": 0, "click": (18, 26), "chute": (20, 13, 3, 3), "chute_to": 5},
            {"id": 5, "rect": (18, 23, 29, 30), "target": 4, "capacity": 4, "start": 1, "click": (25, 24), "void": (21, 28, 2, 2)},
        ],
        "seal_rect": (14, 14, 16, 17),
        "solution_clicks": [(4, 5, 2), (14, 21, 1), (6, 10, 2), (16, 8, 2), (27, 9, 1), (3, 21, 1), (6, 25, 3), (18, 26, 2), (25, 24, 2)],
        "goal_requirements": {"all_basin_targets": True, "no_overfill": True, "no_void_loss": True, "plugs_ready": True, "chutes_used": True},
        "design_contract": {
            "success_trigger": "click_final_button",
            "state_key": "seal_clicked",
            "primary_blocker": "yellow chute mouths redirect local clicks into other basins, so visible source clicks must be estimated separately from final target fills",
            "dependencies": ["use three chute drops shown by connector lines", "clear the plug before filling its basin", "avoid void pockets", "balance direct fills with redirected fills", "click ready seal"],
            "feedback": "chute mouths and their destination rims share connected yellow-white lines; each chute click increments visible remote stone stacks",
            "bypass_guard": "the seal only opens once all fills are exact, the plug is gone, no void/overfill happened, and the required chute-use counter is satisfied",
        },
    },
    6: {
        "name": "Fog Chute Memory Survey",
        "active_tags": ["gravity", "shelves", "voids", "plugs", "chutes", "fog"],
        "budget": 31,
        "fog_radius": 7,
        "required_chute_uses": 4,
        "basins": [
            {"id": 0, "rect": (2, 1, 13, 8), "target": 3, "capacity": 4, "start": 0, "click": (6, 10), "chute": (4, 3, 3, 3), "chute_to": 4, "void": (8, 2, 2, 2)},
            {"id": 1, "rect": (3, 11, 14, 20), "target": 4, "capacity": 4, "start": 1, "click": (16, 8), "shelf": (10, 16, 19)},
            {"id": 2, "rect": (2, 23, 13, 30), "target": 2, "capacity": 4, "start": 0, "click": (28, 10), "plug": (4, 24), "chute": (5, 25, 3, 3), "chute_to": 1},
            {"id": 3, "rect": (18, 1, 29, 8), "target": 4, "capacity": 4, "start": 1, "click": (6, 25), "plug": (20, 2), "shelf": (24, 5, 7)},
            {"id": 4, "rect": (17, 12, 29, 20), "target": 3, "capacity": 4, "start": 0, "click": (17, 26), "plug": (20, 14), "void": (18, 18, 2, 2)},
            {"id": 5, "rect": (18, 23, 29, 30), "target": 2, "capacity": 4, "start": 0, "click": (25, 24), "chute": (20, 25, 3, 3), "chute_to": 3, "void": (25, 28, 2, 2)},
        ],
        "seal_rect": (14, 14, 16, 17),
        "solution_clicks": [(25, 5, 1), (3, 21, 1), (15, 21, 1), (4, 5, 2), (26, 6, 1), (26, 21, 1), (6, 10, 3), (16, 8, 2), (28, 10, 2), (6, 25, 2), (17, 26, 1), (25, 24, 2)],
        "goal_requirements": {"all_basin_targets": True, "no_overfill": True, "no_void_loss": True, "plugs_ready": True, "chutes_used": True},
        "design_contract": {
            "success_trigger": "click_final_button",
            "state_key": "seal_clicked",
            "primary_blocker": "fog hides parts of the chute network, and four redirected drops must be estimated before final fill counts can balance",
            "dependencies": ["clear three fogged plugs before filling", "use four connected chute mouths", "estimate remote fills caused by chutes", "avoid void pockets", "settle every basin to target", "click ready seal"],
            "feedback": "fog reveals only around filled basins; chute mouths and destination rims are joined by yellow connector paths; the seal opens only when all counters are satisfied",
            "bypass_guard": "the final seal remains closed until exact fills, no void/overfill, all plugs cleared, and chutes_used is true",
        },
    },
    7: {
        "name": "Final Six-Sink Survey",
        "active_tags": ["gravity", "shelves", "voids", "plugs", "chutes", "fog"],
        "budget": 34,
        "fog_radius": 6,
        "required_chute_uses": 5,
        "basins": [
            {"id": 0, "rect": (2, 1, 13, 8), "target": 3, "capacity": 4, "start": 0, "click": (6, 10), "chute": (4, 3, 3, 3), "chute_to": 5, "void": (8, 2, 2, 2), "shelf": (10, 5, 7)},
            {"id": 1, "rect": (2, 11, 13, 19), "target": 3, "capacity": 4, "start": 1, "click": (16, 9), "plug": (5, 12), "shelf": (9, 16, 18)},
            {"id": 2, "rect": (2, 22, 13, 30), "target": 4, "capacity": 4, "start": 0, "click": (28, 10), "chute": (5, 24, 3, 3), "chute_to": 1, "void": (4, 28, 2, 2)},
            {"id": 3, "rect": (18, 1, 29, 8), "target": 2, "capacity": 4, "start": 0, "click": (6, 25), "plug": (20, 2), "shelf": (24, 5, 7)},
            {"id": 4, "rect": (17, 11, 29, 20), "target": 4, "capacity": 4, "start": 1, "click": (17, 26), "plug": (18, 13), "chute": (23, 16, 3, 3), "chute_to": 3, "void": (18, 18, 2, 2)},
            {"id": 5, "rect": (18, 23, 29, 30), "target": 3, "capacity": 4, "start": 0, "click": (25, 25), "chute": (20, 25, 3, 3), "chute_to": 2, "void": (25, 28, 2, 2)},
        ],
        "seal_rect": (14, 14, 16, 17),
        "solution_clicks": [(13, 6, 1), (3, 21, 1), (14, 19, 1), (4, 5, 2), (25, 6, 1), (17, 24, 1), (26, 21, 1), (6, 10, 3), (16, 9, 1), (28, 10, 3), (6, 25, 1), (17, 26, 3), (25, 25, 1)],
        "goal_requirements": {"all_basin_targets": True, "no_overfill": True, "no_void_loss": True, "plugs_ready": True, "chutes_used": True},
        "design_contract": {
            "success_trigger": "click_final_button",
            "state_key": "seal_clicked",
            "primary_blocker": "the final survey combines fog, void pockets, shelf shapes, three plugs, and five required chute transfers before the ready seal can open",
            "dependencies": ["clear all three plugs before extra fills", "count five redirected chute drops and their remote destinations", "estimate direct remaining drops for all six basins", "avoid every visible void pocket", "settle exact gravity stacks", "click ready seal"],
            "feedback": "fog reveals local basins, yellow connector paths show chute destinations, plugs disappear when cleared, and the ready seal turns open only after all visible conditions are satisfied",
            "bypass_guard": "early seal clicks are rejected; completion requires exact fills, plugs_ready, chutes_used, no_overfill, and no_void_loss simultaneously",
        },
    }
}


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    """Deterministic history state update (DreamerV3 sequence model)."""
    level = h_t.get("level", 0)
    cfg = LEVELS[level]
    base = a_t[0] if isinstance(a_t, tuple) and len(a_t) >= 1 else a_t
    if base not in get_available_actions():
        return copy.deepcopy(h_t)
    if base == 0:
        return get_initial_state(level)[0]
    if base != 6 or not (isinstance(a_t, tuple) and len(a_t) == 3):
        return copy.deepcopy(h_t)
    x, y = a_t[1], a_t[2]
    if not isinstance(x, int) or not isinstance(y, int):
        return copy.deepcopy(h_t)
    if h_t.get("complete", False) or h_t.get("failed", False):
        return copy.deepcopy(h_t)

    n = copy.deepcopy(h_t)

    clicked_plug = None
    if "plugs" in cfg.get("active_tags", []):
        for b in cfg["basins"]:
            if "plug" in b and not h_t.get("plugs_cleared", [True] * len(cfg["basins"]))[b["id"]]:
                pr, pc = b["plug"]
                if pc <= x <= pc + 3 and pr <= y <= pr + 3:
                    clicked_plug = b
                    break

    clicked_basin = None
    if clicked_plug is None:
        for b in cfg["basins"]:
            r0, c0, r1, c1 = b["rect"]
            if c0 < x < c1 and r0 < y < r1:
                clicked_basin = b
                break

    committed = False
    if clicked_plug is not None:
        i = clicked_plug["id"]
        if n["fills"][i] <= clicked_plug.get("start", 0):
            n["plugs_cleared"][i] = True
            committed = True
        else:
            n["plug_errors"][i] = True
            n["failed"] = True
            committed = True
    elif clicked_basin is not None:
        source_i = clicked_basin["id"]
        if "voids" in cfg.get("active_tags", []) and _point_in_void(clicked_basin, y, x):
            n["voided"][source_i] = True
            n["no_void_loss"] = False
            n["failed"] = True
            committed = True
        else:
            landing_basin = clicked_basin
            if "chutes" in cfg.get("active_tags", []) and _point_in_chute(clicked_basin, y, x):
                landing_basin = cfg["basins"][clicked_basin["chute_to"]]
                n["chute_count"] = n.get("chute_count", 0) + 1
            i = landing_basin["id"]
            n["fills"][i] += 1
            committed = True
            if "gravity" in cfg.get("active_tags", []) and n["fills"][i] > landing_basin["target"]:
                n["overfilled"][i] = True
                n["failed"] = True
    else:
        sr0, sc0, sr1, sc1 = cfg["seal_rect"]
        if sc0 <= x <= sc1 and sr0 <= y <= sr1:
            if _targets_met(n, cfg) and _plugs_ready(n, cfg):
                n["seal_clicked"] = True
                n["complete"] = True
                committed = True
            else:
                return copy.deepcopy(h_t)
        else:
            return copy.deepcopy(h_t)

    if committed:
        n["no_overfill"] = not any(n.get("overfilled", []))
        n["no_void_loss"] = not any(n.get("voided", []))
        n["plugs_ready"] = _plugs_ready(n, cfg)
        n["chutes_used"] = n.get("chute_count", 0) >= cfg.get("required_chute_uses", 0)
        n["all_basin_targets"] = _targets_met(n, cfg)
        n["step"] += 1
        n["budget_left"] -= 1
        if n["budget_left"] < 0 and not n.get("complete", False):
            n["failed"] = True
    return n


def predict(h_t: dict) -> dict:
    """Return minimal/empty z_t. This game is fully deterministic."""
    return {}


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    """Check if the current level's goal has been achieved."""
    if level not in LEVELS or h_t.get("level") != level:
        return False
    cfg = LEVELS[level]
    req = cfg.get("goal_requirements", {})
    if req.get("no_overfill", False) and any(h_t.get("overfilled", [])):
        return False
    if req.get("no_void_loss", False) and not h_t.get("no_void_loss", True):
        return False
    if req.get("plugs_ready", False) and not h_t.get("plugs_ready", True):
        return False
    if req.get("chutes_used", False) and not h_t.get("chutes_used", True):
        return False
    if req.get("all_basin_targets", False) and not _targets_met(h_t, cfg):
        return False
    return bool(h_t.get("seal_clicked", False) and h_t.get("complete", False))


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    """Render the current state as a 32x32 grid."""
    grid = [[BG_COLOR for _ in range(32)] for _ in range(32)]
    cfg = LEVELS[h_t["level"]]

    def _draw_entity(grid, row, col, entity_type):
        if entity_type == "wall":
            if 0 <= row < 32 and 0 <= col < 32:
                grid[row][col] = COLORS["wall"]
        elif entity_type == "floor":
            if 0 <= row < 32 and 0 <= col < 32:
                grid[row][col] = COLORS["floor"]
        elif entity_type == "shelf":
            if 0 <= row < 32 and 0 <= col < 32:
                grid[row][col] = COLORS["seal"] if col % 2 == 0 else COLORS["floor"]
        elif entity_type == "plug":
            for dr in range(4):
                for dc in range(4):
                    rr, cc = row + dr, col + dc
                    if 0 <= rr < 32 and 0 <= cc < 32:
                        grid[rr][cc] = COLORS["seal"] if (dr in (0, 3) or dc in (0, 3)) else COLORS["target"]
        elif entity_type == "chute":
            for dr in range(4):
                for dc in range(4):
                    rr, cc = row + dr, col + dc
                    if 0 <= rr < 32 and 0 <= cc < 32:
                        if dr == dc or dc == 3 or dr == 0:
                            grid[rr][cc] = COLORS["target"]
                        else:
                            grid[rr][cc] = COLORS["seal"]
        elif entity_type == "stone":
            pts = [(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(1,4),(2,0),(2,1),(2,2),(2,3),(2,4),(3,0),(3,1),(3,2),(3,3),(3,4),(4,1),(4,2),(4,3)]
            for dr, dc in pts:
                rr, cc = row + dr, col + dc
                if 0 <= rr < 32 and 0 <= cc < 32:
                    grid[rr][cc] = COLORS["stone"]
        elif entity_type == "target":
            for dc in range(5):
                rr, cc = row, col + dc
                if 0 <= rr < 32 and 0 <= cc < 32:
                    grid[rr][cc] = COLORS["target"]
        elif entity_type == "seal_closed":
            for dr in range(4):
                for dc in range(4):
                    rr, cc = row + dr, col + dc
                    if 0 <= rr < 32 and 0 <= cc < 32 and (dr in (0,3) or dc in (0,3)):
                        grid[rr][cc] = COLORS["seal"]
        elif entity_type == "seal_open":
            for dr in range(4):
                for dc in range(4):
                    rr, cc = row + dr, col + dc
                    if 0 <= rr < 32 and 0 <= cc < 32:
                        if dr in (0,3) or dc in (0,3):
                            grid[rr][cc] = COLORS["seal"]
                        elif dr == 1 or dc == 2:
                            grid[rr][cc] = COLORS["target"]
        elif entity_type == "error":
            for d in range(6):
                for rr, cc in ((row + d, col + d), (row + d, col + 5 - d)):
                    if 0 <= rr < 32 and 0 <= cc < 32:
                        grid[rr][cc] = COLORS["seal"]

    for b in cfg["basins"]:
        r0, c0, r1, c1 = b["rect"]
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if r in (r0, r1) or c in (c0, c1):
                    _draw_entity(grid, r, c, "wall")
        for c in range(c0 + 1, c1):
            _draw_entity(grid, r1 - 1, c, "floor")
        if "shelves" in cfg.get("active_tags", []) and "shelf" in b:
            sr, sc0, sc1 = b["shelf"]
            for c in range(sc0, sc1 + 1):
                _draw_entity(grid, sr, c, "shelf")
        if "voids" in cfg.get("active_tags", []) and "void" in b:
            vr, vc, vh, vw = b["void"]
            for rr in range(vr - 1, vr + vh + 1):
                for cc in range(vc - 1, vc + vw + 1):
                    if 0 <= rr < 32 and 0 <= cc < 32:
                        if rr in (vr - 1, vr + vh) or cc in (vc - 1, vc + vw):
                            grid[rr][cc] = COLORS["seal"]
                        else:
                            grid[rr][cc] = BG_COLOR
        if "chutes" in cfg.get("active_tags", []) and "chute" in b:
            cr, cc, ch, cw = b["chute"]
            _draw_entity(grid, cr, cc, "chute")
            tb = cfg["basins"][b["chute_to"]]
            sr, sc = cr + ch // 2, cc + cw // 2
            tr = tb["rect"][0] + 1
            tc = tb["rect"][1] + 2
            stepc = 1 if tc >= sc else -1
            for c in range(sc, tc + stepc, stepc):
                if 0 <= sr < 32 and 0 <= c < 32:
                    grid[sr][c] = COLORS["target"]
            stepr = 1 if tr >= sr else -1
            for r in range(sr, tr + stepr, stepr):
                if 0 <= r < 32 and 0 <= tc < 32:
                    grid[r][tc] = COLORS["target"]
        for k in range(b["target"]):
            _draw_entity(grid, r1 - 2 - k, c0 + 1, "target")
        if "plugs" in cfg.get("active_tags", []) and "plug" in b:
            cleared = h_t.get("plugs_cleared", [True] * len(cfg["basins"]))[b["id"]]
            if not cleared:
                pr, pc = b["plug"]
                _draw_entity(grid, pr, pc, "plug")

    fills = h_t.get("fills", [0] * len(cfg["basins"]))
    over = h_t.get("overfilled", [False] * len(cfg["basins"]))
    plug_errors = h_t.get("plug_errors", [False] * len(cfg["basins"]))
    for b in cfg["basins"]:
        i = b["id"]
        r0, c0, r1, c1 = b["rect"]
        for k in range(min(fills[i], b["capacity"])):
            stone_top = r1 - 6 - k
            stone_left = c0 + 2
            _draw_entity(grid, stone_top, stone_left, "stone")
        if over[i] or plug_errors[i]:
            _draw_entity(grid, r0 + 2, c0 + 1, "error")

    sr0, sc0, sr1, sc1 = cfg["seal_rect"]
    _draw_entity(grid, sr0, sc0, "seal_open" if (_targets_met(h_t, cfg) and _plugs_ready(h_t, cfg)) else "seal_closed")

    budget = cfg["budget"]
    left = max(0, h_t.get("budget_left", budget))
    lit = int(32 * left / budget)
    for c in range(32):
        grid[0][c] = COLORS["target"] if c < lit else COLORS["seal"]

    radius = cfg.get("fog_radius")
    if radius is not None:
        visible = [[False for _ in range(32)] for _ in range(32)]
        for b in cfg["basins"]:
            cx, cy = b["click"]
            if fills[b["id"]] > 0:
                for r in range(32):
                    for c in range(32):
                        if abs(r - cy) + abs(c - cx) <= radius:
                            visible[r][c] = True
        for r in range(32):
            for c in range(32):
                if not visible[r][c]:
                    grid[r][c] = BG_COLOR
    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    """Get the initial (h_t, z_t) for a given level."""
    cfg = LEVELS[level]
    plug_state = [False if "plug" in b else True for b in cfg["basins"]]
    h_t = {
        "level": level,
        "step": 0,
        "budget_left": cfg["budget"],
        "fills": [b.get("start", 0) for b in cfg["basins"]],
        "overfilled": [False for _ in cfg["basins"]],
        "voided": [False for _ in cfg["basins"]],
        "plugs_cleared": plug_state,
        "plug_errors": [False for _ in cfg["basins"]],
        "seal_clicked": False,
        "all_basin_targets": False,
        "no_overfill": True,
        "no_void_loss": True,
        "plugs_ready": all(plug_state),
        "chute_count": 0,
        "chutes_used": cfg.get("required_chute_uses", 0) == 0,
        "complete": False,
        "failed": False,
    }
    return h_t, predict(h_t)


def get_available_actions() -> list[int]:
    """Return available action integers for this game."""
    return [0, 6]


def solve_level(level: int) -> list:
    """Return a fixed sequence of actions that solves this level."""
    cfg = LEVELS[level]
    actions = []
    if "solution_clicks" in cfg:
        for x, y, count in cfg["solution_clicks"]:
            for _ in range(count):
                actions.append((6, x, y))
        sr0, sc0, sr1, sc1 = cfg["seal_rect"]
        actions.append((6, (sc0 + sc1) // 2, (sr0 + sr1) // 2))
        return actions
    for b in cfg["basins"]:
        if "plug" in b:
            pr, pc = b["plug"]
            actions.append((6, pc + 1, pr + 1))
        x, y = b["click"]
        for _ in range(max(0, b["target"] - b.get("start", 0))):
            actions.append((6, x, y))
    sr0, sc0, sr1, sc1 = cfg["seal_rect"]
    actions.append((6, (sc0 + sc1) // 2, (sr0 + sr1) // 2))
    return actions


def _targets_met(h_t, cfg):
    fills = h_t.get("fills", [])
    if len(fills) != len(cfg["basins"]):
        return False
    for b in cfg["basins"]:
        if fills[b["id"]] != b["target"]:
            return False
    if any(h_t.get("overfilled", [])):
        return False
    if any(h_t.get("voided", [])):
        return False
    if any(h_t.get("plug_errors", [])):
        return False
    return True


def _point_in_void(basin, row, col):
    if "void" not in basin:
        return False
    vr, vc, vh, vw = basin["void"]
    return vr <= row < vr + vh and vc <= col < vc + vw


def _plugs_ready(h_t, cfg):
    if "plugs" not in cfg.get("active_tags", []):
        return True
    states = h_t.get("plugs_cleared", [])
    return len(states) == len(cfg["basins"]) and all(states)


def _point_in_chute(basin, row, col):
    if "chute" not in basin:
        return False
    cr, cc, ch, cw = basin["chute"]
    return cr <= row < cr + ch and cc <= col < cc + cw


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Ss6041(_FunctionalArcGame):
    GAME_ID = "ss6041-1abeadb2"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
