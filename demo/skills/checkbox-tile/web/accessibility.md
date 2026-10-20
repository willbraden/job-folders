# Checkbox tile on web: accessibility

## Semantics

- **Native input.** The tile's control is a native `<input type="checkbox">`.
  Hide it visually but keep it in the accessibility tree; don't use
  `display: none`. The browser then announces the role and state.
- **Name and description.** The heading is the accessible name, because the
  label wraps it. Connect the description with `aria-describedby` so it's
  read after the name instead of as part of it.
- **Icon and indicator.** Both are decorative: give them
  `aria-hidden="true"`.
- **Groups.** Wrap a group of tiles in a `<fieldset>` and use its
  `<legend>` as the group label from [../usage.md](../usage.md).
- **Disabled tiles.** Use the native `disabled` attribute rather than
  `aria-disabled`, so the input leaves the tab order.

## WCAG checks

| Criterion | Requirement for this component |
|---|---|
| 1.4.3 Contrast (minimum) | Heading and description text meet 4.5:1 against the container in every state except `disabled` |
| 1.4.11 Non-text contrast | The unselected indicator border and the focus ring meet 3:1 against the container |
| 2.4.7 Focus visible | The focus ring shows on keyboard focus in every state |
| 2.5.8 Target size (minimum) | The whole tile is the target, so it far exceeds 24×24 px |
| 4.1.2 Name, role, value | Role and checked state come from the native input |

## Screen reader output

With the description connected, a selected tile is read roughly as: "Email
alerts, checkbox, checked. Get a summary every morning at 8 a.m."
