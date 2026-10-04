# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the al7306/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy

BG_COLOR = 1
COLORS = {
    "bg": 1,
    "stitch": 2,
    "rank1": 10,
    "rank2": 0,
    "rank3": 9,
    "rank4": 15,
    "rank5": 5,
    "altar": 7,
    "seal": 0,
    "locked": 2,
    "blocker": 5,
    "selected": 15,
}
GRID_SIZE = 64
CELL_SIZE = 6
CELL_STEP = 8
ORIGIN_R = 14
ORIGIN_C = 12
SEAL_RECT = (29, 50, 9, 9)  # row, col, height, width

LEVELS = {
    0: {
        "cells": [(0, 2), (0, 3), (1, 1), (1, 2), (2, 0), (2, 1)],
        "initial_pieces": {
            "0,2": 1,
            "0,3": 1,
            "1,1": 1,
            "1,2": 1,
            "2,0": 1,
            "2,1": 1,
        },
        "main_target": (1, 2),
        "support_target": (2, 0),
        "seal_rect": SEAL_RECT,
        "budget": 20,
        "active_tags": [],
        "targets": {
            "target_cell": (1, 2),
            "target_rank": 3,
            "support_cell": (2, 0),
            "support_rank": 2,
        },
        "goal_requirements": {
            "main_ready": True,
            "support_ready": True,
        },
        "design_contract": {
            "success_trigger": "click_final_button",
            "state_key": "complete",
            "primary_blocker": "Agree Seal is locked until the main altar holds rank 3 and the support altar holds rank 2.",
            "dependencies": [
                "merge a first rank-1 pair into a rank-2 staging knot",
                "merge a second rank-1 pair onto the main altar",
                "merge the two rank-2 knots with destination on the main altar",
                "merge the support pair with destination on the support altar",
                "click the unlocked Agree Seal",
            ],
            "feedback": "altar rings glow with completed ranks and the seal center changes from gray to blue when ready",
            "bypass_guard": "transition ignores locked-seal clicks; complete can only become true when every goal_requirements relation is already true",
        },
    },
    1: {
        "cells": [
            (0, 0), (0, 1), (0, 2), (0, 3),
            (1, 0), (1, 1), (1, 2), (1, 3),
            (2, 1), (2, 2), (2, 3),
            (3, 0), (3, 3), (4, 0),
        ],
        "initial_pieces": {
            "0,0": 1,
            "1,0": 1,
            "1,1": 1,
            "1,2": 1,
            "2,1": 1,
            "2,2": 1,
            "0,3": 1,
            "1,3": 1,
            "3,3": 1,
            "2,3": 1,
            "4,0": 1,
            "3,0": 1,
        },
        "main_target": (2, 3),
        "support_target": (3, 0),
        "seal_rect": SEAL_RECT,
        "budget": 28,
        "active_tags": [],
        "targets": {
            "target_cell": (2, 3),
            "target_rank": 4,
            "support_cell": (3, 0),
            "support_rank": 2,
        },
        "goal_requirements": {
            "main_ready": True,
            "support_ready": True,
        },
        "design_contract": {
            "success_trigger": "click_final_button",
            "state_key": "complete",
            "primary_blocker": "Agree Seal is locked until a rank-4 knot reaches the main altar and a rank-2 support knot reaches the side altar.",
            "dependencies": [
                "ignore the tempting decoy pair on the left edge",
                "build one rank-3 staging knot at cell (2,2)",
                "build a second rank-3 knot directly on the main altar",
                "merge the rank-3 staging knot into the main altar to create rank 4",
                "build the support rank-2 knot on the side altar",
                "click the unlocked Agree Seal",
            ],
            "feedback": "the higher altar requires one more merge tier; the seal stays gray until both altar checks are true",
            "bypass_guard": "the seal click is ignored until the relational target ranks are present; decoy merges cannot satisfy either altar",
        },
    },
    2: {
        "cells": [
            (0, 2), (0, 3),
            (1, 1), (1, 2), (1, 3),
            (2, 1), (2, 2), (2, 3),
            (3, 0), (3, 3), (4, 0),
        ],
        "initial_pieces": {
            "1,1": 1,
            "1,2": 1,
            "2,1": 1,
            "2,2": 1,
            "0,3": 1,
            "1,3": 1,
            "3,3": 1,
            "2,3": 1,
            "4,0": 1,
            "3,0": 1,
        },
        "donors": [(0, 2)],
        "main_target": (2, 3),
        "support_target": (3, 0),
        "seal_rect": SEAL_RECT,
        "budget": 30,
        "active_tags": ["collectible"],
        "targets": {
            "target_cell": (2, 3),
            "target_rank": 4,
            "support_cell": (3, 0),
            "support_rank": 2,
        },
        "goal_requirements": {
            "main_ready": True,
            "support_ready": True,
            "donor_collected": True,
        },
        "design_contract": {
            "success_trigger": "click_final_button",
            "state_key": "complete",
            "primary_blocker": "Agree Seal is locked until the donor bead is collected by a local merge and both altar ranks are correct.",
            "dependencies": [
                "collect the donor by merging into a cell adjacent to its bead",
                "use the collected merge product as part of the rank-3 staging chain",
                "build a second rank-3 knot on the main altar",
                "merge staging rank-3 into the main altar to make rank 4",
                "build support rank 2 and click the unlocked seal",
            ],
            "feedback": "the donor bead disappears after a qualifying adjacent merge; the seal remains gray until donor_collected and altar checks are true",
            "bypass_guard": "seal readiness includes every goal_requirements flag, so a completed-looking altar cannot finish without donor_collected",
        },
    },
    3: {
        "cells": [
            (2, 2), (2, 3), (4, 3), (3, 3),
            (1, 4), (2, 4), (4, 4), (3, 4),
            (4, 0), (4, 1), (5, 0), (5, 1),
            (0, 0), (0, 1)
        ],
        "initial_pieces": {
            "2,2": 1,
            "2,3": 1,
            "4,3": 1,
            "3,3": 1,
            "1,4": 1,
            "2,4": 1,
            "4,4": 1,
            "3,4": 1,
            "4,0": 1,
            "4,1": 1,
            "5,0": 1,
            "5,1": 1,
            "0,0": 1,
            "0,1": 1
        },
        "donors": [(1, 3)],
        "blockers": [(1, 2), (2, 1), (3, 1), (4, 2), (5, 2)],
        "main_target": (3, 4),
        "support_target": (5, 1),
        "seal_rect": SEAL_RECT,
        "budget": 34,
        "active_tags": ["collectible", "blocker"],
        "targets": {
            "target_cell": (3, 4),
            "target_rank": 4,
            "support_cell": (5, 1),
            "support_rank": 3
        },
        "goal_requirements": {
            "main_ready": True,
            "support_ready": True,
            "donor_collected": True
        },
        "design_contract": {
            "success_trigger": "click_final_button",
            "state_key": "complete",
            "primary_blocker": "Rival blocker cloth splits the board; the seal needs donor collection, a rank-4 main knot, and a rank-3 support knot.",
            "dependencies": [
                "merge near the donor bead so donor_collected becomes true",
                "build the left staging rank-3 knot beside the main altar",
                "build the right rank-3 knot directly on the main altar",
                "merge staging into the main altar to create rank 4",
                "build the separate rank-3 support chain at the lower altar",
                "click the unlocked Agree Seal"
            ],
            "feedback": "striped rival cloth shows blocked lanes, the donor disappears when collected, and the seal turns blue only after all three requirements",
            "bypass_guard": "the final button tests the explicit requirement flags and relational ranks; decoy pair and early altar ranks cannot unlock it"
        },
    },
    4: {
        "cells": [
            (1, 1), (1, 2),
            (3, 1), (2, 1),
            (1, 3), (2, 3),
            (3, 2), (2, 2),
            (4, 0), (4, 1), (5, 0), (5, 1),
            (0, 1), (1, 0), (0, 0), (0, 3), (3, 0), (4, 2)
        ],
        "initial_pieces": {
            "1,2": 1,
            "1,1": 1,
            "3,1": 1,
            "2,1": 1,
            "1,3": 1,
            "2,3": 1,
            "3,2": 1,
            "2,2": 1,
            "4,0": 1,
            "4,1": 1,
            "5,0": 1,
            "5,1": 1
        },
        "donors": [(0, 1)],
        "spread_sources": [(1, 0)],
        "spread_path": [(1, 1), (2, 1), (2, 2)],
        "blockers": [(0, 0), (0, 3), (3, 0), (4, 2)],
        "main_target": (2, 2),
        "support_target": (5, 1),
        "seal_rect": SEAL_RECT,
        "budget": 36,
        "active_tags": ["collectible", "spread", "blocker"],
        "targets": {
            "target_cell": (2, 2),
            "target_rank": 4,
            "support_cell": (5, 1),
            "support_rank": 3
        },
        "goal_requirements": {
            "main_ready": True,
            "support_ready": True,
            "donor_collected": True,
            "spread_capped": True
        },
        "design_contract": {
            "success_trigger": "click_final_button",
            "state_key": "complete",
            "primary_blocker": "Purple spread will consume the staging lane unless the first merge caps it beside the donor bead.",
            "dependencies": [
                "first merge into cell (1,1) to collect the donor and cap the spread",
                "build a rank-3 staging knot in the protected lane",
                "build a rank-3 knot on the main altar",
                "merge staging into the main altar to make rank 4",
                "build the lower rank-3 support knot",
                "click the unlocked Agree Seal"
            ],
            "feedback": "uncapped spread advances as purple cells and deletes pieces on its path; capping stops it and the donor bead disappears",
            "bypass_guard": "the final button requires spread_capped plus donor_collected and the relational altar ranks"
        },
    },
    5: {
        "cells": [
            (0, 3), (1, 3), (2, 2), (2, 3), (5, 3), (4, 3), (3, 2), (3, 3),
            (0, 4), (1, 4), (2, 4), (5, 4), (4, 4), (3, 4),
            (4, 0), (4, 1), (5, 0), (5, 1)
        ],
        "initial_pieces": {
            "0,3": 1, "1,3": 1, "2,2": 1, "2,3": 1,
            "5,3": 1, "4,3": 1, "3,2": 1, "3,3": 1,
            "0,4": 1, "1,4": 1, "2,4": 1,
            "5,4": 1, "4,4": 1, "3,4": 1,
            "4,0": 1, "4,1": 1, "5,0": 1, "5,1": 1
        },
        "donors": [(1, 2)],
        "spread_sources": [(1, 2)],
        "spread_path": [(1, 3), (2, 3), (3, 3), (3, 4)],
        "blockers": [(0, 2), (2, 1), (4, 2), (5, 2)],
        "main_target": (3, 4),
        "support_target": (5, 1),
        "seal_rect": SEAL_RECT,
        "budget": 55,
        "active_tags": ["collectible", "spread", "blocker"],
        "targets": {
            "target_cell": (3, 4),
            "target_rank": 4,
            "support_cell": (5, 1),
            "support_rank": 3
        },
        "goal_requirements": {
            "main_ready": True,
            "support_ready": True,
            "donor_collected": True,
            "spread_capped": True
        },
        "design_contract": {
            "success_trigger": "click_final_button",
            "state_key": "complete",
            "primary_blocker": "A shared donor/spread source must be capped before the rank-4 main merge tree can safely use the central lane.",
            "dependencies": [
                "first merge into cell (1,3) to collect the donor and cap spread",
                "compose a rank-3 staging knot at cell (3,3)",
                "compose a separate rank-3 knot on the main altar at cell (3,4)",
                "merge staging rank-3 into the main altar to create rank 4",
                "compose the lower support altar to rank 3",
                "click the unlocked Agree Seal"
            ],
            "feedback": "purple spread source is visible beside the first merge; if not capped it propagates through critical central cells",
            "bypass_guard": "the seal requires spread_capped, donor_collected, and relational target ranks, so early rank chains cannot finish"
        },
    },
    6: {
        "cells": [
            (0, 3), (1, 3), (2, 2), (2, 3),
            (1, 4), (2, 4), (4, 4), (3, 4),
            (3, 0), (3, 1), (4, 0), (4, 1),
            (4, 2), (5, 2), (5, 0), (5, 1),
            (0, 0), (0, 1)
        ],
        "initial_pieces": {
            "0,3": 1, "1,3": 1, "2,2": 1, "2,3": 1,
            "1,4": 1, "2,4": 1, "4,4": 1, "3,4": 1,
            "3,0": 1, "3,1": 1, "4,0": 1, "4,1": 1,
            "4,2": 1, "5,2": 1, "5,0": 1, "5,1": 1,
            "0,0": 1, "0,1": 1
        },
        "donors": [(1, 2)],
        "spread_sources": [(1, 2)],
        "spread_path": [(1, 3), (2, 3), (2, 4), (3, 4)],
        "blockers": [(0, 2), (2, 1), (3, 2), (4, 3), (5, 3)],
        "main_target": (2, 4),
        "support_target": (5, 1),
        "seal_rect": SEAL_RECT,
        "budget": 44,
        "active_tags": ["collectible", "spread", "blocker"],
        "targets": {
            "target_cell": (2, 4),
            "target_rank": 4,
            "support_cell": (5, 1),
            "support_rank": 4
        },
        "goal_requirements": {
            "main_ready": True,
            "support_ready": True,
            "donor_collected": True,
            "spread_capped": True
        },
        "design_contract": {
            "success_trigger": "click_final_button",
            "state_key": "complete",
            "primary_blocker": "Two rank-4 altars are required, and the first central merge must cap the shared donor/spread source before it consumes the main chain.",
            "dependencies": [
                "first merge into cell (1,3) to collect the donor and cap the spread source",
                "build a rank-3 staging knot at cell (2,3)",
                "build a rank-3 main knot on cell (2,4)",
                "merge staging into the main altar to make rank 4",
                "build a separate rank-3 support staging knot at cell (4,1)",
                "build a rank-3 support knot on cell (5,1)",
                "merge support staging into the support altar to make rank 4",
                "click the unlocked Agree Seal"
            ],
            "feedback": "blocker cloth divides the main and support work; capped spread stops advancing, and both altar glyphs must glow before the seal turns blue",
            "bypass_guard": "the seal requires donor_collected, spread_capped, and both relational rank-4 altar states, so either partial altar remains visibly locked"
        },
    },
    7: {
        "cells": [
            (0, 2), (0, 3), (1, 2), (1, 3), (2, 1), (2, 2), (2, 4), (2, 3),
            (5, 2), (4, 2), (3, 1), (3, 2), (5, 3), (4, 3), (3, 4), (3, 3),
            (4, 0), (4, 1), (5, 0), (5, 1),
            (0, 4), (1, 0), (1, 1)
        ],
        "initial_pieces": {
            "0,2": 1, "0,3": 1, "1,2": 1, "1,3": 1,
            "2,1": 1, "2,2": 1, "2,4": 1, "2,3": 1,
            "5,2": 1, "4,2": 1, "3,1": 1, "3,2": 1,
            "5,3": 1, "4,3": 1, "3,4": 1, "3,3": 1,
            "4,0": 1, "4,1": 1, "5,0": 1, "5,1": 1,
            "1,0": 1, "1,1": 1
        },
        "donors": [(0, 4)],
        "spread_sources": [(0, 4)],
        "spread_path": [(0, 3), (1, 3), (2, 3), (3, 3)],
        "blockers": [(0, 0), (0, 1), (2, 0), (4, 4), (5, 4)],
        "main_target": (3, 3),
        "support_target": (5, 1),
        "seal_rect": SEAL_RECT,
        "budget": 58,
        "active_tags": ["collectible", "spread", "blocker"],
        "targets": {
            "target_cell": (3, 3),
            "target_rank": 5,
            "support_cell": (5, 1),
            "support_rank": 3
        },
        "goal_requirements": {
            "main_ready": True,
            "support_ready": True,
            "donor_collected": True,
            "spread_capped": True
        },
        "design_contract": {
            "success_trigger": "click_final_button",
            "state_key": "complete",
            "primary_blocker": "The final ritual needs a rank-5 ancient garment knot; the first merge must cap the donor/spread source or the central rank-5 spine is eaten.",
            "dependencies": [
                "start with the only safe merge into cell (0,3) to collect donor and cap spread",
                "build the upper rank-4 knot at cell (2,3)",
                "build the lower rank-4 knot directly on the main altar at cell (3,3)",
                "merge the two rank-4 knots downward to create rank 5 on the main altar",
                "build the lower-left support altar to rank 3",
                "avoid the decoy pair, then click the unlocked Agree Seal"
            ],
            "feedback": "the donor/spread bead disappears only when capped; the main altar shows a higher-order dark crown knot before the seal turns blue",
            "bypass_guard": "the final button checks donor_collected, spread_capped, support_ready, and the relational rank-5 main target, so neither a decoy merge nor rank-4 main knot can finish"
        },
    }
}


