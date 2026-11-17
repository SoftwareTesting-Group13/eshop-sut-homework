# HW04 — Automation Testing: Kế hoạch chi tiết & Checklist

> Nguồn: [`2026.HW04.Automation Testing_En.md`](./2026.HW04.Automation%20Testing_En.md) (chuyển từ PDF đề bài).
> Bài **cá nhân**, 10 giờ, nộp Moodle. Tổng **100 điểm**.
> MSSV của bạn: **23120223** (đổi nếu nộp bằng MSSV khác).

---

## 0. TL;DR — điều kiện đạt & điểm

| Hạng mục | Yêu cầu tối thiểu | Bằng chứng | Điểm |
| --- | --- | --- | ---: |
| Task 1 – Feature A (FR-02) | ≥12 TC, data-driven, 3 browser, HTML report | script + data + 3 report | 25 |
| Task 1 – Feature B (FR-10) | như trên | như trên | 25 |
| Task 1 – Feature C (FR-17) | như trên | như trên | 25 |
| Task 2 – Demo video | YouTube unlisted ≥5′, tiếng Việt, có 1 fix | link | 15 |
| Agent Skill | skill tái sử dụng + video demo end-to-end | `skills/` + link | 10 |
| AI Audit Report | tool / thời gian / prompt / output từng lần | `reports/ai-audit.md(.pdf)` | bắt buộc |
| AI Critique | 200–300 từ | `reports/ai-critique.md(.pdf)` | bắt buộc |
| Git | ≥8 commit **chỉ đụng file test script** | `git-commit-log.txt` | bắt buộc |
| Bug report | mỗi bug thật → 1 GitHub Issue + screenshot | Issues + `bugs/` | điểm cộng |
| README.md | bảng tự đánh giá + test summary + link video | `README.md` | bắt buộc |

**Rủi ro 0 điểm:** thiếu bất kỳ tài liệu bắt buộc; nộp trễ; copy bài (kể cả prompt).
**Bằng chứng giả → 0:** HTML report phải có `"Run by: 23120223"` + **ISO timestamp**; video phải có giọng nói của bạn và face-cam **hoặc** `whoami` + `hostname`.

---

## 1. Bối cảnh SUT — đọc để làm nhanh hơn

### 1.1. Chạy SUT local

| Thành phần | Thư mục | Cổng | Ghi chú |
| --- | --- | --- | --- |
| Backend | `backend/` (`node server.js`) | **3000** | API prefix `/api` |
| Frontend web (khách) | `frontend-web/` (`npm run dev`) | **5173** | Vite, không khai báo port → port mặc định |
| Frontend admin | `frontend-admin/` (`npm run dev`) | **5174** | `strictPort: true` → không đổi được port |

> ⚠️ `run_servers.sh` ở thư mục gốc đang hardcode `/Users/hanhtran/Downloads/EShop/...` → **phải sửa thành path máy bạn** trước khi chạy, nếu không script sẽ `cd` fail.
> Backend có `database.sqlite` (đã bị modify trong git) → **copy 1 bản `.sqlite` riêng cho HW04** (`cp backend/database.sqlite backend/database.hw04.sqlite`) để không phá dữ liệu và để chạy lại được nhiều lần.

### 1.2. Tài khoản & fixture có sẵn

| Vai trò | Tài khoản | Mật khẩu | Nguồn |
| --- | --- | --- | --- |
| Admin | `admin@eshop.com` | `Admin123!` | HW02 FR-10 |
| User | `test@eshop.com` | `Test1234!` | HW02 FR-10 |
| Fixture user | `fr02.base@eshop.com` | `Passw0rd!` | HW02 FR-02 (DB test cách ly) |

Khuyến nghị: **fixture do test tự tạo** qua `POST /api/register` trong `beforeEach`/`beforeAll` (email có hậu tố random) để 3 lần chạy browser không đụng nhau.

### 1.3. Bản đồ UI (dùng để viết locator)

**Web khách — `http://localhost:5173`**

| Route | Nội dung | Ghi chú cho test |
| --- | --- | --- |
| `/` | Trang chủ / danh sách sản phẩm | |
| `/login` | Đăng nhập | label **"Username"** (không phải Email!), **"Mật khẩu"**, nút **"Sign In"** |
| `/register` | Đăng ký | |
| `/forgot-password` | Quên mật khật → OTP | 2 bước (FR-03) |
| `/profile` | Hồ sơ cá nhân | |
| `/product/:id` | Chi tiết sản phẩm | |
| `/cart`, `/checkout` | Giỏ hàng / thanh toán | dùng để tạo đơn cho FR-10 |

**Admin — `http://localhost:5174`** (1 trang, đổi tab)

| Tab | Nội dung | Phần tử quan trọng |
| --- | --- | --- |
| Dashboard | Tổng quan | |
| Danh mục / Sản phẩm | CRUD | |
| **Mã giảm giá** | FR-17 | Form: `Mã coupon (VD: SAVE10)`, select `type` (percent/fixed), `Giá trị % (VD: 10)` (number), `Đơn tối thiểu (₫)` (number), `Ngày hết hạn` (date), `Số lần dùng tối đa/người` (number); bảng có nút Sửa/Xoá |
| **Đơn hàng** | FR-10 | Nút chuyển trạng thái theo trạng thái hiện tại: pending→**Xác nhận**/**Hủy**, confirmed→**Giao hàng**/**Hủy**, shipping→**Hoàn thành**, canceled→**Đánh dấu Đã giao** |
| Người dùng | FR-19 | |

