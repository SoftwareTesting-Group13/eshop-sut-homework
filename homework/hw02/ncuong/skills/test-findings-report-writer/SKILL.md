---
name: test-findings-report-writer
description: Prepare Vietnamese bug findings for student review and a human-owned AI Gap Analysis section. Use when documenting reproducible findings before GitHub Issue publication.
---

# Test findings report writer

Write bug-report content in Vietnamese; keep test case, bug, Expected, Actual, and GitHub Issue as technical terms where useful. Separate a missed test, an observed failure, a reproduced candidate bug, and a student-confirmed bug.

For this HW02 student layout, put per-feature bug details and AI Gap Analysis in `features/<FEATURE_CODE>/test-results.md`; `reports/main-report.md` contains the cross-feature summary, a short reproduction for each bug, and links back to those details.

## Human-owned AI Gap Analysis

The student reviews the AI-generated test cases and bugs against their own review and writes this section. Do not perform that comparison on the student's behalf, identify missed cases or bugs as the student's findings, explain why the AI missed them, or assert that no gaps exist. Supply the original AI output and traceable test artifacts when available so the student can compare them. If requested, provide an empty Vietnamese structure with fields for the student to fill.

Suggested blank table: `Gap ID | AI output/source | Test case hoặc bug tôi phát hiện thêm | Cách tôi phát hiện | Vì sao AI bỏ sót (nhận định của tôi) | Bổ sung/sửa chữa`.

Insert the student's completed text into the report only after they provide it. Preserve their meaning and attribution; do not add AI-generated gap claims or causes. Until then, mark the section `Chờ người kiểm thử rà soát và viết` rather than filling it with a speculative analysis.

## Bug reporting

For each observed defect, record a **feature-scoped** bug ID, concise title, requirement and test case IDs, environment/build, preconditions, exact reproduction steps and data, Expected, Actual, reproducibility, impact/severity rationale, and a log/artifact as evidence. Keep a clear link to the GitHub Issue when the assignment requires issue publication. A failing test is not automatically a product bug: check the oracle, setup, and repeatability first; mark unresolved failures as under investigation.

If exploratory work produced findings outside the EP/BVA case catalog, preserve them separately with their evidence and label them outside technique coverage. The student reviews these findings too; any confirmed bug still enters the HW02 bug report and Issue workflow.

- **ID convention:** `BUG-<FEATURE_CODE>-NN` (e.g. `BUG-XX-01`). A master report aggregates bugs from several features, so the feature code must be inside the ID to keep the table searchable and traceable. Do not reuse an ID for a different defect.
- **Manual reproduction:** write each bug so it can be reproduced by hand — numbered steps with exact values, concrete preconditions (specific account and prior state), and the observed result per step. This is the primary artifact; do not replace it with automation-only steps.
- **Screenshots:** prepare reproducible bug evidence first. For HW02, screenshots attached to GitHub Issues are required for final submission. The student reviews each candidate bug, then captures its screenshot and opens the Issue. Mark both artifacts `Chờ người kiểm thử xác nhận` until that review happens.

Suggested summary table: `Bug ID | Test case/requirement | Tóm tắt | Severity | Bằng chứng | GitHub Issue | Trạng thái`. Put the full manual reproduction block below the summary. If no finding was reproduced, state that no bug was reproduced within the executed scope; do not state that the feature has no bugs.

## Publication boundary

For HW02, prepare an issue-ready bug description and evidence, then wait for the student to review the candidate bug. The student captures the screenshot and opens the Issue after confirmation. Record the URL and attached screenshot only after they exist. Do not publish an Issue or mark the submission complete before this review step.

## Review

Any included AI Gap Analysis is identified as student-provided and retains links to the original AI output where the student supplied them. Every reported bug has observed Actual evidence and a requirement-based Expected result. Every bug ID carries its feature code, and every bug has a manual reproduction block. Before student review, label the Issue and screenshot as pending review; this is an expected workflow state. For final submission, verify that every confirmed bug has its GitHub Issue and attached screenshot.
