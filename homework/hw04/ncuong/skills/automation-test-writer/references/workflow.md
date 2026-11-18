# Workflow: prompt ladder + per-step checklist

## Step 1 — Test plan (no code)

> You are an automation tester for [APP] (web: [WEB_URL], admin: [ADMIN_URL], API: [API_URL]).
> Feature: [FR-ID] [one-line description].
> Test-case catalog (confirmed): <paste the table>.
> Build an automation TEST PLAN with >=12 cases (positive/negative/edge). Columns: T-ID | type | input data | UI steps | exact oracle | UI-automatable?
> No code in this step.

Check: ≥12 rows; every oracle falsifiable (URL / text / count / status); API-only rows justify which form constraint blocks them.

## Step 2 — Skeleton (one sample only)

> Generate the Playwright TS skeleton for this feature: playwright.config.ts with chromium/firefox/webkit projects, a data/ JSON file, tests/*.spec.ts, a JSON loader helper. Only the skeleton + 1 sample case reading from JSON. None of the remaining cases yet.

Check: data file parses; `npx playwright test --project=chromium --grep "@<tag>"` → 1 passed.

## Step 3 — Data + specs in batches

> Write the next 2 test cases (T-IDs ...) per the agreed plan. Data comes from data/<id>.json (extend its schema first if a column is missing). Use getByRole/getByLabel, no XPath or positional selectors. No hardcoded test data in code.

After each batch: run the feature tag on chromium; keep the pass/fail signature; fix immediately.

## Step 4 — Three browsers

> Run all three browsers, one report per run, each carrying run-attribution metadata (owner ID + ISO timestamp).

Commands (never add `--reporter=` — it overrides the configured reporters):
`FEATURE=<id> BROWSER=<b> npx playwright test --project=<b> --grep "@<tag>"` for b in chromium firefox webkit. Write a sidecar metadata file next to each report and verify the metadata inside the report bundle.

## Step 5 — Review (human, mandatory)

Ask: (1) what did the AI generate wrong, (2) weak or missing assertions, (3) missed edge cases, (4) root cause — prompt quality, model limits, or app trait. Record as a gap table in the main report. Usual finds: guessed locators, asserts on stale pre-request state, dialog races, missing cleanup, oracles broken by interacting app bugs.

## Step 6 — Bugs + commits

- One tracker issue per root cause (not per red test), each with a screenshot (UI row/dialog or JSON evidence shot).
- Commit per concern: `test(<id>): ...` for spec changes (each commit must touch a `.spec.*` file), `docs(<id>): ...` for reports/bugs.
