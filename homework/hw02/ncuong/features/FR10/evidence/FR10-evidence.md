# FR10 — Evidence log (nhật ký bằng chứng thực thi)

> Mỗi lần thử một test case có một mục `EV-ID`; rerun dùng `EV-ID` mới, giữ lịch sử. Kết quả thô quan sát được, không chép Expected vào Actual.

## Thông tin phiên chạy

| Mục | Giá trị |
| --- | --- |
| Feature | FR-10 — Trạng thái Đơn hàng (Order State Machine) |
| Interface | API `PUT /api/admin/orders/:id/status` (admin), `PUT /api/orders/:id/cancel` (user), quan sát bằng `GET /api/orders/:id` |
| SUT / build | `eshop-sut-homework` commit `09a950cf451428bd8f54542b3f11a0e4b6fdaa91` |
| Môi trường | macOS; Node v26.9.0; backend Node/Express + SQLite; instance cách ly (bản sao `server.js`/`database.js`, `database.sqlite` riêng, `node_modules` symlink) |
| Thời điểm chạy | 2026-10-19T19:56:44.073Z → 2026-10-19T19:56:44.174Z (UTC) |
| Người/agent thực thi | AI agent (theo skill `domain-testing-workflow`); screenshot Issue: người kiểm thử chụp sau khi xác nhận bug |
| Thư mục evidence | `evidence/` |
| Cách reset state | Mỗi ca tạo một đơn mới qua `POST /api/checkout` (user `test@eshop.com`) rồi đưa về trạng thái nguồn bằng chính API admin (các chuyển đổi hợp lệ) |
| Database làm việc trước khi chạy | `backend/database.sqlite`, SHA-256 `c63f00544180ba1fbb1427a9b9dd3f1784842698809972f33ce90482e7420ba6` |
| Database test | `database.sqlite` trong thư mục SUT tạm, tạo mới từ `database.js` khi khởi động server |

**Fixture:** tài khoản seed `admin@eshop.com` / `Admin123!` (role admin) và `test@eshop.com` / `Test1234!` (role user); đơn hàng tạo tại thời điểm chạy.

**Trình điều khiển (driver):** `evidence/run-fr10.mjs` (chạy các ca, ghi `ev` log và `run-summary.json`); thao tác tương đương bằng `curl` nêu trong từng mục.

## Evidence items

### EV-FR10-001 — DT-01 admin pending→confirmed (được phép)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-01 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP |
| Thời điểm | 2026-10-19T19:56:44.073Z (UTC) |
| Interface | API `PUT /api/admin/orders/1/status` |
| Tiền điều kiện / reset state | order id 1; status trước = `pending` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/admin/orders/1/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"confirmed"}'
```

**Kết quả thô:**
```json
{
  "message": "Order status updated"
}
```
```text
HTTP 200 · pre-state status=pending · post-state status=confirmed
```

- **Expected (oracle ref):** Thành công (2xx) và status = "confirmed".
- **Actual:** HTTP 200; status sau = `confirmed`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-01.log`
- **Bug liên quan:** không.
- **Ghi chú:** —

---

### EV-FR10-002 — DT-02 admin confirmed→shipping (được phép)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-02 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP |
| Thời điểm | 2026-10-19T19:56:44.082Z (UTC) |
| Interface | API `PUT /api/admin/orders/2/status` |
| Tiền điều kiện / reset state | order id 2; status trước = `confirmed` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/admin/orders/2/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"shipping"}'
```

**Kết quả thô:**
```json
{
  "message": "Order status updated"
}
```
```text
HTTP 200 · pre-state status=confirmed · post-state status=shipping
```

- **Expected (oracle ref):** Thành công (2xx) và status = "shipping".
- **Actual:** HTTP 200; status sau = `shipping`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-02.log`
- **Bug liên quan:** không.
- **Ghi chú:** —

---

### EV-FR10-003 — DT-03 admin shipping→delivered (được phép, tiến vào terminal delivered)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-03 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP + BVA |
| Thời điểm | 2026-10-19T19:56:44.090Z (UTC) |
| Interface | API `PUT /api/admin/orders/3/status` |
| Tiền điều kiện / reset state | order id 3; status trước = `shipping` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/admin/orders/3/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"delivered"}'
```

**Kết quả thô:**
```json
{
  "message": "Order status updated"
}
```
```text
HTTP 200 · pre-state status=shipping · post-state status=delivered
```

- **Expected (oracle ref):** Thành công (2xx) và status = "delivered".
- **Actual:** HTTP 200; status sau = `delivered`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-03.log`
- **Bug liên quan:** không.
- **Ghi chú:** —

