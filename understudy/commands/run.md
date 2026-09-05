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
- **Describe the thing, then lead with the decision.** Two or three lines
  saying what the product actually is come first — a verdict about something
  the reader cannot picture is unusable. From the Top 5 onwards it is decisions
  only: what is wrong, what it costs, what to do. Never "this report analyses
  the onboarding funnel".
- **Write like a person.** No "it is worth noting", no "delve", no
  three-part flourishes, no sentence that survives having its adjectives
  deleted. Concrete nouns and real numbers. If a line could appear in any
  report about any product, cut it.

```markdown
# <Product> — <Website | Product> assessment — <D Month YYYY>

## What this is

<2–3 lines describing the thing assessed, neutrally, as a stranger would need
it explained: what the company sells, to whom, in which market, at what scale.
Numbers from the site — vendor counts, price ranges, countries. NO verdict and
NO finding here; a reader who has never seen the product must be able to
picture it before being told what is wrong with it.>

## How it was produced

<2–3 sentences, no jargon. A stand-in buyer with a goal drove the real site in
a real browser while everything was recorded; separate reviewers then scored
that recording without seeing each other's work. Say how long, on what device,
how many people were simulated, and that the personas were constructed if they
were.>

## Contents

<LEAVE EMPTY. render_report.py fills this with a numbered, hyperlinked index of
every section, built from what actually ran.>

## Top 5 — fix these first

<ONE sentence: the strongest honest reading of the whole run. This is the
verdict; it lives here, introducing the list, not at the top of the document.>

| # | Severity | What is happening | What it costs | Effort |
|---|---|---|---|---|
| 1 | P0 | <what a reader can see on the page> | <the cost, in the buyer's terms> | <Copy change / Server configuration / Design change / Build> |

<Exactly five rows, highest severity first, drawn from every check. If the run
produced fewer than five P0s — usually — fill from P1, and let the Severity
column say so. Never pad with P2 or P3 to reach five: four serious findings and
a filler reads worse than four.>

<One line under the table grouping the effort: which are copy, which are
configuration, which need building.>

## What a buyer could and could not establish

| Question the buyer had | Answer from the site |
|---|---|

<Their real questions, with times and page counts where they were observed.>

## What the site does well

<2–4 bullets. A report that cannot say anything positive is as untrustworthy as
one that cannot say anything negative.>

## Against comparable sites

<Only when competitors were run. The differences matrix, plus the market caveat
naming which markets the comparison sites serve.>

## What each check looked for

| Check | Question it answers |
|---|---|
| **Clarity** | Can a visitor say what this is, who it is for, and what to do next? |

<In LENS_ORDER, always: Clarity, Conversion, Trust, Compare, SEO, AEO,
Technical — then Usability, Defects, Activation, Content. Include only the
checks that ran. This table's order IS the document's order.>

## How each area scores

<LEAVE EMPTY. render_report.py fills this from each lens's own `Score:` line
and computes the overall. Never write the numbers by hand.>

## How to read these findings

| Severity | Meaning |
|---|---|
| 🔴 **P0** | Blocks the job, or breaks trust badly enough that people leave |
| 🟠 **P1** | They get through, but would not become a customer |
| 🟡 **P2** | Noticeable friction; erodes value over time |
| ⚪ **P3** | Polish. Worth fixing, changes nothing on its own |

<Then one line on what corroboration across checks means, and one on where the
full evidence lives.>

## Raised by more than one check

<LEAVE EMPTY. render_report.py fills this with the findings two or more checks
named independently. Omit the heading entirely if only one check ran.>

## Limits of this assessment

- <Persona mode, coverage depth, surfaces never opened, devices not tested,
  lab-vs-field on any speed number, anything excluded. Stated here rather than
  in a footnote, because acting on the report requires knowing them.>
```

#### ⚑ Sections this document must NOT contain

- **No verdict sentence at the top.** The document opens with a description of
  the thing assessed. A reader who has never seen the product cannot use a
  verdict about it. The verdict opens the Top 5 instead, where the evidence for
  it is directly underneath. *(Gate check 6 applies to lens summaries only.)*
- **No "Recommended first action".** The Top 5 is ranked, so its first row is
  already the recommended first action. Repeating it invites the two to drift.
- **No "technical facts worth separating out".** Anything technical belongs to
  the Technical check, where a reader looking for it will go. A summary that
  keeps its own technical annexe is two reports.
- **No section numbers written by hand.** `render_report.py` numbers every
  section in document order, so an inserted section cannot leave the index
  pointing at the wrong place.
- **No severity tally of your own.** The cover already carries the finding
  count and the P0/P1/P2/P3 split. A second copy in the body is how the two
  come to disagree.

Three headings are written empty and filled by the renderer — **Contents**,
**How each area scores**, and **Raised by more than one check**. Write the
heading, write nothing under it. Each is built from what actually ran, so none
of them can contradict the document it sits in.

