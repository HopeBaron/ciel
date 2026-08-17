---
name: tracer-bullet-coding
description: Vertical-slice discipline for tasks spanning multiple features across multiple layers or a whole stack — build each feature end-to-end and verified before starting the next, never one layer at a time across all features.
---

# Tracer Bullet Coding

Pragmatic Programmer's tracer bullet: thin round, straight through the whole system, real ammo the whole way. See where you land, not where you aimed.

## Failure mode this prevents

Layer-sweep, the default AI ordering: all schemas for every feature, then all endpoints, then all UI. It *looks* organized — every pass locally coherent — which hides that nothing runs until the final pass, so a bad layer-1 assumption rides uncaught into N features before layer 2 exposes it. Nothing demoable, nothing verified, until the sweep ends.

Invert it: one feature, straight down every layer it touches, working and verified, then the next. Trades surface tidiness for cheap continuous feedback.

## Workflow

1. **Name the features and the layers each touches.** No doc — just know the slices before slice one.
2. **One feature, every layer, real code.** No stubs, mocks, or TODOs. Minimal per layer is fine — simplest schema, simplest endpoint, simplest UI — but each piece runs and the next layer genuinely depends on it. Thin, never fake.
3. **Run it. Verify end-to-end** before moving on — execute the path, hit the endpoint, load the UI, run the tests. Integration mismatches caught at 1x cost, not 5x.
4. **Next feature, same full-depth pass.** Reusing slice 1's shared infra (schema, API client): fine. "Fill in this layer later": not fine.
5. **Exception: one-time shared setup** (DB init, scaffolding, build config) up front, minimal, just enough for slice 1. Test: does this serve one feature or all equally? Only "all" goes up front.

## vs. other skills

Not [[writing-prototypes]] (stub-first, fake signatures, shape before code). Here every layer is real from the start — thin, never fake. Prototypes settle shape; this builds.
