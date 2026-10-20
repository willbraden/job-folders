#!/usr/bin/env python3
"""Deterministic audit of a component spec folder.

Usage: python3 audit_spec.py <component-skill-name>
Exits non-zero if any check fails. Needs only the Python standard library.
"""
import re
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parents[2]
TOKENS_FILE = SKILLS_DIR / "design-tokens" / "tokens.yaml"

REQUIRED_FILES = [
    "SKILL.md",
    "usage.md",
    "web/tokens.yaml",
    "web/interaction.md",
    "web/accessibility.md",
    "mobile/overview.md",
    "mobile/tokens.yaml",
    "mobile/ios/interaction.md",
    "mobile/android/interaction.md",
]

# platform -> (token file, file that must declare platform-only states)
PLATFORMS = {
    "web": ("web/tokens.yaml", "web/interaction.md"),
    "mobile": ("mobile/tokens.yaml", "mobile/overview.md"),
}

WEB_TERMS = [r"\baria-", r"\bCSS\b", r":hover\b", r":focus-visible", r"\b\d+\s?px\b", r"<\w+[ >]"]
MOBILE_TERMS = [r"\bVoiceOver\b", r"\bTalkBack\b", r"\bhaptic", r"\bSwiftUI\b", r"\bCompose\b",
                r"\b\d+\s?(dp|pt)\b"]
IOS_TERMS = [r"\bVoiceOver\b", r"\bSwiftUI\b", r"\bUIKit\b", r"\b\d+\s?pt\b"]
ANDROID_TERMS = [r"\bTalkBack\b", r"\bCompose\b", r"\b\d+\s?dp\b"]

# file pattern -> terms that must not appear in it
BOUNDARIES = [
    (("SKILL.md", "usage.md"), WEB_TERMS + MOBILE_TERMS, "shared"),
    (("web/",), MOBILE_TERMS, "web"),
    (("mobile/overview.md", "mobile/tokens.yaml"), WEB_TERMS + IOS_TERMS + ANDROID_TERMS, "mobile shared"),
    (("mobile/ios/",), WEB_TERMS + ANDROID_TERMS, "iOS"),
    (("mobile/android/",), WEB_TERMS + IOS_TERMS, "Android"),
]

RAW_COLOR = re.compile(r"#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?\b")


def load_yaml(path):
    """Parse the nested key: value subset of YAML used by token files."""
    root = {}
    stack = [(-1, root)]
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        key, _, value = line.strip().partition(":")
        value = value.strip().strip('"')
        while stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1]
        if value:
            parent[key] = value
        else:
            parent[key] = {}
            stack.append((indent, parent[key]))
    return root


def flatten(tree, prefix=""):
    flat = {}
    for key, value in tree.items():
        path = f"{prefix}{key}"
        if isinstance(value, dict):
            flat.update(flatten(value, path + "."))
        else:
            flat[path] = value
    return flat


def bullet_names(markdown, heading):
    match = re.search(rf"^### {re.escape(heading)}\s*$(.*?)(?=^#|\Z)", markdown, re.M | re.S)
    if not match:
        return None
    return re.findall(r"^- `([^`]+)`", match.group(1), re.M)


def strip_code(text):
    return re.sub(r"^(`{3,}).*?^\1", "", text, flags=re.M | re.S)


def audit(component):
    comp = SKILLS_DIR / component
    failures = []

    def fail(check, message):
        failures.append(f"[{check}] {message}")

    # Spec quality
    for rel in REQUIRED_FILES:
        if not (comp / rel).is_file():
            fail("spec quality", f"missing {component}/{rel}")
    if not (comp / "SKILL.md").is_file():
        return failures

    skill_md = (comp / "SKILL.md").read_text(encoding="utf-8")
    shared_states = bullet_names(skill_md, "Shared states")
    properties = bullet_names(skill_md, "Token properties")
    if not shared_states:
        fail("spec quality", "SKILL.md has no '### Shared states' list")
    if not properties:
        fail("spec quality", "SKILL.md has no '### Token properties' list")
    if not shared_states or not properties:
        return failures

    tokens = flatten(load_yaml(TOKENS_FILE))

    # Token cells and platform states
    for platform, (token_rel, declaring_rel) in PLATFORMS.items():
        token_file = comp / token_rel
        if not token_file.is_file():
            continue
        spec = load_yaml(token_file)
        states = spec.get("states", {})
        for state in shared_states:
            if state not in states:
                fail("token cells", f"{platform}: shared state '{state}' is missing")
        declaring = comp / declaring_rel
        declared_text = declaring.read_text(encoding="utf-8") if declaring.is_file() else ""
        for state, cells in states.items():
            if state not in shared_states and f"`{state}`" not in declared_text:
                fail("platform states", f"{platform}: state '{state}' is not declared in {declaring_rel}")
            for prop in properties:
                if prop not in cells:
                    fail("token cells", f"{platform}.{state}.{prop}: missing cell")
            for prop in cells:
                if prop not in properties:
                    fail("token cells", f"{platform}.{state}.{prop}: not a contract property")
        for cell, ref in flatten(spec).items():
            if ref not in tokens:
                fail("token cells", f"{platform}.{cell}: '{ref}' is not a published token")

    # Platform boundary and single owner
    for path in sorted(comp.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(comp).as_posix()
        text = path.read_text(encoding="utf-8")
        for match in RAW_COLOR.findall(text):
            fail("single owner", f"{rel}: raw color {match}; reference a token path instead")
        prose = strip_code(text)
        for prefixes, terms, label in BOUNDARIES:
            if any(rel == p or (p.endswith("/") and rel.startswith(p)) for p in prefixes):
                for term in terms:
                    hit = re.search(term, prose)
                    if hit:
                        fail("platform boundary", f"{rel}: '{hit.group(0).strip()}' does not belong in a {label} file")

    return failures


def main():
    if len(sys.argv) != 2:
        print("usage: audit_spec.py <component-skill-name>", file=sys.stderr)
        sys.exit(2)
    component = sys.argv[1]
    if not (SKILLS_DIR / component).is_dir():
        print(f"error: no skill folder named '{component}'", file=sys.stderr)
        sys.exit(2)
    failures = audit(component)
    for failure in failures:
        print(f"FAIL {failure}")
    print(f"{component}: {'PASS' if not failures else f'{len(failures)} failures'}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
