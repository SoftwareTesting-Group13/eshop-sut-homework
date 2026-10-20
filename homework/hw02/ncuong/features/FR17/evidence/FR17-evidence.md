# FR17 — Evidence log (nhật ký bằng chứng thực thi)

> Mỗi lần thử một test case có một mục `EV-ID`; kết quả thô quan sát được, không chép Expected vào Actual. Log chi tiết từng ca nằm trong `evidence/<T-ID>.log`; dữ liệu có cấu trúc trong `run-summary.json`.

## Thông tin phiên chạy

| Mục | Giá trị |
| --- | --- |
| Feature | FR-17 — Quản lý Mã Giảm Giá (Coupon CRUD) |
| Interface | API `POST/GET/DELETE` coupon (admin token); UI admin dự kiến cho manual |
| SUT / build | `eshop-sut-homework` commit `f389502cdb308b133fe9044e34505f19202dd887` |
| Môi trường | macOS; Node v26.9.0; backend Node/Express + SQLite; instance cách ly (bản sao `server.js`/`database.js`, `database.sqlite` riêng, `node_modules` symlink) |
| Thời điểm chạy | 2026-10-20T15:38:26.710Z (2026-10-20 22:38:26 +0700) → 2026-10-20T15:38:27.016Z (2026-10-20 22:38:27 +0700) |
| Người/agent thực thi | AI agent (theo skill `domain-testing-workflow`); screenshot API: người kiểm thử cung cấp 39 ảnh Postman; chỉ dùng bằng chứng Postman/API, không dùng ảnh UI |
| GitHub Issue | [#47](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/47), [#48](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/48), [#49](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/49), [#50](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/50), [#51](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/51), [#52](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/52) |
| Thư mục evidence | `evidence/` |
| Database làm việc | `backend/database.sqlite`, SHA-256 trước/sau: `c63f00544180ba1fbb1427a9b9dd3f1784842698809972f33ce90482e7420ba6` / `c63f00544180ba1fbb1427a9b9dd3f1784842698809972f33ce90482e7420ba6` |
| Database test | `/private/var/folders/2f/64j8q4t10vz15mrnyzk48_j80000gn/T/opencode/fr17-sut/database.sqlite`, SHA-256 sau run FR17 (trước các probe OBS): `8a9e1caac1c8872ee4de72181126604307f4e541b85e2a88a815b821529bab86` |

**Fixture:** seed coupons `SAVE10`, `BIGBUY`, `VIP100`, `EXPIRED`; tài khoản seed `admin@eshop.com` / `Admin123!` (admin) và `test@eshop.com` / `Test1234!` (user, chỉ dùng cho quan sát ngoài phạm vi).

**Trình điều khiển (driver):** `evidence/run-fr17.mjs` (chạy các ca, ghi log và `run-summary.json`).

## Tổng hợp

| Chỉ số | Giá trị |
| --- | ---: |
| T-ID thiết kế | 32 |
| Đã chạy | 32 |
| PASS | 11 |
| FAIL | 20 |
| Quan sát / INCONCLUSIVE | 1 |
| BLOCKED | 0 |
| Chưa chạy | 0 |

> DT-07/DT-32 được người kiểm thử xác nhận là bug ngày 2026-10-21; log giữ nguyên Actual của lần chạy `run-20261020-fr17`, chỉ cập nhật Expected/oracle/status/Bug ID. Hai ca này dùng lại T-ID cũ, không tăng tổng thiết kế.

## Ảnh xác nhận API (người kiểm thử cung cấp)

> 39 ảnh Postman xác nhận request/response API, **không dùng ảnh UI**. 19/20 FAIL có ảnh; chỉ còn `DT-06` chưa có ảnh. File nằm trong `../screenshots/`.

| Bug | Test case | Ảnh request | Ảnh GET |
| --- | --- | --- | --- |
| BUG-FR17-01 | DT-04 | [CodeEmpty](../screenshots/BUG-FR17-01-CodeEmpty.png) | [GetCodeEmpty](../screenshots/BUG-FR17-01-GetCodeEmpty.png) |
| BUG-FR17-01 | DT-05 | [MissingCode](../screenshots/BUG-FR17-01-MissingCode.png) | [CodeNull](../screenshots/BUG-FR17-01-CodeNull.png) |
| BUG-FR17-01 | DT-06 | — | — (chưa có ảnh) |
| BUG-FR17-02 | DT-08 | [TypeInvalid](../screenshots/BUG-FR17-02-TypeInvalid.png) | [GetCodeHasTypeInvalid](../screenshots/BUG-FR17-02-GetCodeHasTypeInvalid.png) |
| BUG-FR17-02 | DT-09 | [MissingType](../screenshots/BUG-FR17-02-MissingType.png) | [GetNullType](../screenshots/BUG-FR17-02-GetNullType.png) |
| BUG-FR17-03 | DT-10 | [DiscountValue0](../screenshots/BUG-FR17-03-DiscountValue0.png) | [GetDiscountValue0](../screenshots/BUG-FR17-03-GetDiscountValue0.png) |
| BUG-FR17-03 | DT-11 | [DiscountValueNegative](../screenshots/BUG-FR17-03-DiscountValueNegative.png) | [GetDiscountNegative](../screenshots/BUG-FR17-03-GetDiscountNegative.png) |
| BUG-FR17-03 | DT-12 | [MissingDiscountValue](../screenshots/BUG-FR17-03-MissingDiscountValue.png) | [GetMissingDiscountValue](../screenshots/BUG-FR17-03-GetMissingDiscountValue.png) |
| BUG-FR17-03 | DT-13 | [DiscountValueInvalid](../screenshots/BUG-FR17-03-DiscountValueInvalid.png) | [GetDiscountValueInvalid](../screenshots/BUG-FR17-03-GetDiscountValueInvalid.png) |
| BUG-FR17-04 | DT-15 | [MissingExpiredAt](../screenshots/BUG-FR17-04-MissingExpiredAt.png) | [GetMissingExpiredAt](../screenshots/BUG-FR17-04-GetMissingExpiredAt.png) |
| BUG-FR17-04 | DT-16 | [EmptyExpiredAt](../screenshots/BUG-FR17-04-EmptyExpiredAt.png) | [GetEmptyExpiredAt](../screenshots/BUG-FR17-04-GetEmptyExpiredAt.png) |
| BUG-FR17-04 | DT-17 | [InvalidExpiredAt](../screenshots/BUG-FR17-04-InvalidExpiredAt.png) | [GetInvalidExpiredAt](../screenshots/BUG-FR17-04-GetInvalidExpiredAt.png) |
| BUG-FR17-05 | DT-21 | [MinOrderNegative](../screenshots/BUG-FR17-05-MinOrderNegative.png) | [GetMinOrderNegative](../screenshots/BUG-FR17-05-GetMinOrderNegative.png) |
| BUG-FR17-05 | DT-22 | [MissingMinOrderAmount](../screenshots/BUG-FR17-05-MissingMinOrderAmount.png) | [GetMissingMinOrderAmount](../screenshots/BUG-FR17-05-GetMissingMinOrderAmount.png) |
| BUG-FR17-05 | DT-23 | [InvalidMinOrder](../screenshots/BUG-FR17-05-InvalidMinOrder.png) | [GetInvalidMinOrder](../screenshots/BUG-FR17-05-GetInvalidMinOrder.png) |
| BUG-FR17-06 | DT-26 | [MaxUsesPerUser0](../screenshots/BUG-FR17-06-MaxUsesPerUser0.png) | [MaxUsesPerUser0Up1](../screenshots/BUG-FR17-06-MaxUsesPerUser0Up1.png) |
| BUG-FR17-06 | DT-27 | [MaxUsesPerUserNegative](../screenshots/BUG-FR17-06-MaxUsesPerUserNegative.png) | [GetMaxUsesPerUserNegative](../screenshots/BUG-FR17-06-GetMaxUsesPerUserNegative.png) |
| BUG-FR17-06 | DT-28 | [MissingMaxUses](../screenshots/BUG-FR17-06-MissingMaxUses.png) | [GetMissingMaxUses](../screenshots/BUG-FR17-06-GetMissingMaxUses.png) |
| BUG-FR17-07 | DT-07 (seed) | [CouponUppercase](../screenshots/BUG-FR17-07-CouponUppercase.png) | — |
| BUG-FR17-07 | DT-07 | [CreateCouponLowercase](../screenshots/BUG-FR17-07-CreateCouponLowercase.png) | [GetCouponLowercase](../screenshots/BUG-FR17-07-GetCouponLowercase.png) |
| BUG-FR17-08 | DT-32 | [Discount150](../screenshots/BUG-FR17-08-Discount150.png) | [GetDiscount150](../screenshots/BUG-FR17-08-GetDiscount150.png) |

## Evidence items

### EV-FR17-001 — DT-01 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-01 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P1, R1, R2, R3, R4, R5, R6, R7 |
| Thời điểm | 2026-10-20T15:38:26.787Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | DB test mới seed 4 coupon (SAVE10, BIGBUY, VIP100, EXPIRED); đăng nhập admin@eshop.com; các trường khác giữ baseline hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-01",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 5
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 5,
      "code": "FR17-DT-01",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 5,
    "code": "FR17-DT-01",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": [
    {
      "field": "code",
      "expected": "FR17-DT-01",
      "actual": "FR17-DT-01",
      "pass": true
    },
    {
      "field": "type",
      "expected": "percent",
      "actual": "percent",
      "pass": true
    },
    {
      "field": "discount_value",
      "expected": 10,
      "actual": 10,
      "pass": true
    },
    {
      "field": "min_order_amount",
      "expected": 100000,
      "actual": 100000,
      "pass": true
    },
    {
      "field": "expired_at",
      "expected": "2099-12-31",
      "actual": "2099-12-31",
      "pass": true
    },
    {
      "field": "max_uses_per_user",
      "expected": 1,
      "actual": 1,
      "pass": true
    }
  ],
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Tạo thành công (2xx); coupon xuất hiện trong GET /api/coupons với đủ 6 trường đúng giá trị. Nguồn: README.md §5 FR-17; api_specification.md §6.4.
- **Actual:** HTTP 200; new_rows=1; target={"id":5,"code":"FR17-DT-01","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","is_active":1,"max_uses_per_user":1}; field_checks=[{"field":"code","expected":"FR17-DT-01","actual":"FR17-DT-01","pass":true},{"field":"type","expected":"percent","actual":"percent","pass":true},{"field":"discount_value","expected":10,"actual":10,"pass":true},{"field":"min_order_amount","expected":100000,"actual":100000,"pass":true},{"field":"expired_at","expected":"2099-12-31","actual":"2099-12-31","pass":true},{"field":"max_uses_per_user","expected":1,"actual":1,"pass":true}]
- **Status:** `PASS`
- **Artifact:** `evidence/DT-01.log`
- **Cleanup:** DELETE /api/admin/coupons/5 -> HTTP 200
- **Bug liên quan:** không
- **Ghi chú:** Baseline percent; đồng thời kiểm tra persistence qua GET danh sách.

