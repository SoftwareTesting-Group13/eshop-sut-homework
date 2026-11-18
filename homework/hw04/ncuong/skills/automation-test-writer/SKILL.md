---
name: automation-test-writer
description: Turn a feature test-case catalog into a data-driven Playwright suite (separate JSON/CSV data, >=3 assertion patterns, 3 browsers, attributable HTML reports). Use when scaffolding or extending web UI automation, or when regenerating a suite skeleton for a new feature.
---

# Automation test writer

Convert a per-feature test-case catalog into a Playwright suite that is data-driven, multi-browser, and reproducible. Proven end to end on three features (16, 16, and 18 cases with identical pass/fail signatures on Chromium/Firefox/WebKit); see `examples/` for that instantiation.

## When to use

- A new web feature with a test-case catalog (each case has setup, input, and a falsifiable oracle).
- Extending an existing feature suite with more catalog cases.
- Regenerating a suite skeleton (config, data file, helpers, one sample test) on a fresh checkout.

Do not use it to invent oracles, skip the test plan, write all cases in a single prompt, or record demo videos.

## Inputs (required)

1. Feature identifier and the UI surface it touches (routes, tabs/dialogs, API endpoints).
2. Test-case catalog: one row per case with setup, input data, UI steps, and exact oracle.
3. Real-DOM facts read from the frontend source: input `type`s, label wiring, button names, status/badge texts. Never guess selectors.
4. Backend facts read from the API source: status codes, counter/lock/validation rules. Never guess behavior.

## Procedure (one prompt per step — never a single "write everything" prompt)

1. **Test plan.** Build a table `T-ID | type | input data | UI steps | exact oracle | UI-automatable?`. Mark cases no form can express (missing keys, null JSON values, values a widget blocks) for API assertions inside the same spec. Every oracle must be falsifiable (URL, text, count, status code).
2. **Skeleton.** Run `scripts/new-feature.sh <feature-id> <tag>` — creates `tests/<id>.spec.ts` (one sample test) and `data/<id>.json` (sample rows) wired to `tests/helpers/`. Then prove it: JSON parses, the 1 sample passes on chromium.
3. **Data file.** Expand `data/<id>.json` to all planned rows. Test data lives only in this file — never as inline datasets in specs (environment-overridable URLs/credentials are config, not data).
4. **Specs in batches (1–2 cases per prompt).** Data-driven loop over rows. Use `getByRole`/`getByLabel`/`getByPlaceholder`/`getByText(exact)`; no XPath, no positional selectors, no hard sleeps. Run the feature tag on chromium after every batch and fix immediately.
5. **Three browsers + stabilization.** Run each browser in its own process and report directory (never pass `--reporter=...` on the CLI — it overrides the configured HTML reporter). Re-run until the pass/fail signature is stable across two consecutive runs; investigate every flake instead of tolerating it.
6. **Review + evidence.** Gap table (AI got wrong / missed / why), bug report per root cause with screenshots, one tracker issue per bug, per-report run-attribution metadata.

Details, prompt templates, and the per-step checklist: `references/workflow.md`.

## Hard rules

- ≥3 distinct assertion patterns per feature (URL/navigation, content/attribute, absence via zero-count, API response status, client storage, dialog events, row counts).
- Unique data per run (timestamp + browser name); per-test isolation; state-changing API cases wrapped in `try/finally` cleanup so re-runs are deterministic and the database returns to seed state.
- Locators must survive re-renders: re-query rows after each mutation; assert pre-state before acting (an assert that passes on stale content is a false pass — see pitfalls).
- Every HTML report must carry run-attribution metadata (e.g. owner ID + ISO timestamp in the report metadata, plus a sidecar metadata file next to it).

## Output contract

- `tests/<id>.spec.ts` (tagged, e.g. `@checkout`), `data/<id>.json`, shared `tests/helpers/`.
- One HTML report per browser with matching pass/fail signatures (or documented, explained differences).
- Test plan, per-root-cause bug reports + evidence screenshots, issue-tracker publish script.

## Pre-delivery check

- [ ] Data file parses; no test-data literals remain in specs.
- [ ] The 1 sample passes before the rest is written.
- [ ] Full suite stable across 2 consecutive runs on one browser, then run on all 3.
- [ ] Every red test maps to a bug report + issue + screenshot; no red without a bug, no green on stale state.
- [ ] Database back to seed state after the suite.

## Common pitfalls

- Asserting before the network response lands → pass on stale content. Always await the response first, then assert the new state; assert pre-state before acting.
- Reading a dialog message via a persistent listener + immediate assert → race. Use a one-shot dialog wait.
- CLI `--reporter=` flags replace configured reporters and silently drop HTML output.
- Cleanup placed after a failing assert never runs → wrap in `try/finally`.
- Local servers die when idle → health-check API/UI before every run and restart as needed.
- Renaming a helper without updating all call sites → rerun the suite right after every refactor.
