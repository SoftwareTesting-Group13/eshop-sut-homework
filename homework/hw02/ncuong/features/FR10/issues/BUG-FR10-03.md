# BUG-FR10-03 — User thường đổi được trạng thái đơn qua API Admin

> **Trạng thái:** Đã tái hiện API; chờ sinh viên review, chụp screenshot và mở GitHub Issue. Đây là bản nháp, chưa có URL Issue.

## Tóm tắt

`PUT /api/admin/orders/:id/status` chỉ kiểm tra JWT hợp lệ, không kiểm tra `role='admin'`. Token user thường chuyển được đơn `pending → confirmed`, kể cả đơn thuộc tài khoản khác.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-12: mọi `/api/admin/*` cần token hợp lệ và role admin; FR-18: Admin quản lý trạng thái; FR-10 R1: Admin xác nhận đơn |
| Test case | DT-21, DT-22; đối chứng DT-01 và DT-23 |
| Build / môi trường | `9955eba27e0e4bf45613649150bf3c2eb681a20f`; Node v26.9.0, backend/SQLite cách ly trên cổng 3000 |
| Severity / Priority | High / High — đã tái hiện khả năng khách hàng tự xác nhận đơn của mình và đơn người khác khi biết ID |
| Lặp lại | Đơn của mình 2/2 trên hai DB test mới; đơn người khác 1/1 |

## Chuẩn bị để tái hiện

Chạy backend với **DB test riêng** chứa hai tài khoản seed: user `test@eshop.com` / `Test1234!` và admin `admin@eshop.com` / `Admin123!`. Tạo đơn qua checkout với token user; đơn mới ở `pending`. Lấy JWT user từ `/api/login`. Dùng chính ID đơn vừa tạo, không giả định ID cố định trên DB khác. Có thể dùng tài khoản admin để tạo thêm đơn thứ hai và kiểm tra biến thể khác chủ sở hữu.

## Các bước tái hiện đã kiểm chứng — API

1. Đăng nhập user thường, giữ JWT trong biến `USER_TOKEN`.
2. Tạo một đơn `pending` của user đó, giữ `orderId` trong biến `ORDER_ID`. Gọi `GET /api/orders/$ORDER_ID` xác nhận `status=pending`.
3. Gửi `PUT /api/admin/orders/$ORDER_ID/status` với **JWT user**, body `{"status":"confirmed"}`.
4. Đọc HTTP response và gọi lại `GET /api/orders/$ORDER_ID`.

```bash
API_BASE=http://127.0.0.1:3000
USER_TOKEN=$(curl -sS -X POST "$API_BASE/api/login" -H 'Content-Type: application/json' --data-raw '{"email":"test@eshop.com","password":"Test1234!"}' | node -pe 'JSON.parse(require("fs").readFileSync(0,"utf8")).token')
ORDER_ID=$(curl -sS -X POST "$API_BASE/api/checkout" -H "Authorization: Bearer $USER_TOKEN" -H 'Content-Type: application/json' --data-raw '{"total_amount":200000,"shipping_address":"FR10 gap 123 Le Loi"}' | node -pe 'JSON.parse(require("fs").readFileSync(0,"utf8")).orderId')
curl -sS "$API_BASE/api/orders/$ORDER_ID"
curl -i -sS -X PUT "$API_BASE/api/admin/orders/$ORDER_ID/status" -H "Authorization: Bearer $USER_TOKEN" -H 'Content-Type: application/json' --data-raw '{"status":"confirmed"}'
curl -sS "$API_BASE/api/orders/$ORDER_ID"
```

| Mốc | Expected theo rule | Actual quan sát |
| --- | --- | --- |
| Trước request | Đơn `pending` | Đơn `pending` |
| User token gọi API Admin | Bị từ chối vì thiếu role admin; đơn giữ `pending` | HTTP **200** `{"message":"Order status updated"}`; đơn thành `confirmed` |
| Đối chứng không token | Bị từ chối; đơn giữ `pending` | HTTP 401 `Unauthorized`; đơn giữ `pending` (2/2) |
| Đối chứng admin token | Được xác nhận đơn | HTTP 200; đơn thành `confirmed` (2/2) |

**Biến thể khác chủ sở hữu đã chạy:** tạo đơn `pending` bằng tài khoản `admin@eshop.com`, sau đó dùng JWT `test@eshop.com` để gửi cùng PUT tới ID đơn này. Actual vẫn HTTP 200 và đơn thành `confirmed` (1/1). Đây là cùng lỗi thiếu kiểm tra role, không tách bug thứ tư.

## UI và bằng chứng

**API-only cho đúng stimulus:** Admin UI từ chối đăng nhập tài khoản role user (`frontend-admin/src/App.jsx:65`); web user không có nút xác nhận đơn. Thao tác request trực tiếp là đường tái hiện đã kiểm chứng. Không ghi nhận Actual UI cho lỗi này.

- [Raw run 1](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR10/evidence/ev-gap-access-run1.json), [raw run 2](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR10/evidence/ev-gap-access-run2.json), [raw biến thể khác chủ sở hữu](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR10/evidence/ev-gap-access-cross.json), [evidence log](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR10/evidence/FR10-evidence.md).
- Screenshot và GitHub Issue: **chờ sinh viên review/chụp/đăng** theo quy trình HW02.

## Điều tra nguyên nhân từ source

Tại [`backend/server.js:525`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/9955eba27e0e4bf45613649150bf3c2eb681a20f/backend/server.js#L525), route chỉ gắn `authenticateToken`:

```js
app.put("/api/admin/orders/:id/status", authenticateToken, (req, res) => {
  const { status } = req.body; // pending, confirmed, shipping, delivered, canceled
```

Middleware xác minh JWT rồi gán `req.user`; route không kiểm tra `req.user.role`. Source giải thích cơ chế, còn kết luận bug dựa trên kết quả API và trạng thái đơn trước/sau trong log.
