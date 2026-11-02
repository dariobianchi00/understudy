# Nimbus Notes — onboarding findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer C activation (C-TTFV, C-STEPS, C-ABANDON, C-SOWHAT), funnel-first
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on invented personas
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached signup (after auth wall) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen | ✓ 00:48 (43 s hesitation) | ✓ before 00:30 |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| Note written | ✓ 02:41 | ✓ 01:00 |
| Note stored by server | ✗ 03:05 and 03:50 — `POST /api/notes → 500`, UI said "Saved ✓" | ✗ 01:00 — `POST /api/notes → 500`, UI said "Saved ✓" |
| **First value: note found again** | ✗ list empty 03:12, search empty 03:30 | ✗ list and search empty 01:00 |
| Outcome | **Abandoned** 06:30 — "I'd stop here" | **Abandoned** 03:00 — "Enough." |

**Steps to value (required path):** 6 — pick workspace type · Create workspace · New block · write · Save · find on dashboard/search — never completed · **Time to value:** not reached (0 of 2) · **Drop-off:** Save → note never appears

- Both personas **abandoned**; neither timed out. Cap was 90 min; they quit at 06:30 and 03:00.
- `timeline.json` records novice first value at 02:41 (161 s) — the live word count/preview.
- That value did not survive: novice debrief Q1 — "right now: nothing". Treat as provisional, retracted by the persona.
- Novice wandered: searched "meeting" on an empty account (01:20) and rewrote the note (03:50) — 2 hunts in `timeline.json`.

---

## Findings

### e53e15315b2c — Save confirms success while the note is never stored, so no first note survives
- **Severity:** P0
- **So what:** 100% of personas lost their first note and quit; the product's one job fails at the first attempt.
- **Framework tags:** C-TTFV, C-ABANDON, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Save shows "Saved ✓" while `POST http://localhost:8765/api/notes` returns 500 (novice 03:05, 03:50; power-user 01:00).
  - Dashboard then shows "Nothing here yet."; searching the note's title returns no results.
  - Novice retried once, then concluded "It is lying to me"; power-user quit at 03:00.
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-power-user/session.log:11` · `persona-power-user/session.log:15` · `persona-novice/network-full.txt` (`[POST] /api/notes → 500 internal error (03:05)`) · `persona-power-user/network-full.txt` (`[POST] /api/notes → 500 internal error (01:00)`) · `timeline.json` objectives `gave_up: true` (both)
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me." — novice
  > "Save doesn't save and search doesn't search. Nothing else matters until those work." — power-user
- **Repro:**
  1. Sign up, pick any workspace type, click "Create workspace".
  2. Click "New block", enter a title and body, click "Save".
  3. Observe "Saved ✓"; check network — `POST /api/notes` returns 500.
  4. Dashboard shows "Nothing here yet."; search the title — "No results".
- **Fix:** Fix the 500 on `POST /api/notes`, and show the "Saved ✓" toast only after a 2xx; on failure, keep the draft and show a retry error.

### 4951081cf771 — Memories page asserts invented facts about a brand-new user, turning one lost note into total distrust
- **Severity:** P0
- **So what:** Fabricated "memories" made the novice doubt every other success message; both personas said they would not trust it.
- **Framework tags:** C-ABANDON, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Observed:**
  - "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footnote claims "Memories are built from your notes and connected accounts." — both accounts held zero stored notes and no connections.
  - Torn P0/P1: rubric names "confident nonsense about the persona's own data" as P0; it did not cause the first drop, it deepened it.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-power-user/session.log:14` · `persona-novice/persona-debrief.md` Q4
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?" — novice
  > "the "memories" it does have aren't mine." — novice debrief Q4
- **Repro:**
  1. Create a new account; save no notes (or attempt one — it fails).
  2. Click "Memories" in the top nav.
  3. Observe three specific claims about the user with no source.
- **Fix:** Show an empty state on /app/memories.html until real notes exist, and link each memory to the note it came from.

