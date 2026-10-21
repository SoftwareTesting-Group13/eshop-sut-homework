# FR-10 — Quan sát ngoài phạm vi EP/BVA

> Các quan sát dưới đây **không thuộc** bộ ca Domain/EP và BVA của FR-10, không cộng vào coverage kỹ thuật. Chúng được lưu riêng để người kiểm thử xem xét; nếu xác nhận là bug thì vẫn báo cáo và mở GitHub Issue kèm screenshot theo HW02 §6.

## OBS-FR10-01 — API đổi trạng thái admin không kiểm tra quyền admin

- **Nguồn quan sát ban đầu:** `backend/server.js:525` — `PUT /api/admin/orders/:id/status` chỉ dùng middleware `authenticateToken` (xác thực token), **không** kiểm tra `req.user.role === 'admin'`. Các API admin khác có thể có cùng vấn đề nhưng chưa được kiểm thử trong AI-GAP-FR10-01.
- **Liên quan đặc tả:** FR-12 (`README.md` §6) — "Tất cả các API Admin (`/api/admin/*`) … đều phải yêu cầu token JWT hợp lệ và `role = 'admin'`".
- **Phạm vi kỹ thuật:** quyền truy cập thuộc FR-12/FR-18, không làm thay đổi mẫu số EP/BVA trạng thái FR-10 cốt lõi. Người kiểm thử yêu cầu kiểm tra riêng miền quyền tại AI-GAP-FR10-01.
- **Trạng thái:** Đã chạy API cách ly: user token đổi được đơn của mình 2/2 và đơn người khác 1/1; không token bị 401, admin token thành công. Xem `features/FR10/test-results.md` DT-21–DT-23, `evidence/ev-gap-access-*.json` và [BUG-FR10-03 / Issue #60](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/60) kèm ảnh log API. Không tuyên bố đã chạy UI.

## OBS-FR10-02 — Nút hủy/đánh dấu giao trên UI tương ứng với 2 bug

- **Nguồn quan sát (đọc source + đã xác nhận qua UI):** `frontend-web/src/pages/Profile.jsx:200` (nút "Hủy đơn" hiển thị khi `status !== "delivered" && status !== "canceled"`, tức cả khi `shipping`); `frontend-admin/src/App.jsx:862-869` (nút "Đánh dấu Đã giao" cho đơn `canceled`).
- **Liên quan:** đây là đường UI tái hiện BUG-FR10-01 và BUG-FR10-02. Người kiểm thử đã chạy trên browser, chụp screenshot và mở Issue [#33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33), [#34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34).
- **Trạng thái:** Đã xác nhận qua UI (EV-FR10-024/025); screenshot tại `features/FR10/screenshots/`.
