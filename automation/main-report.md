# HW04 Automation Testing Report - FR-04, FR-09, FR-15

**Student ID:** 23120102 (inferred from the existing HW03 submission folder; verify)  
**SUT:** EShop web frontends  
**Framework:** Playwright  
**Browsers:** Chromium, Firefox, WebKit

## Scope and method

The three selected features are FR-04 personal profile management, FR-09 discount coupons, and FR-15 admin product CRUD. They cover Pools A, B, and C respectively, as required by HW04. Test inputs are separated into JSON files. The suite uses multiple assertion patterns: visible state and text, form values and disabled/focused state, and observed request behavior.

Each feature has at least 12 data rows. `run-matrix.js` executed each feature independently in each browser and created nine Playwright HTML reports. Reports include a `Run by: 23120102` test annotation and an ISO timestamp. The final matrix was regenerated on 2026-11-17 after the test-script refinements; machine-readable per-run results are in `matrix-results.json`.

| Feature | Cases | Chromium | Firefox | WebKit |
|---|---:|---|---|---|
| FR-04 Profile | 13 | 7 pass / 6 fail | 7 pass / 6 fail | 7 pass / 6 fail |
| FR-09 Coupons | 12 | 12 pass / 0 fail | 12 pass / 0 fail | 12 pass / 0 fail |
| FR-15 Product CRUD | 13 | 7 pass / 6 fail | 7 pass / 6 fail | 7 pass / 6 fail |
| Total | 38 | 26 pass / 12 fail | 26 pass / 12 fail | 26 pass / 12 fail |

**Overall:** 114 browser executions, 78 passed and 36 failed.

These reports correspond to the final committed spec revision. The local video file is 9 minutes 20 seconds at 1280×720 and contains both video and audio streams. The student must review its narration and visible scenes before uploading. Unlisted YouTube URL: **[ADD VIDEO URL]**.

## Test isolation and limits

The current suite intercepts API responses to make frontend flows deterministic and avoid changing the shared SQLite database. This provides frontend form, feedback, navigation, and request-payload coverage. It does not validate live persistence, server-side coupon eligibility, token enforcement, or database constraints. The assignment's browser-automation requirement does not make a real-database run mandatory; the report limits its conclusions to the mocked frontend behavior. The 36 FR-09 passes do not confirm server-side coupon rules.

## Review findings

FR-04 failures were consistent across all three browsers: the form accepts a 10-digit number beginning with `1` and rejects valid examples beginning with `0`. FR-15 failures show the form submits a 256-character name, zero/negative/empty prices, and submits with no categories. In the final run, the edit-isolation assertion failed in all three browsers. These failures were observed with intercepted API responses; confirm candidates against the real SUT before filing public issues.

The AI-generated tests were reviewed and corrected for an ambiguous coupon amount locator, an incorrect expectation for an empty phone, an unrealistic category-selection action, and an alphabetic value that cannot be typed into a numeric HTML input. The first matrix reported 70 passes and 44 failures; the final matrix reports 78 passes and 36 failures. The updated FR-15 edit-isolation assertion fails in all three browsers; verify the underlying behavior before calling it a confirmed product defect.

## Remaining submission evidence

The student must upload the recorded demo as an unlisted YouTube video, insert its URL, confirm the repository is public and push the local commits, and attach the Git commit log. Create GitHub Issues with screenshots only for defects confirmed against the real SUT; current failures were observed with mocked API responses and remain candidates. Do not present the mocked reports as backend verification.
