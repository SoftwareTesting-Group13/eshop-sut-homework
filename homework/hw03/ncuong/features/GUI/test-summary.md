# Test summary — HW03 Task 1 (GUI checklist)

**Student:** Dương Nhật Cường · **MSSV:** 23120223 · **Group:** 13
**SUT:** EShop web frontend · **Date:** 2026-11-07
**Scope:** FR-01 Account registration, FR-02 Login, FR-03 Forgot/reset password, FR-04 Profile management
**Screens:** Login, Register, Forgot Password, Profile
**Interface aspects:** IA-01 General UI standards, IA-02 Forms, IA-03 Navigation, IA-04 Feedback / state

## Headline numbers

| Metric | Value |
| --- | ---: |
| Screens tested | 4 |
| End-to-end flows tested | 0 (Task 2 starts after Task 1) |
| Checklist items designed | 69 |
| Checklist items executed | 69 |
| Passed | 25 |
| Failed | 44 |
| Bugs reported | 26 |
| Blockers | 2 |
| Major | 12 |
| Minor | 12 |
| Participants | 0 (Task 2) |
| Demo videos | 0 (to be recorded with the Agent Skill) |

## Results by interface aspect

| Interface aspect | Items | Passed | Failed |
| --- | ---: | ---: | ---: |
| IA-01 General UI standards | 19 | 8 | 11 |
| IA-02 Forms | 16 | 4 | 12 |
| IA-03 Navigation | 17 | 9 | 8 |
| IA-04 Feedback / state | 17 | 4 | 13 |
| **Total** | **69** | **25** | **44** |

## Source split

| Source | Items |
| --- | ---: |
| AI-generated initial set (`ui-checklist-generator`) | 44 |
| Items added during the critical review | 25 |
| **Total** | **69** |

The 25 review additions and the reason the initial AI pass missed each one are listed in
[`review-additions.md`](review-additions.md). The raw initial set is preserved in
[`ai-initial-checklist.md`](ai-initial-checklist.md).

## Execution environment

| Item | Value |
| --- | --- |
| Backend | `http://localhost:3000` (`backend/server.js`, seeded SQLite) |
| Web frontend | `http://localhost:5173` (`frontend-web`, Vite) |
| Browser | Chromium 158 / Playwright 1.65 |
| Desktop viewport | 1280×900 |
| Mobile viewport | 360×800 |
| 200% zoom equivalent | 640×800 |
| Accessibility engine | axe-core 4.x |
| Test data | Isolated users `hw03.ui.23120223@example.com`, `dup…@example.com`, `silent…@example.com`; order rows injected with Playwright route interception (no production order data was modified) |

## Artifacts

| Artifact | Path |
| --- | --- |
| Full checklist (Markdown) | [`checklist.md`](checklist.md) |
| Full checklist (Excel) | [`checklist.xlsx`](checklist.xlsx) |
| Machine-readable results | [`checklist.json`](checklist.json) |
| AI initial set | [`ai-initial-checklist.md`](ai-initial-checklist.md) |
| Review additions + rationale | [`review-additions.md`](review-additions.md) |
| Bug report | [`bug-report.md`](bug-report.md) |
| Individual bug reports | [`bugs/`](bugs/) |
| GitHub issue drafts | [`issues/`](issues/) |
| Screenshots (44 failed items, 40 images) | [`screenshots/`](screenshots/) |

## Notes and limitations

- All 69 items were executed; a failed item is not automatically a bug (missing confirm-password fields and step indicators are design gaps). The 26 bugs are the reproducible defects.
- Screenshots are annotated with a red banner containing the checklist ID and the observed defect. They show the SUT at `localhost:5173`, not a redesigned mock.
- GitHub Issues are drafted but **not yet published** because this environment has no GitHub CLI/token. The ready-to-publish bodies are in `issues/`; run `bash issues/publish.sh` after `gh auth login`.
- The AI audit report records this session; timestamps are marked "Time not available in source" because the conversation export does not contain them.
