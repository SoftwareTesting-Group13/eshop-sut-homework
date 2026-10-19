---
name: boundary-value-generator
description: >
  Generate specification-based boundary value tests from numeric, length,
  count, temporal, and relational predicates. Use when requirements contain
  thresholds, ranges, inclusive/exclusive limits, or behavior changes at
  domain boundaries. Supports Domain Testing and Boundary Value Analysis.
---

# Boundary Value Generator

Generate boundary-focused test cases from explicit specification predicates.

Prioritize correctness, traceability, feasibility, and observable expected results over test case quantity.

Use outputs from `input-domain-partitioner` or `equivalence-partitioning-generator` when available.

## 1. Analyze requirements

For each relevant rule:

1. Identify the requirement ID and source.
2. Translate the rule into explicit predicates.
3. Identify valid and invalid partitions.
4. Determine whether each bound is inclusive or exclusive.
5. Record input type, units, precision, and representable values.
6. Identify unspecified or ambiguous behavior.

Classify each predicate:

- `CONFIRMED`: Explicitly supported by specification.
- `ASSUMED`: Requires a documented assumption.
- `UNRESOLVED`: Insufficient information to derive a reliable oracle.

Never silently resolve ambiguous requirements.

## 2. Identify boundaries

For each predicate, determine:

- Boundary location and valid side.
- Lower or upper boundary.
- Inclusive or exclusive comparison.
- Discrete or continuous domain.
- Smallest meaningful representable step, if applicable.

Generate:

- `ON`: Exactly at the boundary, when representable.
- `IN`: Closest justified point on the chosen inside/accepted side; state which side that is for this predicate.
- `OUT`: Closest justified point on the opposite side.

For a behavior threshold, both sides may be valid inputs with different expected outcomes (for example, unlocked versus locked). Name the outcomes on both sides; do not call one side invalid merely because its behavior changes. If ON/IN/OUT obscures an equality condition or state transition, record the nearest feasible points as below/at/above the threshold instead.

For exclusive bounds, `ON` is invalid.

For discrete domains, use the immediate predecessor or successor.

For continuous domains, use justified representable values rather than an arbitrary universal epsilon.

Do not invent boundary values for unbounded domains.

## 3. Handle special domains

### Numeric

Consider zero, negative values, integer limits, precision, rounding, and overflow only when relevant to the specification or input representation.

### String and collection

Identify whether length means bytes, Unicode code points, grapheme clusters, UTF-16 code units, or collection elements.

Distinguish empty, null, missing, and whitespace-only values when their behavior differs.

### Temporal

Specify timezone, clock source, precision, inclusivity, and deterministic test setup.

Consider calendar rollover, daylight saving transitions, expiration, and concurrent timing only when relevant.

### Relational

For predicates such as `x <= y`, vary one dimension while holding the other at a feasible baseline.

Test boundary intersections when they involve coupled constraints or distinct expected behavior.

### Input representation

Keep type validation, serialization, and parsing boundaries separate from business-domain boundaries.

## 4. Generate test cases

1. Select a feasible, valid baseline satisfying all unrelated constraints.
2. Vary one target dimension at a time.
3. Generate ON, IN, and OUT cases for each applicable boundary.
4. Add relevant interactions only when justified by constraints, risk, or distinct behavior.
5. Include negative and off-by-one cases where the interface can accept them.
6. Avoid exhaustive Cartesian combinations without explicit justification.
7. Mark infeasible or unobservable cases instead of claiming coverage.

## 5. Define expected results

Derive expected behavior strictly from the specification.

Each test must include an observable oracle such as:

- HTTP status and response contract.
- State transition.
- Persisted data.
- Validation error.
- Observable side effect.

Do not use implementation behavior as the expected oracle.

For `ASSUMED` or `UNRESOLVED` rules, clearly mark the oracle as provisional or undefined. Do not present such tests as confirmed specification-based passes.

## 6. Output

### Boundary inventory

`B-ID | Requirement ID | Predicate | Boundary/inclusion | Type/step | ON/IN/OUT | Baseline/setup | Expected behavior | Feasibility | Confidence`

For every selected point, state its concrete value or prepared state, expected behavior, and linked T-ID. Keep the planned input/state distinct from the Actual measured after running it.

### Test cases

`T-ID | B-ID | Requirement ID | Input/setup | Expected oracle | Test level | Priority | Coverage claim`

Use stable identifiers and link every test to its source rule and boundary.

### Coverage summary

Report:

- Boundaries discovered.
- ON/IN/OUT points covered.
- Missing or infeasible boundary points.
- Ambiguous or assumed requirements.
- Deduplicated tests and retained coverage references.
- Relevant interaction boundaries not covered.

## 7. Quality gates

Before finalizing, verify:

- Every relevant predicate has an identified boundary.
- Both sides of each boundary are covered or explicitly justified as unreachable.
- Inclusive and exclusive conditions are handled correctly.
- Numeric precision and type constraints are respected.
- Unrelated inputs remain at feasible baselines.
- Expected results are specification-based.
- Unresolved requirements are not silently assumed.
- No redundant Cartesian explosion is introduced.
- Each selected test has traceable boundary coverage.
- No infeasible or unobservable case is reported as covered.

## Constraints

- Do not invent business rules.
- Do not infer expected results from existing implementation bugs.
- Do not claim unexecuted tests have passed.
- Do not confuse boundary coverage with complete domain coverage.
- Prefer a minimal, defensible test suite over a large redundant suite.
