# AI Audit Report — HW04

I use AI tools for the following tasks,

- Lập TEST PLAN tự động hóa FR-02 (HW04 Task 1, bước 1 — chỉ thiết kế, chưa viết code).
- Lập TEST PLAN tự động hóa FR-10 (HW04 Task 1, bước 1 — chỉ thiết kế, chưa viết code).
- Lập TEST PLAN tự động hóa FR-17 (HW04 Task 1, bước 1 — chỉ thiết kế, chưa viết code).
- Sinh khung project Playwright TS Bước 2 (skeleton + 1 ca mẫu A-FR02-01, data JSON).
- Triển full FR02: data 16 ca + spec 16 ca, chạy 3 browser, fix A-FR02-10.
- Soạn AI Audit Report này.

> **Phạm vi lập báo cáo (capture notes):**
> - Bằng chứng khả dụng: conversation hiện tại (không có transcript export riêng).
> - Số interaction đã ghi: 5
> - Công cụ AI đã dùng (theo bằng chứng): OpenCode agent — Muse Spark 1.3 Contributor
> - Trường còn thiếu: không
> - Công cụ/phiên được nhắc tới nhưng không kiểm tra được: không

---

## Interaction AI-001

- **AI tool:** OpenCode agent — Muse Spark 1.3 Contributor (provider `opencode-go`)
- **Date and time:** 2026-11-17 (UTC) — thời điểm conversation, không có timestamp nguồn chi tiết hơn
- **Source:** Conversation hiện tại; file đính kèm của người dùng: `2026.HW04.Automation Testing_En.md`, `api_specification.md`, `README.md`, `homework/hw02/ncuong/features/FR02/test-cases.md`, `homework/hw04/docs/HW04_TASK_CHECKLIST.md`
- **Task:** Lập TEST PLAN tự động hóa FR-02 gồm >=12 ca (positive/negative/edge) dạng bảng T-ID | loại | input | bước UI | oracle | chạy được bằng UI không; không viết code.

### Your prompt

```text
Bạn là tester tự động hóa cho SUT EShop (React + Vite, web: http://localhost:5173, admin: http://localhost:5174, API: http://localhost:3000/api).
Đang triển khai HW04: Automation Testing, đọc @homework/hw04/docs/2026.HW04.Automation Testing_En.md. Spec: @api_specification.md  + README @README.md 
Tui phải chọn 3 feature từ HW02, ở đây mình sẽ triển FR đầu tiên là FR02.
Feature: FR-02 Login and account lockout.
Bảng test case HW02 (đã xác nhận): @homework/hw02/ncuong/features/FR02/test-cases.md 
Yêu cầu: hãy lập TEST PLAN tự động hóa gồm >=12 ca (positive/negative/edge), với bảng: T-ID | loại | dữ liệu input | bước thao tác UI | oracle cụ thể | có chạy được bằng UI không. Check @homework/hw04/docs/2026.HW04.Automation Testing_En.md và @homework/hw04/docs/HW04_TASK_CHECKLIST.md 
Không viết code ở bước này. Sau khi làm xong nhớ AI Audit Log.
```

### The AI output

Artifact chính nằm ở `homework/hw04/ncuong/features/FR02/test-plan-automation.md`: bảng 16 ca A-FR02-01..A-FR02-16 (14 chạy được bằng UI thuần/hybrid + 2 API-only DT-10/DT-11), có trace về DT-*/BVA-* của HW02, oracle cụ thể theo URL / message generic / localStorage[token] / API verify, và ghi chú 4 bug SUT đã kiểm chứng (Login.jsx:24 h2 sai, :30 email type=text, :40 password type=text, :18 message generic; server.js:54 +2 thay vì +1, :57 khóa 180s thay vì 30s). Không sinh code Playwright theo yêu cầu.

---

## Interaction AI-002

- **AI tool:** OpenCode agent — Muse Spark 1.3 Contributor (provider `opencode-go`)
- **Date and time:** 2026-11-17 (UTC) — thời điểm conversation, không có timestamp nguồn chi tiết hơn
- **Source:** Conversation hiện tại; file đính kèm của người dùng: `2026.HW04.Automation Testing_En.md`, `api_specification.md`, `README.md`, `homework/hw02/ncuong/features/FR10/test-cases.md`, `homework/hw04/docs/HW04_TASK_CHECKLIST.md`
- **Task:** Lập TEST PLAN tự động hóa FR-10 gồm >=12 ca (positive/negative/edge) dạng bảng T-ID | loại | input | bước UI | oracle | chạy được bằng UI không; không viết code.

