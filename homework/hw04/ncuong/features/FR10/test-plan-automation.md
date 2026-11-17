# FR-10 — TEST PLAN tự động hóa HW04 (UI Playwright + hybrid API verify)

> Feature: FR-10 Order state machine. Admin: `http://localhost:5174` (tab Đơn hàng), user: `http://localhost:5173/profile`, API: `http://localhost:3000/api`.
> Nguồn HW02: `homework/hw02/ncuong/features/FR10/test-cases.md` (23 T-ID: DT-01..DT-23).
> Không viết code ở bước này.
> SUT thực tế đã kiểm chứng:
> - `frontend-admin/src/App.jsx:814-861` — pending có `Xác nhận`/`Hủy`, confirmed có `Giao hàng`/`Hủy`, shipping chỉ có `Hoàn thành`; `delivered` không có nút nào.
> - `frontend-admin/src/App.jsx:862-868` — `canceled` có nút `Đánh dấu Đã giao` (chuyển canceled→delivered, **trái spec final-state**).
> - `backend/server.js:537-551` — cho phép `canceled→delivered` (`isValidTransition=true`) → BUG (HW02 DT-14 đã xác nhận).
> - `backend/server.js:328-331` — user cancel chỉ chặn `delivered`/`canceled`, **cho phép `shipping`** → BUG (spec: shipping user không được hủy; HW02 DT-16).
> - `frontend-web/src/pages/Profile.jsx:200` — nút `Hủy đơn` hiện khi `status !== delivered && !== canceled` (gồm cả shipping) → UI phơi bug trên.
> - `backend/server.js:553-556` — transition sai trả 400 `Invalid state transition from X to Y`; `frontend-admin/src/App.jsx:89-92` hiện `alert("Lỗi: ...")`.
> - Badge: `App.jsx:162-171` pending=`Chờ xác nhận`, confirmed=`Đã xác nhận`, shipping=`Đang giao`, delivered=`Đã giao`, canceled=`Đã hủy`.

**Quy ước:** mỗi ca tạo đơn riêng qua `POST /api/checkout` (user `test@eshop.com`), đưa về trạng thái nguồn bằng API admin hợp lệ. Email/order id duy nhất theo run để 3 browser không đụng. Không `waitForTimeout`; dùng auto-wait + `waitForResponse(/\/api\/admin\/orders/)`.

| T-ID (auto) | Loại | Dữ liệu input | Bước thao tác UI | Oracle cụ thể | Chạy được bằng UI không? (Trace HW02) |
| --- | --- | --- | --- | --- | --- |
| A-FR10-01 | Positive | Đơn `pending` (mới checkout) | Admin tab Đơn hàng → hàng `#<id>` bấm `Xác nhận` | Row `#<id>` badge `Đã xác nhận`; `PUT .../status` 200 `{confirmed}`; reload vẫn giữ | Có — thuần UI (DT-01) |
| A-FR10-02 | Positive | Đơn `confirmed` (setup từ pending) | Bấm `Giao hàng` | Badge `Đang giao`; API 200 `{shipping}` | Có (DT-02) |
| A-FR10-03 | Positive | Đơn `shipping` | Bấm `Hoàn thành` | Badge `Đã giao`; API 200 `{delivered}` | Có (DT-03) |
| A-FR10-04 | Positive | Đơn `pending` | Bấm `Hủy` (admin) | Badge `Đã hủy`; API 200 `{canceled}` | Có (DT-04) |
| A-FR10-05 | Positive | Đơn `confirmed` | Bấm `Hủy` (admin) | Badge `Đã hủy`; API 200 | Có (DT-05) |
| A-FR10-06 | Positive | Đơn `pending` của user | User `/profile` bấm `Hủy đơn` → `alert Hủy đơn thành công!` | Row chuyển `Đã hủy`; `PUT /api/orders/:id/cancel` 200 | Có (DT-06) |
| A-FR10-07 | Positive | Đơn `confirmed` của user | Như trên với đơn confirmed | Như trên → `Đã hủy` | Có (DT-07) |
| A-FR10-08 | Negative (bug) | Đơn `canceled` | Admin bấm `Đánh dấu Đã giao` | Spec: phải từ chối, giữ `Đã hủy`. **Actual SUT cho phép → badge `Đã giao`, API 200 → FAIL thành bug** (DT-14) | Có — thuần UI, dự kiến FAIL (DT-14) |
| A-FR10-09 | Negative | Đơn `shipping` | Mở hàng `#<id>`, assert không có nút `Hủy` trong cell Hành động | `getByRole(button,{name:'Hủy'})` count=0 trong row; chỉ có `Hoàn thành` | Có — assert absence (DT-20 chặn shipping→canceled admin) |
| A-FR10-10 | Negative | Đơn `delivered` | Mở hàng `#<id>` | Không có nút hành động nào trong row; user `/profile` không có `Hủy đơn` | Có — assert absence (DT-13/DT-17) |
| A-FR10-11 | Edge | Đơn `shipping_address=""` | Mở tab Đơn hàng, đọc cell Địa chỉ | Cell hiện `Chưa cập nhật` (`App.jsx:802`), không crash | Có |
| A-FR10-12 | Edge | Đơn `total_amount=0` | Đọc cell Tổng tiền | Hiện `0 ₫` (`Number(0).toLocaleString()`), không crash | Có |
| A-FR10-13 | Negative | Đơn `pending` → `{"status":"shipping"}` (nhảy cóc) | Không có nút UI → gọi `PUT /api/admin/orders/:id/status` bằng token admin (API assertion trong cùng spec) | 400 `Invalid state transition from pending to shipping`; `GET /api/orders/:id` vẫn `pending` | Không thuần UI (không render nút) — tự động hóa bằng API (DT-08) |
| A-FR10-14 | Negative | Đơn `confirmed` → `{"status":"delivered"}` + `confirmed→pending` + `pending→pending` + `{"status":"shipped"}` | Như trên, 4 sub-assert API | Mỗi lần 400 + trạng thái giữ nguyên | Không thuần UI — API (DT-09/DT-10/DT-12/DT-15) |
| A-FR10-15 | Negative | Đơn `shipping` + `delivered` + `canceled`, user `PUT /:id/cancel` | API assertion: (a) shipping user cancel, (b) delivered user cancel, (c) canceled user cancel | Spec: cả 3 phải 400 + giữ nguyên. **Actual (a) shipping succeeds 200 → FAIL thành bug**; (b)(c) 400 đúng | Không thuần UI cho (b)(c) (nút ẩn); (a) có nút UI nhưng assert qua API cho chắc (DT-16/DT-17/DT-18) |
| A-FR10-16 | Negative | Đơn `pending`, actor A2/A3/A4 | API assertion: user JWT gọi admin endpoint / đơn người khác / không token | 401/403 + giữ `pending` (FR-12) | Không — web user không có control admin (DT-21/DT-22/DT-23) |

**Tổng: 16 ca (7 P / 6 N / 3 E). Chạy được thuần UI: 12 ca (01–12) ≥ 12 theo đề. API assertion trong spec: 4 ca (13–16, phủ DT-08..DT-23).**
**3 assertion pattern FR-10:** (D) bảng/row `getByRole('row',{name:/#id/}).toContainText('Đã giao')`, (G) không tồn tại `toHaveCount(0)`, (E) API response `waitForResponse` + status 200/400.
