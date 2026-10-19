# Nimbus Notes — onboarding findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer C activation (C-TTFV, C-STEPS, C-ABANDON, C-SOWHAT), with Layer A tags where they apply
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on personas the agent invented
- Scoring model: opus
- Every finding cites an artifact; unsupported observations are dropped and listed at the end
- Auth wall at `/app/login.html` excluded; the clock starts after it (novice waited 70 s, power-user 40 s, not scored)

---

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached entry point (`/app/signup.html`) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen, workspace created | ✓ 00:55 | ✓ 00:30 |
| Opened "New block" and wrote a note | ✓ 01:55 | ✓ 01:00 |
| Micro-value: live word count and preview | ✓ 02:41 (retracted in debrief) | — not remarked |
| Note persisted (shown in "Your cards") | ✗ 03:05 and 03:50, POST 500 both times | ✗ 01:00, POST 500 |
| **First value: note found again** | ✗ | ✗ |
| Outcome | **Abandoned 06:30**: "I'd stop here." | **Abandoned 03:00**: "Enough." |

- **Steps to value (product-required):** 5 (pick type → Create workspace → New block → write → Save), then find it. No step 6 is possible.
- **Time to value:** not reached. Capture logged 02:41 for the novice's preview moment. In the debrief she says the product does "nothing".
- **Drop-off:** both personas drop at the same point: right after "Saved ✓", back on the empty "Your cards" list.
- **Abandonment, not time-out:** both quit on their own with 84+ minutes of the 90-minute cap left.
- **Wandering:** the novice took about 9 steps (a search for "meeting" with no notes yet, two save attempts, Memories, Settings). `times_had_to_hunt`: novice 2, power-user 1.

---

## Findings

### 632bacc49f01 — Save reports "Saved ✓" while POST /api/notes fails with 500, so no note survives
- **Severity:** P0
- **So what:** Every persona's first note was lost with a success message, so activation is 0 of 2 and both quit at this screen.
- **Framework tags:** A1, A9, C-TTFV, C-ABANDON
- **Flow:** shape_2
- **Locator:** /api/notes
- **Personas hit:** novice, power-user
- **Observed:**
  - Save shows a green "Saved ✓" and returns to a dashboard that still reads "Nothing here yet."
  - The network log shows `POST /api/notes → 500` on all 3 saves (novice 03:05 and 03:50, power-user 01:00).
  - Searching the saved title returns "No results". Both personas abandoned within 3 minutes.
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:20` · `persona-novice/network-full.txt` (POST /api/notes → 500 ×2) · `persona-power-user/session.log:11` · `persona-power-user/session.log:15` · `persona-power-user/network-full.txt` (POST /api/notes → 500) · `persona-novice/timeline.json` objectives[0].gave_up = true
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me." (novice)
  > "Enough. Save doesn't save and search doesn't search. Nothing else matters until those work." (power-user)
- **Repro:**
  1. Clear the login wall and create any workspace type.
  2. Click "New block", enter a title and body, then click Save.
  3. Observe the "Saved ✓" toast, then the dashboard reading "Nothing here yet.", and a 500 on `POST /api/notes`.
- **Fix:** Fix the 500 on `POST /api/notes`. Show "Saved ✓" only after a 2xx response, and show a retry error otherwise.

### da021f1801a8 — Memories page presents invented facts as "What Nimbus remembers about you"
- **Severity:** P1
- **So what:** Made-up personal facts turned a failed save into active distrust: the novice concluded "Saved" was also a lie and stopped.
- **Framework tags:** A1, A2, C-ABANDON, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Observed:**
  - The page lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - The footer says "Memories are built from your notes and connected accounts." No accounts were connected, and no notes were stored.
  - Both personas cite it in their Q4 promise-match answer ("aren't mine", "claims things I didn't").
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25` · `persona-power-user/session.log:14` · `persona-novice/persona-debrief.md` Q4 · `persona-power-user/persona-debrief.md` Q4
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?" (novice)
  > "Not me. Whatever — a demo panel, I assume. Not going to trust it." (power-user)
- **Repro:**
  1. Create a fresh workspace with no connected accounts.
  2. Open "Memories" from the top nav.
  3. Observe 3 specific claims about the user that come from no input.
- **Fix:** For new workspaces, show an empty state on Memories ("Nothing yet — memories appear after you write notes") and remove the seeded statements.

