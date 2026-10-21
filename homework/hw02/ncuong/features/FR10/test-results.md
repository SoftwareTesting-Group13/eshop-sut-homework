# FR10 — Test results

- **Run được chọn để tổng hợp:** 20 ca cốt lõi từ `run-20261020-fr10`; ba ca Domain/EP quyền truy cập bổ sung từ `run-20261021-fr10-gap-access` (hai lần chạy DT-21 và đối chứng; một lần DT-22). Mỗi T-ID chỉ tính một lần.
- **Build/commit SUT:** repo `eshop-sut-homework`, commit `09a950cf451428bd8f54542b3f11a0e4b6fdaa91`
- **Môi trường:** macOS, Node v26.9.0, backend Node/Express + SQLite; instance cách ly trong thư mục tạm (`server.js`/`database.js` là bản sao, `database.sqlite` riêng, `node_modules` symlink). Thời điểm chạy: `2026-10-20 02:56 +0700` (= `2026-10-19T19:56Z`).
- **Interface:** `PUT http://localhost:3000/api/admin/orders/:id/status` (admin), `PUT /api/orders/:id/cancel` (user), quan sát `GET /api/orders/:id`.
- **Reset trạng thái:** mỗi ca tạo đơn mới qua `POST /api/checkout` (user `test@eshop.com`) rồi đưa về trạng thái nguồn bằng API admin (các chuyển đổi hợp lệ). Không dùng DB làm việc.
- **Chi tiết thô:** `evidence/FR10-evidence.md` + các file `evidence/*.log`, `evidence/run-summary.json`; xác nhận UI: `screenshots/*.png` (EV-FR10-024/025).
- **Run bổ sung:** commit `9955eba27e0e4bf45613649150bf3c2eb681a20f`, backend/SQLite bản sao cách ly; raw log `evidence/ev-gap-access-run1.json`, `ev-gap-access-run2.json`, `ev-gap-access-cross.json`. JWT không lưu trong log; chỉ ghi actor và sự hiện diện của Bearer.

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
| DT-21 | run-20261021-fr10-gap-access | User token đổi **đơn của mình** `pending→confirmed`: HTTP 200; đơn đổi thành `confirmed` (lặp lại 2/2) | **FAIL** | EV-FR10-026/029 (`ev-gap-access-run1/2.json`) | BUG-FR10-03 |
| DT-22 | run-20261021-fr10-gap-access | User token đổi **đơn người khác** `pending→confirmed`: HTTP 200; đơn đổi thành `confirmed` | **FAIL** | EV-FR10-032 (`ev-gap-access-cross.json`) | BUG-FR10-03 |
| DT-23 | run-20261021-fr10-gap-access | Không token: HTTP 401 `Unauthorized`, đơn vẫn `pending` (2/2) | PASS | EV-FR10-028/031 (`ev-gap-access-run1/2.json`) | — |

## Tổng hợp case duy nhất

| Phạm vi | Thiết kế | Đã chạy | PASS | FAIL | Quan sát | BLOCKED | Chưa chạy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Tất cả T-ID duy nhất** | 23 | 23 | 19 | 4 | 0 | 0 | 0 |

Đã chạy = PASS + FAIL + Quan sát = 19 + 4 = 23; Thiết kế = Đã chạy + BLOCKED + Chưa chạy = 23.

- **Theo kỹ thuật:** bộ trạng thái cốt lõi EP/Domain 20 lớp (`P1`–`P20`) trên 20 T-ID, BVA 9 điểm biên trên 8 T-ID; miền quyền bổ sung A1–A4 gồm 4 lớp EP trên DT-01/DT-21–DT-23 (DT-01 dùng chung, không đếm lại). Không có BVA mới cho role rời rạc.
- Bằng chứng: `evidence/FR10-evidence.md` + `evidence/DT-*.log`, `evidence/run-summary.json`, `evidence/session-header.log`, `evidence/ev-gap-access-*.json`.

---

## Bug report

### Bảng tổng hợp

