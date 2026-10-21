# Báo cáo tổng hợp — Domain Testing và Boundary Value Analysis

## 0. Thông tin sinh viên

| Trường | Giá trị |
| --- | --- |
| Họ và tên | Dương Nhật Cường |
| MSSV | 23120223 |
| Lớp / Nhóm | Kiểm thử phần mềm — CQ2023/3 / Group13 |
| Bài tập | HW02 — Domain Testing & BVA |
| Repository | [eshop-sut-homework](https://github.com/SoftwareTesting-Group13/eshop-sut-homework) |

## 1. Feature đã chọn

| Nhóm | Feature | Bộ báo cáo |
| --- | --- | --- |
| A | FR-02 — Login and account lockout | [Domain](../features/FR02/domain-analysis.md) · [BVA](../features/FR02/boundary-analysis.md) · [Test cases](../features/FR02/test-cases.md) · [Results](../features/FR02/test-results.md) |
| B | FR-10 — Order state machine | [Domain](../features/FR10/domain-analysis.md) · [BVA](../features/FR10/boundary-analysis.md) · [Test cases](../features/FR10/test-cases.md) · [Results](../features/FR10/test-results.md) |
| C | FR-17 — Coupon management (CRUD) | [Domain](../features/FR17/domain-analysis.md) · [BVA](../features/FR17/boundary-analysis.md) · [Test cases](../features/FR17/test-cases.md) · [Results](../features/FR17/test-results.md) |
| D | FR-06 — Product detail view (Mobile) | [Domain](../features/FR06/domain-analysis.md) · [BVA](../features/FR06/boundary-analysis.md) · [Test cases](../features/FR06/test-cases.md) · [Results](../features/FR06/test-results.md) |

## 2. Tổng hợp test case và coverage

Đếm theo T-ID duy nhất: một ca phủ cả EP và BVA chỉ tính một lần. Đã chạy = PASS + FAIL + Quan sát; Thiết kế = Đã chạy + BLOCKED + Chưa chạy.

| Feature / run được chọn | Thiết kế | Đã chạy | PASS | FAIL | Quan sát | BLOCKED | Chưa chạy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| FR-02 / run-20261020-fr02 + run-20261021-fr02-gap-api/ui | 18 | 18 | 11 | 6 | 1 | 0 | 0 |
| FR-10 / run-20261020-fr10 | 20 | 20 | 18 | 2 | 0 | 0 | 0 |
| FR-17 / run-20261020-fr17 | 32 | 32 | 11 | 20 | 1 | 0 | 0 |
| FR-06 / run-20261021-fr06-mobile và API-only run-20261021-fr06-api | 16 | 16 | 3 | 9 | 4 | 0 | 0 |
| **Tổng** | **86** | **86** | **43** | **37** | **6** | **0** | **0** |

| Feature | EP: thiết kế / chạy / PASS | BVA: thiết kế / chạy / PASS | Giao diện và giới hạn |
| --- | --- | --- | --- |
| FR-02 | 12 / 12 / 7 | 8 / 8 / 5 | API trên backend/DB cách ly; DT-09 còn có UI Firefox; 1 ca Quan sát thiếu oracle. |
| FR-10 | 20 / 20 / 18 | 9 / 9 / 7 | API đã chạy; 2 bug còn được xác nhận qua UI. |
| FR-17 | 32 / 32 / 11 | 9 / 9 / 5 | Kết quả chính từ API/Postman; UI admin chưa chạy cùng các ca. 1 ca Quan sát thiếu oracle. |
| FR-06 | 16 / 16 / 3 | 6 / 6 / 4 | 12 ca có Actual UI Android; 4 ca ID bất thường chỉ chạy API và thiếu oracle status/body. |

Các phân số coverage trên là số nghĩa vụ EP/BVA, không cộng vào 86 T-ID. FR-02 bổ sung 3 T-ID, 2 bug mới có ảnh UI/API tại [screenshots](../features/FR02/screenshots/) và [evidence](../features/FR02/evidence/FR02-evidence.md). FR-06 có 24 screenshot tại [screenshots](../features/FR06/screenshots/) và [evidence log](../features/FR06/evidence/FR06-evidence.md); FR-17 có 39 ảnh Postman cho 19/20 ca FAIL và 1 ảnh UI minh họa hệ quả coupon 150% tại [screenshots](../features/FR17/screenshots/).

## 3. Tổng hợp bug

### 3.1. Bug đã xác nhận

| Bug ID | Mô tả ngắn | Severity | Priority | T-ID liên quan | Trạng thái / đường xác nhận | Issue / chi tiết |
| --- | --- | --- | --- | --- | --- | --- |
| BUG-FR02-01 | Mỗi lần đăng nhập sai cộng 2, khóa sớm sau 2 lần | High | High | DT-02, BVA-02, BVA-03 | Đã xác nhận API + UI | [#25](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/25) · [Results](../features/FR02/test-results.md) |
| BUG-FR02-02 | Khóa 180 giây thay vì 30 giây | Medium | High | BVA-02, BVA-06 | Đã xác nhận API + UI | [#26](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/26) · [Results](../features/FR02/test-results.md) |
| BUG-FR02-03 | Form login chấp nhận email sai định dạng | Medium | Medium | DT-09 | Đã tái hiện UI + API, có ảnh | [Results](../features/FR02/test-results.md) · Issue đang chuẩn bị |
| BUG-FR02-04 | Login `password:null` cấp JWT | High | High | DT-11 | Đã tái hiện API 2/2, có ảnh log | [Results](../features/FR02/test-results.md) · Issue đang chuẩn bị |
| BUG-FR10-01 | Admin chuyển đơn canceled thành delivered | Medium | Medium | DT-14 | Đã xác nhận API + UI | [#33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33) · [Results](../features/FR10/test-results.md) |
| BUG-FR10-02 | User hủy được đơn đang shipping | High | High | DT-16 | Đã xác nhận API + UI | [#34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34) · [Results](../features/FR10/test-results.md) |
| BUG-FR17-01 | Tạo coupon với code rỗng/thiếu/chỉ khoảng trắng | Medium | Medium | DT-04–DT-06 | Đã xác nhận API/Postman | [#47](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/47) · [Results](../features/FR17/test-results.md) |
| BUG-FR17-02 | Tạo coupon với type sai hoặc thiếu | Medium | Medium | DT-08–DT-09 | Đã xác nhận API/Postman | [#48](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/48) · [Results](../features/FR17/test-results.md) |
| BUG-FR17-03 | Tạo coupon với discount_value không hợp lệ | High | High | DT-10–DT-13 | Đã xác nhận API/Postman | [#49](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/49) · [Results](../features/FR17/test-results.md) |
| BUG-FR17-04 | Tạo coupon với expired_at không hợp lệ | High | High | DT-15–DT-17 | Đã xác nhận API/Postman | [#50](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/50) · [Results](../features/FR17/test-results.md) |
| BUG-FR17-05 | Tạo coupon với min_order_amount không hợp lệ | Medium | Medium | DT-21–DT-23 | Đã xác nhận API/Postman | [#51](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/51) · [Results](../features/FR17/test-results.md) |
| BUG-FR17-06 | max_uses_per_user bằng 0/âm/thiếu vẫn được nhận | Medium | Medium | DT-26–DT-28 | Đã xác nhận API/Postman | [#52](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/52) · [Results](../features/FR17/test-results.md) |
| BUG-FR17-07 | Tạo save10 bên cạnh SAVE10 | Medium | Medium | DT-07 | Đã xác nhận API/Postman | [#53](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/53) · [Results](../features/FR17/test-results.md) |
| BUG-FR17-08 | Tạo coupon percent với discount_value 150 | High | High | DT-32 | Đã xác nhận API/Postman; ảnh UI phụ | [#54](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54) · [Results](../features/FR17/test-results.md) |
| BUG-FR06-01 | Chi tiết sản phẩm thiếu tên danh mục | Medium | Medium | T01–T03 | Đã xác nhận UI Android | [#55](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/55) · [Results](../features/FR06/test-results.md) |
| BUG-FR06-02 | Quantity invalid vẫn thêm vào giỏ | Medium | High | T10–T14, T16 | Đã xác nhận UI Android | [#56](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/56) · [Results](../features/FR06/test-results.md) |

### 3.2. Severity

| Feature | Critical | High | Medium | Low | Tổng |
| --- | ---: | ---: | ---: | ---: | ---: |
| FR-02 | 0 | 2 | 2 | 0 | 4 |
| FR-10 | 0 | 1 | 1 | 0 | 2 |
| FR-17 | 0 | 3 | 5 | 0 | 8 |
| FR-06 | 0 | 0 | 2 | 0 | 2 |
| **Tổng** | **0** | **6** | **10** | **0** | **16** |

| Mức | Tiêu chí |
| --- | --- |
| Critical | Lộ/mất dữ liệu nhạy cảm, lỗi bảo mật nghiêm trọng hoặc luồng chính ngừng hoạt động. |
| High | Sai luồng cốt lõi hoặc quy tắc quan trọng, gây ảnh hưởng lớn đến người dùng hay số tiền. |
| Medium | Sai quy tắc chức năng hoặc validation với phạm vi ảnh hưởng hẹp hơn High. |
| Low | Sai lệch hiển thị/nội dung nhỏ, ít ảnh hưởng đến việc hoàn thành tác vụ. |

Priority đánh giá riêng theo mức ảnh hưởng, tần suất và độ cấp bách; vì vậy BUG-FR02-02 và BUG-FR06-02 có priority High dù severity Medium.

### 3.3. Tái hiện ngắn theo bug

Các bước dưới đây dùng fixture và quyền truy cập của từng [feature report](#1-feature-đã-chọn). FR-17 là kết quả API/Postman; hướng dẫn UI trong feature report chưa được tính là đã chạy.

#### BUG-FR02-01 — Bộ đếm sai tăng 2

1. Chuẩn bị tài khoản test có login_attempts = 0; gửi POST /api/login với mật khẩu WrongPass1!.
2. Đọc login_attempts; lặp lại một lần đăng nhập sai và đọc locked_until.

**Expected:** tăng 1 mỗi lần, chỉ khóa từ lần sai thứ 3. **Actual:** lần đầu thành 2, lần thứ 2 thành 4 và bị khóa. [Evidence](../features/FR02/evidence/FR02-evidence.md) · [Issue #25](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/25).

---

#### BUG-FR02-02 — Thời lượng khóa 180 giây

1. Đưa tài khoản test tới ngưỡng khóa; ghi thời điểm t0 và locked_until.
2. Tại t0 + 31 giây, đăng nhập bằng mật khẩu đúng.

**Expected:** khóa 30 giây, đăng nhập lại được. **Actual:** locked_until cách t0 khoảng 180 giây và API vẫn trả 403. [Evidence](../features/FR02/evidence/FR02-evidence.md) · [Issue #26](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/26).

---

#### BUG-FR02-03 — Email sai định dạng vẫn đăng nhập trên web

1. Trên DB test, tạo `not-an-email` / `Passw0rd!` qua API đăng ký; API hiện cho phép fixture này.
2. Mở form `/login`, nhập `not-an-email` và `Passw0rd!`, bấm **Sign In**.

**Expected:** ô email `type="email"` chặn định dạng sai trước submit. **Actual:** `type="text"`, browser cho submit; trang chủ hiện user đã đăng nhập và token được lưu. [Evidence + ảnh UI](../features/FR02/evidence/FR02-evidence.md) · [Results](../features/FR02/test-results.md).

---

#### BUG-FR02-04 — Password null vẫn cấp JWT

1. Trên DB test, API đăng ký tạo account `fr02.gap.null@eshop.com` với `password:null`; DB lưu `NULL`.
2. Gửi `POST /api/login` với cùng email và `password:null`; lặp lại bằng account thứ hai.

**Expected:** từ chối xác thực, không cấp JWT. **Actual:** cả hai lần trả HTTP 200 + JWT. Ca thiếu hẳn key `password` trả 401 và chỉ tái hiện BUG-FR02-01 ở bộ đếm. [Evidence + ảnh log API](../features/FR02/evidence/FR02-evidence.md) · [Results](../features/FR02/test-results.md).

---

#### BUG-FR10-01 — Rời trạng thái canceled

1. Tạo đơn test rồi đưa về canceled; admin mở đơn đó.
2. Chọn “Đánh dấu Đã giao” hoặc gửi PUT /api/admin/orders/:id/status với status = delivered; đọc lại trạng thái.

**Expected:** từ chối chuyển khỏi canceled. **Actual:** đơn chuyển thành delivered. [Evidence](../features/FR10/evidence/FR10-evidence.md) · [Issue #33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33).

---

#### BUG-FR10-02 — User hủy đơn shipping

1. Tạo đơn của user test, admin đưa đơn qua pending → confirmed → shipping.
2. User bấm “Hủy đơn” trong lịch sử hoặc gửi PUT /api/orders/:id/cancel bằng token của mình; đọc lại đơn.

**Expected:** không hủy được ở shipping. **Actual:** API trả 200 và đơn thành canceled. [Evidence](../features/FR10/evidence/FR10-evidence.md) · [Issue #34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34).

---

#### BUG-FR17-01 — Code không hợp lệ

1. Dùng admin token, gửi POST /api/admin/coupons với các trường hợp lệ khác; lần lượt để code rỗng, bỏ code hoặc đặt code chỉ gồm khoảng trắng.
2. GET /api/coupons để kiểm tra row mới.

**Expected:** từ chối, không tạo row. **Actual:** HTTP 200 và tạo cả ba loại code không hợp lệ. [Evidence](../features/FR17/evidence/FR17-evidence.md) · [Issue #47](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/47).

---

#### BUG-FR17-02 — Type không hợp lệ

1. POST /api/admin/coupons bằng admin token, đặt type = percentage hoặc bỏ type; các trường còn lại hợp lệ.
2. GET danh sách coupon.

**Expected:** từ chối vì type chỉ nhận percent/fixed. **Actual:** HTTP 200 và lưu type sai hoặc NULL. [Evidence](../features/FR17/evidence/FR17-evidence.md) · [Issue #48](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/48).

---

#### BUG-FR17-03 — Discount value không hợp lệ

1. POST /api/admin/coupons bằng admin token với discount_value lần lượt là 0, -1, thiếu hoặc chuỗi abc; các trường còn lại hợp lệ.
2. GET danh sách coupon.

**Expected:** từ chối, không tạo row. **Actual:** HTTP 200, lưu từng giá trị không hợp lệ. [Evidence](../features/FR17/evidence/FR17-evidence.md) · [Issue #49](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/49).

---

#### BUG-FR17-04 — Expiry không hợp lệ

1. POST /api/admin/coupons bằng admin token với expired_at thiếu, rỗng hoặc not-a-date; các trường còn lại hợp lệ.
2. GET danh sách coupon.

**Expected:** từ chối, không tạo row. **Actual:** HTTP 200, lưu NULL/chuỗi rỗng/ngày sai định dạng. [Evidence](../features/FR17/evidence/FR17-evidence.md) · [Issue #50](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/50).

---

#### BUG-FR17-05 — Min order amount không hợp lệ

1. POST /api/admin/coupons bằng admin token với min_order_amount = -1, thiếu hoặc abc; các trường còn lại hợp lệ.
2. GET danh sách coupon.

**Expected:** từ chối, không tạo row. **Actual:** HTTP 200, lưu số âm/NULL/chuỗi. [Evidence](../features/FR17/evidence/FR17-evidence.md) · [Issue #51](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/51).

---

#### BUG-FR17-06 — Max uses per user không hợp lệ

1. POST /api/admin/coupons bằng admin token với max_uses_per_user = 0, -1 hoặc thiếu; các trường còn lại hợp lệ.
2. GET danh sách coupon.

**Expected:** từ chối, không tạo row. **Actual:** HTTP 200; 0/thiếu bị đổi thành 1, -1 được lưu nguyên. [Evidence](../features/FR17/evidence/FR17-evidence.md) · [Issue #52](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/52).

---

#### BUG-FR17-07 — Mã khác hoa/thường

1. Trong DB test đã có code SAVE10, POST /api/admin/coupons bằng admin token với code = save10 và các trường còn lại hợp lệ.
2. GET danh sách coupon.

**Expected:** từ chối mã trùng không phân biệt hoa/thường theo oracle người kiểm thử đã xác nhận. **Actual:** HTTP 200, danh sách có cả SAVE10 và save10. [Evidence](../features/FR17/evidence/DT-07.log) · [Issue #53](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/53).

---

#### BUG-FR17-08 — Phần trăm vượt 100

1. POST /api/admin/coupons bằng admin token với type = percent và discount_value = 150; các trường còn lại hợp lệ.
2. GET danh sách coupon.

**Expected:** từ chối vì percent tối đa 100 theo oracle người kiểm thử đã xác nhận. **Actual:** HTTP 200, lưu 150; ảnh UI minh họa hệ quả khi áp dụng. [Evidence](../features/FR17/evidence/DT-32.log) · [Issue #54](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54).

---

#### BUG-FR06-01 — Thiếu danh mục

1. Trên Android Expo app có backend test seed, mở chi tiết ID 1, ID 2 hoặc ID 5 từ danh sách.
2. Quan sát card từ ảnh lớn đến nút thêm giỏ.

**Expected:** có tên danh mục, ví dụ “Điện thoại” hoặc “Phụ kiện”. **Actual:** chỉ có ảnh, tên, giá, mô tả; không có danh mục. [Evidence](../features/FR06/evidence/FR06-evidence.md) · [Issue #55](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/55).

---

#### BUG-FR06-02 — Quantity invalid vẫn được thêm

1. Reset giỏ về Giỏ (0), mở chi tiết ID 1; xóa số lượng mặc định 1 rồi để rỗng hoặc nhập 0.
2. Bấm “Thêm vào giỏ hàng”, đóng alert và xem Giỏ.

**Expected:** không thêm sản phẩm từ input không hợp lệ. **Actual:** báo thành công, Giỏ có quantity 1; các lớp -1, 1.5, abc, 2abc cũng được ghi trong feature report. [Evidence](../features/FR06/evidence/FR06-evidence.md) · [Issue #56](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/56).

---

## 4. Tài liệu liên quan

- [AI Audit Report](ai-audit.md); [AI Critique](ai-critique.md) — sinh viên tự viết.
- Quan sát ngoài EP/BVA: [FR-02](../supporting-materials/fr02-observations.md), [FR-10](../supporting-materials/fr10-observations.md), [FR-17](../supporting-materials/fr17-observations.md), [FR-06](../supporting-materials/fr06-observations.md). Không cộng vào coverage.