**Không có `data-testid` nào trong toàn bộ SUT** → đừng đợi AI sinh `data-testid` (sẽ fail). Dùng:
`getByRole('button', { name: 'Sign In' })`, `getByLabel('Mật khẩu')`, `getByPlaceholder('Mã coupon (VD: SAVE10)')`, `getByRole('row', { name: /#123/ })`.
Chấp nhận `getByPlaceholder` cho admin form vì label không gắn `for`.

### 1.4. Điểm yếu UI đã phát hiện sẵn (nguyên liệu cho gap analysis & bug report)

| # | Vấn đề | Nơi | Hậu quả test |
| --- | --- | --- | --- |
| 1 | `<h2>` trang login ghi **"Đăng Ký"** (sai, phải "Đăng Nhập") | `frontend-web/src/pages/Login.jsx` | assertion tiêu đề đúng sẽ fail → bug |
| 2 | Ô mật khẩu dùng `type="text"` (hiện rõ mật khẩu) | `Login.jsx` | bug UI/usability |
| 3 | Thông báo lỗi **chung** cho mọi lỗi: *"Đăng nhập thất bại. Vui lòng kiểm tra lại."* | `Login.jsx` | không phân biệt sai mật khẩu / email chưa đăng ký → assertion yếu |
| 4 | Không có `data-testid`; admin dùng `dangerouslySetInnerHTML` cho địa chỉ | `frontend-admin/src/App.jsx` | selector dễ vỡ → phải review lại script AI |
| 5 | UI admin **không có** nút cho chuyển trạng thái không hợp lệ (pending→shipping…) | `App.jsx` | các ca "invalid transition" của HW02 **không tự động hóa được bằng UI** → phải nêu lý do |

> Các mục 1–2 là ứng viên **bug report** (kèm screenshot). Mục 3–5 thuộc phần **gap analysis** (AI thường viết assert sai chỗ này).

---

## 2. 3 feature phải làm — và map từ test case HW02

Đề yêu cầu: **đúng 3 web feature đã chọn ở HW02, mỗi pool 1 feature**. Của bạn (HW02, nhóm 13):

| Pool | FR | Feature | Số T-ID HW02 | Dùng lại được cho HW04 |
| --- | --- | --- | ---: | --- |
| A | **FR-02** | Login and account lockout | 18 | UI: login sai/đúng, HTML5 email validation, reset bộ đếm. API-only: kiểm tra `login_attempts`, `locked_until` |
| B | **FR-10** | Order state machine | 23 | UI (admin tab Đơn hàng): 4 nút chuyển trạng thái hợp lệ. API-only: các transition không hợp lệ, quyền actor |
| C | **FR-17** | Coupon management (CRUD) | 32 | UI (admin tab Mã giảm giá): tạo/duyệt/xoá, validate form. API-only: uniqueness case-khác-case, thiếu key |

**Nguyên tắc mapping:** ca nào **thao tác được bằng UI** → tự động hóa bằng UI (Playwright). Ca nào chỉ kiểm tra **API/DB** → **không** tự động hóa UI được → ghi vào mục *"test case không tự động hóa được + lý do"* (đề yêu cầu rõ), hoặc tự động hóa bằng **API assertion trong cùng spec** (hybrid: UI để setup, API để verify) — cách này được tính vào bản "complete".

---

## 3. Task 1 — Script do AI sinh (75đ)

### 3.1. Quy trình AI-First (6 bước, mỗi bước 1 prompt)

Đề yêu cầu rõ: **không** dùng 1 prompt chung kiểu *"write all the automation scripts"*. Prompt mẫu (thay nội dung theo feature):

**Bước 1 — Đưa ngữ cảnh + test plan (AI chỉ *thiết kế*, chưa viết code)**
```
Bạn là tester tự động hóa cho SUT EShop (React + Vite, web: http://localhost:5173, admin: http://localhost:5174, API: http://localhost:3000/api).
Feature: FR-02 Login and account lockout.
Bảng test case HW02 (đã xác nhận): <dán bảng DT-*/BVA-* từ homework/hw02/ncuong/features/FR02/test-cases.md>
Yêu cầu: hãy lập TEST PLAN tự động hóa gồm >=12 ca (positive/negative/edge), với bảng: T-ID | loại | dữ liệu input | bước thao tác UI | oracle cụ thể | có chạy được bằng UI không.
Không viết code ở bước này.
```
**Bước 2 — Khung project (skeleton)**
```
Sinh cấu trúc Playwright TS cho feature trên: playwright.config.ts với projects chromium/firefox/webkit,
thư mục data/ (file .csv), tests/*.spec.ts, helper đọc CSV. Chỉ sinh skeleton + 1 ca mẫu đọc từ CSV.
```
**Bước 3 — Viết spec từng ca (1–2 ca / prompt)**
```
Viết 2 test case tiếp theo (T-ID ... ) theo test plan đã chốt. Dữ liệu đọc từ data/fr02-login.csv (cho tôi cấu trúc CSV đúng nếu chưa có).
Dùng getByRole/getByLabel, không dùng XPath hay :nth-child. Không hardcode test data trong code.
```
**Bước 4 — Sinh data file** → `data/fr02-login.csv` với cột `id,type,email,password,expected,message`.
**Bước 5 — Chạy thật & debug** → tự chạy, tự sửa, ghi lại lỗi AI.
**Bước 6 — Nhờ AI review lại, rồi tự kiểm tra lần cuối** → đây là chỗ "human review" của đề.

