# Visit shapes — the Mode A-visit skeleton

**[M] methodology.** Loaded during a **website** capture, alongside the persona brief and `playwright-patterns.md`. The product equivalent is `flow-shapes.md`; load one or the other, never both.

> **Read as the persona, not as an analyst.** Reactions in first person. No diagnosis — that is Pass 2's job, and it has a framework you do not have.

---

## Why this file exists

A product user's journey is *entry → activation → first value → surfaces → debrief*. A site visitor's is **land → orient → evaluate → decide**, and their "first value" is not a feature working. It is:

> **"Did I understand what this is, and decide whether to care?"**

Reached in twenty seconds or never.

**Forcing a visitor through product shapes produces findings about a signup flow they were never going to reach.** That is the entire reason these shapes are separate — the evidence-gathering machinery is identical, the questions are not.

**A visit is short.** 15–25 minutes, not 90. The visitor is not invested, owes the site nothing, and leaves the moment it stops being worth the effort. A traversal that lasts an hour is not thorough; it is a persona who has stopped behaving like a visitor.

---

## Setup — before anything

1. Set the viewport from the persona's device profile. **Verify it** (`playwright-patterns.md`).
2. Fresh browser context per persona. **Logged out.** Clear any prior state — a site that recognises you is not the site a visitor meets.
3. Screenshot `00-landing.png` **immediately**, before scrolling or reading.
4. **Log the entry expectation before navigating**:

```
[pre-session] Arrived via: <search / ad / link from a friend / direct / social>
[pre-session] What I was told: "<the promise that brought me here, verbatim>"
[pre-session] What I'm hoping to find out: <one line, the persona's own question>
[pre-session] What would make me leave: <one line>
```

**This is the anchor everything else is judged against**, and it is worthless written afterwards — by then it is contaminated by what was found. If the target names no referring channel, record that the persona arrived cold; arriving cold is itself a condition worth knowing.

---

## Shape V1 — Land (0:00–0:30) ⚑ the most important thirty seconds

**Goal:** what does the persona understand, above the fold, before scrolling?

Most visitors decide here. Capture it before anything else can overwrite the impression.

1. Screenshot the fold as found. Do not scroll first.
2. **Answer, in first person, before scrolling** — this is the whole point of the shape:
   - *What do I think this is?*
   - *Who do I think it's for?*
   - *What does it want me to do?*
   - *Is any of that a guess?*
3. Record **time-to-comprehension**: the second at which the persona could answer "what is this" correctly. If they never can, record `null` — that is the strongest finding a visit can produce.
4. Note the first thing the eye lands on, and whether it is the thing the page most wants read.

**Do not scroll until step 2 is written.** Scrolling and then reporting a first impression produces a first impression that never happened.

---

## Shape V2 — Orient (0:30–5:00)

**Goal:** the persona builds a working model of the offer.

1. Scroll the landing page fully. Screenshot each distinct section.
2. Follow whatever the page most obviously invites — the primary call to action, or the nav item that answers their question.
3. Read as a visitor reads: headings, first lines, anything bold. **Skim. Do not read every word** — a persona who reads the whole page is testing a page nobody reads.
4. Record every point where the persona is **confused, bored, or suspicious**, with a timestamp.

**Instrumentation**
- Scroll depth reached before losing interest.
- Which section made them want to leave, and which made them stay.
- Any jargon they could not define. Quote it exactly.

---

## Shape V3 — Evaluate (5:00–12:00)

**Goal:** the persona tries to answer *"is this for me, and can I trust it?"*

Follow the persona's own question wherever the site lets them. Typically:

- **Pricing** — can they find it? Do they understand it? Can they work out what they would pay? A site that hides price is answering a question the visitor asked.
- **Proof** — customers, numbers, testimonials, logos. Do they believe them?
- **Who is behind this** — about, team, company, address. Is there a person anywhere?
- **What happens to my data** — findable? Comprehensible? A link to a generic corporate policy is a finding.
- **The objection they arrived with.** Every persona has one. Does the site answer it, ignore it, or make it worse?

**Instrumentation**
- Questions the persona could not answer from the site at all. **This list is the core output of a visit traversal.**
- Anything that made them trust the site more, and anything less. Both.
- Dead ends: a link promising an answer that does not deliver one.

### Forms and conversion points — look, don't submit

When the site asks for details — demo request, newsletter, trial, contact:

1. **Open the form and screenshot it.**
2. Count the fields. Note which are required and which feel unreasonable at this stage.
3. Record what the persona feels about being asked *for this, at this point, in exchange for that*.
4. **Back out without submitting.**