---

### EV-FR10-004 — DT-04 admin pending→canceled (được phép, tiến vào terminal canceled)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-04 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP + BVA |
| Thời điểm | 2026-10-19T19:56:44.093Z (UTC) |
| Interface | API `PUT /api/admin/orders/4/status` |
| Tiền điều kiện / reset state | order id 4; status trước = `pending` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/admin/orders/4/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"canceled"}'
```

**Kết quả thô:**
```json
{
  "message": "Order status updated"
}
```
```text
HTTP 200 · pre-state status=pending · post-state status=canceled
```

- **Expected (oracle ref):** Thành công (2xx) và status = "canceled".
- **Actual:** HTTP 200; status sau = `canceled`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-04.log`
- **Bug liên quan:** không.
- **Ghi chú:** —

---

### EV-FR10-005 — DT-05 admin confirmed→canceled (được phép, tiến vào terminal canceled)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-05 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP + BVA |
| Thời điểm | 2026-10-19T19:56:44.099Z (UTC) |
| Interface | API `PUT /api/admin/orders/5/status` |
| Tiền điều kiện / reset state | order id 5; status trước = `confirmed` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/admin/orders/5/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"canceled"}'
```

**Kết quả thô:**
```json
{
  "message": "Order status updated"
}
```
```text
HTTP 200 · pre-state status=confirmed · post-state status=canceled
```

- **Expected (oracle ref):** Thành công (2xx) và status = "canceled".
- **Actual:** HTTP 200; status sau = `canceled`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-05.log`
- **Bug liên quan:** không.
- **Ghi chú:** —

---

### EV-FR10-006 — DT-06 user hủy đơn pending (được phép, B1 dưới biên)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-06 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP + BVA |
| Thời điểm | 2026-10-19T19:56:44.102Z (UTC) |
| Interface | API `PUT /api/orders/6/cancel` |
| Tiền điều kiện / reset state | order id 6; status trước = `pending` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/orders/6/cancel \
  -H "Authorization: Bearer $USER_TOKEN"
```

**Kết quả thô:**
```json
{
  "message": "Order canceled successfully"
}
```
```text
HTTP 200 · pre-state status=pending · post-state status=canceled
```

- **Expected (oracle ref):** Thành công (2xx) và status = "canceled".
- **Actual:** HTTP 200; status sau = `canceled`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-06.log`
- **Bug liên quan:** không.
- **Ghi chú:** —

---

### EV-FR10-007 — DT-07 user hủy đơn confirmed (được phép, B1 tại biên)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-07 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP + BVA |
| Thời điểm | 2026-10-19T19:56:44.107Z (UTC) |
| Interface | API `PUT /api/orders/7/cancel` |
| Tiền điều kiện / reset state | order id 7; status trước = `confirmed` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/orders/7/cancel \
  -H "Authorization: Bearer $USER_TOKEN"
```

**Kết quả thô:**
```json
{
  "message": "Order canceled successfully"
}
```
```text
HTTP 200 · pre-state status=confirmed · post-state status=canceled
```

- **Expected (oracle ref):** Thành công (2xx) và status = "canceled".
- **Actual:** HTTP 200; status sau = `canceled`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-07.log`
- **Bug liên quan:** không.
- **Ghi chú:** —

---

### EV-FR10-008 — DT-08 admin pending→shipping (skip, phải bị từ chối)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-08 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP |
| Thời điểm | 2026-10-19T19:56:44.109Z (UTC) |
| Interface | API `PUT /api/admin/orders/8/status` |
| Tiền điều kiện / reset state | order id 8; status trước = `pending` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/admin/orders/8/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"shipping"}'
```

**Kết quả thô:**
```json
{
  "error": "Invalid state transition from pending to shipping"
}
```
```text
HTTP 400 · pre-state status=pending · post-state status=pending
```

- **Expected (oracle ref):** Lỗi (không 2xx), status giữ nguyên "pending".
- **Actual:** HTTP 400; status sau = `pending`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-08.log`
- **Bug liên quan:** không.
- **Ghi chú:** —

---

