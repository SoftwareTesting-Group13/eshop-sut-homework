---
name: state-transition-test-designer
description: >
  Design specification-based state transition tests for stateful features.
  Model states, events, actors, guards, transitions, sequences, side effects,
  and invariants. Use for authentication, lockouts, bookings, payments,
  order lifecycles, retries, expiration, and approval workflows.
---

# State Transition Test Designer

Model state-dependent behavior and derive traceable, reproducible test cases from authoritative requirements.

Treat prior state, actors, events, guard conditions, and event sequences as test inputs.

Prioritize transition correctness, feasibility, state invariants, observable outcomes, and meaningful coverage.

Do not invent behavior absent from the specification.

## 1. Identify the state model

Extract from requirements:

1. States and stable identifiers (`S-ID`).
2. Initial states and terminal states, when defined.
3. Events and triggering actions.
4. Actors, roles, and permissions.
5. Guards and preconditions.
6. Expected destination states.
7. Actions and side effects.
8. Business invariants.
9. Observable evidence of state changes.

Distinguish:

- `STATE`: A meaningful condition affecting future behavior.
- `STATUS`: An observable representation of state information.
- `EVENT`: An occurrence that may trigger a transition.
- `GUARD`: A predicate controlling transition eligibility.
- `ACTION`: An operation or side effect.
- `INVARIANT`: A condition that must remain true in relevant states or transitions.

Do not assume every status label is a separate state.

Identify persisted, temporary, derived, and externally managed states.

## 2. Construct transition rules

For each transition, record:

- Stable transition ID (`TR-ID`).
- Source state.
- Event and actor.
- Guard predicates.
- Destination state.
- Expected actions and side effects.
- Applicable invariants.
- Source requirement.

Classify transitions as:

- `ALLOWED`: Explicitly supported behavior.
- `FORBIDDEN`: Explicitly prohibited behavior.
- `UNSPECIFIED`: Outcome not defined.
- `UNREACHABLE`: Impossible under established constraints.
- `UNRESOLVED`: Feasibility or applicability uncertain.

Distinguish:

- Invalid events for a given state.
- Allowed events rejected because guards fail.
- Valid transitions with different outcomes.
- Explicitly specified nondeterministic outcomes.

Do not assume unspecified transitions are forbidden.

Do not invent transition precedence or deterministic outcomes.

## 3. Validate model consistency

Check for:

- Missing or unreachable states.
- Unreachable transitions.
- Conflicting transition definitions.
- Overlapping guards with incompatible outcomes.
- Missing or ambiguous event handling.
- Undefined transition precedence.
- Unexpected dead ends and cycles.
- Incomplete recovery or reset behavior.
- Violated state invariants.

Do not assume a terminal state rejects every subsequent event unless specified.

Report specification gaps explicitly.

## 4. Design transition tests

For each selected transition:

1. Establish a known, reachable initial state.
2. Define a reproducible setup sequence.
3. Identify the target transition or guard outcome.
4. Trigger the required event.
5. Observe the response.
6. Verify the resulting state.
7. Verify specified side effects and invariants.
8. Assign or reuse a stable test ID (`T-ID`).
9. Link the test to its source requirement and coverage obligation.

Consider:

- Allowed transitions.
- Forbidden transitions.
- Guard failures.
- Initial-state behavior.
- Terminal-state behavior.
- Recovery and reset behavior.
- Relevant event sequences.

Keep unrelated conditions at feasible valid baselines.

Avoid redundant tests without distinct coverage value.

## 5. Test guard boundaries

For numeric, count, temporal, and relational guards:

1. Express the guard as a predicate.
2. Identify valid and invalid sides.
3. Determine inclusive or exclusive comparisons.
4. Reuse existing constraint IDs (`C-ID`).
5. Delegate ON/IN/OUT selection to `boundary-value-generator`.
6. Link corresponding boundary IDs (`B-ID`).
7. Verify transition behavior on both relevant sides.

Examples:

- `failed_attempts >= max_attempts`
- `now >= expires_at`
- `payment_amount <= remaining_balance`

For temporal guards, specify clock source, timezone, precision, and deterministic test setup.

Do not invent thresholds or arbitrary epsilon values.

## 6. Verify state, side effects, and invariants

Each executed test should verify relevant observable behavior:

- Response or error contract.
- Resulting business state.
- Persisted state changes.
- Related entity updates.
- Created or deleted records.
- Notifications or emitted events.
- Required business invariants.

