---
name: tdd
description: Test-driven development — no implementation code exists before a test that fails without it. Use when implementing a feature, adding a behavior, or fixing a bug in a repo that already has a test framework; when the user asks for test-first or TDD work; when adding a case, branch, or error path to code that already exists; when implementation you already wrote has no test covering it; and especially when the change looks obvious enough that you already know what the code will be, because that is when the failing test gets skipped.
---

# TDD

Red, green, done. No step skipped, none gold-plated.

## Why the order

A test written after the code only proves the code does what it does; a wrong assumption baked into both survives. Watching it fail first proves it exercises what you think. No red step, no evidence.

The evidence is worth most where you feel you need it least. A guard written from a bug description and tested afterward passes — and hides that one of the three cases you "fixed" was never broken. You ship a correct patch and a wrong mental model, and the wrong model is what you carry into the next change.

Minimal-to-pass follows: code written to satisfy a test is scoped by the test. Code written from imagination is scoped by guesses about the future — mostly wrong, all costing review time now.

## Workflow

1. **Find the framework, then pin the baseline.** Read the repo: `package.json` (jest/vitest/mocha/`node --test`), `pytest.ini`/`pyproject.toml`/existing `test_*.py`, `go.mod` + `_test.go`, `Cargo.toml`, `*.gemspec`/`spec/` (rspec), `pom.xml`/`build.gradle` (junit). Match existing naming and structure exactly — same-author look. Truly nothing there? Ecosystem default, say so in one line.

   Then run the suite before touching anything and write down the counts and the name of every test already failing. Cost: seconds. Without it, every later result is unfalsifiable — you cannot tell a failure you caused from one that was waiting for you.

2. **Pick the slice.** One behavior, statable in a sentence. Not "handle auth" — "reject a login with an empty password". The loop variable; you return here after every green.

3. **Red.** Write the test. Run it. Read *why* it failed — the failure has to be the assertion you meant:

   | What you see | What it is | What to do |
   |---|---|---|
   | The assertion fails on the value | Real red | Go to green |
   | Module or symbol does not exist yet | Expected on a new file, but it is not evidence yet — no assertion ran | Add the smallest stub that makes the import resolve, re-run, land on the assertion |
   | Typo, wrong import path, bad fixture in the test | Broken test | Fix the test, never the code, and re-run |

4. **Green.** Least code that passes. Hardcoding a return is legitimate green if no test forces more; the next test will. Cases no test asks for have no test protecting them and none proving they're needed.

5. **Run the full suite and compare to the baseline.** Same failures as step 1, no new ones. Green is the wrong bar in a repo that was not green when you arrived: a suite failing identically before and after is a pass, and one new failure is yours even if the total went down. Confirm by test name, not by count.

6. **Refactor, only now**, suite as safety net: duplication and naming in what you just touched, including comments your change just made false. Re-run after. Nothing to clean? Skip — refactoring isn't mandatory every cycle.

7. **Repeat from 2** until the task is covered. A spec that lists four rules is four slices, not one; you return to step 2 after every green until the list is empty. Cycles small enough that "what was I doing" has an obvious answer mid-interruption.

## When a test passes the first time you run it

It has never failed, so it is unproven. You cannot yet tell "already correct" from "asserting nothing".

Make it fail on purpose, then put it back:

- Change the implementation to the plausible wrong version — the ordering you nearly wrote, the `>` you nearly typed — and confirm this test is the one that catches it.
- No implementation to break, because the behavior falls out of existing code? Break the data instead: add the key the lookup is supposed to miss, and watch the test go red.
- Restore, re-run, confirm green.

Two outcomes, both worth the thirty seconds. It failed as expected: the test is real, keep it. It still passed: the test asserts nothing — you have found a fake test, which is worse than no test, because it will be counted as coverage.

## Red flags

If you catch yourself thinking:

- "It's a one-line guard, I know what the failure is, just ship it."
- "The fix is right there, one more edit, nobody would notice."
- "Returning a bare 0 feels like a joke, I already know the whole rule."
- "It passed immediately — that case is covered, move on."
- "All of them passed on the first run, so no fixes were needed."

All of these mean the same thing: nothing has been watched failing, so nothing is proven yet. Return to step 3.

The last two are the easiest to miss, because they arrive wearing the costume of success.

## Guardrails

- Never write implementation and test in the same pass. Caught writing both before running anything: stop, run the test alone.
- Code exists before its test — even code you wrote seconds ago on impulse? Drop it, restart from red. The test gets shaped to fit code that already worked, so it proves nothing.
- Retrofitting tests onto a finished change is testing after, not TDD. TDD is the order of operations, not the presence of tests.
- A pre-existing failure someone else owns is not yours to fix mid-task. Record it in step 1, leave it, mention it when you report.
- The user asked you to try several approaches and pick one? That's exploration, and TDD doesn't fit it. Say so, and offer to switch back once an approach is chosen.
