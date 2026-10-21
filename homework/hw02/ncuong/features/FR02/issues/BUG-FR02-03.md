# BUG-FR02-03 — Form đăng nhập cho email sai định dạng đi qua và cấp phiên đăng nhập

**GitHub Issue:** [#58](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/58)

## Tóm tắt

FR-02 yêu cầu ô Email của form đăng nhập dùng `type="email"` để kiểm tra định dạng HTML5. Sau khi tạo fixture `not-an-email` qua API đăng ký, form web vẫn chấp nhận chuỗi này và đăng nhập thành công.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-02 R4 — [README §FR-02](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/2010a50344e8b94fa19fba48335963de2cb55c7a/README.md#fr-02-đăng-nhập--khóa-tài-khoản); FR-01 chỉ là dependency tạo fixture |
| Test case | DT-09 / P10 / AI-GAP-FR02-01 |
| Build / môi trường | `2010a50344e8b94fa19fba48335963de2cb55c7a`; Firefox 158 headless, `http://127.0.0.1:5173/login`; backend Node/SQLite cô lập cổng 3000 |
| Severity / Priority | Medium / Medium — ràng buộc định dạng trên form bị bỏ qua |
| Lặp lại | UI 1/1, API login 2/2 trên hai email sai định dạng |

## Chuẩn bị để tái hiện

Trên **DB test riêng**, tạo tài khoản fixture bằng request API sau. `POST /api/register` hiện nhận email sai định dạng; đó là vấn đề liên quan FR-01. Dùng API để setup vì form đăng ký còn có logic mật khẩu riêng và bài test này cô lập form đăng nhập FR-02.

```bash
curl -sS -X POST http://localhost:3000/api/register \
  -H 'Content-Type: application/json' \
  --data-raw '{"name":"FR02 Gap Malformed","email":"not-an-email","password":"Passw0rd!"}'
```

Actual setup trong run: HTTP 200, tài khoản `not-an-email` được lưu.

## Các bước tái hiện và kết quả

**Đường đã kiểm chứng: UI web.**

1. Mở `http://localhost:5173/login` trong browser chưa đăng nhập.
2. Ở ô email/Username nhập `not-an-email`; ở ô Mật khẩu nhập `Passw0rd!`.
3. Bấm **Sign In**.
4. Quan sát trang sau submit và header; có thể kiểm tra token trong localStorage của profile test.

| Mốc | Expected | Actual |
| --- | --- | --- |
| Trước submit | Email input là `type="email"`; giá trị thiếu `@` bị HTML5 báo `typeMismatch` và form không hợp lệ | DOM là `type="text"`; `typeMismatch=false`, `form.checkValidity()=true` |
| Sau submit | Không gửi login/không tạo session với email sai định dạng | Điều hướng về trang chủ, header hiện “Chào, FR02 Gap Malformed”; localStorage có JWT |

**Đối chiếu API:** `POST /api/login` với cùng email/password trả HTTP 200 và JWT. Tài khoản fixture thứ hai `plainsecond` cũng login API thành công; kết quả API không thay cho bằng chứng UI về `type=email`.

## Bằng chứng

- [Raw API log](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR02/evidence/ev-gap-api.json) và [raw UI/BiDi log](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR02/evidence/ev-gap-ui.json), tổng hợp tại [FR02 evidence](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR02/evidence/FR02-evidence.md).
- Form trước submit (email sai định dạng hiển thị): ![BUG-FR02-03 trước submit](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR02/screenshots/BUG-FR02-03-before.png)
- Trang sau submit (header đã đăng nhập): ![BUG-FR02-03 sau submit](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR02/screenshots/BUG-FR02-03-after.png)

## Nguyên nhân đối chiếu mã nguồn

[`frontend-web/src/pages/Login.jsx:30`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/2010a50344e8b94fa19fba48335963de2cb55c7a/frontend-web/src/pages/Login.jsx#L30) dùng `type="text"` cho email thay vì `type="email"`. Backend [`/api/login`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/2010a50344e8b94fa19fba48335963de2cb55c7a/backend/server.js#L32) chỉ tra cứu email theo chuỗi; [`/api/register`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/2010a50344e8b94fa19fba48335963de2cb55c7a/backend/server.js#L18) cũng không validate format. Expected và verdict FR-02 ở trên dựa trên requirement của form và run UI thực tế.
