# The record — required structure

One file. Opened in Phase 0, appended to in every phase, never written at the end.
Default path `docs/study-<scope>.md`.

**Never leave a section empty.** Write `none`, `N/A because ...`, or `[unknown] — needs <who>`.
A blank section is indistinguishable from a forgotten one.

**Record each fact once** and link to it from elsewhere. **Every claim carries a grade**
(`[verified]` / `[inferred]` / `[unknown]`).

---

```markdown
# Study: <scope>

<date> · commit <sha> · <who or what ran this>

## 1. Frame

**Question asked:** <verbatim>
**Quality attribute at stake:** <one or two, named> — source: <where> [grade]
**Scope:** in: <dirs> · out: <dirs>
**Coverage:** read in full: <...> · skimmed: <...> · never opened: <...>

## 2. Evidence base

**Window:** <range>, because <one sentence>
**History is usable:** yes / no — <shallow? squashed? imported? restructure inside the window?>
**Build:** <ran / failed, verbatim error> [grade]
**Tests:** <count, pass/fail, duration, what they cover> [grade]
If the build or the suite does not run, that is a finding, not an obstacle. Record it here.

## 3. Model

What the system is and how a request moves through it. Per element: what it is for, the files it
is grounded in, what it talks to. Every line graded.

**Traced paths:** <entry point → work → what it returns or persists>, one per capability.
**Vocabulary:** the domain terms the code actually uses, and any that differ from the terms in
docs, commits, and issues.
**Hypotheses that were wrong:** what you expected, what is actually there. Do not drop these —
they are where the model got corrected, and the next reader will make the same wrong guess.

## 4. Ranking

| # | Candidate | Revisions | Size | Coupled to | Grade |
|---|---|---|---|---|---|

The measurements only. Nothing here is a finding yet.

**Cleared on reading:** <candidates the measurement flagged and the code exonerated, with why>
A ranking with nothing cleared was not confirmed by reading.

## 5. Weak points

Ordered by cost. One entry each:

### W1 — <name>
- **Location:** `path:line`
- **Mechanism:** <named, from the catalogue>
- **Cost:** <what it has actually cost, in evidence> [grade]
- **Serves:** <which Phase 0 quality attribute this harms, and how>
- **Already addressed?** <commits that previously repaired this, or `no`>

## 6. Proposals

### M1 — <short name>
```
Removes:        W<n> — <how the cost goes away>
From:           <structure now> [verified] `path:line`
To:             <structure proposed>
At the cost of: <what gets worse>
First step:     <smallest reversible change that can ship alone>
Safety net:     <tests that already cover this, or the ones that must be written first>
```

**Accepted, not addressed:** <weak points above the cut that no move targets, and why>

## 7. Open questions

Every `[unknown]` in the study, in one list, each with what would answer it and who could.

| # | Question | What would answer it | Who |
|---|---|---|---|

This list is the handoff. It is the part a person can act on that you could not.
```

---

## Notes on filling it in

**Write for the reader, not as a log of your process.** Nobody needs the order in which you
discovered things. Sections 3–7 are the deliverable; the phases were only how you got there.

**Explain any notation you introduce.** A diagram without a key is ambiguous.

**State what the record does not cover.** If the model describes six of nine modules, say which
three are missing rather than letting the reader assume completeness.

**Rationale is usually unrecoverable.** For a system you did not build, most of the *why* is gone.
Mark it `[unknown]` and put it in section 7. Never reconstruct what an interview would have said.
