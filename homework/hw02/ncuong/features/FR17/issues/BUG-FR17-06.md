# BUG-FR17-06 — Tạo được coupon với `max_uses_per_user < 1` hoặc thiếu; number `0` bị đổi thành `1`

> **Trạng thái:** Đã xác nhận qua API bằng ảnh Postman do người kiểm thử cung cấp; **chỉ dùng bằng chứng Postman/API, không dùng ảnh UI**. GitHub Issue: [#52](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/52).

## Tóm tắt

`POST /api/admin/coupons` trả HTTP 200 và tạo coupon khi `max_uses_per_user` bằng `0`, bằng `-1`, hoặc bị bỏ hẳn khỏi JSON; number `0` còn bị âm thầm đổi thành `1`. FR-17 quy định `max_uses_per_user` là trường bắt buộc và phải là số nguyên `>= 1`; cả ba input phải bị từ chối thay vì được tạo.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | `FR-17` — Quản lý Mã Giảm Giá (Coupon CRUD); [`README.md` §5 FR-17](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/README.md#L213-L216) — `max_uses_per_user` là trường bắt buộc, `>= 1`; [`api_specification.md` §6.4](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/api_specification.md#L201-L213) |
| Test case | `DT-26` (`0` — dưới biên B2), `DT-27` (`-1`), `DT-28` (thiếu key) |
| Build / môi trường | commit `f389502cdb308b133fe9044e34505f19202dd887`; Node v26.9.0 + Express + SQLite; API `http://localhost:3000`; DB test cách ly seed 4 coupon |
| Severity / Priority | **Medium / Medium** — `0` bị đổi thành `1` (dữ liệu khác input), `-1` làm coupon bị coi là hết lượt ngay từ đầu, thiếu key được default thay vì từ chối; coupon vẫn `is_active=1`. Cả ba input đều API-only vì UI có `min="1"` |
| Trạng thái / lặp lại | **Đã xác nhận qua API** (ảnh Postman); UI không dùng làm bằng chứng; 1/1 run API cho mỗi input trong cùng run `run-20261020-fr17` |

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

**Đường tái hiện đã kiểm chứng:** API. UI không có đường thông thường vì **Số lần dùng tối đa/người** có `min="1"`; đây là finding API-only.

1. Đăng nhập admin và lấy `ADMIN_TOKEN` bằng lệnh ở trên.
2. Gửi ba request `POST /api/admin/coupons`; các trường còn lại giữ baseline `type=percent`, `discount_value=10`, `min_order_amount=100000`, `expired_at=2099-12-31`, `code` duy nhất.
3. Đọc HTTP status/body; cả ba trả `200` kèm `id` của coupon vừa tạo.
4. Gọi `GET /api/coupons`, kiểm tra `max_uses_per_user` thực tế của ba row.
5. Xóa ba row vừa tạo; giữ nguyên 4 seed.

```zsh
# DT-26 — max_uses_per_user = 0
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-26","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":0}'

# DT-27 — max_uses_per_user = -1
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-27","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":-1}'

# DT-28 — bỏ hẳn key max_uses_per_user
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-28","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31"}'

curl -s "$BASE/api/coupons" -H "Authorization: Bearer $ADMIN_TOKEN" \
  | jq '.[] | select(.code == "FR17-DT-26" or .code == "FR17-DT-27" or .code == "FR17-DT-28")'
```

| Input | Expected theo rule | Actual quan sát được (run `run-20261020-fr17`) |
| --- | --- | --- |
| `max_uses_per_user=0` | Non-2xx; không có row mới | `HTTP 200`; row `id=29`, `max_uses_per_user=1` (number `0` bị đổi thành `1`) |
| `max_uses_per_user=-1` | Non-2xx; không có row mới | `HTTP 200`; row `id=30`, `max_uses_per_user=-1` |
| Thiếu key `max_uses_per_user` | Non-2xx; không có row mới | `HTTP 200`; row `id=31`, `max_uses_per_user=1` |

**Kết luận:** Backend dùng `max_uses_per_user || 1`, nên number `0` và `undefined` bị thay bằng `1`, còn `-1` (truthy) được lưu nguyên. Cột `max_uses_per_user INTEGER DEFAULT 1` không có `CHECK >= 1`. Coupon `-1` bị coi là hết lượt ngay từ đầu vì `usage_count >= -1` luôn đúng trong FR-09; coupon `0` bị biến thành `1` mà không báo cho người tạo.

### Ảnh xác nhận API (người kiểm thử cung cấp)

> Ảnh Postman dưới đây xác nhận request/response API; **không dùng ảnh UI**.

- `DT-26` — POST `max_uses_per_user=0` trả 200; GET row lưu `max_uses_per_user=1`:
  ![Ảnh DT-26 request](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-06-MaxUsesPerUser0.png)
  ![Ảnh DT-26 GET](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-06-MaxUsesPerUser0Up1.png)
- `DT-27` — POST `max_uses_per_user=-1` trả 200; GET row `max_uses_per_user=-1`:
  ![Ảnh DT-27 request](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-06-MaxUsesPerUserNegative.png)
  ![Ảnh DT-27 GET](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-06-GetMaxUsesPerUserNegative.png)
- `DT-28` — POST thiếu key `max_uses_per_user` trả 200; GET row lưu `max_uses_per_user=1`:
  ![Ảnh DT-28 request](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-06-MissingMaxUses.png)
  ![Ảnh DT-28 GET](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-06-GetMissingMaxUses.png)

## Cách kiểm tra thủ công trên UI

**Trạng thái:** **API-only** — control **Số lần dùng tối đa/người** có `min="1"`; trình duyệt chặn `0`/`-1` khi submit. Người dùng thông thường không gửi được cùng input/state; không dùng devtools để coi là đường UI thông thường.

Không có bước UI thay thế cho cùng input/state; giữ đường API ở trên. Nếu xóa trắng ô, form gửi `""` — đây là input khác với "bỏ hẳn key" và cũng không gán cho `DT-26`/`DT-28`.

## Đối chiếu kỹ thuật

`GET /api/coupons` trả nguyên row, ví dụ:

```json
{"id":29,"code":"FR17-DT-26","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","is_active":1,"max_uses_per_user":1}
```

Cần đối chiếu vì response tạo coupon không trả lại giá trị đã lưu; phải đọc `GET` mới thấy `0` đã thành `1`.

## Bằng chứng

- Log/run: [`DT-26.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-26.log), [`DT-27.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-27.log), [`DT-28.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-28.log); tổng hợp [`FR17-evidence.md`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/FR17-evidence.md) — EV-FR17-026…028, run `run-20261020-fr17`.
- Screenshot: **Đã có 6 ảnh API** do người kiểm thử cung cấp (xem mục “Ảnh xác nhận API” ở trên); chỉ dùng ảnh Postman, không dùng ảnh UI.
- Lặp lại: **1/1** run API cho mỗi input (ba input trong cùng run); chưa có rerun độc lập; UI không dùng làm bằng chứng.
- GitHub Issue: [#52](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/52).

## Điều tra nguyên nhân (theo source, đã đối chiếu)

**Vị trí:** [`backend/server.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/backend/server.js#L474) dòng 474; [`backend/database.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/backend/database.js#L37) dòng 37.

```js
      max_uses_per_user || 1,
```

```sql
max_uses_per_user INTEGER DEFAULT 1
```

**Cơ chế:** `max_uses_per_user` không được kiểm tra `>= 1` trước khi `INSERT`. Toán tử `||` biến number `0` và `undefined` thành `1`; `-1` là truthy nên được giữ nguyên. Cột `max_uses_per_user` chỉ có default, không có `CHECK`. Đây là nhận định từ mã nguồn; Expected/Actual ở trên dựa trên đặc tả và lần chạy thực tế.
