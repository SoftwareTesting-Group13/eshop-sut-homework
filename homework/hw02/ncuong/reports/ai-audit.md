# AI Audit Report

I use AI tools for the following tasks,

- Đọc đặc tả FR-02 và bộ skill Domain/EP + BVA, lập mô hình miền, thiết kế test case.
- Thiết lập instance SUT cách ly, thực thi các ca qua API, ghi evidence và đánh giá coverage.
- Soạn báo cáo feature FR02 (domain, boundary, catalog, results) và cập nhật master report/README.
- Tạo GitHub Issue cho 2 bug đã được sinh viên xác nhận, đính screenshot vào báo cáo và issue.
- Xóa 2 issue cũ và tạo lại theo template mới của skill `test-findings-report-writer` sau khi template được bổ sung.
- Soạn AI Audit Report này.

> **Phạm vi lập báo cáo (capture notes):**
> - Bằng chứng khả dụng: phiên hội thoại hiện tại (prompt của người dùng + các artifact do agent tạo trong repo); không có file export transcript riêng. Hai screenshot (`features/FR02/screenshots/BUG-FR02-01.png`, `BUG-FR02-02.png`) do **người dùng** cung cấp, không phải AI tạo.
> - Số interaction đã ghi: **3** (ba prompt của người dùng; các tool call nội bộ không phải prompt của người dùng nên không liệt kê).
> - Công cụ AI đã dùng (theo bằng chứng): OpenCode agent, model `DeepSeek V4.1 Flash Free` (provider `opencode`).
> - Trường còn thiếu: AI-002 và AI-003 không có timestamp cho prompt trong nguồn hội thoại; AI-001 dùng timestamp do người dùng cung cấp (2026-10-20 00:25 +0700). Ngày phiên và giờ chạy lệnh lấy từ môi trường/terminal.
> - Công cụ/phiên được nhắc tới nhưng không kiểm tra được: không.

---

## Interaction AI-001

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time: 2026-10-20 00:25 +0700**.
- **Source:** Phiên hội thoại hiện tại (không có transcript export).
- **Task:** Triển khai toàn bộ quy trình Domain Testing + BVA cho FR-02 (Login and account lockout) theo `homework/hw02/ncuong/prompt.txt` và đề HW02.

### Your prompt

```text
Tiến hành đọc @homework/hw02/ncuong/prompt.txt để triển khai test domain tesing cho feature 02: Login and account lockout nhé.
```

Phần đính kèm của prompt là toàn văn file `homework/hw02/ncuong/prompt.txt` (nội dung người dùng cung cấp trong cùng lượt gửi; file còn trong repo để đối chiếu nguyên văn), bắt đầu bằng:

```text
# Prompt kiểm thử Domain/EP + BVA cho một feature HW02

## Cấu hình duy nhất cần đổi

TARGET_FEATURE_ID: FR02
```

### The AI output

Output của agent là bộ artifact tạo/cập nhật trong repo (nội dung đầy đủ, kiểm tra được):

| Artifact | Đường dẫn |
| --- | --- |
| Domain analysis (EP) | `homework/hw02/ncuong/features/FR02/domain-analysis.md` |
| Boundary analysis (BVA) | `homework/hw02/ncuong/features/FR02/boundary-analysis.md` |
| Test case catalog | `homework/hw02/ncuong/features/FR02/test-cases.md` |
| Test results + bug + coverage | `homework/hw02/ncuong/features/FR02/test-results.md` |
| Evidence log + log thô | `homework/hw02/ncuong/features/FR02/evidence/` |
| Quan sát ngoài EP/BVA | `homework/hw02/ncuong/supporting-materials/fr02-observations.md` |
| Master report cập nhật | `homework/hw02/ncuong/reports/main-report.md` |
| README cập nhật | `homework/hw02/ncuong/README.md` |

Tóm tắt kết quả agent đã tạo (số liệu nằm trong các file trên): 15 T-ID; 15 đã chạy; 11 PASS, 3 FAIL, 1 Quan sát, 0 BLOCKED, 0 chưa chạy; 2 bug ứng viên `BUG-FR02-01` và `BUG-FR02-02` đang chờ sinh viên xác nhận. Agent không tự mở GitHub Issue, không tự chụp screenshot, không điền AI Gap Analysis hay AI Critique.

> Phản hồi cuối của agent cho người dùng là bản tóm tắt bàn giao (số ca, coverage, bug, câu hỏi mở, trạng thái AI Audit); toàn bộ nội dung kỹ thuật chi tiết nằm trong các artifact liên kết ở trên. Các thông điệp tool nội bộ (đọc file, chạy lệnh) không phải output người dùng thấy nên không chép vào đây.

---

## Interaction AI-002

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time:** Time not available in source (ngày phiên: 2026-10-20, theo môi trường).
- **Source:** Phiên hội thoại hiện tại; screenshot người dùng cung cấp tại `homework/hw02/ncuong/features/FR02/screenshots/`.
- **Task:** Cập nhật báo cáo với 2 screenshot đã được sinh viên xác nhận và tạo GitHub Issue (kèm ảnh) cho từng bug theo `features/FR02/test-results.md`; ghi lại kết quả vào file và cập nhật AI Audit.

### Your prompt

