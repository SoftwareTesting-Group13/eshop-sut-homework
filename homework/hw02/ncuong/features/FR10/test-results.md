# FR10 — Test results

- **Run được chọn để tổng hợp:** `run-20261020-fr10`
- **Build/commit SUT:** repo `eshop-sut-homework`, commit `09a950cf451428bd8f54542b3f11a0e4b6fdaa91`
- **Môi trường:** macOS, Node v26.9.0, backend Node/Express + SQLite; instance cách ly trong thư mục tạm (`server.js`/`database.js` là bản sao, `database.sqlite` riêng, `node_modules` symlink). Thời điểm chạy: `2026-10-20 02:56 +0700` (= `2026-10-19T19:56Z`).
- **Interface:** `PUT http://localhost:3000/api/admin/orders/:id/status` (admin), `PUT /api/orders/:id/cancel` (user), quan sát `GET /api/orders/:id`.
- **Reset trạng thái:** mỗi ca tạo đơn mới qua `POST /api/checkout` (user `test@eshop.com`) rồi đưa về trạng thái nguồn bằng API admin (các chuyển đổi hợp lệ). Không dùng DB làm việc.
- **Chi tiết thô:** `evidence/FR10-evidence.md` + các file `evidence/*.log`, `evidence/run-summary.json`; xác nhận UI: `screenshots/*.png` (EV-FR10-024/025).

## Kết quả theo run

| T-ID | Run ID | Actual | Status | EV-ID / evidence | Bug ID |
| --- | --- | --- | --- | --- | --- |
| DT-01 | run-20261020-fr10 | 200 `Order status updated`; đơn `pending` → `confirmed` | PASS | EV-FR10-001 (`DT-01.log`) | — |
| DT-02 | run-20261020-fr10 | 200; `confirmed` → `shipping` | PASS | EV-FR10-002 (`DT-02.log`) | — |
| DT-03 | run-20261020-fr10 | 200; `shipping` → `delivered` | PASS | EV-FR10-003 (`DT-03.log`) | — |
| DT-04 | run-20261020-fr10 | 200; `pending` → `canceled` | PASS | EV-FR10-004 (`DT-04.log`) | — |
| DT-05 | run-20261020-fr10 | 200; `confirmed` → `canceled` | PASS | EV-FR10-005 (`DT-05.log`) | — |
| DT-06 | run-20261020-fr10 | 200 `Order canceled successfully`; `pending` → `canceled` | PASS | EV-FR10-006 (`DT-06.log`) | — |
| DT-07 | run-20261020-fr10 | 200; `confirmed` → `canceled` | PASS | EV-FR10-007 (`DT-07.log`) | — |
| DT-08 | run-20261020-fr10 | 400 `Invalid state transition from pending to shipping`; giữ `pending` | PASS | EV-FR10-008 (`DT-08.log`) | — |
| DT-09 | run-20261020-fr10 | 400 `Invalid state transition from confirmed to delivered`; giữ `confirmed` | PASS | EV-FR10-009 (`DT-09.log`) | — |
| DT-10 | run-20261020-fr10 | 400 `... from confirmed to pending`; giữ `confirmed` | PASS | EV-FR10-010 (`DT-10.log`) | — |
| DT-11 | run-20261020-fr10 | 400 `... from shipping to confirmed`; giữ `shipping` | PASS | EV-FR10-011 (`DT-11.log`) | — |
| DT-12 | run-20261020-fr10 | 400 `... from pending to pending`; giữ `pending` | PASS | EV-FR10-012 (`DT-12.log`) | — |
| DT-13 | run-20261020-fr10 | 400 `... from delivered to shipping`; giữ `delivered` | PASS | EV-FR10-013 (`DT-13.log`) | — |
| DT-14 | run-20261020-fr10 | **200 `Order status updated`; `canceled` → `delivered`** | **FAIL** | EV-FR10-014, EV-FR10-021 rerun (`DT-14.log`, `DT-14-rerun.log`) | BUG-FR10-01 |
| DT-15 | run-20261020-fr10 | 400 `... from pending to shipped`; giữ `pending` | PASS | EV-FR10-015 (`DT-15.log`) | — |
| DT-16 | run-20261020-fr10 | **200 `Order canceled successfully`; `shipping` → `canceled`** | **FAIL** | EV-FR10-016, EV-FR10-022 rerun (`DT-16.log`, `DT-16-rerun.log`) | BUG-FR10-02 |
| DT-17 | run-20261020-fr10 | 400 `Cannot cancel this order.`; giữ `delivered` | PASS | EV-FR10-017 (`DT-17.log`) | — |
| DT-18 | run-20261020-fr10 | 400 `Cannot cancel this order.`; giữ `canceled` | PASS | EV-FR10-018 (`DT-18.log`) | — |
| DT-19 | run-20261020-fr10 | 404 `Order not found` (đơn 999999); biến thể: user hủy đơn không sở hữu → 404, đơn giữ `pending` | PASS | EV-FR10-019, EV-FR10-023 (`DT-19.log`, `DT-19-variants.log`) | — |
| DT-20 | run-20261020-fr10 | 400 `... from shipping to canceled`; giữ `shipping` | PASS | EV-FR10-020 (`DT-20.log`) | — |

