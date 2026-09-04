# Lens output contract

**[M] methodology. Pass 2 only.** Binding on **every** lens, whatever its mode.

This file exists because the contract is identical for all of them, and eleven
copies of it would drift. A lens file says *"follow the output contract"* and
adds only what is specific to that lens.

---

## What you write

Follow `report-template.md` exactly. Two files in the run folder:

- `<lens>/exec-summary.md` — verdict sentence first, then the top 3. Gate check 6 enforces this.
- `<lens>/findings-final.md`

## House style — binding on every line

- **Conclusion first.** The finding title *is* the conclusion. The exec summary opens with the verdict.
- **Bullets, never prose paragraphs.** One idea per bullet, ≤ 25 words.
- **Cut anything that does not change a decision.**
- **Numbers over adjectives.**

Compress the *reasoning*, never the *proof*. Evidence citations, repro steps and
severity are not subject to the word budget. **A finding stripped of its evidence
is not concise, it is unsupported.**

---

## ⚑ The finding block is machine-parsed — format is not cosmetic

`check_report.py` reads each finding field by field and **fails closed**: a field
it cannot find is treated as absent, and an absent field silently changes the
finding's ID.

**Every field is its own bullet, on its own line.** Never join fields onto one
line with `·` separators, however much more compact that reads:

```markdown
### <finding-id> — <The conclusion, in one line, dev-ticketable>
- **Severity:** P1
- **So what:** <ONE line. What this costs. The reason to fix it.>
- **Framework tags:** <per the lens>
- **Flow:** <the flow or stage this belongs to>
- **Locator:** <the exact string you passed to finding_id.py --locator>
- **Personas hit:** <comma-separated, or "n/a" for lenses with no persona>
- **Observed:**
  - <bullet — neutral, concrete>
  - <max 3>
- **Evidence:** `persona-<slug>/screenshots/NN-*.png` · `session.log:NN`
  > "<verbatim quote, if there is one>"
- **Repro:**
  1. …
- **Fix:** <one line>
```

`·` is fine *inside* a field's value — several artifacts on one Evidence line is
the expected shape. It is only the field bullets that must never be merged.

---

## ⚑ Compute the ID, never compose it

The ID is a pure function of `lens`, `flow`, `locator` and `title`. The gate
recomputes it from your own report text and rejects any mismatch. A plausible-
looking hex string you wrote yourself will fail, and a whole report can fail on
nothing else.

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/finding_id.py \
    --lens <this lens> \
    --flow "<exactly the Flow value in your bullet>" \
    --locator "<the path or selector the finding lives at>" \
    --title "<exactly your finding title>"
```

Pass the **same** `flow` and `title` strings that appear in the report. The gate
derives its inputs from the file, so any drift between what you hashed and what
you wrote is a failure.

**The locator is the trap, and passing `--locator` to the script is only half
the fix.** The gate re-derives the locator from your *report*, not from your
shell command. If the finding block has no `**Locator:**` field, it infers one —
the first `` `/path` `` in the body, else the first Evidence artifact — and any
difference from what you hashed is a rejected ID.

**So write the `Locator:` field with exactly the string you passed.** That makes
the two agree by construction, and it is the only way to be sure.

> Observed 2026-09-04: a lens passed `--locator` correctly, omitted the field,
> and had two IDs rejected because the gate found a `/path` in the prose and
> preferred it.

**Write the finding block first, then hash what you wrote.**

---

## Hard rules

1. **Every finding cites evidence** — screenshot path, `session.log:NN`, console line, network entry, DOM excerpt, or a crawl/measurement record. No evidence → the **Dropped for want of evidence** list, not the report. This holds for findings that are obviously true.
2. **Every finding carries a stable ID.** Not a sequence number.
3. **Apply the scope exclusions** in `manifest.json`. Excluded items are never findings — but an excluded thing that blocked the persona still explains why they got stuck.
4. **Never report the auth wall.** Infrastructure.
5. **Split findings when severity flips across personas.** Never average.
6. **Stay in your lens.** Note out-of-scope observations in one line under **For other lenses** and move on.
7. **If `persona_mode` is `generic`, say so on the face of the report.** Findings rest on inferred personas.
8. **Never dedupe against another lens, and never read one.** Each lens report stands alone. Overlap is reconciled once, at the run level, by the orchestrator.
9. **If the run has `coverage_depth: deep`, mark findings from auditor-style exploration.** A finding from a screen no real user would reach is real, but it is not evidence about the ordinary experience. See CLAUDE.md Phase 4, R3.

---

## If the harness blocks you from writing files

Some hosts do not let a subagent write report files. **This is not a reason to
abandon the report or to shorten it.** Return the *complete* contents of both
files as text, clearly labelled with the path each belongs at, and the
orchestrator will persist them verbatim.

A truncated report is worse than an unwritten one, because it looks finished.

---

## What you return to the orchestrator

The verdict sentence, the count by severity, and anything you dropped for want of
evidence. Short — the report is the deliverable, not the summary of it.
