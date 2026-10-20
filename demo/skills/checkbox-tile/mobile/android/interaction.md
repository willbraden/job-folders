# Checkbox tile on Android

Only what Android changes. Everything shared lives in
[../overview.md](../overview.md).

## Build

In Jetpack Compose, put `Modifier.toggleable(value = checked, role =
Role.Checkbox, onValueChange = …)` on the tile's container. Read the
pressed state from its `MutableInteractionSource` for the `pressed` cells.

## Touch and feedback

- The minimum touch target is 48 dp. The tile's padding and type tokens
  already exceed it.
- Call `performHapticFeedback(HapticFeedbackType.SegmentTick)` on each
  toggle, or the closest equivalent on older API levels.

## TalkBack

- Use `Modifier.semantics(mergeDescendants = true)` so the tile is read as
  one node.
- The heading becomes the content description through the merge. Expose
  the description with `stateDescription` only if product research shows
  people need it read first; otherwise let the merge read it after the
  heading.
- `Role.Checkbox` makes TalkBack say "checked" or "not checked", and
  "double-tap to toggle".
- When disabled, set `enabled = false` on `toggleable`. TalkBack then reads
  the tile as disabled.
