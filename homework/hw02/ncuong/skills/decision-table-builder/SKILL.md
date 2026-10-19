---
name: decision-table-builder
description: >
  Build specification-based decision tables from combinations of boolean,
  categorical, state, and actor conditions. Use when outcomes depend on
  multiple interacting conditions, business rules, permissions, or states.
  Identify feasible rules, conflicts, missing outcomes, and test coverage.
---

# Decision Table Builder

Transform interacting conditions and business rules into traceable decision tables and test cases.

Prioritize specification correctness, rule completeness, feasibility, and observable outcomes over exhaustive combinations.

A decision table models specified behavior. Never invent outcomes for unspecified combinations.

## 1. Analyze conditions

For each condition:

1. Identify its source requirement or rule.
2. Assign a stable decision-condition ID (`DC-ID`); reserve `C-ID` for domain constraints. Link a condition to its source `C-ID` when applicable.
3. Define possible values and data types.
4. Identify dependencies and constraints.
5. Include actor, permission, state, or prior action when they affect the decision.

For each action or outcome:

- Assign an action ID (`A-ID`).
- Define expected behavior from the specification.
- Identify observable results or state changes.

Do not assume conditions are independent.

## 2. Construct decision rules

1. Enumerate feasible condition combinations.
2. Apply known constraints to eliminate impossible combinations.
3. Identify outcomes for each feasible combination.
4. Assign stable decision rule IDs (`DR-ID`).
5. Preserve requirement traceability.

Classify combinations as:

- `DEFINED`: Feasible with a specified outcome.
- `UNSPECIFIED`: Feasible but expected behavior is unknown.
- `INFEASIBLE`: Violates known constraints.
- `CONFLICTING`: Multiple applicable rules specify incompatible outcomes.
- `UNRESOLVED`: Feasibility or applicability cannot be determined.

Never treat unspecified behavior as automatically invalid.

For large condition spaces, use constraints and incremental construction instead of blindly generating every combination.

## 3. Validate rule consistency

Check for:

- Missing feasible combinations.
- Conflicting outcomes.
- Overlapping rules.
- Duplicate rules.
- Undefined rule precedence.
- Contradictory conditions.

When multiple rules match an input, apply precedence only if explicitly defined by the specification.

Otherwise, report the ambiguity.

Do not silently resolve conflicting business rules.

## 4. Simplify decision tables

Collapse rules using don't-care (`-`) only when changing the omitted condition cannot affect the outcome under the stated constraints.

Before collapsing:

1. Verify equivalent outcomes.
2. Verify condition independence for the proposed group.
3. Preserve original rule IDs.
4. Record the reason for simplification.
5. Ensure no feasible combination with different behavior is hidden.

Do not use don't-care to conceal unknown, conflicting, or unexamined combinations.

## 5. Generate test cases

For each feasible rule with a defined outcome:

1. Select concrete values satisfying its conditions.
2. Use equivalence classes and boundary points where appropriate.
3. Maintain valid baselines for unrelated inputs.
4. Include required actors, states, and setup.
5. Define an observable specification-based oracle.
6. Assign or reuse a stable test case ID (`T-ID`).
7. Link the test to its decision rule IDs.

A test may cover multiple rules only when the coverage claim is justified.

Avoid redundant tests that do not provide additional coverage or fault-detection value.

Keep test execution results separate from test design.

## 6. Coverage and traceability

Define one coverage obligation per feasible, specified decision rule, or per justified collapsed rule group when the chosen criterion permits it.

Maintain:

`Requirement → C-ID (when applicable) → DC-ID → DR-ID → T-ID → Oracle → Evidence`

Track separately:

- Rules identified.
- Feasible rules with specified outcomes.
- Rules covered by designed tests.
- Rules supported by execution evidence.
- Uncovered rules.
- Infeasible and unresolved combinations.

Preserve original rule IDs when reporting coverage for collapsed groups.

Do not count infeasible combinations as uncovered executable rules.

Do not exclude unresolved feasible combinations without documenting the gap.

Use `coverage-goal-planner` for coverage targets, percentages, and residual-risk assessment.

## 7. Output

### Conditions and actions

`DC-ID | Condition | Possible values | Source C-ID/constraints | Source rule`

`A-ID | Action/Outcome | Observable behavior | Source rule`

### Decision table

`DR-ID | Condition values | Action/Outcome | Classification | Source`

### Simplification

`Collapsed group | Original DR-IDs | Don't-care conditions | Justification`

### Test cases

`T-ID | DR-ID(s) | Concrete inputs/setup | Expected oracle | Coverage obligation`

### Completeness

Report:

- Defined feasible rules.
- Unspecified combinations.
- Conflicting rules.
- Infeasible combinations.
- Intentionally collapsed rules.
- Missing test coverage.
- Unresolved assumptions.

Use the shared `test-case-catalog` rather than duplicating existing test cases.

## 8. Quality gates

Before finalizing, verify:

- All conditions originate from requirements or justified model assumptions.
- Condition dependencies and feasibility constraints are respected.
- Every defined feasible rule has a test or documented exclusion.
- Every generated test has an observable oracle.
- Conflicting and unspecified outcomes remain visible.
- Rule precedence is not invented.
- Don't-care simplification is justified and traceable.
- Simplification preserves defined behavior.
- Tests do not contain unrelated invalid inputs that mask the target rule.
- Coverage uses rule obligations rather than raw test counts.
- Designed and executed coverage remain separate.
- No test is reported as passed without execution evidence.

## Constraints

- Do not invent business rules or expected outcomes.
- Do not silently resolve conflicting requirements.
- Do not assume all conditions are independent.
- Do not blindly enumerate large Cartesian products.
- Do not collapse rules without proving outcome equivalence.
- Do not duplicate existing test cases unnecessarily.
- Do not infer successful execution from generated tests.
- Do not claim complete product correctness from decision-rule coverage alone.
