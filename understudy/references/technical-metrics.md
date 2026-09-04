# Technical metrics — the measured set

**[M] methodology.** Loaded by `traversal-measure` (Mode B capture) and by `lens-technical` (scoring). Contains no scoring vocabulary — safe to load during capture.

All of it is obtainable from Playwright MCP with no extra tooling: Navigation Timing, `PerformanceObserver`, the network log, response headers.

---

## ⚑ These are lab numbers. The report must say so on its face.

One measurement, one machine, one connection, one moment.

**What they are good for:** identifying what is wrong with the *page*. A 4 MB hero image is a fact at any sample size. An uncompressed response is a fact. A render-blocking script is a fact.

**What they are not:** a description of what users experience. That needs field data — real sessions, many devices, many networks — which understudy cannot reach.

> **Presenting a lab LCP as "your users' LCP" is confidently wrong, and it is the kind of error that gets a whole tool distrusted.** Every other number beside it becomes suspect.

The caveat sits **in the report body, not a footnote**. Non-negotiable.

**Measure mobile and desktop separately.** For most marketing sites the mobile number is the real one and the desktop number is the flattering one. Reporting one figure hides which.

---

## Tier 1 — Experience

The Core Web Vitals, plus the two that explain them.

| Metric | What it is | How |
|---|---|---|
| **LCP** | Largest Contentful Paint — when the main thing appeared | `PerformanceObserver` on `largest-contentful-paint`; take the last entry |
| **CLS** | Cumulative Layout Shift — how much the page moved under the reader | `PerformanceObserver` on `layout-shift`, summing entries where `!hadRecentInput` |
| **TBT** | Total Blocking Time — an INP proxy; how long the page ignored input | Sum of `(duration − 50ms)` over long tasks between FCP and load |
| **FCP** | First Contentful Paint — when anything appeared | `performance.getEntriesByName('first-contentful-paint')` |
| **TTFB** | Time To First Byte — server and network before anything could start | `navigation.responseStart − navigation.requestStart` |

**Thresholds** (Google's, for reference — not understudy's judgement):

| | Good | Needs work | Poor |
|---|---|---|---|
| LCP | ≤ 2.5 s | ≤ 4.0 s | > 4.0 s |
| CLS | ≤ 0.1 | ≤ 0.25 | > 0.25 |
| TBT | ≤ 200 ms | ≤ 600 ms | > 600 ms |
| FCP | ≤ 1.8 s | ≤ 3.0 s | > 3.0 s |
| TTFB | ≤ 800 ms | ≤ 1.8 s | > 1.8 s |

**⚑ TBT is a proxy for INP, not INP.** INP needs real interactions from real users. Say "TBT" in the report and never label it INP.

---

## Tier 2 — Delivery

Where a fast site went slow. Oversized images and third parties account for most of it.

| Metric | How |
|---|---|
| **Page weight** | Sum of `transferSize` across all resources |
| **Request count** | Number of entries in the resource timing log |
| **5 largest assets** | Sorted by `transferSize`, with type and URL |
| **Image hygiene** | For each image: format · `transferSize` · `naturalWidth/Height` vs displayed `clientWidth/Height` · whether `loading="lazy"` below the fold |
| **Compression** | `content-encoding` on text resources — anything text-like without gzip/br is a finding |
| **Cache headers** | `cache-control` on static assets — missing or trivially short is a finding |
| **Render-blocking** | Stylesheets and non-`async`/`defer` scripts in `<head>` |
| **Third-party weight** | Requests grouped by registrable domain ≠ the site's own, with count and bytes |

**Image hygiene is where most sites lose most of their weight**, and the natural-vs-displayed comparison is the finding that writes itself: an image delivered at 3000px and displayed at 400px is wasting 98% of its bytes, on every visit, forever.

**Third-party weight deserves its own line.** A site owner controls their own bundle and often does not realise a tag manager brought twelve friends.

---

## Tier 3 — Hygiene

Cheap to check, embarrassing to miss.

| Check | Fail condition |
|---|---|
| **HTTPS** | Any http:// that does not redirect |
| **HSTS** | No `strict-transport-security` header |
| **Mixed content** | Any http:// subresource on an https:// page |
| **Viewport meta** | Missing or missing `width=device-width` |
| **Redirect chains** | More than one hop from the entry URL |
| **404s on linked assets** | Any 404 in the resource log |
| **Console errors on load** | Any error before `load` fires |

---

## How to measure — the discipline that makes the numbers mean anything

1. **Fresh context per measurement.** A warm cache measures your second visit, not a visitor's first.
2. **Measure the same URL on mobile and desktop separately**, with the viewport verified both times.
3. **Wait for the network to settle** before reading — LCP can change until the page is quiet. Wait for `load`, then a short quiet period, then read.
4. **Record the conditions with the numbers**: viewport, timestamp, whether throttling was applied, and that the cache was cold. **A number without its conditions is not reproducible, and an unreproducible number is not evidence.**
5. **Do not average across pages.** Measure the pages that matter and report them separately; a site-wide mean hides the one page that is broken.
6. **Never re-run until you get a better number.** If you measure twice, report both or report the worse one, and say you measured twice.

---

## What Mode B does not do

Named so nobody expects it:

- **No field data.** No real-user monitoring, no CrUX, no traffic.
- **No throttling by default.** Numbers are from this machine on this connection unless the target says otherwise — which is exactly why they are lab numbers.
- **No accessibility audit.** Related, separate, not built.
- **No repeat-visit measurement.** Cold cache only.
- **No JavaScript profiling.** TBT tells you the page blocked; it does not tell you which function.
