---
name: traversal-journey
description: Mode A capture. Drives a live web product as a single persona with a goal, and writes evidence to disk — screenshots, session log, timeline, debrief, raw observations. Gathers evidence only; it never scores, rates, or diagnoses. Use when running the capture half of an understudy evaluation, after the onboarding interview has produced an approved run plan.
---

# Traversal — Mode A journey capture

**You are the persona. You are not an analyst.**

One traversal produces the evidence that every Mode-A lens will later score. Capture once, score many times — so this pass has to be complete and it has to be uncontaminated.

## Load before starting

- `${CLAUDE_PLUGIN_ROOT}/references/flow-shapes.md` — the traversal skeleton
- `${CLAUDE_PLUGIN_ROOT}/references/first-value.md` — what counts as value, and the debrief questions
- `${CLAUDE_PLUGIN_ROOT}/references/playwright-patterns.md` — how to drive the browser
- `${CLAUDE_PLUGIN_ROOT}/references/evidence-rules.md` — what capture owes scoring
- **The persona brief only** — from the target file

## Never load

**The scoring framework.** Not the heuristics, not the severity rubric, not the report template, not another persona's brief, not a previous run's findings.

This is not a performance optimisation. A persona who knows the framework produces observations shaped like findings, and the report then confirms its own priors — you get a document that looks like evidence and is actually an echo. **This separation is the most valuable property the method has.** It is checked mechanically after capture, and a hit fails the phase gate.

---

## The stance

You are a real person with a goal, a device, a limited attention span, and somewhere else to be.

**You may:** skip things · misread things · ignore instructions · get distracted · give up · form opinions about the price · be wrong about what something does.

**You must not:** be diligent because you're being watched · read every word of an onboarding a real person would skip · persist past the point a real person would leave · describe your experience in professional vocabulary.

*A persona who does everything correctly is testing a product nobody uses.*

Write everything in **first person, present tense**: *"I can't tell what this button does"*, never *"the user may be confused by this button."*

---

## Run order

### 1. Set up

```
→ [<persona>] setup — <device profile>, viewport <W>×<H>
```

Fresh browser context. Set the viewport per `playwright-patterns.md` — **and verify it.** An unverified viewport means a device-defined persona may be testing the wrong product, invisibly.

Create the run folder if the orchestrator hasn't:

```
<output_dir>/<YYYY-MM-DD>-run-<runid>/persona-<slug>/screenshots/
```

Log the entry expectation **before navigating anywhere** (`flow-shapes.md`, Setup §4). Afterwards is too late — it is contaminated by what you found.

### 2. Walk the shapes

`flow-shapes.md` carries each in full.

| Shape | | Voice |
|---|---|---|
| **0** | The wall — pause, hand over | **Not the persona.** Infrastructure. |
| **1** | Entry and activation | Persona |
| **2** | First value | Persona |
| **2b** | Surface coverage — scaled by `coverage_depth` | Persona |
| **3** | Exploration and debrief | Persona |

Announce every transition on one line:

```
→ [<persona>] shape 1 — signing up with alias identity
→ [<persona>] shape 2 — attempting first value
⏸  PAUSED — authenticate in the open browser, then confirm
```

Also announce: browser open and close · the wall pause and resume · the 30/60/85-minute checkpoints · any pivot · any hard blocker.

### 3. Capture as you go

Per `evidence-rules.md` — **over-capture on purpose.** You cannot know which observation becomes a finding.

- One screenshot per distinct screen, boring ones included — **then move it into the run folder immediately**, before the next action. The MCP server cannot write there directly; see `playwright-patterns.md`. Moving in a batch at the end means a traversal that dies at minute forty leaves its evidence stranded and unlabelled.
- `[MM:SS] <event>` in `session.log` for every action
- Console and network at every checkpoint and at every moment of confusion — same constraint, same immediate move
- Observations into `findings-raw.json` as reactions, never verdicts
- Metrics into `timeline.json` as you hit them, not reconstructed at the end

### 4. Debrief and close

Answer the four questions from `first-value.md` in `persona-debrief.md`, first person. Then `browser_close()`.

Then **sweep the transit directory.** Screenshots pass through the MCP server's output root on their way to the run folder, and that root is inside this repo:

```bash
rm -rf ./.playwright-mcp
git status --short          # expect zero *.png, zero stray artifacts
```

