"""Drawing helpers shared by several scenes: status bar, messages, pop-ups."""

import config
from engine.canvas import wrap

ROUTE_NAMES = {None: "-", "tech": "Tech", "human": "Human", "sneak": "Sneak"}


def draw_status_bar(canvas, state, place):
    """Row 0: place | clock | time left | route | tasks | fragments."""
    row = config.STATUS_ROW
    canvas.fill(row, 0, 1, canvas.width, " ", "status")
    warning = state.time_left() <= config.WARNING_TIME
    clock_style = "status_warn" if warning else "status"
    canvas.put(row, 1, place[:22], "status")
    col = 24
    canvas.put(row, col, f" {state.clock_text()} ", clock_style)
    canvas.put(row, col + 7, f"{state.minutes_left():>2} min left", clock_style
               if warning else "status_dim")
    canvas.put(row, 45, f"Route {ROUTE_NAMES[state.route]:<5}", "status_dim")
    canvas.put(row, 57, f"Tasks {state.tasks_done()}/{config.TOTAL_TASKS}",
               "status")
    canvas.put(row, 68, f"Frag {len(state.fragments)}/{config.TOTAL_FRAGMENTS}",
               "status_dim")


def draw_prompt_row(canvas, prompt=None):
    """Row 19: a thin separator, with an action prompt when there is one."""
    row = config.PROMPT_ROW
    canvas.put(row, 0, "─" * canvas.width, "separator")
    if prompt:
        canvas.put(row, 2, f" {prompt} ", "prompt")


def draw_messages(canvas, state):
    """Rows 20-22: the newest messages, older ones dimmed."""
    recent = state.recent_messages()
    for index, (text, style_name, number) in enumerate(recent):
        newest = number == state.message_count
        canvas.put(config.MESSAGE_TOP + index, 1, text,
                   style_name if newest else "dim")


def draw_key_bar(canvas, keys):
    """Row 23: key reminders, e.g. [("WASD", "move"), ("E", "use")]."""
    col = 1
    for key, action in keys:
        label = f" {key} "
        if col + len(label) + len(action) + 2 > canvas.width:
            break
        canvas.put(config.KEYS_ROW, col, label, "key")
        canvas.put(config.KEYS_ROW, col + len(label) + 1, action, "dim")
        col += len(label) + len(action) + 3


def draw_popup(canvas, title, lines, width=60, footer="E / Enter / Esc  close",
               style_name="panel"):
    """A framed box in the middle of the room view with wrapped text.

    lines is a list of (text, style name); long texts are wrapped.
    """
    inner = width - 4
    wrapped = []
    for text, line_style in lines:
        for part in wrap(text, inner):
            wrapped.append((part, line_style))
    max_lines = config.MAP_HEIGHT - 4
    wrapped = wrapped[:max_lines]
    height = len(wrapped) + 4
    top = config.MAP_TOP + (config.MAP_HEIGHT - height) // 2
    left = (canvas.width - width) // 2
    canvas.box(top, left, height, width, "panel_title", "double", title,
               "panel_title", fill_style=style_name)
    for index, (text, line_style) in enumerate(wrapped):
        canvas.put(top + 1 + index, left + 2, text, line_style)
    if footer:
        canvas.put(top + height - 2, left + width - len(footer) - 3, footer,
                   "status_dim" if style_name == "status" else "dim")
    return top, left, height
