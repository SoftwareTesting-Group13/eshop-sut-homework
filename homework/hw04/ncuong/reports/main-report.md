# HW04 — AI Automation Testing: Main Report
**Sinh viên:** Dương Nhật Cường · **MSSV:** 23120223
**Repo:** https://github.com/SoftwareTesting-Group13/eshop-sut-homework (nhánh `ncuong`, thư mục `homework/hw04/ncuong`)

## 1. Thông tin chung và feature đã chọn

Bài cá nhân HW04-AI, tự động hóa web frontend bằng Playwright + data-driven JSON + chạy 3 browser, theo đúng đề `homework/hw04/docs/2026.HW04.Automation Testing_En.md`.

Ba feature trùng HW02 (mỗi pool một feature, nhóm 13 không trùng nhau):

| Pool | FR | Feature | T-ID HW02 | TC tự động HW04 |
| --- | --- | --- | ---: | ---: |
| A | FR-02 | Login and account lockout | 18 | 16 (A-FR02-01..16) |
| B | FR-10 | Order state machine | 23 | 16 (A-FR10-01..16) |
| C | FR-17 | Coupon management (CRUD) | 32 | 18 (A-FR17-01..18) |

## 2. Môi trường và cách chạy

| Thành phần | Giá trị |
| --- | --- |
| Backend API | `http://localhost:3000/api` (Node + Express + SQLite) |
| Web khách | `http://localhost:5173` (React + Vite) |
| Web admin | `http://localhost:5174` (React + Vite) |
| Framework | Playwright 1.65.1, TypeScript, Node v26.9.0 |
| Browser | chromium-1255, firefox-1572, webkit-2388 (3 projects) |
| Tài khoản | admin `admin@eshop.com` / `Admin123!`, user `test@eshop.com` / `Test1234!` (seed); fixture user/đơn/coupon tạo mới mỗi test qua API nên 3 browser không đụng dữ liệu |

Config `playwright.config.ts`: `fullyParallel: false`, `retries: 0`, reporter `list` + `html` với `outputFolder reports/html/${FEATURE}-${BROWSER}`, top-level `metadata` gồm `Run by: 23120223` + `ISO timestamp` + Feature/Browser (đã verify nằm trong `report.json` của mỗi HTML report), kèm file `report-meta.txt` cạnh mỗi report. Lệnh chạy: `FEATURE=<fr> BROWSER=<b> npx playwright test --project=<b> --grep "@<fr>"` (9 lần, không dùng `--reporter=...` vì flag này ghi đè reporter config làm mất HTML).

## 3. Quy trình AI-first đã dùng

Không dùng 1 prompt chung. Đi theo từng bước, mỗi bước 1 prompt (chi tiết trong `reports/ai-audit.md`, 7 interactions AI-001..AI-007):

1. **Test plan**: đưa context SUT + bảng HW02, yêu cầu bảng T-ID/loại/input/bước UI/oracle/chạy được bằng UI không, **cấm viết code** → `features/FR*/test-plan-automation.md` (16/16/18 ca).
2. **Skeleton**: config 3 browser + `data/*.json` + helper đọc JSON + **1 ca mẫu** (A-FR02-01).
3. **Viết spec**: data JSON full (thống nhất JSON thay vì lẫn csv/json như checklist gợi ý) + spec đọc từ file (không hardcode dataset).
4. **Chạy thật từng browser, fix, verify lại** + dọn DB (xóa fixture rò rỉ, phát hiện qua `sqlite3`).
5. **Bug report + GitHub Issues + screenshot** cho mỗi fail thật.
6. **Review-hardening** (5 commit): tách helper, assert pre-state, sửa try/finally thiếu.

## 4. Automation report

### 4.1 FR-02 — Login and account lockout (16 ca: 2 P / 7 N / 7 E)

- Data: `data/fr02-login.json` (`id/type/email/password/altPassword/expected/message`).
- UI: `/login` — locator `getByRole('textbox')` theo thứ tự (label `Username`/`Mật khẩu` không gắn với input nên `getByLabel` fail — phát hiện khi review).
- Hybrid verify: `localStorage[token]`, `GET /api/users/me`, `GET /api/admin/users` (đọc `login_attempts`/`locked_until` vì UI không lộ), backdate `locked_until` bằng `sqlite3` cho ca hết hạn (tránh chờ 180s).
- Kết quả (giống hệt 3 browser): **16 ca, 11 pass / 5 fail**. 5 fail đều là bug SUT (xem §6).

### 4.2 FR-10 — Order state machine (16 ca: 7 P / 7 N / 2 E)

