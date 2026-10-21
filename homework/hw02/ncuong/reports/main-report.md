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
| FR-10 / run-20261020-fr10 + run-20261021-fr10-gap-access | 23 | 23 | 19 | 4 | 0 | 0 | 0 |
| FR-17 / run-20261020-fr17 | 32 | 32 | 11 | 20 | 1 | 0 | 0 |
| FR-06 / run-20261021-fr06-mobile và API-only run-20261021-fr06-api | 16 | 16 | 3 | 9 | 4 | 0 | 0 |
| **Tổng** | **89** | **89** | **44** | **39** | **6** | **0** | **0** |

| Feature | EP: thiết kế / chạy / PASS | BVA: thiết kế / chạy / PASS | Giao diện và giới hạn |
| --- | --- | --- | --- |
| FR-02 | 12 / 12 / 7 | 8 / 8 / 5 | API trên backend/DB cách ly; DT-09 còn có UI Firefox; 1 ca Quan sát thiếu oracle. |
| FR-10 | 20 / 20 / 18 (trạng thái); 4 / 4 / 2 (quyền, DT-01 dùng chung) | 9 / 9 / 7 | 2 bug trạng thái có UI; BUG-FR10-03 chỉ xác nhận API. |
| FR-17 | 32 / 32 / 11 | 9 / 9 / 5 | Kết quả chính từ API/Postman; UI admin chưa chạy cùng các ca. 1 ca Quan sát thiếu oracle. |
| FR-06 | 16 / 16 / 3 | 6 / 6 / 4 | 12 ca có Actual UI Android; 4 ca ID bất thường chỉ chạy API và thiếu oracle status/body. |

Các phân số coverage trên là số nghĩa vụ EP/BVA, không cộng vào 89 T-ID; lớp A1 của FR-10 dùng lại DT-01. FR-02 bổ sung 3 T-ID, 2 bug mới có ảnh UI/API tại [screenshots](../features/FR02/screenshots/) và [evidence](../features/FR02/evidence/FR02-evidence.md). FR-10 bổ sung 3 T-ID quyền truy cập, có [raw API log](../features/FR10/evidence/FR10-evidence.md) và [ảnh trình bày log](../features/FR10/screenshots/BUG-FR10-03-api-evidence.png) trong Issue #60. FR-06 có 24 screenshot tại [screenshots](../features/FR06/screenshots/) và [evidence log](../features/FR06/evidence/FR06-evidence.md); FR-17 có 39 ảnh Postman cho 19/20 ca FAIL và 1 ảnh UI minh họa hệ quả coupon 150% tại [screenshots](../features/FR17/screenshots/).

## 3. Domain Testing — phân lớp tương đương

Phân miền theo đầu vào, trạng thái và tác nhân của từng FR; mỗi lớp có một ca đại diện. Kỳ vọng lấy từ [README của SUT](../../../../README.md) và [API specification](../../../../api_specification.md). Các giả định và trường hợp thiếu oracle được ghi rõ trong báo cáo feature; FAIL là kết quả chạy sai kỳ vọng, còn Quan sát là đã chạy nhưng chưa đủ cơ sở chấm. Bảng dưới tóm lược lớp, oracle và Actual; bảng lớp đầy đủ cùng EV-ID nằm trong các link ở §1.

### 3.1. FR-02 — Login and account lockout

Miền gồm `email`, `password`, trạng thái khóa và bộ đếm đăng nhập sai. Baseline là tài khoản test chưa khóa, mật khẩu `Passw0rd!`.

