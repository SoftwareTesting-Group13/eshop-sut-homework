# FR17 — Domain analysis (EP)

**Feature / interface:** FR-17 — Quản lý Mã Giảm Giá (Coupon CRUD); API `POST/GET/DELETE` coupon và màn hình admin **Mã Giảm Giá**.  
**Phạm vi:** Thêm coupon (`POST /api/admin/coupons`), xem danh sách (`GET /api/coupons`), xóa coupon (`DELETE /api/admin/coupons/:id`) và validation 6 trường bắt buộc của FR-17. Không kiểm thử áp dụng mã (FR-09), phân quyền (FR-12) hoặc sửa coupon (FR-17 không có Update).  
**Nguồn yêu cầu:** `README.md` §5 FR-17; `api_specification.md` §5.2 và §6.4; bảng seed coupon `README.md` §4 dùng làm fixture.

## Quy tắc dùng để chia miền

| Rule | Hệ thống phải làm gì? | Điều kiện ảnh hưởng | Trạng thái | Nguồn |
| --- | --- | --- | --- | --- |
| R1 | Admin thêm được coupon hợp lệ; coupon được lưu và nhìn thấy trong danh sách. | `POST /api/admin/coupons` với body hợp lệ | CONFIRMED | `README.md` §5 FR-17 ("Thêm") |
| R2 | `code` là trường bắt buộc và duy nhất. | `code` rỗng/thiếu/trùng; uniqueness phân biệt hoa-thường chưa rõ | CONFIRMED (case-sensitivity: UNRESOLVED) | `README.md` §5 FR-17 |
| R3 | `type` là trường bắt buộc, chỉ nhận `percent` hoặc `fixed`. | `type` thiếu/ngoài enum | CONFIRMED | `README.md` §5 FR-17 |
| R4 | `discount_value` là trường bắt buộc, phải là số dương (`> 0`). | `0`, âm, không phải số, thiếu; upper bound của percent chưa rõ | CONFIRMED (upper bound: UNRESOLVED) | `README.md` §5 FR-17 |
| R5 | `expired_at` là trường bắt buộc và phải là ngày hợp lệ. | thiếu/rỗng/sai định dạng; ngày quá khứ | CONFIRMED (format/past: ASSUMED) | `README.md` §5 FR-17; `api_specification.md` §6.4 |
| R6 | `min_order_amount` là trường bắt buộc, là số `>= 0`. | `0`, dương, âm, không phải số, thiếu | CONFIRMED | `README.md` §5 FR-17 |
| R7 | `max_uses_per_user` là trường bắt buộc, là số nguyên `>= 1`. | `0`, âm, thiếu; số thập phân không được đặc tả | CONFIRMED (integer: ASSUMED) | `README.md` §5 FR-17 |
| R8 | Admin xem được danh sách coupon, gồm coupon vừa tạo và các coupon seed. | `GET /api/coupons` | CONFIRMED | `README.md` §5 FR-17 ("Xem"); `api_specification.md` §5.2 |
| R9 | Admin xóa được coupon đang tồn tại; coupon biến mất khỏi danh sách. | `DELETE /api/admin/coupons/:id`; id không tồn tại chưa được đặc tả | CONFIRMED (id không tồn tại: UNRESOLVED) | `README.md` §5 FR-17 ("Xóa"); `api_specification.md` §6.4 |

**Giả định và điểm chưa rõ ảnh hưởng oracle:**

- **ASSUMED — code chỉ toàn khoảng trắng là không hợp lệ (DT-06):** đặc tả chỉ nói `code` bắt buộc; một mã chỉ có khoảng trắng không thể là mã có nghĩa. UI dùng `required` nhưng `required` không chặn chuỗi khoảng trắng.
- **ASSUMED — `expired_at` phải là ngày hợp lệ (DT-17):** API example dùng `YYYY-MM-DD`; UI dùng `input type="date"`. FR-17 chỉ nói trường bắt buộc, không nói rõ định dạng.
- **ASSUMED — coupon đã hết hạn vẫn được tạo (DT-18):** FR-17 không cấm ngày quá khứ; bảng seed có coupon `EXPIRED` với `expired_at = 2020-01-01`. Đây là lớp hợp lệ theo nghĩa CRUD, dù coupon sẽ không dùng được ở FR-09.
- **UNRESOLVED — uniqueness phân biệt hoa/thường (DT-07):** đặc tả chỉ nói "duy nhất"; không nói `SAVE10` và `save10` có bị coi là trùng không.
- **UNRESOLVED — upper bound của `discount_value` khi `type = percent` (DT-32):** FR-17 chỉ nói dương; không có ngưỡng 100%. Đây là quan sát, không chấm PASS/FAIL.
- **UNRESOLVED — xóa id không tồn tại (DT-31):** FR-17 không quy định status/message.
- **UNRESOLVED — status/message chính xác khi validation thất bại:** đặc tả không quy định; oracle dùng **non-2xx và coupon không được tạo**, không áp đặt 400/422.
- **Ngoài mô hình:** `is_active` không nằm trong danh sách trường bắt buộc của FR-17; DB mặc định 1 khi tạo. Không kiểm thử `is_active` như một chiều input.
- **Ngoài mô hình:** độ dài/định dạng `code` không có ngưỡng trong đặc tả → không áp BVA độ dài.

