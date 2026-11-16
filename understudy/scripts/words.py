"""The one word count the report layer uses (v0.8.0).

Word limits on the merged report — a short title, a fix, the verdict — are
checked by the gate, and a limit two scripts count two ways is a limit that
passes in one place and fails in the other. So there is one rule, here:

  a word is a whitespace-separated token that carries a letter or a digit,
  and is not a severity code (P0-P3) or an emoji.

Severity chips and lone punctuation ("—", "·", "→") are not words; a number
in a sentence ("4.4 s") is. Category chips, scores and UI labels on a slide
are template text, never overlay text, so they never reach this count.
"""
import re

_SEV = re.compile(r"^P[0-3]$")
_WORDISH = re.compile(r"[A-Za-z0-9À-ɏ]")


def count(text):
    """Words in `text` by the rule above. None and "" are 0."""
    if not text:
        return 0
    n = 0
    for tok in str(text).split():
        core = tok.strip(".,;:!?()[]{}\"'“”‘’*_`")
        if not core or _SEV.match(core) or not _WORDISH.search(core):
            continue
        n += 1
    return n
