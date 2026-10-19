---
name: test-oracle-writer
description: >
  Define precise, observable, specification-based test oracles for
  designed test cases. Use when tests require expected responses,
  validation errors, state transitions, persistence checks, side effects,
  invariants, or asynchronous outcomes. Ensure expectations are traceable,
  testable, and independent from observed SUT behavior.
---

# Test Oracle Writer

Define reliable, observable pass/fail expectations for specification-based test cases.

An oracle describes **what the system should do**, not what the current implementation happens to do.

Prioritize requirement traceability, observable behavior, appropriate precision, and defect detection.

Do not invent expected behavior absent from authoritative requirements.

## 1. Identify oracle sources

For each test case (`T-ID`):

1. Identify the source requirement or rule.
2. Determine the behavior being verified.
3. Identify applicable constraints and invariants.
4. Select an authoritative oracle source.
5. Record any assumptions or ambiguities.

Acceptable oracle sources include:

- Explicit feature specifications.
- Acceptance criteria.
- Agreed business rules.
- Approved domain models.
- Documented contracts or standards.
- Independent reference implementations, when justified.
- Derived mathematical or logical invariants.

Implementation observations may help investigate discrepancies but must not silently become normative expectations.

Classify oracle certainty:

- `CONFIRMED`: Directly specified by an authoritative source.
- `DERIVED`: Logically follows from confirmed rules.
- `ASSUMED`: Depends on an explicitly documented assumption.
- `UNRESOLVED`: Insufficient or conflicting information.

Do not present assumed or unresolved expectations as confirmed.

## 2. Identify observable outcomes

Determine which observable interfaces are relevant:

- API response.
- HTTP status and response body.
- UI feedback and component state.
- Persisted database records.
- Business state transitions.
- Emitted events or messages.
- External service interactions.
- Notifications.
- Audit records.
- Relevant invariants and side effects.

Select only observations necessary to verify the specified behavior.

Do not add arbitrary assertions based solely on implementation details.

## 3. Define expected behavior

For each test, specify:

1. Preconditions and required initial state.
2. Exact stimulus or operation.
3. Expected observable outcome.
4. Allowed values or result constraints.
5. Expected state changes.
6. Required or prohibited side effects.
7. Observation method.
8. Oracle source and certainty.

Use precise, verifiable assertions.

Examples:

- `quantity` must satisfy the specified range.
- A successful booking creates exactly one booking record.
- An expired token must not authorize the protected operation.
- A rejected update must preserve the specified business invariant.

These are illustrative only; apply them when supported by the feature specification.

Avoid vague expectations such as:

- "Works correctly."
- "Returns an appropriate error."
- "Processes successfully."
- "Updates data properly."

Do not invent exact error codes, messages, or response schemas when the specification does not define them.

## 4. Support composite oracles

A single test may require multiple observable assertions.

Group assertions by relevant layer:

### Response oracle

Verify specified status, response structure, values, or validation errors.

### State oracle

Verify the resulting business state and required transitions.

### Persistence oracle

Verify expected database mutations or unchanged data.

### Side-effect oracle

Verify required events, notifications, logs, or external effects.

### Invariant oracle

Verify business conditions that must remain true.

Assign stable assertion identifiers when useful:

`T-ID.A1`, `T-ID.A2`, `T-ID.A3`

Each assertion must have a source and observation method.

Define which assertions are mandatory for the test to pass.

Do not mark a test as passed when a required assertion fails or cannot be evaluated.

## 5. Handle negative tests

For invalid inputs, rejected operations, and forbidden transitions:

1. Identify the violated rule.
2. Define the expected rejection behavior.
3. Specify relevant state or data changes.
4. Identify required or prohibited side effects.
5. Define how rejection and resulting state are observed.

Do not assume rejected operations cause no mutations.

Some rejected operations may legitimately:

- Increment failure counters.
- Record audit events.
- Update lockout state.
- Trigger security notifications.

Verify unchanged state only where required by the specification or a justified invariant.

Separate client-side rejection from backend rejection.

Do not treat frontend validation as evidence of backend correctness.

## 6. Handle multiple allowed outcomes

When the specification permits more than one result:

1. Define the complete allowed outcome set.
2. Specify conditions under which each result is valid.
3. Identify shared invariants.
4. Define observations needed to distinguish outcomes.

An oracle may be a predicate rather than one exact value.

For nondeterministic or concurrent systems, verify that the observed result belongs to the specified allowed set and satisfies all required invariants.