### Your prompt

```text
Bạn là tester tự động hóa cho SUT EShop (React + Vite, web: http://localhost:5173, admin: http://localhost:5174, API: http://localhost:3000/api).
Đang triển khai HW04: Automation Testing, đọc @homework/hw04/docs/2026.HW04.Automation Testing_En.md . Spec: @api_specification.md  + README @README.md 
Tui phải chọn 3 feature từ HW02, ở đây mình sẽ triển FR thứ 2 là FR10.
Feature: FR-10 
Bảng test case HW02 của FR10(đã xác nhận): @homework/hw02/ncuong/features/FR10/test-cases.md 
Yêu cầu: hãy lập TEST PLAN tự động hóa gồm >=12 ca (positive/negative/edge), với bảng: T-ID | loại | dữ liệu input | bước thao tác UI | oracle cụ thể | có chạy được bằng UI không. Check @homework/hw04/docs/2026.HW04.Automation Testing_En.md  và @homework/hw04/docs/HW04_TASK_CHECKLIST.md 
Không viết code ở bước này. Sau khi làm xong nhớ AI Audit Log.
```

### The AI output

Artifact chính nằm ở `homework/hw04/ncuong/features/FR10/test-plan-automation.md`: bảng 16 ca A-FR10-01..A-FR10-16 (12 chạy được thuần UI + 4 API assertion DT-08..DT-23), trace HW02 đầy đủ, oracle theo badge `Chờ xác nhận/Đã xác nhận/Đang giao/Đã giao/Đã hủy` + `waitForResponse` 200/400 + `toHaveCount(0)`, ghi chú 2 bug đã kiểm chứng (canceled→delivered `App.jsx:862-868` + `server.js:550-551`; user cancel shipping `Profile.jsx:200` + `server.js:329`). Không sinh code Playwright theo yêu cầu.

---

## Interaction AI-003

- **AI tool:** OpenCode agent — Muse Spark 1.3 Contributor (provider `opencode-go`)
- **Date and time:** 2026-11-17 (UTC) — thời điểm conversation, không có timestamp nguồn chi tiết hơn
- **Source:** Conversation hiện tại; file đính kèm của người dùng: `homework/hw02/ncuong/features/FR17/test-cases.md`, `homework/hw04/docs/HW04_TASK_CHECKLIST.md`
- **Task:** Lập TEST PLAN tự động hóa FR-17 gồm >=12 ca (positive/negative/edge) dạng bảng T-ID | loại | input | bước UI | oracle | chạy được bằng UI không; không viết code.

### Your prompt

```text
Bạn là tester tự động hóa cho SUT EShop (React + Vite, web: http://localhost:5173, admin: http://localhost:5174, API: http://localhost:3000/api).
Đang triển khai HW04: Automation Testing, đọc @homework/hw04/docs/2026.HW04.Automation Testing_En.md . Spec: @api_specification.md  + README @README.md 
Tui phải chọn 3 feature từ HW02, ở đây mình sẽ triển FR thứ 3 là FR17.
Feature: FR-17
Bảng test case HW02 của FR10(đã xác nhận): @homework/hw02/ncuong/features/FR17/test-cases.md 
Yêu cầu: hãy lập TEST PLAN tự động hóa gồm >=12 ca (positive/negative/edge), với bảng: T-ID | loại | dữ liệu input | bước thao tác UI | oracle cụ thể | có chạy được bằng UI không. Check @homework/hw04/docs/2026.HW04.Automation Testing_En.md  và @homework/hw04/docs/HW04_TASK_CHECKLIST.md 
Không viết code ở bước này. Sau khi làm xong nhớ AI Audit Log.
```

### The AI output

Artifact chính nằm ở `homework/hw04/ncuong/features/FR17/test-plan-automation.md`: bảng 18 ca A-FR17-01..A-FR17-18 (15 chạy được thuần UI + 3 API-only DT-05/07/08/13/17/26), trace HW02 đầy đủ, oracle theo row bảng + `row.count()` + `waitForResponse(/\/api\/admin\/coupons/)` + `alert Lỗi`, ghi chú backend `server.js:457-481` không validate + `database.js:31` chỉ UNIQUE + quirk `max_uses||1`. Không sinh code Playwright theo yêu cầu.

