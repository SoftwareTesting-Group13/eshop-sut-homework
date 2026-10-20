# BUG-FR10-01 — Admin chuyển được đơn "Đã hủy" sang "Đã giao" (xuyên trạng thái kết thúc)

> **Trạng thái:** Đã xác nhận bởi người kiểm thử qua UI; screenshot đã có. GitHub Issue: [#33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33).

## Tóm tắt

Trong Web Admin, một đơn đã ở trạng thái **Đã hủy** (`canceled` — trạng thái kết thúc) vẫn hiển thị nút **"Đánh dấu Đã giao"**; bấm vào thì đơn chuyển sang **Đã giao** (`delivered`). Đặc tả FR-10 quy định `canceled` là trạng thái kết thúc — không được chuyển sang bất kỳ trạng thái nào khác, và mọi chuyển đổi không hợp lệ phải trả về lỗi.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | `FR-10` — Trạng thái Đơn hàng; `README.md` §5 FR-10 (Final States: `delivered` và `canceled` là trạng thái kết thúc; mọi chuyển đổi không hợp lệ phải lỗi) |
| Test case | `DT-14` (đồng thời điểm biên BVA B3 "rời terminal canceled") |
| Build / môi trường | commit `09a950cf451428bd8f54542b3f11a0e4b6fdaa91`; Node v26.9.0 + Express 5 + SQLite; Web Admin `http://localhost:5174`, API `http://localhost:3000` |
| Severity / Priority | **Medium / Medium** — admin phải chủ động bấm nút trên một đơn đã hủy; hệ quả là sai trạng thái và có thể khiến đơn đã hủy bị tính vào doanh thu (FR-13 chỉ tính đơn `delivered`), nhưng phạm vi ảnh hưởng giới hạn và cần thao tác admin |
| Trạng thái / lặp lại | **Đã xác nhận qua UI**; tái hiện 2/2 qua API (DT-14 + rerun) và 1/1 qua UI |

## Chuẩn bị để tái hiện

- Tài khoản admin seed: `admin@eshop.com` / `Admin123!` (role `admin`); tài khoản user: `test@eshop.com` / `Test1234!`.
- Một đơn hàng ở trạng thái **Đã hủy**: tạo đơn bằng user rồi admin hủy từ `pending`.
- Backend `http://localhost:3000` và Web Admin `http://localhost:5174` đang chạy.

## Các bước tái hiện và kết quả

**Đường tái hiện đã kiểm chứng:** UI (Web Admin) + đối chiếu API/trạng thái. 

1. Đăng nhập Web Admin bằng `admin@eshop.com`, mở tab **"Đơn hàng"**.
2. Tìm một đơn đang ở trạng thái **"Đã hủy"**. Quan sát: đơn vẫn có nút **"Đánh dấu Đã giao"**.
   ![Đơn hàng số 1 ở trạng thái Đã hủy vẫn có nút Đánh dấu Đã giao](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR10/screenshots/BUG-FR10-01-Cancelled-Admin.png)
3. Bấm **"Đánh dấu Đã giao"**.
4. Quan sát trạng thái đơn: chuyển thành **"Đã giao"**.
   ![Sau khi bấm, đơn hàng số 1 chuyển sang Đã giao](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR10/screenshots/BUG-FR10-01-Delivered-Admin.png)
5. Đăng nhập Web bằng `test@eshop.com`, mở trang Hồ sơ → **"Lịch sử đơn hàng"**: đơn hàng số 1 cũng hiển thị **"Đã giao"**.
   ![Lịch sử đơn hàng phía user cũng hiển thị Đã giao](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR10/screenshots/BUG-FR10-01-Delivered-User.png)

| Mốc / bước | Expected theo rule | Actual quan sát được |
| --- | --- | --- |
| Đơn ở `canceled` | Không có thao tác chuyển sang trạng thái khác (trạng thái kết thúc) | Vẫn có nút "Đánh dấu Đã giao" |
| Bấm "Đánh dấu Đã giao" | Bị từ chối / không có thao tác | Đơn chuyển sang "Đã giao" |
| Trạng thái sau | Vẫn "Đã hủy" | "Đã giao" (cả Admin và User đều thấy) |

**Kết luận:** SUT cho phép chuyển khỏi trạng thái kết thúc `canceled`, vi phạm rule Final States của FR-10. Hệ quả: một đơn **đã hủy** có thể bị đánh dấu **đã giao**, sai trạng thái nghiệp vụ và có thể làm sai tổng doanh thu của Dashboard (FR-13 tính doanh thu theo đơn `delivered`).

## Đối chiếu kỹ thuật (chỉ khi cần)

Trạng thái đọc trực tiếp bằng API `GET /api/orders/:id`; request tương ứng với nút UI là `PUT /api/admin/orders/:id/status` body `{"status":"delivered"}`.

```bash
curl -s -X PUT http://localhost:3000/api/admin/orders/1/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"delivered"}'
curl -s http://localhost:3000/api/orders/1
```

## Bằng chứng

- Log/run: [`evidence/DT-14.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR10/evidence/DT-14.log), [`DT-14-rerun.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR10/evidence/DT-14-rerun.log); tổng hợp [`FR10-evidence.md`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR10/evidence/FR10-evidence.md) (EV-FR10-014, EV-FR10-021; run `run-20261020-fr10`).
- Screenshot: 3 ảnh ở trên (`BUG-FR10-01-Cancelled-Admin.png`, `BUG-FR10-01-Delivered-Admin.png`, `BUG-FR10-01-Delivered-User.png`) thể hiện chuỗi Đã hủy → Đánh dấu Đã giao → Đã giao.
- Lặp lại: **2/2** qua API (DT-14 + rerun) và **1/1** qua UI.

## Điều tra nguyên nhân (theo source, đã đối chiếu)

**Vị trí:** [`backend/server.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/09a950cf451428bd8f54542b3f11a0e4b6fdaa91/backend/server.js#L550-L551) dòng 550-551.

```js
      if (currentStatus === "canceled" && status === "delivered")
        isValidTransition = true;
```

**Cơ chế:** hàm kiểm tra chuyển đổi hợp lệ trong `PUT /api/admin/orders/:id/status` có thêm một nhánh cho phép `canceled → delivered`, trong khi sơ đồ FR-10 không có cung này và `canceled` là trạng thái kết thúc. Vì `isValidTransition = true`, request vượt qua kiểm tra và chạy `UPDATE orders SET status = ?`, dẫn tới Actual. Phía Admin UI, nút "Đánh dấu Đã giao" được render cho đơn `canceled` tại `frontend-admin/src/App.jsx:862-869`, tạo đường thao tác cho người dùng.

Đây là nhận định từ mã nguồn; Expected và Actual ở trên dựa trên đặc tả và lần chạy thực tế (API + UI).
