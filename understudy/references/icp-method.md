# ICP method — deriving ideal customer profiles from a traversal

**[M] methodology. Pass 2 only.** Loaded by `lens-icp`. Never loaded during capture — a persona who knows what an ICP is stops behaving like a visitor and starts behaving like a market analyst.

---

## What an ICP is here

An **ideal customer profile** is the kind of customer most likely to get the product's full value, stay, and be worth having — specific enough that someone could go and find fifty of them today. It is not a persona (that is one person and how they decide) and not a target market (that is everyone who could conceivably buy).

Two shapes, and the lens picks one per run:

| Shape | The unit is | Defined by |
|---|---|---|
| **Account-type** (B2B) | a company, team or role inside one | industry · size · stage · the tool it runs today · the trigger that makes it look · who signs |
| **Life-situation** (consumer) | a person in a moment | the situation they are in · the job they are hiring for · what they tried before · what they'd pay · where they can be found |

**Everything in a profile is inferred from what the product and its site actually said and did.** This lens does not research the market. Where the evidence does not reach, the profile says *not inferable* — a profile that reads confidently on every line was written from the model's priors, and that is the one output this lens must never produce.

---

## Detecting the shape

Read the captured evidence for these signals before writing anything, and state the call and the evidence for it in the exec summary:

| Points to account-type | Points to life-situation |
|---|---|
| pricing per seat, per team, per workspace; "contact sales"; annual plans by tier of company size | pricing per person, per month; app-store links; a free tier aimed at one person |
| "for teams", "for your organisation", role-named tiers, SSO, invite-your-team flows | "you", "your day", "your health", second-person life language |
| proof is company logos, case studies with a company name, ROI numbers | proof is individual testimonials, star ratings, download counts |
| sign-up asks for a company or work email | sign-up asks for a name, or nothing |

Mixed signals are a finding in their own right (*the site sells to individuals and prices for teams*). Record `market_shape: account-type | life-situation | mixed` and, if the interview supplied an override (`icp_market` in the manifest), use it and note that it overrode the evidence.

---

## The method — positioning first, then fit and propensity

Adapted from April Dunford's positioning exercise, which is the one framework that derives target customers from the product rather than from a customer list. Five steps, in order, with evidence at every step.

### 1. Unique attributes — what this product has that the persona noticed

List what the product actually does or offers, from the captured evidence only: features the persona used, claims the site made, proof it showed, constraints it imposed (price, platform, sign-up friction). Cite each. **Do not list what a product in this category usually has.**

### 2. Value — what each attribute is worth, and to whom it is worth most

For each attribute: what does it let someone do that they could not do before? Then the question that produces segments: **who would care about that the most?** Not "small businesses" — *which* small businesses, and what is it about them.

### 3. Candidate segments — five to seven, never three

Write 5–7 candidates. Three candidates scored is a shortlist that was never a list. Each candidate is one line: *who, in what situation, hiring the product for what job.*

Draw candidates from four places, and label the source:
- **Named by the site** — "built for X", a case study about Y, a pricing tier called Z.
- **Implied by the product** — a feature only makes sense if you have a certain problem (an export to a payroll system implies someone who runs payroll).
- **The persona's own read** — debrief Q2 ("who is it for? is that you?") for every persona, including the ones who said *not me*; a persona who bounced is evidence about who it is not for.
- **Adjacent** — same attributes, a different job. At most two of these, and they are marked as the lens's inference.

### 4. Score every candidate — fit × propensity

Two axes, each 1–5, each the mean of its criteria. Score from evidence; where a criterion cannot be scored from the run, write `?` and exclude it from the mean rather than guessing a 3.

**Fit — would this product genuinely serve them?**

| Criterion | 1 | 5 |
|---|---|---|
| Pain severity | a nice-to-have | the problem costs them money, time or risk every week |
| Product alignment | the product does a fraction of the job | the product does the whole job, as observed in the traversal |
| Evidence on site/product | nothing addressed to them | named proof, a tier, a flow built for them |
| Use-case clarity | you would struggle to explain it to them in a sentence | one sentence, in their words, and it is obviously true |

