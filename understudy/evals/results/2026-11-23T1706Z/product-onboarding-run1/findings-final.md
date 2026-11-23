# Nimbus Notes — onboarding findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer C activation (C-TTFV, C-STEPS, C-ABANDON, C-SOWHAT) plus Layer A tags; Layer B not applied — no AI surface was exercised beyond a static Memories list
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on personas the agent invented
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached entry point (signup, after auth wall) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen, workspace created | ✓ 00:48 (28 s hesitation) | ✓ by 00:30 |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| Note written and Save clicked ("Saved ✓" shown) | ✓ 03:05 | ✓ 01:00 |
| Note stored (`POST /api/notes`) | ✗ 500 at 03:05 and 03:50 | ✗ 500 at 01:00 |
| **First value — note found again in list or search** | ✗ | ✗ |
| Returned to a second task | ✗ abandoned 06:30 | ✗ abandoned 03:00 |

**Steps to value (required path):** 5 — choose type · Create workspace · New block · write · Save; product breaks at step 5 · **Time to value:** not reached (0/2) · **Drop-off:** Save → dashboard, both personas

- **Both stops are abandonment, not time-out:** novice quit at 06:30, power-user at 03:00, of a 90-minute cap.
- **Required path is short and was not the problem:** 5 steps, 0 permission prompts.
- **Wandering, beyond the required path:** novice searched an empty dashboard, wrote the note twice, then probed Memories and Settings; power-user tried 3 keyboard shortcuts.
- **Capture recorded first value for novice at 02:41** (live word count/preview, `timeline.json` shape_2); she retracted it in debrief — *"right now: nothing."* Scored as not reached.

---

## Findings

### ded37edbcc62 — Save confirms success while the note is never stored, so no persona reaches first value
- **Severity:** P0
- **So what:** 2 of 2 personas wrote a note, were told it saved, lost it, and quit — the funnel ends at its first real action.
- **Framework tags:** A1, A9, C-TTFV, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Save shows "Saved ✓" and returns to the dashboard; every `POST /api/notes` returns 500 (3 of 3 attempts).
  - Dashboard still reads "Nothing here yet."; searching the note title returns "No results".
  - Novice retried once, then called it lying; power-user stopped after one attempt.
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/session.log:17-20` · `persona-power-user/session.log:11` · `persona-power-user/session.log:15` · `persona-novice/network-full.txt:5` · `persona-novice/network-full.txt:7` · `persona-power-user/network-full.txt:3` · `persona-novice/persona-debrief.md` (Q1, Q3)
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me."
  > "Enough. Save doesn't save and search doesn't search. Nothing else matters until those work."
- **Repro:**
  1. Create a workspace at /app/signup.html.
  2. Click "New block", enter a title and body, click Save.
  3. Observe "Saved ✓"; observe `POST /api/notes` → 500.
  4. Dashboard shows "Nothing here yet."; search the title → no results.
- **Fix:** Make `POST /api/notes` persist the note, and show "Saved ✓" only after a 2xx response; on failure show an error with Retry.

### d249c9f8d55c — Memories page shows invented facts about the user, which made the novice distrust the Saved confirmation
- **Severity:** P1
- **So what:** Fabricated "memories" turned a lost note into a trust failure — she concluded the product invents things, including "Saved".
- **Framework tags:** A1, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer says "Memories are built from your notes and connected accounts."; she had zero saved notes and no connected accounts.
  - She stopped 100 seconds later; debrief Q4 cites it against the promise.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21-22` · `persona-novice/session.log:25` · `persona-novice/persona-debrief.md` (Q4)
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Sign up with a fresh workspace; do not save any notes.
  2. Open Memories.
  3. Observe three specific claims about the user with no source.
- **Fix:** Show an honest empty state on /app/memories.html until real notes exist, and link each memory to the note it came from.

### 94ffb13d26b7 — Memories page shows invented facts about the user, which the power user dismissed as demo content
- **Severity:** P2
- **So what:** He wrote the panel off as a demo — the product's headline "remembers" feature earned zero credibility with an evaluator.
- **Framework tags:** B-G11, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same three fabricated memories on a fresh workspace.
  - He shrugged and moved on; his stop at 03:00 cites Save and search, not Memories.
  - Debrief Q4 still lists it: "claims things I didn't."
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md` (Q4) · `persona-novice/screenshots/06-memories.png` (same screen, novice capture)
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Sign up with a fresh workspace.
  2. Open Memories.
  3. Observe facts not derived from any user data.
- **Fix:** Label any sample content as "Example" on /app/memories.html, or remove it until the user's own notes produce memories.

### 93ef683d9386 — Signup forces an irreversible workspace-type choice in unexplained terms before the user sees the product
- **Severity:** P2
- **So what:** The first screen asks a novice for a permanent decision she cannot understand — a likely exit for less patient users.
- **Framework tags:** A2, A3, A5, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - "Before we begin, choose your workspace type": "Federated graph", "Sovereign vault", "Hybrid mesh"; no descriptions.
  - "This cannot be changed later."
  - Novice hesitated 28 seconds and guessed; power-user was untroubled ("Fine — I've seen worse").
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9-11` · `persona-power-user/session.log:8`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the auth wall; land on /app/signup.html.
  2. Observe three unexplained options and "This cannot be changed later."
- **Fix:** Default the workspace type and move the choice to Settings, or add one plain-language line per option and make it changeable.

### 09d06641adb2 — Empty dashboard offers no first step, and the create action is labelled "New block", not note
- **Severity:** P2
- **So what:** A novice expecting her own content got "Nothing here yet." and had to hunt for how to write a note — 45 s lost.
- **Framework tags:** A2, A6, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Dashboard shows "Your cards" and "Nothing here yet." with no call to action.
  - Nav offers "Cards" and "New block"; search placeholder says "Search your notes" — three nouns for one thing.
  - Novice searched the empty list first, then guessed "New block" at 01:40; `times_had_to_hunt` 2.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12-14` · `persona-novice/timeline.json` (shape_2.times_had_to_hunt = 2)
  > "Dashboard. "Your cards" — "Nothing here yet." Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a workspace.
  2. Land on /app/dashboard.html; observe empty state with no action.
- **Fix:** Replace "Nothing here yet." with a "Write your first note" button, and use "note" consistently in nav and headings.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- "Saved ✓" toast on screen — `persona-novice/screenshots/04-note-saved-toast.png` shows the empty New block form, no toast; toast rests on session.log only.
- Power-user's search for "Roadmap" — `03-search-empty.png` shows an empty dashboard with an empty search box, not the query or a "No results" message; the log carries it.

## For other lenses
- `renderGraphOverlay is not defined` on every dashboard load; `POST /api/notes` 500 — bugs.
- "Cards" / "block" / "notes" naming and settings jargon ("Enable webhook sync", "Vault attestation") — content.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) — `persona-power-user/session.log:12` — ux.
- "Federated graph replication" in Settings not linked to the signup choice — `persona-power-user/session.log:13` — ux.

## Coverage gaps
- No note was ever stored, so retrieval, editing, search relevance and Export were never exercised.
- Desktop 1440×900 only; no mobile.
- No price in the target; Q3 asked as "would you keep using this".

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice: 00-start, 00-wall-cleared, 01-signup-workspace-type, 02-dashboard-empty, 03-new-note, 04-note-saved-toast (shows form, no toast), 05-notes-list-missing, 06-memories, 07-settings · power-user: 00-start, 02-dashboard, 03-search-empty, 07-settings