### EV-FR10-009 — DT-09 admin confirmed→delivered (skip, phải bị từ chối)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-09 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP |
| Thời điểm | 2026-10-19T19:56:44.113Z (UTC) |
| Interface | API `PUT /api/admin/orders/9/status` |
| Tiền điều kiện / reset state | order id 9; status trước = `confirmed` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/admin/orders/9/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"delivered"}'
```

**Kết quả thô:**
```json
{
  "error": "Invalid state transition from confirmed to delivered"
}
```
```text
HTTP 400 · pre-state status=confirmed · post-state status=confirmed
```

- **Expected (oracle ref):** Lỗi (không 2xx), status giữ nguyên "confirmed".
- **Actual:** HTTP 400; status sau = `confirmed`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-09.log`
- **Bug liên quan:** không.
- **Ghi chú:** —

---

### EV-FR10-010 — DT-10 admin confirmed→pending (lùi, phải bị từ chối)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-10 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP |
| Thời điểm | 2026-10-19T19:56:44.118Z (UTC) |
| Interface | API `PUT /api/admin/orders/10/status` |
| Tiền điều kiện / reset state | order id 10; status trước = `confirmed` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/admin/orders/10/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"pending"}'
```

**Kết quả thô:**
```json
{
  "error": "Invalid state transition from confirmed to pending"
}
```
```text
HTTP 400 · pre-state status=confirmed · post-state status=confirmed
```

- **Expected (oracle ref):** Lỗi (không 2xx), status giữ nguyên "confirmed".
- **Actual:** HTTP 400; status sau = `confirmed`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-10.log`
- **Bug liên quan:** không.
- **Ghi chú:** —

---

### EV-FR10-011 — DT-11 admin shipping→confirmed (lùi, phải bị từ chối)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-11 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP |
| Thời điểm | 2026-10-19T19:56:44.122Z (UTC) |
| Interface | API `PUT /api/admin/orders/11/status` |
| Tiền điều kiện / reset state | order id 11; status trước = `shipping` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/admin/orders/11/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"confirmed"}'
```

**Kết quả thô:**
```json
{
  "error": "Invalid state transition from shipping to confirmed"
}
```
```text
HTTP 400 · pre-state status=shipping · post-state status=shipping
```

- **Expected (oracle ref):** Lỗi (không 2xx), status giữ nguyên "shipping".
- **Actual:** HTTP 400; status sau = `shipping`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-11.log`
- **Bug liên quan:** không.
- **Ghi chú:** —

---

### EV-FR10-012 — DT-12 admin pending→pending (trùng trạng thái, phải bị từ chối)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-12 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP |
| Thời điểm | 2026-10-19T19:56:44.125Z (UTC) |
| Interface | API `PUT /api/admin/orders/12/status` |
| Tiền điều kiện / reset state | order id 12; status trước = `pending` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/admin/orders/12/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"pending"}'
```

**Kết quả thô:**
```json
{
  "error": "Invalid state transition from pending to pending"
}
```
```text
HTTP 400 · pre-state status=pending · post-state status=pending
```

- **Expected (oracle ref):** Lỗi (không 2xx), status giữ nguyên "pending".
- **Actual:** HTTP 400; status sau = `pending`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-12.log`
- **Bug liên quan:** không.
- **Ghi chú:** —

---

### EV-FR10-013 — DT-13 admin delivered→shipping (rời terminal delivered, phải bị từ chối)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-13 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP + BVA |
| Thời điểm | 2026-10-19T19:56:44.136Z (UTC) |
| Interface | API `PUT /api/admin/orders/13/status` |
| Tiền điều kiện / reset state | order id 13; status trước = `delivered` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/admin/orders/13/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"shipping"}'
```

**Kết quả thô:**
```json
{
  "error": "Invalid state transition from delivered to shipping"
}
```
```text
HTTP 400 · pre-state status=delivered · post-state status=delivered
```

- **Expected (oracle ref):** Lỗi (không 2xx), status giữ nguyên "delivered".
- **Actual:** HTTP 400; status sau = `delivered`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-13.log`
- **Bug liên quan:** không.
- **Ghi chú:** —

---

### EV-FR10-014 — DT-14 admin canceled→delivered (rời terminal canceled, phải bị từ chối) — FAIL

