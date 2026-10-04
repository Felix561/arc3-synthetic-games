# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# AUTO-GENERATED from the ml2048/game_functions.py bundle — edit the
# source bundle and rerun build_generated_environments instead.
import copy

BG_COLOR = 0
CELL = 6
BOARD_TOP = 10
BOARD_LEFT = 8
BOARD_SIZE = 8
GRID_SIZE = 64

COLORS = {
    "bg": 0,
    "wall": 2,
    "brace": 2,
    "pit": 2,
    "player": 5,
    "settled": 5,
    "goal": 8,
    "warn": 8,
}

LEVELS = {
    0: {
        "layout": [
            "........",
            "#......#",
            "#......#",
            "#..##..#",
            "#......#",
            "#.G..G.#",
            "#.p..p.#",
            "########",
        ],
        "walls": [(r, c) for r, row in enumerate([
            "........",
            "#......#",
            "#......#",
            "#..##..#",
            "#......#",
            "#.G..G.#",
            "#.p..p.#",
            "########",
        ]) for c, ch in enumerate(row) if ch == "#"],
        "goals": [(5, 2), (5, 5)],
        "pit_cells": [(6, 2), (6, 5)],
        "brace_sites": [(6, 2), (6, 5)],
        "piece_spawns": [(0, 3), (0, 4), (0, 3)],
        "max_braces": 2,
        "budget": 24,
        "fog_radius": None,
        "active_tags": [],
        "goal_requirements": {"goals_filled": 2, "braces_placed": 2},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "goals_filled",
            "primary_blocker": "central grit baffles force early steering, and prosper sockets need lens braces underneath before a falling artefact can settle in them",
            "dependencies": ["place left lens brace", "steer first artefact left before the baffle", "place right lens brace", "steer second artefact right before the baffle", "settle artefacts into both sockets"],
            "feedback": "spent brace sites become gray supports with black centers; filled sockets keep a red rim with a black artefact inside; the HUD budget and lens markers shrink",
            "bypass_guard": "unbraced socket supports are pits, so an artefact falling through a red socket is lost instead of becoming a hidden support; all required sockets must visibly contain settled artefacts",
        },
    },
    1: {
        "layout": [
            "........",
            "#......#",
            "#......#",
            "#......#",
            "#......#",
            "#G..G.G#",
            "#p..p.p#",
            "########",
        ],
        "walls": [(r, c) for r, row in enumerate([
            "........",
            "#......#",
            "#......#",
            "#......#",
            "#......#",
            "#G..G.G#",
            "#p..p.p#",
            "########",
        ]) for c, ch in enumerate(row) if ch == "#"],
        "goals": [(5, 1), (5, 4), (5, 6)],
        "pit_cells": [(6, 1), (6, 4), (6, 6)],
        "brace_sites": [(6, 1), (6, 4), (6, 6)],
        "piece_spawns": [(0, 3), (0, 4), (0, 3), (0, 4)],
        "max_braces": 3,
        "budget": 26,
        "fog_radius": None,
        "active_tags": [],
        "goal_requirements": {"goals_filled": 3, "braces_placed": 3},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "goals_filled",
            "primary_blocker": "three separated prosper sockets each need their own limited lens brace support before they can catch a falling artefact",
            "dependencies": ["brace the left socket support before the first drop", "steer the first artefact two columns left", "brace and fill the far-right socket", "brace the center support last", "settle all three artefacts into red sockets"],
            "feedback": "each legal brace turns into a gray framed support, and each filled socket shows a black core inside its red rim while the lens HUD drains",
            "bypass_guard": "unbraced socket supports are pits, and the three red sockets are in separated lanes, so the visible target pattern cannot be reached without spending the three declared braces",
        },
    },
    2: {
        "layout": [
            "........",
            "#......#",
            "#S.....#",
            "#....g.#",
            "#......#",
            "#G..G.G#",
            "#p..p.p#",
            "########",
        ],
        "walls": [(r, c) for r, row in enumerate([
            "........",
            "#......#",
            "#S.....#",
            "#....g.#",
            "#......#",
            "#G..G.G#",
            "#p..p.p#",
            "########",
        ]) for c, ch in enumerate(row) if ch == "#"],
        "goals": [(5, 1), (5, 4), (5, 6)],
        "pit_cells": [(6, 1), (6, 4), (6, 6)],
        "brace_sites": [(6, 1), (6, 4), (6, 6)],
        "switches": [(2, 1)],
        "gate_cells": [(3, 5)],
        "initial_switch_on": False,
        "piece_spawns": [(0, 3), (0, 4), (0, 3), (0, 4)],
        "max_braces": 3,
        "budget": 30,
        "fog_radius": None,
        "active_tags": ["switch"],
        "goal_requirements": {"goals_filled": 3, "braces_placed": 3, "switch_on": True, "switches_used": 1},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "goals_filled",
            "primary_blocker": "a red-gray switch controls the only open route to the right prosperity socket; leaving it closed catches the right-bound artefact on the gate",
            "dependencies": ["place the left lens support", "fill the left socket", "click the linked switch to open the marked gate", "place the right and center supports", "steer two later artefacts through the open gate pattern into the remaining sockets"],
            "feedback": "the switch changes from a red-speckled gray frame to a red rim with black cross, and the linked gate changes from a red-gray barrier to an open red-gray guide",
            "bypass_guard": "the closed gate cell is a solid blocker in the right lane, so the third red socket cannot be visibly filled until the switch has been clicked on",
        },
    },
    3: {
        "layout": [
            "........",
            "#......#",
            "##.....#",
            "#......#",
            "#......#",
            "#.G.G.G#",
            "#.p.p.p#",
            "########",
        ],
        "walls": [(r, c) for r, row in enumerate([
            "........",
            "#......#",
            "##.....#",
            "#......#",
            "#......#",
            "#.G.G.G#",
            "#.p.p.p#",
            "########",
        ]) for c, ch in enumerate(row) if ch == "#"],
        "goals": [(5, 2), (5, 4), (5, 6)],
        "pit_cells": [(6, 2), (6, 4), (6, 6)],
        "brace_sites": [(6, 2), (6, 4), (6, 6)],
        "patrol_route": [(4, 1), (4, 3), (4, 1), (4, 3)],
        "patrol_start_idx": 0,
        "piece_spawns": [(0, 3), (0, 4), (0, 3), (0, 4)],
        "max_braces": 3,
        "budget": 31,
        "fog_radius": None,
        "active_tags": ["patrol"],
        "goal_requirements": {"goals_filled": 3, "braces_placed": 3},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "goals_filled",
            "primary_blocker": "a black patrol shard sweeps a left-side row-four lane while a new upper grit notch changes the safe steering order from earlier levels",
            "dependencies": ["brace and fill the offset-left socket while avoiding the shard's alternating lane", "time the far-right drop while the patrol continues moving", "brace the center support last", "steer the final artefact one column right", "fill all three shifted sockets"],
            "feedback": "the patrol route is drawn as a connected gray track and the shard advances one route marker after every committed action",
            "bypass_guard": "the patrol collision sets failed immediately, and the three shifted red sockets still require three visible supports and planned steering",
        },
    },
    4: {
        "layout": [
            "........",
            "#......#",
            "#S.....#",
            "#....g.#",
            "#......#",
            "#G.G.GG#",
            "#p.p.pp#",
            "########",
        ],
        "walls": [(r, c) for r, row in enumerate([
            "........",
            "#......#",
            "#S.....#",
            "#....g.#",
            "#......#",
            "#G.G.GG#",
            "#p.p.pp#",
            "########",
        ]) for c, ch in enumerate(row) if ch == "#"],
        "goals": [(5, 1), (5, 3), (5, 5), (5, 6)],
        "pit_cells": [(6, 1), (6, 3), (6, 5), (6, 6)],
        "brace_sites": [(6, 1), (6, 3), (6, 5), (6, 6)],
        "switches": [(2, 1)],
        "gate_cells": [(3, 5)],
        "initial_switch_on": False,
        "patrol_route": [(4, 2), (4, 4), (4, 2), (4, 4)],
        "patrol_start_idx": 0,
        "piece_spawns": [(0, 3), (0, 4), (0, 3), (0, 4), (0, 3)],
        "max_braces": 4,
        "budget": 34,
        "fog_radius": 5,
        "active_tags": ["switch", "patrol", "fog"],
        "goal_requirements": {"goals_filled": 4, "braces_placed": 4, "switch_on": True, "switches_used": 1},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "goals_filled",
            "primary_blocker": "four sockets stretch the lens supply exactly, while the switch-gate blocks the right lane and the patrol punishes careless waiting in the middle-left lane",
            "dependencies": ["brace and fill the far-left socket", "click the switch before routing to the far-right socket", "thread the right artefact through the open gate while the patrol is elsewhere", "spend the last two braces on the middle sockets", "complete the visible four-socket target under fog"],
            "feedback": "the switch and gate change shape together, the patrol advances along a connected gray route, filled sockets show black cores, and fog recedes around the active falling artefact",
            "bypass_guard": "every socket has an unbraced pit under it, the right route settles early against the closed gate unless switched on, and patrol contact fails the run",
        },
    },
    5: {
        "layout": [
            "........",
            "#......#",
            "#..S...#",
            "#....g.#",
            "#......#",
            "#GG.GGG#",
            "#pp.ppp#",
            "########",
        ],
        "walls": [(r, c) for r, row in enumerate([
            "........",
            "#......#",
            "#..S...#",
            "#....g.#",
            "#......#",
            "#GG.GGG#",
            "#pp.ppp#",
            "########",
        ]) for c, ch in enumerate(row) if ch == "#"],
        "goals": [(5, 1), (5, 2), (5, 4), (5, 5), (5, 6)],
        "pit_cells": [(6, 1), (6, 2), (6, 4), (6, 5), (6, 6)],
        "brace_sites": [(6, 1), (6, 2), (6, 4), (6, 5), (6, 6)],
        "switches": [(2, 3)],
        "gate_cells": [(3, 5)],
        "initial_switch_on": False,
        "patrol_route": [(4, 3), (4, 4), (4, 3), (4, 3)],
        "patrol_start_idx": 0,
        "piece_spawns": [(0, 3), (0, 4), (0, 3), (0, 4), (0, 3), (0, 4)],
        "max_braces": 5,
        "budget": 40,
        "fog_radius": 4,
        "active_tags": ["switch", "patrol", "fog"],
        "goal_requirements": {"goals_filled": 5, "braces_placed": 5, "switch_on": True, "switches_used": 1},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "goals_filled",
            "primary_blocker": "five sockets demand every lens brace, the switch must open the right-lane gate, and the patrol's central sweep makes the final center fill timing-sensitive",
            "dependencies": ["spend the first brace on the far-left socket", "open the gate before the far-right artefact reaches it", "use exact braces for the left-middle and right-middle sockets", "save the center brace for the final timed drop", "finish the five-socket pattern under tighter fog"],
            "feedback": "all five supports are visible as gray-black braces, the switch/gate visibly opens, the patrol route is a connected center track, and fog follows the active artefact",
            "bypass_guard": "unbraced supports are pits, the closed gate catches right-bound pieces before they reach a socket, and patrol collision fails the run before completion",
        },
    },
    6: {
        "layout": [
            "........",
            "#......#",
            "#.S....#",
            "#....g.#",
            "#......#",
            "#GGGGGG#",
            "#pppppp#",
            "########",
        ],
        "walls": [(r, c) for r, row in enumerate([
            "........",
            "#......#",
            "#.S....#",
            "#....g.#",
            "#......#",
            "#GGGGGG#",
            "#pppppp#",
            "########",
        ]) for c, ch in enumerate(row) if ch == "#"],
        "goals": [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6)],
        "pit_cells": [(6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)],
        "brace_sites": [(6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)],
        "switches": [(2, 2)],
        "gate_cells": [(3, 5)],
        "initial_switch_on": False,
        "piece_spawns": [(0, 3), (0, 4), (0, 3), (0, 4), (0, 3), (0, 4), (0, 3)],
        "max_braces": 6,
        "budget": 42,
        "fog_radius": 3,
        "active_tags": ["switch", "fog"],
        "goal_requirements": {"goals_filled": 6, "braces_placed": 6, "switch_on": True, "switches_used": 1},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "goals_filled",
            "primary_blocker": "all six prosper sockets are pits without lens supports, and the right-side gate must be opened before the far-right drop can pass",
            "dependencies": ["click the moon switch before committing to the right lane", "spend exactly one brace under each of the six sockets", "fill the outer columns first to preserve steering lanes", "pack the inner columns in a remembered order under tight fog", "finish with every red socket visibly black-filled"],
            "feedback": "each brace drains the lens HUD, each filled socket gets a black center, the gate changes to an open guide after the switch, and fog keeps only the local falling area clear",
            "bypass_guard": "there are no spare braces and unbraced sockets are pit cells, while the closed gate physically blocks the route to the far-right socket",
        },
    },
    6: {
        "layout": [
            "........",
            "#......#",
            "#.S....#",
            "#....g.#",
            "#......#",
            "#GGGGGG#",
            "#pppppp#",
            "########",
        ],
        "walls": [(r, c) for r, row in enumerate([
            "........",
            "#......#",
            "#.S....#",
            "#....g.#",
            "#......#",
            "#GGGGGG#",
            "#pppppp#",
            "########",
        ]) for c, ch in enumerate(row) if ch == "#"],
        "goals": [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6)],
        "pit_cells": [(6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)],
        "brace_sites": [(6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)],
        "switches": [(2, 2)],
        "gate_cells": [(3, 5)],
        "initial_switch_on": False,
        "piece_spawns": [(0, 3), (0, 4), (0, 3), (0, 4), (0, 3), (0, 4), (0, 3)],
        "max_braces": 6,
        "budget": 42,
        "fog_radius": 3,
        "active_tags": ["switch", "fog"],
        "goal_requirements": {"goals_filled": 6, "braces_placed": 6, "switch_on": True, "switches_used": 1},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "goals_filled",
            "primary_blocker": "all six prosper sockets are pits without lens supports, and the right-side gate must be opened before the far-right drop can pass",
            "dependencies": ["click the moon switch before committing to the right lane", "spend exactly one brace under each of the six sockets", "fill the outer columns first to preserve steering lanes", "pack the inner columns in a remembered order under tight fog", "finish with every red socket visibly black-filled"],
            "feedback": "each brace drains the lens HUD, each filled socket gets a black center, the gate changes to an open guide after the switch, and fog keeps only the local falling area clear",
            "bypass_guard": "there are no spare braces and unbraced sockets are pit cells, while the closed gate physically blocks the route to the far-right socket",
        },
    },
    7: {
        "layout": [
            "........",
            "#S...g.#",
            "##.....#",
            "#......#",
            "#......#",
            "#GGGGGG#",
            "#pppppp#",
            "########",
        ],
        "walls": [(r, c) for r, row in enumerate([
            "........",
            "#S...g.#",
            "##.....#",
            "#......#",
            "#......#",
            "#GGGGGG#",
            "#pppppp#",
            "########",
        ]) for c, ch in enumerate(row) if ch == "#"],
        "goals": [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6)],
        "pit_cells": [(6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)],
        "brace_sites": [(6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)],
        "switches": [(1, 1)],
        "gate_cells": [(1, 5)],
        "initial_switch_on": False,
        "patrol_route": [(4, 3), (4, 5), (4, 4), (4, 5), (4, 4), (4, 3), (4, 4)],
        "patrol_start_idx": 0,
        "piece_spawns": [(0, 3), (0, 4), (0, 3), (0, 4), (0, 3), (0, 4), (0, 3)],
        "max_braces": 6,
        "budget": 43,
        "fog_radius": 2,
        "active_tags": ["switch", "patrol", "fog"],
        "goal_requirements": {"goals_filled": 6, "braces_placed": 6, "switch_on": True, "switches_used": 1},
        "design_contract": {
            "success_trigger": "board_matches_target",
            "state_key": "goals_filled",
            "primary_blocker": "the final well combines exact six-brace packing, a top gate that blocks the right route unless switched, tight fog, and a central patrol phase that punishes the wrong inner-column timing",
            "dependencies": ["open the top gate with the local switch before routing right", "place all six lens braces with no spare support", "fill the two outer sockets first", "pack the inner sockets in a phase-safe order around the patrol", "finish the fully filled six-socket moon pattern"],
            "feedback": "the switch/gate visibly opens, every brace and filled socket is shown locally, the patrol route is a connected gray track, and only a small fog window follows the falling artefact",
            "bypass_guard": "unbraced targets are pits, the closed top gate physically blocks the right steering lane, and patrol contact immediately fails the run before the board can match the target",
        },
    }
}