---

## Interaction AI-004

- **AI tool:** OpenCode agent — Muse Spark 1.3 Contributor (provider `opencode-go`)
- **Date and time:** 2026-11-17 (UTC) — thời điểm conversation, không có timestamp nguồn chi tiết hơn
- **Source:** Conversation hiện tại
- **Task:** Bước 2 — sinh khung Playwright TS (config 3 browser + data JSON + helper + 1 ca mẫu A-FR02-01), chưa viết các ca còn lại.

### Your prompt

```text
Bạn là tester tự động hóa cho SUT EShop (React + Vite, web: http://localhost:5173, admin: http://localhost:5174, API: http://localhost:3000/api).

Context HW04 đã chốt Bước 1, đọc:
- @homework/hw04/ncuong/features/FR02/test-plan-automation.md
- @homework/hw04/ncuong/features/FR10/test-plan-automation.md
- @homework/hw04/ncuong/features/FR17/test-plan-automation.md
- @frontend-web/src/pages/Login.jsx, @frontend-admin/src/App.jsx, @backend/server.js

Yêu cầu Bước 2 — chỉ sinh KHUNG project, chưa viết hết các ca:
1. Cấu trúc dưới `homework/hw04/ncuong/`: `playwright.config.ts`, `tests/`, `data/`, helper đọc JSON.
2. `playwright.config.ts`: testDir `./tests`, projects chromium/firefox/webkit, `fullyParallel: false`, `retries: 0`, reporter `list` + `html` với `title: "Run by: 23120223"`, metadata `Run by` + `ISO timestamp` + Feature + Browser, outputFolder riêng theo FEATURE/BROWSER, baseURL web 5173, `trace: retain-on-failure`, `screenshot: only-on-failure`.
3. Data file JSON (thống nhất JSON, không CSV):
   - `data/fr02-login.json`: [{id, type, email, password, expected, message}]
   - `data/fr10-orders.json`: [{id, type, sourceStatus, action, expectedStatus, actor}]
   - `data/fr17-coupons.json`: [{id, type, code, discountType, discountValue, minOrderAmount, expiredAt, maxUsesPerUser, expected}]
   Đủ cột phủ test plan, không hardcode data trong spec, sinh giá trị duy nhất theo run (timestamp + browserName).
4. Helper load JSON bằng `readFileSync + JSON.parse`, loop `for (const row of rows)`.
5. Chỉ viết 1 ca mẫu A-FR02-01 đọc từ JSON (getByRole/getByLabel, không XPath/nth-child, không waitForTimeout, dùng auto-wait + waitForResponse). Các ca còn lại để Bước 3.

Không viết code các ca còn lại ở bước này. Nhớ AI Audit log
```

### The AI output

Khung Bước 2 đã tạo, chưa viết các ca còn lại:
- `homework/hw04/ncuong/playwright.config.ts` — 3 projects, `fullyParallel: false`, reporter html `title Run by: 23120223` + metadata ISO/Feature/Browser, outputFolder `reports/html/${FEATURE}-${BROWSER}`.
- `homework/hw04/ncuong/package.json` — `@playwright/test` + scripts.
- `homework/hw04/ncuong/tests/helpers/json-loader.ts` — `loadJson` + `uniqueSuffix`.
- `homework/hw04/ncuong/data/fr02-login.json` — 1 row A-FR02-01 (schema id/type/email/password/expected/message).
- `homework/hw04/ncuong/data/fr10-orders.json` — 1 row A-FR10-01 (schema id/type/sourceStatus/action/expectedStatus/actor).
- `homework/hw04/ncuong/data/fr17-coupons.json` — 1 row A-FR17-01 (schema full coupon).
- `homework/hw04/ncuong/tests/fr02-login.spec.ts` — 1 test `@fr02` A-FR02-01: register unique email qua API, fill 2 textbox theo thứ tự (ghi chú `Login.jsx` label không gắn input nên `getByLabel` fail), `waitForResponse(/api/login)` 200, assert `toHaveURL`, error count 0, `localStorage[token]`, `GET /api/users/me` 200.

