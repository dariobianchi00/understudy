# Nimbus Notes — trust findings — Run 2026-09-08 (fixture01)

## Method
- Framework: the four trust questions (real? · cost? · who? · data?), applied to proof, pricing, provenance, data handling, claim quality and consistency
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop-1440x900 · sceptic, iphone-13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Only what a visitor could check on the site counts. No outside sources used. This is not a compliance review.

---

## Findings

### 9f10a532b359 — Cookie banner says "no tracking cookies" while every page load sends a visitor ID to a third-party analytics host
- **Severity:** P0
- **So what:** The first promise a visitor reads turns out false. Both personas had already seen it contradicted by the privacy page, and the sceptic left over it.
- **Framework tags:** data handling · consistency
- **Flow:** V1 — Land
- **Locator:** /index.html #cookie
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The banner says "We use no tracking cookies on this site." Its OK button only removes the banner (`onclick="document.getElementById('cookie').remove()"`).
  - Both sessions load `analytics.example-tracker.test/t.js` and POST `/collect?uid=…` → 204 on landing. Neither request waits for any consent.
  - The privacy page says "We use cookies and similar technologies." Both personas caught this contradiction themselves.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/network-full.txt:4-5` · `persona-sceptic/network-full.txt:2-3` · `crawl/html/1-index.html:3` (`<script src="https://analytics.example-tracker.test/t.js" async>`) · `crawl/html/1-index.html:37` · `persona-sceptic/session.log:10` · `persona-evaluator/session.log:27`
  > "The bar said no tracking cookies. This page says they use cookies. One of those is wrong." (sceptic)
  > "The cookie bar said no tracking. This page says they use cookies and share with partners. Which is it?" (evaluator)
- **Repro:**
  1. Open `/` with network logging on.
  2. Read the bottom banner: "We use no tracking cookies on this site."
  3. Before you click anything, see `t.js` load and a POST to `analytics.example-tracker.test/collect?uid=…`.
- **Fix:** Either remove the third-party analytics or change the banner to name it. Put any consent choice before the script loads, and make the banner match the privacy page.
- *Note:* the capture logged requests, not cookies. The finding rests on an identifier beacon to a third-party analytics host under a "no tracking" banner. Whether a cookie was actually set is not proven.

### 823356cbe5ec — Privacy page names no partners and commits to nothing specific, and the sceptic left over it
- **Severity:** P1
- **So what:** The sceptic came only to learn what happens to her notes. The page did not tell her, so she left.
- **Framework tags:** data handling
- **Flow:** V3 — Evaluate
- **Locator:** /privacy.html
- **Personas hit:** sceptic
- **Observed:**
  - The whole policy is one paragraph: "We may share information with partners and service providers to improve your experience."
  - It names no partners, no data categories and no retention. It ends "We may update this policy at any time."
  - The only contact route is "Questions? Use the demo form."
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-sceptic/session.log:9` · `persona-sceptic/session.log:14` · `crawl/html/5-privacy.html:10-11` · `persona-sceptic/timeline.json` shape_v4.verdict "left; data handling unclear"
  > "With whom? Not said. 'We may update this policy at any time.' That's not a privacy policy, that's a shrug."
  > "The About page made them real … The privacy page took it back." (Q5)
- **Repro:**
  1. Open `/`, then tap Privacy in the footer.
  2. Look for a named partner, a list of what data is collected, or a contact that is not the demo form.
- **Fix:** Rewrite `/privacy.html`. Name each third party and its purpose, list what is collected, and give a privacy contact address. Move the Frankfurt storage answer here too.

