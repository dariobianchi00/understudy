# Nimbus Notes — onboarding findings — Run 2026-09-08 (fixture02)

## Method
- Framework: activation funnel — Layer C (C-TTFV, C-STEPS, C-ABANDON, C-SOWHAT) with Layer A tags where the drop-off has a usability cause
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (novice, power-user; both desktop-1440x900)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Layer B not applied: no AI surface was experienced during the funnel; "Memories" is scored on trust (Layer A/C), not on AI guidelines
- Timings are taken from `timeline.json`, not recomputed from the log
- Auth wall excluded per manifest; clock starts at wall-cleared

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached entry point (post-wall) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen (irreversible) | ✓ 00:48 | ✓ 00:30 |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| Found "New block" | ✓ 01:40 (2 hunts) | ✓ 01:00 |
| Note composed | ✓ 02:41 | ✓ 01:00 |
| "Saved ✓" shown | ✓ 03:05 | ✓ 01:00 |
| Note listed / searchable | ✗ 03:12 · ✗ 03:30 · ✗ retry 03:50 | ✗ 01:00 |
| **First value reached** | ✓ 02:41 (live preview) — revoked 03:12 | ✗ |
| Abandoned (declared, not timed out) | 06:30 | 03:00 |
| Returned to a second task | ✗ | ✗ |

**Steps to value:** 5 required · **Time to value:** 02:41 novice / not reached power-user · **Drop-off:** Save → dashboard, both personas

- Required path: workspace type → dashboard → "New block" → type → Save (5 steps, `persona-novice/timeline.json` `steps_to_first_value: 5`).
- Novice wandered 2 extra steps before "New block": search "meeting" at 01:20, menu read at 01:40 (`times_had_to_hunt: 2`).
- Power-user's 1 hunt was keyboard shortcuts at 01:30, after the drop-off — not on the required path.
- Both exits are abandonment at 06:30 and 03:00 against a 90-minute cap; neither is a time-out.

---

## Findings

> **⚑ This block is machine-parsed.** Every field on its own bullet.

### 9efe714b14ba — Save shows "Saved ✓" but the note is never listed or searchable; both personas abandon here
- **Severity:** P0
- **So what:** The core objective ("write a note and find it again") fails for 2/2 personas, and the false confirmation makes them distrust everything else.
- **Framework tags:** A1, A9, C-ABANDON, C-TTFV
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Novice clicked Save at 03:05, saw "Saved ✓", was returned to dashboard reading "Nothing here yet."; search "Dentist" returned "No results for 'Dentist'."
  - Novice retried at 03:50 with identical result; power-user hit the same at 01:00 with "Roadmap".
  - Network shows `POST /api/notes → 500 internal error` on every save (novice 03:05, 03:50; power-user 01:00) while the UI reported success.
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:20` · `persona-power-user/session.log:11` · `persona-novice/network-full.txt:5` · `persona-novice/network-full.txt:7` · `persona-power-user/network-full.txt:3` · `persona-novice/timeline.json` objectives[0].gave_up=true · `persona-power-user/timeline.json` objectives[0].gave_up=true
  > "Saved twice, empty twice. It is lying to me." — novice, 03:50
  > "Enough. Save doesn't save and search doesn't search. Nothing else matters until those work." — power-user, 03:00
  > "Nothing yet — it accepts a note and then loses it." — power-user debrief Q1
- **Repro:**
  1. Clear the wall, pick any workspace type, click "New block".
  2. Enter title "Dentist" and a body, click Save.
  3. Observe "Saved ✓" toast, then dashboard "Your cards" — "Nothing here yet."
  4. Type "Dentist" in "Search your notes" — "No results for 'Dentist'."
- **Fix:** Make `POST /api/notes` persist and return the note; show the "Saved ✓" toast only on a 2xx, and on failure keep the form with an error that offers retry.

### a240d0b18d4e — Memories page asserts facts that are not the persona's, and both stop trusting "Saved"
- **Severity:** P1
- **So what:** After losing their note, both personas read invented "memories" as proof the product fabricates, which ends any chance of a second session.
- **Framework tags:** A1, A2, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Observed:**
  - "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4." for accounts with zero persisted notes.
  - Footer reads "Memories are built from your notes and connected accounts." — no notes exist and no accounts were connected.
  - Novice links it directly to the save failure; power-user labels it a demo panel and refuses to trust it.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:24` · `persona-power-user/session.log:14`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the 'Saved' too?" — novice, 04:50
  > "Not going to trust it." — power-user, 02:30
  > "It remembers nothing I gave it and claims things I didn't." — power-user debrief Q4
- **Repro:**
  1. Create a fresh workspace; add no notes and connect no accounts.
  2. Click "Memories" in the top nav.
  3. Observe three pre-filled memories attributed to the user.
- **Fix:** On `/app/memories.html`, replace the placeholder memories with an empty state ("Nothing remembered yet — write your first note") until real notes or connected accounts exist; if sample content must stay, label it "Example".

