# Nimbus Notes — content findings — Run 2026-09-08 (fixture02)

## Method
- Framework: promise-vs-delivery (first-value Q4) plus Nielsen A2/A4/A9 on reading level, jargon density, error and empty-state copy
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — **INFERRED**, not researched; every persona-specific judgement below is weaker for it
- Scoring model: opus
- Every screenshot cited was opened; every finding cites an artifact; unsupported observations are listed at the end
- Layer B (AI-specific) applies only to the "Memories" surface, which presents derived claims about the user

## Promise vs delivery

| Persona | Arrived expecting | Product delivered | Match | Cost |
|---|---|---|---|---|
| novice | "remembers everything so you never start from zero" | Empty dashboard, manual "New block" form, two notes lost after "Saved ✓", three "memories" that are not hers | Fail | Quit at 06:30 with zero notes saved |
| power-user | "remembers everything so you never start from zero" | Empty dashboard, one note lost after "Saved ✓", search returns nothing, no shortcuts | Fail | Quit at 03:00; "Not going to trust it" |

- Both personas answered Q4 "no" in their own words; my reading does not disagree with theirs.
- The subtlety their answers add: the product does not merely fail to deliver the promise, it *simulates* delivering it on the Memories surface, which is what converted disappointment into distrust.

---

## Findings

### 90176dc30226 — "Memories" asserts three facts about the user that are not theirs and captions them as built from their notes
- **Severity:** P0
- **So what:** Both personas stopped believing anything the product said about their own data, including the save confirmation.
- **Framework tags:** A2, B-G2, B-G11, C-ABANDON
- **Flow:** surfaces
- **Locator:** persona-novice/screenshots/06-memories.png
- **Personas hit:** novice, power-user
- **Observed:**
  - Heading reads "What Nimbus remembers about you" above three first-person claims: "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Caption reads "Memories are built from your notes and connected accounts." — the novice had written one note, about a dentist, and connected no accounts.
  - The power-user read the panel as "a demo panel, I assume" and discounted the surface entirely.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:22` · `persona-power-user/session.log:14`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Complete signup as a brand-new user.
  2. Write nothing, or write one unrelated note.
  3. Open "Memories" in the top nav and read the three entries and the caption beneath them.
- **Fix:** On the Memories screen, show an empty state until a memory is actually derived from the user's own content, and label any seeded example as an example in the panel itself.

### ba33e6c03d8f — "Saved ✓" is the only copy about persistence and it is false; no failure or error message exists
- **Severity:** P0
- **So what:** The only words the product says about saving are wrong, and both personas abandoned within four minutes of reading them.
- **Framework tags:** A1, A9, C-ABANDON
- **Flow:** shape_2
- **Locator:** persona-novice/screenshots/05-notes-list-missing.png
- **Personas hit:** novice, power-user
- **Observed:**
  - Saving shows a green "Saved ✓" top right; the dashboard then still reads "Your cards" / "Nothing here yet."
  - No error, warning, retry prompt or diagnostic copy appears at any point in either session.
  - The novice saved the same note twice, read "Saved ✓" twice, and concluded the product was lying.
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:20` · `persona-power-user/session.log:11` · `persona-novice/timeline.json`
  > "Saved twice, empty twice. It is lying to me."
- **Repro:**
  1. Open "New block", enter a title and body.
  2. Click Save and read the green "Saved ✓".
  3. Return to the dashboard and read "Nothing here yet."
- **Fix:** Do not render "Saved ✓" until the write is confirmed, and add failure copy on the New block screen that names what failed and what the user should do next.

### 0ad96e22b8b4 — No copy anywhere reconciles "never start from zero" with an empty notes app the user must fill by hand
- **Severity:** P1
- **So what:** Both personas answered the promise-match question "no"; the pitch sold automatic recall and the first screen hands them a blank page.
- **Framework tags:** A2, B-G1, C-SOWHAT, C-ABANDON
- **Flow:** shape_1
- **Locator:** persona-novice/screenshots/02-dashboard-empty.png
- **Personas hit:** novice, power-user
- **Observed:**
  - Both arrived on "remembers everything so you never start from zero"; the novice expected "a notes app that fills itself in from things I already have".
  - The first post-signup screen reads "Your cards" / "Nothing here yet." with no line saying what Nimbus can import or that content must be typed.
  - The only surface that echoes the pitch is "Memories", whose contents belong to neither persona.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:3` · `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
  > "I arrived with "remembers everything so you never start from zero". No — it started completely empty, it lost what I gave it, and the "memories" it does have aren't mine."