- Data: `data/fr10-orders.json` (`sourceStatus/action/expectedStatus/actor/total/address`).
- UI admin (tab Đơn hàng): bấm `Xác nhận/Giao hàng/Hoàn thành/Hủy`, assert badge (`Chờ xác nhận/Đã xác nhận/Đang giao/Đã giao/Đã hủy`), assert vắng mặt nút (`toHaveCount(0)`) cho transition bị cấm, dialog `Hủy đơn thành công` bắt bằng `waitForEvent`. Định vị row bằng cell `#id` exact (tránh `#1` khớp `#10`).
- UI user (`/profile`): `Hủy đơn` cho pending/confirmed.
- API trong cùng spec: transition sai (DT-08..DT-15), user cancel sai trạng thái (DT-16..18), phân quyền actor (DT-21..23).
- Kết quả (giống hệt 3 browser): **16 ca, 13 pass / 3 fail**. 3 fail đều là bug SUT (xem §6).

### 4.3 FR-17 — Coupon management CRUD (18 ca: 9 P / 8 N / 1 E)

- Data: `data/fr17-coupons.json` (full schema coupon + `__OMITTED__` cho ca thiếu key).
- UI admin (tab Mã Giảm Giá): fill theo placeholder, `selectOption` loại, submit + `waitForResponse POST`, assert row/count/seeds, dialog `Lỗi` cho trùng mã, `DELETE` + assert row biến mất. Mã duy nhất theo run (`CODE-<timestamp>`) + `try/finally` + `deleteByCode` dọn dữ liệu (DB luôn về đúng 4 seed sau suite).
- API trong cùng spec: thiếu key, `save10` thường, type/date/discount/max sai.
- Kết quả (giống hệt 3 browser): **18 ca, 10 pass / 8 fail**. 8 fail đều là thiếu validation backend (xem §6).

### 4.4 Assertion patterns (mỗi feature ≥ 3 kiểu, đề yêu cầu)

| Kiểu | FR-02 | FR-10 | FR-17 |
| --- | --- | --- | --- |
| URL/navigation (`toHaveURL`) | x | | |
| Hiển thị/nội dung (`toBeVisible`, `toHaveAttribute`) | x | x (badge) | x (badge/row) |
| Vắng mặt (`toHaveCount(0)`) | x (lỗi/token) | x (nút cấm) | x (row) |
| Đếm tập hợp (row count trước/sau) | | | x |
| API response (`waitForResponse` + status) | x | x | x |
| Storage (`localStorage`) | x | x (token inject) | x (token inject) |
| Dialog (`waitForEvent`) | | x | x |
| DB/API verify (`login_attempts`, `GET /api/coupons`) | x | x (`GET /api/orders/:id`) | x |

## 5. Review / gap analysis (human review — phần bắt buộc)

| # | AI làm sai / bỏ sót | Mức độ | Nguyên nhân gốc | Cách sửa (commit) |
| --- | --- | --- | --- | --- |
| 1 | `getByLabel('Mật khẩu')` — label SUT không gắn input, locator fail | Cao | AI không đọc DOM thật, đoán theo chuẩn form | textbox theo thứ tự + comment (`757fb80`) |
| 2 | A-FR02-10 assert 401 cho cả 3 lần sai — thực tế lần 3 trả 403 vì khóa sớm (bug +2) | Trung bình | AI không mô phỏng tương tác giữa các bug SUT | 401×2 + 403 + comment trace |
| 3 | Literal `Passw0rd!`/`WrongPass1!` trong spec — vi phạm data-driven | Cao | Prompt không nhấn mạnh "mọi test data vào file" | cột `altPassword` trong JSON; quét lại toàn spec |
| 4 | `page.on('dialog')` + assert ngay — race, alert chưa kịp hiện (A-FR10-06 fail lẻ) | Cao | AI không lý luận về async UI | `waitForEvent('dialog')` |
| 5 | A-FR10-08 assert trên state cũ trước khi PUT về — false-pass | Cao | AI không đợi phản hồi mạng | `waitForResponse` PUT + assert actual trước, spec sau |
| 6 | Kết quả 08 khác nhau giữa chromium/firefox — race re-render | Cao | Assert phụ thuộc timing | chốt pattern deterministic (actual → spec) |
| 7 | `adminLogin` vs `adminToken` lệch tên sau refactor → 16 fail trắng | Trung bình | Đổi tên không sửa hết chỗ dùng | alias import + chạy lại suite |
| 8 | A-FR17-16 thiếu `try/finally` — rò rỉ 3 row `NULL` vào DB | Trung bình | AI viết cleanup sau expect, fail là bỏ qua | bọc `try/finally` (phát hiện bằng `sqlite3 COUNT`) |
| 9 | `--reporter=line` ghi đè config, mất HTML report | Quy trình | Không đọc kỹ cơ chế reporter Playwright | chỉ dùng reporter config, `tail` output |
| 10 | Server SUT tự chết khi idle — loạt fail `ECONNREFUSED` giả | Môi trường | Hiểu nhầm fail môi trường là fail test | guard `curl` trước mỗi run; `nohup` + restart |