**Propensity — would they actually buy, and stay?**

| Criterion | 1 | 5 |
|---|---|---|
| Reachability | no observable place they gather | a channel, community, job title or app-store category you can name |
| Trigger / urgency | no event makes them look | a datable trigger (new role, new baby, funding, a deadline, a regulation) |
| Willingness to pay | the price seen would be a stretch or absurd for them | the price seen is trivially inside what they already spend on this |
| Openness to switching | locked into something with high switching cost | using nothing, or something they complain about |

### 5. Place them, pick three, name the trap

Plot on the 2×2:

| | Low propensity | High propensity |
|---|---|---|
| **High fit** | **Expansion** — worth the product, slow to win | **Primary** — the beachhead |
| **Low fit** | Deprioritise | **Trap** — easy to sell, churns |

Return **three** profiles: the primary, the expansion bet, and the next-best (usually a second high-fit candidate, occasionally a second primary if two are close). Name the **trap** separately, in one paragraph, so nobody targets it by accident.

If fewer than three candidates clear fit ≥ 3, return fewer and say why. Three weak ICPs padded to a number is worse than two real ones.

---

## The case against — every profile argues with itself

For each of the three, write the strongest honest case that it will **not** work. This is the one place the lens reasons rather than observes, and it is labelled as reasoning. Four lines:

- **What they use instead.** The competitive alternative — a product the site itself names (a "vs" page, a migration guide, an import-from feature), a product the persona brief said they already use, or the status quo (a spreadsheet, a notebook, doing nothing). *Doing nothing is the most common competitor and the one sites never name.*
- **Switching cost.** What they would have to give up, re-enter, re-learn or convince someone of.
- **The fact that would kill it.** The single thing which, if true, means this ICP is wrong — *if they already have this feature in the tool they pay for*, *if the price is above what a person spends on this category*, *if the trigger only happens once a decade.*
- **The cheapest test.** How to find out in a week: five conversations, one landing-page variant, one search, one look at a community.

No web research. If naming the alternative requires a fact the run did not capture, say *the alternative is not inferable from this run* and give the test that would surface it.

---

## The persona for a re-run

Every profile ends with a persona block in the target-file shape, so the orchestrator can offer to run the product as this customer next:

```yaml
- name: <slug, lower-case, one word or hyphenated>
  device: <desktop-1440x900 | iphone-13 | android | …>
  goal: "<what this ICP would try to do in the first session, in their words>"
  gives_up_when: "<the moment this ICP would stop, in their words>"
```

The goal and the give-up condition come from the profile's job and its case against — a re-run persona whose give-up condition is the kill fact is the fastest way to test the profile.

---

## The score this lens gives

The lens's 0–10 score measures **how clearly the product signals who it is for** — the only thing about ICPs that is observable in a traversal. Not the quality of the market, not the size of the segment, not how good the ICPs are.

| Band | Means |
|---|---|
| 9–10 | A visitor can say who it is for in the first thirty seconds and every candidate segment is named or implied by the site itself |
| 6–8 | The primary is evident; the others took product use or inference to find |
| 3–5 | Segments had to be inferred from features; the site addresses "everyone" |
| 0–2 | Nothing in the site or product narrows who it is for; every profile is the lens's guess |

Findings (in `findings-final.md`) are the **gaps**: what the product lacks for a profile, what the site never says that a profile would need to hear, contradictions between who it addresses and who it prices for. They carry the normal severity rubric — a P1 here is *the primary ICP cannot see a price*, not *the headline could be punchier.*

---

## Never

- Never write a profile the run has no evidence for. Fewer profiles, honestly.
- Never use a real company or person from outside the run as an example of the segment.
- Never fill a `?` with a plausible number.
- Never present the case against as a finding — it is reasoning, and it says so.
- Never let a bounced persona disappear: *not for them* is a boundary of the ICP and belongs in the profile.
