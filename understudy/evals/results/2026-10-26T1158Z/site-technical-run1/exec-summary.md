# Nimbus Notes — technical — Run 2026-09-08 (fixture01)

One unoptimised 3.9 MB hero image makes the home page a 4.1 MB, 5.8 s-LCP "poor" load on mobile, while the pricing page is tiny and fast.

> **Lab measurements.** One machine, one connection, one moment, cold cache.
> These identify what is wrong with the *page* — an oversized image is a fact at
> any sample size. They do **not** describe what your users experience, which
> needs field data this tool cannot reach.

## Core Web Vitals — measured separately, reported separately
| Page | Viewport | LCP | CLS | TBT | FCP | TTFB |
|---|---|---|---|---|---|---|
| / | mobile 390×844 | 5.8 s ✗ poor | 0.04 ✓ | 410 ms ⚠ | 2.9 s ⚠ | 120 ms ✓ |
| / | desktop 1440×900 | 2.1 s ✓ | 0.02 ✓ | 90 ms ✓ | 0.9 s ✓ | 110 ms ✓ |
| /pricing.html | mobile 390×844 | 1.4 s ✓ | 0.01 ✓ | 30 ms ✓ | 0.8 s ✓ | 110 ms ✓ |
| /pricing.html | desktop 1440×900 | 0.9 s ✓ | 0.01 ✓ | 10 ms ✓ | 0.5 s ✓ | 100 ms ✓ |

## Weight
| Page | Viewport | Weight | Requests | Third-party |
|---|---|---|---|---|
| / | mobile | 4.1 MB | 9 | 99 KB / 2 domains |
| / | desktop | 4.1 MB | 9 | 99 KB / 2 domains |
| /pricing.html | mobile | 5.2 KB | 3 | 0 / 0 domains |
| /pricing.html | desktop | 5.2 KB | 3 | 0 / 0 domains |

## Top 3
1. **[P1] 3.9 MB hero.png (3000×2000 shown at 350×233) drives a 5.8 s mobile LCP and a 4.1 MB page** — 95% of the home page's bytes are one image (n/a)
2. **[P2] No cache-control on style.css or hero.png** — repeat visits re-download the 3.9 MB image (n/a)
3. **[P2] Render-blocking third-party font CSS sits ahead of first paint (mobile FCP 2.9 s)** — 62 KB cross-origin stylesheet blocks paint (n/a)

## Score
- **Score:** 7/10 — Pricing loads fast; home is a 4.1 MB, poor-LCP page on mobile due to one fixable image.

## Limits on this read
- **Personas:** n/a — no-persona lens; run `persona_mode` is generic, so ⚠ INFERRED personas elsewhere
- **Not reached:** features, about, privacy not measured; each page measured once, no throttling
- **Excluded:** none in manifest; auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Severity flips
- None — a no-persona lens; mobile and desktop are reported separately above (home LCP is poor on mobile, good on desktop).

## Next action
- Resize and re-encode hero.png (≤150 KB, `srcset`), then re-measure home on mobile.