### EV-FR17-002 — DT-02 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-02 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P2, R1, R2, R3, R4, R5, R6, R7 |
| Thời điểm | 2026-10-20T15:38:26.799Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | DB test mới seed 4 coupon; đăng nhập admin; type=fixed, discount_value=50000, min_order_amount=200000. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-02",
  "type": "fixed",
  "discount_value": 50000,
  "min_order_amount": 200000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 6
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 6,
      "code": "FR17-DT-02",
      "type": "fixed",
      "discount_value": 50000,
      "min_order_amount": 200000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 6,
    "code": "FR17-DT-02",
    "type": "fixed",
    "discount_value": 50000,
    "min_order_amount": 200000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": [
    {
      "field": "code",
      "expected": "FR17-DT-02",
      "actual": "FR17-DT-02",
      "pass": true
    },
    {
      "field": "type",
      "expected": "fixed",
      "actual": "fixed",
      "pass": true
    },
    {
      "field": "discount_value",
      "expected": 50000,
      "actual": 50000,
      "pass": true
    },
    {
      "field": "min_order_amount",
      "expected": 200000,
      "actual": 200000,
      "pass": true
    },
    {
      "field": "expired_at",
      "expected": "2099-12-31",
      "actual": "2099-12-31",
      "pass": true
    },
    {
      "field": "max_uses_per_user",
      "expected": 1,
      "actual": 1,
      "pass": true
    }
  ],
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Tạo thành công (2xx); coupon type=fixed xuất hiện trong GET /api/coupons với đủ 6 trường đúng giá trị. Nguồn: README.md §5 FR-17; api_specification.md §6.4.
- **Actual:** HTTP 200; new_rows=1; target={"id":6,"code":"FR17-DT-02","type":"fixed","discount_value":50000,"min_order_amount":200000,"expired_at":"2099-12-31","is_active":1,"max_uses_per_user":1}; field_checks=[{"field":"code","expected":"FR17-DT-02","actual":"FR17-DT-02","pass":true},{"field":"type","expected":"fixed","actual":"fixed","pass":true},{"field":"discount_value","expected":50000,"actual":50000,"pass":true},{"field":"min_order_amount","expected":200000,"actual":200000,"pass":true},{"field":"expired_at","expected":"2099-12-31","actual":"2099-12-31","pass":true},{"field":"max_uses_per_user","expected":1,"actual":1,"pass":true}]
- **Status:** `PASS`
- **Artifact:** `evidence/DT-02.log`
- **Cleanup:** DELETE /api/admin/coupons/6 -> HTTP 200
- **Bug liên quan:** không
- **Ghi chú:** Lớp hợp lệ của type=fixed.