**Prompt cho gap analysis (bước nghiệm thu):**
```
Đây là script Playwright đã chạy thật + log lỗi của tôi. Hãy liệt kê: (1) lỗi AI tạo ra,
(2) lỗi thiếu assertion, (3) test case edge bị bỏ sót, (4) nguyên nhân gốc (prompt nào thiếu thông tin?).
```

### 3.2. ≥12 test case / feature — danh sách đề xuất cụ thể

**FR-02 (Pool A) — `data/fr02-login.csv`**

| T-ID | Loại | Input | Oracle (assert) |
| --- | --- | --- | --- |
| TC-01 | P | email đúng + MK đúng | URL về `/`, token lưu, không hiện lỗi |
| TC-02 | P | email đúng + MK đúng (chữ hoa email) | đăng nhập thành công (hoặc fail → ghi bug) |
| TC-03 | N | MK sai | hiện đúng message *"Đăng nhập thất bại. Vui lòng kiểm tra lại."*, vẫn ở `/login`, **không** có token |
| TC-04 | N | email chưa đăng ký | hiện message lỗi, không chuyển trang |
| TC-05 | N | email sai định dạng (`not-an-email`) | HTML5 `type=email` chặn → **không** gửi request / không chuyển trang |
| TC-06 | N | email rỗng | form `required` chặn submit |
| TC-07 | N | mật khẩu rỗng | form `required` chặn submit |
| TC-08 | E | sai MK lần 1 | vẫn đăng nhập được (chưa khoá) |
| TC-09 | E | sai MK lần 2 | vẫn đăng nhập được (chưa khoá) |
| TC-10 | E | sai MK lần 3 | tài khoản bị **khoá** → message lỗi, login lại bằng MK đúng vẫn bị từ chối |
| TC-11 | E | sau khi khoá, thử MK đúng | bị từ chối (trạng thái khoá) |
| TC-12 | P | sau khi login sai rồi login đúng | thành công và bộ đếm được reset (verify bằng API `GET /api/users/me` + login lại) |
| TC-13 | P | link "Quên mật khẩu?" | điều hướng `/forgot-password` |

> Lưu ý thời gian: khoá 30 giây → TC-10/11 dùng **API setup** (`PUT`/SQL trên DB test) thay vì click 3 lần, hoặc `test.setTimeout(60_000)`; **đừng** `waitForTimeout` cứng.

**FR-10 (Pool B) — `data/fr10-order.json`**

| T-ID | Loại | Input | Oracle |
| --- | --- | --- | --- |
| TC-01 | P | order `pending` → bấm **Xác nhận** | badge trạng thái đổi sang *Đã xác nhận* |
| TC-02 | P | `confirmed` → **Giao hàng** | → *Đang giao* |
| TC-03 | P | `shipping` → **Hoàn thành** | → *Đã giao* |
| TC-04 | P | `pending` → **Hủy** | → *Đã huỷ* |
| TC-05 | P | `confirmed` → **Hủy** | → *Đã huỷ* |
| TC-06 | N | `shipping` → không có nút Hủy | assert **không tồn tại** nút "Hủy" (chặn transition không hợp lệ) |
| TC-07 | N | `delivered` → không có nút chuyển trạng thái | assert không có nút hành động |
| TC-08 | N | `canceled` → nút "Đánh dấu Đã giao" (transition **không hợp lệ** theo sơ đồ) | assert trạng thái → *Đã giao* ⇒ **phát hiện bug** (HW02 đã xác nhận DT-14 là lỗi) |
| TC-09 | E | đơn chưa có địa chỉ ("Chưa cập nhật") | hiển thị đúng placeholder |
| TC-10 | E | tổng tiền 0 / null | format `0 ₫`, không crash |
| TC-11 | N | admin chưa đăng nhập → mở `/admin` | bị chặn/redirect login (FR-12 access control) |
| TC-12 | P | lọc/tìm trong bảng đơn (nếu UI có) | đúng số dòng |
| TC-13 | E | đơn của user khác bị admin sửa trạng thái | phản hồi lỗi, trạng thái không đổi (verify bằng API) |

**FR-17 (Pool C) — `data/fr17-coupon.csv`**

| T-ID | Loại | Input | Oracle |
| --- | --- | --- | --- |
| TC-01 | P | code hợp lệ, percent 10 | tạo thành công, xuất hiện trong bảng |
| TC-02 | P | code hợp lệ, fixed 50000 | 2xx/UI list có row `type=fixed` |
| TC-03 | N | `code` rỗng | không tạo được, hiện lỗi |
| TC-04 | N | `code` = 3 khoảng trắng | không tạo được (ASSUMED) |
| TC-05 | N | trùng code seed `SAVE10` | không tạo row mới |
| TC-06 | N | `save10` (khác hoa/thường so với `SAVE10`) | không tạo row mới (HW02 xác nhận uniqueness không phân biệt hoa/thường) |
| TC-07 | N | `type` = `percentage` (sai chính tả) | bị từ chối |
| TC-08 | N | `discount_value` = 0 | bị từ chối (biên dưới) |
| TC-09 | N | `discount_value` = -1 | bị từ chối |
| TC-10 | N | `discount_value` = "abc" | bị từ chối (UI: input type=number chặn sẵn) |
| TC-11 | P | `discount_value` = 1 | tạo được (biên trên) |
| TC-12 | N | `min_order_amount` = -1 | bị từ chối |
| TC-13 | P | `min_order_amount` = 0 | tạo được |
| TC-14 | N | `expired_at` = `not-a-date` | bị từ chối |
| TC-15 | P | `expired_at` quá khứ (2020-01-01) | tạo được (theo ASSUMED của HW02) |
| TC-16 | N | `max_uses_per_user` = 0 | bị từ chối |
| TC-17 | N | `max_uses_per_user` = -1 | bị từ chối |
| TC-18 | P | Edit coupon (nút Sửa) | giá trị cập nhật trong bảng |
| TC-19 | P | Delete coupon | row biến mất khỏi bảng |
| TC-20 | E | 2 lần tạo cùng code trong 1 run | lần 2 bị từ chối, chỉ 1 row |

