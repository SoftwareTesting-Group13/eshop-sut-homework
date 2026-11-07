# AI Critique

**Bản nháp — sinh viên cần review trước khi nộp.**

AI hữu ích về độ phủ nhưng không đáng tin khi làm oracle. Nó mở rộng tám nhóm của skill `ui-checklist-generator` thành 44 item và sinh Markdown, Excel, bug report nhất quán. Nhưng nó sai đúng ở những chỗ quyết định chất lượng review GUI. Nó coi `<label>` hiển thị là label accessible, bỏ qua việc thiếu `for`/`id`; nói “kiểm tra contrast” mà không tính ratio, trong khi axe-core tìm ra 2.53:1, 3.76:1 và 3.92:1. Nó mặc định LTR, light mode, zoom 100%, nên RTL, dark mode và reflow 200% chỉ xuất hiện sau khi tôi bổ sung. Nó cũng không thấy `tabIndex={1}` đẩy focus vào nút Sign In, focus mất sau bước OTP, response 500 hiển thị thành danh sách rỗng, regex số điện thoại từ chối số Việt Nam hợp lệ, hay copy password rule mâu thuẫn với regex. Ngược lại, bản đầu còn xếp OTP demo và vài mục ngoài phạm vi Task 1 thành lỗi; review sau đã sửa.

Ba nguyên nhân giải thích điều này. Thứ nhất, prompt yêu cầu checklist chứ không yêu cầu oracle thực thi được, nên AI viết câu chung không thể chấm Pass/Fail. Thứ hai, model không chạy được SUT: không nhấn Tab, không delay request, không chặn response 500 hay đọc `document.activeElement`. Thứ ba, model bám theo happy path thị giác và giả định của developer: LTR, theme sáng, label nhìn thấy là đủ.

Bài học: AI chỉ nên là bên sinh ứng viên, không phải bằng chứng. Con người phải định nghĩa oracle, chạy edge case và chất vấn giả định accessibility. Output của AI chỉ đáng tin sau khi được thực thi và review.