For rejected events, verify specified behavior rather than assuming no mutation.

Possible specified effects include:

- No state change.
- Retry counter updates.
- Audit logging.
- Security-event recording.
- Other permitted side effects.

Distinguish expected side effects from incidental implementation behavior.

Do not infer normative behavior from existing code.

## 7. Test sequences and concurrency

When requirements or risks justify them, consider:

- Transition pairs.
- Repeated events.
- Duplicate requests.
- Retry behavior.
- Invalid event ordering.
- Recovery after failure.
- Expiration during a workflow.
- Concurrent events targeting shared state.

For each sequence:

1. Define the initial state.
2. Specify the complete ordered event sequence.
3. Identify intermediate observations when required.
4. Define expected final state and side effects.
5. Verify applicable invariants.

For concurrency:

- Identify the shared resource.
- Identify the required invariant.
- Define allowed observable outcomes.
- Use controlled synchronization where possible.
- Do not assume a specific event ordering without justification.

For asynchronous systems, distinguish immediate responses from eventual outcomes.

Use specified timing guarantees or documented assumptions.

Do not invent consistency deadlines.

## 8. Ensure reproducible setup

Every test must start from a known state.

Specify:

- Required test data and fixtures.
- Actor and permissions.
- Initial entity state.
- Required preceding events.
- State reset or isolation strategy.
- External dependencies and controlled mocks, if needed.

Prefer isolated test data and deterministic setup.

Do not let one test depend on the execution order or side effects of another unless explicitly testing a sequence.

Do not modify production data or shared resources without authorization.

## 9. Plan coverage

Use `coverage-goal-planner` to define applicable criteria:

- State coverage.
- Allowed transition coverage.
- Forbidden transition coverage.
- Guard outcome coverage.
- Transition-pair coverage.
- Relevant event-sequence coverage.

Maintain distinct obligation IDs for each criterion.

Track separately:

- Feasible obligations.
- Designed tests.
- Executed tests.
- Passed and failed evidence.
- Blocked or uncovered obligations.
- Unreachable and unresolved transitions.

Do not combine different coverage criteria into one percentage without a justified method.

Do not claim complete path coverage for cyclic or unbounded state machines.

## 10. Preserve traceability

Use the shared `test-case-catalog`.

Maintain:

`Requirement → S-ID → TR-ID → Guard/C-ID/B-ID → T-ID → Oracle → Evidence`

A single test may cover multiple obligations when justified.

Preserve established identifiers across domain modeling, BVA, execution, coverage, and reporting.

Separate test design from execution observations.

Do not duplicate existing test cases unnecessarily.

## 11. Output

### State inventory

`S-ID | State | Description | Observable evidence | Initial/Terminal | Source`

### Transition table

`TR-ID | From | Event/Actor | Guard | To | Actions/Side effects | Invariants | Classification | Source`

### Test cases

`T-ID | TR-ID | Setup sequence | Event/Input | Expected response | Expected state | Side effects/Invariants | Oracle`

### Coverage and gaps

Report:

- States and transitions identified.
- Feasible transition obligations.
- Guard outcomes and sequence obligations.
- Designed and executed coverage.
- Untested transitions.
- Unreachable states or setup paths.
- Unspecified behavior.
- Residual risks.

Keep complete execution evidence in the shared test-case catalog.

## 12. Quality gates

Before finalizing, verify:

- States and transitions trace to source requirements.
- Initial states and setup paths are reproducible.
- State and status are distinguished.
- Transition guards are explicit.
- Allowed, forbidden, and unspecified behavior is separated.
- Guard failure is distinguished from invalid events.
- Conflicting transitions remain visible.
- Expected destination states are observable.
- Relevant side effects and invariants are verified.
- Guard boundaries use correct units and inclusion.
- Event ordering and concurrency risks are considered where applicable.
- Every selected test has a coverage purpose and oracle.
- Test IDs match the shared catalog.
- Coverage obligations and exclusions are explicit.
- Execution claims have supporting evidence.
- Unresolved behavior is not presented as passing.

## Constraints

- Do not invent states, transitions, guards, or expected outcomes.
- Do not infer requirements from implementation behavior.
- Do not treat unspecified transitions as automatically forbidden.
- Do not assume rejected events have no side effects.
- Do not create unnecessary event-sequence combinations.
- Do not claim complete path coverage from finite tests on unbounded models.
- Do not fabricate execution evidence.
- Do not duplicate existing test cases unnecessarily.
- Do not equate state or transition coverage with complete system correctness.
