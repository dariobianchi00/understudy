# Nimbus Notes — technical findings — Run 2026-09-08 (fixture01)

## Method
- Framework: Tier 1 experience → Tier 2 delivery → Tier 3 hygiene (`technical-metrics.md`)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a (generic mode; no-persona lens)
- Scoring model: sonnet
- Lab measurements: one machine, one connection, one moment, cold cache, no throttling, 1 run. Not field data; not what users experience.
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### f2d93a6de83c — 3.9 MB 3000×2000 PNG hero shown at 350×233 drives 5.8 s mobile LCP
- **Severity:** P1
- **So what:** One image is 95% of a 4.10 MB page and a single asset over 1 MB; mobile LCP is 5.8 s (poor, >4.0 s).
- **Framework tags:** Tier1-LCP, Tier2-image-hygiene, Tier2-weight
- **Flow:** measure:index:mobile
- **Locator:** /assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - Delivered 3000×2000 PNG, 3,900,000 B, not lazy; displayed 350×233 mobile, 600×400 desktop.
  - Mobile LCP 5.8 s; desktop 2.1 s (good). Page weight 4,104,000 B on both viewports.
  - Pixels delivered are ~98% more than the mobile display needs (6.0 MP vs 0.08 MP).
- **Evidence:** `measure/index-mobile.json` · `measure/index-desktop.json` · `measure/screenshots/index-mobile.png`
- **Repro:**
  1. Load http://localhost:8765/ at 390×844, cold cache.
  2. Read `tier2.images` and `tier1.lcp_ms` in the measurement record.
- **Fix:** Re-export hero as WebP/AVIF at ~700 px wide with `srcset` (target <100 KB); stop serving the 3000 px PNG.

### 8896079a2e4e — Text resources served without compression on both measured pages
- **Severity:** P2
- **So what:** HTML and CSS travel at full size on every visit; avoidable bytes on every page.
- **Framework tags:** Tier2-compression
- **Flow:** measure:index:mobile
- **Locator:** /style.css
- **Personas hit:** n/a
- **Observed:**
  - No gzip/br on `/style.css` and `/` (landing); `/style.css` and `/pricing.html` (pricing).
  - style.css is 3,174 B — the saving is small; the missing setting is the finding.
- **Evidence:** `measure/index-mobile.json` · `measure/pricing-mobile.json` · `measure/pricing-desktop.json`
- **Repro:**
  1. Request each URL; inspect `content-encoding`.
- **Fix:** Enable brotli/gzip for text/html and text/css at the server or CDN.

### 65979ef84a5f — No cache-control on style.css or hero.png
- **Severity:** P2
- **So what:** Repeat visitors would re-download the 3.9 MB hero and the stylesheet.
- **Framework tags:** Tier2-cache-headers
- **Flow:** measure:index:mobile
- **Locator:** /assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - `missing_cache_headers`: `/style.css`, `/assets/generated/hero.png` (landing); `/style.css` (pricing).
  - Repeat visits not measured (cold cache only); consequence inferred from headers.
- **Evidence:** `measure/index-mobile.json` · `measure/pricing-mobile.json`
- **Repro:**
  1. Request each asset; inspect `cache-control`.
- **Fix:** Send `cache-control: public, max-age=31536000, immutable` on versioned static assets.

### ab1751cee28d — Third-party font stylesheet blocks render, FCP 2.9 s on mobile
- **Severity:** P2
- **So what:** Nothing paints until an external CSS file on another domain arrives; mobile FCP is 2.9 s (needs improvement).
- **Framework tags:** Tier1-FCP, Tier2-render-blocking, Tier2-third-party
- **Flow:** measure:index:mobile
- **Locator:** https://fonts.example-cdn.test/all.css
- **Personas hit:** n/a
- **Observed:**
  - Render-blocking in head: `https://fonts.example-cdn.test/all.css` (62,464 B) and `/style.css`.
  - FCP 2.9 s mobile vs 0.9 s desktop; pricing, with only `/style.css`, is 0.8 s mobile.
- **Evidence:** `measure/index-mobile.json` · `measure/pricing-mobile.json`
- **Repro:**
  1. Read `tier2.render_blocking` and `tier1.fcp_ms` for both pages.
- **Fix:** Self-host a subset of the fonts with `font-display: swap`, or load the stylesheet non-blocking with `preconnect`.

### 18d475ca6749 — Mobile TBT of 410 ms on the landing page sits in needs-improvement
- **Severity:** P2
- **So what:** The page ignored input for a measured 410 ms in the lab, over the 200 ms good threshold.
- **Framework tags:** Tier1-TBT
- **Flow:** measure:index:mobile
- **Locator:** tbt_ms
- **Personas hit:** n/a
- **Observed:**
  - TBT 410 ms mobile (200–600 ms band); 90 ms desktop; pricing 30 ms / 10 ms.
  - TBT is a lab proxy, not INP; cause not profiled (no JS profiling in this capture).
- **Evidence:** `measure/index-mobile.json` · `measure/index-desktop.json`
- **Repro:**
  1. Read `tier1.tbt_ms` in both landing-page records.
- **Fix:** Profile the landing page under mobile CPU conditions; defer the analytics tag and any non-critical script.

### 27eafd5ee7d9 — Landing page throws ReferenceError on load
- **Severity:** P3
- **So what:** A script error before `load` is a hygiene signal and may mean a bootstrap script never ran.
- **Framework tags:** Tier3-console-errors
- **Flow:** measure:index:mobile
- **Locator:** nimbusBootstrap
- **Personas hit:** n/a
- **Observed:**
  - `ReferenceError: nimbusBootstrap is not defined` on both viewports.
  - Pricing page: no console errors on load.
- **Evidence:** `measure/index-mobile.json` · `persona-sceptic/console-full.txt:1`
  > "Uncaught ReferenceError: nimbusBootstrap is not defined"
- **Repro:**
  1. Open the landing page with the console open.
- **Fix:** Define `nimbusBootstrap` or remove the call at `index.html:9`.

### b28fe2642c8e — Third-party tags add 101 KB across 2 domains to the landing page
- **Severity:** P3
- **So what:** Third-party code the owner does not control is 2.5% of weight; small, but includes a tracker.
- **Framework tags:** Tier2-third-party
- **Flow:** measure:index:mobile
- **Locator:** analytics.example-tracker.test/t.js
- **Personas hit:** n/a
- **Observed:**
  - `fonts.example-cdn.test` 62,464 B; `analytics.example-tracker.test` 38,912 B; 3 requests.
  - Pricing page: zero third-party requests.
- **Evidence:** `measure/index-mobile.json` · `measure/index-desktop.json`
- **Repro:**
  1. Read `tier2.third_party` in the record.
- **Fix:** Audit the tracker; load it `async`/`defer` after the primary content.

---

## Dropped for want of evidence
- None.

## For other lenses
- Privacy page and cookie bar disagree (debriefs) — trust lens.

## Coverage gaps
- /features, /about, /privacy not measured; no repeat-visit, throttled or field data.
- Each page measured once, so variance is unknown.

## Appendices
- A. Persona debriefs
- B. Session timelines
- C. Screenshot index: `measure/screenshots/`
