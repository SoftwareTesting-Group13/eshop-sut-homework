# BUG-FR17-01 — Tạo được coupon với `code` rỗng, thiếu hoặc chỉ khoảng trắng

> **Trạng thái:** Đã xác nhận qua API bằng ảnh Postman do người kiểm thử cung cấp; **chỉ dùng bằng chứng Postman/API, không dùng ảnh UI**. GitHub Issue: [#47](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/47).

## Tóm tắt

`POST /api/admin/coupons` trả HTTP 200 và tạo coupon khi `code` là chuỗi rỗng, bị bỏ hẳn khỏi JSON, hoặc chỉ gồm khoảng trắng. FR-17 quy định `code` là trường bắt buộc và duy nhất; cả ba input phải bị từ chối và không được tạo coupon.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | `FR-17` — Quản lý Mã Giảm Giá (Coupon CRUD); [`README.md` §5 FR-17](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/README.md#L213-L216) — `code` là trường bắt buộc và duy nhất; [`api_specification.md` §6.4](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/api_specification.md#L201-L213) |
| Test case | `DT-04` (`code=""`), `DT-05` (thiếu key `code`), `DT-06` (`code="   "` — ASSUMED: khoảng trắng không phải mã hợp lệ) |
| Build / môi trường | commit `f389502cdb308b133fe9044e34505f19202dd887`; Node v26.9.0 + Express + SQLite; API `http://localhost:3000`; DB test cách ly seed 4 coupon, không dùng DB làm việc |
| Severity / Priority | **Medium / Medium** — tạo được coupon không có mã có nghĩa; coupon vẫn `is_active=1` và có thể xuất hiện trong danh sách/áp dụng. Input rỗng/thiếu cần gọi API trực tiếp, nhưng chuỗi khoảng trắng có thể đi qua form UI thông thường |
| Trạng thái / lặp lại | **Đã xác nhận qua API** (ảnh Postman); UI không dùng làm bằng chứng; 1/1 run API cho mỗi input trong cùng run `run-20261020-fr17` |

## Chuẩn bị để tái hiện

- Tài khoản admin seed: `admin@eshop.com` / `Admin123!` (role `admin`).
- DB test cách ly đang có đúng 4 seed coupon: `SAVE10`, `BIGBUY`, `VIP100`, `EXPIRED`. Không chạy lệnh trên `backend/database.sqlite` của repo.
- Backend SUT đang chạy tại `http://localhost:3000`.
- Cần `curl` và `jq`; nếu không có `jq`, đọc trường `token`/`id` trực tiếp trong JSON response.

```zsh
BASE=http://localhost:3000
ADMIN_TOKEN=$(curl -s -X POST "$BASE/api/login" \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@eshop.com","password":"Admin123!"}' | jq -r .token)
echo "$ADMIN_TOKEN" | head -c 20; echo
```

## Các bước tái hiện và kết quả

**Đường tái hiện đã kiểm chứng:** API. UI chỉ có hướng dẫn dự kiến cho `DT-06`, chưa chạy.

1. Đăng nhập admin và lấy `ADMIN_TOKEN` bằng lệnh ở trên.
2. Gửi ba request `POST /api/admin/coupons`; các trường còn lại giữ baseline `type=percent`, `discount_value=10`, `min_order_amount=100000`, `expired_at=2099-12-31`, `max_uses_per_user=1`.
3. Đọc HTTP status/body. Cả ba trả `200` và trả về `id` của coupon vừa tạo.
4. Gọi `GET /api/coupons`, tìm các row vừa tạo và kiểm tra giá trị `code` thực tế.
5. Xóa các row vừa tạo bằng `DELETE /api/admin/coupons/{id}` (id lấy từ response), giữ nguyên 4 seed.

```zsh
# DT-04 — code rỗng
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

# DT-05 — bỏ hẳn key code
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

# DT-06 — ba khoảng trắng
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"   ","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

# Đọc các row vừa tạo; điều kiện lọc đúng cho cả ba input
curl -s "$BASE/api/coupons" -H "Authorization: Bearer $ADMIN_TOKEN" \
  | jq '.[] | select(.code == "" or .code == null or (.code | test("^ +$")))'
```

| Input | Expected theo rule | Actual quan sát được (run `run-20261020-fr17`) |
| --- | --- | --- |
| `code=""` | Non-2xx; không có row mới | `HTTP 200`; row `id=7`, `code=""`, các trường còn lại đúng baseline |
| Thiếu key `code` | Non-2xx; không có row mới | `HTTP 200`; row `id=8`, `code=null` |
| `code="   "` | Non-2xx; không có row mới (ASSUMED) | `HTTP 200`; row `id=9`, `code="   "` |

**Kết luận:** Backend không kiểm tra `code` trước khi `INSERT`; `UNIQUE` chỉ chặn giá trị trùng và SQLite cho phép nhiều `NULL`. Vì vậy coupon không có mã có nghĩa vẫn được tạo và có `is_active=1`; mã rỗng/`NULL`/khoảng trắng không phải mã có nghĩa để người dùng nhập, nhưng vẫn nằm trong dữ liệu quản lý và có thể khớp nếu gửi đúng chuỗi qua API.

### Ảnh xác nhận API (người kiểm thử cung cấp)

> Ảnh Postman dưới đây xác nhận request/response API; **không dùng ảnh UI**.

- `DT-04` — POST `code=""` trả 200; GET row `code=""`:
  ![Ảnh DT-04 request](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-01-CodeEmpty.png)
  ![Ảnh DT-04 GET](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-01-GetCodeEmpty.png)
- `DT-05` — POST thiếu key `code` trả 200; GET row `code=null`:
  ![Ảnh DT-05 request](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-01-MissingCode.png)
  ![Ảnh DT-05 GET](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-01-CodeNull.png)
- `DT-06` — **chưa có ảnh**; UI dự kiến nhập ba khoảng trắng, xem hướng dẫn bên dưới.

## Cách kiểm tra thủ công trên UI

**Trạng thái:** **Hướng dẫn dự kiến — chưa kiểm chứng UI** cho `DT-06`. `DT-04`/`DT-05` là API-only vì ô **Mã coupon** có `required` và form luôn gửi key `code`; không dùng devtools để coi là đường UI thông thường.

1. Mở `http://localhost:5174`, đăng nhập `admin@eshop.com` / `Admin123!`, chọn tab **Mã Giảm Giá**.
2. Trong form **Tạo mã giảm giá mới**, nhập **Mã coupon** = ba khoảng trắng; chọn **Loại** = `Phần trăm (%)`; **Giá trị** = `10`; **Đơn tối thiểu** = `100000`; **Ngày hết hạn** = `2099-12-31`; **Số lần dùng tối đa/người** = `1`; bấm **Tạo mã**.
3. Expected: không có row mới (mã toàn khoảng trắng không phải mã hợp lệ). Actual cần kiểm tra: row mới có cột **Mã** trắng/khó thấy trong bảng; không dùng ảnh UI làm bằng chứng. Sau đó bấm **Xóa** ở đúng row nếu row xuất hiện.

## Đối chiếu kỹ thuật

`GET /api/coupons` trả nguyên row vừa tạo, ví dụ với input thiếu `code`:

```json
{"id":8,"code":null,"type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","is_active":1,"max_uses_per_user":1}
```

Cần đối chiếu vì UI chỉ hiển thị cột **Mã**; API/DB mới cho thấy rõ `NULL`, chuỗi rỗng và khoảng trắng.

## Bằng chứng

- Log/run: [`DT-04.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-04.log), [`DT-05.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-05.log), [`DT-06.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-06.log); tổng hợp [`FR17-evidence.md`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/FR17-evidence.md) — EV-FR17-004…006, run `run-20261020-fr17`.
- Screenshot: **Đã có 4 ảnh API** do người kiểm thử cung cấp (xem mục “Ảnh xác nhận API” ở trên); chỉ dùng ảnh Postman, không dùng ảnh UI.
- Lặp lại: **1/1** run API cho mỗi input (ba input trong cùng run); chưa có rerun độc lập; UI không dùng làm bằng chứng.
- GitHub Issue: [#47](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/47).

## Điều tra nguyên nhân (theo source, đã đối chiếu)

**Vị trí:** [`backend/server.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/backend/server.js#L457-L481) dòng 457–481; [`backend/database.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/backend/database.js#L29-L38) dòng 31.

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
code TEXT UNIQUE,
```

**Cơ chế:** handler không kiểm tra `code` trước khi truyền thẳng vào `INSERT`; cột `code` không có `NOT NULL`/`CHECK`. `UNIQUE` không coi `NULL` là trùng và không chặn chuỗi rỗng/khoảng trắng. Vì vậy cả ba input đều tạo được row. Đây là nhận định từ mã nguồn; Expected/Actual ở trên dựa trên đặc tả và lần chạy thực tế.
