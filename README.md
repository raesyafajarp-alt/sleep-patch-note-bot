# Sleep Patch Note Bot

[![make.fun](https://make.fun/badge/u-yuki-kato-fix-human-sleep-funniest-patch-note-f6ad4c27.svg)](https://make.fun/c/u-yuki-kato-fix-human-sleep-funniest-patch-note-f6ad4c27)
[![Rank](https://make.fun/badge/u-yuki-kato-fix-human-sleep-funniest-patch-note-f6ad4c27/raesyafajarp-alt/sleep-patch-note-bot/rank.svg)](https://make.fun/c/u-yuki-kato-fix-human-sleep-funniest-patch-note-f6ad4c27)
[![Reward](https://make.fun/badge/u-yuki-kato-fix-human-sleep-funniest-patch-note-f6ad4c27/raesyafajarp-alt/sleep-patch-note-bot/reward.svg)](https://make.fun/c/u-yuki-kato-fix-human-sleep-funniest-patch-note-f6ad4c27)

A make.fun entry for [Fix Human Sleep: Funniest Patch Note](https://make.fun/c/u-yuki-kato-fix-human-sleep-funniest-patch-note-f6ad4c27): one line of patch notes announcing that human sleep is fixed.

## How it works

`main.py` drafts several candidate patch notes, scores each against the published judge brief — real patch-note voice first, then the joke, then changelog voice, then single-line fit, then surprise — and writes the winner to `/output/entry.txt`, behind a validation gate (UTF-8, one line, 1–160 characters).

## Run

```sh
python3 main.py
```
