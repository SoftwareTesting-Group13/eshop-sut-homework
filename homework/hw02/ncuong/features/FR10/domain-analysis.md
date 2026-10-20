# FR10 — Domain analysis (EP)

**Feature / interface:** FR-10 Trạng thái Đơn hàng (Order State Machine). Kiểm thử qua **Backend API** — đổi trạng thái bởi admin `PUT /api/admin/orders/:id/status` (body `{"status": ...}`) và hủy đơn bởi user `PUT /api/orders/:id/cancel`; quan sát trạng thái bằng `GET /api/orders/:id`.  
**Phạm vi:** các chuyển đổi trạng thái của đơn hàng và quyền tác nhân trên chuyển đổi hủy. Không kiểm thử FR-11/FR-13/FR-18 (chỉ dùng API admin để tạo fixture trạng thái), không kiểm thử layout/DOM.  
**Nguồn yêu cầu:** `README.md` §5 FR-10; hợp đồng API `api_specification.md` §4.6 (`cancel`) và §6.2 (`/api/admin/orders/:id/status`); quy tắc tác nhân ở FR-18 (`README.md` §6) và FR-20 (`README.md` §7).

## Quy tắc dùng để chia miền

| Rule | Hệ thống phải làm gì? | Điều kiện ảnh hưởng | Nguồn | Tin cậy |
| --- | --- | --- | --- | --- |
| R1 | `pending → confirmed` (admin xác nhận) | đơn đang `pending`, tác nhân admin | README §5 FR-10 (sơ đồ) | CONFIRMED |
| R2 | `confirmed → shipping` (admin giao hàng) | đơn đang `confirmed` | README §5 FR-10 (sơ đồ) | CONFIRMED |
| R3 | `shipping → delivered` (admin hoàn tất) | đơn đang `shipping` | README §5 FR-10 (sơ đồ) | CONFIRMED |
| R4 | `pending → canceled` (User/Admin hủy) | đơn đang `pending` | README §5 FR-10 (sơ đồ) | CONFIRMED |
| R5 | `confirmed → canceled` (User/Admin hủy) | đơn đang `confirmed` | README §5 FR-10 (sơ đồ) | CONFIRMED |
| R6 | `delivered` là trạng thái kết thúc — không chuyển sang bất kỳ trạng thái nào khác | đơn đang `delivered` | README §5 FR-10 (Final States) | CONFIRMED |
| R7 | `canceled` là trạng thái kết thúc — không chuyển sang bất kỳ trạng thái nào khác | đơn đang `canceled` | README §5 FR-10 (Final States) | CONFIRMED |
| R8 | Ở `shipping`, **User không được tự hủy**; chỉ Admin thao tác (theo sơ đồ: `shipping → delivered`) | đơn đang `shipping`, tác nhân user | README §5 FR-10; FR-20 §7 | CONFIRMED (cấm user hủy) |
| R9 | Mọi chuyển đổi **không hợp lệ** phải trả về lỗi với thông báo phù hợp | transition ngoài sơ đồ | README §5 FR-10 | CONFIRMED (có lỗi); mã lỗi/thông báo cụ thể ASSUMED |

**Giả định / điểm chưa rõ ảnh hưởng chia lớp:**

- **A1 (mã lỗi):** đặc tả chỉ yêu cầu "trả về lỗi với thông báo phù hợp", **không** quy định HTTP status hay nội dung. Oracle dùng ở mức "phản hồi là lỗi (không 2xx) và trạng thái đơn không đổi"; SUT trả `400`/`404` — ghi nhận là hành vi quan sát, không phải Expected từ đặc tả.
- **Q1 (biên `shipping → canceled` cho admin):** câu "chỉ Admin mới có thể thao tác" ở `shipping` có thể đọc là admin được hủy đơn đang giao. Sơ đồ FR-10 **không** có cung `shipping → canceled` và yêu cầu "phải tuân theo sơ đồ", nên lớp này chấm **phải bị từ chối** theo sơ đồ — đánh dấu `ASSUMED` (DT-20).
- **Q2 (đơn không tồn tại/không sở hữu):** đặc tả không định nghĩa phản hồi cho đơn không tồn tại; ghi nhận `404` là hành vi quan sát (DT-19).
- **Q3 (quyền gọi API admin):** việc user thường có thể gọi `PUT /api/admin/orders/:id/status` là rủi ro kiểm soát truy cập (FR-12), **không** phải miền dữ liệu của FR-10 ⇒ không tính EP/BVA (xem `../../supporting-materials/fr10-observations.md`).

