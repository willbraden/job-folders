---
name: skill-maker
description: Creates new Claude skills and improves existing ones in Will's skills workspace, including orchestrator skills that coordinate other skills. Use whenever Will asks to "make a skill", "turn this into a skill", "write a SKILL.md", "make an orchestrator", "chain these skills", "save this workflow so Claude can repeat it", or wants to edit, rename, split, merge or audit a skill under skills/. Also use when a conversation has just worked out a repeatable process and Will wants to keep it.
---

# Skill maker

A skill is a folder with a `SKILL.md`. Claude always sees the frontmatter
`description`. It reads the body only after deciding the skill applies, and
it opens other files in the folder only when the body tells it to.

The goal is predictable behavior: the same request produces the same kind of
result, and anything that must be true gets checked by code rather than by
judgment. Judgment still belongs inside a step. Requirements belong in a
check.

## Principles

1. **Frontmatter is a selection contract.** The description is the only
   thing that decides whether a skill loads, so it must say exactly what the
   skill covers and when to use it.
2. **One fact, one owner.** Each piece of information is written in exactly
   one skill, such as a sheet ID, a column layout, a tone rule or a token
   value. Other skills point to that owner and never restate the fact.
   Duplicated facts drift apart.
3. **Cross-references are explicit dependencies.** When a skill relies on
   another, it names that skill and says what it gets from it.
4. **Load only what applies.** Orchestrators pick sub-skills based on the
   request. They never load everything "just in case".
5. **Resolve before asking.** Read the owning skill or source file before
   asking Will something it already answers.
6. **Stop on ambiguity.** If the request or the inputs don't settle a
   decision, stop and ask. Don't make up a confident answer.
7. **Generative inside, deterministic outside.** Claude can take any
   reasonable route through a step. The result still has to pass named
   checks, ideally a script.
8. **Shared intent stays shared.** When a skill has variants (web vs.
   mobile, Gmail vs. Outlook), keep what's common in the root `SKILL.md`.
   Put only the differences in a subfolder, and let each subfolder use its
   own vocabulary.
9. **Collapse when it stops paying.** If two skills always load together,
   or a model no longer needs the help, merge or delete them.

## Kinds of skill

Choose a kind before writing. It decides the shape of the skill.

- **Leaf skill:** does one job end to end and owns the facts for that job.
  Most skills are this kind.
- **Orchestrator:** turns a request (the "order") into a sequence of
  sub-skills, loads only the ones that order needs, passes results from one
  to the next, and checks each handoff. It owns the routing and the order
  of steps, and no domain facts. Read
  [references/orchestrator.md](references/orchestrator.md) before writing
  one.
- **Owner skill:** holds shared facts that several skills need, such as Will's
  Pipeline sheet layout or a set of design tokens. Other skills point to it.
  It usually has no workflow of its own.

If a request covers several separable jobs, build leaf skills plus an
orchestrator instead of one big skill.

## Workspace layout

```
skills/
  README.md           # index: one line per skill (the router)
  <skill-name>/
    SKILL.md          # required
    scripts/          # code for deterministic steps and checks
    references/       # long docs loaded on demand
    assets/           # templates the skill copies or fills in
    <variant>/        # optional: differences only, e.g. web/, mobile/
```

## Workflow

### 1. Pin down the intent

Get answers to these before writing anything. Pull them from the current
conversation first, and only ask Will about what is still missing:

- **Job:** what the skill produces or changes, in one sentence.
- **Triggers:** the phrases Will would actually type, plus any schedule.
- **Inputs and outputs:** where data comes from and where results go.
- **Tools:** the connectors, APIs, CLIs or browsers it needs.
- **Requirements:** what must be true of the result. These become the checks
  in step 5.
- **Known failure modes:** what has broken before, and the fix.

If the conversation just walked through the process, use the steps that
worked, Will's corrections, and the IDs, URLs and column names that came up.

### 2. Decide its shape and owners

