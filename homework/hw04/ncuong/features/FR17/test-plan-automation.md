# FR-17 — TEST PLAN tự động hóa HW04 (UI Playwright + hybrid API verify)

> Feature: FR-17 Coupon management. Admin: `http://localhost:5174` tab Mã Giảm Giá, API: `http://localhost:3000/api`.
> Nguồn HW02: `homework/hw02/ncuong/features/FR17/test-cases.md` (32 T-ID: DT-01..DT-32).
> Không viết code ở bước này.
> SUT thực tế đã kiểm chứng:
> - Form `frontend-admin/src/App.jsx:636-714`: Mã `placeholder="Mã coupon (VD: SAVE10)"` + `required` + auto `toUpperCase()` (`:644`); Loại select chỉ `percent/fixed` (`:649-658`); Giá trị `type=number` + `required`, không `min/max` (`:659-675`); Đơn tối thiểu `type=number`, không `min` (`:676-687`); Ngày hết hạn `type=date` + `required` (`:688-697`); Số lần `type=number` + `min="1"` (`:698-710`); nút `Tạo mã` (`:712`).
> - Bảng `:716-773`: cột Mã/Loại/Giá trị/Đơn tối thiểu/Hết hạn/Giới hạn/Hành động (nút `Xóa` `:754-768`); giá trị percent `N%` / fixed `N ₫` (`:737-741`); quá hạn hiện `Hết hạn` đỏ (`:746-750`).
> - Lỗi tạo: `alert("Lỗi: ...")` (`:630`); bảng không thêm row là oracle chính khi validate fail.
> - Backend `server.js:457-481`: `INSERT` trực tiếp, **không validate** (chỉ DB `code TEXT UNIQUE` — `database.js:31`); trùng mã → 500 SQLite; `max_uses_per_user || 1` nên input `0` bị biến thành `1`.
> - `database.js:29-38`: coupons không có `CHECK` → `discount 0/-1/150`, `min -1`, `type` lạ, `expired` lạ đều INSERT được → các ca spec-expect-reject sẽ FAIL thành bug.

**Quy ước:** code duy nhất theo run (`FR17-<TID>-<ts>`), trừ ca trùng seed `SAVE10`. Setup: login admin `admin@eshop.com/Admin123!`. Verify hybrid: đếm row bảng + `GET /api/coupons`. Không `waitForTimeout`.

