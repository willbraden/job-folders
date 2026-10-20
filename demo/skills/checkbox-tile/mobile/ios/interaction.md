# Checkbox tile on iOS

Only what iOS changes. Everything shared lives in
[../overview.md](../overview.md).

## Build

In SwiftUI, build the tile as a `Button` that toggles a `Bool` binding, with
a custom `ButtonStyle` that reads `configuration.isPressed` for the
`pressed` cells.

## Touch and feedback

- The minimum touch target is 44 pt. The tile's padding and type tokens
  already exceed it.
- Play `UISelectionFeedbackGenerator().selectionChanged()` on each toggle.

## VoiceOver

- Combine the tile into one element with
  `.accessibilityElement(children: .ignore)`.
- Set `.accessibilityLabel` to the heading and `.accessibilityHint` to the
  description.
- Add `.accessibilityAddTraits(.isSelected)` when checked, and
  `.isButton` always.
- When disabled, apply `.disabled(true)`. VoiceOver then reads the tile as
  dimmed.

VoiceOver reads it roughly as: "Selected, Email alerts, button. Get a
summary every morning at 8 a.m."
