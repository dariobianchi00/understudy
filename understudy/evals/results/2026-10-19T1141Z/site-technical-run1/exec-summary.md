# Nimbus Notes — technical — Run 2026-09-08 (fixture01)

One 3.9 MB hero image makes the home page 4.1 MB and pushes mobile LCP to a poor 5.8 s, while the pricing page is fast.

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

- All viewports verified; throttling none; 1 run each. Desktop flatters the home page.

## Weight
| Page | Viewport | Weight | Requests | Third-party |
|---|---|---|---|---|
| / | mobile | 4.1 MB | 9 | 99 KB / 2 domains |
| / | desktop | 4.1 MB | 9 | 99 KB / 2 domains |
| /pricing.html | mobile | 5.2 KB | 3 | 0 |
| /pricing.html | desktop | 5.2 KB | 3 | 0 |

## Top 3
1. **[P1] 3.9 MB hero.png delivered at 3000×2000 and shown at 350×233** — poor mobile LCP, 95% of page weight (n/a)
2. **[P2] Third-party font CSS and style.css block first paint** — mobile FCP 2.9 s (n/a)
3. **[P2] Mobile TBT is 410 ms** — page ignores input for 410 ms on mobile (n/a)

## Score
- **Score:** 6/10 — One image makes the home page slow on mobile; pricing is fast and the remaining items are small.

## Limits on this read
- **Personas:** n/a — measurement lens
- **Not reached:** features, about, privacy not measured
- **Excluded:** none; auth wall never reported
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Severity flips
- Home page LCP differs by viewport (poor mobile, good desktop); reported as one P1 on mobile.

## Next action
- Replace hero.png with a responsive ≤150 KB AVIF/WebP and re-measure mobile.
