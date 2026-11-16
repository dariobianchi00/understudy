# Nimbus Notes — bugs findings — Run 2026-09-08 (fixture02)

## Method
- Framework: bug report — console, network, dead ends, lying feedback, state corruption
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (`persona_mode: generic`)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 0459f9803b0f — Save fails with HTTP 500 yet shows a "Saved ✓" toast and the note is lost
- **Severity:** P0
- **So what:** Every note a user writes is silently discarded while the UI says it was saved; no user can write a note and find it again.
- **Framework tags:** lying-feedback, failed-request, data-loss
- **Flow:** create-note
- **Locator:** /api/notes
- **Personas hit:** novice, power-user
- **Environment:** personas `novice`, `power-user` · desktop 1440×900 · `http://localhost:8765/app/new.html` · build n/a (manifest records none) · novice `[03:05]` and `[03:50]`, power-user `[01:00]`
- **Expected:** `POST /api/notes` returns 2xx, the note appears under "Your cards" and in search.
- **Actual:** `POST http://localhost:8765/api/notes 500 (Internal Server Error)`; green "Saved ✓" still shown; dashboard still "Nothing here yet."
- **Observed:**
  - Novice saved "Dentist" twice; both POSTs returned 500, both showed "Saved ✓", dashboard stayed empty both times.
  - Power-user saved "Roadmap"; same 500, same toast, search for "Roadmap" returned "No results".
  - Both personas left in the debrief: "it accepts a note and then loses it" (power-user), "the one I wrote disappeared twice" (novice).
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:20` · `persona-novice/console-full.txt:2` · `persona-novice/network-full.txt:5` · `persona-novice/network-full.txt:7` · `persona-power-user/session.log:11` · `persona-power-user/console-full.txt:2` · `persona-power-user/network-full.txt:3`
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me."
  - Note: `04-note-saved-toast.png` actually shows the empty New block form, not the toast. The toast is evidenced by `session.log` only.
- **Repro:**
  1. Sign in, complete signup at `/app/signup.html` (any workspace type), reach `/app/dashboard.html`.
  2. Open `/app/new.html` via "New block".
  3. Enter title "Dentist" and any body text; click Save.
  4. Observe "Saved ✓" toast, redirect to the dashboard, and in the network log `POST /api/notes → 500`.
  5. Dashboard still shows "Nothing here yet."; search "Dentist" returns "No results for 'Dentist'."
  - Server-side cause not visible from the capture; reproducible on both personas in 3 of 3 attempts.
- **Fix:** Fix the 500 in `POST /api/notes`; show the "Saved ✓" toast only on a 2xx response and show an error with the draft retained otherwise.

### 65db4cf73580 — Memories page asserts facts the user never provided, and the novice stopped trusting the product
- **Severity:** P0
- **So what:** Confident false claims about the user's own life made the novice doubt the "Saved" message and stop the session at 06:30.
- **Framework tags:** false-data, trust
- **Flow:** view-memories
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Environment:** persona `novice` · desktop 1440×900 · `http://localhost:8765/app/memories.html` · build n/a · `[04:30]`
- **Expected:** With zero saved notes and no connected accounts, the page shows an empty state or nothing.
- **Actual:** Page lists three claims: "You prefer to schedule meetings on Tuesday afternoons." "Your team uses Jira and Slack." "You are working on a product launch in Q4."
- **Observed:**
  - Footer reads "Memories are built from your notes and connected accounts." The novice had saved no notes and connected no accounts.
  - Novice: "None of that is true." Then questioned whether "Saved" was also made up.
  - Novice ended the session at 06:30 and said in the debrief they would not keep using the product or pay.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25`
  > "None of that is true. I've written one note about a dentist. Where is this from?"
- **Repro:**
  1. Sign up as a new user with no notes and no connected accounts.
  2. Click "Memories" in the top nav (`/app/memories.html`).
  3. Observe the three claims above.
- **Fix:** Render memories only from the user's own saved notes or connected accounts; show an empty state when there are none, and remove the hardcoded sample items.
- **Ambiguity:** P0 vs P1. Rubric names "confident nonsense about the persona's own data" as P0, and the novice's trust collapse was observed, so P0.

### 6ab990e94d83 — Memories page asserts facts the user never provided, and the power-user dismissed it as a demo
- **Severity:** P2
- **So what:** Same false content, but the power-user ruled it a demo panel and carried on; the cost is lower trust, not a stopped session.
- **Framework tags:** false-data, trust
- **Flow:** view-memories
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Environment:** persona `power-user` · desktop 1440×900 · `http://localhost:8765/app/memories.html` · build n/a · `[02:30]`
- **Expected:** An empty state for a workspace with no notes.
- **Actual:** "Tuesday meetings, Jira, Q4 launch" shown as facts about the user.
- **Observed:**
  - Power-user: "Not me. Whatever — a demo panel, I assume. Not going to trust it."
  - Debrief: "It remembers nothing I gave it and claims things I didn't."
  - Severity flip against novice: the power-user's low expectation of this panel kept the damage to one panel.
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/network-full.txt:5`
  > "Not me. Whatever — a demo panel, I assume. Not going to trust it."
  - Note: no power-user screenshot of the Memories page exists; the content is cited from the log and matches `persona-novice/screenshots/06-memories.png`.
- **Repro:**
  1. Sign up as a new user with no notes.
  2. Click "Memories" in the top nav.
  3. Observe the pre-filled claims.
- **Fix:** Same as the novice finding: drive Memories only from the user's own data and show an empty state otherwise.

### 471fcbe6e167 — Dashboard throws uncaught ReferenceError: renderGraphOverlay is not defined on every load
- **Severity:** P3
- **So what:** A script error on every dashboard load; no user-visible effect could be tied to it in this run, but it may hide further breakage.
- **Framework tags:** console-error
- **Flow:** view-dashboard
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Environment:** personas `novice`, `power-user` · desktop 1440×900 · `http://localhost:8765/app/dashboard.html` · build n/a · every dashboard load (novice `[00:55]`, `[03:12]`; power-user `[00:30]`)
- **Expected:** The dashboard loads with no uncaught exceptions.
- **Actual:** `dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined`
- **Observed:**
  - Logged 4 times for the novice and 2 times for the power-user, once per dashboard load.
  - The dashboard still rendered its search box and empty state; no feature visibly depended on it.
  - Cause of the empty list is the failed save, not this error, so it stays P3.
- **Evidence:** `persona-novice/console-full.txt:1` · `persona-novice/console-full.txt:3` · `persona-power-user/console-full.txt:1` · `persona-novice/session.log:12`
  > "dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined"
- **Repro:**
  1. Open `/app/dashboard.html` after signup, with the browser console open.
  2. Observe the `ReferenceError` on load.
- **Fix:** Define or import `renderGraphOverlay` in `dashboard.html`, or remove the call if the graph overlay is not shipped.

---

## Dropped for want of evidence
- Search returns nothing for saved notes — no note was ever stored (500), so search behaviour was never testable; not a separate bug.

## For other lenses
- Irreversible "Federated graph / Sovereign vault / Hybrid mesh" choice before any product view — ux, onboarding.
- Unexplained jargon in Settings ("Enable webhook sync", "Vault attestation") — content.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) — missing feature, ux.
- Cards/blocks naming mismatch between nav and dashboard — content.

## Coverage gaps
- Single device profile (desktop 1440×900); no mobile run.
- Search never tested against stored data.
- Refresh, back-button and multi-tab state not exercised.
- Settings Export button never clicked.

## Appendices
- A. Persona debriefs
- B. Session timelines
- C. Screenshot index
