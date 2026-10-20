---
name: component-build
description: Orchestrates building a design-system component end to end, from spec to platform implementation, an optional Figma component, and an audit. Use when the user asks to "build", "spec out", "implement" or "ship" a component for web, iOS or Android, or asks for more than one of spec, code, Figma and audit for the same component. Do not use for a single content or usage question; let the component's own skill answer it.
---

# Component build (orchestrator)

This skill holds routing and order only. Anatomy, tokens, platform behavior
and checks all live in the sub-skills below.

## Order

Settle this before acting:

- **Component:** which component. It must have its own skill. If it
  doesn't, stop and offer to create one with skill-maker.
- **Platforms:** any of web, iOS and Android. Default: all three.
- **Outputs:** any of spec, code and Figma. Default: spec and code.

If the request names a component or platform not listed here, stop and ask.

## Sub-skills

| Sub-skill | Load when | Provides | Hands off |
|---|---|---|---|
| `checkbox-tile` | component is checkbox tile | anatomy, properties, contract; the platform files for the selected platforms only | the files to build from |
| `design-tokens` | always | token values for the cells the component references | resolved values |
| `figma:figma-use` | outputs include Figma | Figma component set built from the spec | Figma node link |
| `spec-audit` | always, last | deterministic checks | pass, or a list of failures |

Each new component adds one row like `checkbox-tile`.

## Sequence

1. Settle the order.
2. Read the component's `SKILL.md`. Then read only the files its routing
   table names for the selected platforms and outputs. For a web-only build
   of the checkbox tile, that's `usage.md` and the files in `web/`, and
   nothing in `mobile/`.
3. Resolve every token path the selected platform files reference, using
   `design-tokens`.
4. Produce each requested output, following the component's files.
5. If Figma was requested, build it from the spec's anatomy, properties and
   token cells, following `figma:figma-use`. Bind every fill, stroke and
   text style to a published token or style; never approximate.
6. Run `spec-audit` for the component.

## Handoff checks

- **After step 2:** every selected platform has a token file and an
  interaction file. If one is missing, stop: the spec isn't ready.
- **After step 3:** every referenced token path resolved exactly. If any
  didn't, stop and report it; don't substitute a similar token.
- **After step 5:** the Figma component set has one variant for each layout
  and state combination in the selected platform's token file.

## Done when

- Every requested output exists for every selected platform.
- `spec-audit` exits with status 0.
- Nothing was built for a platform or output that wasn't requested.

## Report

One line per step: ran or skipped, the reason, and what it produced. Then
the audit result, and anything that needs the user's decision.
