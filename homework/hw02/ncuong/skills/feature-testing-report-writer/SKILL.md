---
name: feature-testing-report-writer
description: Write a detailed Vietnamese testing report for one feature, tracing specification analysis through Domain Testing, BVA, case design, execution, coverage, bugs, and evidence. Use for reusable per-feature testing reports across projects.
---

# Feature testing report writer

Write the four **per-feature report files** in Vietnamese; keep established technical terms in English when clearer. Derive rules, IDs, and interfaces from the current task. If a course or user provides a method/template, follow it while preserving the trace from requirement to evidence. Use the specialized domain, BVA, oracle, catalog, coverage, and findings skills when relevant.

## Reader path

The report must let a reader answer, in order: **What did the spec require? How was the input/state space modeled? Why were these cases selected? What was executed? What happened? What is still unknown?** Do not begin with a wall of test IDs or repeat the same full cases in several sections.

For `domain-analysis.md` and `boundary-analysis.md`, make the main entries directly reviewable. An EP row should show the class condition, concrete representative, Expected, source rule, and case. A BVA block should show the rule, exact threshold, prepared value/state, Expected at each meaningful point, and case. Choose a table, compact block, or short prose according to the feature; do not copy the bug-report format into these analyses. Avoid separate “Đọc nhanh” sections and duplicate mapping tables. Add a note only where precision, setup, ambiguity, or feasibility needs explanation. Keep detailed Actual/verdicts in `test-results.md`.

1. **Scope and sources.** Name the feature, interface/platform, build/version, source requirements and exclusions. State the environment and isolation needed to reproduce execution. Give a short result snapshot only if evidence exists.
2. **Specification analysis.** Extract testable rules and acceptance oracles with source references. Separate explicit rules, assumptions, ambiguities, and contradictions. Identify actors, inputs, outputs, state, side effects, dependencies, and any cross-feature rules. Do not turn observed SUT behavior into a requirement.
3. **Domain Testing.** Show the reasoning steps: dimensions/constraints, valid-invalid-unknown partitions, representative choices, and decision/state models only when they affect behavior. Map obligations to test IDs. Link the shared catalog for full cases.
4. **Boundary Value Analysis.** As a separate section, derive each applicable predicate edge, inclusion, type/unit/precision, selected ON/IN/OUT or nearest feasible values, and case IDs. Explain where a boundary is unavailable, infeasible, or cannot be observed exactly.
5. **Test case design.** Maintain one authoritative catalog of EP and BVA cases with stable IDs, technique/obligation links, setup, concrete input and action, observable Expected, and current design status. A case serving both methods appears once. Do not add a separate UI validation section merely because the feature has a page.
6. **Execution and results.** Execute cases when the request includes testing execution and an authorized, suitable SUT is available. For a full testing request, aim to run every feasible designed case and explain any that remain unrun. State what ran, on which build/environment, in what order, and how state was reset. Record Actual, PASS/FAIL/BLOCKED/CHƯA CHẠY/INCONCLUSIVE, evidence, and related bug ID against each case. A design-only report identifies the planned verification method without presenting observations. An execution table may reference catalog IDs instead of repeating all setup/Expected prose. Keep code inspection separate from a browser/device run. Maintain the **evidence log** with the template at `assets/evidence-log-template.md`: one `EV-ID` per execution attempt, linked to its `T-ID`, with the real command/action and raw result.
7. **Coverage and gaps.** Count feasible obligations with explicit denominators and distinguish designed, executed, passed, and untested coverage. Record unmodeled or unresolved rules, blocked cases, evidence gaps, and limitations; a failed test may still satisfy execution coverage.
8. **Bug reports.** Give each reproduced candidate defect its own feature-scoped ID, linked requirement/cases, a full manual reproduction block (see below), Expected/Actual, evidence, impact/severity rationale, and issue status. Include a severity-and-priority summary table with the classification criteria used, and keep per-bug details consistent with it. Do not count every failed case as a bug, and do not merge distinct observable defects into one ID merely because they share a code line, nor split one defect into several IDs merely because several cases hit it.
9. **Human AI Gap and follow-up.** Reserve the student's AI Gap Analysis without filling it for them. List remaining verification and artifact work. Link the AI audit/critique or commit log only when the assignment requires them.