> **Cạm bẫy quan trọng:** UI admin **không hiển thị message lỗi rõ ràng** khi validate fail → oracle phải là "**row không được thêm vào bảng**" + verify bằng `GET /api/coupons` (hybrid UI+API). Nếu UI có toast/alert thì assert thêm cả nó.

### 3.3. Data-driven: schema & cách nạp

`data/fr02-login.csv`
```csv
id,type,email,password,expected_result,expected_message
TC-01,positive,fr02.p1@eshop.com,Passw0rd!,success,
TC-03,negative,fr02.p1@eshop.com,WrongPass1!,error,Đăng nhập thất bại. Vui lòng kiểm tra lại.
TC-05,edge,not-an-email,Passw0rd!,blocked,
```
`data/fr10-order.json`
```json
[
  { "id": "TC-01", "type": "positive", "orderStatus": "pending", "action": "Xác nhận", "expectedStatus": "Đã xác nhận" }
]
```
`data/fr17-coupon.csv`
```csv
id,type,code,discountType,discountValue,minOrderAmount,expiredAt,maxUsesPerUser,expected,errorField
TC-01,positive,FR17-TC-01,percent,10,100000,2099-12-31,1,created,
TC-03,negative,,percent,10,100000,2099-12-31,1,rejected,code
```

**Cách nạp (đừng hardcode):**
```ts
import { readFileSync } from 'node:fs';
import { parse } from 'csv-parse/sync';   // hoặc đọc csv-parse
const rows = parse(readFileSync(new URL('../data/fr02-login.csv', import.meta.url)));
for (const row of rows) test(row.id, async ({ page }) => { /* ... */ });
```
Bảo đảm: **không** có mảng/object dữ liệu trong file `.spec.*` (đề nói rõ sẽ không được chấp nhận).

**Sinh dữ liệu duy nhất theo lần chạy** (tránh 3 browser đụng dữ liệu):
```ts
const code = `${row.code}-${process.env.TEST_RUN_ID ?? Date.now()}-${browserName}`;
```

### 3.4. Catalog assertion (cần **≥3 kiểu khác nhau** mỗi feature)

| Kiểu | Ví dụ | Dùng cho |
| --- | --- | --- |
| A. Điều hướng/URL | `await expect(page).toHaveURL(/\/login$/)` | sau login/fail |
| B. Hiển thị/nội dung | `await expect(page.getByText('Đăng nhập thất bại...')).toBeVisible()` | message lỗi, badge trạng thái |
| C. Giá trị input | `await expect(page.getByLabel('Mật khẩu')).toHaveValue('')` | sau submit lỗi |
| D. Bảng/list | `await expect(page.getByRole('row', { name: /#42/ })).toContainText('Đang giao')` | đơn hàng, coupon |
| E. API response | `const res = await page.waitForResponse(r => r.url().includes('/api/login')); expect(res.status()).toBe(200)` | verify token, row count |
| F. Count/collection | `expect(await page.getByRole('row').count()).toBeGreaterThan(0)` | danh sách |
| G. Không tồn tại | `await expect(page.getByRole('button', { name: 'Hủy' })).toHaveCount(0)` | chặn transition sai |

Gợi ý phân bổ: FR-02 dùng A+B+C+E; FR-10 dùng B+D+G+E; FR-17 dùng D+E+F+C.

### 3.5. `playwright.config.ts` — 3 browser + report có "Run by:" + ISO timestamp

```ts
import { defineConfig, devices } from '@playwright/test';

const STUDENT_ID = process.env.STUDENT_ID ?? '23120223';
const ISO = new Date().toISOString();

export default defineConfig({
  testDir: './tests',
  fullyParallel: false,           // tránh đụng dữ liệu khi 3 browser chạy song song
  retries: 0,
  reporter: [
    ['list'],
    ['html', {
      outputFolder: `reports/html/${process.env.FEATURE ?? 'suite'}-${process.env.BROWSER ?? 'chromium'}`,
      title: `Run by: ${STUDENT_ID}`,
      open: 'never',
      metadata: {
        'Run by': STUDENT_ID,
        'ISO timestamp': ISO,
        'Feature': process.env.FEATURE ?? '',
        'Browser': process.env.BROWSER ?? 'chromium',
      },
    }],
  ],
  use: {
    baseURL: process.env.WEB_URL ?? 'http://localhost:5173',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox',  use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit',   use: { ...devices['Desktop Safari'] } },
  ],
});
```
Lệnh chạy 9 lần (3 feature × 3 browser), **mỗi lần 1 report riêng**:
```bash
for f in fr02 fr10 fr17; do for b in chromium firefox webkit; do \
  FEATURE=$f BROWSER=$b npx playwright test --project=$b --grep "@$f"; done; done
```
> HTML report của Playwright có `metadata` → hiển thị ở tab **Metadata**; `title` hiển thị ở header. Nếu TAs tìm "Run by:" ở header → đã đạt; nếu muốn chắc hơn, thêm `outputFolder` + 1 file `report-meta.txt` cạnh report ghi `Run by: 23120223 — ISO: 2026-...`.

