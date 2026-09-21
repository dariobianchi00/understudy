# Nimbus Notes — conversion — Run 2026-09-08 (fixture01)

Neither visitor could start a free trial because the site sells no trial — every route ends at a seven-field sales form — and the one who came to price the product left to look for an alternative.

## Top 3
1. **[P0] No self-serve trial route exists: every plan CTA is "Contact sales"** — the stated goal is unreachable by construction, on every page (evaluator)
2. **[P1] Pricing page carries no numbers, and the visitor who came to price it gave up** — the one buying visitor abandoned at 02:30 and would search elsewhere (evaluator)
3. **[P1] Demo form asks seven fields, five required including phone, before the product is shown** — the only conversion point on the site, and the evaluator backed out of it (evaluator)

## Against the stated goal
**Goal:** Start a free trial without talking to sales
**Outcome:** could not — no trial exists to start; "trial", "sign up", "get started" and "free" appear zero times across all five crawled pages
**In their words:** "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page."

## Score
- **Score:** 2/10 — the site's only conversion path is a sales form, the goal it was measured against has no route at all, and both visitors' answer to "what next" was nothing.

## Limits on this read
- **Personas:** evaluator (desktop 1440x900), sceptic (iPhone 13) — ⚠ INFERRED (generic `persona_mode`); findings rest on personas the harness invented
- **Not reached:** `app/login.html` (logged-out run) · no form submitted, by design — nothing here describes what happens after submit
- **Excluded:** none declared in `manifest.json`
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | Next step at the fold | Forms opened / submitted | Reached the goal | Q3 outcome |
|---|---|---|---|---|
| evaluator | newsletter only (hero CTA inert) | 1 / 0 | No — `price_found: false` | "Nothing" — would search for an alternative |
| sceptic | newsletter only (hero CTA inert) | 0 / 0 | Not attempted | "Leave" |

## Severity flips
- **Missing price:** P1 for the evaluator, who came to price it and gave up; not observed for the sceptic, who never looked (`timeline.json` → `attempted: false`) — scored on the evaluator only, not averaged.

## Next action
Ship a "Start free trial" button in the header and on the Starter and Team cards, with a price beside each, before touching anything else.