```text
T vừa thêm 2 bức ảnh screenshot xác nhận 2 bug mà m đã phát hiện. Và t xác nhận 2 bug này. Thêm vào báo cáo 2 bức ảnh đó và tạo issue cho mỗi bug dựa trên @homework/hw02/ncuong/features/FR02/test-results.md. Sau đó ghi lại vào file nhé (Issue phải đầy đủ tương tự test-result, có đủ thông tin report bug kèm ảnh đã đính). Xong nhớ ai audit log @homework/hw02/ncuong/skills/ai-audit-logger/SKILL.md
```

### The AI output

Agent đã (nội dung kiểm tra được trong repo và trên GitHub):

- Push screenshot do người dùng cung cấp lên nhánh `ncuong` (commit `test(FR02): add bug confirmation screenshots for BUG-FR02-01/02`).
- Tạo 2 GitHub Issue kèm ảnh nhúng:
    - [#23 [BUG-FR02-01] Bộ đếm đăng nhập sai tăng 2 thay vì 1 → khóa tài khoản sau 2 lần sai](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/23)
    - [#24 [BUG-FR02-02] Thời lượng khóa tài khoản là 180 giây thay vì 30 giây](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/24)
- Lưu toàn văn nội dung issue tại `homework/hw02/ncuong/features/FR02/issues/BUG-FR02-01.md` và `BUG-FR02-02.md`.
- Cập nhật trạng thái bug/Issue và ảnh vào `features/FR02/test-results.md`, `features/FR02/evidence/FR02-evidence.md`, `reports/main-report.md`, `README.md`.

---

## Interaction AI-003

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time:** Time not available in source (ngày phiên: 2026-10-20, theo môi trường).
- **Source:** Phiên hội thoại hiện tại; template do người dùng bổ sung tại `homework/hw02/ncuong/skills/test-findings-report-writer/assets/github-issue-template.md`.
- **Task:** Xóa 2 GitHub Issue đã tạo ở AI-002 (#23, #24) và tạo lại cho từng bug theo template issue mới; ghi lại vào file và cập nhật AI Audit.

### Your prompt

```text
Xóa 2 issues vừa làm, tạo lại 2 issue đó nha. Vì t vừa bổ sung thêm bộ skills template issue @homework/hw02/ncuong/skills/test-findings-report-writer/assets/github-issue-template.md nên tôi cần bỏ 2 issue cũ và làm lại với template mới này. AI Audit report sau khi xong nhé
```

### The AI output

Agent đã (nội dung kiểm tra được trong repo và trên GitHub):

- Xóa 2 Issue cũ #23 và #24 bằng GraphQL `deleteIssue` (đã kiểm tra danh sách issue không còn FR-02 nào ngoài 2 issue mới).
- Viết lại hoàn toàn `features/FR02/issues/BUG-FR02-01.md` và `BUG-FR02-02.md` theo đúng 5 mục của template (Tóm tắt + bảng Metadata, Chuẩn bị để tái hiện, Các bước tái hiện và kết quả, Bằng chứng, Điều tra nguyên nhân), không để lại placeholder.
- Tạo lại 2 GitHub Issue kèm ảnh nhúng:
    - [#25 BUG-FR02-01 — Bộ đếm đăng nhập sai tăng 2 thay vì 1 khiến tài khoản bị khóa sớm sau 2 lần sai](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/25)
    - [#26 BUG-FR02-02 — Thời lượng khóa tài khoản là 180 giây thay vì 30 giây](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/26)
- Cập nhật lại link Issue (#25/#26) và lệnh tái hiện trong `features/FR02/test-results.md`, `features/FR02/evidence/FR02-evidence.md`, `reports/main-report.md`, `README.md`.

---

## Optional audit table (theo mẫu `[AI-02]` — bổ sung, không thay thế 4 trường bắt buộc)

| (1) Prompt + Công cụ | (2) Output AI | (3) Verdict | (4) Lý do | (5) Bản SV sửa |
| --- | --- | --- | --- | --- |
| OpenCode · DeepSeek V4.1 Flash Free · Time not available in source · “Tiến hành đọc @homework/hw02/ncuong/prompt.txt để triển khai test domain tesing cho feature 02: Login and account lockout nhé.” | Bộ artifact FR02 tại `features/FR02/` + cập nhật `reports/main-report.md`, `README.md` | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| OpenCode · DeepSeek V4.1 Flash Free · Time not available in source · “T vừa thêm 2 bức ảnh screenshot xác nhận 2 bug … Xong nhớ ai audit log …” | Issue #23, #24 kèm screenshot; cập nhật `test-results.md`, `FR02-evidence.md`, `main-report.md`, `README.md`; lưu issue tại `features/FR02/issues/` | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| OpenCode · DeepSeek V4.1 Flash Free · Time not available in source · “Xóa 2 issues vừa làm, tạo lại 2 issue đó nha … làm lại với template mới này …” | Xóa #23/#24; viết lại `issues/*.md` theo template mới; tạo Issue #25, #26 kèm screenshot; cập nhật link trong `test-results.md`, `FR02-evidence.md`, `main-report.md`, `README.md` | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |

> Cột (3)–(5) do **sinh viên** tự đánh giá/điền; báo cáo không tự suy diễn verdict hay bản sửa của sinh viên.
