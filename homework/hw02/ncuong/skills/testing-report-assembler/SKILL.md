---
name: testing-report-assembler
description: Build a concise Vietnamese master testing report from detailed per-feature reports. Use when several features need shared test counts, findings, bug summaries, and links without repeating their full testing process.
---

# Testing report assembler

Write the **master report** in Vietnamese, retaining technical terms when clearer. Treat the user's template as a layout/style reference; verify every row against the selected features and their actual reports. Never copy example bug IDs, counts, links, screenshots, or claims into a new report. Do not mention the template or the report-writing process in the submitted report unless the user explicitly requests a provenance note. Use `feature-testing-report-writer` for each detailed feature report and `test-case-catalog` for unique case counts.

## Two-level contract

- **Master report:** `reports/main-report.md` provides navigation and cross-feature synthesis. Show student information if provided, selected features and links to their four report files, one test execution summary by feature and total, a master bug table, severity statistics and criteria, then one short reproduction entry for **every** bug in that table. Do not repeat spec analysis, partitions, BVA derivation, or full case rows here. Link to `../features/<FEATURE_CODE>/domain-analysis.md`, `boundary-analysis.md`, `test-cases.md`, and `test-results.md`; evidence links use `../features/<FEATURE_CODE>/evidence/...`.
- **Feature reports:** the four files in `features/<FEATURE_CODE>/` trace specification, domain model, boundaries, selected cases, execution, coverage, and findings. The master report links to them as the source of detail.
- **Incidental findings outside EP/BVA:** retain their evidence in supporting materials and link it from the master report. Keep their cases out of EP/BVA technique counts. If the student confirms them as bugs, include them in the final bug reporting and GitHub Issue workflow required by HW02.
- Keep the AI Audit Report, AI Critique, commit log, and submission packaging separate or linked as the assignment requires. A master report can point to these artifacts but cannot silently substitute for them.

## Assemble

1. Identify the actual selected features and map each to its four report paths. Mark missing feature reports `Chưa thực hiện`; do not substitute a different feature merely because it appears in a sample template.
2. Read the single case catalog and bug list for each feature. Select and name the run used for current result counts; retain links to earlier runs. Aggregate unique `T-ID`s and reproduced candidate findings, using stable IDs and direct links to detailed sections; distinguish candidates awaiting student review from student-confirmed bugs. Show `designed`, `executed`, `passed`, `failed`, `inconclusive`, `blocked`, and `not yet run`. Count distinct cases, not EV-ID attempts or overlapping technique subtotals. For the selected run, `executed = passed + failed + inconclusive` and `designed = executed + blocked + not yet run`; explain any other status convention explicitly.
3. In the master bug table, include reproducible candidate defects supported by execution evidence, marked as awaiting student review until the student confirms them. Keep source-only observations in the detailed feature report until verified; do not add a separate source-observation section to the master unless requested. Give **every distinct bug** its own row and its own short detail entry; never merge two defects because they affect the same feature or rule. One defect may cite several related failed cases. Keep the feature-scoped bug ID (`BUG-<FEATURE_CODE>-NN`) so a row traces straight back to its feature report. Link published issues only when they exist; otherwise mark them pending. For HW02, mark Issue and screenshot as pending student review until the student confirms the bug; the final submission requires both.
4. Include severity totals by feature and a concise table defining Critical/High/Medium/Low. Give priority separately from severity when the table uses both; justify the assigned levels from impact and urgency rather than copying unverified examples.
5. Preserve the student's AI Gap Analysis verbatim or mark it pending. Do not write the student's gap comparison or inferred reasons for them.
6. For every master-table bug, provide a compact entry with the feature-scoped ID, severity, feature, numbered manual reproduction steps, Actual, Expected, and root cause only when supported. Keep screenshot status pending until the student reviews the bug, captures the screenshot, and attaches it to the Issue. Link the feature report for the full reproduction block; keep both descriptions consistent. End each bug entry with a `---` rule so entries stay separated. A blank copy of the master outline is provided at `assets/master-report-template.md`.

## Suggested master outline

0. `Thông tin sinh viên` when supplied
1. `Feature đã chọn` — one row per feature and a link to its detailed report
2. `Tổng hợp test case và kết quả` — one row per feature plus total
3. `Tổng hợp bug` — full bug table; severity statistics; severity criteria; one concise reproduction entry for every table row

Adapt headings to the user's template. Keep the master short enough that a reader can find a feature, a case, or a bug without scrolling through its full derivation.

## Final checks

- The feature list matches the actual selection; sample-template data are not treated as results.
- Every count reconciles with unique case IDs in feature reports for the named run; reruns do not increase case counts, and total bugs count defect IDs, not failing tests.
- Any case counted as `Đã chạy` cites a real execution and an `EV-ID` for the named run in the feature evidence log; source-code inspection alone is **not** execution.
- Every included finding has exactly one master-table row and one concise master detail entry, plus a feature report entry, related case/evidence, and an honest issue status. Bug IDs keep their feature code; distinct bugs stay separate even if related; for HW02, final Issue screenshots are required and are captured by the student after review.
- Links resolve from `reports/main-report.md` and the master report does not contradict any feature file or required README summary.
