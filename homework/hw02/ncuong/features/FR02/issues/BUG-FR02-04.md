# BUG-FR02-04 — API đăng nhập cấp JWT với `password: null`

**GitHub Issue:** [#59](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/59)

## Tóm tắt

Nếu API đăng ký tạo một tài khoản có password DB `NULL`, API đăng nhập cho phép gửi `password: null` và trả JWT. Đây là credential không có mật khẩu sử dụng được. **Body thiếu hẳn key `password` là ca khác:** nó bị từ chối 401, không thuộc lỗi cấp JWT này.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-02 R8 (người dùng phải nhập Email và Mật khẩu) và FR-01 (mật khẩu mạnh); [README §2](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/2010a50344e8b94fa19fba48335963de2cb55c7a/README.md#2-quản-lý-tài-khoản-authentication--authorization) |
| Test case | DT-11 / P12 / mở rộng AI-GAP-FR02-03 |
| Build / môi trường | `2010a50344e8b94fa19fba48335963de2cb55c7a`; Node/Express + SQLite; API/DB test cô lập cổng 3000 |
| Severity / Priority | High / High — cấp JWT cho account không có mật khẩu hợp lệ |
| Lặp lại | API 2/2 với hai tài khoản độc lập |

## Chuẩn bị để tái hiện

Khởi động backend với DB test riêng. Đăng ký tài khoản qua **API** vì form web có `required` và không thể gửi JSON `null` bằng thao tác người dùng bình thường. API đăng ký chấp nhận `password:null` và DB lưu `NULL`; đây cũng là vấn đề đầu vào liên quan FR-01.

```bash
curl -sS -X POST http://localhost:3000/api/register \
  -H 'Content-Type: application/json' \
  --data-raw '{"name":"FR02 Gap Null","email":"fr02.gap.null@eshop.com","password":null}'
```

Actual setup: HTTP 200; DB test có `users.password = NULL`, `login_attempts=0`, `locked_until=NULL`.

## Các bước tái hiện và kết quả

**Đường đã kiểm chứng: API-only.**

1. Gửi request đăng nhập dưới đây tới chính backend/DB test vừa tạo fixture.
2. Đọc HTTP status và response; kiểm tra có trường `token` hay không.
3. Lặp lại trên email `fr02.gap.null2@eshop.com` đã đăng ký cùng cách để loại trừ fixture đơn lẻ.

```bash
curl -sS -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.gap.null@eshop.com","password":null}'
```

| Mốc | Expected | Actual |
| --- | --- | --- |
| Tài khoản có `password=NULL`; login gửi `password:null` | Từ chối xác thực, không cấp JWT | HTTP 200 `Login successful` và có JWT |
| Fixture độc lập thứ hai | Tương tự, không cấp JWT | HTTP 200 và có JWT |

**Phân biệt DT-10:** request `{"email":"fr02.gap.valid@eshop.com"}` **thiếu key password** trả 401/no-token. Bộ đếm tăng 2 ở ca đó là BUG-FR02-01 đã có Issue #25; không báo trùng ở issue này.

## Bằng chứng

- [Raw API log hai fixture](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR02/evidence/ev-gap-api.json) và [evidence log có oracle/verdict](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR02/evidence/FR02-evidence.md).
- Ảnh sau là **screenshot bản trình bày các record API thật** từ `ev-gap-api.json`, không phải ảnh UI app: ![BUG-FR02-04 API evidence](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR02/screenshots/BUG-FR02-04-api-evidence.png)
- Token thật đã được redacted trong log/ảnh; chỉ giữ bằng chứng token hiện diện.

## Nguyên nhân đối chiếu mã nguồn

[`backend/server.js:18-27`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/2010a50344e8b94fa19fba48335963de2cb55c7a/backend/server.js#L18) INSERT mật khẩu đăng ký mà không validate. Sau đó [`backend/server.js:44`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/2010a50344e8b94fa19fba48335963de2cb55c7a/backend/server.js#L44) so sánh `user.password === password`; với hai giá trị `null`, nhánh thành công ký và trả JWT. Đây là nhận định từ source, còn Actual 200 + JWT dựa trên hai lần chạy API thực tế.
