# FR02 — Evidence log (nhật ký bằng chứng thực thi)

> Mỗi lần thử một test case có một mục `EV-ID`; rerun dùng `EV-ID` mới, giữ lịch sử. Kết quả thô quan sát được, không chép Expected vào Actual.

## Thông tin phiên chạy

| Mục | Giá trị |
| --- | --- |
| Feature | FR02 — Đăng nhập & Khóa tài khoản |
| Interface | API `POST /api/login`, `GET /api/users/me`, `POST /api/register` (tạo fixture) |
| SUT / build | `eshop-sut-homework` commit `f3162660d5c4f9005cbb15910290adb4b58ef2c7` |
| Môi trường | macOS; Node v26.9.0; backend Node/Express + SQLite; instance cách ly (bản sao `server.js`/`database.js`, `database.sqlite` riêng, `node_modules` symlink) |
| Thời điểm chạy | 2026-10-20 00:25–00:27 +0700 (mỗi mục có timestamp trong file log) |
| Người/agent thực thi | AI agent (theo skill); screenshot Issue: người kiểm thử chụp sau khi xác nhận bug |
| Thư mục evidence | `evidence/` |
| Cách reset state | Tài khoản fixture riêng cho mỗi ca; `sqlite3` cập nhật `login_attempts`/`locked_until` trên DB test |
| Database làm việc trước khi chạy | `backend/database.sqlite`, SHA-256 `c63f00544180ba1fbb1427a9b9dd3f1784842698809972f33ce90482e7420ba6` (chỉ seed, attempts=0) |
| Database test | `database.sqlite` trong thư mục tạm, tạo mới từ `database.js` khi khởi động server |

**Fixture:** `fr02.base`, `fr02.wrong`, `fr02.lock`, `fr02.reset`, `fr02.expired`, `fr02.thr`, `fr02.rerun` @ `eshop.com`, mật khẩu `Passw0rd!` (tạo qua `POST /api/register`, log `fixture-register.log`).

## Evidence items

### EV-FR02-001 — DT-01 đăng nhập thành công

| Trường | Giá trị |
| --- | --- |
| Test case | DT-01 |
| Run ID / lần thử | run-20261020-fr02 / 1 |
| Kỹ thuật | Domain/EP |
| Thời điểm | 2026-10-20 00:25:17 +0700 |
| Interface | API `POST /api/login` |
| Tiền điều kiện | `fr02.base@eshop.com`, `login_attempts=0`, `locked_until=NULL` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.base@eshop.com","password":"Passw0rd!"}'
```

**Kết quả thô:**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9…",
  "user": {
    "id": 3,
    "email": "fr02.base@eshop.com",
    "password": "Passw0rd!",
    "role": "user",
    "login_attempts": 0,
    "locked_until": null
  }
}
```
```text
HTTP 200 · post-state login_attempts=0 locked_until=NULL
```

- **Expected (oracle ref):** R1 — thành công trả JWT Token.
- **Actual:** 200, có `token`; `login_attempts=0`.
- **Status:** `PASS`
- **Artifact:** `evidence/ev-DT-01.log`
- **Bug liên quan:** không (ghi nhận `password` plaintext là quan sát ngoài phạm vi).
- **Screenshot / Issue:** Không áp dụng.

---

### EV-FR02-002 — DT-01 token dùng được cho request xác thực

| Trường | Giá trị |
| --- | --- |
| Test case | DT-01 |
| Run ID / lần thử | run-20261020-fr02 / 2 |
| Kỹ thuật | Domain/EP |
| Thời điểm | 2026-10-20 00:27 +0700 |
| Interface | API `GET /api/users/me` |
| Tiền điều kiện | token lấy từ đăng nhập `fr02.base@eshop.com` |

**Thao tác / lệnh:**
```zsh
TOKEN=$(curl -s -X POST http://localhost:3000/api/login -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.base@eshop.com","password":"Passw0rd!"}' \
  | node -e "let d='';process.stdin.on('data',c=>d+=c).on('end',()=>console.log(JSON.parse(d).token))")
curl -s -w "\nHTTP_STATUS:%{http_code}\n" http://localhost:3000/api/users/me \
  -H "Authorization: Bearer $TOKEN"
```

