---
name: writing-prototypes
description: Design-by-contract stubbing mode. Before real implementation, sketch pure stubs — signatures, types, contracts, zero logic — walk the user through the design before a line of implementation exists. Only activate if the user explicitly invokes it by name, or asks to "sketch", "stub out", "prototype the interface", "design first", "figure out the shape" before writing real code. Not for ordinary coding requests, even nontrivial ones, unless user wants the interface settled first — explicit invocation only.
disable-model-invocation: true
---

# Writing Prototypes (stub-first design)

Contract-first design, before implementation. Not about saving typing — about putting the *shape* in front of the user while still cheap to change, not after it's buried in logic they now have to read around.

## What a stub is

Skeleton, flesh deliberately missing:

- Function/method signatures, real names, real types. Not `doStuff(x)`.
- Class/interface definitions: fields, methods, relationships.
- Docstrings/comments stating the *contract*: preconditions, postconditions, invariants, what errors when. Not what the code does internally.
- Bodies: `TODO`, `NotImplementedError`, `raise NotImplementedError`, `unimplemented!()`, `pass  # stub` — language's nearest equivalent. Nothing that runs, computes, branches on real data, touches I/O.
- Stubs calling other stubs — fine, encouraged even. Composing a design out of stubbed pieces is how boundaries get tested. Off-limits: any stub producing a real result, even simplified or hardcoded. A hardcoded "fake" return is an implementation choice in disguise — hides the exact questions this skill exists to ask.

Catch yourself writing an `if`, a real loop, a computation, a call to a real (non-stub) dependency — stop. Implementation, not design.

## Where stubs live

Not for keeps. Scratch/temp location only — session scratchpad if there is one, `/tmp` otherwise. Never the project tree. No creating/overwriting real project files, no `git add`, no commits, during this phase. Real source gets written fresh at implementation time, informed by the agreed stub, not promoted from it. No cleanup to remember, no stray `NotImplementedError` bodies left behind if implementation stalls or gets handed off.

## Workflow

1. **Draft the stub**, scratch location. Only the pieces that matter for the design question — not the whole system if the user's just settling one module's shape.
2. **Present as a design, not a deliverable.** Name the decisions baked in: why this boundary here not there, why this method on this type, assumed data ownership/lifetime, error propagation, what's left out.
3. **Ask, don't assume.** Naming, public vs. internal, sync vs. async, dependency injection vs. construction, error contract — ask, don't pick silently. Silent choices are what this skill exists to kill.
4. **Iterate on the stub, not prose.** Pushback → change the stub, show the shape diff. Don't just describe the change and move on.
5. **Stop at sign-off.** Shape agreed → stub-and-discuss phase over. Implementation is a separate step — say so, don't start filling bodies unless asked.

## Why

Cheap to fix in a stub, expensive once real logic exists — review effort and sunk cost both fight reopening a bad boundary after the fact. Interface first, every nonobvious call turned into a question instead of a silent assumption — that's what makes "common ground before code" real instead of aspirational.
