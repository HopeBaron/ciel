---
name: beelzebub
description: Produce a grounded account of a codebase you did not write - a verified model of how it works, a cost-ranked list of where its structure is expensive, and proposals for changing it, each claim carrying its evidence. Use when handed an unfamiliar, inherited, or legacy repository to learn, review, audit, or take over; when asked why a system is hard to change, slow to onboard into, or keeps breaking in the same places; when asked where the technical debt is or what to refactor first; when asked how to structure a new feature, module, or boundary inside a codebase that already exists; before planning an extraction, migration, modularisation, or rewrite of code nobody has read end to end; when writing architecture documentation or a handoff for a system that has none; and when a request arrives with the architectural diagnosis already assumed but never checked against the code, because the assumption is the thing most likely to be wrong.
---

# Beelzebub

Study a codebase you did not write and produce three things: a **model** of how it works, a
**cost-ranked list** of where its structure is expensive, and **proposals** for changing it.
Every claim carries the evidence that produced it.

## Run the same study whatever the question was

Three agents were handed the same feature on the same day and asked three different questions —
"how should I improve this", "why does this keep breaking", "write me a handoff". They returned
three near-disjoint answers. The one asked "why does this keep breaking" read the git history and
found the real defect. The other two never ran a single `git` command, and missed it.

The wording of the request had picked the method. That is the failure this skill exists to
prevent, so the phases below are **not** selected to match the question. Run all of them. What
the question changes is Phase 0 and what you emphasise in the record — never which evidence you
go and get.

## Every claim carries a grade

Mark every factual statement in the record with exactly one:

- **`[verified]`** — you read the code, ran the command, or ran the test that shows it. Cite
  `path:line`, or the command and its output.
- **`[inferred]`** — you concluded it from things you verified. Say in one line what it rests on.
- **`[unknown]`** — the repository cannot settle it. Name the question and who could answer.

**`[unknown]` is a result, and it is the grade most at risk.** You have nobody to interview. The
five books this skill comes from all assume a colleague to ask — maintainers to chat with, a
demo to watch, a second person to tell the story of the system to — and you have none of them.
The failure that produces is not silence. It is a fluent, plausible account of intent that
nobody can check. An unaided agent studying this exact feature wrote *"it already exhibits what
you're presumably going for"* — inventing a goal for a team it had never spoken to.

**Never write a sentence about why someone made a decision unless a comment, commit message, or
document says so.** Where the reason is not recorded, the reason is `[unknown]`.

## Phase 0 — Frame

Nothing in the corpus behind this skill will tell you what a good architecture is. All five
sources refuse it: *"In isolation, an architecture is never good or bad"*; *"'better' is context
dependent"*; recovering an architecture from legacy code is *"beyond the scope of this book"*.

So "better" is not a property you can assert. It is only ever relative to something named in
advance — before you have looked at anything and can be influenced by what you find.

Write into the record, before opening a source file:

1. **The question you were asked**, verbatim.
2. **The quality attribute at stake** — modifiability, or performance, or onboarding time, or
   the ability to extract a component. One or two, named. Not a list of virtues. Where you got
   it: the request, the README, the tests, or `[inferred]`.
3. **The scope** — which directories are in, which are out.

If the request names no quality attribute and you cannot infer one from the repository, ask.
This is the one question worth interrupting for; every other missing human input becomes an
`[unknown]`.

**Done when:** the record's first section names a quality attribute specific enough that a
Phase 4 proposal could be judged against it, and you have not yet formed an opinion about the
code.

## Phase 1 — Mine the history

**This is the phase that gets skipped, and skipping it is the single largest observed defect.**
Two of three unaided agents never ran `git` at all. The one that did found in two commits what
the others missed entirely with more files read.

Static structure tells you what *could* be a problem. The commit log tells you what *has been*
one. Run the analyses in [HISTORY.md](references/HISTORY.md) — change frequency, change
coupling, ownership, and the trend check — over a stated window. Everything there is plain
`git` and standard shell.

