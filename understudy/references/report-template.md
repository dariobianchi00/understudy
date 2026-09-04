# Report template

**[M] methodology.** **Pass 2 only.** Produces two files per lens in the run folder: `exec-summary.md` and `findings-final.md`.

---

## ⚑ House style — pyramid, bullets, no prose

This applies to **every line of every file a lens writes**, not just the summary.

1. **Conclusion first, everywhere.** The finding title *is* the conclusion. The exec summary opens with the verdict. A reader who stops after one line must still have the answer.
2. **Bullets, not paragraphs.** No prose blocks anywhere in a report. If a thought needs three sentences, it is three bullets — or it is two thoughts.
3. **One idea per bullet, ≤ 25 words.** Longer means it is really two bullets.
4. **Cut anything that does not change a decision.** Background, throat-clearing, "it is worth noting that", restating the framework. The reader knows why they ran this.
5. **Numbers over adjectives.** "2:41 to first value" beats "reasonably quick".

**Why this is a rule and not a preference:** a lens can produce twenty findings, and a run can carry seven lenses. Prose does not survive that volume — it is skimmed, then skipped, then the report goes unread and the run was wasted. Pyramid structure is what lets a reader stop at any depth and still be correctly informed.

**What concision must never cost:** evidence citations, repro steps, or the severity. Compress the *reasoning*, never the *proof*. A finding stripped of its evidence is not concise, it is unsupported — see `evidence-rules.md`.

---

## Why the exec summary leads with a verdict

The one-sentence verdict and the top-3 are the only things standing between the user and a great deal of unread output. **Phase-2 gate check 6 enforces this mechanically** — a report whose first non-heading block is not a single sentence fails the gate.

Write the verdict first, before the findings. If you cannot state the verdict in one sentence, you have not finished analysing.

---

## `exec-summary.md` (per lens)

**Length: about one page.** Soft target, not a gate — but every line past it should have earned its place.

```markdown
# <Product> — <lens> — Run <YYYY-MM-DD> (<run-id>)

<ONE SENTENCE. The strongest honest reading of the evidence. No hedging,
no "it depends", no list. This is the line someone repeats in a meeting.>

## Top 3
1. **[P0] <Title>** — <one line: the cost, not the description> (<personas>)
2. **[P1] <Title>** — <one line> (<personas>)
3. **[P1] <Title>** — <one line> (<personas>)

## Limits on this read
- **Personas:** <list> — ⚠ INFERRED (generic) | researched (supplied)
- **Not reached:** <surfaces, flows — or "none">
- **Excluded:** <scope exclusions, verbatim — auth wall always>
- **Models:** traversal `<model>` · scoring `<model>`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| <name> | <MM:SS> | healthy / at risk / not reached | Pass/Partial/Fail | Pass/Partial/Fail |

## Severity flips
<One line per behaviour scoring differently across personas. "None" if none —
and if only one persona ran, say that instead: a flip could not be observed.>

## Next action
<One line.>
```

**⚑ If `persona_mode` is `generic`, the inferred-persona warning appears in the summary itself, not a footnote.** Findings resting on personas the agent invented are materially weaker than findings from researched ones, and a reader who misses that will over-trust the report.

---

## `findings-final.md` (per lens)

```markdown
# <Product> — <lens> findings — Run <YYYY-MM-DD> (<run-id>)

## Method
- Framework: <the lens's framework, one line>
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: <generic — INFERRED | supplied — researched>
- Scoring model: <model>
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

> **⚑ This block is machine-parsed.** `check_report.py` reads it field by field
> and fails closed — a field it cannot find is treated as absent, and an absent
> `Flow` silently changes the finding's ID. **Keep every field on its own
> bullet; never merge them onto one line with `·` separators.** A `·` inside a
> field's value is fine and expected (several artifacts on one Evidence line);
> it is only the field bullets themselves that must stay separate.
>
> **The `<finding-id>` is computed, never composed** — see the lens agent's
> Output section for the `finding_id.py` invocation. Write the block first, then
> hash exactly the `flow`, `locator` and `title` strings you wrote.

### <finding-id> — <The conclusion, in one line, dev-ticketable>
- **Severity:** P0 | P1 | P2 | P3
- **So what:** <ONE line. What this costs this persona. The reason to fix it.>
- **Framework tags:** <A?, B-G?, C-? — per the lens>
- **Flow:** <shape_1 | shape_2 | shape_2b | shape_3>
- **Personas hit:** <comma-separated>
- **Observed:**
  - <bullet — neutral and concrete>
  - <bullet>
  - <max 3; if it needs a fourth it is probably two findings>
- **Evidence:** `persona-<slug>/screenshots/NN-*.png` · `session.log:NN`
  > "<verbatim persona quote, if there is one>"
- **Repro:**
  1. …
  2. …
- **Fix:** <One line. A direction, not a spec.>
```

**The title carries the finding.** `Same meal shows three different times across surfaces` — not `Timestamp issue` and not `Investigation of meal timestamps`. A reader scanning only the titles should get the whole report.

**`So what` is the field most often written badly.** It is not a restatement of the title and not a framework citation. *"She could not tell which time the product had actually recorded"* is a so-what; *"violates consistency heuristic A4"* is not.

```markdown
---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- <observation> — <what evidence was missing>

## For other lenses
- <observation> — <which lens>

## Coverage gaps
- <surface never opened, flow never completed, device never tested>

## Appendices
- A. Persona debriefs
- B. Session timelines
- C. Screenshot index
```

---

## Rules

**One finding = one issue.** Do not merge unrelated problems because they share a screen.

**Dedupe across personas.** Same issue hit by three personas → one finding, `Personas hit: a, b, c`.

**⚑ Split when severity flips.** If the same behaviour is P1 for one persona and a non-issue for another, that is **two findings**, not an average. Name the persona-specific variants (`<id>-a`, `<id>-b`) and flag the flip in the exec summary.

> A flip usually means the product has picked a user without saying so. Averaging it away destroys the most valuable signal the method produces — and it is the failure mode a hurried analyst falls into every time.

**Do NOT dedupe across lenses.** Each lens report stands alone and is read alone; a problem another lens also found still belongs in yours, scored on your terms. Cross-lens overlap is reconciled once, at the run level, by the orchestrator — never by you, and never by reading another lens's output.

**Every finding carries a stable ID.** `scripts/finding_id.py --lens <lens> --flow <flow> --locator <where> --title <title>`. Not a sequence number — the ID must survive across runs so `report --since` can classify **new · persisting · resolved**. IDs cannot be retrofitted.

**Every finding cites evidence.** No exceptions, including for findings that are obviously true. See `evidence-rules.md`.

**The verdict is the strongest honest reading.** Not bland, not polite, not hedged. If the product is good, say so plainly; a report that cannot say anything positive is as untrustworthy as one that cannot say anything negative.

**Never compare to competitors the user did not ask about.**

**Never report an excluded item.** Scope exclusions from the target file are applied here, at scoring — the traversal still recorded what it saw. An excluded thing that blocked the persona still explains why they got stuck; it explains, it does not score.

**Never report the auth wall.** Infrastructure, always.
