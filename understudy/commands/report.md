---
description: "Score existing captured evidence — re-run lenses without re-driving the product"
argument-hint: "[run-folder] [--lens <name>] [--since <run-id>]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Task"]
---

# understudy report

Score evidence that has already been captured. **No browser opens.**

**Arguments:** "$ARGUMENTS"

---

## Why this command exists

Capture is the expensive, irreversible part; scoring is cheap and repeatable. Separating them means:

- **Adding a lens later costs nothing.** Ran `ux` on Tuesday, want `content` too? It reads the same folder.
- **Improving a lens is testable.** Re-score the same evidence and compare — the only variable that changed is the lens.
- **A failed scoring pass is not a lost run.** The evidence survives.

This is the payoff of the two-pass design, and the reason capture over-captures.

---

## Usage

```
/understudy:report <run-folder>                    all lenses in the target
/understudy:report <run-folder> --lens content     add one lens
/understudy:report <run-folder> --since <run-id>   diff against an earlier run
```

With no run folder, use the most recent under `~/.understudy/runs/`, and say which you picked.

---

## Method

### 1. Verify the capture first

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/check_capture.py <run_folder>
```

**If capture never passed its gate, do not score it.** Scoring contaminated or incomplete evidence produces a report that looks exactly like a good one. Report the failure and stop.

### 2. Read the manifest

`manifest.json` gives the objectives, the personas, `persona_mode`, the scope exclusions, and the models. **Apply the exclusions.** **Carry `persona_mode` into every report** — if it is `generic`, findings rest on inferred personas and the report must say so on its face.

### 3. Fan out the lenses — in parallel

One agent per lens, launched together. They read the same evidence and do not interact.

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

**Pass the model explicitly** from `manifest.json` → `models.scoring.<lens>`. Do not rely on frontmatter inheritance — see CLAUDE.md §6. If the manifest and the frontmatter disagree, the manifest wins; it records what the user chose.

Give each agent the run folder path and nothing else it does not need. **Never pass one lens's output to another** — six agents agreeing because they read each other is not corroboration.

### 4. Verify the output

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/check_report.py <run_folder>
```

Gate checks 1, 3, 4, 6 and 7. **Do not present a report that fails.** Fix the lens output and re-run the check.

### 5. Aggregate

Write a run-level `exec-summary.md` at the run root — **rewriting the existing one**, since it now covers a lens it did not before.

**⚑ Use the template in `/understudy:run` §3.6 verbatim.** It is the one place the run
document's shape is defined, and rewriting the summary is the moment that shape is most
easily lost. In particular:

- Open with **What this is** — a description of the thing assessed — then **How it was
  produced**. No verdict sentence at the top; the verdict opens the Top 5.
- **Top 5**, always five, ranked by severity across every check, filled from P1 when the
  run carries fewer than five P0s.
- Write **Contents**, **How each area scores** and **Raised by more than one check** as
  empty headings. `render_report.py` fills all three from what actually ran.
- Sections in `LENS_ORDER` and named in Title Case — never by folder name.
- No section numbers by hand, no severity tally of your own, no "Recommended first action".

If the newly-scored lens published a `- **Score:** N/10 — why` line, it joins the score
table automatically and the overall is recomputed. **The overall score is never authored.**

House style applies — pyramid, bullets, no prose paragraphs. Roughly one page per lens in the run.

### 6. Offer an export

Same as a full run. Print the run folder path, then ask:

```
Report is in <run-folder> as markdown.

Export a copy?  PDF · HTML · skip
```

Then what goes in it — **exec summary only · one named lens · everything** — and render:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/render_report.py <run_folder> \
    --format html|pdf --scope summary|<lens>|all
```

Markdown stays canonical; the export is a copy. **Re-export after adding a lens** if one already exists, or the shared file silently omits the lens you just paid for.

---

## `--since <run-id>` — diff two runs

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/compare_runs.py <old_run> <new_run> [--lens <name>] [--json]
```

Matches findings across two runs by **stable ID** and classifies each as **new · persisting · resolved**, with an overlap percentage.

**Why by ID and not by title:** findings get reworded between runs. Matching on text silently drops anything a model phrased differently, inflating both "new" and "resolved" until the diff looks busier than reality. The ID normalises away rewording, staging hosts and changed timings for exactly this reason — and it is why IDs could not be retrofitted.

### ⚑ Read the comparability warnings before the numbers

The script prints them **above** the diff and carries them in `--json` as `warnings`, so they cannot be dropped by accident. It flags:

- **A changed traversal or scoring model.** Findings are not comparable across models — a "resolved" finding may be a weaker model that failed to notice it.
- **A changed persona mode.** `generic` against `supplied` compares two different questions.
- **A changed coverage depth.** A deeper run finds more because it looked at more, not because the product got worse.
- **A changed lens set.** A lens that did not run cannot resolve anything.
- **Different targets**, which is not a diff at all.

**Never present a diff with warnings as though it were clean.** Repeat them in whatever you hand the user, in the same position — before the counts.

### What "resolved" does and does not mean

It means **absent from the new run**. That is not the same as fixed:

- The lens may not have run.
- A different model may not have noticed it.
- Coverage may not have reached the screen.
- The finding may have been reworded past the normaliser.

Say "absent", let the user conclude "fixed", and give them the warnings they need to decide.

### The self-overlap baseline

Running the **same target twice, unchanged**, and diffing gives this harness's own noise floor — how much understudy disagrees with itself. That number belongs in the README. A tool that publishes how much it disagrees with itself is more trustworthy than one that does not mention it.

`compare_runs.py --self-test` covers the classification and the overlap arithmetic on synthetic data, so it stays runnable without run folders.