### EV-FR17-003 — DT-03 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-03 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P3, R2 |
| Thời điểm | 2026-10-20T15:38:26.806Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | DB test có seed SAVE10; đăng nhập admin; gửi code trùng SAVE10 với các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "SAVE10",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 500
{
  "error": "SQLITE_CONSTRAINT: UNIQUE constraint failed: coupons.code"
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 4,
  "new_rows": [],
  "target_row": null,
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; code phải duy nhất. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 500; new_rows=0; body={"error":"SQLITE_CONSTRAINT: UNIQUE constraint failed: coupons.code"}
- **Status:** `PASS`
- **Artifact:** `evidence/DT-03.log`
- **Cleanup:** không tạo row nào
- **Bug liên quan:** không
- **Ghi chú:** Đặc tả không quy định status/message cho trùng code; verdict chỉ dựa trên việc coupon không được tạo. Quan sát mã lỗi thô trong log.

### EV-FR17-004 — DT-04 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-04 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P4, R2 |
| Thời điểm | 2026-10-20T15:38:26.813Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; code = chuỗi rỗng; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 7
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 7,
      "code": "",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": null,
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; code là trường bắt buộc. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":7}; unexpected_rows=[{"id":7,"code":"","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-04.log`
- **Cleanup:** DELETE /api/admin/coupons/7 -> HTTP 200
- **Bug liên quan:** BUG-FR17-01
- **Ghi chú:** UI có thuộc tính required nên không gửi được chuỗi rỗng qua form thông thường.

### EV-FR17-005 — DT-05 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-05 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P5, R2 |
| Thời điểm | 2026-10-20T15:38:26.818Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; bỏ hẳn key code khỏi JSON; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 8
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 8,
      "code": null,
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": null,
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; code là trường bắt buộc. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":8}; unexpected_rows=[{"id":8,"code":null,"type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-05.log`
- **Cleanup:** DELETE /api/admin/coupons/8 -> HTTP 200
- **Bug liên quan:** BUG-FR17-01
- **Ghi chú:** Khác với code rỗng: request không có key code. UI luôn gửi key code nên ca này API-only.

### EV-FR17-006 — DT-06 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-06 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P6, R2 |
| Thời điểm | 2026-10-20T15:38:26.825Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; code = ba khoảng trắng; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "   ",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 9
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 9,
      "code": "   ",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 9,
    "code": "   ",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; code chỉ gồm khoảng trắng không phải code hợp lệ (ASSUMED: cần trim trước khi kiểm tra bắt buộc). Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":9}; unexpected_rows=[{"id":9,"code":"   ","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-06.log`
- **Cleanup:** DELETE /api/admin/coupons/9 -> HTTP 200
- **Bug liên quan:** BUG-FR17-01
- **Ghi chú:** ASSUMED: đặc tả không nói rõ trim, nhưng code chỉ có khoảng trắng không thể là mã duy nhất có nghĩa. UI required không chặn chuỗi khoảng trắng.

### EV-FR17-007 — DT-07 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-07 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P7, R2 |
| Thời điểm | 2026-10-20T15:38:26.831Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | DB test có seed SAVE10; đăng nhập admin; gửi code viết thường save10. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "save10",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 10
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 10,
      "code": "save10",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 10,
    "code": "save10",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Từ chối (non-2xx) và không tạo coupon mới; uniqueness của `code` không phân biệt hoa/thường, nên `save10` trùng với seed `SAVE10` (người kiểm thử xác nhận 2026-10-21). Nguồn: R2.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":10}; new_rows_data=[{"id":10,"code":"save10","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-07.log`
- **Cleanup:** DELETE /api/admin/coupons/10 -> HTTP 200
- **Bug liên quan:** BUG-FR17-07
- **Screenshot:** [seed SAVE10](../screenshots/BUG-FR17-07-CouponUppercase.png), [POST save10](../screenshots/BUG-FR17-07-CreateCouponLowercase.png), [GET save10](../screenshots/BUG-FR17-07-GetCouponLowercase.png); ảnh chụp lần chạy lại có row `id=5` thay vì `id=10` trong log, cùng request/response.
- **Ghi chú:** UI tự uppercase code nên không gửi được save10 qua form thông thường; ca này API-only. Quy tắc uniqueness không phân biệt hoa/thường do người kiểm thử xác nhận ngày 2026-10-21.

### EV-FR17-008 — DT-08 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-08 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P8, R3 |
| Thời điểm | 2026-10-20T15:38:26.838Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; type = percentage; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-08",
  "type": "percentage",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 11
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 11,
      "code": "FR17-DT-08",
      "type": "percentage",
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 11,
    "code": "FR17-DT-08",
    "type": "percentage",
    "discount_value": 10,
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; type chỉ nhận percent/fixed. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":11}; unexpected_rows=[{"id":11,"code":"FR17-DT-08","type":"percentage","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-08.log`
- **Cleanup:** DELETE /api/admin/coupons/11 -> HTTP 200
- **Bug liên quan:** BUG-FR17-02
- **Ghi chú:** UI là select percent/fixed nên không gửi được type ngoài enum; ca này API-only.

### EV-FR17-009 — DT-09 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-09 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P9, R3 |
| Thời điểm | 2026-10-20T15:38:26.847Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; bỏ hẳn key type; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-09",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 12
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 12,
      "code": "FR17-DT-09",
      "type": null,
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 12,
    "code": "FR17-DT-09",
    "type": null,
    "discount_value": 10,
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; type là trường bắt buộc và chỉ nhận percent/fixed. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":12}; unexpected_rows=[{"id":12,"code":"FR17-DT-09","type":null,"discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-09.log`
- **Cleanup:** DELETE /api/admin/coupons/12 -> HTTP 200
- **Bug liên quan:** BUG-FR17-02
- **Ghi chú:** UI select luôn có giá trị nên ca này API-only.

### EV-FR17-010 — DT-10 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-10 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP + BVA |
| Obligation IDs | P10, B3-ON, R4 |
| Thời điểm | 2026-10-20T15:38:26.852Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; discount_value=0; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-10",
  "type": "percent",
  "discount_value": 0,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 13
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 13,
      "code": "FR17-DT-10",
      "type": "percent",
      "discount_value": 0,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 13,
    "code": "FR17-DT-10",
    "type": "percent",
    "discount_value": 0,
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; discount_value phải dương (> 0). 0 là điểm biên ON phía invalid. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":13}; unexpected_rows=[{"id":13,"code":"FR17-DT-10","type":"percent","discount_value":0,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-10.log`
- **Cleanup:** DELETE /api/admin/coupons/13 -> HTTP 200
- **Bug liên quan:** BUG-FR17-03
- **Ghi chú:** UI type=number không có min nên người dùng có thể nhập 0 và submit.

### EV-FR17-011 — DT-11 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-11 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP + BVA |
| Obligation IDs | P11, B3-below, R4 |
| Thời điểm | 2026-10-20T15:38:26.859Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; discount_value=-1; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-11",
  "type": "percent",
  "discount_value": -1,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 14
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 14,
      "code": "FR17-DT-11",
      "type": "percent",
      "discount_value": -1,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 14,
    "code": "FR17-DT-11",
    "type": "percent",
    "discount_value": -1,
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; discount_value phải dương. -1 là điểm ngay dưới biên 0. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":14}; unexpected_rows=[{"id":14,"code":"FR17-DT-11","type":"percent","discount_value":-1,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-11.log`
- **Cleanup:** DELETE /api/admin/coupons/14 -> HTTP 200
- **Bug liên quan:** BUG-FR17-03
- **Ghi chú:** UI type=number không có min nên nhập được -1.

### EV-FR17-012 — DT-12 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-12 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P12, R4 |
| Thời điểm | 2026-10-20T15:38:26.867Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; bỏ hẳn key discount_value; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-12",
  "type": "percent",
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 15
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 15,
      "code": "FR17-DT-12",
      "type": "percent",
      "discount_value": null,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 15,
    "code": "FR17-DT-12",
    "type": "percent",
    "discount_value": null,
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; discount_value là trường bắt buộc. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":15}; unexpected_rows=[{"id":15,"code":"FR17-DT-12","type":"percent","discount_value":null,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-12.log`
- **Cleanup:** DELETE /api/admin/coupons/15 -> HTTP 200
- **Bug liên quan:** BUG-FR17-03
- **Ghi chú:** UI có required nên ca bỏ hẳn key là API-only.

### EV-FR17-013 — DT-13 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-13 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P13, R4 |
| Thời điểm | 2026-10-20T15:38:26.872Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; discount_value='abc'; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-13",
  "type": "percent",
  "discount_value": "abc",
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 16
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 16,
      "code": "FR17-DT-13",
      "type": "percent",
      "discount_value": "abc",
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 16,
    "code": "FR17-DT-13",
    "type": "percent",
    "discount_value": "abc",
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; discount_value phải là số dương. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":16}; unexpected_rows=[{"id":16,"code":"FR17-DT-13","type":"percent","discount_value":"abc","min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-13.log`
- **Cleanup:** DELETE /api/admin/coupons/16 -> HTTP 200
- **Bug liên quan:** BUG-FR17-03
- **Ghi chú:** UI type=number không gửi được abc; ca này API-only.

### EV-FR17-014 — DT-14 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-14 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP + BVA |
| Obligation IDs | P14, B3-above, R4 |
| Thời điểm | 2026-10-20T15:38:26.881Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; discount_value=1; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-14",
  "type": "percent",
  "discount_value": 1,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 17
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 17,
      "code": "FR17-DT-14",
      "type": "percent",
      "discount_value": 1,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 17,
    "code": "FR17-DT-14",
    "type": "percent",
    "discount_value": 1,
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": [
    {
      "field": "code",
      "expected": "FR17-DT-14",
      "actual": "FR17-DT-14",
      "pass": true
    },
    {
      "field": "type",
      "expected": "percent",
      "actual": "percent",
      "pass": true
    },
    {
      "field": "discount_value",
      "expected": 1,
      "actual": 1,
      "pass": true
    },
    {
      "field": "min_order_amount",
      "expected": 100000,
      "actual": 100000,
      "pass": true
    },
    {
      "field": "expired_at",
      "expected": "2099-12-31",
      "actual": "2099-12-31",
      "pass": true
    },
    {
      "field": "max_uses_per_user",
      "expected": 1,
      "actual": 1,
      "pass": true
    }
  ],
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Tạo thành công (2xx); discount_value=1 là giá trị dương nhỏ nhất, coupon xuất hiện với discount_value=1. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; target={"id":17,"code":"FR17-DT-14","type":"percent","discount_value":1,"min_order_amount":100000,"expired_at":"2099-12-31","is_active":1,"max_uses_per_user":1}; field_checks=[{"field":"code","expected":"FR17-DT-14","actual":"FR17-DT-14","pass":true},{"field":"type","expected":"percent","actual":"percent","pass":true},{"field":"discount_value","expected":1,"actual":1,"pass":true},{"field":"min_order_amount","expected":100000,"actual":100000,"pass":true},{"field":"expired_at","expected":"2099-12-31","actual":"2099-12-31","pass":true},{"field":"max_uses_per_user","expected":1,"actual":1,"pass":true}]
- **Status:** `PASS`
- **Artifact:** `evidence/DT-14.log`
- **Cleanup:** DELETE /api/admin/coupons/17 -> HTTP 200
- **Bug liên quan:** không
- **Ghi chú:** Điểm ngay trên biên 0 của B3.

### EV-FR17-015 — DT-15 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-15 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P15, R5 |
| Thời điểm | 2026-10-20T15:38:26.887Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; bỏ hẳn key expired_at; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-15",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 100000,
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 18
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 18,
      "code": "FR17-DT-15",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": null,
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 18,
    "code": "FR17-DT-15",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": 100000,
    "expired_at": null,
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; expired_at là trường bắt buộc. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":18}; unexpected_rows=[{"id":18,"code":"FR17-DT-15","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":null,"max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-15.log`
- **Cleanup:** DELETE /api/admin/coupons/18 -> HTTP 200
- **Bug liên quan:** BUG-FR17-04
- **Ghi chú:** UI có required nên ca bỏ hẳn key là API-only.

### EV-FR17-016 — DT-16 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-16 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P16, R5 |
| Thời điểm | 2026-10-20T15:38:26.894Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; expired_at=chuỗi rỗng; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-16",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 19
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 19,
      "code": "FR17-DT-16",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": "",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 19,
    "code": "FR17-DT-16",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": 100000,
    "expired_at": "",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; expired_at là trường bắt buộc. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":19}; unexpected_rows=[{"id":19,"code":"FR17-DT-16","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-16.log`
- **Cleanup:** DELETE /api/admin/coupons/19 -> HTTP 200
- **Bug liên quan:** BUG-FR17-04
- **Ghi chú:** UI required chặn chuỗi rỗng; ca này API-only.

### EV-FR17-017 — DT-17 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-17 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P17, R5 |
| Thời điểm | 2026-10-20T15:38:26.901Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; expired_at='not-a-date'; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-17",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "not-a-date",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 20
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 20,
      "code": "FR17-DT-17",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": "not-a-date",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 20,
    "code": "FR17-DT-17",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": 100000,
    "expired_at": "not-a-date",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; expired_at phải là ngày hợp lệ (ASSUMED: API example dùng YYYY-MM-DD, UI dùng input type=date). Nguồn: README.md §5 FR-17; api_specification.md §6.4.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":20}; unexpected_rows=[{"id":20,"code":"FR17-DT-17","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"not-a-date","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-17.log`
- **Cleanup:** DELETE /api/admin/coupons/20 -> HTTP 200
- **Bug liên quan:** BUG-FR17-04
- **Ghi chú:** ASSUMED về định dạng ngày; UI date input không gửi được chuỗi này nên ca API-only.

### EV-FR17-018 — DT-18 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-18 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P18, R5 |
| Thời điểm | 2026-10-20T15:38:26.906Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; expired_at='2020-01-01'; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-18",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "2020-01-01",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 21
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 21,
      "code": "FR17-DT-18",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": "2020-01-01",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 21,
    "code": "FR17-DT-18",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": 100000,
    "expired_at": "2020-01-01",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": [
    {
      "field": "code",
      "expected": "FR17-DT-18",
      "actual": "FR17-DT-18",
      "pass": true
    },
    {
      "field": "type",
      "expected": "percent",
      "actual": "percent",
      "pass": true
    },
    {
      "field": "discount_value",
      "expected": 10,
      "actual": 10,
      "pass": true
    },
    {
      "field": "min_order_amount",
      "expected": 100000,
      "actual": 100000,
      "pass": true
    },
    {
      "field": "expired_at",
      "expected": "2020-01-01",
      "actual": "2020-01-01",
      "pass": true
    },
    {
      "field": "max_uses_per_user",
      "expected": 1,
      "actual": 1,
      "pass": true
    }
  ],
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Tạo thành công (2xx); FR-17 chỉ yêu cầu expired_at, không cấm ngày quá khứ; seed có coupon EXPIRED. (ASSUMED từ seed + phạm vi FR-17.)
- **Actual:** HTTP 200; new_rows=1; target={"id":21,"code":"FR17-DT-18","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2020-01-01","is_active":1,"max_uses_per_user":1}; field_checks=[{"field":"code","expected":"FR17-DT-18","actual":"FR17-DT-18","pass":true},{"field":"type","expected":"percent","actual":"percent","pass":true},{"field":"discount_value","expected":10,"actual":10,"pass":true},{"field":"min_order_amount","expected":100000,"actual":100000,"pass":true},{"field":"expired_at","expected":"2020-01-01","actual":"2020-01-01","pass":true},{"field":"max_uses_per_user","expected":1,"actual":1,"pass":true}]
- **Status:** `PASS`
- **Artifact:** `evidence/DT-18.log`
- **Cleanup:** DELETE /api/admin/coupons/21 -> HTTP 200
- **Bug liên quan:** không
- **Ghi chú:** ASSUMED: đặc tả không nói expired_at phải ở tương lai. UI date cho phép chọn ngày quá khứ.

