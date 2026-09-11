# Nimbus Notes — bugs findings — Run 2026-09-08 (fixture02)

## Method
- Framework: console/network evidence first, correlated with persona-observed impact
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 7f1c23ec2622 — Save note returns 500 but shows false success toast; note never persists
- **Severity:** P0
- **So what:** Both personas wrote a note, were told it saved, and lost it — the core objective ("write a note and find it again") fails outright and neither could tell without checking.
- **Framework tags:** lying feedback, failed request, broken state
- **Flow:** shape_2
- **Locator:** /api/notes
- **Personas hit:** novice, power-user
- **Observed:**
  - `POST http://localhost:8765/api/notes` returns `500 (Internal Server Error)` every time Save is clicked (novice: 03:05 and 03:50; power-user: 01:00).
  - UI shows a green "Saved ✓" toast regardless of the 500, then returns to a dashboard that still reads "Nothing here yet."
  - Searching for the note's own title immediately after ("Dentist", "Roadmap") returns "No results for '<title>'."
- **Evidence:** `persona-novice/network-full.txt:5` · `persona-novice/console-full.txt:3` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/network-full.txt:3` · `persona-power-user/console-full.txt:2` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/session.log:17-20` · `persona-power-user/session.log:11`
  > "Saved twice, empty twice. It is lying to me."
  > "Enough. Save doesn't save and search doesn't search. Nothing else matters until those work."
- **Repro:**
  1. Complete signup, land on empty dashboard.
  2. Go to New block, enter a title and body, click Save.
  3. Observe network tab: `POST /api/notes` → 500; UI still shows "Saved ✓".
  4. Return to dashboard: "Your cards" still shows "Nothing here yet."
  5. Search the note's title in the search box: "No results for '<title>'."
- **Fix:** Fix the 500 on `POST /api/notes` (check server logs for the actual exception), and gate the success toast on the API response actually succeeding rather than firing unconditionally on submit.

### cbc16c1d3ac5 — Memories panel presents fabricated personal facts as real data
- **Severity:** P0
- **So what:** The page claims "Memories are built from your notes and connected accounts" and states specific false facts about the persona, destroying trust in every other claim the product makes.
- **Framework tags:** lying feedback, confident nonsense about persona's own data
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Memories page lists: "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer text on the same page reads "Memories are built from your notes and connected accounts."
  - Neither persona had written more than one dentist/roadmap note (which itself failed to save, see acc57c7bca5b) and connected zero accounts.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-power-user/session.log:14` · `persona-novice/session.log:21-22`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the 'Saved' too?"
  > "Memories aren't mine. A demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Complete signup with an empty account (no notes saved, no accounts connected).
  2. Click "Memories" in the top nav.
  3. Observe three specific personal-sounding claims are shown as fact, unrelated to any input.
- **Fix:** Either populate Memories only from data the account actually has (and show a genuine empty state when there is none), or clearly label this panel as sample/demo content until real memories exist.

### 2b5127b7eee6 — Uncaught ReferenceError renderGraphOverlay is not defined on every dashboard load
- **Severity:** P3
- **So what:** A JS exception fires on every visit to the dashboard for every persona; no confirmed missing UI was reported this run, but it is a real, reproducible code defect worth triaging before it masks a future regression.
- **Framework tags:** console error, uncaught exception
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - `[error] dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined` logged on every dashboard.html load in both sessions (3 times for novice, 2 times for power-user).
  - No visible UI breakage was reported by either persona in the debrief or timeline beyond the console noise.
- **Evidence:** `persona-novice/console-full.txt:1-6` · `persona-power-user/console-full.txt:1,3`
- **Repro:**
  1. Sign up and land on /app/dashboard.html (or navigate back to it from any other screen).
  2. Open the browser console.
  3. Observe `Uncaught ReferenceError: renderGraphOverlay is not defined` on each load.
- **Fix:** Define `renderGraphOverlay` (or remove the dangling call) so dashboard.html loads without throwing.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Screenshot `persona-novice/screenshots/04-note-saved-toast.png` (captured at the moment of the "Saved ✓" toast per session.log:17) actually shows the New block form reset to 0 words with no toast visible — could not independently confirm the toast's visual appearance from this artifact; relied on session.log narration and the corroborating 500 network entry instead.

## For other lenses
- Signup forces an irreversible "workspace type" choice (Federated graph / Sovereign vault / Hybrid mesh) before the user has seen the product — onboarding/UX.
- Nav labels "Cards" / "New block" / "Memories" are inconsistent with each other and with "note" — content/UX.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) despite power-user expectation — missing feature, UX.
- Settings label "Federated graph replication" duplicates the signup workspace-type wording with no link explaining the relationship — content/UX.
- Settings jargon ("Enable webhook sync", "Vault attestation") unexplained to a novice persona — content/UX.

## Coverage gaps
- Neither persona reached the "Cards" list view directly (nav item exists but was not clicked in either session) — unconfirmed whether it differs from the dashboard "Your cards" panel.
- No persona attempted editing or deleting an existing note (none ever successfully saved).
- Mobile/responsive viewport not tested — both personas ran desktop-1440x900 only.

## Appendices
- A. Persona debriefs: `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines: `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index: `persona-novice/screenshots/`, `persona-power-user/screenshots/`
