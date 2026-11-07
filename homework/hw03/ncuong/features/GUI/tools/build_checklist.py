#!/usr/bin/env python3
"""Sinh artifact GUI checklist HW03 (Markdown + Excel + JSON + manifest).

Nguồn chân lý duy nhất cho 62 item sau review theo spec FR-21..FR-24 và
FR-01..FR-04. Chạy:
    python tools/build_checklist.py
"""
import json
import os
from collections import Counter, OrderedDict

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(BASE)

ITEMS = [
    # ================= IA-01 — General UI standards =================
    dict(id="CHK-01", ia="IA-01", fr="FR-02", screen="Login",
         item="Trang Đăng nhập có đúng một thẻ <h1> mô tả màn hình và tiêu đề khớp với hành động đăng nhập.",
         source="AI initial", result="Failed",
         notes="0 <h1>; tiêu đề là <h2>Đăng Ký</h2> thay vì Đăng nhập.",
         evidence="screenshots/CHK-01-login-heading.png", bug="BUG-GUI-01"),
    dict(id="CHK-03", ia="IA-01", fr="FR-02", screen="Login",
         item="Card đăng nhập dùng cùng alignment, spacing và typography với Register/Forgot Password.",
         source="AI initial", result="Passed",
         notes="Cả ba màn hình dùng max-w-md mx-auto mt-10 bg-white p-8 border rounded shadow-sm.",
         evidence="DOM inspection", bug=""),
    dict(id="CHK-04", ia="IA-01", fr="FR-02", screen="Login",
         item="Trang Đăng nhập không có horizontal scroll ở viewport 360px.",
         source="AI initial", result="Passed",
         notes="scrollWidth = clientWidth = 360.",
         evidence="Playwright viewport 360px", bug=""),
    dict(id="CHK-05", ia="IA-01", fr="FR-01", screen="Register",
         item="Trang Đăng ký có đúng một thẻ <h1> mô tả màn hình.",
         source="AI initial", result="Failed",
         notes="0 <h1>; chỉ có <h2>Đăng Ký Tài Khoản</h2>.",
         evidence="screenshots/CHK-05-register-h1.png", bug="BUG-GUI-05"),
    dict(id="CHK-07", ia="IA-01", fr="FR-01", screen="Register",
         item="Helper text và nút submit đạt WCAG 2.2 AA contrast (4.5:1 cho text thường).",
         source="Review addition", result="Failed",
         notes="axe-core: #9ca3af trên #ffffff = 2.53:1; trắng trên #ef4444 = 3.76:1.",
         evidence="screenshots/CHK-07-register-contrast.png", bug="BUG-GUI-03"),
    dict(id="CHK-08", ia="IA-01", fr="FR-01", screen="Register",
         item="Trang Đăng ký không có horizontal scroll ở viewport 360px.",
         source="AI initial", result="Passed",
         notes="scrollWidth = clientWidth = 360.",
         evidence="Playwright viewport 360px", bug=""),
    dict(id="CHK-09", ia="IA-01", fr="FR-03", screen="Forgot Password",
         item="Trang Quên mật khẩu có đúng một thẻ <h1> mô tả màn hình.",
         source="AI initial", result="Failed",
         notes="0 <h1>; chỉ có <h2>Quên Mật Khẩu</h2>.",
         evidence="screenshots/CHK-09-forgot-h1.png", bug="BUG-GUI-05"),
    dict(id="CHK-11", ia="IA-01", fr="FR-03", screen="Forgot Password",
         item="Ở bước 2, primary action nổi bật, dùng màu xanh dương theo FR-21 và phân biệt với secondary action.",
         source="AI initial", result="Failed",
         notes="“Đặt lại mật khẩu” và “← Quay lại” đều là nút xanh lá full-width, style giống nhau; primary không dùng màu xanh dương.",
         evidence="screenshots/CHK-11-forgot-buttons.png", bug="BUG-GUI-04"),
    dict(id="CHK-12", ia="IA-01", fr="FR-03", screen="Forgot Password",
         item="Trang Quên mật khẩu không có horizontal scroll ở viewport 360px.",
         source="AI initial", result="Passed",
         notes="scrollWidth = clientWidth = 360.",
         evidence="Playwright viewport 360px", bug=""),
    dict(id="CHK-13", ia="IA-01", fr="FR-04", screen="Profile",
         item="Trang Hồ sơ có đúng một thẻ <h1> và hierarchy heading hợp lý.",
         source="Review addition", result="Failed",
         notes="0 <h1>; hai <h2> (“Hồ sơ của bạn”, “Lịch sử đơn hàng”).",
         evidence="screenshots/CHK-13-profile-h1.png", bug="BUG-GUI-05"),
    dict(id="CHK-15", ia="IA-01", fr="FR-04", screen="Profile",
         item="Bảng lịch sử đơn hàng dùng được ở 360px, không tạo horizontal scroll cho cả trang.",
         source="Review addition", result="Failed",
         notes="scrollWidth 399px vs clientWidth 360px (overflow 39px); bảng 5 cột giữ width desktop.",
         evidence="screenshots/CHK-15-profile-mobile-table.png", bug="BUG-GUI-06"),
    dict(id="CHK-16", ia="IA-01", fr="FR-04", screen="Profile",
         item="Text và badge trạng thái đơn hàng đạt WCAG 2.2 AA contrast.",
         source="Review addition", result="Failed",
         notes="axe-core: #fde047 trên #2563eb = 3.92:1; trắng trên #ef4444 = 3.76:1.",
         evidence="screenshots/CHK-16-profile-contrast.png", bug="BUG-GUI-03"),
    dict(id="CHK-71", ia="IA-01", fr="FR-01..04", screen="All auth screens",
         item="Ngôn ngữ giao diện nhất quán tiếng Việt (trừ thuật ngữ kỹ thuật chuẩn) theo FR-21.",
         source="Review addition", result="Failed",
         notes="Login dùng “Username” và “Sign In” trong khi phần còn lại là tiếng Việt; các màn hình khác không có chuỗi tiếng Anh không cần thiết.",
         evidence="screenshots/CHK-71-login-language.png", bug="BUG-GUI-28"),
    dict(id="CHK-74", ia="IA-01", fr="FR-01, FR-03", screen="Register, Forgot Password",
         item="Các nút submit tích cực dùng màu xanh dương theo FR-21.",
         source="Review addition", result="Failed",
         notes="Register dùng bg-red-500 (#ef4444); bước 2 Forgot dùng bg-green-600; Login, Forgot bước 1 và Profile dùng xanh dương.",
         evidence="screenshots/CHK-74-button-color.png", bug="BUG-GUI-31"),
    dict(id="CHK-76", ia="IA-01", fr="FR-04", screen="Profile",
         item="Tổng tiền đơn hàng dùng ký hiệu ₫ và phân cách hàng nghìn theo FR-21.",
         source="Review addition", result="Passed",
         notes="Quan sát với order inject: “1.234.567 ₫”.",
         evidence="Playwright injected order", bug=""),
    dict(id="CHK-65", ia="IA-01", fr="FR-01..04", screen="All auth screens",
         item="Layout vẫn dùng được khi document direction là RTL.",
         source="Review addition", result="Failed",
         notes="Với dir=\"rtl\", utility vật lý giữ link “Quên mật khẩu?” ở bên phải và header không đảo; layout không mirror.",
         evidence="screenshots/CHK-65-login-rtl.png", bug="BUG-GUI-07"),
    dict(id="CHK-66", ia="IA-01", fr="FR-01..04", screen="All auth screens",
         item="Text vẫn đọc được khi hệ điều hành dùng dark mode.",
         source="Review addition", result="Passed",
         notes="Chưa có dark theme, nhưng card trắng và text đen vẫn đọc được với colorScheme=dark.",
         evidence="Playwright colorScheme=dark", bug=""),
    dict(id="CHK-67", ia="IA-01", fr="FR-01..04", screen="All auth screens",
         item="Nội dung reflow ở 200% zoom (640 CSS px) mà không có horizontal scroll.",
         source="Review addition", result="Passed",
         notes="Login, Register và Forgot Password đều có scrollWidth = clientWidth = 640.",
         evidence="Playwright viewport 640px", bug=""),

    # ================= IA-02 — Forms =================
    dict(id="CHK-17", ia="IA-02", fr="FR-02", screen="Login",
         item="Ô email/username dùng input type phù hợp với email (FR-02, FR-22).",
         source="AI initial", result="Failed",
         notes="type=\"text\" và label “Username”, trong khi backend xác thực bằng email.",
         evidence="screenshots/CHK-17-18-19-login-fields.png", bug="BUG-GUI-08"),
    dict(id="CHK-18", ia="IA-02", fr="FR-02", screen="Login",
         item="Ô mật khẩu che ký tự đã nhập (FR-22).",
         source="AI initial", result="Failed",
         notes="type=\"text\"; mật khẩu hiển thị rõ trên màn hình.",
         evidence="screenshots/CHK-17-18-19-login-fields.png", bug="BUG-GUI-08"),
    dict(id="CHK-19", ia="IA-02", fr="FR-02", screen="Login",
         item="Mọi input có label liên kết bằng chương trình (for/id hoặc aria-label).",
         source="Review addition", result="Failed",
         notes="Label không có for/id; axe-core báo 2 critical label violations.",
         evidence="screenshots/CHK-17-18-19-login-fields.png", bug="BUG-GUI-09"),
    dict(id="CHK-20", ia="IA-02", fr="FR-02", screen="Login",
         item="Trường bắt buộc được chặn bằng native validation khi submit rỗng.",
         source="AI initial", result="Passed",
         notes="Cả hai input có required; browser báo “Please fill out this field.” và focus ô trống đầu tiên.",
         evidence="Playwright native validation", bug=""),
    dict(id="CHK-21", ia="IA-02", fr="FR-01", screen="Register",
         item="Ô email dùng type=email và từ chối địa chỉ sai định dạng (FR-01, FR-22).",
         source="AI initial", result="Failed",
         notes="type=\"text\"; “not-an-email-<timestamp>” được chấp nhận và chuyển về /login.",
         evidence="screenshots/CHK-21-register-invalid-email.png", bug="BUG-GUI-10"),
    dict(id="CHK-22", ia="IA-02", fr="FR-01", screen="Register",
         item="Ô mật khẩu che ký tự đã nhập (FR-22).",
         source="AI initial", result="Passed",
         notes="type=\"password\".",
         evidence="DOM inspection", bug=""),
    dict(id="CHK-23", ia="IA-02", fr="FR-01", screen="Register",
         item="Nội dung mô tả password rule khớp với validation thực tế (FR-01: có ký tự đặc biệt).",
         source="Review addition", result="Failed",
         notes="Text hứa “ký tự đặc biệt” nhưng regex yêu cầu whitespace và chặn ký tự đặc biệt; “Abcd1234!” bị từ chối.",
         evidence="screenshots/CHK-23-register-password-rule.png", bug="BUG-GUI-11"),
    dict(id="CHK-24", ia="IA-02", fr="FR-01", screen="Register",
         item="Có trường xác nhận mật khẩu và chặn khi hai trường không khớp (FR-01).",
         source="AI initial", result="Failed",
         notes="Chỉ có một input mật khẩu.",
         evidence="screenshots/CHK-24-register-no-confirm.png", bug="BUG-GUI-12"),
    dict(id="CHK-25", ia="IA-02", fr="FR-03", screen="Forgot Password",
         item="Ô email dùng type=email và validate định dạng (FR-22).",
         source="AI initial", result="Failed",
         notes="type=\"text\"; email sai định dạng chỉ bị backend từ chối sau khi submit.",
         evidence="screenshots/CHK-25-forgot-email-type.png", bug="BUG-GUI-10"),
    dict(id="CHK-26", ia="IA-02", fr="FR-03", screen="Forgot Password",
         item="OTP gồm 6 chữ số (FR-03, SEC-07) và ô nhập giới hạn đúng 6 chữ số.",
         source="Review addition", result="Failed",
         notes="SUT sinh OTP 4 chữ số (“Mã OTP của bạn là: 2809”), label ghi “Mã OTP (4 số)”; input type=text, không maxlength/inputmode/pattern.",
         evidence="screenshots/CHK-26-forgot-otp-input.png", bug="BUG-GUI-13"),
    dict(id="CHK-27", ia="IA-02", fr="FR-03", screen="Forgot Password",
         item="Ô mật khẩu mới che ký tự đã nhập (FR-22).",
         source="AI initial", result="Passed",
         notes="type=\"password\".",
         evidence="DOM inspection", bug=""),
    dict(id="CHK-28", ia="IA-02", fr="FR-03", screen="Forgot Password",
         item="Bước 2 yêu cầu xác nhận mật khẩu mới (FR-03).",
         source="AI initial", result="Failed",
         notes="Chỉ có một input “Mật khẩu mới”.",
         evidence="screenshots/CHK-28-forgot-no-confirm.png", bug="BUG-GUI-12"),
    dict(id="CHK-29", ia="IA-02", fr="FR-04", screen="Profile",
         item="Email không thể chỉnh sửa qua giao diện (FR-04).",
         source="AI initial", result="Passed",
         notes="disabled + label “Email (Không đổi)”.",
         evidence="DOM inspection", bug=""),
    dict(id="CHK-31", ia="IA-02", fr="FR-04", screen="Profile",
         item="Số điện thoại được validate theo FR-04 (bắt đầu bằng 0, 10–11 chữ số) và lỗi hiển thị trên nút submit.",
         source="Review addition", result="Failed",
         notes="Regex /^[1-9][0-9]{8,9}$/ từ chối mọi số bắt đầu bằng 0, gồm placeholder 0912345678; lỗi dùng alert(), không nằm trên nút submit.",
         evidence="screenshots/CHK-31-profile-phone-alert.png", bug="BUG-GUI-14"),
    dict(id="CHK-32", ia="IA-02", fr="FR-04", screen="Profile",
         item="Mọi label của Profile liên kết bằng chương trình với input.",
         source="Review addition", result="Failed",
         notes="Cả bốn label thiếu for/id; axe-core báo critical label violations.",
         evidence="screenshots/CHK-32-profile-labels.png", bug="BUG-GUI-09"),
    dict(id="CHK-70", ia="IA-02", fr="FR-01..04", screen="All auth screens",
         item="Mọi trường bắt buộc có ký hiệu * bên cạnh nhãn (FR-22).",
         source="Review addition", result="Failed",
         notes="Không label nào có * dù tất cả input đều required.",
         evidence="screenshots/CHK-70-required-asterisk.png", bug="BUG-GUI-27"),
    dict(id="CHK-75", ia="IA-02", fr="FR-01..04", screen="All auth screens",
         item="Thông báo lỗi nằm trên nút submit, không nằm dưới (FR-22).",
         source="Review addition", result="Failed",
         notes="Login: error div nằm sau form, dưới nút Sign In. Register: error nằm trên form (đạt). Forgot/Profile: dùng alert(), không có inline message.",
         evidence="screenshots/CHK-75-error-position.png", bug="BUG-GUI-21"),

    # ================= IA-03 — Navigation =================
    dict(id="CHK-33", ia="IA-03", fr="FR-02", screen="Login",
         item="Header toàn cục hiện diện và các link hoạt động trên trang Đăng nhập.",
         source="AI initial", result="Passed",
         notes="Header có EShop, Giỏ hàng, Đăng nhập, Đăng ký; điều hướng đúng.",
         evidence="Playwright navigation", bug=""),
    dict(id="CHK-35", ia="IA-03", fr="FR-02", screen="Login",
         item="Link “Đăng ký ngay” điều hướng tới /register.",
         source="AI initial", result="Passed",
         notes="Điều hướng đúng.",
         evidence="Playwright navigation", bug=""),
    dict(id="CHK-36", ia="IA-03", fr="FR-02", screen="Login",
         item="Tab order theo đúng thứ tự thị giác từ trên xuống, trái sang phải (FR-21).",
         source="Review addition", result="Failed",
         notes="Nút Sign In có tabindex=\"1\" nên Tab đầu tiên focus vào nút, trước email/password.",
         evidence="screenshots/CHK-36-login-tab-order.png", bug="BUG-GUI-16"),
    dict(id="CHK-37", ia="IA-03", fr="FR-01", screen="Register",
         item="Header navigation hiện diện và nhất quán với Login.",
         source="AI initial", result="Passed",
         notes="Cùng link và style.",
         evidence="DOM inspection", bug=""),
    dict(id="CHK-38", ia="IA-03", fr="FR-01", screen="Register",
         item="Link “Đăng nhập” điều hướng tới /login.",
         source="AI initial", result="Passed",
         notes="Điều hướng đúng.",
         evidence="Playwright navigation", bug=""),
    dict(id="CHK-39", ia="IA-03", fr="FR-01", screen="Register",
         item="Tab order theo đúng thứ tự thị giác (FR-21).",
         source="AI initial", result="Passed",
         notes="Header → Họ Tên → Email → Mật khẩu → Đăng Ký → link đăng nhập.",
         evidence="Playwright keyboard test", bug=""),
    dict(id="CHK-40", ia="IA-03", fr="FR-01", screen="Register",
         item="Đăng ký thành công quay về trang Đăng nhập (FR-01).",
         source="AI initial", result="Passed",
         notes="navigate('/login') sau POST thành công.",
         evidence="Playwright registration flow", bug=""),
    dict(id="CHK-41", ia="IA-03", fr="FR-03", screen="Forgot Password",
         item="Quay lại bước 1 giữ nguyên email đã nhập.",
         source="AI initial", result="Passed",
         notes="Email state được giữ sau “← Quay lại”.",
         evidence="Playwright step-back test", bug=""),
    dict(id="CHK-42", ia="IA-03", fr="FR-03", screen="Forgot Password",
         item="Có đường quay lại đăng nhập từ màn hình Quên mật khẩu (FR-03).",
         source="AI initial", result="Passed",
         notes="Link “Đăng nhập” trên header.",
         evidence="DOM inspection", bug=""),
    dict(id="CHK-43", ia="IA-03", fr="FR-03", screen="Forgot Password",
         item="Focus được chuyển tới field đầu tiên của bước mới sau khi chuyển bước.",
         source="Review addition", result="Failed",
         notes="Sau “Lấy mã OTP”, document.activeElement là BODY; focus không vào ô OTP hay heading bước 2.",
         evidence="screenshots/CHK-43-forgot-focus.png", bug="BUG-GUI-17"),
    dict(id="CHK-44", ia="IA-03", fr="FR-03", screen="Forgot Password",
         item="Bước 2 có step indicator rõ ràng, ví dụ “Bước 2 / 2” (FR-03, FR-22).",
         source="AI initial", result="Failed",
         notes="Không có progress indicator hay số bước.",
         evidence="screenshots/CHK-44-forgot-step-indicator.png", bug="BUG-GUI-13"),
    dict(id="CHK-46", ia="IA-03", fr="FR-04", screen="Profile",
         item="Header hiển thị trạng thái đã đăng nhập và link Profile hoạt động.",
         source="AI initial", result="Passed",
         notes="“Chào, <name>” link tới /profile; có nút đăng xuất.",
         evidence="DOM inspection", bug=""),
    dict(id="CHK-47", ia="IA-03", fr="FR-04", screen="Profile",
         item="Nút đăng xuất có nhãn “Đăng xuất”, không phải “Thoát” (FR-23).",
         source="AI initial", result="Failed",
         notes="Nhãn quan sát: “Thoát”.",
         evidence="screenshots/CHK-47-logout-label.png", bug="BUG-GUI-29"),
    dict(id="CHK-48", ia="IA-03", fr="FR-04", screen="Profile",
         item="Navbar highlight trang hiện tại (FR-23).",
         source="Review addition", result="Failed",
         notes="Không có aria-current, active class hay trạng thái thị giác cho /profile.",
         evidence="screenshots/CHK-48-profile-active-nav.png", bug="BUG-GUI-19"),
    dict(id="CHK-80", ia="IA-03", fr="FR-01..04", screen="All auth screens",
         item="Link “Giỏ hàng” trên header hiển thị badge số lượng sản phẩm (FR-23).",
         source="Review addition", result="Failed",
         notes="Header chỉ có text “Giỏ hàng”; không có badge hay số lượng cạnh link.",
         evidence="screenshots/CHK-80-cart-badge.png", bug="BUG-GUI-32"),

    # ================= IA-04 — Feedback / state =================
    dict(id="CHK-49", ia="IA-04", fr="FR-02", screen="Login",
         item="Nút submit có loading/disabled state khi đang xác thực.",
         source="AI initial", result="Failed",
         notes="Khi delay /api/login, nút vẫn enabled, label “Sign In”, không spinner/aria-busy.",
         evidence="screenshots/CHK-49-login-loading.png", bug="BUG-GUI-20"),
    dict(id="CHK-50", ia="IA-04", fr="FR-02", screen="Login",
         item="Lỗi đăng nhập nằm trên nút submit và được announce cho assistive technology (FR-22).",
         source="AI initial", result="Failed",
         notes="Error div nằm sau form (dưới nút Sign In), không có role=\"alert\"/aria-live, không gắn với field.",
         evidence="screenshots/CHK-50-login-error.png", bug="BUG-GUI-21"),
    dict(id="CHK-51", ia="IA-04", fr="FR-02", screen="Login",
         item="Thông báo lỗi đăng nhập không tiết lộ nguyên nhân cụ thể (FR-02).",
         source="AI initial", result="Passed",
         notes="Chỉ hiển thị “Đăng nhập thất bại. Vui lòng kiểm tra lại.” cho mọi lỗi.",
         evidence="Playwright login flow", bug=""),
    dict(id="CHK-52", ia="IA-04", fr="FR-02", screen="Login",
         item="Đăng nhập thành công có phản hồi rõ và chuyển hướng.",
         source="AI initial", result="Passed",
         notes="Chuyển về / và header đổi thành “Chào, <name>”.",
         evidence="Playwright login flow", bug=""),
    dict(id="CHK-54", ia="IA-04", fr="FR-01", screen="Register",
         item="Email trùng bị từ chối với thông báo dễ hiểu (FR-01).",
         source="AI initial", result="Failed",
         notes="Đăng ký cùng email hai lần đều chuyển về /login, không báo lỗi; backend không có unique constraint.",
         evidence="screenshots/CHK-54-register-duplicate-email.png", bug="BUG-GUI-10"),
    dict(id="CHK-55", ia="IA-04", fr="FR-01", screen="Register",
         item="Lỗi server không lộ chi tiết kỹ thuật (SEC-04, FR-24).",
         source="Review addition", result="Failed",
         notes="Catch block render err.response.data.error trực tiếp; giả lập 500 hiện “SQLITE_ERROR: no such column: name”.",
         evidence="screenshots/CHK-55-register-raw-error.png", bug="BUG-GUI-23"),
    dict(id="CHK-56", ia="IA-04", fr="FR-01", screen="Register",
         item="Nút submit có loading/disabled state khi đang đăng ký.",
         source="AI initial", result="Failed",
         notes="Khi delay /api/register, nút vẫn enabled, label “Đăng Ký”, không aria-busy.",
         evidence="screenshots/CHK-56-register-loading.png", bug="BUG-GUI-20"),
    dict(id="CHK-57", ia="IA-04", fr="FR-03", screen="Forgot Password",
         item="Yêu cầu OTP thành công được hiển thị rõ.",
         source="AI initial", result="Passed",
         notes="Green box và bước 2 hiện ra sau khi request.",
         evidence="Playwright forgot-password flow", bug=""),
    dict(id="CHK-58", ia="IA-04", fr="FR-03", screen="Forgot Password",
         item="OTP được hiển thị trực tiếp trên màn hình trong môi trường demo (FR-03).",
         source="Review addition", result="Passed",
         notes="Bước 2 hiện “Mã OTP của bạn là: …” — đúng yêu cầu demo của FR-03.",
         evidence="Playwright forgot-password flow", bug=""),
    dict(id="CHK-59", ia="IA-04", fr="FR-03", screen="Forgot Password",
         item="Lỗi email không tồn tại hiển thị inline, không blocking, nằm trên nút submit (FR-22).",
         source="AI initial", result="Failed",
         notes="Dùng alert(“Lỗi: User not found”); không có inline message, field highlight hay live region.",
         evidence="screenshots/CHK-59-forgot-alert.png", bug="BUG-GUI-21"),
    dict(id="CHK-60", ia="IA-04", fr="FR-03", screen="Forgot Password",
         item="Phản hồi thành công/thất bại khi đặt lại mật khẩu rõ ràng.",
         source="AI initial", result="Passed",
         notes="Success alert + chuyển /login; failure alert hiện ra. Modality alert của lỗi được ghi nhận ở CHK-59.",
         evidence="Playwright forgot-password flow", bug=""),
    dict(id="CHK-61", ia="IA-04", fr="FR-04", screen="Profile",
         item="Cập nhật hồ sơ thành công có phản hồi rõ ràng cho người dùng.",
         source="AI initial", result="Passed",
         notes="Alert “Cập nhật thành công!” xác nhận thao tác đã lưu; item này chỉ chấm sự hiện diện của phản hồi.",
         evidence="Playwright profile update flow", bug=""),
    dict(id="CHK-62", ia="IA-04", fr="FR-04", screen="Profile",
         item="Lịch sử đơn hàng có loading state.",
         source="AI initial", result="Failed",
         notes="Khi delay /api/orders/my-orders, empty state “Bạn chưa có đơn hàng nào.” hiện ngay; không spinner/skeleton/aria-busy.",
         evidence="screenshots/CHK-62-profile-orders-loading.png", bug="BUG-GUI-25"),
    dict(id="CHK-63", ia="IA-04", fr="FR-04", screen="Profile",
         item="Lỗi tải đơn hàng được phân biệt với danh sách rỗng.",
         source="Review addition", result="Failed",
         notes="Response 500 đặt orders=[] và UI hiện “Bạn chưa có đơn hàng nào.”; không error/retry.",
         evidence="screenshots/CHK-63-profile-orders-error.png", bug="BUG-GUI-25"),
    dict(id="CHK-68", ia="IA-04", fr="FR-04", screen="Profile",
         item="Trạng thái đơn hàng được truyền đạt bằng text, không chỉ bằng màu.",
         source="AI initial", result="Passed",
         notes="statusLabel() map mỗi status sang text tiếng Việt cạnh badge màu.",
         evidence="DOM inspection", bug=""),
    dict(id="CHK-73", ia="IA-04", fr="FR-04", screen="Profile",
         item="Empty state có icon/hình minh họa và message thân thiện (FR-24).",
         source="Review addition", result="Failed",
         notes="Chỉ có <p>Bạn chưa có đơn hàng nào.</p>, không icon/hình minh họa.",
         evidence="screenshots/CHK-73-empty-state.png", bug="BUG-GUI-30"),
]

