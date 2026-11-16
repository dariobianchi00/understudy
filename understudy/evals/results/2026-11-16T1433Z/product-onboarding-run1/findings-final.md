# Nimbus Notes — onboarding findings — Run 2026-09-08 (fixture02)

## Method
- Framework: first-value definition + Layer C (C-TTFV, C-STEPS, C-ABANDON, C-SOWHAT); severity per rubric
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on invented personas
- Scoring model: opus
- Every finding cites an artifact. Unsupported observations are dropped and listed at the end
- Auth wall at `/app/login.html` excluded; clock starts after it (novice wall 70 s, power-user 40 s, not scored)

---

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached signup (wall cleared) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen, workspace created | ✓ 00:48 (43 s hesitation) | ✓ <00:30 |
| Landed on dashboard | ✓ 00:55 | ✓ 00:30 |
| Found "New block" | ✓ 01:40 (after searching an empty product) | ✓ 01:00 |
| Wrote a note | ✓ 02:41 (capture-marked TTFV: live preview) | ✓ 01:00 |
| Product said "Saved ✓" | ✓ 03:05 (and again 03:50) | ✓ 01:00 |
| **First value: note found again (list or search)** | ✗ never | ✗ never |
| Returned to a second task | ✗ abandoned 06:30 | ✗ abandoned 03:00 |

**Steps to value (required):** 5 (novice `timeline.json` steps_to_first_value) · **Time to value:** capture logged 02:41 for novice, null for power user. Neither persona actually got value · **Drop-off:** after "Saved ✓", empty "Your cards" list

- **Both abandoned. Neither timed out.** They stopped at 06:30 and 03:00 of a 90-minute cap
- **The capture's 02:41 TTFV is the product's word-count preview, not value.** The novice called it "Small"; in the debrief she said it does "right now: nothing"
- **Gap between "Saved ✓" and value:** the product declared success 3 times (03:05, 03:50, 01:00); `POST /api/notes` returned 500 every time
- **Wandering:** novice took 2 hunts (`timeline.json` times_had_to_hunt), including a search of an empty product at 01:20

---

## Findings

### 06af80cef054 — Save says "Saved ✓" but the note is never stored, so no persona reaches first value
- **Severity:** P0
- **So what:** 2 of 2 personas wrote a note, were told it was saved, lost it, and quit. Activation is 0%.
- **Framework tags:** C-TTFV, C-ABANDON, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Clicking Save shows "Saved ✓", then the dashboard still reads "Nothing here yet."; searching the title returns "No results"
  - `POST /api/notes → 500 internal error` at 03:05 and 03:50 (novice) and 01:00 (power user). The success toast shows anyway
  - Novice retried once and then quit at 06:30. Power user quit at 03:00. Both debriefs: would not keep using, would pay nothing
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17-20` · `persona-novice/network-full.txt:5,7` · `persona-power-user/screenshots/03-search-empty.png` · `persona-power-user/session.log:11,15` · `persona-power-user/network-full.txt:3` · `persona-*/timeline.json` objectives gave_up: true
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me." (novice)
  > "Enough. Save doesn't save and search doesn't search. Nothing else matters until those work." (power-user)
- **Repro:**
  1. Create a workspace at /app/signup.html
  2. Click "New block", enter a title and body, click Save
  3. Observe "Saved ✓", then the empty "Your cards" list; search the title
- **Fix:** Fix `POST /api/notes`. Show "Saved ✓" only after a 2xx response, and show a retryable error on failure.

### 488380b43f26 — Memories invents facts about the novice and makes her doubt every "Saved ✓"
- **Severity:** P0
- **So what:** Confident nonsense about her own life made the novice decide the whole product lies, including the save confirmations.
- **Framework tags:** C-ABANDON, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer claims "Memories are built from your notes and connected accounts." She had no saved notes and no connected accounts
  - Her final in-session statement was about this page, and she stopped 100 s later
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21-22,25` · `persona-novice/persona-debrief.md` Q4
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Create a fresh workspace with no notes
  2. Open Memories in the top nav
- **Fix:** On Memories, show an empty state ("Nothing yet — memories appear after your first notes") until the user's own data exists; never show sample facts as theirs.