### 3.6. Setup/teardown & chống trùng dữ liệu

- `beforeAll`: tạo fixture bằng **API** (`request.post('/api/register')`) → nhanh và ổn định hơn UI.
- `beforeEach`: mỗi ca có `id` riêng trong CSV → tài khoản/coupon/đơn riêng.
- `afterAll`: xoá dữ liệu tạm (`DELETE /api/admin/coupons/:id`) để repo không bị bẩn.
- **Không** `waitForTimeout` cứng; dùng `expect(...).toBeVisible()` (auto-wait) — đây là 1 lý do hay để nói "AI viết wait sai gây flaky".

### 3.7. Gap analysis — mẫu ghi trong main report (bắt buộc)

Mỗi feature 1 mục, dạng bảng:

| # | AI làm sai / bỏ sót | Mức độ | Nguyên nhân gốc | Cách tôi sửa |
| --- | --- | --- | --- | --- |
| 1 | Dùng `page.locator('div.flex > button:nth-child(2)')` cho nút Hủy | Cao (vỡ khi DOM đổi) | Prompt không cấm selector theo vị trí, không cho biết SUT không có `data-testid` | Đổi sang `getByRole('button', { name: 'Hủy' })` |
| 2 | Chỉ assert "đăng nhập thất bại" mà không kiểm tra URL còn ở `/login` | Trung bình | AI mặc định "thấy text lỗi = đúng" | Thêm `expect(page).toHaveURL(/\/login/)` |
| 3 | Không có ca biên (0 / -1 / 1) | Cao | Prompt chỉ yêu cầu "happy path" | Đưa bảng BVA của HW02 vào prompt |
| 4 | `await page.waitForTimeout(3000)` | Trung bình | AI không biết app là SPA/Vite | Bỏ, dùng auto-wait |
| 5 | Thiếu case "code trùng khác hoa/thường" | Trung bình | AI không đọc được seed `SAVE10` | Bổ sung từ HW02 DT-07 |

Kết luận nên có: *"AI-first không phải để giảm effort, mà để có nguyên liệu để review — giá trị nằm ở chỗ bạn biết chính xác nó sai ở đâu và vì sao."*

### 3.8. Bug report — mẫu

```markdown
# BUG-FR17-01 — Coupon trùng mã khác hoa/thường vẫn được tạo
- **Feature:** FR-17 · **Pool:** C
- **Test case:** FR17-TC-06 (data/fr17-coupon.csv, dòng id=TC-06)
- **Severity:** Medium · **Browser:** Chromium, Firefox, WebKit (cả 3 đều lỗi)
- **Precondition:** đã có coupon `SAVE10` (seed)
- **Steps:** Admin → tab "Mã giảm giá" → Mã coupon = `save10`, type=percent, value=10, min=100000, hạn=2099-12-31, max=1 → nút tạo
- **Expected:** không tạo được row mới (uniqueness không phân biệt hoa/thường — nếu quy tắc là không phân biệt)
- **Actual:** tạo thành công, bảng có 2 row `SAVE10`/`save10`
- **Evidence:** screenshot, log Playwright, `GET /api/coupons`
- **GitHub Issue:** <link>
```

Mỗi bug → **1 GitHub Issue** kèm **screenshot** (dán ảnh vào issue). Ưu tiên các lỗi đã xác nhận ở HW02 (4 + 3 + 8 bug) — dễ tái hiện, dễ có evidence.

### 3.9. Test case **không** tự động hóa được — cách ghi

| T-ID HW02 | Vì sao không tự động hóa bằng UI | Hướng xử lý |
| --- | --- | --- |
| FR10 DT-08…DT-15 (transition không hợp lệ) | UI admin không render nút cho transition sai | chuyển sang **API assertion** trong cùng spec (vẫn tự động hóa) |
| FR10 DT-21…DT-23 (quyền actor A2–A4) | web user không có control admin để thao tác | API-only: nêu rõ "không có đường UI" |
| FR02 DT-10/DT-11 (thiếu key / null password) | không thể nhập `password: null` qua form | API-only, hoặc đưa vào mục không tự động hóa |
| FR17 DT-07 (case-insensitive uniqueness) | UI có thể tạo được → đây là **bug**, đã tự động hóa thành công | giữ nguyên, log bug |

---

## 4. Task 2 — Demo video (15đ)

**Dạng video:** YouTube **Unlisted** (không Public, không Private — unlisted mới gửi link cho TA xem được).

**Kịch bản 5–6 phút (timeline gợi ý)**

