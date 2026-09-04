# Sample finding — what a well-written one looks like

**[M] methodology reference.** The product is fictional. Read this before writing your first finding; it is faster than the template at showing what "good" means.

---

### `8f2c1a9d4b7e` — Consent screen requests calendar access with no explanation of why

- **Severity:** P1
- **Framework tags:** A2 (match system/real world), B-G11 (why did it do that), C-ABANDON
- **Flow:** shape_1
- **Personas hit:** novice
- **What happened:** After creating an account, the persona lands on a screen titled *"Connect your calendar"* with a single primary button, *"Connect Google Calendar."* No body copy explains why the product needs this or what happens once connected. The persona paused for 14 seconds, clicked Back, then closed the tab.
- **Why it's a problem:** This persona is the non-technical target buyer. There is no *why* on the screen (B-G11), and *"Connect"* with no context reads as a demand rather than a value exchange (A2). At this price point this is the moment trust is earned or the user leaves. This one left, before seeing the product do anything at all.
- **Evidence:** `persona-novice/screenshots/09-connect-calendar.png` · `session.log:214`
  > "Why does it need my calendar? It hasn't shown me anything yet."
- **Repro steps:**
  1. Visit `/signup` in a fresh browser context.
  2. Complete the email and password step.
  3. Observe the *"Connect your calendar"* screen with no contextual copy.
- **Fix direction:** Add one sentence above the button saying what the product will do with calendar access and why it is needed to reach a first result. Consider showing a sample of the output it enables. Offer a "Skip for now" escape hatch — users who skip should still reach some value path, or the skip is theatre.

---

## Why this finding works

**The title is dev-ticketable.** *"Consent screen requests calendar access with no explanation of why"* can be pasted into a tracker and worked on. *"Onboarding is confusing"* cannot.

**"What happened" contains no diagnosis.** It reports behaviour and timings. The interpretation is quarantined in the next field, so a reader who disagrees with the analysis can still trust the observation.

**"Why it's a problem" ties the framework to this person.** Not *"this violates B-G11"* — it says what the missing *why* cost this persona at this moment. A framework tag with no human consequence attached is a citation, not an argument.

**The evidence is specific and checkable.** A screenshot path, a log line, and a verbatim quote. A reader can open all three in under a minute.

**The fix is a direction, not a spec.** One paragraph pointing at the problem's shape. Writing the actual copy is the product team's job, and a report that does it for them tends to be ignored for the wrong reasons.

**The persona's own words are quoted, not paraphrased.** *"It hasn't shown me anything yet"* is the finding. Any rewording weakens it.