A fourth, **Site-by-site comparison**, is appended by the renderer as the final
section and is not declared at all — see below.

#### ⚑ The site-by-site matrix closes the document

When `compare` ran, `render_report.py` lifts the `## Differences matrix` table
whole from `compare/exec-summary.md` and appends it as the last numbered
section, on its own landscape page.

**Do not re-type it into the run summary.** It is the only place in the report
where each competitor's own observed value sits beside ours, it is built from
four separate captures, and a hand-copied second version is how one number
comes to differ between two pages of one document.

`## Against comparable sites` earlier in the summary stays, and stays short: it
carries our column and the lead/trail/level count, for the reader who stops
before the findings. The matrix at the end is the evidence behind it — summary
and detail, the same split as the Top 5 against the per-lens sections.

> Requested 2026-09-05 by the first client to read one: the summary told him
> where the site trailed but never showed what the other three actually did, so
> the comparison could not be checked. The lens had built the table; only the
> export was dropping it.

#### ⚑ The order is fixed, and the table announces it

`LENS_ORDER` in `render_report.py` — **Clarity · Conversion · Trust · Compare ·
SEO · AEO · Technical**, then **Usability · Defects · Activation · Content** —
is the order the detailed sections appear in, the order the contents lists
them, and the order "What each check looked for" must use.

> Observed 2026-09-05: the summary's own table listed the checks in one order
> and the document presented them in another. A reader who uses the table as a
> map is then wrong on every jump, and the report looks assembled rather than
> written. **If you reorder the table, you have introduced a bug.**

**Check names are Title Case; `SEO` and `AEO` are always upper case.** They are
what the client reads, never the folder name.

| Folder | In the report |
|---|---|
| `clarity` | Clarity |
| `conversion` | Conversion |
| `trust` | Trust and credibility |
| `compare` | Competitive comparison |
| `seo` | Search visibility |
| `aeo` | Answer-engine readiness |
| `technical` | Performance and delivery |
| `ux` | Usability |
| `bugs` | Defects |
| `onboarding` | Activation |
| `content` | Content |

`render_report.py` uses this same mapping (`LENS_LABELS`), so a report that says
"aeo" in one table and "Answer-engine readiness" in the next looks like two
documents stapled together.

**⚑ Never name a run-folder path in prose the client reads.** A link's target
is a relative path and stays one; the link *text* is the display name. A
sentence like "see `trust/findings-final.md` in the run folder" is meaningless
to someone who was sent a PDF — say "in the full report".

#### Ranking across lenses is legitimate — merging is not

`severity-rubric.md` is shared and lens-agnostic: P0–P3 are defined by user impact, not by lens, and every lens loads it. **So you may rank findings from different lenses against each other.** Note in the limits that scoring models differed if they did — the manifest records which.

**Do not rewrite, merge or re-score a lens's finding.** Quote its title, cite its ID, link to its report.

#### ⚑ Cross-lens corroboration — the one thing only this layer can see

Lens reports deliberately do not dedupe against each other (`report-template.md`): each stands alone. So the same problem legitimately appears in several. **At the run level, say so:**

> **[P0] Memories asserts facts that are not the user's** — flagged independently by `ux`, `bugs` and `onboarding`

**Three independent lenses reaching the same finding is the strongest signal this architecture can produce** — the lenses never read each other, so agreement is real corroboration rather than an echo. Reported as three separate findings it reads as padding; reported as a corroboration count it reads as confidence.

Rules: a corroborated finding takes **one** slot in the top 3, not three. Count lenses, never average severities — cite the highest and say which lens assigned it.

**`render_report.py` also computes this mechanically** and prints a "Raised by
more than one check" table above the lens sections, plus an *Also raised by*
note on each affected row. That is a floor, not a substitute: it pairs findings
on a shared verbatim quotation or a similar title at the same locator, so it
catches the obvious agreements and misses ones phrased differently. **Your
top-3 corroboration counts are the authoritative ones** — write them from
reading the lens reports, not from the generated table.

It never merges, re-scores or drops anything (§11.8) — a false pair costs a
misleading note, not a lost finding.

### 3.7 — Close the manifest

```
${CLAUDE_PLUGIN_ROOT}/scripts/close_run.py <run_folder>
```

Records what was captured, what was scored and when the run finished — **every
field read off the disk, never from memory**, which is the same reason
`init_run.py` writes the manifest at the start rather than reconstructing it at
the end.

Until this runs, the manifest says the run never got past capture. `report
--since` compares runs by what the manifest claims they contain, so an unclosed
run is one that cannot be honestly diffed. `check_report.py` warns when it is
still open.

Use `--phase 2b-scoring` if scoring is not finished, and `--reopen` before
adding a lens to a run that was already closed.

### 3.8 — Offer an export, then hand over

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