| Thời gian | Nội dung | Lưu ý |
| --- | --- | --- |
| 0:00–0:30 | Giới thiệu: tên, MSSV, feature nào được demo, stack (Playwright + 3 browser) | có face-cam từ đầu |
| 0:30–1:00 | Mở terminal: `whoami` + `hostname` | bằng chứng tác giả |
| 1:00–1:30 | Show cấu trúc repo: `tests/`, `data/*.csv`, `playwright.config.ts` | giải thích data-driven |
| 1:30–2:00 | Show `data/fr02-login.csv` (mở bằng editor) → giải thích cột, `type` positive/negative/edge | |
| 2:00–4:00 | **Chạy thật**: `npx playwright test --project=chromium` → log xanh/đỏ | chạy 1 feature đầy đủ |
| 4:00–4:30 | Mở HTML report → chỉ ra tiêu đề **"Run by: 23120223"**, timestamp ISO, danh sách test case | điểm TAs kiểm tra |
| 4:30–5:00 | Chạy tiếp `--project=firefox` → `--project=webkit`, mở 2 report còn lại | chứng minh multi-browser |
| 5:00–5:30 | **Kể 1 fix**: mở diff script AI cũ vs bản đã sửa (vd: selector `nth-child` → `getByRole`) + giải thích vì sao AI sai | **bắt buộc** |
| 5:30–6:00 | Kết: tổng kết ca đã chạy/pass/fail, số bug, link repo & video | |

**Checklist video:** unlisted · ≥5 phút · lời kể **tiếng Việt** (giọng thật, không AI) · có **face-cam hoặc** `whoami`+`hostname` · có **≥1 fix** được kể · có HTML report trong video · link dán vào README + main report + .zip.

---

## 5. Agent Skill (10đ)

- Skill mô tả workflow: *đọc test case → sinh skeleton Playwright → sinh data file → viết spec → chạy 3 browser → đóng gói report + gap analysis*.
- Cấu trúc gợi ý:
  ```
  homework/hw04/ncuong/skills/automation-test-writer/
  ├── SKILL.md          # mô tả workflow, input/output, quy tắc (data-driven, 3 browser, "Run by:")
  ├── templates/spec.ts.template
  ├── templates/data.csv.template
  └── scripts/new-feature.sh    # sinh skeleton cho feature mới
  ```
- `SKILL.md` nên mô tả rõ: input = feature + test case catalog; output = `tests/<fr>.spec.ts` + `data/<fr>.csv` + 3 HTML report; các quy tắc bắt buộc (không hardcode data, ≥3 assertion, không `waitForTimeout`, locator theo role/label).
- **Phải có video demo** (YouTube link) dùng skill end-to-end trên **một feature hoàn chỉnh** — video này **khác** video Task 2 (Task 2 = chạy script; video skill = dùng skill để tạo ra script).
- Có thể **refactor từ** `homework/hw03/ncuong/skills/cross-browser-testing` và `ai-audit-logger` đã có sẵn → tiết kiệm thời gian, nhưng phải viết lại cho ngữ cảnh HW04.

---

## 6. AI Audit Report (phụ lục bắt buộc)

Cấu trúc bảng cho **từng** lần tương tác AI:

| # | Công cụ AI | Ngày giờ | Prompt (rút gọn) | Output AI (rút gọn) | Hành động của tôi |
| ---: | --- | --- | --- | --- | --- |
| 1 | ChatGPT / Claude / opencode… | 2026-… 10:12 | "Lập test plan tự động hóa cho FR-02…" | (dán output) | chọn 13 ca, bỏ 2 ca thiếu oracle |

- Mở đầu bằng khai báo: *"I use AI tools for the following tasks,"* (hoặc nếu không dùng: *"I do not use any AI help in this exercise."*).
- **Mẹo:** dùng lại skill `homework/hw03/ncuong/skills/ai-audit-logger` (hoặc viết script `scripts/log-ai-session.sh`) để tự động trích **4 trường** sau mỗi phiên → giảm rủi ro quên ghi log (quên = 0 điểm).
- Nên ghi **cả** các lần dùng AI để hỏi lỗi test, viết lời kể video, viết critique → càng đầy đủ càng tốt.

---

## 7. AI Critique (200–300 từ)

Dàn ý (bám vào gap thật của bạn):

1. **AI sai ở đâu**: selector theo vị trí; assert dừng ở "có thông báo lỗi"; bỏ sót ca biên; viết `waitForTimeout`; không phân biệt lỗi "sai mật khẩu" với "chưa đăng ký" vì SUT trả message chung.
2. **Vì sao AI không bắt được**: AI chỉ thấy prompt của tôi — nếu tôi không đưa bảng BVA/domain analysis của HW02, nó không có biên để test; AI không biết DOM thật của SUT nên đoán selector; AI không chạy code nên không biết cái gì thật sự fail.
3. **Bài học**: AI-first ≠ hỏi 1 lần rồi copy; giá trị nằm ở *vòng lặp* prompt → chạy → đọc log → sửa → lại nhờ AI review; người học nắm kỹ thuật mới biết **hỏi** gì; và trách nhiệm cuối cùng vẫn là của người.

> Nhớ **đếm từ** (200–300). Và nhớ rà lại bằng mắt — đề nói rõ "submit raw AI output không được chấp nhận".

---

## 8. Git & commit log

- Repo **GitHub công khai** (scripts + data + HTML report).
- **≥8 commit**, và **chỉ commit nào đụng file test script** (`.spec.ts` / `.spec.js`) mới tính. Commit README/PDF **không tính**.
- Kế hoạch 10–12 commit (đề xuất):