## Các lớp tương đương và ca đại diện

**Baseline cho các ca tạo coupon:** `code` duy nhất, `type = percent`, `discount_value = 10`, `min_order_amount = 100000`, `expired_at = 2099-12-31`, `max_uses_per_user = 1`; mỗi ca chỉ đổi đúng trường đang kiểm tra. Trước/sau mỗi request, driver lấy `GET /api/coupons` để xác nhận coupon có hoặc không được tạo.

**Nhóm `code`:**

| Lớp | Điều kiện của nhóm | Giá trị/trạng thái đem test | Expected theo đặc tả | Test case | Rule |
| --- | --- | --- | --- | --- | --- |
| P1 | Code mới, duy nhất, hợp lệ | `FR17-DT-01` | Tạo thành công (2xx); danh sách có row với đúng 6 trường | DT-01 | R1, R2 |
| P3 | Code trùng chính xác code đã có | `SAVE10` (seed đã tồn tại) | Từ chối (non-2xx); không có row mới | DT-03 | R2 |
| P4 | Code rỗng | `""` | Từ chối; không có row mới | DT-04 | R2 |
| P5 | Thiếu hẳn key `code` | body không có `code` | Từ chối; không có row mới | DT-05 | R2 |
| P6 | Code chỉ toàn khoảng trắng | `"   "` | Từ chối; không có row mới (ASSUMED) | DT-06 | R2 |
| P7 | Code khác hoa/thường với code đã có | `save10` khi đã có `SAVE10` | Chưa xác định — Quan sát | DT-07 | R2 |

**Nhóm `type`:**

| Lớp | Điều kiện của nhóm | Giá trị/trạng thái đem test | Expected theo đặc tả | Test case | Rule |
| --- | --- | --- | --- | --- | --- |
| P2 | Type hợp lệ `fixed` | `fixed`, discount `50000`, min `200000` | Tạo thành công; row có `type = fixed` | DT-02 | R1, R3 |
| P8 | Type ngoài enum | `percentage` | Từ chối; không có row mới | DT-08 | R3 |
| P9 | Thiếu hẳn key `type` | body không có `type` | Từ chối; không có row mới | DT-09 | R3 |

**Nhóm `discount_value`:**

| Lớp | Điều kiện của nhóm | Giá trị/trạng thái đem test | Expected theo đặc tả | Test case | Rule |
| --- | --- | --- | --- | --- | --- |
| P10 | Discount bằng 0 (biên ON phía invalid) | `0` | Từ chối; không có row mới | DT-10 | R4 |
| P11 | Discount âm (ngay dưới biên 0) | `-1` | Từ chối; không có row mới | DT-11 | R4 |
| P12 | Thiếu hẳn key `discount_value` | body không có `discount_value` | Từ chối; không có row mới | DT-12 | R4 |
| P13 | Discount không phải số | `"abc"` | Từ chối; không có row mới | DT-13 | R4 |
| P14 | Discount dương nhỏ nhất (ngay trên biên 0) | `1` | Tạo thành công; row có `discount_value = 1` | DT-14 | R4 |

**Nhóm `expired_at`:**

| Lớp | Điều kiện của nhóm | Giá trị/trạng thái đem test | Expected theo đặc tả | Test case | Rule |
| --- | --- | --- | --- | --- | --- |
| P15 | Thiếu hẳn key `expired_at` | body không có `expired_at` | Từ chối; không có row mới | DT-15 | R5 |
| P16 | `expired_at` rỗng | `""` | Từ chối; không có row mới | DT-16 | R5 |
| P17 | `expired_at` sai định dạng | `"not-a-date"` | Từ chối; không có row mới (ASSUMED) | DT-17 | R5 |
| P18 | `expired_at` là ngày quá khứ | `"2020-01-01"` | Tạo thành công; row giữ nguyên ngày (ASSUMED) | DT-18 | R5 |

