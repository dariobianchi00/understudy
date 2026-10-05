# Nimbus Notes — onboarding findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer C activation (C-TTFV, C-STEPS, C-ABANDON, C-SOWHAT), with Layer A tags where relevant
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on inferred personas
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Clock starts after the login wall (excluded: "The login wall at /app/login.html — infrastructure, not a defect.")

---

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached entry point (after wall) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen (forced, irreversible) | ✓ 00:48 | ✓ ~00:00–00:30 |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| New block opened, note typed | ✓ 01:55 | ✓ 01:00 |
| Capture-recorded first value (live preview) | ✓ 02:41 | ✗ |
| **Note saved and visible in "Your cards"** | ✗ 03:12 (×2 attempts) | ✗ 01:00 |
| Note found by search | ✗ 03:30 | ✗ 01:00 |
| Returned to a second task | ✗ abandoned 06:30 | ✗ abandoned 03:00 |

**Steps to value (product-required):** 5 — choose workspace type → Create workspace → New block → type → Save · **Time to value:** never reached durably by either persona · **Drop-off:** Save on `/app/new.html` — POST `/api/notes` → 500 while UI says "Saved ✓"

- Both personas **abandoned**; neither timed out — novice at 06:30, power-user at 03:00, against a 90-minute cap
- Novice's timeline records first value at 161 s (02:41, the live word-count/preview); her debrief revokes it: "right now: nothing"
- Novice wandered: searched an empty dashboard at 01:20 before finding "New block" — `times_had_to_hunt: 2`
- Objective "A new user can write a note and find it again": **failed for 2/2 personas**

---

## Findings

### 9ca4d57c250b — Note save shows "Saved ✓" but the server rejects it, so every first note is lost
- **Severity:** P0
- **So what:** Every new user's first note silently vanishes; both personas quit here and the novice concluded "It is lying to me."
- **Framework tags:** A1, A9, C-TTFV, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Save fires POST /api/notes → 500 (novice 03:05 and 03:50; power-user 01:00), yet a green "Saved ✓" appears
  - Dashboard then shows "Your cards" — "Nothing here yet."; search for the title returns "No results"
  - Novice retried once and abandoned; power-user abandoned after one try: "Save doesn't save and search doesn't search."
- **Evidence:** `persona-novice/network-full.txt` · `persona-novice/console-full.txt` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-power-user/network-full.txt` · `persona-power-user/screenshots/03-search-empty.png` · `persona-power-user/session.log:11` · `persona-power-user/session.log:15`
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me."
- **Repro:**
  1. Sign up, choose any workspace type, click "Create workspace"
  2. Click "New block", enter a title and body, click "Save"
  3. Observe "Saved ✓" toast; network shows POST /api/notes → 500
  4. Dashboard shows "Nothing here yet."; search the title → "No results"
- **Fix:** Make POST /api/notes succeed, and show "Saved ✓" only on a 2xx response — on failure keep the draft and show a retry error.

### 2f70097354b0-a — Memories page asserts facts about the user that they never gave it
- **Severity:** P1
- **So what:** Fabricated "memories" turned the novice's lost note into distrust of the whole product; she stopped minutes later.
- **Framework tags:** A1, B-G11, C-ABANDON, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer claims "Memories are built from your notes and connected accounts." — she had zero saved notes and no connected accounts
  - Novice linked it to the save failure, then quit at 06:30
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25` · `persona-novice/persona-debrief.md`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Create a fresh workspace with no notes and no connected accounts
  2. Click "Memories"
  3. Observe three specific claims about the user
- **Fix:** On /app/memories.html, show an empty state ("Nimbus will learn from your notes as you write") until real memories exist; never seed demo facts into a new account.

