# Review additions — các item AI bỏ sót hoặc làm sai

Sau review theo README FR-21…FR-24, checklist cuối có **66 item**: **41 item AI ban đầu** và **25 item bổ sung/sửa**. Bộ AI ban đầu (44 item được sinh, 41 item được giữ sau review) nằm trong `ai-initial-checklist.md` để đối chiếu audit.

## 1. Item bổ sung mới

| ID | IA | Màn hình | Item bổ sung | Vì sao AI bỏ sót |
| --- | --- | --- | --- | --- |
| CHK-07 | IA-01 | Register | Helper text và nút submit đạt WCAG 2.2 AA contrast (4.5:1 cho text thường). | AI viết “đủ contrast” nhưng không tính ratio; axe-core tìm ra 2.53:1 và 3.76:1. |
| CHK-13 | IA-01 | Profile | Trang Hồ sơ có đúng một thẻ <h1> và hierarchy heading hợp lý. | AI coi heading là typography, không kiểm tra outline h1/h2. |
| CHK-15 | IA-01 | Profile | Bảng lịch sử đơn hàng dùng được ở 360px, không tạo horizontal scroll cho cả trang. | AI viết “mobile usable” chung chung, không test bảng dữ liệu 5 cột. |
| CHK-16 | IA-01 | Profile | Text và badge trạng thái đơn hàng đạt WCAG 2.2 AA contrast. | Như CHK-07: AI không tính contrast cho badge trạng thái và header. |
| CHK-71 | IA-01 | All auth screens | Ngôn ngữ giao diện nhất quán tiếng Việt (trừ thuật ngữ kỹ thuật chuẩn) theo FR-21. | AI bỏ sót yêu cầu nhất quán ngôn ngữ tiếng Việt (FR-21). |
| CHK-74 | IA-01 | Register, Forgot Password | Các nút submit tích cực dùng màu xanh dương theo FR-21. | AI bỏ sót quy tắc nút tích cực dùng màu xanh dương (FR-21). |
| CHK-76 | IA-01 | Profile | Tổng tiền đơn hàng dùng ký hiệu ₫ và phân cách hàng nghìn theo FR-21. | AI bỏ sót yêu cầu định dạng tiền ₫ và phân cách hàng nghìn (FR-21). |
| CHK-65 | IA-01 | All auth screens | Layout vẫn dùng được khi document direction là RTL. | AI mặc định layout LTR, không thử dir="rtl"; đây là ví dụ điển hình về item AI thường bỏ sót. |
| CHK-66 | IA-01 | All auth screens | Text vẫn đọc được khi hệ điều hành dùng dark mode. | AI mặc định light mode, không kiểm tra colorScheme=dark. |
| CHK-67 | IA-01 | All auth screens | Nội dung reflow ở 200% zoom (640 CSS px) mà không có horizontal scroll. | AI mặc định 100% zoom, không kiểm tra reflow ở 200% (640 CSS px). |
| CHK-19 | IA-02 | Login | Mọi input có label liên kết bằng chương trình (for/id hoặc aria-label). | AI kiểm tra label hiển thị, không kiểm tra for/id hoặc aria-label. |
| CHK-23 | IA-02 | Register | Nội dung mô tả password rule khớp với validation thực tế (FR-01: có ký tự đặc biệt). | AI không so sánh copy password rule với regex thực tế; mâu thuẫn chỉ lộ khi đọc cả hai. |
| CHK-26 | IA-02 | Forgot Password | OTP gồm 6 chữ số (FR-03, SEC-07) và ô nhập giới hạn đúng 6 chữ số. | AI lấy label “4 số” của SUT thay vì đọc FR-03/SEC-07 yêu cầu OTP 6 chữ số. |
| CHK-31 | IA-02 | Profile | Số điện thoại được validate theo FR-04 (bắt đầu bằng 0, 10–11 chữ số) và lỗi hiển thị trên nút submit. | AI chỉ kiểm tra “có lỗi”, không kiểm tra regex có nhận số Việt Nam hợp lệ và vị trí lỗi. |
| CHK-32 | IA-02 | Profile | Mọi label của Profile liên kết bằng chương trình với input. | Như CHK-19: label hiển thị được coi là đủ. |
| CHK-70 | IA-02 | All auth screens | Mọi trường bắt buộc có ký hiệu * bên cạnh nhãn (FR-22). | AI bỏ sót yêu cầu dấu * cho trường bắt buộc (FR-22). |
| CHK-75 | IA-02 | All auth screens | Thông báo lỗi nằm trên nút submit, không nằm dưới (FR-22). | AI bỏ sót yêu cầu thông báo lỗi nằm trên nút submit (FR-22). |
| CHK-36 | IA-03 | Login | Tab order theo đúng thứ tự thị giác từ trên xuống, trái sang phải (FR-21). | AI không chạy keyboard-only test; tabindex="1" không thấy trong screenshot. |
| CHK-43 | IA-03 | Forgot Password | Focus được chuyển tới field đầu tiên của bước mới sau khi chuyển bước. | AI bỏ sót focus management sau step transition của form 2 bước. |
| CHK-48 | IA-03 | Profile | Navbar highlight trang hiện tại (FR-23). | AI không kiểm tra aria-current/active state của navbar. |
| CHK-80 | IA-03 | All auth screens | Link “Giỏ hàng” trên header hiển thị badge số lượng sản phẩm (FR-23). | AI chỉ kiểm tra nội dung từng trang, bỏ sót yêu cầu badge giỏ hàng trên header toàn cục (FR-23). |
| CHK-55 | IA-04 | Register | Lỗi server không lộ chi tiết kỹ thuật (SEC-04, FR-24). | AI không test server-error path nên bỏ sót raw error leakage. |
| CHK-58 | IA-04 | Forgot Password | OTP được hiển thị trực tiếp trên màn hình trong môi trường demo (FR-03). | AI coi OTP hiển thị là lỗi, nhưng FR-03 cho phép hiển thị trong môi trường demo; review sửa thành pass. |
| CHK-63 | IA-04 | Profile | Lỗi tải đơn hàng được phân biệt với danh sách rỗng. | AI kiểm tra empty state nhưng không phân biệt error với empty list. |
| CHK-73 | IA-04 | Profile | Empty state có icon/hình minh họa và message thân thiện (FR-24). | AI bỏ sót yêu cầu empty state có icon/hình minh họa (FR-24). |

