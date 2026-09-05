# History analyses — Phase 1

Everything here is plain `git` plus standard shell. No JVM, no installed tool. Run from the
repository root. `$SCOPE` is the path filter from Phase 0 (`.` for the whole repo).

## 0. Check the history is trustworthy first

Before relying on any number below:

```sh
git rev-parse --is-shallow-repository          # true => counts are truncated
git log --oneline | wc -l                       # total commits
git log --format='%ad' --date=short | tail -1   # first commit date
git log --diff-filter=R --name-status | head    # renames
git log --format='%an' | sort | uniq -c | sort -rn | head   # one author for everything => imported
```

Four things invalidate the analyses, and each must be stated in the record if present:

- **Shallow clone** — counts are meaningless.
- **Squashed history** — co-change evidence is destroyed; change coupling is unavailable.
- **An import commit** crediting one author for the whole tree — ownership analyses are unusable.
- **A directory restructure inside the window** — file-level counts do not carry across it.
  Check with `git log --diff-filter=R --name-status`, and either pick a window after the move or
  say the counts are split.

**A repository younger than a few months has no trend.** Say so rather than reading one in.

## 1. Choose the window

Default to **one year**. Shrink it for very high commit volume. Or anchor it to a known event —
a rewrite, a team change, a release. State the window and one sentence of why.

```sh
WINDOW="--since=1.year"
```

Run the whole repository's window *and* a full-history pass when the repo is small enough; a
candidate that is hot in one and cold in the other is itself a finding.

## 2. Change frequency

```sh
git log $WINDOW --format='' --name-only --no-renames -- $SCOPE \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -40
```

## 3. Cross it with size

```sh
git log $WINDOW --format='' --name-only --no-renames -- $SCOPE \
  | grep -v '^$' | sort | uniq -c | sort -rn \
  | while read -r n f; do [ -f "$f" ] && echo "$n $(wc -l < "$f") $f"; done | head -40
```

Columns: revisions, lines, path. A file high on both axes is a candidate. **Sort and read the
top; do not set a cut-off.** High-revision/low-size is usually config or a route table. Low
revision, however large and ugly, is not costing anyone anything.

## 4. Change coupling

Files that change in the same commits. This is the signal no static tool gives you.

```sh
git log $WINDOW --format='__C__%H' --name-only --no-renames -- $SCOPE \
  | awk '/^__C__/{if(n>1&&n<50)for(i=1;i<=n;i++)for(j=i+1;j<=n;j++)print (f[i]<f[j]?f[i]" "f[j]:f[j]" "f[i]); n=0; next} NF{f[++n]=$0}' \
  | sort | uniq -c | sort -rn | head -30
```

The `n<50` guard drops bulk commits (reformats, imports) that couple everything to everything.

**Coupling is only a fault when it crosses a boundary the design says should hold.** A file and
its own test changing together is expected. Two modules that are supposed to be independent
changing together in 40% of commits is architectural decay. **State which boundary you are
testing against before you judge** — and if none is documented, derive one from the directory
structure and say that you did.

Three causes, and they are not equally bad: copy-paste; a module boundary that does not support
the change; and a producer/consumer pair, which may be entirely correct.

## 5. Ownership

```sh
git log $WINDOW --format='' --numstat --no-renames -- $SCOPE \
  | awk 'NF==3{a[$3]+=$1} END{for(f in a)print a[f], f}' | sort -rn | head -20

git log $WINDOW --format='%an' --name-only --no-renames -- $SCOPE   # authors per file
```

Many minor contributors and no clear owner predicts defects more strongly than ownership share
does. This is a finding to **report to a human**, not an input to your own decisions — and it
must never be presented as individual performance data.

## 6. What was already fixed

For each candidate, read the commits that touched it.

```sh
git log $WINDOW --oneline -- <candidate>       # one line per commit
git show -s --format='%B' <sha>                 # the message - it usually names the fix
git show --stat <sha>                           # which files moved together
```

**Read the message and the stat first. They answer the question most of the time.** A commit
message saying what was fixed, plus the list of files it touched, is usually the whole finding.

Open a diff only when message and stat leave the mechanism unclear, and scope it to one path:

```sh
git show <sha> -- <the one path you care about>
```

**Never run a bare `git show` across a list of candidates.** Measured on a small repository, one
full commit diff was **34 KB (~8,500 tokens)**; its message and stat together were **2.5 KB**.
The whole of steps 2-5 above costs about 1,700 tokens, because every one of them returns a
bounded aggregate rather than raw log output. Keep it that way: the ranking exists to *aim* your
reading, and it is only worth running because it costs less than the files it saves you opening.

**Do this before writing any finding about the candidate.** A problem the team already
diagnosed and repaired is a different finding from a fresh one, and the repair usually names the
mechanism better than you would have. An unaided agent that read these commits found the real
defect in this codebase; two that skipped them missed it while reading more files.

## 7. Trend — only where the history is long enough

Whether a candidate is getting worse. Needs many months of history to mean anything.

```sh
for sha in $(git log $WINDOW --format='%H' --reverse -- <file> | awk 'NR%5==1'); do
  printf '%s %s\n' "$(git show --format='%ad' --date=short -s "$sha")" \
                   "$(git show "$sha:<file>" 2>/dev/null | wc -l)"
done
```

For a complexity proxy that is language-neutral, count leading indentation instead of lines
(4 spaces or 1 tab = 1 unit); track the total and the maximum.

Three shapes:

- **Deteriorating** — climbing with no plateau. A refactoring candidate.
- **Refactored** — a visible dip. A good sign; keep watching.
- **Stable** — flat. Small tweaks only; often needs nothing.

**Total complexity rising while line count stays flat is the bad case** — existing lines are
getting worse. Rising together is growth by addition. Shrinkage is real consolidation.

## 8. Tests are architecture too

```sh
git log $WINDOW --format='' --name-only --no-renames \
  | grep -Ec '(test|spec)' ; git log $WINDOW --format='' --name-only --no-renames | grep -vEc '(test|spec)'
```

Watch the ratio over time. Test churn suddenly outpacing application churn is a warning; test
maintenance dominating is a structural problem in the tests themselves.