| # | Commit message | File test được đụng |
| ---: | --- | --- |
| 1 | `test(fr02): add Playwright skeleton + login data-driven suite` | ✅ `tests/fr02-login.spec.ts` |
| 2 | `test(fr02): add lockout boundary cases from HW02 BVA` | ✅ |
| 3 | `test(fr02): fix AI-generated selector -> role-based locator` | ✅ (chứng minh human review) |
| 4 | `test(fr10): add order state machine spec (admin UI)` | ✅ `tests/fr10-order.spec.ts` |
| 5 | `test(fr10): cover invalid transitions via API assertion` | ✅ |
| 6 | `test(fr10): fix brittle row lookup + add count assertion` | ✅ |
| 7 | `test(fr17): add coupon CRUD spec + data file` | ✅ `tests/fr17-coupon.spec.ts` |
| 8 | `test(fr17): add edge cases (0/-1/1) and delete flow` | ✅ |
| 9 | `test(fr17): replace hardcoded data with CSV loader` | ✅ |
| 10 | `test(fr02): stabilize flaky wait (auto-wait instead of timeout)` | ✅ |

- Xuất log: `git log --oneline --stat > git-commit-log.txt` (định dạng text, đính kèm .zip).
- Nhớ: **không** commit nhầm file report/PDF vào commit đếm — tách commit riêng cho tài liệu (được, nhưng không tính).

---

## 9. README.md (bắt buộc trong .zip) — mẫu

```markdown
# HW04 — AI Automation Testing
**Sinh viên:** Dương Nhật Cường · **MSSV:** 23120223

- Repo: <link GitHub>
- Demo video: <link YouTube unlisted>
- AI Audit Report: [reports/ai-audit.md](reports/ai-audit.md)
- AI Critique: [reports/ai-critique.md](reports/ai-critique.md)
- Main report: [reports/main-report.md](reports/main-report.md)

## Test summary
| Feature | Pool | TC automated | TC executed | PASS | FAIL | Browser runs | Bugs |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| FR-02 | A | 13 | 13 | 12 | 1 | 3 | 2 |
| FR-10 | B | 13 | 13 | 11 | 2 | 3 | 1 |
| FR-17 | C | 20 | 20 | 17 | 3 | 3 | 3 |
| **Tổng** | | **46** | **46** | **40** | **6** | **9** | **6** |

## Bảng tự đánh giá
| No. | Criteria | Điểm tối đa | Điểm tự đánh giá |
| ---: | --- | ---: | ---: |
| 1 | Task 1 - Feature A (FR-02) | 25 | |
| 1 | Task 1 - Feature B (FR-10) | 25 | |
| 1 | Task 1 - Feature C (FR-17) | 25 | |
| 2 | Task 2 — Demo video | 15 | |
| 3 | Agent Skills | 10 | |
| **Tổng** | | **100** | |
```

> Số liệu trên là **ví dụ** — phải thay bằng số thật sau khi chạy.

---

## 10. Main report — dàn ý (giữ nguyên bằng Markdown)

1. Thông tin chung (bảng đề) + feature đã chọn & lý do (trùng HW02).
2. Môi trường & cách chạy (URL, account, Playwright version, browser).
3. Quy trình AI-first đã dùng (prompt ladder + AI Audit trích dẫn).
4. **Automation report** từng feature: test plan, data file, assertion dùng, kết quả chạy (ảnh chụp report).
5. **Review / gap analysis** (mục 3.7) — phần bị chấm nặng nhất của Task 1.
6. Bug report tổng hợp + link GitHub Issues.
7. Test case không tự động hóa được + lý do.
8. Agent Skill (mô tả + video link).
9. **AI Critique** (200–300 từ) — hoặc để riêng file, đề yêu cầu nộp cả 2 bản.
10. Bảng tự đánh giá + test summary.
11. Tài liệu tham khảo.

Xuất **PDF** từ Markdown sau khi duyệt (pandoc / VS Code Markdown PDF) — đề yêu cầu **cả Markdown + PDF**.

---

## 11. Đóng gói & nộp — lệnh cụ thể

```bash
cd homework/hw04
zip -r 23120223_HW04_AI_Automation_090.zip ncuong \
  -x "*.DS_Store" "*/node_modules/*" "*/.git/*"
# đổi 090 → điểm tự đánh giá (3 chữ số, [000,100])
```
Kiểm tra trước khi nén:
- [ ] Main report `.md` **+ `.pdf`**
- [ ] AI Audit `.md` + `.pdf` · AI Critique `.md` + `.pdf`
- [ ] `git-commit-log.txt`
- [ ] `README.md` (bảng tự đánh giá + test summary + link video)
- [ ] **≥9 HTML report** (3 feature × 3 browser) — hoặc link repo chứa chúng
- [ ] Bug report + screenshot (trong `bugs/` + Issues)
- [ ] Link repo GitHub **công khai** + link YouTube unlisted (trong README và main report)
- [ ] `skills/` (Agent Skill) + link video demo skill
- [ ] `data/` `.csv`/`.json` + `tests/` `.spec.ts` (đã trong repo)
- [ ] Tên file đúng định dạng, nộp qua **Moodle**.

---

## 12. Oral defense (30% ngẫu nhiên, 5–7 phút) — chuẩn bị

