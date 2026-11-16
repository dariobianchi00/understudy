# Nimbus Notes — content findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Nielsen A2/A4/A9 for copy · HAX B-G2/B-G11 for the Memories surface · promise-vs-delivery (first-value Q4)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on personas the agent invented
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Scope exclusion applied: "The login wall at /app/login.html — infrastructure, not a defect."

## Promise vs delivery

| Persona | Arrived expecting | Product delivered | Match | Cost |
|---|---|---|---|---|
| novice | "remembers everything so you never start from zero" — "a notes app that fills itself in from things I already have" | "Nothing here yet."; two notes lost behind "Saved ✓"; three invented "memories" | Fail | Gave up at 06:30; "No. Nothing, until saving works." |
| power-user | "remembers everything so you never start from zero" — "fast capture, good search, keyboard-driven" | Save loses the note; search returns nothing; Memories "Not me" | Fail | Gave up at 03:00; "No. Nothing." |

- Both Q4 answers say "No" — agrees with this reading; no disagreement to log.
- The promise mismatch is the root of F-promise, F-saved and F-memories: the copy claims memory the product does not have.

## Reading level and jargon

- Plain (≈ grade 4–6): dashboard ("Your cards", "Nothing here yet."), editor ("Title", "Body", "0 words", "Preview below"), Memories bullets.
- Engineer-level (≈ grade 14+ / domain-specific): signup ("Federated graph", "Sovereign vault", "Hybrid mesh") and Settings ("Enable webhook sync", "Federated graph replication", "Vault attestation").
- Jargon count on surfaces the novice met: 6 terms, 0 with any explanation; novice could explain none ("I don't know what any of these are").

---

## Findings

### 017babda2f61 — "Saved ✓" confirms a save that never happened, and no error copy ever appears
- **Severity:** P0
- **So what:** Both personas lost every note they wrote while the product told them it was saved; the novice concluded "It is lying to me."
- **Framework tags:** A9, A1, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Save shows green "Saved ✓"; dashboard then still reads "Nothing here yet." (3 saves across 2 personas)
  - Searching the saved title returns "No results for 'Dentist'" — no message ever says the save failed
  - Network shows `POST /api/notes → 500` each time; the copy never reflects it
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-power-user/session.log:11` · `persona-novice/network-full.txt`
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me."
- **Repro:**
  1. Open New block, enter a title and body, click Save
  2. Note the "Saved ✓" toast; return to the dashboard
  3. Dashboard shows "Nothing here yet."; search the title — "No results"
- **Fix:** Show "Saved ✓" only after the server confirms; on failure, show an error on /app/new.html that keeps the text and offers retry.

### b4b9f321ecda-a — Memories page states invented facts as "What Nimbus remembers about you"
- **Severity:** P0
- **So what:** Novice read fabricated facts about herself and stopped trusting every other message, including "Saved".
- **Framework tags:** B-G2, B-G11, A1, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - Heading "What Nimbus remembers about you" over "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer "Memories are built from your notes and connected accounts." — persona had no saved notes and connected no accounts
  - Novice: "If it's making these up, is it making up the "Saved" too?"
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:24`
  > "None of that is true. I've written one note about a dentist. Where is this from?"
- **Repro:**
  1. Create a new workspace; connect nothing
  2. Open Memories
  3. Three specific personal claims appear, attributed to "your notes and connected accounts"
- **Fix:** On /app/memories.html, show only facts derived from the user's own data, each linked to its source note; otherwise show an empty state.

### b4b9f321ecda-b — Memories page states invented facts as "What Nimbus remembers about you"
- **Severity:** P1
- **So what:** Power-user wrote the surface off as a demo and said he would not trust it — the product's headline feature, discarded.
- **Framework tags:** B-G2, B-G11
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same three claims ("Tuesday meetings, Jira, Q4 launch") shown to a second, unrelated workspace
  - Persona dismissed rather than abandoned: "A demo panel, I assume."
- **Evidence:** `persona-power-user/session.log:14` · `persona-novice/screenshots/06-memories.png`
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Create a workspace as a different user
  2. Open Memories
  3. Identical claims appear
- **Fix:** If the panel is sample content, label it "Example" in the heading on /app/memories.html; otherwise remove the fixed claims.

### 24c48151fba1 — Product contradicts its "remembers everything so you never start from zero" promise from the first screen
- **Severity:** P1
- **So what:** Both personas answered Q4 "No" and would not return or pay; the pitch set an expectation the first screen refutes.
- **Framework tags:** A2, B-G1, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Promise: "remembers everything so you never start from zero"; first screen: "Your cards" — "Nothing here yet."
  - Novice expected "a notes app that fills itself in from things I already have"; nothing offers to import or connect anything
  - Power-user Q4: "It remembers nothing I gave it and claims things I didn't."
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:2` · `persona-novice/session.log:3` · `persona-novice/session.log:12` · `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
  > "No — it started completely empty, it lost what I gave it, and the "memories" it does have aren't mine."
