# <FEATURE_CODE> — Boundary analysis (BVA)

**Feature / interface:** `<mã feature; API hoặc UI thực sự được kiểm thử>`  
**Nguồn yêu cầu:** `<file §mục>`

## B1 — <tên ngưỡng hoặc quan hệ cần kiểm tra>

**Rule:** `<R-ID: quy tắc trực tiếp từ đặc tả>`  
**Biên:** `<ngưỡng; dấu bằng thuộc phía nào; đơn vị và bước/độ chính xác>`  
**Setup chung:** `<trạng thái trước test và các input giữ cố định>`

| Điểm | Giá trị/trạng thái cần tạo | Expected | Test case | Khả năng thử |
| --- | --- | --- | --- | --- |
| Ngay dưới | `<giá trị>` | `<hành vi>` | `<T-ID>` | `<Khả thi/Không thể + lý do>` |
| Tại biên | `<giá trị>` | `<hành vi>` | `<T-ID>` | `<Khả thi/Không thể + lý do>` |
| Ngay trên | `<giá trị>` | `<hành vi>` | `<T-ID>` | `<Khả thi/Không thể + lý do>` |

`<Chỉ giữ các điểm có ý nghĩa cho biên này; có thể dùng ON/IN/OUT nếu rõ hơn. Với điểm không thể tạo hoặc quan sát, ghi Không có case, lý do và không tính đã phủ. Chỉ thêm chú thích cho setup hoặc độ chính xác khó nhìn từ bảng. Lặp lại khối B2, B3... cho các biên khác.>`

## Coverage BVA

| Nghĩa vụ biên | Khả thi | Có case | Đã chạy đúng điểm có evidence | Đạt oracle | Còn thiếu / không quan sát được |
| --- | ---: | ---: | ---: | ---: | --- |
| `<B-ID + điểm>` | `<n>` | `<n>` | `<n hoặc Chưa chạy>` | `<n hoặc Chưa chạy>` | `<điểm + lý do>` |

`<Ghi rõ các điểm trong mẫu số. Chỉ tính đã chạy khi evidence cho thấy SUT thực sự ở giá trị/trạng thái đã thiết kế; Actual sai không biến thành một điểm đầu vào khác. Chi tiết Actual và bug nằm ở test-results.md.>`