- **Repro:**
  1. Arrive from the marketing claim "remembers everything so you never start from zero".
  2. Complete signup.
  3. Read every word on the first screen and look for any statement of what Nimbus imports.
- **Fix:** Put one line on the dashboard empty state stating what Nimbus can bring in automatically and what the user must type, and bring the marketing claim into line with it.

### 2e97f6a54729 — Irreversible workspace choice offers three undefined terms and no explanation of any of them
- **Severity:** P1
- **So what:** The novice guessed on a decision the screen says is permanent, 20 seconds after taking over and before seeing the product.
- **Framework tags:** A2, A5, A6, C-ABANDON
- **Flow:** shape_1
- **Locator:** persona-novice/screenshots/01-signup-workspace-type.png
- **Personas hit:** novice
- **Observed:**
  - "Before we begin, choose your workspace type" offers three bare radio labels: "Federated graph", "Sovereign vault", "Hybrid mesh".
  - No description, tooltip or help link on any option; the only supporting sentence is "This cannot be changed later."
  - The novice took 28 seconds and picked "Hybrid mesh" on the reasoning that it "sounds like it includes the other two".
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:11` · `persona-novice/findings-raw.json`
  > "Three words I don't know, and it can't be changed. I haven't seen the product yet."
- **Repro:**
  1. Clear the auth wall and land on the signup workspace-type screen.
  2. Read the three option labels and the supporting line.
  3. Attempt to find any explanation of the difference between them.
- **Fix:** Give each workspace-type option a one-line plain-English description of what the user gets, or move the choice into Settings after first value so it need not be irreversible.

### 39406abfc2b4 — Every Settings toggle is labelled in internal vocabulary with no description
- **Severity:** P2
- **So what:** The novice cannot tell what her own workspace is doing or what any switch would change.
- **Framework tags:** A2, A10
- **Flow:** surfaces
- **Locator:** persona-novice/screenshots/07-settings.png
- **Personas hit:** novice
- **Observed:**
  - Three toggles read "Enable webhook sync", "Federated graph replication" and "Vault attestation", with no description text under any of them.
  - "Federated graph replication" is checked on by default and unexplained.
  - The one control the novice understood was the "Export" button, captioned "Markdown, all cards".
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-novice/findings-raw.json`
  > "Webhook sync, graph replication, vault attestation — no idea. Export is clear."
- **Repro:**
  1. Open "Settings" from the top nav.
  2. Read the three toggle labels.
  3. Look for any explanatory text or help link on the screen.
- **Fix:** Add a one-line plain-English description under each Settings toggle saying what it does and what changes if it is switched off.

### c0f5f80b27c5 — Settings reuses the signup term "Federated graph" without saying whether it is the same choice
- **Severity:** P2
- **So what:** The power-user could not tell whether Settings was showing the irreversible choice he made at signup or a separate switch.
- **Framework tags:** A4, A2
- **Flow:** surfaces
- **Locator:** persona-power-user/screenshots/07-settings.png
- **Personas hit:** power-user
- **Observed:**
  - He selected "Federated graph" at signup; Settings shows a checked toggle labelled "Federated graph replication".
  - Neither screen references the other and the Settings row carries no description.
  - Signup said the workspace type "cannot be changed later", while the Settings toggle appears editable.
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-power-user/session.log:13` · `persona-power-user/findings-raw.json` · `persona-novice/screenshots/01-signup-workspace-type.png`
  > "Is "Federated graph replication" the thing I picked at signup? Same words, no link."
- **Repro:**
  1. Pick "Federated graph" at signup.
  2. Open Settings.
  3. Read "Federated graph replication" and try to establish whether it is the same setting.
- **Fix:** Use one string for the workspace type across signup and Settings, and state on the Settings row whether it is that workspace type or an independent setting.

### 8500923e4d09 — One concept is named three ways across the nav, the list heading and the search box
- **Severity:** P2
- **So what:** The novice spent 45 seconds working out that "New block" was how to write a note.
- **Framework tags:** A4, A2, C-STEPS
- **Flow:** shape_1
- **Locator:** persona-novice/screenshots/02-dashboard-empty.png
- **Personas hit:** novice
- **Observed:**
  - The nav reads "Cards" and "New block"; the list heading reads "Your cards"; the search placeholder reads "Search your notes".
  - The compose screen is titled "New block"; the Settings export caption reads "Markdown, all cards".
  - The novice asked whether cards and blocks were the same thing before clicking either.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json`
  > "Cards, blocks, notes — are these the same thing?"
