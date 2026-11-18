---
name: automation-test-writer
description: Use when creating data-driven Playwright automation for an EShop web feature (FR-##) from an HW02 test-case catalog; triggers include automation test, Playwright spec, data-driven test, multi-browser run, FR-02, FR-10, FR-17.
license: PolyForm-Noncommercial-1.0.0
metadata:
  version: "1.0.0"
  compatibility: "Playwright 1.65+, Node 22+, EShop SUT (web 5173, admin 5174, API 3000)"
  author: "ncuong (HW04)"
  language: "en"
  category: "test-automation"
---

# Automation Test Writer (HW04 EShop workflow)

Convert an HW02 test-case catalog for one EShop web feature into a data-driven Playwright suite that runs on Chromium/Firefox/WebKit and produces `Run by:` HTML reports. Proven on FR-02 (16 tests, 11/5), FR-10 (16 tests, 13/3), FR-17 (18 tests, 10/8).

## When to Use

- New web feature (FR-##, Pools A/B/C) with an HW02-style catalog (`DT-*`/`BVA-*`, setup + oracle per case).
- Extending an existing feature suite with more cases from the same catalog.
- Regenerating the skeleton (config, data file, helpers) for a fresh checkout.

Do not use it to invent oracles, skip the test plan, write all cases in one prompt, or record the demo video.

## Inputs (required)

1. Feature ID + pool (e.g. `FR-10`, Pool B) and SUT routes it touches (web `/...`, admin tab, API endpoints).
2. Test-case catalog file with per-case oracle (e.g. `homework/hw02/ncuong/features/FR10/test-cases.md`).
3. Real-DOM facts: actual input `type`s, label wiring, button names, badge texts (read the `.jsx` — never guess).
4. Backend facts: status codes, counter/lock rules, validation gaps (read `server.js` — never guess).

## Procedure (6 steps, one prompt per step — never a single "write everything" prompt)

1. **Test plan.** Build table `T-ID | loại | input | bước UI | oracle | chạy được bằng UI không`. Mark API-only cases (no form control for that input-state) for request assertions in the same spec. See `references/workflow.md`.
2. **Skeleton.** Run `scripts/new-feature.sh <FR-ID> <tag>` — creates `tests/<fr>.spec.ts` (1 sample test), `data/<fr>.json` (sample rows), wired to `tests/helpers/` (`json-loader`, `eshop-api`). Verify: JSON parses, 1 test passes on chromium.
3. **Data file.** Expand `data/<fr>.json` to all planned rows. Schema per domain (login/order/coupon — see templates). No test data in `.spec` files.
4. **Specs in batches (1–2 cases per prompt).** From `templates/`, data-driven loop `for (const row of rows)`. Then run on chromium immediately.
5. **Run 3 browsers + fix.** `FEATURE=<fr> BROWSER=<b> npx playwright test --project=<b> --grep "@<tag>"` (never `--reporter=...` — it overrides the HTML reporter). Fix failures, re-run; keep failing-on-bug asserts strict and document them.
6. **Review + evidence.** Gap table (AI got wrong/missed/why), bug reports + screenshots + GitHub issues, `report-meta.txt` next to each report.

## Hard Rules (violations fail HW04 grading)

- Test data only in `data/*.json` — no inline datasets; env-overridable creds/URLs only.
- ≥3 assertion patterns per feature (URL, content/attribute, absence `toHaveCount(0)`, API `waitForResponse` + status, storage, dialog `waitForEvent`, row count).
- Locators: `getByRole`/`getByLabel`/`getByPlaceholder`/`getByText(exact)`; no XPath, no `:nth-child`, no `waitForTimeout`.
- Unique data per run (`uniqueSuffix(projectName)`); `beforeEach`-style isolation; `try/finally` + delete helpers so re-runs and DB stay deterministic.
- Every report embeds `Run by: 23120223` + ISO timestamp (top-level `metadata`, verified inside `report.json`).

## Output Contract

- `tests/<fr>-*.spec.ts` (tagged `@<tag>`), `data/<fr>*.json`, `tests/helpers/` reused.
- `reports/html/<fr>-{chromium,firefox,webkit}/` + `report-meta.txt` each; same pass/fail signature on all 3 browsers.
- `features/<FR>/test-plan-automation.md`, `features/<FR>/bugs/BUG-*.md` + `screenshots/`, `features/<FR>/issues/publish.sh`.

## Pre-delivery Check

- [ ] JSON parses; `grep` shows no test-data literals in spec.
- [ ] 1 sample passes on chromium before writing the rest.
- [ ] Full suite green-count stable across 2 consecutive chromium runs (flakes fixed, not tolerated).
- [ ] All 3 browsers run; failure sets identical or differences explained.
- [ ] Every red test maps to a bug report + issue + screenshot (no red without a bug).
- [ ] DB back to seed state after suite (`sqlite3 ... SELECT COUNT(*)`).

## Common Pitfalls (from FR-02/10/17)

- Asserting before the PUT response arrives → false-pass on stale state. Always `waitForResponse` first.
- `page.on('dialog')` + immediate assert → race. Use `await page.waitForEvent('dialog')`.
- `--reporter=line` kills HTML output (overrides config reporters).
- `expect` before cleanup in API-reject tests leaks DB rows → wrap in `try/finally`.
- SUT servers die when idle → `curl` health-guard API/WEB/ADMIN before every run.
- Refactors that rename helpers must update all call sites — rerun the suite right after.
