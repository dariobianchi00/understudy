# Nimbus Notes — technical findings — Run 2026-09-08 (fixture01)

## Method
- Framework: Core Web Vitals (lab) → delivery causes → hygiene checklist
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (no persona lens; measurement-based)
- Scoring model: sonnet
- Conditions: all four measurements `viewport_verified: true`, cache cold, throttling none, runs 1
- Lab numbers: one machine, one connection, one moment. They describe the page, not users' experience.
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 72fb2e2f358e — 3.9 MB hero.png delivered at 3000×2000 and shown at 350×233 drives a 5.8 s mobile LCP
- **Severity:** P1
- **So what:** Mobile LCP is "poor" (5.8 s, limit 4.0 s) and the page weighs 4.1 MB, because of one image.
- **Framework tags:** Tier 1 LCP, Tier 2 image hygiene, Tier 2 page weight
- **Flow:** measure:index:mobile
- **Locator:** /assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - PNG, 3,900,000 B, natural 3000×2000, displayed 350×233 mobile / 600×400 desktop, not lazy; 95% of 4,104,000 B page weight.
  - Mobile LCP 5.8 s (poor); desktop LCP 2.1 s (good) — same bytes, so desktop flatters.
  - Cause named, not symptom: delivered pixel area is about 73× what mobile displays.
- **Evidence:** `measure/index-mobile.json` · `measure/index-desktop.json` · `measure/screenshots/index-mobile.png`
- **Repro:**
  1. Load `/` cold at 390×844, no throttling.
  2. Read `tier1.lcp_ms` and `tier2.images[0]`.
- **Fix:** Re-export hero as AVIF/WebP at ≤ 1200 px wide with `srcset` (350/700/1200), target under 150 KB.

### ee115b768572 — Third-party font stylesheet and style.css block first paint; mobile FCP is 2.9 s
- **Severity:** P2
- **So what:** Nothing paints until an external font host and the local stylesheet both arrive; mobile FCP is 2.9 s, in the needs-work band.
- **Framework tags:** Tier 1 FCP, Tier 2 render-blocking, Tier 2 third-party
- **Flow:** measure:index:mobile
- **Locator:** https://fonts.example-cdn.test/all.css
- **Personas hit:** n/a
- **Observed:**
  - Render-blocking: `fonts.example-cdn.test/all.css` (62,464 B) and `/style.css`.
  - Third-party total 101,376 B over 3 requests, 2 domains (fonts 62,464 B; `analytics.example-tracker.test/t.js` 38,912 B).
  - Mobile FCP 2.9 s vs desktop 0.9 s.
- **Evidence:** `measure/index-mobile.json` · `measure/index-desktop.json`
- **Repro:**
  1. Load `/` cold at 390×844.
  2. Read `tier2.render_blocking` and `tier2.third_party`.
- **Fix:** Self-host a subset of the fonts with `font-display: swap`; load the analytics script with `async`/`defer`.

### aee8477944fd — HTML and style.css are served without compression
- **Severity:** P2
- **So what:** Text is sent at full size on every visit, which slows first paint on slow connections.
- **Framework tags:** Tier 2 compression
- **Flow:** measure:index:desktop
- **Locator:** /style.css
- **Personas hit:** n/a
- **Observed:**
  - `/` and `/style.css` listed under `uncompressed_text_resources` on the home page.
  - `/pricing.html` and `/style.css` are also uncompressed — one finding, two pages.
  - Absolute cost is small (style.css 3,174 B); this is a server setting, not a page problem.
- **Evidence:** `measure/index-desktop.json` · `measure/pricing-desktop.json`
- **Repro:**
  1. Request `/style.css` with `Accept-Encoding: gzip, br`.
  2. Check for `content-encoding`.
- **Fix:** Enable gzip/brotli for text/html, text/css and JS at the web server or CDN.

### f804b163f2d2 — Static assets carry no cache-control header
- **Severity:** P2
- **So what:** Returning visitors re-download the 3.9 MB hero and the stylesheet instead of reusing them.
- **Framework tags:** Tier 2 cache headers
- **Flow:** measure:index:desktop
- **Locator:** cache-control:/style.css
- **Personas hit:** n/a
- **Observed:**
  - `missing_cache_headers`: `/style.css` and `/assets/generated/hero.png` on the home page.
  - `/style.css` also lacks it on `/pricing.html`.
  - Lab runs are cold-cache only; repeat-visit cost was not measured.
- **Evidence:** `measure/index-desktop.json` · `measure/pricing-desktop.json`
- **Repro:**
  1. Request `/style.css` and `/assets/generated/hero.png`.
  2. Check for `cache-control`.
- **Fix:** Send `Cache-Control: public, max-age=31536000, immutable` on fingerprinted assets; a short max-age on HTML.

### faf27b2bf49b — Mobile TBT is 410 ms on the home page
- **Severity:** P2
- **So what:** The page ignores input for 410 ms on mobile, in the needs-work band (limit 200 ms); desktop is 90 ms.
- **Framework tags:** Tier 1 TBT
- **Flow:** measure:index:mobile
- **Locator:** tbt:index-mobile
- **Personas hit:** n/a
- **Observed:**
  - Mobile TBT 410 ms; desktop 90 ms. TBT is a lab proxy, not INP.
  - Cause not identifiable from this data; no JS profiling was done.
  - Pricing page: 30 ms mobile, fine.
- **Evidence:** `measure/index-mobile.json` · `measure/index-desktop.json`
- **Repro:**
  1. Load `/` cold at 390×844.
  2. Read `tier1.tbt_ms`.
- **Fix:** Profile main-thread long tasks on `/` and defer or split the scripts responsible, starting with the analytics tag.

### a22d00fb396f — Load-time ReferenceError: nimbusBootstrap is not defined on the home page
- **Severity:** P3
- **So what:** A script error fires on every home-page load; hygiene signal, with unknown user effect.
- **Framework tags:** Tier 3 console errors on load
- **Flow:** measure:index:mobile
- **Locator:** console:nimbusBootstrap
- **Personas hit:** n/a
- **Observed:**
  - `ReferenceError: nimbusBootstrap is not defined` on both mobile and desktop loads.
  - Whether it breaks anything is for the bugs lens.
- **Evidence:** `measure/index-mobile.json` · `measure/index-desktop.json`
- **Repro:**
  1. Load `/` and watch the console before `load`.
- **Fix:** Define `nimbusBootstrap` before the script that calls it, or remove the call.

---

## Dropped for want of evidence
- None.

## For other lenses
- `ReferenceError` may break page behaviour — bugs.
- Pricing page is light (5,200 B) and fast; no finding.

## Coverage gaps
- Only `/` and `/pricing.html` measured; features, about, privacy not measured.
- One run per measurement; no variance observed or testable.
- Throttling none, so mobile numbers are optimistic for real mobile networks.
- No field data, no repeat-visit measurement.

## Appendices
- A. Persona debriefs
- B. Session timelines
- C. Screenshot index