**Kết quả thô:**
```json
{
  "id": 3,
  "name": "FR02 base",
  "email": "fr02.base@eshop.com",
  "password": "Passw0rd!",
  "role": "user",
  "login_attempts": 0,
  "locked_until": null,
  "reset_token": null,
  "shipping_address": null,
  "phone": null
}
```
```text
HTTP 200
```

- **Expected (oracle ref):** R1 — token hợp lệ cho request xác thực.
- **Actual:** 200 với token.
- **Status:** `PASS`
- **Artifact:** `evidence/ev-DT-01-token-check.log`
- **Bug liên quan:** không.
- **Screenshot / Issue:** Không áp dụng.

---

### EV-FR02-003 — DT-02/BVA-01 một lần sai đầu tiên

| Trường | Giá trị |
| --- | --- |
| Test case | DT-02 |
| Run ID / lần thử | run-20261020-fr02 / 1 |
| Kỹ thuật | Domain/EP + BVA |
| Thời điểm | 2026-10-20 00:25 +0700 |
| Interface | API `POST /api/login` |
| Tiền điều kiện | `fr02.wrong@eshop.com`, `login_attempts=0`, `locked_until=NULL` |

**Thao tác / lệnh:**
```zsh
sqlite3 "$SUT/database.sqlite" "SELECT login_attempts,locked_until FROM users WHERE email='fr02.wrong@eshop.com';"
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.wrong@eshop.com","password":"WrongPass1!"}'
sqlite3 "$SUT/database.sqlite" "SELECT login_attempts,locked_until FROM users WHERE email='fr02.wrong@eshop.com';"
```

**Kết quả thô:**
```json
{
  "error": "Invalid email or password"
}
```
```text
HTTP 401 · pre-state login_attempts=0 · post-state login_attempts=2 locked_until=NULL
```

