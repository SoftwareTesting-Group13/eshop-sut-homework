---
name: input-domain-partitioner
description: >
  Build specification-based input domain models for Domain Testing.
  Identify input dimensions, types, valid and invalid domains,
  predicates, constraints, dependencies, feasibility, and candidate
  regions. Use before equivalence partitioning, boundary analysis,
  decision tables, or representative test generation.
---

# Input Domain Partitioner

Transform feature requirements into a structured, testable input domain model.

Prioritize specification correctness, complete constraint identification, feasibility, and traceability.

**This skill models the input space. It does not generate concrete test cases or select boundary points.**

Delegate representative selection to `equivalence-partitioning-generator` and boundary analysis to `boundary-value-generator`.

## 1. Identify operation and scope

Determine:

1. Feature or operation under test.
2. Authoritative requirements and source rules.
3. Observable operations and outcomes.
4. Inputs that influence behavior.
5. Relevant actors, roles, prior states, environment, and time.
6. Known assumptions and specification gaps.

Distinguish:

- `INPUT`: Values directly supplied to the operation.
- `STATE`: Existing system state affecting behavior.
- `CONTEXT`: Actor, permission, environment, or time.
- `OBSERVATION`: Outputs or side effects used to evaluate behavior.

Assign stable dimension IDs (`D-ID`).

Do not infer normative requirements from implementation behavior.

## 2. Define input dimensions

For each dimension, record:

- ID and name.
- Type and representation.
- Granularity, units, and precision.
- Input domain.
- Business-valid domain.
- Default behavior.
- Optional or required status.
- Null and omitted behavior.
- Source requirement.
- Controllability and reachability.

Distinguish:

### Input domain

Values that can be represented or submitted through the tested interface.

### Valid domain

Values satisfying applicable specification constraints.

### Invalid domain

Values violating one or more specified constraints.

### Unknown domain

Values whose validity or expected behavior is not established by the specification.

Consider when relevant:

- Missing or omitted inputs.
- Explicit `null`.
- Empty strings and collections.
- Whitespace-only values.
- Incorrect data types.
- Malformed representations.
- Out-of-range values.
- Unsupported enum values.
- Encoding and precision differences.

Do not automatically treat unknown values as invalid.

## 3. Extract constraints

Translate each relevant requirement into an explicit predicate.

Assign stable constraint IDs (`C-ID`).

For each constraint, record:

1. Predicate expression.
2. Source rule.
3. Affected dimensions.
4. Valid and invalid conditions.
5. Inclusion or exclusion of equality.
6. Constraint category.
7. Specification confidence.

### Constraint categories

- `SINGLE_FIELD`: Restricts one input.
- `CROSS_FIELD`: Relates multiple inputs.
- `CONDITIONAL`: Applies only when a condition holds.
- `STATE_DEPENDENT`: Depends on prior system state.
- `ACTOR_DEPENDENT`: Depends on role or permission.
- `TEMPORAL`: Depends on time or event order.
- `UNIQUENESS`: Depends on existing data.

Express conditional constraints using explicit logical conditions.

For example:

`C1: quantity >= 1`

`C2: quantity <= available_stock`

`C3: discount_applied => coupon_is_valid`

Preserve distinctions between strict and non-strict comparisons.

Never invent thresholds, equality rules, or conditional behavior.

## 4. Validate constraint consistency

Review the constraint model for:

- Contradictory predicates.
- Missing dependencies.
- Ambiguous conditions.
- Conflicting source rules.
- Impossible combinations.
- Unspecified behavior.
- Unreachable states.

Classify specification confidence:

- `CONFIRMED`: Explicitly supported by authoritative requirements.
- `ASSUMED`: Based on a documented assumption.
- `UNRESOLVED`: Missing, ambiguous, or conflicting specification.

Do not silently resolve conflicting requirements.

Record which rule or clarification would resolve each uncertainty.

## 5. Identify candidate domain regions

Derive candidate regions from predicates and expected behavioral distinctions.

For each region:

1. Assign or reuse a stable region ID (`RG-ID`); reserve `R-ID` for requirements and rules.
2. Define membership using logical predicates.
3. Identify the relevant constraints.
4. Classify validity.
5. Assess feasibility and reachability.
6. Explain the behaviorally relevant distinction.
7. Link source requirements.

### Validity

