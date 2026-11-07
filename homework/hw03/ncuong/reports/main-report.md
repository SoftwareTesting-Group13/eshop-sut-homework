# HW03 — GUI & Usability

**Student:** Dương Nhật Cường · **MSSV:** 23120223 · **Group:** 13
**SUT:** EShop — `https://github.com/ttbhanh/eshop-sut`
**Submission scope of this draft:** Task 1 (GUI checklist) completed; Task 2 and Task 3 are not started yet.
**Date:** 2026-11-07

## 0. Deliverable map

| Deliverable | Link |
| --- | --- |
| GUI checklist (Markdown) | [`features/GUI/checklist.md`](../features/GUI/checklist.md) |
| GUI checklist (Excel, 69 items) | [`features/GUI/checklist.xlsx`](../features/GUI/checklist.xlsx) |
| Test summary | [`features/GUI/test-summary.md`](../features/GUI/test-summary.md) |
| AI initial set | [`features/GUI/ai-initial-checklist.md`](../features/GUI/ai-initial-checklist.md) |
| Review additions + rationale | [`features/GUI/review-additions.md`](../features/GUI/review-additions.md) |
| Bug report | [`features/GUI/bug-report.md`](../features/GUI/bug-report.md) |
| Individual bug reports (26) | [`features/GUI/bugs/`](../features/GUI/bugs/) |
| GitHub issue drafts (26) | [`features/GUI/issues/`](../features/GUI/issues/) |
| Screenshots (failed items only) | [`features/GUI/screenshots/`](../features/GUI/screenshots/) |
| AI audit report | [`reports/ai-audit.md`](ai-audit.md) |

---

# Task 1 — GUI checklist

## 1.1 Scope and objectives

The checklist targets the authentication and profile area of the EShop web frontend:

| FR | Screen | Why it is in scope |
| --- | --- | --- |
| FR-01 Account registration | `/register` | The first screen a new user meets; many validation and feedback states. |
| FR-02 Login and account lockout | `/login` | The entry point to every authenticated flow; security-sensitive input handling. |
| FR-03 Forgot password and reset | `/forgot-password` | Two-step flow with OTP, a state transition and error recovery. |
| FR-04 Profile management | `/profile` | Mixed form + data table; update, empty, loading and error states. |

The four interface aspects required by the homework are covered explicitly:

- **IA-01 General UI standards** — layout, typography, colour/contrast, responsiveness, RTL, dark mode, zoom.
- **IA-02 Forms** — input types, labels, required fields, validation, password rules, OTP constraints.
- **IA-03 Navigation** — header, links, SPA routing, tab order, focus, route guards, current-page state.
- **IA-04 Feedback / state** — loading, success, error, empty, destructive-action confirmation, OTP privacy.

**Objective:** produce a non-repetitive checklist of more than 40 executable items, execute every item against the SUT, and separate genuine defects from design gaps.

## 1.2 Method

The work followed the course's AI-first but human-reviewed process:

1. **Initial AI generation with the `ui-checklist-generator` skill.**
   The skill's eight categories (layout, typography, colour, interaction, responsiveness, accessibility, product states, polish) were expanded across the four screens. This produced **44 initial items** (preserved in [`ai-initial-checklist.md`](../features/GUI/ai-initial-checklist.md)).
2. **Critical review of the AI output.**
   The initial set was compared with what can actually fail on these screens: computed contrast, DOM/ARIA facts, keyboard order, SPA routing, step focus, route guards, responsive data tables, destructive actions and error/empty state separation. The review added **25 items** (see [`review-additions.md`](../features/GUI/review-additions.md)). These additions were produced in the same AI-assisted review pass and are still **pending the student's accept/reject decision**; the AI audit records them as agent output, not as human-authored work.
3. **Execution.**
   Every item was executed against a locally running SUT. Functional behaviour was driven with Playwright 1.65 (Chromium 158); DOM/ARIA facts were read from the live page; accessibility facts came from axe-core 4.x. Failed items were screenshotted with an annotation banner.
4. **Bug triage.**
   Failed items were grouped by root cause. A failed item is not automatically a bug: missing confirm-password fields and missing step indicators are recorded as design gaps, not defects. The reproducible defects became 26 bug reports.

## 1.3 Checklist design

**69 items** were designed and executed: 44 from the AI initial pass and 25 added during review. Every item belongs to exactly one IA and one FR/screen.

