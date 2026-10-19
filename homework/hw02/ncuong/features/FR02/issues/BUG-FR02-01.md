# [BUG-FR02-01] Bộ đếm đăng nhập sai tăng 2 thay vì 1 → khóa tài khoản sau 2 lần sai

- **GitHub Issue:** [#23](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/23) — kèm screenshot `BUG-FR02-01.png`
- **Feature:** FR02 — Đăng nhập & Khóa tài khoản
- **Test case liên quan:** DT-02 (đồng thời BVA-01), BVA-02, BVA-03
- **Requirement:** `README.md` §2 FR-02 (R2 — tăng bộ đếm đúng 1 đơn vị mỗi lần sai; R3 — sai từ 3 lần trở lên liên tiếp mới khóa 30 giây)
- **Severity / Priority:** High / High
- **Trạng thái:** Đã tái hiện 2/2, đã được người kiểm thử xác nhận
- **Evidence:** `features/FR02/evidence/ev-DT-02.log`, `ev-DT-02-rerun.log`, `ev-BVA-02.log`; `features/FR02/screenshots/BUG-FR02-01.png`

**Environment:** commit `f3162660d5c4f9005cbb15910290adb4b58ef2c7`; backend Node/Express + SQLite chạy cách ly; base URL `http://localhost:3000`; API `POST /api/login`; kiểm tra bộ đếm bằng đọc DB test.

**Preconditions:**
- Tài khoản `fr02.wrong@eshop.com` / `Passw0rd!` tồn tại.
- DB test có `login_attempts = 0`, `locked_until = NULL`.

**Steps to reproduce:**
1. Gửi `POST /api/login` với `{"email":"fr02.wrong@eshop.com","password":"WrongPass1!"}`.
2. Đọc `login_attempts` của tài khoản trong DB.
3. Lặp bước 1 một lần nữa (mô phỏng 2 lần sai liên tiếp) và đọc lại `login_attempts`, `locked_until`.

| Bước | Input / hành động | Quan sát |
| --- | --- | --- |
| 1 | sai lần 1 | HTTP 401 `Invalid email or password`; `login_attempts = 2` (kỳ vọng 1) |
| 3 | sai lần 2 | `login_attempts = 4`; `locked_until` bị đặt ⇒ **khóa ngay ở lần sai thứ 2** (kỳ vọng chưa khóa) |

**Expected:** sau lần sai thứ nhất `login_attempts = 1`; chỉ khi sai **từ 3 lần trở lên liên tiếp** mới khóa tài khoản (R2, R3).

**Actual:** mỗi lần sai cộng 2, nên chỉ sau 2 lần sai bộ đếm đã `= 4 ≥ 3` và tài khoản bị khóa sớm hơn đặc tả.

**Độ lặp lại:** 2/2 (chạy lại trên tài khoản `fr02.rerun@eshop.com` cho cùng kết quả `login_attempts = 2`).

**Root cause:** `backend/server.js:54` dùng `user.login_attempts + 2` thay vì `+ 1`.

**Reproduce nhanh (API):**
```bash
curl -s -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.wrong@eshop.com","password":"WrongPass1!"}'
sqlite3 backend/database.sqlite "SELECT login_attempts,locked_until FROM users WHERE email='fr02.wrong@eshop.com';"
```

**Screenshot xác nhận:**

![BUG-FR02-01 — login_attempts 0 → 2 → 4 và locked_until](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR02/screenshots/BUG-FR02-01.png)
