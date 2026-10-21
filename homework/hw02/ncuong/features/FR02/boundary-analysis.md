# FR02 — Boundary analysis (BVA)

**Feature / interface:** FR-02 Đăng nhập & Khóa tài khoản — **Backend API** `POST /api/login`; quan sát side effect qua `users.login_attempts` và `users.locked_until`.  
**Nguồn yêu cầu:** `README.md` §2 FR-02.  
**Đơn vị / độ chính xác:** bộ đếm là số nguyên (bước 1); thời gian khóa là mili-giây, đo bằng `Date.now()` của Node (sai số đo do độ trễ mạng/lệnh, ghi ở từng ca). Fixture khóa dùng chuỗi ISO UTC (`new Date(...).toISOString()`) đúng định dạng server ghi, **không** dùng `datetime('now')` của SQLite (UTC, bị JS hiểu là giờ local).

## B1 — Ngưỡng khóa "sai từ 3 lần trở lên liên tiếp"

**Rule:** R3 — `login_attempts >= 3` sau một lần sai thì khóa tài khoản (`README §FR-02`).  
**Biên:** `login_attempts = 3`, dấu bằng **thuộc phía khóa** (bao gồm 3); đơn vị: lần sai liên tiếp, bước 1.  
**Setup chung:** tài khoản chưa khóa, `locked_until = NULL`; mật khẩu test `WrongPass1!`.

| Điểm | Giá trị/trạng thái cần tạo | Expected | Test case | Khả năng thử |
| --- | --- | --- | --- | --- |
| Ngay dưới (2 lần sai) | sai lần 1 rồi lần 2; `login_attempts` kỳ vọng = 2 | **Không** khóa, `locked_until = NULL` | BVA-02 | Khả thi |
| Tại biên (3 lần sai) | chuẩn bị `login_attempts = 2`, `locked_until = NULL` (đã sai 2 lần), rồi sai lần 3 | **Khóa được kích hoạt** (`locked_until` được đặt); giá trị bộ đếm và độ dài khóa chấm ở B3/B2 | BVA-03 | Khả thi |
| Ngay trên (thử thêm khi đang khóa) | tài khoản đang khóa, gửi thêm một lần đăng nhập | Bị từ chối với trạng thái khóa; bộ đếm không đổi | BVA-04 | Khả thi |

*Ghi chú:* trên SUT hiện tại tài khoản đã bị khóa ngay sau 2 lần sai (do `BUG-FR02-01`), nên "tại biên" phải chuẩn bị trạng thái `login_attempts = 2` bằng DB test thay vì tạo tuần tự; giá trị bộ đếm `3` là nghĩa vụ của B3/DT-02, BVA-03 chỉ chấm việc **khóa có được kích hoạt đúng tại ngưỡng** hay không.

## B2 — Thời lượng khóa 30 giây và mốc hết hạn

**Rule:** R3 — khóa tạm **30 giây**; R6 — còn `locked_until` thì bị từ chối (`README §FR-02`).  
**Biên:** `locked_until − now = 30 000 ms`; quan hệ `now < locked_until` quyết định còn bị khóa. Đơn vị: giây (đo tương đối từ thời điểm khóa `t0`), độ chính xác ±1 s.  
**Setup chung:** kích hoạt khóa bằng lần sai đưa bộ đếm qua ngưỡng; `t0` = thời điểm server ghi `locked_until`; giữ nguyên `locked_until` giữa các điểm.

| Điểm | Giá trị/trạng thái cần tạo | Expected | Test case | Khả năng thử |
| --- | --- | --- | --- | --- |
| Ngay dưới 30 s | `t0 + 29 s`, mật khẩu **đúng** | Vẫn bị khóa (chưa hết 30 s) | BVA-05 | Khả thi (chờ 29 s) |
| Tại/Ngay trên 30 s | `t0 + 31 s`, mật khẩu **đúng** | Hết khóa, đăng nhập thành công + token | BVA-06 | Khả thi (chờ 31 s) |
| Trạng thái hết hạn | `locked_until` = quá khứ (`now − 60 phút`), mật khẩu đúng | Hết khóa, đăng nhập thành công + token | BVA-08 | Khả thi (chuẩn bị DB) |