## Mô hình trạng thái (hỗ trợ, không phải kỹ thuật coverage riêng)

Trạng thái: `S1 pending` (khởi tạo), `S2 confirmed`, `S3 shipping`, `S4 delivered` (kết thúc), `S5 canceled` (kết thúc).

| TR-ID | Từ | Tác nhân / sự kiện | Đến | Hợp lệ |
| --- | --- | --- | --- | --- |
| TR1 | pending | admin xác nhận | confirmed | ALLOWED |
| TR2 | confirmed | admin giao hàng | shipping | ALLOWED |
| TR3 | shipping | admin hoàn tất | delivered | ALLOWED |
| TR4 | pending | user/admin hủy | canceled | ALLOWED |
| TR5 | confirmed | user/admin hủy | canceled | ALLOWED |
| — | delivered | mọi chuyển đi | — | FORBIDDEN (R6) |
| — | canceled | mọi chuyển đi | — | FORBIDDEN (R7) |
| — | shipping | user hủy | — | FORBIDDEN (R8) |

## Các lớp tương đương và ca đại diện

Baseline dùng chung: mỗi ca tạo một **đơn mới** qua `POST /api/checkout` với user `test@eshop.com` rồi đưa về trạng thái nguồn bằng chính API admin (các chuyển đổi hợp lệ R1–R5). Tác nhân admin dùng `admin@eshop.com`, tác nhân user dùng `test@eshop.com`. Oracle chung cho lớp bất hợp lệ: **phản hồi lỗi (không 2xx) và trạng thái đơn giữ nguyên**.

**Dimension đầu vào:** trạng thái nguồn `status` (S1–S5) × trạng thái đích yêu cầu (S1–S5 hoặc giá trị lạ) × tác nhân (admin qua status API / user qua cancel API) × quyền sở hữu đơn.

| Lớp | Điều kiện của nhóm | Giá trị/trạng thái đem test | Expected theo đặc tả | Test case | Rule |
| --- | --- | --- | --- | --- | --- |
| P1 | Hợp lệ, tiến: pending→confirmed, admin | order `pending`; admin `status=confirmed` | Thành công; đơn → `confirmed` | DT-01 | R1 |
| P2 | Hợp lệ, tiến: confirmed→shipping, admin | order `confirmed`; admin `status=shipping` | Thành công; đơn → `shipping` | DT-02 | R2 |
| P3 | Hợp lệ, tiến: shipping→delivered, admin | order `shipping`; admin `status=delivered` | Thành công; đơn → `delivered` | DT-03 | R3 |
| P4 | Hợp lệ, hủy từ `pending`, admin | order `pending`; admin `status=canceled` | Thành công; đơn → `canceled` | DT-04 | R4 |
| P5 | Hợp lệ, hủy từ `confirmed`, admin | order `confirmed`; admin `status=canceled` | Thành công; đơn → `canceled` | DT-05 | R5 |
| P6 | Hợp lệ, hủy từ `pending`, user (đơn của mình) | order `pending`; user `PUT /api/orders/:id/cancel` | Thành công; đơn → `canceled` | DT-06 | R4 |
| P7 | Hợp lệ, hủy từ `confirmed`, user (đơn của mình) | order `confirmed`; user cancel | Thành công; đơn → `canceled` | DT-07 | R5 |
| P8 | Không hợp lệ, bỏ qua trạng thái: pending→shipping | order `pending`; admin `status=shipping` | Lỗi; đơn giữ `pending` | DT-08 | R9 |
| P9 | Không hợp lệ, bỏ qua trạng thái: confirmed→delivered | order `confirmed`; admin `status=delivered` | Lỗi; đơn giữ `confirmed` | DT-09 | R9 |
| P10 | Không hợp lệ, lùi: confirmed→pending | order `confirmed`; admin `status=pending` | Lỗi; đơn giữ `confirmed` | DT-10 | R9 |
| P11 | Không hợp lệ, lùi: shipping→confirmed | order `shipping`; admin `status=confirmed` | Lỗi; đơn giữ `shipping` | DT-11 | R9 |
| P12 | Không hợp lệ, trùng trạng thái: pending→pending | order `pending`; admin `status=pending` | Lỗi; đơn giữ `pending` | DT-12 | R9 |
| P13 | Không hợp lệ, rời terminal `delivered`: delivered→shipping | order `delivered`; admin `status=shipping` | Lỗi; đơn giữ `delivered` | DT-13 | R6, R9 |
| P14 | Không hợp lệ, rời terminal `canceled`: canceled→delivered | order `canceled`; admin `status=delivered` | Lỗi; đơn giữ `canceled` | DT-14 | R7, R9 |
| P15 | Không hợp lệ, status đích không thuộc tập trạng thái | order `pending`; admin `status="shipped"` | Lỗi; đơn giữ `pending` | DT-15 | R9 |
| P16 | Không hợp lệ, user hủy khi `shipping` | order `shipping`; user cancel | Lỗi; đơn giữ `shipping` | DT-16 | R8, R9 |
| P17 | Không hợp lệ, user hủy khi `delivered` | order `delivered`; user cancel | Lỗi; đơn giữ `delivered` | DT-17 | R6, R9 |
| P18 | Không hợp lệ, user hủy khi đã `canceled` | order `canceled`; user cancel | Lỗi; đơn giữ `canceled` | DT-18 | R7, R9 |
| P19 | Đơn không tồn tại / không thuộc người gọi | id `999999`; và đơn của user bị admin hủy | Lỗi; không đổi trạng thái | DT-19 | R9 (ASSUMED) |
| P20 | `shipping→canceled` bởi admin (biên nhập nhằng Q1) | order `shipping`; admin `status=canceled` | Lỗi (theo sơ đồ); đơn giữ `shipping` | DT-20 | R8 (ASSUMED) |

