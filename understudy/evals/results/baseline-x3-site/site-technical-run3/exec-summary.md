# Nimbus Notes — technical — Run 2026-09-08 (fixture01)

The homepage is slow on mobile because a single 3.9 MB hero image is delivered at 8x the size it is shown, pushing mobile LCP to 5.8 s and page weight to 4.1 MB, while the pricing page is fast and clean on both viewports.

> **Lab measurements.** One machine, one connection, one moment, cold cache.
> These identify what is wrong with the *page* — an oversized image is a fact at
> any sample size. They do **not** describe what your users experience, which
> needs field data this tool cannot reach.

## Top 3
1. **[P1] Unoptimized hero image drives poor mobile LCP and 4.1 MB page weight** — homepage LCP is 5.8 s on mobile, more than double the "good" threshold (n/a)
2. **[P2] Static assets served without cache-control headers** — every repeat visit re-downloads the stylesheet and the 3.9 MB hero image (n/a)
3. **[P2] Text and CSS responses served without compression** — HTML and CSS ship uncompressed on both pages, adding avoidable bytes to every request (n/a)

## Score
- **Score:** 5/10 — homepage is genuinely slow on mobile from one fixable image; pricing page and hygiene are otherwise clean.

## Limits on this read
- **Personas:** n/a — this is a no-persona lens; `persona_mode: generic` applies to the run overall, not to these measurements.
- **Not reached:** none — index and pricing measured on both mobile and desktop.
- **Excluded:** none.
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
| /pricing.html | mobile & desktop | 5.2 KB | 3 | none |

## Severity flips
- Index page LCP is P1 on mobile (5.8 s, poor) and non-issue on desktop (2.1 s, good) — same cause, same asset, worse on the viewport most visitors use.

## Next action
Resize and re-encode `hero.png` to the displayed dimensions (~600×400) before touching anything else on this page.