Three results carry the most weight:

- **Change frequency crossed with size.** Concentrated, not evenly spread. The head of this list
  is where cost lives; the long tail is not worth touching.
- **Change coupling that crosses a boundary.** Files that change together but live in different
  modules. This is the strongest available evidence against an intended separation of concerns,
  and no static dependency tool will show it.
- **What the history says was already fixed.** Read the commits that touched your candidates.
  A problem the team has already diagnosed and repaired twice is a different finding from a
  fresh one — and reporting it as fresh makes you look like you did not look.

**Mining is cheaper than the reading it replaces.** The ranked analyses are aggregates, not log
dumps — the whole set costs on the order of a thousand tokens. Of three unaided agents on the
same feature, the one that mined the history used the *fewest* tokens of the three and found the
defect the other two missed: it opened 15 files instead of 24 and 27, because the ranking told
it which ones mattered. If this phase is costing more than the reading it saves, you are dumping
diffs instead of ranking. [HISTORY.md](references/HISTORY.md) says where that happens.

**When the history is unusable** — shallow clone, squashed, imported, or a repository only days
old — say so explicitly in the record and state that the ranking has lost its cost axis. Rank on
structure and reading instead, and mark that ranking `[inferred]`. Do not present a
structure-only ranking as though it were cost-weighted. A directory restructure inside the
window distorts file-level counts across it; check for one before trusting the numbers.

**Done when:** the record holds a ranked candidate table, the numbers behind it, the window you
chose, one sentence on why that window, and — where relevant — the commits that already
addressed a candidate.

## Phase 2 — Read

Rank by measurement; confirm by reading. A measurement nominates a suspect. Only reading the
code convicts one.

**Sort and inspect the outliers. Never apply a numeric cut-off.** A threshold hides how many
ordinary entities there are and encodes a coding standard you do not have. This holds for every
signal here — change frequency, size, coupling, author count. Say "third by change frequency",
never "exceeds the limit".

For each candidate in rank order, write down what you expect it to be and how it is put
together, then read it and find out whether you were right. **Log confirmations and mismatches
both. A mismatch is the valuable half** — it is where your model was wrong and is about to stop
being wrong.

Then trace concepts, not files. Reading a file at a time is what produced the baseline's worst
miss: an agent read all four files containing the same duplicated idea, one after another, and
never saw it, because it reported per-file impressions and never asked where else this idea
lives. For each concept the candidate handles, search for every other place that names or
re-implements it.

**Done when:** every Phase 1 candidate has been read and its entry is either confirmed as a weak
point or **explicitly cleared**. A study that convicts every suspect it nominated did not do
this phase — it decorated Phase 1.

## Phase 3 — Diagnose

A weak point is not a smell, and not code you dislike. It is a place where the structure costs
something. Each entry in the record has four required parts:

| Part | What it must contain |
|---|---|
| **Location** | `path:line` |
| **Mechanism** | What about the structure creates the cost — named, from the catalogue in [WEAK-POINTS.md](references/WEAK-POINTS.md) |
| **Cost** | What it has actually cost, in evidence: a commit that touched N files to make one change, a defect that recurred, a test that cannot be written. Graded. |
| **Serves** | Which Phase 0 quality attribute this harms, and how |

**An entry with an empty Cost is a preference.** Delete it or complete it. Unaided agents
returned six and nine findings respectively with no cost on any of them, ordered by nothing.

**An entry with an empty Serves is a true observation about code nobody asked you to improve.**

Order the list by cost. Severity adjectives are not an ordering; change frequency is.

Record honestly rather than paper over: **business intent is not recoverable from code.** What
the system does is knowable; what it was supposed to do is not. Where behaviour looks wrong,
record it as suspicious with your reasoning, mark it `[unknown]`, and name it as a question for a
person. Do not silently correct it, and do not encode it as intended.