### EV-FR17-019 — DT-19 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-19 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP + BVA |
| Obligation IDs | P19, B1-ON, R6 |
| Thời điểm | 2026-10-20T15:38:26.914Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; min_order_amount=0; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-19",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 0,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 22
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 22,
      "code": "FR17-DT-19",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 0,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 22,
    "code": "FR17-DT-19",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": 0,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": [
    {
      "field": "code",
      "expected": "FR17-DT-19",
      "actual": "FR17-DT-19",
      "pass": true
    },
    {
      "field": "type",
      "expected": "percent",
      "actual": "percent",
      "pass": true
    },
    {
      "field": "discount_value",
      "expected": 10,
      "actual": 10,
      "pass": true
    },
    {
      "field": "min_order_amount",
      "expected": 0,
      "actual": 0,
      "pass": true
    },
    {
      "field": "expired_at",
      "expected": "2099-12-31",
      "actual": "2099-12-31",
      "pass": true
    },
    {
      "field": "max_uses_per_user",
      "expected": 1,
      "actual": 1,
      "pass": true
    }
  ],
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Tạo thành công (2xx); min_order_amount=0 thỏa >= 0 (điểm biên ON hợp lệ). Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; target={"id":22,"code":"FR17-DT-19","type":"percent","discount_value":10,"min_order_amount":0,"expired_at":"2099-12-31","is_active":1,"max_uses_per_user":1}; field_checks=[{"field":"code","expected":"FR17-DT-19","actual":"FR17-DT-19","pass":true},{"field":"type","expected":"percent","actual":"percent","pass":true},{"field":"discount_value","expected":10,"actual":10,"pass":true},{"field":"min_order_amount","expected":0,"actual":0,"pass":true},{"field":"expired_at","expected":"2099-12-31","actual":"2099-12-31","pass":true},{"field":"max_uses_per_user","expected":1,"actual":1,"pass":true}]
- **Status:** `PASS`
- **Artifact:** `evidence/DT-19.log`
- **Cleanup:** DELETE /api/admin/coupons/22 -> HTTP 200
- **Bug liên quan:** không
- **Ghi chú:** UI cho phép 0 (không có min).

