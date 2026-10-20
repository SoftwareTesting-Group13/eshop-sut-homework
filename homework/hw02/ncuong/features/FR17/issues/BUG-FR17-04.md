# BUG-FR17-04 — Tạo được coupon với `expired_at` thiếu, rỗng hoặc sai định dạng

> **Trạng thái:** Đã xác nhận qua API bằng ảnh Postman do người kiểm thử cung cấp; **chỉ dùng bằng chứng Postman/API, không dùng ảnh UI**.

## Tóm tắt

`POST /api/admin/coupons` trả HTTP 200 và tạo coupon khi `expired_at` bị bỏ hẳn khỏi JSON, là chuỗi rỗng, hoặc là chuỗi `"not-a-date"`. FR-17 quy định `expired_at` là trường bắt buộc; định dạng ngày hợp lệ là ASSUMED từ API example `YYYY-MM-DD` và UI `type="date"`.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | `FR-17` — Quản lý Mã Giảm Giá (Coupon CRUD); [`README.md` §5 FR-17](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/README.md#L213-L216) — `expired_at` là trường bắt buộc; [`api_specification.md` §6.4](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/api_specification.md#L201-L213) dùng ví dụ `2025-01-31` |
| Test case | `DT-15` (thiếu key), `DT-16` (`""`), `DT-17` (`"not-a-date"` — ASSUMED: phải là ngày hợp lệ) |
| Build / môi trường | commit `f389502cdb308b133fe9044e34505f19202dd887`; Node v26.9.0 + Express + SQLite; API `http://localhost:3000`; DB test cách ly seed 4 coupon |
| Severity / Priority | **High / High** — coupon có expiry `NULL`/rỗng/không parse được vẫn `is_active=1`; điều kiện C2 của FR-09 dựa trên `new Date(expired_at)`, nên coupon có thể không bao giờ hết hạn hoặc không bao giờ áp dụng được. Input không đi qua form UI thông thường vì ô ngày có `required`/`type="date"` |
| Trạng thái / lặp lại | **Đã xác nhận qua API** (ảnh Postman); UI chưa chạy; 1/1 run API cho mỗi input trong cùng run `run-20261020-fr17` |

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

**Đường tái hiện đã kiểm chứng:** API. UI không có đường thông thường vì **Ngày hết hạn** có `required` và `type="date"`; đây là finding API-only.

1. Đăng nhập admin và lấy `ADMIN_TOKEN` bằng lệnh ở trên.
2. Gửi ba request `POST /api/admin/coupons`; các trường còn lại giữ baseline `type=percent`, `discount_value=10`, `min_order_amount=100000`, `max_uses_per_user=1`, `code` duy nhất.
3. Đọc HTTP status/body; cả ba trả `200` kèm `id` của coupon vừa tạo.
4. Gọi `GET /api/coupons`, kiểm tra `expired_at` thực tế của ba row.
5. Xóa ba row vừa tạo; giữ nguyên 4 seed.

```zsh
# DT-15 — bỏ hẳn key expired_at
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-15","type":"percent","discount_value":10,"min_order_amount":100000,"max_uses_per_user":1}'

# DT-16 — expired_at = ""
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-16","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"","max_uses_per_user":1}'

# DT-17 — expired_at = "not-a-date"
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-17","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"not-a-date","max_uses_per_user":1}'

curl -s "$BASE/api/coupons" -H "Authorization: Bearer $ADMIN_TOKEN" \
  | jq '.[] | select(.code == "FR17-DT-15" or .code == "FR17-DT-16" or .code == "FR17-DT-17")'
```

| Input | Expected theo rule | Actual quan sát được (run `run-20261020-fr17`) |
| --- | --- | --- |
| Thiếu key `expired_at` | Non-2xx; không có row mới | `HTTP 200`; row `id=18`, `expired_at=null` |
| `expired_at=""` | Non-2xx; không có row mới | `HTTP 200`; row `id=19`, `expired_at=""` |
| `expired_at="not-a-date"` | Non-2xx; không có row mới (ASSUMED format) | `HTTP 200`; row `id=20`, `expired_at="not-a-date"` |

**Kết luận:** Backend không kiểm tra `expired_at` có tồn tại và parse được thành ngày hợp lệ; cột `expired_at DATETIME` không có `NOT NULL`/`CHECK`. Coupon với expiry sai vẫn được tạo và active. Trong FR-09, `new Date("")` và `new Date("not-a-date")` là `Invalid Date`, nên phép so sánh `expiry < now` trả `false` và coupon có thể được coi là còn hạn; `new Date(null)` là 1970 nên coupon `NULL` luôn bị coi là hết hạn.

### Ảnh xác nhận API (người kiểm thử cung cấp)

> Ảnh Postman dưới đây xác nhận request/response API; **không phải ảnh UI**. UI vẫn chưa kiểm chứng.

- `DT-15` — POST thiếu key `expired_at` trả 200; GET row `expired_at=null`:
  ![Ảnh DT-15 request](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-04-MissingExpiredAt.png)
  ![Ảnh DT-15 GET](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-04-GetMissingExpiredAt.png)
- `DT-16` — POST `expired_at=""` trả 200; GET row `expired_at=""`:
  ![Ảnh DT-16 request](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-04-EmptyExpiredAt.png)
  ![Ảnh DT-16 GET](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-04-GetEmptyExpiredAt.png)
- `DT-17` — POST `expired_at="not-a-date"` trả 200; GET row `expired_at="not-a-date"`:
  ![Ảnh DT-17 request](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-04-InvalidExpiredAt.png)
  ![Ảnh DT-17 GET](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-04-GetInvalidExpiredAt.png)

## Cách kiểm tra thủ công trên UI

**Trạng thái:** **API-only** — control **Ngày hết hạn** là `input type="date"` và có `required`; trình duyệt chặn chuỗi rỗng/không phải ngày, còn form luôn gửi key `expired_at`. Người dùng thông thường không gửi được cùng input/state; không dùng devtools để coi là đường UI thông thường.

Không có bước UI thay thế cho cùng input/state; giữ đường API ở trên.

## Đối chiếu kỹ thuật

`GET /api/coupons` trả nguyên row, ví dụ:

```json
{"id":20,"code":"FR17-DT-17","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"not-a-date","is_active":1,"max_uses_per_user":1}
```

Cần đối chiếu vì UI có thể hiển thị chuỗi ngày sai hoặc `Invalid Date` khác nhau; API/DB cho thấy giá trị thô.

## Bằng chứng

- Log/run: [`DT-15.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-15.log), [`DT-16.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-16.log), [`DT-17.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-17.log); tổng hợp [`FR17-evidence.md`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/FR17-evidence.md) — EV-FR17-015…017, run `run-20261020-fr17`.
- Screenshot: **Đã có 6 ảnh API** do người kiểm thử cung cấp (xem mục “Ảnh xác nhận API” ở trên); chỉ dùng ảnh Postman, không dùng ảnh UI.
- Lặp lại: **1/1** run API cho mỗi input (ba input trong cùng run); chưa có rerun độc lập và chưa chạy UI.
- GitHub Issue: **Chưa mở** — người kiểm thử quyết định publish từ draft này.

## Điều tra nguyên nhân (theo source, đã đối chiếu)

**Vị trí:** [`backend/server.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/backend/server.js#L457-L481) dòng 457–481; [`backend/database.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/backend/database.js#L35) dòng 35.

```js
app.post("/api/admin/coupons", authenticateToken, (req, res) => {
  const {
    code,
    type,
    discount_value,
    min_order_amount,
    expired_at,
    max_uses_per_user,
  } = req.body;
  db.run(
    "INSERT INTO coupons (code, type, discount_value, min_order_amount, expired_at, max_uses_per_user) VALUES (?, ?, ?, ?, ?, ?)",
    [code, type, discount_value, min_order_amount, expired_at, max_uses_per_user || 1],
```

```sql
expired_at DATETIME,
```

**Cơ chế:** handler không kiểm tra `expired_at` trước khi `INSERT`; cột `expired_at DATETIME` không có `NOT NULL`/`CHECK`. SQLite lưu `NULL`, chuỗi rỗng và chuỗi bất kỳ vào cột này. Đây là nhận định từ mã nguồn; Expected/Actual ở trên dựa trên đặc tả và lần chạy thực tế.
