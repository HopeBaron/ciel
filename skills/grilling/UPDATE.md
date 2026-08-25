# Keeping this skill in sync with mattpocock/skills

This folder is a `git subtree` pulled from
`skills/productivity/grilling` in
https://github.com/mattpocock/skills (branch `main`).

To pull in upstream changes:

```bash
git fetch mattpocock-skills main
git subtree split -P skills/productivity/grilling mattpocock-skills/main -b grilling-split
git subtree merge --prefix=skills/grilling grilling-split --squash
git branch -D grilling-split
```

Resolve any conflicts as normal, then commit.

Note: the upstream path nests this skill under `skills/productivity/`,
but here it lives directly at `skills/grilling` (this repo's skills
aren't categorized by discipline).