### EV-FR17-020 — DT-20 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-20 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP + BVA |
| Obligation IDs | P20, B1-above, R6 |
| Thời điểm | 2026-10-20T15:38:26.921Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; min_order_amount=1; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-20",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 1,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 23
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 23,
      "code": "FR17-DT-20",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 1,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 23,
    "code": "FR17-DT-20",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": 1,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": [
    {
      "field": "code",
      "expected": "FR17-DT-20",
      "actual": "FR17-DT-20",
      "pass": true
    },
    {
      "field": "type",
      "expected": "percent",
      "actual": "percent",
      "pass": true
    },
    {
      "field": "discount_value",
      "expected": 10,
      "actual": 10,
      "pass": true
    },
    {
      "field": "min_order_amount",
      "expected": 1,
      "actual": 1,
      "pass": true
    },
    {
      "field": "expired_at",
      "expected": "2099-12-31",
      "actual": "2099-12-31",
      "pass": true
    },
    {
      "field": "max_uses_per_user",
      "expected": 1,
      "actual": 1,
      "pass": true
    }
  ],
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Tạo thành công (2xx); min_order_amount=1 thỏa >= 0 (điểm ngay trên biên 0). Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; target={"id":23,"code":"FR17-DT-20","type":"percent","discount_value":10,"min_order_amount":1,"expired_at":"2099-12-31","is_active":1,"max_uses_per_user":1}; field_checks=[{"field":"code","expected":"FR17-DT-20","actual":"FR17-DT-20","pass":true},{"field":"type","expected":"percent","actual":"percent","pass":true},{"field":"discount_value","expected":10,"actual":10,"pass":true},{"field":"min_order_amount","expected":1,"actual":1,"pass":true},{"field":"expired_at","expected":"2099-12-31","actual":"2099-12-31","pass":true},{"field":"max_uses_per_user","expected":1,"actual":1,"pass":true}]
- **Status:** `PASS`
- **Artifact:** `evidence/DT-20.log`
- **Cleanup:** DELETE /api/admin/coupons/23 -> HTTP 200
- **Bug liên quan:** không
- **Ghi chú:** UI cho phép 1.

