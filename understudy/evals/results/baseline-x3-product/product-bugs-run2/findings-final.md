# Nimbus Notes — bugs findings — Run 2026-09-08 (fixture02)

## Method
- Framework: console/network evidence correlated with persona-observed impact
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### e8eb77359df0 — Save reports success while the note is silently dropped
- **Severity:** P0
- **So what:** Both personas lost their only note, were told it saved, and abandoned the product within minutes.
- **Framework tags:** Failed request, Lying feedback, State corruption
- **Flow:** shape_2
- **Locator:** /api/notes
- **Personas hit:** novice, power-user
- **Observed:**
  - `POST http://localhost:8765/api/notes` returns `500 (Internal Server Error)` every time a note is saved.
  - UI shows a green "Saved ✓" toast regardless of the 500.
  - Dashboard and search return no trace of the note afterward ("Nothing here yet." / "No results for 'Dentist'").
- **Evidence:** `persona-novice/console-full.txt:3` · `persona-novice/network-full.txt:5` · `persona-novice/screenshots/04-note-saved-toast.png` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/network-full.txt:3` · `session.log` novice `[03:05]`–`[03:50]`, power-user `[01:00]`
  > "[error] new.html:1 POST http://localhost:8765/api/notes 500 (Internal Server Error)"
  > "Saved twice, empty twice. It is lying to me." — novice session.log [03:50]
- **Repro:**
  1. Complete signup, land on empty dashboard.
  2. Click "New block", enter a title and body, click Save.
  3. Observe "Saved ✓" toast appears; network tab shows `POST /api/notes` returning 500.
  4. Return to dashboard: "Your cards" — "Nothing here yet." Search for the title: "No results."
- **Fix:** Make the save toast reflect the actual request outcome; surface an error and retain the draft when `/api/notes` returns 500. Fix the 500 itself server-side.

### 78d578180c5a — Memories panel presents fabricated personal facts as real
- **Severity:** P1
- **So what:** The persona sees confident claims about their own habits and tools that are entirely false, and stops trusting any other feedback the product gives (including "Saved").
- **Framework tags:** Lying feedback, Broken state
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Memories screen states "You prefer to schedule meetings on Tuesday afternoons," "Your team uses Jira and Slack," "You are working on a product launch in Q4" for accounts that contain zero saved notes.
  - Neither persona ever provided this information; novice had written exactly one (failed) note about a dentist appointment.
  - No label distinguishes this as sample/demo content.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `session.log` novice `[04:30]`–`[04:50]` · `persona-debrief.md` novice Q4 · `persona-power-user/session.log:[02:30]`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the 'Saved' too?" — novice session.log [04:50]
  > "Not me. Whatever — a demo panel, I assume. Not going to trust it." — power-user session.log [02:30]
- **Repro:**
  1. Create a new workspace with no notes saved.
  2. Open the "Memories" surface from the top menu.
  3. Observe fabricated personal statements presented without a demo/sample disclaimer.
- **Fix:** Remove placeholder "memory" content for accounts with no data, or clearly label it as example content until the account has real history.

### 82757f0242fd — Uncaught ReferenceError floods console on every dashboard load
- **Severity:** P2
- **So what:** Signals an unhandled JS failure on the dashboard; may be masking or contributing to other broken rendering (e.g. the graph overlay never appears).
- **Framework tags:** Console error
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - `dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined` fires on every dashboard load for both personas (3 occurrences for novice, 2 for power-user).
  - No visible UI element (graph overlay) appears where this function was presumably meant to render.
  - Error recurs identically after each save-and-return-to-dashboard cycle.
- **Evidence:** `persona-novice/console-full.txt:1,2,4,6` · `persona-power-user/console-full.txt:1,3`
  > "[error] dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined"
- **Repro:**
  1. Sign up and land on the dashboard.
  2. Open browser console.
  3. Observe `Uncaught ReferenceError: renderGraphOverlay is not defined` on load, and again after any navigation back to the dashboard.
- **Fix:** Define or remove the `renderGraphOverlay` call in dashboard.html; ship the intended graph overlay or delete the dead reference.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- None — all observed anomalies had corroborating log/console/network/screenshot evidence.

## For other lenses
- Irreversible workspace-type choice ("Federated graph / Sovereign vault / Hybrid mesh," cannot be changed later) presented before the persona has seen the product — onboarding/ux.
- Jargon-heavy settings labels ("Enable webhook sync," "Federated graph replication," "Vault attestation") with no explanation — content/ux.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, `/` all no-ops) despite power-user expectation of "keyboard-driven" — ux.
- Ambiguous terminology: "Cards," "New block," and "notes" used interchangeably in the UI — content/ux.
- Unclear relationship between the signup-time workspace choice and the identically-worded "Federated graph replication" settings toggle — ux.

## Coverage gaps
- Novice persona never reached a state with more than one note attempted; multi-note organization/search-with-data untested.
- No mobile or non-desktop viewport tested (both personas ran desktop-1440x900).
- Export ("Markdown, all cards") button was seen but never clicked by either persona — its behavior is unverified.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json`, `persona-power-user/timeline.json`, `persona-novice/session.log`, `persona-power-user/session.log`
- C. Screenshot index — `persona-novice/screenshots/`, `persona-power-user/screenshots/`
