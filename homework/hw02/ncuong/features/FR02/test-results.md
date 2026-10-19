# FR02 — Test results

- **Run được chọn để tổng hợp:** `run-20261020-fr02`
- **Build/commit SUT:** repo `eshop-sut-homework`, commit `f3162660d5c4f9005cbb15910290adb4b58ef2c7`
- **Môi trường:** macOS, Node v26.9.0, backend Node/Express + SQLite; instance cách ly trong thư mục tạm (`server.js`/`database.js` là bản sao, `database.sqlite` riêng, `node_modules` symlink). Interface: `POST http://localhost:3000/api/login` (và `GET /api/users/me` để xác nhận token).
- **Reset trạng thái:** mỗi ca dùng tài khoản fixture riêng; trạng thái bộ đếm/khóa chuẩn bị bằng `sqlite3` trên DB test. DB làm việc `backend/database.sqlite` giữ nguyên checksum `c63f0054…` (không bị sửa).
- **Chi tiết thô:** `evidence/FR02-evidence.md` + các file `evidence/*.log`.

## Kết quả theo run

| T-ID | Run ID | Actual | Status | EV-ID / evidence | Bug ID |
| --- | --- | --- | --- | --- | --- |
| DT-01 | run-20261020-fr02 | Thân phản hồi success + `token`; `GET /api/users/me` trả 200 với token | PASS | EV-FR02-001, EV-FR02-002 (`ev-DT-01.log`, `ev-DT-01-token-check.log`) | — |
| DT-02 | run-20261020-fr02 | Thất bại (401, không token); `login_attempts` = **2** sau 1 lần sai (kỳ vọng 1) | FAIL | EV-FR02-003, EV-FR02-004 (`ev-DT-02.log`, `ev-DT-02-rerun.log`) | BUG-FR02-01 |
| DT-03 | run-20261020-fr02 | Thất bại (401, không token); số user khớp email = 0 | PASS | EV-FR02-005 (`ev-DT-03.log`) | — |
| DT-04 | run-20261020-fr02 | Mật khẩu rỗng → 401, không token | PASS | EV-FR02-006 (`ev-DT-04-05.log`) | — |
| DT-05 | run-20261020-fr02 | Email rỗng và body `{}` → 401, không token | PASS | EV-FR02-007 (`ev-DT-04-05.log`) | — |
| DT-06 | run-20261020-fr02 | Email `not-an-email` → 401, không token (đặc tả không định nghĩa kết quả ở API) | INCONCLUSIVE (Quan sát) | EV-FR02-008 (`ev-DT-06.log`) | — |
| DT-07 | run-20261020-fr02 | Tài khoản khóa + mật khẩu đúng → 403 thông báo khóa, không token; `login_attempts=3`, `locked_until` giữ nguyên | PASS | EV-FR02-009 (`ev-DT-07-08.log`) | — |
| DT-08 | run-20261020-fr02 | Tài khoản khóa + mật khẩu sai → 403 thông báo khóa; bộ đếm không đổi | PASS | EV-FR02-010 (`ev-DT-07-08.log`) | — |
| BVA-02 | run-20261020-fr02 | Sau 2 lần sai: `login_attempts=4` **và** đã khóa (`locked_until` ≈ now+180 s) | FAIL | EV-FR02-011 (`ev-BVA-02.log`) | BUG-FR02-01, BUG-FR02-02 |
| BVA-03 | run-20261020-fr02 | Từ `login_attempts=2` (chưa khóa), sai lần 3 → tài khoản bị khóa (`locked_until` được đặt) | PASS | EV-FR02-012 (`ev-BVA-03-04.log`) | — (bộ đếm/thời lượng thuộc DT-02/BVA-06) |
| BVA-04 | run-20261020-fr02 | Gửi thêm khi đang khóa → 403 thông báo khóa; bộ đếm/khóa không đổi | PASS | EV-FR02-013 (`ev-BVA-03-04.log`) | — |
| BVA-05 | run-20261020-fr02 | Tại `t0+29 s`, mật khẩu đúng → vẫn 403 (đang trong cửa sổ khóa) | PASS | EV-FR02-014 (`ev-BVA-05-06.log`) | — |
| BVA-06 | run-20261020-fr02 | Tại `t0+31 s`, mật khẩu đúng → vẫn 403 (chưa hết khóa) | FAIL | EV-FR02-015 (`ev-BVA-05-06.log`) | BUG-FR02-02 |
| BVA-07 | run-20261020-fr02 | 1 lần sai rồi đúng → 200 + token; `login_attempts=0`, `locked_until=NULL` | PASS | EV-FR02-016 (`ev-BVA-07.log`) | — |
| BVA-08 | run-20261020-fr02 | `locked_until` quá khứ + mật khẩu đúng → 200 + token | PASS | EV-FR02-017 (`ev-BVA-08.log`) | — |

## Tổng hợp case duy nhất

| Phạm vi | Thiết kế | Đã chạy | PASS | FAIL | Quan sát | BLOCKED | Chưa chạy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Tất cả T-ID duy nhất** | 15 | 15 | 11 | 3 | 1 | 0 | 0 |