| Trường | Giá trị |
| --- | --- |
| Test case | DT-14 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP + BVA |
| Thời điểm | 2026-10-19T19:56:44.140Z (UTC) |
| Interface | API `PUT /api/admin/orders/14/status` |
| Tiền điều kiện / reset state | order id 14; status trước = `canceled` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/admin/orders/14/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"delivered"}'
```

**Kết quả thô:**
```json
{
  "message": "Order status updated"
}
```
```text
HTTP 200 · pre-state status=canceled · post-state status=delivered
```

- **Expected (oracle ref):** Lỗi (không 2xx), status giữ nguyên "canceled".
- **Actual:** HTTP 200; status sau = `delivered`.
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-14.log`
- **Bug liên quan:** BUG-FR10-01 (ứng viên).
- **Ghi chú:** Bug ứng viên BUG-FR10-01 (canceled là trạng thái kết thúc)

---

### EV-FR10-015 — DT-15 admin status đích không hợp lệ 'shipped' (phải bị từ chối)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-15 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP |
| Thời điểm | 2026-10-19T19:56:44.143Z (UTC) |
| Interface | API `PUT /api/admin/orders/15/status` |
| Tiền điều kiện / reset state | order id 15; status trước = `pending` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/admin/orders/15/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"shipped"}'
```

**Kết quả thô:**
```json
{
  "error": "Invalid state transition from pending to shipped"
}
```
```text
HTTP 400 · pre-state status=pending · post-state status=pending
```

- **Expected (oracle ref):** Lỗi (không 2xx), status giữ nguyên "pending".
- **Actual:** HTTP 400; status sau = `pending`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-15.log`
- **Bug liên quan:** không.
- **Ghi chú:** —

---

### EV-FR10-016 — DT-16 user hủy đơn shipping (phải bị từ chối) — FAIL

| Trường | Giá trị |
| --- | --- |
| Test case | DT-16 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP + BVA |
| Thời điểm | 2026-10-19T19:56:44.149Z (UTC) |
| Interface | API `PUT /api/orders/16/cancel` |
| Tiền điều kiện / reset state | order id 16; status trước = `shipping` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/orders/16/cancel \
  -H "Authorization: Bearer $USER_TOKEN"
```

**Kết quả thô:**
```json
{
  "message": "Order canceled successfully"
}
```
```text
HTTP 200 · pre-state status=shipping · post-state status=canceled
```

- **Expected (oracle ref):** Lỗi (không 2xx), status giữ nguyên "shipping".
- **Actual:** HTTP 200; status sau = `canceled`.
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-16.log`
- **Bug liên quan:** BUG-FR10-02 (ứng viên).
- **Ghi chú:** Bug ứng viên BUG-FR10-02 (User tự hủy khi shipping)

---

### EV-FR10-017 — DT-17 user hủy đơn delivered (phải bị từ chối)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-17 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP + BVA |
| Thời điểm | 2026-10-19T19:56:44.156Z (UTC) |
| Interface | API `PUT /api/orders/17/cancel` |
| Tiền điều kiện / reset state | order id 17; status trước = `delivered` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/orders/17/cancel \
  -H "Authorization: Bearer $USER_TOKEN"
```

**Kết quả thô:**
```json
{
  "error": "Cannot cancel this order."
}
```
```text
HTTP 400 · pre-state status=delivered · post-state status=delivered
```

- **Expected (oracle ref):** Lỗi (không 2xx), status giữ nguyên "delivered".
- **Actual:** HTTP 400; status sau = `delivered`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-17.log`
- **Bug liên quan:** không.
- **Ghi chú:** —

---

### EV-FR10-018 — DT-18 user hủy đơn canceled (phải bị từ chối)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-18 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP |
| Thời điểm | 2026-10-19T19:56:44.159Z (UTC) |
| Interface | API `PUT /api/orders/18/cancel` |
| Tiền điều kiện / reset state | order id 18; status trước = `canceled` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/orders/18/cancel \
  -H "Authorization: Bearer $USER_TOKEN"
```

**Kết quả thô:**
```json
{
  "error": "Cannot cancel this order."
}
```
```text
HTTP 400 · pre-state status=canceled · post-state status=canceled
```

- **Expected (oracle ref):** Lỗi (không 2xx), status giữ nguyên "canceled".
- **Actual:** HTTP 400; status sau = `canceled`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-18.log`
- **Bug liên quan:** không.
- **Ghi chú:** —

---

