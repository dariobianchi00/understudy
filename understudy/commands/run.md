---
description: "Evaluate a live web product — interview, traverse, score through the chosen lenses"
argument-hint: "[target-slug or product URL]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Skill", "Task"]
---

# understudy run

Stand in for a user, drive a live web product, and report back through a chosen lens.

**Argument (optional):** "$ARGUMENTS" — a saved target slug, or a product URL to start from. If empty, the interview asks for everything.

---

## What this command does

Three stages, in order. Do not skip or reorder them.

1. **Pre-flight** — verify the browser dependency before promising anything.
2. **Onboarding interview** — establish the target, the objectives, the personas. One question at a time.
3. **Orchestrate** — group objectives by mode, capture once per mode, fan out every scoring for that mode.

**All modes are built.** Product assessment (Mode A) and website assessment (A-visit, B, C, D) run end to end — pre-flight, interview, capture, scoring, verification, export.

**Never approximate one mode with another.** A crawl is not a traversal, a traversal is not a measurement, and a single-site run is not a comparison. If something cannot run — no competitors supplied, a site that blocks automation — say so plainly and skip it.

---

## Stage 1 — Pre-flight

**Run this before the interview.** An interview that ends in "actually, the browser doesn't work" wastes the user's time.

### Check: Playwright MCP is connected

Call `mcp__*playwright*__browser_*` (any read-only tool), or run `claude mcp list`, and confirm a Playwright MCP server responds.

**If it is missing or does not respond, stop and print this verbatim:**

```
✗ Playwright MCP is not connected.

understudy drives a real browser through the Playwright MCP server. Without it,
traversal cannot run.

  claude mcp add playwright npx @playwright/mcp@latest

Then restart Claude Code and run /understudy:run again.
```

Do not offer to continue without it. Do not fall back to fetching pages over HTTP and calling it a traversal — that is a different product with the same report format, which is worse than failing.

### Check: the session model

**understudy cannot change the model it is running on.** Only the user can, with `/model`. So pre-flight reports it and recommends — it never switches, and it never pretends it could.

State the model you are currently running as, then:

- **Strongest available** → one line, move on. `✓ Session model: <name> — traversal will run on this.`
- **Not the strongest** → say so before the interview, because after the interview the user has committed hours:

```
⚠ Session model: <name>

Traversal runs on the session model — I can't change it, only you can.
It's the irreversible part of a run: the persona is deciding what to do
next, and a weak journey can't be rescued by good scoring.

Recommended: /model <stronger>, then re-run /understudy:run.
Continue on <name> anyway? (scoring models are chosen separately, later)
```

Accept "continue" without argument if they say so — it is their spend and their call. Record the answer; it goes in the manifest.

### Two version-dependent quirks — do NOT open the session with these

Both are upstream Playwright-MCP behaviour, not understudy bugs, and the
traversal handles both automatically. They are recorded here so that if one
surfaces you can name it in a line rather than debugging it live.

- **`browser_resize` may reject numeric arguments in older versions.** Current
  versions accept them (working as of 2026-09-04). The fallback is
  `page.setViewportSize({width, height})` via the run-code tool — whose name is
  `browser_run_code` or `browser_run_code_unsafe` depending on version. Either
  way the viewport is verified afterwards with `browser_evaluate`, and *that*
  check runs every time.
- **Screenshots cannot be written directly into the run folder.** The server
  confines writes to its own roots, so the traversal captures with a plain
  filename and moves each file into `persona-<slug>/screenshots/` immediately.
  See `references/playwright-patterns.md`.

**Say nothing about either at pre-flight.** Mention one only if it actually
fires. Opening a session with a wall of caveats about bugs that will not occur
is worse than the bugs.

---

## Stage 2 — Onboarding interview

Invoke the `onboarding` skill. It owns the full interview contract — saved-target lookup, the seven objectives, the persona fork, device profiles, time caps, the auth pause, output destination, and scope exclusions.

Do not re-implement the interview here. Do not shortcut it because the user supplied a URL in `$ARGUMENTS` — a URL answers one question of about nine.

---

## Stage 3 — Orchestrate

> **Group the requested objectives by mode → capture ONCE per mode → fan out every scoring for that mode.**

