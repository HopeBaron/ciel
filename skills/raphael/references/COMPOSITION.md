# Composition

## Reaching another skill

Write dependencies as an explicit instruction to call the tool, never as a file link and never as
a bare slash-name:

```
Call the Skill tool with "synthesis".
```

Naming the tool is what gets it fired. One skill per call — a step needing two is two calls.
Dropping the leading slash keeps it harness-neutral.

**This only works on model-invoked targets.** A user-invoked skill has no description, so nothing
but the human can reach it. When a step's precondition is a user-invoked skill, phrase it as an
instruction to the human: "tell the user to run `/setup-x`".

**Name which skills must NOT be called next** when a wrong next step is plausible. Without it an
agent free-associates to a plausible-sounding neighbour.

## Handoff between skills

- Pass **named, typed artifacts** — a spec, tickets with blocking edges, an agent brief. Never
  "the previous output".
- **Centralise shared config.** One setup skill's output is the single source every downstream
  skill reads. Repeat a verbatim escape hatch rather than re-encoding the mechanics: "X should
  have been provided to you. If not, tell the user to run `/setup-x`."
- **Resolve conditionals once, at setup.** Bake a choice into one resolved file rather than
  re-branching on it at every invocation.

## Routers

When user-invoked skills multiply past what you can remember, the cure is one router skill that
names the others and when to reach for each. It can only hint, never fire them.

Keep it honest: a new skill it never mentions, or a stale one it still routes to, is a router
that lies. Update it in the same changeset as the skill it routes to.

## Discovery

Only one skill can be pushed into every session; everything else is pulled by the model reading
`description` frontmatter. That is why the description carries the entire triggering load, and
why a description that summarises the workflow gets followed instead of the skill.

## Shared reference between two user-invoked skills

Neither can reach the other, so shared material can live in neither. Push it to a plain file
outside the skill system that both point at.