### EV-FR10-019 — DT-19 admin cập nhật đơn không tồn tại id 999999 (phải lỗi 404)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-19 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP |
| Thời điểm | 2026-10-19T19:56:44.160Z (UTC) |
| Interface | API `PUT /api/admin/orders/999999/status` (đơn không tồn tại) |
| Tiền điều kiện / reset state | order id 999999; status trước = `N/A (không tồn tại)` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/admin/orders/999999/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"confirmed"}'
```

**Kết quả thô:**
```json
{
  "error": "Order not found"
}
```
```text
HTTP 404 · pre-state status=N/A (không tồn tại) · post-state status=N/A
```

- **Expected (oracle ref):** Lỗi (không 2xx), status giữ nguyên "N/A (không tồn tại)".
- **Actual:** HTTP 404; status sau = `N/A`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-19.log`, `evidence/DT-19-variants.log`
- **Bug liên quan:** không.
- **Ghi chú:** Đơn id 999999 không tồn tại (admin)

---

### EV-FR10-020 — DT-20 admin shipping→canceled (ASSUMED: phải bị từ chối)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-20 |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP |
| Thời điểm | 2026-10-19T19:56:44.164Z (UTC) |
| Interface | API `PUT /api/admin/orders/19/status` |
| Tiền điều kiện / reset state | order id 19; status trước = `shipping` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/admin/orders/19/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"canceled"}'
```

**Kết quả thô:**
```json
{
  "error": "Invalid state transition from shipping to canceled"
}
```
```text
HTTP 400 · pre-state status=shipping · post-state status=shipping
```

- **Expected (oracle ref):** Lỗi (không 2xx), status giữ nguyên "shipping".
- **Actual:** HTTP 400; status sau = `shipping`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-20.log`
- **Bug liên quan:** không.
- **Ghi chú:** ASSUMED theo sơ đồ FR-10 (không có cung shipping→canceled)

---

### EV-FR10-021 — DT-14-rerun rerun admin canceled→delivered (độ lặp lại BUG-FR10-01)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-14-rerun |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP |
| Thời điểm | 2026-10-19T19:56:44.168Z (UTC) |
| Interface | API `PUT /api/admin/orders/20/status` |
| Tiền điều kiện / reset state | order id 20; status trước = `canceled` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/admin/orders/20/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"delivered"}'
```

**Kết quả thô:**
```json
{
  "message": "Order status updated"
}
```
```text
HTTP 200 · pre-state status=canceled · post-state status=delivered
```

- **Expected (oracle ref):** Lỗi (không 2xx), status giữ nguyên "canceled".
- **Actual:** HTTP 200; status sau = `delivered`.
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-14-rerun.log`
- **Bug liên quan:** BUG-FR10-01 (ứng viên).
- **Ghi chú:** Rerun độ lặp lại BUG-FR10-01

---

### EV-FR10-022 — DT-16-rerun rerun user hủy đơn shipping (độ lặp lại BUG-FR10-02)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-16-rerun |
| Run ID / lần thử | run-20261020-fr10 / 1 |
| Kỹ thuật | EP |
| Thời điểm | 2026-10-19T19:56:44.174Z (UTC) |
| Interface | API `PUT /api/orders/21/cancel` |
| Tiền điều kiện / reset state | order id 21; status trước = `shipping` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X PUT http://localhost:3000/api/orders/21/cancel \
  -H "Authorization: Bearer $USER_TOKEN"
