# Nimbus Notes — bugs findings — Run 2026-09-08 (fixture02)

## Method
- Framework: bug report — console, network, dead ends, broken and lying states, state corruption
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (findings rest on inferred personas)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Build id: not recorded in run folder

---

## Findings

### 283350d788e1 — Save shows Saved while POST /api/notes returns 500 and the note is discarded
- **Severity:** P0
- **So what:** Users lose every note while the UI says it was saved; the core job (write a note, find it again) fails.
- **Framework tags:** lying-feedback, failed-request, data-loss
- **Flow:** create-note
- **Locator:** POST /api/notes
- **Personas hit:** novice, power-user
- **Observed:**
  - Clicking Save returns `POST /api/notes → 500 internal error`, yet a green "Saved ✓" toast appears.
  - App redirects to the dashboard, which still says "Nothing here yet."; reproduced 2× novice, 1× power-user.
  - Searching for the saved title returns "No results for 'Dentist'."
- **Environment:** persona `novice` · desktop 1440×900 · `http://localhost:8765/app/new.html` · build not recorded · `[03:05]` and `[03:50]`; persona `power-user` · desktop 1440×900 · same URL · `[01:00]`
- **Expected:** 2xx from POST /api/notes, note listed on dashboard and findable by search; on failure, an error message and the form input retained.
- **Actual:** `new.html:1 POST http://localhost:8765/api/notes 500 (Internal Server Error)` with "Saved ✓" shown and the note gone.
- **Evidence:** `persona-novice/screenshots/04-note-saved-toast.png` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/network-full.txt:5` · `persona-novice/network-full.txt:7` · `persona-novice/console-full.txt:3` · `persona-power-user/network-full.txt:3` · `persona-novice/session.log:17`
  > "It said saved."
  > "It is lying to me."
- **Repro:**
  1. Sign up, choose any workspace type, open the dashboard.
  2. Click "New block", enter title "Dentist" and a few lines of body.
  3. Click Save; observe "Saved ✓" and the 500 on POST /api/notes.
  4. On the dashboard, observe "Nothing here yet."; search "Dentist" returns "No results for 'Dentist'."
- **Fix:** Fix the 500 in the /api/notes handler, and show the success toast only after a 2xx response (otherwise show an error and keep the form).

### b0a1e1e83e53 — Memories lists three facts about the user in a workspace with no notes
- **Severity:** P1
- **So what:** Fabricated personal claims make both personas distrust the product, including its "Saved" confirmations.
- **Framework tags:** broken-state, wrong-data
- **Flow:** surfaces
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Observed:**
  - New account with zero saved notes shows "You prefer to schedule meetings on Tuesday afternoons."
  - Also "Your team uses Jira and Slack." and "You are working on a product launch in Q4."
  - Footer says "Memories are built from your notes and connected accounts." No accounts were connected.
- **Environment:** persona `novice` · desktop 1440×900 · `http://localhost:8765/app/memories.html` · build not recorded · `[04:30]`; persona `power-user` · same · `[02:30]`
- **Expected:** An empty state, or only facts derived from the user's own notes and connected accounts.
- **Actual:** Three hard-coded-looking memories shown unconditionally; no console or network error accompanies them.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-power-user/session.log:14`
  > "None of that is true. I've written one note about a dentist."
- **Repro:**
  1. Sign up with a fresh account; do not connect any account or save a note.
  2. Click "Memories" in the top menu.
  3. Observe the three statements above. Cause is not visible in the logs; source of the data unconfirmed.
- **Fix:** Render an empty state on /app/memories.html until memories derive from the user's own notes; remove the seeded or demo entries.

### b67f251be813 — Dashboard throws ReferenceError renderGraphOverlay is not defined on every load
- **Severity:** P2
- **So what:** A script on every dashboard load crashes; user-visible impact is unconfirmed but any feature behind it is dead.
- **Framework tags:** console-error, uncaught-exception
- **Flow:** dashboard
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Logged 4× for novice and 2× for power-user, once per dashboard load.
  - No visible graph overlay on the dashboard screenshots.
  - No persona noticed it; it did not block any step they took.
- **Environment:** persona `novice` · desktop 1440×900 · `http://localhost:8765/app/dashboard.html` · build not recorded · from `[00:55]`; persona `power-user` · same · from `[00:30]`
- **Expected:** No uncaught exceptions on load; `renderGraphOverlay` defined or its call removed.
- **Actual:** `dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined`
- **Evidence:** `persona-novice/console-full.txt:1` · `persona-novice/console-full.txt:2` · `persona-power-user/console-full.txt:1` · `persona-novice/screenshots/05-notes-list-missing.png`
- **Repro:**
  1. Complete signup.
  2. Open `/app/dashboard.html` with the browser console open.
  3. Observe the exception on load.
- **Fix:** Define or load `renderGraphOverlay` in dashboard.html, or remove the call, and add a console-error check to CI.

---

## Dropped for want of evidence
- Power-user claim "search doesn't search" — no note ever persisted, so search against real data was never exercised.
- Whether `renderGraphOverlay` causes the empty dashboard list — no log links the two.

## For other lenses
- Workspace type "This cannot be changed later." chosen before the product is seen, with unexplained terms — ux / onboarding.
- Settings jargon: "Federated graph replication", "Vault attestation", "Enable webhook sync" — content.
- "Cards" vs "New block" naming inconsistency — content.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) — ux (missing feature, not a bug).

## Coverage gaps
- Search never exercised against stored notes, since no save succeeded.
- Export to Markdown never run.
- Single device profile (desktop 1440×900); no mobile or multi-tab testing.

## Appendices
- A. Persona debriefs
- B. Session timelines
- C. Screenshot index
