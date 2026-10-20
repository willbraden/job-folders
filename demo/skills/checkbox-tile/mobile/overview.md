# Checkbox tile on mobile: overview

Behavior shared by iOS and Android. Each platform folder adds only what its
platform changes:

- [ios/interaction.md](ios/interaction.md)
- [android/interaction.md](android/interaction.md)

For anatomy and properties see [../SKILL.md](../SKILL.md); for content see
[../usage.md](../usage.md).

## Mobile-only states

In addition to the shared states, mobile defines:

- `pressed`: a finger is down on the tile. It applies whether or not the
  tile is selected, so there's no separate selected-pressed state.

Mobile has no hover state.

## Touch

- A tap anywhere on the tile toggles `checked`. The change happens on
  release, so dragging off the tile cancels it.
- The tile is always taller than the platform's minimum touch target, so it
  needs no extra hit-area padding.
- Each toggle plays the platform's light selection feedback. Disabled tiles
  play none.

## Assistive technology

The tile is announced as one element: the heading is the name, the
description is the hint, and the checked state is spoken. The icon and the
indicator are not announced. Each platform file says how to achieve this
with that platform's APIs.

## Tokens

Mobile uses [tokens.yaml](tokens.yaml). Token dimensions are unitless and
render in the platform's own unit.
