#!/usr/bin/env python3
"""Validate a skill directory. Exit 0 if valid, 1 if any FAIL.

Enforces Anthropic's frontmatter contract plus the size and pointer checks their
validator omits -- the omissions that let published skills blow their own budgets
undetected.
"""
import re, sys, os

ANTHROPIC_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
CLAUDE_CODE_KEYS = {"disable-model-invocation", "argument-hint"}
ALLOWED = ANTHROPIC_KEYS | CLAUDE_CODE_KEYS

WARN_LINES, FAIL_LINES, TOC_LINES = 150, 500, 300

fails, warns = [], []
def fail(m): fails.append(m)
def warn(m): warns.append(m)

def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, "SKILL.md must begin with '---'"
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None, "frontmatter block is not closed with '---'"
    fm, key = {}, None
    for line in m.group(1).split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if re.match(r"^\S.*?:", line):
            key, _, val = line.partition(":")
            key = key.strip()
            fm[key] = val.strip().strip('"').strip("'")
        elif key:
            fm[key] += " " + line.strip()
    return fm, None

def main(path):
    skill = os.path.join(path, "SKILL.md")
    if not os.path.isfile(skill):
        print(f"FAIL: no SKILL.md in {path}"); return 1
    text = open(skill, encoding="utf-8").read()
    lines = text.count("\n") + 1

    fm, err = parse_frontmatter(text)
    if err:
        fail(err); fm = {}

    for k in set(fm) - ALLOWED:
        fail(f"unexpected frontmatter key '{k}' (allowed: {', '.join(sorted(ALLOWED))})")

    name = fm.get("name")
    if not name:
        fail("missing 'name' in frontmatter")
    else:
        if not re.match(r"^[a-z0-9-]+$", name):
            fail(f"name '{name}' must be kebab-case: lowercase letters, digits, hyphens only")
        if name.startswith("-") or name.endswith("-") or "--" in name:
            fail(f"name '{name}' cannot start/end with a hyphen or contain '--'")
        if len(name) > 64:
            fail(f"name is {len(name)} chars; maximum is 64")

    desc = fm.get("description")
    if not desc:
        fail("missing 'description' in frontmatter")
    else:
        if "<" in desc or ">" in desc:
            fail("description cannot contain angle brackets (< or >)")
        if len(desc) > 1024:
            fail(f"description is {len(desc)} chars; maximum is 1024")
        if len(desc.split()) > 220:
            warn(f"description is {len(desc.split())} words; target is 100-200")

    compat = fm.get("compatibility")
    if compat and len(compat) > 500:
        fail(f"compatibility is {len(compat)} chars; maximum is 500")

    if lines > FAIL_LINES:
        fail(f"SKILL.md is {lines} lines; hard limit is {FAIL_LINES}. Add hierarchy, don't delete meaning")
    elif lines > WARN_LINES:
        warn(f"SKILL.md is {lines} lines; house median is ~40. Justify it or disclose more")

    # pointers and depth
    for root, _, files in os.walk(path):
        for f in files:
            if not f.endswith(".md"):
                continue
            fp = os.path.join(root, f)
            body = open(fp, encoding="utf-8").read()
            rel = os.path.relpath(fp, path)
            if re.search(r"(^|\s)@[\w./-]+\.md", body):
                fail(f"{rel}: '@'-link force-loads the file immediately; name it instead")
            if rel.count(os.sep) > 1:
                fail(f"{rel}: reference is more than one level deep from SKILL.md")
            n = body.count("\n") + 1
            if n > TOC_LINES and not re.search(r"(?i)^#+\s*(contents|table of contents)", body, re.M):
                warn(f"{rel} is {n} lines and has no table of contents")

    for target in re.findall(r"\]\(([^)#:]+\.md)\)", text) + re.findall(r"`(references/[\w./-]+)`", text):
        if not os.path.isfile(os.path.join(path, target)):
            fail(f"SKILL.md points at '{target}', which does not exist")

    for m in fails: print(f"FAIL: {m}")
    for m in warns: print(f"warn: {m}")
    if not fails:
        print(f"Skill is valid ({lines} lines, description {len(desc or '')} chars)"
              + (f", {len(warns)} warning(s)" if warns else ""))
    return 1 if fails else 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate.py <skill-dir>"); sys.exit(2)
    sys.exit(main(sys.argv[1]))