### EV-FR17-021 — DT-21 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-21 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP + BVA |
| Obligation IDs | P21, B1-below, R6 |
| Thời điểm | 2026-10-20T15:38:26.928Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; min_order_amount=-1; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-21",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": -1,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 24
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 24,
      "code": "FR17-DT-21",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": -1,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 24,
    "code": "FR17-DT-21",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": -1,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; min_order_amount phải >= 0. -1 là điểm ngay dưới biên 0. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":24}; unexpected_rows=[{"id":24,"code":"FR17-DT-21","type":"percent","discount_value":10,"min_order_amount":-1,"expired_at":"2099-12-31","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-21.log`
- **Cleanup:** DELETE /api/admin/coupons/24 -> HTTP 200
- **Bug liên quan:** BUG-FR17-05
- **Ghi chú:** UI type=number không có min nên nhập được -1.

### EV-FR17-022 — DT-22 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-22 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P22, R6 |
| Thời điểm | 2026-10-20T15:38:26.934Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; bỏ hẳn key min_order_amount; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-22",
  "type": "percent",
  "discount_value": 10,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 25
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 25,
      "code": "FR17-DT-22",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": null,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 25,
    "code": "FR17-DT-22",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": null,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; min_order_amount là trường bắt buộc. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":25}; unexpected_rows=[{"id":25,"code":"FR17-DT-22","type":"percent","discount_value":10,"min_order_amount":null,"expired_at":"2099-12-31","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-22.log`
- **Cleanup:** DELETE /api/admin/coupons/25 -> HTTP 200
- **Bug liên quan:** BUG-FR17-05
- **Ghi chú:** UI luôn gửi key min_order_amount (có thể là chuỗi rỗng), nên ca bỏ hẳn key là API-only.

### EV-FR17-023 — DT-23 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-23 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P23, R6 |
| Thời điểm | 2026-10-20T15:38:26.941Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; min_order_amount='abc'; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-23",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": "abc",
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 26
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 26,
      "code": "FR17-DT-23",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": "abc",
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 26,
    "code": "FR17-DT-23",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": "abc",
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; min_order_amount phải là số >= 0. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":26}; unexpected_rows=[{"id":26,"code":"FR17-DT-23","type":"percent","discount_value":10,"min_order_amount":"abc","expired_at":"2099-12-31","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-23.log`
- **Cleanup:** DELETE /api/admin/coupons/26 -> HTTP 200
- **Bug liên quan:** BUG-FR17-05
- **Ghi chú:** UI type=number không gửi được abc; ca này API-only.

### EV-FR17-024 — DT-24 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-24 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP + BVA |
| Obligation IDs | P24, B2-ON, R6 |
| Thời điểm | 2026-10-20T15:38:26.949Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; max_uses_per_user=1; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-24",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 27
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 27,
      "code": "FR17-DT-24",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 27,
    "code": "FR17-DT-24",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": [
    {
      "field": "code",
      "expected": "FR17-DT-24",
      "actual": "FR17-DT-24",
      "pass": true
    },
    {
      "field": "type",
      "expected": "percent",
      "actual": "percent",
      "pass": true
    },
    {
      "field": "discount_value",
      "expected": 10,
      "actual": 10,
      "pass": true
    },
    {
      "field": "min_order_amount",
      "expected": 100000,
      "actual": 100000,
      "pass": true
    },
    {
      "field": "expired_at",
      "expected": "2099-12-31",
      "actual": "2099-12-31",
      "pass": true
    },
    {
      "field": "max_uses_per_user",
      "expected": 1,
      "actual": 1,
      "pass": true
    }
  ],
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Tạo thành công (2xx); max_uses_per_user=1 thỏa >= 1 (điểm biên ON hợp lệ). Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; target={"id":27,"code":"FR17-DT-24","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","is_active":1,"max_uses_per_user":1}; field_checks=[{"field":"code","expected":"FR17-DT-24","actual":"FR17-DT-24","pass":true},{"field":"type","expected":"percent","actual":"percent","pass":true},{"field":"discount_value","expected":10,"actual":10,"pass":true},{"field":"min_order_amount","expected":100000,"actual":100000,"pass":true},{"field":"expired_at","expected":"2099-12-31","actual":"2099-12-31","pass":true},{"field":"max_uses_per_user","expected":1,"actual":1,"pass":true}]
- **Status:** `PASS`
- **Artifact:** `evidence/DT-24.log`
- **Cleanup:** DELETE /api/admin/coupons/27 -> HTTP 200
- **Bug liên quan:** không
- **Ghi chú:** UI min=1 cho phép 1.

### EV-FR17-025 — DT-25 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-25 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP + BVA |
| Obligation IDs | P25, B2-above, R6 |
| Thời điểm | 2026-10-20T15:38:26.955Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; max_uses_per_user=2; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-25",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 2
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 28
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 28,
      "code": "FR17-DT-25",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 2,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 28,
    "code": "FR17-DT-25",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 2
  },
  "field_checks": [
    {
      "field": "code",
      "expected": "FR17-DT-25",
      "actual": "FR17-DT-25",
      "pass": true
    },
    {
      "field": "type",
      "expected": "percent",
      "actual": "percent",
      "pass": true
    },
    {
      "field": "discount_value",
      "expected": 10,
      "actual": 10,
      "pass": true
    },
    {
      "field": "min_order_amount",
      "expected": 100000,
      "actual": 100000,
      "pass": true
    },
    {
      "field": "expired_at",
      "expected": "2099-12-31",
      "actual": "2099-12-31",
      "pass": true
    },
    {
      "field": "max_uses_per_user",
      "expected": 2,
      "actual": 2,
      "pass": true
    }
  ],
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Tạo thành công (2xx); max_uses_per_user=2 thỏa >= 1 (điểm ngay trên biên 1). Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; target={"id":28,"code":"FR17-DT-25","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","is_active":1,"max_uses_per_user":2}; field_checks=[{"field":"code","expected":"FR17-DT-25","actual":"FR17-DT-25","pass":true},{"field":"type","expected":"percent","actual":"percent","pass":true},{"field":"discount_value","expected":10,"actual":10,"pass":true},{"field":"min_order_amount","expected":100000,"actual":100000,"pass":true},{"field":"expired_at","expected":"2099-12-31","actual":"2099-12-31","pass":true},{"field":"max_uses_per_user","expected":2,"actual":2,"pass":true}]
- **Status:** `PASS`
- **Artifact:** `evidence/DT-25.log`
- **Cleanup:** DELETE /api/admin/coupons/28 -> HTTP 200
- **Bug liên quan:** không
- **Ghi chú:** UI min=1 cho phép 2.

### EV-FR17-026 — DT-26 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-26 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP + BVA |
| Obligation IDs | P26, B2-below, R6 |
| Thời điểm | 2026-10-20T15:38:26.963Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; max_uses_per_user=0; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-26",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 0
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 29
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 29,
      "code": "FR17-DT-26",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 29,
    "code": "FR17-DT-26",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; max_uses_per_user phải >= 1. 0 là điểm ngay dưới biên 1. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":29}; unexpected_rows=[{"id":29,"code":"FR17-DT-26","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-26.log`
- **Cleanup:** DELETE /api/admin/coupons/29 -> HTTP 200
- **Bug liên quan:** BUG-FR17-06
- **Ghi chú:** UI min=1 chặn submit 0; ca này API-only. Backend dùng max_uses_per_user || 1 nên cần kiểm tra giá trị lưu thực tế.

### EV-FR17-027 — DT-27 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-27 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P27, R6 |
| Thời điểm | 2026-10-20T15:38:26.968Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; max_uses_per_user=-1; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-27",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": -1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 30
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 30,
      "code": "FR17-DT-27",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": -1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 30,
    "code": "FR17-DT-27",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": -1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; max_uses_per_user phải >= 1. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":30}; unexpected_rows=[{"id":30,"code":"FR17-DT-27","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":-1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-27.log`
- **Cleanup:** DELETE /api/admin/coupons/30 -> HTTP 200
- **Bug liên quan:** BUG-FR17-06
- **Ghi chú:** UI min=1 chặn submit -1; ca này API-only.

### EV-FR17-028 — DT-28 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-28 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P28, R6 |
| Thời điểm | 2026-10-20T15:38:26.974Z (2026-10-20 22:38:26 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; bỏ hẳn key max_uses_per_user; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-28",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31"
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 31
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 31,
      "code": "FR17-DT-28",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 31,
    "code": "FR17-DT-28",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Bị từ chối (non-2xx) và không tạo coupon mới; max_uses_per_user là trường bắt buộc. Nguồn: README.md §5 FR-17.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":31}; unexpected_rows=[{"id":31,"code":"FR17-DT-28","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-28.log`
- **Cleanup:** DELETE /api/admin/coupons/31 -> HTTP 200
- **Bug liên quan:** BUG-FR17-06
- **Ghi chú:** UI luôn gửi key max_uses_per_user (có thể là chuỗi rỗng), nên ca bỏ hẳn key là API-only.

### EV-FR17-029 — DT-29 (API GET /api/coupons (sau khi POST tạo coupon))

| Trường | Giá trị |
| --- | --- |
| Test case | DT-29 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P29, R1, R7 |
| Thời điểm | 2026-10-20T15:38:26.983Z (2026-10-20 22:38:26 +0700) |
| Interface | API GET /api/coupons (sau khi POST tạo coupon) |
| Setup / trạng thái trước | Đăng nhập admin; DB test có 4 seed coupon; tạo coupon FR17-DT-29 rồi gọi GET /api/coupons. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-29",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 32
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 32,
      "code": "FR17-DT-29",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 32,
    "code": "FR17-DT-29",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": [
    {
      "field": "code",
      "expected": "FR17-DT-29",
      "actual": "FR17-DT-29",
      "pass": true
    },
    {
      "field": "type",
      "expected": "percent",
      "actual": "percent",
      "pass": true
    },
    {
      "field": "discount_value",
      "expected": 10,
      "actual": 10,
      "pass": true
    },
    {
      "field": "min_order_amount",
      "expected": 100000,
      "actual": 100000,
      "pass": true
    },
    {
      "field": "expired_at",
      "expected": "2099-12-31",
      "actual": "2099-12-31",
      "pass": true
    },
    {
      "field": "max_uses_per_user",
      "expected": 1,
      "actual": 1,
      "pass": true
    }
  ],
  "seeds_present": {
    "before": true,
    "after": true
  },
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** GET /api/coupons trả danh sách nhìn thấy được, gồm 4 seed coupon và coupon vừa tạo với đủ trường đúng giá trị. Nguồn: README.md §5 FR-17 (Xem); api_specification.md §5.2.
- **Actual:** POST HTTP 200; before_count=4; after_count=5; seeds_before=true; seeds_after=true; target={"id":32,"code":"FR17-DT-29","type":"percent","discount_value":10,"min_order_amount":100000,"expired_at":"2099-12-31","is_active":1,"max_uses_per_user":1}; field_checks=[{"field":"code","expected":"FR17-DT-29","actual":"FR17-DT-29","pass":true},{"field":"type","expected":"percent","actual":"percent","pass":true},{"field":"discount_value","expected":10,"actual":10,"pass":true},{"field":"min_order_amount","expected":100000,"actual":100000,"pass":true},{"field":"expired_at","expected":"2099-12-31","actual":"2099-12-31","pass":true},{"field":"max_uses_per_user","expected":1,"actual":1,"pass":true}]
- **Status:** `PASS`
- **Artifact:** `evidence/DT-29.log`
- **Cleanup:** DELETE /api/admin/coupons/32 -> HTTP 200
- **Bug liên quan:** không
- **Ghi chú:** Ca này kiểm tra yêu cầu Xem danh sách; không kiểm tra thứ tự hiển thị vì đặc tả không quy định.

### EV-FR17-030 — DT-30 (API DELETE /api/admin/coupons/:id + GET /api/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-30 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P30, R8 |
| Thời điểm | 2026-10-20T15:38:26.990Z (2026-10-20 22:38:26 +0700) |
| Interface | API DELETE /api/admin/coupons/:id + GET /api/coupons |
| Setup / trạng thái trước | Đăng nhập admin; tạo coupon FR17-DT-30 rồi xóa theo id. |

**Request thật:**

```http
DELETE /api/admin/coupons/33
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

(no body)
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon deleted"
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 4,
  "new_rows": [
    {
      "id": 33,
      "code": "FR17-DT-30",
      "type": "percent",
      "discount_value": 10,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 33,
    "code": "FR17-DT-30",
    "type": "percent",
    "discount_value": 10,
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": true
}
```

- **Expected (oracle ref):** Xóa coupon đang tồn tại thành công (2xx) và coupon biến mất khỏi GET /api/coupons. Nguồn: README.md §5 FR-17 (Xóa); api_specification.md §6.4.
- **Actual:** POST create HTTP 200; DELETE HTTP 200; body={"message":"Coupon deleted"}; still_present=false; after_delete_count=4
- **Status:** `PASS`
- **Artifact:** `evidence/DT-30.log`
- **Cleanup:** row đã bị xóa bởi chính ca test
- **Bug liên quan:** không
- **Ghi chú:** Không kiểm tra confirm dialog vì đặc tả FR-17 không yêu cầu.

### EV-FR17-031 — DT-31 (API DELETE /api/admin/coupons/:id)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-31 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P31 |
| Thời điểm | 2026-10-20T15:38:26.994Z (2026-10-20 22:38:26 +0700) |
| Interface | API DELETE /api/admin/coupons/:id |
| Setup / trạng thái trước | Đăng nhập admin; DB test không có coupon id 999999; gọi DELETE /api/admin/coupons/999999. |

**Request thật:**

```http
DELETE /api/admin/coupons/999999
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

(no body)
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon deleted"
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 4,
  "new_rows": [],
  "target_row": null,
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": true
}
```

- **Expected (oracle ref):** Chưa xác định — FR-17 yêu cầu Admin có thể Xóa mã giảm giá nhưng không quy định hành vi khi id không tồn tại. Đây là Quan sát/INCONCLUSIVE.
- **Actual:** HTTP 200; body={"message":"Coupon deleted"}; before_count=4; after_count=4
- **Status:** `INCONCLUSIVE`
- **Artifact:** `evidence/DT-31.log`
- **Cleanup:** không tạo tài nguyên
- **Bug liên quan:** không
- **Ghi chú:** Quan sát status/body thực tế; không chấm PASS/FAIL vì thiếu oracle. Nếu thấy 2xx thì ghi nhận như một điểm cần người kiểm thử quyết định.

### EV-FR17-032 — DT-32 (API POST /api/admin/coupons)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-32 |
| Run ID / lần thử | run-20261020-fr17 / 1 |
| Kỹ thuật | EP |
| Obligation IDs | P32, R4 |
| Thời điểm | 2026-10-20T15:38:27.002Z (2026-10-20 22:38:27 +0700) |
| Interface | API POST /api/admin/coupons |
| Setup / trạng thái trước | Đăng nhập admin; type=percent, discount_value=150; các trường còn lại hợp lệ. |

**Request thật:**

```http
POST /api/admin/coupons
Authorization: Bearer <redacted-test-token>
Content-Type: application/json

{
  "code": "FR17-DT-32",
  "type": "percent",
  "discount_value": 150,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

**Kết quả thô:**

```json
HTTP 200
{
  "message": "Coupon created",
  "id": 34
}
```

**Kiểm tra qua `GET /api/coupons`:**

```json
{
  "before_count": 4,
  "after_count": 5,
  "new_rows": [
    {
      "id": 34,
      "code": "FR17-DT-32",
      "type": "percent",
      "discount_value": 150,
      "min_order_amount": 100000,
      "expired_at": "2099-12-31",
      "max_uses_per_user": 1,
      "is_active": 1
    }
  ],
  "target_row": {
    "id": 34,
    "code": "FR17-DT-32",
    "type": "percent",
    "discount_value": 150,
    "min_order_amount": 100000,
    "expired_at": "2099-12-31",
    "is_active": 1,
    "max_uses_per_user": 1
  },
  "field_checks": null,
  "seeds_present": null,
  "absent_after_delete": null
}
```

- **Expected (oracle ref):** Từ chối (non-2xx) và không tạo coupon mới; với `type = percent`, `discount_value` không được vượt quá `100`, nên `150` không hợp lệ (người kiểm thử xác nhận 2026-10-21). Nguồn: R4.
- **Actual:** HTTP 200; new_rows=1; body={"message":"Coupon created","id":34}; new_rows_data=[{"id":34,"code":"FR17-DT-32","type":"percent","discount_value":150,"min_order_amount":100000,"expired_at":"2099-12-31","max_uses_per_user":1,"is_active":1}]
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-32.log`
- **Cleanup:** DELETE /api/admin/coupons/34 -> HTTP 200
- **Bug liên quan:** BUG-FR17-08
- **Screenshot:** [POST discount 150](../screenshots/BUG-FR17-08-Discount150.png), [GET discount 150](../screenshots/BUG-FR17-08-GetDiscount150.png); ảnh chụp lần chạy lại có row `id=6` thay vì `id=34` trong log, cùng request/response.
- **Ghi chú:** UI không có max nên người dùng nhập được 150; finding mới xác nhận qua API. Upper bound 100 do người kiểm thử xác nhận ngày 2026-10-21.
