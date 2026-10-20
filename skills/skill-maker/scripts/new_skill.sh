#!/usr/bin/env bash
# Scaffold a new skill folder:
#   bash new_skill.sh [--orchestrator] [--into <skills-dir>] <skill-name>
# Without --into, the skill is created next to skill-maker.
set -euo pipefail

kind=leaf
skills_dir="$(cd "$(dirname "$0")/../.." && pwd)"
while [[ "${1:-}" == --* ]]; do
  case "$1" in
    --orchestrator) kind=orchestrator; shift ;;
    --into) skills_dir="$(cd "${2:?--into needs a directory}" && pwd)"; shift 2 ;;
    *) echo "unknown option: $1" >&2; exit 1 ;;
  esac
done

name="${1:-}"
if [[ ! "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "usage: $0 [--orchestrator] [--into <skills-dir>] <skill-name>  (lowercase kebab-case)" >&2
  exit 1
fi

dir="$skills_dir/$name"
if [[ -e "$dir" ]]; then
  echo "error: $dir already exists" >&2
  exit 1
fi

mkdir -p "$dir"

if [[ "$kind" == "orchestrator" ]]; then
  cat > "$dir/SKILL.md" <<EOF
---
name: $name
description: TODO what the end-to-end outcome is. Use when Will says "TODO trigger phrase" or asks for more than one of TODO stages. Do not use for a single stage on its own; let that stage's skill handle it.
---

# ${name//-/ } (orchestrator)

This skill holds routing and order only. Domain facts live in the sub-skills
below. See skills/skill-maker/references/orchestrator.md.

## Order

Settle this before acting:
- **TODO input:** TODO options. Default: TODO.

If a required input can't be settled, stop and ask.

## Sub-skills

| Sub-skill | Load when | Provides | Hands off |
|---|---|---|---|
| \`TODO-sub-skill\` | TODO condition | TODO | TODO |

## Sequence

1. Settle the order.
2. For each selected sub-skill, in table order, read its SKILL.md and follow it.
3. Run that step's handoff check before moving on.

## Handoff checks

- After TODO: TODO checkable condition.

## Done when

- Every selected sub-skill either ran or stopped with a stated reason.
- No step ran after a failed handoff check.

## Report

One line per sub-skill: ran or skipped, the reason, and its output.
EOF
else
  cat > "$dir/SKILL.md" <<EOF
---
name: $name
description: TODO what it does. Use whenever Will asks to "TODO trigger phrase", "TODO trigger phrase", or TODO follow-up/failure case.
---

# ${name//-/ }

TODO one-paragraph summary of the job and its output.

## Steps

1. TODO

## Done when

- TODO checkable statement about the result.

## Troubleshooting

- **TODO symptom:** TODO fix.
EOF
fi

echo "created $dir/SKILL.md ($kind)"
echo "next: fill in the TODOs, add it to skills/README.md, then run scripts/check_skills.py"