| Mode | Capture skill | Lenses that score it | Personas |
|---|---|---|---|
| **A — Journey** | `traversal-journey` — one traversal per persona | ux · bugs · onboarding · content | yes |
| **A-visit — Visit** | `traversal-visit` — one visit per persona | clarity · conversion · trust | yes |
| **B — Instrumented** | `traversal-measure` — scripted, mobile + desktop | technical | no |
| **C — Crawl** | `traversal-crawl` — no session, no login | seo · aeo | no |
| **D — Comparative** | `traversal-compare` — N sites, then a diff | compare | reuses A-visit / C |

**Mode D has its own command**, `/understudy:compare` — it needs the competitor set confirmed before anything runs. Route there rather than improvising it here.

**Group by mode, then capture once per mode.** `clarity + conversion + trust` is **one** visit traversal scored three ways. `clarity + seo` is **two** captures in different modes. Say the cost out loud before starting.

### 3.1 — Initialise the run

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/init_run.py --target ~/.understudy/targets/<slug>.yaml \
                    --traversal-model "<the session model you reported at pre-flight>"
```

Prints the run folder. Writes `manifest.json` **at run start** — not reconstructed at the end, because a manifest assembled afterwards records what someone remembers rather than what ran. It refuses to write output inside this repo.

### 3.2 — Capture, one persona at a time

Invoke the capture skill for the mode:

| Mode | Skill | Notes |
|---|---|---|
| A | `traversal-journey` | Auth pause; the human clears the wall |
| A-visit | `traversal-visit` | Logged out; never submits a form |
| B | `traversal-measure` | No persona; mobile and desktop separately |
| C | `traversal-crawl` | No persona; obeys `robots.txt` |

For persona modes, run one persona at a time — sequentially, never in parallel. They share a browser, and parallel personas would interleave into one unreadable session log.

**Do not pass the scoring framework to the traversal.** Not the heuristics, not the severity rubric, not a previous run's findings. The traversal skill loads only what it needs, and the separation is checked mechanically afterwards.

Between personas: `browser_close()`, fresh context.

### 3.3 — Verify the capture before claiming it worked

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/check_capture.py <run_folder>
```

Enforces phase-gate checks 2 and 5 — scoring vocabulary in the artifacts, and manifest completeness — plus whether a human could open the folder and follow what happened.

**If it fails on check 2, the traversal was contaminated. Re-run it. Do not edit the offending words out** — the words are a symptom, and removing them leaves a traversal whose evidence still confirms its own priors while now passing the check.

### 3.4 — Score: fan out every lens for that mode

**One capture, N scorings, in parallel.** The Mode-A lenses all read the same traversal — this is the whole point of the architecture, and running one agent per objective through the product would cost ~4× for identical evidence.

| Lens | Agent | Mode | Default model |
|---|---|---|---|
| `ux` | `lens-ux` | A | opus |
| `bugs` | `lens-bugs` | A | sonnet |
| `onboarding` | `lens-onboarding` | A | opus |
| `content` | `lens-content` | A | opus |
| `clarity` | `lens-clarity` | A-visit | opus |
| `conversion` | `lens-conversion` | A-visit | opus |
| `trust` | `lens-trust` | A-visit | opus |
| `technical` | `lens-technical` | B | sonnet |
| `seo` | `lens-seo` | C | sonnet |
| `aeo` | `lens-aeo` | C | sonnet |
| `compare` | `lens-compare` | D | opus |

**If the run has objectives**, also dispatch `objectives-scorer` — it reads the expected outcomes for the first time, after capture is fixed.

**Pass the model explicitly** from `manifest.json` → `models.scoring.<lens>`. Never rely on frontmatter inheritance (CLAUDE.md §6).

**Never pass one lens's output to another.** Lenses that read each other agree with each other, and that is not corroboration.

#### ⚑ You are responsible for the files landing on disk

**Some hosts do not let a subagent write files**, and a lens that hits this
returns its report as text instead. Whether it wrote the files or handed them
back is not something to assume from a cheerful summary — check.

After every lens returns:

```bash
ls <run_folder>/<lens>/exec-summary.md <run_folder>/<lens>/findings-final.md
```

