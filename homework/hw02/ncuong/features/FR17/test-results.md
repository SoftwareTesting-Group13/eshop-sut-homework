# FR17 — Test results

- **Run được chọn để tổng hợp:** `run-20261020-fr17`.
- **Build/commit SUT:** repo `eshop-sut-homework`, commit `f389502cdb308b133fe9044e34505f19202dd887` (backend `server.js` SHA-256 `47573ce5…`, `database.js` SHA-256 `33664206…`).
- **Môi trường:** macOS (darwin), Node v26.9.0; backend Node/Express + SQLite; instance cách ly trong thư mục tạm (`server.js`/`database.js`/`package.json` là bản sao, `database.sqlite` riêng, `node_modules` symlink). Thời điểm chạy: `2026-10-20 22:38:26 +0700` → `2026-10-20 22:38:27 +0700` (= `2026-10-20T15:38:26Z` → `15:38:27Z`).
- **Interface đã chạy:** API `POST /api/admin/coupons`, `GET /api/coupons`, `DELETE /api/admin/coupons/:id` với admin token. UI admin chỉ chuẩn bị đường manual; **UI không dùng làm bằng chứng**, không có verdict UI.
- **Reset trạng thái:** DB test mới seed 4 coupon (`SAVE10`, `BIGBUY`, `VIP100`, `EXPIRED`); mỗi ca lấy snapshot `GET /api/coupons` trước/sau và xóa coupon do ca tạo. DB làm việc `backend/database.sqlite` giữ nguyên SHA-256 `c63f0054…` trước và sau run.
- **Source code:** không sửa `backend/` hoặc `frontend-admin/`; backend `server.js` SHA-256 `47573ce5…`, `database.js` SHA-256 `33664206…`. Các thay đổi có sẵn của người dùng ở `prompt.txt`/`skills/` không thuộc phiên này và không bị chỉnh sửa.
- **Chi tiết thô:** `evidence/FR17-evidence.md` + `evidence/DT-*.log`, `evidence/run-summary.json`, `evidence/session-header.log`, driver `evidence/run-fr17.mjs`.
- **Screenshot API:** 39 ảnh Postman do người kiểm thử cung cấp tại `screenshots/`; 19/20 FAIL có ảnh, `DT-06` chưa có ảnh; bổ sung **1 ảnh UI** áp dụng coupon `150%` cho `BUG-FR17-08` (chỉ minh họa hệ quả, không thay bằng chứng API).

## Kết quả theo run