### 9559fd6eb003 — No price anywhere: all three plans say "Contact sales", so the evaluator would not trust them with money
- **Severity:** P1
- **So what:** Price was the evaluator's reason for visiting. They gave up at 02:30 and said they would look for an alternative.
- **Framework tags:** pricing transparency
- **Flow:** V3 — Evaluate
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - The Starter, Team and Enterprise cards each say only "Contact sales". There are no numbers.
  - The only explanation is "Pricing depends on your workspace type and sync topology." The evaluator said they didn't know their workspace type.
  - The evaluator also checked `/index.html#demo` and found no price there.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-19` · `persona-evaluator/session.log:29` · `persona-evaluator/timeline.json` objectives[0].gave_up = true, price_found = false
  > "So I can't find out what it costs. That's the thing I came to check."
  > "Money, no — I don't know what they'd charge." (Q5)
- **Repro:**
  1. Click Pricing in the nav.
  2. Look for a number on any plan.
- **Fix:** Put a starting price, or a price range, on each card in `/pricing.html`. Replace "workspace type and sync topology" with what actually changes the price, in plain words.

### 0d2fe4b6dee2 — The only route to a price demands a phone number before any product is shown, and the evaluator backed out
- **Severity:** P1
- **So what:** Asking for a phone number before showing anything costs trust. The evaluator refused, so their last route to a price closed.
- **Framework tags:** data handling · pricing transparency
- **Flow:** V3 — Evaluate
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - "Contact sales" goes to the home-page demo form, which has seven fields.
  - Phone number is `required`, along with first name, last name, work email and company.
  - The evaluator abandoned the form at 03:15.
- **Evidence:** `persona-evaluator/session.log:20-22` · `crawl/html/1-index.html:30-32` (`<label>Phone number</label><input type="tel" required>`)
  > "Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. On `/pricing.html`, click any "Contact sales".
  2. Count the required fields on the form you land on.
- **Fix:** Make phone optional on the demo form and drop it to email-only. Also link the pricing cards to a published price instead of the form.

### d80f05129006 — "See it in action" does nothing, so neither persona ever saw the product exist
- **Severity:** P2
- **So what:** Neither persona saw proof that the product exists. The sceptic listed the dead button as a reason she trusted the site less.
- **Framework tags:** proof · claim quality
- **Flow:** V2 — Orient
- **Locator:** /index.html a.cta
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The hero button goes to `href="#"`. Clicking it twice (evaluator) or tapping it (sceptic) did nothing.
  - The site shows no product screenshot or demo anywhere, so "remembers everything" is never shown.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `crawl/html/1-index.html:12` · `persona-sceptic/timeline.json` trust_down
  > "I want to see it 'remember' something. The button does nothing when I tap it." (sceptic)
  > "nothing on the site shows it remembering anything; the button that might have doesn't work." (sceptic Q6)
- **Repro:**
  1. Open `/`.
  2. Click "See it in action" and watch whether anything happens.
- **Fix:** Point "See it in action" at a short product video or screenshot tour that shows a note being recalled.

### 7279f342b044 — "Loved by teams" quotes are attributed to nobody, and the evaluator disbelieved all three
- **Severity:** P2
- **So what:** The site's only social proof made the evaluator trust it less. A sceptical buyer reads quotes with no names as invented.
- **Framework tags:** proof
- **Flow:** V2 — Orient
- **Locator:** /index.html #proof
- **Personas hit:** evaluator
- **Observed:**
  - The quotes are signed "— a happy customer", "— a user", "— anonymous".
  - There is no name, company, number or link on any of them.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:15` · `crawl/html/1-index.html:24-26` · `persona-evaluator/timeline.json` trust_down "Anonymous testimonials"
  > "Nobody has a name. I don't believe these."
- **Repro:**
  1. Scroll `/` to "Loved by teams".
  2. Read the attributions.
- **Fix:** Replace the three quotes with one or two from named customers, each with a role, a company and a specific result. Otherwise delete the section.

### 4a30d6882dc7 — Privacy page left the evaluator "unsure" about data, but price is what made them leave
- **Severity:** P2
- **So what:** This is the same page that drove the sceptic away, but here it was a complaint, not a reason to leave. That is a severity flip.
- **Framework tags:** data handling
- **Flow:** V3 — Evaluate
- **Locator:** /privacy.html (evaluator)
- **Personas hit:** evaluator
- **Observed:**
  - The evaluator read the same "partners and service providers" line and asked "Which partners?"
  - They listed "Who they share my data with" as unanswered.
  - Their stated reason for leaving was price, not data.
