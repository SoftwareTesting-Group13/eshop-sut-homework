# FR17 — Test cases (EP + BVA)

Thiết kế ca từ lớp tương đương trong `domain-analysis.md` và điểm biên trong `boundary-analysis.md`. Mỗi `T-ID` chỉ có một dòng trong catalog; một ca có thể phủ cả EP và BVA. Kết quả quan sát và `EV-ID` nằm trong `test-results.md`.

**Baseline cho ca tạo coupon:** `code` duy nhất, `type = percent`, `discount_value = 10`, `min_order_amount = 100000`, `expired_at = 2099-12-31`, `max_uses_per_user = 1`; chỉ đổi trường đang kiểm tra. API dùng JSON number cho các trường số; UI nhập cùng giá trị nhưng trình duyệt gửi chuỗi, backend/SQLite chuyển đổi.

## Catalog T-ID

| T-ID | Phương pháp & obligation IDs | Setup + input + thao tác | Expected / oracle |
| --- | --- | --- | --- |
| DT-01 | EP; P1, R1–R7 | Tạo coupon `FR17-DT-01`, percent, 10, min 100000, expiry 2099-12-31, max 1 | 2xx; `GET /api/coupons` có row đúng 6 trường |
| DT-02 | EP; P2, R1–R7 | Tạo `FR17-DT-02`, fixed, 50000, min 200000 | 2xx; row `type = fixed`, đúng 6 trường |
| DT-03 | EP; P3, R2 | Tạo code trùng `SAVE10` (seed đã có) | Non-2xx; không có row mới |
| DT-04 | EP; P4, R2 | `code = ""` | Non-2xx; không có row mới |
| DT-05 | EP; P5, R2 | Bỏ hẳn key `code` | Non-2xx; không có row mới |
| DT-06 | EP; P6, R2 | `code = "   "` | Non-2xx; không có row mới (ASSUMED) |
| DT-07 | EP; P7, R2 | `code = "save10"` khi đã có `SAVE10` | Chưa xác định — Quan sát uniqueness hoa/thường |
| DT-08 | EP; P8, R3 | `type = "percentage"` | Non-2xx; không có row mới |
| DT-09 | EP; P9, R3 | Bỏ hẳn key `type` | Non-2xx; không có row mới |
| DT-10 | EP + BVA; P10, B3-ON, R4 | `discount_value = 0` | Non-2xx; không có row mới |
| DT-11 | EP + BVA; P11, B3-below, R4 | `discount_value = -1` | Non-2xx; không có row mới |
| DT-12 | EP; P12, R4 | Bỏ hẳn key `discount_value` | Non-2xx; không có row mới |
| DT-13 | EP; P13, R4 | `discount_value = "abc"` | Non-2xx; không có row mới |
| DT-14 | EP + BVA; P14, B3-above, R4 | `discount_value = 1` | 2xx; row `discount_value = 1` |
| DT-15 | EP; P15, R5 | Bỏ hẳn key `expired_at` | Non-2xx; không có row mới |
| DT-16 | EP; P16, R5 | `expired_at = ""` | Non-2xx; không có row mới |
| DT-17 | EP; P17, R5 | `expired_at = "not-a-date"` | Non-2xx; không có row mới (ASSUMED format) |
| DT-18 | EP; P18, R5 | `expired_at = "2020-01-01"` | 2xx; row giữ nguyên ngày (ASSUMED cho phép quá khứ) |
| DT-19 | EP + BVA; P19, B1-ON, R6 | `min_order_amount = 0` | 2xx; row `min_order_amount = 0` |
| DT-20 | EP + BVA; P20, B1-above, R6 | `min_order_amount = 1` | 2xx; row `min_order_amount = 1` |
| DT-21 | EP + BVA; P21, B1-below, R6 | `min_order_amount = -1` | Non-2xx; không có row mới |
| DT-22 | EP; P22, R6 | Bỏ hẳn key `min_order_amount` | Non-2xx; không có row mới |
| DT-23 | EP; P23, R6 | `min_order_amount = "abc"` | Non-2xx; không có row mới |
| DT-24 | EP + BVA; P24, B2-ON, R7 | `max_uses_per_user = 1` | 2xx; row `max_uses_per_user = 1` |
| DT-25 | EP + BVA; P25, B2-above, R7 | `max_uses_per_user = 2` | 2xx; row `max_uses_per_user = 2` |
| DT-26 | EP + BVA; P26, B2-below, R7 | `max_uses_per_user = 0` | Non-2xx; không có row mới |
| DT-27 | EP; P27, R7 | `max_uses_per_user = -1` | Non-2xx; không có row mới |
| DT-28 | EP; P28, R7 | Bỏ hẳn key `max_uses_per_user` | Non-2xx; không có row mới |
| DT-29 | EP; P29, R1, R8 | Tạo `FR17-DT-29` rồi `GET /api/coupons` | 2xx; danh sách có 4 seed + row mới, đúng trường |
| DT-30 | EP; P30, R9 | Tạo `FR17-DT-30`, `DELETE` theo id, rồi `GET` | 2xx; coupon biến mất khỏi danh sách |
| DT-31 | EP; P31 | `DELETE /api/admin/coupons/999999` | Chưa xác định — Quan sát |
| DT-32 | EP; P32, R4 | `type = percent`, `discount_value = 150` | Chưa xác định — Quan sát (không có upper bound) |

