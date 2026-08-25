# Keeping this skill in sync with mattpocock/skills

This folder is a `git subtree` pulled from
`skills/engineering/codebase-design` in
https://github.com/mattpocock/skills (branch `main`).

To pull in upstream changes:

```bash
git fetch mattpocock-skills main
git subtree split -P skills/engineering/codebase-design mattpocock-skills/main -b codebase-design-split
git subtree merge --prefix=skills/codebase-design codebase-design-split --squash
git branch -D codebase-design-split
```

Resolve any conflicts as normal, then commit.

Note: the upstream path nests this skill under `skills/engineering/`,
but here it lives directly at `skills/codebase-design` (this repo's
skills aren't categorized by discipline).
