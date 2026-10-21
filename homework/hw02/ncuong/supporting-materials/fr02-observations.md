# FR02 — Quan sát ngoài phạm vi EP/BVA

> Các quan sát dưới đây **không thuộc** bộ ca Domain/EP và BVA của FR02, không cộng vào coverage kỹ thuật. Chúng được lưu riêng để người kiểm thử xem xét; nếu xác nhận là bug thì vẫn báo cáo và mở GitHub Issue kèm screenshot theo HW02 §6.

## OBS-FR02-01 — Phản hồi đăng nhập trả về mật khẩu plaintext

- **Nguồn quan sát (đã chạy thật):** `features/FR02/evidence/ev-DT-01.log`, `ev-DT-01-token-check.log`, `ev-DT-07-08.log`, `ev-BVA-07.log`.
- **Quan sát:** `POST /api/login` thành công trả `user.password = "Passw0rd!"`; `GET /api/users/me` cũng trả trường `password`. DB test lưu mật khẩu dạng plaintext.
- **Liên quan đặc tả:** SEC-01 "Mật khẩu không được lưu dưới dạng plaintext"; FR-04 (API hồ sơ) và các response user không nên lộ mật khẩu.
- **Vì sao ngoài EP/BVA:** Đây là kiểm tra nội dung response/bảo mật lưu trữ, không phải lớp tương đương hay điểm biên của input đăng nhập.
- **Trạng thái:** Quan sát; chưa xác nhận là bug FR02 (có thể thuộc phạm vi SEC/FR-04). Chờ người kiểm thử quyết định.

## OBS-FR02-02 — UI đăng nhập dùng `type="text"` cho email và mật khẩu

- **Nguồn:** `frontend-web/src/pages/Login.jsx` dòng 30 và 40; riêng ô email đã được kiểm tra trên Firefox headless trong `features/FR02/evidence/ev-gap-ui.json` và [ảnh trước/sau](../features/FR02/screenshots/).
- **Liên quan đặc tả:** FR-02 yêu cầu email `type="email"`; FR-22 yêu cầu mật khẩu `type="password"`.
- **Trạng thái email:** Đã chuyển vào miền kiểm thử FR-02 P10/DT-09. Form thực tế có email `type="text"`, không báo `typeMismatch` cho `not-an-email`, và đăng nhập thành công với tài khoản tạo qua API đăng ký. Xem [BUG-FR02-03 / Issue #58](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/58); không tính quan sát này thành bug thứ năm.
- **Trạng thái mật khẩu:** Source cho thấy `type="text"`; đây là yêu cầu FR-22, chưa mở test case hay bug riêng trong bộ FR-02. Ảnh của DT-09 có hiện mật khẩu fixture giả do cách render này.