- **Expected (oracle ref):** R2 — bộ đếm tăng **đúng 1** (0→1); R3 — chưa khóa.
- **Actual:** bộ đếm = 2 (tăng 2), chưa khóa.
- **Status:** `FAIL`
- **Artifact:** `evidence/ev-DT-02.log`
- **Bug liên quan:** BUG-FR02-01.
- **Screenshot / Issue:** `screenshots/BUG-FR02-01.png`; Issue [#23](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/23) (đã xác nhận).

---

### EV-FR02-004 — DT-02 rerun (độ lặp lại BUG-FR02-01)

| Trường | Giá trị |
| --- | --- |
| Test case | DT-02 |
| Run ID / lần thử | run-20261020-fr02 / 2 |
| Kỹ thuật | Domain/EP |
| Thời điểm | 2026-10-20 00:27 +0700 |
| Interface | API `POST /api/login` |
| Tiền điều kiện | `fr02.rerun@eshop.com`, `login_attempts=0` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.rerun@eshop.com","password":"WrongPass1!"}'
sqlite3 "$SUT/database.sqlite" "SELECT login_attempts FROM users WHERE email='fr02.rerun@eshop.com';"
```

**Kết quả thô:**
```json
{
  "error": "Invalid email or password"
}
```
```text
HTTP 401 · post-state login_attempts=2
```

- **Expected (oracle ref):** R2 — tăng đúng 1 (0→1).
- **Actual:** `login_attempts=2`.
- **Status:** `FAIL`
- **Artifact:** `evidence/ev-DT-02-rerun.log`
- **Bug liên quan:** BUG-FR02-01 (tái hiện 2/2).
- **Screenshot / Issue:** `screenshots/BUG-FR02-01.png`; Issue [#23](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/23) (đã xác nhận).

---

### EV-FR02-005 — DT-03 email chưa đăng ký

| Trường | Giá trị |
| --- | --- |
| Test case | DT-03 |
| Run ID / lần thử | run-20261020-fr02 / 1 |
| Kỹ thuật | Domain/EP |
| Thời điểm | 2026-10-20 00:25 +0700 |
| Interface | API `POST /api/login` |
| Tiền điều kiện | `nobody.fr02@eshop.com` chưa tồn tại |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"nobody.fr02@eshop.com","password":"Passw0rd!"}'
sqlite3 "$SUT/database.sqlite" "SELECT COUNT(*) FROM users WHERE email='nobody.fr02@eshop.com';"
```

**Kết quả thô:**
```json
{
  "error": "Invalid email or password"
}
```
```text
HTTP 401 · số user khớp email = 0
```

- **Expected (oracle ref):** R1/R7 — thất bại, không token; không có tài khoản để tăng bộ đếm.
- **Actual:** 401, không token, không tạo user.
- **Status:** `PASS`
- **Artifact:** `evidence/ev-DT-03.log`
- **Bug liên quan:** không.
- **Screenshot / Issue:** Không áp dụng.

---

### EV-FR02-006 — DT-04 mật khẩu rỗng

| Trường | Giá trị |
| --- | --- |
| Test case | DT-04 |
| Run ID / lần thử | run-20261020-fr02 / 1 |
| Kỹ thuật | Domain/EP |
| Thời điểm | 2026-10-20 00:25 +0700 |
| Interface | API `POST /api/login` |
| Tiền điều kiện | `fr02.base@eshop.com` tồn tại |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.base@eshop.com","password":""}'
```

**Kết quả thô:**
```json
{
  "error": "Invalid email or password"
}
```
```text
HTTP 401 · post-state login_attempts=2 locked_until=NULL
```

- **Expected (oracle ref):** R1 — thất bại, không token.
- **Actual:** 401, không token.
- **Status:** `PASS`
- **Artifact:** `evidence/ev-DT-04-05.log`
- **Bug liên quan:** không (việc tăng bộ đếm là BUG-FR02-01).
- **Screenshot / Issue:** Không áp dụng.

---

### EV-FR02-007 — DT-05 email rỗng/thiếu trường

| Trường | Giá trị |
| --- | --- |
| Test case | DT-05 |
| Run ID / lần thử | run-20261020-fr02 / 1 |
| Kỹ thuật | Domain/EP |
| Thời điểm | 2026-10-20 00:25 +0700 |
| Interface | API `POST /api/login` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"","password":"Passw0rd!"}'
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{}'
```

**Kết quả thô:**
```json
{
  "error": "Invalid email or password"
}
```
```text
HTTP 401 · HTTP 401 (cả hai biến thể)
```

- **Expected (oracle ref):** R1 — thất bại, không token.
- **Actual:** 401, không token cho cả `email=""` và body `{}`.
- **Status:** `PASS`
- **Artifact:** `evidence/ev-DT-04-05.log`
- **Bug liên quan:** không.
- **Screenshot / Issue:** Không áp dụng.

---

### EV-FR02-008 — DT-06 email sai định dạng

| Trường | Giá trị |
| --- | --- |
| Test case | DT-06 |
| Run ID / lần thử | run-20261020-fr02 / 1 |
| Kỹ thuật | Domain/EP (oracle chưa xác định) |
| Thời điểm | 2026-10-20 00:25 +0700 |
| Interface | API `POST /api/login` |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"not-an-email","password":"Passw0rd!"}'
```

**Kết quả thô:**
```json
{
  "error": "Invalid email or password"
}
```
```text
HTTP 401
```

- **Expected (oracle ref):** Chưa xác định theo đặc tả (R4 chỉ ràng buộc `type="email"` ở UI; API không định nghĩa).
- **Actual:** 401, không token.
- **Status:** `INCONCLUSIVE (Quan sát)` — không chấm PASS/FAIL.
- **Artifact:** `evidence/ev-DT-06.log`
- **Bug liên quan:** không.
- **Screenshot / Issue:** Không áp dụng.

---

### EV-FR02-009 — DT-07 tài khoản khóa + mật khẩu đúng

| Trường | Giá trị |
| --- | --- |
| Test case | DT-07 |
| Run ID / lần thử | run-20261020-fr02 / 2 (rerun sau khi sửa fixture) |
| Kỹ thuật | Domain/EP |
| Thời điểm | 2026-10-20 00:25 +0700 |
| Interface | API `POST /api/login` |
| Tiền điều kiện | `fr02.lock@eshop.com`, `login_attempts=3`, `locked_until=2026-10-19T17:35:42.298Z` (tương lai) |

**Thao tác / lệnh:**
```zsh
FUT=$(node -e "console.log(new Date(Date.now()+600000).toISOString())")
sqlite3 "$SUT/database.sqlite" "UPDATE users SET login_attempts=3, locked_until='$FUT' WHERE email='fr02.lock@eshop.com';"
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.lock@eshop.com","password":"Passw0rd!"}'
sqlite3 "$SUT/database.sqlite" "SELECT login_attempts,locked_until FROM users WHERE email='fr02.lock@eshop.com';"
```

**Kết quả thô:**
```json
{
  "error": "Tài khoản đã bị khóa. Vui lòng thử lại sau."
}
```
```text
HTTP 403 · post-state login_attempts=3 locked_until=2026-10-19T17:35:42.298Z (không đổi)
```

- **Expected (oracle ref):** R6 — tài khoản đang khóa thì bị từ chối, không cấp token; bộ đếm giữ nguyên.
- **Actual:** 403 thông báo khóa, không token, bộ đếm/khóa không đổi.
- **Status:** `PASS`
- **Artifact:** `evidence/ev-DT-07-08.log`
- **Ghi chú:** Lần thử 1 dùng fixture sai định dạng (`datetime('now')` UTC bị JS hiểu là giờ local) nên bị bỏ; rerun dùng ISO UTC đúng như server ghi.
- **Bug liên quan:** không.
- **Screenshot / Issue:** Không áp dụng.

---

### EV-FR02-010 — DT-08 tài khoản khóa + mật khẩu sai

| Trường | Giá trị |
| --- | --- |
| Test case | DT-08 |
| Run ID / lần thử | run-20261020-fr02 / 2 |
| Kỹ thuật | Domain/EP |
| Thời điểm | 2026-10-20 00:25 +0700 |
| Interface | API `POST /api/login` |
| Tiền điều kiện | `fr02.lock@eshop.com` đang khóa (như DT-07) |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.lock@eshop.com","password":"WrongPass1!"}'
sqlite3 "$SUT/database.sqlite" "SELECT login_attempts,locked_until FROM users WHERE email='fr02.lock@eshop.com';"
```

