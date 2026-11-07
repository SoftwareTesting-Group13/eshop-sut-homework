# AI Audit Report

Tôi dùng AI cho các công việc sau:

- Đọc và tóm tắt yêu cầu HW03.
- Sinh bộ GUI checklist ban đầu cho Login, Register, Forgot Password và Profile bằng skill `ui-checklist-generator`.
- Review bộ ban đầu, bổ sung item còn thiếu và giải thích vì sao AI bỏ sót.
- Chạy checklist trên SUT local bằng Playwright và axe-core; chụp screenshot cho item Failed.
- Gom các failure thành bug report và chuẩn bị GitHub issue draft.
- Rà lại toàn bộ checklist, bug report và screenshot theo README/API spec; viết lại tài liệu tiếng Việt.
- Viết báo cáo Task 1, test summary và AI Audit Report này.

> **Ghi chú về phạm vi và bằng chứng:**
> - Bằng chứng hiện có: conversation hiện tại (ba prompt của người dùng và các phản hồi hiển thị của agent) cùng các artifact agent đã tạo trong repo. Không có bản export chat đầy đủ.
> - Số interaction được ghi: **3** (`AI-001`, `AI-002`, `AI-003`). Các tool call nội bộ (đọc file, chạy server, chạy Playwright) không phải prompt của người dùng nên không ghi thành interaction riêng.
> - AI tool có bằng chứng: **OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`)**. Không dùng AI tool nào khác.
> - Nguồn thời gian: conversation export không có timestamp. Vì vậy cả ba entry ghi **“Không có trong nguồn”**; ngày session 2026-11-07 lấy từ môi trường, không phải từ chat.
> - Trạng thái human review: checklist 66 item và 26 bug report là **bản nháp do agent tạo**. Sinh viên vẫn phải review, xác nhận bug và publish GitHub Issues. Báo cáo này không khẳng định human review đã xảy ra.
> - Agent không publish được GitHub Issues vì môi trường không có `gh` CLI/token. Draft và script publish nằm trong `features/GUI/issues/`.

---

## Interaction AI-001

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Ngày và giờ:** 2026-11-07 · **Không có trong nguồn**.
- **Nguồn:** Conversation hiện tại; không có transcript export.
- **Task:** Đọc đề HW03 và giải thích yêu cầu trước khi bắt đầu làm bài.

### Prompt của người dùng

```text
đọc @homework/hw03/docs/2026.HW03.GUI_Usability_En.md trước để hiểu yêu cầu của thầy t nhé
```

File đính kèm là `homework/hw03/docs/2026.HW03.GUI_Usability_En.md` (toàn bộ đề HW03).

### Output của AI

Agent trả lời bằng bản tóm tắt yêu cầu sau (nguyên văn):

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
- **Ngày và giờ:** 2026-11-07 · **Không có trong nguồn**.
- **Nguồn:** Conversation hiện tại; artifact trong `homework/hw03/ncuong/`.
- **Task:** Dùng skill `ui-checklist-generator` sinh hơn 40 item cho Login, Register, Forgot Password, Profile (FR-01…FR-04), chia theo IA-01…IA-04; thực thi Task 1; ghi AI audit log.

### Prompt của người dùng

```text
Dùng skill ui-checklist-generator @homework/hw03/ncuong/skills/ui-checklist-generator/ sinh ra >40 mục checklist cho 4 màn hình: Login, Register, Forgot Password, Profile. Chia rõ 4 nhóm IA-01, IA-02, IA-03, IA-04. 4 FR t chọn là FR 01, 02, 03, 04 nhé. Triển Task 1 trước dùm t. Làm xong nhớ ghi ai-audit log. @homework/hw03/ncuong/skills/
```

Thư mục đính kèm: `homework/hw03/ncuong/skills/ui-checklist-generator/` và `homework/hw03/ncuong/skills/` (bảy skill nháp).

### Output của AI

Agent tạo các artifact có thể kiểm tra sau (nội dung đầy đủ nằm trong repo; bảng này là danh mục output, không thay thế nội dung):

| Artifact | Đường dẫn | Nội dung |
| --- | --- | --- |
| Checklist AI ban đầu + review additions | `homework/hw03/ncuong/features/GUI/ai-checklist-and-review.md` | 44 item sinh từ tám nhóm của skill + 25 item bổ sung/sửa kèm lý do AI bỏ sót |
| Checklist đầy đủ (Markdown) | `homework/hw03/ncuong/features/GUI/checklist.md` | 66 item, nhóm IA, Passed/Failed, Notes, evidence |
| Checklist đầy đủ (Excel) | `homework/hw03/ncuong/features/GUI/checklist.xlsx` | Sheet Checklist + Summary + Execution, filter, màu kết quả |
| Kết quả máy đọc | `homework/hw03/ncuong/features/GUI/checklist.json` | Item, summary, phân nguồn, bug ID |
| Test summary | `homework/hw03/ncuong/features/GUI/test-summary.md` | Số screen/flow/item/passed/failed/bug/participant/video |
| Bug report | `homework/hw03/ncuong/features/GUI/bug-report.md` | 26 bug kèm severity, FR, màn hình, checklist ID, screenshot |
| Bug report riêng | `homework/hw03/ncuong/features/GUI/bugs/` | 26 file `BUG-GUI-*.md`: bước tái hiện, expected/actual, root cause, suggested fix, screenshot |
| GitHub issue draft | `homework/hw03/ncuong/features/GUI/issues/` | 26 file `BUG-GUI-*.md` + `issues.json` + `publish.sh`; publish bị chặn do thiếu GitHub auth |
| Screenshot | `homework/hw03/ncuong/features/GUI/screenshots/` | 38 PNG có annotation tiếng Việt cho 39 item Failed, kèm `manifest.json` |
| Script build | `homework/hw03/ncuong/features/GUI/tools/build_checklist.py`, `build_bugs.py` | Sinh lại Markdown/Excel/bug artifact |
| Báo cáo chính | `homework/hw03/ncuong/reports/main-report.md` | Task 1: phương pháp, review rationale, kết quả, phân tích |
| AI audit | `homework/hw03/ncuong/reports/ai-audit.md` | Báo cáo này |

Bộ artifact ban đầu có 69 item / 25 Passed / 44 Failed / 40 screenshot. Interaction AI-003 rà lại theo README và API spec, sau đó chốt số liệu cuối dưới đây.

Số liệu chính của bộ artifact cuối:

- **66 checklist item**: 18 IA-01, 17 IA-02, 15 IA-03, 16 IA-04.
- **41 item AI ban đầu được giữ + 25 item bổ sung/sửa sau review.**
- **Thực thi 66/66: 27 Passed, 39 Failed.**
- **26 bug:** 1 Blocker, 11 Major, 14 Minor.
- **38 screenshot** phủ 39 item Failed (một số ảnh dùng chung cho hai item).
- Môi trường: backend `localhost:3000`, web frontend `localhost:5173`, Chromium 158 / Playwright 1.65, axe-core 4.x, desktop 1280×900, mobile 360×800, 640×800 tương đương zoom 200%.

---

## Interaction AI-003

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Ngày và giờ:** 2026-11-07 · **Không có trong nguồn**.
- **Nguồn:** Conversation hiện tại; artifact trong `homework/hw03/ncuong/`.
- **Task:** Rà lại Task 1 theo README và API spec; sửa các điểm sai/ngoài phạm vi; viết lại toàn bộ tài liệu và screenshot bằng tiếng Việt, không bỏ sót.

### Prompt của người dùng

```text
Tiếp tục đi m, mấy cái ảnh kia còn tiếng anh thì sửa tiếng việt luôn nhé, làm kỹ lưỡng đầy đủ và không bỏ sót.
```

### Output của AI

Agent thực hiện một vòng review và sửa lại toàn bộ Task 1:

- **Đối chiếu lại checklist với README FR-01…FR-04, FR-21…FR-24 và API spec.** Loại các item ngoài phạm vi GUI của Task 1 (tab title, full-page reload, route guard, order cancel, success toast, `inputmode=tel`); sửa oracle của các item bị đánh giá sai (OTP hiển thị trong demo là đúng FR-03; lỗi đăng nhập generic là đúng FR-02; feedback cập nhật profile vẫn xác nhận thao tác).
- **Chốt checklist 66 item:** 41 item AI ban đầu được giữ + 25 item bổ sung/sửa; 27 Passed / 39 Failed.
- **Viết lại 26 bug report tiếng Việt**, mỗi bug có code block chứa đúng dòng source gây lỗi và link GitHub tới đúng dòng tại commit `85af3ba875c88283615e22cb108f13e2fccaf0e9`.
- **Chụp lại 38 screenshot** bằng Playwright; toàn bộ banner và annotation chuyển sang tiếng Việt; xóa ảnh cũ/không dùng; cập nhật `manifest.json`.
- **Viết lại** `reports/main-report.md`, `features/GUI/test-summary.md`, `README.md`, `reports/ai-audit.md`, `reports/ai-critique.md` bằng tiếng Việt với số liệu mới.
- **Sinh lại PDF** cho main report, AI audit và AI critique từ Markdown.

Kết quả sau review:

| Hạng mục | Trước review | Sau review |
| --- | ---: | ---: |
| Checklist item | 69 | 66 |
| Passed | 25 | 27 |
| Failed | 44 | 39 |
| Bug | 26 (2 Blocker / 12 Major / 12 Minor) | 26 (1 Blocker / 11 Major / 14 Minor) |
| Screenshot | 40 | 38 |

---

## Integrity check

| Kiểm tra | Kết quả |
| --- | --- |
| Mọi prompt truy cập được có output tương ứng | Có — AI-001, AI-002, AI-003 |
| Follow-up bị gộp vào một entry? | Không — ba prompt là ba entry riêng |
| Tên tool và model được ghi | Có — OpenCode agent, `DeepSeek V4.1 Flash Free` |
| Timestamp bị bịa? | Không — ghi “Không có trong nguồn” |
| Human correction bị thay bằng output AI? | Không — artifact là output của agent; human review của sinh viên vẫn đang chờ |
| Bằng chứng thiếu/không có được nêu rõ? | Có — không có transcript export, không có GitHub auth, chưa chạy Task 2/3 |
| Số interaction được ghi | 3 |
