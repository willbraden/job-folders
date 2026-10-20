# Demo: a component as skills

A small, complete example of the deterministic, intent-driven structure,
using a **checkbox tile** (a selectable card with an icon, a heading and a
description) as the component.

Nothing here runs on its own. It shows how the files are split, who owns
what, and how a check catches drift.

## The structure

```
demo/skills/
├── README.md                     index: the router orchestrators read
├── component-build/              ORCHESTRATOR: the order ticket
│   └── SKILL.md                  routing, sequence, handoff checks; owns no facts
├── design-tokens/                OWNER: the one place token values live
│   ├── SKILL.md
│   └── tokens.yaml
├── checkbox-tile/                COMPONENT: one skill per component
│   ├── SKILL.md                  identity, anatomy, properties, contract
│   ├── usage.md                  when to use it and content rules (all platforms)
│   ├── web/                      only what web changes
│   │   ├── tokens.yaml           state × property → token path
│   │   ├── interaction.md        hover, keyboard, the HTML structure
│   │   └── accessibility.md      ARIA, WCAG
│   └── mobile/                   only what mobile changes
│       ├── overview.md           pressed state, touch, shared mobile behavior
│       ├── tokens.yaml
│       ├── ios/interaction.md    SwiftUI, VoiceOver, 44 pt
│       └── android/interaction.md  Compose, TalkBack, 48 dp
└── spec-audit/                   LEAF: deterministic checks
    ├── SKILL.md
    └── scripts/audit_spec.py
```

## How it maps to the deck

| Idea | Where you see it |
|---|---|
| Frontmatter is a selection contract | Each `SKILL.md` description says what the skill covers and names what it doesn't |
| One fact, one owner | Hex values exist only in `design-tokens/tokens.yaml`. Content rules exist only in `usage.md` |
| Reference, don't re-derive | Component token files hold paths like `color.border.selected`, never values |
| Shared root, platform deltas | Anatomy and states are in `checkbox-tile/SKILL.md`. Hover exists only in `web/`; pressed exists only in `mobile/` |
| Platform vocabulary can't leak | The audit fails if "VoiceOver" appears in a web or shared file, or "aria-" in a mobile one |
| Load only what applies | The routing table in `checkbox-tile/SKILL.md` says which file to load for which task |
| Orchestrator as order ticket | `component-build` settles component, platforms and outputs, then pulls only those files |
| Generative inside, deterministic outside | Claude writes the build; `audit_spec.py` checks the contract |
| "Nearest" is not equivalent | An unpublished token path fails the audit. There is no fuzzy match |

## Three orders, three different loads

| Request | What loads |
|---|---|
| "Build the checkbox tile for web" | `component-build` → `checkbox-tile/SKILL.md`, `usage.md`, `web/*` → `design-tokens` → `spec-audit`. Nothing in `mobile/` loads. |
| "Build the checkbox tile for iOS, with a Figma component" | `component-build` → `checkbox-tile/SKILL.md`, `usage.md`, `mobile/overview.md`, `mobile/tokens.yaml`, `mobile/ios/*` → `design-tokens` → `figma:figma-use` → `spec-audit`. Nothing in `web/` or `android/` loads. |
| "How long should a checkbox tile description be?" | Just `checkbox-tile/SKILL.md` and `usage.md`. No orchestrator, because it's a single question. |

## Run the checks

From `demo/skills/`:

```
python3 spec-audit/scripts/audit_spec.py checkbox-tile
python3 ../../skills/skill-maker/scripts/check_skills.py .
```

Both should pass. The first checks the component contract; the second
checks that the skills themselves are well formed.

## Try breaking it

Make any of these edits, then run the audit again. Each failure names the
exact file and cell.

- In `checkbox-tile/web/tokens.yaml`, change `color.border.hover` to
  `color.border.hovered`. **Result:** the hover border cell fails as an
  unpublished token.
- Delete one line under `selected:` in that same file. **Result:** the
  audit reports a missing cell for that state and property.
- Add "VoiceOver" to `usage.md`. **Result:** the audit reports a platform
  word in a shared file.
- Paste `#2F6FEB` into `web/interaction.md`. **Result:** the audit reports
  a raw color that should be a token reference.
- Rename `pressed` to `long-pressed` in `mobile/tokens.yaml`. **Result:**
  the audit reports an undeclared platform state.

Undo your edits with `git checkout demo/`.

## Adding a second component

1. Scaffold the skill from `demo/skills/`:
   `bash ../../skills/skill-maker/scripts/new_skill.sh --into . radio-tile`
2. Copy the `checkbox-tile` file layout and fill it in.
3. Add a row for it to the `component-build` routing table and to
   `README.md`.
4. Run both checks.