**Kết quả thô:**
```json
{
  "error": "Tài khoản đã bị khóa. Vui lòng thử lại sau."
}
```
```text
HTTP 403 · post-state login_attempts=3 locked_until=2026-10-19T17:35:42.298Z (không đổi)
```

- **Expected (oracle ref):** R6 — bị từ chối với trạng thái khóa; không tăng bộ đếm thêm.
- **Actual:** 403, bộ đếm không đổi.
- **Status:** `PASS`
- **Artifact:** `evidence/ev-DT-07-08.log`
- **Bug liên quan:** không.
- **Screenshot / Issue:** Không áp dụng.

---

### EV-FR02-011 — BVA-02 hai lần sai liên tiếp (ngay dưới ngưỡng)

| Trường | Giá trị |
| --- | --- |
| Test case | BVA-02 |
| Run ID / lần thử | run-20261020-fr02 / 1 |
| Kỹ thuật | BVA |
| Thời điểm | 2026-10-19T17:25:58–59Z (2026-10-20 00:25:58 +0700) |
| Interface | API `POST /api/login` |
| Tiền điều kiện | `fr02.wrong@eshop.com` reset `login_attempts=0`, `locked_until=NULL` |

**Thao tác / lệnh:**
```zsh
sqlite3 "$SUT/database.sqlite" "UPDATE users SET login_attempts=0, locked_until=NULL WHERE email='fr02.wrong@eshop.com';"
curl -s -X POST http://localhost:3000/api/login -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.wrong@eshop.com","password":"WrongPass1!"}'
curl -s -X POST http://localhost:3000/api/login -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.wrong@eshop.com","password":"WrongPass1!"}'
sqlite3 "$SUT/database.sqlite" "SELECT login_attempts,locked_until FROM users WHERE email='fr02.wrong@eshop.com';"
```

