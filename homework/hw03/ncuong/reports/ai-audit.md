# AI Audit Report

I use AI tools for the following tasks,

- Reading and summarizing the HW03 requirements.
- Generating an initial GUI checklist for Login, Register, Forgot Password and Profile with the `ui-checklist-generator` skill.
- Reviewing the initial set, adding missing items, and explaining why the AI missed them.
- Running the checklist against the local SUT with Playwright and axe-core, capturing screenshots for failed items.
- Grouping failures into bug reports and preparing GitHub issue drafts.
- Writing the Task 1 report, test summary and this AI Audit Report.

> **Capture notes (scope and evidence):**
> - Available evidence: the current conversation (two user prompts and the agent's visible replies) and the artifacts the agent created in this repository. No exported chat transcript is available.
> - Interactions logged: **2** (`AI-001`, `AI-002`). Internal tool calls (reading files, starting servers, running Playwright) are not user prompts and are not logged as separate interactions.
> - AI tool evidenced: **OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`)**. No other AI tool was used.
> - Time source: the conversation export does not contain timestamps. Both entries therefore say **“Time not available in source”**; the session date is 2026-11-07 from the environment, not from the chat.
> - Human review status: the 69-item checklist and the 26 bug reports are **agent-produced drafts**. The student still has to review them, confirm the bugs, and publish the GitHub issues. This report does not claim that review happened.
> - The agent could not publish GitHub Issues because this environment has no `gh` CLI/token. The drafts and a publish script are in `features/GUI/issues/`.

---

## Interaction AI-001

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time:** 2026-11-07 · **Time not available in source**.
- **Source:** Current conversation; no exported transcript.
- **Task:** Read the HW03 specification and explain the requirements before starting the assignment.

### Your prompt

```text
đọc @homework/hw03/docs/2026.HW03.GUI_Usability_En.md trước để hiểu yêu cầu của thầy t nhé
```

The attached file was `homework/hw03/docs/2026.HW03.GUI_Usability_En.md` (the full HW03 specification).

### The AI output

The agent replied with the following requirement summary (verbatim):

```markdown
## Tóm tắt HW03

**SUT:** EShop (`ttbhanh/eshop-sut`) — web frontend, admin web, mobile app. UI được chia 4 interface aspect: **IA-01 General UI**, **IA-02 Forms**, **IA-03 Navigation**, **IA-04 Feedback/State**.

### Task 1 — GUI Checklist (30đ)
- Checklist **> 40 item**, phủ đủ 4 IA.
- Quy trình bắt buộc: dùng AI sinh bộ ban đầu → **tự review**, bổ sung item AI bỏ sót → với mỗi item tự thêm phải **giải thích tại sao AI missed** (prompt, model limit, đặc thù UI...).
- Thực thi checklist trên SUT: mỗi item **Passed/Failed** + cột **Notes** lý do fail.
- **Chỉ chụp screenshot cho item Failed**.
- Bug phải báo ở **cả Markdown report và GitHub Issues**, mỗi issue có screenshot.
- Nên chọn nhiều screen (1 screen khó đủ 40 item chất lượng).

### Task 2 — Usability Evaluation (40đ)
- Chọn **1 end-to-end flow**, chạy **7 participant thật**, 7 session riêng.
- Phase 1: objectives, task scenario dạng goal-oriented (không chỉ từng bước), instrument **SUS hoặc UEQ-S** + câu hỏi mở về **clarity, error recovery, speed, trust**, tuyển 7 người **ngoài lớp**, che 4 số giữa liên hệ, **chạy pilot 1 người** rồi tinh chỉnh.
- Phase 2: think-aloud, quan sát trung lập, quay màn hình/audio có consent, ghi chú friction/hesitation/error.
- Phase 3: tính điểm SUS/UEQ-S, gom pain point, phân biệt bug lẻ vs systemic issue, **severity ranking**, báo bug lên GitHub Issues.
- TA có thể gọi ngẫu nhiên 2 participant để xác minh — **không được bịa**.

### Task 3 — Cross-Browser/Platform (20đ)
- Chạy lại Task 1 trên **≥ 3 platform**: Chrome, Firefox, Safari (hoặc Android Chrome); **Expo Go trên điện thoại thật được tính thay 1 platform**.
- Ưu tiên BrowserStack/LambdaTest trial; nếu hết trial thì dùng cloud khác hoặc thiết bị thật, miễn screenshot thể hiện rõ browser/OS/device + URL localhost.
- Screenshot phải overlay **username dạng email sinh viên**. Lưu ý §11 còn yêu cầu **student ID + full name** → nên overlay cả hai cho chắc.

### Các phần bắt buộc khác
- **Agent Skills** (10đ) + video demo YouTube end-to-end.
- **AI Audit Report** đầy đủ: tool, ngày giờ, prompt, output.
- **AI Critique 200–300 từ**.
- **Git commit cho từng bước** + file git commit log.
- **README.md** có bảng self-assessment + test summary (số screen/flow, item designed/executed/passed/failed, số bug, số participant, video).
- Nộp zip đúng format `<StudentID>_HW03_AI_GUIUsability_<3 số>.zip`, gồm report MD+PDF, Excel checklist, evidence 7 session, screenshot cross-platform...
- Cấm trùng screen/flow với thành viên khác trong nhóm; cấm copy prompt.

## Hiện trạng repo
`homework/hw03/ncuong/` mới có `skills/` (7 skill đã nháp), còn `features/` và `reports/` đang trống. Source SUT đã có sẵn (`frontend-web`, `frontend-admin`, `frontend-mobile`, `backend`).

## Cần bạn xác nhận để mình bắt tay vào làm
1. **Student ID + họ tên + username email** (để đặt tên file và overlay screenshot).
2. **Screen nào** bạn chọn cho checklist? (cần tránh trùng với bạn cùng nhóm)
3. **Flow nào** cho usability test? (cũng cần không trùng nhóm)
4. Bạn **đã có 7 participant** chưa, hay cần mình soạn kế hoạch/template để bạn đi tuyển?
5. Bạn **đã có trial BrowserStack/LambdaTest** chưa?
6. Bạn muốn mình bắt đầu ngay từ **Task 1** (sinh checklist + review + cấu trúc report), hay dựng khung toàn bộ deliverable trước?
```

---

## Interaction AI-002

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time:** 2026-11-07 · **Time not available in source**.
- **Source:** Current conversation; artifacts in `homework/hw03/ncuong/`.
- **Task:** Use the `ui-checklist-generator` skill to generate more than 40 checklist items for Login, Register, Forgot Password and Profile (FR-01…FR-04), split across IA-01…IA-04; execute Task 1; write the AI Audit Report.

### Your prompt

```text
Dùng skill ui-checklist-generator @homework/hw03/ncuong/skills/ui-checklist-generator/ sinh ra >40 mục checklist cho 4 màn hình: Login, Register, Forgot Password, Profile. Chia rõ 4 nhóm IA-01, IA-02, IA-03, IA-04. 4 FR t chọn là FR 01, 02, 03, 04 nhé. Triển Task 1 trước dùm t. Làm xong nhớ ghi ai-audit log. @homework/hw03/ncuong/skills/
```

Attached directories: `homework/hw03/ncuong/skills/ui-checklist-generator/` and `homework/hw03/ncuong/skills/` (the seven draft skills).

### The AI output

The agent produced the following inspectable artifacts (the full content is in the repository; this is the complete output set, not a substitute for it):

| Artifact | Path | Content |
| --- | --- | --- |
| AI initial checklist | `homework/hw03/ncuong/features/GUI/ai-initial-checklist.md` | 44 items generated from the skill's eight categories |
| Review additions | `homework/hw03/ncuong/features/GUI/review-additions.md` | 25 added items, each with the reason the AI missed it |
| Full checklist (Markdown) | `homework/hw03/ncuong/features/GUI/checklist.md` | 69 items, IA groups, Passed/Failed, Notes, evidence links |
| Full checklist (Excel) | `homework/hw03/ncuong/features/GUI/checklist.xlsx` | Checklist + Summary + Execution sheets, filters, colour-coded results |
| Machine-readable results | `homework/hw03/ncuong/features/GUI/checklist.json` | Items, summary, source split, bug IDs |
| Test summary | `homework/hw03/ncuong/features/GUI/test-summary.md` | Screens/flows/items/passed/failed/bugs/participants/demo-video counts |
| Bug report | `homework/hw03/ncuong/features/GUI/bug-report.md` | 26 bugs with severity, FR, screen, checklist IDs and screenshots |
| Individual bug reports | `homework/hw03/ncuong/features/GUI/bugs/BUG-GUI-01.md` … `BUG-GUI-26.md` | Steps, expected/actual, root cause, suggested fix, screenshot |
| GitHub issue drafts | `homework/hw03/ncuong/features/GUI/issues/BUG-GUI-01.md` … `BUG-GUI-26.md`, `issues.json`, `publish.sh` | Ready-to-publish issue bodies; publication blocked by missing GitHub auth |
| Screenshots | `homework/hw03/ncuong/features/GUI/screenshots/` | 40 annotated PNGs covering all 44 failed items, plus `manifest.json` |
| Build scripts | `homework/hw03/ncuong/features/GUI/tools/build_checklist.py`, `build_bugs.py` | Reproducible generation of the Markdown/Excel/bug artifacts |
| Main report | `homework/hw03/ncuong/reports/main-report.md` | Task 1 report with method, review rationale, results and analysis |
| AI audit | `homework/hw03/ncuong/reports/ai-audit.md` | This report |

Key numbers produced by the agent:

- **69 checklist items**: 19 IA-01, 16 IA-02, 17 IA-03, 17 IA-04.
- **44 AI-initial items + 25 review additions.**
- **Executed 69/69: 25 Passed, 44 Failed.**
- **26 bugs:** 2 Blocker, 12 Major, 12 Minor.
- **40 screenshots** covering all failed items.
- Execution environment: EShop backend on `localhost:3000`, web frontend on `localhost:5173`, Chromium 158 / Playwright 1.65, axe-core 4.x, 1280×900 desktop, 360×800 mobile, 640×800 zoom equivalent.

Finalization performed by the agent after the artifact build:

- Repaired the malformed YAML frontmatter in `skills/ui-checklist-generator/SKILL.md` (the description string was unterminated, so the skill could not load).
- Added the missing `skills/cross-browser-testing/prompts/cross-browser-testing.md` referenced by that skill, and verified all Markdown links resolve.
- Committed the work in five logical commits and wrote `homework/hw03/ncuong/git-commit-log.txt`.
- Re-rendered the three report PDFs after the final consistency fixes.

What the agent did **not** do (and did not claim to do):

- It did not publish the GitHub Issues (no `gh` CLI/token in the environment).
- It did not run Task 2 (no participants, no SUS/UEQ-S, no sessions).
- It did not run Task 3 (no Firefox/Safari/Expo Go runs).
- It did not perform the student's human review of the 69 items or the 26 bugs; the artifacts are drafts for that review.

---

## Integrity check

| Check | Result |
| --- | --- |
| Every accessible prompt has a matching output | Yes — AI-001 and AI-002 |
| Follow-ups collapsed into one entry? | No — the two user prompts are separate |
| Tool name and model recorded | Yes — OpenCode agent, `DeepSeek V4.1 Flash Free` |
| Timestamps invented? | No — marked “Time not available in source” |
| Human corrections substituted for AI output? | No — the artifacts are the agent's output; student review is explicitly pending |
| Missing/unavailable evidence stated? | Yes — no transcript export, no GitHub auth, no Task 2/3 runs |
| Number of interactions logged | 2 |