- Choose the kind: leaf, orchestrator or owner.
- List every fact the skill needs. For each one, check whether some skill in
  `skills/` already owns it (search with `grep -r`). If one does, link to
  that skill. If none does, this skill owns the fact, or it's shared enough
  to need its own owner skill.
- If an existing skill already covers most of the job, extend it instead of
  creating a new one.

### 3. Name and scaffold it

Use lowercase kebab-case that describes the job. The folder name and the
frontmatter `name` must match.

```
bash skills/skill-maker/scripts/new_skill.sh <skill-name>                 # leaf or owner
bash skills/skill-maker/scripts/new_skill.sh --orchestrator <skill-name>  # orchestrator
```

The script refuses to overwrite an existing folder.

### 4. Write it

**Description:** say what the skill does, then when to use it. Include the
literal trigger phrases, the services involved, and the failure or
follow-up cases. Write it in the third person and keep it under about 1,000
characters. Lean slightly pushy. If neighboring skills overlap, add a
"Do not use for…" line naming the skill that should handle those requests
instead.

**Body:**
- Write imperative steps in the order Claude runs them, and give the reason
  for any rule that isn't obvious.
- Include the facts this skill owns, such as IDs, column names and paths.
  For facts another skill owns, link to that skill instead. Never include
  secrets.
- Write a **Done when** section of checkable statements. "Every new row has
  a non-empty URL" can be checked. "Results look good" cannot.
- When a step runs the same code every time, or a requirement can be
  checked mechanically, put that code in `scripts/`.
- End with a **Troubleshooting** section pairing each symptom with its fix.
- Keep `SKILL.md` under about 500 lines. Move long material into
  `references/` and link to it from the step that needs it.

### 5. Verify it

Run the deterministic checks:

```
python3 skills/skill-maker/scripts/check_skills.py
```

They confirm that frontmatter is valid, the name matches the folder, no
TODOs are left, linked files exist, an orchestrator's sub-skills exist, and
`skills/README.md` lists every skill. Fix every error.

Then test the skill's judgment. Write two or three realistic prompts,
including one edge case or failure. For each one, read the skill as if
seeing it for the first time and confirm three things:

1. The description would trigger on the prompt.
2. Every requirement in **Done when** could actually be checked.
3. Nothing in the body restates a fact that another skill owns.

Run each script in `scripts/` at least once.

### 6. Index and save

Add a line for the skill to `skills/README.md`: its name, its kind, and
what it's for. Show Will the finished skill and get his go-ahead, then
commit with a message like `Add <skill-name> skill`. To make the skill
usable:

- **Claude Code:** copy or symlink the folder into `~/.claude/skills/` or
  `<project>/.claude/skills/`.
- **claude.ai:** zip the folder and upload it under Settings → Capabilities
  → Skills. Upload sub-skills along with their orchestrator.

## Improving an existing skill

Read the whole folder first, and run `check_skills.py`. Then make the
smallest change that fixes the problem:

- **It didn't trigger:** add the missing phrases to the description.
- **It triggered wrongly:** narrow the description or add "Do not use for…".
- **It did the wrong thing:** fix the step and say why, or add a check that
  would have caught it.
- **It hit a new failure:** add an entry to Troubleshooting.
- **The same fact appears in two places:** keep it in its owner and replace
  the copy with a link.

Keep names stable unless Will asks to rename one, because scheduled tasks
and orchestrators refer to skills by name. When you do rename, run
`check_skills.py` to find any references that broke.

## Troubleshooting

- **The skill never triggers:** the description is vague. Add concrete
  trigger phrases and service names.
- **Two skills both trigger:** their descriptions overlap. Give each one a
  "Do not use for…" line naming the other skill.
- **Results vary from run to run:** a requirement exists only as prose. Turn
  it into a **Done when** check or a script.
- **A fact is wrong in one skill and right in another:** it was duplicated.
  Keep it in one owner and link to it from everywhere else.
- **The orchestrator loads everything:** its routing table has no "load
  when" conditions. See [references/orchestrator.md](references/orchestrator.md).
- **SKILL.md is huge:** split reference material into `references/`, or
  split the job into leaf skills plus an orchestrator.
