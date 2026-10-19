# FR02 — Quan sát ngoài phạm vi EP/BVA

> Các quan sát dưới đây **không thuộc** bộ ca Domain/EP và BVA của FR02, không cộng vào coverage kỹ thuật. Chúng được lưu riêng để người kiểm thử xem xét; nếu xác nhận là bug thì vẫn báo cáo và mở GitHub Issue kèm screenshot theo HW02 §6.

## OBS-FR02-01 — Phản hồi đăng nhập trả về mật khẩu plaintext

- **Nguồn quan sát (đã chạy thật):** `features/FR02/evidence/ev-DT-01.log`, `ev-DT-01-token-check.log`, `ev-DT-07-08.log`, `ev-BVA-07.log`.
- **Quan sát:** `POST /api/login` thành công trả `user.password = "Passw0rd!"`; `GET /api/users/me` cũng trả trường `password`. DB test lưu mật khẩu dạng plaintext.
- **Liên quan đặc tả:** SEC-01 "Mật khẩu không được lưu dưới dạng plaintext"; FR-04 (API hồ sơ) và các response user không nên lộ mật khẩu.
- **Vì sao ngoài EP/BVA:** Đây là kiểm tra nội dung response/bảo mật lưu trữ, không phải lớp tương đương hay điểm biên của input đăng nhập.
- **Trạng thái:** Quan sát; chưa xác nhận là bug FR02 (có thể thuộc phạm vi SEC/FR-04). Chờ người kiểm thử quyết định.

## OBS-FR02-02 — UI đăng nhập không dùng `type="email"` / `type="password"`

- **Nguồn quan sát (đọc source, **chưa chạy browser**):** `frontend-web/src/pages/Login.jsx` dòng 30 dùng `<input type="text">` cho email; dòng 40 dùng `<input type="text">` cho mật khẩu.
- **Liên quan đặc tả:** FR-02 "Trường email phải dùng `type=\"email\"`"; FR-22 "Trường Mật khẩu phải dùng `type=\"password\"`".
- **Vì sao ngoài EP/BVA:** Là thuộc tính DOM/UI, không phải miền dữ liệu; theo phạm vi HW02 không mở bộ kiểm tra UI Validation riêng. Chưa có bằng chứng chạy browser nên **không** tuyên bố đã kiểm thử UI.
- **Trạng thái:** Quan sát từ source; nếu người kiểm thử muốn báo cáo thì cần chạy browser và chụp screenshot.