def _draw_entity(grid, row, col, entity_type):
    """Draw a distinctive pixel glyph at top-left pixel row, col."""
    def put(r, c, color):
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            grid[r][c] = color

    if entity_type == "cell":
        for dr in range(CELL_SIZE):
            for dc in range(CELL_SIZE):
                if dr in (0, CELL_SIZE - 1) or dc in (0, CELL_SIZE - 1):
                    put(row + dr, col + dc, COLORS["stitch"])
    elif entity_type == "main_altar":
        for dr in range(CELL_SIZE):
            for dc in range(CELL_SIZE):
                if dr in (0, CELL_SIZE - 1) or dc in (0, CELL_SIZE - 1):
                    put(row + dr, col + dc, COLORS["altar"])
        put(row + 2, col + 2, COLORS["rank3"])
        put(row + 2, col + 3, COLORS["rank3"])
        put(row + 3, col + 2, COLORS["rank3"])
        put(row + 3, col + 3, COLORS["rank3"])
    elif entity_type == "main_altar4":
        for dr in range(CELL_SIZE):
            for dc in range(CELL_SIZE):
                if dr in (0, CELL_SIZE - 1) or dc in (0, CELL_SIZE - 1):
                    put(row + dr, col + dc, COLORS["altar"])
        for dr in range(1, CELL_SIZE - 1):
            put(row + dr, col + dr, COLORS["rank4"])
            put(row + dr, col + CELL_SIZE - 1 - dr, COLORS["rank4"])
        put(row + 2, col + 2, COLORS["rank3"])
        put(row + 2, col + 3, COLORS["rank3"])
        put(row + 3, col + 2, COLORS["rank3"])
        put(row + 3, col + 3, COLORS["rank3"])
    elif entity_type == "main_altar5":
        for dr in range(CELL_SIZE):
            for dc in range(CELL_SIZE):
                if dr in (0, CELL_SIZE - 1) or dc in (0, CELL_SIZE - 1):
                    put(row + dr, col + dc, COLORS["altar"])
        for dc in range(1, CELL_SIZE - 1):
            put(row + 1, col + dc, COLORS["rank5"])
        put(row + 2, col + 1, COLORS["rank5"])
        put(row + 2, col + 4, COLORS["rank5"])
        put(row + 3, col + 2, COLORS["rank5"])
        put(row + 3, col + 3, COLORS["rank5"])
        put(row + 4, col + 1, COLORS["rank4"])
        put(row + 4, col + 4, COLORS["rank4"])
    elif entity_type == "support_altar":
        for dr in range(CELL_SIZE):
            for dc in range(CELL_SIZE):
                if dr in (0, CELL_SIZE - 1) or dc in (0, CELL_SIZE - 1):
                    put(row + dr, col + dc, COLORS["rank2"])
        put(row + 2, col + 2, COLORS["rank1"])
        put(row + 2, col + 3, COLORS["rank1"])
    elif entity_type == "support_altar3":
        for dr in range(CELL_SIZE):
            for dc in range(CELL_SIZE):
                if dr in (0, CELL_SIZE - 1) or dc in (0, CELL_SIZE - 1):
                    put(row + dr, col + dc, COLORS["rank2"])
        for dr in range(1, CELL_SIZE - 1):
            put(row + dr, col + 1, COLORS["rank3"])
            put(row + dr, col + CELL_SIZE - 2, COLORS["rank3"])
            put(row + 1, col + dr, COLORS["rank3"])
            put(row + CELL_SIZE - 2, col + dr, COLORS["rank3"])
    elif entity_type == "blocker":
        for dr in range(CELL_SIZE):
            for dc in range(CELL_SIZE):
                if dr in (0, CELL_SIZE - 1) or dc in (0, CELL_SIZE - 1):
                    put(row + dr, col + dc, COLORS["blocker"])
                elif (dr + dc) % 2 == 0:
                    put(row + dr, col + dc, COLORS["stitch"])
                else:
                    put(row + dr, col + dc, COLORS["blocker"])
    elif entity_type == "piece1":
        mid = CELL_SIZE // 2
        for k in range(1, CELL_SIZE - 1):
            put(row + mid, col + k, COLORS["rank1"])
            put(row + k, col + mid, COLORS["rank1"])
        put(row + mid, col + mid, COLORS["rank2"])
    elif entity_type == "piece2":
        pts = [(1, 3), (2, 2), (2, 4), (3, 1), (3, 5), (4, 2), (4, 4), (5, 3)]
        for dr, dc in pts:
            put(row + dr - 1, col + dc - 1, COLORS["rank2"])
        put(row + 2, col + 2, COLORS["rank1"])
        put(row + 2, col + 3, COLORS["rank1"])
        put(row + 3, col + 2, COLORS["rank1"])
        put(row + 3, col + 3, COLORS["rank1"])
    elif entity_type == "piece3":
        for dr in range(1, CELL_SIZE - 1):
            put(row + dr, col + 1, COLORS["rank3"])
            put(row + dr, col + CELL_SIZE - 2, COLORS["rank3"])
            put(row + 1, col + dr, COLORS["rank3"])
            put(row + CELL_SIZE - 2, col + dr, COLORS["rank3"])
        put(row + 2, col + 2, COLORS["rank2"])
        put(row + 2, col + 3, COLORS["rank2"])
        put(row + 3, col + 2, COLORS["rank2"])
        put(row + 3, col + 3, COLORS["rank2"])
    elif entity_type == "piece4":
        for dr in range(1, CELL_SIZE - 1):
            for dc in range(1, CELL_SIZE - 1):
                if dr in (1, CELL_SIZE - 2) or dc in (1, CELL_SIZE - 2) or dr == dc or dr + dc == CELL_SIZE - 1:
                    put(row + dr, col + dc, COLORS["rank4"])
        put(row + 2, col + 2, COLORS["rank3"])
        put(row + 2, col + 3, COLORS["rank3"])
        put(row + 3, col + 2, COLORS["rank3"])
        put(row + 3, col + 3, COLORS["rank3"])
    elif entity_type == "piece5":
        for dr in range(1, CELL_SIZE - 1):
            for dc in range(1, CELL_SIZE - 1):
                if dr in (1, CELL_SIZE - 2) or dc in (1, CELL_SIZE - 2):
                    put(row + dr, col + dc, COLORS["rank5"])
        put(row + 2, col + 2, COLORS["rank4"])
        put(row + 2, col + 3, COLORS["rank4"])
        put(row + 3, col + 2, COLORS["rank4"])
        put(row + 3, col + 3, COLORS["rank4"])
    elif entity_type == "spread":
        for dr in range(CELL_SIZE):
            for dc in range(CELL_SIZE):
                if dr in (0, CELL_SIZE - 1) or dc in (0, CELL_SIZE - 1):
                    put(row + dr, col + dc, COLORS["rank4"])
                elif (dr + dc) % 2 == 0:
                    put(row + dr, col + dc, COLORS["rank4"])
        put(row + 2, col + 2, COLORS["altar"])
        put(row + 3, col + 3, COLORS["altar"])
    elif entity_type == "donor":
        for dr in range(1, CELL_SIZE - 1):
            for dc in range(1, CELL_SIZE - 1):
                if (dr - 2) * (dr - 2) + (dc - 2) * (dc - 2) <= 4:
                    put(row + dr, col + dc, COLORS["rank1"])
        put(row + 2, col + 2, COLORS["rank2"])
        put(row + 2, col + 3, COLORS["rank2"])
        put(row + 3, col + 2, COLORS["rank2"])
        put(row + 3, col + 3, COLORS["rank2"])
    elif entity_type == "selected":
        for dc in range(-1, CELL_SIZE + 1):
            put(row - 1, col + dc, COLORS["selected"])
            put(row + CELL_SIZE, col + dc, COLORS["selected"])
        for dr in range(-1, CELL_SIZE + 1):
            put(row + dr, col - 1, COLORS["selected"])
            put(row + dr, col + CELL_SIZE, COLORS["selected"])
    elif entity_type == "seal_locked" or entity_type == "seal_ready":
        color = COLORS["rank3"] if entity_type == "seal_ready" else COLORS["locked"]
        for dr in range(9):
            for dc in range(9):
                if dr in (0, 8) or dc in (0, 8):
                    put(row + dr, col + dc, COLORS["seal"])
        put(row + 2, col + 4, color)
        put(row + 3, col + 3, color)
        put(row + 3, col + 5, color)
        put(row + 4, col + 2, color)
        put(row + 4, col + 6, color)
        put(row + 5, col + 3, color)
        put(row + 5, col + 5, color)
        put(row + 6, col + 4, color)


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    """Deterministic history state update (DreamerV3 sequence model).

    Deterministically computes the next history state from h_t and a_t.
    This game is deterministic, so z_t is always {} and must be ignored.
    """
    new_h = copy.deepcopy(h_t)
    base = a_t[0] if isinstance(a_t, tuple) and len(a_t) > 0 else a_t
    if base not in get_available_actions():
        return new_h

    level = new_h["level"]
    if base == 0:
        reset_h, _ = get_initial_state(level)
        return reset_h
    if base != 6 or not (isinstance(a_t, tuple) and len(a_t) == 3):
        return new_h
    if new_h.get("complete", False):
        return new_h

    x, y = a_t[1], a_t[2]
    cfg = LEVELS[level]

    def ready_to_seal(state):
        level_cfg = LEVELS[state["level"]]
        req = level_cfg["targets"]
        pieces = state.get("pieces", {})
        target_key = str(req["target_cell"][0]) + "," + str(req["target_cell"][1])
        support_key = str(req["support_cell"][0]) + "," + str(req["support_cell"][1])
        relational = pieces.get(target_key) == req["target_rank"] and pieces.get(support_key) == req["support_rank"]
        flags = True
        for key, val in level_cfg.get("goal_requirements", {}).items():
            flags = flags and (state.get(key) == val)
        return relational and flags

    sr, sc, sh, sw = cfg["seal_rect"]
    if sc <= x < sc + sw and sr <= y < sr + sh:
        if ready_to_seal(new_h):
            new_h["complete"] = True
            new_h["selected"] = None
            new_h["step"] += 1
        return new_h

    clicked_cell = None
    for br, bc in cfg["cells"]:
        pr = ORIGIN_R + br * CELL_STEP
        pc = ORIGIN_C + bc * CELL_STEP
        if pc <= x < pc + CELL_SIZE and pr <= y < pr + CELL_SIZE:
            clicked_cell = str(br) + "," + str(bc)
            break
    if clicked_cell is None:
        return new_h

    pieces = new_h["pieces"]
    selected = new_h.get("selected")
    if selected is None:
        if clicked_cell in pieces:
            new_h["selected"] = clicked_cell
        return new_h

    if clicked_cell == selected:
        new_h["selected"] = None
        return new_h

    if clicked_cell not in pieces:
        new_h["selected"] = None
        return new_h

    sr0, sc0 = [int(v) for v in selected.split(",")]
    tr0, tc0 = [int(v) for v in clicked_cell.split(",")]
    adjacent = abs(sr0 - tr0) + abs(sc0 - tc0) == 1
    if adjacent and pieces.get(selected) == pieces.get(clicked_cell):
        rank = pieces[clicked_cell] + 1
        del pieces[selected]
        pieces[clicked_cell] = rank
        target_cfg = cfg["targets"]
        main_key = str(target_cfg["target_cell"][0]) + "," + str(target_cfg["target_cell"][1])
        support_key = str(target_cfg["support_cell"][0]) + "," + str(target_cfg["support_cell"][1])
        new_h["main_ready"] = pieces.get(main_key) == target_cfg["target_rank"]
        new_h["support_ready"] = pieces.get(support_key) == target_cfg["support_rank"]
        if "collectible" in cfg.get("active_tags", []):
            for dr_d, dc_d in cfg.get("donors", []):
                if abs(dr_d - tr0) + abs(dc_d - tc0) <= 1:
                    new_h["donor_collected"] = True
        if "spread" in cfg.get("active_tags", []):
            spread_cells = [tuple(cell) for cell in new_h.get("spread_cells", [])]
            for sp_r, sp_c in spread_cells:
                if abs(sp_r - tr0) + abs(sp_c - tc0) <= 1:
                    new_h["spread_capped"] = True
            if not new_h.get("spread_capped", False):
                idx = int(new_h.get("spread_index", 0))
                path = cfg.get("spread_path", [])
                if idx < len(path):
                    next_cell = tuple(path[idx])
                    if next_cell not in spread_cells:
                        spread_cells.append(next_cell)
                    next_key = str(next_cell[0]) + "," + str(next_cell[1])
                    if next_key in pieces:
                        del pieces[next_key]
                    new_h["spread_index"] = idx + 1
                    new_h["spread_cells"] = spread_cells
        new_h["selected"] = None
        new_h["step"] += 1
    else:
        new_h["selected"] = clicked_cell
    return new_h


