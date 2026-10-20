---
name: checkbox-tile
description: Owns the checkbox tile component, a selectable card with an icon, a heading, a description and a check indicator. Covers its anatomy, properties, variants, states and platform contracts. Use when designing, building, reviewing or writing content for a checkbox tile on web, iOS or Android. Do not use for plain checkboxes or for single-choice radio tiles.
---

# Checkbox tile

A checkbox tile lets someone pick any number of options from a set, where
each option needs more explanation than a checkbox label can carry. The
whole tile toggles the selection.

This file owns identity, anatomy, properties and the shared contract. Other
concerns live in their own files. Load only the ones the task needs:

| Concern | Owner | Load when |
|---|---|---|
| When to use it and how to write content | [usage.md](usage.md) | writing or reviewing content, or choosing between components |
| Web token cells | [web/tokens.yaml](web/tokens.yaml) | building or auditing for web |
| Web interaction | [web/interaction.md](web/interaction.md) | building for web |
| Web accessibility | [web/accessibility.md](web/accessibility.md) | building or reviewing for web |
| Mobile behavior shared by iOS and Android | [mobile/overview.md](mobile/overview.md) | building for either mobile platform |
| Mobile token cells | [mobile/tokens.yaml](mobile/tokens.yaml) | building or auditing for mobile |
| iOS specifics | [mobile/ios/interaction.md](mobile/ios/interaction.md) | building for iOS |
| Android specifics | [mobile/android/interaction.md](mobile/android/interaction.md) | building for Android |

Token values are owned by the [design-tokens](../design-tokens/SKILL.md)
skill. Files here reference token paths and never copy values.

## Anatomy

```
┌──────────────────────────────────────────┐
│ [icon]  Heading                      [✓] │
│         Description text that can wrap   │
│         onto a second line.              │
└──────────────────────────────────────────┘
```

| Part | Required | Notes |
|---|---|---|
| container | yes | The whole tile. It is the hit area and carries the border. |
| indicator | yes | The check box in the top trailing corner. It shows the selection; it is not a separate control. |
| icon | no | A slot for one icon from the system set. It's decorative: the heading carries the meaning. |
| heading | yes | One line. It names the option. |
| description | no | Up to two lines. It explains the option. |

## Properties

| Property | Type | Default |
|---|---|---|
| `checked` | boolean | false |
| `disabled` | boolean | false |
| `showIcon` | boolean | true |
| `showDescription` | boolean | true |
| `layout` | `inline` or `stacked` | `inline` |

In `inline` layout the icon sits to the leading side of the text. In
`stacked` layout it sits above the heading. Both layouts use the same token
cells.

## Contract

The audit reads the three lists below. Every platform must define every
shared state, and every state must define every token property.

### Shared states

- `default`
- `selected`
- `disabled`

Platforms add their own states (web adds hover; mobile adds pressed). Each
platform declares its additions in its interaction file.

### Token properties

- `container-background`
- `container-border`
- `icon-color`
- `heading-color`
- `description-color`
- `indicator-fill`
- `indicator-border`
- `indicator-check`

## Done when

- The spec passes the audit in [spec-audit](../spec-audit/SKILL.md).
- Every part in the anatomy table appears in each platform's build.
- No file in this folder contains a raw color value.