- `VALID`: Satisfies the applicable specification rules.
- `INVALID`: Violates at least one applicable rule.
- `UNKNOWN`: Validity cannot be established.

### Feasibility

- `FEASIBLE`: A concrete input and setup can satisfy the region.
- `INFEASIBLE`: The region contradicts established constraints.
- `UNREACHABLE`: The region cannot be reached through the scoped interface or state model.
- `UNRESOLVED`: Feasibility is not established.

**Validity and feasibility are independent classifications.**

An invalid region may still be feasible and important to test.

Do not confuse an invalid business input with an impossible input combination.

## 6. Analyze interactions

Identify dependencies between dimensions.

Check whether:

- Individually valid values form an invalid combination.
- A conditional rule activates additional constraints.
- Existing state changes input validity.
- Actor or permission changes allowed operations.
- Time affects eligibility or expiration.
- Constraints intersect or contradict one another.

Document relevant intersections when they create distinct behavior or testing obligations.

Do not blindly enumerate the Cartesian product of all dimensions.

Use `decision-table-builder` when several conditions jointly determine outcomes.

Use `state-transition-test-designer` when behavior depends on state history or event order.

## 7. Validate region quality

### Completeness

Check whether candidate regions account for all relevant stated rules and input dimensions.

Document uncovered or unspecified portions of the domain.

### Consistency

Ensure region predicates do not contradict their assigned validity.

### Overlap

Identify overlapping regions.

Distinguish intentional cross-dimension intersections from accidental overlap within one partition scheme.

### Feasibility

Verify whether the defining predicates can be satisfied simultaneously.

Do not claim feasibility without a defensible model or concrete witness when one is needed.

### Behavioral distinction

Explain which specified rule or expected behavior makes each region meaningful.

Do not create arbitrary regions based solely on sample values.

## 8. Preserve traceability

Maintain:

`Source Requirement/R-ID → D-ID → C-ID → RG-ID`

Reuse existing identifiers when available.

If existing artifacts use an ID namespace differently, preserve those identifiers, label their object type, and map them to the shared namespace rather than silently renumbering them.

Pass the model to:

- `equivalence-partitioning-generator`
- `boundary-value-generator`
- `decision-table-builder`
- `state-transition-test-designer`
- `coverage-goal-planner`

Do not assign concrete test IDs unless they already exist in an authoritative shared artifact.

## 9. Output

### Input dimensions

`D-ID | Input/State | Category | Type/Precision | Input Domain | Valid Domain | Default/Null | Source`

### Constraints

`C-ID | Predicate | Category | Affected D-IDs | Source Rule | Confidence`

### Candidate regions

`RG-ID | Defining Predicates | Validity | Feasibility | Relevant Constraints | Rationale`

### Constraint dependencies

`C-ID | Dependent Dimensions | Interaction | Affected Regions`

### Open questions

`Q-ID | Missing/Ambiguous Rule | Affected Dimensions/Regions | Required Clarification`

Keep tables compact and avoid repeating identical information.

## 10. Quality gates

Before finalizing, verify:

- Every scoped input and relevant state is identified.
- Input and business-valid domains are distinguished.
- Data types, units, and precision are recorded.
- Missing, null, empty, malformed, and out-of-range values are considered when relevant.
- Every constraint traces to a source rule.
- Cross-field and conditional dependencies are identified.
- Equality and boundary inclusion are not invented.
- Contradictory requirements remain visible.
- Candidate regions have explicit predicates.
- Validity and feasibility are evaluated separately.
- Relevant intersections are considered.
- Accidental overlaps are identified.
- Infeasible and unreachable regions are not confused.
- Unresolved behavior is not silently classified.
- Model completeness claims are justified.
- Identifiers remain stable across downstream artifacts.

## Constraints

- Do not invent requirements or expected outcomes.
- Do not infer specifications from observed SUT behavior.
- Do not silently resolve missing or conflicting rules.
- Do not assume input dimensions are independent.
- Do not generate unnecessary Cartesian combinations.
- Do not classify unknown behavior as automatically invalid.
- Do not confuse invalid regions with infeasible regions.
- Do not select representative test values.
- Do not generate ON/IN/OUT boundary tests.
- Do not claim complete domain coverage while interactions remain unresolved.
- Keep the model reusable, minimal, and traceable.