## Đường chạy API và thao tác UI thủ công

> **Trạng thái UI:** toàn bộ hướng dẫn UI dưới đây là **Dự kiến — chưa kiểm chứng UI**. Không có Actual UI nào được ghi; verdict trong `test-results.md` là của đường API đã chạy thật.

### Setup UI chung

1. Chạy backend SUT cách ly tại `http://localhost:3000` và admin app tại `http://localhost:5174` (nếu chưa chạy: `cd frontend-admin && npm run dev`).
2. Mở `http://localhost:5174`, đăng nhập `admin@eshop.com` / `Admin123!`.
3. Chọn tab **Mã Giảm Giá**. Form **Tạo mã giảm giá mới** có các ô theo thứ tự: **Mã coupon**, **Loại**, **Giá trị**, **Đơn tối thiểu**, **Ngày hết hạn**, **Số lần dùng tối đa/người**; nút **Tạo mã**. Bảng bên dưới có các cột **Mã**, **Loại**, **Giá trị**, **Đơn tối thiểu**, **Hết hạn**, **Giới hạn/người**, **Hành động** (nút **Xóa**).
4. Trước mỗi ca, đảm bảo DB test chỉ có 4 seed `SAVE10`, `BIGBUY`, `VIP100`, `EXPIRED` (khởi động lại SUT cách ly để reset). Sau mỗi ca, xóa coupon vừa tạo bằng nút **Xóa** ở đúng row; nếu không thấy row, ghi lại hiện tượng.
5. Khi kiểm tra Actual: nhìn row mới trong bảng, alert `Lỗi: ...`, hoặc tooltip validation của trình duyệt. Chụp screenshot toàn màn hình (thấy URL, tab, row/alert) cho bug ứng viên.

### Nhóm `code`

#### DT-01

- **API:** `POST /api/admin/coupons` — `{"code":"FR17-DT-01","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}`.
- **UI thông thường:** Khả thi.
- **Manual UI:** tab Mã Giảm Giá → Mã=`FR17-DT-01`, Loại=`Phần trăm (%)`, Giá trị=`10`, Đơn tối thiểu=`100000`, Ngày hết hạn=`2099-12-31`, Số lần=`1` → click **Tạo mã** → Expected: row `FR17-DT-01` xuất hiện đúng các cột; screenshot bảng.
- **Reset:** click **Xóa** ở row `FR17-DT-01`.

#### DT-02

