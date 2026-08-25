# Keeping this skill in sync with mattpocock/skills

This folder is a `git subtree` pulled from
`skills/engineering/improve-codebase-architecture` in
https://github.com/mattpocock/skills (branch `main`).

To pull in upstream changes:

```bash
git fetch mattpocock-skills main
git subtree split -P skills/engineering/improve-codebase-architecture mattpocock-skills/main -b improve-arch-split
git subtree merge --prefix=skills/improve-codebase-architecture improve-arch-split --squash
git branch -D improve-arch-split
```

Resolve any conflicts as normal, then commit.

Note: the upstream path nests this skill under `skills/engineering/`,
but here it lives directly at `skills/improve-codebase-architecture`
(this repo's skills aren't categorized by discipline).
