# Nimbus Notes — technical findings — Run 2026-09-08 (fixture01)

## Method
- Framework: technical-metrics.md — Tier 1 Core Web Vitals, Tier 2 delivery, Tier 3 hygiene, mobile/desktop measured separately
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — no-persona lens, lab measurements only
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Scope: `manifest.json` + `measure/` only. Two pages measured: `/` and `/pricing.html`, mobile (390×844) and desktop (1440×900). `viewport_verified: true` on all four records — treated as usable evidence.

---

## Findings

### 3ce561f1cd1a — Oversized hero image drives 4.1MB page weight and 5.8s mobile LCP
- **Severity:** P1
- **So what:** Mobile visitors wait 5.8s for the homepage's largest content to appear — 3.7s longer than the same page on desktop — because the LCP element is a 3.9 MB PNG.
- **Framework tags:** Tier1-LCP, Tier2-image-hygiene, Tier2-page-weight
- **Flow:** measure:index:mobile
- **Locator:** /assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - `hero.png` is the LCP element and the single largest asset: 3,900,000 bytes, delivered at 3000×2000px.
  - Displayed at 350×233 on mobile and 600×400 on desktop — up to 98% of delivered pixels are discarded by the browser.
  - Mobile LCP 5,800ms (poor, >4,000ms threshold); desktop LCP 2,100ms (good) on the identical asset and page.
  - Page weight is 4,104,000 bytes on both viewports — over the ~4MB weight threshold, driven almost entirely by this one file.
- **Evidence:** `measure/index-mobile.json` (tier1.lcp_ms, tier2.images[0], tier2.page_weight_bytes) · `measure/index-desktop.json` (tier1.lcp_ms) · `measure/screenshots/index-mobile.png`
- **Repro:**
  1. Load `http://localhost:8765/` on a 390×844 viewport with cold cache, no throttling.
  2. Observe LCP fires at 5.8s against the hero image.
  3. Compare `measure/index-desktop.json` — same asset, same weight, LCP 2.1s.
- **Fix:** Serve `hero.png` pre-resized to its displayed dimensions (~600×400 max) as compressed WebP/AVIF with responsive `srcset`, targeting under 150KB.

### c161af9eefbe — Render-blocking stylesheets delay mobile first paint to 2.9s
- **Severity:** P2
- **So what:** Mobile readers stare at a blank screen 2s longer than desktop readers before anything paints, on the same page and same resources.
- **Framework tags:** Tier1-FCP, Tier1-TBT, Tier2-render-blocking
- **Flow:** measure:index:mobile
- **Locator:** https://fonts.example-cdn.test/all.css
- **Personas hit:** n/a
- **Observed:**
  - Two blocking stylesheets sit in `<head>` with no `async`/`defer`/`preload`: `https://fonts.example-cdn.test/all.css` (62,464 bytes, third-party) and `/style.css`.
  - Mobile FCP is 2,900ms ("needs improvement", 1.8–3.0s band); desktop FCP is 900ms ("good") for the identical render-blocking resources.
  - Mobile TBT is 410ms ("needs improvement", 200–600ms band); desktop TBT is 90ms ("good").
- **Evidence:** `measure/index-mobile.json` (tier1.fcp_ms, tier1.tbt_ms, tier2.render_blocking) · `measure/index-desktop.json` (tier1.fcp_ms, tier1.tbt_ms)
- **Repro:**
  1. Load `http://localhost:8765/` on mobile viewport, cold cache.
  2. Inspect network waterfall — both stylesheets block the head before first paint.
  3. Compare FCP/TBT to the desktop measurement of the same URL.
- **Fix:** Self-host or `preconnect`+`preload` the font stylesheet, and inline or defer non-critical CSS in `/style.css`.

### ea28917952ae — Static assets ship uncompressed and without cache-control headers
- **Severity:** P2
- **So what:** Every visit re-downloads the full, uncompressed CSS, HTML, and hero image — no browser can cache or shrink them on the wire.
- **Framework tags:** Tier2-compression, Tier2-cache-headers
- **Flow:** measure:index:mobile
- **Locator:** /style.css
- **Personas hit:** n/a
- **Observed:**
  - `/style.css` and the HTML document ship with no `content-encoding` (gzip/br) on both `/` and `/pricing.html`, mobile and desktop.
  - `/style.css` and `/assets/generated/hero.png` have no usable `cache-control` on the homepage; `/style.css` also lacks it on the pricing page.
  - Pricing page weight (5,200 bytes) is trivial, but the same missing headers apply there too — this is a site-wide server/CDN config gap, not a page-specific one.
- **Evidence:** `measure/index-mobile.json` (tier2.uncompressed_text_resources, tier2.missing_cache_headers) · `measure/pricing-mobile.json` (tier2.uncompressed_text_resources, tier2.missing_cache_headers) · `measure/index-desktop.json` · `measure/pricing-desktop.json`
- **Repro:**
  1. Load `/` and `/pricing.html`, inspect response headers for `content-encoding` and `cache-control` on `style.css`, the HTML document, and `hero.png`.
- **Fix:** Enable gzip/brotli for text responses and set `cache-control: max-age=31536000, immutable` (with content hashing) for static assets at the server/CDN.

### c5e84d2ee659 — Console error fires on every page load of the homepage
- **Severity:** P3
- **So what:** A script error on every homepage load is a hygiene signal worth cleaning up; no measured performance or functional consequence found this run.
- **Framework tags:** Tier3-console-errors
- **Flow:** measure:index:mobile
- **Locator:** nimbusBootstrap
- **Personas hit:** n/a
- **Observed:**
  - `ReferenceError: nimbusBootstrap is not defined` fires before `load` on `/`, on both mobile and desktop measurements.
  - Does not occur on `/pricing.html` in either viewport.
- **Evidence:** `measure/index-mobile.json` (tier3.console_errors_on_load) · `measure/index-desktop.json` (tier3.console_errors_on_load)
- **Repro:**
  1. Load `http://localhost:8765/` with devtools console open.
  2. Observe the `ReferenceError` before the `load` event.
- **Fix:** Find the script referencing `nimbusBootstrap` before it's defined (likely a missing script tag or load-order issue) and fix the ordering.

---

## Dropped for want of evidence
- None — all Tier1-3 fields in `measure/` were populated and `viewport_verified: true` for both pages measured.

## For other lenses
- `/features.html` returns HTTP 404 when navigated from the homepage — seen in the persona screenshot `04-features-404.png` and in `crawl/` data, which is out of this lens's `manifest.json` + `measure/` input scope. Flag for SEO/broken-link and bugs lenses.
- Third-party analytics script (`analytics.example-tracker.test/t.js`, 38,912 bytes) and its behavior — trust/privacy implications are for the trust lens, not weight (already reported in Weight table).

## Coverage gaps
- `/features.html`, `/about.html`, `/privacy.html` were crawled but never Tier1-3 measured — no `measure/*.json` exists for them, so no CWV/weight/hygiene claims can be made about those pages this run.
- Only one run (`runs: 1`) per page/viewport — no repeat-measurement variance data available.
- No throttled-network measurement — all numbers are unthrottled-connection lab numbers on this machine.

## Appendices
- A. Persona debriefs — n/a (no-persona lens)
- B. Session timelines — n/a (no-persona lens)
- C. Screenshot index — `measure/screenshots/index-mobile.png`, `measure/screenshots/index-desktop.png`, `measure/screenshots/pricing-mobile.png`, `measure/screenshots/pricing-desktop.png`