## Execution setup (when execution is in scope and the SUT is runnable)

1. Identify persistent state and existing changes before execution. When a working database is involved, record its path and pre-run state; prefer an isolated test database. If the working database must be used, establish an authorized snapshot and recovery procedure, including applicable SQLite sidecars. Never assume `git restore` is safe for automatic cleanup.
2. Start only the SUT components needed for the scoped cases on seeded/reset **test** data; record build, ports, and versions. Reset test state before each stateful case.
3. Use a browser driver only when needed to execute an EP/BVA case through the feature's UI and permitted by the environment.
4. When a case runs through the browser, record its actual input and observable outcome; do not derive standalone UI appearance or DOM cases from this execution.
5. Execute feasible API cases with real requests, capture HTTP status and body, and read the data store directly when a side effect is part of the oracle.
6. Log one `EV-ID` per execution attempt with `assets/evidence-log-template.md`, linked to its `T-ID`; retain earlier attempts when rerunning.
7. If a case is genuinely unreachable (service down, no device), mark it `BLOCKED` with the concrete reason — never downgrade it to "source inspection".
8. Apply the methods required by the user or assignment. For HW02, write the Domain Testing/EP and BVA analyses separately; if no meaningful boundary exists, explain why there are no BVA cases. Add another test technique only when the user explicitly includes it in scope. Do not expand a design-only or limited report request into SUT execution.
9. **Keep raw logs human-readable.** Put every real command in a fenced shell code block (`zsh`/`bash`) with **full arguments** — never abbreviate as `curl …` and never bury a command mid-sentence. Pretty-print JSON bodies — **one field per line** — inside a fenced `json` block, and label `request / response / pre-state / post-state`. Non-JSON bodies (HTML, DOM snippet, DB output) still go in a fenced block and break across lines by structure. Never dump a whole object or a whole result on a single line; a log that cannot be read at a glance is a failed artifact. See `assets/evidence-log-template.md` → "Định dạng bắt buộc" for the good/bad example.
10. **Final cleanup after execution:** stop services started for this work and remove identified test-owned temporary resources. If a working database was used, restore it only through an authorized, verified procedure. Perform cleanup even on failure/interruption; verify and record the result. Never discard pre-existing changes or user-owned data.

## Report files and directory layout

Use four files per feature. Keep each test definition once in `test-cases.md`; the analysis files link to its `T-ID`, and `test-results.md` records execution, coverage, bugs, and remaining gaps. Start from the four matching templates in `assets/` (`domain-analysis-template.md`, `boundary-analysis-template.md`, `test-cases-template.md`, `test-results-template.md`). Use `assets/evidence-log-template.md` for execution attempts.

```
homework/hw02/
  docs/                          # assignment requirements
  <student-short-name>/
    README.md                     # submission summary
    reports/
      main-report.md             # cross-feature summary
      main-report.pdf            # final submission export
      ai-audit.md                # AI interaction log
      ai-audit.pdf               # final submission export
      ai-critique.md             # student critique
      ai-critique.pdf            # final submission export
    features/
      <FEATURE_CODE>/            # e.g. FR02, FR10, FR17, MOBILE
        domain-analysis.md       # scope, specification, domain/EP model
        boundary-analysis.md     # BVA predicates and boundary cases
        test-cases.md            # one EP/BVA design catalog
        test-results.md          # execution, coverage, bugs, gaps
        evidence/                # evidence log and raw artifacts
    skills/                      # this student's reusable skills
    git-commit-log.txt           # HW02 final submission
    supporting-materials/        # other supporting artifacts, if any
```

HW02 final submission requires PDF exports of all three shared reports beside their Markdown sources in `reports/`, plus `git-commit-log.txt`. During work in progress, mark missing deliverables pending; do not create empty feature files or placeholder PDFs and present them as completed work.

- Each feature's four report files and its evidence live in `features/<FEATURE_CODE>/`. Keep `T-ID` and `EV-ID` stable across those files.
- The three shared reports live in `reports/`; the student skill bundle lives in `skills/`, outside both `reports/` and `features/`.
- From a feature file, evidence is `evidence/...`; from `reports/main-report.md`, link with `../features/<FEATURE_CODE>/...`.
- Keep the source requirements in `homework/hw02/docs/`; do not copy them into a student's report directory.

