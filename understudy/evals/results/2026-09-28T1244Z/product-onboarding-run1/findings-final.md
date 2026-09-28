# Nimbus Notes — onboarding findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer C funnel — C-TTFV, C-STEPS, C-ABANDON, C-SOWHAT — with A/B tags where they explain the drop-off
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- TTFV, steps and hunt counts taken from `timeline.json`, not recomputed

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached entry point (after auth wall) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen | ✓ 00:48 (guessed) | ✓ ~00:30 |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| First note written | ✓ 02:41 | ✓ 01:00 |
| Note saved and visible in list | ✗ 03:12 (retried 03:50, failed again) | ✗ 01:00 |
| Note found by search | ✗ 03:30 | ✗ 01:00 |
| **First value reached** | ✗ | ✗ |
| Stopped | abandoned 06:30 | abandoned 03:00 |

**Steps to value (required path):** 5 · **Time to value:** not reached · **Drop-off:** Save → list/search, both personas

- Required path: pick workspace type → Create workspace → New block → type title/body → Save = 5 (`timeline.json` `steps_to_first_value: 5`).
- Novice wandered: searched "meeting" on an empty dashboard first; `times_had_to_hunt: 2` (novice), `1` (power-user).
- Both abandoned well inside the 90-minute cap; neither timed out.
- Gap: capture logged novice `first_value_reached: true` at 161 s for the live word-count preview; the persona's debrief rejects it — Q1: "right now: nothing".
- Objective "A new user can write a note and find it again": failed for both (`gave_up: true` in both timelines).

---

## Findings

### 9f4962c53919 — Save shows "Saved ✓" while POST /api/notes returns 500, so no first note ever persists
- **Severity:** P0
- **So what:** Every new user's first note is silently lost, so 0 of 2 personas activated and both quit.
- **Framework tags:** A1, A9, C-TTFV, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Save shows a green "Saved ✓", then the dashboard still reads "Nothing here yet."
  - Every POST /api/notes returned 500 — twice for novice (03:05, 03:50), once for power-user (01:00)
  - Search for the note title returns "No results"; both personas stopped here
- **Evidence:** `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:20` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/network-full.txt:5` · `persona-novice/network-full.txt:7` · `persona-power-user/session.log:11` · `persona-power-user/session.log:15` · `persona-power-user/network-full.txt:3` · `persona-power-user/screenshots/03-search-empty.png`
  > "Saved twice, empty twice. It is lying to me." — novice
  > "Save doesn't save and search doesn't search. Nothing else matters until those work." — power-user
  - Note: `04-note-saved-toast.png` shows the blank New block form, not the toast; the toast rests on `session.log:17`.
- **Repro:**
  1. Create a workspace at /app/signup.html
  2. Click "New block", enter a title and body, click Save
  3. Observe "Saved ✓", then an empty "Your cards" list and a 500 on POST /api/notes
- **Fix:** Fix the /api/notes 500, and show "Saved ✓" only on a 2xx response — otherwise show an error and keep the draft.

### e330857d724f — Memories page asserts invented facts about a brand-new user, making the novice doubt every save
- **Severity:** P1
- **So what:** It converted one bug into general distrust; the novice decided to stop and would pay nothing.
- **Framework tags:** A1, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer claims "Memories are built from your notes and connected accounts." — the user had zero saved notes and no connected accounts
  - Novice said "I'd stop here" at 06:30, two minutes after seeing it
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25` · `persona-novice/persona-debrief.md`
  > "If it's making these up, is it making up the "Saved" too?"
  > "the "memories" it does have aren't mine." — debrief Q4
- **Repro:**
  1. Sign up as a new user, save nothing
  2. Open Memories
  3. Observe three specific claims about the user
- **Fix:** Show an honest empty state on /app/memories.html ("Nothing yet — memories appear after your first notes"), or label sample content "Example".

