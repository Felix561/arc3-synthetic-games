import pytest
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

from arc3_synthetic_games.dataset import catalog, dataset_root
from arc3_synthetic_games.native import NativeGame

GAMES = catalog()["games"]


@pytest.mark.parametrize("entry", GAMES, ids=lambda g: g["id"])
def test_seven_level_selection_reset_and_session_independence(entry):
    game = NativeGame(entry["game_id"])
    for level in range(7):
        first = game.select_level(level)
        assert first["level_index"] == level
        assert first["state"] == "NOT_FINISHED"
        assert sorted(first["available_actions"]) == sorted(entry["controls"])
        first_pixels = first["frames"][-1]
        action = next(a for a in entry["controls"] if a != 7)
        after = game.act(action, {"x": 32, "y": 32} if action == 6 else {})
        current_level = after["level_index"]
        reset = game.reset()
        independent = NativeGame(entry["id"], current_level)
        assert reset["level_index"] == current_level
        assert independent.observation["frames"][-1] == reset["frames"][-1]
        if current_level == level:
            assert reset["frames"][-1] == first_pixels
    assert game.restart()["level_index"] == 0


@pytest.mark.parametrize("entry", GAMES, ids=lambda g: g["id"])
def test_clean_official_sdk_discovery_and_action(entry):
    arcade = Arcade(
        operation_mode=OperationMode.OFFLINE, environments_dir=str(dataset_root() / "environment_files")
    )
    env = arcade.make(entry["game_id"], seed=0, save_recording=False)
    assert env is not None
    frame = env.reset()
    assert frame.state.value == "NOT_FINISHED"
    action = next(a for a in frame.available_actions if a != 7)
    result = env.step(GameAction.from_id(action), data={"x": 32, "y": 32} if action == 6 else {})
    assert result is not None and result.frame


def test_reject_invalid_actions_and_coordinates():
    game = NativeGame("sg06")
    for action, data in [
        (True, {}),
        (1, {}),
        (6, {"x": -1, "y": 0}),
        (6, {"x": True, "y": 0}),
        (6, {"x": 64, "y": 0}),
        (6, {"x": 0, "y": 0, "extra": 1}),
    ]:
        with pytest.raises(ValueError):
            game.act(action, data)
    with pytest.raises(ValueError):
        game.select_level(7)


@pytest.mark.parametrize("terminal", ["WIN", "GAME_OVER"])
def test_terminal_input_guard_uses_native_state_names(terminal):
    game = NativeGame("sg06")
    # A focused guard test; this does not assert an actual completed playthrough.
    game.observation["state"] = terminal
    with pytest.raises(ValueError, match="Reset this level"):
        game.act(6, {"x": 32, "y": 32})
