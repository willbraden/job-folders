# Checkbox tile on web: interaction

Covers only how the web platform changes the mechanism. For anatomy and
properties see [../SKILL.md](../SKILL.md); for content see
[../usage.md](../usage.md).

## Web-only states

In addition to the shared states, web defines:

- `hover`: the pointer is over an unselected tile.
- `selected-hover`: the pointer is over a selected tile.

Focus is an overlay rather than a state. The ring draws over whichever
state is current, using the `focus` cells in [tokens.yaml](tokens.yaml).

## Pointer and keyboard

- A click anywhere on the tile toggles `checked`.
- Tab moves focus to the tile. Space toggles it. Enter does nothing, which
  matches a native checkbox.
- The focus ring appears for keyboard focus only (`:focus-visible`), never
  on mouse click.
- A disabled tile can't take focus and ignores clicks.

## Implementation

Build the tile as a `<label>` wrapping a native checkbox input, so clicking,
keyboard toggling and form submission all work without script.

```html
<label class="checkbox-tile">
  <input type="checkbox" class="checkbox-tile__input" aria-describedby="tile-email-desc">
  <span class="checkbox-tile__icon" aria-hidden="true"><!-- icon --></span>
  <span class="checkbox-tile__heading">Email alerts</span>
  <span class="checkbox-tile__description" id="tile-email-desc">Get a summary every morning at 8 a.m.</span>
  <span class="checkbox-tile__indicator" aria-hidden="true"></span>
</label>
```

Reference token cells as CSS custom properties, for example
`border-color: var(--color-border-selected)` for
`states.selected.container-border`. Drive state styles from the input:
`.checkbox-tile:has(:checked)` for selected and `:hover` for hover.
