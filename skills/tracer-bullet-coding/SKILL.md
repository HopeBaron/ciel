---
name: tracer-bullet-coding
description: Vertical-slice build ordering for work spanning several features and several layers. Use when a request names more than one feature, command, endpoint, screen, or capability that each touch the same layers; when scaffolding a new app, service, or CLI with more than one capability; when adding a batch of endpoints, commands, migrations, or screens to an existing codebase; when a plan or task list is organised by layer — all the models, then all the parsers, then all the views — rather than by feature; when choosing what order to implement a multi-part feature set in; and when the pull is to build the shared foundation for everything before anything runs, because that is the ordering that hides integration failures until the end.
---

# Tracer Bullet Coding

Pragmatic Programmer's tracer bullet: thin round, straight through the whole system, real ammo the whole way. See where you land, not where you aimed.

## Failure mode this prevents

Layer-sweep, the default AI ordering: all schemas for every feature, then all endpoints, then all UI. It *looks* organized — every pass locally coherent — which hides that nothing runs until the final pass, so a bad layer-1 assumption rides uncaught into N features before layer 2 exposes it. Nothing demoable, nothing verified, until the sweep ends.

Invert it: one feature, straight down every layer it touches, working and verified, then the next. Trades surface tidiness for cheap continuous feedback.

## Dependency order is not build order

The instinct behind layer-sweep is a good one misapplied: *build what nothing depends on first.* Leaves before the composing layer — store before CLI, schema before endpoint before view.

That instinct is right, and what it orders is **the layers inside one slice**. It does not order the slices. A dependency graph has many valid linearisations, and sweeping one layer across every feature is the linearisation that maximises the distance between the first line of code and the first working path. Nothing about feature 2's schema requires it to be written alongside feature 1's — that grouping is tidiness, not dependency.

Dependency order **within** a slice. Feature order **across** slices.

## When the plan you were handed is a layer-sweep

Sometimes the layer ordering is not yours — the user stated it: *"first port all the config models, then all the parsers, then all the formatters."* What triggers this is an **ordering**, not a decomposition. "It needs a parser, a converter, and a renderer" only names the layers; that is the normal way to describe a stack and asks for nothing. Only a stated sequence across features is a layer-sweep.

When it is one, say what it costs, once, and offer the alternative:

> In that order nothing runs until the last pass, so a wrong assumption in the config models rides into every parser before anything exposes it. Porting one command end-to-end first proves the three layers fit and leaves it demoable. Want that instead?

Then take the answer. Reaffirmed, you build it their way — this skill informs the user's decision, it does not overrule it. Raise it once, at the start; do not re-open it at each layer boundary.

## Workflow

1. **Name the features and the layers each touches.** No doc — just know the slices before slice one.

2. **Shared setup only, before slice 1.** DB init, scaffolding, build config. Gate, applied per item: *does this serve one feature, or all of them equally?* Only "all" goes up front, and only enough of it to get slice 1 running. A column one feature needs is that feature's, not setup's. On a small project the right amount is routinely none — an empty step 2 is compliance, not an omission.

3. **One slice: that feature, every layer it touches, in dependency order, real code.** Callee before caller, so each layer has something real to call. Layers that sit beside each other rather than stacked — a renderer and a store both used by one command — have no order between them; take either.

   No stubs, mocks, or TODOs. Minimal per layer is fine — simplest schema, simplest endpoint, simplest UI — but each piece runs and the next layer genuinely depends on it. Thin, never fake.

4. **Run the real path.**
   **Done when:** you have executed the path a user would take — issued the request, run the command, loaded the page — and read the actual output. Not "the module imports", not "the layer compiles", not a mental trace. Integration mismatches surface here at 1x cost instead of Nx.

5. **Next slice, same full-depth pass.** Repeat from 3 until the feature list is empty.

## Slices after the first

Later slices land on code slice 1 already wrote. Three cases, all fine:

- **Reuse** — the layer already does what this feature needs; call it, change nothing.
- **Revision** — the layer needs a new column, a wider signature, another branch. Change it. Feedback arriving from slice 2 is the mechanism working, not a slice-1 defect.
- **No-op** — this layer needs nothing at all for this feature.

Not fine: "fill in this layer later."

A slice that reuses or no-ops through most of its layers is thin, and a thin slice is where step 4 gets skipped for feeling redundant. It is not redundant. The run is what proves the new feature reaches through code written for a different one — which is exactly the seam that breaks. **Every slice ends with the real path executed, however little code it added.**

## With other skills

`tdd` fires on the same tasks and composes one level down: a tracer slice is a feature through every layer; a tdd slice is one behaviour with one failing test. Many tdd cycles inside one tracer slice. Step 4 is the slice's integration run — where tests exist they are part of it, never a substitute for it.

Term collision worth holding straight: **slice** here means the feature, not the assertion.

Not stub-first design (`writing-prototypes`): that settles an interface's shape with fake signatures before implementation exists. Here every layer is real from the start — thin, never fake.