```

**Kết quả thô:**
```json
{
  "message": "Order canceled successfully"
}
```
```text
HTTP 200 · pre-state status=shipping · post-state status=canceled
```

- **Expected (oracle ref):** Lỗi (không 2xx), status giữ nguyên "shipping".
- **Actual:** HTTP 200; status sau = `canceled`.
- **Status:** `FAIL`
- **Artifact:** `evidence/DT-16-rerun.log`
- **Bug liên quan:** BUG-FR10-02 (ứng viên).
- **Ghi chú:** Rerun độ lặp lại BUG-FR10-02

---

### EV-FR10-023 — DT-19 biến thể (đơn không sở hữu)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-19 |
| Run ID / lần thử | run-20261020-fr10 / 2 |
| Kỹ thuật | Domain/EP |
| Thời điểm | 2026-10-19T19:56:44.177Z (UTC) |
| Interface | API `PUT /api/orders/:id/cancel` |
| Tiền điều kiện / reset state | đơn id 22 thuộc user `test@eshop.com`; gọi hủy bằng token admin (user_id=1) |

**Kết quả thô:**
```json
{
  "id": "DT-19-variants",
  "run": "run-20261020-fr10",
  "time": "2026-10-19T19:56:44.177Z",
  "variants": [
    {
      "name": "user cancel non-existent 999999",
      "httpStatus": 404,
      "body": "{\"error\":\"Order not found\"}"
    },
    {
      "name": "user cancel non-owned order (admin token)",
      "orderId": 22,
      "httpStatus": 404,
      "body": "{\"error\":\"Order not found\"}",
      "statusAfter": "pending"
    }
  ]
}
```

- **Expected (oracle ref):** đơn không tồn tại / không thuộc người gọi ⇒ lỗi, không đổi trạng thái.
- **Actual:** cả hai biến thể trả `404 {"error":"Order not found"}`; đơn id 22 giữ `pending`.
- **Status:** `PASS`
- **Artifact:** `evidence/DT-19-variants.log`
- **Bug liên quan:** không.

---

## Xác nhận qua UI (người kiểm thử thực hiện)

> Hai mục dưới đây là **bằng chứng xác nhận độc lập bằng UI** do người kiểm thử chạy trên môi trường làm việc, kèm screenshot. Chúng không thay thế các EV chạy API ở trên; T-ID tương ứng vẫn là DT-14 và DT-16.

### EV-FR10-024 — DT-14 xác nhận qua UI: Admin bấm "Đánh dấu Đã giao" trên đơn Đã hủy

| Trường | Giá trị |
| --- | --- |
| Test case | DT-14 (đồng thời BVA B3) |
| Run ID / lần thử | xác nhận UI / 1 |
| Kỹ thuật | UI confirmation |
| Thời điểm | 2026-10-20 ~11:53–11:55 +0700 (theo thời điểm file ảnh) |
| Interface | Web Admin `http://localhost:5174` → tab "Đơn hàng" → nút "Đánh dấu Đã giao"; đối chiếu Web `http://localhost:5173` → Hồ sơ → "Lịch sử đơn hàng" |
| Tiền điều kiện / reset state | đơn hàng số 1 của `test@eshop.com` đang ở trạng thái "Đã hủy" |

**Kết quả thô (theo ảnh):**
- Trước: đơn hàng số 1 hiển thị "Đã hủy" nhưng vẫn có nút "Đánh dấu Đã giao".
- Sau khi bấm: đơn hàng số 1 hiển thị "Đã giao"; phía user cũng thấy "Đã giao".

