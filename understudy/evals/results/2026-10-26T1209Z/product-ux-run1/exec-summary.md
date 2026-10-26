# Nimbus Notes — ux — Run 2026-09-08 (fixture02)

Nimbus Notes fails its core job: both personas wrote a note, were told "Saved ✓", never saw it again, and left saying they would not pay.

## Top 3
1. **[P0] Save shows "Saved ✓" but the note never appears in the cards list or search** — the stated objective failed for 2/2 personas; both gave up (novice, power-user)
2. **[P0] Memories page states invented facts about a brand-new user, and the novice stops trusting "Saved" too** — fabricated "memories" turned a lost note into "It is lying to me" (novice)
3. **[P2] Signup forces an irreversible workspace-type choice between three unexplained terms before the product is seen** — novice guessed "Hybrid mesh" at random in the first 48 seconds (novice)

## Score
- **Score:** 2/10 — neither persona could save and find a note; both quit and would pay nothing

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic). Findings rest on personas the agent invented, not researched users.
- **Not reached:** Export output (button seen, never clicked); any note detail or edit view (no note ever persisted)
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect." Auth wall always excluded.
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Layer B:** applied to the Memories surface only — it presents inferred facts "built from your notes and connected accounts"

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview only; saved note never reached) | not reached | Fail | Fail |
| power-user | — | not reached | Fail | Fail |

- Objective "write a note and find it again": 0/2 personas; 3 save attempts, 0 notes visible
- Session length before quitting: novice 06:30, power-user 03:00
- Only positives named in debrief: live word count/preview (novice), Markdown export (both)

## Severity flips
- Memories page: P0 for novice (spread distrust to "Saved"), P1 for power-user (dismissed as "a demo panel", refused to trust it) — split into two findings
- Workspace-type choice: P2 for novice (random guess), non-issue for power-user ("Fine — I've seen worse")
- Keyboard shortcuts: P2 for power-user only; novice never looked for them

## Next action
- Make Save fail visibly when the write fails, then fix persistence so saved notes list and search — nothing else matters until then.
