"""Tunable numbers for the whole game, kept in one place for balancing."""

# Screen layout
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 24
STATUS_ROW = 0
MAP_TOP = 1
MAP_HEIGHT = 18
PROMPT_ROW = 19
MESSAGE_TOP = 20
MESSAGE_LINES = 3
KEYS_ROW = 23

# Clock (time) in seconds after midnight.
START_TIME = 42 * 60    # 00:42
SEAL_TIME = 90 * 60     # 01:30
WARNING_TIME = 10 * 60

# Time costs in seconds. One key press = one turn; only these actions move the clock forward.
STEP_SECONDS = 4
WRONG_ANSWER_SECONDS = 3 * 60
HINT_SECONDS = 2 * 60

# Movement: terminal cells are about twice as tall as they are wide, so one horizontal step moves two columns to make walking feel even.
STEP_COLUMNS = 2

# Number of tasks in one full run and hidden fragments for the true ending.
TOTAL_TASKS = 5
TOTAL_FRAGMENTS = 3

# Animation tick in milliseconds. Ticks only animate decorations, don't change game state (turn-based).
TICK_MS = 100