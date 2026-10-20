# BUG-FR17-07 — Tạo được `save10` bên cạnh `SAVE10` do uniqueness phân biệt hoa/thường

> **Trạng thái:** Đã xác nhận qua API bằng ảnh Postman do người kiểm thử cung cấp; **chỉ dùng bằng chứng Postman/API, không dùng ảnh UI**. GitHub Issue sẽ được cập nhật sau khi tạo.

## Tóm tắt

`POST /api/admin/coupons` trả HTTP 200 và tạo coupon `code = "save10"` trong khi coupon seed `SAVE10` đã tồn tại. FR-17 yêu cầu `code` duy nhất; người kiểm thử xác nhận uniqueness phải **không phân biệt hoa/thường**, nên `save10` phải bị từ chối. UI admin tự `toUpperCase()` nên finding này chỉ tái hiện được qua API.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | `FR-17` — Quản lý Mã Giảm Giá (Coupon CRUD); [`README.md` §5 FR-17](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/README.md) — `code` bắt buộc và duy nhất; quy tắc uniqueness không phân biệt hoa/thường do người kiểm thử xác nhận 2026-10-21 |
| Test case | `DT-07` — `code = "save10"` khi seed `SAVE10` đã tồn tại |
| Build / môi trường | commit `f389502cdb308b133fe9044e34505f19202dd887`; Node v26.9.0 + Express + SQLite; API `http://localhost:3000`; DB test cách ly seed 4 coupon |
| Severity / Priority | **Medium / Medium** — tạo được mã nhìn giống hệt mã đã có, gây trùng nghĩa/nhầm lẫn dữ liệu; đường UI bị chặn bởi uppercase nên đây là lỗi API-only |
| Trạng thái / lặp lại | **Đã xác nhận qua API**; 1/1 run API; **đã có 3 ảnh Postman**; Issue đang được tạo |

## Chuẩn bị để tái hiện

- Tài khoản admin seed: `admin@eshop.com` / `Admin123!` (role `admin`).
- DB test cách ly đang có đúng 4 seed coupon: `SAVE10`, `BIGBUY`, `VIP100`, `EXPIRED`. Không chạy lệnh trên `backend/database.sqlite` của repo.
- Backend SUT đang chạy tại `http://localhost:3000`; cần `curl` và `jq`.

```zsh
BASE=http://localhost:3000
ADMIN_TOKEN=$(curl -s -X POST "$BASE/api/login" \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@eshop.com","password":"Admin123!"}' | jq -r .token)
```

## Các bước tái hiện và kết quả

**Đường tái hiện đã kiểm chứng:** API. UI không gửi được cùng input vì ô **Mã coupon** tự `toUpperCase()` tại `frontend-admin/src/App.jsx:641-645`; đây là finding API-only.

1. Đăng nhập admin và lấy `ADMIN_TOKEN` bằng lệnh ở trên.
2. Xác nhận seed `SAVE10` tồn tại bằng `GET /api/coupons`.
3. Gửi `POST /api/admin/coupons` với `code = "save10"`; các trường còn lại giữ baseline `type=percent`, `discount_value=10`, `min_order_amount=100000`, `expired_at=2099-12-31`, `max_uses_per_user=1`.
4. Đọc HTTP status/body; dự kiến phải bị từ chối.
5. Gọi `GET /api/coupons` để kiểm tra `SAVE10` và `save10` cùng tồn tại.
6. Xóa row `save10` vừa tạo; giữ nguyên 4 seed.

```zsh
curl -s "$BASE/api/coupons" -H "Authorization: Bearer $ADMIN_TOKEN" \
  | jq '.[] | select(.code == "SAVE10")'

curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"save10","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

curl -s "$BASE/api/coupons" -H "Authorization: Bearer $ADMIN_TOKEN" \
  | jq '.[] | select(.code == "SAVE10" or .code == "save10")'
```

| Mốc / bước | Expected theo rule | Actual quan sát được (run `run-20261020-fr17`) |
| --- | --- | --- |
| Tạo `save10` khi đã có `SAVE10` | Non-2xx; không có row mới | `HTTP 200`; body `{"message":"Coupon created","id":10}` |
| Danh sách sau request | Chỉ có `SAVE10` | Có cả `SAVE10` và `save10`; row mới `id=10` |

**Kết luận:** Backend coi `SAVE10` và `save10` là hai giá trị duy nhất khác nhau, vi phạm quy tắc uniqueness không phân biệt hoa/thường. Người dùng có thể có hai coupon cùng nghĩa; nếu áp dụng mã, hành vi phụ thuộc vào cách tra cứu.

### Ảnh xác nhận API (người kiểm thử cung cấp)

> Ảnh Postman dưới đây xác nhận request/response API; **không dùng ảnh UI**. Ảnh được chụp ở lần chạy lại trên DB seed; id row trong ảnh là `5`, khác id `10` trong log run `run-20261020-fr17`, nhưng cùng request/response và cùng kết luận.

- `DT-07` — GET xác nhận seed `SAVE10` đã tồn tại:
  ![Ảnh seed SAVE10](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-07-CouponUppercase.png)
- `DT-07` — POST `code=save10` trả HTTP 200, tạo coupon:
  ![Ảnh POST save10](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-07-CreateCouponLowercase.png)
- `DT-07` — GET trả cả `SAVE10` và `save10`:
  ![Ảnh GET save10](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-07-GetCouponLowercase.png)

## Cách kiểm tra thủ công trên UI

**Trạng thái:** **API-only** — ô **Mã coupon** tự chuyển thành chữ hoa khi nhập, nên không thể gửi `save10` qua form thông thường. Không dùng devtools để coi là đường UI thông thường.

Không có bước UI thay thế cho cùng input/state; giữ đường API ở trên. Nếu nhập `save10` trên UI, giá trị gửi đi sẽ thành `SAVE10` và bị uniqueness chặn — đây là hành vi khác, không phải đường tái hiện bug.

## Bằng chứng

- Log/run: [`DT-07.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-07.log); tổng hợp [`FR17-evidence.md`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/FR17-evidence.md) — EV-FR17-007, run `run-20261020-fr17`.
- Screenshot: **Đã có 3 ảnh API** do người kiểm thử cung cấp (xem mục “Ảnh xác nhận API” ở trên); chỉ dùng ảnh Postman, không dùng ảnh UI.
- Lặp lại: **1/1** run API; ảnh chụp lần chạy lại xác nhận cùng hành vi.
- GitHub Issue: sẽ cập nhật sau khi tạo.

## Điều tra nguyên nhân (theo source, đã đối chiếu)

**Vị trí:** [`backend/database.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/backend/database.js#L31) dòng 31; [`backend/server.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/backend/server.js#L466-L479) dòng 466–479.

```sql
code TEXT UNIQUE,
```

```js
db.run(
  "INSERT INTO coupons (code, type, discount_value, min_order_amount, expired_at, max_uses_per_user) VALUES (?, ?, ?, ?, ?, ?)",
  [code, type, discount_value, min_order_amount, expired_at, max_uses_per_user || 1],
```

**Cơ chế:** Cột `code TEXT UNIQUE` dùng collation BINARY mặc định của SQLite, nên `SAVE10` và `save10` được xem là hai giá trị khác nhau. Route `POST` không chuẩn hóa `code` trước khi `INSERT`. UI che lỗi bằng `toUpperCase()`, nhưng API vẫn nhận được mã viết thường. Đây là nhận định từ mã nguồn; Expected/Actual ở trên dựa trên quy tắc người kiểm thử xác nhận và lần chạy thực tế.
