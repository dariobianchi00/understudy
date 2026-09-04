# Severity rubric — P0 / P1 / P2 / P3

**[M] methodology.** **Pass 2 only.**

| Severity | Definition | Examples |
|---|---|---|
| **P0 — Blocker** | The persona cannot complete the flow, **or** the product breaks trust irreparably. | Signup errors out. Auth fails silently. The product produces confident nonsense about the persona's own data. Data appears lost. |
| **P1 — Critical friction** | The persona completes the flow but would realistically churn before paying. | Onboarding over 10 minutes. First value unclear even after it happens. Permissions feel invasive without explanation. The persona says *"I don't trust this"* in the debrief. |
| **P2 — Friction** | Noticeable annoyance. Erodes perceived value; accumulates into churn risk. | Jargon in copy. Unexpected modals. Navigation ambiguity. Unclear empty states. |
| **P3 — Polish** | Worth fixing; does not change behaviour. | Typos. Minor visual inconsistency. Off-brand microcopy. |

---

## The business-impact rule

**Any P0 or P1 in the first 15 minutes is business-critical** at consumer self-serve price points. Users do not come back after a bad first session.

Scale this to the target's actual price and complexity. An enterprise tool with an onboarding call earns patience a £5/month app does not — but the first 15 minutes still decide more than any later hour.

---

## Discipline

- **When torn between two severities, choose the higher** and add one sentence explaining the ambiguity. A reader can downgrade a flagged finding; they cannot discover one you buried.
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

**P2** — A settings screen labels a toggle *"Enable webhook sync"* with no explanation. The persona, non-technical, shrugs and moves on. No immediate consequence, but trust is nicked.
→ Friction. `P2` · `A2`

**P3** — A confirmation toast reads *"You're changes were saved."*
→ Polish. `P3` · `A4`

---

## The severity flip

The most valuable signal this method produces, and the easiest to lose.

When the same behaviour lands at different severities for different personas — P1 for the novice, non-issue for the power user — **that is not noise to average away.** It usually means the product has picked a user without saying so.

Write it as **two findings** with persona-specific variants, and flag the flip explicitly in the exec summary. See `report-template.md`.