---

## Interaction AI-005

- **AI tool:** OpenCode agent — Muse Spark 1.3 Contributor (provider `opencode-go`)
- **Date and time:** 2026-11-17 (UTC) — thời điểm conversation
- **Source:** Conversation hiện tại
- **Task:** Triển full FR02 HW04: data JSON 16 ca + spec 16 ca, start lại SUT, chạy 3 browser (chromium/firefox/webkit), fix 1 lỗi test, verify report có `Run by` + ISO timestamp.

### Your prompt

```text
OK v giờ triển full cho FR02 của HW04 nha (3 trình duyệt), AI Audit Log
```

### The AI output

- `homework/hw04/ncuong/data/fr02-login.json` — mở rộng 1 → 16 rows (A-FR02-01..16, đúng schema đã chốt).
- `homework/hw04/ncuong/tests/fr02-login.spec.ts` — viết lại full 16 test data-driven (`byId`, `uniqueEmail`, `register`, `adminToken`, `findUser`, `uiLogin`, `expectLoginSuccess`; locator `getByRole('textbox')` theo thứ tự vì `Login.jsx` label không gắn input; không `waitForTimeout`; A-FR02-13 backdate `locked_until` qua `sqlite3` CLI thay vì chờ 180s).
- SUT restart (`backend` + `frontend-web` bằng `nohup` sau khi 2 shell background cũ chết; phát hiện 1 lần chạy nhầm `npm run dev` trong thư mục backend và sửa ngay).
- Fix 1 lỗi do AI viết: A-FR02-10 assert 401 cho cả 3 lần sai — thực tế lần 3 trả 403 vì bug +2 khóa sớm ở lần 2; sửa thành 401×2 rồi 403 + comment trace về A-FR02-03/09.
- Kết quả cả 3 browser giống hệt: **16 ca, 11 pass / 5 fail** (chromium 26.5s, firefox 34.1s, webkit 30.8s). 5 fail đều là bug SUT thật: 03 (+2 thay vì +1), 05 (`type=text`), 09 (khóa sớm ở lần 2), 14 (2 input `type=text`), 16 (**null-password bypass: `POST /api/login` với `password:null` được cấp JWT** — critical).
- 3 report `reports/html/fr02-{chromium,firefox,webkit}/`: verify `report.json` trong zip của `index.html` có metadata `Run by: 23120223` + `ISO timestamp` + Feature/Browser, kèm `report-meta.txt` cạnh mỗi report.

---

## Optional audit table

| (1) Prompt + Công cụ | (2) Output AI | (3) Verdict | (4) Lý do | (5) Bản SV sửa |
| --- | --- | --- | --- | --- |
| OpenCode Muse Spark 1.3 Contributor · 2026-11-17 · lập test plan FR-02 >=12 ca | `homework/hw04/ncuong/features/FR02/test-plan-automation.md` (16 ca) | (SV tự điền sau review) | (SV tự điền) | (SV tự điền) |
| OpenCode Muse Spark 1.3 Contributor · 2026-11-17 · lập test plan FR-10 >=12 ca | `homework/hw04/ncuong/features/FR10/test-plan-automation.md` (16 ca) | (SV tự điền sau review) | (SV tự điền) | (SV tự điền) |
| OpenCode Muse Spark 1.3 Contributor · 2026-11-17 · lập test plan FR-17 >=12 ca | `homework/hw04/ncuong/features/FR17/test-plan-automation.md` (18 ca) | (SV tự điền sau review) | (SV tự điền) | (SV tự điền) |
| OpenCode Muse Spark 1.3 Contributor · 2026-11-17 · Bước 2 skeleton + 1 ca mẫu JSON | `playwright.config.ts`, `tests/fr02-login.spec.ts`, `tests/helpers/json-loader.ts`, `data/*.json` | (SV tự điền sau review) | (SV tự điền) | (SV tự điền) |
| OpenCode Muse Spark 1.3 Contributor · 2026-11-17 · full FR02 16 ca + 3 browser | `data/fr02-login.json`, `tests/fr02-login.spec.ts`, `reports/html/fr02-{chromium,firefox,webkit}/` (11 pass / 5 fail mỗi browser) | (SV tự điền sau review) | (SV tự điền) | (SV tự điền) |
