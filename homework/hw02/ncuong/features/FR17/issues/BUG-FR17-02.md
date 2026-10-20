# BUG-FR17-02 — Tạo được coupon với `type` ngoài `percent/fixed` hoặc thiếu `type`

> **Trạng thái:** Đã xác nhận qua API bằng ảnh Postman do người kiểm thử cung cấp; **chỉ dùng bằng chứng Postman/API, không dùng ảnh UI**. GitHub Issue: [#48](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/48).

## Tóm tắt

`POST /api/admin/coupons` trả HTTP 200 và tạo coupon khi `type` là `"percentage"` (ngoài enum) hoặc bị bỏ hẳn khỏi JSON. FR-17 quy định `type` là trường bắt buộc và chỉ nhận `percent` hoặc `fixed`; cả hai input phải bị từ chối.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | `FR-17` — Quản lý Mã Giảm Giá (Coupon CRUD); [`README.md` §5 FR-17](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/README.md#L213-L216) — `type` là trường bắt buộc, chỉ nhận `percent/fixed`; [`api_specification.md` §6.4](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/api_specification.md#L201-L213) |
| Test case | `DT-08` (`type="percentage"`), `DT-09` (thiếu key `type`) |
| Build / môi trường | commit `f389502cdb308b133fe9044e34505f19202dd887`; Node v26.9.0 + Express + SQLite; API `http://localhost:3000`; DB test cách ly seed 4 coupon |
| Severity / Priority | **Medium / Medium** — coupon có `type` không hợp lệ vẫn được tạo và `is_active=1`; khi áp dụng, nhánh `else` của FR-09 coi mọi giá trị khác `percent` là `fixed`, nên cách tính giảm giá có thể sai. Tuy nhiên input không đi qua select UI thông thường, cần API trực tiếp |
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

**Đường tái hiện đã kiểm chứng:** API. UI không có đường thông thường vì **Loại** là `<select>` chỉ có `percent`/`fixed`; đây là finding API-only.

1. Đăng nhập admin và lấy `ADMIN_TOKEN` bằng lệnh ở trên.
2. Gửi hai request `POST /api/admin/coupons`; các trường còn lại giữ baseline `code` duy nhất, `discount_value=10`, `min_order_amount=100000`, `expired_at=2099-12-31`, `max_uses_per_user=1`.
3. Đọc HTTP status/body; cả hai trả `200` kèm `id` của coupon vừa tạo.
4. Gọi `GET /api/coupons`, kiểm tra `type` thực tế của hai row.
5. Xóa hai row vừa tạo bằng `DELETE /api/admin/coupons/{id}`; giữ nguyên 4 seed.

```zsh
# DT-08 — type ngoài enum
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-08","type":"percentage","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

# DT-09 — bỏ hẳn key type
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-09","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

curl -s "$BASE/api/coupons" -H "Authorization: Bearer $ADMIN_TOKEN" \
  | jq '.[] | select(.code == "FR17-DT-08" or .code == "FR17-DT-09")'
```

| Input | Expected theo rule | Actual quan sát được (run `run-20261020-fr17`) |
| --- | --- | --- |
| `type="percentage"` | Non-2xx; không có row mới | `HTTP 200`; row `id=11`, `type="percentage"` |
| Thiếu key `type` | Non-2xx; không có row mới | `HTTP 200`; row `id=12`, `type=null` |

**Kết luận:** Backend không kiểm tra enum/bắt buộc của `type`; cột `type` có default `percent` nhưng giá trị `undefined` được bind thành `NULL`, ghi đè default. Coupon sai `type` vẫn được tạo với `is_active=1`. Khi áp dụng, `server.js:398-404` chỉ kiểm tra `coupon.type === "percent"`, còn mọi giá trị khác rơi vào nhánh `fixed`, dẫn tới cách tính giảm giá không đúng loại coupon.

### Ảnh xác nhận API (người kiểm thử cung cấp)

> Ảnh Postman dưới đây xác nhận request/response API; **không dùng ảnh UI**.

- `DT-08` — POST `type="percentage"` trả 200; GET row `type="percentage"`:
  ![Ảnh DT-08 request](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-02-TypeInvalid.png)
  ![Ảnh DT-08 GET](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-02-GetCodeHasTypeInvalid.png)
- `DT-09` — POST thiếu key `type` trả 200; GET row `type=null`:
  ![Ảnh DT-09 request](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-02-MissingType.png)
  ![Ảnh DT-09 GET](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-02-GetNullType.png)

## Cách kiểm tra thủ công trên UI

**Trạng thái:** **API-only** — control **Loại** là `<select>` chỉ có `Phần trăm (%)` (`percent`) và `Số tiền cố định (₫)` (`fixed`); người dùng thông thường không gửi được `"percentage"` hoặc bỏ hẳn key `type`. Không dùng devtools để coi là đường UI thông thường.

Không có bước UI thay thế cho cùng input/state; giữ đường API ở trên.

## Đối chiếu kỹ thuật

`GET /api/coupons` trả nguyên row, ví dụ:

```json
{
  "id":12,
  "code":"FR17-DT-09",
  "type":null,
  "discount_value":10,
  "min_order_amount":100000,
  "expired_at":"2099-12-31",
  "is_active":1,
  "max_uses_per_user":1
}
```

Cần đối chiếu vì UI không hiển thị giá trị `type` thô; bảng chỉ hiển thị nhãn **Cố định** cho mọi giá trị khác `percent`.

## Bằng chứng

- Log/run: [`DT-08.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-08.log), [`DT-09.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-09.log); tổng hợp [`FR17-evidence.md`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/FR17-evidence.md) — EV-FR17-008/009, run `run-20261020-fr17`.
- Screenshot: **Đã có 4 ảnh API** do người kiểm thử cung cấp (xem mục “Ảnh xác nhận API” ở trên); chỉ dùng ảnh Postman, không dùng ảnh UI.
- Lặp lại: **1/1** run API cho mỗi input (hai input trong cùng run); chưa có rerun độc lập; UI không dùng làm bằng chứng.
- GitHub Issue: [#48](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/48).

## Điều tra nguyên nhân (theo source, đã đối chiếu)

**Vị trí:** [`backend/server.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/backend/server.js#L457-L481) dòng 457–481; [`backend/database.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/backend/database.js#L32) dòng 32.

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
type TEXT DEFAULT 'percent',
```

**Cơ chế:** handler không kiểm tra `type` thuộc `percent/fixed` trước khi `INSERT`; cột `type` chỉ có default, không có `CHECK`/`NOT NULL`. Khi key `type` bị bỏ, giá trị `undefined` được bind thành `NULL` và ghi đè default. Đây là nhận định từ mã nguồn; Expected/Actual ở trên dựa trên đặc tả và lần chạy thực tế.