| Lớp EP | Ca đại diện và oracle | Kết quả |
| --- | --- | --- |
| P1 | Email đã đăng ký + mật khẩu đúng → JWT; DT-01 | PASS |
| P2 | Mật khẩu sai từ bộ đếm 0 → không token, bộ đếm tăng đúng 1; DT-02 | FAIL: tăng 2, BUG-FR02-01 |
| P3–P5 | Email chưa đăng ký, mật khẩu rỗng, email rỗng/thiếu → không token; DT-03–DT-05 | 3 PASS |
| P6 | Email sai định dạng chưa đăng ký gửi thẳng API; spec chỉ quy định validation ở UI; DT-06 | Quan sát |
| P7–P8 | Tài khoản đang khóa + mật khẩu đúng/sai → từ chối, không tăng bộ đếm; DT-07–DT-08 | 2 PASS |
| P9 | Một lần sai rồi đăng nhập đúng → reset bộ đếm về 0; BVA-07 | PASS; giả định từ chữ “liên tiếp” |
| P10 | Tài khoản đăng ký với `not-an-email`; form login phải chặn email sai định dạng; DT-09 | FAIL: form gửi request và đăng nhập, BUG-FR02-03 |
| P11 | Body có email nhưng thiếu key `password` → không token, nếu tăng bộ đếm thì chỉ tăng 1; DT-10 | FAIL ở bộ đếm +2, cùng BUG-FR02-01; không cấp token |
| P12 | Account có password DB `NULL`, gửi `password:null` → không token; DT-11 | FAIL: cấp JWT, BUG-FR02-04 |

**Coverage EP:** 12/12 lớp đã thiết kế và chạy; 7 PASS, 4 FAIL, 1 Quan sát. Riêng thời lượng khóa sai được phát hiện ở BVA, BUG-FR02-02.

### 3.2. FR-10 — Order state machine

Miền cốt lõi là trạng thái nguồn × trạng thái đích × tác nhân. Luồng tiến hợp lệ: `pending → confirmed → shipping → delivered`; `canceled` là nhánh kết thúc. Cả `delivered` và `canceled` không được rời đi. User chỉ hủy đơn của mình khi còn `pending` hoặc `confirmed`.

| Lớp EP | Ca đại diện và oracle | Kết quả |
| --- | --- | --- |
| P1–P3 | Admin tiến tuần tự qua ba cạnh hợp lệ; DT-01–DT-03 | 3 PASS |
| P4–P7 | Admin/user hủy ở `pending` hoặc `confirmed` → `canceled`; DT-04–DT-07 | 4 PASS |
| P8–P12 | Bỏ qua, lùi hoặc đặt lại cùng trạng thái → lỗi và không đổi đơn; DT-08–DT-12 | 5 PASS |
| P13–P14 | Rời `delivered`/`canceled` → lỗi và không đổi đơn; DT-13–DT-14 | 1 PASS, 1 FAIL: `canceled → delivered`, BUG-FR10-01 |
| P15 | Đích `shipped` ngoài tập trạng thái → lỗi, không đổi; DT-15 | PASS |
| P16–P18 | User hủy ở `shipping`/`delivered`/`canceled` → lỗi, không đổi; DT-16–DT-18 | 2 PASS, 1 FAIL: hủy `shipping`, BUG-FR10-02 |
| P19–P20 | Đơn không tồn tại/không sở hữu; admin hủy từ `shipping` theo sơ đồ → lỗi, không đổi; DT-19–DT-20 | 2 PASS; oracle P20 là giả định cần nhóm xác nhận |

**Coverage EP trạng thái:** 20/20 lớp đã chạy; 18 PASS, 2 FAIL. Miền quyền bổ sung AI-GAP-FR10-01 có 4 lớp: admin token được phép (DT-01, PASS); user token trên đơn của mình và của người khác phải bị chặn (DT-21/DT-22, 2 FAIL, BUG-FR10-03); không token bị chặn (DT-23, PASS). Miền quyền 4/4 đã chạy, 2 PASS, 2 FAIL; DT-01 dùng chung nên tổng feature là 23 T-ID.

### 3.3. FR-17 — Coupon management

Baseline tạo coupon qua API Admin: code mới, `type=percent`, `discount_value=10`, `min_order_amount=100000`, `expired_at=2099-12-31`, `max_uses_per_user=1`; mỗi nhóm chỉ đổi một trường. Với input không hợp lệ, oracle là từ chối và không tạo row.

