# AI Audit Report

I use AI tools for the following tasks,

- Đọc đặc tả FR-02 và bộ skill Domain/EP + BVA, lập mô hình miền, thiết kế test case.
- Thiết lập instance SUT cách ly, thực thi các ca qua API, ghi evidence và đánh giá coverage.
- Soạn báo cáo feature FR02 (domain, boundary, catalog, results) và cập nhật master report/README.
- Soạn AI Audit Report này.

> **Phạm vi lập báo cáo (capture notes):**
> - Bằng chứng khả dụng: phiên hội thoại hiện tại (prompt của người dùng + các artifact do agent tạo trong repo); không có file export transcript riêng.
> - Số interaction đã ghi: **1** (một prompt chính của người dùng; các tool call nội bộ không phải prompt của người dùng nên không liệt kê).
> - Công cụ AI đã dùng (theo bằng chứng): OpenCode agent, model `DeepSeek V4.1 Flash Free` (provider `opencode`).
> - Trường còn thiếu: timestamp chính xác của prompt không có trong nguồn hội thoại; ngày phiên và giờ chạy lệnh lấy từ môi trường/terminal (xem bên dưới).
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

## Optional audit table (theo mẫu `[AI-02]` — bổ sung, không thay thế 4 trường bắt buộc)

| (1) Prompt + Công cụ | (2) Output AI | (3) Verdict | (4) Lý do | (5) Bản SV sửa |
| --- | --- | --- | --- | --- |
| OpenCode · DeepSeek V4.1 Flash Free · Time not available in source · “Tiến hành đọc @homework/hw02/ncuong/prompt.txt để triển khai test domain tesing cho feature 02: Login and account lockout nhé.” | Bộ artifact FR02 tại `features/FR02/` + cập nhật `reports/main-report.md`, `README.md` | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |

> Cột (3)–(5) do **sinh viên** tự đánh giá/điền; báo cáo không tự suy diễn verdict hay bản sửa của sinh viên.
