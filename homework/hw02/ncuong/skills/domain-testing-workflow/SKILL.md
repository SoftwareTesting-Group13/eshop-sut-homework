---
name: domain-testing-workflow
description: >
  Orchestrate specification-based Domain Testing and Boundary Value Analysis
  for software features, with equivalence partitions, boundary cases,
  test oracles, execution evidence, coverage, and reports.
---

# Domain Testing Workflow

Coordinate a complete, traceable, and reusable Domain Testing workflow from requirements to test evidence and reporting.

Act as the **orchestrator** of specialized testing skills. Delegate detailed analysis to the appropriate skills instead of duplicating their responsibilities.

Prioritize specification correctness, meaningful coverage, execution safety, and evidence-backed conclusions.

Follow the user's course methodology, terminology, and deliverable requirements when provided.

## 0. Required HW02 entry sequence

Before opening specialized skills or inspecting SUT implementation, read these three files from the repository root, in order:

1. `README.md` — authoritative business rules and expected behavior.
2. `api_specification.md` — project API contract; read it even if the selected feature is exercised through a UI or mobile app.
3. `homework/hw02/docs/2026.HW02.Domain Testing_En.md` — HW02 scope, EP/BVA method, and deliverables.

Then scan the repository at a structural level (for example with `rg --files`) to locate applications, the target feature, interfaces, test setup, and existing artifacts. Do not inspect implementation in depth or run the SUT during this scan. Only after these steps, open the other skills and targeted source files. If this orchestrator skill was opened before the three documents, complete this entry sequence immediately before continuing.

Use the root README for business-rule oracles, the API specification for endpoint contracts, and the assignment for submission scope. Record discrepancies as `UNRESOLVED` with affected cases/oracles; do not silently choose the SUT's current behavior. If a required document is unavailable, identify it and hold work that depends on it rather than inventing requirements.

## 1. Terminology and completeness

For HW02, derive the submitted test suite with the two techniques required by the assignment:

- Domain modeling and constraint analysis.
- Equivalence Partitioning (EP) for Domain Testing.
- Boundary Value Analysis (BVA).

Decision tables and state models may clarify a feature's rules or test setup, but do not create a third test suite or claim separate technique coverage unless the user requests it. A browser may be used to execute an EP/BVA case when that is the relevant interface; rendered UI attributes, layout, language, and navigation checks are not automatically in scope.

**Completeness means covering the relevant equivalence classes and meaningful boundaries with traceable cases, not adding unrelated validation categories.**

When the deliverable requires both Domain Testing and BVA:

- Produce a separate Domain Testing section.
- Produce a separate BVA section.
- If no meaningful boundary exists, explicitly document why BVA is not applicable.
- Share test cases through one catalog.

Keep decision tables and state models conditional on feature behavior.

## 2. Phase 1 — Requirement discovery

Establish:

1. Feature and operation under test.
2. Authoritative specifications and acceptance criteria.
3. Included and excluded requirements.
4. Input types, business rules, and constraints.
5. Actors, permissions, prior states, and dependencies.
6. Testing environment and available tools.

Assign or preserve stable requirement and rule IDs.

Classify requirement information as:

- `CONFIRMED`: Explicitly specified.
- `ASSUMED`: Necessary documented assumption.
- `UNRESOLVED`: Missing, conflicting, or ambiguous.

Do not infer normative requirements from SUT implementation.

**Gate:** Every scoped requirement is traceable or explicitly unresolved.

## 3. Phase 2 — Domain modeling

Use `input-domain-partitioner` to identify:

- Input dimensions and types.
- Valid and invalid domains.
- Predicates and constraints.
- Cross-field dependencies.
- Relevant system states.
- Feasible and infeasible regions.

Use `equivalence-partitioning-generator` to derive behaviorally distinct equivalence classes.

Preserve source rules, class IDs, predicates, and feasibility.

Do not create exhaustive Cartesian combinations without a distinct testing purpose.

**Gate:** Every scoped rule has a corresponding model element or documented exclusion.

## 4. Phase 3 — Test design

### Equivalence Partitioning

