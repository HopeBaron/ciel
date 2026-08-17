---
name: tdd
description: Test-driven development — one failing test first, confirmed failing for the right reason, then minimal code to pass. Use when the user asks for test-first/TDD work, or asks you to implement anything in a repo that already has a test framework. Detect the framework from the repo (pytest, jest/vitest, go test, cargo test, rspec, junit, etc.) — don't ask, look.
---

# TDD

Red, green, done. No step skipped, none gold-plated.

## Why the order

A test written after the code only proves the code does what it does; a wrong assumption baked into both survives. Watching a test fail first proves it exercises what you think it exercises. No red step, no evidence.

Minimal-to-pass follows from the same logic: code written to satisfy a test is scoped by the test. Code written from imagination is scoped by guesses about the future — mostly wrong, all costing review time now.

## Workflow

1. **Find the framework.** Read the repo: `package.json` (jest/vitest/mocha), `pytest.ini`/`pyproject.toml`/existing `test_*.py`, `go.mod` + `_test.go`, `Cargo.toml`, `*.gemspec`/`spec/` (rspec), `pom.xml`/`build.gradle` (junit). Match existing test naming and structure exactly — the new file should look like the same author wrote it. Truly nothing there? Pick the ecosystem default, say so in one line.

2. **Pick the slice.** One behavior, statable in a sentence. Not "handle auth" — "reject a login with an empty password". This step is the loop variable; you return here after every green.

3. **Red.** Write the test. Run it. Read *why* it failed. A typo or import error is a broken test, not red. Fix the test — not the code — until the failure is the assertion you meant.

4. **Green.** Least code that passes. Hardcoding a return is legitimate green if no test forces more; the next test will. Cases no test asks for have no test protecting them and no test proving they're needed.

5. **Run the full suite.** Green, and nothing else broke.

6. **Refactor, only now**, with the suite as safety net: duplication and naming in what you just touched. Re-run after. Nothing to clean? Skip — refactoring isn't mandatory every cycle.

7. **Repeat from 2** until the task is covered. Cycles small enough that "what was I doing" has an obvious answer mid-interruption.

## Guardrails

- Never write implementation and test in the same pass. Caught writing both before running anything: stop, run the test alone.
- Code exists before its test — even code you wrote seconds ago on impulse? Drop it, restart from red. Code-before-test is cheating: the test gets shaped to fit code that already worked, so it proves nothing.
- A test that passed on first run and never failed is suspect — unseen failing means unproven failable. Force one real failure before trusting it.
- Retrofitting tests onto a finished change isn't TDD, it's testing after. TDD is the order of operations, not the presence of tests.
- Genuinely exploratory asks ("try a few approaches, see what sticks") don't fit TDD. Say so, offer to switch back once an approach is chosen.
