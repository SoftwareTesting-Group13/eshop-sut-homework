# HW03 — GUI & Usability

**Sinh viên:** Dương Nhật Cường · **MSSV:** 23120223 · **Nhóm:** 13
**SUT:** EShop — `https://github.com/ttbhanh/eshop-sut`
**Phạm vi bản nộp này:** Task 1 — GUI Checklist. Task 2 và Task 3 chưa bắt đầu.
**Ngày thực thi:** 2026-11-07

## 0. Bản đồ deliverable

| Deliverable | Đường dẫn |
| --- | --- |
| GUI checklist (Markdown, 66 item) | [`features/GUI/checklist.md`](../features/GUI/checklist.md) |
| GUI checklist (Excel: Checklist, Summary, Execution) | [`features/GUI/checklist.xlsx`](../features/GUI/checklist.xlsx) |
| Checklist AI sinh ban đầu + 25 item bổ sung/sửa sau review | [`features/GUI/ai-checklist-and-review.md`](../features/GUI/ai-checklist-and-review.md) |
| Test summary | [`features/GUI/test-summary.md`](../features/GUI/test-summary.md) |
| Bug report tổng hợp (26 bug) | [`features/GUI/bug-report.md`](../features/GUI/bug-report.md) |
| Báo cáo bug riêng (26 file) | [`features/GUI/bugs/`](../features/GUI/bugs/) |
| GitHub Issues (26 issue đã publish: #80–#105) | [`features/GUI/issues/`](../features/GUI/issues/), [`published.json`](../features/GUI/issues/published.json) |
| Screenshot cho item Failed (38 ảnh) | [`features/GUI/screenshots/`](../features/GUI/screenshots/) |
| AI Audit Report | [`reports/ai-audit.md`](ai-audit.md) |

---

# Task 1 — GUI Checklist

## 1.1 Phạm vi và mục tiêu

Checklist tập trung vào khu vực authentication và profile của EShop web frontend:

| FR | Màn hình | Vì sao chọn |
| --- | --- | --- |
| FR-01 Đăng ký tài khoản | `/register` | Nhiều validation, password rule, email uniqueness và feedback sau đăng ký. |
| FR-02 Đăng nhập & khóa tài khoản | `/login` | Điểm vào của mọi luồng authenticated; input type và thông báo lỗi nhạy cảm. |
| FR-03 Quên mật khẩu & đặt lại (2 bước) | `/forgot-password` | Luồng 2 bước có OTP, step transition, focus và error recovery. |
| FR-04 Quản lý hồ sơ | `/profile` | Form + bảng dữ liệu; có update, empty, loading và error state. |

Bốn interface aspect của đề bài được phủ tường minh:

- **IA-01 General UI standards** — heading, ngôn ngữ, màu hành động, contrast, responsive, RTL, dark mode, zoom.
- **IA-02 Forms** — input type, label, dấu `*`, validation, password rule, OTP, số điện thoại.
- **IA-03 Navigation** — header, link, tab order, focus, active nav, badge giỏ hàng.
- **IA-04 Feedback / state** — loading, success, error, empty, phân biệt lỗi với rỗng.

**Mục tiêu:** tạo checklist hơn 40 item, không trùng lặp, thực thi được; chạy toàn bộ trên SUT; ghi Passed/Failed kèm lý do; tách bug thật khỏi design gap.

## 1.2 Căn cứ đối chiếu

Mỗi item có oracle lấy từ một trong các nguồn sau:

1. **README §FR-01…FR-04** — yêu cầu chức năng của bốn màn hình.
2. **README §FR-21…FR-24** — yêu cầu GUI: ngôn ngữ, màu, đơn vị tiền, `<h1>`, tab order, form, navigation, feedback/state.
3. **API specification** — endpoint, payload và response dùng để chuẩn bị fixture (đăng ký user, lấy OTP, cập nhật profile, lấy orders).
4. **Accessibility baseline** — WCAG 2.2 AA cho contrast, label association, heading, focus và live region. Đây là nhóm item bổ sung có chủ đích, vì đề bài nêu accessibility là ví dụ AI thường bỏ sót.

Các chủ đề **không** thuộc Task 1 đã bị loại khỏi checklist: browser tab title, full-page reload, route guard, order state machine/hủy đơn, coupon, cart, admin, mobile app, cross-browser. Những phần này thuộc Task 2/3 hoặc FR khác.

## 1.3 Phương pháp

Quy trình theo hướng AI-first nhưng có review:

1. **Sinh bộ ban đầu bằng skill `ui-checklist-generator`.**
   Skill mở rộng 8 nhóm (layout, typography, colour, interaction, responsiveness, accessibility, product states, polish) trên 4 màn hình. Kết quả: **44 item**, lưu cùng phần review tại [`ai-checklist-and-review.md`](../features/GUI/ai-checklist-and-review.md).

2. **Review theo README FR-21…FR-24 và API spec.**
   Đối chiếu từng item với yêu cầu thật, sửa oracle sai và bổ sung item còn thiếu. Kết quả:
   - **41 item AI ban đầu được giữ** (3 item bị loại vì ngoài phạm vi GUI: `inputmode=tel`, success toast sau đăng ký, route guard).
   - **25 item bổ sung/sửa** trong review, mỗi item có lý do AI bỏ sót ở [`ai-checklist-and-review.md`](../features/GUI/ai-checklist-and-review.md).
   - Checklist cuối: **66 item**.

3. **Thực thi trên SUT local.**
   Hành vi chức năng được điều khiển bằng Playwright 1.65 (Chromium 158); DOM/ARIA facts đọc từ trang live; contrast và label violation lấy từ axe-core 4.x. Mỗi item được đánh Passed/Failed; item Failed có Notes ghi quan sát cụ thể.

4. **Chụp screenshot cho item Failed.**
   Mỗi ảnh có banner đỏ tiếng Việt ghi checklist ID, mô tả lỗi và quan sát thực tế. Không chụp cho item Passed.

5. **Triage bug.**
   Các Failed item được gom theo root cause. Một Failed item không tự động là bug: thiếu confirm-password hay thiếu step indicator là design gap; bug report chỉ gồm defect tái hiện được. Kết quả: **26 bug**.

## 1.4 Thiết kế checklist

**66 item**, chia theo IA:

| Interface aspect | Items | Passed | Failed |
| --- | ---: | ---: | ---: |
| IA-01 General UI standards | 18 | 7 | 11 |
| IA-02 Forms | 17 | 4 | 13 |
| IA-03 Navigation | 15 | 9 | 6 |
| IA-04 Feedback / state | 16 | 7 | 9 |
| **Tổng** | **66** | **27** | **39** |

Phân nguồn: **41 item AI ban đầu** + **25 item bổ sung/sửa sau review**.

Phân bố theo màn hình:

| Màn hình | Items | Nội dung chính |
| --- | ---: | --- |
| Login | 14 | heading, ngôn ngữ, input type, label, tab order, loading, error, RTL |
| Register | 14 | `<h1>`, contrast, email format, password rule, confirm password, duplicate email, raw error, loading |
| Forgot Password | 15 | `<h1>`, email type, OTP 6 số, confirm password, step indicator, focus, alert, button hierarchy |
| Profile | 15 | `<h1>`, label, phone validation, contrast, active nav, logout label, empty/loading/error state, mobile table |
| All auth screens | 7 | ngôn ngữ, dấu `*`, error position, RTL, dark mode, 200% zoom, badge giỏ hàng |
| Register + Forgot Password | 1 | màu nút hành động tích cực |

Bảng đầy đủ từng item, kết quả và lý do fail nằm ở [`checklist.md`](../features/GUI/checklist.md) và [`checklist.xlsx`](../features/GUI/checklist.xlsx).

## 1.5 Review: AI bỏ sót gì và vì sao

25 item bổ sung/sửa được ghi chi tiết ở [`ai-checklist-and-review.md`](../features/GUI/ai-checklist-and-review.md). Lý do chia thành ba nhóm.

### A. Chất lượng prompt

Prompt đầu yêu cầu checklist cho 4 màn hình nhưng không buộc AI viết **executable oracle** cho từng item. Vì vậy AI viết những câu chung như “đủ contrast”, “mobile dùng được”, “feedback rõ ràng” mà không có cách quyết định Pass/Fail. Review đã chuyển thành kiểm tra đo được:

- contrast ratio tính bằng axe-core ≥ 4.5:1;
- `scrollWidth = clientWidth` ở 360px;
- `document.activeElement` sau step transition;
- `label[for]`/`input#id` hoặc `aria-label`;
- `aria-current`, `aria-live`, `aria-busy`.

### B. Giới hạn của model

- **Không chạy được SPA.** AI không thấy `tabindex="1"` đẩy focus vào nút Sign In, không thấy focus mất sau bước OTP, không thấy 500 response bị hiển thị thành empty list.
- **Accessibility theo bề ngoài.** AI coi label hiển thị là đủ; không kiểm tra `for`/`id`, `aria-label`, `aria-live`, `aria-invalid`, heading level.
- **Không tính contrast.** AI chỉ nói “kiểm tra contrast”; axe-core mới tìm ra 2.53:1, 3.76:1, 3.92:1.
- **Mặc định LTR, light mode, 100% zoom.** RTL, dark mode và 200% reflow chỉ xuất hiện sau review.
- **Đọc OTP là feedback hữu ích.** AI không phân biệt “hiển thị OTP trong demo” (FR-03 cho phép) với “lộ OTP trong production”; review sửa oracle thành Passed cho môi trường demo.

### C. Đặc thù của SUT

- Copy password rule hứa “ký tự đặc biệt” nhưng regex yêu cầu whitespace và chặn ký tự đặc biệt — mâu thuẫn chỉ lộ khi đọc cả copy và regex.
- Regex số điện thoại `/^[1-9][0-9]{8,9}$/` từ chối mọi số Việt Nam bắt đầu bằng `0`, gồm placeholder `0912345678`.
- Luồng reset 2 bước nằm trong một component, nên focus management và step indicator dễ bị bỏ sót.
- Bảng lịch sử đơn hàng 5 cột không có wrapper responsive, chỉ tràn khi có order.
- Header dùng utility vật lý (`text-right`, `ml/mr`) nên RTL không mirror.

## 1.6 Môi trường thực thi

| Item | Giá trị |
| --- | --- |
| Backend | `http://localhost:3000` (`backend/server.js`, SQLite seed) |
| Web frontend | `http://localhost:5173` (`frontend-web`, Vite) |
| Browser | Chromium 158 / Playwright 1.65 |
| Desktop viewport | 1280×900 |
| Mobile viewport | 360×800 |
| 200% zoom equivalent | 640×800 |
| Accessibility engine | axe-core 4.x |
| Test user | `test@eshop.com` / `Test1234!` (seed) |
| Fixture | User đăng ký qua API/UI; order inject bằng Playwright route interception, không sửa DB order thật |

Quy ước kết quả:

- **Passed** = hành vi quan sát khớp oracle trong môi trường đã chạy.
- **Failed** = hành vi quan sát mâu thuẫn oracle; Notes ghi chính xác quan sát.
- Screenshot chỉ có cho item Failed; banner đỏ ghi ID và lỗi.
- Contrast lấy từ ratio axe-core tính, không ước lượng bằng mắt.

## 1.7 Kết quả và phân tích

### 1.7.1 Kết quả tổng

**27/66 item Passed, 39/66 Failed.** Tỷ lệ fail cao vì SUT được seed lỗi UI/UX có chủ đích, và checklist cố ý phủ accessibility cùng các state edge case mà smoke test happy-path thường bỏ qua.

### 1.7.2 Vấn đề hệ thống (không phải bug lẻ)

1. **Auth screen thiếu semantic pass.** Login ghi “Đăng Ký”, mật khẩu `type="text"`, email `type="text"`, mọi label thiếu `for/id`, không trang nào có `<h1>`. Đây là một pattern copy/paste form chứ không phải bốn lỗi rời.
2. **Feedback thiếu hoặc blocking.** Login render error dưới nút submit, không `role="alert"`/`aria-live`; Forgot Password dùng `alert()`; Profile dùng `alert()` cho phone error. Không có pattern inline message dùng chung.
3. **State handling nhị phân.** Login/Register không có loading state; Profile hiện “chưa có đơn hàng” cả khi đang load và khi 500. UI không phân biệt “chưa bắt đầu”, “rỗng”, “lỗi”, “xong”.
4. **Accessibility chưa nằm trong definition of done.** axe-core báo critical label violation trên cả bốn màn hình; contrast fail ở Register/Profile; tab order bị `tabIndex={1}` phá; RTL không mirror.
5. **Security-sensitive action thiếu safeguard.** OTP chỉ 4 chữ số thay vì 6 (FR-03/SEC-07); Forgot Password hiển thị OTP trên màn hình (đúng demo FR-03 nhưng cần lưu ý production); phone validation chặn số hợp lệ.

### 1.7.3 Bug theo severity

| Severity | Số lượng | Ví dụ |
| --- | ---: | --- |
| Blocker | 1 | Regex số điện thoại từ chối số Việt Nam hợp lệ, chặn lưu profile (BUG-GUI-14) |
| Major | 11 | Mật khẩu hiển thị, label thiếu association, email format/duplicate, password rule mâu thuẫn, mobile table overflow, tab order, raw server error, alert-only feedback, order loading/error, OTP 4 số |
| Minor | 14 | Heading sai, thiếu `<h1>`, contrast, button hierarchy, RTL, active nav, logout label, empty state, badge giỏ hàng, loading state, focus loss |
| **Tổng** | **26** | Xem [`bug-report.md`](../features/GUI/bug-report.md) |

Mỗi bug report có:

- bước tái hiện;
- bảng Expected/Actual;
- screenshot;
- **root cause kèm code block lấy trực tiếp từ source** và link GitHub tới đúng dòng, ví dụ [`frontend-web/src/pages/Login.jsx:24`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Login.jsx#L24);
- đề xuất sửa.

## 1.8 Hạn chế và việc còn lại

- **GitHub Issues đã publish.** 26 issue (#80–#105) đã được tạo và screenshot dùng raw URL trên nhánh `ncuong` đã push; danh sách máy đọc ở [`features/GUI/issues/published.json`](../features/GUI/issues/published.json).
- **Task 1 mới chạy trên một browser engine (Chromium).** Firefox, Safari và Expo Go thuộc Task 3.
- **Bộ AI ban đầu được giữ nguyên để đối chiếu audit.** Sinh viên cần xác nhận 66 item và 26 bug trước khi nộp.
- **Timestamp trong AI audit** ghi “không có trong nguồn” vì conversation export không chứa thời gian.

---

# Task 2 — Usability Evaluation

Chưa bắt đầu. Khi làm sẽ chọn một end-to-end flow, chạy 7 participant, pilot 1 người, dùng SUS/UEQ-S và phân tích severity.

# Task 3 — Cross-Browser / Cross-Platform

Chưa bắt đầu. Khi làm sẽ chạy lại checklist trên Chrome, Firefox và Safari (hoặc Android Chrome / Expo Go), screenshot có overlay MSSV + họ tên.
