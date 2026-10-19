---
name: boundary-value-report-writer
description: >
  Write Vietnamese Boundary Value Analysis (BVA) report sections from
  specification-derived boundaries, ON/IN/OUT points, shared test cases,
  and verified execution evidence. Use when documenting boundary selection,
  test traceability, feasibility, and designed versus executed coverage.
---

# Boundary Value Analysis Report Writer

Write a clear, evidence-grounded Boundary Value Analysis (BVA) section in Vietnamese.

Retain technical terms such as BVA, ON/IN/OUT, predicate, test case, oracle, and coverage when useful.

The report must explain not only **which boundary values were selected**, but also **why they were selected**.

Write for the student who must review the test design. For each boundary, make the **boundary entry itself** show the threshold, tested setup/value, Expected on each relevant side, and linked case. Define ON/IN/OUT only if they help this boundary; use a note for precision or feasibility that the entry cannot express.

## 1. Scope and responsibilities

BVA must appear in `features/<FEATURE_CODE>/boundary-analysis.md`, separate from `domain-analysis.md`.

Do not duplicate the complete test-case catalog.

A test case covering both Domain Testing and BVA keeps one shared test-case ID and is referenced from both sections.

Use `feature-testing-report-writer` for the surrounding specification, test catalog, execution evidence, and findings.

This skill documents and evaluates boundary tests. It is not responsible for independently generating a new test suite.

## 2. Required inputs

Prefer structured output from:

- `input-domain-partitioner`
- `equivalence-partitioning-generator`
- `boundary-value-generator`
- Existing Domain Testing analysis
- Shared test-case catalog
- Verified execution evidence, when available

Preserve existing:

- Requirement IDs
- Rule IDs
- Predicate definitions
- Boundary IDs (B-ID)
- Test case IDs (T-ID)
- Expected oracles
- Execution statuses

Never silently modify identifiers, predicates, expected results, or boundary values.

If inputs conflict, report the inconsistency explicitly.

If required information is missing, mark it as unresolved rather than inventing values.

## 3. Report structure

The subsections below describe information to retain, not a fixed sequence of headings. A boundary block can contain its rule, point values, Expected, case links, and feasibility together when that reads better than several tables.

Open with scope and the specification rule that creates each boundary. Organize the main body by boundary, not by separate inventories of predicates, points, explanations, and case links that repeat the same facts. No required “Đọc nhanh” or generic BVA introduction.

### 3.1. Mục tiêu và phạm vi BVA

Briefly explain:

- What behavior is being tested.
- Why boundaries are relevant.
- Which inputs and predicates contain boundaries.
- How BVA complements Domain Testing.

Avoid repeating the entire feature specification.

### 3.2. Xác định các biên kiểm thử

For each relevant predicate, record:

- Source requirement or rule.
- Predicate expression.
- Boundary value or relation.
- Valid and invalid sides.
- Inclusive or exclusive condition.
- Data type, unit, precision, and step.
- Feasibility and unresolved assumptions.

Use separate entries for lower and upper boundaries.

Do not infer an equality rule when the specification is ambiguous.

### 3.3. Phương pháp lựa chọn giá trị

Define the following at first use:

- `ON`: The value exactly at the boundary, when representable.
- `IN`: The nearest justified value on the chosen inside/accepted side of the condition.
- `OUT`: The nearest justified value on the opposite side.

State explicitly which side is called IN for **this** boundary. ON/IN/OUT labels are not a substitute for the expected behavior: show whether each point should be accepted, rejected, locked, unlocked, or unspecified. If equality, a state transition, or a two-sided valid range makes IN/OUT misleading, use “ngay dưới / tại biên / ngay trên” (or equivalent) and map the points to test cases without forcing the labels. Do not call a value “invalid” when it is a valid input that should trigger a different business outcome.

For each boundary, explain:

1. Which predicate defines the boundary.
2. Whether equality is valid or invalid.
3. Which value is selected as ON.
4. Why IN and OUT were selected.
5. What other input dimensions remain fixed.
6. Whether any point is infeasible or unobservable.

For open boundaries, ON belongs to the invalid side.

For discrete values, use valid predecessor/successor points.

For continuous values, justify representable points using the specified precision.

For time boundaries, document clock source, timezone, precision, and setup.

For text lengths, document the counting unit.

For relational boundaries, vary the target relation while maintaining feasible values for all unrelated constraints.

Discuss boundary intersections only when they represent distinct behavior or a justified fault hypothesis.

### 3.4. Bảng giá trị biên

Use one compact entry per boundary. Give its rule, threshold and inclusion, unit/step, and preparation/baseline once; then show only the meaningful points in a table such as:

`Điểm | Giá trị/trạng thái cần tạo | Expected | T-ID | Khả năng thử`

