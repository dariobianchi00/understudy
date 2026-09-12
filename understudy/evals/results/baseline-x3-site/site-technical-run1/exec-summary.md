# Nimbus Notes — technical — Run 2026-09-08 (fixture01)

The homepage is carrying a 3.9 MB hero image that pushes mobile LCP to 5.8 s and total page weight to 4.1 MB, while the pricing page is fast and clean on both viewports.

> **Lab measurements.** One machine, one connection, one moment, cold cache.
> These identify what is wrong with the *page* — an oversized image is a fact at
> any sample size. They do **not** describe what your users experience, which
> needs field data this tool cannot reach.

## Core Web Vitals — measured separately, reported separately
| Page | Viewport | LCP | CLS | TBT | FCP | TTFB |
|---|---|---|---|---|---|---|
| / | mobile 390×844 | 5.8 s ⛔ | 0.04 ✓ | 410 ms ⚠ | 2.9 s ⚠ | 120 ms ✓ |
| / | desktop 1440×900 | 2.1 s ✓ | 0.02 ✓ | 90 ms ✓ | 0.9 s ✓ | 110 ms ✓ |
| /pricing.html | mobile 390×844 | 1.4 s ✓ | 0.01 ✓ | 30 ms ✓ | 0.8 s ✓ | 110 ms ✓ |
| /pricing.html | desktop 1440×900 | 0.9 s ✓ | 0.01 ✓ | 10 ms ✓ | 0.5 s ✓ | 100 ms ✓ |

## Weight
| Page | Viewport | Weight | Requests | Third-party |
|---|---|---|---|---|
| / | mobile | 4.1 MB | 9 | 101 KB / 2 domains |
| / | desktop | 4.1 MB | 9 | 101 KB / 2 domains |
| /pricing.html | mobile | 5.2 KB | 3 | 0 KB / 0 domains |
| /pricing.html | desktop | 5.2 KB | 3 | 0 KB / 0 domains |

## Top 3
1. **[P1] Oversized hero image drives poor mobile LCP and 4 MB page weight** — 3000×2000 PNG shown at 350×233 on mobile, 3.9 MB of the page's 4.1 MB. (n/a)
2. **[P2] Render-blocking stylesheets delay first paint and inflate TBT on mobile** — FCP 2.9 s and TBT 410 ms on mobile, both in the "needs improvement" band. (n/a)
3. **[P2] Static assets ship without compression or cache headers** — style.css and the homepage HTML have no content-encoding; style.css and hero.png have no cache-control. (n/a)

## Score
- **Score:** 6/10 — the primary landing page is heavy and slow on mobile from one oversized, uncompressed, uncached image; everything else measured is clean.

## Limits on this read
- **Personas:** n/a — this lens has no personas
- **Not reached:** none — both pages measured on both viewports
- **Excluded:** none
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Severity flips
- Not applicable — no personas run under this lens.

## Next action
Compress and responsively-size `hero.png` (target ≤150 KB at displayed dimensions) before anything else on this page.
