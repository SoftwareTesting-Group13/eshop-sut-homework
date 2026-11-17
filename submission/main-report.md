# HW03 GUI Usability Report

**Student:** Nguyễn Ngọc Minh Tuấn  
**ID:** 23120102  
**Email:** 2312102@student.hcmus.edu.vn  
**Selected requirements:** FR-09 Coupons, FR-10 Order state machine, FR-11 User order history, FR-13 Dashboard

> **Evidence status:** Prepared submission and source-based review only. The frontend could not start because dependencies are absent (`vite` unavailable). No live checklist execution, participant sessions, cross-platform run, or screenshots are claimed. Complete the marked evidence templates before Moodle submission.

## Scope and method

Four areas: checkout coupon, admin order transitions, user order history, and admin dashboard. IA-01 general UI, IA-02 forms, IA-03 navigation, IA-04 feedback/state are covered. The workbook contains 80 distinct checks with procedures, expected results, execution status, evidence and notes. Manual review expanded initial AI ideas with keyboard and screen-reader checks, responsive layouts, loading/error/empty states, boundary values, recovery, and trust.

## Execution summary

| Measure | Count |
|---|---:|
| Items designed | 80 |
| Live UI executed | 0 |
| Passed / failed in live UI | 0 / 0 |
| Not run | 80 |
| Source-review candidates | 3 |
| GitHub issues created | 0 |

No pass/fail is assigned to an unobserved UI. Capture a screenshot for each live failure and update the workbook.

## Source-review candidates (pending runtime reproduction)

1. **FR-09/FR-08 checkout amount is editable.** `frontend-web/src/pages/Checkout.jsx` binds `editableTotal` to a numeric input and submits it as `total_amount`, while the SRS says the total is derived and backend-recomputed. Verify with UI and API evidence.
2. **FR-13 revenue is doubled.** `frontend-admin/src/App.jsx` adds `o.total_amount * 2` for delivered orders, conflicting with the required sum. Verify with known fixture totals.
3. **FR-10 canceled orders offer a delivered transition.** `frontend-admin/src/App.jsx` renders “Đánh dấu Đã giao” for canceled orders even though canceled is terminal. Verify UI and API behavior.

These are hypotheses from code, not confirmed runtime bugs. GitHub issue publication and authentic screenshots remain pending.

## Usability evaluation plan

**Objective:** Learn whether users can find/apply a valid discount, understand eligibility and errors, recover from an invalid code, and trust the final payable amount.

**Scenario:** “You are buying household items and have the code SAVE10. Review the order, try to use the code, and complete the purchase if the site allows it. Tell me what you expect to happen as you go.” Use a resettable test account and cart subtotal >= 300,000 VND. Do not coach navigation or eligibility.

**Protocol:** One pilot, then seven real participants outside the HW03 class, one moderated session each. Ask participants to think aloud; test the product, not them. Record only with consent. After each session administer SUS (10 items, 5-point response), then probes about clarity, recovery, speed, and trust. Keep the pilot separate from the seven scored sessions.

**Current evidence:** 0/7 sessions; pilot not run; no SUS responses, findings, or severity scores. Blank forms and seven-row participant register are provided. Do not fabricate names, contacts, scores, or observations.

## Cross-platform coverage

Required Chrome, Firefox, and Safari or Android Chrome with `2312102@student.hcmus.edu.vn` overlay and local URL visible. Completed: 0/3. See `cross-platform/README.md`; no screenshot is fabricated.

## Limitations and remaining work

Vite is unavailable because dependencies are not installed. GitHub Issues and cloud browser testing were not accessed. Complete live checklist, verify bugs and attach screenshots, publish verified issues, run pilot plus seven real sessions, score SUS, run three platforms, update self-grade and report, then regenerate the ZIP.

## References

HW03 assignment PDF supplied by student; local EShop `README.md` and `api_specification.md`; Brooke (1996), System Usability Scale.
