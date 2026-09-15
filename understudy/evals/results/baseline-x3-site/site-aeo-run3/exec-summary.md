# Nimbus Notes — aeo — Run 2026-09-08 (fixture01)

An answer engine reading this site's static markup would find no Organization schema, one broken JSON-LD block, and only one page with any extractable answer content — this site is largely unattributable and unquotable as it stands.

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
1. **[P1] No Organization schema anywhere on the site** — no machine-readable statement of who this company is, despite clear facts in prose (n/a)
2. **[P2] Homepage's only JSON-LD block is invalid and unparseable** — the one schema attempt on the entry page fails to parse at all (n/a)
3. **[P2] Homepage has zero extractable answer blocks** — the highest-traffic page is pure marketing prose with no question-shaped headings (n/a)

## Score
- **Score:** 3/10 — one valid (partial) FAQPage block is the only extractable structured content on the whole site; everything else fails to parse or has nothing to lift.

## Limits on this read
- **Personas:** n/a — this is a no-persona lens (schema/markup only)
- **Not reached:** `/app/login.html` (robots-excluded), off-domain analytics/font assets
- **Excluded:** none beyond the standard auth-wall exclusion (n/a here — no auth content in scope)
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
None — this lens has no personas; findings are per-page, not per-persona.

## Next action
Add valid `Organization` JSON-LD (name, url, logo, sameAs) sitewide, fix the broken homepage schema, and turn the pricing page's marketing copy into a self-contained Q&A block.
