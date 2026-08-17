---
name: tracer-bullet-coding
description: Vertical-slice discipline for multi-layer feature work. Build feature-by-feature, each one end-to-end through every layer it touches (schema/DB, backend, API, frontend), run and verified before the next — never one whole layer across all features at a time. Use whenever a task spans multiple features that each touch multiple layers, or files across a stack, or is a "build out X, Y, and Z" request, even without the words "vertical slice" or "tracer bullet". Especially for early or exploratory builds where layer boundaries aren't settled and up-front design would be wasted.
---

# Tracer Bullet Coding

Pragmatic Programmer's tracer bullet: thin round, straight through the whole system, real ammo the whole way. See where you land, not where you aimed.

## Failure mode this prevents

Layer-sweep, the default AI ordering: all schemas for every feature, then all endpoints, then all UI. Nothing runs until the final pass, so a bad assumption in layer 1 is baked into N features before layer 2 exposes it. Nothing demoable, nothing verified, until the sweep ends.

Invert it: one feature, straight down every layer it touches, working and verified, then the next.

## Workflow

1. **Name the features and the layers each touches.** No doc needed — just know the slices before slice one.
2. **One feature, every layer, real code.** No stubs, mocks, or TODOs. Minimal per layer is fine — simplest schema, simplest endpoint, simplest UI — but each piece runs and the next layer genuinely depends on it. Thin, never fake.
3. **Run it. Verify end-to-end** before moving on — execute the path, hit the endpoint, load the UI, run the tests. Integration mismatches caught at 1x cost, not 5x.
4. **Next feature, same full-depth pass.** Reusing slice 1's shared infra (schema, API client): fine. "Fill in this layer later": not fine.
5. **Exception: one-time shared setup** (DB init, scaffolding, build config) up front, minimal, just enough for slice 1. Test: does this serve one feature or all of them equally? Only "all" goes up front.

## Why this hits AI harder

Layer-sweep *looks* organized — all models, then all routes, then all views, every pass locally coherent — which hides that nothing works yet and a bad layer-1 call is riding uncaught through every feature. Vertical trades that surface tidiness for cheap continuous feedback.

## vs. other skills

Not [[writing-prototypes]] (stub-first, fake signatures, shape before code). Here every layer is real from the start — thin, never fake. Prototypes settle shape; this builds.