Đã chạy = PASS + FAIL + Quan sát = 11 + 3 + 1 = 15; Thiết kế = Đã chạy + BLOCKED + Chưa chạy = 15. `DT-06` là Quan sát/INCONCLUSIVE, không tính vào pass/fail.

- **Theo kỹ thuật (có thể chồng lấp, không cộng thành tổng):** EP/Domain 9 T-ID (P1–P9); BVA 8 điểm biên trên 8 T-ID (BVA-01 gộp DT-02).
- Bằng chứng: `evidence/FR02-evidence.md` + `evidence/*.log` (+ `fixture-register.log`, `final-db-state.log`).

---

## Bug report

### Bảng tổng hợp

| Bug ID | Feature | Title | Severity | Priority | Related TC | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BUG-FR02-01 | FR02 | Bộ đếm đăng nhập sai tăng 2 thay vì 1 → khóa tài khoản sau 2 lần sai | High | High | DT-02, BVA-02, BVA-03 | Đã tái hiện (2/2); chờ SV xác nhận | `ev-DT-02.log`, `ev-DT-02-rerun.log`, `ev-BVA-02.log` |
| BUG-FR02-02 | FR02 | Thời lượng khóa tài khoản là 180 giây thay vì 30 giây | Medium | High | BVA-02, BVA-06 | Đã tái hiện (2/2); chờ SV xác nhận | `ev-BVA-02.log`, `ev-BVA-05-06.log` |

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

> **Môi trường chung:** commit `f3162660…`; backend Node/Express + SQLite chạy cách ly; base URL `http://localhost:3000`. **Sau khi SV xác nhận bug, người kiểm thử chụp screenshot và gắn vào GitHub Issue theo yêu cầu HW02.**

#### BUG-FR02-01 — Bộ đếm đăng nhập sai tăng 2 thay vì 1 → khóa tài khoản sau 2 lần sai

| Trường | Giá trị |
| --- | --- |
| Feature | FR02 — Đăng nhập & Khóa tài khoản |
| Test case liên quan | DT-02 (đồng thời BVA-01), BVA-02 |
| Requirement | README §2 FR-02 (R2, R3) |
| Severity / Priority | High / High |
| Trạng thái | Đã tái hiện 2/2; chờ người kiểm thử xác nhận |
| Evidence | `evidence/ev-DT-02.log`, `evidence/ev-DT-02-rerun.log`, `evidence/ev-BVA-02.log` |

**Tiền điều kiện:** tài khoản `fr02.wrong@eshop.com` / `Passw0rd!` tồn tại, DB test có `login_attempts = 0`, `locked_until = NULL`.

**Các bước tái hiện:**
1. Gửi `POST /api/login` với `{"email":"fr02.wrong@eshop.com","password":"WrongPass1!"}`.
2. Đọc `login_attempts` của tài khoản trong DB.
3. (Mô phỏng 2 lần sai liên tiếp) lặp bước 1 một lần nữa và đọc lại `login_attempts`, `locked_until`.

| Bước | Input / hành động | Quan sát |
| --- | --- | --- |
| 1 | sai lần 1 | `HTTP 401` `Invalid email or password`; `login_attempts = 2` (kỳ vọng 1) |
| 3 | sai lần 2 | `login_attempts = 4`; `locked_until` bị đặt ⇒ **khóa ngay ở lần sai thứ 2** (kỳ vọng chưa khóa) |

**Expected:** sau lần sai thứ nhất `login_attempts = 1`; chỉ khi sai **từ 3 lần trở lên liên tiếp** mới khóa (R2, R3). **Actual:** mỗi lần sai cộng 2, nên chỉ sau 2 lần sai bộ đếm đã = 4 ≥ 3 và tài khoản bị khóa sớm hơn đặc tả.
**Độ lặp lại:** 2/2 (chạy lại trên tài khoản `fr02.rerun@eshop.com` cho cùng kết quả `login_attempts = 2`). **Root cause (theo code):** `backend/server.js:54` dùng `user.login_attempts + 2`.
**Reproduce nhanh (API):**
```bash
curl -s -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.wrong@eshop.com","password":"WrongPass1!"}'
sqlite3 backend/database.sqlite "SELECT login_attempts,locked_until FROM users WHERE email='fr02.wrong@eshop.com';"
```
**GitHub Issue:** Chờ người kiểm thử xác nhận bug trước khi mở. **Screenshot:** Chờ người kiểm thử xác nhận rồi chụp và gắn vào Issue.

---

#### BUG-FR02-02 — Thời lượng khóa tài khoản là 180 giây thay vì 30 giây

| Trường | Giá trị |
| --- | --- |
| Feature | FR02 — Đăng nhập & Khóa tài khoản |
| Test case liên quan | BVA-02 (đo `locked_until`), BVA-06 |
| Requirement | README §2 FR-02 (R3) |
| Severity / Priority | Medium / High |
| Trạng thái | Đã tái hiện 2/2; chờ người kiểm thử xác nhận |
| Evidence | `evidence/ev-BVA-02.log`, `evidence/ev-BVA-05-06.log` |