- **Expected (oracle ref):** `canceled` là trạng thái kết thúc ⇒ không có thao tác chuyển đi, trạng thái giữ "Đã hủy".
- **Actual:** đơn chuyển "Đã hủy" → "Đã giao" qua UI.
- **Status:** `FAIL` (khớp kết quả API của DT-14)
- **Artifact:** `screenshots/BUG-FR10-01-Cancelled-Admin.png`, `screenshots/BUG-FR10-01-Delivered-Admin.png`, `screenshots/BUG-FR10-01-Delivered-User.png`
- **Bug liên quan:** BUG-FR10-01 — Issue [#33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33).

---

### EV-FR10-025 — DT-16 xác nhận qua UI: User bấm "Hủy đơn" khi đơn Đang giao

| Trường | Giá trị |
| --- | --- |
| Test case | DT-16 (đồng thời BVA B1) |
| Run ID / lần thử | xác nhận UI / 1 |
| Kỹ thuật | UI confirmation |
| Thời điểm | 2026-10-20 ~11:48–11:50 +0700 (theo thời điểm file ảnh) |
| Interface | Web `http://localhost:5173` → Hồ sơ → "Lịch sử đơn hàng" → nút "Hủy đơn"; đối chiếu Web Admin tab "Đơn hàng" |
| Tiền điều kiện / reset state | đơn hàng số 2 của `test@eshop.com` đang ở trạng thái "Đang giao" (admin đã chuyển) |

**Kết quả thô (theo ảnh):**
- Admin: đơn hàng số 2 "Đang giao", chỉ có nút "Hoàn thành".
- User: đơn hàng số 2 "Đang giao" vẫn có nút "Hủy đơn"; bấm → thông báo "Hủy đơn thành công!"; sau đó đơn hiển thị "Đã hủy".

- **Expected (oracle ref):** ở `shipping`, User không được tự hủy ⇒ không có nút hủy / bị từ chối, trạng thái giữ "Đang giao".
- **Actual:** UI cho phép hủy và đơn chuyển "Đang giao" → "Đã hủy".
- **Status:** `FAIL` (khớp kết quả API của DT-16)
- **Artifact:** `screenshots/BUG-FR10-02-Delivering-Admin.png`, `screenshots/BUG-FR10-02-Delivering-User.png`, `screenshots/BUG-FR10-02-Noti-Cancelled-User.png`, `screenshots/BUG-FR10-02-Status-Cancelled-User.png`
- **Bug liên quan:** BUG-FR10-02 — Issue [#34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34).

---

## Tổng hợp evidence

| Chỉ số | Số lượng |
| --- | ---: |
| Ca thiết kế | 23 (20 cốt lõi + 3 quyền bổ sung) |
| Ca đã chạy duy nhất qua các run được chọn | 23 |
| Tổng lần thử thực thi (EV-ID) | 32 (25 cũ + 7 API bổ sung, gồm rerun/đối chứng) |
| PASS | 19 |
| FAIL | 4 |
| Quan sát / Inconclusive | 0 |
| BLOCKED (nêu lý do) | 0 |

- **Artifact thô:** `DT-01.log` … `DT-20.log`, `DT-14-rerun.log`, `DT-16-rerun.log`, `DT-19-variants.log`, `run-summary.json`, `session-header.log`, `run-fr10.mjs`; xác nhận UI: `../screenshots/*.png`; quyền bổ sung: `ev-gap-access-run1.json`, `ev-gap-access-run2.json`, `ev-gap-access-cross.json`.
- **Đối chiếu catalog:** 20 T-ID cũ có EV gốc; DT-21/22/23 có EV bổ sung. DT-01 được chạy lại làm đối chứng (EV-027/030), không tăng T-ID. DT-14/16 và DT-21 có rerun. Không có EV-ID mồ côi.

## Xác nhận cleanup sau khi hoàn tất

| Mục | Kết quả thực tế |
| --- | --- |
| Test services đã dừng | `kill 96828`; `lsof -nP -iTCP:3000 -sTCP:LISTEN` → `PORT3000_FREE` |
| Database test/file tạm đã xóa | `rm -rf /private/.../T/opencode/fr10-sut`; đã kiểm tra không còn thư mục |
| Database làm việc đã trở về trạng thái trước khi chạy | `backend/database.sqlite` SHA-256 vẫn `c63f00544180ba1fbb1427a9b9dd3f1784842698809972f33ce90482e7420ba6` (khớp trước/sau); `git status` không có thay đổi ngoài `features/FR10/` |

## Run bổ sung — AI-GAP-FR10-01

| Mục | Giá trị |
| --- | --- |
| Run ID | `run-20261021-fr10-gap-access` |
| SUT | commit `9955eba27e0e4bf45613649150bf3c2eb681a20f`; backend Node v26.9.0/SQLite bản sao ở `/private/tmp/fr10-gap-run.Trf42g` |
| Interface | `POST /api/login`, `POST /api/checkout`, `PUT /api/admin/orders/:id/status`, `GET /api/orders/:id` trên localhost:3000 |
| Setup/reset | Mỗi lần chạy khởi động bản sao `server.js`/`database.js`, tạo DB test mới; từng ca checkout đơn riêng ở `pending`. Run 2 khởi tạo lại DB, nên cùng id là đơn độc lập. |
| DB làm việc trước run | SHA-256 `c63f00544180ba1fbb1427a9b9dd3f1784842698809972f33ce90482e7420ba6` |

**Lệnh chạy thật** (script test tạm gọi API bằng Node `fetch`; request/response không chứa JWT nguyên văn trong log):

```zsh
node /private/tmp/fr10-gap-run.Trf42g/run.cjs
node /private/tmp/fr10-gap-run.Trf42g/run.cjs
node /private/tmp/fr10-gap-run.Trf42g/run-cross.cjs
```

Mỗi lần chạy lấy token từ đăng nhập seed `admin@eshop.com` hoặc `test@eshop.com`, xác nhận role từ response, rồi tạo đơn mới. Lệnh trên là lệnh phiên test đã chạy; thư mục tạm được dọn sau khi lưu raw log. Để tái hiện thủ công lâu dài, xem [BUG-FR10-03 / Issue #60](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/60).

| EV-ID | T-ID / actor / đơn | Thời điểm UTC | Request thực tế | Before → HTTP/response → After | Verdict / raw log |
| --- | --- | --- | --- | --- | --- |
| EV-FR10-026 | DT-21 / user token / đơn của mình #1 | 2026-10-21 03:00:38 | `PUT /api/admin/orders/1/status`, `{"status":"confirmed"}` | `pending` → 200 `Order status updated` → `confirmed` | **FAIL** · [run 1](ev-gap-access-run1.json) |
| EV-FR10-027 | DT-01 đối chứng / admin token / đơn user #2 | 2026-10-21 03:00:38 | `PUT /api/admin/orders/2/status`, cùng body | `pending` → 200 `Order status updated` → `confirmed` | PASS · [run 1](ev-gap-access-run1.json) |
| EV-FR10-028 | DT-23 / không token / đơn user #3 | 2026-10-21 03:00:38 | `PUT /api/admin/orders/3/status`, cùng body | `pending` → 401 `Unauthorized` → `pending` | PASS · [run 1](ev-gap-access-run1.json) |
| EV-FR10-029 | DT-21 / user token / đơn của mình #1, DB mới | 2026-10-21 03:00:51 | `PUT /api/admin/orders/1/status`, cùng body | `pending` → 200 `Order status updated` → `confirmed` | **FAIL** · [run 2](ev-gap-access-run2.json) |
| EV-FR10-030 | DT-01 đối chứng / admin token / đơn user #2, DB mới | 2026-10-21 03:00:51 | `PUT /api/admin/orders/2/status`, cùng body | `pending` → 200 `Order status updated` → `confirmed` | PASS · [run 2](ev-gap-access-run2.json) |
| EV-FR10-031 | DT-23 / không token / đơn user #3, DB mới | 2026-10-21 03:00:51 | `PUT /api/admin/orders/3/status`, cùng body | `pending` → 401 `Unauthorized` → `pending` | PASS · [run 2](ev-gap-access-run2.json) |
| EV-FR10-032 | DT-22 / user token / đơn của admin #1, DB mới | 2026-10-21 03:01:30 | `PUT /api/admin/orders/1/status`, cùng body | `pending` → 200 `Order status updated` → `confirmed` | **FAIL** · [cross-owner](ev-gap-access-cross.json) |

**Oracle trước chạy:** token user hoặc không token phải bị từ chối và trạng thái giữ `pending` theo FR-12; token admin được phép chuyển `pending→confirmed` theo FR-10 R1/FR-18. HTTP status cụ thể không quy định. Raw JSON lưu request, response, status trước/sau và timestamp cho từng EV; Bearer đã redacted. UI Admin chặn login role user, nên không có lần chạy UI cho đúng input user-token tới API Admin.

**Screenshot evidence:** [BUG-FR10-03-api-evidence.png](../screenshots/BUG-FR10-03-api-evidence.png) là ảnh chụp bằng Firefox headless của bản trình bày đúng các record DT-21/DT-22 từ `ev-gap-access-run1.json` và `ev-gap-access-cross.json`, thêm đối chứng DT-23/DT-01 từ run 1. Ảnh ghi rõ nguồn và redacted JWT; **không phải ảnh UI app hoặc Postman, không phải lần chạy API mới**. EV-026/032 và raw JSON vẫn là bằng chứng gốc.

Ảnh đã đính trong [GitHub Issue #60](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/60); URL raw image trả HTTP 200 khi kiểm tra trước khi đăng.

Thư mục dựng ảnh và Firefox profile tạm `/private/tmp/fr10-issue-shot.rkwU5b` đã được xóa sau khi publish Issue; ảnh cần giữ lại nằm ở `../screenshots/BUG-FR10-03-api-evidence.png`.

### Cleanup run bổ sung

| Mục | Kết quả |
| --- | --- |
| Dịch vụ test | Node child process dừng sau mỗi lần chạy; `lsof -nP -iTCP:3000 -sTCP:LISTEN` không còn listener. |
| Thư mục tạm | Đã xóa đúng `/private/tmp/fr10-gap-run.Trf42g`; `test ! -e` thành công. |
| DB làm việc | SHA-256 sau run vẫn `c63f00544180ba1fbb1427a9b9dd3f1784842698809972f33ce90482e7420ba6`, khớp trước run. |
| Chỉnh sửa có sẵn khác | Giữ nguyên các file người dùng đã sửa tại FR-06, FR-17 và `prompt.txt`; các file đó không thuộc run này. |
