# FR-02 — TEST PLAN tự động hóa HW04 (UI Playwright + hybrid API verify)

> Feature: FR-02 Login and account lockout. Web: `http://localhost:5173/login`, API: `http://localhost:3000/api`.
> Nguồn HW02: `homework/hw02/ncuong/features/FR02/test-cases.md` (18 T-ID: DT-01..DT-11, BVA-02..BVA-08).
> Không viết code ở bước này — chỉ chốt plan để sinh script data-driven ở bước sau.
> SUT thực tế đã kiểm chứng (không đoán):
> - `frontend-web/src/pages/Login.jsx:24` — `<h2>Đăng Ký</h2>` (sai, phải "Đăng Nhập").
> - `frontend-web/src/pages/Login.jsx:30` — input email `type="text"` (spec FR-02 yêu cầu `type="email"`).
> - `frontend-web/src/pages/Login.jsx:40` — input mật khẩu `type="text"` (spec FR-22 yêu cầu `type="password"`).
> - `frontend-web/src/pages/Login.jsx:18` — mọi lỗi đều `Đăng nhập thất bại. Vui lòng kiểm tra lại.` (không phân biệt sai MK / chưa đăng ký / đang khóa).
> - `frontend-web/src/pages/Login.jsx:28` — label `Username` (không phải Email).
> - `backend/server.js:54` — `login_attempts + 2` (spec: +1 đúng 1 đơn vị) → BUG.
> - `backend/server.js:57` — `Date.now() + 180000` = 180s (spec: 30s) → BUG.
> - `backend/server.js:40-43` — khi khóa trả 403 `Tài khoản đã bị khóa...`, nhưng UI nuốt thành message generic → UI không phân biệt được trạng thái khóa nếu chỉ assert text.
> - `frontend-web/src/context/AuthContext.jsx:27-32` — login thành công lưu `localStorage[token]` + `navigate('/')`.

**Quy ước chạy:**
- Mỗi ca tạo user riêng qua `POST /api/register` (`email=fr02.auto<NN>.<timestamp>@eshop.com`, `password=Passw0rd!`) trong `beforeEach` để 3 browser không đụng dữ liệu.
- "Hybrid" = thao tác bằng UI, verify thêm bằng API (`POST /api/login` trực tiếp / `GET /api/admin/users` / đọc `locked_until`) vì UI không lộ `login_attempts`/`locked_until`.
- Không dùng `waitForTimeout` cứng; dùng auto-wait (`expect(...).toBeVisible()`, `toHaveURL`).
- Ca khóa thật (180s thực tế) không chờ tường minh trong suite: preset `locked_until` qua API/SQL để mô phỏng, chỉ 1 ca chờ hết hạn nếu cần.

