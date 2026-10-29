"""Play the game without a terminal by sending keys to the Game object."""

import config
from engine.canvas import Canvas
from engine.game import Game
from scenes.ending import EndingScene
from scenes.explore import ExploreScene
from scenes.intro import IntroScene
from scenes.overlays import ReadOverlay
from scenes.puzzle_scene import PuzzleScene
from scenes.title import TitleScene


def start_game():
    """Title -> intro -> skip -> standing on the platform."""
    game = Game()
    game.reset_to(TitleScene(game))
    game.handle_key("enter")
    assert isinstance(game.top, IntroScene)
    game.handle_key("space")        # skip the animation
    game.handle_key("space")        # start playing
    assert isinstance(game.top, ExploreScene)
    return game


def press(game, *keys):
    for key in keys:
        game.handle_key(key)


def draw(game):
    canvas = Canvas()
    game.draw(canvas)
    return canvas.text_lines()


def stand_at(game, x, y):
    game.state.x, game.state.y = x, y


def test_new_game_starts_on_the_platform_at_0042():
    game = start_game()
    assert game.state.room == "platform"
    assert game.state.clock_text() == "00:42"
    assert "00:42" in draw(game)[0]


def test_each_step_costs_time_but_bumping_a_wall_does_not():
    game = start_game()
    state = game.state
    before = state.time
    press(game, "a")
    assert state.time == before + config.STEP_SECONDS
    stand_at(game, 41, 4)               # right under the back wall
    before = state.time
    press(game, "w")
    assert (state.x, state.y) == (41, 4)
    assert state.time == before


def test_overlays_cost_no_time():
    game = start_game()
    before = game.state.time
    for key in ("?", "m", "i"):
        press(game, key)
        draw(game)                      # every overlay draws without error
        press(game, "esc")
    assert game.state.time == before
    assert isinstance(game.top, ExploreScene)


def test_locked_gate_blocks_the_player():
    game = start_game()
    stand_at(game, 75, 8)
    press(game, "d")
    assert game.state.room == "platform"
    assert "locked" in game.state.messages[-1][0]


def find_all_receipts(game):
    for x, y in [(23, 6), (61, 9), (41, 10)]:   # machine, bin, bench
        stand_at(game, x, y)
        press(game, "e")
        assert isinstance(game.top, ReadOverlay)
        press(game, "esc")
    assert game.state.clues == {"receipt_a", "receipt_b", "receipt_c"}


def open_keypad(game):
    stand_at(game, 73, 5)
    press(game, "e")
    assert isinstance(game.top, PuzzleScene)


def test_full_platform_route_to_the_concourse():
    game = start_game()
    find_all_receipts(game)
    open_keypad(game)
    draw(game)
    before = game.state.time
    press(game, "1", "2", "3", "enter")         # wrong code
    assert game.state.time == before + config.WRONG_ANSWER_SECONDS
    press(game, "h")                            # one hint
    assert game.state.hints_used["gate_code"] == 1
    press(game, "9", "6", "4", "enter")         # right code
    assert "gate_code" in game.state.solved
    press(game, "esc")                          # close "task complete"
    stand_at(game, 75, 8)
    press(game, "d")
    assert game.state.room == "concourse"
    assert "concourse" in game.state.visited
    draw(game)


def test_solved_task_cannot_be_opened_again():
    game = start_game()
    game.state.solved.add("gate_code")
    stand_at(game, 73, 5)
    press(game, "e")
    assert isinstance(game.top, ExploreScene)


def test_fragment_is_collected_once():
    game = start_game()
    stand_at(game, 5, 11)
    press(game, "e")
    assert game.state.fragments == {"ticket_0300"}
    press(game, "esc", "e")                     # the spot is gone now
    assert isinstance(game.top, ExploreScene)


def test_running_out_of_time_gives_the_trapped_ending():
    game = start_game()
    game.state.time = config.SEAL_TIME - 1
    press(game, "a")
    assert isinstance(game.top, EndingScene)
    assert game.state.ending == "trapped"
    assert "01:30" in "".join(draw(game))
    press(game, "r")                            # restart
    assert isinstance(game.top, IntroScene)
    assert game.state.clock_text() == "00:42"


def test_wrong_answer_can_also_run_out_the_clock():
    game = start_game()
    open_keypad(game)
    game.state.time = config.SEAL_TIME - 60
    press(game, "1", "2", "3", "enter")
    assert isinstance(game.top, EndingScene)


def test_quit_needs_confirmation():
    game = start_game()
    press(game, "q", "n")
    assert game.running
    press(game, "q", "y")
    assert not game.running


def test_every_screen_fits_80_by_24():
    game = start_game()
    for frame in range(0, 200, 7):              # animations at many frames
        game.frame = frame
        lines = draw(game)
        assert len(lines) == 24 and all(len(line) == 80 for line in lines)
    intro = Game()
    intro.new_game()
    for frame in range(0, 150, 3):
        intro.frame = frame
        draw(intro)


# ----- whole runs through each route -------------------------------------
import pytest  # noqa: E402

import engine.canvas  # noqa: E402
from engine.styles import STYLES  # noqa: E402
from scenes.platform_zero import PlatformZeroScene  # noqa: E402
from tests.test_route_puzzles import (safe_tunnel_keys, solve_boxes,  # noqa: E402
                                      wire_keys)


