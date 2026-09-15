# Nimbus Notes — onboarding findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer C activation (C-TTFV, C-STEPS, C-ABANDON, C-SOWHAT), with Layer A tags where the funnel loss has a usability cause
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED, not researched
- Scoring model: opus
- Timings, step counts and hunt counts taken from `timeline.json` as measured live, not recomputed
- Every finding cites an artifact; unsupported observations dropped, listed at the end

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached entry point (post-wall) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen (irreversible) | ✓ 00:48 | ✓ ~00:20 |
| Workspace created → dashboard | ✓ 00:55 | ✓ 00:30 |
| Found the compose surface ("New block") | ✓ 01:55 | ✓ 01:00 |
| Product confirmed "Saved ✓" | ✓ 03:05 | ✓ 01:00 |
| Note visible in list or search | ✗ 03:12 | ✗ 01:30 |
| **First value reached (retained)** | ✗ | ✗ |
| Returned to a second task | ✗ abandoned 06:30 | ✗ abandoned 03:00 |

**Steps to value (required):** 5 — workspace type → Create workspace → New block → type → Save
**Time to value:** not reached by either persona
**Drop-off:** Save → list/search, between `/app/new.html` and `/app/dashboard.html`

- Both personas **abandoned voluntarily**; neither hit the 90-minute cap. Novice quit at 06:30, power-user at 03:00.
- `timeline.json` records `first_value_reached: true` at 161s for novice. That moment is the live word-count/preview inside the editor (`session.log:16`), and it did not survive Save — the debrief reads "the one I wrote disappeared twice, so right now: nothing." Reported as measured, scored as not reached.
- Wandering, counted separately: novice took 8 actions after the first failed save (re-write, re-save, search ×2, Memories, Settings) that the product never required.

---

## Findings

### a73144efec7b — Save confirms success and the note never appears in the list or search
- **Severity:** P0
- **So what:** The one thing both personas came to do silently fails while the product claims it worked, and both ended the session over it.
- **Framework tags:** A1, A9, C-TTFV, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Both personas saw a green "Saved ✓" toast, were returned to the dashboard, and found "Nothing here yet."
  - Searching the note's own title returned "No results for 'Dentist'" / "No results for 'Roadmap'".
  - Every save posted `POST /api/notes → 500`; the UI reported success on all three attempts across both personas.
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/session.log:17-20` · `persona-power-user/session.log:11` · `persona-novice/network-full.txt:5,7` · `persona-power-user/network-full.txt:3`
  > "Saved twice, empty twice. It is lying to me."
- **Repro:**
  1. Sign in, choose any workspace type, click Create workspace.
  2. Open "New block", enter a title and body, click Save.
  3. Observe "Saved ✓", then the dashboard: "Nothing here yet."
  4. Search the title in the dashboard search box: "No results for '<title>'."
- **Fix:** Make `POST /api/notes` succeed, and gate the "Saved ✓" toast on a 2xx response — on failure show an inline error on the New block form with the draft text preserved.

### 4417ef6b5a22 — Memories asserts three facts about a user who has written nothing
- **Severity:** P1
- **So what:** It converts a save bug into a trust collapse — the novice began doubting every other thing the product told her, including "Saved".
- **Framework tags:** A1, B-G2, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Personas hit:** novice, power-user
- **Locator:** /app/memories.html
- **Observed:**
  - "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Caption reads "Memories are built from your notes and connected accounts." — the novice had written one note, about a dentist, and connected nothing.
  - Novice generalised the distrust back onto the save confirmation; power-user wrote the panel off as demo content and stopped trusting it.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21-22` · `persona-power-user/session.log:14`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the 'Saved' too?"
- **Repro:**
  1. Create a new workspace and write at most one note.
  2. Click "Memories" in the top nav.
  3. Observe three specific claims about the user that no session data supports.
- **Fix:** Show an honest empty state on `/app/memories.html` for accounts with no derived memories — "Nothing remembered yet. Memories appear once you've written a few notes." — and label any seeded examples "Example".

