# AI Audit Report - working log

**AI tool:** OpenAI Codex (GPT-6)
**Dates covered:** 2026-11-16 to 2026-11-17 (Asia/Saigon)
**Student ID used in this draft:** 23120102 (from the existing HW03 submission folder; verify before submission)

This log records the prompts and outputs in this Codex conversation. The assistant used the HW04 PDF and the repository SRS as source material. The test suite uses mocked API responses, so its current reports are browser-level UI evidence, not evidence that the backend coupon/profile/product rules pass.

## Interaction 1 - requirement interpretation

**Time:** 2026-11-16 11:17 (Asia/Saigon; approximate conversation time)

**Prompt:** “Các FR ở HW2 là FR 04 09 15, b có thể đọc yêu cầu và giải thích kèm hướng dẫn chi tiết hoàn thành không”

**Output summary:** Codex read the attached HW04 brief, mapped FR-04/09/15 to Pools A/B/C, extracted the three-feature, 12-case-per-feature, separate-data, three-assertion-pattern, three-browser, HTML-report, AI-audit, AI-critique, demo-video, and Git-history requirements, then outlined candidate cases for each FR.

## Interaction 2 - implementation request

**Time:** 2026-11-16 11:19 (Asia/Saigon; approximate conversation time)

**Prompt:** “b có thể hoàn thành và mục ai-audit sẽ prompt theo mục 6 của b không”

**Output summary:** Codex inspected the EShop UI and SRS, created a Playwright project with separate JSON data and FR-04/09/15 specs, installed Playwright and Chromium/Firefox/WebKit, then executed an initial 114-run matrix (70 passed, 44 failed). Review found both SUT defects and automation issues. The corrected run produced nine HTML reports and a JSON summary: 114 runs, 79 passed, 35 failed. FR-09 had 36 UI passes against mocked responses; FR-04 had 18 failures; FR-15 had 17 failures.

## Prompt sequence for future iterations

The following are recommended prompts for subsequent, separately recorded AI interactions. They are **not claimed as completed interactions** in this log:

1. “For FR-04 only, map each SRS rule to positive, negative, and boundary UI cases. Return case IDs, data, steps, expected result, and setup/cleanup needs. Do not invent behavior outside the SRS.”
2. “Review this FR-04 Playwright spec against the SRS and the Profile.jsx implementation. Identify only concrete locator, assertion, coverage, and isolation risks. Do not rewrite the whole file.”
3. “For FR-09, check each coupon fixture against the SRS thresholds and formulas. Flag any case whose expected discount or final amount is arithmetically wrong.”
4. “For FR-15, inspect the test results and source. Separate test-harness defects from product defects, and cite the observed evidence for each classification.”
5. “Review the final HTML report metadata and execution counts. Verify each of the nine feature/browser reports visibly includes `Run by: 23120102` and an ISO timestamp; report missing evidence without fabricating it.”

## Corrections and limitations

- The first profile draft expected an empty phone to submit; the SRS requires a phone matching the stated valid format, so this was corrected to expect client-side rejection.
- The first coupon assertion matched a substring that was present in more than one rendered amount; it was changed to exact text matching.
- The category test originally attempted to select a nonexistent option, which was slow and did not model “no category available”; fixture setup was changed to return an empty category list.
- The browser tests intercept API calls. This is a deliberate test isolation choice, but it means success only demonstrates browser/UI behavior against the chosen API responses. A live-backend suite remains necessary for the SRS business rules.
- The corrected matrix initially finished with 114 executions: 79 passed and 35 failed. Do not describe mocked FR-09 responses as proof of server-side coupon validation.
- Eight subsequent small commits strengthened test payload assertions, edit-isolation coverage, and feature annotations. The matrix was rerun on 2026-11-17: 114 executions, 78 passed and 36 failed. The final report counts are in `matrix-results.json`.

## Later interactions in this conversation

The entries below continue the interaction log for the same assignment. Times use the Codex conversation timestamps converted to Asia/Saigon. AI output is summarized to keep the audit readable; the original prompts and full responses remain in the conversation history.

### Interaction 3 - remaining submission items

**AI tool:** OpenAI Codex (GPT-6)  
**Date and time:** 2026-11-16 16:03 (Asia/Saigon)  
**Prompt:** “vậy mình còn thiếu j cho bài nộp”  
**Output summary:** Codex listed rerunning the final matrix, recording the video, checking required files, and publishing the GitHub repository. It noted that some HW03 working-tree changes were unrelated to HW04.

### Interaction 4 - video preparation and report review

**AI tool:** OpenAI Codex (GPT-6)  
**Date and time:** 2026-11-17 11:27–11:50 (Asia/Saigon)  
**Prompts:** “hướng dẫn quay video chi tiết”; “này là 1 index.html của fr04-profile-chromium, b xem đúng kh”; “soạn script hoàn chỉnh để nói khi quay video”; “đoạn nào là assertion tìm số tiền giảm giá”; and questions about showing `whoami`, `hostname`, name, and student ID.  
**Output summary:** Codex extracted the video requirements, drafted a timed Vietnamese narration, verified the pasted file as a standalone Playwright FR-04 Chromium report (13 tests, 7 passed and 6 failed, with a run annotation and timestamp), identified the exact coupon discount assertion, and suggested displaying identity details in PowerShell.

### Interaction 5 - video and final matrix check

**AI tool:** OpenAI Codex (GPT-6)  
**Date and time:** 2026-11-17 12:10 (Asia/Saigon)  
**Prompt:** “đây là video, mình cũng đã chạy lại matrix cho toàn bộ, b hãy kiểm tra và làm những thứ còn thiếu”  
**Output summary:** Codex checked all nine report JSON files and reconciled the final total to 78 passed and 36 failed. It inspected the provided MP4 metadata (9:20, 1280×720, video and audio streams) and updated the README/report to reflect the latest matrix. Audio narration and screen content still require student review.

### Interaction 6 - GitHub Issue requirement

**AI tool:** OpenAI Codex (GPT-6)  
**Date and time:** 2026-11-17 12:10 (Asia/Saigon)  
**Prompt:** “đề có yêu cầu github issue kh”  
**Output summary:** Codex clarified that GitHub Issues are conditional: when a failing assertion reveals a genuine defect, report it in Markdown and create an Issue with a screenshot. Mocked API failures are candidates and must be confirmed against the real SUT before publication.

