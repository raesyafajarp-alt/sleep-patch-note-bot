#!/usr/bin/env python3
"""Sleep Patch Note Bot -- make.fun entry for "Fix Human Sleep: Funniest Patch Note".

The program drafts several one-line patch notes announcing that human
sleep is fixed, scores each against the judge brief published in the
competition rules, and writes the winner to /output/entry.txt.

Judge brief, most important first:
  1. Reads as a real patch note announcing a fix for human sleep.
  2. Is funny: the joke lands on a single read and earns a laugh.
  3. Sounds like genuine release notes: terse, confident, changelog voice.
  4. Stays a single line and under the 160-character cap, no padding.
  5. Surprises: the fix is specific and unexpected, not a flat claim.

Gate (sealed scorer): /output/entry.txt must be UTF-8 text of 1 to
160 characters, not only white space. This program enforces the same
gate before writing anything.
"""

import os
import sys

MAX_CHARS = 160

# Candidate patch notes, drafted from scratch for this entry.
CANDIDATES = [
    "Fixed a bug where sleep took 8 hours. It now takes 20 minutes; dreams are still in beta.",
    "Fixed: humans can now sleep in 20 minutes. Dreams are still in beta, and nightmares have been moved to the backlog.",
    "Fixed an issue where sleep took all night. It now takes 45 minutes. Waking up tired has been deprecated.",
    "Sleep no longer requires 8 hours, a bed, or closing your eyes. Side effects include being rested.",
    "Fixed a bug where humans spent a third of their lives asleep. Sleep now takes 15 minutes; the extra hours are yours.",
    "Humans can now fall asleep instantly. Fixed a bug where the body insisted on 8 hours, a dark room, and no thoughts.",
    "Patch: sleep duration reduced from 8 hours to 90 seconds. Naps are now classified as a full night's rest.",
    "Fixed an issue where the human body treated sleep as optional. It is now mandatory, instant, and 400% more restful.",
    "Sleep is fixed. Humans no longer need to lie still in the dark for eight hours pretending to be dead.",
    "Fixed a bug where sleep quality depended on mattress, moon phase, and childhood trauma. It now just works.",
    "Fixed a bug where sleep took 8 hours. It now takes 20 minutes; waking up tired has been deprecated.",
]

# Weights mirror the judge brief's order of importance.
WEIGHTS = {
    "patch_note": 0.30,   # 1. real patch note about fixing human sleep
    "funny": 0.25,        # 2. the joke lands on a single read
    "changelog": 0.15,    # 3. genuine release-notes voice
    "single_line": 0.10,  # 4. single line, under the cap, no padding
    "surprise": 0.20,     # 5. specific and unexpected, not a flat claim
}

JOKE_DEVICES = [
    "beta", "backlog", "deprecated", "pretending to be dead",
    "no thoughts", "the extra hours are yours",
    "full night's rest", "just works", "mandatory",
    "side effects include being rested", "400% more restful",
]

CHANGELOG_TERMS = [
    "fixed", "bug", "issue", "patch", "deprecated",
    "backlog", "beta", "reduced", "mandatory",
]

NEW_DURATIONS = [
    "20 minutes", "45 minutes", "15 minutes", "90 seconds",
    "instantly", "instant", "400%",
]


def score_patch_note(text):
    low = text.lower()
    if low.startswith(("fixed", "patch")) and "sleep" in low:
        return 1.0
    if "sleep" in low and "fix" in low:
        return 0.7
    return 0.3


def score_funny(text):
    low = text.lower()
    hits = sum(1 for d in JOKE_DEVICES if d in low)
    return min(1.0, hits / 2.0)


def score_changelog(text):
    low = text.lower()
    hits = sum(1 for t in CHANGELOG_TERMS if t in low)
    return min(1.0, hits / 3.0)


def score_single_line(text):
    if "\n" in text or "\r" in text:
        return 0.0
    if not (1 <= len(text) <= MAX_CHARS) or not text.strip():
        return 0.0
    return 1.0 if len(text) <= 130 else 0.8


def score_surprise(text):
    low = text.lower()
    if any(d in low for d in NEW_DURATIONS):
        return 1.0
    if "8 hours" in low or "eight hours" in low:
        return 0.5
    return 0.2


def score(text):
    parts = {
        "patch_note": score_patch_note(text),
        "funny": score_funny(text),
        "changelog": score_changelog(text),
        "single_line": score_single_line(text),
        "surprise": score_surprise(text),
    }
    total = sum(WEIGHTS[k] * v for k, v in parts.items())
    return total, parts


def gate_ok(text):
    """Same gate as the sealed scorer: UTF-8, 1-160 chars, not blank."""
    if not text or not text.strip():
        return False
    if len(text) > MAX_CHARS:
        return False
    if "\n" in text or "\r" in text:
        return False
    text.encode("utf-8")
    return True


def main():
    ranked = []
    for i, cand in enumerate(CANDIDATES):
        total, parts = score(cand)
        ranked.append((total, len(cand), i, cand, parts))
    # Highest score wins; ties break to the shorter line, then the
    # earlier draft -- deterministic, no randomness.
    ranked.sort(key=lambda r: (-r[0], r[1], r[2]))

    for total, n, i, cand, parts in ranked:
        print(f"[{total:.3f}] ({n} chars) #{i}: {cand}")
        print(f"         patch_note={parts['patch_note']:.2f} funny={parts['funny']:.2f} "
              f"changelog={parts['changelog']:.2f} single_line={parts['single_line']:.2f} "
              f"surprise={parts['surprise']:.2f}")

    winner = ranked[0][3]
    if not gate_ok(winner):
        print("GATE FAIL: winner does not pass the entry gate", file=sys.stderr)
        return 1

    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(winner)

    print(f"\nWINNER ({len(winner)} chars): {winner}")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
