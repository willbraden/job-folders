#!/usr/bin/env bash
# Scaffold a new skill folder: bash new_skill.sh <skill-name>
set -euo pipefail

name="${1:-}"
if [[ ! "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "usage: $0 <skill-name>  (lowercase kebab-case)" >&2
  exit 1
fi

skills_dir="$(cd "$(dirname "$0")/../.." && pwd)"
dir="$skills_dir/$name"
if [[ -e "$dir" ]]; then
  echo "error: $dir already exists" >&2
  exit 1
fi

mkdir -p "$dir"
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

TODO what finished looks like and what to report back.

## Troubleshooting

- **TODO symptom:** TODO fix.
EOF

echo "created $dir/SKILL.md"