## 2. Item AI làm sai và đã sửa

| ID | AI ban đầu | Vấn đề | Cách sửa |
| --- | --- | --- | --- |
| CHK-01, CHK-05, CHK-09, CHK-13 | Chỉ kiểm tra text heading | FR-21 yêu cầu đúng một `<h1>` mỗi trang; cả 4 trang dùng `<h2>` | Đổi oracle sang `<h1>` + nội dung heading |
| CHK-11 | Chỉ kiểm tra primary/secondary khác nhau | FR-21 quy định nút tích cực màu xanh dương | Thêm ràng buộc màu xanh dương cho primary action |
| CHK-17, CHK-18, CHK-21, CHK-25 | “Input type phù hợp” | FR-22 quy định chính xác `type=email` và `type=password` | Ghi rõ type trong oracle |
| CHK-26 | OTP 4 chữ số | FR-03 và SEC-07 yêu cầu OTP 6 chữ số | Sửa oracle thành 6 chữ số và giới hạn input 6 chữ số |
| CHK-47 | Logout phải redirect | FR-23 chỉ quy định nhãn “Đăng xuất”, không quy định redirect | Đổi oracle sang nhãn nút |
| CHK-51 | Lỗi phải phân biệt sai mật khẩu/khóa/mạng | FR-02 yêu cầu “không để lộ chi tiết nguyên nhân” | Đảo oracle: thông báo generic là pass |
| CHK-58 | OTP không được hiển thị | FR-03 cho phép hiển thị OTP trong môi trường demo | Đảo oracle: hiển thị OTP là pass |
| CHK-60 | Không ghi rõ modality | Alert là blocking nhưng item này chỉ chấm clarity | Ghi chú alert modality thuộc CHK-59 |

## 3. Item bị loại vì ngoài phạm vi Task 1

| ID cũ | Lý do loại |
| --- | --- |
| CHK-02, CHK-06, CHK-10, CHK-14 | Browser tab title không có trong spec GUI |
| CHK-30 | `inputmode=tel` không có trong spec; validity của số điện thoại đã được CHK-31 cover |
| CHK-34 | Full page reload là chi tiết implementation, không phải yêu cầu GUI |
| CHK-45, CHK-69 | Route guard/redirect không có trong spec GUI |
| CHK-53 | Success toast khi đăng ký không có trong spec; FR-01 chỉ yêu cầu redirect (CHK-40) |
| CHK-64 | Hủy đơn là business rule FR-10, ngoài FR-01…FR-04 của Task 1 |
