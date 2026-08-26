---
name: raphael
description: Author, improve, and test Claude Code skills. Use when writing a new skill, editing or fixing an existing one, deciding what belongs in SKILL.md versus a reference file, wording a description so it triggers reliably, or checking whether a skill actually changes an agent's behaviour.
---

# Raphael

A skill is not done when it reads well. It is done when you have watched it change an agent's
behaviour.

Two fresh agents given the same authoring task both produced a plausible skill, both skipped
testing entirely, and both bolted an exemption onto a rule and could not resolve the
contradiction they created. Those are the failures this skill exists to prevent.

## Entry

State the entry and its phases before touching anything. The subset is fixed per entry, not
chosen: announcing it makes a wrong entry visible immediately.

| Entry | Phases | Baseline arm |
|---|---|---|
| `create` | describe, baseline, structure, enforce, test | run the task with no skill |
| `improve` | describe, baseline, structure, enforce, test | snapshot the current skill, run against it |
| `fix-triggering` | describe, test | trigger eval only |
| `test` | baseline, test | no edit is made |

Say it plainly: `Entry: fix-triggering — phases: describe, test.`

## Phase 1 — Describe

The description is the whole triggering mechanism. It is injected into every query, so it is
pruned harder than the body.

**Formula:** `<what it does>. Use when <branch>, <branch>, or <branch>.` Front-load the first
word. 100-200 words.

**The one rule that is not obvious:** the description states *when*, never the workflow. A
description that summarises the sequence gets followed **instead of** the skill body. One
observed case: a description saying "code review between tasks" made an agent do one review
where the skill specified two.

For a discipline skill, name the moment of violation rather than the topic:
`Use when implementing any feature or bugfix, before writing implementation code`.

**Hard constraints** (`scripts/validate.py` enforces these):

- `name`: `^[a-z0-9-]+$`, max 64, no leading/trailing hyphen, no `--`
- `description`: max 1024 chars, **no `<` or `>`**
- Allowed frontmatter keys, closed set: `name`, `description`, `license`, `allowed-tools`,
  `metadata`, `compatibility`, plus the Claude Code keys `disable-model-invocation` and
  `argument-hint`. Anything else fails. (Anthropic's own validator rejects the last two; this
  one allows them because Claude Code is the only target here.)

**Invocation mode.** Default to user-invoked (`disable-model-invocation: true`) — zero context
cost. Choose model-invoked only when the agent must reach the skill on its own or another skill
must reach it. A user-invoked skill can never be called by another skill; make it an instruction
to the human instead.

**Done when:** the description names what the skill is and every distinct branch that should
trigger it, and contains no step, sequence, or "then".

## Phase 2 — Baseline

Skipping this is the failure mode with the strongest evidence behind it. Both baseline agents
skipped it, and one called it "a real gap rather than a considered pass".

Write 2-3 realistic prompts a user would actually send, then run the arms your entry calls for.

- `create` — there is only one arm, because the skill does not exist yet. Run the task **unaided**
  and read what the agent does wrong. This arm is the whole point: it tells you what to write.
- `improve` — two arms, spawned **in the same turn** so conditions match: current version against
  no skill, or new against snapshot. Do not run one and collect the other later; conditions drift.

Baseline the **behaviour you want to change**, not the artifact. If the skill is meant to change
how an agent converses, run a conversation; do not ask an agent to write a skill about conversing
and read that instead. The two produce different answers, and only the first one predicts
behaviour.

Read the transcripts, not just the outputs.

Capture, verbatim, every rationalisation and every wrong turn. These are the raw material for
Phase 4; inventing them later produces enforcement that defends against nothing.

**If the no-skill arm does not exhibit the failure, stop. There is nothing to fix.**

**Done when:** you can name the specific failure the skill must prevent, in the agent's own
words, quoted from a transcript.

## Phase 3 — Structure

**Match the form to the failure.** This is the highest-value decision in the whole skill. The
form that fixes one failure type measurably backfires on another.

