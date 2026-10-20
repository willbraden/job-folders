#!/usr/bin/env python3
"""Deterministic checks for every skill in the workspace.

Usage: python3 check_skills.py [skills_dir]
Exits non-zero if any check fails.
"""
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\]\(([^)#\s]+)\)")
SUBSKILL_ROW_RE = re.compile(r"^\|\s*`([^`]+)`", re.M)


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    fields = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields, text[end + 4:]


def section(body, title):
    match = re.search(rf"^## {re.escape(title)}\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
    return match.group(1) if match else None


def check_skill(skill_dir, all_names):
    errors = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_dir.name}: missing SKILL.md"]

    text = skill_md.read_text(encoding="utf-8")
    fields, body = parse_frontmatter(text)
    if fields is None:
        return [f"{skill_dir.name}: SKILL.md has no frontmatter"]

    name = fields.get("name", "")
    description = fields.get("description", "")
    if name != skill_dir.name:
        errors.append(f"{skill_dir.name}: frontmatter name '{name}' does not match folder")
    if not NAME_RE.match(skill_dir.name):
        errors.append(f"{skill_dir.name}: folder name is not lowercase kebab-case")
    if not description:
        errors.append(f"{skill_dir.name}: missing description")
    elif ": " in description and not description.startswith(("'", '"')):
        errors.append(f"{skill_dir.name}: description contains ': ' which breaks YAML; quote it or reword")
    elif len(description) > 1024:
        errors.append(f"{skill_dir.name}: description is {len(description)} chars (max 1024)")

    # TODOs inside fenced code blocks are examples, not unfinished work.
    prose = re.sub(r"^(`{3,}).*?^\1", "", text, flags=re.M | re.S)
    if re.search(r"\bTODO\b", prose):
        errors.append(f"{skill_dir.name}: unfinished TODOs in SKILL.md")

    for target in LINK_RE.findall(prose):
        if "://" in target:
            continue
        if not (skill_dir / target).exists():
            errors.append(f"{skill_dir.name}: broken link '{target}'")

    sub_skills = section(body, "Sub-skills")
    if sub_skills is not None:
        rows = SUBSKILL_ROW_RE.findall(sub_skills)
        if not rows:
            errors.append(f"{skill_dir.name}: Sub-skills section has no `skill` rows")
        for sub in rows:
            if ":" in sub:
                continue  # installed elsewhere, e.g. anthropic-skills:foo
            if sub not in all_names:
                errors.append(f"{skill_dir.name}: sub-skill '{sub}' not found in skills/")
            if sub == skill_dir.name:
                errors.append(f"{skill_dir.name}: lists itself as a sub-skill")

    return errors


def main():
    skills_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
    skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith("."))
    all_names = {p.name for p in skill_dirs}

    errors = []
    for skill_dir in skill_dirs:
        errors += check_skill(skill_dir, all_names)

    index = skills_dir / "README.md"
    if not index.is_file():
        errors.append("skills/README.md index is missing")
    else:
        index_text = index.read_text(encoding="utf-8")
        for name in sorted(all_names):
            if f"`{name}`" not in index_text:
                errors.append(f"{name}: not listed in skills/README.md")

    for error in errors:
        print(f"FAIL {error}")
    print(f"{len(skill_dirs)} skills checked, {len(errors)} problems")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