### 2f70097354b0-b — Memories page asserts facts about the user that they never gave it
- **Severity:** P2
- **So what:** Power-user dismissed it as a demo panel and kept going, but it undercut the "remembers everything" promise he arrived with.
- **Framework tags:** A1, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same three claims ("Tuesday meetings, Jira, Q4 launch") shown to a fresh account
  - He dismissed it and did not cite it as his reason to leave — save and search were
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/session.log:15` · `persona-power-user/persona-debrief.md`
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Create a fresh workspace with no notes
  2. Click "Memories"
  3. Observe claims about the user drawn from no data they supplied
- **Fix:** On /app/memories.html, show an empty state until real memories exist; if a demo is wanted, label it "Example" explicitly.

### bc4f2c1d10de — Irreversible workspace-type choice is demanded before the user has seen the product
- **Severity:** P2
- **So what:** The first screen forces a guess the novice could not make; a less patient user leaves at second 20, before any value.
- **Framework tags:** A2, A10, C-STEPS, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - "Before we begin, choose your workspace type": "Federated graph", "Sovereign vault", "Hybrid mesh" — no descriptions; "This cannot be changed later."
  - Novice spent 43 s (00:05–00:48) and picked "Hybrid mesh" by guessing
  - Her Settings later shows "Federated graph replication" ticked, not anything named "Hybrid mesh" — the choice has no visible consequence
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall; land on /app/signup.html
  2. Observe three unexplained options and "This cannot be changed later."
- **Fix:** Remove the workspace-type step from signup and default it; if it must stay, add a one-line plain-English description per option and make it changeable in Settings.

### 47c61574c4b3 — Empty dashboard offers no first action, contradicting "never start from zero"
- **Severity:** P2
- **So what:** The persona who came for "remembers everything" met "Nothing here yet." with no next step and wandered for 45 s.
- **Framework tags:** A6, A10, C-TTFV, C-SOWHAT
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" — "Nothing here yet." with no button, prompt or import offer
  - Novice searched the empty workspace ("meeting" → no results) before finding "New block" at 01:40
  - Timeline records `times_had_to_hunt: 2` for the novice
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/timeline.json` · `persona-novice/persona-debrief.md`
  > "Dashboard. "Your cards" — "Nothing here yet." Screenshot 02-dashboard-empty.png. Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a workspace
  2. Land on /app/dashboard.html
  3. Observe "Nothing here yet." with no call to action
- **Fix:** Replace "Nothing here yet." with a "Write your first note" button that opens /app/new.html, plus one line on what Nimbus will remember.

### ada28ed3202e — Three names for one object ("Cards", "New block", "Search your notes") slow the first action
- **Severity:** P2
- **So what:** The novice could not tell which menu item creates a note, adding a hunt before her first write.
- **Framework tags:** A2, A4, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html nav
- **Personas hit:** novice
- **Observed:**
  - Top nav reads "Cards", "New block"; search placeholder reads "Search your notes"; list heading reads "Your cards"
  - Novice paused at 01:40 asking whether cards and blocks are the same
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14`
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing? Clicked "New block"."
- **Repro:**
  1. Land on the dashboard
  2. Compare nav labels, search placeholder and list heading
- **Fix:** Use one noun everywhere — rename "New block" to "New note", "Cards"/"Your cards" to "Notes"/"Your notes".

### a8cabfed8729 — No keyboard shortcuts for capture or search
- **Severity:** P2
- **So what:** The power-user arrived expecting "keyboard-driven" capture and found none — another strike in a team-switch evaluation.
- **Framework tags:** A7, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/dashboard.html keyboard
- **Personas hit:** power-user
- **Observed:**
  - Ctrl+K, Ctrl+N and / did nothing at 01:30
  - Pre-session expectation was "fast capture, good search, keyboard-driven"
- **Evidence:** `persona-power-user/session.log:3` · `persona-power-user/session.log:12`
  > "Tried keyboard: Ctrl+K, Ctrl+N, / — nothing. No shortcuts."
- **Repro:**
  1. On the dashboard, press Ctrl+K, Ctrl+N, then /
  2. Observe no response
- **Fix:** Bind / (or Ctrl+K) to focus "Search your notes" and Ctrl+N to open New block, and list them in a "?" help overlay.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- `persona-novice/screenshots/04-note-saved-toast.png` shows the empty "New block" form, not the "Saved ✓" toast — toast is evidenced only by `session.log:17`/`:20`; not cited as a screenshot
- `persona-power-user/screenshots/03-search-empty.png` shows the empty dashboard with a blank search box, not a "Roadmap" query or "No results" — search failure rests on `session.log:11`
- Power-user's "Saved ✓" and Memories visits have no screenshots of their own — rely on session.log and novice captures of the same screens

## For other lenses
- Console: "Uncaught ReferenceError: renderGraphOverlay is not defined" on every dashboard load — bugs
- Settings labels "Enable webhook sync", "Federated graph replication", "Vault attestation" are unexplained jargon — content
- Settings checkboxes sit centred above their labels, detached from them — ux
- "Federated graph replication" ticked by default regardless of signup choice; power-user asked "is this the same thing?" — ux

## Coverage gaps
- No persona reached a second task; retention could not be observed
- Export ("Markdown, all cards") was seen, never clicked
- Desktop 1440×900 only; no mobile
- Only two personas, both generic (INFERRED)

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice 00–07 (04 mislabelled, see Dropped); power-user 00, 02, 03 (03 mislabelled), 07