| Nhóm EP | Lớp/ca đại diện | Oracle chính | Kết quả |
| --- | --- | --- | --- |
| `code` | P1, P3–P7; DT-01, DT-03–DT-07 | Code bắt buộc, duy nhất; `save10` trùng `SAVE10` theo oracle người kiểm thử xác nhận | 2 PASS, 4 FAIL |
| `type` | P2, P8–P9; DT-02, DT-08–DT-09 | Chỉ `percent`/`fixed`, trường bắt buộc | 1 PASS, 2 FAIL |
| `discount_value` | P10–P14; DT-10–DT-14 | Số dương; 0, âm, thiếu, chữ bị từ chối | 1 PASS, 4 FAIL |
| `expired_at` | P15–P18; DT-15–DT-18 | Trường bắt buộc, ngày hợp lệ; ngày quá khứ được chấm theo giả định | 1 PASS, 3 FAIL |
| `min_order_amount` | P19–P23; DT-19–DT-23 | Số ≥ 0, trường bắt buộc | 2 PASS, 3 FAIL |
| `max_uses_per_user` | P24–P28; DT-24–DT-28 | Số nguyên ≥ 1, trường bắt buộc | 2 PASS, 3 FAIL |
| Xem/xóa | P29–P31; DT-29–DT-31 | Xem đúng danh sách, xóa ID tồn tại; ID không tồn tại thiếu oracle | 2 PASS, 1 Quan sát |
| Percent > 100 | P32; DT-32 (`150`) | Từ chối giá trị >100% theo oracle người kiểm thử xác nhận | 1 FAIL, BUG-FR17-08 |

**Coverage EP:** 32/32 lớp đã chạy; 11 PASS, 20 FAIL, 1 Quan sát. Các ca FAIL được nhóm thành 8 bug trong §5. Giới hạn 100% là kết luận nghiệp vụ được người kiểm thử xác nhận sau khi đọc spec; không diễn đạt như giới hạn có sẵn trong spec gốc.

### 3.4. FR-06 — Product detail view (Mobile)

Miền gồm sản phẩm được chọn, dữ liệu chi tiết và chuỗi quantity trong ô nhập. UI được chạy trên Android emulator; ID ngoài danh sách chỉ thử qua API vì không chọn được trên UI.

| Lớp EP | Ca đại diện và oracle | Kết quả |
| --- | --- | --- |
| P01–P03 | ID 1, 2, 5 → đủ ảnh, tên, giá, mô tả và danh mục; T01–T03 | 3 FAIL: thiếu danh mục, BUG-FR06-01 |
| P04–P07 | ID `0`, `6`, `abc`, `1.5`; T04–T07 | 4 Quan sát: API spec thiếu oracle status/body cho ID sai |
| P08–P09 | Quantity `1`, `2` → giỏ nhận đúng số lượng và có phản hồi; T08–T09 | 2 PASS |
| P10–P14 | Rỗng, `0`, `-1`, `1.5`, `abc` → không được thêm hàng; T10–T14 | 5 FAIL: giỏ vẫn nhận, BUG-FR06-02 |
| P15 | Thêm cùng sản phẩm lần hai → giỏ tăng đúng; T15 | PASS |
| P16 | Chuỗi hỗn hợp `2abc` → không được thêm hàng; T16 | FAIL, BUG-FR06-02 |

**Coverage EP:** 16/16 lớp đã chạy; 3 PASS, 9 FAIL, 4 Quan sát. T13 dùng ADB để đưa `1.5` vào TextInput; đường nhập bằng bàn phím mềm/dán trên thiết bị thật chưa được xác nhận.

## 4. Boundary Value Analysis — điểm biên

BVA chỉ đặt trên ngưỡng hoặc chuyển trạng thái có oracle; các ca trùng EP dùng chung T-ID. Các cột kết quả đếm **nghĩa vụ điểm biên**, không cộng với 89 test case duy nhất ở §2.

