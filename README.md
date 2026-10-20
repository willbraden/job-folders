# skills

Workspace for my Claude skills. See [skills/README.md](skills/README.md) for the
index, and `skills/skill-maker` for how skills are built and checked.

Each skill lives in its own folder under `skills/`:

```
skills/
  <skill-name>/
    SKILL.md        # frontmatter (name, description) + instructions
    scripts/        # optional helper scripts
    references/     # optional docs the skill loads on demand
```

For a worked example of the structure (an orchestrator, an owner skill, a
component with web and mobile files, and an audit script), see
[demo/](demo/README.md).
