---
name: test-case-catalog
description: Maintain one authoritative catalog of test cases shared by Domain Testing and BVA. Use when test IDs, obligations, or counts must stay consistent across report sections and the summary.
---

# Test case catalog

Keep a single source of truth for every designed test case. Domain Testing and Boundary Value Analysis may both propose cases; the catalog is where they become one de-duplicated, traceable set so no case is counted twice and no `T-ID` drifts between sections.

For this HW02 student layout, write that catalog in `features/<FEATURE_CODE>/test-cases.md`; put run-specific Actual, Status, and `EV-ID` in `test-results.md` and the feature's `evidence/` log.

## Row schema

`T-ID | feature/requirement | technique(s) | obligation IDs (C/P/B/DR/TR/S/RG-ID as applicable) | objective | precondition/setup | data & action | Expected (oracle ref) | Actual | Status | Evidence`

This is the **data schema**, not a required 11-column report table. In a detailed feature report, display one design catalog such as `ID | Kỹ thuật/nghĩa vụ | Setup + thao tác | Expected`. A separate execution section may use `ID | Actual | Kết quả | Evidence | Bug ID` to make observations easy to scan; it references the same IDs and is not a second case definition. Keep the full mapping in the underlying catalog or evidence. A master report shows counts and links, not full cases.

- **T-ID:** one stable ID per distinct case, never reused for a different case.
- **technique:** where the case was derived. A case covering both a partition and a boundary lists both and stays one row.
- **obligation IDs:** every class, boundary point, decision rule, or transition the case covers, so `coverage-goal-planner` can count from here.
- **Expected:** the oracle from `test-oracle-writer` (or its reference), kept separate from **Actual**.
- **Status:** `designed / passed / failed / blocked / inconclusive / chưa chạy` for a named run. Keep each execution attempt and its `EV-ID` in the evidence log; a designed case is not evidence that behavior passed.
- **Interface routes:** For each T-ID, keep API and ordinary manual UI routes under the same case when they exercise the same input/state and oracle. Give UI steps, visible observation and screenshot target where reachable. If the UI blocks or transforms the input, explain the difference and retain the API route; create a separate T-ID only when the UI stimulus or oracle is materially different. Keep route-specific execution status and EV-ID separate, so one API PASS/FAIL does not claim a UI result.

## Method

1. Create the catalog before drafting any report section. Add a row when a technique selects a case; do not re-declare the same case in a second section.
2. Assign the `T-ID` once and reuse it everywhere: report writers, coverage, bug reports, and the summary. Link, do not copy.
3. Merge proposed cases when the same setup, stimulus, and observation can verify their required oracle assertions in one execution. Keep one row and list **all** technique and obligation links, even when the obligations differ. Use a separate case when setup, stimulus, or required observation differs materially; similar inputs alone do not justify merging.
4. Update status and evidence only from observed execution. Leave unreached or unexecuted cases visibly not-executed. For reruns, keep every `EV-ID` and identify the run used for summary counts rather than overwriting history.
5. When EP/Domain and BVA select cases, choose a stable ID when the case first enters the catalog (`DT-` or `BVA-` may identify its origin). Its prefix does not limit its coverage links. Count unique catalog rows for totals; technique subtotals may overlap and must not be summed.
6. Mark cases whose Expected is genuinely undefined by the spec as an explicit observation/inconclusive status rather than PASS or FAIL, and exclude them from pass/fail arithmetic.

## Integration

- `domain-testing-report-writer` and `boundary-value-report-writer` embed or link rows instead of maintaining their own tables; a shared case appears once with both sections linking to it.
- `feature-testing-report-writer` uses the catalog for one feature and may present execution as an ID-linked view.
- `testing-report-assembler` aggregates counts from feature catalogs: unique test cases designed, executed, passed, failed, not yet executed. State the counting convention.
- `test-findings-report-writer` links each bug to its `T-ID`; bug IDs are feature-scoped (`BUG-<FEATURE_CODE>-NN`) so they stay unambiguous when several features are aggregated.
- `coverage-goal-planner` maps obligation IDs to `T-ID`s using the catalog.

## Checks

- Every reported case appears exactly once, with a unique `T-ID`.
- Every `T-ID` traces to at least one obligation and one oracle.
- Counts in the summary equal the number of distinct catalog rows in each status for the named run; no case is double-counted across Domain Testing and BVA, and reruns do not add new cases.
- A summary that sums several case classes names each class, and any inconclusive/observation case is stated and excluded from pass/fail totals.
- Expected and Actual are never merged, and unexecuted cases are never marked passed.
