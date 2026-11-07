# Cross-Browser Testing — Domain Procedure and Oracle

Use this prompt with `SKILL.md` when you need to derive cross-browser quality candidates from a support matrix, user distribution, engine/version data, device inventory, or known-defect list.

## Inputs to collect

1. **Objective** — which release, feature, or risk question the coverage must answer.
2. **Scope** — pages, flows, components, and platforms in and out of scope.
3. **Material** — support matrix, analytics, browser/device inventory, design declarations, defect history.
4. **Environment** — real browsers, devices, emulators, cloud providers, CI capacity, and access limits.
5. **Evidence** — what was actually observed at runtime versus what is only declared or inferred.
6. **Constraints** — budget, schedule, licensing, and Human decisions that bound the work.

Record each input as *known*, *missing*, *conflicting*, *stale*, *out_of_scope*, or *assumption* before producing findings.

## Derivation procedure

1. Convert the support matrix and user distribution into engine / platform / version / device cells.
2. Keep the identity of each cell explicit: real browser, real device, emulator, or automation engine. A brand name or emulator count is not target-environment coverage.
3. Rank cells by user share, business criticality, defect history, rendering risk, and input-modality risk.
4. Select a risk-based sample that covers the highest-ranked cells and the smallest set that can falsify the main compatibility assumptions.
5. For each selected cell, state the concern, source evidence, expected oracle, validation action, evidence state, impact/priority, owner role, and close condition.
6. Preserve conflicts, unknown constraints, and open questions instead of resolving them by convention.

## Oracle

A candidate is supported only when runtime evidence from the named cell shows the expected behaviour for the stated concern. Until then, keep the item `unassessed`, `blocked`, or `NOT_RUN`. Do not convert file presence, a design declaration, a candidate count, or a passing desktop run into cross-browser coverage or release evidence.

## Output

Produce `CBT-##` findings that separate:

- static analysis and design intent,
- unexecuted work,
- runtime evidence and its state,
- Human decisions and accepted risk.
