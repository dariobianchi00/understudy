# Nimbus Notes — conversion — Run 2026-09-08 (fixture01)

The site has no way to start a free trial: every plan says "Contact sales", no price is shown, and the one visitor who tried to act abandoned.

⚠ **Personas are INFERRED (generic), not researched — weigh every finding accordingly.**

## Top 3
1. **[P0] No free trial or self-serve signup exists; every route to start goes through sales** — the stated goal is impossible for every visitor (evaluator)
2. **[P1] Pricing page shows no price on any of its three plans** — the evaluator came for the cost, got none, and gave up (evaluator)
3. **[P1] Contact sales leads to a 7-field demo form that requires a phone number before any product is shown** — the evaluator backed out of the only available ask (evaluator)

## Against the stated goal
**Goal:** Start a free trial without talking to sales
**Outcome:** could not — no trial path exists
**In their words:** "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page." (evaluator) · "Leave. The cookie bar and the privacy page disagree, and the privacy page won't say who the partners are." (sceptic)

## Score
- **Score:** 1/10 — no visitor can start a trial without sales; the evaluator gave up at pricing, and the sceptic left for trust reasons

## Limits on this read
- **Personas:** evaluator (desktop), sceptic (iPhone 13) — ⚠ INFERRED (generic)
- **Not reached:** `app/login.html`; sceptic never opened pricing or the demo form; no form submitted (by design)
- **Excluded:** none in manifest; auth wall always excluded
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | Reached goal | Price found | Forms opened / submitted | Demo form burden | Q3 outcome |
|---|---|---|---|---|---|
| evaluator | No | No | 1 / 0 | 7 fields, 5 required incl. phone | "Nothing" — search for alternative |
| sceptic | No | Not looked | 0 / 0 | not seen | "Leave" |

- Findings: P0 ×1 · P1 ×2 · P2 ×2 · P3 ×0

## Severity flips
- None observed; the sceptic never reached pricing or a form, so conversion flips could not be tested on mobile.

## Next action
- Ship a self-serve "Start free trial" button with a visible price on the Starter and Team cards.
