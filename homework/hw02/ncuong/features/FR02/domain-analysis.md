# FR02 — Domain analysis (EP)

**Feature / interface:** FR-02 Đăng nhập & Khóa tài khoản — kiểm thử **Backend API** `POST /api/login` (đọc `users` trong DB test để quan sát `login_attempts`, `locked_until`) và form web `/login` cho lớp email sai định dạng.
**Phạm vi:** Rule đăng nhập, tăng bộ đếm đăng nhập sai, ngưỡng khóa 3 lần, thời lượng khóa 30 giây, hành vi tài khoản đang bị khóa và ràng buộc email của form đăng nhập. FR-01 chỉ dùng để tạo fixture: API đăng ký chấp nhận email sai định dạng và mật khẩu `null`, hai hành vi đó được ghi như tiền điều kiện liên quan FR-01, không tính thành ca FR-02 riêng. Không kiểm thử layout.
**Nguồn yêu cầu:** `README.md` §2 FR-02; hợp đồng API `api_specification.md` §1.2.

## Quy tắc dùng để chia miền

| Rule | Hệ thống phải làm gì? | Điều kiện ảnh hưởng | Nguồn | Tin cậy |
| --- | --- | --- | --- | --- |
| R1 | Đăng nhập đúng trả về JWT Token | email + mật khẩu đúng, tài khoản không khóa | README §FR-02 | CONFIRMED |
| R2 | Mỗi lần đăng nhập sai tăng bộ đếm lên **đúng 1 đơn vị** | một lần thất bại cho tài khoản tồn tại | README §FR-02 | CONFIRMED |
| R3 | Sai **từ 3 lần trở lên liên tiếp** thì khóa tạm **30 giây** | `login_attempts` sau lần sai | README §FR-02 | CONFIRMED |
| R4 | Trường email dùng `type="email"` (HTML5); email sai định dạng không được đi qua form đăng nhập | input email của UI đăng nhập | README §FR-02 (+FR-22) | CONFIRMED (UI; bổ sung lớp P10) |
| R5 | "liên tiếp" ⇒ đăng nhập thành công đặt lại bộ đếm | một lần đăng nhập đúng xen giữa các lần sai | suy ra từ R3 | ASSUMED |
| R6 | Tài khoản đang bị khóa thì đăng nhập bị từ chối, kể cả mật khẩu đúng | `locked_until` còn hiệu lực | suy ra từ R3 ("khóa tài khoản") | DERIVED |
| R7 | Thông báo lỗi không để lộ chi tiết nguyên nhân | mọi trường hợp thất bại | README §FR-02 | CONFIRMED, nhưng tiêu chí "chi tiết" chưa rõ → UNRESOLVED về cách chấm |
| R8 | Đăng nhập phải có mật khẩu thực sự; `password` vắng hoặc `null` không thể được xem là credential hợp lệ | request không có mật khẩu sử dụng được | README §FR-02 ("người dùng nhập Email và Mật khẩu"), FR-01 (mật khẩu mạnh) | DERIVED; không suy mã HTTP cụ thể |

**Giả định/điểm chưa rõ ảnh hưởng chia lớp:** (R5) đặc tả không nói rõ bộ đếm có reset sau khi hết khóa hay không → lớp "hết khóa" chỉ chấm hành vi đăng nhập được phép, không tự đặt kỳ vọng bộ đếm. (R7) thông báo khóa thực tế là "Tài khoản đã bị khóa…" nêu đúng trạng thái khóa; đặc tả yêu cầu "thông báo lỗi phù hợp" cho khóa nên coi đây là điểm chưa rõ, không phải bug.

## Các lớp tương đương và ca đại diện

Baseline dùng chung: tài khoản fixture tạo qua `POST /api/register` với mật khẩu mạnh `Passw0rd!`; trạng thái DB sạch (`login_attempts = 0`, `locked_until = NULL`) trừ khi hàng ghi khác. Mật khẩu sai dùng `WrongPass1!`.

**Đầu vào `email` (kiểu chuỗi), `password` (kiểu chuỗi), trạng thái tài khoản:**

