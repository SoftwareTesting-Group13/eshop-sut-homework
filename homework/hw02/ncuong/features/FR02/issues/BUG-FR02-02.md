# [BUG-FR02-02] Thời lượng khóa tài khoản là 180 giây thay vì 30 giây

- **GitHub Issue:** [#24](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/24) — kèm screenshot `BUG-FR02-02.png`
- **Feature:** FR02 — Đăng nhập & Khóa tài khoản
- **Test case liên quan:** BVA-02 (đo `locked_until`), BVA-06
- **Requirement:** `README.md` §2 FR-02 (R3 — khóa tạm 30 giây)
- **Severity / Priority:** Medium / High
- **Trạng thái:** Đã tái hiện 2/2, đã được người kiểm thử xác nhận
- **Evidence:** `features/FR02/evidence/ev-BVA-02.log`, `ev-BVA-05-06.log`; `features/FR02/screenshots/BUG-FR02-02.png`

**Environment:** commit `f3162660d5c4f9005cbb15910290adb4b58ef2c7`; backend Node/Express + SQLite chạy cách ly; base URL `http://localhost:3000`; API `POST /api/login`; đo thời lượng bằng `locked_until − now`.

**Preconditions:**
- Tài khoản chưa khóa (`fr02.thr@eshop.com` / `Passw0rd!`).
- Kích hoạt khóa bằng lần sai đưa bộ đếm qua ngưỡng; ghi lại thời điểm khóa `t0`.

**Steps to reproduce:**
1. Kích hoạt khóa tài khoản (chuẩn bị `login_attempts = 2` rồi gửi 1 lần sai).
2. Đọc `locked_until`; so với `t0`.
3. Chờ tới `t0 + 31 s`, gửi `POST /api/login` với mật khẩu **đúng**.

| Bước | Input / hành động | Quan sát |
| --- | --- | --- |
| 1–2 | đọc `locked_until` sau khóa | `locked_until − now ≈ 180.014 s` (kỳ vọng 30 s) |
| 3 | tại `t0 + 31 s`, mật khẩu đúng | HTTP 403 `Tài khoản đã bị khóa. Vui lòng thử lại sau.` (kỳ vọng 200 + token) |

**Expected:** khóa tạm **30 giây**; hết 30 giây thì đăng nhập lại được (R3).

**Actual:** khóa 180 giây; vẫn bị từ chối ở `t0 + 31 s` (`seconds_remaining = 180`, `RETRY_AT = t0 + 31 s` vẫn 403).

**Độ lặp lại:** 2/2 (đo tại BVA-02 và quan sát tại BVA-06).

**Root cause:** `backend/server.js:57` dùng `Date.now() + 180000` thay vì `+ 30000`.

**Reproduce nhanh (API):**
```bash
sleep 31
curl -s -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.thr@eshop.com","password":"Passw0rd!"}'
```

**Screenshot xác nhận:**

![BUG-FR02-02 — locked_until còn 180 giây, retry ở t0+31s vẫn 403](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR02/screenshots/BUG-FR02-02.png)
