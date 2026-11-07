#!/usr/bin/env bash
set -euo pipefail
# Publish 26 issue drafts. Yêu cầu: gh auth login và đã push nhánh ncuong (để raw screenshot URL hoạt động).
cd "$(dirname "$0")"
command -v gh >/dev/null || { echo "gh CLI chưa cài; cài gh rồi chạy lại."; exit 1; }
gh auth status >/dev/null || { echo "Chưa đăng nhập gh; chạy 'gh auth login'."; exit 1; }

gh issue create --title "[BUG-GUI-14] Regex số điện thoại từ chối số Việt Nam hợp lệ và dùng alert chặn" --body-file BUG-GUI-14.md --label bug --label blocker --label ia-02
gh issue create --title "[BUG-GUI-03] Text phụ và nút đỏ không đạt WCAG 2.2 AA về contrast" --body-file BUG-GUI-03.md --label bug --label major --label ia-01
gh issue create --title "[BUG-GUI-06] Bảng lịch sử đơn hàng gây horizontal scroll ở viewport 360px" --body-file BUG-GUI-06.md --label bug --label major --label ia-01
gh issue create --title "[BUG-GUI-08] Ô email dùng `type=text` và ô mật khẩu hiển thị rõ ký tự" --body-file BUG-GUI-08.md --label bug --label major --label ia-02
gh issue create --title "[BUG-GUI-09] Input không có label liên kết bằng chương trình" --body-file BUG-GUI-09.md --label bug --label major --label ia-02
gh issue create --title "[BUG-GUI-10] Không kiểm tra định dạng email và không chặn email trùng" --body-file BUG-GUI-10.md --label bug --label major --label ia-02 --label ia-04
gh issue create --title "[BUG-GUI-11] Nội dung mô tả password rule mâu thuẫn với regex thực tế" --body-file BUG-GUI-11.md --label bug --label major --label ia-02
gh issue create --title "[BUG-GUI-13] OTP chỉ có 4 chữ số, input không giới hạn và bước 2 thiếu step indicator" --body-file BUG-GUI-13.md --label bug --label major --label ia-02 --label ia-03
gh issue create --title "[BUG-GUI-16] Tab order bắt đầu ở nút Sign In vì `tabIndex=1`" --body-file BUG-GUI-16.md --label bug --label major --label ia-03
gh issue create --title "[BUG-GUI-21] Thông báo lỗi nằm dưới nút submit hoặc dùng alert chặn" --body-file BUG-GUI-21.md --label bug --label major --label ia-04
gh issue create --title "[BUG-GUI-23] UI render nguyên văn lỗi kỹ thuật từ server" --body-file BUG-GUI-23.md --label bug --label major --label ia-04
gh issue create --title "[BUG-GUI-25] Loading và lỗi tải đơn hàng đều hiển thị thành “chưa có đơn hàng”" --body-file BUG-GUI-25.md --label bug --label major --label ia-04
gh issue create --title "[BUG-GUI-01] Tiêu đề trang Đăng nhập ghi “Đăng Ký” thay vì “Đăng nhập”" --body-file BUG-GUI-01.md --label bug --label minor --label ia-01
gh issue create --title "[BUG-GUI-04] Hai nút ở bước 2 Quên mật khẩu trông giống hệt nhau" --body-file BUG-GUI-04.md --label bug --label minor --label ia-01
gh issue create --title "[BUG-GUI-05] Ba màn hình Register, Forgot Password và Profile không có thẻ `<h1>`" --body-file BUG-GUI-05.md --label bug --label minor --label ia-01
gh issue create --title "[BUG-GUI-07] Layout không mirror khi document direction là RTL" --body-file BUG-GUI-07.md --label bug --label minor --label ia-01
gh issue create --title "[BUG-GUI-12] Form đăng ký và đặt lại mật khẩu thiếu trường xác nhận mật khẩu" --body-file BUG-GUI-12.md --label bug --label minor --label ia-02
gh issue create --title "[BUG-GUI-17] Focus bị mất sau khi chuyển sang bước OTP" --body-file BUG-GUI-17.md --label bug --label minor --label ia-03
gh issue create --title "[BUG-GUI-19] Navbar không chỉ ra trang hiện tại" --body-file BUG-GUI-19.md --label bug --label minor --label ia-03
gh issue create --title "[BUG-GUI-20] Nút Login và Register không có loading/disabled state" --body-file BUG-GUI-20.md --label bug --label minor --label ia-04
gh issue create --title "[BUG-GUI-27] Không có ký hiệu `*` cạnh nhãn trường bắt buộc" --body-file BUG-GUI-27.md --label bug --label minor --label ia-02
gh issue create --title "[BUG-GUI-28] Login dùng “Username” và “Sign In” giữa giao diện tiếng Việt" --body-file BUG-GUI-28.md --label bug --label minor --label ia-01
gh issue create --title "[BUG-GUI-29] Nút đăng xuất có nhãn “Thoát” thay vì “Đăng xuất”" --body-file BUG-GUI-29.md --label bug --label minor --label ia-03
gh issue create --title "[BUG-GUI-30] Empty state lịch sử đơn hàng không có icon/hình minh họa" --body-file BUG-GUI-30.md --label bug --label minor --label ia-04
gh issue create --title "[BUG-GUI-31] Nút hành động tích cực dùng màu đỏ/xanh lá thay vì xanh dương" --body-file BUG-GUI-31.md --label bug --label minor --label ia-01
gh issue create --title "[BUG-GUI-32] Link “Giỏ hàng” trên header không có badge số lượng" --body-file BUG-GUI-32.md --label bug --label minor --label ia-03
