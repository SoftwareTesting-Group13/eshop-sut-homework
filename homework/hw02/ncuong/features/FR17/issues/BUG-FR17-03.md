# BUG-FR17-03 — Tạo được coupon với `discount_value <= 0`, không phải số hoặc thiếu

> **Trạng thái:** Đã xác nhận qua API bằng ảnh Postman do người kiểm thử cung cấp; **chỉ dùng bằng chứng Postman/API, không dùng ảnh UI**.

## Tóm tắt

`POST /api/admin/coupons` trả HTTP 200 và tạo coupon khi `discount_value` bằng `0`, bằng `-1`, bị bỏ hẳn khỏi JSON, hoặc là chuỗi `"abc"`. FR-17 quy định `discount_value` là trường bắt buộc và phải là số dương; cả bốn input phải bị từ chối.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | `FR-17` — Quản lý Mã Giảm Giá (Coupon CRUD); [`README.md` §5 FR-17](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/README.md#L213-L216) — `discount_value` là trường bắt buộc, phải dương; [`api_specification.md` §6.4](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/api_specification.md#L201-L213) |
| Test case | `DT-10` (`0` — biên B3), `DT-11` (`-1` — dưới biên B3), `DT-12` (thiếu key), `DT-13` (`"abc"`) |
| Build / môi trường | commit `f389502cdb308b133fe9044e34505f19202dd887`; Node v26.9.0 + Express + SQLite; API `http://localhost:3000`; DB test cách ly seed 4 coupon |
| Severity / Priority | **High / High** — coupon `0%`/`-1%`/`NULL`/`"abc"` vẫn `is_active=1`; khi áp dụng, công thức percent hiện tại `total * (1 - discount_value)` có thể cho giảm giá âm hoặc `NaN`, ảnh hưởng trực tiếp số tiền người dùng phải trả (FR-09). `0`/`-1` đi được qua form UI thông thường |
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

**Đường tái hiện đã kiểm chứng:** API. UI có hướng dẫn dự kiến cho `DT-10`/`DT-11`, chưa chạy.

1. Đăng nhập admin và lấy `ADMIN_TOKEN` bằng lệnh ở trên.
2. Gửi bốn request `POST /api/admin/coupons`; các trường còn lại giữ baseline `type=percent`, `min_order_amount=100000`, `expired_at=2099-12-31`, `max_uses_per_user=1`, `code` duy nhất.
3. Đọc HTTP status/body; cả bốn trả `200` kèm `id` của coupon vừa tạo.
4. Gọi `GET /api/coupons`, kiểm tra `discount_value` thực tế của bốn row.
5. Xóa bốn row vừa tạo; giữ nguyên 4 seed.

```zsh
# DT-10 — discount_value = 0
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-10","type":"percent","discount_value":0,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

# DT-11 — discount_value = -1
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-11","type":"percent","discount_value":-1,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

# DT-12 — bỏ hẳn key discount_value
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-12","type":"percent","min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

# DT-13 — discount_value = "abc"
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-13","type":"percent","discount_value":"abc","min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

curl -s "$BASE/api/coupons" -H "Authorization: Bearer $ADMIN_TOKEN" \
  | jq '.[] | select(.code == "FR17-DT-10" or .code == "FR17-DT-11" or .code == "FR17-DT-12" or .code == "FR17-DT-13")'
```

| Input | Expected theo rule | Actual quan sát được (run `run-20261020-fr17`) |
| --- | --- | --- |
| `discount_value=0` | Non-2xx; không có row mới | `HTTP 200`; row `id=13`, `discount_value=0` |
| `discount_value=-1` | Non-2xx; không có row mới | `HTTP 200`; row `id=14`, `discount_value=-1` |
| Thiếu key `discount_value` | Non-2xx; không có row mới | `HTTP 200`; row `id=15`, `discount_value=null` |
| `discount_value="abc"` | Non-2xx; không có row mới | `HTTP 200`; row `id=16`, `discount_value="abc"` (typeof text) |

**Kết luận:** Backend không kiểm tra kiểu số và điều kiện `> 0`; cột `discount_value INTEGER` không có `CHECK`. Coupon sai giá trị vẫn được tạo và active. Với coupon `percent`, `server.js:398-401` tính `total_amount * (1 - discount_value)`, nên `0` cho giảm giá bằng đúng tổng đơn, `-1` cho giảm giá vượt tổng, `"abc"` cho `NaN`; đây là hệ quả nghiêm trọng khi coupon được áp dụng.

### Ảnh xác nhận API (người kiểm thử cung cấp)

> Ảnh Postman dưới đây xác nhận request/response API; **không phải ảnh UI**. UI vẫn chưa kiểm chứng.

- `DT-10` — POST `discount_value=0` trả 200; GET row `discount_value=0`:
  ![Ảnh DT-10 request](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-03-DiscountValue0.png)
  ![Ảnh DT-10 GET](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-03-GetDiscountValue0.png)
- `DT-11` — POST `discount_value=-1` trả 200; GET row `discount_value=-1`:
  ![Ảnh DT-11 request](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-03-DiscountValueNegative.png)
  ![Ảnh DT-11 GET](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-03-GetDiscountNegative.png)
- `DT-12` — POST thiếu key `discount_value` trả 200; GET row `discount_value=null`:
  ![Ảnh DT-12 request](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-03-MissingDiscountValue.png)
  ![Ảnh DT-12 GET](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-03-GetMissingDiscountValue.png)
- `DT-13` — POST `discount_value="abc"` trả 200; GET row `discount_value="abc"`:
  ![Ảnh DT-13 request](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-03-DiscountValueInvalid.png)
  ![Ảnh DT-13 GET](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-03-GetDiscountValueInvalid.png)

## Cách kiểm tra thủ công trên UI

**Trạng thái:** **Hướng dẫn dự kiến — chưa kiểm chứng UI** cho `DT-10`/`DT-11`. `DT-12`/`DT-13` là API-only vì ô **Giá trị** có `required` và `type="number"`.

1. Mở `http://localhost:5174`, đăng nhập `admin@eshop.com` / `Admin123!`, chọn tab **Mã Giảm Giá**.
2. Với `DT-10`: nhập **Mã coupon** = `FR17-UI-DT-10` (mã chỉ để phân biệt row UI với row API, không phải biến đang kiểm tra); **Loại** = `Phần trăm (%)`; **Giá trị** = `0`; **Đơn tối thiểu** = `100000`; **Ngày hết hạn** = `2099-12-31`; **Số lần** = `1`; bấm **Tạo mã**. Lặp lại với `DT-11`, **Giá trị** = `-1`, mã `FR17-UI-DT-11`.
3. Expected: không có row mới. Actual cần kiểm tra: row mới hiển thị `0%` hoặc `-1%`; chụp screenshot bảng. Sau đó bấm **Xóa** ở đúng row nếu row xuất hiện.

Không dùng ô **Giá trị** trống để đại diện cho `DT-12`: UI gửi chuỗi rỗng `""`, khác với input bỏ hẳn key; đó là input khác, không gán cho test case này.

## Đối chiếu kỹ thuật

`GET /api/coupons` trả nguyên row, ví dụ:

```json
{"id":16,"code":"FR17-DT-13","type":"percent","discount_value":"abc","min_order_amount":100000,"expired_at":"2099-12-31","is_active":1,"max_uses_per_user":1}
```

Cần đối chiếu vì UI có thể hiển thị `abc ₫`/`NaN%` hoặc không phân biệt được kiểu dữ liệu; API/DB cho thấy giá trị thô.

## Bằng chứng

- Log/run: [`DT-10.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-10.log), [`DT-11.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-11.log), [`DT-12.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-12.log), [`DT-13.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-13.log); tổng hợp [`FR17-evidence.md`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/FR17-evidence.md) — EV-FR17-010…013, run `run-20261020-fr17`.
- Screenshot: **Đã có 8 ảnh API** do người kiểm thử cung cấp (xem mục “Ảnh xác nhận API” ở trên); chỉ dùng ảnh Postman, không dùng ảnh UI.
- Lặp lại: **1/1** run API cho mỗi input (bốn input trong cùng run); chưa có rerun độc lập và chưa chạy UI.
- GitHub Issue: **Chưa mở** — người kiểm thử quyết định publish từ draft này.

## Điều tra nguyên nhân (theo source, đã đối chiếu)

**Vị trí:** [`backend/server.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/backend/server.js#L457-L481) dòng 457–481; [`backend/database.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/backend/database.js#L33) dòng 33.

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
discount_value INTEGER,
```

**Cơ chế:** handler không kiểm tra `discount_value` là số hữu hạn và `> 0` trước khi `INSERT`; cột `discount_value INTEGER` không có `CHECK`. SQLite giữ nguyên `0`/`-1`, lưu `NULL` khi thiếu key, và lưu `"abc"` dưới dạng text vì không chuyển được thành số. Đây là nhận định từ mã nguồn; Expected/Actual ở trên dựa trên đặc tả và lần chạy thực tế.
