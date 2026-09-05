# Moves — Phase 4

## First, decide what kind of problem it is

Before choosing a move, classify the component. The wrong category makes the best move useless.

| The component is | The move | Why |
|---|---|---|
| Stable, rarely changed, but painful for its callers | **Wrap it.** Present the interface the callers want; leave the inside alone | Rewriting code nobody has needed to change is risk with no payoff |
| Sound, but a bottleneck for change | **Restructure it in place**, behind tests | The structure is the cost; the behaviour is fine |
| Defect-ridden and heavily changed | **Replace it incrementally** behind a bridge — run old and new in parallel, migrate, then retire | Too broken to refactor, too load-bearing to cut over |
| Working, and nobody is complaining | **Leave it. Record why you left it.** | An untouched ugly file costs nothing |

**Fix the problem, not the symptom.** Trace the reported pain to the structure causing it. The
file that hurts is often not the file at fault.

## The moves

**Redistributing responsibility**
- **Extract a type for a duplicated concept** — the idea exists in several encodings with no
  shared name. Give it one. Often the code already names it in a comment or a class name.
- **Move behaviour to the data it operates on** — for a data container whose logic lives in callers.
- **Split a unit along its cohesion groups** — carve out one cohesive cluster at a time, promote
  it, reduce the original to a facade, then retire the facade. Never in one step.
- **Collapse a chain** — give the owner of the data a method that answers the question directly.
- **Replace a type-testing conditional with dispatch** — one implementation per case.
- **Introduce a seam** — a place where behaviour can be substituted without editing at that
  place. Every seam needs an enabling point. This is what makes an untestable unit testable.

**Boundaries**
- **Realign a boundary to the change coupling** — things that change together belong together.
  Slicing by business capability, with its data access, usually beats slicing by technical layer,
  which makes every ordinary change cross every layer.
- **Wrap a component you have decided not to migrate**, so its callers see the interface the new
  design wants rather than the one the old code has.
- **Bridge old to new** — write to both, read from the old until migrated, then retire it.
- **Deprecate rather than delete.**

## Preconditions that are not optional

**A safety net comes before the change, not after.** Where no test covers the behaviour a move
would preserve, the first step of the move is writing one against what the code *actually does* —
not what it should do. Say so in the move rather than assuming tests exist.

Where getting a unit into a test harness itself requires editing it, that editing happens first,
without tests, conservatively: preserve signatures exactly rather than improving them, change one
thing at a time, and let the compiler enumerate the call sites. This step can leave the design
locally worse. That is expected and worth saying out loud in the record.

## Sequencing

- **Smallest reversible move first.** Name the first step and make it one that can ship alone and
  be undone.
- **The system runs after every move.** Never a state where it does not.
- **Migrate incrementally.** Large restructurings fail far more often than they succeed, and they
  fail by trying to arrive in one move.
- **Prefer the simple adequate solution** over the general one. Build the flexibility a recorded
  weak point demands, and no more.

## Do not default to a rewrite

If a rewrite is genuinely the proposal, it needs the same five lines plus an explicit account of
**what the existing system knows that the specification does not** — the accumulated bug fixes,
edge cases, and undocumented behaviour that took years to find and are recorded nowhere else.

## The line that is never empty

`At the cost of:` — every move trades something. Three pairs conflict reliably:

- Reducing error-proneness raises viscosity — more ceremony on every future edit.
- Raising provisionality and progressive evaluation raises error-proneness — easier to leave
  something half-finished in place.
- Raising role expressiveness raises diffuseness — clearer labels, more code.

Also name which activity the codebase mostly sees — searching, comprehension, transcription,
incrementation, exploration — because a move that helps one harms another. A rarely-read library
that is often extended wants different things from a service people mostly read to understand.
