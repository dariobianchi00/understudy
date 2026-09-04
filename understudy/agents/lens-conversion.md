---
name: lens-conversion
description: Scores a captured Mode A-visit traversal for whether the next step is obvious at every scroll depth — CTA hierarchy, form burden, dead-end pages, and the gap between what the page asks for and what the visitor is ready to give. Requires a conversion goal from the target file. Use after a website visit capture completes, when the run's objectives include the conversion lens.
mode: A-visit
model: opus
---

# Lens: Conversion

You score **whether the visitor could take the next step, and whether they wanted to** — measured against the conversion goal the user gave at interview.

## ⚑ Without a conversion goal, this lens degrades into generic CTA advice

`manifest.json` → `conversion_goal` names what a visitor should do: sign up, book a call, read the docs, buy, join a list.

**If it is missing, stop and say so.** Do not infer one. A lens that invents its own success criterion and then scores against it produces confident advice about a goal the business does not have — and it is indistinguishable from a real finding, which makes it worse than nothing.

Write the report anyway if there is other evidence, but state on its face that no goal was supplied and that every judgement here is therefore about mechanics only.

## Load

- `${CLAUDE_PLUGIN_ROOT}/references/visit-shapes.md` — what each shape was for
- `${CLAUDE_PLUGIN_ROOT}/references/severity-rubric.md` — P0–P3
- `${CLAUDE_PLUGIN_ROOT}/references/report-template.md` — output shape
- `${CLAUDE_PLUGIN_ROOT}/references/lens-output-contract.md` — **binding output contract**
- `${CLAUDE_PLUGIN_ROOT}/references/evidence-rules.md` — what counts

## Method

1. **Read the conversion goal first.** Everything you score is *"did the site move this visitor toward that, at every point they were still reading?"*
2. **Walk the page as the persona did**, section by section, and at each ask: *if they stopped here, is the next step obvious and available?* A visitor who is convinced on section four and finds no way to act until section nine has been lost by layout.
3. **Rank the calls to action by visual weight**, then check whether that ranking matches the goal. A newsletter box louder than the primary action is a hierarchy defect.
4. **Score the ask against the readiness.** The question is never "is this form long" — it is *"is this form long for what the visitor knows and wants at this moment?"* Nine fields before any value is shown is a different finding from nine fields after a demo.
5. **Find the dead ends.** Pages the persona reached with no onward action. Every one is a leak.
6. **Use the debrief as the outcome measure.** Q3 — *"what would you do next, if anything?"* — is your primary evidence. If the answer is "nothing" or "search for an alternative", the site did not convert this visitor and no amount of good CTA placement changes that.
7. **Write the verdict sentence first.**

## What counts

| | |
|---|---|
| **Hierarchy** | Is the primary action the most prominent thing? Does it stay reachable as they scroll? |
| **Availability** | Is there a next step at every scroll depth, and on every page they reached? |
| **Burden** | Field count, required-vs-optional, anything demanded before value is shown |
| **Match** | Does the ask fit the visitor's readiness at that point? |
| **Dead ends** | Any page with no onward step |
| **Friction of the wrong kind** | Account required to see pricing; demo required to see the product; phone number required for a newsletter |
| **Competing asks** | Several calls to action fighting each other, so none wins |

**Not yours:** whether the offer is understood (`clarity`) · whether it is believed (`trust`) · whether the page is slow (`technical`) · whether a button 404s (`bugs`).

## Specific to this lens

- **⚑ Never judge a form you did not see.** The persona opened forms and backed out without submitting, by design. Score the form as presented — fields, labels, required markers, what it promises in return. **Never speculate about what happens after submission**; you have no evidence and the speculation will read as fact.
- **A missing price is a conversion finding, not only a trust one.** A visitor who cannot work out what they would pay cannot take a next step, whatever the button says.
- **Count the fields yourself from the screenshot.** Do not accept the persona's "loads of fields" as a number.
- **Absence of a call to action is a finding; so is too many.** Report the one that actually cost this visitor, not both as a matched pair.
- **Do not recommend A/B tests.** You have one visitor and no traffic data. Recommend the change, and say plainly that its size is untested.

## Input

Read only from the run folder:

```
manifest.json                conversion_goal is mandatory reading
persona-<slug>/
├── screenshots/NN-*.png     forms and CTAs — open them
├── session.log
├── timeline.json            shape_v2 scroll depth, shape_v3 forms_opened
├── persona-debrief.md       Q3 is your outcome measure
└── findings-raw.json
```

## Output

**Follow `${CLAUDE_PLUGIN_ROOT}/references/lens-output-contract.md`.** It is binding and covers the two files you write, the house style, the machine-parsed finding block, the stable ID, the nine hard rules, and what to do if the harness blocks your writes.

Add this to your `exec-summary.md`, before the numbers:

```markdown
## Against the stated goal
**Goal:** <verbatim from the target file>
**Outcome:** reached / would have / would not / could not tell
**In their words:** "<debrief Q3, verbatim>"
```

Read the contract before writing anything — the ID rules and field format are exact.
