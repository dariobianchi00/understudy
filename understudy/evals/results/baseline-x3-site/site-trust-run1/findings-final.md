# Nimbus Notes — trust findings — Run 2026-09-08 (fixture01)

## Method
- Framework: the four trust questions — is this real · what does it cost · who is behind it · what happens to my data — scored on the persona's own reactions and debrief Q5
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (evaluator on desktop 1440×900, sceptic on iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Only what the persona could verify from the site is reported; nothing was checked outside the capture. This is not a compliance review.

---

## Findings

### 2d00b724d8c5 — Cookie bar promises "no tracking cookies" while a third-party analytics beacon fires and the privacy page says cookies are used
- **Severity:** P0
- **So what:** Both visitors read the contradiction as the site being caught out, and it cancelled the trust the About page had just built.
- **Framework tags:** data-handling, consistency
- **Flow:** V3
- **Locator:** /privacy.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Landing bar reads "We use no tracking cookies on this site." — dismissed by both personas before reading anything else
  - Privacy page reads "We use cookies and similar technologies." and "We may share information with partners and service providers."
  - On page load, before the bar is dismissed, `https://analytics.example-tracker.test/t.js` loads and `POST …/collect?uid=8f3a…` (evaluator) / `uid=2c91…` (sceptic) returns 204
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/06-privacy.png` · `persona-sceptic/screenshots/01-privacy.png` · `persona-evaluator/network-full.txt:4-5` · `persona-sceptic/network-full.txt:2-3` · `crawl/html/1-index.html:3,37` · `persona-evaluator/session.log:27` · `persona-sceptic/session.log:10`
  > "The cookie bar said no tracking. This page says they use cookies and share with partners. Which is it?" — evaluator
  > "The bar said no tracking cookies. This page says they use cookies. One of those is wrong." — sceptic
- **Repro:**
  1. Open `/` in a fresh context; read the black bar at the bottom.
  2. Open the network panel: observe `t.js` and the `collect?uid=` POST fire without any interaction.
  3. Footer → Privacy; read the third sentence.
- **Fix:** Either remove the analytics script or rewrite the bar to say what it loads; then make the Privacy page and the bar say the same thing.

### 9a56db1e0d42 — Pricing page shows no price on any plan; every card ends in "Contact sales"
- **Severity:** P1
- **So what:** The evaluator arrived to check price, could not, and left to search for an alternative — the run's stated objective fails.
- **Framework tags:** pricing-transparency
- **Flow:** V3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Three cards — Starter, Team, Enterprise — each with a "Contact sales" button and no number, range or "from" figure
  - Footnote reads "Pricing depends on your workspace type and sync topology." — the persona could not say what a workspace type is
  - "Contact sales" routes to the home-page demo form; persona looked 01:48–02:30 and gave up
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-20` · `persona-evaluator/timeline.json` (`price_found: false`, `objectives[0].gave_up: true`)
  > "So I can't find out what it costs. That's the thing I came to check." — evaluator, 02:30
  > "Without a price I can't take this to my team. I'd search for an alternative." — evaluator, 06:10
- **Repro:**
  1. Nav → Pricing.
  2. Look for any currency figure on the page; click "Contact sales" on any card.
- **Fix:** Put a monthly figure or a "from £X/user" line on Starter and Team, and replace the "workspace type and sync topology" footnote with plain words for what changes the price.

### d74933971e98 — Privacy page names no partners and no data categories, and routes questions to the demo form
- **Severity:** P1
- **So what:** The sceptic's only question — who gets my notes — has no answer, and they left on it; the evaluator's data trust dropped to "unsure".
- **Framework tags:** data-handling, claim-quality
- **Flow:** V3
- **Locator:** /privacy.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Whole policy is four sentences; "partners and service providers" are not named and no data category is listed
  - "We may update this policy at any time." with no date or version
  - Only contact route offered is "Questions? Use the demo form." — the seven-field sales form
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-evaluator/screenshots/06-privacy.png` · `persona-sceptic/session.log:9` · `persona-evaluator/session.log:26` · `persona-sceptic/persona-debrief.md` (Q3, Q5)
  > "That's not a privacy policy, that's a shrug." — sceptic, 00:45
  > "Leave. The cookie bar and the privacy page disagree, and the privacy page won't say who the partners are." — sceptic, Q3
- **Repro:**
  1. Footer → Privacy.
  2. Look for a partner name, a data category, a date, or a contact address.
- **Fix:** Name the service providers, list what is collected, date the policy, and give a privacy contact that is not the sales form.

### f32a5b752d10 — All three testimonials are anonymous — "a happy customer", "a user", "anonymous"
- **Severity:** P2
- **So what:** The one proof section on the site is disbelieved on sight, and it is the moment the evaluator's interest in the page ended (01:25).
- **Framework tags:** proof, claim-quality
- **Flow:** V2
- **Locator:** /index.html #loved-by-teams
- **Personas hit:** evaluator
- **Observed:**
  - Section "Loved by teams" carries three quotes: "It changed how we work." — a happy customer · "Finally, notes that sync." — a user · "10/10 would recommend." — anonymous
  - No name, company, logo or number anywhere in the section
  - `timeline.json` records `point_of_lost_interest: "01:25"`, the timestamp of this reaction
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:15` · `persona-evaluator/findings-raw.json` (t 01:25)
  > "Nobody has a name. I don't believe these." — evaluator, 01:25
- **Repro:**
  1. Open `/`, scroll to "Loved by teams".
  2. Read the attribution under each quote.
- **Fix:** Replace the three quotes with one named customer and a number, or delete the section until one exists.

### 784bad2d71d8 — Demo form requires a phone number before the visitor has seen the product
- **Severity:** P2
- **So what:** The only route past "Contact sales" asks for a phone number first, and the evaluator backed out rather than give it.
- **Framework tags:** data-handling, pricing-transparency
- **Flow:** V3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - Seven fields: first name, last name, work email, phone number, company, company size, what do you want to see
  - Markup: `<label>Phone number</label><input type="tel" required>` — five of seven fields required
  - Persona counted the fields at 02:58 and backed out at 03:15 without submitting
- **Evidence:** `crawl/html/1-index.html:30-33` · `persona-evaluator/session.log:21-22` · `persona-evaluator/timeline.json` (`trust_down: "Phone number required for a demo"`)
  > "Phone is required. I haven't seen the product and they want my phone number." — evaluator, 02:58
- **Repro:**
  1. Pricing → any "Contact sales" → lands on `#demo`.
  2. Try to submit with the phone field empty.
- **Fix:** Make phone optional, and say in one line beside the form what happens after "Request demo".

### 1b5a8cf51bb4-a — "See it in action" does nothing, so nothing on the site shows the product exists
- **Severity:** P1
- **So what:** The sceptic came on the promise "it remembers everything", found nothing that demonstrates it, and left calling the promise unmet.
- **Framework tags:** proof
- **Flow:** V2
- **Locator:** /index.html .cta-see-it-in-action
- **Personas hit:** sceptic
- **Observed:**
  - Tapping "See it in action" produces no navigation, scroll or modal
  - Console on load: `Uncaught ReferenceError: nimbusBootstrap is not defined` (index.html:9)
  - No screenshot, video or product image anywhere the sceptic reached — the hero is a placeholder graphic
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `persona-sceptic/session.log:13` · `persona-sceptic/console-full.txt:1` · `persona-sceptic/persona-debrief.md` (Q6)
  > "I want to see it 'remember' something. The button does nothing when I tap it." — sceptic, 02:20
  > "No — nothing on the site shows it remembering anything; the button that might have doesn't work." — sceptic, Q6
- **Repro:**
  1. Open `/` on a 390×844 viewport; tap "See it in action".
  2. Check the console for `nimbusBootstrap is not defined`.
- **Fix:** Fix the broken bootstrap so the button opens a real product demo, and put one genuine product screenshot in the hero.

### 1b5a8cf51bb4-b — "See it in action" does nothing, so nothing on the site shows the product exists
- **Severity:** P2
- **So what:** The evaluator clicked twice, got nothing, and carried on to pricing — trust nicked but not the reason they left.
- **Framework tags:** proof
- **Flow:** V2
- **Locator:** /index.html .cta-see-it-in-action
- **Personas hit:** evaluator
- **Observed:**
  - Clicked at 00:40, twice; "The page didn't move."
  - Console on load: `Uncaught ReferenceError: nimbusBootstrap is not defined` twice (index.html:9)
  - Not listed in the evaluator's `trust_down`; Q6 still says "nothing shows me it happening"
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-evaluator/console-full.txt:1-2` · `persona-evaluator/persona-debrief.md` (Q6)
  > "Clicked 'See it in action'. Nothing happened. The page didn't move. Clicked again. Still nothing." — evaluator, 00:40
- **Repro:**
  1. Open `/` at 1440×900; click "See it in action" twice.
- **Fix:** Same as 1b5a8cf51bb4-a — make the button work and show the product.

### 5902a1825616 — Data-location, export and offline answers live on About, not on Privacy or the home page
- **Severity:** P2
- **So what:** The only sentences that raised trust are found late and by luck; the sceptic hit Privacy first and had already decided to leave.
- **Framework tags:** provenance, data-handling, consistency
- **Flow:** V3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About FAQ: "Where is my data stored? In the EU (Frankfurt) by default." · "Can I export my notes? Yes … on every plan." · works offline
  - Privacy page, the page a visitor opens for data questions, contains none of these
  - Both personas logged the About page as the first thing that "felt real" and asked why it was not elsewhere
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/01-privacy.png` · `persona-evaluator/session.log:24-25` · `persona-sceptic/session.log:12`
  > "That's the answer I wanted and it's on the About page, not the Privacy page." — sceptic, 01:50
  > "Those are actual answers. Why isn't this on the home page?" — evaluator, 04:20
- **Repro:**
  1. Footer → Privacy; look for where data is stored.
  2. Nav → About; find it under "Frequently asked questions".
- **Fix:** Copy the three FAQ answers onto the Privacy page and put "Data stored in the EU (Frankfurt)" one line under the home-page headline.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The tracker may set a cookie — the network log shows a `uid=` beacon but no `Set-Cookie` header was captured, so the P0 is written on "a third-party beacon fires", not "a cookie is set".
- The "Enterprise" card's "vault residency" may contradict "Frankfurt by default" — no persona read them together; no reaction logged.
- `03-demo-form.png` is a blank capture; the form finding rests on the crawl markup and the session log instead.

## For other lenses
- "Features" in the nav returns a 404 (`persona-evaluator/screenshots/04-features-404.png`) — bugs, ux
- JSON-LD `"offers": {"price": }` is malformed on `/index.html` line 3 — seo, aeo
- Newsletter box outranks the primary CTA visually (`01-scrolled.png`) — conversion
- "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology" undefined — clarity
- Seven-field form burden as a conversion cost — conversion (scored here only for the trust cost of the phone field)

## Coverage gaps
- Sceptic never opened Pricing or scrolled to the testimonials; no flip observable on findings 9a56db1e0d42 and f32a5b752d10
- `/features.html` never rendered (404) for either persona
- No terms-of-service page exists in the crawl; renewal and refund terms could not be assessed
- Cookie-banner behaviour tested on first load only; no re-visit to see whether the beacon fires after "OK"

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/00–06`, `persona-sceptic/screenshots/00–02`
