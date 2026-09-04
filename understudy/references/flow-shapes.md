# Flow shapes — the traversal skeleton

**[M] methodology.** Loaded during capture, alongside the persona brief and `playwright-patterns.md`.

Flow **shapes** are portable. A specific product's steps are not — those come from the target file and from what the persona actually finds on screen. This file says *what kind of thing happens next*, never *click the blue button*.

> **Read as the persona, not as an analyst.** If a step feels unclear or wrong, record the reaction in first person. Do not diagnose it. Diagnosis is Pass 2's job and it has a framework you do not have.

---

## Setup — before anything

1. Set the viewport from the persona's device profile. **Verify it** (see `playwright-patterns.md`).
2. Fresh browser context per persona.
3. Screenshot `00-start.png` immediately after the first navigation.
4. **Load the persona's entry expectation** and log it at the top of `session.log`:

```
[pre-session] Arrived via: <channel — search, ad, word of mouth, direct>
[pre-session] What I was told: "<the promise that brought me here>"
[pre-session] What I expect this to be: <one line, persona's own words>
```

**Why this matters:** it is the anchor the persona judges the first screens against, captured *before* they see anything. Written afterwards it is contaminated by what they found. This is what makes the promise-vs-delivery question answerable later — without it, the `content` lens has nothing to compare against.

If the target file has no entry message, the persona arrives cold — record that, because arriving cold is itself a condition worth knowing about.

---

## Shape 0 — The wall (HUMAN, NOT PERSONA)

Applies when the target sits behind auth, an identity proxy, or a paywall. **The persona is not in scene yet.**

1. Navigate to the base URL. A wall appears.
2. **Stop driving.** Announce:
   ```
   → [<persona>] traversal — auth wall detected at <url>
   ⏸  PAUSED — authenticate in the open browser, then confirm
   ```
3. Wait for the human. **Do not click, type, or guess.** Never drive an identity provider's UI.
4. On confirmation, screenshot `00-wall-cleared.png` and re-snapshot.
5. `→ [<persona>] traversal — resuming at <path>`

**No persona voice in Shape 0.** No first-person reactions, no `session.log` entries as the persona. This is infrastructure.

**The wall is never a finding.** It is excluded at scoring time. But record the wall-clock time spent — it is not part of time-to-first-value, and the clock only starts when the persona takes over.

---

## Shape 1 — Entry and activation (PERSONA TAKES OVER)

**Goal:** get the persona to *"I'm in and ready to use this."*

From here on, you are the persona.

1. Reach the product's entry point — sign up, start a trial, or simply land, per the target.
2. Use the persona's alias identity where an account is needed: `<base>+<persona>-<YYYYMMDD>@<domain>`, so every run is a genuinely fresh signup.
3. Complete whatever onboarding the product imposes. Fill its forms, click its modals, connect what it asks for.
4. **Stop when you believe you're in and ready to use it** — not when the product says you're all set. Those are different moments and the gap between them is worth noticing.

**Instrumentation**
- Timestamp every action in `session.log` as `[MM:SS] <event>`.
- One screenshot per distinct screen.
- For each field, toggle or permission the product asks about, record in `findings-raw.json`: was its purpose clear — yes / no / partly.

**Persona stance**
- Hold the pricing expectation from the target file, even if no payment is collected. It changes what counts as acceptable friction.
- You may skip, ignore, misread and get distracted like a real person. A persona who does everything correctly is testing a product nobody uses.

---

## Shape 2 — First value

**Goal:** the moment the product does visible, useful work on the persona's own data. See `first-value.md` for what counts.

Attempt it whatever way the product offers. Then decide, **as the persona**, whether that was *"yes, it did something useful for me."*

**Stop condition:** either the persona sees it, or the persona concludes they cannot get there. Both are results. Giving up is data.

**Instrumentation**
- **Time-to-first-value**, in seconds, from the moment the persona took over (not from the wall) to the first visible useful output on their data.
- Count of distinct steps to get there.
- Count of permission prompts.
- Count of times the persona had to go hunting versus being led.

### Permission and consent screens — look, don't grant

When the product asks to connect an external account, **capture the consent screen and back out without granting**, unless the target explicitly enables full grants with isolated accounts.

Record: what scope was requested (read it off the URL parameters), whether it was the narrow or broad version, whether legal links were present, and what the persona felt about being asked at that point.

**Why back out:** granting real access from a test alias pollutes a real account, and shared aliases usually resolve to one real inbox. The consent screen is where most of the finding lives anyway.

---

## Shape 2b — Surface coverage (REQUIRED, scaled by coverage depth)

**Goal:** probe the product surfaces the persona would not otherwise open.

**Why this is required and not optional:** without it, the scoring pass makes judgements about surfaces the persona only saw as a nav label. That produces confident findings about screens nobody opened — the most embarrassing failure this method has, because it is invisible in the report.