### d661b00d16f9 — Signup forces an irreversible workspace-type choice in unexplained jargon before the product is seen
- **Severity:** P2
- **So what:** The novice spent 43 s on the first screen and guessed. A less persistent first-timer stops here, before seeing anything.
- **Framework tags:** A2, A10, C-STEPS, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - The heading reads "Before we begin, choose your workspace type", with "Federated graph", "Sovereign vault" and "Hybrid mesh" offered and no descriptions.
  - The page states "This cannot be changed later."
  - The novice picked "Hybrid mesh" by guessing at 00:48. The power-user picked in seconds: "Fine — I've seen worse." That is a severity flip.
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-power-user/session.log:8`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo." (novice)
- **Repro:**
  1. Clear the login wall and land on `/app/signup.html`.
  2. Read the three options and the "This cannot be changed later." note.
- **Fix:** Default to one workspace type and drop the step from signup. If it must stay, add one plain-language line per option and make the choice changeable.

### 7a1a8f629e99 — Empty dashboard says "Nothing here yet." with no next step toward a first note
- **Severity:** P2
- **So what:** It contradicts "never start from zero". The novice searched an empty product before finding "New block", costing about 45 s.
- **Framework tags:** A6, A10, C-TTFV
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" shows only "Nothing here yet.", with no button and no prompt to write a first note.
  - At 01:20 the novice searched "meeting" in an empty workspace, then reached "New block" at 01:40.
  - The power-user was not slowed down. This is a flip by persona.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/timeline.json` shape_2.times_had_to_hunt = 2
  > "Dashboard. "Your cards" — "Nothing here yet." … Nothing tells me what to do. I thought it would have my stuff." (novice)
- **Repro:**
  1. Create a workspace.
  2. Land on `/app/dashboard.html` and look for a first action inside the "Your cards" panel.
- **Fix:** Replace "Nothing here yet." with "Write your first note" and a button that opens `/app/new.html`.

### cdb2b814ed7c — Three names for one object — "New block", "Your cards", "Search your notes" — slow the path to the first note
- **Severity:** P2
- **So what:** The novice could not tell whether "New block" made a note, adding hesitation on the one required creation step.
- **Framework tags:** A4, A2, C-STEPS
- **Flow:** shape_2
- **Locator:** nav: New block
- **Personas hit:** novice
- **Observed:**
  - The nav reads "Cards" and "New block". The dashboard reads "Your cards" with the placeholder "Search your notes".
  - At 01:40 the novice asked whether cards and blocks are the same thing before clicking "New block".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14`
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing? Clicked "New block"." (novice)
- **Repro:**
  1. Open `/app/dashboard.html`.
  2. Compare the nav labels, the panel heading and the search placeholder.
- **Fix:** Pick one noun ("note") and rename "New block" to "New note" and "Your cards" to "Your notes".

### 87e3d074b5f9 — Signup choice "Federated graph" resurfaces as an unexplained Settings toggle
- **Severity:** P3
- **So what:** It undermines the "cannot be changed later" warning and leaves the evaluator unsure what signup actually decided.
- **Framework tags:** A4, A2
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** power-user
- **Observed:**
  - Settings shows "Federated graph replication" checked by default, beside "Enable webhook sync" and "Vault attestation".
  - Nothing connects it to the signup choice of "Federated graph".
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-power-user/session.log:13`
  > ""Federated graph replication" is on by default. I picked that at signup — is this the same thing?" (power-user)
- **Repro:**
  1. At signup, pick "Federated graph".
  2. Open Settings and find "Federated graph replication" already checked.
- **Fix:** Show the signup workspace type read-only in Settings, and add a one-line description to each toggle.

### 7f8e67f1c55a — No keyboard shortcuts for capture or search for a keyboard-driven evaluator
- **Severity:** P3
- **So what:** It misses the power-user's stated "keyboard-driven" expectation, but it did not cause his exit.
- **Framework tags:** A7
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** power-user
- **Observed:**
  - Ctrl+K, Ctrl+N and / all did nothing at 01:30.
  - His pre-session expectation was "fast capture, good search, keyboard-driven".
- **Evidence:** `persona-power-user/session.log:3` · `persona-power-user/session.log:12` · `persona-power-user/screenshots/02-dashboard.png`
  > "Tried keyboard: Ctrl+K, Ctrl+N, / — nothing. No shortcuts." (power-user)
- **Repro:**
  1. On the dashboard, press Ctrl+K, Ctrl+N or /.
  2. Observe that nothing happens.
- **Fix:** Bind / to focus search and Ctrl+N to open "New block", and list both shortcuts in the nav tooltips.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast as a visual: `persona-novice/screenshots/04-note-saved-toast.png` shows an empty New block form with no toast. The toast rests on `session.log:17` and `:20` only.
- The power-user's search for "Roadmap" as a visual: `persona-power-user/screenshots/03-search-empty.png` shows an empty search box with no query. The search rests on `session.log:11`.
- "Search doesn't search": no stored note existed to find, so search could not be tested on its own.

## For other lenses
- `POST /api/notes` returns 500 and the console logs `renderGraphOverlay is not defined` on every dashboard load. → bugs
- Settings labels "Enable webhook sync", "Federated graph replication" and "Vault attestation" are unexplained to the novice (`persona-novice/session.log:23`). → content / ux
- Settings checkboxes sit centred, away from their labels (`persona-novice/screenshots/07-settings.png`). → ux

## Coverage gaps
- Neither persona returned for a second task. Retention cannot be observed.
- Export → Markdown was seen but never clicked.
- Mobile was not tested; both runs were desktop 1440×900.
- Search on a stored note was never tested because nothing persisted.

## Appendices
- A. Persona debriefs: `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines: `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index: novice `00-start` … `07-settings` (8) · power-user `00-start`, `02-dashboard`, `03-search-empty`, `07-settings` (4). All were opened for this report.