def _cell_rect(row, col):
    y0 = BOARD_TOP + row * CELL
    x0 = BOARD_LEFT + col * CELL
    return y0, x0


def _draw_entity(grid, row, col, entity_type):
    y0, x0 = _cell_rect(row, col)
    if row < 0 or col < 0:
        return
    if entity_type == "wall":
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                if 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                    grid[y][x] = COLORS["wall"] if (x + y) % 3 != 0 else BG_COLOR
    elif entity_type == "goal":
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                if 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                    if y in (y0, y0 + CELL - 1) or x in (x0, x0 + CELL - 1):
                        grid[y][x] = COLORS["goal"]
    elif entity_type == "brace_site":
        pts = [(0, 0), (0, 1), (1, 0), (0, 5), (1, 5), (0, 4), (5, 0), (4, 0), (5, 1), (5, 5), (5, 4), (4, 5)]
        for dy, dx in pts:
            y, x = y0 + dy, x0 + dx
            if 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                grid[y][x] = COLORS["pit"]
    elif entity_type == "patrol_route":
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                if 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                    if y == y0 + CELL // 2 or x in (x0, x0 + CELL - 1):
                        grid[y][x] = COLORS["wall"]
    elif entity_type == "patrol":
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                if 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                    if (x - x0) + (y - y0) in (2, 3, 4, 5, 6) or y == y0 + CELL - 2:
                        grid[y][x] = COLORS["settled"]
                    elif y in (y0, y0 + CELL - 1) or x in (x0, x0 + CELL - 1):
                        grid[y][x] = COLORS["goal"]
    elif entity_type == "switch_off":
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                if 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                    if y in (y0, y0 + CELL - 1) or x in (x0, x0 + CELL - 1):
                        grid[y][x] = COLORS["wall"]
                    elif (x + y) % 2 == 0:
                        grid[y][x] = COLORS["goal"]
    elif entity_type == "switch_on":
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                if 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                    if y in (y0, y0 + CELL - 1) or x in (x0, x0 + CELL - 1):
                        grid[y][x] = COLORS["goal"]
                    elif y == y0 + CELL // 2 or x == x0 + CELL // 2:
                        grid[y][x] = COLORS["settled"]
    elif entity_type == "gate_closed":
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                if 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                    grid[y][x] = COLORS["goal"] if (y - y0 + x - x0) % 2 == 0 else COLORS["wall"]
    elif entity_type == "gate_open":
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                if 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                    if y in (y0, y0 + CELL - 1) or x in (x0, x0 + CELL - 1):
                        grid[y][x] = COLORS["wall"]
                    elif y == y0 + CELL // 2:
                        grid[y][x] = COLORS["goal"]
    elif entity_type == "brace":
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                if 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                    if y in (y0, y0 + CELL - 1) or x in (x0, x0 + CELL - 1):
                        grid[y][x] = COLORS["brace"]
                    elif (y == y0 + CELL // 2) or (x == x0 + CELL // 2):
                        grid[y][x] = COLORS["settled"]
    elif entity_type == "settled":
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                if 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                    grid[y][x] = COLORS["settled"] if not (y == y0 + 2 and x == x0 + 2) else BG_COLOR
    elif entity_type == "settled_goal":
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                if 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                    if y in (y0, y0 + CELL - 1) or x in (x0, x0 + CELL - 1):
                        grid[y][x] = COLORS["goal"]
                    else:
                        grid[y][x] = COLORS["settled"]
    elif entity_type == "player":
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                if 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                    if y in (y0 + 2, y0 + 3) or x in (x0 + 2, x0 + 3):
                        grid[y][x] = COLORS["player"]
        for y in (y0 + 1, y0 + 4):
            for x in (x0 + 1, x0 + 4):
                if 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                    grid[y][x] = COLORS["player"]


def _pixel_to_cell(x, y):
    col = (x - BOARD_LEFT) // CELL
    row = (y - BOARD_TOP) // CELL
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        return (row, col)
    return None


def _solid_cells(h, lvl):
    solids = set(tuple(p) for p in lvl["walls"]) | set(tuple(p) for p in h.get("braces", [])) | set(tuple(p) for p in h.get("settled", []))
    if "switch" in lvl.get("active_tags", []) and not h.get("switch_on", False):
        solids |= set(tuple(p) for p in lvl.get("gate_cells", []))
    return solids


def _patrol_pos(h, lvl):
    route = lvl.get("patrol_route", [])
    if not route:
        return None
    return tuple(route[h.get("patrol_idx", 0) % len(route)])


def _can_occupy(h, lvl, row, col):
    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        return False
    return (row, col) not in _solid_cells(h, lvl)


def _update_goals(h, lvl):
    settled = set(tuple(p) for p in h.get("settled", []))
    h["goals_filled"] = sum(1 for g in lvl["goals"] if tuple(g) in settled)


def _spawn_next(h, lvl):
    spawns = lvl["piece_spawns"]
    if h["piece_index"] < len(spawns):
        r, c = spawns[h["piece_index"]]
        h["active_r"] = r
        h["active_c"] = c
        h["orientation"] = h["piece_index"] % 2
    else:
        h["active_r"] = None
        h["active_c"] = None
        h["failed"] = True


def _finish_active(h, lvl, settled):
    if h.get("active_r") is None:
        return
    if settled:
        h.setdefault("settled", []).append((h["active_r"], h["active_c"]))
    else:
        h["lost_pieces"] = h.get("lost_pieces", 0) + 1
    h["piece_index"] += 1
    _update_goals(h, lvl)
    if h["goals_filled"] >= len(lvl["goals"]):
        h["active_r"] = None
        h["active_c"] = None
        h["complete"] = True
    else:
        _spawn_next(h, lvl)


def _resolve_fall(h, lvl):
    if h.get("active_r") is None:
        return
    pits = set(tuple(p) for p in lvl.get("pit_cells", []))
    braces = set(tuple(p) for p in h.get("braces", []))
    cur = (h["active_r"], h["active_c"])
    if cur in pits and cur not in braces:
        _finish_active(h, lvl, settled=False)
        return
    nr, nc = h["active_r"] + 1, h["active_c"]
    if _can_occupy(h, lvl, nr, nc):
        h["active_r"] = nr
        cur = (h["active_r"], h["active_c"])
        if cur in pits and cur not in braces:
            _finish_active(h, lvl, settled=False)
            return
        if not _can_occupy(h, lvl, h["active_r"] + 1, h["active_c"]):
            _finish_active(h, lvl, settled=True)
    else:
        _finish_active(h, lvl, settled=True)


def transition(h_t: dict, z_t: dict, a_t: int) -> dict:
    """Deterministic history state update (DreamerV3 sequence model)."""
    h = copy.deepcopy(h_t)
    base = a_t[0] if isinstance(a_t, tuple) and len(a_t) > 0 else a_t
    if base not in get_available_actions():
        return h
    level = h.get("level", 0)
    lvl = LEVELS[level]
    if base == 0:
        return get_initial_state(level)[0]
    if h.get("complete") or h.get("failed") or h.get("budget_remaining", 0) <= 0:
        return h

    committed = False

    if base == 6:
        if not (isinstance(a_t, tuple) and len(a_t) == 3):
            return h
        cell = _pixel_to_cell(a_t[1], a_t[2])
        if cell is None:
            return h
        if "switch" in lvl.get("active_tags", []) and cell in [tuple(p) for p in lvl.get("switches", [])]:
            h["switch_on"] = not h.get("switch_on", False)
            h["switches_used"] = h.get("switches_used", 0) + 1
            committed = True
        elif (cell in [tuple(p) for p in lvl["brace_sites"]] and
                cell not in [tuple(p) for p in h.get("braces", [])] and
                h.get("braces_remaining", 0) > 0 and
                cell not in [tuple(p) for p in h.get("settled", [])]):
            h["braces"].append(cell)
            h["braces_remaining"] -= 1
            h["braces_placed"] += 1
            committed = True
        else:
            return h
    elif base in (1, 2, 3, 4, 5):
        if h.get("active_r") is None:
            return h
        if base == 1:
            h["orientation"] = 1 - h.get("orientation", 0)
            committed = True
        elif base == 2:
            nr, nc = h["active_r"] + 1, h["active_c"]
            if _can_occupy(h, lvl, nr, nc):
                h["active_r"] = nr
            committed = True
        elif base == 3:
            nr, nc = h["active_r"], h["active_c"] - 1
            if not _can_occupy(h, lvl, nr, nc):
                return h
            h["active_c"] = nc
            committed = True
        elif base == 4:
            nr, nc = h["active_r"], h["active_c"] + 1
            if not _can_occupy(h, lvl, nr, nc):
                return h
            h["active_c"] = nc
            committed = True
        elif base == 5:
            committed = True

    if not committed:
        return h

    _resolve_fall(h, lvl)
    if "patrol" in lvl.get("active_tags", []):
        p = _patrol_pos(h, lvl)
        if p is not None and h.get("active_r") is not None and (h["active_r"], h["active_c"]) == p:
            h["failed"] = True
        if not h.get("failed") and not check_level_complete(h, {}, level):
            route = lvl.get("patrol_route", [])
            if route:
                h["patrol_idx"] = (h.get("patrol_idx", 0) + 1) % len(route)
                h["patrol_steps"] = h.get("patrol_steps", 0) + 1
                p = _patrol_pos(h, lvl)
                if p is not None and h.get("active_r") is not None and (h["active_r"], h["active_c"]) == p:
                    h["failed"] = True
    h["step"] += 1
    h["budget_remaining"] -= 1
    _update_goals(h, lvl)
    if check_level_complete(h, {}, level):
        h["complete"] = True
        h["failed"] = False
        return h
    if h["budget_remaining"] <= 0:
        h["failed"] = True
    return h


def predict(h_t: dict) -> dict:
    """Return minimal/empty z_t. This game is fully deterministic."""
    return {}


def check_level_complete(h_t: dict, z_t: dict, level: int) -> bool:
    """Check if the current level's goal has been achieved."""
    if h_t.get("level") != level or h_t.get("failed"):
        return False
    lvl = LEVELS[level]
    req = lvl.get("goal_requirements", {})
    settled = set(tuple(p) for p in h_t.get("settled", []))
    visible_filled = sum(1 for g in lvl["goals"] if tuple(g) in settled)
    if visible_filled < req.get("goals_filled", len(lvl["goals"])):
        return False
    if h_t.get("braces_placed", 0) < req.get("braces_placed", 0):
        return False
    if req.get("switch_on", False) and not h_t.get("switch_on", False):
        return False
    if h_t.get("switches_used", 0) < req.get("switches_used", 0):
        return False
    if h_t.get("patrol_steps", 0) < req.get("patrol_steps", 0):
        return False
    return True


def render(h_t: dict, z_t: dict) -> list[list[int]]:
    """Render the current state as a 64x64 grid."""
    lvl = LEVELS[h_t["level"]]
    grid = [[BG_COLOR for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # HUD: budget bar and lens markers.
    max_budget = max(1, lvl["budget"])
    remaining = max(0, h_t.get("budget_remaining", 0))
    width = 48
    filled = int(width * remaining / max_budget)
    for x in range(8, 8 + width):
        grid[1][x] = COLORS["wall"]
    for x in range(8, 8 + filled):
        grid[2][x] = COLORS["settled"]
    for i in range(lvl["max_braces"]):
        x0 = 8 + i * 8
        col = COLORS["brace"] if i < h_t.get("braces_remaining", 0) else COLORS["warn"]
        for y in range(4, 8):
            for x in range(x0, x0 + 4):
                grid[y][x] = col

    for r, c in lvl["walls"]:
        _draw_entity(grid, r, c, "wall")
    if "switch" in lvl.get("active_tags", []):
        for r, c in lvl.get("gate_cells", []):
            _draw_entity(grid, r, c, "gate_open" if h_t.get("switch_on", False) else "gate_closed")
        for r, c in lvl.get("switches", []):
            _draw_entity(grid, r, c, "switch_on" if h_t.get("switch_on", False) else "switch_off")
    if "patrol" in lvl.get("active_tags", []):
        for r, c in lvl.get("patrol_route", []):
            _draw_entity(grid, r, c, "patrol_route")
    for r, c in lvl.get("pit_cells", []):
        if (r, c) not in [tuple(p) for p in h_t.get("braces", [])]:
            _draw_entity(grid, r, c, "brace_site")
    for r, c in lvl["goals"]:
        _draw_entity(grid, r, c, "goal")
    for r, c in h_t.get("braces", []):
        _draw_entity(grid, r, c, "brace")
    goal_set = set(tuple(p) for p in lvl["goals"])
    for r, c in h_t.get("settled", []):
        _draw_entity(grid, r, c, "settled_goal" if (r, c) in goal_set else "settled")
    if "patrol" in lvl.get("active_tags", []):
        p = _patrol_pos(h_t, lvl)
        if p is not None:
            _draw_entity(grid, p[0], p[1], "patrol")
    if h_t.get("active_r") is not None:
        _draw_entity(grid, h_t["active_r"], h_t["active_c"], "player")

    fog = lvl.get("fog_radius")
    if fog is not None and h_t.get("active_r") is not None:
        cy = BOARD_TOP + h_t["active_r"] * CELL + CELL // 2
        cx = BOARD_LEFT + h_t["active_c"] * CELL + CELL // 2
        radius = fog * CELL
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if abs(y - cy) + abs(x - cx) > radius:
                    grid[y][x] = COLORS["wall"] if (x + y) % 2 == 0 else BG_COLOR

    return grid


def get_initial_state(level: int) -> tuple[dict, dict]:
    """Get the initial (h_t, z_t) for a given level."""
    lvl = LEVELS[level]
    r, c = lvl["piece_spawns"][0]
    h = {
        "level": level,
        "step": 0,
        "budget_remaining": lvl["budget"],
        "active_r": r,
        "active_c": c,
        "orientation": 0,
        "piece_index": 0,
        "settled": [],
        "braces": [],
        "braces_remaining": lvl["max_braces"],
        "braces_placed": 0,
        "goals_filled": 0,
        "lost_pieces": 0,
        "complete": False,
        "failed": False,
        "switch_on": lvl.get("initial_switch_on", False),
        "switches_used": 0,
        "patrol_idx": lvl.get("patrol_start_idx", 0),
        "patrol_steps": 0,
    }
    return h, predict(h)


def get_available_actions() -> list[int]:
    """Return available action integers for this game."""
    return [0, 1, 2, 3, 4, 5, 6]


def solve_level(level: int) -> list:
    """Return a fixed sequence of actions that solves this level."""
    if level == 0:
        left_brace = (6, BOARD_LEFT + 2 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        right_brace = (6, BOARD_LEFT + 5 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        return [
            left_brace,
            3,
            5,
            5,
            5,
            right_brace,
            4,
            5,
            5,
            5,
        ]
    if level == 1:
        left_brace = (6, BOARD_LEFT + 1 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        center_brace = (6, BOARD_LEFT + 4 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        right_brace = (6, BOARD_LEFT + 6 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        return [
            left_brace,
            3,
            3,
            5,
            5,
            right_brace,
            4,
            4,
            5,
            5,
            center_brace,
            4,
            5,
            5,
            5,
        ]
    if level == 2:
        left_brace = (6, BOARD_LEFT + 1 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        center_brace = (6, BOARD_LEFT + 4 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        right_brace = (6, BOARD_LEFT + 6 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        switch_click = (6, BOARD_LEFT + 1 * CELL + CELL // 2, BOARD_TOP + 2 * CELL + CELL // 2)
        return [
            left_brace,
            3,
            3,
            5,
            5,
            switch_click,
            right_brace,
            4,
            4,
            5,
            5,
            center_brace,
            4,
            5,
            5,
            5,
        ]
    if level == 3:
        left_brace = (6, BOARD_LEFT + 2 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        center_brace = (6, BOARD_LEFT + 4 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        right_brace = (6, BOARD_LEFT + 6 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        return [
            left_brace,
            3,
            5,
            5,
            5,
            right_brace,
            4,
            4,
            5,
            5,
            center_brace,
            4,
            5,
            5,
            5,
        ]
    if level == 4:
        left_brace = (6, BOARD_LEFT + 1 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        mid_left_brace = (6, BOARD_LEFT + 3 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        mid_right_brace = (6, BOARD_LEFT + 5 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        right_brace = (6, BOARD_LEFT + 6 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        switch_click = (6, BOARD_LEFT + 1 * CELL + CELL // 2, BOARD_TOP + 2 * CELL + CELL // 2)
        return [
            left_brace,
            3,
            3,
            5,
            5,
            switch_click,
            right_brace,
            4,
            4,
            5,
            5,
            mid_left_brace,
            5,
            5,
            5,
            5,
            mid_right_brace,
            4,
            5,
            5,
            5,
        ]
    if level == 5:
        far_left = (6, BOARD_LEFT + 1 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        left_mid = (6, BOARD_LEFT + 2 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        center = (6, BOARD_LEFT + 4 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        right_mid = (6, BOARD_LEFT + 5 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        far_right = (6, BOARD_LEFT + 6 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        switch_click = (6, BOARD_LEFT + 3 * CELL + CELL // 2, BOARD_TOP + 2 * CELL + CELL // 2)
        return [
            far_left,
            3,
            3,
            5,
            5,
            switch_click,
            far_right,
            4,
            4,
            5,
            left_mid,
            3,
            5,
            5,
            5,
            right_mid,
            4,
            5,
            5,
            5,
            center,
            4,
            5,
            5,
            5,
        ]
    if level == 6:
        c1 = (6, BOARD_LEFT + 1 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        c2 = (6, BOARD_LEFT + 2 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        c3 = (6, BOARD_LEFT + 3 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        c4 = (6, BOARD_LEFT + 4 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        c5 = (6, BOARD_LEFT + 5 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        c6 = (6, BOARD_LEFT + 6 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        switch_click = (6, BOARD_LEFT + 2 * CELL + CELL // 2, BOARD_TOP + 2 * CELL + CELL // 2)
        return [
            switch_click,
            c1,
            3,
            3,
            5,
            c6,
            4,
            4,
            5,
            5,
            c2,
            3,
            5,
            5,
            5,
            c5,
            4,
            5,
            5,
            5,
            c3,
            5,
            5,
            5,
            5,
            c4,
            5,
            5,
            5,
            5,
        ]
    if level == 7:
        c1 = (6, BOARD_LEFT + 1 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        c2 = (6, BOARD_LEFT + 2 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        c3 = (6, BOARD_LEFT + 3 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        c4 = (6, BOARD_LEFT + 4 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        c5 = (6, BOARD_LEFT + 5 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        c6 = (6, BOARD_LEFT + 6 * CELL + CELL // 2, BOARD_TOP + 6 * CELL + CELL // 2)
        switch_click = (6, BOARD_LEFT + 1 * CELL + CELL // 2, BOARD_TOP + 1 * CELL + CELL // 2)
        return [
            switch_click,
            c1,
            3,
            3,
            5,
            c6,
            4,
            4,
            5,
            5,
            c2,
            3,
            5,
            5,
            5,
            c5,
            4,
            5,
            5,
            5,
            c3,
            5,
            5,
            5,
            5,
            c4,
            5,
            5,
            5,
            5,
        ]
    return []


# ---------------------------------------------------------------------------
# AUTO-GENERATED SDK adapter (arc_agi_3.game_creator.build_generated_environments).
# Everything above is the verbatim game_functions.py source.
# ---------------------------------------------------------------------------
from arc_agi_3.game_creator.arcengine_adapter import (
    FunctionalArcGame as _FunctionalArcGame,
)


class Ml2048(_FunctionalArcGame):
    GAME_ID = "ml2048-a6677a07"
    NUM_LEVELS = 8
    FUNCTIONS = {
        "transition": transition,
        "predict": predict,
        "check_level_complete": check_level_complete,
        "render": render,
        "get_initial_state": get_initial_state,
        "get_available_actions": get_available_actions,
    }
