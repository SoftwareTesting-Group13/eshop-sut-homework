# BUG-FR17-05 — Tạo được coupon với `min_order_amount` âm, không phải số hoặc thiếu

> **Trạng thái:** Đã xác nhận qua API bằng ảnh Postman do người kiểm thử cung cấp; **chỉ dùng bằng chứng Postman/API, không dùng ảnh UI**.

## Tóm tắt

`POST /api/admin/coupons` trả HTTP 200 và tạo coupon khi `min_order_amount` bằng `-1`, bị bỏ hẳn khỏi JSON, hoặc là chuỗi `"abc"`. FR-17 quy định `min_order_amount` là trường bắt buộc và phải là số `>= 0`; cả ba input phải bị từ chối.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | `FR-17` — Quản lý Mã Giảm Giá (Coupon CRUD); [`README.md` §5 FR-17](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/README.md#L213-L216) — `min_order_amount` là trường bắt buộc, `>= 0`; [`api_specification.md` §6.4](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/api_specification.md#L201-L213) |
| Test case | `DT-21` (`-1` — dưới biên B1), `DT-22` (thiếu key), `DT-23` (`"abc"`) |
| Build / môi trường | commit `f389502cdb308b133fe9044e34505f19202dd887`; Node v26.9.0 + Express + SQLite; API `http://localhost:3000`; DB test cách ly seed 4 coupon |
| Severity / Priority | **Medium / Medium** — `-1` vô hiệu hóa ngưỡng đơn tối thiểu (mọi đơn đều đủ điều kiện), `NULL`/`"abc"` có thể làm coupon không bao giờ áp dụng hoặc so sánh sai; coupon vẫn `is_active=1`. `-1` đi được qua form UI thông thường |
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

**Đường tái hiện đã kiểm chứng:** API. UI có hướng dẫn dự kiến cho `DT-21`, chưa chạy.

1. Đăng nhập admin và lấy `ADMIN_TOKEN` bằng lệnh ở trên.
2. Gửi ba request `POST /api/admin/coupons`; các trường còn lại giữ baseline `type=percent`, `discount_value=10`, `expired_at=2099-12-31`, `max_uses_per_user=1`, `code` duy nhất.
3. Đọc HTTP status/body; cả ba trả `200` kèm `id` của coupon vừa tạo.
4. Gọi `GET /api/coupons`, kiểm tra `min_order_amount` thực tế của ba row.
5. Xóa ba row vừa tạo; giữ nguyên 4 seed.

```zsh
# DT-21 — min_order_amount = -1
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-21","type":"percent","discount_value":10,"min_order_amount":-1,"expired_at":"2099-12-31","max_uses_per_user":1}'

# DT-22 — bỏ hẳn key min_order_amount
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-22","type":"percent","discount_value":10,"expired_at":"2099-12-31","max_uses_per_user":1}'

# DT-23 — min_order_amount = "abc"
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-23","type":"percent","discount_value":10,"min_order_amount":"abc","expired_at":"2099-12-31","max_uses_per_user":1}'

curl -s "$BASE/api/coupons" -H "Authorization: Bearer $ADMIN_TOKEN" \
  | jq '.[] | select(.code == "FR17-DT-21" or .code == "FR17-DT-22" or .code == "FR17-DT-23")'
```

| Input | Expected theo rule | Actual quan sát được (run `run-20261020-fr17`) |
| --- | --- | --- |
| `min_order_amount=-1` | Non-2xx; không có row mới | `HTTP 200`; row `id=24`, `min_order_amount=-1` |
| Thiếu key `min_order_amount` | Non-2xx; không có row mới | `HTTP 200`; row `id=25`, `min_order_amount=null` |
| `min_order_amount="abc"` | Non-2xx; không có row mới | `HTTP 200`; row `id=26`, `min_order_amount="abc"` |

**Kết luận:** Backend không kiểm tra kiểu số và điều kiện `>= 0`; cột `min_order_amount INTEGER DEFAULT 0` không có `CHECK`, và giá trị `undefined` được bind thành `NULL` nên default `0` không được áp dụng. Với `-1`, mọi đơn đều thỏa `total_amount > min_order_amount`; với `NULL`/`"abc"`, phép so sánh trong FR-09 không còn đúng nghĩa, coupon có thể không bao giờ áp dụng.

### Ảnh xác nhận API (người kiểm thử cung cấp)

> Ảnh Postman dưới đây xác nhận request/response API; **không phải ảnh UI**. UI vẫn chưa kiểm chứng.

- `DT-21` — POST `min_order_amount=-1` trả 200; GET row `min_order_amount=-1`:
  ![Ảnh DT-21 request](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-05-MinOrderNegative.png)
  ![Ảnh DT-21 GET](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-05-GetMinOrderNegative.png)
- `DT-22` — POST thiếu key `min_order_amount` trả 200; GET row `min_order_amount=null`:
  ![Ảnh DT-22 request](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-05-MissingMinOrderAmount.png)
  ![Ảnh DT-22 GET](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-05-GetMissingMinOrderAmount.png)
- `DT-23` — POST `min_order_amount="abc"` trả 200; GET row `min_order_amount="abc"`:
  ![Ảnh DT-23 request](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-05-InvalidMinOrder.png)
  ![Ảnh DT-23 GET](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-05-GetInvalidMinOrder.png)

## Cách kiểm tra thủ công trên UI

**Trạng thái:** **Hướng dẫn dự kiến — chưa kiểm chứng UI** cho `DT-21`. `DT-22`/`DT-23` là API-only vì form luôn gửi key và ô **Đơn tối thiểu** là `type="number"`.

1. Mở `http://localhost:5174`, đăng nhập `admin@eshop.com` / `Admin123!`, chọn tab **Mã Giảm Giá**.
2. Nhập **Mã coupon** = `FR17-UI-DT-21` (mã chỉ để phân biệt row UI với row API, không phải biến đang kiểm tra); **Loại** = `Phần trăm (%)`; **Giá trị** = `10`; **Đơn tối thiểu** = `-1`; **Ngày hết hạn** = `2099-12-31`; **Số lần** = `1`; bấm **Tạo mã**.
3. Expected: không có row mới. Actual cần kiểm tra: row mới hiển thị `-1 ₫` ở cột **Đơn tối thiểu**; chụp screenshot bảng. Sau đó bấm **Xóa** ở đúng row nếu row xuất hiện.

Không dùng ô **Đơn tối thiểu** trống để đại diện cho `DT-22`: UI gửi chuỗi rỗng `""`, khác với input bỏ hẳn key; đó là input khác, không gán cho test case này.

## Đối chiếu kỹ thuật

`GET /api/coupons` trả nguyên row, ví dụ:

```json
{"id":26,"code":"FR17-DT-23","type":"percent","discount_value":10,"min_order_amount":"abc","expired_at":"2099-12-31","is_active":1,"max_uses_per_user":1}
```

Cần đối chiếu vì UI có thể hiển thị `undefined ₫`/blank hoặc `abc ₫`; API/DB cho thấy giá trị thô.

## Bằng chứng

- Log/run: [`DT-21.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-21.log), [`DT-22.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-22.log), [`DT-23.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-23.log); tổng hợp [`FR17-evidence.md`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/FR17-evidence.md) — EV-FR17-021…023, run `run-20261020-fr17`.
- Screenshot: **Đã có 6 ảnh API** do người kiểm thử cung cấp (xem mục “Ảnh xác nhận API” ở trên); chỉ dùng ảnh Postman, không dùng ảnh UI.
- Lặp lại: **1/1** run API cho mỗi input (ba input trong cùng run); chưa có rerun độc lập và chưa chạy UI.
- GitHub Issue: **Chưa mở** — người kiểm thử quyết định publish từ draft này.

## Điều tra nguyên nhân (theo source, đã đối chiếu)

**Vị trí:** [`backend/server.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/backend/server.js#L457-L481) dòng 457–481; [`backend/database.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/backend/database.js#L34) dòng 34.

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
min_order_amount INTEGER DEFAULT 0,
```

**Cơ chế:** handler không kiểm tra `min_order_amount` là số hữu hạn và `>= 0` trước khi `INSERT`; cột chỉ có default, không có `CHECK`. Khi key bị bỏ, `undefined` bind thành `NULL` và default `0` không được áp dụng. Đây là nhận định từ mã nguồn; Expected/Actual ở trên dựa trên đặc tả và lần chạy thực tế.
