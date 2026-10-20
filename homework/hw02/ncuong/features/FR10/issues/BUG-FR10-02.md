# BUG-FR10-02 — User tự hủy được đơn đang `shipping` (hủy sai trạng thái)

> **Trạng thái:** Đã xác nhận bởi người kiểm thử qua UI; screenshot đã có. GitHub Issue: [#34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34).
>
> **Liên quan:** cùng defect được ghi nhận từ góc nhìn FR-11 tại Issue #13 (người kiểm thử khác); bản này giữ oracle theo FR-10 (`shipping` → User không được tự hủy).

## Tóm tắt

Đơn hàng đang ở trạng thái **Đang giao** (`shipping`) vẫn hiển thị nút **"Hủy đơn"** cho chính user và hủy thành công. FR-10 quy định khi đơn đã `shipping` thì User không được phép tự hủy; đặc tả cũng yêu cầu chuyển đổi không hợp lệ phải trả về lỗi.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | `FR-10` — Trạng thái Đơn hàng; `README.md` §5 FR-10 ("Khi đơn hàng đã ở trạng thái `shipping`, User không được phép tự hủy"); liên quan FR-20 §7 |
| Test case | `DT-16` (đồng thời điểm biên BVA B1 "ngay trên biên") |
| Build / môi trường | commit `09a950cf451428bd8f54542b3f11a0e4b6fdaa91`; Node v26.9.0 + Express 5 + SQLite; Web `http://localhost:5173`, Web Admin `http://localhost:5174`, API `http://localhost:3000` |
| Severity / Priority | **High / High** — bất kỳ user nào cũng hủy được đơn đã bàn giao vận chuyển chỉ bằng một nút trên UI; phá vỡ rule tác nhân của state machine và gây hậu quả vận chuyển/kế toán thực tế |
| Trạng thái / lặp lại | **Đã xác nhận qua UI**; tái hiện 2/2 qua API (DT-16 + rerun) và 1/1 qua UI |

## Chuẩn bị để tái hiện

- Tài khoản user seed: `test@eshop.com` / `Test1234!`; tài khoản admin: `admin@eshop.com` / `Admin123!`.
- Một đơn của user ở trạng thái **Đang giao** (`shipping`): tạo đơn bằng user rồi admin chuyển `pending → confirmed → shipping`.
- Backend `http://localhost:3000`, Web `http://localhost:5173`, Web Admin `http://localhost:5174` đang chạy.

## Các bước tái hiện và kết quả

**Đường tái hiện đã kiểm chứng:** UI (Web) + đối chiếu API/trạng thái.

1. Đăng nhập Web Admin bằng `admin@eshop.com`, mở tab **"Đơn hàng"**, đưa đơn về trạng thái **"Đang giao"**. Quan sát: đơn có nút **"Hoàn thành"** (admin không có nút hủy).
   ![Đơn hàng số 2 ở trạng thái Đang giao trong Admin](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR10/screenshots/BUG-FR10-02-Delivering-Admin.png)
2. Đăng nhập Web bằng `test@eshop.com`, mở Hồ sơ → **"Lịch sử đơn hàng"**. Quan sát: đơn hàng số 2 **"Đang giao"** vẫn hiển thị nút **"Hủy đơn"** — trái với rule "ở `shipping`, User không được tự hủy".
   ![Đơn Đang giao vẫn có nút Hủy đơn phía user](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR10/screenshots/BUG-FR10-02-Delivering-User.png)
3. Bấm **"Hủy đơn"**. Quan sát: hiện thông báo **"Hủy đơn thành công!"**.
   ![Thông báo Hủy đơn thành công](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR10/screenshots/BUG-FR10-02-Noti-Cancelled-User.png)
4. Đóng thông báo, quan sát trạng thái đơn: chuyển thành **"Đã hủy"**.
   ![Đơn hàng số 2 chuyển sang Đã hủy](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR10/screenshots/BUG-FR10-02-Status-Cancelled-User.png)

| Mốc / bước | Expected theo rule | Actual quan sát được |
| --- | --- | --- |
| Đơn ở `shipping` | User không có thao tác hủy | Vẫn có nút "Hủy đơn" |
| Bấm "Hủy đơn" | Bị từ chối / không có thao tác | Thông báo "Hủy đơn thành công!", HTTP 200 |
| Trạng thái sau | Vẫn "Đang giao" | "Đã hủy" |

**Kết luận:** SUT cho phép user hủy đơn đang giao, vi phạm rule tác nhân của FR-10 (chỉ Admin thao tác khi `shipping`) và FR-20. Hệ quả: đơn đã xuất kho/đang giao vẫn có thể bị hủy bởi người dùng, gây sai lệch trạng thái vận chuyển và xử lý đơn.

## Đối chiếu kỹ thuật (chỉ khi cần)

Trạng thái đọc trực tiếp qua `GET /api/orders/:id` (endpoint công khai theo `api_specification.md` §4.5); request tương ứng với nút UI là `PUT /api/orders/:id/cancel` bằng token của user.

```bash
curl -s -X PUT http://localhost:3000/api/orders/2/cancel \
  -H "Authorization: Bearer $USER_TOKEN"
curl -s http://localhost:3000/api/orders/2
```

## Bằng chứng

- Log/run: [`evidence/DT-16.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR10/evidence/DT-16.log), [`DT-16-rerun.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR10/evidence/DT-16-rerun.log); tổng hợp [`FR10-evidence.md`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR10/evidence/FR10-evidence.md) (EV-FR10-016, EV-FR10-022; run `run-20261020-fr10`).
- Screenshot: 4 ảnh ở trên (`BUG-FR10-02-Delivering-Admin.png`, `BUG-FR10-02-Delivering-User.png`, `BUG-FR10-02-Noti-Cancelled-User.png`, `BUG-FR10-02-Status-Cancelled-User.png`) thể hiện chuỗi Đang giao → Hủy đơn → Đã hủy.
- Lặp lại: **2/2** qua API (DT-16 + rerun trên đơn mới) và **1/1** qua UI.

## Điều tra nguyên nhân (theo source, đã đối chiếu)

**Vị trí:** [`backend/server.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/09a950cf451428bd8f54542b3f11a0e4b6fdaa91/backend/server.js#L328-L331) dòng 328-331.

```js
      // Lẽ ra phải là: if (order.status !== 'pending' && order.status !== 'confirmed')
      if (order.status === "delivered" || order.status === "canceled") {
        return res.status(400).json({ error: "Cannot cancel this order." });
      }
```

**Cơ chế:** `PUT /api/orders/:id/cancel` chỉ chặn khi đơn ở `delivered` hoặc `canceled`. Với `shipping`, điều kiện không đúng nên code đi tiếp và chạy `UPDATE orders SET status = 'canceled'`. Chính comment trong mã nguồn cũng ghi điều kiện đúng phải là chỉ cho hủy khi `pending`/`confirmed`. Phía Web, nút "Hủy đơn" hiển thị khi `status !== "delivered" && status !== "canceled"` (`frontend-web/src/pages/Profile.jsx:200`) nên vẫn hiện cho đơn `shipping`, tạo đường thao tác cho người dùng.

Đây là nhận định từ mã nguồn; Expected và Actual ở trên dựa trên đặc tả và lần chạy thực tế (API + UI).
