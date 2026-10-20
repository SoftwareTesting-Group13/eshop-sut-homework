# FR-17 — Quan sát bổ sung (OBS-FR17-03/04 đã chuyển thành bug)

> Các quan sát dưới đây ban đầu được lưu riêng để người kiểm thử xem xét. Ngày **2026-10-21**, người kiểm thử xác nhận **OBS-FR17-03** và **OBS-FR17-04** là bug; hai mục này đã được chuyển vào báo cáo bug với ID `BUG-FR17-07` và `BUG-FR17-08`, dùng lại test case DT-07/DT-32 (không cộng thêm T-ID mới). Các quan sát còn lại vẫn nằm ngoài coverage kỹ thuật.

## OBS-FR17-01 — Trùng `code` trả HTTP 500 kèm lỗi SQLite

- **Nguồn:** `backend/server.js:466-479` — route `POST /api/admin/coupons` gọi `INSERT` trực tiếp; khi vi phạm `UNIQUE`, callback trả `res.status(500).json({ error: err.message })`.
- **Liên quan đặc tả:** FR-17 yêu cầu `code` duy nhất; test DT-03 xác nhận coupon trùng **không được tạo** (PASS về uniqueness).
- **Vì sao ngoài EP/BVA:** FR-17 không quy định status/message khi validation thất bại, nên không có oracle để chấm 4xx/500. Đây là quan sát chất lượng/error handling.
- **Bằng chứng:** `features/FR17/evidence/DT-03.log` — HTTP 500, body `{"error":"SQLITE_CONSTRAINT: UNIQUE constraint failed: coupons.code"}`; `GET /api/coupons` không có row mới.
- **Trạng thái:** Quan sát; **chờ người kiểm thử quyết định** có báo bug hay không (nếu báo, nên tách khỏi BUG-FR17-01 vì uniqueness vẫn được enforce).

## OBS-FR17-02 — Xóa id không tồn tại trả 200 `Coupon deleted`

- **Nguồn:** `backend/server.js:483-488` — `DELETE FROM coupons WHERE id = ?`; không kiểm tra `this.changes`/số row bị ảnh hưởng, luôn trả `{"message":"Coupon deleted"}`.
- **Liên quan đặc tả:** FR-17 chỉ nói Admin có thể Xóa mã giảm giá; không quy định hành vi khi id không tồn tại.
- **Bằng chứng:** `features/FR17/evidence/DT-31.log` — `DELETE /api/admin/coupons/999999` → HTTP 200 `{"message":"Coupon deleted"}`; `GET /api/coupons` vẫn 4 row.
- **Trạng thái:** Quan sát/INCONCLUSIVE; không chấm PASS/FAIL. Đây là điểm cần người kiểm thử quyết định (idempotent delete hay nên 404).

## OBS-FR17-03 — `save10` được tạo bên cạnh `SAVE10`

