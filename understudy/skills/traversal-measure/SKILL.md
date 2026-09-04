---
name: traversal-measure
description: Mode B capture. Measures page performance and delivery hygiene with no persona and no session — Core Web Vitals, page weight, image hygiene, compression, cache headers, third-party weight, and security hygiene, on mobile and desktop separately. Produces lab measurements only; it never scores or diagnoses. Use when running the capture half of a technical objective.
---

# Traversal — Mode B measurement

**No persona. No session.** A scripted measurement of what the page costs to load.

## Load before starting

- `${CLAUDE_PLUGIN_ROOT}/references/technical-metrics.md` — the metric set and how to obtain each
- `${CLAUDE_PLUGIN_ROOT}/references/playwright-patterns.md` — driving the browser
- `${CLAUDE_PLUGIN_ROOT}/references/evidence-rules.md` — what capture owes scoring

## ⚑ Before you measure anything

These numbers are **lab measurements** — one machine, one connection, one moment. They are sound evidence about the page and no evidence at all about what users experience.

Your job at capture time is to **record the conditions alongside every number**, so the lens cannot present them as field data even by accident. A number without its conditions is not reproducible, and an unreproducible number is not evidence.

---

## Run order

### 1. Pick the pages

Default: the entry URL. Add any page the target names, and — if a Mode C crawl already ran — the pages the site itself links most prominently.

**Cap at 5 pages.** Measuring twenty pages badly is worse than five well, and the report becomes a spreadsheet nobody reads.

### 2. Per page, per viewport — mobile AND desktop, separately

```
→ measure — <url> @ <mobile 390×844 | desktop 1440×900>, cold cache
```

**The discipline, in order. Skipping a step silently invalidates the number:**

1. **Fresh browser context.** A warm cache measures your second visit, not a visitor's first.
2. Set the viewport and **verify it** with `browser_evaluate`.
3. Install the observers **before navigating** — LCP and layout-shift entries emitted before the observer exists are lost, and the number will be quietly wrong rather than obviously missing.
4. Navigate.
5. Wait for `load`, then a short quiet period so LCP settles.
6. Read everything in one evaluation.

```js
// installed BEFORE navigation
window.__u = { lcp: 0, cls: 0, tbt: 0, longtasks: [] };
new PerformanceObserver(l => { const e = l.getEntries(); window.__u.lcp = e[e.length-1].startTime; })
  .observe({ type: 'largest-contentful-paint', buffered: true });
new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__u.cls += e.value; })
  .observe({ type: 'layout-shift', buffered: true });
new PerformanceObserver(l => { for (const e of l.getEntries()) window.__u.longtasks.push([e.startTime, e.duration]); })
  .observe({ type: 'longtask', buffered: true });
```

Then read Tier 1, Tier 2 and Tier 3 per `technical-metrics.md`.

### 3. Record

`measure/<page-slug>-<viewport>.json`:

```json
{
  "url": "", "viewport": {"width": 0, "height": 0}, "viewport_verified": true,
  "measured_utc": "", "cache": "cold", "throttling": "none",
  "runs": 1,
  "tier1": {"lcp_ms": 0, "cls": 0, "tbt_ms": 0, "fcp_ms": 0, "ttfb_ms": 0},
  "tier2": {
    "page_weight_bytes": 0, "request_count": 0,
    "largest_assets": [{"url": "", "type": "", "bytes": 0}],
    "images": [{"url": "", "format": "", "bytes": 0,
                "natural": [0,0], "displayed": [0,0], "lazy": false}],
    "uncompressed_text_resources": [],
    "missing_cache_headers": [],
    "render_blocking": [],
    "third_party": {"domains": 0, "requests": 0, "bytes": 0, "by_domain": {}}
  },
  "tier3": {
    "https": true, "hsts": false, "mixed_content": [],
    "viewport_meta": true, "redirect_chain": [],
    "asset_404s": [], "console_errors_on_load": []
  }
}
```

**`viewport_verified` is not decoration.** A device-specific measurement taken at the wrong viewport is worse than no measurement — it looks authoritative and describes a page nobody saw.

### 4. Screenshot each measured page at each viewport

Evidence that the numbers describe the page you think they do. Move them into the run folder immediately.

### 5. Verify

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/check_capture.py <run_folder>
```

---

## Things that go wrong

| Situation | Do |
|---|---|
| LCP reads 0 | The observer was installed after the entry fired. Re-measure with a fresh context — do not report 0. |
| Numbers differ a lot between two runs | **Report both, or report the worse one, and say you measured twice.** Never re-run until a nicer number appears; that is fabricating data. |
| A cookie banner covers the page | Measure as loaded — that is what a visitor gets. Note the banner; a banner that delays LCP *is* the LCP. |
| The page never settles (polling, animation) | Record what you have at a fixed cut-off and say the page never went quiet. That is itself a finding. |
| A third party is slow today | Record it. Note that third-party timing varies by the hour — one measurement cannot separate "slow vendor" from "slow afternoon". |
| Redirects to a different domain | Measure where you land, record the chain, say so plainly. |

---

## What you do not do

- **Do not score or diagnose.** Record `lcp_ms: 4820`. Do not write "LCP is poor" — the lens judges.
- **Do not average across pages or viewports.** A mean hides the page that is broken.
- **Do not throttle silently.** If throttling is applied, it goes in `throttling`.
- **Do not measure with a warm cache** and call it a first visit.
- **Do not present any of this as user experience.** You measured a machine.
