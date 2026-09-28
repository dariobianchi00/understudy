# Nimbus Notes — technical — Run 2026-09-08 (fixture01)

The homepage's mobile LCP is poor at 5.8 s, driven almost entirely by a 3.9 MB hero image delivered at native 3000×2000 resolution and shown at 350×233; the pricing page and both desktop views are fast and clean.

> **Lab measurements.** One machine, one connection, one moment, cold cache.
> These identify what is wrong with the *page* — an oversized image is a fact at
> any sample size. They do **not** describe what your users experience, which
> needs field data this tool cannot reach.

## Core Web Vitals — measured separately, reported separately
| Page | Viewport | LCP | CLS | TBT | FCP | TTFB |
|---|---|---|---|---|---|---|
| / | mobile 390×844 | 5.8 s ✗ | 0.04 ✓ | 410 ms ⚠ | 2.9 s ⚠ | 120 ms ✓ |
| / | desktop 1440×900 | 2.1 s ✓ | 0.02 ✓ | 90 ms ✓ | 0.9 s ✓ | 110 ms ✓ |
| /pricing.html | mobile 390×844 | 1.4 s ✓ | 0.01 ✓ | 30 ms ✓ | 0.8 s ✓ | 110 ms ✓ |
| /pricing.html | desktop 1440×900 | 0.9 s ✓ | 0.01 ✓ | 10 ms ✓ | 0.5 s ✓ | 100 ms ✓ |

## Weight
| Page | Viewport | Weight | Requests | Third-party |
|---|---|---|---|---|
| / | mobile | 3.9 MB | 9 | 99 KB / 2 domains |
| / | desktop | 3.9 MB | 9 | 99 KB / 2 domains |
| /pricing.html | mobile | 5.1 KB | 3 | 0 KB / 0 domains |
| /pricing.html | desktop | 5.1 KB | 3 | 0 KB / 0 domains |

## Top 3
1. **[P1] Unresized hero image drives mobile LCP to 5.8 s** — 3.9 MB image is 95% of homepage weight and the sole cause of the poor mobile LCP (n/a)
2. **[P2] Render-blocking stylesheet and font CSS delay first paint** — two blocking resources sit in `<head>` before any paint on both pages (n/a)
3. **[P2] CSS and HTML served without compression** — every text response ships uncompressed, inflating transfer on every visit (n/a)

## Score
- **Score:** 6/10 — the site is fast everywhere except one uncompressed hero image that makes the homepage slow on mobile, the page that matters most.

## Limits on this read
- **Personas:** n/a — this lens scores measured pages, not persona runs.
- **Not reached:** No pages beyond `/` and `/pricing.html` were measured this run.
- **Excluded:** none recorded in manifest.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
See Core Web Vitals and Weight tables above — this lens has no personas, so the standard per-persona numbers table does not apply.

## Severity flips
n/a — no personas in this lens; nothing to flip across.

## Next action
Resize and compress `/assets/generated/hero.png` to its displayed dimensions (≤600×400) before anything else on this page.
