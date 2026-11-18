# HW04 prompt ladder + per-step checklist (extract of the proven FR-02/10/17 run)

## Step 1 — Test plan (no code)

> Bạn là tester tự động hóa cho SUT EShop (React + Vite, web: http://localhost:5173, admin: http://localhost:5174, API: http://localhost:3000/api).
> Feature: FR-__ (Pool __). Bảng test case HW02: <paste DT-*/BVA-* table>.
> Hãy lập TEST PLAN tự động hóa gồm >=12 ca (positive/negative/edge), bảng: T-ID | loại | dữ liệu input | bước thao tác UI | oracle cụ thể | có chạy được bằng UI không.
> Không viết code ở bước này.

Check: ≥12 rows, each oracle falsifiable (URL / text / count / status), API-only rows justified (which form constraint blocks them).

## Step 2 — Skeleton (1 sample only)

> Sinh cấu trúc Playwright TS: playwright.config.ts với projects chromium/firefox/webkit, thư mục data/ (file .json), tests/*.spec.ts, helper đọc JSON. Chỉ sinh skeleton + 1 ca mẫu đọc từ JSON. Không viết các ca còn lại.

Check: `npx playwright test --project=chromium --grep "@<tag>"` → 1 passed; JSON parses.

## Step 3 — Data + specs in batches

> Viết 2 test case tiếp theo (T-ID ...) theo test plan. Dữ liệu đọc từ data/<fr>.json. Dùng getByRole/getByLabel, không XPath hay :nth-child. Không hardcode test data trong code.

After each batch: run chromium for the feature tag; keep pass/fail signature; fix immediately.

## Step 4 — 3 browsers

> Chạy đủ 3 browser, mỗi lần 1 report riêng có "Run by: {StudentID}" + ISO timestamp.

Commands (never add `--reporter=`):
`FEATURE=<fr> BROWSER=<b> npx playwright test --project=<b> --grep "@<tag>"` for b in chromium firefox webkit; write `report-meta.txt` per report; verify `report.json` metadata inside each `index.html`.

## Step 5 — Review (human, mandatory)

Prompt yourself: (1) what did AI generate wrong, (2) weak/missing assertions, (3) missed edge cases, (4) root cause (prompt quality / model limits / SUT trait). Record as gap table in the main report. Typical finds: label-not-wired locators, assert-before-PUT false-pass, dialog race, missing try/finally cleanup, SUT bug interactions (e.g. +2 counter causing early lock).

## Step 6 — Bugs + commits

- One GitHub issue per root cause (not per red test), each with screenshot (UI row/dialog or JSON evidence shot).
- Commit per concern: `test(<fr>): ...` for spec changes (each must touch a `.spec.*` file), `docs(<fr>): ...` for reports/bugs.
