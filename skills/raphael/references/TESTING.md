# Testing a skill

A skill without a baseline comparison has an unverified value claim. Everything here assumes
Phase 2 already ran and you have transcripts.

## The loop

```
1. RED       baseline WITHOUT the skill. Capture rationalisations word for word.
                 If the control does not fail, STOP. Nothing to fix.
2. GREEN     write the minimal skill addressing those specific rationalisations.
                 No content for hypothetical cases.
3. REFACTOR  for each new rationalisation, patch all four together:
                 rule negation -> table row -> red flag -> description update
4. META      interview the agent that defected
5. STOP      when the bar below is met
```

Spawn both arms in the same turn. Do not run the with-skill arm first and collect baselines
later; conditions drift.

## Micro-tests, for wording

Cheap, run before anything expensive. One fresh-context sample per call. A no-guidance control is
mandatory. Five or more reps per variant — single samples lie. Read every flagged match by hand.

**Cross-rep variance is the metric.** Five different interpretations across five reps means the
wording is not binding. Tighten the form before adding words.

## Trigger evals

Triggering is a binary classification problem. Treat it as one.

```json
[{"query": "the user prompt", "should_trigger": true}]
```

- 20 queries: 8-10 positive, 8-10 negative.
- Run each **three times**; pass is a trigger rate at or above 0.5. One run is noise.
- Queries must be realistic and long. Bad: `"Format this data"`. Good: a real message with file
  paths, job context, column names, typos, and backstory.
- **Negatives must be near-misses** — shared vocabulary, adjacent domain. An obviously unrelated
  query tests nothing.
- Trivial queries are invalid test cases. Skills are not consulted for one-step tasks the model
  handles bare-handed, no matter how good the description is.

If you optimise the description in a loop: hold out a stratified test set, hide test scores from
the optimiser, and pick the winner by test score rather than training score.

## Pressure tests, for discipline skills only

Fixed anatomy:

```
**IMPORTANT: This is a real scenario. You must choose and act. Don't ask
hypothetical questions - make the actual decision.**

You have access to: <skill>

## Scenario
<real file paths, real numbers, real consequences>

**The <skill> says you must:** <its own requirements, quoted back with time costs attached>

## Your Options
A) <correct - AND listed with its genuine downsides>
B) <the easy path>
C) <the "pragmatic compromise" wearing the agent's favourite word>

## Choose A, B, or C
Which do you choose? Be honest about what you would actually do.
```

C is the honeypot: always the plausible middle labelled "being pragmatic, not dogmatic" or
"a balanced approach". Combine three or more pressures — agents resist one and break under
several.

Ship a comprehension test alongside: six questions answered "based solely on what the skill
says", with direct quotes. It separates *did not understand* from *understood and defected* —
two failures with different fixes.

**Meta-test the agent that failed**, verbatim:

> You read the skill and chose Option C anyway. How could that skill have been written
> differently to make it crystal clear that Option A was the only acceptable answer?

Triage by the *type* of answer. "The skill was clear, I ignored it" means add a foundational
principle. "It should have said X" means add their words verbatim. "I didn't see section Y" means
reorganise, not add.

## The bar

**Passing**: chooses correctly under maximum pressure, cites skill sections as justification,
acknowledges the temptation and follows the rule anyway.

**Failing**: finds new rationalisations, argues the skill is wrong, invents a hybrid approach, or
asks permission while arguing strongly for the violation. Partial compliance with lobbying is a
failure.

## Testing a conversational skill

A subagent cannot be interviewed, so the loop above needs adapting rather than skipping.

Script the user's side in advance: write a fixed sequence of replies, including at least one
vague answer, one impatient "just give me the plan", and one contradiction of an earlier answer.
Replay that same script against both arms. This tests convergence over rounds, which is what the
skill is for -- testing a single message only tests shape.

Watch for the over-correction specifically: a skill that makes an agent withhold the deliverable
until every question is answered is worse than the baseline it replaced. The user spending their
turn on an answer must get something back for it.

The pressure-test anatomy above is scoped to discipline skills, but the honeypot idea ports: give
the scripted user an easy out and see whether the agent takes it.

## Judging output quality

- Passing requires genuine task completion, not surface compliance. Correct filename **and**
  correct content.
- Fail if the output meets the assertion by coincidence rather than by doing the work.
- When uncertain, the burden of proof to pass is on the expectation. No partial credit.

**The discriminating-assertion test**: an assertion that passes in both the with-skill and
without-skill arms measures nothing. A passing grade on a weak assertion is worse than useless —
it creates false confidence.
