---
name: writing-prototypes
description: Design-by-contract stubbing mode. Before writing any real implementation, sketch pure stubs — signatures, types, and contracts with zero logic — and walk the user through the design decisions before a single line of implementation is written. Only activate this skill if the user explicitly invokes it by name, or explicitly asks to "sketch", "stub out", "prototype the interface", "design first", or "figure out the shape" before writing real code. Do not activate it for ordinary coding requests, even nontrivial ones, unless the user has signaled they want the interface settled before implementation — explicit invocation only.
disable-model-invocation: true
---

# Writing Prototypes (stub-first design)

Contract-first design, applied before implementation. The point isn't to save typing — it's to put the *shape* of the code in front of the user while it's still cheap to change, instead of after it's buried in logic they now have to read around.

## What a stub is

A stub is the skeleton of a design with the flesh deliberately missing:

- Function/method signatures with real names and real types — not placeholders like `doStuff(x)`.
- Class/interface definitions: fields, methods, relationships between them.
- Docstrings or comments stating the *contract*: preconditions, postconditions, invariants, what errors can be raised and when — not what the code will do internally.
- Bodies that are `TODO`, `NotImplementedError`, `raise NotImplementedError`, `unimplemented!()`, `pass  # stub`, or the language's nearest equivalent. Nothing that runs, computes, branches on real data, or touches I/O.
- Stubs may call other stubs — composing a design out of several stubbed pieces is exactly the point, since it's how you surface whether the boundaries between pieces make sense. What's off-limits is any stub containing logic that actually produces a real result, even a simplified or hardcoded one. A hardcoded "fake" return is still an implementation choice in disguise — it hides exactly the questions this skill exists to ask.

If you catch yourself writing an `if`, a loop that does real work, a computation, or a call to a real dependency that isn't itself a stub — stop. That's implementation, not design.

## Where stubs live

Stubs are not for keeps — write them to a scratch/temp location (the session's scratchpad directory if one is available, otherwise a throwaway spot like `/tmp`), never into the project tree itself. Don't create or overwrite real project files during this phase, and don't `git add` or commit stub files. The project's actual source layout gets written fresh during implementation, informed by the agreed-on stub but not literally promoted from it — so there's no cleanup step to remember and no risk of a stub's `NotImplementedError` bodies lingering in the repo if implementation gets delayed or handed to someone else.

## Workflow

1. **Draft the stub** in the scratch location. Cover the pieces that matter for the design question at hand — don't stub out the entire universe of a large system if the user is only trying to settle one module's shape.
2. **Present it as a design, not a deliverable.** Show the stub and name the decisions embedded in it: why this boundary is here and not there, why this method belongs to this type, what's assumed about ownership/lifetime of data, how errors propagate, what's deliberately left out.
3. **Ask, don't assume.** For each nonobvious choice — naming, what's public vs. internal, sync vs. async, how a dependency gets injected vs. constructed, what the error contract is — ask the user rather than picking silently. Silent choices here are exactly what this skill is meant to prevent.
4. **Iterate on the stub, not on prose.** When the user pushes back, change the stub itself and show the diff in shape — don't just describe the change verbally and move on.
5. **Stop at sign-off.** Once the user agrees the shape is right, the stub-and-discuss phase is done. Implementing it is a separate step — say so explicitly, and don't start filling in bodies unless the user asks you to move forward.

## Why

Design mistakes are cheap to fix in a stub and expensive to fix in a finished implementation — once real logic exists, both the user's review effort and the sunk cost work against reopening a bad boundary. Writing the interface first, and forcing every nonobvious call into a question instead of a silent assumption, is what makes "common ground before code" actually true rather than aspirational.
