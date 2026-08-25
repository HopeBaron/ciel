#!/usr/bin/env bash
# Manage symlinks from ~/.claude/skills/ into this repo's skills/ directory.
# Claude Code only discovers a skill when the symlink target itself contains
# SKILL.md, so each skill gets its own "ciel-<name>" symlink (never one
# symlink pointing at the whole skills/ directory).
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_DIR/skills"
TARGET_DIR="$HOME/.claude/skills"
PREFIX="ciel-"

list_skills() {
    local d
    for d in "$SKILLS_DIR"/*/; do
        [ -f "${d}SKILL.md" ] || continue
        basename "$d"
    done
}

link_skill() {
    local name="$1"
    local src="$SKILLS_DIR/$name"
    if [ ! -f "$src/SKILL.md" ]; then
        echo "No such skill (missing SKILL.md): $name" >&2
        return 1
    fi
    mkdir -p "$TARGET_DIR"
    ln -sfn "$src" "$TARGET_DIR/${PREFIX}${name}"
    echo "linked: ${PREFIX}${name} -> $src"
}

unlink_skill() {
    local name="$1"
    local dest="$TARGET_DIR/${PREFIX}${name}"
    if [ -L "$dest" ]; then
        rm "$dest"
        echo "unlinked: $dest"
    else
        echo "no symlink for '$name' at $dest" >&2
        return 1
    fi
}

cleanup() {
    local removed=0
    local entry name
    if [ -d "$TARGET_DIR" ]; then
        for entry in "$TARGET_DIR"/${PREFIX}*; do
            [ -e "$entry" ] || [ -L "$entry" ] || continue
            [ -L "$entry" ] || continue
            name="$(basename "$entry")"
            name="${name#$PREFIX}"
            if [ ! -e "$entry" ] || [ ! -f "$SKILLS_DIR/$name/SKILL.md" ]; then
                rm "$entry"
                echo "removed dead/orphaned: $entry"
                removed=1
            fi
        done
    fi
    # legacy leftover from before per-skill symlinks (a single "ciel" symlink
    # pointing at the whole skills/ directory, which Claude Code never loads)
    if [ -L "$TARGET_DIR/ciel" ]; then
        rm "$TARGET_DIR/ciel"
        echo "removed legacy leftover: $TARGET_DIR/ciel"
        removed=1
    fi
    [ "$removed" -eq 1 ] || echo "nothing to clean up"
}

link_all() {
    local name
    while IFS= read -r name; do
        link_skill "$name"
    done < <(list_skills)
}

select_skill() {
    local prompt="$1"
    local names=()
    while IFS= read -r n; do names+=("$n"); done < <(list_skills)
    if [ "${#names[@]}" -eq 0 ]; then
        echo "No skills found under $SKILLS_DIR" >&2
        exit 1
    fi
    echo "$prompt" >&2
    select name in "${names[@]}"; do
        [ -n "${name:-}" ] && { echo "$name"; return; }
        echo "Invalid choice." >&2
    done
}

usage() {
    cat <<EOF
Usage: $(basename "$0") <command> [skill-name]

Commands:
  link [name]     Symlink (or re-symlink) one skill. Prompts if name omitted.
  unlink [name]   Remove the symlink for one skill. Prompts if name omitted.
  cleanup         Remove dead/orphaned symlinks and legacy leftovers.
  all             Symlink every skill in this repo.

With no arguments, opens an interactive menu.
EOF
}

interactive_menu() {
    PS3="Choose an action: "
    select action in "link a skill" "unlink a skill" "cleanup dead/leftover symlinks" "link all skills" "quit"; do
        case "$action" in
            "link a skill") link_skill "$(select_skill "Pick a skill to (re)link:")"; break ;;
            "unlink a skill") unlink_skill "$(select_skill "Pick a skill to unlink:")"; break ;;
            "cleanup dead/leftover symlinks") cleanup; break ;;
            "link all skills") link_all; break ;;
            "quit") exit 0 ;;
            *) echo "Invalid choice." ;;
        esac
    done
}

main() {
    local cmd="${1:-}"
    case "$cmd" in
        link)
            local name="${2:-$(select_skill "Pick a skill to (re)link:")}"
            link_skill "$name"
            ;;
        unlink)
            local name="${2:-$(select_skill "Pick a skill to unlink:")}"
            unlink_skill "$name"
            ;;
        cleanup)
            cleanup
            ;;
        all)
            link_all
            ;;
        -h|--help)
            usage
            ;;
        "")
            interactive_menu
            ;;
        *)
            echo "Unknown command: $cmd" >&2
            usage
            exit 1
            ;;
    esac
}

main "$@"
