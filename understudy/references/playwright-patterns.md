# Playwright MCP — call patterns & gotchas

**[M] methodology.** Loaded during capture (Pass 1) so the traversal agent knows how to drive the browser. Contains no scoring vocabulary — safe to load alongside a persona brief.

---

## Tools

| Tool | Use for |
|---|---|
| `browser_navigate(url)` | Load a URL |
| `browser_navigate_back()` | Back button |
| `browser_snapshot()` | Accessibility-tree snapshot — the primary "look at the page" tool. Returns element refs (`e21`, `e35`…) |
| `browser_take_screenshot(filename?)` | Pixel screenshot. One per distinct screen. |
| `browser_click(ref)` | Click using a ref from a recent snapshot |
| `browser_type(ref, text)` | Type into a field |
| `browser_fill_form([{ref,value},…])` | Batch fill |
| `browser_select_option(ref, value)` | Select dropdown option |
| `browser_press_key(key)` | Keyboard |
| `browser_hover(ref)` | Hover |
| `browser_wait_for({text?, time?})` | Wait for text or elapsed time |
| `browser_resize(w, h)` | ⚠️ **See below — may be broken.** |
| `browser_tabs(action)` | Manage tabs |
| `browser_evaluate(js)` | Last-resort JS eval |
| `browser_console_messages()` | Read console |
| `browser_network_requests()` | Inspect network |
| `browser_handle_dialog(action)` | Accept/dismiss native dialog |
| `browser_close()` | Close browser between personas |

---

## Setting the viewport — try, then verify

**Try `browser_resize(width, height)` first.** In current versions it works and
simply calls `setViewportSize` internally (confirmed working 2026-09-04). Older
versions reject numeric arguments — **an upstream bug, not an understudy bug.**
Only if it errors, set the viewport directly:

```js
await page.setViewportSize({ width: W, height: H })
```

via the run-code tool, whose name varies by version — `browser_run_code` or
`browser_run_code_unsafe`. Check the tool list rather than assuming either.

**Then verify, whichever path set it:**

```js
browser_evaluate → ({ w: window.innerWidth, h: window.innerHeight })
```

**The verification is the load-bearing step, not the workaround.** Do not assume
the resize worked and do not skip the check because `browser_resize` returned
without an error. A persona defined by their device is testing a different
product if the viewport silently stayed at the default, and that failure is
invisible in the screenshots — they just look like a slightly different layout.
Log the verified numbers into `timeline.json` so a reader can confirm what was
actually measured.

---

## The core loop: look → decide → act

```
1. browser_snapshot()                     read the accessibility tree
2. (reason about what's on screen, as the persona)
3. browser_take_screenshot("NN-description.png")
4. browser_click(e21)   or   browser_type(e21, "...")
5. browser_wait_for({ text: "expected next-screen text" })
6. repeat
```

Every distinct screen gets **one** screenshot with a descriptive, zero-padded filename: `03-signup-form.png`, `07-consent-screen.png`, `12-dashboard-empty-state.png`. The number is the order seen; the description is what a human scanning the folder needs.

---

## Rules

**Refs expire.** Element refs from `browser_snapshot()` are valid only until the next snapshot or any DOM mutation. If a click navigates, re-snapshot before the next click.

**Screenshots must end up in the run folder — but you usually cannot write them there directly.**

The MCP server confines writes to its own output roots: normally the directory Claude Code was started in, plus `.playwright-mcp/` beneath it. An absolute path into `~/.understudy/runs/…` is refused outright:

```
Error: File access denied: /Users/…/.understudy/runs/… is outside allowed roots.
        Allowed roots: /path/to/cwd/.playwright-mcp, /path/to/cwd
```

So **capture, then move.** Every screenshot, one at a time:

```
browser_take_screenshot(filename: "07-consent-screen.png")
```

then immediately, before the next action:

```bash
mv -f ./07-consent-screen.png "<run_folder>/persona-<slug>/screenshots/" \
  || mv -f ./.playwright-mcp/07-consent-screen.png "<run_folder>/persona-<slug>/screenshots/"
```

The server may write to either location depending on version, hence the fallback. **Move immediately — not in a batch at the end.** A traversal that dies at minute forty leaves forty screenshots in the wrong place with no record of which screen each belonged to, and the evidence rule has no sympathy: a finding whose artifact is not on disk gets dropped.

**Why this is safe for a public repo:** the transit directory is inside the repo, so `.gitignore` covers `*.png` and `.playwright-mcp/` from day one (CLAUDE.md §7). It is transit, never storage — the run folder outside the repo is the authoritative copy, and the traversal removes `.playwright-mcp/` when it closes the browser.

**Console and network dumps have the same constraint.** `browser_console_messages(filename:)` and `browser_network_requests(filename:)` write to the same roots; move them into the run folder the same way.

**Console and network are evidence, not debug output.**
- `browser_console_messages()` — JS errors go into `session.log`.
- `browser_network_requests()` — failed API calls, especially during auth and first-value flows.

Capture both at every checkpoint and at any moment the persona is confused. A persona who says *"it just spun forever"* plus a 502 in the network log is a complete finding; either alone is half of one.

**Prefer text waits over time waits.** `browser_wait_for({text})` over `{time}`. Fixed waits hide flakiness — and flakiness the persona experienced as slowness is itself a finding.

**Fresh context per persona.** `browser_close()` between personas. Running headed, launch the MCP server `--isolated` or with a per-persona `userDataDir` under `~/.understudy/profiles/<slug>/`.

---

## Auth walls and second factors

- At an auth wall, **stop.** Do not click, type, or guess. Hand the open browser to the human (see the traversal skill's pause protocol).
- After the human authenticates, **re-snapshot** — the ref landscape has changed completely.
- OAuth consent screens may open a popup or redirect. Re-snapshot the product tab afterwards.
- A second-factor challenge is the same as an auth wall: pause, hand over, never type a code.

---

## Do not

- **Do not use CSS selectors.** Use refs from snapshots.
- **Do not click without snapshotting first.** Refs expire.
- **Do not screenshot mid-animation.** Wait for text, then shoot.
- **Do not trust a success toast alone.** Re-snapshot after any state change to confirm the page actually did what it claimed. A toast that lies is a finding — but only if you looked.