- **Evidence:** `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:26` · `persona-evaluator/persona-debrief.md` Q4, Q5
  > "Data, unsure. The About page made them feel real … The privacy page and the cookie bar contradicting each other undid that."
- **Repro:**
  1. Click Privacy in the footer.
  2. Look for who "partners and service providers" are.
- **Fix:** Use the same `/privacy.html` rewrite as 823356cbe5ec, with named third parties and their purposes.

### c544be43a34e — The strongest trust signals live only on the About page, not on the home or privacy page where personas looked
- **Severity:** P2
- **So what:** The About page is the only place either persona said trust went up. Both had to dig for it, and both asked why it wasn't elsewhere.
- **Framework tags:** provenance · data handling
- **Flow:** V3 — Evaluate
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The About page names "Priya Raman", "Bristol", "2023", "Company number 14482201" and eight people. It also says data is stored "In the EU (Frankfurt) by default".
  - None of this appears on `/` or on the privacy page.
  - The evaluator found it at 03:50 and the sceptic at 01:30–01:50. Both were looking elsewhere first.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:24-25` · `persona-sceptic/session.log:11-12` · `crawl/html/4-about.html:10-17`
  > "Those are actual answers. Why isn't this on the home page?" (evaluator)
  > "That's the answer I wanted and it's on the About page, not the Privacy page." (sceptic)
- **Repro:**
  1. Open `/` and `/privacy.html` and look for who runs the company and where data is stored.
  2. Open `/about.html` and find both answers there.
- **Fix:** Add a one-line "Made by Nimbus Notes Ltd, Bristol, data in Frankfurt" strip to the home footer. Repeat the storage location on `/privacy.html`.

### dcbad8f277be — Home page says nothing is "ever lost or exposed" while the privacy page says data may be shared with partners
- **Severity:** P3
- **So what:** No persona connected the two lines. A reader who does will doubt "zero-knowledge vault", which is the headline security claim.
- **Framework tags:** claim quality · consistency
- **Flow:** V1 — Land
- **Locator:** /index.html .hero p
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The hero says "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - The privacy page says "We may share information with partners and service providers".
  - The site gives no mechanism for "zero-knowledge" anywhere. The evaluator said: "I don't know what either of those means."
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/06-privacy.png` · `crawl/html/1-index.html:11` · `crawl/html/5-privacy.html:10` · `persona-evaluator/session.log:10`
- **Repro:**
  1. Read the hero sub-line on `/`.
  2. Read the second sentence of `/privacy.html`.
- **Fix:** Say on the privacy page what "zero-knowledge" covers and what is still shared (e.g. analytics, never note content). Otherwise remove the claim.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Whether a tracking cookie was actually set: the network log has no Set-Cookie or cookie-jar data. The P0 rests on the identifier beacon only.
- What the demo form looked like on screen: `persona-evaluator/screenshots/03-demo-form.png` is blank. The form finding rests on session.log and the crawl markup.

## For other lenses
- The "Features" nav link returns 404 ("That page does not exist."), see `persona-evaluator/session.log:23` and network-full.txt:8 — technical
- The headline does not say what the product is or who it is for, and both personas guessed — clarity
- The newsletter box is bigger than the primary CTA, and "Contact sales" is the only path to buy — conversion
- The 3.9 MB hero image and a render-blocking third-party font CSS are in network-full.txt — technical
- The `SoftwareApplication` JSON-LD has an empty `"price": }` (malformed), see `crawl/html/1-index.html:3` — seo / aeo

## Coverage gaps
- The sceptic never opened `/pricing.html`, so we cannot tell how a privacy-first visitor reacts to "Contact sales".
- No persona submitted a form, so what happens to data after submission was not observed.
- Cookie storage was not captured. Only requests were logged.
- `03-demo-form.png` capture failed (blank).

## Appendices
- A. Persona debriefs: `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines: `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index: evaluator 00-landing, 01-scrolled, 02-pricing, 03-demo-form (blank), 04-features-404, 05-about, 06-privacy · sceptic 00-landing, 01-privacy, 02-about
