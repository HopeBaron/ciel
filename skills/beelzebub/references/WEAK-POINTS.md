# Weak-point mechanisms — Phase 3

Name the mechanism from this catalogue rather than inventing a description. A named mechanism is
checkable against a known procedure; a paraphrase is not.

**Apply this catalogue to the head of the Phase 1 ranking, not to the whole repository.**
Applied to the long tail it produces volume, not value.

Every entry below still needs a **Cost** line from evidence. A smell with no cost is a
preference. The catalogue tells you what to *call* it; the history and the code tell you whether
it *matters*.

## Inside one unit

| Mechanism | What it is | Why it costs |
|---|---|---|
| **Nested logic** | Deep conditional nesting | Taxes working memory directly; nesting depth outranks conditional count as a difficulty driver |
| **Bumpy road** | One function with several separate chunks of nested logic | Each bump is a missing abstraction. Deeper bumps cost more; more bumps cost more to fix |
| **Long parameter list** | Many parameters | Overloads working memory. Count chunks, not parameters — two `x,y` pairs may be one "origin" and one "destination" |
| **Low cohesion** | One unit implements several responsibilities | Group method names by task; if the groups are disjoint, they are separate units. Prevents chunking, forcing line-by-line reading |
| **God class / Brain method** | A unit that accumulated responsibilities and now owns most of a subsystem's state | Every change touches it; nobody can say what it is for in one sentence; it cannot be tested |
| **Data container** | A class with only accessors and no behaviour | Behaviour that belongs to the data lives in its callers, duplicated |
| **Primitive obsession** | Built-in types standing in for domain concepts | Validation duplicates at every use; the type system cannot help; ranges go unchecked |
| **Control coupling** | A boolean parameter selecting an execution path | Two functions sharing a name and a body |

**Never split a unit on length alone.** Split on behaviour and on abstractions that have a name.
A line-count rule is an alert, never a decision.

## Between units

| Mechanism | What it is | Why it costs |
|---|---|---|
| **Change coupling across a boundary** | Files that change together but sit in modules the design says are independent | The strongest available evidence of architectural decay. Static analysis cannot see it |
| **Duplicated concept** | One idea implemented or encoded in several places, with no shared name | Changing the idea means finding every site, with nothing to link them. Near-duplicates are worse than exact ones: they read as equivalent and are not |
| **Message chains** | `a.b.c.d` — reaching through objects to reach data | Every intermediate becomes a dependency of the caller |
| **Feature envy / misplaced operation** | A unit that mostly manipulates another's data | The behaviour is on the wrong side of the boundary |
| **Shotgun surgery** | One conceptual change requires edits in many places | Measurable directly: find a past commit implementing one change and count the files |
| **Hidden dependency** | A relationship the code does not show — dynamic dispatch, reflection, registration, a shared string format | Callers cannot see what they depend on, so they break it |
| **Type-testing conditional** | Branching on a type or a kind, repeated at several sites | Adding a case means finding every branch |

## Naming

Misleading names cost more than ugly code. Measured: names that contradict behaviour raise
cognitive load significantly; inconsistent formatting does not.

- **Names that carry no information** — `Manager`, `Util`, `Helper`, `Impl`, `Data`, `Handler`.
- **Conjunction names** — `ConnectionAndSessionPool`. The `And` names the missing split.
- **Names that say more than the thing does**, or **less**, or **the opposite**. An `is`-prefixed
  identifier that is not a boolean; a getter that mutates; a comment that contradicts the code.
- **Vocabulary drift** — the words in commit messages, issues, and docs differ from the words in
  the identifiers. A structural finding, not a nitpick.

## The costs that are not in the code

- **Test suite as a burden.** Tests coupled to implementation internals; a local change breaking
  unrelated tests; test maintenance outpacing feature work.
- **Missing safety net.** No test covers the behaviour a proposal would have to preserve. This
  constrains every Phase 4 move and must be recorded.
- **Knowledge concentration.** A candidate whose history has one author who no longer commits.
- **Code nobody has touched in years that nobody understands.** Only a finding if something now
  requires changing it.

## Two things to say honestly

- **Over-modularisation has no detector.** You may observe fragmentation and say so `[inferred]`,
  but you have no cost signal for it. Say that.
- **A dead abstraction is a real finding.** Machinery that is built on every call and consumed by
  nothing — a value object only the tests read, an event nothing subscribes to. Report it as
  what it is: either unwired, or dead. You usually cannot tell which, and that is `[unknown]`.

## Before writing any entry

Has this already been fixed? See [HISTORY.md](HISTORY.md) §6 for how to check.
