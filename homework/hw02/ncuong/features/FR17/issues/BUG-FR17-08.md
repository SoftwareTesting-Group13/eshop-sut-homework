# BUG-FR17-08 — Tạo được coupon `percent` với `discount_value = 150` (vượt 100%)

> **Trạng thái:** Đã xác nhận qua API bằng ảnh Postman; bổ sung **1 ảnh UI** minh họa hệ quả khi áp dụng coupon `150%` (không thay thế bằng chứng API). GitHub Issue: [#54](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54).

## Tóm tắt

`POST /api/admin/coupons` trả HTTP 200 và tạo coupon `type = "percent"`, `discount_value = 150`; `GET /api/coupons` lưu nguyên `150`. FR-17 yêu cầu `discount_value` dương; người kiểm thử xác nhận với `type = percent`, mức giảm không được vượt quá `100`, vì `150%` không phải mức giảm hợp lệ.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | `FR-17` — Quản lý Mã Giảm Giá (Coupon CRUD); [`README.md` §5 FR-17](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/README.md) — `discount_value` dương; upper bound `100` cho `percent` do người kiểm thử xác nhận 2026-10-21 |
| Test case | `DT-32` — `type = "percent"`, `discount_value = 150` |
| Build / môi trường | commit `f389502cdb308b133fe9044e34505f19202dd887`; Node v26.9.0 + Express + SQLite; API `http://localhost:3000`; DB test cách ly seed 4 coupon |
| Severity / Priority | **High / High** — mức giảm không thể tồn tại; dữ liệu sai có thể làm FR-09 tính số tiền âm/không hợp lý, ảnh hưởng trực tiếp tới giá trị đơn hàng |
| Trạng thái / lặp lại | **Đã xác nhận qua API**; 1/1 run API; **2 ảnh Postman + 1 ảnh UI bổ sung**; Issue [#54](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54) đã publish |

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

**Đường tái hiện đã kiểm chứng:** API. UI có thể nhập cùng giá trị vì ô **Giá trị** không có `max`; ảnh UI bổ sung chỉ minh họa bước áp dụng coupon đã tạo, chưa chạy UI tạo coupon. Bằng chứng chính vẫn là API.

1. Đăng nhập admin và lấy `ADMIN_TOKEN` bằng lệnh ở trên.
2. Gửi `POST /api/admin/coupons` với `code = "FR17-DT-32"`, `type = "percent"`, `discount_value = 150`; các trường còn lại giữ baseline `min_order_amount=100000`, `expired_at=2099-12-31`, `max_uses_per_user=1`.
3. Đọc HTTP status/body; dự kiến phải bị từ chối.
4. Gọi `GET /api/coupons` để kiểm tra row vừa tạo.
5. Xóa row `FR17-DT-32`; giữ nguyên 4 seed.

```zsh
curl -s -w '\nHTTP %{http_code}\n' -X POST "$BASE/api/admin/coupons" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-32","type":"percent","discount_value":150,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

curl -s "$BASE/api/coupons" -H "Authorization: Bearer $ADMIN_TOKEN" \
  | jq '.[] | select(.code == "FR17-DT-32")'
```

| Mốc / bước | Expected theo rule | Actual quan sát được (run `run-20261020-fr17`) |
| --- | --- | --- |
| Tạo coupon `percent` với `150` | Non-2xx; không có row mới | `HTTP 200`; body `{"message":"Coupon created","id":34}` |
| Danh sách sau request | Không có `FR17-DT-32` | Row `id=34`, `type=percent`, `discount_value=150` |

**Kết luận:** Backend không kiểm tra upper bound `100` cho `percent`, nên lưu một mức giảm vô nghĩa. UI cũng không có `max` trên ô Giá trị, nên người dùng có thể nhập trực tiếp `150`; đây là lỗi validation của cả API và đường UI tiềm năng, nhưng bằng chứng hiện tại là API.

### Ảnh xác nhận (Postman/API + UI bổ sung)

> Hai ảnh Postman dưới đây xác nhận request/response API; ảnh UI bổ sung minh họa hệ quả khi áp dụng coupon `150%`. Ảnh Postman được chụp ở lần chạy lại trên DB seed; id row trong ảnh là `6`, khác id `34` trong log run `run-20261020-fr17`, nhưng cùng request/response và cùng kết luận.

- `DT-32` — POST `discount_value=150` trả HTTP 200, tạo coupon:
  ![Ảnh POST discount 150](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-08-Discount150.png)
- `DT-32` — GET trả row `FR17-DT-32` với `discount_value=150`:
  ![Ảnh GET discount 150](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-08-GetDiscount150.png)
- **Ảnh UI bổ sung** — áp dụng coupon `FR17-DT-32` thành công với mức giảm `150%`; UI hiển thị tiết kiệm `-4,470,000,000 đ` và thành tiền `4,500,000,000 đ`, xác nhận hệ quả bất thường ở FR-09:
  ![Ảnh UI áp dụng coupon 150%](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/refs/heads/ncuong/homework/hw02/ncuong/features/FR17/screenshots/BUG-FR17-08-AppliedDiscount150.png)

## Cách kiểm tra thủ công trên UI

**Trạng thái:** Đã có ảnh UI áp dụng coupon `FR17-DT-32` với `150%` (bổ sung hệ quả); **chưa chạy UI tạo coupon**. Ảnh UI không thay thế bằng chứng API.

1. Mở `http://localhost:5174`, đăng nhập `admin@eshop.com` / `Admin123!`.
2. Chọn tab **Mã Giảm Giá**; nhập Mã=`FR17-UI-32`, Loại=`Phần trăm (%)`, Giá trị=`150`, Đơn tối thiểu=`100000`, Ngày hết hạn=`2099-12-31`, Số lần=`1`.
3. Bấm **Tạo mã**; Expected: không có row mới và có thông báo lỗi validation. Ghi lại Actual nếu chạy; không dùng ảnh UI làm bằng chứng chính.

## Bằng chứng

- Log/run: [`DT-32.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/DT-32.log); tổng hợp [`FR17-evidence.md`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR17/evidence/FR17-evidence.md) — EV-FR17-032, run `run-20261020-fr17`.
- Screenshot: **Đã có 2 ảnh Postman + 1 ảnh UI bổ sung** do người kiểm thử cung cấp (xem mục “Ảnh xác nhận” ở trên); bằng chứng chính là Postman/API, ảnh UI chỉ minh họa hệ quả FR-09.
- Lặp lại: **1/1** run API; ảnh chụp lần chạy lại xác nhận cùng hành vi.
- GitHub Issue: [#54](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54) — đã publish.

## Điều tra nguyên nhân (theo source, đã đối chiếu)

**Vị trí:** [`backend/server.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/backend/server.js#L457-L481) dòng 457–481; [`frontend-admin/src/App.jsx`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f389502cdb308b133fe9044e34505f19202dd887/frontend-admin/src/App.jsx#L659-L675) dòng 659–675.

```js
app.post("/api/admin/coupons", authenticateToken, (req, res) => {
  const { code, type, discount_value, min_order_amount, expired_at, max_uses_per_user } = req.body;
  db.run(
    "INSERT INTO coupons (code, type, discount_value, min_order_amount, expired_at, max_uses_per_user) VALUES (?, ?, ?, ?, ?, ?)",
    [code, type, discount_value, min_order_amount, expired_at, max_uses_per_user || 1],
```

```jsx
<input
  type="number"
  className="border p-2 rounded"
  value={couponForm.discount_value}
  onChange={(e) => setCouponForm({ ...couponForm, discount_value: e.target.value })}
  required
/>
```

**Cơ chế:** Route `POST` chỉ chuyển các giá trị vào `INSERT`, không kiểm tra `type === "percent"` và `discount_value <= 100`. Ô Giá trị trên UI là `type="number"` nhưng không có `max`, nên trình duyệt không chặn `150`. Với `type=percent`, đây là dữ liệu không hợp lệ; FR-09 có thể tính ra số tiền âm hoặc sai. Đây là nhận định từ mã nguồn; Expected/Actual ở trên dựa trên quy tắc người kiểm thử xác nhận và lần chạy thực tế.
