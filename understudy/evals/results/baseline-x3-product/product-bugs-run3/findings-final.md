# Nimbus Notes — bugs findings — Run 2026-09-08 (fixture02)

## Method
- Framework: console/network evidence correlated with persona experience, per severity-rubric.md
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### b4cad38c3a44 — Save reports success while the API call fails and the note is never stored
- **Severity:** P0
- **So what:** Every note the user writes is silently discarded; the product's core function does not work and tells the user it does.
- **Framework tags:** Lying feedback, Broken state
- **Flow:** shape_2
- **Locator:** /api/notes
- **Personas hit:** novice, power-user
- **Observed:**
  - `POST http://localhost:8765/api/notes` returns `500 (Internal Server Error)` on every save attempt (novice: 03:05, 03:50; power-user: 01:00).
  - Console logs `[error] new.html:1 POST http://localhost:8765/api/notes 500 (Internal Server Error)` at the same timestamps.
  - Despite the 500, the UI shows a green "Saved ✓" toast and returns the user to the dashboard, which still reads "Nothing here yet." Search for the saved title returns "No results" immediately after.
- **Evidence:** `persona-novice/network-full.txt:5` · `persona-novice/network-full.txt:7` · `persona-novice/console-full.txt:3` · `persona-novice/session.log:17-20` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/network-full.txt:3` · `persona-power-user/console-full.txt:2` · `persona-power-user/screenshots/03-search-empty.png`
  > "Clicked Save. Green 'Saved ✓' popped up top right. ... Dashboard still says 'Nothing here yet.' Where did it go?"
- **Repro:**
  1. Complete signup and land on the empty dashboard.
  2. Click "New block", enter a title and body, click Save.
  3. Observe the "Saved ✓" toast and redirect to dashboard.
  4. Note the dashboard still shows "Nothing here yet." and `POST /api/notes` returned 500 in the network log.
- **Fix:** Make the Save button surface the actual API result — show an error state on the 500 instead of the success toast, and fix the endpoint so notes persist.

### 6afeb350adf9 — Memories panel presents fabricated facts as the user's own data
- **Severity:** P0
- **So what:** The product asserts confident, specific claims about the user's work habits and tools that the user never provided, breaking trust in anything else it reports.
- **Framework tags:** Lying feedback
- **Flow:** surfaces
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Observed:**
  - The Memories screen displays "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4." — none entered by either persona, whose only saved content was a dentist note (novice) or a Roadmap note (power-user), neither of which persisted.
  - Footer text claims "Memories are built from your notes and connected accounts" — but no notes exist (see b4cad38c3a44) and no accounts were connected.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21-22` · `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md:13`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the 'Saved' too?"
- **Repro:**
  1. Sign up as a new user (any workspace type).
  2. Do not connect any accounts; optionally save one unrelated note.
  3. Navigate to Memories.
  4. Observe three specific personal claims about meetings, tools, and a product launch that were never provided.
- **Fix:** Remove the Memories panel's placeholder/demo content from real accounts, or clearly label it as sample data until genuine memories exist.

### 2b5127b7eee6 — Uncaught ReferenceError on every dashboard load: `renderGraphOverlay is not defined`
- **Severity:** P2
- **So what:** A JS exception fires on every dashboard visit; it does not yet visibly break rendering but indicates a broken/incomplete feature path shipping to production.
- **Framework tags:** Console error
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - `[error] dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined` fires on every dashboard.html load for both personas (novice: 3 occurrences, power-user: 2 occurrences).
  - No visible layout break was observed in the accompanying dashboard screenshots, so current user-facing impact is limited to console noise.
- **Evidence:** `persona-novice/console-full.txt:1,2,4,6` · `persona-power-user/console-full.txt:1,3`
  > "Uncaught ReferenceError: renderGraphOverlay is not defined"
- **Repro:**
  1. Complete signup with any workspace type.
  2. Load the dashboard.
  3. Open the browser console — the ReferenceError is thrown immediately.
- **Fix:** Define or remove the `renderGraphOverlay` call from `dashboard.html`'s load path.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- None — all observed defects in this run had direct console/network/screenshot evidence.

## For other lenses
- Irreversible, unexplained workspace-type choice ("Federated graph / Sovereign vault / Hybrid mesh... cannot be changed later") forced before any product value is shown — onboarding/UX.
- Inconsistent terminology ("Cards" nav label vs. "New block" form vs. "notes" in copy) — content/UX.
- Settings screen uses unexplained jargon ("Enable webhook sync", "Federated graph replication", "Vault attestation") — content.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, `/` all no-ops) for a persona who explicitly wanted keyboard-driven use — onboarding/UX for power users.

## Coverage gaps
- "Cards" list view never opened directly (only the dashboard's embedded "Your cards" panel).
- No successful save was ever achieved by either persona, so the intended find-again flow (the stated objective) was never reached.

## Appendices
- A. Persona debriefs: `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines: `persona-novice/session.log`, `persona-power-user/session.log`
- C. Screenshot index: `persona-novice/screenshots/`, `persona-power-user/screenshots/`
