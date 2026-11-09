# Nimbus Notes — ux — Run 2026-09-08 (fixture02)

Nimbus Notes fails its one job: both personas were told "Saved ✓", never saw their note again, gave up, and were shown invented "memories" that broke their trust.

## Top 3
1. **[P0] Save shows "Saved ✓" but the note never appears in "Your cards" or search** — both personas failed the objective and said they would not return or pay (novice, power-user)
2. **[P0] Memories page states invented facts about a brand-new user** — novice: "If it's making these up, is it making up the "Saved" too?" (novice; P1 for power-user)
3. **[P2] Signup forces an irreversible choice between three undefined terms** — novice guessed blind 20 s in, before seeing anything (novice)

## Score
- **Score:** 2/10 — neither persona could save and find a note, both gave up within 7 minutes, and neither would return or pay.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on personas the agent invented
- **Not reached:** card view/edit/delete (no card ever appeared), Export output, connected accounts, mobile
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect." · auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview only; objective not met) | at risk | Fail | Fail |
| power-user | not reached | not reached | Fail | Fail |

- Findings: 2 × P0 · 1 × P1 · 5 × P2 · 0 × P3
- Objective "A new user can write a note and find it again": 0 of 2 personas succeeded; both `gave_up: true`

## Severity flips
- Invented memories: P0 for novice (spread distrust to "Saved") · P1 for power-user (dismissed as "a demo panel", still cited in debrief).
- Irreversible workspace-type choice: P2 for novice (28 s stall, blind guess) · non-issue for power-user ("Fine — I've seen worse").

## Next action
- Make save persist and show the note in "Your cards" and search before touching anything else.