### 3afacad255ae — Signup forces an irreversible, unexplained workspace-type choice before the novice has seen the product
- **Severity:** P2
- **So what:** Novice spent 43 s guessing at jargon under "This cannot be changed later."; a less patient user stops here.
- **Framework tags:** C-STEPS, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - "Before we begin, choose your workspace type" offers "Federated graph", "Sovereign vault", "Hybrid mesh" with no descriptions.
  - "This cannot be changed later." sits under the options; no default, no help link.
  - Novice guessed "Hybrid mesh" at 00:48; power-user picked in under 30 s — severity flip (non-issue for power-user).
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-power-user/session.log:8`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo." — novice
- **Repro:**
  1. Clear the login wall; land on /app/signup.html.
  2. Read the three options and the "This cannot be changed later." line.
- **Fix:** Default the workspace type silently and move the choice to Settings, or add one-line plain-English descriptions and make it changeable.

### c7d77c8d9a7b — Empty dashboard gives a new user no next step and contradicts the never-start-from-zero promise
- **Severity:** P2
- **So what:** Novice arrived expecting her stuff, got "Nothing here yet." and no prompt, and spent 45 s searching an empty account.
- **Framework tags:** C-STEPS, C-SOWHAT
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" shows only "Nothing here yet." — no button, hint, or import option.
  - Novice searched "meeting" on an empty account at 01:20 before finding "New block" at 01:40.
  - Power-user expected an empty account ("Expected, nothing's in it yet.") — non-issue for them; severity flip.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:1` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-power-user/session.log:10`
  > "Nothing tells me what to do. I thought it would have my stuff." — novice
- **Repro:**
  1. Create a workspace.
  2. Land on /app/dashboard.html and look for a next action inside "Your cards".
- **Fix:** Put a "Write your first note" button inside the "Your cards" empty state, plus an import option if "never start from zero" stays in marketing.

### e7ba02e91c5a — Notes, cards and blocks name one object three ways, sending the novice hunting for where to write
- **Severity:** P2
- **So what:** The novice could not tell which nav item creates a note; vocabulary drift adds a hunt to the shortest path to value.
- **Framework tags:** C-STEPS
- **Flow:** shape_1
- **Locator:** Cards / New block nav
- **Personas hit:** novice
- **Observed:**
  - Nav reads "Cards", "New block"; the search field reads "Search your notes"; the list is headed "Your cards".
  - Novice asked whether cards and blocks are the same, then guessed "New block".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json` (01:40)
  > "Cards and blocks — same thing? Clicked "New block"." — novice
- **Repro:**
  1. On /app/dashboard.html read the top nav, the search placeholder and the list heading.
  2. Try to identify the control that creates a note.
- **Fix:** Use one noun everywhere — rename "New block" to "New note", "Your cards" to "Your notes", and "Cards" nav to "Notes".

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast itself — `persona-novice/screenshots/04-note-saved-toast.png` shows an empty New block form, not the toast; toast rests on `session.log:17` and network only.
- Live preview as first value — `03-new-note.png` shows "0 words" and an empty form, so the preview moment is not visually captured.

## For other lenses
- `POST /api/notes` returns 500; `renderGraphOverlay is not defined` on every dashboard load (console) — bugs.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, `/` do nothing) — power-user `session.log:12` — ux.
- Settings jargon "Enable webhook sync", "Federated graph replication", "Vault attestation"; unclear link to the signup choice — content.
- Settings checkboxes render above their labels, centred; signup radios likewise — ux.

## Coverage gaps
- No persona ever had a stored note, so search, the cards list, and Export were never exercised with data.
- Export ("Markdown, all cards") was seen but not clicked.
- Return visit / second task never reached.
- Desktop 1440×900 only; no mobile.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice: 00-start, 00-wall-cleared, 01-signup-workspace-type, 02-dashboard-empty, 03-new-note, 04-note-saved-toast (shows empty form), 05-notes-list-missing, 06-memories, 07-settings · power-user: 00-start, 02-dashboard, 03-search-empty, 07-settings