### 5690d58acf98 — Irreversible workspace-type choice between three undefined terms stalls the novice 48s before any value
- **Severity:** P1
- **So what:** The first screen after signup forces an unexplained, permanent decision; the novice guesses and enters the product already uneasy.
- **Framework tags:** A2, A3, A6, C-STEPS, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Screen reads "Before we begin, choose your workspace type" with radio options "Federated graph", "Sovereign vault", "Hybrid mesh" and the note "This cannot be changed later."
  - No description, default, or "learn more" for any option; novice spent 00:05→00:48 on this screen.
  - Novice chose "Hybrid mesh" on the guess that it "includes the other two".
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-novice/findings-raw.json` t=00:20
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo." — novice, 00:20
- **Repro:**
  1. Clear the wall; land on `/app/signup.html`.
  2. Read the three options and the "This cannot be changed later." note.
- **Fix:** Pick a sensible default (or move the choice to Settings), and add one plain-language line under each option saying what it changes for the user.

### 4b60b49e43d5 — Irreversible workspace-type choice costs the power user nothing beyond a shrug
- **Severity:** P3
- **So what:** Same screen, no measurable cost for this persona — the flip against the novice shows the product assumes an expert user.
- **Framework tags:** A2, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** power-user
- **Observed:**
  - Power-user chose "Federated graph" within the first 30s and moved on.
  - Later, in Settings, could not tell whether "Federated graph replication" was the same thing chosen at signup.
- **Evidence:** `persona-power-user/session.log:8` · `persona-power-user/session.log:13` · `persona-power-user/screenshots/07-settings.png` · `persona-power-user/findings-raw.json` t=02:00
  > "Fine — I've seen worse. Picked Federated graph." — power-user, 00:00
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link." — power-user, 02:00
- **Repro:**
  1. Clear the wall; pick "Federated graph"; open Settings.
  2. Observe "Federated graph replication" checked with no reference to the signup choice.
- **Fix:** Keep the fix from 5690d58acf98; additionally show the chosen workspace type in Settings so the two labels are visibly the same thing.

### f11175ca74dc — Empty dashboard gives no next step; novice hunts twice and takes 60s to find "New block"
- **Severity:** P2
- **So what:** The first screen of the product contradicts the "never start from zero" promise and leaves the novice to discover the only action by elimination.
- **Framework tags:** A6, A10, C-STEPS
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Dashboard shows "Search your notes" and "Your cards" — "Nothing here yet." with no create button, prompt, or link in the card area.
  - Novice searched "meeting" at 01:20 (hunt 1), then read the nav at 01:40 (hunt 2) before clicking "New block"; `times_had_to_hunt: 2`.
  - Power-user went straight to "New block" at 01:00 — no cost observed for that persona.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/session.log:14` · `persona-novice/timeline.json` shape_2.times_had_to_hunt=2
  > "'Nothing here yet.' Nothing tells me what to do. I thought it would have my stuff." — novice, 00:55
- **Repro:**
  1. Create a workspace; land on `/app/dashboard.html`.
  2. Observe the empty "Your cards" area with no call to action.
- **Fix:** Replace "Nothing here yet." with a primary "Write your first note" button that opens `/app/new.html`, plus one line on what a card is.

### 48754a8d2097 — Three words for one object ("Cards", "New block", "notes") send the novice hunting
- **Severity:** P2
- **So what:** The novice cannot tell which nav item creates a note, adding a hunt on the required path to first value.
- **Framework tags:** A2, A4, C-STEPS
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Nav reads "Cards", "New block", "Memories", "Settings"; search placeholder reads "Search your notes"; list heading reads "Your cards"; create form is titled "New block".
  - Novice asked whether cards and blocks were the same thing before clicking "New block" at 01:40.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json` t=01:40
  > "Cards, blocks, notes — are these the same thing?" — novice, 01:40
- **Repro:**
  1. Land on `/app/dashboard.html`; compare the nav labels, the search placeholder, and the list heading.
- **Fix:** Use one word everywhere — rename "Cards" and "New block" to "Notes" and "New note" to match "Search your notes".

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast itself was not captured — `persona-novice/screenshots/04-note-saved-toast.png` shows the blank form; the toast rests on `session.log:17` and the network record. Worth a screenshot next run.
- Whether "Export — Markdown, all cards" works on an empty workspace — neither persona clicked it.

## For other lenses
- `POST /api/notes → 500` on every save and `Uncaught ReferenceError: renderGraphOverlay is not defined` on every dashboard load — bugs
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) for the power-user (`persona-power-user/session.log:12`) — ux (A7)
- Settings labels "Enable webhook sync", "Federated graph replication", "Vault attestation" with no explanation (`persona-novice/session.log:23`) — content / ux
- Marketing promise "remembers everything so you never start from zero" vs an empty first screen — content (promise match), also scored Fail here in Numbers

## Coverage gaps
- No persona ever saw a persisted note, a populated Cards list, or a search result — the post-save half of the funnel is unmeasured.
- Export not exercised.
- Desktop 1440x900 only; no mobile capture.
- Time on product: novice 07:00, power-user 03:20 — both far below the 90-min cap because both abandoned.

## Appendices
- A. Persona debriefs: `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines: `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index:
  - novice: `00-start.png` (login wall, excluded), `00-wall-cleared.png` (signup, workspace type), `01-signup-workspace-type.png`, `02-dashboard-empty.png`, `03-new-note.png`, `04-note-saved-toast.png` (blank form, toast not visible), `05-notes-list-missing.png`, `06-memories.png`, `07-settings.png`
  - power-user: `00-start.png` (login wall, excluded), `02-dashboard.png`, `03-search-empty.png`, `07-settings.png`