**Tương tác cần kiểm tra:** (a) trạng thái nguồn × trạng thái đích — ma trận `5×5` ở mô hình trạng thái, kiểm tra bằng P1–P14 + P20; (b) tác nhân × trạng thái — `+cancel` bị chặn ở `shipping`/`delivered`/`canceled` (P16–P18) nhưng cho phép ở `pending`/`confirmed` (P6–P7); (c) hai trạng thái kết thúc (P13, P14) phải chặn mọi chuyển đi.

**Lớp gộp, không khả thi hoặc chưa rõ:**

- Các lớp bất hợp lệ cùng nhóm (skip/lùi/trùng/từ terminal) có **cùng** Expected "lỗi + không đổi", nhưng được tách thành nhiều lớp vì chúng là **các chuyển đổi khác nhau** trong ma trận trạng thái cần phủ; mỗi lớp một `T-ID`.
- P19 gộp hai biến thể (đơn không tồn tại và đơn không sở hữu) — cùng Expected "lỗi, không đổi"; chạy chung một ca DT-19.
- P20 đánh dấu `ASSUMED` (Q1); nếu nhóm chốt rằng admin **được** hủy đơn `shipping` thì Expected của P20 đảo chiều và DT-20 phải chấm lại.
- P15 dùng giá trị đích `"shipped"` (không thuộc tập `{pending, confirmed, shipping, delivered, canceled}`) làm đại diện cho "status đích lạ".

## Coverage EP

Mẫu số là các lớp EP đủ điều kiện: **P1–P20 = 20 lớp** (không loại trừ lớp nào; P20 tính dù `ASSUMED`).

| Nghĩa vụ | Khả thi | Có case | Đã chạy có evidence | Đạt oracle | Còn thiếu / chưa rõ |
| --- | ---: | ---: | ---: | ---: | --- |
| Lớp `P1`–`P20` | 20 | 20 | 20 | 18 | `P14` FAIL, `P16` FAIL (evidence ở `test-results.md`); P20 `ASSUMED` |

- **Mẫu số EP:** 20 lớp đủ điều kiện. **Designed 20/20**, **Executed 20/20**, **Passed 18/20**; `P14` và `P16` FAIL.
- FAIL vẫn tính đã chạy. Chi tiết Actual, `EV-ID` và bug ở `test-results.md`.
