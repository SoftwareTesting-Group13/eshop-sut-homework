# Bug report — HW03 Task 1 (GUI checklist)

**Tổng số bug:** 26 · **Blocker:** 1 · **Major:** 11 · **Minor:** 14

Mỗi bug có báo cáo riêng trong [`bugs/`](bugs/) với bước tái hiện, Expected/Actual, screenshot và root cause kèm code block + link tới đúng dòng source.

| ID | Severity | FR | Màn hình | Checklist | Tiêu đề | Bug report |
| --- | --- | --- | --- | --- | --- | --- |
| BUG-GUI-14 | **Blocker** | FR-04 | `/profile` | CHK-31 | Regex số điện thoại từ chối số Việt Nam hợp lệ và dùng alert chặn | [chi tiết](bugs/BUG-GUI-14.md) |
| BUG-GUI-03 | **Major** | FR-21 | `/register, /profile` | CHK-07, CHK-16 | Text phụ và nút đỏ không đạt WCAG 2.2 AA về contrast | [chi tiết](bugs/BUG-GUI-03.md) |
| BUG-GUI-06 | **Major** | FR-04 | `/profile` | CHK-15 | Bảng lịch sử đơn hàng gây horizontal scroll ở viewport 360px | [chi tiết](bugs/BUG-GUI-06.md) |
| BUG-GUI-08 | **Major** | FR-02 | `/login` | CHK-17, CHK-18 | Ô email dùng `type=text` và ô mật khẩu hiển thị rõ ký tự | [chi tiết](bugs/BUG-GUI-08.md) |
| BUG-GUI-09 | **Major** | FR-22 | `/login, /register, /forgot-password, /profile` | CHK-19, CHK-32 | Input không có label liên kết bằng chương trình | [chi tiết](bugs/BUG-GUI-09.md) |
| BUG-GUI-10 | **Major** | FR-01 | `/register, /forgot-password` | CHK-21, CHK-25, CHK-54 | Không kiểm tra định dạng email và không chặn email trùng | [chi tiết](bugs/BUG-GUI-10.md) |
| BUG-GUI-11 | **Major** | FR-01 | `/register, /forgot-password` | CHK-23 | Nội dung mô tả password rule mâu thuẫn với regex thực tế | [chi tiết](bugs/BUG-GUI-11.md) |
| BUG-GUI-13 | **Major** | FR-03 | `/forgot-password` | CHK-26, CHK-44 | OTP chỉ có 4 chữ số, input không giới hạn và bước 2 thiếu step indicator | [chi tiết](bugs/BUG-GUI-13.md) |
| BUG-GUI-16 | **Major** | FR-21 | `/login` | CHK-36 | Tab order bắt đầu ở nút Sign In vì `tabIndex=1` | [chi tiết](bugs/BUG-GUI-16.md) |
| BUG-GUI-21 | **Major** | FR-22 | `/login, /forgot-password` | CHK-50, CHK-59, CHK-75 | Thông báo lỗi nằm dưới nút submit hoặc dùng alert chặn | [chi tiết](bugs/BUG-GUI-21.md) |
| BUG-GUI-23 | **Major** | FR-01 | `/register` | CHK-55 | UI render nguyên văn lỗi kỹ thuật từ server | [chi tiết](bugs/BUG-GUI-23.md) |
| BUG-GUI-25 | **Major** | FR-04 | `/profile` | CHK-62, CHK-63 | Loading và lỗi tải đơn hàng đều hiển thị thành “chưa có đơn hàng” | [chi tiết](bugs/BUG-GUI-25.md) |
| BUG-GUI-01 | **Minor** | FR-02 | `/login` | CHK-01 | Tiêu đề trang Đăng nhập ghi “Đăng Ký” thay vì “Đăng nhập” | [chi tiết](bugs/BUG-GUI-01.md) |
| BUG-GUI-04 | **Minor** | FR-03 | `/forgot-password` | CHK-11 | Hai nút ở bước 2 Quên mật khẩu trông giống hệt nhau | [chi tiết](bugs/BUG-GUI-04.md) |
| BUG-GUI-05 | **Minor** | FR-21 | `/register, /forgot-password, /profile` | CHK-05, CHK-09, CHK-13 | Ba màn hình Register, Forgot Password và Profile không có thẻ `<h1>` | [chi tiết](bugs/BUG-GUI-05.md) |
| BUG-GUI-07 | **Minor** | FR-21 | `/login, /register, /forgot-password, /profile` | CHK-65 | Layout không mirror khi document direction là RTL | [chi tiết](bugs/BUG-GUI-07.md) |
| BUG-GUI-12 | **Minor** | FR-01 | `/register, /forgot-password` | CHK-24, CHK-28 | Form đăng ký và đặt lại mật khẩu thiếu trường xác nhận mật khẩu | [chi tiết](bugs/BUG-GUI-12.md) |
| BUG-GUI-17 | **Minor** | FR-03 | `/forgot-password` | CHK-43 | Focus bị mất sau khi chuyển sang bước OTP | [chi tiết](bugs/BUG-GUI-17.md) |
| BUG-GUI-19 | **Minor** | FR-23 | `/profile` | CHK-48 | Navbar không chỉ ra trang hiện tại | [chi tiết](bugs/BUG-GUI-19.md) |
| BUG-GUI-20 | **Minor** | FR-01 | `/login, /register` | CHK-49, CHK-56 | Nút Login và Register không có loading/disabled state | [chi tiết](bugs/BUG-GUI-20.md) |
| BUG-GUI-27 | **Minor** | FR-22 | `/login, /register, /forgot-password, /profile` | CHK-70 | Không có ký hiệu `*` cạnh nhãn trường bắt buộc | [chi tiết](bugs/BUG-GUI-27.md) |
| BUG-GUI-28 | **Minor** | FR-21 | `/login` | CHK-71 | Login dùng “Username” và “Sign In” giữa giao diện tiếng Việt | [chi tiết](bugs/BUG-GUI-28.md) |
| BUG-GUI-29 | **Minor** | FR-23 | `/profile` | CHK-47 | Nút đăng xuất có nhãn “Thoát” thay vì “Đăng xuất” | [chi tiết](bugs/BUG-GUI-29.md) |
| BUG-GUI-30 | **Minor** | FR-24 | `/profile` | CHK-73 | Empty state lịch sử đơn hàng không có icon/hình minh họa | [chi tiết](bugs/BUG-GUI-30.md) |
| BUG-GUI-31 | **Minor** | FR-21 | `/register, /forgot-password` | CHK-74 | Nút hành động tích cực dùng màu đỏ/xanh lá thay vì xanh dương | [chi tiết](bugs/BUG-GUI-31.md) |
| BUG-GUI-32 | **Minor** | FR-23 | `/login, /register, /forgot-password, /profile` | CHK-80 | Link “Giỏ hàng” trên header không có badge số lượng | [chi tiết](bugs/BUG-GUI-32.md) |

## Ghi chú

- Screenshot chỉ tồn tại cho các item Failed; mỗi ảnh có banner đỏ ghi checklist ID và lỗi quan sát.
- 26 GitHub Issues đã publish: [#80–#105](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues?q=is%3Aissue+%5BBUG-GUI-). Danh sách máy đọc ở [`issues/published.json`](issues/published.json).
- Severity: **Blocker** = không thể hoàn thành tác vụ chính; **Major** = sai requirement rõ ràng hoặc cản trở đáng kể; **Minor** = lỗi hiển thị/nhất quán.