| Lớp | Điều kiện của nhóm | Giá trị/trạng thái đem test | Expected theo đặc tả | Test case | Rule |
| --- | --- | --- | --- | --- | --- |
| P1 | Email đã đăng ký + mật khẩu đúng + chưa khóa | `fr02.base@eshop.com` / `Passw0rd!`, `login_attempts=0` | Đăng nhập thành công, trả JWT Token; token dùng được cho request xác thực | DT-01 | R1 |
| P2 | Email đã đăng ký + mật khẩu sai + chưa khóa + chưa tới ngưỡng | `fr02.wrong@eshop.com` / `WrongPass1!` (trước đó 0 lần sai) | Thất bại, không cấp token; `login_attempts` tăng **đúng 1** (0→1) | DT-02 | R2, R3 |
| P3 | Email hợp lệ nhưng **chưa đăng ký** | `nobody.fr02@eshop.com` / `Passw0rd!` | Thất bại, không cấp token; không tạo/tăng bộ đếm tài khoản nào | DT-03 | R1, R7 |
| P4 | Mật khẩu rỗng | `fr02.base@eshop.com` / `""` | Thất bại, không cấp token (rỗng ≠ mật khẩu hợp lệ) | DT-04 | R1 |
| P5 | Email rỗng/thiếu trường | `""` / `Passw0rd!` và body `{}` | Thất bại, không cấp token | DT-05 | R1 |
| P6 | Email sai định dạng (không có `@`) | `not-an-email` / `Passw0rd!` | **Chưa xác định theo đặc tả** (đặc tả chỉ ràng buộc định dạng ở UI) → quan sát | DT-06 | R4 (UI) |
| P7 | Tài khoản **đang bị khóa** + mật khẩu đúng | `fr02.lock@eshop.com`, `locked_until` ở tương lai ngắn | Bị từ chối với trạng thái khóa; không cấp token; bộ đếm giữ nguyên | DT-07 | R3, R6 |
| P8 | Tài khoản **đang bị khóa** + mật khẩu sai | `fr02.lock@eshop.com`, `locked_until` tương lai, mật khẩu sai | Bị từ chối với trạng thái khóa; **không** tăng bộ đếm thêm | DT-08 | R3, R6 |
| P9 | Vài lần sai rồi đăng nhập đúng (chưa khóa) | `fr02.reset@eshop.com`: 1 lần sai rồi đúng | Thành công; bộ đếm được đặt lại (đưa về 0) | BVA-07 | R5 |
| P10 | Email sai định dạng **nhưng đã được tạo qua API FR-01** | đăng ký `not-an-email` / `Passw0rd!`, rồi nhập hai giá trị ấy trên `/login` | Form email phải dùng `type="email"` và không gửi/đăng nhập với `not-an-email`; API login được ghi riêng để thấy hệ quả của fixture | DT-09 | R4; fixture FR-01 |
| P11 | Email đã đăng ký, JSON body **thiếu hẳn key** `password` | `{"email":"fr02.gap.valid@eshop.com"}` | Không cấp JWT; theo R2, nếu tính là lần đăng nhập sai thì bộ đếm chỉ tăng đúng 1 | DT-10 | R2, R8 |
| P12 | Email đã đăng ký từ API FR-01 với `password = NULL`; login gửi **`password: null`** | `fr02.gap.null@eshop.com` / `null` | Không cấp JWT cho credential không có mật khẩu dùng được | DT-11 | R8; fixture FR-01 |

**Tương tác cần kiểm tra:** (a) `login_attempts` × ngưỡng 3 × thời lượng khóa — xem `boundary-analysis.md` B1–B2; (b) mật khẩu đúng trong lúc tài khoản bị khóa (P7) chứng minh trạng thái khóa chặn trước khi kiểm tra mật khẩu; (c) tăng bộ đếm (P2) × đặt lại sau thành công (P9) là hai vế của quy tắc "liên tiếp".

**Lớp gộp, không khả thi hoặc chưa rõ:**

- DT-02 gộp `P2` và điểm biên `B3` (tăng đúng 1) — một lần chạy quan sát cả kết quả đăng nhập và giá trị bộ đếm.
- BVA-07 gộp `P9` và biên `B4` (đặt lại về 0).
- `P6` không có Expected từ đặc tả ⇒ ghi Quan sát/INCONCLUSIVE, không chấm PASS/FAIL.
- Email khác hoa/thường, khoảng trắng đầu/cuối: đặc tả không quy định ⇒ không tạo lớp, ghi điểm chưa rõ Q3.
- P10 là lớp UI theo ràng buộc R4, tách khỏi P6 API: `DT-06` với email chưa đăng ký không chứng minh form có chặn email sai định dạng. P11 (key vắng) và P12 (`null` tường minh) là hai stimulus khác nhau; UI `required` không thể tạo hai JSON body này bằng thao tác thông thường.

**Câu hỏi còn mở:** Q1 — hết khóa thì bộ đếm có đặt lại về 0 không? (ảnh hưởng hành vi lần sai kế tiếp). Q2 — "không để lộ chi tiết nguyên nhân" có cấm thông báo nêu rõ tài khoản đang bị khóa không? Q3 — email có phân biệt hoa/thường hoặc trim khoảng trắng không? Q4 — API trả gì với email sai định dạng (đặc tả chỉ ràng buộc ở UI)?

## Coverage EP

Mẫu số là các lớp EP đã chọn (P1–P12 = 12 lớp; P6 để Quan sát, không tính vào pass/fail). Bổ sung P10–P12 từ run `run-20261021-fr02-gap-api` và `run-20261021-fr02-gap-ui`; 9 lớp cũ giữ kết quả run `run-20261020-fr02`.

| Nghĩa vụ | Khả thi | Có case | Đã chạy có evidence | Đạt oracle | Còn thiếu / chưa rõ |
| --- | ---: | ---: | ---: | ---: | --- |
| Lớp `P1`–`P12` | 12 | 12 | 12 | 7 | `P2`, `P10`–`P12` FAIL; `P6` INCONCLUSIVE |

- **Mẫu số EP:** 12 lớp đã chọn. **Designed 12/12**, **Executed 12/12**, **Passed 7/12**; bốn lớp FAIL (`P2`, `P10`–`P12`) và một lớp Quan sát (`P6`). P11 FAIL ở side effect `login_attempts +2`, cùng defect BUG-FR02-01; riêng assertion không cấp JWT đạt.
- FAIL vẫn tính đã chạy. Chi tiết Actual, `EV-ID` và bug ở `test-results.md`.
