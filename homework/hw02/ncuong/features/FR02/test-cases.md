# FR02 — Test cases (EP + BVA)

Catalog dùng chung cho Domain/EP và BVA. Mỗi `T-ID` một dòng; ca phục vụ cả hai kỹ thuật vẫn chỉ có một dòng. `DT-*` bắt nguồn từ EP/Domain, `BVA-*` từ BVA; tiền tố không giới hạn nghĩa vụ mà ca phủ. Trạng thái/`EV-ID` ở `test-results.md`.

**Setup chung:** Backend test cách ly (bản sao `server.js`/`database.js` trong thư mục tạm, DB riêng); tài khoản fixture tạo bằng `POST /api/register`, mật khẩu đúng `Passw0rd!`, mật khẩu sai `WrongPass1!`. Trạng thái bộ đếm/khóa chuẩn bị bằng câu lệnh SQL trên **DB test** (không phải DB làm việc) khi cần.

| T-ID | Phương pháp & obligation IDs | Setup + input + thao tác | Expected / oracle |
| --- | --- | --- | --- |
| DT-01 | EP P1; baseline R1 | DB sạch, `fr02.base@eshop.com` / `Passw0rd!`; `POST /api/login`; dùng token gọi `GET /api/users/me` | Thành công (có thân phản hồi success), trả `token`; token hợp lệ cho request xác thực; `login_attempts = 0` |
| DT-02 | EP P2; BVA B3 (đồng thời BVA-01, B1 ngay dưới) | DB sạch `login_attempts=0`, `fr02.wrong@eshop.com` / `WrongPass1!`; `POST /api/login` | Thất bại, không có `token`; `login_attempts` = **1** (tăng đúng 1); chưa khóa |
| DT-03 | EP P3; R7 | `nobody.fr02@eshop.com` / `Passw0rd!`; `POST /api/login`; đếm user cùng email | Thất bại, không có `token`; không tạo/tăng bộ đếm cho email chưa đăng ký |
| DT-04 | EP P4 | `fr02.base@eshop.com` / `""`; `POST /api/login` | Thất bại, không có `token` |
| DT-05 | EP P5 | `email=""` (mật khẩu đúng) và body `{}`; `POST /api/login` | Thất bại, không có `token` cho cả hai biến thể |
| DT-06 | EP P6 (chưa rõ) | `not-an-email` / `Passw0rd!`; `POST /api/login` | **Chưa xác định theo đặc tả** (đặc tả chỉ ràng buộc `type="email"` ở UI) → Quan sát, không chấm PASS/FAIL |
| DT-07 | EP P7; R6; trạng thái B1 | `fr02.lock@eshop.com` với `locked_until` tương lai (ISO), mật khẩu **đúng**; `POST /api/login` | Bị từ chối với trạng thái khóa; không có `token`; `login_attempts`/`locked_until` giữ nguyên |
| DT-08 | EP P8; R6 | Tài khoản khóa như DT-07, mật khẩu **sai**; `POST /api/login` | Bị từ chối với trạng thái khóa; không có `token`; bộ đếm **không** tăng thêm |
| BVA-02 | BVA B1 ngay dưới (2 lần sai); EP P2 | DB sạch `fr02.wrong@eshop.com`; sai liên tiếp 2 lần (`POST /api/login`) | Sau 2 lần: `login_attempts = 2`, **chưa khóa** (`locked_until = NULL`) |
| BVA-03 | BVA B1 tại biên (3 lần sai) | Chuẩn bị `login_attempts = 2`, `locked_until = NULL`, `fr02.thr@eshop.com`; sai 1 lần (lần thứ 3) | Tài khoản **bị khóa** (`locked_until` được đặt); giá trị bộ đếm/độ dài khóa thuộc B3/B2 |
| BVA-04 | BVA B1 ngay trên; R6 | Tài khoản đang khóa (`fr02.wrong` sau BVA-02); gửi thêm một lần đăng nhập | Bị từ chối với trạng thái khóa; `login_attempts`/`locked_until` không đổi |
| BVA-05 | BVA B2 ngay dưới 30 s | Tài khoản khóa, chờ `t0 + 29 s`, mật khẩu **đúng**; `POST /api/login` | Vẫn bị khóa (chưa hết 30 s) |
| BVA-06 | BVA B2 tại/ngay trên 30 s | Cùng tài khoản, chờ `t0 + 31 s`, mật khẩu **đúng**; `POST /api/login` | Hết khóa: đăng nhập thành công, trả `token` |
| BVA-07 | BVA B4 (đặt lại về 0); EP P9 | `fr02.reset@eshop.com`: 1 lần sai rồi đăng nhập đúng | Thành công, trả `token`; `login_attempts = 0`, `locked_until = NULL` |
| BVA-08 | BVA B2 (trạng thái hết hạn); R6 | `fr02.expired@eshop.com` với `locked_until` = quá khứ (ISO), mật khẩu đúng | Hết khóa: đăng nhập thành công, trả `token` |
| DT-09 | EP P10; R4; AI-GAP-FR02-01 | Dùng API FR-01 tạo `not-an-email` / `Passw0rd!`; mở form web `/login`, điền đúng hai giá trị và submit; đối chiếu API login riêng | Input email là `type="email"`; HTML5 chặn `not-an-email`, không gửi yêu cầu đăng nhập/không tạo session. Việc API FR-01 nhận fixture sai định dạng là vấn đề liên quan FR-01, không phải oracle của ca UI này |
| DT-10 | EP P11; R8, R2; AI-GAP-FR02-03 | Tài khoản `fr02.gap.valid@eshop.com` / `Passw0rd!` có `login_attempts=0`; `POST /api/login` body chỉ có `{"email":"fr02.gap.valid@eshop.com"}` | Không cấp JWT; nếu xử lý như đăng nhập sai thì `login_attempts` tăng đúng 1 theo R2; không khóa |
| DT-11 | EP P12; R8; mở rộng AI-GAP-FR02-03 | API FR-01 tạo `fr02.gap.null@eshop.com` với `password:null` (DB `NULL`); `POST /api/login` cùng email và `password:null` | Không cấp JWT cho tài khoản không có mật khẩu hợp lệ; không coi `null === null` là xác thực thành công |

