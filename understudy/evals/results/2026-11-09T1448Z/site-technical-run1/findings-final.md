# Nimbus Notes — technical findings — Run 2026-09-08 (fixture01)

## Method
- Framework: Core Web Vitals (Tier 1) explained by delivery (Tier 2), then hygiene checklist (Tier 3)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (not used by this lens)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- ⚠ Lab measurements: one machine, one connection, one moment, cold cache, no throttling, 1 run. They describe the page, not your users.

---

## Findings

### 86c7f63a1269 — 3.9 MB hero PNG delivered at 3000×2000 and shown at 350×233 drives a 5.8 s mobile LCP
- **Severity:** P1
- **So what:** A single asset of 3.9 MB makes up 95% of a 4.1 MB page, and mobile LCP is poor in the lab.
- **Framework tags:** Tier 1 LCP, Tier 2 image hygiene, Tier 2 page weight
- **Flow:** measure:index:mobile
- **Locator:** /assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - Delivered 3000×2000 PNG, 3,900,000 B; displayed 350×233 on mobile (1.4% of pixels), 600×400 on desktop (4%). Not lazy.
  - Mobile LCP 5.8 s (poor, >4.0 s), FCP 2.9 s; desktop LCP 2.1 s. Page weight 4,104,000 B.
  - Same asset on both viewports; the mobile number is the one to act on.
- **Evidence:** `measure/index-mobile.json` (tier1, tier2.images) · `measure/index-desktop.json` · `measure/screenshots/index-mobile.png`
- **Repro:**
  1. Load http://localhost:8765/ at 390×844, cold cache, no throttling.
  2. Read largest asset and LCP from the resource log.
- **Fix:** Re-export hero.png as WebP/AVIF at ~700×467 (2× the mobile display), with a 1200px srcset variant for desktop, target under 150 KB.

### 0a8a9f567fa7 — Text responses are served uncompressed and static assets carry no cache headers
- **Severity:** P2
- **So what:** Every visit re-downloads CSS and the hero at full size; HTML and CSS go over the wire uncompressed.
- **Framework tags:** Tier 2 compression, Tier 2 cache headers
- **Flow:** measure:index:mobile
- **Locator:** /style.css
- **Personas hit:** n/a
- **Observed:**
  - No gzip/br on `/` and `/style.css` (both pages); pricing.html also uncompressed.
  - No cache-control on `/style.css` (both pages) and `/assets/generated/hero.png`.
  - Absolute savings on text are small (style.css 3,174 B); the cache gap on hero.png is the costly part.
- **Evidence:** `measure/index-mobile.json` (tier2.uncompressed_text_resources, missing_cache_headers) · `measure/pricing-mobile.json` · `measure/pricing-desktop.json`
- **Repro:**
  1. Request `/` and `/style.css`; inspect `content-encoding` and `cache-control`.
- **Fix:** Enable gzip/brotli for text types, and send `cache-control: public, max-age=31536000, immutable` on fingerprinted CSS and images.

### 62e5f9127f58 — Third-party font stylesheet blocks first paint alongside style.css
- **Severity:** P2
- **So what:** First paint waits on a request to another domain, and mobile FCP reaches 2.9 s.
- **Framework tags:** Tier 2 render-blocking, Tier 2 third-party weight
- **Flow:** measure:index:mobile
- **Locator:** https://fonts.example-cdn.test/all.css
- **Personas hit:** n/a
- **Observed:**
  - Render-blocking: `fonts.example-cdn.test/all.css` (62,464 B) and `/style.css`, on the landing page.
  - Third-party total 101,376 B across 2 domains, 3 requests; the other is `analytics.example-tracker.test/t.js` (38,912 B).
  - Mobile TBT 410 ms (needs improvement, ≤600 ms); desktop 90 ms. Cause not isolated; no profiling in this method.
- **Evidence:** `measure/index-mobile.json` (tier2.render_blocking, third_party) · `measure/index-desktop.json`
- **Repro:**
  1. Load `/` cold; list head stylesheets and scripts without async/defer.
- **Fix:** Self-host the needed font subset, use `font-display: swap`, and load the analytics script with `defer`.

### f1736542f0a4 — Load-time ReferenceError: nimbusBootstrap is not defined
- **Severity:** P3
- **So what:** A script error fires on every landing-page load, a hygiene signal for what else on the page may not initialise.
- **Framework tags:** Tier 3 console errors on load
- **Flow:** measure:index:mobile
- **Locator:** console:nimbusBootstrap
- **Personas hit:** n/a
- **Observed:**
  - "ReferenceError: nimbusBootstrap is not defined" before load on `/`, mobile and desktop.
  - No error on pricing.html. Functional impact is for the bugs lens.
- **Evidence:** `measure/index-mobile.json` (tier3.console_errors_on_load) · `measure/index-desktop.json`
- **Repro:**
  1. Open http://localhost:8765/ with the console open.
- **Fix:** Define `nimbusBootstrap` before it is called, or remove the call if the script is no longer shipped.

---

## Passed
- HTTPS yes, HSTS present, no mixed content, viewport meta present, no redirects, no asset 404s — all four measurements.
- CLS ≤ 0.04 everywhere; TTFB ≤ 120 ms everywhere.
- pricing.html: 5.2 KB, 3 requests, no third parties, all Tier 1 good on both viewports.

## Dropped for want of evidence
- None.

## For other lenses
- Features page returned a 404 in the evaluator session — bugs.

## Coverage gaps
- Features, about and privacy pages not measured; no repeat-visit or throttled run; each measurement ran once.

## Appendices
- A. Persona debriefs — not used by this lens
- B. Session timelines — not used by this lens
- C. Screenshot index — `measure/screenshots/`
