# Heuristics framework — Layers A, B, C

**[M] methodology.** **Pass 2 only.** Never load this during capture — a persona who has read it produces observations shaped like findings, and the report then confirms its own priors.

Every finding carries one or more layer tags. Multi-layer findings are normal and usually the most interesting: `A2 + B-G11 + C-ABANDON` says more than any one tag alone.

---

## Layer A — Nielsen's 10 (usability hygiene)

Applies to every product.

| # | Heuristic | What to look for |
|---|---|---|
| **A1** | Visibility of system status | Does the system say what it's doing? Loading states, progress, confirmations. |
| **A2** | Match between system and the real world | Language matches the user's vocabulary. No internal jargon leaking out. |
| **A3** | User control and freedom | Undo, cancel, back. Escape hatches everywhere. |
| **A4** | Consistency and standards | Same concept = same word; same action = same UI. |
| **A5** | Error prevention | Prevent the problem, don't just handle it afterwards. |
| **A6** | Recognition rather than recall | The user sees the options; they don't have to remember them. |
| **A7** | Flexibility and efficiency | Shortcuts for experts; the basics stay clear for novices. |
| **A8** | Aesthetic and minimalist design | No irrelevant information competing with the relevant. |
| **A9** | Recognise, diagnose, recover from errors | Plain-language errors with a way forward. |
| **A10** | Help and documentation | Findable, task-focused, concrete. |

---

## Layer B — Microsoft HAX / Amershi (AI-specific)

**Apply only if the product uses AI in a way the user experiences.** For a product with no AI surface, Layer B is not applicable — say so once in the report rather than forcing tags.

The six that carry the most weight for a consumer-facing AI product:

| # | Guideline | What to look for |
|---|---|---|
| **B-G1** | Make clear what the system can do | Can the user tell what it's capable of? |
| **B-G2** | Make clear how well it can do it | Are expectations set about accuracy and limits? |
| **B-G3** | Time services based on context | Does it interrupt at appropriate moments? |
| **B-G8** | Support efficient dismissal | How easy is it to stop or cancel an AI action? |
| **B-G9** | Support efficient correction | How easy is it to redirect or fix it? |
| **B-G11** | Make clear why the system did what it did | Is the AI's reasoning visible? |

The full 18 apply if the product warrants it — G4–G7 (contextual relevance, social norms, bias, safe failure), G10 (scope services to context), G12–G18 (remember recent interactions, learn from behaviour, update cautiously, encourage granular feedback, convey consequences, provide global controls, notify about changes). Reach for those when the six above don't fit what you're seeing; don't pad a report with them.

---

## Layer C — Activation and business impact

| # | Metric | Reading |
|---|---|---|
| **C-TTFV** | Time from the persona taking over to first useful output on their own data | <5 min healthy for consumer self-serve; adjust for price and complexity from the target file |
| **C-STEPS** | Distinct screens and clicks to first value | Fewer is better; flag anything over ~10 |
| **C-ABANDON** | Points where this persona would plausibly quit | *"Too much setup"* · *"I don't get it"* · *"this feels risky"* |
| **C-SOWHAT** | Can the persona say in one sentence what it does, and name two more things it can do? | Pass / Partial / Fail — from the debrief |

**The clock starts when the persona takes over.** An auth wall is infrastructure and never counts against the product.

---

## Tagging

- Multiple tags per finding are fine and usually right.
- **Do not force a tag.** A pure funnel-time issue that is only `C-TTFV` is a legitimate finding.
- Worked example: a consent screen that asks for broad access with no explanation → `A2` (the word "Connect" without context reads as a demand), `B-G11` (no why), `C-ABANDON` (this is where the persona left).

---

## Out of scope for this lens

Each of these is a real concern and a *different lens* — routing them elsewhere is what keeps the `ux` report readable:

| Not here | Belongs to |
|---|---|
| WCAG / accessibility | Mode B `accessibility` (not yet built) |
| Load time, performance | Mode B `performance` (not yet built) |
| Console errors, failed requests | `bugs` |
| Copy quality, reading level, jargon density | `content` |
| Funnel shape, drop-off points | `onboarding` |
| Localisation | Out of scope — personas are fluent in the product's language |

Seeing something outside your lens is normal. Note it in one line at the end of your output under **"For other lenses"** and move on. Do not score it.