| T-ID (auto) | Loại | Dữ liệu input | Bước thao tác UI | Oracle cụ thể | Chạy được bằng UI không? (Trace HW02) |
| --- | --- | --- | --- | --- | --- |
| A-FR02-01 | Positive | `email=<fresh>`, `password=Passw0rd!` (đúng) | 1. Mở `/login` (chưa login). 2. Điền Username + Mật khẩu. 3. Bấm `Sign In`. | 1. URL về `/` (`toHaveURL(/\/$/)`). 2. Không hiện lỗi generic. 3. `localStorage[token]` tồn tại. 4. `GET /api/users/me` với token → 200. | Có — thuần UI + API verify. (DT-01) |
| A-FR02-02 | Positive | Link `Quên mật khẩu?` | 1. Mở `/login`. 2. Bấm link `Quên mật khẩu?`. | URL → `/forgot-password`. | Có — thuần UI. (điều hướng, FR-03 liên quan) |
| A-FR02-03 | Negative | `email=<fresh>`, `password=WrongPass1!` | Như A-FR02-01 nhưng MK sai. | 1. Vẫn ở `/login`. 2. Hiện đúng `Đăng nhập thất bại. Vui lòng kiểm tra lại.`. 3. `localStorage[token]` rỗng. 4. Hybrid: `login_attempts` tăng đúng 1 (spec) — **dự kiến FAIL vì backend +2** → bug. | Có — UI trigger + API verify counter. (DT-02) |
| A-FR02-04 | Negative | `email=nobody.<ts>@eshop.com` (chưa đăng ký), `password=Passw0rd!` | Như trên. | Như A-FR02-03 (vẫn `/login` + message generic + không token). Không tạo user mới. | Có — thuần UI. (DT-03) |
| A-FR02-05 | Negative | `email=not-an-email`, `password=Passw0rd!` | 1. Mở `/login`. 2. Điền `not-an-email`. 3. Bấm `Sign In`. Đồng thời assert thuộc tính input. | Spec: input `type="email"` + HTML5 chặn, 0 request `/api/login`, vẫn `/login`. **Actual SUT `type="text"` nên request vẫn gửi → ca FAIL → bug FR-02/FR-22.** Oracle automation ghi theo spec để lộ bug. | Có — thuần UI (dự kiến FAIL thành bug). (DT-09, DT-06) |
| A-FR02-06 | Negative | `email=""`, `password=Passw0rd!` | 1. Mở `/login`. 2. Để trống Username. 3. Bấm `Sign In`. | `required` chặn submit: vẫn `/login`, 0 request `/api/login`, không token. | Có — thuần UI (native validation). (DT-05) |
| A-FR02-07 | Negative | `email=<fresh>`, `password=""` | Như trên nhưng để trống Mật khẩu. | Như A-FR02-06. | Có — thuần UI. (DT-04 biến thể) |
| A-FR02-08 | Edge | `email=<fresh>` sai 1 lần rồi đúng (`WrongPass1!` → `Passw0rd!`) | 1. Login sai 1 lần (verify lỗi). 2. Xóa MK, nhập đúng, bấm lại. | Lần 2 thành công như A-FR02-01; `login_attempts=0`, `locked_until=NULL` (hybrid verify). | Có — UI + API verify. (BVA-07) |
| A-FR02-09 | Edge | `email=<fresh>` sai liên tiếp 2 lần | Sai 2 lần liên tiếp trên UI. | Sau lần 2: vẫn `/login` + lỗi generic; hybrid: `login_attempts=2`, `locked_until=NULL` (chưa khóa) — **dự kiến lệch vì bug +2 (lần 1 đã =2, lần 2 =4 → khóa sớm)** → bug. | Có — UI + API verify. (BVA-02) |
| A-FR02-10 | Edge | `email=<fresh>` preset `login_attempts=2`, sai lần 3 | Setup API/SQL `attempts=2`, rồi sai 1 lần trên UI. | Tài khoản bị khóa: login đúng ngay sau đó vẫn bị từ chối (vẫn `/login` + lỗi). Hybrid: `locked_until` được đặt (ISO tương lai). Thời gian khóa spec 30s nhưng actual 180s → assert khoảng thời gian sẽ FAIL → bug. | Có — setup API + trigger UI. (BVA-03) |
| A-FR02-11 | Edge | Tài khoản đang khóa, nhập MK **đúng** | Preset `locked_until` tương lai; mở `/login`, nhập đúng MK, submit. | Vẫn `/login` + lỗi (UI không hiện message khóa riêng — assert text khóa riêng sẽ FAIL, phải assert generic + verify 403 qua API trực tiếp). Không token; `attempts`/`locked_until` không đổi. | Có (hybrid) — UI không phân biệt lý do, phải verify API. (DT-07) |
| A-FR02-12 | Edge | Tài khoản đang khóa, nhập MK **sai** | Như trên nhưng MK sai. | Như A-FR02-11 + hybrid: bộ đếm **không** tăng thêm khi đang khóa. | Có (hybrid). (DT-08, BVA-04) |
| A-FR02-13 | Edge | `locked_until` quá khứ (hết hạn), MK đúng | Setup `locked_until=<now-60s>`; login đúng trên UI. | Thành công như A-FR02-01 (hết khóa). | Có — setup API + trigger UI. (BVA-08) |
| A-FR02-14 | Edge | Check `type` của 2 input + label | Mở `/login`, đọc DOM. | Email `type="email"`, password `type="password"` (spec FR-02/FR-22). **Actual cả hai `type="text"` → FAIL → 2 bug.** | Có — thuần UI DOM assert. (DT-09 mở rộng, FR-22) |
| A-FR02-15 | Negative (API-only) | Body `{"email":<valid>}` thiếu key `password` | Không thao tác form (form `required` không tạo được body thiếu key). Gọi `POST /api/login` trực tiếp. | Không cấp JWT; nếu tính là sai thì `attempts` +1, không khóa. | Không — không nhập được qua UI. (DT-10) |
| A-FR02-16 | Negative (API-only) | `{"email":<null-pwd-user>,"password":null}` | Tương tự: fixture tạo qua `POST /api/register` với `password:null`, rồi `POST /api/login` với `null`. | Không cấp JWT; không coi `null===null` là thành công. | Không — form gửi chuỗi, không gửi JSON `null`. (DT-11) |

**Tổng: 16 ca (4 P / 6 N / 6 E). Chạy được bằng UI (thuần + hybrid): 14 ca ≥ 12 theo đề. API-only: 2 ca (ghi lý do, không bỏ).**
**3 assertion pattern chính dùng cho FR-02:** (A) URL/navigation `toHaveURL`, (B) hiển thị/nội dung `toBeVisible` + message generic, (C) storage/API `localStorage[token]` + `waitForResponse(/\/api\/login/)` + status code.