| Feature | Biên, phía invalid/valid và ca | Kỳ vọng tại điểm biên | Kết quả |
| --- | --- | --- | --- |
| FR-02 B1 | Lần sai thứ 2 / thứ 3 / thử thêm khi đã khóa; BVA-02–BVA-04 | 2 chưa khóa; 3 bắt đầu khóa; sau khóa bị chặn, bộ đếm giữ nguyên | 2 PASS, 1 FAIL: khóa sớm ở lần 2 |
| FR-02 B2 | `t0+29s` / `t0+31s` / khóa đã hết hạn; BVA-05, BVA-06, BVA-08 | 29s còn khóa; sau 30s và khi hết hạn được đăng nhập | 2 PASS, 1 FAIL: khóa 180s |
| FR-02 B3/B4 | Bộ đếm `0→1` khi sai / reset về 0 sau đúng; DT-02, BVA-07 | Tăng đúng 1 / reset về 0 | 1 PASS, 1 FAIL: tăng 2 |
| FR-10 B1 | User hủy ở `pending`, `confirmed` / `shipping`, `delivered`, `canceled`; DT-06, DT-07, DT-16–DT-18 | Chỉ hai trạng thái đầu cho hủy | 4 PASS, 1 FAIL: hủy được ở `shipping` |
| FR-10 B2 | Vào `delivered` từ `shipping` / rời `delivered` về `shipping`; DT-03, DT-13 | Cho vào, chặn rời | 2 PASS |
| FR-10 B3 | Vào `canceled` từ `pending`/`confirmed` / rời `canceled` đến `delivered`; DT-04/DT-05, DT-14 | Cho vào, chặn rời | 1 PASS, 1 FAIL: rời được `canceled` |
| FR-17 B1 | `min_order_amount = -1 / 0 / 1`; DT-21, DT-19, DT-20 | -1 bị từ chối; 0 và 1 được nhận | 2 PASS, 1 FAIL |
| FR-17 B2 | `max_uses_per_user = 0 / 1 / 2`; DT-26, DT-24, DT-25 | 0 bị từ chối; 1 và 2 được nhận | 2 PASS, 1 FAIL |
| FR-17 B3 | `discount_value = -1 / 0 / 1`; DT-11, DT-10, DT-14 | -1 và 0 bị từ chối; 1 được nhận | 1 PASS, 2 FAIL |
| FR-06 B1 | Quantity `0 / 1 / 2`; T11, T08, T09 | 0 bị từ chối; 1 và 2 được nhận | 2 PASS, 1 FAIL |
| FR-06 B2 | Quantity `1 / 1.5 / 2`; T08, T13, T09 | Số nguyên được nhận; 1.5 bị từ chối | 2 PASS, 1 FAIL |

| Feature | Điểm biên thiết kế | Đã chạy | Đạt oracle | Không đạt | Ghi chú |
| --- | ---: | ---: | ---: | ---: | --- |
| FR-02 | 8 | 8 | 5 | 3 | B3 dùng lại DT-02 |
| FR-10 | 9 | 9 | 7 | 2 | Các ca BVA dùng lại EP |
| FR-17 | 9 | 9 | 5 | 4 | Chỉ có biên dưới từ spec gốc |
| FR-06 | 6 | 6 | 4 | 2 | 6 điểm, 4 T-ID vì T08/T09 dùng hai lần |
| **Tổng nghĩa vụ điểm** | **32** | **32** | **21** | **11** | **Không cộng vào 89 T-ID** |

**Giới hạn BVA:** FR-17 có thêm giới hạn nghiệp vụ percent tối đa 100% do người kiểm thử xác nhận; DT-32 (`150`) là một lớp EP, chưa phải bộ điểm biên trên. Các điểm sát biên `99/100/101` chưa được thiết kế/chạy nên coverage BVA 9/9 chỉ tính ba biên dưới đã xác định trước. FR-06 không coi ID `0/6` là điểm biên vì `1…5` chỉ là dải fixture; keyboard thường cho T13 chưa được kiểm tra. Miền role của FR-10 là phân loại rời rạc nên nằm ở EP, không tạo BVA số học.

## 5. Tổng hợp bug

### 5.1. Bug đã xác nhận

