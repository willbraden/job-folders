---
name: spec-audit
description: Runs deterministic checks on a component spec folder and reports exactly which file, state or token cell fails. Use when the user asks to "audit", "check", "validate" or "lint" a component spec, after any change to a component's spec files or tokens, and as the final step of a component build. Do not use to judge visual design quality; it checks the contract, not taste.
---

# Spec audit

Checks a component spec against stable requirements using code, so the
result is the same every time it runs.

## Run

From the `skills/` folder:

```
python3 spec-audit/scripts/audit_spec.py <component-skill-name>
```

For example: `python3 spec-audit/scripts/audit_spec.py checkbox-tile`.

## What it checks

| Check | What it rules out | A failure points to |
|---|---|---|
| Spec quality | Missing required files or contract lists | The missing file or section |
| Token cells | Missing, extra or unpublished state × property cells | The exact platform, state and property |
| Platform states | Platform-only states that no interaction file declares | The undeclared state |
| Platform boundary | Web words in mobile files, mobile words in web files, platform words in shared files | The file and the term |
| Single owner | Raw color values copied into component files | The file and the value |

## Steps

1. Run the script for the component.
2. If it fails, fix each failure in the file it names. Fix the spec, not
   the check. If a check itself is wrong, tell the user and don't change it
   without their agreement.
3. Run it again until it passes.

## Done when

- The script exits with status 0.
- The report you give the user lists any failures you fixed, and in which
  file.
