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
