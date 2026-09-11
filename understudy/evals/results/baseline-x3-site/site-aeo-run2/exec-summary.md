# Nimbus Notes — aeo — Run 2026-09-08 (fixture01)

An answer engine reading this site's static markup could not reliably identify who Nimbus Notes is or quote it cleanly: the only schema on the homepage is broken JSON, no page anywhere declares `Organization`, and 3 of 5 crawled pages have zero extractable answer blocks.

> **Scope: static markup only.** This report judges whether an answer engine
> *could* extract and attribute this site. It does **not** query live answer
> engines and says nothing about whether the site is cited today — that half is
> not in v1.

## Coverage
| | |
|---|---|
| Pages with any structured data | 2 of 5 |
| Organization schema | absent |
| Extractable answer blocks | 3 across 1 page (about.html) |
| llms.txt | absent |

## Top 3
1. **[P1] No `Organization` schema anywhere on the site** — no page states machine-readably who Nimbus Notes Ltd is, so nothing anchors attribution. (n/a)
2. **[P1] Homepage's only JSON-LD is invalid** — the `SoftwareApplication` block has a truncated price value and fails to parse. (n/a)
3. **[P2] 3 of 5 crawled pages have zero extractable answer blocks** — homepage, pricing and privacy are marketing/legal prose with no question-shaped headings. (n/a)

## Score
- **Score:** 5/10 — Only the About page is cleanly extractable; the homepage's schema is broken and the entity itself is never declared machine-readably.

## Limits on this read
- **Personas:** n/a — this lens has no personas.
- **Not reached:** `/app/login.html` (excluded — auth wall, infrastructure); off-domain analytics/font assets (out of scope).
- **Excluded:** auth wall (`/app/login.html`, disallowed by robots.txt) — infrastructure, not scored.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
None — this lens has no personas, so a flip could not be observed.

## Next action
Fix the homepage's malformed JSON-LD and add site-wide `Organization` schema with `name`, `url`, `logo`, `sameAs`.