def predict(h_t: dict, seed: int) -> dict:
    """Return exactly {}. This game is fully deterministic."""
    return {}


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    """Check if the current level's goal has been achieved."""
    if level not in LEVELS or h_t.get("level") != level:
        return False
    target_cfg = LEVELS[level]["targets"]
    pieces = h_t.get("pieces", {})
    target_key = str(target_cfg["target_cell"][0]) + "," + str(target_cfg["target_cell"][1])
    support_key = str(target_cfg["support_cell"][0]) + "," + str(target_cfg["support_cell"][1])
    relational_met = pieces.get(target_key) == target_cfg["target_rank"] and pieces.get(support_key) == target_cfg["support_rank"]
    reqs_met = True
    for key, val in LEVELS[level].get("goal_requirements", {}).items():
        reqs_met = reqs_met and (h_t.get(key) == val)
    return bool(h_t.get("complete", False) and relational_met and reqs_met)


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    """Render the current state as a 64x64 grid."""
    grid = [[BG_COLOR for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    cfg = LEVELS[h_t["level"]]

    # HUD budget bar: gray rail with light-blue remaining actions.
    for c in range(2, 62):
        grid[1][c] = COLORS["stitch"]
    budget = max(1, int(h_t.get("budget", cfg["budget"])))
    remaining = max(0, budget - int(h_t.get("step", 0)))
    fill = min(60, (60 * remaining) // budget)
    for c in range(2, 2 + fill):
        grid[1][c] = COLORS["rank1"]

    for br, bc in cfg["cells"]:
        pr = ORIGIN_R + br * CELL_STEP
        pc = ORIGIN_C + bc * CELL_STEP
        cell_type = "cell"
        if (br, bc) == cfg["main_target"]:
            cell_type = "main_altar5" if cfg["targets"]["target_rank"] >= 5 else ("main_altar4" if cfg["targets"]["target_rank"] >= 4 else "main_altar")
        elif (br, bc) == cfg["support_target"]:
            cell_type = "support_altar3" if cfg["targets"]["support_rank"] >= 3 else "support_altar"
        _draw_entity(grid, pr, pc, cell_type)

    for br, bc in cfg.get("blockers", []):
        pr = ORIGIN_R + br * CELL_STEP
        pc = ORIGIN_C + bc * CELL_STEP
        _draw_entity(grid, pr, pc, "blocker")

    if "spread" in cfg.get("active_tags", []):
        for br, bc in h_t.get("spread_cells", []):
            pr = ORIGIN_R + br * CELL_STEP
            pc = ORIGIN_C + bc * CELL_STEP
            _draw_entity(grid, pr, pc, "spread")

    if "collectible" in cfg.get("active_tags", []) and not h_t.get("donor_collected", False):
        for br, bc in cfg.get("donors", []):
            pr = ORIGIN_R + br * CELL_STEP
            pc = ORIGIN_C + bc * CELL_STEP
            _draw_entity(grid, pr, pc, "donor")

    for key, rank in h_t.get("pieces", {}).items():
        br, bc = [int(v) for v in key.split(",")]
        pr = ORIGIN_R + br * CELL_STEP
        pc = ORIGIN_C + bc * CELL_STEP
        _draw_entity(grid, pr, pc, "piece" + str(min(rank, 5)))

    selected = h_t.get("selected")
    if selected is not None:
        br, bc = [int(v) for v in selected.split(",")]
        pr = ORIGIN_R + br * CELL_STEP
        pc = ORIGIN_C + bc * CELL_STEP
        _draw_entity(grid, pr, pc, "selected")

    req = cfg["targets"]
    pieces = h_t.get("pieces", {})
    target_key = str(req["target_cell"][0]) + "," + str(req["target_cell"][1])
    support_key = str(req["support_cell"][0]) + "," + str(req["support_cell"][1])
    ready = pieces.get(target_key) == req["target_rank"] and pieces.get(support_key) == req["support_rank"]
    _draw_entity(grid, cfg["seal_rect"][0], cfg["seal_rect"][1], "seal_ready" if ready else "seal_locked")
    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    """Get the initial (h_t, z_t) for a given level."""
    cfg = LEVELS[level]
    h_t = {
        "level": level,
        "step": 0,
        "budget": cfg["budget"],
        "pieces": copy.deepcopy(cfg["initial_pieces"]),
        "selected": None,
        "complete": False,
        "main_ready": False,
        "support_ready": False,
        "donor_collected": False,
        "spread_capped": False,
        "spread_cells": [tuple(cell) for cell in cfg.get("spread_sources", [])],
        "spread_index": 0,
    }
    return h_t, {}


def get_available_actions() -> list[int]:
    """Return available action integers for this click game."""
    return [0, 6]


def solve_level(level: int) -> list:
    """Return a fixed sequence of actions that solves this level."""
    def center(br, bc):
        return (6, ORIGIN_C + bc * CELL_STEP + CELL_SIZE // 2, ORIGIN_R + br * CELL_STEP + CELL_SIZE // 2)
    seal = (6, SEAL_RECT[1] + 4, SEAL_RECT[0] + 4)
    if level == 0:
        return [
            center(0, 3), center(0, 2),  # staging rank 2
            center(1, 1), center(1, 2),  # main altar rank 2
            center(0, 2), center(1, 2),  # main altar rank 3
            center(2, 1), center(2, 0),  # support altar rank 2
            seal,
        ]
    if level == 1:
        return [
            center(1, 1), center(1, 2),  # rank 2 for staging chain
            center(2, 1), center(2, 2),  # rank 2 at staging destination
            center(1, 2), center(2, 2),  # rank 3 staging knot
            center(0, 3), center(1, 3),  # rank 2 above main altar
            center(3, 3), center(2, 3),  # rank 2 on main altar
            center(1, 3), center(2, 3),  # rank 3 on main altar
            center(2, 2), center(2, 3),  # rank 4 on main altar
            center(4, 0), center(3, 0),  # support altar rank 2
            seal,
        ]
    if level == 2:
        return [
            center(1, 1), center(1, 2),  # collect donor while making rank 2
            center(2, 1), center(2, 2),  # rank 2 at staging destination
            center(1, 2), center(2, 2),  # rank 3 staging knot
            center(0, 3), center(1, 3),  # rank 2 above main altar
            center(3, 3), center(2, 3),  # rank 2 on main altar
            center(1, 3), center(2, 3),  # rank 3 on main altar
            center(2, 2), center(2, 3),  # rank 4 on main altar
            center(4, 0), center(3, 0),  # support altar rank 2
            seal,
        ]
    if level == 3:
        return [
            center(2, 2), center(2, 3),  # collect donor and make staging rank 2
            center(4, 3), center(3, 3),  # second staging rank 2
            center(2, 3), center(3, 3),  # staging rank 3 beside main
            center(1, 4), center(2, 4),  # main branch rank 2
            center(4, 4), center(3, 4),  # main altar rank 2
            center(2, 4), center(3, 4),  # main altar rank 3
            center(3, 3), center(3, 4),  # main altar rank 4
            center(4, 0), center(4, 1),  # support branch rank 2
            center(5, 0), center(5, 1),  # support altar rank 2
            center(4, 1), center(5, 1),  # support altar rank 3
            seal,
        ]
    if level == 4:
        return [
            center(1, 2), center(1, 1),  # cap spread and collect donor
            center(3, 1), center(2, 1),  # protected staging rank 2
            center(1, 1), center(2, 1),  # staging rank 3
            center(1, 3), center(2, 3),  # main branch rank 2
            center(3, 2), center(2, 2),  # main altar rank 2
            center(2, 3), center(2, 2),  # main altar rank 3
            center(2, 1), center(2, 2),  # main altar rank 4
            center(4, 0), center(4, 1),  # support branch rank 2
            center(5, 0), center(5, 1),  # support altar rank 2
            center(4, 1), center(5, 1),  # support altar rank 3
            seal,
        ]
    if level == 5:
        return [
            center(0, 3), center(1, 3),  # collect donor and cap spread
            center(5, 3), center(4, 3),  # staging lower rank 2
            center(3, 2), center(3, 3),  # staging altar-side rank 2
            center(4, 3), center(3, 3),  # staging rank 3
            center(5, 4), center(4, 4),  # main lower rank 2
            center(2, 4), center(3, 4),  # main altar rank 2
            center(4, 4), center(3, 4),  # main altar rank 3
            center(3, 3), center(3, 4),  # main altar rank 4
            center(4, 0), center(4, 1),  # support branch rank 2
            center(5, 0), center(5, 1),  # support altar rank 2
            center(4, 1), center(5, 1),  # support altar rank 3
            seal,
        ]
    if level == 6:
        return [
            center(0, 3), center(1, 3),  # cap spread and collect donor
            center(2, 2), center(2, 3),  # staging rank 2
            center(1, 3), center(2, 3),  # staging rank 3
            center(1, 4), center(2, 4),  # main altar rank 2
            center(4, 4), center(3, 4),  # main lower rank 2
            center(3, 4), center(2, 4),  # main altar rank 3
            center(2, 3), center(2, 4),  # main altar rank 4
            center(3, 0), center(3, 1),  # support staging rank 2
            center(4, 0), center(4, 1),  # support lower rank 2
            center(3, 1), center(4, 1),  # support staging rank 3
            center(4, 2), center(5, 2),  # support side rank 2
            center(5, 0), center(5, 1),  # support altar rank 2
            center(5, 2), center(5, 1),  # support altar rank 3
            center(4, 1), center(5, 1),  # support altar rank 4
            seal,
        ]
    if level == 7:
        return [
            center(0, 2), center(0, 3),  # cap spread and collect donor
            center(1, 2), center(1, 3),  # upper rank 2
            center(0, 3), center(1, 3),  # upper rank 3
            center(2, 1), center(2, 2),  # mid rank 2
            center(2, 4), center(2, 3),  # spine rank 2
            center(2, 2), center(2, 3),  # spine rank 3
            center(1, 3), center(2, 3),  # upper rank 4
            center(5, 2), center(4, 2),  # lower-left rank 2
            center(3, 1), center(3, 2),  # lower-left adjacent rank 2
            center(4, 2), center(3, 2),  # lower-left rank 3
            center(5, 3), center(4, 3),  # lower-right rank 2
            center(3, 4), center(3, 3),  # main altar rank 2
            center(4, 3), center(3, 3),  # main altar rank 3
            center(3, 2), center(3, 3),  # main altar rank 4
            center(2, 3), center(3, 3),  # main altar rank 5
            center(4, 0), center(4, 1),  # support rank 2
            center(5, 0), center(5, 1),  # support altar rank 2
            center(4, 1), center(5, 1),  # support altar rank 3
            seal,
        ]
    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Al7306(_FunctionalArcGame):
    GAME_ID = "al7306-000afcc7"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
