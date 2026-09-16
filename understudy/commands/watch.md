---
description: "Watch the current understudy run live — in its own window, or as a status line"
argument-hint: "[--statusline]"
allowed-tools: ["Bash"]
---

# understudy watch

Show the person what a run is doing while it runs. Nothing here needs a path:
the newest run is remembered by the run command itself.

**Arguments:** "$ARGUMENTS"

## What to do

1. **Open the live view in its own window** — run this, and say what it does in
   one line: who is running, where the persona is against its time cap, every
   screenshot as it lands, and the persona's own commentary as it is written.

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/watch.py --open
   ```

   If it prints a command instead of opening a window, show that command and
   say to paste it into any terminal.

2. **Offer the status line, once**, unless the argument is `--statusline`, in
   which case skip the question. Ask exactly this:

   > Want a one-line summary of the run at the bottom of Claude Code too? It
   > shows the persona, the time, and their latest comment. One-time setup,
   > takes effect next time Claude Code starts. Yes / no

   On yes:

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/watch.py --setup-statusline
   ```

   It adds one entry to `~/.claude/settings.json` and keeps everything else in
   the file as it was (a copy is left beside it). Say that it appears after
   restarting Claude Code. On no, say nothing more.

## Never

- Never ask for a path. If there is no run yet, say so and point at
  `/understudy:run`.
- Never paste settings JSON for the person to edit by hand. The script does it.
