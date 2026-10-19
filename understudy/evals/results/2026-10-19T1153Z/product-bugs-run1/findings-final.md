# Nimbus Notes — bugs findings — Run 2026-09-08 (fixture02)

## Method
- Framework: bug report (console, network, dead ends, broken states, lying feedback, state corruption)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 29830887b14c — Save returns 500 on POST /api/notes but UI shows Saved and the note is lost
- **Severity:** P0
- **So what:** Users believe notes are stored, but every note is discarded; the product's core job fails.
- **Framework tags:** lying-feedback, failed-request, data-loss
- **Flow:** shape_2
- **Locator:** POST /api/notes
- **Personas hit:** novice, power-user
- **Observed:**
  - Save sends POST /api/notes and gets `500 (Internal Server Error)`. A green "Saved ✓" toast follows anyway.
  - The app redirects to the dashboard, which still shows "Nothing here yet."
  - Reproduced 3 times: novice twice (03:05, 03:50), power-user once (01:00). Search for the saved title returns "No results".
- **Environment:** persona `novice` · desktop-1440x900 · `http://localhost:8765/app/new.html` · build n/a (not recorded) · `[03:05]`; also persona `power-user` · desktop-1440x900 · same URL · `[01:00]`
- **Expected:** a 2xx response, the note stored and listed under "Your cards" and found by search. On failure, an error message and the input kept.
- **Actual:** `new.html:1 POST http://localhost:8765/api/notes 500 (Internal Server Error)` with a "Saved ✓" toast and an empty list.
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:20` · `persona-novice/console-full.txt` · `persona-novice/network-full.txt` (`[POST] .../api/notes → 500 internal error (03:05)`, `(03:50)`) · `persona-power-user/session.log:11` · `persona-power-user/network-full.txt` (`(01:00)`)
  > "It said saved. The list is empty. Where did it go?"
  - Note: `04-note-saved-toast.png` shows the empty form with no toast. The toast is evidenced by the session log only.
- **Repro:**
  1. Sign in and complete workspace-type signup (any choice).
  2. Open "New block" (`/app/new.html`).
  3. Enter title "Dentist" and a few lines of body text.
  4. Click Save, and observe the "Saved ✓" toast and the 500 in the network panel.
  5. Open the dashboard: "Nothing here yet." Search "Dentist": "No results for 'Dentist'."
- **Fix:** Fix the server error on POST /api/notes, and make new.html show "Saved ✓" only on a 2xx; on failure keep the form and show an error.

### fe17127893bf — Dashboard throws ReferenceError renderGraphOverlay is not defined on every load
- **Severity:** P2
- **So what:** An uncaught exception fires on every dashboard visit; it may break dashboard rendering, but that link is unproven.
- **Framework tags:** console-error
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - `dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined` logged on each dashboard load.
  - Novice: 4 occurrences. Power-user: 2.
  - No visible failure is attributable to it, since the list was empty anyway because the save failed.
- **Environment:** persona `novice` · desktop-1440x900 · `http://localhost:8765/app/dashboard.html` · build n/a (not recorded) · `[00:55]`; also persona `power-user` · desktop-1440x900 · same URL · `[00:30]`
- **Expected:** the dashboard loads with no uncaught exceptions.
- **Actual:** `dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined`
- **Evidence:** `persona-novice/console-full.txt` · `persona-power-user/console-full.txt` · `persona-novice/screenshots/02-dashboard-empty.png`
- **Repro:**
  1. Sign in and complete signup.
  2. Open `/app/dashboard.html`.
  3. Open the browser console and read the ReferenceError.
- **Fix:** Define or import `renderGraphOverlay` in dashboard.html, or remove the call; then check whether list rendering depends on it.

### 19f96ab711b8 — Memories lists facts the user never provided
- **Severity:** P2
- **So what:** Users see invented claims under "What Nimbus remembers about you" and doubt the other "Saved" claims too.
- **Framework tags:** broken-state, wrong-data
- **Flow:** surfaces
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Page lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack." and "You are working on a product launch in Q4."
  - The footer says "Memories are built from your notes and connected accounts." Neither persona had saved a note or connected an account.
  - Cause unknown: this may be hard-coded demo data or another account's data. The run cannot tell.
- **Environment:** persona `novice` · desktop-1440x900 · `http://localhost:8765/app/memories.html` · build n/a (not recorded) · `[04:30]`; also persona `power-user` · desktop-1440x900 · same URL · `[02:30]`
- **Expected:** an empty state, or only facts derived from the user's own notes and connected accounts.
- **Actual:** three statements the user did not supply, shown as fact.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-power-user/session.log:15`
  > "None of that is true. I've written one note about a dentist."
- **Repro:**
  1. Sign in as a new user with no saved notes and no connected accounts.
  2. Click "Memories".
  3. Read the three statements.
- **Fix:** Remove the hard-coded memories (or scope them to the signed-in user) and show an empty state until real data exists.

---

## Dropped for want of evidence
- "Federated graph replication" is on by default and may not match the workspace type chosen at signup — the novice chose Hybrid mesh, but no state was captured.
- Search returning "No results" may be broken — no note ever persisted, so search could not be tested.

## For other lenses
- Irreversible workspace-type choice ("This cannot be changed later.") with unexplained terms Federated graph, Sovereign vault, Hybrid mesh — ux/onboarding.
- Mixed vocabulary "Cards", "New block", "notes" — content.
- Settings jargon "Enable webhook sync", "Vault attestation" — content.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) — ux; a missing feature, not a bug.

## Coverage gaps
- Note edit, delete and the Export button were never exercised.
- Search against real data never tested, since nothing persisted.
- Only desktop-1440x900 tested.

## Appendices
- A. Persona debriefs
- B. Session timelines
- C. Screenshot index
