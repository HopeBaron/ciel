---
name: tracer-bullet-coding
description: Vertical-slice discipline for multi-layer feature work. Forces implementation feature-by-feature, end-to-end through every layer (schema/DB, backend, API, frontend, etc.), with each slice actually run and verified working before starting the next feature — instead of finishing one whole layer for all features before moving to the next layer. Use this whenever a task involves multiple features that each touch multiple layers, multiple files spanning a stack, or "build out X, Y, and Z" style requests, even if the user doesn't say "vertical slice" or "tracer bullet" explicitly. Especially relevant for early-stage or exploratory builds where the layer boundaries aren't settled yet and full up-front design would be wasted work.
---

# Tracer Bullet Coding

Pragmatic Programmer's tracer bullet: thin round, straight through the whole system, real ammo the whole way. See where you land, not where you aimed.

## Failure mode this prevents

Default AI ordering: layer-sweep. All schemas for every feature, then all endpoints, then all UI. Nothing works till the last pass — so a bad assumption in layer 1 gets baked into N features before layer 2 ever exposes it. Zero demoable, zero verified, until the whole sweep's done.

Fix: invert it. Per feature, straight down through every layer it touches, working, verified — then next feature.

```
Layer-sweep (avoid):          Vertical slice (do):
  DB:    F1 F2 F3 F4 F5         F1: DB -> API -> UI, run, confirm
  API:   F1 F2 F3 F4 F5         F2: DB -> API -> UI, run, confirm
  UI:    F1 F2 F3 F4 F5         F3: DB -> API -> UI, run, confirm
                                 ...
```

## Workflow

1. **Name features + layers each touches.** No formal doc needed — just know the slices before slice one starts.
2. **One feature, every layer, real code.** No stubs, no mocks, no TODOs. Minimal version per layer is fine — simplest schema, simplest endpoint, simplest UI — but each piece must actually run and the next layer must actually depend on it. Thin, never fake.
3. **Run it. Verify end-to-end** before the next feature — execute the path, hit the endpoint, load the UI, run the tests. Catches integration mismatches at 1x cost instead of 5x.
4. **Next feature, same full-depth pass.** Reusing shared infra from slice 1 (schema, API client) — fine. "Come back and fill in this layer later" — not fine.
5. **Exception: one-time shared setup** (DB init, scaffolding, build config) — up front, minimal, just enough for slice 1. Test: does this piece serve one feature, or all of them equally? Only "all of them" belongs up front.

## Why this hits AI harder

Layer-sweep *looks* organized — all models, then all routes, then all views, each pass locally coherent — while hiding that nothing works till the end and a bad call in layer 1 rides uncaught through every feature. Vertical trades that surface tidiness for real, cheap, continuous feedback.

## vs. other skills

Not [[writing-prototypes]] (stub-first, fake signatures, shape before code). Here every layer is real from the start — thin, never fake. Prototypes for settling shape; this for actually building.
