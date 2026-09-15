# Nimbus Notes — technical — Run 2026-09-08 (fixture01)

The homepage is unusable-fast on desktop and poor on mobile because a single 3.9 MB hero image is shipped unresized to every visitor, while the pricing page is lean and fast on both.

> **Lab measurements.** One machine, one connection, one moment, cold cache.
> These identify what is wrong with the *page* — an oversized image is a fact at
> any sample size. They do **not** describe what your users experience, which
> needs field data this tool cannot reach.

## Top 3
1. **[P1] 3.9 MB unresized hero image drives mobile LCP to 5.8s** — page fails Core Web Vitals on mobile and ships 4.1 MB on every load (n/a)
2. **[P2] Render-blocking stylesheets delay homepage mobile FCP to 2.9s** — visitors wait nearly 3s to see anything on mobile (n/a)
3. **[P2] Homepage and pricing assets served uncompressed with no cache headers** — every repeat visit re-downloads the same bytes at full size (n/a)

## Score
- **Score:** 6/10 — one avoidable image mistake fails mobile Core Web Vitals on the homepage; everything else measured, including the entire pricing page, is fast and clean.

## Limits on this read
- **Personas:** n/a — this lens has no personas
- **Not reached:** no other pages were measured beyond index and pricing
- **Excluded:** none recorded
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Core Web Vitals — measured separately, reported separately
| Page | Viewport | LCP | CLS | TBT | FCP | TTFB |
|---|---|---|---|---|---|---|
| / | mobile 390×844 | 5.8 s ⚠ poor | 0.04 ✓ | 410 ms ⚠ needs work | 2.9 s ⚠ needs work | 120 ms ✓ |
| / | desktop 1440×900 | 2.1 s ✓ | 0.02 ✓ | 90 ms ✓ | 900 ms ✓ | 110 ms ✓ |
| /pricing.html | mobile 390×844 | 1.4 s ✓ | 0.01 ✓ | 30 ms ✓ | 800 ms ✓ | 110 ms ✓ |
| /pricing.html | desktop 1440×900 | 900 ms ✓ | 0.01 ✓ | 10 ms ✓ | 500 ms ✓ | 100 ms ✓ |

## Weight
| Page | Viewport | Weight | Requests | Third-party |
|---|---|---|---|---|
| / | mobile & desktop | 4.10 MB | 9 | 101 KB / 2 domains |
| /pricing.html | mobile & desktop | 5.2 KB | 3 | 0 KB / 0 domains |

## Severity flips
- None across viewport for pricing.html — good on both.
- The hero-image finding is P1 by consequence on mobile (LCP fails); the identical asset costs desktop only page weight, not a Vitals failure — noted in the finding, not split, since it is one root cause.

## Next action
Resize and compress `assets/generated/hero.png` to its displayed dimensions before the next measurement pass.