### ff8769e052ac — Signup demands an irreversible workspace-type choice before the product is seen
- **Severity:** P1
- **So what:** The first screen after the wall asks the novice for an unchangeable decision in vocabulary she does not have, and she guessed.
- **Framework tags:** A2, A3, A5, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - "Before we begin, choose your workspace type" offers "Federated graph", "Sovereign vault", "Hybrid mesh", with no explanation of any option.
  - Sub-label reads "This cannot be changed later."; there is no skip, no default and no back.
  - Novice stalled 28 seconds (00:20 → 00:48) and picked "Hybrid mesh" on the guess that it includes the other two.
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9-11` · `persona-novice/findings-raw.json` entry t=00:20
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the auth wall and land on `/app/signup.html`.
  2. Observe three unexplained options and "This cannot be changed later." with no default selected.
- **Fix:** Default to one option, add a one-line plain-English description under each ("Sovereign vault — your notes stay on your own storage"), and either make the choice reversible in Settings or move it out of signup.
- **Note:** Severity flips — the power-user met the same screen and shrugged ("Fine — I've seen worse", `persona-power-user/session.log:8`). Scoped to novice rather than averaged.

### 35dc876707d5 — Empty dashboard offers no first action, costing 60 seconds of hunting
- **Severity:** P2
- **So what:** The novice landed on her home screen and could not tell what to do, spending a minute before finding the compose surface.
- **Framework tags:** A1, A6, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Post-signup dashboard shows a search box, "Your cards", and "Nothing here yet." — no button, link or prompt to create anything.
  - Novice searched "meeting" into an empty account before working out the nav, reaching "New block" at 01:55, 60 seconds after landing.
  - `timeline.json` records `times_had_to_hunt: 2` for this persona.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12-14` · `persona-novice/timeline.json` (`shape_2.times_had_to_hunt`)
  > "'Nothing here yet.' Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Complete signup and land on `/app/dashboard.html` with no notes.
  2. Observe the empty state offers no call to action.
- **Fix:** Replace "Nothing here yet." with a primary "Write your first note" button that opens the compose form, plus one line saying what a card is.

### 55f2a58042c5 — Cards, blocks and notes name the same object, stalling the path to the first note
- **Severity:** P2
- **So what:** The novice had to test a guess to find the compose screen, because the product uses three words for one thing.
- **Framework tags:** A2, A4, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Top nav reads "Cards", "New block", "Memories", "Settings"; the panel heading reads "Your cards"; the search placeholder reads "Search your notes".
  - Novice paused at 01:40 to ask whether cards and blocks were the same thing, then clicked "New block" to find out.
  - The compose screen is headed "New block" while the object it creates is counted under "Your cards".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json` entry t=01:40
  > "Cards, blocks, notes — are these the same thing?"
- **Repro:**
  1. Open `/app/dashboard.html` and read the nav, the panel heading and the search placeholder.
  2. Click "New block" and compare its heading to "Your cards".
- **Fix:** Pick one noun — "note" — and use it in the nav ("Notes", "New note"), the dashboard heading ("Your notes") and the compose screen.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast itself — `persona-novice/screenshots/04-note-saved-toast.png` shows an empty New block form with no toast visible. The toast is evidenced only by `session.log:17` and is reported on that basis.
- Power-user's reaction to the Memories panel — no screenshot was captured for that persona; the log line stands, the screen state does not.
- Whether the novice would have returned later — the session ended at her own stopping point, not at the cap; no second-session data exists.
- Whether the 60-second dashboard hunt repeats for a returning user — only first-session data captured.

## For other lenses
- `POST /api/notes → 500` on all three attempts, and `Uncaught ReferenceError: renderGraphOverlay is not defined` on every dashboard load — **bugs**.
- No keyboard shortcuts at all (Ctrl+K, Ctrl+N, `/` all inert), a stated dealbreaker for the power-user — **ux**.
- Settings labels "Enable webhook sync", "Federated graph replication", "Vault attestation" are opaque to the novice, and the power-user cannot tell whether "Federated graph replication" is the workspace type he picked — **content**, **ux**.
- Marketing promise "Nimbus remembers everything so you never start from zero" versus an empty account both personas rejected in Q4 — **content**.

## Coverage gaps
- No Memories screenshot for power-user; no signup screenshot for power-user.
- Export never clicked by either persona, despite being the one affordance both called clear.
- Only desktop 1440×900 tested; no mobile or tablet viewport.
- No second session, so retention and returning-user onboarding are unobserved.
- Only one of the three workspace types was exercised per persona; "Sovereign vault" was never selected.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index — `persona-novice/screenshots/` (8), `persona-power-user/screenshots/` (4)
