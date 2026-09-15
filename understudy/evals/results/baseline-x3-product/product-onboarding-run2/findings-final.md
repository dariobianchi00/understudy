# Nimbus Notes — onboarding findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer C activation metrics (C-TTFV, C-STEPS, C-ABANDON, C-SOWHAT) with Nielsen (A) and HAX (B-G) tags where they sharpen a finding
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED, not researched
- Scoring model: opus · traversal: fixture-hand-authored
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Clock starts after the auth wall (excluded per manifest); TTFV and step counts taken from `timeline.json`, not recomputed

---

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached entry point (`/app/signup.html`) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen, "Create workspace" | ✓ 00:48 | ✓ ~00:25 |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| First action found ("New block") | ✓ 01:40 | ✓ 01:00 |
| Note composed | ✓ 02:41 | ✓ 01:00 |
| Note persisted (visible in "Your cards") | ✗ 03:12 — "Nothing here yet." | ✗ 01:00 — empty |
| Note found by search | ✗ 03:30 — "No results for 'Dentist'." | ✗ 01:00 — "Roadmap" no results |
| **First value reached** | ⚠ nominal 02:41 (live word count/preview) · durable: ✗ | ✗ |
| Returned to a second task | ✗ | ✗ |
| Session end | **abandoned 06:30** — "I'd stop here." | **abandoned 03:00** — "Enough." |

- **Steps to value (product-required path):** 5 — pick workspace type → Create workspace → New block → type title/body → Save. Neither persona got value from it.
- **Time to value:** novice 02:41 nominal (`timeline.json` `seconds_to_first_value: 161`) — the persona's own debrief retracts it: "right now: nothing." Power-user: not reached.
- **Drop-off:** both at the same point — the Save → dashboard return, when the "Saved ✓" toast is followed by an empty list. Novice retried once (03:50) before quitting; power-user did not retry.
- **Abandonment, not time-out:** both quit inside 7 minutes of a 90-minute cap.
- **Wandering (novice):** 2 hunts recorded (`times_had_to_hunt: 2`) — searched an empty workspace at 01:20, and stalled over "Cards" vs "New block" at 01:40. 45 s between dashboard and first action.
- **Wandering (power-user):** 1 hunt — tried Ctrl+K / Ctrl+N / "/" at 01:30, none bound.

---

## Findings

> **⚑ This block is machine-parsed.** Every field on its own bullet.

### 664ae0869f45 — "Saved ✓" toast fires while POST /api/notes returns 500, so every note is lost
- **Severity:** P0
- **So what:** Both personas lost every note they wrote, were told it saved, and quit — the run's only objective fails here for 2 of 2.
- **Framework tags:** A1, A9, B-G11, C-ABANDON, C-TTFV
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Save → green "Saved ✓" → redirect to dashboard → "Your cards" still reads "Nothing here yet."; search for the exact title returns "No results".
  - Network: `POST /api/notes → 500 internal error` at novice 03:05 and 03:50, power-user 01:00 — 3 of 3 saves failed, 0 error shown to the user.
  - Novice retried once and got the same result; power-user quit on the first failure.
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/screenshots/04-note-saved-toast.png` (form reset after Save; toast itself not in frame) · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:20` · `persona-novice/network-full.txt` · `persona-novice/console-full.txt` · `persona-power-user/screenshots/03-search-empty.png` · `persona-power-user/session.log:11` · `persona-power-user/network-full.txt` · `persona-novice/timeline.json` objectives[0].gave_up=true · `persona-power-user/timeline.json` objectives[0].gave_up=true
  > novice, 03:50: "Wrote it again, saved again, 'Saved ✓' again, dashboard empty again. It is lying to me."
  > power-user, 03:00: "Save doesn't save and search doesn't search. Nothing else matters until those work."
- **Repro:**
  1. Clear the login wall, create a workspace with any type.
  2. Click "New block", enter a title and body, click "Save".
  3. Observe "Saved ✓" and the redirect; observe "Your cards" still shows "Nothing here yet."
  4. Type the title into "Search your notes" — "No results".
  5. DevTools → Network: `POST /api/notes` is 500.
- **Fix:** Make the "Saved ✓" toast conditional on a 2xx from `/api/notes`; on failure keep the form populated and show "Couldn't save — try again" inline. Then fix the 500.

### 3970a4ef2a0b-a — Irreversible "workspace type" choice between three unexplained terms precedes any sight of the product
- **Severity:** P1
- **So what:** The novice's first 48 seconds were spent on an irreversible decision she could not understand — before the product had done anything for her.
- **Framework tags:** A2, A3, B-G1, C-STEPS, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Screen headed "Before we begin, choose your workspace type" offers "Federated graph", "Sovereign vault", "Hybrid mesh" — no description of any, and "This cannot be changed later."
  - Novice stalled 00:05 → 00:48 (43 s) and chose by guesswork: "Picked 'Hybrid mesh' because it sounds like it includes the other two."
  - Same wording reappears pre-checked in Settings as "Federated graph replication", still unexplained.
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-novice/screenshots/07-settings.png`
  > novice, 00:20: "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall; land on `/app/signup.html`.
  2. Read the three radio labels — no descriptions, no default, no "learn more".
- **Fix:** Remove the choice from signup — default to one type and move it to Settings with a one-line description per option, or at minimum drop "This cannot be changed later."

### 3970a4ef2a0b-b — Irreversible "workspace type" choice between three unexplained terms precedes any sight of the product
- **Severity:** P3
- **So what:** The power-user shrugged it off in under 30 seconds; it cost a mild eye-roll, not a step toward quitting.
- **Framework tags:** A2, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** power-user
- **Observed:**
  - Chose "Federated graph" immediately; on the dashboard by 00:30.
  - Later confusion in Settings: "'Federated graph replication' is on by default. I picked that at signup — is this the same thing?"
- **Evidence:** `persona-power-user/session.log:8` · `persona-power-user/session.log:13` · `persona-power-user/screenshots/07-settings.png`
  > power-user, 00:00: "Workspace type: Federated graph / Sovereign vault / Hybrid mesh, cannot be changed. Fine — I've seen worse."
- **Repro:**
  1. Clear the login wall; land on `/app/signup.html`; pick any option.
  2. Open Settings; note the matching, pre-checked, unlinked toggle.
- **Fix:** Same as -a; additionally link the Settings toggle to the signup choice with one line of copy.

### 77c5cc3d8f49-a — Memories page asserts three facts about a brand-new user that are not theirs
- **Severity:** P0
- **So what:** The novice read fabricated facts about herself and concluded the product was lying about "Saved" too — trust gone in the first 5 minutes.
- **Framework tags:** B-G1, B-G11, C-ABANDON, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - Page headed "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer says "Memories are built from your notes and connected accounts." — the user had written one note about a dentist and connected nothing.
  - Nothing marks the items as sample, demo, or placeholder.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25` · `persona-novice/persona-debrief.md`
  > novice, 04:50: "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the 'Saved' too?"
  > novice, 06:30: "I have zero notes saved and a page telling me things about myself that aren't true. I'd stop here."