### c9561541c29c — Memories shows facts that are not the power user, who writes the feature off
- **Severity:** P1
- **So what:** The headline "remembers everything" feature is dismissed as a demo before the evaluator gets to the team-switch decision.
- **Framework tags:** C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same three fabricated memories ("Tuesday meetings, Jira, Q4 launch")
  - He read it as a demo panel, not as a lie. Lower severity than for the novice: a severity flip
  - Debrief Q4: "It remembers nothing I gave it and claims things I didn't."
- **Evidence:** `persona-novice/screenshots/06-memories.png` (same page, fresh workspace) · `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md` Q4
  > "Not me. Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Create a fresh workspace with no notes
  2. Open Memories
- **Fix:** On Memories, show an empty state ("Nothing yet — memories appear after your first notes") until the user's own data exists; never show sample facts as theirs.

### 6098867893ad — Empty dashboard breaks the "never start from zero" promise and gives no next step
- **Severity:** P2
- **So what:** The novice arrived expecting her stuff, got "Nothing here yet.", and spent 45 s hunting, including searching an empty product.
- **Framework tags:** C-STEPS, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" shows only "Nothing here yet.". There is no button, hint or link to create a first note
  - Novice searched "meeting" at 01:20 and reached "New block" at 01:40. That is 2 hunts (`timeline.json`)
  - Nav says "Cards" and "New block", search says "Search your notes". She asked whether these were the same thing
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12-14` · `persona-novice/timeline.json` shape_2.times_had_to_hunt=2 · `persona-novice/persona-debrief.md` Q4
  > "Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a workspace
  2. Land on /app/dashboard.html and look for a way to start
- **Fix:** Replace "Nothing here yet." with a primary "Write your first note" button linking to /app/new.html.

### 3b4261c35f51 — Signup forces an irreversible jargon choice before the novice has seen the product
- **Severity:** P2
- **So what:** The first screen spends 43 s on an undoable guess, which costs confidence before any value. A less patient novice leaves here.
- **Framework tags:** C-ABANDON, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - "Before we begin, choose your workspace type": "Federated graph", "Sovereign vault", "Hybrid mesh". None of them is explained
  - "This cannot be changed later." She guessed "Hybrid mesh" at 00:48 and carried on
  - Severity flip: the power user called it "Fine — I've seen worse" and chose in under 30 s
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9-11` · `persona-power-user/session.log:8`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall, land on /app/signup.html
  2. Read the three options and the "cannot be changed later" note
- **Fix:** Default the workspace type silently, and move the choice to Settings with one-line explanations and the ability to change it.

### 326b92f02f49 — Signup workspace type reappears in Settings with no link, leaving the power user unsure what he chose
- **Severity:** P3
- **So what:** It adds doubt about the one setup decision he made. It did not change his behaviour.
- **Framework tags:** C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** power-user
- **Observed:**
  - Settings shows "Federated graph replication" pre-checked, next to "Enable webhook sync" and "Vault attestation"
  - He had picked "Federated graph" at signup. Nothing ties the two together
- **Evidence:** `persona-novice/screenshots/07-settings.png` (same page) · `persona-power-user/session.log:8,13` · `persona-power-user/findings-raw.json` 02:00
  > ""Federated graph replication" is on by default. I picked that at signup — is this the same thing?"
- **Repro:**
  1. Choose "Federated graph" at signup
  2. Open Settings
- **Fix:** In Settings, show "Workspace type: Federated graph" as a labelled row with one-line help, separate from the replication toggle.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast is not visible in any screenshot. `persona-novice/screenshots/04-note-saved-toast.png` shows an empty New block form. The toast is cited from `session.log:17` only
- `persona-power-user/screenshots/03-search-empty.png` shows an empty search box, not the "No results for 'Roadmap'" message. That message is cited from `session.log:11`

## For other lenses
- `POST /api/notes → 500` while the UI reports success — bugs
- "Enable webhook sync", "Vault attestation" and the Cards/block/notes naming are unexplained jargon — content
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) for a keyboard-first evaluator (`persona-power-user/session.log:12`) — ux
- Signup radio buttons sit centred, detached from their labels (`01-signup-workspace-type.png`) — ux

## Coverage gaps
- No persona saw a stored note, so editing, retrieval, search ranking and Export were never exercised with data
- Desktop 1440×900 only; no mobile run
- No price given, so TTFV is read against consumer self-serve

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-*/timeline.json`, `persona-*/session.log`
- C. Screenshots — novice 00–07; power-user 00, 02, 03, 07 (all opened)
