# Nimbus Notes — onboarding findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer C activation (C-TTFV, C-STEPS, C-ABANDON, C-SOWHAT), with Layer A tags where they explain the drop
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on personas the agent invented
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Auth wall at `/app/login.html` excluded per manifest; clock starts after it

---

## Funnel

| Stage (as the product imposed it) | novice | power-user |
|---|---|---|
| Reached signup (after auth wall) | ✓ 00:00 | ✓ 00:00 |
| Chose irreversible workspace type → dashboard | ✓ 00:55 (43 s deciding) | ✓ 00:30 |
| Opened "New block" form | ✓ 01:55 (after 1 failed search + menu hunt) | ✓ ~01:00 |
| Live word count / preview while typing | ✓ 02:41 (capture's TTFV) | not recorded |
| Clicked Save, saw "Saved ✓" | ✓ 03:05 (and again 03:50) | ✓ 01:00 |
| Note visible in "Your cards" or search | ✗ 03:12 — empty; search "Dentist" no results | ✗ 01:00 — empty; search "Roadmap" no results |
| **First value (persona's judgement)** | ✗ — "right now: nothing" | ✗ — "Nothing yet" |
| Would return | ✗ "No. Nothing, until saving works." | ✗ "No. Nothing." |

- **Required steps to the objective:** 6 — workspace type → Create workspace → New block → title/body → Save → find in list/search
- **Steps taken:** novice ~9 (search on empty board, menu hunt, second save, Memories, Settings); power-user ~8 (shortcut attempts, Settings, Memories)
- **Time to value:** not reached by either persona
- **Capture-recorded TTFV:** novice 02:41 (`timeline.json` shape_2.seconds_to_first_value = 161) — a live preview, revoked by the persona 31 s later
- **Drop-off:** both at "Note visible in list/search", after a false "Saved ✓"
- **Abandonment, not time-out:** novice quit at 06:30, power-user at 03:00 — against a 90-minute cap
- **Permission prompts:** 0 for both

---

## Findings

### e7aa532cf05b — Save confirms "Saved ✓" but the note is never stored, so neither persona reached first value
- **Severity:** P0
- **So what:** The core job fails behind a success message; both personas abandoned within 7 minutes and said they would not return.
- **Framework tags:** A1, A9, C-TTFV, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Save shows "Saved ✓", returns to dashboard; "Your cards" still reads "Nothing here yet."
  - Every save POSTs to `/api/notes` → 500 (novice at 03:05 and 03:50; power-user at 01:00)
  - Search for the saved title returns "No results"; novice retried once, then quit at 06:30
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:20` · `persona-novice/network-full.txt` · `persona-power-user/screenshots/03-search-empty.png` · `persona-power-user/session.log:11` · `persona-power-user/network-full.txt` · `timeline.json` objectives[0].gave_up = true (both)
  > "Saved twice, empty twice. It is lying to me." (novice)
  > "Enough. Save doesn't save and search doesn't search. Nothing else matters until those work." (power-user)
  - Note: `04-note-saved-toast.png` shows an empty New block form, not the toast; the toast rests on `session.log:17`
- **Repro:**
  1. Create a workspace, click "New block"
  2. Enter a title and body, click Save
  3. Observe "Saved ✓", then the empty "Your cards" list; search the title
- **Fix:** Make POST /api/notes succeed, and show "Saved ✓" only on a 2xx — show an error with Retry otherwise.

### da021f1801a8-a — Memories page presents invented facts as "What Nimbus remembers about you"
- **Severity:** P1
- **So what:** The novice read fabricated memories as proof the product lies, and extended that distrust to the "Saved" message.
- **Framework tags:** A1, B-G2, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - Page lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer claims "Memories are built from your notes and connected accounts." — novice had saved no note and connected nothing
  - Novice decided to stop 100 s later; debrief Q4 cites the memories as a reason the promise failed
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:22` · `persona-novice/session.log:25` · `persona-novice/persona-debrief.md`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Create a fresh workspace without saving any note
  2. Click "Memories"
- **Fix:** On a new workspace, replace sample memories with an empty state: "Nimbus will remember things here once you've written a few notes."

### da021f1801a8-b — Memories page presents invented facts as "What Nimbus remembers about you"
- **Severity:** P2
- **So what:** The power-user dismissed it as a demo panel and kept going, but now distrusts the product's headline feature.
- **Framework tags:** A1, B-G2
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same three invented memories on a fresh workspace
  - Persona shrugged it off in-flight; raised it again in debrief Q4
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md` · `persona-novice/screenshots/06-memories.png` (same page; power-user captured no screenshot of it)
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Create a fresh workspace
  2. Click "Memories"
- **Fix:** Label any sample content "Example" explicitly, or remove it until real notes exist.

### b0a42de524ff — Signup forces an irreversible workspace-type choice in undefined jargon before the product is shown
- **Severity:** P2
- **So what:** The novice's first decision was a blind, permanent guess; a less patient user stops here before seeing anything.
- **Framework tags:** A2, A6, C-STEPS, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - "Before we begin, choose your workspace type": "Federated graph", "Sovereign vault", "Hybrid mesh" — no descriptions, no default
  - "This cannot be changed later." under the options
  - Novice took 43 s (00:05–00:48) and guessed "Hybrid mesh" because "it sounds like it includes the other two"
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the auth wall, land on `/app/signup.html`
  2. Read the three options and the irreversibility note
- **Fix:** Default the workspace type silently and move the choice to Settings, or add a one-line plain-English description under each option.

### afd3bb73856d — Empty dashboard says only "Nothing here yet." and offers no first step
- **Severity:** P2
- **So what:** The novice's first action was searching an empty board; 45 s lost before finding how to write a note.
- **Framework tags:** A6, A10, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" panel shows only "Nothing here yet." — no button, no hint
  - Novice searched "meeting" (01:20), got no results, then scanned the top menu (01:40)
  - `timeline.json` shape_2.times_had_to_hunt = 2
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/findings-raw.json`
  > "'Nothing here yet.' Nothing tells me what to do."
- **Repro:**
  1. Create a workspace
  2. Look at the dashboard
- **Fix:** Put a "Write your first note" button inside the empty "Your cards" panel that opens `/app/new.html`.

### c5daf3015622 — Three names for one object (cards, blocks, notes) sent the novice hunting for how to write
- **Severity:** P2
- **So what:** The novice had to guess that "New block" makes the "note" the search box looks for; adds a hunt to a 6-step path.
- **Framework tags:** A2, A4, C-STEPS
- **Flow:** shape_2
- **Locator:** nav.top
- **Personas hit:** novice
- **Observed:**
  - Top nav: "Cards", "New block"; search placeholder: "Search your notes"; list heading: "Your cards"
  - Novice paused at 01:40 asking whether cards and blocks are the same, then clicked "New block"
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14`
  > "Cards, blocks, notes — are these the same thing?"
- **Repro:**
  1. Open the dashboard
  2. Compare the nav labels, search placeholder and list heading
- **Fix:** Use "note" everywhere: rename nav to "Notes" and "New note", heading to "Your notes".

### b80115246ec4 — Workspace starts empty despite the "never start from zero" promise, with no import or connect step
- **Severity:** P2
- **So what:** The novice arrived expecting her existing material pulled in; the blank start contradicted the pitch before any bug appeared.
- **Framework tags:** C-SOWHAT, C-TTFV
- **Flow:** shape_1
- **Locator:** /app/dashboard.html#cards
- **Personas hit:** novice
- **Observed:**
  - Pre-session expectation: "a notes app that fills itself in from things I already have"
  - First screen after signup: "Nothing here yet."; no import or connect offer anywhere in the observed path
  - Debrief Q4: "No — it started completely empty"
- **Evidence:** `persona-novice/session.log:3` · `persona-novice/session.log:12` · `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/persona-debrief.md`
  > "I thought it would have my stuff."
- **Repro:**
  1. Arrive from the marketing line "remembers everything so you never start from zero"
  2. Create a workspace and land on the dashboard
- **Fix:** Add an import step after workspace creation (paste, upload Markdown, connect a source), or soften the marketing line.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- "Saved ✓" toast appearance — `04-note-saved-toast.png` shows the empty form, not the toast; the finding rests on the log instead
- Power-user search result for "Roadmap" — `03-search-empty.png` shows an empty dashboard with no query or "No results" text visible; the log carries it

## For other lenses
- POST `/api/notes` → 500 and `renderGraphOverlay is not defined` on every dashboard load — bugs
- No keyboard shortcuts (Ctrl+K, Ctrl+N, / do nothing) for a persona expecting "keyboard-driven" — ux
- Settings labels "Enable webhook sync", "Federated graph replication", "Vault attestation" unexplained; power-user could not tell if the toggle is his signup choice — content
- Radio buttons on signup and checkboxes in Settings render centred, detached from their labels — ux

## Coverage gaps
- No persona reached a second task: nothing saved, so retrieval, editing and export were never exercised
- Export ("Markdown, all cards") seen, not clicked
- Desktop 1440×900 only; no mobile
- No price in the target; TTFV judged against consumer self-serve

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice: 00-start, 00-wall-cleared, 01-signup-workspace-type, 02-dashboard-empty, 03-new-note, 04-note-saved-toast (shows empty form), 05-notes-list-missing, 06-memories, 07-settings · power-user: 00-start, 02-dashboard, 03-search-empty, 07-settings
