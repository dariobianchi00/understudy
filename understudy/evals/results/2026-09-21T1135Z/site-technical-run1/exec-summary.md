# Nimbus Notes — technical — Run 2026-09-08 (fixture01)

The homepage's mobile Core Web Vitals fail on a single 3.9 MB hero image shipped at 3000×2000 into a 350×233 slot; the pricing page is fast and clean on every measured dimension.

> **Lab measurements.** One machine, one connection, one moment, cold cache.
> These identify what is wrong with the *page* — an oversized image is a fact at
> any sample size. They do **not** describe what your users experience, which
> needs field data this tool cannot reach.

## Core Web Vitals — measured separately, reported separately
| Page | Viewport | LCP | CLS | TBT | FCP | TTFB |
|---|---|---|---|---|---|---|
| / | mobile 390×844 | 5.8 s ⚠ poor | 0.04 ✓ | 410 ms ⚠ | 2.9 s ⚠ | 120 ms ✓ |
| / | desktop 1440×900 | 2.1 s ✓ | 0.02 ✓ | 90 ms ✓ | 0.9 s ✓ | 110 ms ✓ |
| /pricing.html | mobile 390×844 | 1.4 s ✓ | 0.01 ✓ | 30 ms ✓ | 0.8 s ✓ | 110 ms ✓ |
| /pricing.html | desktop 1440×900 | 0.9 s ✓ | 0.01 ✓ | 10 ms ✓ | 0.5 s ✓ | 100 ms ✓ |

## Weight
| Page | Viewport | Weight | Requests | Third-party |
|---|---|---|---|---|
| / | mobile | 4.10 MB | 9 | 101 KB / 2 domains |
| / | desktop | 4.10 MB | 9 | 101 KB / 2 domains |
| /pricing.html | mobile | 5.2 KB | 3 | 0 |
| /pricing.html | desktop | 5.2 KB | 3 | 0 |

## Top 3
1. **[P1] Homepage hero image ships at 10x display size, driving poor mobile LCP** — 3.9 MB PNG delivered at 3000×2000, shown at 350×233 on mobile; mobile LCP hits 5.8 s. (n/a)
2. **[P2] Render-blocking stylesheets delay first paint on homepage and pricing** — Two stylesheets block rendering site-wide, one fetched cross-origin from a font CDN. (n/a)
3. **[P2] Text responses served without compression across the site** — HTML and CSS ship with no `content-encoding` on both pages measured. (n/a)

## Score
- **Score:** 6/10 — homepage mobile fails Core Web Vitals on one fixable image; pricing page and desktop are clean.

## Limits on this read
- **Personas:** n/a — this lens measures pages, not personas
- **Not reached:** no pages beyond index and pricing were measured
- **Excluded:** none
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
Only one persona-independent measurement per page/viewport — a flip could not be observed (this lens has no personas).

## Next action
Compress and correctly size `hero.png` for its 350–600px display width; re-measure homepage mobile LCP.
