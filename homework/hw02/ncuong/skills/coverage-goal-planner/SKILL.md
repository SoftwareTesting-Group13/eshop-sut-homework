---
name: coverage-goal-planner
description: >
  Plan, measure, and assess evidence-based test coverage goals for Domain
  Testing and other test models. Use when choosing coverage criteria,
  identifying obligations, calculating designed/executed coverage,
  evaluating gaps, or defining test completion criteria.
---

# Coverage Goal Planner

Define measurable coverage goals and evaluate test coverage against explicit model-based obligations.

Prioritize traceability, accurate accounting, risk, and evidence over raw test-case counts.

Do not interpret coverage percentages as proof of overall software correctness.

## 1. Establish scope

Identify:

- Feature or component under test.
- Source requirements and model version.
- Testing techniques in scope.
- Relevant business and technical risks.
- Available test budget or constraints.
- Existing test-case catalog and execution evidence.

Distinguish planning from assessment.

If the coverage model is incomplete or ambiguous, identify the gap before calculating coverage.

## 2. Select coverage criteria

Choose criteria that match the test model and risk.

For HW02, report Equivalence Partitioning and BVA coverage as the primary technique coverage. Decision-rule and state-transition models can support explanation of the domain; do not add them as separate coverage goals solely because their supporting skills were used.

### Domain-based criteria

- Equivalence class coverage.
- Boundary point coverage (ON/IN/OUT).
- Boundary-side coverage.
- Feasible decision rule coverage.
- Reachable state transition coverage.
- Relevant boundary intersection coverage.

Only include criteria supported by the selected test technique and available model.

### Structural criteria (optional)

- Statement coverage.
- Branch coverage.
- Condition coverage.
- Path coverage.
- MC/DC coverage.

For structural criteria, require source-code analysis or instrumentation evidence.

Never infer structural coverage from a test-case catalog.

## 3. Define coverage obligations

For each selected criterion:

1. Enumerate individual coverage obligations.
2. Assign stable obligation IDs.
3. Link obligations to source requirements or model elements.
4. Record feasibility and scope.
5. Document exclusions and supporting rationale.
6. Identify dependencies or overlapping obligations.

Use a consistent status:

- `ELIGIBLE`: In scope and feasible.
- `INFEASIBLE`: Cannot be satisfied under valid model constraints.
- `UNREACHABLE`: Cannot be reached under the stated system model.
- `OUT_OF_SCOPE`: Explicitly excluded by agreed scope.
- `UNRESOLVED`: Feasibility or applicability is not established.

Do not silently exclude obligations.

Do not exclude temporarily blocked tests from the denominator.

## 4. Define coverage goals

For each criterion, specify:

- Target coverage.
- Coverage denominator.
- Risk-based justification.
- Required evidence.
- Completion or exit conditions.

Do not automatically assume every criterion requires 100%.

If no target is provided, propose a justified target and mark it as proposed rather than approved.

Coverage goals should reflect:

- Requirement criticality.
- Boundary and validation risks.
- Test feasibility.
- Available resources.
- Assignment or project requirements.

## 5. Map obligations to test cases

Create traceability links:

`Requirement/Rule → Obligation → T-ID → Oracle → Execution Evidence`

Use the shared `test-case-catalog`.

A test case may satisfy multiple obligations.

An obligation may be linked to multiple test cases.

Preserve all valid coverage relationships without duplicating test cases.

Do not count a mapped test as executed unless execution evidence exists.

When API and UI exercise one obligation, keep interface execution status alongside the mapping: API evidence covers only the API attempt, UI evidence only the UI attempt. Report route gaps separately from the EP/BVA denominator; do not create a third technique metric or count the same case twice because it has two routes.

## 6. Evaluate coverage

Track separately:

- `DESIGNED`: Obligation has at least one valid designed test.
- `EXECUTED`: Obligation has at least one qualifying executed test with an observed result.
- `PASSED`: Obligation has qualifying execution evidence satisfying the oracle.
- `FAILED`: Relevant execution evidence contradicts the oracle.
- `BLOCKED`: Required execution cannot proceed.
- `UNCOVERED`: No qualifying test satisfies the coverage obligation.
- `INCONCLUSIVE`: Evidence is missing or insufficient.

Keep test-run status separate from obligation status when multiple tests map to the same obligation.

A failed execution may contribute to executed coverage but not passed coverage.

Do not treat test design as evidence of successful execution.

### Coverage calculations

For each criterion:

`Eligible = Total - justified exclusions`

`Designed coverage = Designed eligible obligations / Eligible`

`Executed coverage = Executed eligible obligations / Eligible`

`Passed coverage = Eligible obligations with sufficient passing evidence / Eligible`

Define how multiple linked tests and conflicting results are handled before calculating passed coverage.

Do not combine percentages from different criteria into a single metric without an explicitly justified method.

If the denominator is zero or unresolved, report coverage as `N/A` or `UNDETERMINED` rather than 100%.

## 7. Analyze gaps and residual risk

For uncovered or insufficiently evidenced obligations:

1. Identify the missing obligation.
2. Explain its risk or fault hypothesis.
3. Determine whether an existing test can cover it.
4. Propose a new test only when it adds distinct coverage.
5. Record feasibility, priority, and any dependency.

Separate:

- Coverage gaps.
- Execution gaps.
- Unresolved model assumptions.
- Out-of-scope residual risks.

Avoid exhaustive combinations without a risk-based justification.

## 8. Assess completion

Evaluate each criterion against its stated target.

Use one of:

- `GOAL_MET`: The specified coverage target and exit conditions are satisfied.
- `GOAL_NOT_MET`: The goal is measurable but not satisfied.
- `UNDETERMINED`: Insufficient model or execution evidence exists.

State whether the assessment concerns designed coverage, executed coverage, or passed coverage.

Do not claim a feature is defect-free or production-ready solely because coverage goals are met.

## 9. Output

### Coverage plan

`Criterion | Goal | Obligation IDs | Denominator | Justification | Required evidence`

### Coverage assessment

`Criterion | Eligible | Designed | Executed | Passed | Exclusions | Gaps | Goal status`

### Traceability

`Requirement/Model ID | Obligation ID | T-ID | Oracle | Evidence | Status`

### Residual risk

`Gap ID | Missing obligation | Risk | Proposed action | Priority`

Keep the output concise and consistent with the shared test-case catalog.

## 10. Quality gates

Before finalizing, verify:

- Each criterion matches the model and testing technique.
- Every denominator is explicitly defined.
- Obligations have stable IDs and traceable sources.
- Exclusions are justified and visible.
- Blocked tests are not silently removed from scope.
- Coverage metrics count obligations, not test cases.
- Designed, executed, and passed coverage are distinct.
- Multiple mappings do not inflate coverage.
- Pass/fail claims rely on observed evidence.
- Structural coverage uses valid instrumentation or analysis.
- Unresolved obligations are not treated as covered.
- Coverage gaps and residual risks are reported.
- Goal achievement is not equated with overall correctness.

## Constraints

- Do not invent coverage evidence.
- Do not fabricate test execution results.
- Do not silently reduce coverage targets.
- Do not exclude difficult obligations merely to increase coverage.
- Do not infer source-code coverage from black-box tests.
- Do not create redundant tests without distinct coverage value.
- Do not claim complete product correctness from model-specific coverage.