- **API:** `POST /api/admin/coupons` — `{"code":"FR17-DT-02","type":"fixed","discount_value":50000,"min_order_amount":200000,"expired_at":"2099-12-31","max_uses_per_user":1}`.
- **UI thông thường:** Khả thi.
- **Manual UI:** Mã=`FR17-DT-02`, Loại=`Số tiền cố định (₫)`, Giá trị=`50000`, Đơn tối thiểu=`200000`, Ngày hết hạn=`2099-12-31`, Số lần=`1` → **Tạo mã** → Expected: row loại `Cố định`, giá trị `50,000 ₫`.
- **Reset:** **Xóa** row `FR17-DT-02`.

#### DT-03

- **API:** `POST /api/admin/coupons` — body hợp lệ nhưng `code = "SAVE10"`.
- **UI thông thường:** Khả thi — nhập `SAVE10` (UI tự uppercase) và submit.
- **Manual UI:** Mã=`SAVE10`, các trường còn lại baseline → **Tạo mã** → Expected: không có row mới; UI hiện alert `Lỗi: ...` (hiện tại dự kiến alert chứa lỗi SQLite). Ghi lại nguyên văn alert; screenshot.
- **Reset:** không có row mới để xóa.

#### DT-04

- **API:** `POST /api/admin/coupons` — `code = ""`.
- **UI thông thường:** Không cùng input-state — ô Mã có `required`, trình duyệt chặn submit chuỗi rỗng; ca API-only.
- **Manual UI:** không có đường UI thông thường cho chuỗi rỗng. Không ghi Actual UI.

#### DT-05

- **API:** `POST /api/admin/coupons` — body **không có** key `code`.
- **UI thông thường:** Không cùng input-state — form luôn gửi key `code` và `required` chặn rỗng; ca API-only.
- **Manual UI:** không có đường UI thông thường. Không ghi Actual UI.

#### DT-06

- **API:** `POST /api/admin/coupons` — `code = "   "`.
- **UI thông thường:** Khả thi — `required` coi ba khoảng trắng là có giá trị.
- **Manual UI:** Mã=ba khoảng trắng, các trường còn lại baseline → **Tạo mã** → Expected: không có row mới (ASSUMED); nếu row có mã trắng xuất hiện, chụp screenshot row đó.
- **Reset:** nếu có row, **Xóa** row vừa tạo.

#### DT-07

- **API:** `POST /api/admin/coupons` — `code = "save10"` khi DB có `SAVE10`.
- **UI thông thường:** Không cùng input-state — UI tự `toUpperCase()`, không gửi được `save10`; ca API-only.
- **Manual UI:** không có đường UI thông thường. Đây là quan sát, không có Expected PASS/FAIL.

### Nhóm `type`

#### DT-08

- **API:** `POST /api/admin/coupons` — `type = "percentage"`.
- **UI thông thường:** Không cùng input-state — Loại là select chỉ có `percent`/`fixed`; ca API-only.
- **Manual UI:** không có đường UI thông thường.

#### DT-09

- **API:** `POST /api/admin/coupons` — body **không có** key `type`.
- **UI thông thường:** Không cùng input-state — select luôn có giá trị; ca API-only.
- **Manual UI:** không có đường UI thông thường.

### Nhóm `discount_value`

#### DT-10

- **API:** `POST /api/admin/coupons` — `discount_value = 0`.
- **UI thông thường:** Khả thi — ô Giá trị là `type="number"` không có `min`.
- **Manual UI:** Giá trị=`0`, các trường còn lại baseline → **Tạo mã** → Expected: không có row mới; nếu row `0%` xuất hiện, chụp screenshot.
- **Reset:** **Xóa** row nếu có.

#### DT-11

- **API:** `POST /api/admin/coupons` — `discount_value = -1`.
- **UI thông thường:** Khả thi — ô number không có `min`.
- **Manual UI:** Giá trị=`-1` → **Tạo mã** → Expected: không có row mới; nếu row `-1%` xuất hiện, chụp screenshot.
- **Reset:** **Xóa** row nếu có.

#### DT-12

- **API:** `POST /api/admin/coupons` — body **không có** key `discount_value`.
- **UI thông thường:** Không cùng input-state — ô Giá trị có `required`, ca API-only.
- **Manual UI:** không có đường UI thông thường.

#### DT-13

