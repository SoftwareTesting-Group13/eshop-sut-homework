# FR10 — Test cases (EP + BVA)

Catalog dùng chung cho Domain/EP và BVA. Mỗi `T-ID` một dòng; ca phục vụ cả hai kỹ thuật vẫn chỉ có một dòng. Tiền tố `DT-` bắt nguồn từ EP/Domain; một số ca đồng thời là điểm biên BVA (ghi trong cột obligation). Trạng thái/`EV-ID` ở `test-results.md`.

**Setup chung cho bộ cốt lõi:** Backend test cách ly (bản sao `server.js`/`database.js` trong thư mục tạm, DB riêng). Mỗi ca tạo một **đơn mới** bằng `POST /api/checkout` với user `test@eshop.com`, rồi đưa về trạng thái nguồn bằng chính API admin `PUT /api/admin/orders/:id/status` (các chuyển đổi hợp lệ). Token admin: `admin@eshop.com`/`Admin123!`; token user: `test@eshop.com`/`Test1234!`. Oracle chung cho ca phải từ chối: **phản hồi lỗi (không 2xx) và trạng thái đơn giữ nguyên**. DT-21–DT-23 có setup riêng bên dưới.

| T-ID | Phương pháp & obligation IDs | Setup + input + thao tác | Expected / oracle |
| --- | --- | --- | --- |
| DT-01 | EP P1; R1 | order `pending`; admin `PUT /api/admin/orders/:id/status` body `{"status":"confirmed"}` | Thành công (2xx); đơn → `confirmed` |
| DT-02 | EP P2; R2 | order `confirmed`; admin body `{"status":"shipping"}` | Thành công; đơn → `shipping` |
| DT-03 | EP P3; BVA B2 tiến vào terminal; R3 | order `shipping`; admin body `{"status":"delivered"}` | Thành công; đơn → `delivered` |
| DT-04 | EP P4; BVA B3 tiến vào terminal; R4 | order `pending`; admin body `{"status":"canceled"}` | Thành công; đơn → `canceled` |
| DT-05 | EP P5; BVA B3 tiến vào terminal; R5 | order `confirmed`; admin body `{"status":"canceled"}` | Thành công; đơn → `canceled` |
| DT-06 | EP P6; BVA B1 ngay dưới biên; R4 | order `pending` (của user); `PUT /api/orders/:id/cancel` bằng token user | Thành công; đơn → `canceled` |
| DT-07 | EP P7; BVA B1 tại biên; R5 | order `confirmed` (của user); user cancel | Thành công; đơn → `canceled` |
| DT-08 | EP P8; R9 | order `pending`; admin body `{"status":"shipping"}` (bỏ qua `confirmed`) | Lỗi; đơn giữ `pending` |
| DT-09 | EP P9; R9 | order `confirmed`; admin body `{"status":"delivered"}` (bỏ qua `shipping`) | Lỗi; đơn giữ `confirmed` |
| DT-10 | EP P10; R9 | order `confirmed`; admin body `{"status":"pending"}` (lùi) | Lỗi; đơn giữ `confirmed` |
| DT-11 | EP P11; R9 | order `shipping`; admin body `{"status":"confirmed"}` (lùi) | Lỗi; đơn giữ `shipping` |
| DT-12 | EP P12; R9 | order `pending`; admin body `{"status":"pending"}` (trùng) | Lỗi; đơn giữ `pending` |
| DT-13 | EP P13; BVA B2 rời terminal; R6 | order `delivered`; admin body `{"status":"shipping"}` | Lỗi; đơn giữ `delivered` |
| DT-14 | EP P14; BVA B3 rời terminal; R7 | order `canceled`; admin body `{"status":"delivered"}` | Lỗi; đơn giữ `canceled` |
| DT-15 | EP P15; R9 | order `pending`; admin body `{"status":"shipped"}` (đích không hợp lệ) | Lỗi; đơn giữ `pending` |
| DT-16 | EP P16; BVA B1 ngay trên biên; R8 | order `shipping` (của user); `PUT /api/orders/:id/cancel` bằng token user | Lỗi; đơn giữ `shipping` |
| DT-17 | EP P17; BVA B1 xa trên biên; R6 | order `delivered` (của user); user cancel | Lỗi; đơn giữ `delivered` |
| DT-18 | EP P18; BVA B1 ngoài chuỗi; R7 | order `canceled` (của user); user cancel | Lỗi; đơn giữ `canceled` |
| DT-19 | EP P19; R9 (ASSUMED) | (a) admin `PUT .../orders/999999/status` body `{"status":"confirmed"}`; (b) `PUT /api/orders/999999/cancel`; (c) admin hủy đơn của user khác | Lỗi; không đổi trạng thái đơn nào |
| DT-20 | EP P20; R8 (ASSUMED — Q1) | order `shipping`; admin body `{"status":"canceled"}` | Lỗi (sơ đồ không có cung shipping→canceled); đơn giữ `shipping` |