**Ca gộp:** DT-02 = BVA-01 (một lần chạy quan sát cả kết quả đăng nhập lẫn giá trị bộ đếm). BVA-07 gộp `P9` + `B4`. DT-09–DT-11 không tạo nghĩa vụ BVA mới. Tổng **18 T-ID duy nhất**.

## Đường chạy và tính khả thi của các ca bổ sung

### DT-09 — email sai định dạng trên form

- **Fixture qua API FR-01:** `POST http://localhost:3000/api/register` với `{"name":"FR02 Gap Malformed","email":"not-an-email","password":"Passw0rd!"}` trên DB test; kiểm tra tài khoản được tạo. Đây là setup liên quan FR-01, không tính thành T-ID FR-02.
- **UI đã chạy:** mở `http://127.0.0.1:5173/login` trong Firefox, chưa đăng nhập; điền `not-an-email` và `Passw0rd!`, bấm **Sign In**. Expected: email input `type="email"`, browser báo sai định dạng và không chuyển trang/không lưu token. Chụp form với giá trị sai trước bấm và trang sau bấm. Actual ở `EV-FR02-018`.
- **Đối chiếu API:** `POST /api/login` cùng email/password để chứng minh fixture có thể xác thực; kết quả API không thay cho verdict UI.

### DT-10 — chỉ thiếu key password

- **API đã chạy:** `POST http://localhost:3000/api/login`, `Content-Type: application/json`, body `{"email":"fr02.gap.valid@eshop.com"}`; đọc response và `login_attempts` trước/sau ở DB test. Actual ở `EV-FR02-020`.
- **UI thông thường:** không cùng input. Form `/login` có ô mật khẩu `required`; để trống sẽ bị chặn hoặc gửi chuỗi rỗng, không tạo body JSON **thiếu hẳn key**. Giữ ca này API-only.

### DT-11 — password null tường minh

- **Fixture qua API FR-01:** `POST /api/register` với email `fr02.gap.null@eshop.com`, `password:null`; kiểm tra DB test lưu `NULL`.
- **API đã chạy:** `POST /api/login` với `{"email":"fr02.gap.null@eshop.com","password":null}`; kiểm tra HTTP response và token. Lặp lại trên `fr02.gap.null2@eshop.com`. Actual ở `EV-FR02-021`.
- **UI thông thường:** không cùng input. Form nhập mật khẩu `required` và gửi chuỗi, không gửi JSON `null`; ảnh bằng chứng cho ca này là ảnh chụp trang trình bày log API thực tế, không phải ảnh UI app.
