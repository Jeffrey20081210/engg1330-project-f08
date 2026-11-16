"""The text of the documents the player carries (inventory, press 'I' to open)."""

from puzzles.signals import clue_lines


def document_lines(item):
    """Lines of (text, style) for a document item, or [] for other items."""
    if item == "signal_log":
        return ([("Last emergency release, signal states:", "default")]
                + [(line, "info") for line in clue_lines("signal_log")])
    if item == "staff_logbook":
        return ([("Last page - exit release pattern:", "default")]
                + [(line, "info") for line in clue_lines("staff_logbook")])
    if item == "tunnel_map":
        return ([("Painted on the back: 'Exit release lamps'", "default")]
                + [(line, "info") for line in clue_lines("tunnel_map")])
    return []