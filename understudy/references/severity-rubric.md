# Severity rubric — P0 / P1 / P2 / P3

**[M] methodology.** **Pass 2 only.**

| Severity | Definition | Examples |
|---|---|---|
| **P0 — Blocker** | The persona cannot complete the flow, **or** the product breaks trust irreparably. | Signup errors out. Auth fails silently. The product produces confident nonsense about the persona's own data. Data appears lost. |
| **P1 — Critical friction** | The persona completes the flow, but **the run shows** them stopping, leaving, or failing to reach the thing they came for — or saying in the debrief that they would not pay or would not return. | Onboarding over 10 minutes and the persona says so. First value never recognised as value. The persona abandons a step and does something else. *"I don't trust this"* or *"I wouldn't pay for this"* in the debrief. |
| **P2 — Friction** | Noticeable annoyance the persona pushed through. Erodes perceived value; accumulates into churn risk. **A complaint with continued use is a P2, however loud.** | Jargon in copy. Unexpected modals. Navigation ambiguity. Unclear empty states. A persona who grumbled and carried on. |
| **P3 — Polish** | Worth fixing; does not change behaviour. | Typos. Minor visual inconsistency. Off-brand microcopy. |

---

## The business-impact rule

**Any P0 or P1 in the first 15 minutes is business-critical** at consumer self-serve price points. Users do not come back after a bad first session.

Scale this to the target's actual price and complexity. An enterprise tool with an onboarding call earns patience a £5/month app does not — but the first 15 minutes still decide more than any later hour.

---

## Discipline

- **P1 is observed, not predicted.** It needs a moment in the run — a log line, a debrief answer, a screenshot — where the persona stopped, left, failed, or said they would not pay or return. "Would realistically churn" without that moment is a P2 with a sentence about the risk. This is the line most often crossed, and every crossing costs the product two points it did not earn.
- **Torn between P0 and P1? Choose P0** and add one sentence explaining the ambiguity — a reader can downgrade a flagged blocker; they cannot discover one you buried. **Torn between P1 and P2? Choose P2** and name the churn risk in the *So what* line; the P1 evidence rule above is what settles it, not your feeling about the product.
- **A finding with no user-visible consequence is not a finding.** Drop it.
- **A finding without evidence is not a finding.** Drop it — see `evidence-rules.md`. This holds even when the finding is obviously true.
- **Severity describes impact, never confidence.** Do not upgrade a P2 because you feel strongly about it, and never inflate severity to compensate for weak evidence.
- **Severity is per persona.** If the same behaviour is P1 for one persona and a non-issue for another, that is two findings, not an average. See `report-template.md`.

---

## Worked examples

**P0** — The persona clicks *Sign up*, waits on a spinner for 60 seconds, gets a generic error page with no next step offered.
→ Blocker. `P0` · `A1, A9, C-ABANDON`

**P1** — The persona completes signup in 8 minutes, reaches the dashboard, cannot find any way to produce a first result. Explores for 4 minutes, gives up.
→ Critical friction; activation fails. `P1` · `B-G1, C-TTFV`

**P2, not P1** — The persona says *"this onboarding is way too long"* at minute 6, finishes it at minute 9, reaches first value at minute 11 and says in the debrief they would use it again.
→ A loud complaint with continued use. `P2`, with the *So what* naming the risk that a less patient user leaves at minute 6. It becomes a P1 only if a persona actually left.

**P2** — A settings screen labels a toggle *"Enable webhook sync"* with no explanation. The persona, non-technical, shrugs and moves on. No immediate consequence, but trust is nicked.
→ Friction. `P2` · `A2`

**P3** — A confirmation toast reads *"You're changes were saved."*
→ Polish. `P3` · `A4`

---

## The severity flip

The most valuable signal this method produces, and the easiest to lose.

When the same behaviour lands at different severities for different personas — P1 for the novice, non-issue for the power user — **that is not noise to average away.** It usually means the product has picked a user without saying so.

Write it as **two findings** with persona-specific variants, and flag the flip explicitly in the exec summary. See `report-template.md`.