| Câu hỏi dự kiến | Gợi ý trả lời |
| --- | --- |
| Vì sao chọn 3 feature này? | Trùng HW02, có sẵn test case & bug đã xác nhận → tái dùng được, giảm rủi ro |
| AI sai ở đâu? | Nêu 2–3 lỗi cụ thể từ bảng gap analysis + vì sao (prompt chưa đủ context, không biết DOM thật) |
| Bạn đã sửa gì? | Ví dụ selector `nth-child` → `getByRole`; bỏ `waitForTimeout`; thêm assert URL |
| Data-driven thể hiện thế nào? | Chỉ ra CSV, cột, cách load bằng `csv-parse`, không có data trong spec |
| 3 browser khác nhau thế nào? | Chromium/Firefox/WebKit, 9 lần chạy, HTML report riêng từng lần |
| HTML report chứng minh gì? | `Run by: 23120223` + ISO timestamp → bằng chứng chạy thật |
| Test case nào không tự động hóa được? | Transition sai ở admin, quyền actor → nêu lý do cụ thể |
| Nếu làm lại? | Viết test plan trước rồi mới prompt; tách prompt theo ca; tự động hoá AI audit log |

---

## 13. Timeline gợi ý (10 giờ)

| Giờ | Việc |
| ---: | --- |
| 0:00–0:30 | Đọc đề lại, chạy SUT, xác nhận URL/account, cài Playwright + 3 browser |
| 0:30–2:00 | **FR-02**: test plan (AI) → skeleton → data file → 13 ca → chạy chromium → fix |
| 2:00–3:30 | **FR-10**: plan → spec → data → 13 ca → chạy chromium → fix |
| 3:30–5:00 | **FR-17**: plan → spec → data → 20 ca → chạy chromium → fix |
| 5:00–6:00 | Chạy đủ 9 lần (3 feature × 3 browser), lưu 9 HTML report |
| 6:00–7:00 | Bug report + GitHub Issues + screenshot; viết gap analysis |
| 7:00–7:45 | Agent Skill + chạy thử skill trên 1 feature |
| 7:45–8:30 | Main report + AI Audit + AI Critique; commit ≥8 lần + commit log |
| 8:30–9:30 | Quay video Task 2 + video demo skill |
| 9:30–10:00 | README, đóng gói .zip, kiểm tra checklist, nộp Moodle |

---

## 14. Checklist tổng hợp

**A. Chuẩn bị**
- [ ] SUT chạy được: web 5173, admin 5174, API 3000; `run_servers.sh` đã sửa path
- [ ] Copy DB riêng cho HW04 để chạy lại an toàn
- [ ] `npm i -D @playwright/test` + `npx playwright install chromium firefox webkit`
- [ ] Xác nhận 3 feature: FR-02 (A), FR-10 (B), FR-17 (C)

**B. Task 1**
- [ ] Mỗi feature: ≥12 TC (13/13/20), có positive + negative + edge
- [ ] Data file `.csv`/`.json` riêng, **không** hardcode trong spec
- [ ] ≥3 kiểu assertion mỗi feature
- [ ] Chạy 3 browser × 3 feature = **9 lần**, lưu **9 HTML report**
- [ ] Mỗi report có `Run by: 23120223` + ISO timestamp
- [ ] Gap analysis mỗi feature (AI sai gì + vì sao + đã sửa gì) — có bảng
- [ ] ≥1 lỗi AI đã sửa được **kể trong video**
- [ ] Bug report + GitHub Issue + screenshot cho mỗi bug
- [ ] Danh sách test case không tự động hóa được + lý do

**C. Task 2**
- [ ] Video unlisted ≥5′, lời kể tiếng Việt, face-cam **hoặc** `whoami`+`hostname`
- [ ] Có HTML report trong video + kể 1 fix
- [ ] Link video ở README, main report, .zip

**D. Agent Skill**
- [ ] `SKILL.md` + templates/script, chạy thật trên 1 feature
- [ ] Video demo skill end-to-end (link)

**E. Tài liệu bắt buộc**
- [ ] AI Audit Report (`.md` + `.pdf`) — mọi lần dùng AI
- [ ] AI Critique 200–300 từ (`.md` + `.pdf`)
- [ ] Main report (`.md` + `.pdf`)
- [ ] `git-commit-log.txt`
- [ ] `README.md`: bảng tự đánh giá + test summary + link video + link repo
- [ ] ≥8 commit **chỉ đụng file test script**

**F. Nộp**
- [ ] `23120223_HW04_AI_Automation_0XX.zip` (đúng định dạng)
- [ ] Đủ mọi mục trong §11 trong zip
- [ ] Nộp Moodle trước deadline (trễ = không được nhận)

---

## 15. Bảng rủi ro

| Rủi ro | Hậu quả | Phòng tránh |
| --- | --- | --- |
| Quên AI Audit Report | 0 điểm | Log ngay từ đầu; dùng `ai-audit-logger` |
| Hardcode test data trong spec | Không đạt yêu cầu data-driven | Load từ `data/*.csv` |
| Chỉ chạy 1 browser | Thiếu 6 lần chạy | Script loop 3×3 |
| Report thiếu `Run by:`/timestamp | Bị coi là bằng chứng giả | Set `title` + `metadata` trong reporter |
| Commit không đụng file test | <8 commit hợp lệ | Commit theo từng thay đổi `.spec.ts` |
| Video để public/private, không giọng nói | Mất điểm Task 2 | Unlisted + thu âm giọng Việt + face-cam |
| Chạy 3 browser song song → đụng dữ liệu coupon/đơn | flaky, fail giả | `fullyParallel: false` + dữ liệu unique theo run |
| Test lockout 30s làm suite chậm/timeout | timeout, mất điểm | Setup bằng API, `test.setTimeout` hợp lý, không `waitForTimeout` |
| Thiếu tài liệu trong .zip | 0 điểm | Đối chiếu §11 |
| Copy prompt/script của bạn khác | 0 điểm cả hai | Tự viết prompt & script |