**Done when:** every weak point has all four parts filled, the list is ordered by cost, and — if
reading cleared every candidate — the record says so and names what was checked. A phase that
finds nothing is complete when it shows its work; it is only skipped when it shows nothing.

## Phase 4 — Propose

Read [MOVES.md](references/MOVES.md) before writing proposals — it carries the move catalogue
and the wrap-refactor-replace decision rule.

Each proposal is a **move** with five required lines:

```
Move:           <short name>
Removes:        <the Phase 3 weak point, by its record ID, and how the cost goes away>
From:           <the structure as it is now, [verified], with a citation>
To:             <the structure proposed>
At the cost of: <what gets worse - this line is never empty>
```

**A named architecture — layers, hexagonal, event-driven, microservices — may appear only on the
`To:` line.** Never as the proposal itself. A move whose `Removes:` line points at no recorded
weak point is a preference wearing a proposal's clothes.

**`At the cost of:` is never empty.** Every structural change trades something: types cost
ceremony on every future edit, extraction costs indirection, splitting costs locality. A move
with no stated cost has not been thought about — see [MOVES.md](references/MOVES.md) for the
pairs that conflict reliably.

**Prefer the smallest reversible move that removes a named cost.** Sequence moves so the system
runs after each one.

**Every weak point ranked above the cut is either addressed by a move or explicitly listed as
accepted.** Silence about one reads as an oversight.

**Stop at the proposal.** Hand back the record. Do not begin editing — the study's value is that
someone can disagree with it before code moves. If the user then wants the change made, the
first step is a safety net over the behaviour being preserved, not the restructuring.

**Done when:** every move has all five lines filled, every `Removes:` cites a Phase 3 entry, and
no `At the cost of:` line is empty.

## Designing something new inside this codebase

When the request is "how should I structure this new feature / module / boundary" rather than
"what is wrong here", the study is what makes the answer more than a pattern name. Run every
phase over the code the new work will touch and sit beside. Phase 3 usually comes back with
nothing to convict — there is no existing feature to be a weak point in — and its done-when
covers that: say so, and name what you checked. Write the proposal as Phase 4 moves whose
`From:` is the structure that exists and whose `Removes:` is the Phase 0 quality attribute at
risk rather than a recorded weak point.

**On a blank page this skill has nothing to offer** — every technique here reads something that
already exists. Say so and design without it.

## The record

One file, opened in Phase 0 and appended to in every phase, structured as specified in
[RECORD.md](references/RECORD.md). Default `docs/study-<scope>.md`; the user may name another.

**Write it as you go.** Not at the end. The corpus treats its own sketches as disposable —
*"there is little value in keeping them around"*, *"put the map on the wall near the coffee
machine"* — because the people who made them keep the understanding. You keep nothing. There is
no wall, no team walking past it, and no memory between sessions. **The record is not a
byproduct of the study; it is the study's only durable output.**

[RECORD.md](references/RECORD.md) states the structural rules — never leave a section empty,
record each fact once. The one worth restating here, because it is the one that gets broken: no
section is a byproduct written up at the end, and **collect every `[unknown]` into one list** at
the end, where a person can answer them in a single pass. That list is the handoff.

## Not this skill

- **Making the change.** This produces a proposal and stops.
- **Reviewing a diff or a pull request.** Different job, different unit of work.
- **Explaining one function or one file.** Read it and answer. Five phases on a single function
  is the most likely way this skill fires when it should not.

## Reference files

- [HISTORY.md](references/HISTORY.md) — the `git` analyses, windows, and how to read their output. Phase 1.
- [WEAK-POINTS.md](references/WEAK-POINTS.md) — the catalogue of mechanisms, for naming what is wrong. Phase 3.
- [MOVES.md](references/MOVES.md) — the move catalogue and the wrap-refactor-replace rule. Phase 4.
- [RECORD.md](references/RECORD.md) — the record's required structure. Open it at Phase 0.