| Bug ID | Feature | Title | Severity | Priority | Related TC | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BUG-FR10-01 | FR10 | Admin chuyển được đơn `canceled` sang `delivered` (xuyên trạng thái kết thúc) | Medium | Medium | DT-14 | Đã xác nhận qua UI; Issue [#33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33) (kèm screenshot) | `DT-14.log`, `DT-14-rerun.log`, `screenshots/BUG-FR10-01-*.png` |
| BUG-FR10-02 | FR10 | User tự hủy được đơn đang `shipping` (được phép hủy sai trạng thái) | High | High | DT-16 | Đã xác nhận qua UI; Issue [#34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34) (kèm screenshot) | `DT-16.log`, `DT-16-rerun.log`, `screenshots/BUG-FR10-02-*.png` |
| BUG-FR10-03 | FR10 / FR12 | User thường tự xác nhận được đơn của mình **và đơn người khác** qua API Admin | High | High | DT-21, DT-22 | Đã tái hiện API; ảnh log đính trong Issue [#60](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/60) | `ev-gap-access-run1.json`, `ev-gap-access-run2.json`, `ev-gap-access-cross.json`; [ảnh API](screenshots/BUG-FR10-03-api-evidence.png) |

### Thống kê severity

| Critical | High | Medium | Low | Tổng |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 2 | 1 | 0 | **3** |

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

#### BUG-FR10-03 — User thường gọi API Admin để xác nhận đơn

| Trường | Giá trị |
| --- | --- |
| Feature / rule | FR-12 mọi `/api/admin/*` phải có JWT hợp lệ và role admin; FR-18 chỉ Admin quản lý trạng thái; FR-10 R1 |
| Test case | DT-21 (đơn của mình), DT-22 (đơn người khác); DT-01 và DT-23 là đối chứng |
| Build / run | `9955eba27e0e4bf45613649150bf3c2eb681a20f`; `run-20261021-fr10-gap-access`; backend/SQLite cách ly |
| Severity / Priority | High / High — user thường đã đổi được cả đơn thuộc tài khoản khác khi biết ID |
| Evidence | [run 1](evidence/ev-gap-access-run1.json), [run 2](evidence/ev-gap-access-run2.json), [đơn người khác](evidence/ev-gap-access-cross.json), [ảnh API](screenshots/BUG-FR10-03-api-evidence.png), [nội dung Issue](issues/BUG-FR10-03.md) |
| Trạng thái | API tái hiện 2/2 với đơn của mình và 1/1 với đơn người khác; [Issue #60](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/60) kèm ảnh trình bày log |

**Tiền điều kiện:** đăng nhập `test@eshop.com` để lấy JWT role `user`; có đơn `pending` được tạo qua checkout. DT-22 dùng đơn khác thuộc `admin@eshop.com`. Trên DB test mới, mỗi ca có đơn riêng.

**Đường API đã chạy:** gửi `PUT /api/admin/orders/:id/status` với `Authorization: Bearer <JWT user>` và body `{"status":"confirmed"}`; đọc `GET /api/orders/:id` trước/sau. Expected: từ chối vì token không có `role='admin'`, đơn vẫn `pending`. Actual: HTTP 200 `Order status updated`; đơn thành `confirmed` ở cả đơn của mình lẫn đơn người khác. Không có token thì HTTP 401 và trạng thái giữ nguyên; token admin thành công như đối chứng.

**Đường UI:** Admin UI chặn đăng nhập tài khoản role user ở `frontend-admin/src/App.jsx:65`; web user không có nút xác nhận đơn. Vì vậy cùng input user-token tới API Admin chỉ đi được qua request trực tiếp; **chưa có xác nhận UI**. Root cause từ source: route `backend/server.js:525` chỉ dùng `authenticateToken`, không kiểm tra role sau xác thực.

---

## Coverage & gaps

| Tiêu chí coverage | Nghĩa vụ đủ điều kiện | Thiết kế | Đã chạy | PASS | Chưa phủ |
| --- | ---: | ---: | ---: | ---: | ---: |
| Lớp tương đương EP (P1–P20) | 20 | 20 | 20 | 18 | 0 (P14, P16 FAIL) |
| Điểm biên BVA (B1–B3) | 9 | 9 | 9 | 7 | 0 (2 điểm FAIL) |
| EP bổ sung quyền API Admin (A1–A4, FR-12/FR-18) | 4 | 4 | 4 | 2 | 0 (A2, A3 FAIL) |

- **Coverage theo nghĩa vụ:** EP trạng thái designed 20/20, executed 20/20, passed 18/20. BVA designed 9/9, executed 9/9, passed 7/9. EP quyền bổ sung designed 4/4, executed 4/4, passed 2/4; A1 dùng chung DT-01 nên không cộng trùng. Gộp T-ID: 23 thiết kế / 23 đã chạy / 19 PASS / 4 FAIL.
- **Mục tiêu đề xuất (chưa được duyệt):** thiết kế và thực thi 100% nghĩa vụ đủ điều kiện; đạt oracle theo từng nghĩa vụ. **Goal status:** designed `GOAL_MET`, executed `GOAL_MET`, passed `GOAL_NOT_MET` (EP 18/20, BVA 7/9 do 2 nghĩa vụ FAIL). Coverage đạt không đồng nghĩa feature không còn lỗi.
- **Chưa bao phủ:** không có nghĩa vụ EP/BVA đã chọn nào bị bỏ trống. Điểm chưa rõ còn lại: Q1 — `shipping→canceled` cho admin (DT-20 chấm theo sơ đồ, `ASSUMED`); Q2 — phản hồi đơn không tồn tại/không sở hữu (DT-19 ghi nhận hành vi `404`). Q3 đã chạy trong miền quyền bổ sung.
- **Infeasible/khó:** không có; mọi điểm biên đều tạo được bằng API hợp lệ.
- **Ca BLOCKED:** không có.

## Ngoài phạm vi EP/BVA (không tính coverage)

- Quan sát source về thiếu kiểm tra role ở API Admin đã được chạy xác nhận dưới AI-GAP-FR10-01 và chuyển thành DT-21/DT-22, BUG-FR10-03. Đây là miền quyền FR-12/FR-18 bổ sung, **không** cộng vào EP/BVA trạng thái FR-10 cốt lõi. Ghi nguồn tại `../../supporting-materials/fr10-observations.md`.
- Nút "Hủy đơn" trên UI web và nút "Đánh dấu Đã giao" trên Admin UI đã được xác nhận bằng UI (screenshot) và là đường tái hiện của 2 bug; không phải lớp dữ liệu mới nên không cộng coverage.

## AI Gap Analysis

| Gap ID | AI output/source | Test case/bug tôi phát hiện thêm | Cách tôi phát hiện | Vì sao AI bỏ sót (nhận định của tôi) | Bổ sung/sửa chữa |
| --- | --- | --- | --- | --- | --- |
| AI-GAP-FR10-01 | Trong `test-cases.md`, các ca gọi `PUT /api/admin/orders/:id/status` đều dùng token admin. AI có ghi rủi ro thiếu kiểm tra quyền ở `fr10-observations.md` nhưng chưa thiết kế và chạy ca với token user thường. | Tôi thấy cần thử cho user thường gọi API này để tự chuyển đơn `pending → confirmed`. Theo nghiệp vụ, khách hàng không thể tự xác nhận đơn thay admin; nếu API chấp nhận thì đây là lỗi phân quyền. | Đối chiếu sơ đồ FR-10 và FR-18: bước xác nhận/giao hàng do Admin thực hiện. FR-12 còn yêu cầu mọi API `/api/admin/*` kiểm tra `role = 'admin'`. Trong `backend/server.js`, route đổi trạng thái chỉ dùng `authenticateToken`, không kiểm tra role. | AI tập trung vào cặp trạng thái trước/sau và luôn dùng đúng tài khoản admin cho ca hợp lệ. AI đã nhận ra rủi ro khi đọc source nhưng xếp ra ngoài phạm vi EP/BVA, nên chưa kiểm chứng quyền thao tác trong luồng thực tế. | Đã chạy DT-21 (đơn mình, 2/2), DT-22 (đơn người khác, 1/1), DT-23 (không token, 2/2), đối chứng admin DT-01; phát hiện **BUG-FR10-03**. Raw log và ảnh API đã gắn vào [Issue #60](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/60). Coverage EP/BVA trạng thái FR-10 giữ nguyên; miền quyền có coverage riêng A1–A4. |

## Việc còn lại

1. ~~Người kiểm thử xác nhận 2 bug và mở GitHub Issue~~ — **đã xong**: xác nhận qua UI + screenshot; Issue [#33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33), [#34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34).
2. Chốt Q1 (`shipping→canceled` cho admin) với nhóm giảng viên/nhóm; Q3 đã xác nhận là BUG-FR10-03 bằng API.
3. ~~Gắn screenshot API và mở Issue BUG-FR10-03~~ — **đã xong** ([#60](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/60)). Sinh viên viết AI Critique theo yêu cầu bài.