# ---- kiểm tra tính nhất quán ----
ids = [i["id"] for i in ITEMS]
assert len(ids) == len(set(ids)), "duplicate IDs"
assert len(ITEMS) > 40, len(ITEMS)

summary = OrderedDict()
for ia in ["IA-01", "IA-02", "IA-03", "IA-04"]:
    rows = [i for i in ITEMS if i["ia"] == ia]
    summary[ia] = {
        "total": len(rows),
        "passed": sum(1 for i in rows if i["result"] == "Passed"),
        "failed": sum(1 for i in rows if i["result"] == "Failed"),
        "screens": sorted({i["screen"] for i in rows}),
    }

source_counts = Counter(i["source"] for i in ITEMS)
result_counts = Counter(i["result"] for i in ITEMS)
bug_ids = sorted({i["bug"] for i in ITEMS if i["bug"]})

# ---- JSON ----
with open(os.path.join(OUT, "checklist.json"), "w", encoding="utf-8") as f:
    json.dump({"items": ITEMS, "summary": summary,
               "source_counts": source_counts, "result_counts": result_counts,
               "bugs": bug_ids}, f, ensure_ascii=False, indent=2)

# ---- manifest cho screenshots ----
manifest = []
for i in ITEMS:
    if i["result"] == "Failed" and i["evidence"].startswith("screenshots/"):
        manifest.append({"file": i["evidence"], "ids": [i["id"]],
                         "title": i["item"], "detail": i["notes"]})