## Tổng hợp case duy nhất

| Phạm vi | Thiết kế | Đã chạy | PASS | FAIL | Quan sát | BLOCKED | Chưa chạy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Tất cả T-ID duy nhất** | 20 | 20 | 18 | 2 | 0 | 0 | 0 |

Đã chạy = PASS + FAIL + Quan sát = 18 + 2 = 20; Thiết kế = Đã chạy + BLOCKED + Chưa chạy = 20.

- **Theo kỹ thuật (có thể chồng lấp, không cộng thành tổng):** EP/Domain 20 lớp (`P1`–`P20`) trên 20 T-ID; BVA 9 điểm biên (B1 5, B2 2, B3 2) trên 8 T-ID (dùng lại ca EP).
- Bằng chứng: `evidence/FR10-evidence.md` + `evidence/DT-*.log`, `evidence/run-summary.json`, `evidence/session-header.log`.

---

## Bug report

### Bảng tổng hợp

| Bug ID | Feature | Title | Severity | Priority | Related TC | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BUG-FR10-01 | FR10 | Admin chuyển được đơn `canceled` sang `delivered` (xuyên trạng thái kết thúc) | Medium | Medium | DT-14 | Đã xác nhận qua UI; Issue [#33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33) (kèm screenshot) | `DT-14.log`, `DT-14-rerun.log`, `screenshots/BUG-FR10-01-*.png` |
| BUG-FR10-02 | FR10 | User tự hủy được đơn đang `shipping` (được phép hủy sai trạng thái) | High | High | DT-16 | Đã xác nhận qua UI; Issue [#34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34) (kèm screenshot) | `DT-16.log`, `DT-16-rerun.log`, `screenshots/BUG-FR10-02-*.png` |

### Thống kê severity

| Critical | High | Medium | Low | Tổng |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 1 | 1 | 0 | **2** |

### Tiêu chí phân loại

| Severity | Tiêu chí |
| --- | --- |
| **Critical** | Lộ/mất dữ liệu nhạy cảm hoặc lỗi bảo mật nghiêm trọng. |
| **High** | Luồng cốt lõi hoặc business rule quan trọng sai, ảnh hưởng lớn tới người dùng. |
| **Medium** | Quy tắc/validation sai với ảnh hưởng giới hạn hơn High. |
| **Low** | Sai lệch hiển thị/nội dung nhỏ, ít ảnh hưởng đến việc hoàn thành tác vụ. |

Priority là mức ưu tiên xử lý, đánh giá riêng theo mức ảnh hưởng và tính cấp bách.

### Chi tiết (manual reproduction)

> **Môi trường chung:** commit `09a950cf…`; backend Node/Express + SQLite; base URL `http://localhost:3000`. Evidence gồm **API đã chạy thật** (instance cách ly) và **xác nhận UI** do người kiểm thử thực hiện kèm screenshot. Nội dung Issue độc lập nằm ở `issues/BUG-FR10-01.md`, `issues/BUG-FR10-02.md`; Issue đã mở: [#33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33), [#34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34).

#### BUG-FR10-01 — Admin chuyển được đơn `canceled` sang `delivered`

| Trường | Giá trị |
| --- | --- |
| Feature | FR10 — Trạng thái Đơn hàng |
| Test case liên quan | DT-14 (đồng thời BVA B3 "rời terminal canceled") |
| Requirement | README §5 FR-10 (R7 — `canceled` là trạng thái kết thúc; R9) |
| Severity / Priority | Medium / Medium |
| Trạng thái | **Đã xác nhận qua UI**; tái hiện API 2/2 + UI 1/1 |
| Evidence | `evidence/DT-14.log`, `evidence/DT-14-rerun.log`, `screenshots/BUG-FR10-01-*.png` |
| GitHub Issue / Screenshot | Issue [#33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33), kèm 3 screenshot (`BUG-FR10-01-Cancelled-Admin.png`, `BUG-FR10-01-Delivered-Admin.png`, `BUG-FR10-01-Delivered-User.png`) |

**Tiền điều kiện:** một đơn hàng đang ở trạng thái `canceled` (ví dụ hủy đơn `pending` bằng admin).

**Các bước tái hiện (API đã kiểm chứng):**
1. Tạo đơn rồi hủy để đưa về `canceled`.
2. Gửi `PUT /api/admin/orders/:id/status` với `{"status":"delivered"}`.
3. Đọc `HTTP response` và `GET /api/orders/:id`.

| Bước | Input / hành động | Quan sát |
| --- | --- | --- |
| 1 | order `canceled` (order id 14) | status trước = `canceled` |
| 2 | admin `{"status":"delivered"}` | `HTTP 200 {"message":"Order status updated"}` (kỳ vọng lỗi) |
| 3 | đọc lại đơn | status sau = `delivered` (kỳ vọng giữ `canceled`) |

**Expected:** `canceled` là trạng thái kết thúc — mọi chuyển đổi khỏi `canceled` phải trả lỗi và giữ nguyên trạng thái (R7, R9). **Actual:** API chấp nhận và đặt đơn thành `delivered`.
**Độ lặp lại:** 2/2 (DT-14 và rerun trên đơn mới). **Root cause (theo code):** `backend/server.js:550-551`.
**Đường UI (đã xác nhận):** Web Admin → tab "Đơn hàng"; đơn hàng số 1 ở "Đã hủy" vẫn hiển thị nút "Đánh dấu Đã giao" (`frontend-admin/src/App.jsx:862-869`). Bấm nút → đơn chuyển "Đã giao"; Web phía user cũng hiển thị "Đã giao". Ảnh: `screenshots/BUG-FR10-01-Cancelled-Admin.png` → `BUG-FR10-01-Delivered-Admin.png` → `BUG-FR10-01-Delivered-User.png`.
**Reproduce nhanh (API):**
```bash
curl -s -X PUT http://localhost:3000/api/admin/orders/14/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  --data-raw '{"status":"delivered"}'
curl -s http://localhost:3000/api/orders/14
```

---

#### BUG-FR10-02 — User tự hủy được đơn đang `shipping`

| Trường | Giá trị |
| --- | --- |
| Feature | FR10 — Trạng thái Đơn hàng |
| Test case liên quan | DT-16 (đồng thời BVA B1 "ngay trên biên") |
| Requirement | README §5 FR-10 (R8 — ở `shipping` User không được tự hủy; R9); FR-20 §7 |
| Severity / Priority | High / High |
| Trạng thái | **Đã xác nhận qua UI**; tái hiện API 2/2 + UI 1/1 |
| Evidence | `evidence/DT-16.log`, `evidence/DT-16-rerun.log`, `screenshots/BUG-FR10-02-*.png` |
| GitHub Issue / Screenshot | Issue [#34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34), kèm 4 screenshot (`BUG-FR10-02-Delivering-Admin.png`, `BUG-FR10-02-Delivering-User.png`, `BUG-FR10-02-Noti-Cancelled-User.png`, `BUG-FR10-02-Status-Cancelled-User.png`); cùng defect được ghi nhận từ góc nhìn FR-11 tại Issue #13 |

**Tiền điều kiện:** một đơn của user `test@eshop.com` đang ở trạng thái `shipping`.

**Các bước tái hiện (API đã kiểm chứng):**
1. Tạo đơn (user) rồi đưa tới `shipping` bằng admin (pending→confirmed→shipping).
2. User gửi `PUT /api/orders/:id/cancel` bằng token của chính mình.
3. Đọc response và `GET /api/orders/:id`.

| Bước | Input / hành động | Quan sát |
| --- | --- | --- |
| 1 | order id 16 đưa tới `shipping` | status trước = `shipping` |
| 2 | user `PUT /api/orders/16/cancel` | `HTTP 200 {"message":"Order canceled successfully"}` (kỳ vọng lỗi) |
| 3 | đọc lại đơn | status sau = `canceled` (kỳ vọng giữ `shipping`) |

**Expected:** ở `shipping`, User không được phép tự hủy; yêu cầu hủy phải trả lỗi và giữ nguyên trạng thái (R8, R9). **Actual:** API hủy thành công và đặt đơn thành `canceled`.
**Độ lặp lại:** 2/2 (DT-16 và rerun trên đơn mới). **Root cause (theo code):** `backend/server.js:328-331` (chỉ chặn `delivered`/`canceled`).
**Đường UI (đã xác nhận):** Web (`frontend-web/src/pages/Profile.jsx:200`) → Hồ sơ → "Lịch sử đơn hàng": đơn hàng số 2 "Đang giao" vẫn hiển thị nút "Hủy đơn" (điều kiện `status !== "delivered" && status !== "canceled"`). Bấm nút → alert "Hủy đơn thành công!" → đơn chuyển "Đã hủy". Ảnh: `screenshots/BUG-FR10-02-Delivering-Admin.png`, `BUG-FR10-02-Delivering-User.png`, `BUG-FR10-02-Noti-Cancelled-User.png`, `BUG-FR10-02-Status-Cancelled-User.png`.
**Reproduce nhanh (API):**
```bash
curl -s -X PUT http://localhost:3000/api/orders/16/cancel \
  -H "Authorization: Bearer $USER_TOKEN"
curl -s http://localhost:3000/api/orders/16
```

---

## Coverage & gaps

| Tiêu chí coverage | Nghĩa vụ đủ điều kiện | Thiết kế | Đã chạy | PASS | Chưa phủ |
| --- | ---: | ---: | ---: | ---: | ---: |
| Lớp tương đương EP (P1–P20) | 20 | 20 | 20 | 18 | 0 (P14, P16 FAIL) |
| Điểm biên BVA (B1–B3) | 9 | 9 | 9 | 7 | 0 (2 điểm FAIL) |

- **Coverage theo nghĩa vụ:** EP designed 20/20, executed 20/20, passed 18/20. BVA designed 9/9, executed 9/9, passed 7/9. Gộp T-ID: 20 thiết kế / 20 đã chạy / 18 PASS / 2 FAIL.
- **Mục tiêu đề xuất (chưa được duyệt):** thiết kế và thực thi 100% nghĩa vụ đủ điều kiện; đạt oracle theo từng nghĩa vụ. **Goal status:** designed `GOAL_MET`, executed `GOAL_MET`, passed `GOAL_NOT_MET` (EP 18/20, BVA 7/9 do 2 nghĩa vụ FAIL). Coverage đạt không đồng nghĩa feature không còn lỗi.
- **Chưa bao phủ:** không có nghĩa vụ EP/BVA nào bị bỏ trống. Điểm chưa rõ: Q1 — `shipping→canceled` cho admin (DT-20 chấm theo sơ đồ, `ASSUMED`); Q2 — phản hồi đơn không tồn tại/không sở hữu (DT-19 ghi nhận hành vi `404`); Q3 — quyền gọi API admin (quan sát ngoài EP/BVA).
- **Infeasible/khó:** không có; mọi điểm biên đều tạo được bằng API hợp lệ.
- **Ca BLOCKED:** không có.

## Ngoài phạm vi EP/BVA (không tính coverage)

- API đổi trạng thái admin `PUT /api/admin/orders/:id/status` **không kiểm tra `role = 'admin'`** (chỉ `authenticateToken`): user thường vẫn gọi được. Đây là rủi ro FR-12/truy cập, không phải miền dữ liệu FR-10. Ghi tại `../../supporting-materials/fr10-observations.md`.
- Nút "Hủy đơn" trên UI web và nút "Đánh dấu Đã giao" trên Admin UI đã được xác nhận bằng UI (screenshot) và là đường tái hiện của 2 bug; không phải lớp dữ liệu mới nên không cộng coverage.

## AI Gap Analysis

> Phần này do **người kiểm thử tự rà soát và viết** (không điền thay). Trạng thái: `Chờ người kiểm thử rà soát và viết`.

| Gap ID | AI output/source | Test case/bug tôi phát hiện thêm | Cách tôi phát hiện | Vì sao AI bỏ sót (nhận định của tôi) | Bổ sung/sửa chữa |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Việc còn lại

1. ~~Người kiểm thử xác nhận 2 bug và mở GitHub Issue~~ — **đã xong**: xác nhận qua UI + screenshot; Issue [#33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33), [#34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34).
2. Chốt Q1 (`shipping→canceled` cho admin) và Q3 (kiểm soát truy cập API admin) với nhóm giảng viên/nhóm.
3. Viết AI Gap Analysis cho FR10 và AI Critique (phần của sinh viên).
