---
name: writing-prototypes
description: Design-by-contract stubbing mode. Sketch pure stubs — signatures, types, contracts, zero logic — and settle the shape with the user before any implementation exists. Activate only on explicit invocation by name, or when the user asks to "sketch", "stub out", "prototype the interface", "design first", "figure out the shape" before real code. Not for ordinary coding requests, however nontrivial, unless the user wants the interface settled first.
disable-model-invocation: true
---

# Writing Prototypes (stub-first design)

Put the *shape* in front of the user while it's still cheap to change — not after it's buried in logic they'd have to read around.

## What a stub is

Skeleton, flesh deliberately missing:

- Signatures with real names and real types. Not `doStuff(x)`.
- Class/interface definitions: fields, methods, relationships.
- Docstrings stating the *contract* — preconditions, postconditions, invariants, what errors when. Not internals.
- Bodies: `TODO`, `NotImplementedError`, `unimplemented!()`, `pass  # stub`, whatever the language offers. Nothing that runs, computes, branches, or touches I/O.
- Stubs calling stubs: encouraged — that's how boundaries get tested.

Never a real result, not even simplified or hardcoded. A fake return is an implementation decision in disguise, and it hides the exact question this skill exists to ask.

Writing an `if`, a loop, a computation, a call into a real dependency — stop. That's implementation.

## Where stubs live

Scratch only: session scratchpad, else `/tmp`. Never the project tree, never `git add`, never a commit. Real source gets written fresh at implementation time, informed by the agreed stub, not promoted from it. Nothing to clean up, no orphan `NotImplementedError` if the work stalls or changes hands.

## Workflow

1. **Draft the stub** in scratch. Only the pieces the design question turns on — not the whole system to settle one module.
2. **Present it as a design, not a deliverable.** Name the decisions baked in: this boundary and not that one, this method on this type, data ownership, error propagation, what's deliberately absent.
3. **Ask, don't assume.** Naming, public vs. internal, sync vs. async, injected vs. constructed, error contract — ask. Silent choices are what this skill kills.
4. **Iterate on the stub, not on prose.** Pushback → edit the stub, show the shape diff.
5. **Stop at sign-off.** Shape agreed, phase over. Implementation is a separate step — say so, don't start filling bodies uninvited.

## Why

A bad boundary costs one edit in a stub and a fight once real logic exists — review effort and sunk cost both resist reopening it. Interface first turns every nonobvious call into a question instead of a silent assumption.
