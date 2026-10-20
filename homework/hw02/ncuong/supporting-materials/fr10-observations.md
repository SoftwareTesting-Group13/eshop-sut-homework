# FR-10 — Quan sát ngoài phạm vi EP/BVA

> Các quan sát dưới đây **không thuộc** bộ ca Domain/EP và BVA của FR-10, không cộng vào coverage kỹ thuật. Chúng được lưu riêng để người kiểm thử xem xét; nếu xác nhận là bug thì vẫn báo cáo và mở GitHub Issue kèm screenshot theo HW02 §6.

## OBS-FR10-01 — API đổi trạng thái admin không kiểm tra quyền admin

- **Nguồn quan sát (đọc source, chưa chạy thử với token user):** `backend/server.js:525` — `PUT /api/admin/orders/:id/status` chỉ dùng middleware `authenticateToken` (xác thực token), **không** kiểm tra `req.user.role === 'admin'`. Các API admin khác cũng tương tự.
- **Liên quan đặc tả:** FR-12 (`README.md` §6) — "Tất cả các API Admin (`/api/admin/*`) … đều phải yêu cầu token JWT hợp lệ và `role = 'admin'`".
- **Vì sao ngoài EP/BVA:** đây là kiểm soát truy cập (FR-12), không phải miền dữ liệu/trạng thái của FR-10. Trong bộ ca FR-10, mọi thao tác admin đều dùng token admin; quyền truy cập không phải biến của state machine.
- **Trạng thái:** Quan sát từ source; **chưa** chạy xác nhận (nếu muốn báo cáo cần chạy request bằng token user và đối chiếu; có thể thuộc phạm vi FR-12). Chờ người kiểm thử quyết định.

## OBS-FR10-02 — Nút hủy/đánh dấu giao trên UI tương ứng với 2 bug

- **Nguồn quan sát (đọc source + đã xác nhận qua UI):** `frontend-web/src/pages/Profile.jsx:200` (nút "Hủy đơn" hiển thị khi `status !== "delivered" && status !== "canceled"`, tức cả khi `shipping`); `frontend-admin/src/App.jsx:862-869` (nút "Đánh dấu Đã giao" cho đơn `canceled`).
- **Liên quan:** đây là đường UI tái hiện BUG-FR10-01 và BUG-FR10-02. Người kiểm thử đã chạy trên browser, chụp screenshot và mở Issue [#33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33), [#34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34).
- **Trạng thái:** Đã xác nhận qua UI (EV-FR10-024/025); screenshot tại `features/FR10/screenshots/`.
