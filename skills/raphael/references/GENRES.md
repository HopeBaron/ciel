# Genre skeletons

Genre picks the **body shape only**. It does not set the enforcement dose (that is blast radius
times observed defection rate) and it does not decide whether to test.

A skill can be two genres. If it is four, split it.

## Discipline — stop the agent doing the easy wrong thing under pressure

```
## Overview               one or two sentences, then the spirit/letter clause
## The Iron Law           fenced, all-caps, unconditional, followed by its consequence
## When to Use            graded: ANY... / ESPECIALLY when... / Don't skip when...
## The Process            numbered phases with explicit gates
## Red Flags              inner-monologue list, terminated by the required action
## Common Rationalizations   | Excuse | Reality | table
## Quick Reference
```

The "Don't skip when" list is not an exclusion list. It is a pre-emptive refusal of the three
commonest excuses, each with its counter in parentheses.

## Procedure — do these steps in order, in a real repo

```
# <Name>
<one-line job, then the defining constraint>
### 1. <Step>
    <action>
    **Done when:** <checkable AND exhaustive>
### 2. ...
```

Completion criteria need two properties. **Clarity**: can the agent tell done from not-done? A
vague bound ("understanding reached") invites stopping early. **Demand**: "every modified model
accounted for" forces thorough work where "produce a change list" does not.

For any skill that installs an enforcement mechanism, the completion criterion is to break the
rule deliberately and watch it fail. A check that does not fail on a violation is worthless.

## Vocabulary — install a shared mental model

```
# <Name>
<thesis sentence, key term bolded inline>
## Glossary              "Use these terms exactly" + Term: definition. _Avoid_: synonyms.
## <Visual anchor>       ASCII before/after, if the concept has a shape
## Principles            aphorisms written to be quoted verbatim by other skills
## <Applying it>         testable sub-questions that operationalise the abstraction
## Relationships         each term restated as a one-line ontology
## Rejected framings     name and refute the plausible-but-wrong adjacent model
```

`Term: definition. _Avoid_: near-synonyms.` is the load-bearing micro-format. It turns "pick good
words" into something checkable and gives other skills something to cite.

`## Rejected framings` pre-empts contamination from vocabulary the agent already knows. Naming
and refuting the wrong model is distinctive to this genre and unusually effective.

## Dialogue — script a multi-turn conversation

```
# <Name>
<stance sentence: "Interview the user relentlessly until...">
<the data structure: "Map this as a design tree...">
## <Turn mechanic>       rounds / frontier / phases
<literal output template for one turn, down to formatting>
## <Division of labour>
## <Termination condition>
```

Four mechanics that work. **Baseline them before writing any of them in** — measured behaviour
says agents already batch and already attach recommended answers unprompted, so prescribing those
two is usually a no-op. What agents reliably fail at is stopping: they terminate after one round,
proceed on assumptions they noticed privately, and write the user's escape hatch for them.

- **Batch by dependency, not one at a time.** Ask everything answerable now in one round; defer
  anything gated on an open question to a later round. Both baseline agents defaulted to
  one-question-at-a-time and both doubted it.
- **Every question carries the agent's own recommended answer.** Turns an interview into
  accept/reject rather than an essay prompt.
- **Facts are the agent's job; decisions are the user's.** Dispatch a subagent for anything
  discoverable; never ask the human what you could look up.
- **A named terminal state**, not "when you feel you understand".

## Orchestration — drive other agents

```
## Why subagents / Core principle
## When to Use  /  ## When NOT to Use
## The Process           numbered, with the dispatch points
## Model Selection
## <Loop with escalation ladder and round caps>
## Example Workflow      a transcript
+ one <role>-prompt.md per role, never inlined
+ scripts/ that print paths, never payloads
```

Context hygiene is the whole game: anything pasted into a dispatch prompt, and anything a
subagent prints back, stays resident and is re-read every later turn. Hand artifacts over as
files. Helper scripts print a path and nothing else.

Note the isolation exception: a subagent cannot read the parent skill's sibling files, so content
it needs must be inlined into its prompt. Say so explicitly when you break disclosure for this
reason.

## Router — dispatch to other skills

Names the other skills and when to reach for each. It can only hint at user-invoked skills;
nothing but the human can fire those.

A router must not lie. Whenever a skill it routes to is added, renamed, or removed, update the
router in the same changeset.