### 90ee65151d53 — Memories page asserts invented facts, which the power user dismissed as a demo panel
- **Severity:** P2
- **So what:** Power user shrugged and continued, but wrote the feature off; the headline "remembers everything" promise lost credibility.
- **Framework tags:** A1, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Saw "Tuesday meetings, Jira, Q4 launch" and read them as "Not me"
  - Assumed a demo panel and moved on rather than stopping
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md` · `persona-novice/screenshots/06-memories.png` (same page content)
  > "Whatever — a demo panel, I assume. Not going to trust it."
  > "It remembers nothing I gave it and claims things I didn't." — debrief Q4
- **Repro:**
  1. Sign up as a new user
  2. Open Memories
  3. Observe claims unrelated to anything the user entered
- **Fix:** Same as the novice variant: empty state or an explicit "Example" label on /app/memories.html.

### 4fe6244171c0 — Signup forces an irreversible, unexplained workspace-type choice before the user has seen the product
- **Severity:** P2
- **So what:** Step 1 of onboarding is a blind, permanent guess; a less patient novice leaves before the dashboard.
- **Framework tags:** A2, B-G11, C-STEPS, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - "Before we begin, choose your workspace type": "Federated graph", "Sovereign vault", "Hybrid mesh" — no descriptions
  - "This cannot be changed later." directly under the options
  - Novice took 43 s (00:05–00:48) and picked "Hybrid mesh" by guessing; power-user was unbothered ("Fine — I've seen worse")
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-power-user/session.log:8`
  > "I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the auth wall; land on /app/signup.html
  2. Observe three unexplained options and "This cannot be changed later."
- **Fix:** Default the workspace type silently and move the choice to Settings, or add a one-line plain-English description per option.

### 2cf1d96e5b29 — Empty dashboard says only "Nothing here yet." with no route to a first note
- **Severity:** P2
- **So what:** First screen after signup gives no next step and contradicts "never start from zero"; novice wandered to search first.
- **Framework tags:** B-G1, C-STEPS, C-SOWHAT
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" panel shows only "Nothing here yet." — no button, no hint
  - Novice searched "meeting" on the empty workspace before finding "New block" at 01:40
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/findings-raw.json` (00:55)
  > "Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a workspace
  2. Land on /app/dashboard.html
  3. Observe "Nothing here yet." with no call to action
- **Fix:** Put a "Write your first note" button inside the empty "Your cards" panel on /app/dashboard.html.

### 16db58452e10 — Nav labels "Cards" and "New block" do not match "Search your notes", costing the novice a hunt
- **Severity:** P2
- **So what:** Three names for one object slow the first task and make the novice unsure what she is creating.
- **Framework tags:** A4, C-STEPS
- **Flow:** shape_1
- **Locator:** nav: Cards / New block
- **Personas hit:** novice
- **Observed:**
  - Top nav reads "Cards", "New block"; search placeholder reads "Search your notes"; list heading "Your cards"
  - Novice paused at 01:40 to ask whether cards and blocks are the same thing
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14`
  > "Cards and blocks — same thing?"
- **Repro:**
  1. Reach the dashboard
  2. Compare nav labels with the search placeholder
- **Fix:** Use one noun everywhere — rename "Cards" and "New block" to "Notes" and "New note".

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Toast visibility/placement — `04-note-saved-toast.png` shows the blank form, not the toast; only the log records it.
- Power-user search result for "Roadmap" — `03-search-empty.png` shows an empty search box, not the "No results" message; rests on `session.log:11` only.

## For other lenses
- `Uncaught ReferenceError: renderGraphOverlay is not defined` on every dashboard load (`console-full.txt`) — bugs
- No keyboard shortcuts: Ctrl+K, Ctrl+N, "/" do nothing (`persona-power-user/session.log:12`) — ux
- Settings jargon "Enable webhook sync", "Federated graph replication", "Vault attestation" with no explanation (`07-settings.png`) — content
- "Federated graph replication" checked by default; unclear link to signup choice (`persona-power-user/session.log:13`) — ux
- Settings checkboxes centred far from their labels (`07-settings.png`) — ux

## Coverage gaps
- No persona got a note to persist, so retrieval, editing, a second task and return visits are untested
- Export was seen, never run
- Desktop 1440×900 only; no mobile

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice: 00-start, 00-wall-cleared, 01-signup-workspace-type, 02-dashboard-empty, 03-new-note, 04-note-saved-toast, 05-notes-list-missing, 06-memories, 07-settings · power-user: 00-start, 02-dashboard, 03-search-empty, 07-settings
