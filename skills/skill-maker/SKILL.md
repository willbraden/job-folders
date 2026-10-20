---
name: skill-maker
description: Creates new Claude skills and improves existing ones in Will's skills workspace. Use whenever Will asks to "make a skill", "turn this into a skill", "write a SKILL.md", "save this workflow so Claude can repeat it", or wants to edit, rename, split or tighten an existing skill under skills/. Also use when a conversation has just worked out a repeatable process and Will wants to keep it.
---

# Skill maker

A skill is a folder with a `SKILL.md`. Claude always sees the frontmatter
`description`. It reads the body only after deciding the skill applies, and
it opens other files in the folder only when the body tells it to. Everything
below follows from that.

## Workspace layout

```
skills/
  <skill-name>/
    SKILL.md          # required
    scripts/          # optional: code for deterministic or repeated steps
    references/       # optional: long docs, schemas, examples loaded on demand
    assets/           # optional: templates or files the skill copies or fills in
```

## Workflow

### 1. Pin down what the skill does

Get answers to these before writing anything. Pull them from the current
conversation first, and only ask Will about what is still missing:

- **Job:** what the skill produces or changes, in one sentence.
- **Triggers:** the phrases Will would actually type, plus any schedule
  ("every 6 hours", "each morning").
- **Inputs and outputs:** where data comes from (Gmail, a Google Sheet, a
  website, files) and where results go.
- **Tools:** which connectors, APIs, CLIs or browsers it needs.
- **Known failure modes:** what has broken before, and how it was fixed.

If the conversation just walked through the process, use the steps that
worked, the corrections Will made, and the IDs, URLs and column names that
came up. Those details are what make a skill reliable.

### 2. Name it

Use lowercase kebab-case that describes the job, such as `jobright-scrape` or
`followup-email`. The folder name and the frontmatter `name` must match.
Before creating the folder, check that `skills/<name>` doesn't already exist.

To scaffold the folder, run:

```
bash skills/skill-maker/scripts/new_skill.sh <skill-name>
```

### 3. Write the description

The description decides whether the skill fires, so spend the most care here.

- Say what it does, then when to use it.
- Include the literal trigger phrases from step 1, and name the services and
  file types involved.
- Cover the failure or follow-up cases too ("…or when Will reports the sheet
  hasn't updated").
- Write it in the third person and keep it under about 1,000 characters.
- Lean slightly pushy. A skill that never triggers is worth nothing.

### 4. Write the body

- Write imperative steps in the order Claude runs them.
- Explain the reason behind any rule that isn't obvious. Claude handles edge
  cases better when it knows why a rule exists than when it gets a bare
  MUST.
- Hard-code stable facts like sheet IDs, column names, label names and file
  paths. Never include secrets: point to an environment variable or a
  connector instead.
- Say what "done" looks like and what to report back.
- End with a **Troubleshooting** section that pairs each known failure mode
  with its fix.
- Keep `SKILL.md` under about 500 lines. Move long reference material into
  `references/` and link to it from the step that needs it, with a note on
  when to read it.
- If a step means running the same code every time (parsing, API calls,
  formatting), put the code in `scripts/` and tell Claude to run it rather
  than rewrite it.

### 5. Test it

Write two or three realistic prompts Will might send, including one
edge-case or failure prompt. For each, read the skill as if you were seeing
it for the first time and check two things:

1. Would the description trigger on this prompt?
2. Could someone follow the body to the right result without guessing?

Fix any gaps you find. Run every script in `scripts/` at least once.

### 6. Save it

Show Will the finished `SKILL.md` and get his go-ahead before committing,
then commit with a message like `Add <skill-name> skill`. To make the skill
usable:

- **Claude Code:** copy or symlink the folder into `~/.claude/skills/` for
  every project, or into `<project>/.claude/skills/` for one project.
- **claude.ai:** zip the skill folder and upload it under Settings →
  Capabilities → Skills.

## Improving an existing skill

Read the whole folder first. Then make the smallest change that fixes the
problem, which is usually one of these:

- **It didn't trigger:** add the missing phrases to the description.
- **It did the wrong thing:** fix or clarify the step and say why.
- **It hit a new failure:** add an entry to Troubleshooting.

Keep the name stable unless Will asks to rename it, because scheduled tasks
may refer to it.

## Troubleshooting

- **The skill never triggers:** the description is too vague or too short.
  Add concrete trigger phrases and the names of the services involved.
- **The skill triggers on unrelated requests:** the description is too broad.
  Add a "Do not use for…" line.
- **Claude ignores part of the body:** the step is buried or has no stated
  reason. Move it earlier and explain why it matters.
- **SKILL.md is huge:** split the reference material into `references/` and
  link to it from the relevant step.