| Interface aspect | Items | Passed | Failed |
| --- | ---: | ---: | ---: |
| IA-01 General UI standards | 19 | 8 | 11 |
| IA-02 Forms | 16 | 4 | 12 |
| IA-03 Navigation | 17 | 9 | 8 |
| IA-04 Feedback / state | 17 | 4 | 13 |
| **Total** | **69** | **25** | **44** |

Coverage is deliberately spread over the four screens rather than concentrated on one:

| Screen | Items | Examples of what was checked |
| --- | ---: | --- |
| Login | 17 | heading, tab title, input types, label association, tab order, error/loading, authenticated redirect |
| Register | 16 | email format, duplicate email, password-rule consistency, confirm password, contrast, success feedback, raw server error |
| Forgot Password | 16 | two-step flow, OTP exposure, OTP input constraints, focus after transition, step indicator, button hierarchy, invalid-email alert |
| Profile | 17 | heading hierarchy, label association, phone validation, mobile table, order loading/error/empty, cancel confirmation, logout redirect |
| All auth screens | 3 | RTL layout, dark-mode legibility, 200% zoom |

The complete table with the result and failure reason for every item is in [`checklist.md`](../features/GUI/checklist.md) and [`checklist.xlsx`](../features/GUI/checklist.xlsx).

## 1.4 Critical review: what the AI missed and why

The 25 review additions are listed with a per-item rationale in [`review-additions.md`](../features/GUI/review-additions.md). The reasons fall into three groups.

### A. Prompt quality

The first prompt asked for a GUI checklist for four screens but did not force the AI to produce an *executable oracle* per item. The AI therefore wrote broad statements such as “sufficient contrast” and “mobile usable” without a way to decide pass/fail. The review converted them into measurable checks (computed ratio ≥ 4.5:1, `scrollWidth = clientWidth` at 360px, `activeElement` after a step transition).

### B. Model limitations

- **No execution.** The AI could not run the SPA, so it could not see that the forgot-password link causes a full reload, that `tabindex="1"` puts the submit button first, or that a 500 response is rendered as an empty order list.
- **Accessibility by appearance.** The AI treated visible `<label>` text as a label. It did not check `for`/`id`, `aria-label`, `aria-live`, `aria-invalid` or heading levels.
- **No computed contrast.** The AI said “check contrast” but did not calculate it. axe-core found 2.53:1, 3.76:1 and 3.92:1 failures.
- **Default assumptions.** The model assumed LTR, light mode and 100% zoom. RTL, dark mode and 200% reflow only appeared after an explicit review.
- **Feedback vs privacy.** The AI read “Mã OTP của bạn là: …” as helpful feedback; it did not flag it as a password-reset takeover vector.

### C. Interface characteristics

Some defects are only visible in this particular SUT:

- The register/reset regex requires a whitespace character while the copy promises a special character — a contradiction that only appears when the regex and the copy are read together.
- The profile phone regex `/^[1-9][0-9]{8,9}$/` rejects every normal Vietnamese number starting with `0`, including the placeholder `0912345678`.
- The two-step reset flow keeps both steps in one component, so focus management and step indication are easy to miss.
- The order-history table has five columns and no responsive wrapper, so the page overflows only when an order exists.

## 1.5 Execution

| Item | Value |
| --- | --- |
| Backend | `http://localhost:3000` (`backend/server.js`, seeded SQLite) |
| Web frontend | `http://localhost:5173` (`frontend-web`, Vite) |
| Browser | Chromium 158 / Playwright 1.65 |
| Desktop viewport | 1280×900 |
| Mobile viewport | 360×800 |
| 200% zoom equivalent | 640×800 |
| Accessibility engine | axe-core 4.x |
| Test users | `hw03.ui.23120223@example.com`, plus isolated `dup…` and `silent…` accounts |
| Order fixtures | Injected with Playwright route interception; no real order rows were created or modified |

Execution rules:

- **Passed** = the observed behaviour matches the item's oracle in the executed environment.
- **Failed** = the observed behaviour contradicts the oracle. The Notes column records the exact observation.
- Screenshots were captured **only for failed items**; each screenshot has a red banner with the checklist ID and the observed defect.
- Contrast verdicts come from axe-core's computed ratios, not from visual judgement.

## 1.6 Results and analysis

### 1.6.1 Headline result

25 of 69 items passed and 44 failed. The failure rate is high because the SUT is intentionally seeded with UI/UX defects, and because the checklist deliberately includes accessibility and state-edge cases that a happy-path smoke test would skip.