If either is missing, **write it yourself from the text the lens returned,
verbatim.** Do not summarise it, do not re-score it, do not drop the sections
you find repetitive — the gate in 3.5 checks the file, and a report you
paraphrased is no longer the lens's finding.

Two rules when you persist a lens's output:

- **Split at the lens's own boundary.** `exec-summary.md` is the verdict
  sentence, the top 3 and the stated limits; `findings-final.md` is `## Findings`
  onward. Do not invent a verdict the lens did not write. If a lens returned no
  verdict sentence and no top 3, say so plainly in your handover rather than
  authoring one and presenting it as the lens's.
- **Never edit a finding to make the gate pass.** If 3.5 rejects an ID, the fix
  is to recompute it with `finding_id.py` from the finding's own `flow`,
  `locator` and `title` — that is a formatting repair. Changing a severity, a
  title or an evidence citation to clear a check is falsifying the report.

A run where two lenses silently returned text and only one wrote files produces
a gate that passes while checking a third of the work. That failure is invisible
in the output — the check prints `PASSED` either way. **Confirm the lens count
in the gate output matches the lens count you dispatched.**

### 3.5 — Verify the report

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/check_report.py <run_folder>
```

Gate checks 1, 3, 4 and 6 — evidence rule, no unsupported P0s, stable IDs reproducible, verdict first. **Do not present a report that fails the check.**

**Read the per-lens lines above the verdict, not just the verdict.** The gate
discovers lenses by looking for `<run_folder>/<lens>/findings-final.md`, so a
lens whose files never landed is not failed — it is *not checked*, and the run
still prints `PASSED`. The output names each lens it scanned and its finding
count:

```
  · bugs: 9 finding(s), 1 P0
  · onboarding: 8 finding(s), 0 P0
  · ux: 22 finding(s), 1 P0
```

If that list is shorter than the lenses you dispatched in 3.4, the gate is
green on incomplete work. Go back and persist the missing ones.

### 3.6 — Write the run-level exec summary

**Always written, every run, whatever was asked for.** It sits above the lens reports at `<run_folder>/exec-summary.md`.

**House style is binding here too** — pyramid, bullets, no prose paragraphs. See `references/report-template.md`. **Length: roughly one page per lens run**, soft. A three-lens run gets about three pages; a one-lens run gets one. Past that, every line must earn its place.

#### ⚑ Written for someone who has never heard of understudy

The run summary is the only part an executive reads. Assume they did not
commission the run, do not know what a "lens" is, and will not open anything
else. Three consequences:

- **Explain the vocabulary before using it.** `ux`, `bugs`, `onboarding`,
  `P0`, `persona` are all jargon. The summary carries a short "what was tested"
  block that says what each lens actually looked for, in plain English.
- **Lead with the decision, not the description.** Not "this report analyses
  the onboarding funnel" — say what is wrong, what it costs, and what to do.
- **Write like a person.** No "it is worth noting", no "delve", no
  three-part flourishes, no sentence that survives having its adjectives
  deleted. Concrete nouns and real numbers. If a line could appear in any
  report about any product, cut it.

```markdown
# <Product> — understudy run <YYYY-MM-DD> (<run-id>)

<ONE SENTENCE across the whole run. What is true about this product, and what
it costs. The line someone repeats in a meeting.>

## The three things that matter
1. **<Plain-English title>** — <one line: the cost, in the user's terms>
   <severity> · found by <n> of <m> independent checks · `<lens> <id>`
2. …
3. …

## What we did
<2–3 sentences, no jargon. A stand-in user with a goal drove the real product
in a real browser while everything was recorded; separate reviewers then scored
that recording. Say how long, on what device, and how many people were simulated.>

## What each check looked for
| Check | Question it answers |
|---|---|
| **ux** | Can someone use this without being taught? Is anything confusing, misleading, or harder than it needs to be? |
| **bugs** | Is anything actually broken — errors, failed requests, dead ends, contradictory data? |
| **onboarding** | How long from arriving to getting something useful, and where do people give up? |
| **content** | Does the product deliver what its words promise, in language people understand? |