- **API:** `POST /api/admin/coupons` — `discount_value = "abc"`.
- **UI thông thường:** Không cùng input-state — `type="number"` không gửi được `abc`; ca API-only.
- **Manual UI:** không có đường UI thông thường.

#### DT-14

- **API:** `POST /api/admin/coupons` — `discount_value = 1`.
- **UI thông thường:** Khả thi.
- **Manual UI:** Giá trị=`1` → **Tạo mã** → Expected: row `FR17-DT-14` với `1%`.
- **Reset:** **Xóa** row `FR17-DT-14`.

### Nhóm `expired_at`

#### DT-15

- **API:** `POST /api/admin/coupons` — body **không có** key `expired_at`.
- **UI thông thường:** Không cùng input-state — ô Ngày hết hạn có `required`; ca API-only.
- **Manual UI:** không có đường UI thông thường.

#### DT-16

- **API:** `POST /api/admin/coupons` — `expired_at = ""`.
- **UI thông thường:** Không cùng input-state — `required` chặn rỗng; ca API-only.
- **Manual UI:** không có đường UI thông thường.

#### DT-17

- **API:** `POST /api/admin/coupons` — `expired_at = "not-a-date"`.
- **UI thông thường:** Không cùng input-state — `type="date"` không gửi được chuỗi này; ca API-only.
- **Manual UI:** không có đường UI thông thường.

#### DT-18

- **API:** `POST /api/admin/coupons` — `expired_at = "2020-01-01"`.
- **UI thông thường:** Khả thi — date input cho chọn ngày quá khứ.
- **Manual UI:** Ngày hết hạn=`2020-01-01` → **Tạo mã** → Expected (ASSUMED): row xuất hiện, cột Hết hạn hiển thị `Hết hạn` (đỏ).
- **Reset:** **Xóa** row `FR17-DT-18`.

### Nhóm `min_order_amount`

#### DT-19

- **API:** `POST /api/admin/coupons` — `min_order_amount = 0`.
- **UI thông thường:** Khả thi.
- **Manual UI:** Đơn tối thiểu=`0` → **Tạo mã** → Expected: row `FR17-DT-19`, cột Đơn tối thiểu `0 ₫`.
- **Reset:** **Xóa** row `FR17-DT-19`.

#### DT-20

- **API:** `POST /api/admin/coupons` — `min_order_amount = 1`.
- **UI thông thường:** Khả thi.
- **Manual UI:** Đơn tối thiểu=`1` → **Tạo mã** → Expected: row `FR17-DT-20`, cột Đơn tối thiểu `1 ₫`.
- **Reset:** **Xóa** row `FR17-DT-20`.

#### DT-21

- **API:** `POST /api/admin/coupons` — `min_order_amount = -1`.
- **UI thông thường:** Khả thi — ô number không có `min`.
- **Manual UI:** Đơn tối thiểu=`-1` → **Tạo mã** → Expected: không có row mới; nếu row có `-1 ₫` xuất hiện, chụp screenshot.
- **Reset:** **Xóa** row nếu có.

#### DT-22

- **API:** `POST /api/admin/coupons` — body **không có** key `min_order_amount`.
- **UI thông thường:** Không cùng input-state — UI luôn gửi key này; nếu người dùng xóa trắng, UI gửi `""` (khác với bỏ hẳn key). Ca API-only cho input "omitted".
- **Manual UI:** không dùng ô trống để tái hiện ca này; nếu muốn thử UI empty-string, ghi thành quan sát riêng, không gán cho DT-22.

#### DT-23

- **API:** `POST /api/admin/coupons` — `min_order_amount = "abc"`.
- **UI thông thường:** Không cùng input-state — `type="number"` không gửi được `abc`; ca API-only.
- **Manual UI:** không có đường UI thông thường.

### Nhóm `max_uses_per_user`

#### DT-24

- **API:** `POST /api/admin/coupons` — `max_uses_per_user = 1`.
- **UI thông thường:** Khả thi.
- **Manual UI:** Số lần=`1` → **Tạo mã** → Expected: row `FR17-DT-24`, cột Giới hạn/người `1 lần`.
- **Reset:** **Xóa** row `FR17-DT-24`.

