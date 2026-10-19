---
name: equivalence-partitioning-generator
description: >
  Derive specification-based valid, invalid, and unresolved equivalence
  classes with representative test cases. Use when input domains contain
  values expected to behave alike, including field validation, business
  constraints, cross-field interactions, and state-dependent behavior.
---

# Equivalence Partitioning Generator

Partition input domains into behaviorally meaningful equivalence classes and select representative test cases.

Prioritize specification correctness, class completeness, feasibility, traceability, and minimal nonredundant test design.

Use `input-domain-partitioner` output when available. Otherwise, identify the relevant input dimensions, types, constraints, and source rules first.

## 1. Analyze input domains

For each relevant dimension:

1. Identify its source requirement or rule.
2. Define its input type and applicable domain.
3. Identify valid, invalid, and unspecified values.
4. Record constraints and dependencies.
5. Identify relevant system states or actors.
6. Determine expected behavior from the specification.

Distinguish when relevant:

- Missing or omitted values.
- Null values.
- Empty or whitespace-only values.
- Incorrect data types.
- Values outside permitted ranges.
- Values violating business rules.
- Values violating cross-field constraints.

Do not create separate classes without a meaningful rule-based distinction.

## 2. Derive equivalence classes

For each behaviorally distinct region:

1. Assign or reuse a stable class ID (`P-ID`).
2. Express class membership as an explicit predicate.
3. Identify its source requirement.
4. Classify it as `VALID`, `INVALID`, or `UNKNOWN`.
5. Define the specification-based expected behavior.
6. Determine feasibility and reachability.

Split classes when their members may produce different specified behaviors.

Do not merge classes solely because they all produce a generic success or error response if they exercise distinct specified rules.

Classify requirement confidence separately:

- `CONFIRMED`: Explicitly supported by the specification.
- `ASSUMED`: Based on a documented assumption.
- `UNRESOLVED`: Insufficient or conflicting specification.

Do not invent behavior for unresolved classes.

## 3. Validate partition quality

For each partition scheme, verify:

### Completeness

The identified classes collectively cover the relevant modeled input domain.

Document missing or unspecified regions.

### Disjointness

Classes within the same partition scheme should not overlap unintentionally.

If overlap is intentional, explain its meaning.

Cross-dimension classes may overlap when they represent different constraints or behaviors.

### Behavioral consistency

Members of a class must be expected to behave equivalently under the relevant specification rules.

Split classes when distinct outcomes, constraints, or fault hypotheses justify separation.

### Feasibility

Determine whether the class can be reached under the system's constraints and testing interface.

Distinguish:

- `FEASIBLE`
- `INFEASIBLE`
- `UNREACHABLE`
- `UNRESOLVED`

Do not report infeasible classes as executable tests.

## 4. Select representative values

For each feasible class with a reliable oracle:

1. Select a concrete representative belonging to the class.
2. Explain why the value represents the class.
3. Hold unrelated dimensions at a feasible valid baseline.
4. Avoid additional invalid inputs that could mask the target condition.
5. Establish the required actor, state, and setup.
6. Define or reference the expected oracle.
7. Assign or reuse a stable test case ID (`T-ID`).

Prefer simple, unambiguous representatives.

Use ordinary interior values for range-based equivalence classes when possible.

Delegate systematic edge selection to `boundary-value-generator`.

A representative test provides evidence for the selected input, not proof that every member of the equivalence class behaves correctly.

## 5. Handle interacting dimensions

When behavior depends on multiple inputs:

1. Identify the relevant cross-field predicates.
2. Determine feasible combinations of classes.
3. Identify combinations with distinct behavior.
4. Select representative interaction tests.
5. Keep unrelated inputs at valid baselines.
6. Document invalid or infeasible combinations.

Use `decision-table-builder` when several conditions jointly determine outcomes.

Use `state-transition-test-designer` when behavior depends on history, state, or event order.

Do not blindly generate the Cartesian product of all classes.

Add interaction tests only when they represent distinct obligations or justified fault hypotheses.

## 6. Handle interface layers

Distinguish between:

- Client-side validation.
- API/server-side validation.
- Business-domain validation.
- Persistence constraints.

When invalid input cannot pass through the UI, determine whether it can be tested at another authorized interface.

Do not treat client-side rejection as evidence that backend validation is correct.

Mark untestable or unobservable behavior explicitly.

## 7. Reuse test cases and coverage

Use the shared `test-case-catalog`.

Maintain traceability:

`Requirement → Constraint → P-ID → T-ID → Oracle → Evidence`

A single test may cover multiple classes when its inputs and oracle genuinely satisfy the respective coverage obligations.

When deduplicating:

1. Compare setup, concrete stimulus, and observations needed for all required oracle assertions.
2. Reuse the existing `T-ID` when one execution can verify both proposals; union their class and other obligation links even if those obligations differ.
3. Keep separate cases when setup, stimulus, or required observation differs materially.

Do not duplicate test cases merely because they are referenced by multiple techniques.

Use `coverage-goal-planner` for coverage targets, accounting, and residual-risk assessment.

Keep designed coverage separate from executed and passed coverage.

## 8. Output

### Equivalence class inventory

`P-ID | Dimension(s) | Predicate | Validity | Expected behavior | Source rule | Feasibility | Confidence`

### Representative test cases

`T-ID | P-ID(s) | Concrete inputs/setup | Baseline/selection rationale | Expected oracle | Coverage obligation`

### Coverage and gaps

Report:

- Identified equivalence classes.
- Feasible classes.
- Classes represented by designed tests.
- Untested feasible classes.
- Infeasible or unreachable classes.
- Unresolved requirements and oracles.
- Relevant interaction gaps.
- Deduplicated tests and retained coverage claims.

Do not claim execution coverage without verified execution evidence.

## 9. Quality gates

Before finalizing, verify:

- Every class traces to a source requirement or justified model assumption.
- Class predicates are explicit.
- Relevant input domains are covered.
- Classes do not overlap unintentionally.
- Behavioral distinctions are justified.
- Valid, invalid, and unknown classes are distinguished.
- Feasibility and reachability are checked.
- Representatives satisfy their target predicates.
- Unrelated inputs use valid baselines.
- Invalid tests avoid masking effects where possible.
- Relevant cross-field interactions are considered.
- Unspecified behavior is not silently assigned an oracle.
- Test IDs match the shared catalog.
- Coverage mappings preserve distinct obligations.
- Boundary analysis is delegated when appropriate.
- No unexecuted test is reported as passed.

## Constraints

- Do not invent business rules or expected outcomes.
- Do not infer requirements from implementation behavior.
- Do not assume input dimensions are independent.
- Do not create unnecessary Cartesian combinations.
- Do not merge behaviorally distinct classes without justification.
- Do not treat one representative as proof of an entire class.
- Do not confuse equivalence partitioning with systematic BVA.
- Do not duplicate existing test cases unnecessarily.
- Do not claim complete product correctness from equivalence class coverage alone.
