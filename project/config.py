"""Tunable numbers for the whole game, kept in one place for balancing."""

# Screen layout: the game never draws outside this 80 x 24 area.
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 24
STATUS_ROW = 0          # top status bar
MAP_TOP = 1             # first screen row of the room view
MAP_HEIGHT = 18         # room maps are exactly 18 rows x 80 columns
PROMPT_ROW = 19         # separator line, shows "[E] ..." prompts
MESSAGE_TOP = 20        # three lines of messages (rows 20-22)
MESSAGE_LINES = 3
KEYS_ROW = 23           # key reminder line

# Clock, in seconds after midnight.
START_TIME = 42 * 60    # 00:42 - the player wakes up
SEAL_TIME = 90 * 60     # 01:30 - the station seals
WARNING_TIME = 10 * 60  # status bar turns red when this much time is left

# Time costs, in seconds. One key press is one turn; only these actions
# move the clock forward.
STEP_SECONDS = 4        # one step on the map
WRONG_ANSWER_SECONDS = 3 * 60
HINT_SECONDS = 2 * 60

# Movement: terminal cells are about twice as tall as they are wide, so one
# horizontal step moves two columns to make walking feel even.
STEP_COLUMNS = 2

# Number of tasks in one full run and hidden fragments for the true ending.
TOTAL_TASKS = 5
TOTAL_FRAGMENTS = 3

# Animation tick in milliseconds. Ticks only animate decorations; they never
# change the game state (the game is turn-based).
TICK_MS = 100