| T-ID | Interface | Actual (API) | Status | Oracle | UI manual | EV-ID / evidence | Bug ID |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DT-01 | API POST | 200; row id 5: percent, 10, min 100000, expiry 2099-12-31, max 1 | PASS | CONFIRMED | CHƯA CHẠY — khả thi | EV-FR17-001 (`DT-01.log`) | — |
| DT-02 | API POST | 200; row id 6: fixed, 50000, min 200000, expiry 2099-12-31, max 1 | PASS | CONFIRMED | CHƯA CHẠY — khả thi | EV-FR17-002 (`DT-02.log`) | — |
| DT-03 | API POST | 500 `SQLITE_CONSTRAINT: UNIQUE constraint failed: coupons.code`; 0 row mới | PASS | CONFIRMED | CHƯA CHẠY — khả thi | EV-FR17-003 (`DT-03.log`) | — (xem OBS-FR17-01) |
| DT-04 | API POST | 200 `Coupon created`; row mới `code=""` | FAIL | CONFIRMED | CHƯA CHẠY — API-only (`required`) | EV-FR17-004 (`DT-04.log`) | BUG-FR17-01 |
| DT-05 | API POST | 200 `Coupon created`; row mới `code=NULL` | FAIL | CONFIRMED | CHƯA CHẠY — API-only (không có key) | EV-FR17-005 (`DT-05.log`) | BUG-FR17-01 |
| DT-06 | API POST | 200 `Coupon created`; row mới `code="   "` | FAIL | ASSUMED | CHƯA CHẠY — khả thi | EV-FR17-006 (`DT-06.log`) | BUG-FR17-01 |
| DT-07 | API POST | 200; row mới `code="save10"` bên cạnh `SAVE10` | FAIL | CONFIRMED (quy tắc uniqueness không phân biệt hoa/thường, người kiểm thử xác nhận 2026-10-21) | CHƯA CHẠY — API-only (UI uppercase) | EV-FR17-007 (`DT-07.log`) | BUG-FR17-07 |
| DT-08 | API POST | 200; row mới `type="percentage"` | FAIL | CONFIRMED | CHƯA CHẠY — API-only (select) | EV-FR17-008 (`DT-08.log`) | BUG-FR17-02 |
| DT-09 | API POST | 200; row mới `type=NULL` | FAIL | CONFIRMED | CHƯA CHẠY — API-only (select) | EV-FR17-009 (`DT-09.log`) | BUG-FR17-02 |
| DT-10 | API POST | 200; row mới `discount_value=0` | FAIL | CONFIRMED | CHƯA CHẠY — khả thi | EV-FR17-010 (`DT-10.log`) | BUG-FR17-03 |
| DT-11 | API POST | 200; row mới `discount_value=-1` | FAIL | CONFIRMED | CHƯA CHẠY — khả thi | EV-FR17-011 (`DT-11.log`) | BUG-FR17-03 |
| DT-12 | API POST | 200; row mới `discount_value=NULL` | FAIL | CONFIRMED | CHƯA CHẠY — API-only (`required`) | EV-FR17-012 (`DT-12.log`) | BUG-FR17-03 |
| DT-13 | API POST | 200; row mới `discount_value="abc"` (typeof text) | FAIL | CONFIRMED | CHƯA CHẠY — API-only (`type=number`) | EV-FR17-013 (`DT-13.log`) | BUG-FR17-03 |
| DT-14 | API POST | 200; row mới `discount_value=1` | PASS | CONFIRMED | CHƯA CHẠY — khả thi | EV-FR17-014 (`DT-14.log`) | — |
| DT-15 | API POST | 200; row mới `expired_at=NULL` | FAIL | CONFIRMED | CHƯA CHẠY — API-only (`required`) | EV-FR17-015 (`DT-15.log`) | BUG-FR17-04 |
| DT-16 | API POST | 200; row mới `expired_at=""` | FAIL | CONFIRMED | CHƯA CHẠY — API-only (`required`) | EV-FR17-016 (`DT-16.log`) | BUG-FR17-04 |
| DT-17 | API POST | 200; row mới `expired_at="not-a-date"` | FAIL | ASSUMED | CHƯA CHẠY — API-only (`type=date`) | EV-FR17-017 (`DT-17.log`) | BUG-FR17-04 |
| DT-18 | API POST | 200; row mới `expired_at="2020-01-01"` | PASS | ASSUMED | CHƯA CHẠY — khả thi | EV-FR17-018 (`DT-18.log`) | — |
| DT-19 | API POST | 200; row mới `min_order_amount=0` | PASS | CONFIRMED | CHƯA CHẠY — khả thi | EV-FR17-019 (`DT-19.log`) | — |
| DT-20 | API POST | 200; row mới `min_order_amount=1` | PASS | CONFIRMED | CHƯA CHẠY — khả thi | EV-FR17-020 (`DT-20.log`) | — |
| DT-21 | API POST | 200; row mới `min_order_amount=-1` | FAIL | CONFIRMED | CHƯA CHẠY — khả thi | EV-FR17-021 (`DT-21.log`) | BUG-FR17-05 |
| DT-22 | API POST | 200; row mới `min_order_amount=NULL` | FAIL | CONFIRMED | CHƯA CHẠY — API-only (không có key) | EV-FR17-022 (`DT-22.log`) | BUG-FR17-05 |
| DT-23 | API POST | 200; row mới `min_order_amount="abc"` | FAIL | CONFIRMED | CHƯA CHẠY — API-only (`type=number`) | EV-FR17-023 (`DT-23.log`) | BUG-FR17-05 |
| DT-24 | API POST | 200; row mới `max_uses_per_user=1` | PASS | CONFIRMED | CHƯA CHẠY — khả thi | EV-FR17-024 (`DT-24.log`) | — |
| DT-25 | API POST | 200; row mới `max_uses_per_user=2` | PASS | CONFIRMED | CHƯA CHẠY — khả thi | EV-FR17-025 (`DT-25.log`) | — |
| DT-26 | API POST | 200; input `0` nhưng row lưu `max_uses_per_user=1` | FAIL | CONFIRMED | CHƯA CHẠY — API-only (`min="1"`) | EV-FR17-026 (`DT-26.log`) | BUG-FR17-06 |
| DT-27 | API POST | 200; row mới `max_uses_per_user=-1` | FAIL | CONFIRMED | CHƯA CHẠY — API-only (`min="1"`) | EV-FR17-027 (`DT-27.log`) | BUG-FR17-06 |
| DT-28 | API POST | 200; thiếu key, row lưu `max_uses_per_user=1` | FAIL | CONFIRMED | CHƯA CHẠY — API-only (không có key) | EV-FR17-028 (`DT-28.log`) | BUG-FR17-06 |
| DT-29 | API GET | 200; list 5 rows: 4 seed + `FR17-DT-29`, đúng trường | PASS | CONFIRMED | CHƯA CHẠY — khả thi | EV-FR17-029 (`DT-29.log`) | — |
| DT-30 | API DELETE | POST tạo 200; DELETE 200 `Coupon deleted`; list còn 4 row, coupon biến mất | PASS | CONFIRMED | CHƯA CHẠY — khả thi | EV-FR17-030 (`DT-30.log`) | — |
| DT-31 | API DELETE | 200 `Coupon deleted` cho id 999999; list vẫn 4 row | Quan sát | UNRESOLVED | CHƯA CHẠY — API-only | EV-FR17-031 (`DT-31.log`) | — (OBS-FR17-02) |
| DT-32 | API POST | 200; row mới `type=percent`, `discount_value=150` | FAIL | CONFIRMED (percent tối đa 100, người kiểm thử xác nhận 2026-10-21) | CHƯA CHẠY — khả thi | EV-FR17-032 (`DT-32.log`) | BUG-FR17-08 |

**Ghi chú DT-03:** R2 (code duy nhất) được enforce — coupon trùng không được tạo, nên verdict PASS theo oracle "non-2xx + không tạo row". Tuy nhiên API trả **500** kèm chuỗi lỗi SQLite thay vì một lỗi validation; đặc tả FR-17 không quy định status/message, nên đây là **quan sát** OBS-FR17-01, không phải FAIL của R2.

**Ghi chú UI:** 16 T-ID có đường UI thông thường (DT-01, 02, 03, 06, 10, 11, 14, 18, 19, 20, 21, 24, 25, 29, 30, 32); 16 T-ID còn lại API-only vì UI `required`, `select`, `type="number"`, `min="1"` hoặc tự uppercase. **Không có UI nào được chạy trong run này**; cột UI chỉ ghi trạng thái `CHƯA CHẠY`, không lấy verdict API gán cho UI. Hướng dẫn manual ở `test-cases.md`.

## Tổng hợp case duy nhất

| Phạm vi | Thiết kế | Đã chạy | PASS | FAIL | Quan sát | BLOCKED | Chưa chạy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Tất cả T-ID duy nhất** | **32** | **32** | **11** | **20** | **1** | **0** | **0** |

Đã chạy = PASS + FAIL + Quan sát = 11 + 20 + 1 = 32; Thiết kế = Đã chạy + BLOCKED + Chưa chạy = 32.

