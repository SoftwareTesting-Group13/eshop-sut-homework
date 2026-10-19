# BUG-FR02-01 — Bộ đếm đăng nhập sai tăng 2 thay vì 1 khiến tài khoản bị khóa sớm sau 2 lần sai

## Tóm tắt

Đăng nhập sai mật khẩu bằng tài khoản đã đăng ký làm server cộng **2** vào `login_attempts` thay vì **1**, nên chỉ sau 2 lần sai bộ đếm đã đạt ngưỡng và tài khoản bị khóa. Đặc tả yêu cầu mỗi lần sai chỉ tăng **đúng 1 đơn vị** và chỉ khóa khi sai **từ 3 lần trở lên liên tiếp**.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | `FR-02` — Đăng nhập & Khóa tài khoản; `R2` (mỗi lần sai tăng đúng 1) và `R3` (khóa khi sai ≥ 3 lần) — [`README.md` §FR-02](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f3162660d5c4f9005cbb15910290adb4b58ef2c7/README.md#fr-02-đăng-nhập--khóa-tài-khoản) |
| Test case | `DT-02` (= `BVA-01`/`B3`: quan sát `login_attempts` sau 1 lần sai); `BVA-02` (biên ngay dưới ngưỡng — 2 lần sai phải **chưa** khóa); `BVA-03` (đạt ngưỡng thì khóa — dùng đối chiếu hệ quả khóa sớm) |
| Build / môi trường | commit `f3162660d5c4f9005cbb15910290adb4b58ef2c7`; Node v26.9.0, Express + SQLite; base URL `http://localhost:3000`; `POST /api/login`; quan sát `users.login_attempts`/`locked_until` trong DB test |
| Severity / Priority | High / High — vi phạm trực tiếp business rule cốt lõi R2/R3; người dùng bị khóa oan chỉ sau 2 lần sai |
| Trạng thái / lặp lại | Đã xác nhận bởi người kiểm thử; 2/2 fixture độc lập |

## Chuẩn bị để tái hiện

- **Fixture:** tài khoản `fr02.wrong@eshop.com` / `Passw0rd!` (tạo qua `POST /api/register`). Mật khẩu sai dùng ở bước tái hiện: `WrongPass1!`.
- **Trạng thái ban đầu:** `users.login_attempts = 0`, `users.locked_until = NULL` cho tài khoản trên.
- **SUT:** server Node/Express (`backend/server.js`), DB SQLite tại `backend/database.sqlite` (đường dẫn do `backend/database.js` resolve theo `__dirname`). Lần chạy gốc dùng một **instance cách ly** trong thư mục tạm (bản sao `server.js`/`database.js`, `database.sqlite` riêng) để **không sửa DB làm việc**; phần dưới dựng lại instance tương tự và là **tái hiện thủ công**.
- **Reset dữ liệu:** chỉ tác động DB test của instance cách ly; lệnh `UPDATE` chỉ sửa tài khoản fixture nêu trên.

```bash
# --- Dựng instance cách ly (chạy từ thư mục gốc repo) ---
WORK="$TMPDIR/fr02-repro"; mkdir -p "$WORK/backend"
cp backend/server.js backend/database.js backend/package.json "$WORK/backend/"
ln -sfn "$PWD/backend/node_modules" "$WORK/backend/node_modules"
DB="$WORK/backend/database.sqlite"

# --- Khởi động SUT (cổng 3000) rồi chờ sẵn sàng ---
(cd "$WORK/backend" && node server.js >"$WORK/server.log" 2>&1 &)
sleep 1

# --- Tạo fixture và đưa về trạng thái sạch ---
curl -s -X POST http://localhost:3000/api/register -H 'Content-Type: application/json' \
  --data-raw '{"name":"FR02 Wrong","email":"fr02.wrong@eshop.com","password":"Passw0rd!"}'
sqlite3 "$DB" "UPDATE users SET login_attempts=0, locked_until=NULL WHERE email='fr02.wrong@eshop.com';"
```

## Các bước tái hiện và kết quả

1. Gửi `POST /api/login` với mật khẩu sai (lần sai 1).
2. Đọc `login_attempts` của tài khoản ngay sau đó.
3. Lặp lại bước 1 (lần sai 2) và đọc `login_attempts` cùng `locked_until` để xem ngưỡng khóa có bị kích hoạt sớm không.

```bash
# Lần sai 1
curl -s -X POST http://localhost:3000/api/login -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.wrong@eshop.com","password":"WrongPass1!"}'
sqlite3 "$DB" "SELECT login_attempts, locked_until FROM users WHERE email='fr02.wrong@eshop.com';"

# Lần sai 2
curl -s -X POST http://localhost:3000/api/login -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.wrong@eshop.com","password":"WrongPass1!"}'
sqlite3 "$DB" "SELECT login_attempts, locked_until FROM users WHERE email='fr02.wrong@eshop.com';"
```

| Mốc / bước | Expected theo rule | Actual quan sát được |
| --- | --- | --- |
| Lần sai 1 (từ `login_attempts = 0`) | HTTP 401, không token; `login_attempts = 1` | HTTP 401 `Invalid email or password`; `login_attempts = 2` |
| Lần sai 2 (từ `login_attempts = 2` thực tế) | HTTP 401; `login_attempts = 2` (**từ 0 cộng đúng 2 lần**); `locked_until = NULL` — chưa đạt ngưỡng 3 nên chưa khóa | `login_attempts = 4`; `locked_until` bị đặt (`now + ~180 s`) ⇒ tài khoản **bị khóa ngay ở lần sai thứ 2** |

**Kết luận:** Server vi phạm R2 — mỗi lần sai phải tăng `login_attempts` đúng 1 đơn vị, nhưng thực tế tăng 2. Vì điều kiện khóa là `login_attempts >= 3` (đúng theo R3), việc tăng gấp đôi khiến ngưỡng bị chạm chỉ sau **2** lần sai, tức người dùng bị khóa sớm hơn đặc tả một lần đăng nhập.

## Bằng chứng

- Log/run: [`evidence/ev-DT-02.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR02/evidence/ev-DT-02.log), [`evidence/ev-DT-02-rerun.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR02/evidence/ev-DT-02-rerun.log), [`evidence/ev-BVA-02.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR02/evidence/ev-BVA-02.log); tổng hợp EV tại [`evidence/FR02-evidence.md`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR02/evidence/FR02-evidence.md) (EV-FR02-003/004/011, run `run-20261020-fr02`).
- Screenshot: ảnh dưới đây cho thấy chuỗi `login_attempts` 0 → 2 → 4 và `locked_until` được đặt ngay sau lần sai thứ 2, khớp với log.

  ![BUG-FR02-01 — login_attempts 0 → 2 → 4 và locked_until](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR02/screenshots/BUG-FR02-01.png)

- Lặp lại: **2/2** — hai fixture độc lập `fr02.wrong@eshop.com` (`DT-02`) và `fr02.rerun@eshop.com` (rerun trong `ev-DT-02-rerun.log`) đều cho `login_attempts` tăng 2 sau một lần sai.

## Điều tra nguyên nhân (chỉ khi đã kiểm chứng)

**Vị trí:** [`backend/server.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f3162660d5c4f9005cbb15910290adb4b58ef2c7/backend/server.js#L54) dòng `54`.

```js
} else {
  const newAttempts = user.login_attempts + 2;
  let lockedUntil = null;
  if (newAttempts >= 3) {
    lockedUntil = new Date(Date.now() + 180000).toISOString();
  }
```

**Cơ chế:** Ở nhánh mật khẩu sai, server tính `newAttempts = user.login_attempts + 2` rồi ghi giá trị này vào DB, trong khi R2 yêu cầu tăng đúng 1. Do đó từ `login_attempts = 0`, chỉ một lần sai đã cho `2`, và lần sai thứ hai cho `4`. Vì điều kiện khóa `newAttempts >= 3` (đúng theo R3 nếu bộ đếm tăng đúng) bị chạm ngay từ sau lần sai thứ hai, tài khoản bị khóa sớm hơn đặc tả.

Đây là nhận định từ mã nguồn; Expected và Actual ở trên dựa trên đặc tả và lần chạy thực tế. Trích đúng phiên bản commit đã kiểm thử.