The point label may be “ngay dưới / tại biên / ngay trên” or ON/IN/OUT, whichever makes this predicate easier to read. An equality check may need a different set of points; do not force three. Every row must state its own value and expected outcome. If the case is unobservable or infeasible, write that in its row and do not invent a T-ID. Do not repeat the same facts in separate boundary inventory, point mapping, explanation, and case-link tables.

Use one row per distinct boundary obligation.

Mark missing, infeasible, or unobservable points explicitly.

Do not present unavailable points as covered.

### 3.5. Liên kết test cases

For each selected boundary test, ensure its point entry contains or links to:

- Reference the existing test-case ID.
- State which boundary point it covers.
- Explain the valid baseline for unrelated inputs.
- Reference its specification-based oracle.
- Link to the shared test-case catalog.

Keep the following in the shared catalog:

- Full preconditions and setup
- Exact input
- Test actions
- Expected result
- Observed result
- Execution evidence
- Execution status

Do not duplicate identical test cases simply because they support both Domain Testing and BVA.

Preserve all coverage claims when deduplicating. If the boundary entries already contain T-ID, baseline, and Expected, do not add a second case-link table.

### 3.6. Coverage và kết quả

Distinguish:

- `DESIGNED`: Test case exists but has not been executed.
- `PASS`: Executed and matched the expected oracle.
- `FAIL`: Executed and differed from the expected oracle.
- `BLOCKED`: Execution prevented by a known obstacle.
- `INCONCLUSIVE`: Evidence is insufficient to determine the outcome.

For coverage calculations, distinguish:

- Total identified boundary obligations.
- Feasible obligations.
- Designed obligations.
- Executed obligations.
- Uncovered obligations.
- Infeasible or unobservable obligations.

An obligation is covered by design only when linked to a concrete test case.

An obligation is covered by execution only when supported by verified execution evidence.

Execution coverage is not equivalent to pass rate.

Do not calculate percentages without a clearly defined denominator.

Suggested table:

`Coverage criterion | Total | Feasible | Designed | Executed | Uncovered | Notes`

Only include the coverage table when it adds information not already clear from the boundary mapping.

For each coverage count, name the exact point set in the denominator. Count a point as executed only if the corresponding case reached and observed that specified input/state; an observed SUT value different from the planned point does not retroactively count as executing the planned point. Mark unreachable or unobservable points separately and explain why.

## 4. Evidence requirements

Use repository test results, logs, screenshots, CI reports, or other available execution artifacts only when they provide verifiable evidence.

Never:

- Invent actual results.
- Mark unexecuted cases as PASS.
- Treat a test file as proof that its tests passed.
- Use implementation behavior to redefine a specification-based oracle.
- Claim complete coverage while obligations remain missing or unobservable.

Where evidence is unavailable, report `Not executed` or `Evidence unavailable`.

If observed behavior contradicts the specification, report the discrepancy for investigation.

## 5. Writing guidelines

Write in clear, formal Vietnamese suitable for a university Software Testing report.

Use concise analytical paragraphs.

Explain technical decisions instead of merely listing test values.

Prefer the structure:

**Requirement → Predicate → Boundary → ON/IN/OUT selection → Test case mapping → Coverage.**

Use a predicate only when it makes an inclusion rule or precision clearer than direct wording. Distinguish a **test input or prepared state**, the **expected output/state**, and the **actual output/state**. A measured wrong output (for example, a counter increment of 2 instead of 1) is a failure of the oracle; it is not automatically a test input on the other side of the boundary. Explain only genuinely tricky timing, state setup, or unavailable points.

Avoid:

- Repeating full Domain Testing analysis.
- Unnecessary theoretical explanations.
- Large redundant tables.
- Unsupported claims of completeness.
- Confusing test design with test execution.

Every boundary should be independently traceable to its source requirement.

## 6. Quality checks

Before finalizing, verify:

- Every boundary comes from a specified predicate.
- Lower and upper boundaries are considered separately.
- Inclusive and exclusive comparisons are correct.
- ON/IN/OUT values are justified using the actual input domain.
- Type, unit, and precision are documented.
- Other dimensions remain at feasible baselines.
- Boundary-to-test mappings reference real shared IDs.
- Reused Domain Testing cases are not duplicated.
- Missing and infeasible points are identified.
- Designed coverage and execution results are separated.
- PASS/FAIL claims are supported by evidence.
- Coverage totals are internally consistent.
- The report explains how boundaries were derived, not only which values were selected.
- Every table row lets the reader see the value, expected behavior, linked case, and whether that point was actually observed.

## Constraints

- Do not invent requirements, test cases, or execution evidence.
- Do not silently resolve specification ambiguity.
- Do not change previously established test identifiers.
- Do not claim that boundary coverage implies complete domain coverage.
- Do not duplicate entire test catalogs inside the BVA section.
- Prefer concise, traceable explanations over verbose repetition.