- **Nguồn:** `backend/database.js:31` — `code TEXT UNIQUE` dùng collation mặc định (BINARY), nên `SAVE10` và `save10` là hai giá trị khác nhau. UI admin tự `toUpperCase()` (`frontend-admin/src/App.jsx:641-645`) nên người dùng thường không gửi được `save10`; API thì gửi được.
- **Liên quan đặc tả:** FR-17 yêu cầu `code` duy nhất. Ngày **2026-10-21**, người kiểm thử xác nhận uniqueness phải **không phân biệt hoa/thường**; vì cột `code TEXT UNIQUE` dùng collation BINARY, `save10` đang được tạo bên cạnh `SAVE10` là bug.
- **Bằng chứng:** `features/FR17/evidence/DT-07.log` — HTTP 200, row mới `code="save10"` trong khi seed `SAVE10` vẫn tồn tại.
- **Trạng thái:** **Đã xác nhận — `BUG-FR17-07`**. Bug đã vào `test-results.md` và master report; ảnh Postman đã có, Issue [#53](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/53) đã publish.

## OBS-FR17-04 — `percent` với `discount_value=150` được chấp nhận

- **Nguồn:** `backend/server.js:457-481` không có upper bound; `frontend-admin/src/App.jsx:659-675` ô Giá trị không có `max`.
- **Liên quan đặc tả:** FR-17 yêu cầu `discount_value` dương. Ngày **2026-10-21**, người kiểm thử xác nhận với `type = percent`, mức giảm không được vượt quá `100`; `150%` là mức không hợp lệ kể cả khi đặc tả không ghi upper bound.
- **Bằng chứng:** `features/FR17/evidence/DT-32.log` — HTTP 200, row mới `discount_value=150`. Ảnh UI bổ sung: [`BUG-FR17-08-AppliedDiscount150.png`](../features/FR17/screenshots/BUG-FR17-08-AppliedDiscount150.png) — coupon `150%` áp dụng thành công, tiết kiệm `-4,470,000,000 đ`, thành tiền `4,500,000,000 đ` (hệ quả FR-09).
- **Ảnh hưởng tiềm ẩn (FR-09, ngoài phạm vi):** công thức percent hiện tại là `total * (1 - discount_value)` thay vì `total * discount_value / 100`; với 150% có thể cho kết quả âm/không hợp lý. Xem OBS-FR17-07.
- **Trạng thái:** **Đã xác nhận — `BUG-FR17-08`**. Bug đã vào `test-results.md` và master report; 2 ảnh Postman + 1 ảnh UI bổ sung, Issue [#54](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54) đã publish.

## OBS-FR17-05 — Form coupon thiếu nhãn và dấu `*` cho trường bắt buộc

- **Nguồn:** `frontend-admin/src/App.jsx:637-710` — các input chỉ có `placeholder` (Mã coupon, Giá trị, Đơn tối thiểu, Ngày hết hạn, Số lần dùng tối đa/người), không có `<label>` và không có ký hiệu `*`; `select` Loại cũng không có nhãn.
- **Liên quan đặc tả:** FR-22 (`README.md` §7) — "Tất cả trường bắt buộc phải có ký hiệu `*` bên cạnh nhãn." Đây là yêu cầu GUI, không phải rule dữ liệu của FR-17.
- **Bằng chứng:** đọc source; **chưa chạy UI**.
- **Trạng thái:** Quan sát source; nếu báo bug nên gắn FR-22, không gắn FR-17.

## OBS-FR17-06 — User token gọi được API tạo coupon admin (FR-12)

- **Nguồn:** `backend/server.js:457` — route `POST /api/admin/coupons` chỉ dùng `authenticateToken`, không kiểm tra `req.user.role === 'admin'`. Các route admin khác có cùng pattern.
- **Liên quan đặc tả:** `api_specification.md` §6 — "Tất cả API dưới đây yêu cầu ... tài khoản phải có quyền Admin"; `README.md` FR-12/SEC-03.
- **Bằng chứng:** `features/FR17/evidence/OBS-fr17-user-token.log` — đăng nhập `test@eshop.com` (role `user`) → `POST /api/admin/coupons` trả **200**, tạo row `FR17-OBS-USER`; `GET /api/coupons` bằng user token trả 200. Row đã được xóa bằng admin token sau quan sát.
- **Vì sao ngoài EP/BVA:** đây là kiểm soát truy cập (FR-12), không phải miền dữ liệu/trạng thái của FR-17. Trong bộ ca FR-17, mọi thao tác admin đều dùng token admin.
- **Trạng thái:** Đã xác nhận qua API; **chờ người kiểm thử quyết định** báo cáo dưới FR-12 (không cộng vào coverage FR-17).

## OBS-FR17-07 — FR-09 `apply-coupon`: công thức percent sai, dùng `>` thay `>=`, endpoint công khai

- **Nguồn:** `backend/server.js:363-441`:
  - `if (total_amount > coupon.min_order_amount)` dùng `>` thay vì `>=` (README FR-09 C3 yêu cầu `>=`).
  - Percent: `discount_amount = total_amount * (1 - coupon.discount_value)` thay vì `total * discount_value / 100` (README FR-09).
  - Fixed: `discount_amount = coupon.discount_value`, không chặn discount > total.
  - Route `POST /api/apply-coupon` không dùng `authenticateToken`; lấy `user_id` từ body, trong khi README FR-09 C4 yêu cầu JWT hợp lệ.
- **Bằng chứng (đã chạy, không gửi Authorization header):** `features/FR17/evidence/OBS-fr09-apply-coupon.log`:
  - `SAVE10`, total `500000` → HTTP 200, `discount_amount = -4500000`, `final_amount = 5000000` (theo đặc tả phải là 50,000 / 450,000).
  - `SAVE10`, total `300000` (bằng min) → HTTP 400 "chưa đủ giá trị tối thiểu" (đặc tả `>=` phải cho áp dụng).
  - `SAVE10`, total `299999` → HTTP 400 (đúng là phải từ chối).
  - `BIGBUY`, total `500000` (bằng min) → HTTP 400 (đặc tả `>=` phải cho áp dụng).
  - `BIGBUY`, total `500001` → HTTP 200, `discount_amount = 50000`, `final_amount = 450001`.
  - `EXPIRED`, total `500000` → HTTP 400 "Mã giảm giá đã hết hạn" (đúng).
- **Vì sao ngoài EP/BVA:** đây là rule của FR-09 (áp dụng coupon), không phải FR-17 (CRUD). Chỉ ghi nhận để người kiểm thử không bỏ sót; không cộng vào coverage FR-17.
- **Trạng thái:** Đã tái hiện qua API; **chờ người kiểm thử quyết định** báo cáo dưới FR-09.

## OBS-FR17-08 — UI hiển thị dữ liệu NULL/sai một cách khó hiểu

- **Nguồn:** `frontend-admin/src/App.jsx`:
  - `735`: `type === "percent" ? "Phần trăm" : "Cố định"` → `type = NULL` hoặc `"percentage"` đều hiển thị **"Cố định"**.
  - `738-740`: percent hiển thị `${discount_value}%`; fixed gọi `discount_value?.toLocaleString()` → `NULL` thành `undefined ₫`, `"abc"` thành `abc ₫`.
  - `742-744`: `min_order_amount?.toLocaleString()` → `NULL` thành `undefined ₫`.
  - `745-751`: `new Date(expired_at)` với `""`/`"not-a-date"` là Invalid Date → hiển thị chuỗi gốc (hoặc blank), không báo "sai ngày".
  - `752`: `max_uses_per_user` âm hiển thị `-1 lần`.
- **Liên quan:** đây là hệ quả hiển thị của dữ liệu không hợp lệ được tạo qua API (BUG-FR17-01…06); không phải một rule dữ liệu mới của FR-17.
- **Bằng chứng:** đọc source; **chưa chạy UI**.
- **Trạng thái:** Quan sát source; nếu báo bug nên gắn GUI/FR-22 hoặc để chung với bug validation tương ứng.

## OBS-FR17-09 — `GET /api/coupons` yêu cầu token nhưng không giới hạn role

- **Nguồn:** `backend/server.js:356-359` — `app.get("/api/coupons", authenticateToken, ...)`.
- **Liên quan:** API spec §5.2 ghi "Dành cho Admin"; FR-12 yêu cầu role admin. Đây là cùng nhóm với OBS-FR17-06.
- **Bằng chứng:** `OBS-fr17-user-token.log` — user token `GET /api/coupons` trả 200 và 4 row.
- **Trạng thái:** Đã xác nhận qua API; ngoài phạm vi FR-17.

## OBS-FR17-10 — Không có confirm khi xóa coupon

- **Nguồn:** `frontend-admin/src/App.jsx:753-768` — nút **Xóa** gọi `axios.delete` ngay, không có `confirm()` hay bước xác nhận.
- **Liên quan đặc tả:** FR-17 chỉ nói Admin có thể Xóa; không yêu cầu confirm. FR-24/FR-07 chỉ yêu cầu confirm cho giỏ hàng/đặt hàng, không áp dụng trực tiếp cho coupon.
- **Trạng thái:** Quan sát source; **không gọi bug** vì thiếu oracle. Nếu người kiểm thử muốn cải thiện UX, ghi riêng.

## Đã rà source nhưng không đủ căn cứ để báo

- **`coupon_usage` không có FK/cascade:** `backend/database.js` tạo bảng usage tham chiếu `coupon_id` nhưng không khai báo foreign key; xóa coupon có thể để lại row usage mồ côi. FR-17 không quy định cascade và chưa chạy thử, nên chỉ ghi nhận.
- **`GET /api/coupons` không có nhánh xử lý lỗi DB:** nếu `db.all` trả lỗi, route không có `if (err)` rõ ràng; chưa tái hiện được lỗi DB nên không đủ oracle.
- **Không có pagination/search/rate limit:** FR-17 không yêu cầu; không báo.
- **Không có `is_active` trong form/API tạo coupon:** FR-17 không yêu cầu trường này; DB mặc định 1.
- **Không có confirm khi xóa:** xem OBS-FR17-10; FR-17 không yêu cầu confirm.

## Tổng hợp trạng thái

| ID | Loại | Đã chạy? | Có oracle FR-17? | Ghi chú |
| --- | --- | --- | --- | --- |
| OBS-FR17-01 | Error handling | API (DT-03) | Không | Chờ quyết định |
| OBS-FR17-02 | Delete id không tồn tại | API (DT-31) | Không | Chờ quyết định |
| OBS-FR17-03 | Case-sensitive uniqueness | API (DT-07) | Có — người kiểm thử xác nhận | **BUG-FR17-07** |
| OBS-FR17-04 | Percent >100 | API (DT-32) | Có — người kiểm thử xác nhận | **BUG-FR17-08** |
| OBS-FR17-05 | UI labels/`*` | Chưa (source) | Không (FR-22) | Chờ người kiểm thử |
| OBS-FR17-06 | Thiếu role check | API | Không (FR-12) | Đã xác nhận, ngoài phạm vi |
| OBS-FR17-07 | FR-09 apply-coupon | API | Không (FR-09) | Đã xác nhận, ngoài phạm vi |
| OBS-FR17-08 | UI hiển thị NULL/sai | Chưa (source) | Không | Chờ người kiểm thử |
| OBS-FR17-09 | GET coupons thiếu role | API | Không (FR-12) | Đã xác nhận, ngoài phạm vi |
| OBS-FR17-10 | Không confirm xóa | Chưa (source) | Không | Quan sát UX |