@pytest.fixture(autouse=True)
def strict_styles(monkeypatch):
    """Fail if any drawing code uses a style name that does not exist."""
    real = engine.canvas.style

    def checked(name):
        assert name in STYLES, f"unknown style {name!r}"
        return real(name)
    monkeypatch.setattr(engine.canvas, "style", checked)


def use(game, x, y, *keys):
    """Stand at (x, y), press E, then the given keys, drawing every screen."""
    stand_at(game, x, y)
    press(game, "e")
    for key in keys:
        draw(game)
        press(game, key)
    draw(game)


def close_popup(game):
    assert isinstance(game.top, ReadOverlay)
    press(game, "esc")


def reach_concourse(game):
    find_all_receipts(game)
    open_keypad(game)
    press(game, "9", "6", "4", "enter")
    close_popup(game)
    stand_at(game, 75, 8)
    press(game, "d")
    assert game.state.room == "concourse"


def choose_route(game, keys, door_x, room):
    use(game, 13, 10, *keys)
    close_popup(game)
    stand_at(game, door_x, 4)
    press(game, "w")
    assert game.state.room == room


def finish_in_exit_hall(game, enter_from_concourse=True):
    if enter_from_concourse:
        stand_at(game, 39, 14)
        press(game, "s", "s")                    # back to the concourse
        assert game.state.room == "concourse"
        stand_at(game, 75, 8)
        press(game, "d")
    assert game.state.room == "exit_hall"
    stand_at(game, 75, 8)
    press(game, "d")                             # shutter still down
    assert game.state.room == "exit_hall"
    use(game, 37, 5, "w", "w", "d", "d", "w", "d", "w", "w", "e")
    assert "shutter_released" in game.state.flags
    close_popup(game)


def walk_out(game):
    stand_at(game, 75, 8)
    press(game, "d")
    assert isinstance(game.top, EndingScene)
    draw(game)
    return game.state.ending


def test_tech_route_escape():
    game = start_game()
    reach_concourse(game)
    choose_route(game, ["3", "e", "y"], 14, "control_room")
    stand_at(game, 67, 5)
    press(game, "e")                             # wiring before breakers
    assert "breakers" in game.state.messages[-1][0]
    use(game, 10, 5, "w", "e", "s", "a", "e", "d", "d", "e", "s", "e")
    close_popup(game)
    use(game, 67, 5, *wire_keys())
    close_popup(game)
    assert game.state.has("signal_log")
    finish_in_exit_hall(game)
    assert walk_out(game) == "escape"
    assert game.state.tasks_done() == 5


def test_human_route_escape():
    game = start_game()
    reach_concourse(game)
    choose_route(game, ["s", "1", "e", "y"], 39, "ticket_office")
    use(game, 10, 5, "1", "5", "0", "4", "enter")
    close_popup(game)
    assert game.state.has("staff_logbook")
    use(game, 64, 5, "d", "e")
    close_popup(game)
    finish_in_exit_hall(game)
    assert walk_out(game) == "escape"


def test_sneak_route_and_true_ending():
    game = start_game()
    game.state.fragments.update({"ticket_0300", "newspaper"})
    reach_concourse(game)
    choose_route(game, ["s", "s", "4", "e", "y"], 64, "storeroom")
    stand_at(game, 70, 5)                        # fragment 3 on the shelf
    press(game, "e")
    close_popup(game)
    assert len(game.state.fragments) == 3
    use(game, 39, 12, *solve_boxes())
    close_popup(game)
    use(game, 39, 12, *safe_tunnel_keys())
    close_popup(game)
    finish_in_exit_hall(game, enter_from_concourse=False)
    stand_at(game, 10, 4)
    press(game, "w")                             # the hidden door
    assert isinstance(game.top, PlatformZeroScene)
    for frame in range(0, 60, 5):
        game.frame = frame
        draw(game)
    press(game, "space", "b")
    assert game.state.ending == "true_board"
    draw(game)


def test_hidden_door_stays_shut_without_fragments():
    game = start_game()
    game.state.flags.add("shutter_released")
    game.state.room = "exit_hall"
    stand_at(game, 10, 4)
    press(game, "w")
    assert isinstance(game.top, ExploreScene)
    game.state.fragments.update({"a", "b", "c"})
    press(game, "w")
    assert isinstance(game.top, PlatformZeroScene)
    press(game, "space", "l")
    assert game.state.ending == "true_leave"


def test_route_doors_need_their_key():
    game = start_game()
    game.state.room = "concourse"
    for door_x in (14, 39, 64):
        stand_at(game, door_x, 4)
        press(game, "w")
        assert game.state.room == "concourse"
    game.state.flags.add("route_human")
    stand_at(game, 14, 4)
    press(game, "w")
    assert game.state.room == "concourse"        # still the wrong door


def test_leaving_a_puzzle_keeps_its_progress():
    game = start_game()
    open_keypad(game)
    press(game, "9", "6", "esc")
    open_keypad(game)
    assert game.top.puzzle.entry == "96"


def test_alarm_ending_from_the_tunnel():
    from tests.test_route_puzzles import careless_tunnel_keys
    game = start_game()
    game.state.room = "storeroom"
    game.state.flags.add("hatch_clear")
    use(game, 39, 12)
    before = game.state.time
    press(game, *careless_tunnel_keys())
    assert game.state.time == before + 5 * 60
    press(game, *careless_tunnel_keys())
    assert isinstance(game.top, EndingScene)
    assert game.state.ending == "alarm"
