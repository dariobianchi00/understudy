# Nimbus Notes — technical findings — Run 2026-09-08 (fixture01)

## Method
- Framework: technical-metrics.md — Tier 1 Core Web Vitals, Tier 2 delivery, Tier 3 hygiene
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — no-persona lens, measurements only
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Conditions verified before use: `viewport_verified: true`, `cache: cold`, `throttling: none`, `runs: 1` on all four measurements

---

## Findings

### a7380f84647c — Homepage hero image ships at 10x display size, driving poor mobile LCP
- **Severity:** P1
- **So what:** Mobile visitors wait 5.8 s to see the page's main content — past Google's "poor" line — before the homepage even finishes drawing.
- **Framework tags:** Tier 1 (LCP), Tier 2 (image hygiene)
- **Flow:** measure:index:mobile
- **Locator:** http://localhost:8765/assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - Mobile LCP 5.8 s (poor, threshold >4.0 s); desktop LCP 2.1 s (good) on the same page
  - `hero.png` delivered at 3000×2000 px, 3.9 MB, `content-encoding` absent
  - Displayed at 350×233 (mobile) / 600×400 (desktop) — under 5% and 8% of delivered pixels respectively
- **Evidence:** `measure/index-mobile.json` (tier1.lcp_ms, tier2.images[0]) · `measure/index-desktop.json` (tier1.lcp_ms, tier2.images[0]) · `measure/screenshots/index-mobile.png`
- **Repro:**
  1. Load `http://localhost:8765/` on a 390×844 viewport with a cold cache.
  2. Observe `largest-contentful-paint` timing and the network transfer size of `assets/generated/hero.png`.
- **Fix:** Resize and re-encode the hero image to roughly its largest displayed size (≈600×400) and serve responsive/WebP variants; target under 150 KB.

### d8397cf82e99 — Render-blocking stylesheets delay first paint on homepage and pricing
- **Severity:** P2
- **So what:** Every page waits on two stylesheet round-trips, one to a third-party font CDN, before anything can be painted.
- **Framework tags:** Tier 2 (render-blocking)
- **Flow:** measure:index:mobile
- **Locator:** https://fonts.example-cdn.test/all.css
- **Personas hit:** n/a
- **Observed:**
  - Homepage `render_blocking` lists `fonts.example-cdn.test/all.css` (62 KB, third-party) and `style.css`
  - Pricing page `render_blocking` lists `style.css` only
  - Homepage mobile FCP is 2.9 s (needs improvement); pricing mobile FCP is 0.8 s (good) with only the local stylesheet blocking
- **Evidence:** `measure/index-mobile.json` (tier2.render_blocking, tier1.fcp_ms) · `measure/pricing-mobile.json` (tier2.render_blocking, tier1.fcp_ms)
- **Repro:**
  1. Load `http://localhost:8765/` and `http://localhost:8765/pricing.html`.
  2. Inspect `<head>` for stylesheet `<link>` tags without `media` gating and confirm they precede first paint in the network log.
- **Fix:** Self-host or preload the font stylesheet, and inline or defer non-critical CSS so first paint does not wait on a cross-origin fetch.

### c17c4e90fa1b — Text responses served without compression across the site
- **Severity:** P2
- **So what:** Every HTML and CSS response is sent uncompressed, adding avoidable transfer time on every visit to every page.
- **Framework tags:** Tier 2 (compression)
- **Flow:** measure:index:mobile
- **Locator:** http://localhost:8765/style.css
- **Personas hit:** n/a
- **Observed:**
  - Homepage `uncompressed_text_resources`: `style.css` and `/` (the document itself)
  - Pricing `uncompressed_text_resources`: `style.css` and `pricing.html`
  - No `content-encoding` (gzip/br) present on any first-party text response measured
- **Evidence:** `measure/index-mobile.json` (tier2.uncompressed_text_resources) · `measure/pricing-mobile.json` (tier2.uncompressed_text_resources)
- **Repro:**
  1. Request `/`, `/pricing.html`, and `/style.css` and inspect response headers.
  2. Confirm no `content-encoding: gzip` or `br` header is present.
- **Fix:** Enable gzip or Brotli compression for HTML and CSS at the web server or CDN layer.

### 098eb9534f71 — Static assets missing cache-control headers
- **Severity:** P2
- **So what:** Repeat visits re-download the same stylesheet and hero image instead of reading them from cache, on every page.
- **Framework tags:** Tier 2 (cache headers)
- **Flow:** measure:index:mobile
- **Locator:** http://localhost:8765/style.css
- **Personas hit:** n/a
- **Observed:**
  - Homepage `missing_cache_headers`: `style.css`, `assets/generated/hero.png`
  - Pricing `missing_cache_headers`: `style.css`
  - No `cache-control` header recorded on either static asset in any of the four measurements
- **Evidence:** `measure/index-mobile.json` (tier2.missing_cache_headers) · `measure/pricing-mobile.json` (tier2.missing_cache_headers)
- **Repro:**
  1. Request `/style.css` and `/assets/generated/hero.png`.
  2. Inspect response headers for `cache-control`.
- **Fix:** Add long-lived `cache-control` headers (with content hashing or versioned filenames) to static CSS and image assets.

### b865754fa445 — Homepage throws a ReferenceError on load
- **Severity:** P3
- **So what:** A broken script reference on every homepage load is a hygiene signal, even though it did not visibly block rendering in this measurement.
- **Framework tags:** Tier 3 (console errors on load)
- **Flow:** measure:index:mobile
- **Locator:** console:nimbusBootstrap
- **Personas hit:** n/a
- **Observed:**
  - `console_errors_on_load: ["ReferenceError: nimbusBootstrap is not defined"]` recorded on both homepage mobile and desktop measurements
  - Not present on either pricing measurement
- **Evidence:** `measure/index-mobile.json` (tier3.console_errors_on_load) · `measure/index-desktop.json` (tier3.console_errors_on_load)
- **Repro:**
  1. Load `http://localhost:8765/` with devtools console open.
  2. Observe the `ReferenceError: nimbusBootstrap is not defined` thrown before `load`.
- **Fix:** Find the script expecting `nimbusBootstrap` and either define it or remove the dangling reference.

---

## Dropped for want of evidence
None — every Tier 1/2/3 observation used here traces to a field in one of the four measurement JSON files.

## For other lenses
- `ReferenceError: nimbusBootstrap is not defined` is a console error, not assessed here as a functional bug — see `bugs` lens if in scope.

## Coverage gaps
- Only two pages measured (`/`, `/pricing.html`); no other site surfaces were captured under Mode B.
- No throttled ("real-world" 4G/3G) measurement was taken — all numbers are unthrottled, this machine's connection.
- No repeat-visit (warm cache) measurement — cold cache only, per methodology.

## Appendices
- A. Persona debriefs — n/a, no-persona lens
- B. Session timelines — n/a, measurement snapshots only (see `measure/*.json`)
- C. Screenshot index — `measure/screenshots/index-mobile.png`, `measure/screenshots/index-desktop.png`, `measure/screenshots/pricing-mobile.png`, `measure/screenshots/pricing-desktop.png`