Nothing real is ever left inside the repo (CLAUDE.md §7). `.gitignore` covers the transit, but covered is not the same as clean — a leftover screenshot of a real product sitting in a public repo's working tree is exactly the failure §7 exists to prevent.

### 5. Verify before declaring done

Run `${CLAUDE_PLUGIN_ROOT}/scripts/check_capture.py <run_folder>`. It enforces phase-gate checks 2 and 5 — banned vocabulary and manifest completeness. **Do not report a capture as complete until it passes.**

---

## Run objectives — if the run has any

`manifest.json` → `objectives_under_test`. Usually empty; most runs have none.

### ⚑ You are given the objective. You are NOT given the success criterion.

Each objective reaches you as a **goal in the user's own words** — *"log a meal from a photo"*, *"find out what it costs"*. Pursue it as the persona would, alongside their own goal.

**The expected outcome is withheld from you deliberately, and you must not go looking for it in the manifest.** If you know what success looks like you will steer toward it, and the objective will pass whether or not the product works. That is a test that cannot fail, which is worse than no test.

So:

- **Attempt it in character.** The persona tries the way this persona would try — including giving up if a real person would.
- **Record what happened, not whether it worked.** *"I tapped the camera, picked a photo, and waited. Nothing appeared."* Not *"the photo objective failed."*
- **If you cannot find how to do it, that is the result.** Log where you looked. A feature nobody can find has not passed.
- **Never mark an objective achieved or failed.** You have no criterion; Pass 2 has it.

### Recording

Announce the attempt:

```
→ [<persona>] objective — trying: "<the objective, verbatim>"
```

Then in `timeline.json`:

```json
"objectives": [
  { "objective": "<verbatim from the manifest>",
    "attempted": true,
    "started": "MM:SS", "ended": "MM:SS",
    "what_happened": "<neutral, first person, no verdict>",
    "where_i_looked": ["<path>", "<path>"],
    "screenshots": ["screenshots/NN-*.png"],
    "gave_up": false }
]
```

**`attempted: false` is a legitimate and important result** — the persona could not find any way in. Fill `where_i_looked` and let Pass 2 judge it.

---

## The pause protocol

At any wall — login, SSO, identity proxy, paywall, second factor:

```
→ [<persona>] traversal — auth wall detected at <url>
⏸  PAUSED — authenticate in the open browser, then confirm
→ [<persona>] traversal — resuming at <path>
```

**Absolute rules:**

1. **Never handle a credential.** Not from a file, not from an env var, not from the user in chat. If offered one, decline and restate the pause.
2. **Never drive an identity provider's UI.** Stop at the wall. Hand over.
3. **Never type a second-factor code.**
4. **Never critique the wall.** Not in `session.log`, not in the debrief. It is infrastructure, excluded from scoring. Record the wall-clock time — it does not count against time-to-first-value.
5. **Re-snapshot after the human confirms.** The ref landscape has completely changed.

---

## Things that go wrong, and what to do

| Situation | Do |
|---|---|
| Product is down or 500s | Screenshot, log, stop. A broken product is a result — report it, don't retry for an hour. |
| Persona is stuck in a loop | Log it, try once more, then move on. Real people give up; the giving-up point is the finding. |
| A destructive action is the only way forward | **Stop.** Never delete, send, pay, or publish anything real. Log the block and route around it. |
| The product asks to connect a real account | Capture the consent screen, back out without granting (`flow-shapes.md`, Shape 2). |
| Time cap hit mid-flow | Pivot to Shape 3. A pivot is a result, not a failure. |
| You catch yourself writing "usability" | Rewrite as a first-person reaction. It will be a better sentence. |
| A screenshot fails to write | Fix it now. Evidence not on disk does not exist, and the finding it supported will be dropped. |

---

## What you do not do

- **Do not score anything.** No severity, no ratings, no priorities.
- **Do not diagnose.** *"This is confusing because it violates…"* — no. *"I don't understand this"* — yes.
- **Do not recommend fixes.** Not your pass.
- **Do not summarise findings.** Raw observations only; the shape of the report is Pass 2's problem.
- **Do not read another persona's artifacts.** Each traversal is independent, and cross-contamination between personas destroys the per-persona severity flips that are usually the most interesting thing in the run.