- **Repro:**
  1. Land on the dashboard and read the nav, the search placeholder and the list heading.
  2. Open "New block" and read its title.
  3. Open Settings and read the Export caption.
- **Fix:** Choose one noun for the unit of content and use it in the nav, the list heading, the compose screen title, the search placeholder and the export caption.

### 91b0bdd26c5d — Empty state says "Nothing here yet." and never says how to fill it
- **Severity:** P2
- **So what:** The first screen after signup gives the novice no instruction, and she went to the search box before finding the way to write anything.
- **Framework tags:** A2, A6, C-TTFV
- **Flow:** shape_1
- **Locator:** persona-novice/screenshots/02-dashboard-empty.png
- **Personas hit:** novice, power-user
- **Observed:**
  - The "Your cards" panel shows only the grey line "Nothing here yet." — no action, button or link.
  - No onboarding line, no suggested first step, nothing naming "New block" as the way to add content.
  - The novice searched "meeting" on an empty workspace before opening the compose screen.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-power-user/screenshots/02-dashboard.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/findings-raw.json`
  > ""Nothing here yet." Nothing tells me what to do."
- **Repro:**
  1. Complete signup and land on the dashboard.
  2. Read the "Your cards" panel.
  3. Look for any instruction naming the next step.
- **Fix:** Replace the empty-state line with copy that names what a card is and a button on the panel that opens the compose screen.

### b296a78e0e6d — Search no-results copy offers no next step and cannot distinguish an empty workspace from a failed search
- **Severity:** P2
- **So what:** After a save silently failed, the search result told both personas nothing was wrong and gave them nowhere to go.
- **Framework tags:** A9, A1
- **Flow:** shape_2
- **Locator:** persona-novice/session.log
- **Personas hit:** novice, power-user
- **Observed:**
  - Searching returns only "No results for 'meeting'." / "No results for 'Dentist'." / "No results for 'test'." with no next step.
  - The same string appears whether the workspace is genuinely empty or an item that reported "Saved ✓" failed to index.
  - The novice read it on a title she had saved 20 seconds earlier.
- **Evidence:** `persona-novice/session.log:13` · `persona-novice/session.log:19` · `persona-power-user/session.log:10` · `persona-power-user/screenshots/03-search-empty.png`
  > "Typed "Dentist" in search. "No results for 'Dentist'." It said saved."
- **Repro:**
  1. Save a note titled "Dentist".
  2. Type "Dentist" into the dashboard search box.
  3. Read the result line.
- **Fix:** Extend the no-results copy to state how many items exist in the workspace and offer a next step, and give an empty workspace its own distinct message.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The green "Saved ✓" toast was never captured in a screenshot — `persona-novice/screenshots/04-note-saved-toast.png` is byte-identical in content to the blank `03-new-note.png` form. The finding above rests on `session.log:17` and `:20` instead; the toast's exact wording, colour and dwell time are unverified.
- The "No results for 'X'." string was never captured in a screenshot — `persona-power-user/screenshots/03-search-empty.png` shows the dashboard with an empty search box, not a result state. The finding rests on the session logs' verbatim transcription.
- Reading level of the signup and Settings copy could not be scored numerically — the screens are label-only, with too few sentences to estimate.
- No help, documentation, tooltip or onboarding surface was opened in either session, so A10 could not be scored beyond its absence from Settings.

## For other lenses
- Save and search both fail silently; the note is never persisted or indexed — `bugs`.
- No keyboard shortcuts at all (Ctrl+K, Ctrl+N, `/` all dead) — `ux`.
- First value never reached for the power-user; the novice's 02:41 "first value" is a live word count and preview, not a saved note — `onboarding`.
- The workspace-type decision is demanded before any value is shown and is declared irreversible — `ux`.

## Coverage gaps
- No note detail or edit view was ever opened, so no copy on that surface was seen.
- No error, validation or offline state was ever triggered, so there is no error copy in evidence at all.
- Mobile and tablet viewports were not tested; both personas ran desktop-1440x900.
- The marketing page carrying the promise was never captured — the promise is known only from the pre-session lines in both session logs.
- Consent, privacy and billing copy were never reached.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — `persona-novice/screenshots/` (8 files, all opened) · `persona-power-user/screenshots/` (4 files, all opened)