Kết luận: AI-first không thay thế review — giá trị nằm ở vòng lặp prompt → chạy thật → đọc log → sửa. 5 commit hardening (`ed36549`, `a41fa26`, `c682007`, `ca0b2bf`, `3dbf6cb`) đều sinh ra từ vòng lặp này, nâng tổng số commit đụng spec lên 8/8.

## 6. Bug report tổng hợp

| Bug | Feature | Test fail | Severity | Root cause | Issue |
| --- | --- | --- | --- | --- | --- |
| Counter +2, khóa sớm ở lần 2 | FR-02 | 03, 09 | Major | `server.js:54` (`+2` thay vì `+1`) | #128 |
| Input `type="text"`, không validate HTML5, lộ MK | FR-02 | 05, 14 | Major | `Login.jsx:30,40` | #129 |
| Login `password:null` được cấp JWT (null===null) | FR-02 | 16 | Blocker | `server.js:46` | #130 |
| `canceled→delivered` được cho phép | FR-10 | 08 | Major | `server.js:550-551` + `App.jsx:862-868` | #131 |
| User hủy được đơn `shipping` | FR-10 | 15 | Major | `server.js:329` + `Profile.jsx:200` | #132 |
| API admin không check `role` | FR-10/FR-12 | 16 | Blocker | thiếu check `req.user.role` toàn backend | #133 |
| Biên số không validate (discount 0/-1/150, min -1) | FR-17 | 05, 06, 08, 12 | Major | `server.js:457-481`, `database.js` không CHECK | #134 |
| Code không validate (trắng, trùng khác hoa/thường, thiếu key → NULL) | FR-17 | 04, 16, 17 | Major | `server.js:457-481`, `UNIQUE` phân biệt hoa/thường + nullable | #135 |
| Trường còn lại không validate (type lạ, discount chữ, date rác, max 0→1) | FR-17 | 18 | Major | `server.js:457-481,474` (`\|\| 1`) | #136 |

Chi tiết từng bug + screenshot trong `features/FR*/bugs/BUG-*.md`; tất cả 9 issues OPEN tại https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues (lọc `BUG-FR`).

## 7. Test case không tự động hóa được

Không có. Mọi ca HW02 dạng API-only đều được tự động hóa bằng request assertion trong cùng spec Playwright: DT-10/DT-11 → A-FR02-15/16; DT-08..DT-23 → A-FR10-13..16 (invalid transition, user cancel sai trạng thái, actor gates); DT-05/07/08/13/17/26 → A-FR17-16/17/18. Không dùng thao tác DevTools giả UI.

## 8. Agent Skill (10đ)

Skill `skills/automation-test-writer/` (mô tả workflow data-driven + 3 browser + `Run by`, templates, script sinh skeleton) — **đang xây dựng**. Video demo dùng skill end-to-end trên 1 feature: **chưa quay** (link sẽ bổ sung vào README).

## 9. Test summary và tự đánh giá

| Feature | Pool | TC automated | TC executed | PASS | FAIL | Browser runs | Bugs |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| FR-02 | A | 16 | 48 | 33 | 15 | 3 | 3 |
| FR-10 | B | 16 | 48 | 39 | 9 | 3 | 3 |
| FR-17 | C | 18 | 54 | 30 | 24 | 3 | 3 |
| **Tổng** | | **50** | **150** | **102** | **48** | **9** | **9** |

Mọi fail đều là bug SUT đã xác nhận (16 fail-instance gộp theo root cause thành 9 issues); không có fail do script sau vòng hardening.

| No. | Criteria | Điểm tối đa | Điểm tự đánh giá |
| ---: | --- | ---: | --- |
| 1 | Task 1 - Feature A (FR-02) | 25 | |
| 1 | Task 1 - Feature B (FR-10) | 25 | |
| 1 | Task 1 - Feature C (FR-17) | 25 | |
| 2 | Task 2 — Demo video | 15 | |
| 3 | Agent Skills | 10 | |
| **Tổng** | | **100** | |

*(Cột tự đánh giá do sinh viên điền khi chốt; demo video và skill video chưa có.)*

## 10. Tài liệu tham khảo

- Đề HW04 (`homework/hw04/docs/2026.HW04.Automation Testing_En.md`); checklist HW04.
- `api_specification.md`; `README.md` (SRS EShop).
- Test case HW02: `homework/hw02/ncuong/features/{FR02,FR10,FR17}/test-cases.md`.
- Playwright docs (test runner, reporters, locators); SQLite docs.