### How many surfaces — set at interview, recorded in the manifest

`manifest.json` → `coverage_depth` (CLAUDE.md Phase 4, R1–R5):

| Depth | Shape 2b |
|---|---|
| `overview` | **Skipped.** The persona's natural path only. Highest realism; says nothing about screens nobody would find. |
| `standard` *(default)* | 2–3 surfaces relevant to this persona's goal. 8–12 min. |
| `deep` | **Every reachable surface** in the product's own navigation, after the natural path completes. |

**⚑ On a `deep` run, mark where the persona stops being a persona.** When natural curiosity is exhausted — the point a real newcomer would genuinely have stopped — log:

```
[MM:SS] --- auditor mode: natural interest exhausted ---
```

and keep going. Findings after that line are real, but they are **not evidence about an ordinary first session**, and Pass 2 must be able to tell them apart. Without the marker, deep coverage silently launders auditor findings as user findings (R3).

**⚑ Use the budget you were given (R5).** If the sweep finishes with time left on the cap, keep exploring — do not stop early and leave surfaces unopened. A run that ends with `cap_hit: false` *and* unopened surfaces is a traversal that gave up, and the report will say so. Record why you stopped, either way.

### Per surface, 2–3 minutes

Pick surfaces **relevant to this persona's goal** first, from the product's own navigation:

- Open it. Screenshot the state as found — empty, populated, or locked.
- Attempt the one action it most obviously invites. **Do not create, delete or send anything real.** Open the creation flow, look, back out.
- Ask, in first person: *is it obvious what this is for? Would I use it? Does it know things about me I didn't expect?*
- Log as `[MM:SS] surface: <name> — <observation>`.

Append to `findings-raw.json` tagged `"flow": "surfaces"`.

---

## Shape 3 — Exploration and debrief

**Goal:** understand what the product is actually for. Up to 10 minutes, then the debrief.

1. Click around freely. Read things. Try what catches your eye.
2. Answer the debrief questions from `first-value.md` in `persona-debrief.md`.
3. **Write in first person, as the persona.** Not *"the user might find…"* — *"I couldn't tell what this was for."*
4. Close the browser.

---

## Checkpoints — announce and pivot

Default caps: 90 minutes per persona, hard stop.

| Mark | Action |
|---|---|
| **30 min** | If still in Shape 1, log `checkpoint_30: still_in_entry` and continue. Already a signal. |
| **60 min** | If no first value yet, **pivot to Shape 3.** Do not force completion. |
| **85 min** | Announce "close to cap" and move to debrief regardless of progress. |

**A pivot is a result, not a failure.** A persona who never reached first value in 60 minutes has told you something more useful than one who was dragged there in 89.

---

## Banned vocabulary during capture

In `session.log`, `persona-debrief.md` and `findings-raw.json`, never write:

> heuristic · Nielsen · HAX · Amershi · severity · P0 · P1 · P2 · P3 · usability · UX (as an analyst term) · WCAG · accessibility audit · activation funnel · TTFV · friction (as jargon)

The persona may say *"this was hard to use"* or *"it took ages."* They may not say *"this is a P1 usability issue."*

**This is checked mechanically after capture.** Any hit fails the phase gate. If you catch yourself reaching for one of these words, rewrite it as a first-person reaction — which is almost always the better sentence anyway.

---

## Artifacts, per persona

Under `<run_folder>/persona-<slug>/`:

| File | Contains |
|---|---|
| `screenshots/NN-*.png` | One per distinct screen |
| `session.log` | Narrative, one timestamped line per action |
| `timeline.json` | Structured metrics — see below |
| `persona-debrief.md` | The debrief answers, first person |
| `findings-raw.json` | Observations, untagged and unscored |
| `trace.zip`, `video.webm` | If the MCP server produces them |

```json
{
  "shape_0": { "wall_present": true, "wall_wait_seconds": 0, "excluded_from_scoring": true },
  "shape_1": { "start": "00:00", "end": "MM:SS", "steps": 0, "screens": 0, "checkpoint_30": "ok" },
  "shape_2": { "start": "MM:SS", "end": "MM:SS", "first_value_reached": false,
               "seconds_to_first_value": null, "steps_to_first_value": 0,
               "permission_prompts": 0, "times_had_to_hunt": 0 },
  "shape_2b": { "surfaces_probed": [], "minutes": 0 },
  "shape_3": { "start": "MM:SS", "end": "MM:SS" }
}
```

`findings-raw.json` entries are observations, never verdicts:

```json
[
  { "t": "03:42", "screen": "04-consent.png", "flow": "shape_2",
    "reaction": "Why does it need my calendar? It hasn't shown me anything yet." }
]
```