**Tiền điều kiện:** tài khoản chưa khóa; kích hoạt khóa bằng lần sai đưa bộ đếm qua ngưỡng; ghi lại thời điểm khóa `t0`.

**Các bước tái hiện:**
1. Kích hoạt khóa tài khoản (chuẩn bị `login_attempts = 2` rồi gửi 1 lần sai).
2. Đọc `locked_until`; so với `t0`.
3. Chờ tới `t0 + 31 s`, gửi `POST /api/login` với mật khẩu **đúng**.

| Bước | Input / hành động | Quan sát |
| --- | --- | --- |
| 1–2 | đọc `locked_until` sau khóa | `locked_until − now ≈ 180.014 s` (kỳ vọng 30 s) |
| 3 | tại `t0+31 s`, mật khẩu đúng | `HTTP 403` `Tài khoản đã bị khóa. Vui lòng thử lại sau.` (kỳ vọng 200 + token) |

**Expected:** khóa tạm **30 giây**, hết 30 s thì đăng nhập lại được (R3). **Actual:** khóa 180 s, vẫn bị từ chối ở `t0+31 s`.
**Độ lặp lại:** 2/2 (đo tại BVA-02 và quan sát tại BVA-06). **Root cause (theo code):** `backend/server.js:57` dùng `Date.now() + 180000`.
**Reproduce nhanh (API):**
```bash
sleep 31
curl -s -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.thr@eshop.com","password":"Passw0rd!"}'
```
**GitHub Issue:** Chờ người kiểm thử xác nhận bug trước khi mở. **Screenshot:** Chờ người kiểm thử xác nhận rồi chụp và gắn vào Issue.

---

## Coverage & gaps

| Tiêu chí coverage | Nghĩa vụ đủ điều kiện | Thiết kế | Đã chạy | PASS | Chưa phủ |
| --- | ---: | ---: | ---: | ---: | ---: |
| Lớp tương đương EP (P1–P9) | 9 | 9 | 9 | 7 | 0 (P2 FAIL, P6 Quan sát) |
| Điểm biên BVA (B1–B4) | 8 | 8 | 8 | 5 | 0 (3 điểm FAIL) |

- **Coverage theo nghĩa vụ:** EP designed 9/9, executed 9/9, passed 7/9. BVA designed 8/8, executed 8/8, passed 5/8. Gộp T-ID: 15 thiết kế / 15 đã chạy / 11 PASS / 3 FAIL / 1 Quan sát.
- **Mục tiêu đề xuất (chưa được duyệt):** thiết kế và thực thi 100% nghĩa vụ đủ điều kiện; đạt oracle theo từng nghĩa vụ. **Goal status:** designed `GOAL_MET`, executed `GOAL_MET`, passed `GOAL_NOT_MET` (EP 7/9, BVA 5/8 do 3 nghĩa vụ FAIL). Coverage đạt không đồng nghĩa feature không còn lỗi.
- **Chưa bao phủ:** không có nghĩa vụ EP/BVA nào bị bỏ trống. Điểm chưa rõ: Q1 — đặc tả không nói bộ đếm có đặt lại sau khi hết khóa hay không; Q2 — tiêu chí "không lộ chi tiết nguyên nhân" cho thông báo khóa chưa được định nghĩa cụ thể; Q3 — chuẩn hóa hoa/thường và khoảng trắng của email; Q4 — hành vi API với email sai định dạng (DT-06 chỉ Quan sát).
- **Infeasible/khó:** BVA-03 phải chuẩn bị `login_attempts = 2` bằng DB test vì SUT khóa sớm (BUG-FR02-01) khiến không thể tạo "lần sai thứ 3" một cách tuần tự.
- **Ca BLOCKED:** không có.

## Ngoài phạm vi EP/BVA (không tính coverage)

- Thân phản hồi đăng nhập thành công và `GET /api/users/me` trả về trường `password` dạng plaintext; mật khẩu lưu plaintext trong DB (liên quan SEC-01). Ghi tại `../../supporting-materials/fr02-observations.md`.
- UI `frontend-web/src/pages/Login.jsx` dùng `<input type="text">` cho email (đặc tả FR-02 yêu cầu `type="email"`) và cho mật khẩu. Là thuộc tính DOM/UI, không phải miền dữ liệu ⇒ không tính EP/BVA.

## AI Gap Analysis

> Phần này do **người kiểm thử tự rà soát và viết** (không điền thay). Trạng thái: `Chờ người kiểm thử rà soát và viết`.

| Gap ID | AI output/source | Test case/bug tôi phát hiện thêm | Cách tôi phát hiện | Vì sao AI bỏ sót (nhận định của tôi) | Bổ sung/sửa chữa |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Việc còn lại

1. Người kiểm thử review **BUG-FR02-01** và **BUG-FR02-02**; sau khi xác nhận thì chụp screenshot và mở GitHub Issue kèm ảnh.
2. Viết AI Gap Analysis cho FR02 và AI Critique (phần của sinh viên).
3. Bổ sung bằng chứng screenshot/Issue vào báo cáo sau khi có.
