---
name: traversal-visit
description: Mode A-visit capture. Drives a live marketing or content website as a single persona with a question, and writes evidence to disk — screenshots, session log, timeline, debrief, raw observations. Gathers evidence only; it never scores, rates, or diagnoses. Use when running the capture half of a website assessment, after the onboarding interview has produced an approved run plan.
---

# Traversal — Mode A-visit capture

**You are the persona. You are not an analyst.**

One traversal produces the evidence every website lens will later score. Capture once, score many times — so this pass has to be complete and it has to be uncontaminated.

## Load before starting

- `${CLAUDE_PLUGIN_ROOT}/references/visit-shapes.md` — the traversal skeleton
- `${CLAUDE_PLUGIN_ROOT}/references/playwright-patterns.md` — how to drive the browser
- `${CLAUDE_PLUGIN_ROOT}/references/evidence-rules.md` — what capture owes scoring
- **The persona brief only** — from the target file

**Do not load `flow-shapes.md`.** That is the product skeleton. A visitor pushed through product shapes produces findings about a signup they were never going to reach.

## Never load

**The scoring framework.** Not the heuristics, not the severity rubric, not the report template, not another persona's brief, not a previous run's findings.

A persona who knows the framework produces observations shaped like findings, and the report then confirms its own priors — a document that looks like evidence and is an echo. **Checked mechanically after capture; a hit fails the phase gate.**

---

## How a visitor differs from a product user

This is the whole reason the skill exists. Hold it the entire session:

- **They owe the site nothing.** No account, no investment, no sunk cost. They leave the instant it stops being worth the effort, and leaving is the finding.
- **They are answering one question**, not completing a task. Usually *"is this for me?"*
- **They decide in the first thirty seconds** and spend the rest confirming or revising it.
- **They skim.** Headings, first lines, bold text, prices. Nobody reads a marketing page.
- **They are suspicious by default** — of claims, of prices that aren't shown, of testimonials without names.

**A persona who dutifully reads every word and explores every page is not a visitor. They are an auditor**, and their findings describe a site nobody experiences.

---

## Run order

### 1. Set up

```
→ [<persona>] visit setup — <device profile>, viewport <W>×<H>, logged out
```

Fresh context, **logged out**, prior state cleared. Set the viewport and **verify it**.

Log the entry expectation **before navigating anywhere** (`visit-shapes.md`, Setup §4). Written afterwards it is contaminated by what was found, and the promise-match question becomes unanswerable.

### 2. Walk the shapes

| Shape | | Voice |
|---|---|---|
| **V1** | Land — the first 30 seconds | Persona |
| **V2** | Orient — build a model of the offer | Persona |
| **V3** | Evaluate — is this for me, can I trust it | Persona |
| **V4** | Decide and debrief | Persona |

Announce every transition on one line:

```
→ [<persona>] V1 — landing, before scroll
→ [<persona>] V3 — looking for pricing
```

Also announce: browser open and close · the 10-minute checkpoint · any pivot · an early exit · the auditor-mode line on a deep run.

**⚑ V1 is the shape most easily ruined.** Screenshot the fold and write the four first-impression answers **before scrolling**. Once you have scrolled you cannot report a first impression honestly, and no later observation replaces it.

### 3. Capture as you go

Per `evidence-rules.md` — **over-capture on purpose.**

- The fold first, then one screenshot per distinct section or page — **then move each into the run folder immediately** (`playwright-patterns.md`). The server cannot write there directly.
- `[MM:SS] <event>` in `session.log` for every action and every reaction.
- Console and network at the landing page and at any moment of confusion — a slow page the persona experienced as "broken" is a complete finding only with both halves.
- Observations into `findings-raw.json` as reactions, never verdicts.
- `timeline.json` as you hit each metric, not reconstructed at the end.
- **`questions_unanswered` as they arise.** This is the field the whole traversal exists to fill.

### 4. Debrief and close

Answer Q1–Q6 from `visit-shapes.md` in `persona-debrief.md`, first person. Then `browser_close()` and sweep the transit directory (`rm -rf ./.playwright-mcp`, confirm `git status` clean).

### 5. Verify before declaring done

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/check_capture.py <run_folder>
```

Enforces phase-gate checks 2 and 5. **Do not report a capture as complete until it passes.**

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

## Things that go wrong, and what to do

| Situation | Do |
|---|---|
| The persona would genuinely leave after 90 seconds | **Let them.** Record the time and the reason, go to the debrief. An early exit is the strongest finding a visit produces; padding the session destroys it. |
| A form is the only way to see more | Screenshot it, count the fields, back out. Never submit — a real lead in a real CRM, and on a competitor's site never at all. |
| A cookie banner blocks the page | Screenshot it **first** — it is part of the landing experience and often a finding — then dismiss it the way a visitor would and continue. |
| The site has a login | Not this mode. A visitor does not have an account. Record that the wall exists and stay outside it. |
| A chat widget opens on its own | Screenshot, record the reaction, close it. Do not converse — there may be a human on the other end. |
| The site is down or 500s | Screenshot, log, stop. A broken site is a result. |
| Time cap hit mid-shape | Pivot to V4. A pivot is a result, not a failure. |
| You catch yourself writing "conversion funnel" | Rewrite as a first-person reaction. It will be a better sentence. |

---

## What you do not do

- **Do not score anything.** No severity, no ratings, no priorities.
- **Do not diagnose.** *"I can't find the price"* — yes. *"Pricing is buried, violating…"* — no.
- **Do not recommend fixes.** Not your pass.
- **Do not submit forms, request demos, or start trials.**
- **Do not read another persona's artifacts.** Cross-contamination destroys the per-persona severity flips, which are usually the most interesting thing in the run.
- **Do not compare to another site**, even in a Mode D run. Each site is captured independently; the diff is a separate pass. A persona who has just seen a competitor is no longer describing this site.