## Bug entry format (manual reproduction)

Write every bug so that a reader can reproduce it **by hand** without reading code — the way a manual tester did before automation. State the feature code, the related test case, and the exact numbers/values/sequence. One reproduced finding = one entry, and the same entry appears (condensed) in the master report with its student-review status.

- **Bug ID is feature-scoped:** `BUG-<FEATURE_CODE>-NN` (e.g. `BUG-XX-01`) so a master aggregating several features can be searched and traced. Never reuse or renumber an ID for a different defect.
- **Preconditions** must be concrete: exact account/email, prior state (`login_attempts`, `locked_until`), how it was prepared.
- **Steps** are numbered and use exact values, not placeholders like "some value".
- **Expected** comes from the spec (cite the rule); **Actual** is the observed result.
- **Evidence** points to a log/artifact; do **not** take screenshots on your own — record `Screenshot/Issue: Chờ người kiểm thử xác nhận`; after review, the student captures the screenshot and opens the Issue. For HW02, a screenshot attached to each GitHub Issue is required for final submission; mark it pending until the student reviews the bug and captures it.
- Add a ready-to-run API snippet only when it helps reproduce (not a substitute for the manual steps).

```markdown
#### BUG-<FEATURE>-NN — <title>

| Trường | Giá trị |
| --- | --- |
| Feature | <FEATURE_CODE> — <tên> |
| Test case liên quan | <DT/BVA-ID> |
| Requirement | <R#/mục đặc tả> |
| Severity / Priority | <Critical/High/Medium/Low> / <...> |
| Trạng thái | Đã tái hiện; chờ người kiểm thử xác nhận |
| Evidence | `<đường dẫn log>` |

**Môi trường:** <build/OS/version>
**Tiền điều kiện:** <tài khoản cụ thể + state cụ thể>
**Các bước tái hiện:**
1. <bước với giá trị cụ thể>
2. ...

| Bước | Input / hành động | Quan sát |
| --- | --- | --- |
| 1 | `<giá trị thật>` | `<...>` |

**Expected:** <theo đặc tả + rule>
**Actual:** <kết quả quan sát>
**Độ lặp lại:** <1/1 hoặc n/m>
**Root cause:** <chỉ khi có bằng chứng code, kèm file:dòng>
**Reproduce nhanh (API):** <tùy chọn>
    curl -s -X POST ... 
**GitHub Issue:** Chờ người kiểm thử xác nhận bug trước khi mở
**Screenshot:** Chờ người kiểm thử xác nhận rồi chụp và gắn vào Issue

---
```

Separate consecutive bug entries with a `---` rule after each entry so long bug sections stay scannable.

## Presentation

- Use direct headings and column names; define uncommon IDs and symbols at first use when the label alone is insufficient.
- For BVA, write “ngay dưới / tại biên / ngay trên” with the Expected behavior for each point when ON/IN/OUT could hide which side changes behavior. Never use an observed wrong output as though it were a planned boundary input.
- Give each table one job. Combine obligation, concrete test value, Expected, and case in the relevant analysis row when that makes it reviewable; avoid a second table that merely remaps the same IDs. The execution table reports Actual and verdicts.
- Prefer a small table plus a short explanation over large condition matrices when the latter add no new decision rule. Use stable anchors/links from summary to details.
- Keep honest statuses: `Chưa chạy` for cases outside the requested execution or not yet attempted, `BLOCKED` for an attempted execution prevented by a concrete obstacle, and `Chưa xác định theo đặc tả` for unresolved oracles. A case whose Expected the spec does not define is an explicit observation, not PASS/FAIL.

## Review before handoff

Check the complete chain `source rule → domain/boundary obligation → case → oracle → observed result/evidence → bug or gap`. Confirm case IDs are unique, bug IDs carry the feature code, counts reconcile, links resolve, and every conclusion is supported by the right evidence type. For execution in scope, confirm each claimed observation links to an `EV-ID` for that attempt; a rendered-DOM claim must cite a real browser run, never a source read. Verify and log cleanup when execution modified resources. The master report should summarize this report, never supply missing detail retroactively.
