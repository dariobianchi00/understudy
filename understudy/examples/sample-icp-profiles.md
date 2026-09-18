# What the `icp` lens writes — a fictional example

Every product, person and number below is invented (CLAUDE.md §7). The shape
is the contract in `agents/lens-icp.md`; the run report lifts everything under
`## ICP profiles` whole.

---

# Nimbus Notes — icp — Run 2026-09-01 (t0000001)

The site says it is for "everyone who takes notes", and the product is built for one person selling something they teach.

## Top 3
1. **Solo course creator** — PRIMARY · fit 4.5 · propensity 4.0
2. **Tutoring micro-business (2–5 people)** — EXPANSION · fit 4.0 · propensity 2.8
3. **Conference speaker with a paid workshop** — NEXT-BEST · fit 3.5 · propensity 3.5

## Score
- **Score:** 5/10 — the product narrows its audience on every screen; the site widens it on every page

## Market shape
**Life-situation (consumer).** Pricing is per person per month (`persona-evaluator/screenshots/03-pricing.png`); proof is six individual testimonials, none with a company (`04-customers.png`); sign-up asks for a name and nothing else (`persona-novice/session.log:14`). One mixed signal: a "Teams" tier exists with no description (`03-pricing.png`).

## ICP profiles

### 1. Solo course creator — PRIMARY · fit 4.5 · propensity 4.0
- **Who:** One person who already teaches something live — a cohort, a class, a workshop — and wants to sell the material without building a site.
- **Find fifty of them:** Creator communities; anyone with a "join the waitlist" page for a course; a search for "sell my course without a website".
- **Job to be done:** "Get paid for the notes I already write, before Friday."
- **Trigger:** A cohort sells out, or a student asks "can I buy the notes?"
- **Why this product wins for them:**
  - A note becomes a paid page in two clicks — the novice did it by minute 9 (`persona-novice/session.log:31`, `07-publish.png`)
  - Pricing is per person, not per seat; the $9 tier covers it (`03-pricing.png`)
- **What it lacks for them:**
  - No way to bundle several notes into one purchase; the power-user tried for four minutes and gave up (`persona-power-user/session.log:52–58`)
- **Fit:** pain 5 · alignment 4 · evidence 4 · clarity 5 → 4.5
- **Propensity:** reach 4 · trigger 4 · pay 4 · openness 4 → 4.0
- **Case against (reasoning, not evidence):**
  - Instead they use: a payment link and a PDF — the status quo the site never names
  - Switching cost: low; the notes are already text
  - The fact that would kill it: they sell once and never again, so a subscription is the wrong shape
  - Cheapest test: five conversations with people who have a waitlist page; ask what they did last time someone wanted to buy
- **Not inferable from this run:** willingness to pay above the $9 tier — nothing in the run tested the $29 tier
- **Re-run persona:**
  ```yaml
  - name: creator
    device: desktop-1440x900
    goal: "Sell my next cohort's notes by Friday"
    gives_up_when: "I have to build a page before I can take money"
  ```

### 2. Tutoring micro-business (2–5 people) — EXPANSION · fit 4.0 · propensity 2.8
…

### 3. Conference speaker with a paid workshop — NEXT-BEST · fit 3.5 · propensity 3.5
…

### The trap — Agencies managing clients' notes · fit 2.0 · propensity 4.5
Easy to sell — the "Teams" tier looks made for them — and they would churn inside a quarter: nothing in the product separates one client's notes from another's (`persona-power-user/session.log:71`), and the sceptic asked exactly that question and left (`persona-sceptic/persona-debrief.md`, Q3).

### Candidates considered
| Candidate | Source | Fit | Propensity | Outcome |
|---|---|---|---|---|
| Solo course creator | named by site | 4.5 | 4.0 | primary |
| Tutoring micro-business | implied by product | 4.0 | 2.8 | expansion |
| Conference speaker | persona's read | 3.5 | 3.5 | next-best |
| Agencies | adjacent | 2.0 | 4.5 | trap |
| Students taking lecture notes | named by site | 2.5 | ? | dropped — no willingness to pay observed |
| Corporate L&D teams | adjacent | 2.0 | 2.0 | dropped — nothing multi-user works |

## Limits on this read
- **Captures:** website visit (with sweep) and product journey — both.
- **Personas:** novice · power-user · sceptic · evaluator — ⚠ INFERRED (generic)
- **Unscorable for every candidate:** none. `?` on willingness to pay for students only.
