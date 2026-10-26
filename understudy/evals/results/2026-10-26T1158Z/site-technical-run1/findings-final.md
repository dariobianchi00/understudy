# Nimbus Notes — technical findings — Run 2026-09-08 (fixture01)

## Method
- Framework: Core Web Vitals (lab) + delivery + hygiene, per `technical-metrics.md`
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (this lens uses none)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Conditions: all four measurements `viewport_verified: true`, cold cache, no throttling, 1 run, 2026-09-08 09:30 UTC
- ⚑ Lab numbers: one machine, one connection, one moment. They describe the page, not your users.

---

## Findings

### e3c5f6ae21cf — 3.9 MB hero.png (3000×2000 shown at 350×233) drives a 5.8 s mobile LCP and a 4.1 MB page
- **Severity:** P1
- **So what:** One image is 95% of a 4.1 MB home page and pushes mobile LCP into "poor" (5.8 s vs 4.0 s threshold).
- **Framework tags:** Tier 1 LCP, Tier 2 image hygiene, page weight
- **Flow:** measure:index:mobile
- **Locator:** /assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - PNG, 3,900,000 bytes, delivered 3000×2000, displayed 350×233 mobile / 600×400 desktop; `lazy: false`.
  - Mobile lab LCP 5800 ms, FCP 2900 ms; desktop LCP 2100 ms. Page weight 4,104,000 bytes, 9 requests.
  - Delivered pixels are ~73× the mobile display area (6.0 M vs 81.5 k px).
- **Evidence:** `measure/index-mobile.json` (tier1, tier2.images) · `measure/index-desktop.json` · `measure/screenshots/index-mobile.png`
- **Repro:**
  1. Load `http://localhost:8765/` at 390×844, cold cache.
  2. Read the largest asset and LCP in the resource log.
- **Fix:** Export hero at ≤800 px wide as AVIF/WebP with `srcset`; target under 150 KB. Keep it eager (it is the LCP element), not lazy.

### d8065dc20cf8 — HTML and style.css are served uncompressed on the home and pricing pages
- **Severity:** P2
- **So what:** Text is sent at full size on every first visit; small here, but a one-line server setting.
- **Framework tags:** Tier 2 compression
- **Flow:** measure:index:mobile
- **Locator:** /style.css
- **Personas hit:** n/a
- **Observed:**
  - Uncompressed on `/` and `/style.css` (home, mobile and desktop).
  - Uncompressed on `/pricing.html` and `/style.css` (pricing, mobile and desktop); style.css is 3,174 bytes.
- **Evidence:** `measure/index-mobile.json` (tier2.uncompressed_text_resources) · `measure/pricing-mobile.json` · `measure/pricing-desktop.json`
- **Repro:**
  1. Request `/style.css` and `/pricing.html`.
  2. Check for a `content-encoding` header; none gzip/br.
- **Fix:** Enable gzip or brotli for text/html, text/css and application/javascript on the web server or CDN.

### 8fd5c8a4b400 — No cache-control on style.css or hero.png, so every visit re-downloads 3.9 MB
- **Severity:** P2
- **So what:** Returning visitors pay the full 4 MB again; no repeat visit was measured, so the size of the effect is unknown.
- **Framework tags:** Tier 2 cache headers
- **Flow:** measure:index:mobile
- **Locator:** cache-control:/style.css,/assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - `missing_cache_headers`: `/style.css` and `/assets/generated/hero.png` on the home page.
  - `/style.css` also lacks cache headers on `/pricing.html`.
- **Evidence:** `measure/index-mobile.json` (tier2.missing_cache_headers) · `measure/pricing-mobile.json`
- **Repro:**
  1. Request each static asset.
  2. Inspect response headers for `cache-control`.
- **Fix:** Send `Cache-Control: public, max-age=31536000, immutable` on fingerprinted assets; a shorter max-age on style.css until it is fingerprinted.

### 52ccd315c000 — Render-blocking third-party font CSS sits ahead of first paint (mobile FCP 2.9 s)
- **Severity:** P2
- **So what:** Mobile FCP is 2.9 s, just under the 3.0 s poor line; a cross-origin stylesheet must arrive before anything paints.
- **Framework tags:** Tier 1 FCP/TBT, Tier 2 render-blocking, third-party
- **Flow:** measure:index:mobile
- **Locator:** https://fonts.example-cdn.test/all.css
- **Personas hit:** n/a
- **Observed:**
  - Render-blocking: `https://fonts.example-cdn.test/all.css` (62,464 bytes) and `/style.css`.
  - Third-party total 101,376 bytes, 3 requests, 2 domains (fonts 62,464; analytics.example-tracker.test 38,912). First-party is the remaining ~4.0 MB.
  - Mobile TBT 410 ms ("needs improvement", ≤600 ms); desktop TBT 90 ms. Cause not isolated — no JS profiling.
- **Evidence:** `measure/index-mobile.json` (tier1, tier2.render_blocking, tier2.third_party)
- **Repro:**
  1. Load `/` at 390×844 cold.
  2. List `<head>` stylesheets and scripts without async/defer.
- **Fix:** Self-host the font subset with `font-display: swap`, preload it, and load analytics `t.js` with `defer`.

### bad8c77f65cc — Home page throws "ReferenceError: nimbusBootstrap is not defined" on load
- **Severity:** P3
- **So what:** A script runs against a missing dependency on the front door; a hygiene signal, with no measured effect here.
- **Framework tags:** Tier 3 console errors on load
- **Flow:** measure:index:mobile
- **Locator:** ReferenceError: nimbusBootstrap is not defined
- **Personas hit:** n/a
- **Observed:**
  - Error present on load in both mobile and desktop measurements of `/`.
  - Pricing page: no console errors on load.
- **Evidence:** `measure/index-mobile.json` (tier3.console_errors_on_load) · `measure/index-desktop.json`
- **Repro:**
  1. Open `/` with the console attached before load.
- **Fix:** Load the script that defines `nimbusBootstrap` before its caller, or remove the call. Triage as a bug in the bugs lens.

---

## Dropped for want of evidence
- None.

## For other lenses
- Pricing page is 5.2 KB and fast (mobile LCP 1.4 s); no performance barrier to the cost-without-email objective — conversion.

## Coverage gaps
- Only `/` and `/pricing.html` measured; features, about, privacy not measured.
- Each page measured once; no variance observed. No repeat-visit, throttled or field data.
- Measurement records `https: true` and `hsts: true` for an `http://localhost` URL; Tier 3 transport checks not independently verified.

## Appendices
- A. Persona debriefs — not used by this lens
- B. Session timelines — not used by this lens
- C. Screenshots: `measure/screenshots/index-mobile.png`, `index-desktop.png`, `pricing-mobile.png`, `pricing-desktop.png`