- **Repro:**
  1. Arrive from the marketing site line "Nimbus remembers everything so you never start from zero"
  2. Complete signup
  3. Dashboard reads "Nothing here yet." with no import or connect path
- **Fix:** Either change the marketing line to describe a notes app, or make the first dashboard screen offer the import/connect step the line implies.

### 3be6f0d70791 — Irreversible workspace choice is offered in three undefined terms before the user has seen the product
- **Severity:** P2
- **So what:** Novice guessed at a permanent setting ("sounds like it includes the other two"); a less persistent user stops here.
- **Framework tags:** A2, A5, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - "Before we begin, choose your workspace type" — "Federated graph", "Sovereign vault", "Hybrid mesh"; no description under any option
  - "This cannot be changed later." under the options
  - Power-user: "Fine — I've seen worse" — non-issue for him (severity flip)
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-power-user/session.log:8`
  > "I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall; land on /app/signup.html
  2. Read the three options and the warning
- **Fix:** On /app/signup.html, add a one-line plain-language consequence under each option, or default it and move the choice to Settings.

### 709b16aab0fd — Empty state "Nothing here yet." gives no next step
- **Severity:** P2
- **So what:** The novice's first look at the product told her nothing to do; she hunted the nav and searched an empty list instead.
- **Framework tags:** A2, A10, C-TTFV
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" panel contains only "Nothing here yet." — no action, no link to New block
  - Novice searched "meeting" on an empty list before finding New block (`times_had_to_hunt: 2`)
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/timeline.json`
  > "Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a workspace
  2. Land on /app/dashboard.html
- **Fix:** Make the "Your cards" empty state say how to create a first note and link directly to the New block form.

### 160262dd6477 — One object is called "cards", "block" and "notes" across nav, editor and search
- **Severity:** P2
- **So what:** The novice could not tell whether "Cards" and "New block" were the same thing, so the nav did not tell her where her note would go.
- **Framework tags:** A4, A2
- **Flow:** shape_1
- **Locator:** nav
- **Personas hit:** novice, power-user
- **Observed:**
  - Nav: "Cards", "New block"; editor heading: "New block"
  - Dashboard: "Search your notes" above "Your cards"; Settings: "Markdown, all cards"
  - Marketing and both personas call it a "note"
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14`
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing?"
- **Repro:**
  1. Open the dashboard; read nav, search placeholder and panel heading
  2. Click "New block"; read the heading
- **Fix:** Pick one noun for a saved item and use it in the nav, editor heading, search placeholder and export label.

### d46f3386d731 — Settings labels "Enable webhook sync", "Federated graph replication" and "Vault attestation" carry no explanation
- **Severity:** P2
- **So what:** The novice could act on one Settings control of four; she could not tell whether the pre-ticked option affects her notes.
- **Framework tags:** A2
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** novice
- **Observed:**
  - Three checkbox labels with no helper text; "Federated graph replication" is ticked by default
  - Only "Export" — "Markdown, all cards" — was understood
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23`
  > "Webhook sync, graph replication, vault attestation — no idea. Export is clear."
- **Repro:**
  1. Open Settings as a new user
- **Fix:** Add a one-line plain-language description under each Settings checkbox saying what it does to the user's notes.

### d1dfa0c878b1 — "Federated graph replication" reuses the signup term with no stated link to the workspace choice
- **Severity:** P3
- **So what:** Power-user could not tell if a setting he can toggle is the one signup called permanent; he asked and moved on.
- **Framework tags:** A4
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** power-user
- **Observed:**
  - Signup option "Federated graph" ("This cannot be changed later."); Settings checkbox "Federated graph replication", ticked
  - No copy connects or distinguishes the two
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-power-user/session.log:13`
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link."
- **Repro:**
  1. Pick "Federated graph" at signup
  2. Open Settings; compare labels
- **Fix:** On /app/settings.html, either rename the checkbox so it does not echo the workspace type, or state that it relates to it.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Exact wording and placement of the "Saved ✓" toast — `04-note-saved-toast.png` shows the empty New block form, no toast; only the log records it.
- "No results for '…'" copy layout and whether it offers a next step — no screenshot captures a search result; `03-search-empty.png` shows the empty dashboard with no query.

## For other lenses
- `POST /api/notes → 500` on every save; `renderGraphOverlay is not defined` on dashboard — bugs
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) for a power-user expecting "keyboard-driven" — ux
- Irreversible choice placed before any value, and 0 notes after 6:30 — onboarding

## Coverage gaps
- No screenshot of the "Saved ✓" toast or any "No results" state
- Error copy for a failed save never observed — the product never shows one
- Export output never opened; its copy unscored
- Only desktop 1440×900; no mobile copy reviewed

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice 01, 02, 03, 04 (toast not visible), 05, 06, 07 · power-user 02, 03 (no query visible), 07
