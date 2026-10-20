# FR17 — Boundary analysis (BVA)

**Feature / interface:** FR-17 — Quản lý Mã Giảm Giá (Coupon CRUD); API `POST /api/admin/coupons` là interface chính cho các biên số.  
**Nguồn yêu cầu:** `README.md` §5 FR-17.

BVA chỉ áp dụng cho các ngưỡng số học có trong FR-17: `min_order_amount >= 0`, `max_uses_per_user >= 1`, `discount_value > 0`. Các trường phân loại (`code`, `type`) và `expired_at` không có ngưỡng số/độ dài trong FR-17 nên không tạo điểm biên.

## B1 — `min_order_amount >= 0`

**Rule:** R6 — `min_order_amount` là trường bắt buộc, là số `>= 0`.  
**Biên:** `0`, dấu bằng thuộc phía hợp lệ; đơn vị VND; bước nguyên `1`.  
**Setup chung:** DB test mới seed 4 coupon; đăng nhập `admin@eshop.com`; các trường khác giữ baseline (`code` duy nhất, `type = percent`, `discount_value = 10`, `expired_at = 2099-12-31`, `max_uses_per_user = 1`). Mỗi ca lấy `GET /api/coupons` trước/sau để xác nhận coupon có/không được tạo.

| Điểm | Giá trị/trạng thái cần tạo | Expected | Test case | Khả năng thử |
| --- | --- | --- | --- | --- |
| Ngay dưới | `min_order_amount = -1` | Từ chối (non-2xx); không có row mới | DT-21 | Khả thi — UI không có `min` nên nhập được `-1` |
| Tại biên | `min_order_amount = 0` | Tạo thành công (2xx); row có `min_order_amount = 0` | DT-19 | Khả thi — UI cho phép `0` |
| Ngay trên | `min_order_amount = 1` | Tạo thành công (2xx); row có `min_order_amount = 1` | DT-20 | Khả thi — UI cho phép `1` |

**Ghi chú precision:** `min_order_amount` là số tiền VND; đặc tả không nói đến phần thập phân. `-1` là giá trị nguyên gần nhất ngay dưới biên 0; không dùng `-0.5` vì đơn vị/độ chính xác chưa được đặc tả.

## B2 — `max_uses_per_user >= 1`

**Rule:** R7 — `max_uses_per_user` là trường bắt buộc, là số nguyên `>= 1`.  
**Biên:** `1`, dấu bằng thuộc phía hợp lệ; đơn vị: số lần/người; bước nguyên `1`.  
**Setup chung:** như B1; chỉ đổi `max_uses_per_user`.

| Điểm | Giá trị/trạng thái cần tạo | Expected | Test case | Khả năng thử |
| --- | --- | --- | --- | --- |
| Ngay dưới | `max_uses_per_user = 0` | Từ chối (non-2xx); không có row mới | DT-26 | API khả thi; UI có `min="1"` nên chặn submit `0` |
| Tại biên | `max_uses_per_user = 1` | Tạo thành công (2xx); row có `max_uses_per_user = 1` | DT-24 | Khả thi — UI cho phép `1` |
| Ngay trên | `max_uses_per_user = 2` | Tạo thành công (2xx); row có `max_uses_per_user = 2` | DT-25 | Khả thi — UI cho phép `2` |

**Ghi chú precision:** đặc tả không nói rõ số thập phân; vì đây là số lần sử dụng, mô hình dùng số nguyên. Không tạo điểm `1.5` để tránh tự đặt quy tắc mới.

## B3 — `discount_value > 0`

**Rule:** R4 — `discount_value` là trường bắt buộc, phải là số dương.  
**Biên:** `0`, dấu bằng **không** thuộc phía hợp lệ (`> 0`); đơn vị: `%` nếu `type = percent`, VND nếu `type = fixed`; bước nguyên `1`.  
**Setup chung:** như B1; chỉ đổi `discount_value`, giữ `type = percent` cho cả 3 điểm để so sánh cùng đơn vị.

| Điểm | Giá trị/trạng thái cần tạo | Expected | Test case | Khả năng thử |
| --- | --- | --- | --- | --- |
| Ngay dưới | `discount_value = -1` | Từ chối (non-2xx); không có row mới | DT-11 | Khả thi — UI không có `min` nên nhập được `-1` |
| Tại biên | `discount_value = 0` | Từ chối (non-2xx); không có row mới | DT-10 | Khả thi — UI cho phép `0` |
| Ngay trên | `discount_value = 1` | Tạo thành công (2xx); row có `discount_value = 1` | DT-14 | Khả thi — UI cho phép `1` |

**Ghi chú:** FR-17 không đặt upper bound cho `discount_value` khi `type = percent`; vì vậy `100` không phải biên của đặc tả và không được thêm vào BVA. Giá trị `150` được ghi nhận riêng như quan sát DT-32, không chấm PASS/FAIL.

## Vì sao các trường khác không có BVA

- **`expired_at`:** FR-17 chỉ yêu cầu trường này và một ngày hợp lệ; không quy định phải ở tương lai hay một khoảng thời gian. Ngày quá khứ `2020-01-01` được kiểm tra như lớp hợp lệ ASSUMED (DT-18). Biên thời gian "current date before expired_at" thuộc FR-09 (C2) và nằm ngoài phạm vi.
- **`code`:** không có độ dài tối thiểu/tối đa hoặc định dạng trong FR-17; chỉ có uniqueness và bắt buộc → EP.
- **`type`:** miền phân loại `percent/fixed` → EP, không có thứ tự số.
- **`max_uses_per_user`:** đã có biên 1; không có upper bound.
- **Xóa theo `id`:** không có khoảng giá trị id trong đặc tả; id không tồn tại là quan sát DT-31.

## Coverage BVA

| Biên | Điểm | T-ID | Kết quả |
| --- | ---: | --- | --- |
| B1 — `min_order_amount >= 0` | 3 | DT-21, DT-19, DT-20 | 2/3 đạt oracle (DT-19, DT-20); DT-21 FAIL |
| B2 — `max_uses_per_user >= 1` | 3 | DT-26, DT-24, DT-25 | 2/3 đạt oracle (DT-24, DT-25); DT-26 FAIL |
| B3 — `discount_value > 0` | 3 | DT-11, DT-10, DT-14 | 1/3 đạt oracle (DT-14); DT-11, DT-10 FAIL |
| **Tổng** | **9** | **9 T-ID duy nhất** | **5 PASS, 4 FAIL, 0 Quan sát** |

- **Thiết kế:** 9/9 điểm biên; **đã chạy:** 9/9.
- **Đạt oracle:** 5/9; **không đạt:** 4/9; **UNRESOLVED:** 0.
- **T-ID BVA-only:** 0 — cả 9 điểm đều dùng lại ca EP tương ứng, nên tổng T-ID duy nhất của feature vẫn là 32, không cộng trùng EP/BVA.
- **Liên kết:** B-ID → T-ID ở bảng trên; Actual/EV-ID ở `test-results.md` và `evidence/`.
