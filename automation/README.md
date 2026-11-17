# HW04 Automation Submission - FR-04, FR-09, FR-15

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

## Latest browser results

**114 executions: 78 passed, 36 failed.** The nine reports were regenerated on 2026-11-17 after the follow-up test-script commits. FR-04 had 18 failures (six per browser): the UI accepts a 10-digit phone beginning with `1` and rejects valid examples beginning with `0`. All 36 FR-09 UI cases passed against controlled API responses. FR-15 had 18 failures (six per browser): the UI submits a name over 255 characters, zero/negative/empty prices, and an empty category list. The edit-isolation regression failed in all three browsers in this run.

Each report includes a `Run by: 23120102` test annotation and ISO timestamp in test metadata. The previous first run (before harness corrections) was 70 passed and 44 failed. The harness fixes included exact matching for coupon amounts, correcting the empty-phone expectation, modeling the no-category fixture accurately, and replacing an untypeable alphabetic value in an HTML number input with a positive decimal price.

Each report is a genuine Playwright execution for the final committed specs and carries `Run by: 23120102` plus an ISO timestamp. The matrix summary is in `matrix-results.json`. The eight qualifying test-script commits are listed in `git-commit-log.txt`.

## Limits and remaining evidence

All API responses are intercepted for repeatability and to avoid modifying the shared SQLite database. The suite tests browser/UI behavior and request handling only; it does not establish live persistence, server-side coupon rules, JWT enforcement, or backend validation. The assignment does not require a real-database run; keep this limitation explicit and add backend evidence only if claiming server-side behavior.

## Submission links and self-assessment

The main report, AI Audit, and AI Critique PDFs are in `output/pdf/`.

- Public GitHub repository: https://github.com/SoftwareTesting-Group13/eshop-sut-homework
- Unlisted YouTube demo: **ADD THE VIDEO URL AFTER UPLOADING `D:/2026-11-17 11-52-18.mp4`**
- Student name: **FILL IN YOUR NAME**
- Student ID: `23120102` (verify before submission)
- Suggested self-assessment (student must review and set the grades):

| Criterion | Maximum | Self-assessed |
|---|---:|---:|
| Task 1 - Feature A (FR-04) | 25 | ___ |
| Task 1 - Feature B (FR-09) | 25 | ___ |
| Task 1 - Feature C (FR-15) | 25 | ___ |
| Task 2 - Demo video | 15 | ___ |
| Agent Skill | 10 | ___ |
| **Total** | **100** | **___** |

No reusable Agent Skill is included in this submission yet. The assignment describes it as encouraged and assesses it separately; only claim that credit if you add the skill and its end-to-end demonstration.

The assignment also requires a student-recorded, unlisted video with Vietnamese narration and face-cam or terminal `whoami`/`hostname`; a public GitHub link; genuine confirmed issues/screenshots when a real defect is found; and eight meaningful commits changing test scripts. See `demo-video-outline.md`. Do not represent the mocked UI reports as backend verification. Git commits are currently local and must be pushed before relying on the public repository link.