#### DT-25

- **API:** `POST /api/admin/coupons` — `max_uses_per_user = 2`.
- **UI thông thường:** Khả thi.
- **Manual UI:** Số lần=`2` → **Tạo mã** → Expected: row `FR17-DT-25`, cột Giới hạn/người `2 lần`.
- **Reset:** **Xóa** row `FR17-DT-25`.

#### DT-26

- **API:** `POST /api/admin/coupons` — `max_uses_per_user = 0`.
- **UI thông thường:** Không cùng input-state — ô number có `min="1"`, trình duyệt chặn submit `0`; ca API-only.
- **Manual UI:** không có đường UI thông thường. Ghi chú: nếu bỏ trống ô này, UI gửi `""` và backend dùng `|| 1`; đó là input khác, không gán cho DT-26.

#### DT-27

- **API:** `POST /api/admin/coupons` — `max_uses_per_user = -1`.
- **UI thông thường:** Không cùng input-state — `min="1"` chặn `-1`; ca API-only.
- **Manual UI:** không có đường UI thông thường.

#### DT-28

- **API:** `POST /api/admin/coupons` — body **không có** key `max_uses_per_user`.
- **UI thông thường:** Không cùng input-state — UI luôn gửi key này; bỏ trống gửi `""`, không phải bỏ hẳn key. Ca API-only.
- **Manual UI:** không dùng ô trống để tái hiện ca này; ghi thành quan sát riêng nếu thử.

### Nhóm xem danh sách, xóa và quan sát

#### DT-29

- **API:** `POST /api/admin/coupons` tạo `FR17-DT-29`, sau đó `GET /api/coupons` với admin token.
- **UI thông thường:** Khả thi — bảng Mã Giảm Giá chính là đường xem.
- **Manual UI:** sau khi tạo `FR17-DT-29`, quan sát bảng: phải thấy 4 seed + row mới, đúng Mã/Loại/Giá trị/Đơn tối thiểu/Hết hạn/Giới hạn. Chụp screenshot bảng.
- **Reset:** **Xóa** row `FR17-DT-29`.

#### DT-30

- **API:** `POST /api/admin/coupons` tạo `FR17-DT-30`, `DELETE /api/admin/coupons/:id`, rồi `GET /api/coupons`.
- **UI thông thường:** Khả thi — nút **Xóa** ở cột Hành động.
- **Manual UI:** tạo `FR17-DT-30` → click **Xóa** ở đúng row → Expected: row biến mất, không còn mã `FR17-DT-30`; chụp screenshot trước/sau.
- **Reset:** row đã bị xóa bởi chính ca test.

#### DT-31

- **API:** `DELETE /api/admin/coupons/999999`.
- **UI thông thường:** Không có đường UI thông thường để xóa một id không tồn tại (UI chỉ xóa row đang có); ca API-only.
- **Manual UI:** không có. Đây là quan sát, không có Expected PASS/FAIL.

#### DT-32

- **API:** `POST /api/admin/coupons` — `type = "percent"`, `discount_value = 150`.
- **UI thông thường:** Khả thi — ô Giá trị không có `max`.
- **Manual UI:** Loại=`Phần trăm (%)`, Giá trị=`150` → **Tạo mã** → Quan sát: row `150%` có xuất hiện không; ghi nhận, không chấm PASS/FAIL vì FR-17 không có upper bound.
- **Reset:** **Xóa** row nếu có.

## Ghi chú về UI và phạm vi

- UI được đọc từ `frontend-admin/src/App.jsx` (form coupon, bảng, nút xóa) để lập đường manual; **chưa chạy UI** trong phiên này.
- Các ca API-only không phải là bug UI; chúng chỉ ra rằng UI chuẩn không gửi được cùng input-state (do `required`, `select`, `type="number"`, `min="1"` hoặc tự uppercase).
- Không kiểm tra layout, DOM hay UI Validation như một bộ ca riêng; UI chỉ là phương tiện chạy cùng EP/BVA khi khả thi.
