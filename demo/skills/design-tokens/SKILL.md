---
name: design-tokens
description: Owns the design system's published tokens (color, space, radius, border width, size and type) and is the single source of their values. Use whenever a component spec, build or audit needs a token value or a token path, or when the user asks to add, rename or look up a token. Do not use for component-specific decisions; those belong to the component's own skill.
---

# Design tokens (owner)

This skill owns token data and nothing else. Components reference tokens by
path, such as `color.border.selected`, and never copy their values.

## Source

All tokens live in [tokens.yaml](tokens.yaml). A token path is the dotted
key path to a leaf value, for example `space.400`.

## Rules

- **Exact match only.** A component either references a published path or
  it fails the audit. There is no "nearest" token. If no token fits, stop
  and propose a new one to the user instead of reusing a close one.
- **Platform-neutral dimensions.** Numbers are unitless. Web renders them
  as px, iOS as pt and Android as dp, so the same token serves every
  platform.
- **Composite type tokens.** Type tokens are `weight size/line-height`,
  such as `600 16/24`.

## Adding a token

1. Check that no existing token already expresses the same intent.
2. Add it under the right group in `tokens.yaml`, keeping its siblings in
   scale order.
3. Run the audit for any component that will use it (see the
   [spec-audit](../spec-audit/SKILL.md) skill).

## Done when

- Every new path resolves to a leaf value in `tokens.yaml`.
- No existing path was renamed without updating every component that uses it.
