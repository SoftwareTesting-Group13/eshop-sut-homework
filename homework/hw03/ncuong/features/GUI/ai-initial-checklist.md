# Checklist AI sinh ban đầu (trước khi review)

Sinh bằng skill `ui-checklist-generator` với 8 nhóm: layout, typography, colour, interaction, responsiveness, accessibility, product states, polish, trải trên 4 màn hình Login, Register, Forgot Password, Profile.

**44 item được sinh.** Sau review, **41 item được giữ** trong checklist cuối; 3 item bị loại vì ngoài phạm vi GUI Task 1:

- `CHK-30` — `inputmode=tel` là chi tiết implementation, không có trong README GUI requirements; validity của số điện thoại đã được CHK-31 bao phủ.
- `CHK-53` — success toast sau đăng ký không có trong FR-01; FR-01 chỉ yêu cầu chuyển về trang Đăng nhập (CHK-40).
- `CHK-69` — redirect người đã đăng nhập khỏi `/login` là route guard, không có trong README GUI requirements.

Một số oracle của bộ ban đầu đã được sửa trong review (heading phải là `<h1>`, lỗi đăng nhập phải generic, OTP được phép hiển thị trong demo, logout chỉ yêu cầu nhãn). Chi tiết ở [`review-additions.md`](review-additions.md).

Đây là bộ ban đầu được giữ lại để đối chiếu audit, không phải checklist cuối. Checklist cuối nằm ở [`checklist.md`](checklist.md).

| ID | IA | Màn hình | FR | Item |
| --- | --- | --- | --- | --- |
| CHK-01 | IA-01 | Login | FR-02 | Tiêu đề trang nêu đúng màn hình Đăng nhập và khớp với hành động đăng nhập. |
| CHK-03 | IA-01 | Login | FR-02 | Card đăng nhập dùng cùng alignment, spacing và typography với Register/Forgot Password. |
| CHK-04 | IA-01 | Login | FR-02 | Trang Đăng nhập không có horizontal scroll ở viewport 360px. |
| CHK-05 | IA-01 | Register | FR-01 | Tiêu đề trang nêu đúng màn hình Đăng ký. |
| CHK-08 | IA-01 | Register | FR-01 | Trang Đăng ký không có horizontal scroll ở viewport 360px. |
| CHK-09 | IA-01 | Forgot Password | FR-03 | Tiêu đề trang nêu đúng màn hình Quên mật khẩu. |
| CHK-11 | IA-01 | Forgot Password | FR-03 | Primary và secondary action ở bước 2 phân biệt được bằng mắt. |
| CHK-12 | IA-01 | Forgot Password | FR-03 | Trang Quên mật khẩu không có horizontal scroll ở viewport 360px. |
| CHK-17 | IA-02 | Login | FR-02 | Ô email/username dùng input type phù hợp với email. |
| CHK-18 | IA-02 | Login | FR-02 | Ô mật khẩu che ký tự đã nhập. |
| CHK-20 | IA-02 | Login | FR-02 | Trường bắt buộc được chặn bằng native validation khi submit rỗng. |
| CHK-21 | IA-02 | Register | FR-01 | Ô email dùng `type=email` và từ chối địa chỉ sai định dạng. |
| CHK-22 | IA-02 | Register | FR-01 | Ô mật khẩu che ký tự đã nhập. |
| CHK-24 | IA-02 | Register | FR-01 | Có trường xác nhận mật khẩu để tránh gõ nhầm. |
| CHK-25 | IA-02 | Forgot Password | FR-03 | Ô email dùng `type=email` và validate định dạng. |
| CHK-27 | IA-02 | Forgot Password | FR-03 | Ô mật khẩu mới che ký tự đã nhập. |
| CHK-28 | IA-02 | Forgot Password | FR-03 | Form đặt lại mật khẩu yêu cầu xác nhận mật khẩu. |
| CHK-29 | IA-02 | Profile | FR-04 | Ô email chỉ đọc và được ghi rõ là không thể sửa. |
| CHK-30 | IA-02 | Profile | FR-04 | Ô số điện thoại dùng `inputmode=tel` và giới hạn format. |
| CHK-33 | IA-03 | Login | FR-02 | Header toàn cục hiện diện và các link hoạt động trên trang Đăng nhập. |
| CHK-35 | IA-03 | Login | FR-02 | Link “Đăng ký ngay” điều hướng tới `/register`. |
| CHK-37 | IA-03 | Register | FR-01 | Header navigation hiện diện và nhất quán với Login. |
| CHK-38 | IA-03 | Register | FR-01 | Link “Đăng nhập” điều hướng tới `/login`. |
| CHK-39 | IA-03 | Register | FR-01 | Tab order theo đúng thứ tự thị giác. |
| CHK-40 | IA-03 | Register | FR-01 | Đăng ký thành công quay về trang Đăng nhập. |
| CHK-41 | IA-03 | Forgot Password | FR-03 | Quay lại bước 1 giữ nguyên email đã nhập. |
| CHK-42 | IA-03 | Forgot Password | FR-03 | Có đường quay lại đăng nhập từ màn hình Quên mật khẩu. |
| CHK-44 | IA-03 | Forgot Password | FR-03 | Bước 2 có step indicator (ví dụ 2/2). |
| CHK-46 | IA-03 | Profile | FR-04 | Header hiển thị trạng thái đã đăng nhập và link Profile hoạt động. |
| CHK-47 | IA-03 | Profile | FR-04 | Đăng xuất đưa người dùng về một trang công khai. |
| CHK-69 | IA-03 | Login | FR-02 | Người đã đăng nhập được chuyển khỏi `/login`. |
| CHK-49 | IA-04 | Login | FR-02 | Nút submit có loading/disabled state khi đang xác thực. |
| CHK-50 | IA-04 | Login | FR-02 | Lỗi đăng nhập hiển thị inline và được announce cho assistive technology. |
| CHK-51 | IA-04 | Login | FR-02 | Thông báo lỗi phân biệt sai thông tin, khóa tài khoản và lỗi mạng. |
| CHK-52 | IA-04 | Login | FR-02 | Đăng nhập thành công có phản hồi rõ và chuyển hướng. |
| CHK-53 | IA-04 | Register | FR-01 | Đăng ký thành công có phản hồi trước khi chuyển hướng. |
| CHK-54 | IA-04 | Register | FR-01 | Email trùng bị từ chối với thông báo dễ hiểu. |
| CHK-56 | IA-04 | Register | FR-01 | Nút submit có loading/disabled state khi đang đăng ký. |
| CHK-57 | IA-04 | Forgot Password | FR-03 | Yêu cầu OTP thành công được hiển thị rõ. |
| CHK-59 | IA-04 | Forgot Password | FR-03 | Lỗi email không tồn tại hiển thị inline, không blocking. |
| CHK-60 | IA-04 | Forgot Password | FR-03 | Phản hồi thành công/thất bại khi đặt lại mật khẩu rõ ràng. |
| CHK-61 | IA-04 | Profile | FR-04 | Cập nhật hồ sơ thành công được hiển thị inline và announce. |
| CHK-62 | IA-04 | Profile | FR-04 | Lịch sử đơn hàng có loading state. |
| CHK-68 | IA-04 | Profile | FR-04 | Trạng thái đơn hàng được truyền đạt bằng text, không chỉ bằng màu. |