### Bổ sung AI-GAP-FR10-01 — miền quyền API Admin (FR-12/FR-18)

Giữ `status=confirmed` và trạng thái nguồn `pending` ở cả ba ca để cô lập actor. DT-01 là đối chứng admin đã có và được chạy lại; không tạo thêm T-ID cho cùng input/Expected. Với actor không đủ quyền, oracle từ FR-12 là **từ chối (không 2xx) và trạng thái đơn không đổi**; mã lỗi cụ thể không được quy định.

| T-ID | Lớp EP bổ sung | Setup + thao tác cụ thể | Expected / oracle | Đường UI thông thường |
| --- | --- | --- | --- | --- |
| DT-21 | A2 — user, đơn của mình | User `test@eshop.com` tạo đơn `pending` qua checkout; gọi `PUT /api/admin/orders/:id/status` bằng **JWT user**, body `{"status":"confirmed"}` | Từ chối; đơn giữ `pending` | API-only: Admin UI từ chối đăng nhập role user; web user không có nút xác nhận đơn. |
| DT-22 | A3 — user, đơn người khác | Admin `admin@eshop.com` tạo đơn `pending`; user `test@eshop.com` gọi cùng endpoint/body với id đơn đó | Từ chối; đơn giữ `pending` | API-only vì cùng role gate/nút thiếu như DT-21. |
| DT-23 | A4 — không token | User tạo đơn `pending`; gọi cùng endpoint/body **không có Authorization** | Từ chối; đơn giữ `pending` | API-only đối với thao tác đổi trạng thái; trình duyệt không trình bày control Admin cho khách chưa đăng nhập. |

Ba ca này dùng cùng API/DB test cách ly; mỗi ca tạo đơn riêng và đọc `GET /api/orders/:id` trước/sau. Không dùng thao tác DevTools làm đường UI. Miền bổ sung có 4 lớp A1–A4 (A1 dùng DT-01), 3 T-ID mới. **Tổng catalog: 23 T-ID duy nhất**; bộ cốt lõi FR-10 bên trên vẫn 20 T-ID, EP P1–P20 và BVA B1–B3 giữ nguyên.

**Ca gộp của bộ cốt lõi:** DT-04/DT-05 gộp lớp EP `P4`/`P5` với điểm BVA B3 "tiến vào terminal canceled"; DT-06/DT-07 gộp `P6`/`P7` với B1 "ngay dưới / tại biên"; DT-03 gộp `P3` với B2 "tiến vào delivered"; DT-13 gộp `P13` với B2 "rời delivered"; DT-14 gộp `P14` với B3 "rời canceled"; DT-16/DT-17/DT-18 gộp `P16`/`P17`/`P18` với các điểm B1. **Bộ cốt lõi có 20 T-ID duy nhất**; ba T-ID bổ sung ở trên được tính riêng vào tổng catalog 23.
