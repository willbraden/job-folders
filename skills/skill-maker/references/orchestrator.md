# Writing an orchestrator

An orchestrator works like a kitchen order ticket. The order says which
burger to make. The ticket pulls only the ingredients that burger needs, the
cook assembles them in sequence, and the plate is checked against the order
before it goes out. Nobody empties the pantry for every burger.

| Kitchen | Skills |
|---|---|
| Kitchen | The workspace: shared standards, tools and connectors |
| Order ticket | The orchestrator: settles what was asked for and runs the assembly |
| Ingredients | Sub-skills: focused, reusable, each defined in one place |
| Quality check | Done-when checks and scripts |

## What an orchestrator owns, and what it doesn't

It owns:
- how to turn a request into an order (which outcome, which options)
- the routing table: which sub-skill loads under which condition
- the sequence, and what each step hands to the next
- the checks run at each handoff and at the end
- the final report

It never owns domain facts, such as a sheet ID, a filter rule, an email
template or a token value. Those live in sub-skills or owner skills. If you
find yourself writing one into the orchestrator, move it into the skill that
owns it.

## Required sections

1. **Order:** the inputs to settle before doing anything, and the default
   for each. If a required input can't be settled from the request, the
   conversation or an owner skill, stop and ask.
2. **Sub-skills:** a routing table with these columns: sub-skill, load when,
   provides, hands off. `check_skills.py` reads the first column. A name
   in backticks must be a folder in `skills/`. Mark skills installed
   elsewhere with their plugin prefix, such as `anthropic-skills:foo`, and
   the check skips them.
3. **Sequence:** numbered steps. Each step reads one sub-skill's `SKILL.md`
   and follows it. The step doesn't restate that skill's rules.
4. **Handoff checks:** what must be true before the next step starts. If a
   check fails, stop and report. Don't let later steps run on bad input.
5. **Done when:** checkable statements about the final result.
6. **Report:** what to tell Will, including which sub-skills ran, which were
   skipped and why, and what each produced.

## Worked example: job pipeline

This example orchestrates three skills Will already has.

````markdown
---
name: job-pipeline
description: Runs Will's job-search pipeline end to end or in part: finds new roles on Jobright, opens queued applications, and drafts recruiter follow-ups. Use when Will says "run my job pipeline", "do my job stuff", "catch me up on applications", or asks for more than one of: scraping new jobs, opening application tabs, drafting follow-ups. Do not use for a single stage on its own; let that stage's skill handle it.
---

# Job pipeline (orchestrator)

This skill holds routing and order only. The Pipeline sheet layout, Jobright
filters and email rules all live in the sub-skills.

## Order

Settle this before acting:
- **Stages:** any of scrape, open, follow-up. Default: all three, in
  that order.
- **Since:** how far back to look for confirmation emails. Default: since
  the last run.

If Will names a stage that isn't listed here, stop and ask.

## Sub-skills

| Sub-skill | Load when | Provides | Hands off |
|---|---|---|---|
| `anthropic-skills:jobright-scrape` | stage `scrape` | new rows in the Pipeline sheet | count of rows added |
| `anthropic-skills:morning-job-tabs` | stage `open` | opened tabs, rows marked applied | list of companies applied to |
| `anthropic-skills:followup-email` | stage `follow-up` | Gmail drafts | list of drafts created or skipped |

## Sequence

1. Settle the order.
2. For each selected stage, in table order, read that sub-skill's SKILL.md
   and follow it.
3. Run that stage's handoff check before moving on.

## Handoff checks

- After scrape: the sheet reports the same number of added rows the stage
  claimed. Zero is allowed; an error is not.
- After open: every row marked applied matches a tab that actually opened.

## Done when

- Every selected stage either ran or stopped with a stated reason.
- No stage ran after a failed handoff check.

## Report

One line per stage: ran or skipped, the reason, and its count. Then list
anything that needs Will.
````

## Common mistakes

- **A fat orchestrator:** the orchestrator copies its sub-skills' rules
  "for convenience". Delete the copies and leave only links.
- **No load conditions:** every sub-skill always loads. If that's really
  true, the sub-skills may belong together in one skill.
- **Silent skips:** a stage was skipped and the report doesn't say why.
- **Nested orchestrators:** an orchestrator may call another, but keep it to
  one level of nesting. Deeper trees are hard to debug.
