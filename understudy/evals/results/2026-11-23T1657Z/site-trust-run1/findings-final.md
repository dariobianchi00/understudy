# Nimbus Notes — trust findings — Run 2026-09-08 (fixture01)

## Method
- Framework: the four trust questions (real? cost? who? data?), plus proof substance, claim quality and consistency
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop; sceptic, iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Trust is scored only on what the site says; nothing here comes from outside the capture
- This is not a compliance review of the privacy policy and implies none

---

## Findings

### a9a8c6dbc59b — Cookie bar claims no tracking while a third-party analytics tracker sends a user ID on page load
- **Severity:** P0
- **So what:** The site's first data-handling claim is contradicted by its own traffic; a visitor who checks has no reason to believe the rest.
- **Framework tags:** data-handling, consistency, cookie-banner-mismatch
- **Flow:** V1
- **Locator:** /index.html#cookie
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Banner on both devices reads "We use no tracking cookies on this site."
  - Both sessions load `analytics.example-tracker.test/t.js` (third-party) and POST to `/collect?uid=…` — a per-visitor ID.
  - Both personas then read "We use cookies and similar technologies" on Privacy and called it a contradiction.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/network-full.txt:4-5` (`[GET] https://analytics.example-tracker.test/t.js → 200`, `[POST] https://analytics.example-tracker.test/collect?uid=8f3a… → 204`) · `persona-sceptic/network-full.txt:2-3` (`[POST] …/collect?uid=2c91… → 204`) · `persona-sceptic/session.log:10` · `persona-evaluator/session.log:27`
  > "The bar said no tracking cookies. This page says they use cookies. One of those is wrong." — sceptic
- **Repro:**
  1. Open `/` in a fresh browser context with network logging on.
  2. Note the banner text "We use no tracking cookies on this site."
  3. Observe the request to `analytics.example-tracker.test/collect?uid=…` before any banner interaction.
- **Fix:** Either remove the analytics tracker or rewrite the banner to name it and gate it behind consent before `/collect` fires.
- P0 not P1: the network log records the identifier call, not a cookie being set; the banner's "no tracking" claim is still contradicted by observed tracking, so P0 is flagged rather than buried.

### a1510a83a07d — Privacy page names no partners and contradicts the cookie bar — the sceptic left over it
- **Severity:** P1
- **So what:** The sceptic came to learn what happens to their notes, could not, and left at 02:40 — this page cost the visit.
- **Framework tags:** data-handling, consistency
- **Flow:** V3
- **Locator:** /privacy.html
- **Personas hit:** sceptic
- **Observed:**
  - Page reads "We may share information with partners and service providers" — no partner named.
  - Page reads "We use cookies and similar technologies" and "We may update this policy at any time."
  - Sceptic's leave condition was a generic policy; debrief Q3 answer is "Leave."
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-sceptic/session.log:9` · `persona-sceptic/session.log:14` · `persona-sceptic/persona-debrief.md` Q3, Q5 · `persona-sceptic/timeline.json` `shape_v4.verdict`: "left; data handling unclear"
  > "That's not a privacy policy, that's a shrug."
  > "The privacy page took it back." — Q5
- **Repro:**
  1. On mobile, tap Privacy in the footer.
  2. Look for who "partners and service providers" are.
  3. Compare "We use cookies" with the home-page banner.
- **Fix:** On /privacy.html, list each third party by name with what it receives, and make the cookie statement match the banner.

### c186cfd28f5d — Privacy page names no partners and contradicts the cookie bar — the evaluator ended unsure about data
- **Severity:** P2
- **So what:** The evaluator's data trust fell to "unsure" after the About page had raised it; they had already left over price.
- **Framework tags:** data-handling, consistency
- **Flow:** V3
- **Locator:** /privacy.html
- **Personas hit:** evaluator
- **Observed:**
  - Same page and wording as the sceptic saw, read at 04:50 on desktop.
  - Evaluator flagged the cookie contradiction at 05:20 and carried on to the home page.
  - Debrief Q5 on data: "unsure" — not a refusal.
- **Evidence:** `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:26-27` · `persona-evaluator/persona-debrief.md` Q5
  > "The privacy page and the cookie bar contradicting each other undid that."
- **Repro:**
  1. On desktop, click Privacy in the footer after visiting About.
  2. Read the single paragraph and compare it with the cookie bar.
- **Fix:** Same as the sceptic variant: name the partners and reconcile the cookie wording on /privacy.html.

### a7faa2f45da6 — No plan shows a price, so the evaluator gave up on cost and would not trust them with money
- **Severity:** P1
- **So what:** Price was the evaluator's stated reason to visit; with none shown they would "search for an alternative".
- **Framework tags:** pricing-transparency
- **Flow:** V3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Starter, Team and Enterprise each show only "Contact sales" — no figure anywhere.
  - Only explanation: "Pricing depends on your workspace type and sync topology." — the evaluator could not say what their workspace type was.
  - Looked 01:48–02:30 at /pricing.html and /index.html#demo; `gave_up: true`.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-19` · `persona-evaluator/session.log:29` · `persona-evaluator/timeline.json` `objectives[0]` · `persona-evaluator/persona-debrief.md` Q3, Q5
  > "Money, no — I don't know what they'd charge." — Q5
- **Repro:**
  1. Click Pricing in the nav.
  2. Look for a number on any of the three plans.
  3. Read the line under the cards.
