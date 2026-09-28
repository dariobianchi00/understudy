# Nimbus Notes — aeo — Run 2026-09-08 (fixture01)

An answer engine can cleanly lift two Q&A pairs from the About page and nothing else — Organization schema is absent everywhere, the homepage's only JSON-LD is broken, and no page states a price.

> **Scope: static markup only.** This report judges whether an answer engine
> *could* extract and attribute this site. It does **not** query live answer
> engines and says nothing about whether the site is cited today — that half is
> not in v1.

## Coverage
| | |
|---|---|
| Pages with any structured data | 2 of 5 |
| Organization schema | absent |
| Extractable answer blocks | 3 across 1 page |
| llms.txt | absent |

## Top 3
1. **[P1] No Organization schema anywhere on the site** — no machine-readable name, url, logo, or sameAs for the entity at all. (n/a)
2. **[P1] Homepage JSON-LD is malformed and fails to parse** — the one structured-data attempt on the homepage yields zero usable data. (n/a)
3. **[P2] Pricing page states no prices, structured or visual** — no page on the site gives an extractable answer to "what does this cost." (n/a)

## Score
- **Score:** 4/10 — one page (About) is genuinely extractable; the other four give an answer engine no reliable entity ID, no valid schema, and no price.

## Limits on this read
- **Personas:** n/a — no-persona lens. Manifest `persona_mode` is `generic`, not used by this lens.
- **Not reached:** `/app/login.html` (disallowed by robots.txt) · off-domain analytics/font assets — see Coverage gaps in findings-final.md.
- **Excluded:** none declared in manifest (`scope_exclusions: []`); the auth wall at `/app/login.html` is infrastructure and not reported.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Severity flips
None — this is a no-persona lens; a flip could not be observed.

## Next action
Add site-wide Organization schema and fix the homepage's truncated JSON-LD before anything else on this list.