*Ghi chú:* ngoài 2 điểm thời gian thực, ca BVA-02/BVA-03 còn ghi `locked_until` sau khi khóa để đối chiếu độ dài đặt bởi server (`locked_until − now`); giá trị này là bằng chứng trực tiếp cho BUG-FR02-02.

## B3 — Bộ đếm tăng đúng 1 đơn vị mỗi lần sai (đẳng thức, không phải ngưỡng)

**Rule:** R2 — "tăng bộ đếm lên đúng 1 đơn vị" (`README §FR-02`).  
**Biên:** giá trị `login_attempts` sau một lần sai phải bằng giá trị trước `+1`; kiểm tra tại chuyển `0 → 1`.  
**Setup:** tài khoản sạch `login_attempts = 0`.

| Điểm | Giá trị/trạng thái cần tạo | Expected | Test case | Khả năng thử |
| --- | --- | --- | --- | --- |
| Từ 0 | sai 1 lần từ `login_attempts = 0` | `login_attempts = 1` | DT-02 (đồng thời là BVA-01, gộp) | Khả thi |

B3 không phải ngưỡng đổi hành vi nên chỉ có một điểm giá trị; các mốc 2, 3 thuộc B1.

## B4 — Đặt lại bộ đếm về 0 sau khi đăng nhập thành công

**Rule:** R5 (ASSUMED từ "liên tiếp") — thành công đặt lại bộ đếm.  
**Biên:** giá trị `0` (rỗng).  
**Setup:** tài khoản chưa khóa, đã sai 1 lần (bộ đếm > 0).

| Điểm | Giá trị/trạng thái cần tạo | Expected | Test case | Khả năng thử |
| --- | --- | --- | --- | --- |
| Tại 0 | sau 1 lần sai, đăng nhập đúng | `login_attempts = 0`, `locked_until = NULL` | BVA-07 | Khả thi |

## Coverage BVA

Các lớp bổ sung `P10` (định dạng email), `P11` (thiếu key password) và `P12` (`password: null`) là các miền phân loại, không tạo ngưỡng số/thời gian mới. Vì vậy không gán B-ID giả hoặc tăng mẫu số BVA; `DT-10` vẫn quan sát cùng quy tắc tăng đúng 1 của B3 và tái hiện BUG-FR02-01, nhưng không tạo thêm điểm biên độc lập.

Mẫu số là các điểm biên đủ điều kiện: B1 có 3 điểm, B2 có 3 điểm, B3 có 1 điểm, B4 có 1 điểm = **8 điểm**.

| Nghĩa vụ biên | Khả thi | Có case | Đã chạy đúng điểm có evidence | Đạt oracle | Còn thiếu / không quan sát được |
| --- | ---: | ---: | ---: | ---: | --- |
| B1 ngay dưới / tại / ngay trên | 3 | 3 | 3 | 2 | B1 ngay dưới FAIL (khóa sớm, BUG-FR02-01) |
| B2 ngay dưới / tại-trên / hết hạn | 3 | 3 | 3 | 2 | B2 tại/ngay trên FAIL (khóa 180 s, BUG-FR02-02) |
| B3 tăng đúng 1 (từ 0) | 1 | 1 | 1 | 0 | FAIL (tăng 2, BUG-FR02-01) |
| B4 đặt lại về 0 | 1 | 1 | 1 | 1 | — |

- **Mẫu số BVA:** 8 điểm đủ điều kiện. **Designed 8/8**, **Executed 8/8**, **Passed 5/8**; 3 điểm FAIL có evidence.
- BVA-01 trùng DT-02 (một ca phục vụ cả EP và BVA) nên chỉ tính một lần trong catalog. Chi tiết Actual và bug ở `test-results.md`.
