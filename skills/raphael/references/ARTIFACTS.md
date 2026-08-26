# Specifying an output artifact

If the skill produces a document, specify it as a **literal fill-in template**, never as prose
description. One file per artifact.

## Shape

```
# {Artifact} Format

## Structure
  <a literal fenced block showing the artifact verbatim,
   with {placeholder} tokens for the variable parts>

## Rules
  - one bullet per constraint, each with a one-line justification
  - explicitly mark what is OPTIONAL and the condition for including it
  - a minimalism gate: "don't over-fill this"

## Edge cases
  <single vs multi-file layouts, numbering, when to create the file at all>

## Tone and vocabulary
  - Use exactly: <terms>   Never substitute: <term> for <term>
  - example phrasings that fit the style
```

## What makes it work

**The template must be fully worked, not abstract.** Show actual passing test code, an actual
command, an actual commit message. A worked example removes ambiguity about what "done" looks
like in a way prose cannot.

**Encode policy in the headings themselves.** `**Recommendations (advisory, do not block
approval):**` structurally prevents recommendations from gating. A heading that carries its own
rule cannot be ignored separately from the content under it.

**Restate the vocabulary, scoped to this artifact.** If a parent skill defines terms, the format
file repeats the use-exactly / never-substitute pairs for this specific deliverable. The format
spec is where lexical discipline gets enforced.

**Ban placeholders greppably.** Enumerate the literal strings — "TBD", "TODO", "Add appropriate
error handling", "Similar to Task N" — and call them failures. This turns a subjective quality bar
into a checklist a reviewer can run.

## Create lazily

Never scaffold empty structure in advance. Materialise a file only when there is real content for
it. A directory of placeholder files is a liability, not a head start.