| Bug ID | Mô tả ngắn | Severity | Priority | T-ID liên quan | Trạng thái / đường xác nhận | Issue / chi tiết |
| --- | --- | --- | --- | --- | --- | --- |
| BUG-FR02-01 | Mỗi lần đăng nhập sai cộng 2, khóa sớm sau 2 lần | High | High | DT-02, BVA-02, BVA-03 | Đã xác nhận API + UI | [#25](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/25) · [Results](../features/FR02/test-results.md) |
| BUG-FR02-02 | Khóa 180 giây thay vì 30 giây | Medium | High | BVA-02, BVA-06 | Đã xác nhận API + UI | [#26](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/26) · [Results](../features/FR02/test-results.md) |
| BUG-FR02-03 | Form login chấp nhận email sai định dạng | Medium | Medium | DT-09 | Đã tái hiện UI + API, có ảnh | [#58](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/58) · [Results](../features/FR02/test-results.md) |
| BUG-FR02-04 | Login `password:null` cấp JWT | High | High | DT-11 | Đã tái hiện API 2/2, có ảnh log | [#59](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/59) · [Results](../features/FR02/test-results.md) |
| BUG-FR10-01 | Admin chuyển đơn canceled thành delivered | Medium | Medium | DT-14 | Đã xác nhận API + UI | [#33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33) · [Results](../features/FR10/test-results.md) |
| BUG-FR10-02 | User hủy được đơn đang shipping | High | High | DT-16 | Đã xác nhận API + UI | [#34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34) · [Results](../features/FR10/test-results.md) |
| BUG-FR10-03 | User thường đổi được trạng thái đơn qua API Admin, kể cả đơn người khác | High | High | DT-21, DT-22 | API tái hiện, ảnh log đính Issue | [#60](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/60) · [Results](../features/FR10/test-results.md) |
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

### 5.2. Severity

| Feature | Critical | High | Medium | Low | Tổng |
| --- | ---: | ---: | ---: | ---: | ---: |
| FR-02 | 0 | 2 | 2 | 0 | 4 |
| FR-10 | 0 | 2 | 1 | 0 | 3 |
| FR-17 | 0 | 3 | 5 | 0 | 8 |
| FR-06 | 0 | 0 | 2 | 0 | 2 |
| **Tổng** | **0** | **7** | **10** | **0** | **17** |

| Mức | Tiêu chí |
| --- | --- |
| Critical | Lộ/mất dữ liệu nhạy cảm, lỗi bảo mật nghiêm trọng hoặc luồng chính ngừng hoạt động. |
| High | Sai luồng cốt lõi hoặc quy tắc quan trọng, gây ảnh hưởng lớn đến người dùng hay số tiền. |
| Medium | Sai quy tắc chức năng hoặc validation với phạm vi ảnh hưởng hẹp hơn High. |
| Low | Sai lệch hiển thị/nội dung nhỏ, ít ảnh hưởng đến việc hoàn thành tác vụ. |

Priority đánh giá riêng theo mức ảnh hưởng, tần suất và độ cấp bách; vì vậy BUG-FR02-02 và BUG-FR06-02 có priority High dù severity Medium.

### 5.3. Tái hiện ngắn theo bug

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

**Expected:** ô email `type="email"` chặn định dạng sai trước submit. **Actual:** `type="text"`, browser cho submit; trang chủ hiện user đã đăng nhập và token được lưu. [Evidence + ảnh UI](../features/FR02/evidence/FR02-evidence.md) · [Issue #58](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/58).

---

#### BUG-FR02-04 — Password null vẫn cấp JWT

1. Trên DB test, API đăng ký tạo account `fr02.gap.null@eshop.com` với `password:null`; DB lưu `NULL`.
2. Gửi `POST /api/login` với cùng email và `password:null`; lặp lại bằng account thứ hai.

**Expected:** từ chối xác thực, không cấp JWT. **Actual:** cả hai lần trả HTTP 200 + JWT. Ca thiếu hẳn key `password` trả 401 và chỉ tái hiện BUG-FR02-01 ở bộ đếm. [Evidence + ảnh log API](../features/FR02/evidence/FR02-evidence.md) · [Issue #59](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/59).

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

#### BUG-FR10-03 — User thường đổi trạng thái qua API Admin

1. Tạo đơn `pending` trên DB test; đăng nhập `test@eshop.com` để lấy JWT role user.
2. Gửi `PUT /api/admin/orders/:id/status` với JWT user và `{"status":"confirmed"}`; đọc lại đơn. Lặp lại với đơn thuộc tài khoản khác.

**Expected:** từ chối và giữ `pending` vì `/api/admin/*` yêu cầu role admin. **Actual:** HTTP 200 và cả hai đơn thành `confirmed`; không token bị 401. [Evidence API + ảnh log](../features/FR10/evidence/FR10-evidence.md) · [Issue #60](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/60).

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

## 6. Tài liệu liên quan

- [AI Audit Report](ai-audit.md); [AI Critique](ai-critique.md) — sinh viên rà soát trước khi nộp.
- Quan sát ngoài EP/BVA: [FR-02](../supporting-materials/fr02-observations.md), [FR-10](../supporting-materials/fr10-observations.md), [FR-17](../supporting-materials/fr17-observations.md), [FR-06](../supporting-materials/fr06-observations.md). Không cộng vào coverage.