**Nhóm `min_order_amount`:**

| Lớp | Điều kiện của nhóm | Giá trị/trạng thái đem test | Expected theo đặc tả | Test case | Rule |
| --- | --- | --- | --- | --- | --- |
| P19 | Min bằng 0 (biên ON hợp lệ) | `0` | Tạo thành công; row có `min_order_amount = 0` | DT-19 | R6 |
| P20 | Min dương nhỏ nhất (ngay trên biên 0) | `1` | Tạo thành công; row có `min_order_amount = 1` | DT-20 | R6 |
| P21 | Min âm (ngay dưới biên 0) | `-1` | Từ chối; không có row mới | DT-21 | R6 |
| P22 | Thiếu hẳn key `min_order_amount` | body không có `min_order_amount` | Từ chối; không có row mới | DT-22 | R6 |
| P23 | Min không phải số | `"abc"` | Từ chối; không có row mới | DT-23 | R6 |

**Nhóm `max_uses_per_user`:**

| Lớp | Điều kiện của nhóm | Giá trị/trạng thái đem test | Expected theo đặc tả | Test case | Rule |
| --- | --- | --- | --- | --- | --- |
| P24 | Max bằng 1 (biên ON hợp lệ) | `1` | Tạo thành công; row có `max_uses_per_user = 1` | DT-24 | R7 |
| P25 | Max bằng 2 (ngay trên biên 1) | `2` | Tạo thành công; row có `max_uses_per_user = 2` | DT-25 | R7 |
| P26 | Max bằng 0 (ngay dưới biên 1) | `0` | Từ chối; không có row mới | DT-26 | R7 |
| P27 | Max âm | `-1` | Từ chối; không có row mới | DT-27 | R7 |
| P28 | Thiếu hẳn key `max_uses_per_user` | body không có `max_uses_per_user` | Từ chối; không có row mới | DT-28 | R7 |

**Nhóm xem danh sách, xóa và quan sát:**

| Lớp | Điều kiện của nhóm | Giá trị/trạng thái đem test | Expected theo đặc tả | Test case | Rule |
| --- | --- | --- | --- | --- | --- |
| P29 | Xem danh sách sau khi tạo coupon | Tạo `FR17-DT-29` rồi `GET /api/coupons` | Danh sách có 4 seed + coupon mới, đúng trường | DT-29 | R1, R8 |
| P30 | Xóa coupon đang tồn tại | Tạo `FR17-DT-30`, `DELETE` theo id | Xóa thành công (2xx); coupon biến mất khỏi danh sách | DT-30 | R9 |
| P31 | Xóa id không tồn tại | `DELETE /api/admin/coupons/999999` | Chưa xác định — Quan sát | DT-31 | R9 |
| P32 | Percent lớn hơn 100 | `type = percent`, `discount_value = 150` | Chưa xác định — Quan sát (không có upper bound trong FR-17) | DT-32 | R4 |

## Coverage theo mô hình EP

| Nhóm | Lớp EP | T-ID | PASS | FAIL | Quan sát |
| --- | --- | ---: | ---: | ---: | ---: |
| `code` | P1, P3–P7 | 6 | 2 | 3 | 1 |
| `type` | P2, P8, P9 | 3 | 1 | 2 | 0 |
| `discount_value` | P10–P14 | 5 | 1 | 4 | 0 |
| `expired_at` | P15–P18 | 4 | 1 | 3 | 0 |
| `min_order_amount` | P19–P23 | 5 | 2 | 3 | 0 |
| `max_uses_per_user` | P24–P28 | 5 | 2 | 3 | 0 |
| Xem / Xóa | P29–P31 | 3 | 2 | 0 | 1 |
| Quan sát percent | P32 | 1 | 0 | 0 | 1 |
| **Tổng** | **P1–P32** | **32** | **11** | **18** | **3** |

- **EP:** thiết kế 32/32 lớp, đã chạy 32/32; 29 lớp có oracle (11 PASS, 18 FAIL); 3 lớp UNRESOLVED/Quan sát (P7, P31, P32).
- **BVA:** 9 điểm biên thuộc B1–B3 dùng lại 9 T-ID (DT-10, DT-11, DT-14, DT-19, DT-20, DT-21, DT-24, DT-25, DT-26); không có T-ID BVA-only. Chi tiết ở `boundary-analysis.md`.
- **Tổng T-ID duy nhất:** 32; không cộng trùng EP và BVA.
- **Liên kết:** P-ID → T-ID ở bảng trên; T-ID → EV-ID/Actual → verdict ở `test-results.md` và `evidence/`.
