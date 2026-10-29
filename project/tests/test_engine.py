"""Canvas drawing and the game clock."""

import config
from engine.canvas import Canvas, wrap
from engine.state import GameState


def test_canvas_clips_text_at_the_edges():
    canvas = Canvas()
    canvas.put(0, 75, "HELLO WORLD")
    canvas.put(-1, 0, "above")
    canvas.put(config.SCREEN_HEIGHT, 0, "below")
    lines = canvas.text_lines()
    assert len(lines) == config.SCREEN_HEIGHT
    assert all(len(line) == config.SCREEN_WIDTH for line in lines)
    assert lines[0].endswith("HELLO")


def test_art_mask_paints_background_behind_spaces():
    canvas = Canvas()
    canvas.draw_art(0, 0, ["A B"], mask=["xxx"], palette={"x": "poster_red"})
    assert canvas.cells[0][1][2] != -1      # the space got a background
    canvas.draw_art(1, 0, ["A B"])           # no mask: the space is skipped
    assert canvas.cells[1][1][2] == -1


def test_style_with_no_background_keeps_the_old_one():
    canvas = Canvas()
    canvas.set_cell(0, 0, " ", "wall")
    background = canvas.cells[0][0][2]
    canvas.set_cell(0, 0, "o", "skin")
    assert canvas.cells[0][0][2] == background


def test_wrap():
    assert wrap("one two three", 7) == ["one two", "three"]
    assert wrap("", 10) == [""]
    assert wrap("abcdefghij", 4) == ["abcd", "efgh", "ij"]


def test_clock_text_and_time_left():
    state = GameState()
    assert state.clock_text() == "00:42"
    assert state.minutes_left() == 48
    state.spend(30)
    assert state.minutes_left() == 48       # rounds up partial minutes
    state.spend(60 * 60)
    assert state.clock_text() == "01:30"    # never past the seal time
    assert state.out_of_time()


def test_boundary_one_second_before_seal():
    state = GameState()
    state.time = config.SEAL_TIME - 1
    assert not state.out_of_time()
    state.spend(1)
    assert state.out_of_time()


def test_messages_are_wrapped_and_limited():
    state = GameState()
    state.say("word " * 40)
    assert all(len(text) <= config.SCREEN_WIDTH - 2
               for text, _style, _number in state.messages)
    for index in range(100):
        state.say(f"message {index}")
    assert len(state.messages) <= 30
    assert state.recent_messages()[-1][0] == "message 99"
