# HW04 automation draft - FR-04, FR-09, FR-15

This folder contains browser automation for the selected EShop web features. Student ID defaults to `23120102` based on the existing HW03 submission folder; verify it before submission and override it with `STUDENT_ID` if needed.

## Coverage

- FR-04 profile: 12 data rows plus one unauthenticated case.
- FR-09 coupon: 12 data rows for percent/fixed discounts, thresholds, expiry, unknown/blank codes, login, and usage limit.
- FR-15 product CRUD: 12 data rows plus one edit-isolation regression case.
- Three browsers: Chromium, Firefox, WebKit; 38 cases × 3 browsers = 114 executions.
- JSON inputs are in `data/`; assertions cover visible state/text, values, disabled/focused state, and requests.

## Run

```powershell
cd automation
npm install
npx playwright install chromium firefox webkit
$env:STUDENT_ID = '23120102'
npm run test:matrix
```

The matrix script starts both Vite frontends and writes nine HTML reports plus `matrix-results.json`. Reports are genuine Playwright executions and should be regenerated after test changes, not manually edited. `reports/all/` is the earlier superseded combined run; use the nine named reports below.

## Final browser results

**114 executions: 79 passed, 35 failed.** All 36 FR-09 UI cases passed against controlled API responses. FR-04 had 18 failures (the same six cases in every browser): the UI accepts a 10-digit phone beginning with `1` and rejects valid examples beginning with `0`. FR-15 had 17 failures: the UI submits a name over 255 characters, zero/negative/empty prices, and an empty category list. The edit-isolation regression failed in Chromium and WebKit but passed in Firefox; confirm that difference before filing a public issue.

Each report includes a `Run by: 23120102` test annotation and ISO timestamp in test metadata. The previous first run (before harness corrections) was 70 passed and 44 failed. The harness fixes included exact matching for coupon amounts, correcting the empty-phone expectation, modeling the no-category fixture accurately, and replacing an untypeable alphabetic value in an HTML number input with a positive decimal price.

These nine reports were generated before the eight follow-up commits that strengthened test assertions and report annotations. They are genuine results for the earlier spec revision; regenerate the matrix before submitting so the report source matches the committed specs. The eight qualifying commits are listed in `git-commit-log.txt`.

## Limits and remaining evidence

All API responses are intercepted for repeatability and to avoid modifying the shared SQLite database. The suite tests browser/UI behavior and request handling only; it does not establish live persistence, server-side coupon rules, JWT enforcement, or backend validation. Add a separate live-backend run using resettable accounts/cart/products before submission.

The assignment also requires evidence the student must create: an unlisted video with their Vietnamese narration and face-cam or terminal `whoami`/`hostname`; a public GitHub link; genuine confirmed issues/screenshots; and eight meaningful commits changing test scripts. See `demo-video-outline.md`. Do not represent the mocked UI reports as backend verification.