| T-ID (auto) | Loại | Dữ liệu input | Bước thao tác UI | Oracle cụ thể | Chạy được bằng UI không? (Trace HW02) |
| --- | --- | --- | --- | --- | --- |
| A-FR17-01 | Positive | `code=FR17-01-<ts>`, percent, 10, min 100000, exp 2099-12-31, max 1 | Tab Mã Giảm Giá → điền 6 ô → `Tạo mã` | Row mới đúng Mã/Phần trăm/`10%`/`100,000 ₫`/2099-12-31/`1 lần`; `POST` 2xx | Có (DT-01) |
| A-FR17-02 | Positive | `FR17-02-<ts>`, fixed, 50000, min 200000 | Như trên, Loại=`Cố định` | Row `Cố định`/`50,000 ₫`; 2xx | Có (DT-02) |
| A-FR17-03 | Negative | `code=SAVE10` (trùng seed), còn lại baseline | Nhập `SAVE10` → `Tạo mã` | `alert Lỗi: ...` (500 UNIQUE); **không** thêm row (đếm row trước/sau bằng nhau + `GET /api/coupons` không có id mới) | Có (DT-03) |
| A-FR17-04 | Edge | `code="   "` (3 space) | Nhập 3 space → `Tạo mã` (`required` cho qua) | Spec ASSUMED: không tạo row. Actual SUT INSERT được → nếu row trắng xuất hiện thì FAIL thành bug quan sát | Có (DT-06) |
| A-FR17-05 | Negative-bug | `discount_value=0` | Giá trị=`0` → `Tạo mã` | Spec: reject, không row. **Actual backend INSERT → row `0%` xuất hiện → FAIL thành bug** | Có (DT-10) |
| A-FR17-06 | Negative-bug | `discount_value=-1` | Giá trị=`-1` → `Tạo mã` | Như trên → row `-1%` → FAIL thành bug | Có (DT-11) |
| A-FR17-07 | Positive | `discount_value=1` | Giá trị=`1` → `Tạo mã` | Row `1%`; 2xx | Có (DT-14) |
| A-FR17-08 | Negative-bug | `type=percent`, `discount_value=150` | Loại `%`, Giá trị=`150` (không `max`) → `Tạo mã` | Spec: reject (>100). **Actual INSERT → row `150%` → FAIL thành bug** | Có (DT-32) |
| A-FR17-09 | Positive | `expired_at=2020-01-01` | Ngày=`2020-01-01` → `Tạo mã` | Row tạo được, cột Hết hạn hiện `Hết hạn` đỏ (ASSUMED cho phép quá khứ) | Có (DT-18) |
| A-FR17-10 | Positive | `min_order_amount=0` | Đơn tối thiểu=`0` → `Tạo mã` | Row `0 ₫`; 2xx | Có (DT-19) |
| A-FR17-11 | Positive | `min_order_amount=1` | Đơn tối thiểu=`1` → `Tạo mã` | Row `1 ₫` | Có (DT-20) |
| A-FR17-12 | Negative-bug | `min_order_amount=-1` | Đơn tối thiểu=`-1` → `Tạo mã` | Spec: reject. **Actual INSERT → row `-1 ₫` → FAIL thành bug** | Có (DT-21) |
| A-FR17-13 | Positive | `max_uses_per_user=2` | Số lần=`2` → `Tạo mã` | Row `2 lần` | Có (DT-25) |
| A-FR17-14 | Positive | Tạo `FR17-29-<ts>` rồi đọc bảng | Tạo xong, không xóa, đọc bảng | Bảng có 4 seed + row mới đúng 6 cột | Có (DT-29) |
| A-FR17-15 | Positive | Tạo `FR17-30-<ts>` rồi bấm `Xóa` ở đúng row | Tạo → `Xóa` → confirm | Row biến mất; `GET /api/coupons` không còn code đó | Có (DT-30) |
| A-FR17-16 | Negative | Body thiếu key `code` | Không form được (`required` + luôn gửi key) → `POST /api/admin/coupons` API | Non-2xx (hoặc 500 NOT NULL); không row mới | Không — API-only (DT-05) |
| A-FR17-17 | Negative | `code=save10` (thường, DB có `SAVE10`) | Không form được (UI `toUpperCase`) → API | Spec: reject (unique case-insensitive). **Actual SQLite UNIQUE phân biệt hoa/thường → INSERT 2xx → FAIL thành bug** | Không — API-only (DT-07) |
| A-FR17-18 | Negative | `type=percentage` / `discount=abc` / `expired=not-a-date` / `max=0` (4 sub-assert API) | Không form được (select/number/date/min=1 chặn) → API | Spec: non-2xx hết. Actual: backend INSERT cả 4 (lưu ý `max 0 → 1` do `\|\| 1`) → FAIL thành bug nếu ra 2xx | Không — API-only (DT-08/DT-13/DT-17/DT-26) |

**Tổng: 18 ca (8 P / 7 N / 3 E). Chạy được thuần UI: 15 ca (01–15) ≥ 12 theo đề. API-only: 3 ca (16–18, phủ DT-05/07/08/13/17/26).**
**3 assertion pattern FR-17:** (D) bảng/row `getByRole('row',{name:/FR17-..}).toContainText(...)`, (F) count `row.count()` trước/sau, (E) API `waitForResponse(/\/api\/admin\/coupons/)` status + `GET /api/coupons` chứa/không chứa code.
