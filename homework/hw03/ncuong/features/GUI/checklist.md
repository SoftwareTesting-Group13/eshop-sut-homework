# GUI Checklist — Login, Register, Forgot Password, Profile

**SUT:** EShop (http://localhost:5173) · **FR:** FR-01, FR-02, FR-03, FR-04 · **Interface aspects:** IA-01…IA-04

**Ngày thực thi:** 2026-11-07 · **Browser:** Chromium 158 (Playwright 1.65) · **Viewport:** 1280×900; mobile 360×800.

**Căn cứ:** README FR-21…FR-24 (GUI), FR-01…FR-04 (chức năng trên 4 màn hình), API specification.


## Tổng hợp

| Interface aspect | Items | Passed | Failed |
| --- | ---: | ---: | ---: |
| IA-01 | 18 | 7 | 11 |
| IA-02 | 17 | 4 | 13 |
| IA-03 | 15 | 9 | 6 |
| IA-04 | 16 | 7 | 9 |
| **Tổng** | **66** | **27** | **39** |

Phân nguồn: **41 item AI ban đầu** + **25 item bổ sung/sửa sau review**. Bug ID: BUG-GUI-01, BUG-GUI-03, BUG-GUI-04, BUG-GUI-05, BUG-GUI-06, BUG-GUI-07, BUG-GUI-08, BUG-GUI-09, BUG-GUI-10, BUG-GUI-11, BUG-GUI-12, BUG-GUI-13, BUG-GUI-14, BUG-GUI-16, BUG-GUI-17, BUG-GUI-19, BUG-GUI-20, BUG-GUI-21, BUG-GUI-23, BUG-GUI-25, BUG-GUI-27, BUG-GUI-28, BUG-GUI-29, BUG-GUI-30, BUG-GUI-31, BUG-GUI-32.


## IA-01 — General UI standards

| ID | Màn hình | FR | Checklist item | Nguồn | Kết quả | Ghi chú / lý do fail | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-01 | Login | FR-02 | Trang Đăng nhập có đúng một thẻ <h1> mô tả màn hình và tiêu đề khớp với hành động đăng nhập. | AI initial | **Failed** | 0 <h1>; tiêu đề là <h2>Đăng Ký</h2> thay vì Đăng nhập. | [CHK-01-login-heading.png](screenshots/CHK-01-login-heading.png) |
| CHK-03 | Login | FR-02 | Card đăng nhập dùng cùng alignment, spacing và typography với Register/Forgot Password. | AI initial | Passed | Cả ba màn hình dùng max-w-md mx-auto mt-10 bg-white p-8 border rounded shadow-sm. | DOM inspection |
| CHK-04 | Login | FR-02 | Trang Đăng nhập không có horizontal scroll ở viewport 360px. | AI initial | Passed | scrollWidth = clientWidth = 360. | Playwright viewport 360px |
| CHK-05 | Register | FR-01 | Trang Đăng ký có đúng một thẻ <h1> mô tả màn hình. | AI initial | **Failed** | 0 <h1>; chỉ có <h2>Đăng Ký Tài Khoản</h2>. | [CHK-05-register-h1.png](screenshots/CHK-05-register-h1.png) |
| CHK-07 | Register | FR-01 | Helper text và nút submit đạt WCAG 2.2 AA contrast (4.5:1 cho text thường). | Review addition | **Failed** | axe-core: #9ca3af trên #ffffff = 2.53:1; trắng trên #ef4444 = 3.76:1. | [CHK-07-register-contrast.png](screenshots/CHK-07-register-contrast.png) |
| CHK-08 | Register | FR-01 | Trang Đăng ký không có horizontal scroll ở viewport 360px. | AI initial | Passed | scrollWidth = clientWidth = 360. | Playwright viewport 360px |
| CHK-09 | Forgot Password | FR-03 | Trang Quên mật khẩu có đúng một thẻ <h1> mô tả màn hình. | AI initial | **Failed** | 0 <h1>; chỉ có <h2>Quên Mật Khẩu</h2>. | [CHK-09-forgot-h1.png](screenshots/CHK-09-forgot-h1.png) |
| CHK-11 | Forgot Password | FR-03 | Ở bước 2, primary action nổi bật, dùng màu xanh dương theo FR-21 và phân biệt với secondary action. | AI initial | **Failed** | “Đặt lại mật khẩu” và “← Quay lại” đều là nút xanh lá full-width, style giống nhau; primary không dùng màu xanh dương. | [CHK-11-forgot-buttons.png](screenshots/CHK-11-forgot-buttons.png) |
| CHK-12 | Forgot Password | FR-03 | Trang Quên mật khẩu không có horizontal scroll ở viewport 360px. | AI initial | Passed | scrollWidth = clientWidth = 360. | Playwright viewport 360px |
| CHK-13 | Profile | FR-04 | Trang Hồ sơ có đúng một thẻ <h1> và hierarchy heading hợp lý. | Review addition | **Failed** | 0 <h1>; hai <h2> (“Hồ sơ của bạn”, “Lịch sử đơn hàng”). | [CHK-13-profile-h1.png](screenshots/CHK-13-profile-h1.png) |
| CHK-15 | Profile | FR-04 | Bảng lịch sử đơn hàng dùng được ở 360px, không tạo horizontal scroll cho cả trang. | Review addition | **Failed** | scrollWidth 399px vs clientWidth 360px (overflow 39px); bảng 5 cột giữ width desktop. | [CHK-15-profile-mobile-table.png](screenshots/CHK-15-profile-mobile-table.png) |
| CHK-16 | Profile | FR-04 | Text và badge trạng thái đơn hàng đạt WCAG 2.2 AA contrast. | Review addition | **Failed** | axe-core: #fde047 trên #2563eb = 3.92:1; trắng trên #ef4444 = 3.76:1. | [CHK-16-profile-contrast.png](screenshots/CHK-16-profile-contrast.png) |
| CHK-71 | All auth screens | FR-01..04 | Ngôn ngữ giao diện nhất quán tiếng Việt (trừ thuật ngữ kỹ thuật chuẩn) theo FR-21. | Review addition | **Failed** | Login dùng “Username” và “Sign In” trong khi phần còn lại là tiếng Việt; các màn hình khác không có chuỗi tiếng Anh không cần thiết. | [CHK-71-login-language.png](screenshots/CHK-71-login-language.png) |
| CHK-74 | Register, Forgot Password | FR-01, FR-03 | Các nút submit tích cực dùng màu xanh dương theo FR-21. | Review addition | **Failed** | Register dùng bg-red-500 (#ef4444); bước 2 Forgot dùng bg-green-600; Login, Forgot bước 1 và Profile dùng xanh dương. | [CHK-74-button-color.png](screenshots/CHK-74-button-color.png) |
| CHK-76 | Profile | FR-04 | Tổng tiền đơn hàng dùng ký hiệu ₫ và phân cách hàng nghìn theo FR-21. | Review addition | Passed | Quan sát với order inject: “1.234.567 ₫”. | Playwright injected order |
| CHK-65 | All auth screens | FR-01..04 | Layout vẫn dùng được khi document direction là RTL. | Review addition | **Failed** | Với dir="rtl", utility vật lý giữ link “Quên mật khẩu?” ở bên phải và header không đảo; layout không mirror. | [CHK-65-login-rtl.png](screenshots/CHK-65-login-rtl.png) |
| CHK-66 | All auth screens | FR-01..04 | Text vẫn đọc được khi hệ điều hành dùng dark mode. | Review addition | Passed | Chưa có dark theme, nhưng card trắng và text đen vẫn đọc được với colorScheme=dark. | Playwright colorScheme=dark |
| CHK-67 | All auth screens | FR-01..04 | Nội dung reflow ở 200% zoom (640 CSS px) mà không có horizontal scroll. | Review addition | Passed | Login, Register và Forgot Password đều có scrollWidth = clientWidth = 640. | Playwright viewport 640px |

## IA-02 — Forms

| ID | Màn hình | FR | Checklist item | Nguồn | Kết quả | Ghi chú / lý do fail | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-17 | Login | FR-02 | Ô email/username dùng input type phù hợp với email (FR-02, FR-22). | AI initial | **Failed** | type="text" và label “Username”, trong khi backend xác thực bằng email. | [CHK-17-18-19-login-fields.png](screenshots/CHK-17-18-19-login-fields.png) |
| CHK-18 | Login | FR-02 | Ô mật khẩu che ký tự đã nhập (FR-22). | AI initial | **Failed** | type="text"; mật khẩu hiển thị rõ trên màn hình. | [CHK-17-18-19-login-fields.png](screenshots/CHK-17-18-19-login-fields.png) |
| CHK-19 | Login | FR-02 | Mọi input có label liên kết bằng chương trình (for/id hoặc aria-label). | Review addition | **Failed** | Label không có for/id; axe-core báo 2 critical label violations. | [CHK-17-18-19-login-fields.png](screenshots/CHK-17-18-19-login-fields.png) |
| CHK-20 | Login | FR-02 | Trường bắt buộc được chặn bằng native validation khi submit rỗng. | AI initial | Passed | Cả hai input có required; browser báo “Please fill out this field.” và focus ô trống đầu tiên. | Playwright native validation |
| CHK-21 | Register | FR-01 | Ô email dùng type=email và từ chối địa chỉ sai định dạng (FR-01, FR-22). | AI initial | **Failed** | type="text"; “not-an-email-<timestamp>” được chấp nhận và chuyển về /login. | [CHK-21-register-invalid-email.png](screenshots/CHK-21-register-invalid-email.png) |
| CHK-22 | Register | FR-01 | Ô mật khẩu che ký tự đã nhập (FR-22). | AI initial | Passed | type="password". | DOM inspection |
| CHK-23 | Register | FR-01 | Nội dung mô tả password rule khớp với validation thực tế (FR-01: có ký tự đặc biệt). | Review addition | **Failed** | Text hứa “ký tự đặc biệt” nhưng regex yêu cầu whitespace và chặn ký tự đặc biệt; “Abcd1234!” bị từ chối. | [CHK-23-register-password-rule.png](screenshots/CHK-23-register-password-rule.png) |
| CHK-24 | Register | FR-01 | Có trường xác nhận mật khẩu và chặn khi hai trường không khớp (FR-01). | AI initial | **Failed** | Chỉ có một input mật khẩu. | [CHK-24-register-no-confirm.png](screenshots/CHK-24-register-no-confirm.png) |
| CHK-25 | Forgot Password | FR-03 | Ô email dùng type=email và validate định dạng (FR-22). | AI initial | **Failed** | type="text"; email sai định dạng chỉ bị backend từ chối sau khi submit. | [CHK-25-forgot-email-type.png](screenshots/CHK-25-forgot-email-type.png) |
| CHK-26 | Forgot Password | FR-03 | OTP gồm 6 chữ số (FR-03, SEC-07) và ô nhập giới hạn đúng 6 chữ số. | Review addition | **Failed** | SUT sinh OTP 4 chữ số (“Mã OTP của bạn là: 2809”), label ghi “Mã OTP (4 số)”; input type=text, không maxlength/inputmode/pattern. | [CHK-26-forgot-otp-input.png](screenshots/CHK-26-forgot-otp-input.png) |
| CHK-27 | Forgot Password | FR-03 | Ô mật khẩu mới che ký tự đã nhập (FR-22). | AI initial | Passed | type="password". | DOM inspection |
| CHK-28 | Forgot Password | FR-03 | Bước 2 yêu cầu xác nhận mật khẩu mới (FR-03). | AI initial | **Failed** | Chỉ có một input “Mật khẩu mới”. | [CHK-28-forgot-no-confirm.png](screenshots/CHK-28-forgot-no-confirm.png) |
| CHK-29 | Profile | FR-04 | Email không thể chỉnh sửa qua giao diện (FR-04). | AI initial | Passed | disabled + label “Email (Không đổi)”. | DOM inspection |
| CHK-31 | Profile | FR-04 | Số điện thoại được validate theo FR-04 (bắt đầu bằng 0, 10–11 chữ số) và lỗi hiển thị trên nút submit. | Review addition | **Failed** | Regex /^[1-9][0-9]{8,9}$/ từ chối mọi số bắt đầu bằng 0, gồm placeholder 0912345678; lỗi dùng alert(), không nằm trên nút submit. | [CHK-31-profile-phone-alert.png](screenshots/CHK-31-profile-phone-alert.png) |
| CHK-32 | Profile | FR-04 | Mọi label của Profile liên kết bằng chương trình với input. | Review addition | **Failed** | Cả bốn label thiếu for/id; axe-core báo critical label violations. | [CHK-32-profile-labels.png](screenshots/CHK-32-profile-labels.png) |
| CHK-70 | All auth screens | FR-01..04 | Mọi trường bắt buộc có ký hiệu * bên cạnh nhãn (FR-22). | Review addition | **Failed** | Không label nào có * dù tất cả input đều required. | [CHK-70-required-asterisk.png](screenshots/CHK-70-required-asterisk.png) |
| CHK-75 | All auth screens | FR-01..04 | Thông báo lỗi nằm trên nút submit, không nằm dưới (FR-22). | Review addition | **Failed** | Login: error div nằm sau form, dưới nút Sign In. Register: error nằm trên form (đạt). Forgot/Profile: dùng alert(), không có inline message. | [CHK-75-error-position.png](screenshots/CHK-75-error-position.png) |

## IA-03 — Navigation

| ID | Màn hình | FR | Checklist item | Nguồn | Kết quả | Ghi chú / lý do fail | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-33 | Login | FR-02 | Header toàn cục hiện diện và các link hoạt động trên trang Đăng nhập. | AI initial | Passed | Header có EShop, Giỏ hàng, Đăng nhập, Đăng ký; điều hướng đúng. | Playwright navigation |
| CHK-35 | Login | FR-02 | Link “Đăng ký ngay” điều hướng tới /register. | AI initial | Passed | Điều hướng đúng. | Playwright navigation |
| CHK-36 | Login | FR-02 | Tab order theo đúng thứ tự thị giác từ trên xuống, trái sang phải (FR-21). | Review addition | **Failed** | Nút Sign In có tabindex="1" nên Tab đầu tiên focus vào nút, trước email/password. | [CHK-36-login-tab-order.png](screenshots/CHK-36-login-tab-order.png) |
| CHK-37 | Register | FR-01 | Header navigation hiện diện và nhất quán với Login. | AI initial | Passed | Cùng link và style. | DOM inspection |
| CHK-38 | Register | FR-01 | Link “Đăng nhập” điều hướng tới /login. | AI initial | Passed | Điều hướng đúng. | Playwright navigation |
| CHK-39 | Register | FR-01 | Tab order theo đúng thứ tự thị giác (FR-21). | AI initial | Passed | Header → Họ Tên → Email → Mật khẩu → Đăng Ký → link đăng nhập. | Playwright keyboard test |
| CHK-40 | Register | FR-01 | Đăng ký thành công quay về trang Đăng nhập (FR-01). | AI initial | Passed | navigate('/login') sau POST thành công. | Playwright registration flow |
| CHK-41 | Forgot Password | FR-03 | Quay lại bước 1 giữ nguyên email đã nhập. | AI initial | Passed | Email state được giữ sau “← Quay lại”. | Playwright step-back test |
| CHK-42 | Forgot Password | FR-03 | Có đường quay lại đăng nhập từ màn hình Quên mật khẩu (FR-03). | AI initial | Passed | Link “Đăng nhập” trên header. | DOM inspection |
| CHK-43 | Forgot Password | FR-03 | Focus được chuyển tới field đầu tiên của bước mới sau khi chuyển bước. | Review addition | **Failed** | Sau “Lấy mã OTP”, document.activeElement là BODY; focus không vào ô OTP hay heading bước 2. | [CHK-43-forgot-focus.png](screenshots/CHK-43-forgot-focus.png) |
| CHK-44 | Forgot Password | FR-03 | Bước 2 có step indicator rõ ràng, ví dụ “Bước 2 / 2” (FR-03, FR-22). | AI initial | **Failed** | Không có progress indicator hay số bước. | [CHK-44-forgot-step-indicator.png](screenshots/CHK-44-forgot-step-indicator.png) |
| CHK-46 | Profile | FR-04 | Header hiển thị trạng thái đã đăng nhập và link Profile hoạt động. | AI initial | Passed | “Chào, <name>” link tới /profile; có nút đăng xuất. | DOM inspection |
| CHK-47 | Profile | FR-04 | Nút đăng xuất có nhãn “Đăng xuất”, không phải “Thoát” (FR-23). | AI initial | **Failed** | Nhãn quan sát: “Thoát”. | [CHK-47-logout-label.png](screenshots/CHK-47-logout-label.png) |
| CHK-48 | Profile | FR-04 | Navbar highlight trang hiện tại (FR-23). | Review addition | **Failed** | Không có aria-current, active class hay trạng thái thị giác cho /profile. | [CHK-48-profile-active-nav.png](screenshots/CHK-48-profile-active-nav.png) |
| CHK-80 | All auth screens | FR-01..04 | Link “Giỏ hàng” trên header hiển thị badge số lượng sản phẩm (FR-23). | Review addition | **Failed** | Header chỉ có text “Giỏ hàng”; không có badge hay số lượng cạnh link. | [CHK-80-cart-badge.png](screenshots/CHK-80-cart-badge.png) |

## IA-04 — Feedback / state

| ID | Màn hình | FR | Checklist item | Nguồn | Kết quả | Ghi chú / lý do fail | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-49 | Login | FR-02 | Nút submit có loading/disabled state khi đang xác thực. | AI initial | **Failed** | Khi delay /api/login, nút vẫn enabled, label “Sign In”, không spinner/aria-busy. | [CHK-49-login-loading.png](screenshots/CHK-49-login-loading.png) |
| CHK-50 | Login | FR-02 | Lỗi đăng nhập nằm trên nút submit và được announce cho assistive technology (FR-22). | AI initial | **Failed** | Error div nằm sau form (dưới nút Sign In), không có role="alert"/aria-live, không gắn với field. | [CHK-50-login-error.png](screenshots/CHK-50-login-error.png) |
| CHK-51 | Login | FR-02 | Thông báo lỗi đăng nhập không tiết lộ nguyên nhân cụ thể (FR-02). | AI initial | Passed | Chỉ hiển thị “Đăng nhập thất bại. Vui lòng kiểm tra lại.” cho mọi lỗi. | Playwright login flow |
| CHK-52 | Login | FR-02 | Đăng nhập thành công có phản hồi rõ và chuyển hướng. | AI initial | Passed | Chuyển về / và header đổi thành “Chào, <name>”. | Playwright login flow |
| CHK-54 | Register | FR-01 | Email trùng bị từ chối với thông báo dễ hiểu (FR-01). | AI initial | **Failed** | Đăng ký cùng email hai lần đều chuyển về /login, không báo lỗi; backend không có unique constraint. | [CHK-54-register-duplicate-email.png](screenshots/CHK-54-register-duplicate-email.png) |
| CHK-55 | Register | FR-01 | Lỗi server không lộ chi tiết kỹ thuật (SEC-04, FR-24). | Review addition | **Failed** | Catch block render err.response.data.error trực tiếp; giả lập 500 hiện “SQLITE_ERROR: no such column: name”. | [CHK-55-register-raw-error.png](screenshots/CHK-55-register-raw-error.png) |
| CHK-56 | Register | FR-01 | Nút submit có loading/disabled state khi đang đăng ký. | AI initial | **Failed** | Khi delay /api/register, nút vẫn enabled, label “Đăng Ký”, không aria-busy. | [CHK-56-register-loading.png](screenshots/CHK-56-register-loading.png) |
| CHK-57 | Forgot Password | FR-03 | Yêu cầu OTP thành công được hiển thị rõ. | AI initial | Passed | Green box và bước 2 hiện ra sau khi request. | Playwright forgot-password flow |
| CHK-58 | Forgot Password | FR-03 | OTP được hiển thị trực tiếp trên màn hình trong môi trường demo (FR-03). | Review addition | Passed | Bước 2 hiện “Mã OTP của bạn là: …” — đúng yêu cầu demo của FR-03. | Playwright forgot-password flow |
| CHK-59 | Forgot Password | FR-03 | Lỗi email không tồn tại hiển thị inline, không blocking, nằm trên nút submit (FR-22). | AI initial | **Failed** | Dùng alert(“Lỗi: User not found”); không có inline message, field highlight hay live region. | [CHK-59-forgot-alert.png](screenshots/CHK-59-forgot-alert.png) |
| CHK-60 | Forgot Password | FR-03 | Phản hồi thành công/thất bại khi đặt lại mật khẩu rõ ràng. | AI initial | Passed | Success alert + chuyển /login; failure alert hiện ra. Modality alert của lỗi được ghi nhận ở CHK-59. | Playwright forgot-password flow |
| CHK-61 | Profile | FR-04 | Cập nhật hồ sơ thành công có phản hồi rõ ràng cho người dùng. | AI initial | Passed | Alert “Cập nhật thành công!” xác nhận thao tác đã lưu; item này chỉ chấm sự hiện diện của phản hồi. | Playwright profile update flow |
| CHK-62 | Profile | FR-04 | Lịch sử đơn hàng có loading state. | AI initial | **Failed** | Khi delay /api/orders/my-orders, empty state “Bạn chưa có đơn hàng nào.” hiện ngay; không spinner/skeleton/aria-busy. | [CHK-62-profile-orders-loading.png](screenshots/CHK-62-profile-orders-loading.png) |
| CHK-63 | Profile | FR-04 | Lỗi tải đơn hàng được phân biệt với danh sách rỗng. | Review addition | **Failed** | Response 500 đặt orders=[] và UI hiện “Bạn chưa có đơn hàng nào.”; không error/retry. | [CHK-63-profile-orders-error.png](screenshots/CHK-63-profile-orders-error.png) |
| CHK-68 | Profile | FR-04 | Trạng thái đơn hàng được truyền đạt bằng text, không chỉ bằng màu. | AI initial | Passed | statusLabel() map mỗi status sang text tiếng Việt cạnh badge màu. | DOM inspection |
| CHK-73 | Profile | FR-04 | Empty state có icon/hình minh họa và message thân thiện (FR-24). | Review addition | **Failed** | Chỉ có <p>Bạn chưa có đơn hàng nào.</p>, không icon/hình minh họa. | [CHK-73-empty-state.png](screenshots/CHK-73-empty-state.png) |

## Ghi chú thực thi

- SUT chạy local: backend `http://localhost:3000`, web frontend `http://localhost:5173`.
- Hành vi chức năng được điều khiển bằng Playwright 1.65 (Chromium 158); DOM/ARIA facts đọc từ trang live.
- Evidence accessibility dùng axe-core 4.x; contrast ratio là số tính bởi axe-core, không ước lượng bằng mắt.
- Mobile dùng viewport 360×800. Screenshot chỉ chụp cho item Failed, có banner đỏ ghi ID và lỗi quan sát.
- Item Failed không tự động là bug: một số là design gap; bug list chỉ gồm defect tái hiện được.
- Ngoài phạm vi Task 1: order state machine (FR-10), coupon (FR-09), cart (FR-07), admin (FR-12…FR-19), mobile (FR-20), route guard/SPA reload/tab title/RTL/dark mode/zoom vì không có trong spec GUI.
