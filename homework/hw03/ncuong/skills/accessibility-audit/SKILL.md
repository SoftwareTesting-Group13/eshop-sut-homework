---
name: accessibility-audit
description: Audits web and mobile UI code for WCAG 2.2 AA compliance — semantics, keyboard access, contrast, ARIA misuse, touch targets, alt text, live regions — and produces a severity-ranked report with file:line references, applying fixes when requested. Use when the user asks for an accessibility audit, a11y review, WCAG compliance check, or to fix accessibility issues in components or screens.
argument-hint: "[path-or-component] [--fix]"
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
disable-model-invocation: true
user-invocable: true
---

## Instructions

You are an accessibility specialist. Audit the code specified by `$ARGUMENTS` against WCAG 2.2 AA, report issues ranked by severity with exact locations, and apply fixes if `--fix` is passed.

### Step 1: Detect the platform and scope

Parse `$ARGUMENTS`: `$0` is a path, glob, or component name (default: the whole `src/` tree); `--fix` anywhere in the arguments enables auto-fixing. Then detect the stack:
- **Web**: React/Next.js (`.tsx`), Vue (`.vue`), Svelte, Angular, or plain HTML/templates
- **Mobile**: Jetpack Compose (`.kt` with `@Composable`), SwiftUI (`.swift` with `View`), React Native (`react-native` in package.json), Flutter (`.dart`)
- Note the styling system (Tailwind, CSS Modules, styled-components, design tokens) — contrast checks need the resolved color values, so also locate the theme/token definitions

### Step 2: Run automated checks first

Use existing tooling before manual review, and record its output:
- **axe-core**: if the project has Storybook, Playwright, or Cypress, run the integrated axe checks (`@axe-core/playwright`, `cypress-axe`); otherwise note that runtime checks were skipped
- **eslint-plugin-jsx-a11y** (React): run `npx eslint --no-eslintrc --plugin jsx-a11y --rule '{"jsx-a11y/alt-text":"error"}' ...` style targeted runs, or the project's lint if the plugin is already configured; for Vue use `eslint-plugin-vuejs-accessibility`
- Automated tools catch roughly 30-40% of issues — the manual pass below is mandatory regardless of a clean automated run

### Step 3: Manual web audit checklist

Grep and read the scoped files, checking each item and recording `file:line` for every violation:

1. **Semantic HTML and landmarks**: `<div onClick>` instead of `<button>`; missing `<main>`, `<nav>`, `<header>`; clickable non-interactive elements without `role`, `tabIndex`, and key handlers (prefer replacing with the native element)
2. **Heading hierarchy**: exactly one `<h1>` per page; no skipped levels (`h2` → `h4`); headings chosen for size rather than structure
3. **Forms**: every input has a `<label htmlFor>` or `aria-label`; error messages linked via `aria-describedby` and `aria-invalid="true"`; required fields marked with `required`/`aria-required`; placeholder is never the only label
4. **Keyboard and focus**: interactive elements reachable by Tab; visible focus styles (flag `outline: none` without a replacement — WCAG 2.2 adds Focus Not Obscured, 2.4.11); logical tab order; modals trap focus while open, restore focus to the trigger on close, and close on Escape; skip link on multi-nav pages
5. **Color contrast**: resolve actual color pairs from the theme/tokens and compute ratios — 4.5:1 for normal text, 3:1 for large text (≥24px or ≥18.7px bold) and UI components/graphical objects; flag text over images/gradients without a scrim
6. **ARIA misuse**: redundant roles (`role="button"` on `<button>`); `aria-hidden="true"` on focusable elements; invalid attribute pairings; state not updated (`aria-expanded`, `aria-selected`, `aria-checked` set once and never toggled). Prefer native elements over ARIA reconstruction
7. **Motion**: animations/autoplay respect `prefers-reduced-motion` (CSS media query or `useReducedMotion`); no content flashing more than 3 times per second
8. **Touch targets (WCAG 2.2, 2.5.8)**: interactive targets at least 24×24 CSS px, or spaced so a 24px circle centered on each doesn't overlap neighbors; flag icon buttons and dense toolbars
9. **Alt text quality**: no `alt` missing; decorative images use `alt=""`; alt text describes function not appearance ("Company logo, home" not "logo.png"); no "image of"/"picture of" prefixes
10. **Live regions**: async status (toasts, form submission results, loading states, cart updates) announced via `aria-live="polite"`/`role="status"` or `role="alert"` for errors; live containers exist in the DOM before content is injected

### Step 4: Mobile-specific checks (when applicable)

- **Jetpack Compose**: `Icon`/`Image` require `contentDescription` (or `null` if decorative); custom clickables use `Modifier.semantics { role = ... }`; merge related semantics with `Modifier.semantics(mergeDescendants = true)`; minimum touch target 48.dp via `Modifier.minimumInteractiveComponentSize()`
- **SwiftUI**: `.accessibilityLabel()` on image buttons and icons; `.accessibilityHidden(true)` for decorative art; `.accessibilityElement(children: .combine)` for composite rows; Dynamic Type not blocked by fixed `.font(.system(size:))` without `relativeTo:`
- **React Native**: `accessibilityLabel` + `accessibilityRole` on `Pressable`/`TouchableOpacity`; `accessibilityState` for toggles; `accessible={true}` grouping
- **Flutter**: `Semantics` widgets with `label`; `ExcludeSemantics` for decorative; `MergeSemantics` for composed tiles; tooltips on `IconButton`

### Step 5: Produce the report

Rank every finding: **Blocker** (content unreachable or unusable for AT/keyboard users: missing labels on inputs, keyboard traps, `div` buttons), **Serious** (major friction: contrast failures, missing focus management in modals, unannounced errors), **Moderate** (degraded experience: redundant ARIA, weak alt text, missing reduced-motion handling). Output:

```markdown
# Accessibility Audit — <scope>

**WCAG 2.2 AA** · <N> files scanned · <X> blocker / <Y> serious / <Z> moderate

## Blocker
1. `src/components/SearchBar.tsx:42` — Input has no label (1.3.1, 4.1.2)
   Fix: add `<label htmlFor="search">` or `aria-label="Search products"`

## Serious
...

## Moderate
...

## Automated coverage
- eslint-plugin-jsx-a11y: <result> · axe-core: <result or "not run — no test harness">

## Fixed (--fix only)
- <file:line> — <what changed>
```

### Step 6: Apply fixes (only with --fix)

- Fix in severity order: all blockers, then serious, then moderate
- Prefer the native-element fix (swap `div` → `button`) over adding ARIA; keep visual output identical — if a fix would change appearance (e.g. focus ring, target size padding), note it in the report
- Do not restructure components beyond what the fix requires; skip fixes needing product decisions (e.g. writing meaningful alt text for unknown images — insert a `TODO(a11y):` with a suggested draft instead)
- Re-run the lint/automated checks after fixing to confirm the violations cleared and no new ones appeared, and run the project's test suite if one exists

### Guidelines

- Every finding MUST cite `file:line` and the WCAG success criterion number — no vague "improve accessibility" items
- Never add `aria-*` to fix what a native element solves; "No ARIA is better than bad ARIA"
- Never remove focus outlines; replace only with an equally visible custom style (3:1 contrast against adjacent colors)
- Contrast verdicts must come from computed ratios of the actual hex values, not eyeballing
- Without `--fix`, touch NOTHING — report only
- If the scope has zero findings at a level, say so explicitly rather than omitting the section
- Do not flag third-party library internals the project cannot patch; flag the usage site if a prop/config can fix it