manifest.append({
    "file": "screenshots/CHK-74-forgot-button-color.png",
    "ids": ["CHK-74"],
    "title": "Nút tích cực ở bước 2 Forgot dùng màu xanh lá",
    "detail": "“Đặt lại mật khẩu” và “← Quay lại” đều dùng bg-green-600; primary không dùng màu xanh dương theo FR-21.",
})
with open(os.path.join(OUT, "screenshots", "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

# ---- Markdown: checklist ----
lines = []
lines.append("# GUI Checklist — Login, Register, Forgot Password, Profile\n")
lines.append("**SUT:** EShop (http://localhost:5173) · **FR:** FR-01, FR-02, FR-03, FR-04 · **Interface aspects:** IA-01…IA-04\n")
lines.append("**Ngày thực thi:** 2026-11-07 · **Browser:** Chromium 158 (Playwright 1.65) · **Viewport:** 1280×900; mobile 360×800.\n")
lines.append("**Căn cứ:** README FR-21…FR-24 (GUI), FR-01…FR-04 (chức năng trên 4 màn hình), API specification.\n")
lines.append("\n## Tổng hợp\n")
lines.append("| Interface aspect | Items | Passed | Failed |")
lines.append("| --- | ---: | ---: | ---: |")
for ia, s in summary.items():
    lines.append(f"| {ia} | {s['total']} | {s['passed']} | {s['failed']} |")
lines.append(f"| **Tổng** | **{len(ITEMS)}** | **{result_counts['Passed']}** | **{result_counts['Failed']}** |")
lines.append(f"\nPhân nguồn: **{source_counts['AI initial']} item AI ban đầu** + **{source_counts['Review addition']} item bổ sung/sửa sau review**. Bug ID: {', '.join(bug_ids)}.\n")

titles = {"IA-01": "IA-01 — General UI standards",
          "IA-02": "IA-02 — Forms",
          "IA-03": "IA-03 — Navigation",
          "IA-04": "IA-04 — Feedback / state"}
for ia in ["IA-01", "IA-02", "IA-03", "IA-04"]:
    lines.append(f"\n## {titles[ia]}\n")
    lines.append("| ID | Màn hình | FR | Checklist item | Nguồn | Kết quả | Ghi chú / lý do fail | Evidence |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for i in ITEMS:
        if i["ia"] != ia:
            continue
        res = "**Failed**" if i["result"] == "Failed" else "Passed"
        notes = i["notes"].replace("|", "\\|")
        ev = f"[{os.path.basename(i['evidence'])}]({i['evidence']})" if i["evidence"].startswith("screenshots/") else i["evidence"]
        lines.append(f"| {i['id']} | {i['screen']} | {i['fr']} | {i['item']} | {i['source']} | {res} | {notes} | {ev} |")

lines.append("\n## Ghi chú thực thi\n")
lines.append("- SUT chạy local: backend `http://localhost:3000`, web frontend `http://localhost:5173`.")
lines.append("- Hành vi chức năng được điều khiển bằng Playwright 1.65 (Chromium 158); DOM/ARIA facts đọc từ trang live.")
lines.append("- Evidence accessibility dùng axe-core 4.x; contrast ratio là số tính bởi axe-core, không ước lượng bằng mắt.")
lines.append("- Mobile dùng viewport 360×800. Screenshot chỉ chụp cho item Failed, có banner đỏ ghi ID và lỗi quan sát.")
lines.append("- Item Failed không tự động là bug: một số là design gap; bug list chỉ gồm defect tái hiện được.")
lines.append("- Ngoài phạm vi Task 1: order state machine (FR-10), coupon (FR-09), cart (FR-07), admin (FR-12…FR-19), mobile (FR-20), route guard/SPA reload/tab title/RTL/dark mode/zoom vì không có trong spec GUI.")

with open(os.path.join(OUT, "checklist.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

# ---- Markdown: review additions + corrections + removals ----
add = [i for i in ITEMS if i["source"] == "Review addition"]
rationale = {
    "CHK-07": "AI viết “đủ contrast” nhưng không tính ratio; axe-core tìm ra 2.53:1 và 3.76:1.",
    "CHK-13": "AI coi heading là typography, không kiểm tra outline h1/h2.",
    "CHK-15": "AI viết “mobile usable” chung chung, không test bảng dữ liệu 5 cột.",
    "CHK-16": "Như CHK-07: AI không tính contrast cho badge trạng thái và header.",
    "CHK-19": "AI kiểm tra label hiển thị, không kiểm tra for/id hoặc aria-label.",
    "CHK-23": "AI không so sánh copy password rule với regex thực tế; mâu thuẫn chỉ lộ khi đọc cả hai.",
    "CHK-26": "AI lấy label “4 số” của SUT thay vì đọc FR-03/SEC-07 yêu cầu OTP 6 chữ số.",
    "CHK-31": "AI chỉ kiểm tra “có lỗi”, không kiểm tra regex có nhận số Việt Nam hợp lệ và vị trí lỗi.",
    "CHK-32": "Như CHK-19: label hiển thị được coi là đủ.",
    "CHK-36": "AI không chạy keyboard-only test; tabindex=\"1\" không thấy trong screenshot.",
    "CHK-43": "AI bỏ sót focus management sau step transition của form 2 bước.",
    "CHK-48": "AI không kiểm tra aria-current/active state của navbar.",
    "CHK-55": "AI không test server-error path nên bỏ sót raw error leakage.",
    "CHK-58": "AI coi OTP hiển thị là lỗi, nhưng FR-03 cho phép hiển thị trong môi trường demo; review sửa thành pass.",
    "CHK-63": "AI kiểm tra empty state nhưng không phân biệt error với empty list.",
    "CHK-70": "AI bỏ sót yêu cầu dấu * cho trường bắt buộc (FR-22).",
    "CHK-71": "AI bỏ sót yêu cầu nhất quán ngôn ngữ tiếng Việt (FR-21).",
    "CHK-73": "AI bỏ sót yêu cầu empty state có icon/hình minh họa (FR-24).",
    "CHK-74": "AI bỏ sót quy tắc nút tích cực dùng màu xanh dương (FR-21).",
    "CHK-75": "AI bỏ sót yêu cầu thông báo lỗi nằm trên nút submit (FR-22).",
    "CHK-76": "AI bỏ sót yêu cầu định dạng tiền ₫ và phân cách hàng nghìn (FR-21).",
    "CHK-65": "AI mặc định layout LTR, không thử dir=\"rtl\"; đây là ví dụ điển hình về item AI thường bỏ sót.",
    "CHK-66": "AI mặc định light mode, không kiểm tra colorScheme=dark.",
    "CHK-67": "AI mặc định 100% zoom, không kiểm tra reflow ở 200% (640 CSS px).",
    "CHK-80": "AI chỉ kiểm tra nội dung từng trang, bỏ sót yêu cầu badge giỏ hàng trên header toàn cục (FR-23).",
}
lines = ["# Review additions — các item AI bỏ sót hoặc làm sai\n",
         f"Sau review theo README FR-21…FR-24, checklist cuối có **{len(ITEMS)} item**: "
         f"**{source_counts['AI initial']} item AI ban đầu** và **{source_counts['Review addition']} item bổ sung/sửa**. "
         "Bộ AI ban đầu (44 item được sinh, 41 item được giữ sau review) nằm trong `ai-initial-checklist.md` để đối chiếu audit.\n",
         "## 1. Item bổ sung mới\n",
         "| ID | IA | Màn hình | Item bổ sung | Vì sao AI bỏ sót |",
         "| --- | --- | --- | --- | --- |"]
for i in add:
    lines.append(f"| {i['id']} | {i['ia']} | {i['screen']} | {i['item']} | {rationale.get(i['id'], 'Xem báo cáo.')} |")

lines += ["\n## 2. Item AI làm sai và đã sửa\n",
          "| ID | AI ban đầu | Vấn đề | Cách sửa |",
          "| --- | --- | --- | --- |",
          "| CHK-01, CHK-05, CHK-09, CHK-13 | Chỉ kiểm tra text heading | FR-21 yêu cầu đúng một `<h1>` mỗi trang; cả 4 trang dùng `<h2>` | Đổi oracle sang `<h1>` + nội dung heading |",
          "| CHK-11 | Chỉ kiểm tra primary/secondary khác nhau | FR-21 quy định nút tích cực màu xanh dương | Thêm ràng buộc màu xanh dương cho primary action |",
          "| CHK-17, CHK-18, CHK-21, CHK-25 | “Input type phù hợp” | FR-22 quy định chính xác `type=email` và `type=password` | Ghi rõ type trong oracle |",
          "| CHK-26 | OTP 4 chữ số | FR-03 và SEC-07 yêu cầu OTP 6 chữ số | Sửa oracle thành 6 chữ số và giới hạn input 6 chữ số |",
          "| CHK-47 | Logout phải redirect | FR-23 chỉ quy định nhãn “Đăng xuất”, không quy định redirect | Đổi oracle sang nhãn nút |",
          "| CHK-51 | Lỗi phải phân biệt sai mật khẩu/khóa/mạng | FR-02 yêu cầu “không để lộ chi tiết nguyên nhân” | Đảo oracle: thông báo generic là pass |",
          "| CHK-58 | OTP không được hiển thị | FR-03 cho phép hiển thị OTP trong môi trường demo | Đảo oracle: hiển thị OTP là pass |",
          "| CHK-60 | Không ghi rõ modality | Alert là blocking nhưng item này chỉ chấm clarity | Ghi chú alert modality thuộc CHK-59 |"]

lines += ["\n## 3. Item bị loại vì ngoài phạm vi Task 1\n",
          "| ID cũ | Lý do loại |",
          "| --- | --- |",
          "| CHK-02, CHK-06, CHK-10, CHK-14 | Browser tab title không có trong spec GUI |",
          "| CHK-30 | `inputmode=tel` không có trong spec; validity của số điện thoại đã được CHK-31 cover |",
          "| CHK-34 | Full page reload là chi tiết implementation, không phải yêu cầu GUI |",
          "| CHK-45, CHK-69 | Route guard/redirect không có trong spec GUI |",
          "| CHK-53 | Success toast khi đăng ký không có trong spec; FR-01 chỉ yêu cầu redirect (CHK-40) |",
          "| CHK-64 | Hủy đơn là business rule FR-10, ngoài FR-01…FR-04 của Task 1 |"]

with open(os.path.join(OUT, "review-additions.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

# ---- Excel ----
try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    ws.title = "Checklist"
    headers = ["ID", "IA", "FR", "Màn hình", "Checklist item", "Nguồn", "Kết quả", "Ghi chú / lý do fail", "Evidence", "Bug ID"]
    ws.append(headers)
    header_fill = PatternFill("solid", fgColor="1F4E78")
    header_font = Font(bold=True, color="FFFFFF")
    thin = Side(style="thin", color="BFBFBF")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border
    pass_fill = PatternFill("solid", fgColor="E2EFDA")
    fail_fill = PatternFill("solid", fgColor="FCE4D6")
    for i in ITEMS:
        ws.append([i["id"], i["ia"], i["fr"], i["screen"], i["item"], i["source"],
                   i["result"], i["notes"], i["evidence"], i["bug"]])
        r = ws.max_row
        for c in range(1, len(headers) + 1):
            cell = ws.cell(row=r, column=c)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = border
        ws.cell(row=r, column=7).fill = pass_fill if i["result"] == "Passed" else fail_fill
        ws.cell(row=r, column=7).font = Font(bold=True)
    widths = [9, 8, 9, 18, 62, 15, 10, 60, 46, 14]
    for idx, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(idx)].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:J{ws.max_row}"
    ws.row_dimensions[1].height = 28

    ws2 = wb.create_sheet("Summary")
    ws2.append(["Interface aspect", "Items", "Passed", "Failed"])
    for c in range(1, 5):
        cell = ws2.cell(row=1, column=c)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = border
        cell.alignment = Alignment(horizontal="center")
    for ia, s in summary.items():
        ws2.append([ia, s["total"], s["passed"], s["failed"]])
    ws2.append(["Tổng", len(ITEMS), result_counts["Passed"], result_counts["Failed"]])
    for row in ws2.iter_rows(min_row=1, max_row=ws2.max_row, max_col=4):
        for cell in row:
            cell.border = border
            cell.alignment = Alignment(horizontal="center", vertical="center")
    ws2.cell(row=ws2.max_row, column=1).font = Font(bold=True)
    for idx, w in enumerate([22, 10, 10, 10], start=1):
        ws2.column_dimensions[get_column_letter(idx)].width = w

    ws3 = wb.create_sheet("Execution")
    ws3.append(["Field", "Value"])
    for k, v in [
        ("SUT", "EShop — frontend-web"),
        ("URL", "http://localhost:5173"),
        ("FR", "FR-01, FR-02, FR-03, FR-04"),
        ("Màn hình", "Login, Register, Forgot Password, Profile"),
        ("Interface aspects", "IA-01, IA-02, IA-03, IA-04"),
        ("Căn cứ", "README FR-21…FR-24 và API specification"),
        ("Browser", "Chromium 158 (Playwright 1.65)"),
        ("Viewport", "1280×900 desktop; 360×800 mobile"),
        ("Ngày", "2026-11-07"),
        ("Tổng item", len(ITEMS)),
        ("Passed", result_counts["Passed"]),
        ("Failed", result_counts["Failed"]),
        ("AI ban đầu", source_counts["AI initial"]),
        ("Bổ sung/sửa sau review", source_counts["Review addition"]),
        ("Bug", len(bug_ids)),
    ]:
        ws3.append([k, v])
    ws3.column_dimensions["A"].width = 26
    ws3.column_dimensions["B"].width = 80

    wb.save(os.path.join(OUT, "checklist.xlsx"))
    print("wrote checklist.xlsx")
except ImportError as e:
    print("openpyxl not available:", e)

print(f"items={len(ITEMS)} passed={result_counts['Passed']} failed={result_counts['Failed']}")
print("sources:", dict(source_counts))
print("bugs:", len(bug_ids))
