# Nimbus Notes — technical findings — Run 2026-09-08 (fixture01)

## Method
- Framework: technical-metrics.md — Tier 1 Core Web Vitals, Tier 2 delivery, Tier 3 hygiene
- Pass 1 naive capture (Mode B measure) → Pass 2 analyst scoring
- Personas: n/a — no-persona lens
- Scoring model: sonnet
- Lab measurements only: one machine, one connection, one moment, cold cache, no throttling. Not a description of real-user experience.
- Every finding cites a measurement record; unsupported observations dropped, listed at the end

---

## Findings

### 0840e5acc421 — Oversized hero image drives poor mobile LCP and 4 MB page weight
- **Severity:** P1
- **So what:** Every mobile visitor downloads a 3.9 MB image to display a 350×233 box, pushing LCP to 5.8 s — into the "poor" band.
- **Framework tags:** Tier 1 (LCP), Tier 2 (page weight, image hygiene)
- **Flow:** measure:index:mobile
- **Locator:** /assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - hero.png is 3000×2000 natural, delivered at 3,900,000 bytes; displayed at 600×400 on desktop and 350×233 on mobile.
  - Mobile LCP measures 5,800 ms (poor, threshold >4,000 ms); desktop LCP measures 2,100 ms (good) on the same asset over a faster viewport pipeline.
  - Total page weight is 4,104,000 bytes on both viewports; the hero image alone accounts for 95% of it.
- **Evidence:** `measure/index-mobile.json:tier1.lcp_ms,tier2.images[0]` · `measure/index-desktop.json:tier1.lcp_ms,tier2.images[0]` · `measure/screenshots/index-mobile.png`
- **Repro:**
  1. Load http://localhost:8765/ on a 390×844 viewport with a cold cache.
  2. Observe LCP candidate is the hero image; time to largest paint is 5.8 s.
- **Fix:** Serve hero.png as a responsive, compressed asset (WebP/AVIF) sized to its largest displayed breakpoint (~600×400), targeting well under 200 KB.

### 544296040ad5 — Render-blocking stylesheets delay first paint and inflate TBT on mobile
- **Severity:** P2
- **So what:** Mobile visitors wait 2.9 s before anything paints and the page ignores input for 410 ms while two blocking stylesheets load.
- **Framework tags:** Tier 1 (FCP, TBT), Tier 2 (render-blocking)
- **Flow:** measure:index:mobile
- **Locator:** /style.css
- **Personas hit:** n/a
- **Observed:**
  - `render_blocking` lists `https://fonts.example-cdn.test/all.css` (62,464 bytes) and `http://localhost:8765/style.css`, both loaded before first paint.
  - Mobile FCP is 2,900 ms and TBT is 410 ms — both "needs improvement" (thresholds: FCP ≤3,000 ms, TBT ≤600 ms for that band).
  - Desktop FCP is 900 ms and TBT is 90 ms on the identical resource set — the same blocking chain costs far less on a faster device profile.
- **Evidence:** `measure/index-mobile.json:tier1.fcp_ms,tier1.tbt_ms,tier2.render_blocking` · `measure/index-desktop.json:tier1.fcp_ms,tier1.tbt_ms`
- **Repro:**
  1. Load http://localhost:8765/ on a 390×844 viewport with a cold cache.
  2. Observe two render-blocking stylesheets ahead of first paint; FCP lands at 2.9 s.
- **Fix:** Inline critical CSS, defer the webfont stylesheet with `media="print" onload`, and self-host or preload the font file.

### 1351b66c070a — Static assets ship without compression or cache headers
- **Severity:** P2
- **So what:** Every visit re-downloads style.css and the homepage HTML in full, and static assets carry no cache-control for repeat views.
- **Framework tags:** Tier 2 (compression, cache headers)
- **Flow:** measure:index:mobile
- **Locator:** /style.css
- **Personas hit:** n/a
- **Observed:**
  - `uncompressed_text_resources` lists `http://localhost:8765/style.css` and `http://localhost:8765/` — no content-encoding on either.
  - `missing_cache_headers` lists `http://localhost:8765/style.css` and `http://localhost:8765/assets/generated/hero.png`.
  - Same result on both mobile and desktop measurements of the homepage.
- **Evidence:** `measure/index-mobile.json:tier2.uncompressed_text_resources,tier2.missing_cache_headers` · `measure/index-desktop.json:tier2.uncompressed_text_resources,tier2.missing_cache_headers`
- **Repro:**
  1. Request http://localhost:8765/style.css and http://localhost:8765/.
  2. Inspect response headers: no `content-encoding`, no `cache-control` on style.css or hero.png.
- **Fix:** Enable gzip/br on the web server for text responses, and set `cache-control: max-age` (with a hashed filename) on style.css and hero.png.

### cb51a1352729 — Uncaught ReferenceError fires on every load of the homepage
- **Severity:** P3
- **So what:** A JavaScript error before load completes is a hygiene signal worth fixing even though it did not block rendering in this measurement.
- **Framework tags:** Tier 3 (console errors on load)
- **Flow:** measure:index:mobile
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `console_errors_on_load` records `ReferenceError: nimbusBootstrap is not defined` on both mobile and desktop measurements of the homepage.
  - Pricing page has zero console errors on load.
- **Evidence:** `measure/index-mobile.json:tier3.console_errors_on_load` · `measure/index-desktop.json:tier3.console_errors_on_load`
  > "ReferenceError: nimbusBootstrap is not defined"
- **Repro:**
  1. Load http://localhost:8765/ with devtools console open.
  2. Observe the ReferenceError logged before the load event.
- **Fix:** Define or remove the `nimbusBootstrap` reference so the homepage loads without a console error.

---

## Dropped for want of evidence
- None.

## For other lenses
- `ReferenceError: nimbusBootstrap is not defined` is a console error, not scored further here — flag for the `bugs` lens if in scope.

## Coverage gaps
- Only two pages measured (homepage, pricing); no other site pages captured in this run.
- Single run per page/viewport (`runs: 1`) — no repeat-measurement variance data.

## Appendices
- A. Persona debriefs — n/a, no-persona lens.
- B. Session timelines — n/a, Mode B measurement has no session log.
- C. Screenshot index — `measure/screenshots/index-mobile.png`, `measure/screenshots/index-desktop.png`, `measure/screenshots/pricing-mobile.png`, `measure/screenshots/pricing-desktop.png`.