*(Include only the lenses that ran. Rewrite the questions if a lens's own
verdict phrases it better — these are defaults, not fixed copy.)*

## Severity, in plain terms
- **P0** — blocks the job, or breaks trust badly enough that people leave.
- **P1** — they get through, but would churn before paying.
- **P2** — noticeable annoyance; erodes value over time.
- **P3** — polish. Worth fixing, changes nothing.

## The numbers
- <5–7 bullets. Real figures only: time to first value, steps, counts.
  No adjective that isn't carrying a number.>

## Where to go deeper
| Report | Findings | What it says |
|---|---|---|
| [`ux`](ux/exec-summary.md) | 14 — 1 P0, 8 P1, 4 P2, 1 P3 | <the lens's own verdict, one line> |

## What we could not see
- <Persona mode, coverage depth, surfaces never opened, devices not tested,
  anything excluded. An executive who acts on this needs to know its edges.>

## What the product got right
- <2–4 bullets. A report that cannot say anything positive is as untrustworthy
  as one that cannot say anything negative.>

## Do this next
<One line. One action, not a list.>
```

#### Ranking across lenses is legitimate — merging is not

`severity-rubric.md` is shared and lens-agnostic: P0–P3 are defined by user impact, not by lens, and every lens loads it. **So you may rank findings from different lenses against each other.** Note in the limits that scoring models differed if they did — the manifest records which.

**Do not rewrite, merge or re-score a lens's finding.** Quote its title, cite its ID, link to its report.

#### ⚑ Cross-lens corroboration — the one thing only this layer can see

Lens reports deliberately do not dedupe against each other (`report-template.md`): each stands alone. So the same problem legitimately appears in several. **At the run level, say so:**

> **[P0] Memories asserts facts that are not the user's** — flagged independently by `ux`, `bugs` and `onboarding`

**Three independent lenses reaching the same finding is the strongest signal this architecture can produce** — the lenses never read each other, so agreement is real corroboration rather than an echo. Reported as three separate findings it reads as padding; reported as a corroboration count it reads as confidence.

Rules: a corroborated finding takes **one** slot in the top 3, not three. Count lenses, never average severities — cite the highest and say which lens assigned it.

### 3.7 — Offer an export, then hand over

Print the run folder path. Then **ask, every run** — two short questions, not a form:

```
Report is in ~/.understudy/runs/<slug>/<run>/ as markdown.

Export a copy?  PDF · HTML · skip
```

If they pick a format, ask what goes in it. Three tiers, and say what each is:

- **`summary`** — the run verdict, then a triage table of **every** finding across all lenses with its severity and its one-line cost. A few pages. This is the report; it is what gets forwarded.
- **`<lens>`** — one lens in full, with evidence. What an engineer or designer acts from.
- **`all`** — everything, screenshots embedded. The archive, not a document anyone reads front to back.

**Never export `summary` alone as though it were the whole deliverable.** A verdict with no route to the findings behind it is a dead end — which is why the summary scope carries the triage tables and names the file holding the detail.

Then run:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/render_report.py <run_folder> \
    --format html|pdf --scope summary|<lens>|all
```

**Markdown in the run folder stays canonical.** The export is a copy for reading or forwarding — never the only place a finding lives, and never edited by hand afterwards.

Finally, mention that `/understudy:report <run-folder> --lens <name>` adds a lens later without re-driving the product — the evidence is the durable artifact.

## Invariants — these hold at every stage

1. **The agent never handles a credential.** Not from a file, not from an env var, not from the user in chat. At an auth wall, pause and hand the open browser to the human. See §5 of the repo spec.
2. **The auth wall is never a finding.** It is infrastructure — excluded from all scoring and from the exec summary.
3. **The traversal agent never sees the scoring framework.** Banned during capture: *heuristic · severity · usability · Nielsen · HAX · P0/P1/P2/P3*. Contaminating the traversal produces a report that confirms its own priors.
4. **Every finding cites evidence.** No screenshot, log line or DOM excerpt → the finding is dropped. No exceptions, including for findings that are obviously true.
5. **Nothing real is ever written into this repo.** Targets, runs, profiles and credentials live under `~/.understudy/`. See §7 of the repo spec.