- **Fix:** Put a starting price (or per-seat range) on the Starter and Team cards and replace "workspace type and sync topology" with what actually changes the price.
- The sceptic never looked for price, so whether this flips by persona could not be observed.

### 593c2be8767b — Contact sales demands a required phone number before the visitor has seen the product
- **Severity:** P2
- **So what:** The only route to a price asks for seven fields including a phone; the evaluator read it as a data grab and backed out.
- **Framework tags:** data-handling, pricing-transparency
- **Flow:** V3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - Every "Contact sales" button lands on the home-page "Book a demo" form.
  - Markup marks first name, last name, work email, phone number and company `required`.
  - Evaluator backed out at 03:15 without submitting; listed it in `trust_down`.
- **Evidence:** `persona-evaluator/session.log:20-22` · `persona-evaluator/timeline.json` `trust_down`: "Phone number required for a demo" · `crawl/html/1-index.html:31` (`<label>Phone number</label><input type="tel" required>`) · `persona-evaluator/screenshots/01-scrolled.png` (form heading "Book a demo")
  > "I haven't seen the product and they want my phone number."
- **Repro:**
  1. On /pricing.html click any "Contact sales".
  2. Count required fields on the "Book a demo" form.
- **Fix:** Make phone optional on the demo form, and do not route price questions to it at all once prices are shown.
- `03-demo-form.png` is blank and is not cited as evidence.

### 0917ae16075b — All three testimonials are anonymous, so the only proof on the home page was disbelieved
- **Severity:** P2
- **So what:** "Loved by teams" is the site's only claim of real users; with no names, the evaluator discounted it outright.
- **Framework tags:** proof, claim-quality
- **Flow:** V2
- **Locator:** /index.html
- **Personas hit:** evaluator
- **Observed:**
  - Quotes attributed to "— a happy customer", "— a user", "— anonymous".
  - No customer names, logos, numbers or case studies anywhere the personas went.
  - Evaluator lost interest at 01:25 — the testimonial moment (`point_of_lost_interest`).
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:15` · `persona-evaluator/timeline.json` `trust_down`: "Anonymous testimonials"
  > "Nobody has a name. I don't believe these."
- **Repro:**
  1. Scroll the home page to "Loved by teams".
  2. Read the attribution on each quote.
- **Fix:** Replace the three quotes with attributed ones (name, role, team) or one named customer with a number; remove any that cannot be attributed.

### 581373ad6f3c — Headline promises nothing is ever lost or exposed, and nothing on the site shows it
- **Severity:** P2
- **So what:** Both personas arrived on "remembers everything" and left saying nothing showed it — the core claim went unproven.
- **Framework tags:** claim-quality, proof
- **Flow:** V1
- **Locator:** /index.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Hero copy: "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed." — no mechanism explained.
  - Hero image is abstract circles; "See it in action" did nothing for either persona.
  - Q6 promise match: evaluator "Close but off", sceptic "No".
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:10,12` · `persona-sceptic/session.log:13` · `persona-evaluator/persona-debrief.md` Q6 · `persona-sceptic/persona-debrief.md` Q6
  > "nothing on the site shows it remembering anything; the button that might have doesn't work." — sceptic
- **Repro:**
  1. Load `/`.
  2. Read the hero sub-line and look for any screenshot, demo or explanation of it.
- **Fix:** Show one real product screenshot or short clip of a note syncing/being recalled beside the hero claim, and explain "zero-knowledge vault" in one plain line.

### 3fd41fe92dec — The site's best trust answers sit only on About, not on Home or Privacy
- **Severity:** P2
- **So what:** Both personas named About as the only thing that made Nimbus feel real; a visitor who skips it never sees that.
- **Framework tags:** provenance, data-handling
- **Flow:** V3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About names "Nimbus Notes Ltd", "Priya Raman", 2023, Bristol address, company number 14482201, eight people.
  - About FAQ answers offline use, Markdown export and "In the EU (Frankfurt) by default."
  - Neither home page nor /privacy.html carries any of it.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:24-25` · `persona-sceptic/session.log:11-12`
  > "That's the answer I wanted and it's on the About page, not the Privacy page." — sceptic
  > "Those are actual answers. Why isn't this on the home page?" — evaluator
- **Repro:**
  1. Read `/` and `/privacy.html` for who runs Nimbus or where data is stored.
  2. Open `/about.html` and compare.
- **Fix:** Add the Frankfurt storage line and company details to /privacy.html, and a one-line "made by Nimbus Notes Ltd, Bristol" plus FAQ link on the home page.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Demo form contents as a screenshot — `persona-evaluator/screenshots/03-demo-form.png` is blank; finding rests on session log and crawl markup instead.
- Whether a tracking cookie is actually set — network log shows the tracker call and `uid`, not `Set-Cookie`; capture cookie jar next run.
- Whether the tracker fires before or after "OK" on the banner — network log has no timestamps.

## For other lenses
- "See it in action" does nothing on click/tap, both devices — conversion / technical
- "Features" nav link returns 404 — technical / conversion
- Headline does not say what the product is; neither persona could answer "what" or "who" — clarity
- Newsletter box outweighs the primary button — conversion
- Hero image is 3.9 MB — technical

## Coverage gaps
- Sceptic never opened /pricing.html — no persona comparison on cost.
- No terms page, login, or signup reached.
- No cookie-jar capture; consent behaviour inferred from network requests only.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00-landing, 01-scrolled, 02-pricing, 03-demo-form (blank), 04-features-404, 05-about, 06-privacy · sceptic 00-landing, 01-privacy, 02-about