**Kết quả thô:**
```text
failure #1 → HTTP 401, post-state login_attempts=2 locked_until=NULL
failure #2 → HTTP 401, post-state login_attempts=4 locked_until=2026-10-19T17:28:59.028Z
```
```text
locked_until − now = 2026-10-19T17:28:59.028Z − 2026-10-19T17:25:59.014Z ≈ 180.014 s
```

- **Expected (oracle ref):** B1 ngay dưới — sau 2 lần sai: `login_attempts=2`, **chưa khóa**.
- **Actual:** `login_attempts=4` và **đã khóa** (khóa sớm do tăng 2); `locked_until` ≈ +180 s.
- **Status:** `FAIL`
- **Artifact:** `evidence/ev-BVA-02.log`
- **Bug liên quan:** BUG-FR02-01 (khóa sau 2 lần sai), BUG-FR02-02 (180 s).
- **Screenshot / Issue:** `screenshots/BUG-FR02-01.png` (Issue [#23](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/23)), `screenshots/BUG-FR02-02.png` (Issue [#24](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/24)) — đã xác nhận.

---

### EV-FR02-012 — BVA-03 lần sai thứ 3 (tại biên)

| Trường | Giá trị |
| --- | --- |
| Test case | BVA-03 |
| Run ID / lần thử | run-20261020-fr02 / 1 |
| Kỹ thuật | BVA |
| Thời điểm | 2026-10-19T17:26:02Z |
| Interface | API `POST /api/login` |
| Tiền điều kiện | `fr02.thr@eshop.com`, `login_attempts=2`, `locked_until=NULL` (đã sai 2 lần) |

**Thao tác / lệnh:**
```zsh
sqlite3 "$SUT/database.sqlite" "UPDATE users SET login_attempts=2, locked_until=NULL WHERE email='fr02.thr@eshop.com';"
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.thr@eshop.com","password":"WrongPass1!"}'
sqlite3 "$SUT/database.sqlite" "SELECT login_attempts,locked_until FROM users WHERE email='fr02.thr@eshop.com';"
```

**Kết quả thô:**
```json
{
  "error": "Invalid email or password"
}
```
```text
HTTP 401 · pre-state login_attempts=2 · post-state login_attempts=4 locked_until=2026-10-19T17:29:02.202Z
```

- **Expected (oracle ref):** B1 tại biên — tại/qua 3 lần sai thì **khóa tài khoản**.
- **Actual:** tài khoản bị khóa (`locked_until` được đặt) ⇒ khóa kích hoạt ở ngưỡng. Bộ đếm = 4 (thuộc nghĩa vụ B3/DT-02) và thời lượng 180 s (thuộc B2/BVA-06).
- **Status:** `PASS` (chỉ chấm việc kích hoạt khóa tại ngưỡng).
- **Artifact:** `evidence/ev-BVA-03-04.log`
- **Bug liên quan:** không (đối với nghĩa vụ của ca này).
- **Screenshot / Issue:** Không áp dụng.

---

### EV-FR02-013 — BVA-04 gửi thêm khi đang khóa (ngay trên ngưỡng)

| Trường | Giá trị |
| --- | --- |
| Test case | BVA-04 |
| Run ID / lần thử | run-20261020-fr02 / 1 |
| Kỹ thuật | BVA |
| Thời điểm | 2026-10-19T17:26:02Z |
| Interface | API `POST /api/login` |
| Tiền điều kiện | `fr02.wrong@eshop.com` đang khóa (`locked_until=2026-10-19T17:28:59.028Z`) |

**Thao tác / lệnh:**
```zsh
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.wrong@eshop.com","password":"Passw0rd!"}'
sqlite3 "$SUT/database.sqlite" "SELECT login_attempts,locked_until FROM users WHERE email='fr02.wrong@eshop.com';"
```

**Kết quả thô:**
```json
{
  "error": "Tài khoản đã bị khóa. Vui lòng thử lại sau."
}
```
```text
HTTP 403 · post-state login_attempts=4 locked_until=2026-10-19T17:28:59.028Z (không đổi)
```

- **Expected (oracle ref):** B1 ngay trên / R6 — bị từ chối, bộ đếm và khóa không đổi.
- **Actual:** 403, không đổi.
- **Status:** `PASS`
- **Artifact:** `evidence/ev-BVA-03-04.log`
- **Bug liên quan:** không.
- **Screenshot / Issue:** Không áp dụng.

---

### EV-FR02-014 — BVA-05 trong cửa sổ 30 s (t0+29 s)

| Trường | Giá trị |
| --- | --- |
| Test case | BVA-05 |
| Run ID / lần thử | run-20261020-fr02 / 1 |
| Kỹ thuật | BVA |
| Thời điểm | t0 = 2026-10-19T17:26:10.181Z; thử lúc 17:26:39.350Z |
| Interface | API `POST /api/login` |
| Tiền điều kiện | `fr02.thr@eshop.com` vừa bị khóa tại t0 |

**Thao tác / lệnh:**
```zsh
# t0: gây khóa bằng lần sai thứ 3
curl -s -X POST http://localhost:3000/api/login -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.thr@eshop.com","password":"WrongPass1!"}'
sleep 29
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.thr@eshop.com","password":"Passw0rd!"}'
```

**Kết quả thô:**
```json
{
  "error": "Tài khoản đã bị khóa. Vui lòng thử lại sau."
}
```
```text
t0 = 2026-10-19T17:26:10.181Z, locked_until = 2026-10-19T17:29:10.196Z
thử lúc t0+29.17 s → HTTP 403
```

- **Expected (oracle ref):** B2 ngay dưới — còn trong 30 s thì vẫn bị khóa.
- **Actual:** 403 tại `t0+29 s`.
- **Status:** `PASS`
- **Artifact:** `evidence/ev-BVA-05-06.log`
- **Bug liên quan:** không.
- **Screenshot / Issue:** Không áp dụng.

---

### EV-FR02-015 — BVA-06 quá 30 s (t0+31 s)

| Trường | Giá trị |
| --- | --- |
| Test case | BVA-06 |
| Run ID / lần thử | run-20261020-fr02 / 1 |
| Kỹ thuật | BVA |
| Thời điểm | thử lúc 2026-10-19T17:26:41.500Z (t0+31.3 s) |
| Interface | API `POST /api/login` |
| Tiền điều kiện | cùng tài khoản khóa tại t0 = 2026-10-19T17:26:10.181Z |

**Thao tác / lệnh:**
```zsh
sleep 2
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.thr@eshop.com","password":"Passw0rd!"}'
```

**Kết quả thô:**
```json
{
  "error": "Tài khoản đã bị khóa. Vui lòng thử lại sau."
}
```
```text
thử lúc t0+31.3 s → HTTP 403 · post-state login_attempts=4 locked_until=2026-10-19T17:29:10.196Z
```

- **Expected (oracle ref):** B2 tại/ngay trên — hết 30 s thì đăng nhập được, trả token.
- **Actual:** vẫn 403 (khóa 180 s).
- **Status:** `FAIL`
- **Artifact:** `evidence/ev-BVA-05-06.log`
- **Bug liên quan:** BUG-FR02-02.
- **Screenshot / Issue:** `screenshots/BUG-FR02-02.png`; Issue [#24](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/24) (đã xác nhận).

---

### EV-FR02-016 — BVA-07 đặt lại bộ đếm sau thành công

| Trường | Giá trị |
| --- | --- |
| Test case | BVA-07 |
| Run ID / lần thử | run-20261020-fr02 / 1 |
| Kỹ thuật | BVA |
| Thời điểm | 2026-10-19T17:26:45Z |
| Interface | API `POST /api/login` |
| Tiền điều kiện | `fr02.reset@eshop.com`, `login_attempts=0` |

**Thao tác / lệnh:**
```zsh
curl -s -X POST http://localhost:3000/api/login -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.reset@eshop.com","password":"WrongPass1!"}'
curl -s -X POST http://localhost:3000/api/login -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.reset@eshop.com","password":"Passw0rd!"}'
sqlite3 "$SUT/database.sqlite" "SELECT login_attempts,locked_until FROM users WHERE email='fr02.reset@eshop.com';"
```

**Kết quả thô:**
```text
1 lần sai → HTTP 401, post-state login_attempts=2
đăng nhập đúng → HTTP 200 (có token), post-state login_attempts=0 locked_until=NULL
```

- **Expected (oracle ref):** R5/B4 — thành công đặt bộ đếm về 0.
- **Actual:** `login_attempts=0`, `locked_until=NULL`.
- **Status:** `PASS`
- **Artifact:** `evidence/ev-BVA-07.log`
- **Bug liên quan:** không.
- **Screenshot / Issue:** Không áp dụng.

---

### EV-FR02-017 — BVA-08 trạng thái khóa đã hết hạn

| Trường | Giá trị |
| --- | --- |
| Test case | BVA-08 |
| Run ID / lần thử | run-20261020-fr02 / 1 |
| Kỹ thuật | BVA |
| Thời điểm | 2026-10-19T17:26:46Z |
| Interface | API `POST /api/login` |
| Tiền điều kiện | `fr02.expired@eshop.com`, `locked_until=2026-10-19T16:26:46.054Z` (quá khứ) |

**Thao tác / lệnh:**
```zsh
PAST=$(node -e "console.log(new Date(Date.now()-3600000).toISOString())")
sqlite3 "$SUT/database.sqlite" "UPDATE users SET login_attempts=3, locked_until='$PAST' WHERE email='fr02.expired@eshop.com';"
curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.expired@eshop.com","password":"Passw0rd!"}'
```

**Kết quả thô:**
```text
pre-state login_attempts=3 locked_until=2026-10-19T16:26:46.054Z
→ HTTP 200 (có token); post-state login_attempts=0 locked_until=NULL
```

- **Expected (oracle ref):** R3/R6 — hết hạn khóa thì đăng nhập được.
- **Actual:** 200 + token.
- **Status:** `PASS`
- **Artifact:** `evidence/ev-BVA-08.log`
- **Bug liên quan:** không.
- **Screenshot / Issue:** Không áp dụng.

---

## Tổng hợp evidence

| Chỉ số | Số lượng |
| --- | ---: |
| Ca thiết kế | 15 |
| Ca đã chạy duy nhất trong run được chọn | 15 |
| Tổng lần thử thực thi (EV-ID) | 17 |
| PASS | 11 |
| FAIL | 3 |
| Quan sát / Inconclusive | 1 |
| BLOCKED (nêu lý do) | 0 |

- **Artifact thô:** `fixture-register.log`, `ev-DT-01.log`, `ev-DT-01-token-check.log`, `ev-DT-02.log`, `ev-DT-02-rerun.log`, `ev-DT-03.log`, `ev-DT-04-05.log`, `ev-DT-06.log`, `ev-DT-07-08.log`, `ev-BVA-02.log`, `ev-BVA-03-04.log`, `ev-BVA-05-06.log`, `ev-BVA-07.log`, `ev-BVA-08.log`, `final-db-state.log`, `../screenshots/BUG-FR02-01.png`, `../screenshots/BUG-FR02-02.png`.
- **Đối chiếu catalog:** mọi T-ID được tính đã chạy đều có ít nhất một EV-ID của run; DT-01 và DT-02 có thêm EV rerun/xác nhận token; không có EV-ID mồ côi.

## Xác nhận cleanup sau khi hoàn tất

| Mục | Kết quả thực tế |
| --- | --- |
| Test services đã dừng | `kill 80029`; `lsof -nP -iTCP:3000 -sTCP:LISTEN` → `PORT3000_FREE` |
| Database test/file tạm đã xóa | `rm -rf` thư mục SUT tạm `/private/.../T/opencode/fr02-sut`; đã xác nhận không còn thư mục |
| Database làm việc đã trở về trạng thái trước khi chạy | `backend/database.sqlite` SHA-256 vẫn `c63f00544180ba1fbb1427a9b9dd3f1784842698809972f33ce90482e7420ba6` (khớp trước khi chạy); `git status` không có thay đổi ngoài `features/` mới |
