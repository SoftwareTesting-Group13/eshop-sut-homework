# HW04 Automation Testing Report - FR-04, FR-09, FR-15

**Student ID:** 23120102 (inferred from the existing HW03 submission folder; verify)  
**SUT:** EShop web frontends  
**Framework:** Playwright  
**Browsers:** Chromium, Firefox, WebKit

## Scope and method

The three selected features are FR-04 personal profile management, FR-09 discount coupons, and FR-15 admin product CRUD. They cover Pools A, B, and C respectively, as required by HW04. Test inputs are separated into JSON files. The suite uses multiple assertion patterns: visible state and text, form values and disabled/focused state, and observed request behavior.

Each feature has at least 12 data rows. `run-matrix.js` executed each feature independently in each browser and created nine Playwright HTML reports. Reports include a `Run by: 23120102` test annotation and an ISO timestamp. The machine-readable per-run results are in `matrix-results.json`.

| Feature | Cases | Chromium | Firefox | WebKit |
|---|---:|---|---|---|
| FR-04 Profile | 13 | 7 pass / 6 fail | 7 pass / 6 fail | 7 pass / 6 fail |
| FR-09 Coupons | 12 | 12 pass / 0 fail | 12 pass / 0 fail | 12 pass / 0 fail |
| FR-15 Product CRUD | 13 | 7 pass / 6 fail | 8 pass / 5 fail | 7 pass / 6 fail |
| Total | 38 | 26 pass / 12 fail | 27 pass / 11 fail | 26 pass / 12 fail |

**Overall:** 114 browser executions, 79 passed and 35 failed.

These reports were generated before the eight follow-up commits that strengthened assertions and report annotations. Regenerate the matrix before submission so the evidence corresponds to the final committed spec revision.

## Test isolation and limits

The current suite intercepts API responses to make frontend flows deterministic and avoid changing the shared SQLite database. This provides frontend form, feedback, navigation, and request-payload coverage. It does not validate live persistence, server-side coupon eligibility, token enforcement, or database constraints. Those rules require a second test pass against a resettable local backend, with isolated accounts, cart contents, and product records. The 36 FR-09 passes confirm only display and interaction against mocked responses; they do not confirm the server-side coupon rules.

## Review findings

FR-04 failures were consistent across all three browsers: the form accepts a 10-digit number beginning with `1` and rejects valid examples beginning with `0`. FR-15 failures show the form submits a 256-character name, zero/negative/empty prices, and submits with no categories. The edit-isolation check failed in Chromium and WebKit but passed in Firefox; source inspection shows a state update that maps the edited name to every product, so investigate this cross-browser difference before filing. Confirm candidates against the live backend before filing public issues.

The AI-generated tests were reviewed and corrected for an ambiguous coupon amount locator, an incorrect expectation for an empty phone, an unrealistic category-selection action, and an alphabetic value that cannot be typed into a numeric HTML input. The first matrix reported 70 passes and 44 failures; the corrected matrix reports 79 passes and 35 failures.

## Remaining submission evidence

The student must record the unlisted five-minute demo in Vietnamese, show a real test/report run, narrate a script correction, and show face-cam or a terminal running `whoami` and `hostname`. Add the public GitHub URL, actual Git history with eight test-script commits, and genuine issues/screenshots after live confirmation. Do not present the mocked reports as backend verification.