### 1.6.2 Systemic issues (not isolated bugs)

1. **Authentication screens are visually and semantically unfinished.** The Login heading says “Đăng Ký”, the password is visible, the email field is `type="text"`, and every form label is unassociated. This is one root pattern (copy/paste auth form without a semantic pass), not four unrelated defects.
2. **Feedback is either absent or blocking.** Login shows a generic unannounced div; Forgot Password and Profile use native `alert()`. There is no shared inline message/`aria-live` pattern.
3. **State handling is binary.** Register/Login have no loading state; Profile shows “no orders” while loading and after a 500 response. The UI cannot distinguish “not started”, “empty”, “failed” and “done”.
4. **Accessibility is not part of the definition of done.** axe-core reports critical label violations on all four screens, no page has an `h1`, contrast fails in several places, tab order is broken by `tabindex="1"`, and RTL/dark-mode/zoom were never considered.
5. **Destructive and security-sensitive actions lack safeguards.** The OTP is printed on screen; cancel-order has no confirmation and is offered for shipping orders; route guards are missing for `/profile` and `/login`.

### 1.6.3 Bugs by severity

| Severity | Count | Examples |
| --- | ---: | --- |
| Blocker | 2 | OTP exposed on screen (BUG-GUI-24); valid Vietnamese phone rejected, blocking profile save (BUG-GUI-14) |
| Major | 12 | visible password, missing labels, email/duplicate validation, password-rule contradiction, mobile table overflow, tab order, route guards, raw server error, alert-only feedback, order loading/error confusion, cancel without confirmation |
| Minor | 12 | wrong Login heading, shared tab title, identical step-2 buttons, missing `h1`, RTL, no active nav, no loading state, silent registration success, focus loss, full reload, unconstrained OTP, missing confirm password |
| **Total** | **26** | See [`bug-report.md`](../features/GUI/bug-report.md) |

Each bug has a report with steps, expected/actual, root cause, suggested fix and screenshot in [`features/GUI/bugs/`](../features/GUI/bugs/). The GitHub issue bodies are in [`features/GUI/issues/`](../features/GUI/issues/).

## 1.7 Limitations and open items

- **GitHub Issues are not published yet.** This environment has no GitHub CLI or token. The 26 issue bodies are ready in `features/GUI/issues/`; after `gh auth login`, run `bash features/GUI/issues/publish.sh` from `homework/hw03/ncuong`. The report does not claim issue links that do not exist.
- **Task 1 was executed on one browser engine (Chromium).** Firefox, Safari and the Expo Go platform belong to Task 3.
- **The AI initial set is preserved as generated.** The student must still review the 69 items and the 26 bugs before submitting; the AI audit records what the agent produced and what it could not verify.
- **Timestamps in the AI audit are marked “Time not available in source”** because the conversation export does not contain them.

## 1.8 Evidence index

- 44 failed items → 40 annotated screenshots in [`screenshots/`](../features/GUI/screenshots/), with `manifest.json` mapping each image to checklist IDs.
- axe-core results and DOM facts are summarized in the Notes column; the raw JSON is in `screenshots/manifest.json` and the execution logs are reproducible from the scripts in [`tools/`](../features/GUI/tools/).
- Excel workbook: `checklist.xlsx` (sheets: Checklist, Summary, Execution).

---

# Task 2 — Usability evaluation

**Status: not started.** To be completed after Task 1 review: flow selection, task scenario, SUS/UEQ-S, 7 participants, pilot, sessions, analysis.

# Task 3 — Cross-browser / cross-platform

**Status: not started.** To be completed after Task 1 review: Chrome, Firefox and Safari (or Android Chrome / Expo Go), with student ID and full name overlaid on every screenshot.

# Agent Skills

The skills used for this task are in [`skills/`](../skills/). The GUI checklist workflow is documented in [`skills/ui-checklist-generator/SKILL.md`](../skills/ui-checklist-generator/SKILL.md) and [`skills/gui-usability-workflow/SKILL.md`](../skills/gui-usability-workflow/SKILL.md). The demo video is not recorded yet.

# AI audit and critique

- AI Audit Report: [`reports/ai-audit.md`](ai-audit.md)
- AI Critique: [`reports/ai-critique.md`](ai-critique.md) (draft — student review pending)

# Self-assessment

The self-assessment table is in [`README.md`](../README.md). It is intentionally left blank until the student reviews the Task 1 deliverables.