Do not arbitrarily select one outcome from a permitted set.

If outcome rules conflict or remain unspecified, mark the oracle unresolved.

## 7. Handle asynchronous and temporal behavior

For asynchronous operations, identify:

- Triggering event.
- Expected eventual condition.
- Observable completion signal.
- Clock source and timezone, when relevant.
- Timing precision.
- Specified deadline or timeout.
- Permitted intermediate states.

Use deterministic clocks and controlled dependencies when feasible.

Do not invent arbitrary response-time or eventual-consistency deadlines.

If the specification guarantees eventual completion without a deadline, distinguish the practical test waiting limit from the normative requirement.

A test timeout alone does not prove a specification violation unless the timing expectation is supported.

For retries and duplicate requests, verify specified idempotency and side-effect guarantees.

## 8. Define observation methods

Every oracle must have a concrete verification method.

Examples:

- API response assertion.
- Database query.
- UI state assertion.
- Event consumer or message inspection.
- State transition verification.
- Controlled fake clock.
- Mock or spy for external interactions.
- Independent calculation.

Observation must be sufficient to distinguish expected and unexpected behavior.

Prefer externally observable behavior over private implementation details.

If an expected outcome cannot be reliably observed, mark it `UNOBSERVABLE` and identify the missing instrumentation or access.

Do not claim the corresponding assertion is verified.

## 9. Preserve traceability

Use the shared `test-case-catalog`.

Maintain:

`Requirement → Constraint/Model → T-ID → Oracle → Observation Method → Evidence`

Reuse existing:

- Requirement IDs.
- Constraint IDs (`C-ID`).
- Partition IDs (`P-ID`).
- Boundary IDs (`B-ID`).
- Decision rule IDs (`DR-ID`).
- Transition IDs (`TR-ID`).
- Test case IDs (`T-ID`).

A test may have multiple oracle assertions.

An oracle assertion may verify multiple obligations when justified.

Preserve source references and avoid duplicating equivalent test cases.

## 10. Separate expected and actual results

Maintain a strict distinction:

- `EXPECTED`: Derived from the specification or justified reference.
- `ACTUAL`: Observed during execution.
- `EVIDENCE`: Artifact supporting the observation.
- `VERDICT`: Comparison between expected and actual results.

Oracle definition belongs to test design.

Actual results and execution verdicts belong to the execution record.

Do not modify expected results merely to match observed implementation behavior.

If an oracle is corrected following a specification clarification, document the source and reason for the change.

Never report unexecuted tests as PASS.

## 11. Output

### Oracle inventory

`T-ID | Source rule | Preconditions | Stimulus | Expected observable result | Observation method | Certainty`

### Oracle assertions

`T-ID | Assertion ID | Oracle type | Expected predicate/value | Source | Verification method | Mandatory?`

### Unresolved oracles

`T-ID | Missing/conflicting rule | Affected expectation | Required clarification`

### Execution linkage

`T-ID | Oracle/Assertion ID | Evidence reference | Actual result | Verdict`

Include execution linkage only when verified observations are available.

Do not fabricate evidence or execution outcomes.

## 12. Quality gates

Before finalizing, verify:

- Every oracle traces to a reliable source.
- Expected results are independent of observed SUT behavior.
- Preconditions and stimuli are explicit.
- Assertions are objectively verifiable.
- Response, state, persistence, and side effects are covered where required.
- Composite oracle assertions are individually traceable.
- Negative tests verify specified rejection and mutations.
- Multiple allowed outcomes are represented correctly.
- Time-based expectations use justified precision and deadlines.
- Unobservable assertions are identified.
- Expected details do not exceed specification precision.
- Assumed and unresolved expectations remain visible.
- Test IDs match the shared catalog.
- Actual results remain separate from expected results.
- PASS/FAIL conclusions require execution evidence.
- No test passes while a mandatory assertion is failed or unverified.

## Constraints

- Do not invent requirements, error codes, or response messages.
- Do not infer expected behavior solely from implementation.
- Do not treat rejected operations as automatically side-effect-free.
- Do not invent timing guarantees or consistency deadlines.
- Do not over-specify behavior beyond authoritative requirements.
- Do not fabricate execution evidence.
- Do not mark unresolved or unobservable assertions as verified.
- Do not silently change oracles after execution.
- Do not duplicate existing test cases unnecessarily.
- Do not equate successful assertions with complete product correctness.