- **Theo kỹ thuật (có thể chồng lấp, không cộng thành tổng):** EP 32 lớp (`P1`–`P32`) trên 32 T-ID; BVA 9 điểm biên (B1 3, B2 3, B3 3) dùng lại 9 T-ID, không có T-ID BVA-only.
- **Theo oracle:** CONFIRMED 28 T-ID; ASSUMED 3 T-ID (DT-06, DT-17, DT-18); UNRESOLVED 1 T-ID (DT-31).
- **Đạt oracle theo nghĩa vụ:** EP 31 lớp có oracle → 11 PASS, 20 FAIL; BVA 9 điểm → 5 PASS, 4 FAIL.
- **UI:** 32/32 T-ID có hướng dẫn manual; 0/32 đã chạy UI; UI không được cộng vào verdict/coverage API.

## Bug report

### Bảng tổng hợp

| Bug ID | Feature | Title | Severity | Priority | Related TC | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BUG-FR17-01 | FR17 | Backend nhận `code` rỗng/thiếu/chỉ khoảng trắng khi tạo coupon | Medium | Medium | DT-04, DT-05, DT-06 | **Đã xác nhận API** (ảnh Postman); Issue [#47](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/47) | `DT-04.log`, `DT-05.log`, `DT-06.log` |
| BUG-FR17-02 | FR17 | Backend nhận `type` ngoài `percent/fixed` hoặc thiếu `type` | Medium | Medium | DT-08, DT-09 | **Đã xác nhận API** (ảnh Postman); Issue [#48](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/48) | `DT-08.log`, `DT-09.log` |
| BUG-FR17-03 | FR17 | Backend nhận `discount_value` `<= 0`, không phải số hoặc thiếu | High | High | DT-10, DT-11, DT-12, DT-13 | **Đã xác nhận API** (ảnh Postman); Issue [#49](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/49) | `DT-10.log`…`DT-13.log` |
| BUG-FR17-04 | FR17 | Backend nhận `expired_at` thiếu/rỗng/sai định dạng | High | High | DT-15, DT-16, DT-17 | **Đã xác nhận API** (ảnh Postman); Issue [#50](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/50) | `DT-15.log`…`DT-17.log` |
| BUG-FR17-05 | FR17 | Backend nhận `min_order_amount` âm, không phải số hoặc thiếu | Medium | Medium | DT-21, DT-22, DT-23 | **Đã xác nhận API** (ảnh Postman); Issue [#51](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/51) | `DT-21.log`…`DT-23.log` |
| BUG-FR17-06 | FR17 | Backend nhận `max_uses_per_user < 1` hoặc thiếu; number `0` bị đổi thành `1` | Medium | Medium | DT-26, DT-27, DT-28 | **Đã xác nhận API** (ảnh Postman); Issue [#52](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/52) | `DT-26.log`…`DT-28.log` |
| BUG-FR17-07 | FR17 | Backend nhận `code` khác hoa/thường khi đã có mã tương ứng (`save10` bên cạnh `SAVE10`) | Medium | Medium | DT-07 | **Đã xác nhận API** (ảnh Postman); Issue [#53](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/53) | `DT-07.log` + 3 ảnh |
| BUG-FR17-08 | FR17 | Backend nhận `discount_value = 150` cho coupon `percent` (vượt 100%) | High | High | DT-32 | **Đã xác nhận API** (ảnh Postman); Issue [#54](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54) | `DT-32.log` + 2 ảnh Postman + 1 ảnh UI |

### Tiêu chí phân loại

| Severity | Tiêu chí |
| --- | --- |
| **Critical** | Lộ/mất dữ liệu nhạy cảm hoặc lỗi bảo mật nghiêm trọng. |
| **High** | Luồng cốt lõi hoặc business rule quan trọng sai, ảnh hưởng lớn tới người dùng/tiền. |
| **Medium** | Quy tắc/validation sai với ảnh hưởng giới hạn hơn High. |
| **Low** | Sai lệch hiển thị/nội dung nhỏ, ít ảnh hưởng đến việc hoàn thành tác vụ. |

Priority là mức ưu tiên xử lý, đánh giá riêng theo mức ảnh hưởng và tính cấp bách.

### Chi tiết (manual reproduction)

> **Môi trường chung:** commit `f389502cdb308b133fe9044e34505f19202dd887`; backend Node/Express + SQLite; base URL `http://localhost:3000`; DB test cách ly seed 4 coupon. Evidence gồm **API đã chạy thật**; UI mới là hướng dẫn `Dự kiến — chưa kiểm chứng UI`. Lấy token admin:
>
> ```zsh
> curl -s -X POST http://localhost:3000/api/login \
>   -H 'Content-Type: application/json' \
>   -d '{"email":"admin@eshop.com","password":"Admin123!"}'
> ```
>
> Dùng `token` trong response làm `<ADMIN_TOKEN>` cho các lệnh dưới đây.

#### BUG-FR17-01 — Backend nhận `code` rỗng/thiếu/chỉ khoảng trắng

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-17 — Coupon CRUD; R2 `code` bắt buộc và duy nhất (`README.md` §5 FR-17) |
| Test case | DT-04 (rỗng), DT-05 (thiếu key), DT-06 (ba khoảng trắng — ASSUMED) |
| Build / môi trường | `f389502…`; API `POST /api/admin/coupons`; DB test cách ly |
| Severity / Priority | Medium / Medium — coupon không có mã có nghĩa, gây rác danh sách; nhiều NULL có thể cùng tồn tại vì SQLite UNIQUE cho phép nhiều NULL; mã rỗng/khoảng trắng vẫn có thể khớp nếu gửi đúng chuỗi qua API |
| Trạng thái / lặp lại | **Đã xác nhận qua API** (ảnh Postman); đã tái hiện 1/1 run API cho cả 3 input |

**Chuẩn bị:** DB test có 4 seed; đăng nhập admin; các trường còn lại baseline (`type=percent`, `discount_value=10`, `min_order_amount=100000`, `expired_at=2099-12-31`, `max_uses_per_user=1`).

**Các bước (API đã chạy):**

```zsh
# DT-04: code rỗng
curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

# DT-05: bỏ hẳn key code
curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

# DT-06: ba khoảng trắng
curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"   ","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'
```

**Expected:** non-2xx và `GET /api/coupons` không có row mới.  
**Actual:** cả ba trả `200 {"message":"Coupon created",...}`; `GET` có row mới với `code=""`, `code=NULL`, `code="   "` tương ứng.  
**UI (Dự kiến — chưa kiểm chứng UI):** DT-04/DT-05 không đi được qua UI vì ô Mã có `required`; DT-06 có thể đi được: nhập ba khoảng trắng vào ô **Mã coupon**, điền các trường còn lại, click **Tạo mã**, kiểm tra bảng có row mã trắng; không dùng ảnh UI làm bằng chứng.
**Evidence:** `DT-04.log`, `DT-05.log`, `DT-06.log`.  
**Screenshot API:** [01-CodeEmpty](screenshots/BUG-FR17-01-CodeEmpty.png), [01-GetCodeEmpty](screenshots/BUG-FR17-01-GetCodeEmpty.png), [01-MissingCode](screenshots/BUG-FR17-01-MissingCode.png), [01-CodeNull](screenshots/BUG-FR17-01-CodeNull.png); `DT-06` chưa có ảnh.
**Root cause (đọc source):** `backend/server.js:457-481` không kiểm tra `code`/trim trước khi `INSERT`; DB `code TEXT UNIQUE` (`backend/database.js:29-38`) chỉ bắt trùng, không bắt rỗng/NULL.

#### BUG-FR17-02 — Backend nhận `type` ngoài enum hoặc thiếu `type`

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-17 — R3 `type` bắt buộc, chỉ `percent`/`fixed` |
| Test case | DT-08 (`percentage`), DT-09 (thiếu key) |
| Build / môi trường | `f389502…`; API `POST /api/admin/coupons` |
| Severity / Priority | Medium / Medium — type sai làm coupon bị hiểu sai loại giảm giá ở FR-09; API-only nên ảnh hưởng người dùng thường thấp hơn |
| Trạng thái / lặp lại | **Đã xác nhận qua API** (ảnh Postman); 1/1 run API cho cả 2 input |

**Chuẩn bị:** như BUG-FR17-01; chỉ đổi `type`.

**Các bước (API đã chạy):**

```zsh
curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-08","type":"percentage","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-09","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'
```

**Expected:** non-2xx; không có row mới.  
**Actual:** cả hai 200; row mới lưu `type="percentage"` và `type=NULL`.  
**UI (Dự kiến — chưa kiểm chứng UI):** không có đường UI thông thường — **Loại** là select chỉ có `Phần trăm (%)` và `Số tiền cố định (₫)`; giữ API-only.  
**Evidence:** `DT-08.log`, `DT-09.log`.  
**Screenshot API:** [02-TypeInvalid](screenshots/BUG-FR17-02-TypeInvalid.png), [02-GetCodeHasTypeInvalid](screenshots/BUG-FR17-02-GetCodeHasTypeInvalid.png), [02-MissingType](screenshots/BUG-FR17-02-MissingType.png), [02-GetNullType](screenshots/BUG-FR17-02-GetNullType.png).
**Root cause:** `backend/server.js:457-481` không kiểm tra enum/bắt buộc; `backend/database.js:32` chỉ có `DEFAULT 'percent'`, không có `CHECK` hay `NOT NULL`. Hệ quả nguồn FR-09: `coupon.type === "percent"` sai thì rơi vào nhánh fixed (`server.js:398-404`).

#### BUG-FR17-03 — Backend nhận `discount_value <= 0`, không phải số hoặc thiếu

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-17 — R4 `discount_value` bắt buộc, là số dương (`> 0`) |
| Test case | DT-10 (`0`), DT-11 (`-1`), DT-12 (thiếu), DT-13 (`"abc"`) |
| Build / môi trường | `f389502…`; API `POST /api/admin/coupons` |
| Severity / Priority | High / High — đây là giá trị tiền/% cốt lõi; 0/âm/không phải số có thể làm giảm giá sai, tăng tổng tiền hoặc tạo `NaN` khi áp dụng |
| Trạng thái / lặp lại | **Đã xác nhận qua API** (ảnh Postman); 1/1 run API cho cả 4 input |

**Chuẩn bị:** như BUG-FR17-01; chỉ đổi `discount_value`.

**Các bước (API đã chạy):**

```zsh
# DT-10: 0
curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-10","type":"percent","discount_value":0,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

# DT-11: -1
curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-11","type":"percent","discount_value":-1,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

# DT-12: bỏ hẳn key discount_value
curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-12","type":"percent","min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

# DT-13: "abc"
curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-13","type":"percent","discount_value":"abc","min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'
```

**Expected:** non-2xx; không có row mới.  
**Actual:** cả bốn 200; row mới lưu `0`, `-1`, `NULL`, `"abc"` (typeof text).  
**UI (Dự kiến — chưa kiểm chứng UI):** DT-10/DT-11 đi được — ô **Giá trị** là `type="number"` không có `min`, nhập `0`/`-1` rồi **Tạo mã**, kiểm tra bảng có row `0%`/`-1%`; không dùng ảnh UI làm bằng chứng. DT-12/DT-13 không đi được vì `required`/`type=number` → API-only.
**Evidence:** `DT-10.log`…`DT-13.log`.  
**Screenshot API:** [03-DiscountValue0](screenshots/BUG-FR17-03-DiscountValue0.png), [03-GetDiscountValue0](screenshots/BUG-FR17-03-GetDiscountValue0.png), [03-DiscountValueNegative](screenshots/BUG-FR17-03-DiscountValueNegative.png), [03-GetDiscountNegative](screenshots/BUG-FR17-03-GetDiscountNegative.png), [03-MissingDiscountValue](screenshots/BUG-FR17-03-MissingDiscountValue.png), [03-GetMissingDiscountValue](screenshots/BUG-FR17-03-GetMissingDiscountValue.png), [03-DiscountValueInvalid](screenshots/BUG-FR17-03-DiscountValueInvalid.png), [03-GetDiscountValueInvalid](screenshots/BUG-FR17-03-GetDiscountValueInvalid.png).
**Root cause:** `backend/server.js:457-481` không kiểm tra kiểu/số dương; cột `discount_value INTEGER` không có `CHECK` (`backend/database.js:33`). Hệ quả nguồn FR-09: percent `total * (1 - discount_value)` (`server.js:398-401`) với số âm/không phải số cho kết quả sai/`NaN`; fixed lấy nguyên `discount_value` (`server.js:402-404`).

#### BUG-FR17-04 — Backend nhận `expired_at` thiếu/rỗng/sai định dạng

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-17 — R5 `expired_at` bắt buộc, là ngày hợp lệ |
| Test case | DT-15 (thiếu), DT-16 (rỗng), DT-17 (`not-a-date` — ASSUMED format) |
| Build / môi trường | `f389502…`; API `POST /api/admin/coupons` |
| Severity / Priority | High / High — ngày sai/không parse được có thể làm coupon không bao giờ hết hạn hoặc không dùng được; ảnh hưởng trực tiếp điều kiện C2 của FR-09 |
| Trạng thái / lặp lại | **Đã xác nhận qua API** (ảnh Postman); 1/1 run API cho cả 3 input |

**Chuẩn bị:** như BUG-FR17-01; chỉ đổi `expired_at`.

**Các bước (API đã chạy):**

```zsh
# DT-15: bỏ hẳn key expired_at
curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-15","type":"percent","discount_value":10,"min_order_amount":100000,"max_uses_per_user":1}'

# DT-16: rỗng
curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-16","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"","max_uses_per_user":1}'

# DT-17: not-a-date
curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-17","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"not-a-date","max_uses_per_user":1}'
```

**Expected:** non-2xx; không có row mới.  
**Actual:** cả ba 200; row mới lưu `NULL`, `""`, `"not-a-date"`.  
**UI (Dự kiến — chưa kiểm chứng UI):** không có đường UI thông thường — ô **Ngày hết hạn** có `required` và `type="date"`; giữ API-only.  
**Evidence:** `DT-15.log`…`DT-17.log`.  
**Screenshot API:** [04-MissingExpiredAt](screenshots/BUG-FR17-04-MissingExpiredAt.png), [04-GetMissingExpiredAt](screenshots/BUG-FR17-04-GetMissingExpiredAt.png), [04-EmptyExpiredAt](screenshots/BUG-FR17-04-EmptyExpiredAt.png), [04-GetEmptyExpiredAt](screenshots/BUG-FR17-04-GetEmptyExpiredAt.png), [04-InvalidExpiredAt](screenshots/BUG-FR17-04-InvalidExpiredAt.png), [04-GetInvalidExpiredAt](screenshots/BUG-FR17-04-GetInvalidExpiredAt.png).
**Root cause:** `backend/server.js:457-481` không kiểm tra `expired_at`; cột `expired_at DATETIME` không có `NOT NULL`/`CHECK` (`backend/database.js:35`). Hệ quả nguồn FR-09: `new Date("")`/`new Date("not-a-date")` là Invalid Date, phép `expiry < now` trả `false` → coupon có thể được coi là còn hạn; `new Date(null)` = 1970 → luôn hết hạn (`server.js:380-384`).

#### BUG-FR17-05 — Backend nhận `min_order_amount` âm, không phải số hoặc thiếu

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-17 — R6 `min_order_amount` bắt buộc, là số `>= 0` |
| Test case | DT-21 (`-1`), DT-22 (thiếu), DT-23 (`"abc"`) |
| Build / môi trường | `f389502…`; API `POST /api/admin/coupons` |
| Severity / Priority | Medium / Medium — ngưỡng đơn hàng bị vô hiệu (âm/NULL) hoặc coupon không bao giờ áp dụng (`"abc"`); dữ liệu kiểu sai |
| Trạng thái / lặp lại | **Đã xác nhận qua API** (ảnh Postman); 1/1 run API cho cả 3 input |

**Chuẩn bị:** như BUG-FR17-01; chỉ đổi `min_order_amount`.

**Các bước (API đã chạy):**

```zsh
# DT-21: -1
curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-21","type":"percent","discount_value":10,"min_order_amount":-1,"expired_at":"2099-12-31","max_uses_per_user":1}'

# DT-22: bỏ hẳn key min_order_amount
curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-22","type":"percent","discount_value":10,"expired_at":"2099-12-31","max_uses_per_user":1}'

# DT-23: "abc"
curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-23","type":"percent","discount_value":10,"min_order_amount":"abc","expired_at":"2099-12-31","max_uses_per_user":1}'
```

**Expected:** non-2xx; không có row mới.  
**Actual:** cả ba 200; row mới lưu `-1`, `NULL`, `"abc"`.  
**UI (Dự kiến — chưa kiểm chứng UI):** DT-21 đi được — ô **Đơn tối thiểu** là `type="number"` không có `min`, nhập `-1`, **Tạo mã**, kiểm tra bảng có `-1 ₫`; không dùng ảnh UI làm bằng chứng. DT-22/DT-23 API-only vì UI luôn gửi key và `type=number` chặn `abc`. (Nếu tester xóa trắng ô, UI gửi `""` — input khác, không gán cho DT-22.)
**Evidence:** `DT-21.log`…`DT-23.log`.  
**Screenshot API:** [05-MinOrderNegative](screenshots/BUG-FR17-05-MinOrderNegative.png), [05-GetMinOrderNegative](screenshots/BUG-FR17-05-GetMinOrderNegative.png), [05-MissingMinOrderAmount](screenshots/BUG-FR17-05-MissingMinOrderAmount.png), [05-GetMissingMinOrderAmount](screenshots/BUG-FR17-05-GetMissingMinOrderAmount.png), [05-InvalidMinOrder](screenshots/BUG-FR17-05-InvalidMinOrder.png), [05-GetInvalidMinOrder](screenshots/BUG-FR17-05-GetInvalidMinOrder.png).
**Root cause:** `backend/server.js:457-481` không kiểm tra số/`>= 0`; cột `min_order_amount INTEGER DEFAULT 0` không có `CHECK` (`backend/database.js:34`). Khi `NULL`, UI có thể hiển thị `undefined ₫`/blank; khi `"abc"`, so sánh số với chuỗi không theo nghĩa mong đợi.

#### BUG-FR17-06 — Backend nhận `max_uses_per_user < 1` hoặc thiếu; number `0` bị đổi thành `1`

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-17 — R7 `max_uses_per_user` bắt buộc, là số nguyên `>= 1` |
| Test case | DT-26 (`0`), DT-27 (`-1`), DT-28 (thiếu key) |
| Build / môi trường | `f389502…`; API `POST /api/admin/coupons` |
| Severity / Priority | Medium / Medium — `0` bị âm thầm đổi thành `1` (hành vi khác input), `-1` làm coupon không dùng được, thiếu key được default thay vì từ chối; API-only |
| Trạng thái / lặp lại | **Đã xác nhận qua API** (ảnh Postman); 1/1 run API cho cả 3 input |

**Chuẩn bị:** như BUG-FR17-01; chỉ đổi `max_uses_per_user`.

**Các bước (API đã chạy):**

```zsh
# DT-26: 0
curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-26","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":0}'

# DT-27: -1
curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-27","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":-1}'

# DT-28: bỏ hẳn key max_uses_per_user
curl -s -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-28","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31"}'
```

**Expected:** non-2xx; không có row mới.  
**Actual:** cả ba 200; JSON number `0` lưu thành `1` (do `max_uses_per_user || 1`), `-1` lưu `-1`, thiếu key lưu `1`.  
**UI (Dự kiến — chưa kiểm chứng UI):** không có đường UI thông thường cho `0`/`-1` vì ô có `min="1"`; ca API-only. Bỏ trống ô gửi `""` (khác input "omitted"), backend `|| 1` cũng cho `1` — nếu tester thử, ghi thành quan sát riêng, không gán cho DT-26/DT-28.  
**Evidence:** `DT-26.log`…`DT-28.log`.  
**Screenshot API:** [06-MaxUsesPerUser0](screenshots/BUG-FR17-06-MaxUsesPerUser0.png), [06-MaxUsesPerUser0Up1](screenshots/BUG-FR17-06-MaxUsesPerUser0Up1.png), [06-MaxUsesPerUserNegative](screenshots/BUG-FR17-06-MaxUsesPerUserNegative.png), [06-GetMaxUsesPerUserNegative](screenshots/BUG-FR17-06-GetMaxUsesPerUserNegative.png), [06-MissingMaxUses](screenshots/BUG-FR17-06-MissingMaxUses.png), [06-GetMissingMaxUses](screenshots/BUG-FR17-06-GetMissingMaxUses.png).
**Root cause:** `backend/server.js:474` dùng `max_uses_per_user || 1`; không có kiểm tra `>= 1`; cột `max_uses_per_user INTEGER DEFAULT 1` không có `CHECK` (`backend/database.js:37`). Hệ quả nguồn FR-09: `usage_count >= -1` luôn đúng → coupon bị coi là hết lượt ngay từ đầu (`server.js:391-396`).

#### BUG-FR17-07 — Backend nhận `code` khác hoa/thường khi đã có mã tương ứng

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-17 — Coupon CRUD; R2 `code` bắt buộc và duy nhất **không phân biệt hoa/thường** (người kiểm thử xác nhận 2026-10-21) |
| Test case | DT-07 — `code = "save10"` khi seed `SAVE10` đã tồn tại |
| Build / môi trường | `f389502…`; API `POST /api/admin/coupons`; Node/Express + SQLite; DB test cách ly |
| Severity / Priority | **Medium / Medium** — tạo được coupon nhìn giống hệt mã đã có; UI tự uppercase nên finding là API-only, nhưng dữ liệu có thể gây nhầm lẫn/trùng nghĩa khi tích hợp |
| Trạng thái / lặp lại | **Đã xác nhận qua API** bằng ảnh Postman; Issue [#53](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/53); 1/1 run API + ảnh chụp lần chạy lại |

**Chuẩn bị:** DB test có 4 seed, gồm `SAVE10`; đăng nhập admin; các trường còn lại baseline (`type=percent`, `discount_value=10`, `min_order_amount=100000`, `expired_at=2099-12-31`, `max_uses_per_user=1`).

**Các bước (API đã chạy):**

```zsh
curl -s -w '\nHTTP %{http_code}\n' -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"save10","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

curl -s http://localhost:3000/api/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq '.[] | select(.code == "SAVE10" or .code == "save10")'
```

| Mốc | Expected theo rule | Actual quan sát được |
| --- | --- | --- |
| Tạo `save10` khi đã có `SAVE10` | Non-2xx; không có row mới | `HTTP 200`, body `{"message":"Coupon created","id":10}` |
| Danh sách sau request | Chỉ còn `SAVE10` | Có cả `SAVE10` và `save10` |

**Kết luận:** Backend coi hai mã khác hoa/thường là hai giá trị duy nhất, vi phạm quy tắc uniqueness không phân biệt hoa/thường. UI admin tự `toUpperCase()` nên người dùng thông thường khó gửi `save10`; đây là lỗi API-only.

**Root cause:** `backend/database.js:31` khai báo `code TEXT UNIQUE` với collation BINARY mặc định; `backend/server.js:466-479` không chuẩn hóa `code` trước khi `INSERT`. UI uppercase tại `frontend-admin/src/App.jsx:641-645` chỉ che lỗi trên đường UI.

**Evidence:** `DT-07.log` (EV-FR17-007). **Screenshot API:** [07-CouponUppercase](screenshots/BUG-FR17-07-CouponUppercase.png), [07-CreateCouponLowercase](screenshots/BUG-FR17-07-CreateCouponLowercase.png), [07-GetCouponLowercase](screenshots/BUG-FR17-07-GetCouponLowercase.png). **Issue:** [#53](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/53).

---

#### BUG-FR17-08 — Backend nhận `discount_value = 150` cho coupon `percent`

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-17 — Coupon CRUD; R4 `discount_value` dương và với `type = percent` không vượt quá `100` (người kiểm thử xác nhận 2026-10-21) |
| Test case | DT-32 — `type = "percent"`, `discount_value = 150` |
| Build / môi trường | `f389502…`; API `POST /api/admin/coupons`; Node/Express + SQLite; DB test cách ly |
| Severity / Priority | **High / High** — coupon có mức giảm không thể tồn tại; dữ liệu sai có thể làm FR-09 tính số tiền âm/không hợp lý |
| Trạng thái / lặp lại | **Đã xác nhận qua API** bằng ảnh Postman; Issue [#54](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54); 1/1 run API + 2 ảnh Postman + 1 ảnh UI bổ sung |

**Chuẩn bị:** DB test có 4 seed; đăng nhập admin; baseline `code=FR17-DT-32`, `min_order_amount=100000`, `expired_at=2099-12-31`, `max_uses_per_user=1`; chỉ đổi `type=percent`, `discount_value=150`.

**Các bước (API đã chạy):**

```zsh
curl -s -w '\nHTTP %{http_code}\n' -X POST http://localhost:3000/api/admin/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -d '{"code":"FR17-DT-32","type":"percent","discount_value":150,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1}'

curl -s http://localhost:3000/api/coupons \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq '.[] | select(.code == "FR17-DT-32")'
```

| Mốc | Expected theo rule | Actual quan sát được |
| --- | --- | --- |
| Tạo coupon `percent` với `150` | Non-2xx; không có row mới | `HTTP 200`, body `{"message":"Coupon created","id":34}` |
| Danh sách sau request | Không có `FR17-DT-32` | Row `FR17-DT-32` có `discount_value=150` |

**Kết luận:** Backend không kiểm tra upper bound `100` cho percent, nên lưu một mức giảm vô nghĩa. UI không có `max` trên ô Giá trị nên người dùng cũng có thể nhập trực tiếp `150`; ảnh UI bổ sung xác nhận coupon `150%` được áp dụng thành công và cho kết quả bất thường (tiết kiệm âm, thành tiền tăng), trong khi bằng chứng chính của bug vẫn là API.

**Root cause:** `backend/server.js:457-481` chỉ `INSERT` giá trị, không kiểm tra `type === "percent"` và `discount_value <= 100`; `frontend-admin/src/App.jsx:659-675` không đặt `max`.

**Evidence:** `DT-32.log` (EV-FR17-032). **Screenshot:** [08-Discount150](screenshots/BUG-FR17-08-Discount150.png), [08-GetDiscount150](screenshots/BUG-FR17-08-GetDiscount150.png), [08-AppliedDiscount150](screenshots/BUG-FR17-08-AppliedDiscount150.png) (ảnh UI bổ sung: giảm `150%`, tiết kiệm `-4,470,000,000 đ`, thành tiền `4,500,000,000 đ`). **Issue:** [#54](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54).

---

## Quan sát ngoài oracle EP/BVA

Các mục dưới đây **không cộng vào coverage**; chi tiết và nguồn ở `supporting-materials/fr17-observations.md`.

| ID | Quan sát | Liên quan | Trạng thái |
| --- | --- | --- | --- |
| OBS-FR17-01 | Trùng `code` trả HTTP 500 kèm `SQLITE_CONSTRAINT` thay vì lỗi validation | DT-03 (PASS về uniqueness) | Chờ người kiểm thử quyết định |
| OBS-FR17-02 | Xóa id không tồn tại trả 200 `Coupon deleted` | DT-31 | Chờ người kiểm thử quyết định |
| OBS-FR17-03 | `save10` được tạo bên cạnh `SAVE10` | DT-07 | **Đã xác nhận — BUG-FR17-07**; không còn là quan sát |
| OBS-FR17-04 | `percent` với `discount_value=150` được chấp nhận | DT-32 | **Đã xác nhận — BUG-FR17-08**; không còn là quan sát |
| OBS-FR17-05 | UI coupon không có `<label>`/dấu `*` cho trường bắt buộc (FR-22) | Source UI | Chưa chạy UI |
| OBS-FR17-06 | User token gọi được `POST /api/admin/coupons` (FR-12) | OBS log | Đã xác nhận qua API |
| OBS-FR17-07 | FR-09 `apply-coupon`: công thức percent sai, dùng `>` thay `>=`, endpoint công khai | OBS log | Đã chạy, ngoài phạm vi FR-17 |
| OBS-FR17-08 | UI hiển thị `type=NULL` thành "Cố định", ngày sai thành chuỗi, `min=NULL` thành `undefined ₫`/blank | Source UI | Chưa chạy UI |
| OBS-FR17-09 | `GET /api/coupons` yêu cầu token nhưng không giới hạn role admin (FR-12) | OBS log | Đã xác nhận qua API |
| OBS-FR17-10 | Không có confirm khi xóa coupon | Source UI | Chưa chạy UI |

## Khoảng trống và câu hỏi mở

- **UI không dùng làm bằng chứng chính:** 16 T-ID UI-reachable chỉ có hướng dẫn manual; kết luận FR-17 dựa trên API/Postman. Ngoại lệ bổ sung: 1 ảnh UI áp dụng coupon `150%` cho `BUG-FR17-08`, chỉ minh họa hệ quả FR-09.
- **GitHub Issue:** 8 bug đã publish [#47](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/47)…[#54](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54) kèm 39 ảnh Postman + 1 ảnh UI bổ sung cho `BUG-FR17-08`; 2 bug mới `BUG-FR17-07/08` có Issue [#53](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/53)/[#54](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54).
- **Oracle chưa đầy đủ:** status/message validation không được đặc tả; hành vi xóa id không tồn tại vẫn UNRESOLVED. Case-sensitivity của `code` và upper bound percent đã được người kiểm thử xác nhận ngày 2026-10-21.
- **Ảnh còn thiếu:** chỉ còn `DT-06` chưa có ảnh; `DT-07` và `DT-32` đã có ảnh Postman, `DT-32` có thêm 1 ảnh UI áp dụng coupon `150%`, Issue tương ứng [#53](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/53)/[#54](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54).
- **ASSUMED:** code toàn khoảng trắng là invalid; `expired_at` phải đúng định dạng ngày; coupon quá khứ vẫn được tạo; `max_uses_per_user` là số nguyên.
- **Ngoài phạm vi:** FR-09 (áp dụng coupon) và FR-12 (phân quyền admin) chỉ ghi quan sát, không tính coverage.
- **Không có Update:** FR-17 chỉ yêu cầu Thêm/Xem/Xóa; không kiểm thử sửa coupon.
- **Database:** working DB giữ nguyên SHA-256 `c63f0054…`; test DB sau run chỉ còn 4 seed; temp SUT đã dừng/xóa sau khi hoàn tất — xem `evidence/cleanup.log`.
- **AI Gap Analysis / AI Critique:** sinh viên tự viết; AI không điền thay.

## Trạng thái Issue / screenshot

- 8 bug `BUG-FR17-01`…`BUG-FR17-08`: **Đã xác nhận qua API**; 8 bug đều có ảnh Postman; `BUG-FR17-08` có thêm 1 ảnh UI bổ sung hệ quả FR-09.
- GitHub Issue đã mở cho 8 bug: [#47](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/47), [#48](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/48), [#49](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/49), [#50](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/50), [#51](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/51), [#52](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/52), [#53](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/53), [#54](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54); draft tương ứng tại [`BUG-FR17-07.md`](issues/BUG-FR17-07.md) và [`BUG-FR17-08.md`](issues/BUG-FR17-08.md).
- **39 ảnh API + 1 ảnh UI** tại `screenshots/` (19/20 FAIL có ảnh API; `DT-06` chưa có ảnh).
- `DT-07`/`DT-32` đã có ảnh và Issue [#53](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/53)/[#54](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54). Ảnh UI chỉ bổ sung hệ quả `BUG-FR17-08`, không thay bằng chứng API.

## AI Gap Analysis

Đặc tả FR-17 chỉ ghi `discount_value` phải dương, **không quy định giới hạn trên**. Vì vậy 100% dưới đây là mốc người kiểm thử suy luận và đề xuất cho coupon loại `percent`, chưa phải biên được xác định trong đặc tả; không áp dụng mốc này cho loại `fixed`.

| Gap ID | AI output/source | Test case/bug tôi phát hiện thêm | Cách tôi phát hiện | Vì sao AI bỏ sót (nhận định của tôi) | Bổ sung/sửa chữa |
| --- | --- | --- | --- | --- | --- |
| AI-GAP-FR17-01 | AI dựa vào FR-17, nơi chỉ yêu cầu `discount_value > 0`, nên các ca ban đầu tập trung vào giá trị 0 và âm; AI không nêu câu hỏi về mức giảm quá lớn của loại `percent`. | Tôi đề xuất rằng mức giảm theo phần trăm không nên vượt quá 100%. Ca `DT-32` cho thấy hệ thống vẫn tạo được coupon `percent` giảm 150%; hiện tượng này đã được báo cáo ở `BUG-FR17-08` (Issue #54) theo suy luận nghiệp vụ của tôi. | Tôi xem công thức tính giảm giá và nhận thấy mức trên 100% không có ý nghĩa với một khoản giảm theo phần trăm. Sau đó tôi thử `discount_value = 150`, kiểm tra coupon được lưu qua API và quan sát kết quả bất thường khi áp dụng mã. | Spec không nêu giới hạn trên, nên AI chỉ kiểm các ràng buộc được viết rõ. AI đã đặt câu hỏi liệu giá trị phần trăm quá lớn có hợp lý trong nghiệp vụ hay không chứ không kết luận. Trong khi với người, chỉ cần thấy giảm giá > 100% là không hợp lý. Dẫn đến việc AI phải suy luận và trả lại 1 bug hiển nhiên cho con người review lại mà không viết luôn report như yêu cầu. | Đề nghị bổ sung giới hạn biên cho percent, làm rõ nghiệp vụ cho `type = percent` và quy định cách xử lý giá trị vượt giới hạn; sau khi yêu cầu được chốt mới thiết kế ca kiểm tra sát biên tương ứng. |
