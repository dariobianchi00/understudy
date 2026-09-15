# Nimbus Notes — bugs findings — Run 2026-09-08 (fixture02)

## Method
- Framework: console errors · failed requests · dead ends · broken states · lying feedback · state corruption
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 260081ca659f — Save reports success while POST /api/notes returns 500 and the note is never persisted
- **Severity:** P0
- **So what:** Both personas wrote a note, were told it saved, and lost it with no error shown — the one objective under test fails every time.
- **Framework tags:** Failed requests, Lying feedback
- **Flow:** shape_2
- **Locator:** /api/notes
- **Personas hit:** novice, power-user
- **Observed:**
  - `POST http://localhost:8765/api/notes` returns `500 (Internal Server Error)` on every save attempt (novice twice, power-user once)
  - Despite the 500, the UI shows a green "Saved ✓" toast and redirects to the dashboard
  - The dashboard "Your cards" list stays "Nothing here yet." and search for the note's title returns "No results" afterward
- **Evidence:** `persona-novice/console-full.txt:3,5` · `persona-novice/network-full.txt:5,7` · `persona-novice/screenshots/04-note-saved-toast.png` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17-20` · `persona-power-user/console-full.txt:2` · `persona-power-user/network-full.txt:3` · `persona-power-user/screenshots/03-search-empty.png` · `persona-power-user/session.log:11`
  > "It is lying to me." — persona-novice/session.log:20
  > "Save doesn't save and search doesn't search. Nothing else matters until those work." — persona-power-user/session.log:15
- **Repro:**
  1. Complete signup with any workspace type, land on empty dashboard.
  2. Click "New block" in the top nav.
  3. Enter a Title and body text, click Save.
  4. Observe "Saved ✓" toast and redirect to dashboard.
  5. Dashboard "Your cards" still shows "Nothing here yet."; search for the title returns "No results".
  6. Check network tab: `POST /api/notes` returned `500`.
- **Fix:** Do not show the "Saved ✓" toast (or navigate away) until the client receives a 2xx from POST /api/notes; surface the 500 as a retryable error instead.

### f4cab459a510 — Memories panel presents fabricated personal claims as fact with zero real notes saved
- **Severity:** P0
- **So what:** The persona is told specific, confident "facts" about their own work habits and team that are entirely invented, while genuinely saved data (zero notes, because saves fail) is ignored — this is the P0-grade "confident nonsense about the persona's own data."
- **Framework tags:** Lying feedback
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Memories page header reads "What Nimbus remembers about you" with the caption "Memories are built from your notes and connected accounts."
  - Three specific claims are shown — "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4." — for an account with zero saved notes and no connected accounts
  - Both personas independently identify the claims as false and state they no longer trust the product
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21-25` · `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the 'Saved' too?" — persona-novice/session.log:22
  > "Memories aren't mine. A demo panel, I assume. Not going to trust it." — persona-power-user/session.log:14
- **Repro:**
  1. Complete signup with any workspace type (no notes need to have saved successfully).
  2. Click "Memories" in the top nav.
  3. Observe three specific personal claims displayed as fact, captioned as built from "your notes and connected accounts."
- **Fix:** Replace the fabricated demo content with either a genuine empty state ("Memories build up as you add notes") or clearly label it as a sample/preview panel, not real data.

### e1ffc10b114c — Uncaught ReferenceError: renderGraphOverlay is not defined fires on every dashboard load
- **Severity:** P3
- **So what:** A JS exception fires on the app's main screen on every load; no visible symptom was confirmed this run, but it indicates broken code shipping on the primary surface.
- **Framework tags:** Console errors
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - `Uncaught ReferenceError: renderGraphOverlay is not defined` logged at `dashboard.html:1` on every dashboard load (3 occurrences for novice, 2 for power-user)
  - Dashboard screenshots (`02-dashboard-empty.png`, `05-notes-list-missing.png`, `02-dashboard.png`) show no visible graph overlay element and no other rendering anomaly
  - Neither persona's session.log or debrief mentions a visual glitch on the dashboard
- **Evidence:** `persona-novice/console-full.txt:1,2,4,6` · `persona-power-user/console-full.txt:1,3` · `persona-novice/screenshots/02-dashboard-empty.png` · `persona-power-user/screenshots/02-dashboard.png`
- **Repro:**
  1. Load /app/dashboard.html (e.g. right after signup, or after any save/redirect back to dashboard).
  2. Open the browser console.
  3. Observe `Uncaught ReferenceError: renderGraphOverlay is not defined` on each load.
- **Fix:** Define or remove the `renderGraphOverlay` call in dashboard.html; if it powers a graph-workspace visualization, confirm it should be rendering something for Federated graph / Hybrid mesh workspace types and restore it.

---

## Dropped for want of evidence
- Search may not work even when notes exist — no evidence this run, because no save ever persisted a note to search for.

## For other lenses
- Irreversible, jargon-laden workspace-type choice at signup ("Federated graph", "Sovereign vault", "Hybrid mesh") before any product value is shown — onboarding/UX.
- "Cards" vs "New block" vs "notes" naming inconsistency across nav and copy — content/UX.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) despite power-user expecting keyboard-driven use — UX.
- Settings toggles ("Enable webhook sync", "Vault attestation", "Federated graph replication") unexplained, and unclear relation to the signup workspace-type choice — content/UX.

## Coverage gaps
- Cards list and search were never exercised against real, persisted data — the save failure blocked that path for both personas.
- "Cards" navigation item was never opened by either persona (both used "New block" then relied on the dashboard's own list).

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index — `persona-novice/screenshots/`, `persona-power-user/screenshots/`
