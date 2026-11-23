# Nimbus Notes — conversion — Run 2026-09-08 (fixture01)

Nobody can start a free trial on this site, because no trial path exists, so the only visitor who looked for a next step found a priceless sales funnel and left.

## Top 3
1. **[P0] No self-serve free trial exists anywhere on the site; every route to a next step ends at sales** — the stated goal is unreachable for every visitor (evaluator)
2. **[P1] Pricing page shows no price on any plan, so the visitor cannot judge whether to start** — evaluator's reason to visit; they gave up at 02:30 (evaluator)
3. **[P1] Demo form asks seven fields, five required including phone, before any product is shown** — evaluator backed out without submitting (evaluator)

## Against the stated goal
**Goal:** Start a free trial without talking to sales
**Outcome:** could not — no trial path exists; evaluator would not, sceptic would not
**In their words:** "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page." (evaluator) · "Leave. The cookie bar and the privacy page disagree, and the privacy page won't say who the partners are." (sceptic)

## Score
- **Score:** 1/10 — the goal cannot be done on this site; neither persona took or wanted a next step

## Limits on this read
- **Personas:** evaluator, sceptic — ⚠ INFERRED (generic); every finding rests on personas the agent invented
- **Not reached:** `app/login.html`, newsletter submission, any form submission; sceptic never looked for price or signup
- **Excluded:** none in manifest · auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | Session | Pages | Forms opened / submitted | Price found | Next step (Q3) |
|---|---|---|---|---|---|
| evaluator | 06:30 | 5 | 1 / 0 | No | Search for an alternative |
| sceptic | 02:50 | 2 | 0 / 0 | Not sought | Leave |

- Calls to action on the site: 0 trial · 3 "Contact sales" · 1 "Request demo" · 1 newsletter · 1 "Log in" · 1 dead "See it in action"
- Demo form: 7 fields, 5 required, phone required

## Severity flips
- None observed — sceptic left over data handling before reaching any conversion point, so no conversion behaviour was tested twice.

## Next action
- Ship a self-serve "Start free trial" button in header, hero and pricing cards, with prices shown beside it.