| Baseline failure | Right form | Wrong form |
|---|---|---|
| Knows the rule, skips it under pressure | Prohibition + iron law + rationalisation table | Soft guidance ("prefer", "consider") |
| Output has the wrong shape | Positive recipe: what the output IS, its parts, in order | Prohibition list |
| A required element is omitted | Structural: a REQUIRED slot in a template | Prose reminders |
| Behaviour should be conditional | Conditional on an **observable predicate** | Unconditional rule + exemptions |
| Doesn't know the concept | Vocabulary: definitions, `_Avoid_:` lists, aphorisms | Rules |

**No nuance clauses.** "Don't X unless it matters" reopens the negotiation. Both baseline agents
wrote a rule, attached an exemption, and reported the two "pull against each other" with no way
to resolve it. **Exemption clauses do not scope** — "this limit doesn't apply to code blocks"
still suppresses code blocks. If part of the output must be exempt, restructure so the rule
cannot reach it.

**Prompt the positive.** A prohibition drags the forbidden behaviour into context and makes it
more available. State the target behaviour so the banned one is never spoken. Keep a prohibition
only as a guardrail you cannot phrase positively, and pair it with the positive target.

**Body shape** by genre — read `references/GENRES.md` for the matching skeleton. Genre picks the
shape only; it does not set the enforcement dose.

**Progressive disclosure.** Inline what every branch needs; push behind a pointer what only some
branches reach.

| Threshold | Rule |
|---|---|
| SKILL.md | under 500 lines; near it, add hierarchy rather than deleting meaning |
| Reference over 300 lines | add a table of contents |
| Reference depth | exactly one level from SKILL.md |
| Code under 50 lines, all concepts | stays inline |

Link at the point of use, mid-sentence, with the condition attached: "read X when Y". Never use
`@`-links — they force-load immediately.

**Done when:** every section traces to a failure observed in Phase 2, and every pointer carries
the condition under which to follow it.

## Phase 4 — Enforce

**Enforcement density is proportional to blast radius times observed defection rate.** Genre does
not set it. An absolute is earned only when you watched the defection in Phase 2; an unearned
absolute trains the reader to skim your emphasis.

Default state is **zero devices**. If Phase 2 observed no defection, that is a pass, not a gap.

Read `references/ENFORCEMENT.md` when Phase 2 showed a rule being skipped under pressure. It
carries the iron law, the rationalisation table, red flags, and the persuasion doses.

**Done when:** every device present names the transcript line that earned it, or it is deleted.

## Phase 5 — Test

Read `references/TESTING.md` for method. It covers micro-tests, trigger evals, pressure tests
and the judge stance.

The bar in short: run each trigger query three times and threshold the rate; make negatives
near-misses, not obvious misses; and no assertion counts if it passes in both the with-skill and
without-skill arms.

If the skill is user-invoked it has no model-facing description, so the trigger eval does not
apply and its absence is not a gap. Say so out loud rather than skipping it silently.

When a test fails, patch and re-run rather than reasoning about the fix. Each iteration changes
one thing; if you change three, you learn nothing about which one worked.

**Done when:** the skill produces the corrected behaviour on the same prompts that produced the
failure in Phase 2, and you have read the transcript rather than the output alone.

## Before you finish

Run `python3 scripts/validate.py <skill-dir>`.

Then check the things a script cannot:

- Every line changes behaviour versus the model's default. Delete whole sentences, never trim
  words from them.
- One term per concept, used throughout.
- No section duplicated between SKILL.md and a reference file.
- Skills that must NOT be called next are named, if a wrong next step is plausible.
- Dependencies are written as `Call the Skill tool with "<name>"`, one skill per call, and the
  target is model-invoked.
- No scaffold files that nothing uses.

## Reference files

- `references/GENRES.md` — the six body skeletons and when each applies.
- `references/ENFORCEMENT.md` — iron laws, rationalisation tables, red flags, persuasion doses.
- `references/TESTING.md` — baselines, micro-tests, trigger evals, pressure tests, judging.
- `references/COMPOSITION.md` — skill-to-skill calls, handoff artifacts, routers, discovery.
- `references/ARTIFACTS.md` — specifying an output document the skill produces.