**Why back out:** a submission creates a real lead in someone's real CRM, triggers real email, and may cost the site owner money. The form itself is where the finding lives. **The only exception is a target that explicitly enables submissions with a disposable identity** — and even then, never on a competitor's site in a Mode D run.

---

## Shape V4 — Decide (12:00–20:00) and debrief

**Goal:** the persona reaches a verdict and says why.

1. Give them a last few minutes to check anything still nagging.
2. Ask, in first person, and write into `persona-debrief.md`:

> **Q1 — In one sentence, what does this company do?**
>
> **Q2 — Who is it for? Is that you?**
>
> **Q3 — What would you do next, if anything? Why that?**
>
> **Q4 — What did you want to know that the site never told you?**
>
> **Q5 — Would you trust them with your money or your data? What made the difference?**
>
> **Q6 — Does the site match the promise that brought you here?** State the promise from your pre-session note, then *yes / close but off / no*, and one sentence on why.

3. `browser_close()`.

**Q4 is the highest-value question in a visit traversal.** A list of questions a real visitor had and could not answer is the most directly actionable output a website assessment produces — every item is a page someone can write.

**Q1 is scored against reality, not against effort.** If the persona's one sentence is wrong, the site failed, however handsome it is.

---

## Coverage depth

Set at interview (CLAUDE.md Phase 4, R1) and recorded in the manifest.

| `coverage_depth` | V2 / V3 behaviour |
|---|---|
| `overview` | Landing page and whatever it directly invites. No nav sweep. |
| `standard` *(default)* | Landing page + 2–3 pages the persona's question leads to. |
| `deep` | Every top-level nav destination, plus footer pages (pricing, about, privacy, terms). |

**⚑ On a `deep` run, mark where the visitor stopped being a visitor.** Log `[MM:SS] --- auditor mode: natural interest exhausted ---` at the point the persona would genuinely have left, and continue. Findings after that line are real, but they are not evidence about a visitor's experience, and Pass 2 must be able to tell them apart.

---

## Checkpoints

| Mark | Action |
|---|---|
| **10 min** | If the persona still cannot say what the site does, log `checkpoint_10: comprehension_failed` — that is a finding in itself, not a reason to keep trying. |
| **20 min** | Move to debrief regardless of progress. |
| **25 min** | Hard stop. |

**A visitor who leaves early is data, not a failed run.** If the persona would genuinely have gone within two minutes, record that and go to the debrief. Padding the session to fill the budget destroys the finding.

---

## Banned vocabulary during capture

Same as `flow-shapes.md`, and for the same reason:

> heuristic · Nielsen · HAX · Amershi · severity · P0 · P1 · P2 · P3 · usability · UX (as an analyst term) · WCAG · accessibility audit · conversion funnel · CTA (as jargon) · friction (as jargon) · above the fold (as jargon)

The persona may say *"I couldn't find the price"*. They may not say *"the pricing CTA is below the fold, a P2 conversion issue."*

**Checked mechanically after capture.** Any hit fails the phase gate.

---

## Artifacts, per persona

Under `<run_folder>/persona-<slug>/`:

| File | Contains |
|---|---|
| `screenshots/NN-*.png` | The fold first, then one per distinct section or page |
| `session.log` | `[MM:SS] <event>` narrative, first person |
| `timeline.json` | Structured metrics — below |
| `persona-debrief.md` | Q1–Q6, first person |
| `findings-raw.json` | Reactions, never verdicts |

```json
{
  "shape_v1": { "time_to_comprehension_seconds": null,
                "understood_what": false, "understood_who": false,
                "understood_next_step": false, "guessed": true },
  "shape_v2": { "start": "00:30", "end": "MM:SS",
                "scroll_depth_pct": 0, "sections_seen": 0,
                "point_of_lost_interest": "MM:SS" },
  "shape_v3": { "start": "MM:SS", "end": "MM:SS",
                "pages_visited": [], "questions_unanswered": [],
                "price_found": false, "price_understood": false,
                "forms_opened": 0, "forms_submitted": 0,
                "trust_up": [], "trust_down": [] },
  "shape_v4": { "start": "MM:SS", "end": "MM:SS", "verdict": "" },
  "coverage_depth": "standard",
  "auditor_mode_from": null,
  "left_early": false,
  "session_end_minutes": 0
}
```

**`questions_unanswered` is the field that earns this whole traversal.** Populate it as they arise, never reconstructed at the end.
