# AI Audit Report

> File mẫu trống. Thay `<...>` bằng nội dung thật. Luôn giữ đủ **4 trường bắt buộc của HW02 §9**:
> **tên công cụ AI · ngày giờ · prompt của bạn · output của AI**. Mỗi tương tác = một prompt đã gửi
> + một phản hồi tương ứng; prompt nối tiếp là một mục riêng, giữ đúng thứ tự. Không dùng thời điểm
> viết báo cáo làm thời điểm tương tác; thiếu timestamp thì ghi **“Time not available in source”**.
> Bảng `[AI-02]` ở cuối là **phần bổ sung**, không thay thế 4 trường bắt buộc.

I use AI tools for the following tasks,

- `<task 1 đã dùng AI>`
- `<task 2 đã dùng AI>`
- Soạn AI Audit Report này.

> **Phạm vi lập báo cáo (capture notes):**
> - Bằng chứng khả dụng: `<phiên hội thoại / transcript export / tool history / hồ sơ người dùng cấp>`
> - Số interaction đã ghi: `<n>`
> - Công cụ AI đã dùng (theo bằng chứng): `<...>`
> - Trường còn thiếu: `<... hoặc "không">`
> - Công cụ/phiên được nhắc tới nhưng không kiểm tra được: `<... hoặc "không">`

---

## Interaction AI-001

- **AI tool:** `<tên công cụ, model/version nếu biết>`
- **Date and time:** `<timestamp nguồn + timezone, hoặc "Time not available in source">`
- **Source:** `<tham chiếu hội thoại/export, nếu có>`
- **Task:** `<mục đích ngắn>`

### Your prompt

```text
<nguyên văn prompt của người dùng — KHÔNG paraphrase>
```

### The AI output

<nguyên văn output người dùng thấy; với non-text thì nêu artifact kèm đường dẫn/link mở kiểm tra được>

---

## Interaction AI-002

<lặp lại cấu trúc của AI-001 cho mỗi tương tác, theo đúng thứ tự xảy ra>

---

## Optional audit table (theo mẫu `[AI-02]` — bổ sung, không thay thế 4 trường bắt buộc)

| (1) Prompt + Công cụ | (2) Output AI | (3) Verdict | (4) Lý do | (5) Bản SV sửa |
| --- | --- | --- | --- | --- |
| `<tool · model · ngày giờ · prompt>` | `<artifact/output>` | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |

> Cột (3)–(5) do **sinh viên** tự đánh giá/điền; báo cáo không tự suy diễn verdict hay bản sửa của sinh viên.

<!-- Trường hợp KHÔNG dùng AI: chỉ ghi đúng câu khai báo
"I do not use any AI help in this exercise."
kèm ghi chú rằng người dùng đã xác nhận; KHÔNG tạo mục tương tác rỗng. -->
