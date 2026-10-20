# FR10 — Boundary analysis (BVA)

**Feature / interface:** FR-10 Trạng thái Đơn hàng — **Backend API** `PUT /api/admin/orders/:id/status` (admin) và `PUT /api/orders/:id/cancel` (user); quan sát bằng `GET /api/orders/:id`.  
**Nguồn yêu cầu:** `README.md` §5 FR-10 (sơ đồ chuyển đổi, Final States, quy tắc tác nhân khi `shipping`); `api_specification.md` §4.6, §6.2.  
**Đơn vị / độ chính xác:** biên nằm trên **chuỗi trạng thái có thứ tự** `pending (0) → confirmed (1) → shipping (2) → delivered (3)`; bước nhảy = **1 trạng thái kế tiếp trong vòng đời**. `canceled` là trạng thái **ngoài chuỗi** (nhánh kết thúc). Không có ngưỡng số học nên **không** dùng `±1` số; biên ở đây là biên thứ tự/trạng thái kết thúc.

## B1 — Ranh giới quyền hủy đơn của User theo vị trí vòng đời

**Rule:** R4/R5 (hủy được từ `pending`/`confirmed`) và R8 (User **không** tự hủy được ở `shipping`).  
**Biên:** vùng hủy được `IN = {pending, confirmed}` (vị trí ≤ 1) so với `OUT = {shipping, delivered}` (vị trí ≥ 2); `canceled` là OUT nhưng nằm ngoài chuỗi. Biên nằm giữa `confirmed` (điểm cuối còn hủy được) và `shipping` (điểm đầu không hủy được).  
**Setup chung:** đơn của user `test@eshop.com`, đưa về trạng thái nguồn bằng API admin (R1–R3); gọi `PUT /api/orders/:id/cancel` bằng token user.

| Điểm | Giá trị/trạng thái cần tạo | Expected | Test case | Khả năng thử |
| --- | --- | --- | --- | --- |
| Ngay dưới biên (vị trí 0) | `pending` | Hủy thành công; đơn → `canceled` | DT-06 | Khả thi |
| Tại biên — điểm cuối còn hủy được (vị trí 1) | `confirmed` | Hủy thành công; đơn → `canceled` | DT-07 | Khả thi |
| Ngay trên biên — điểm đầu không hủy được (vị trí 2) | `shipping` | **Từ chối**; đơn giữ `shipping` | DT-16 | Khả thi |
| Xa trên biên (vị trí 3) | `delivered` | Từ chối; đơn giữ `delivered` | DT-17 | Khả thi |
| Ngoài chuỗi | `canceled` | Từ chối; đơn giữ `canceled` | DT-18 | Khả thi |

*Ghi chú:* "ngay trên biên" là `shipping` — theo R8 đây là điểm **đầu tiên** quyền hủy của user bị chặn, nên là điểm biên quyết định của B1; đây cũng là nơi phát hiện `BUG-FR10-02`.

## B2 — Biên hấp thụ của trạng thái kết thúc `delivered`

**Rule:** R3 (được phép `shipping → delivered`) và R6 (`delivered` là trạng thái kết thúc).  
**Biên:** `delivered` là trạng thái hấp thụ (absorbing): **tiến vào** được từ `shipping`, **rời ra** bị cấm với mọi đích.  
**Setup chung:** đơn được đưa tới `shipping`/`delivered` bằng API admin.

| Điểm | Giá trị/trạng thái cần tạo | Expected | Test case | Khả năng thử |
| --- | --- | --- | --- | --- |
| Tại biên — tiến vào (shipping→delivered) | order `shipping`; admin `status=delivered` | Thành công; đơn → `delivered` | DT-03 | Khả thi |
| Rời biên — ngay trên (delivered→shipping) | order `delivered`; admin `status=shipping` | Từ chối; đơn giữ `delivered` | DT-13 | Khả thi |

*Ghi chú:* mọi đích khác từ `delivered` (pending/confirmed/canceled) cùng lớp "rời biên bị cấm"; DT-13 chọn `shipping` làm đại diện (đích "gần" nhất). Hủy khi `delivered` (DT-17) cũng là một lần rời biên bị cấm.

## B3 — Biên hấp thụ của trạng thái kết thúc `canceled`

**Rule:** R4/R5 (được phép `pending/confirmed → canceled`) và R7 (`canceled` là trạng thái kết thúc).  
**Biên:** `canceled` là trạng thái hấp thụ: **tiến vào** từ `pending`/`confirmed`, **rời ra** bị cấm với mọi đích.  
**Setup chung:** đơn được đưa tới `canceled` bằng API admin hoặc API hủy của user.

| Điểm | Giá trị/trạng thái cần tạo | Expected | Test case | Khả năng thử |
| --- | --- | --- | --- | --- |
| Tại biên — tiến vào (pending→canceled, confirmed→canceled) | order `pending` / `confirmed` | Thành công; đơn → `canceled` | DT-04, DT-05 | Khả thi |
| Rời biên — ngay trên (canceled→delivered) | order `canceled`; admin `status=delivered` | Từ chối; đơn giữ `canceled` | DT-14 | Khả thi |

*Ghi chú:* đích `delivered` là đích "nguy hiểm" nhất khi rời `canceled` (đưa đơn đã hủy vào luồng tính doanh thu FR-13); SUT cho phép chuyển này ⇒ `BUG-FR10-01`.

## Coverage BVA

Mẫu số là các điểm biên đủ điều kiện: B1 có 5 điểm, B2 có 2 điểm, B3 có 2 điểm = **9 điểm**.

| Nghĩa vụ biên | Khả thi | Có case | Đã chạy đúng điểm có evidence | Đạt oracle | Còn thiếu / không quan sát được |
| --- | ---: | ---: | ---: | ---: | --- |
| B1 ngay dưới / tại biên | 2 | 2 | 2 | 2 | — |
| B1 ngay trên biên (shipping) | 1 | 1 | 1 | 0 | FAIL (BUG-FR10-02) |
| B1 xa trên / ngoài chuỗi | 2 | 2 | 2 | 2 | — |
| B2 tiến vào / rời `delivered` | 2 | 2 | 2 | 2 | — |
| B3 tiến vào / rời `canceled` | 2 | 2 | 2 | 1 | B3 rời FAIL (BUG-FR10-01) |

- **Mẫu số BVA:** 9 điểm đủ điều kiện. **Designed 9/9**, **Executed 9/9**, **Passed 7/9**; 2 điểm FAIL có evidence.
- Các điểm B1/B2/B3 trùng `T-ID` với lớp EP (`DT-04…DT-07`, `DT-13`, `DT-14`, `DT-16`, `DT-17`) nên **không cộng thêm** case: một ca phục vụ cả EP và BVA chỉ tính một lần trong catalog. Chi tiết Actual và bug ở `test-results.md`.