- **Repro:**
  1. Create a fresh workspace; write at most one note.
  2. Click "Memories" in the top nav.
- **Fix:** Show an honest empty state ("Nothing remembered yet — memories appear as you write notes") and never render sample memories under "about you"; if samples must exist, label each "Example".
- Severity note: rubric's P0 example — confident nonsense about the persona's own data — fits exactly; reached after the save failure, so it compounds rather than causes the abandonment.

### 77c5cc3d8f49-b — Memories page asserts three facts about a brand-new user that are not theirs
- **Severity:** P2
- **So what:** The power-user wrote it off as a demo panel but still refused to trust the feature that carries the product's core promise.
- **Framework tags:** B-G1, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same three memories shown to a user who had written one note titled "Roadmap".
  - Persona explicitly assumed demo content and moved on within 30 s.
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md` · `persona-novice/screenshots/06-memories.png`
  > power-user, 02:30: "Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
  > power-user, debrief Q4: "It remembers nothing I gave it and claims things I didn't."
- **Repro:**
  1. Create a fresh workspace; write one note.
  2. Click "Memories".
- **Fix:** Same as -a.

### 59e48fdd8d6b — Empty dashboard says "Nothing here yet." with no next step, contradicting "remembers everything"
- **Severity:** P2
- **So what:** The novice arrived expecting pre-filled content, found nothing and no instruction, and spent 45 s searching an empty workspace before finding the create action.
- **Framework tags:** A1, A6, B-G1, C-STEPS, C-TTFV
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Dashboard shows a search box and "Your cards — Nothing here yet."; no CTA, no hint, no link to "New block".
  - Novice typed "meeting" into search at 01:20 — "No results for 'meeting'." — before locating "New block" in the nav at 01:40.
  - Pre-session promise: "remembers everything so you never start from zero"; debrief Q4: "it started completely empty".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/session.log:14` · `persona-novice/persona-debrief.md` · `persona-novice/timeline.json` shape_2.times_had_to_hunt=2
  > novice, 00:55: "Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a fresh workspace; land on `/app/dashboard.html`.
  2. Look for any instruction or primary action below "Your cards".
- **Fix:** Replace "Nothing here yet." with a primary "Write your first note" button and one line explaining that Memories fill in as notes accumulate.

### 66cbea1c04b9 — Nav uses "Cards", "New block" and "Search your notes" for the same object
- **Severity:** P2
- **So what:** The novice paused at the one link that leads to value because its label did not match the list it was meant to feed.
- **Framework tags:** A2, A4, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Top nav: "Cards", "New block", "Memories", "Settings"; list heading "Your cards"; search placeholder "Search your notes"; create form headed "New block".
  - Novice questioned the mapping at 01:40 before clicking "New block".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json`
  > novice, 01:40: "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing?"
- **Repro:**
  1. Open `/app/dashboard.html`; read the nav labels, list heading, and search placeholder.
- **Fix:** Pick one noun — "notes" matches the product name and the search placeholder — and rename "Cards", "Your cards", and "New block" to "Notes", "Your notes", "New note".

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast's visual appearance and timing — `04-note-saved-toast.png` shows the reset form, not the toast; the toast rests on `session.log` and the network 500 only.
- Whether "Export — Markdown, all cards" works — neither persona clicked it.

## For other lenses
- `POST /api/notes → 500` on every save, and `Uncaught ReferenceError: renderGraphOverlay is not defined` on every dashboard load (both `console-full.txt`) — bugs.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, "/" unbound; `persona-power-user/session.log:12`) — ux.
- Settings toggles "Enable webhook sync", "Federated graph replication", "Vault attestation" with no explanation (`07-settings.png`) — content, ux.
- Marketing promise "remembers everything so you never start from zero" vs an empty, non-persisting product — content.

## Coverage gaps
- "Cards" nav item never opened as a distinct page — both personas returned to the dashboard via redirect.
- "Export" never clicked.
- No mobile viewport; both personas desktop 1440×900.
- Return visit / second session not observed — both personas abandoned in the first session.
- Login wall excluded per manifest; wall wait (70 s / 40 s) not counted.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index — novice: 00-start, 00-wall-cleared, 01-signup-workspace-type, 02-dashboard-empty, 03-new-note, 04-note-saved-toast, 05-notes-list-missing, 06-memories, 07-settings · power-user: 00-start, 02-dashboard, 03-search-empty, 07-settings
