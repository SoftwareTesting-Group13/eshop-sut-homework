# BUG-FR02-02 — Thời lượng khóa tài khoản là 180 giây thay vì 30 giây

## Tóm tắt

Khi tài khoản đạt ngưỡng sai liên tiếp, server đặt `locked_until = now + 180000 ms` và tiếp tục từ chối đăng nhập trong 180 giây; đặc tả yêu cầu khóa tạm **30 giây** rồi cho phép đăng nhập lại. Tại `t0 + 31 s` với mật khẩu **đúng**, tài khoản vẫn bị trả về 403.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | `FR-02` — Đăng nhập & Khóa tài khoản; `R3` (khóa tạm 30 giây) và `R6` (còn `locked_until` thì bị từ chối) — [`README.md` §FR-02](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f3162660d5c4f9005cbb15910290adb4b58ef2c7/README.md#fr-02-đăng-nhập--khóa-tài-khoản) |
| Test case | `BVA-02` (đo `locked_until − now` ngay sau khi khóa); `BVA-06` (biên trên `t0 + 31 s`, mật khẩu đúng phải đăng nhập được); `BVA-05` (đối chứng `t0 + 29 s` — còn trong cửa sổ khóa) |
| Build / môi trường | commit `f3162660d5c4f9005cbb15910290adb4b58ef2c7`; Node v26.9.0, Express + SQLite; base URL `http://localhost:3000`; `POST /api/login`; đo thời lượng bằng `locked_until − now` |
| Severity / Priority | Medium / High — thời lượng khóa sai gấp 6 lần khiến người dùng bị chặn lâu hơn đặc tả, nhưng tài khoản vẫn tự mở khóa |
| Trạng thái / lặp lại | Đã xác nhận bởi người kiểm thử; 2/2 sự kiện khóa trên 2 fixture độc lập (cùng run `run-20261020-fr02`) |

## Chuẩn bị để tái hiện

- **Fixture:** tài khoản `fr02.thr@eshop.com` / `Passw0rd!` (tạo qua `POST /api/register`). Mật khẩu sai dùng để kích hoạt khóa: `WrongPass1!`.
- **Trạng thái ban đầu:** tài khoản chưa khóa; đưa bộ đếm về sát ngưỡng bằng `login_attempts = 2`, `locked_until = NULL` (đã sai 2 lần) để lần sai kế tiếp chạm ngưỡng 3 và kích hoạt khóa.
- **SUT:** server Node/Express (`backend/server.js`), DB SQLite tại `backend/database.sqlite`. Lần chạy gốc dùng **instance cách ly** trong thư mục tạm (không sửa DB làm việc); phần dưới dựng lại và là **tái hiện thủ công**.
- **Reset dữ liệu:** chỉ dùng DB test của instance cách ly; lệnh `UPDATE` chỉ sửa tài khoản fixture nêu trên.

```bash
# --- Dựng instance cách ly (chạy từ thư mục gốc repo) ---
WORK="$TMPDIR/fr02-repro"; mkdir -p "$WORK/backend"
cp backend/server.js backend/database.js backend/package.json "$WORK/backend/"
ln -sfn "$PWD/backend/node_modules" "$WORK/backend/node_modules"
DB="$WORK/backend/database.sqlite"

# --- Khởi động SUT (cổng 3000) rồi chờ sẵn sàng ---
(cd "$WORK/backend" && node server.js >"$WORK/server.log" 2>&1 &)
sleep 1

# --- Tạo fixture và đưa bộ đếm về sát ngưỡng (chưa khóa) ---
curl -s -X POST http://localhost:3000/api/register -H 'Content-Type: application/json' \
  --data-raw '{"name":"FR02 Thr","email":"fr02.thr@eshop.com","password":"Passw0rd!"}'
sqlite3 "$DB" "UPDATE users SET login_attempts=2, locked_until=NULL WHERE email='fr02.thr@eshop.com';"
```

## Các bước tái hiện và kết quả

1. Ghi mốc `t0`, rồi kích hoạt khóa bằng một lần đăng nhập sai (đưa bộ đếm từ 2 qua ngưỡng 3).
2. Đọc `locked_until` ngay sau đó và tính `locked_until − now`.
3. Chờ tới `t0 + 31 s`, gửi `POST /api/login` với mật khẩu **đúng** và quan sát HTTP status.

```bash
# 1) Kích hoạt khóa tại t0
T0=$(node -e 'console.log(new Date().toISOString())'); echo "t0=$T0"
curl -s -X POST http://localhost:3000/api/login -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.thr@eshop.com","password":"WrongPass1!"}'

# 2) Đo thời lượng khóa
LU=$(sqlite3 "$DB" "SELECT locked_until FROM users WHERE email='fr02.thr@eshop.com';")
echo "locked_until=$LU"
node -e 'const lu=new Date(process.argv[1]);console.log("seconds_remaining",((lu-Date.now())/1000).toFixed(3))' "$LU"

# 3) Retry tại t0 + 31 s bằng mật khẩu ĐÚNG
sleep 31
echo "retry_at=$(node -e 'console.log(new Date().toISOString())')"
curl -s -i -X POST http://localhost:3000/api/login -H 'Content-Type: application/json' \
  --data-raw '{"email":"fr02.thr@eshop.com","password":"Passw0rd!"}' | sed -n '1p;$p'
```

| Mốc / bước | Expected theo rule | Actual quan sát được |
| --- | --- | --- |
| Ngay sau khi khóa (đo `locked_until − now`) | ≈ **30 000 ms** (`now + 30 s`) | ≈ **180 014 ms** (`now + 180 s`) |
| `t0 + 29 s`, mật khẩu **đúng** (BVA-05, đối chứng) | HTTP 403 — còn trong cửa sổ khóa | HTTP 403 `Tài khoản đã bị khóa. Vui lòng thử lại sau.` (khớp kỳ vọng) |
| `t0 + 31 s`, mật khẩu **đúng** (BVA-06) | HTTP 200 + JWT token — đã hết 30 s | HTTP 403 `Tài khoản đã bị khóa. Vui lòng thử lại sau.` — **vẫn khóa** |

**Kết luận:** Server vi phạm R3 — thời lượng khóa tạm phải là 30 giây, nhưng thực tế là 180 giây. Hệ quả: sau khi nhập sai đủ ngưỡng, người dùng bị chặn đăng nhập lâu gấp 6 lần đặc tả, và việc mật khẩu đúng vẫn bị từ chối ở `t0 + 31 s` chứng minh cửa sổ khóa bị kéo dài sai.

## Bằng chứng

- Log/run: [`evidence/ev-BVA-02.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR02/evidence/ev-BVA-02.log), [`evidence/ev-BVA-05-06.log`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR02/evidence/ev-BVA-05-06.log); tổng hợp EV tại [`evidence/FR02-evidence.md`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR02/evidence/FR02-evidence.md) (EV-FR02-011/014/015, run `run-20261020-fr02`).
- Screenshot: ảnh dưới đây cho thấy `locked_until` còn ~180 giây và lần retry tại `t0 + 31 s` (mật khẩu đúng) vẫn bị 403 khóa.

  ![BUG-FR02-02 — locked_until còn 180 giây, retry ở t0+31s vẫn 403](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR02/screenshots/BUG-FR02-02.png)

- Lặp lại: **2/2** sự kiện khóa độc lập trên 2 fixture — `fr02.wrong@eshop.com` (đo tại `BVA-02`) và `fr02.thr@eshop.com` (đo tại `BVA-05`/`BVA-06`) — cả hai đều cho `locked_until − now ≈ 180 s`. Hai quan sát này nằm trong cùng run `run-20261020-fr02` nên không tính là hai run độc lập.

## Điều tra nguyên nhân (chỉ khi đã kiểm chứng)

**Vị trí:** [`backend/server.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/f3162660d5c4f9005cbb15910290adb4b58ef2c7/backend/server.js#L57) dòng `57`.

```js
} else {
  const newAttempts = user.login_attempts + 2;
  let lockedUntil = null;
  if (newAttempts >= 3) {
    lockedUntil = new Date(Date.now() + 180000).toISOString();
  }
```

**Cơ chế:** Khi bộ đếm chạm ngưỡng, server ghi `locked_until = Date.now() + 180000` (180 000 ms = 180 giây), trong khi R3 yêu cầu 30 giây. Vì `locked_until` được lưu đúng định dạng ISO UTC mà điều kiện `new Date() < new Date(user.locked_until)` (dòng 40) đọc lại chính xác, cửa sổ từ chối kéo dài đủ 180 giây; do đó retry bằng mật khẩu đúng tại `t0 + 31 s` vẫn rơi vào nhánh 403.

Đây là nhận định từ mã nguồn; Expected và Actual ở trên dựa trên đặc tả và lần chạy thực tế. Trích đúng phiên bản commit đã kiểm thử. (Lưu ý: dòng `const newAttempts = user.login_attempts + 2;` là nguyên nhân của `BUG-FR02-01`, không phải của bug này.)