Select representative cases for feasible classes.

Ensure unrelated invalid inputs do not mask the target behavior.

### Boundary Value Analysis

Use `boundary-value-generator` for predicates with meaningful edges.

Identify:

- Boundary inclusion or exclusion.
- ON/IN/OUT points.
- Data type, unit, and precision.
- Feasible baselines.
- Relevant boundary intersections.

Do not apply arbitrary `±1` values to continuous or nonnumeric domains.

### Decision Table Testing

Use `decision-table-builder` when multiple conditions jointly determine behavior.

Identify feasible rules, actions, conflicts, and unspecified combinations.

### State Transition Testing

Use `state-transition-test-designer` when behavior depends on state, prior actions, actor, or event order.

Identify states, events, transitions, guards, and invalid transitions.

### Test oracles

Use `test-oracle-writer` to define observable expected behavior.

Every selected test must have:

- Source requirement.
- Target coverage obligation.
- Preconditions and setup.
- Concrete input.
- Action or event.
- Expected oracle.
- Feasibility status.

If the specification does not establish an oracle, mark it unresolved.

**Gate:** Every selected test has a justified coverage purpose and a valid oracle, or an explicitly documented gap.

## 5. Phase 4 — Shared test catalog

Maintain one authoritative `test-case-catalog`.

Use the traceability contract:

`Requirement → Predicate/Constraint → Class/Boundary/Rule/Transition → T-ID → Oracle → Evidence`

Preserve stable identifiers:

- `R-ID`: Requirement or rule.
- `RG-ID`: Candidate domain region.
- `C-ID`: Constraint.
- `DC-ID`: Decision-table condition.
- `P-ID`: Equivalence partition.
- `B-ID`: Boundary.
- `DR-ID`: Decision rule.
- `TR-ID`: Transition.
- `T-ID`: Test case.

A single test may cover multiple obligations.

Preserve IDs already used in existing artifacts; when an older artifact uses a different prefix, label its object type explicitly and map it to the shared namespace instead of silently renumbering it.

Do not duplicate test cases across Domain Testing, BVA, decision tables, or reports.

Keep test design separate from observed execution results.

## 6. Phase 5 — Coverage planning

Use `coverage-goal-planner` to:

1. Select applicable coverage criteria.
2. Enumerate coverage obligations.
3. Define explicit denominators.
4. Set justified coverage goals.
5. Map obligations to test IDs.
6. Identify missing or infeasible obligations.

Track separately:

- Designed coverage.
- Executed coverage.
- Passed coverage.
- Blocked or unresolved obligations.
- Residual risks.

Coverage is counted by obligations, not raw test-case quantity.

Do not infer code coverage without appropriate instrumentation.

**Gate:** All selected coverage criteria have defined obligations and traceability.

## 7. Phase 6 — Safe execution

Execute tests when execution is within the requested scope and an authorized, suitable environment is available.

For a full testing request, prefer actual execution over source-code inspection alone.

Before execution:

1. Identify the SUT and environment.
2. Verify that the target is not an unauthorized or production environment.
3. Identify persistent data and external side effects.
4. Confirm that test operations can be isolated or safely restored.
5. Record the initial state and execution configuration.
6. Establish evidence collection and cleanup procedures.

Do not run destructive tests against working or production data without explicit authorization and a verified recovery plan.

### Execution methods

- API: Send real HTTP requests to the test SUT.
- Browser: use automation only when an in-scope EP/BVA case must be executed through the UI.
- State-dependent tests: Establish required states before execution.
- Database tests: Use isolated fixtures or test databases.
- External integrations: Use sandbox services or controlled mocks where appropriate.

Use test oracles derived from specifications.

Record:

- T-ID.
- Environment and setup.
- Actual result.
- PASS/FAIL/BLOCKED/INCONCLUSIVE status.
- Execution timestamp or run ID.
- Evidence reference.
- Related defect ID, when applicable.

Do not treat source-code inspection as execution.

Do not fabricate logs, screenshots, or observed outcomes.

If safe execution is unavailable, stop execution and report the blocker while preserving completed test-design artifacts.

