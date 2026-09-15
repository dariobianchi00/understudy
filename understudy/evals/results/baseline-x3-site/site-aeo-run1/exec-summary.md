# Nimbus Notes — aeo — Run 2026-09-08 (fixture01)

An answer engine reading this crawl finds one working FAQ page, a broken schema on the homepage, no Organization markup anywhere, and two pages — home and pricing — with nothing quotable at all.

> **Scope: static markup only.** This report judges whether an answer engine
> *could* extract and attribute this site. It does **not** query live answer
> engines and says nothing about whether the site is cited today — that half is
> not in v1.

## Coverage
| | |
|---|---|
| Pages with any structured data | 2 of 5 (1 invalid) |
| Organization schema | absent |
| Extractable answer blocks | 3 across 1 page (1 of the 3 not schema-marked) |
| llms.txt | absent |

## Top 3
1. **[P1] No `Organization` schema anywhere on the site** — the entity's name, founder and address exist only as prose on /about; no page states it machine-readably (n/a)
2. **[P1] Homepage JSON-LD is invalid and truncated, the site's only schema attempt outside /about** — `SoftwareApplication` block fails to parse (n/a)
3. **[P2] Homepage has zero extractable answer blocks** — marketing headings only, nothing a Q&A engine can lift (n/a)

## Score
- **Score:** 4/10 — one FAQ page extracts cleanly, but there is no valid Organization schema, the homepage's only JSON-LD is broken, and two of five pages yield nothing quotable.

## Limits on this read
- **Personas:** n/a — this lens is not persona-scored; `persona_mode` is `generic` for the run overall.
- **Not reached:** `/app/login.html` (robots-disallowed); off-domain analytics/font assets — none of these carry page content relevant to extraction.
- **Excluded:** none declared in scope_exclusions.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
None — this lens has no personas, so a flip cannot be observed.

## Next action
Fix the truncated homepage JSON-LD and add a site-wide `Organization` block before anything else on this list.