## 8. Database isolation and cleanup

Prefer an isolated application and test database.

Before execution:

- Identify the working database.
- Record its initial state.
- Create a separate test environment.
- Seed deterministic fixtures.
- Track all resources created by the workflow.

Reset state between tests when isolation is necessary for reliable results.

For SQLite, use a transactionally consistent backup method or stop writers before copying database files, accounting for WAL/SHM when applicable.

For external stateful systems, account for caches, queues, files, notifications, and other side effects.

### Cleanup requirements

Use a `finally`-style cleanup path where supported.

After testing:

1. Persist required evidence and reports.
2. Stop only services started or owned by this workflow.
3. Remove only explicitly identified test-owned temporary resources.
4. Restore shared resources only through an authorized, verified recovery procedure.
5. Verify the working environment and database state.
6. Record cleanup status.

Never automatically:

- Delete user-owned databases.
- Stop unrelated services.
- Overwrite existing user changes.
- Run `git restore` to discard pre-existing modifications.
- Claim restoration without verification.

A working-tree check alone does not prove database integrity.

If cleanup or restoration cannot be verified, report `CLEANUP_UNVERIFIED` and identify remaining resources or risks.

## 9. Phase 7 — Coverage assessment

After execution, rerun `coverage-goal-planner` to evaluate actual evidence.

Compare:

- Planned goals.
- Designed obligations.
- Executed obligations.
- Passing and failing evidence.
- Uncovered obligations.
- Remaining risks.

Classify goals as:

- `GOAL_MET`.
- `GOAL_NOT_MET`.
- `UNDETERMINED`.

Never silently exclude blocked cases to improve coverage percentages.

Do not equate coverage achievement with defect-free software.

## 10. Phase 8 — Reporting

Use:

- `domain-testing-report-writer` for Domain Testing.
- `boundary-value-report-writer` for BVA.
- `feature-testing-report-writer` for the four files in `features/<FEATURE_CODE>/`.
- `testing-report-assembler` for multi-feature summaries.

The full report should include:

1. Scope and requirement references.
2. Domain model and constraints.
3. Equivalence classes and representative tests.
4. Boundary analysis and ON/IN/OUT selection.
5. Decision/state analysis when applicable.
6. Shared test-case catalog.
7. Coverage goals and assessment.
8. Execution evidence and findings.
9. Limitations and residual risks.
10. Environment cleanup verification.

Keep Domain Testing and BVA as distinct method sections when required.

Do not duplicate test cases or invent missing evidence.

## 11. Final review

Before handoff, verify:

- All scoped requirements are modeled or explicitly excluded.
- Applicable techniques were considered.
- Valid, invalid, and unresolved regions are distinguished.
- Boundary inclusion and precision are correct.
- Interacting predicates and states are modeled when relevant.
- Every selected test has a source rule and observable oracle.
- Test IDs are stable across all artifacts.
- The shared catalog contains no unnecessary duplicates.
- Coverage metrics use consistent denominators.
- Designed and executed results are clearly separated.
- Pass/fail claims have supporting evidence.
- Unsafe or unavailable execution is explicitly reported.
- Cleanup status has been verified or marked unresolved.
- Reports agree with the authoritative test catalog.

## 12. Final deliverables

Produce:

- Domain model and constraints.
- Partition and boundary inventories.
- Decision/state models when applicable.
- Shared test-case catalog.
- Traceability and coverage assessment.
- Execution results and evidence, when performed.
- Findings and unresolved requirements.
- Cleanup verification, when execution modified resources.
- Final feature-testing report when requested.

Adapt depth to feature complexity without omitting relevant obligations.

## Constraints

- Do not invent requirements or expected outcomes.
- Do not infer normative behavior from implementation.
- Do not generate unnecessary testing techniques.
- Do not claim unexecuted tests have passed.
- Do not run unsafe or unauthorized destructive tests.
- Do not modify or remove user-owned data during automatic cleanup.
- Do not hide incomplete coverage or unresolved assumptions.
- Do not substitute report generation for real execution.
- Do not claim total product correctness from Domain Testing coverage.
