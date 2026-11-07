# GUI Checklist — Login, Register, Forgot Password, Profile

**SUT:** EShop (http://localhost:5173) · **FRs:** FR-01, FR-02, FR-03, FR-04 · **Interface aspects:** IA-01…IA-04

**Execution date:** 2026-11-07 · **Browser:** Chromium 158 (Playwright 1.65) · **Viewport:** 1280×900; mobile checks at 360×800 and 640×800.


## Summary

| Interface aspect | Items | Passed | Failed |
| --- | ---: | ---: | ---: |
| IA-01 | 19 | 8 | 11 |
| IA-02 | 16 | 4 | 12 |
| IA-03 | 17 | 9 | 8 |
| IA-04 | 17 | 4 | 13 |
| **Total** | **69** | **25** | **44** |

Source split: **44 AI-initial items** + **25 review additions**. Bug IDs: BUG-GUI-01, BUG-GUI-02, BUG-GUI-03, BUG-GUI-04, BUG-GUI-05, BUG-GUI-06, BUG-GUI-07, BUG-GUI-08, BUG-GUI-09, BUG-GUI-10, BUG-GUI-11, BUG-GUI-12, BUG-GUI-13, BUG-GUI-14, BUG-GUI-15, BUG-GUI-16, BUG-GUI-17, BUG-GUI-18, BUG-GUI-19, BUG-GUI-20, BUG-GUI-21, BUG-GUI-22, BUG-GUI-23, BUG-GUI-24, BUG-GUI-25, BUG-GUI-26.


## IA-01 — General UI standards

| ID | Screen | FR | Checklist item | Source | Result | Notes / failure reason | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-01 | Login | FR-02 | The page heading names the Login screen and matches the action. | AI initial | **Failed** | Observed <h2>Đăng Ký</h2> on /login; expected a Login heading such as “Đăng nhập”. | [CHK-01-login-heading.png](screenshots/CHK-01-login-heading.png) |
| CHK-02 | Login | FR-02 | The browser tab title is unique and describes the Login page. | Review addition | **Failed** | document.title = "frontend-web" on /login; no page-specific title. | [CHK-02-login-title.png](screenshots/CHK-02-login-title.png) |
| CHK-03 | Login | FR-02 | The auth card uses the same alignment, spacing and typography as Register and Forgot Password. | AI initial | Passed | All three auth screens use max-w-md mx-auto mt-10 bg-white p-8 border rounded shadow-sm. | DOM inspection |
| CHK-04 | Login | FR-02 | The Login page has no horizontal scrolling at a 360px viewport. | AI initial | Passed | scrollWidth = clientWidth = 360. | Playwright viewport 360px |
| CHK-05 | Register | FR-01 | The page heading names the Register screen. | AI initial | Passed | Observed <h2>Đăng Ký Tài Khoản</h2>. | DOM inspection |
| CHK-06 | Register | FR-01 | The browser tab title is unique and describes the Register page. | Review addition | **Failed** | document.title = "frontend-web" on /register. | [CHK-06-register-title.png](screenshots/CHK-06-register-title.png) |
| CHK-07 | Register | FR-01 | Helper text and the primary button meet WCAG 2.2 AA contrast (4.5:1 normal text). | Review addition | **Failed** | axe-core: helper text #9ca3af on #ffffff = 2.53:1; white on #ef4444 = 3.76:1. | [CHK-07-register-contrast.png](screenshots/CHK-07-register-contrast.png) |
| CHK-08 | Register | FR-01 | The Register page has no horizontal scrolling at a 360px viewport. | AI initial | Passed | scrollWidth = clientWidth = 360. | Playwright viewport 360px |
| CHK-09 | Forgot Password | FR-03 | The page heading names the Forgot Password screen. | AI initial | Passed | Observed <h2>Quên Mật Khẩu</h2>. | DOM inspection |
| CHK-10 | Forgot Password | FR-03 | The browser tab title is unique and describes the Forgot Password page. | Review addition | **Failed** | document.title = "frontend-web" on /forgot-password. | [CHK-10-forgot-title.png](screenshots/CHK-10-forgot-title.png) |
| CHK-11 | Forgot Password | FR-03 | Step 2 primary and secondary actions are visually distinguishable. | AI initial | **Failed** | “Đặt lại mật khẩu” and “← Quay lại” are both full-width green buttons with identical styling. | [CHK-11-forgot-buttons.png](screenshots/CHK-11-forgot-buttons.png) |
| CHK-12 | Forgot Password | FR-03 | The Forgot Password page has no horizontal scrolling at a 360px viewport. | AI initial | Passed | scrollWidth = clientWidth = 360. | Playwright viewport 360px |
| CHK-13 | Profile | FR-04 | The Profile page has exactly one h1 and a logical heading hierarchy. | Review addition | **Failed** | 0 <h1> and two <h2> elements (“Hồ sơ của bạn”, “Lịch sử đơn hàng”). | [CHK-13-14-profile-headings-title.png](screenshots/CHK-13-14-profile-headings-title.png) |
| CHK-14 | Profile | FR-04 | The browser tab title is unique and describes the Profile page. | Review addition | **Failed** | document.title = "frontend-web" on /profile. | [CHK-13-14-profile-headings-title.png](screenshots/CHK-13-14-profile-headings-title.png) |
| CHK-15 | Profile | FR-04 | The order-history table remains usable at 360px without page-level horizontal scrolling. | Review addition | **Failed** | Page scrollWidth 399px vs clientWidth 360px (39px overflow); the 5-column table keeps its desktop width. | [CHK-15-profile-mobile-table.png](screenshots/CHK-15-profile-mobile-table.png) |
| CHK-16 | Profile | FR-04 | Profile text and order-status badges meet WCAG 2.2 AA contrast. | Review addition | **Failed** | axe-core: #fde047 on #2563eb = 3.92:1; white on #ef4444 = 3.76:1. | [CHK-16-profile-contrast.png](screenshots/CHK-16-profile-contrast.png) |
| CHK-65 | All auth screens | FR-01..04 | The layout remains usable when the document direction is RTL. | Review addition | **Failed** | With dir="rtl", physical Tailwind utilities keep the “Quên mật khẩu?” link right-aligned and the header unchanged; the layout is not mirrored. | [CHK-65-login-rtl.png](screenshots/CHK-65-login-rtl.png) |
| CHK-66 | All auth screens | FR-01..04 | Text remains legible when the operating system uses dark mode. | Review addition | Passed | No dark theme is implemented, but the explicit white card and black text stay legible under colorScheme=dark. | Playwright colorScheme=dark |
| CHK-67 | All auth screens | FR-01..04 | Content reflows at 200% zoom (640 CSS px) without horizontal scrolling. | Review addition | Passed | Login, Register and Forgot Password all report scrollWidth = clientWidth = 640. | Playwright 640px viewport |

## IA-02 — Forms

| ID | Screen | FR | Checklist item | Source | Result | Notes / failure reason | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-17 | Login | FR-02 | The email/username field uses an input type appropriate for email. | AI initial | **Failed** | type="text" and the label says “Username”, although the backend expects an email. | [CHK-17-18-19-login-fields.png](screenshots/CHK-17-18-19-login-fields.png) |
| CHK-18 | Login | FR-02 | The password field masks entered characters. | AI initial | **Failed** | type="text" — the password is visible on screen. | [CHK-17-18-19-login-fields.png](screenshots/CHK-17-18-19-login-fields.png) |
| CHK-19 | Login | FR-02 | Every input has a programmatically associated label. | Review addition | **Failed** | Labels have no for/id; axe-core reports 2 critical “label” violations. | [CHK-17-18-19-login-fields.png](screenshots/CHK-17-18-19-login-fields.png) |
| CHK-20 | Login | FR-02 | Required fields are enforced with native validation on empty submit. | AI initial | Passed | Both inputs have required; browser reports “Please fill out this field.” and focuses the first empty field. | Playwright native validation |
| CHK-21 | Register | FR-01 | The email field uses type=email and rejects malformed addresses. | AI initial | **Failed** | type="text"; “not-an-email-<timestamp>” was accepted and the app redirected to /login. | [CHK-21-register-invalid-email.png](screenshots/CHK-21-register-invalid-email.png) |
| CHK-22 | Register | FR-01 | The password field masks entered characters. | AI initial | Passed | type="password". | DOM inspection |
| CHK-23 | Register | FR-01 | The password rule text matches the implemented validation. | Review addition | **Failed** | Text promises “ký tự đặc biệt”, but the regex requires whitespace and rejects special characters; “Abcd1234!” is rejected. | [CHK-23-register-password-rule.png](screenshots/CHK-23-register-password-rule.png) |
| CHK-24 | Register | FR-01 | A confirm-password field prevents mistyped passwords. | AI initial | **Failed** | Only one password input is present. | [CHK-24-register-no-confirm.png](screenshots/CHK-24-register-no-confirm.png) |
| CHK-25 | Forgot Password | FR-03 | The email field uses type=email and validates the address format. | AI initial | **Failed** | type="text"; malformed addresses are only rejected by the backend after submission. | [CHK-25-forgot-email-type.png](screenshots/CHK-25-forgot-email-type.png) |
| CHK-26 | Forgot Password | FR-03 | The OTP field restricts input to four digits (inputmode/maxlength/pattern). | Review addition | **Failed** | type="text", maxlength=-1, no inputmode or pattern; arbitrary text is accepted. | [CHK-26-forgot-otp-input.png](screenshots/CHK-26-forgot-otp-input.png) |
| CHK-27 | Forgot Password | FR-03 | The new-password field masks entered characters. | AI initial | Passed | type="password". | DOM inspection |
| CHK-28 | Forgot Password | FR-03 | The reset form requires password confirmation. | AI initial | **Failed** | Step 2 has only one “Mật khẩu mới” input. | [CHK-28-forgot-no-confirm.png](screenshots/CHK-28-forgot-no-confirm.png) |
| CHK-29 | Profile | FR-04 | The email field is read-only and clearly marked as non-editable. | AI initial | Passed | disabled + label “Email (Không đổi)”. | DOM inspection |
| CHK-30 | Profile | FR-04 | The phone field uses tel inputmode and constrains its format. | AI initial | **Failed** | type="text"; no inputmode="tel", pattern, minlength or maxlength. | [CHK-30-profile-phone-inputmode.png](screenshots/CHK-30-profile-phone-inputmode.png) |
| CHK-31 | Profile | FR-04 | Phone validation feedback is inline and associated with the field. | Review addition | **Failed** | Uses alert(); the regex /^[1-9][0-9]{8,9}$/ rejects every 0-prefixed Vietnamese number, including the placeholder 0912345678; no inline error. | [CHK-31-profile-phone-alert.png](screenshots/CHK-31-profile-phone-alert.png) |
| CHK-32 | Profile | FR-04 | All Profile labels are programmatically associated with their inputs. | Review addition | **Failed** | All four labels lack for/id; axe-core reports critical label violations. | [CHK-32-profile-labels.png](screenshots/CHK-32-profile-labels.png) |

## IA-03 — Navigation

| ID | Screen | FR | Checklist item | Source | Result | Notes / failure reason | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-33 | Login | FR-02 | The global header is present and its links work on the Login page. | AI initial | Passed | Header contains EShop, Giỏ hàng, Đăng nhập, Đăng ký; all navigate correctly. | Playwright navigation |
| CHK-34 | Login | FR-02 | The Forgot Password link uses client-side routing and does not reload the document. | Review addition | **Failed** | Raw <a href="/forgot-password">; a window marker was lost after the click, proving a full reload. | [CHK-34-forgot-link-reload.png](screenshots/CHK-34-forgot-link-reload.png) |
| CHK-35 | Login | FR-02 | The “Đăng ký ngay” link navigates to /register. | AI initial | Passed | Navigates to the Register screen. | Playwright navigation |
| CHK-36 | Login | FR-02 | Keyboard tab order follows the visual order. | Review addition | **Failed** | The Sign In button has tabindex="1", so the first Tab from the page focuses it before email/password. | [CHK-36-login-tab-order.png](screenshots/CHK-36-login-tab-order.png) |
| CHK-37 | Register | FR-01 | Header navigation is present and consistent with Login. | AI initial | Passed | Same header links and styling. | DOM inspection |
| CHK-38 | Register | FR-01 | The “Đăng nhập” link navigates to /login. | AI initial | Passed | Navigates to Login. | Playwright navigation |
| CHK-39 | Register | FR-01 | Keyboard tab order follows the visual order. | AI initial | Passed | Header → name → email → password → Đăng Ký → login link. | Playwright keyboard test |
| CHK-40 | Register | FR-01 | Successful registration returns the user to Login. | AI initial | Passed | navigate('/login') after a successful POST. | Playwright registration flow |
| CHK-41 | Forgot Password | FR-03 | Going back to step 1 preserves the entered email. | AI initial | Passed | Email state is retained after “← Quay lại”. | Playwright step-back test |
| CHK-42 | Forgot Password | FR-03 | There is a way back to Login from Forgot Password. | AI initial | Passed | Header “Đăng nhập” link is available. | DOM inspection |
| CHK-43 | Forgot Password | FR-03 | Focus moves to the new step's first field after a step transition. | Review addition | **Failed** | After “Lấy mã OTP”, document.activeElement is BODY; focus is not moved to the OTP field or heading. | [CHK-43-forgot-focus.png](screenshots/CHK-43-forgot-focus.png) |
| CHK-44 | Forgot Password | FR-03 | Step 2 shows a step indicator (for example 2/2). | AI initial | **Failed** | No progress indicator or step count is shown. | [CHK-44-forgot-step-indicator.png](screenshots/CHK-44-forgot-step-indicator.png) |
| CHK-45 | Profile | FR-04 | Unauthenticated access to /profile redirects to Login with a return path. | Review addition | **Failed** | URL stays /profile and only “Vui lòng đăng nhập” is rendered; no redirect or return path. | [CHK-45-profile-unauth.png](screenshots/CHK-45-profile-unauth.png) |
| CHK-46 | Profile | FR-04 | The header shows the authenticated state and a working Profile link. | AI initial | Passed | “Chào, <name>” links to /profile; “Thoát” is present. | DOM inspection |
| CHK-47 | Profile | FR-04 | Logout returns the user to a public page. | AI initial | **Failed** | After “Thoát”, the URL remains /profile and the page shows “Vui lòng đăng nhập”. | [CHK-47-profile-logout.png](screenshots/CHK-47-profile-logout.png) |
| CHK-48 | Profile | FR-04 | The current page is indicated in navigation. | Review addition | **Failed** | No aria-current, active class or visual state identifies the current page. | [CHK-48-profile-active-nav.png](screenshots/CHK-48-profile-active-nav.png) |
| CHK-69 | Login | FR-02 | Authenticated users are redirected away from /login. | AI initial | **Failed** | A logged-in user still sees the Login form; the header shows the authenticated state at the same time. | [CHK-69-login-while-authenticated.png](screenshots/CHK-69-login-while-authenticated.png) |

## IA-04 — Feedback / state

| ID | Screen | FR | Checklist item | Source | Result | Notes / failure reason | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-49 | Login | FR-02 | The submit button shows a loading/disabled state while authenticating. | AI initial | **Failed** | During a delayed /api/login the button stays enabled with the label “Sign In”; no spinner or aria-busy. | [CHK-49-login-loading.png](screenshots/CHK-49-login-loading.png) |
| CHK-50 | Login | FR-02 | The login error is inline and announced to assistive technology. | AI initial | **Failed** | Error div has no role="alert" or aria-live; no field association. | [CHK-50-51-login-error.png](screenshots/CHK-50-51-login-error.png) |
| CHK-51 | Login | FR-02 | The login error text distinguishes wrong credentials, account lockout and network failure. | AI initial | **Failed** | Only “Đăng nhập thất bại. Vui lòng kiểm tra lại.” is shown for every failure. | [CHK-50-51-login-error.png](screenshots/CHK-50-51-login-error.png) |
| CHK-52 | Login | FR-02 | Successful login gives clear feedback and redirects. | AI initial | Passed | Redirects to / and the header changes to “Chào, <name>”. | Playwright login flow |
| CHK-53 | Register | FR-01 | Successful registration gives success feedback before redirecting. | AI initial | **Failed** | Redirects silently to /login; no success message. | [CHK-53-register-silent-success.png](screenshots/CHK-53-register-silent-success.png) |
| CHK-54 | Register | FR-01 | Duplicate-email registration is rejected with a human-readable message. | AI initial | **Failed** | Registering the same email twice both redirected to /login; no error (backend has no unique constraint). | [CHK-54-register-duplicate-email.png](screenshots/CHK-54-register-duplicate-email.png) |
| CHK-55 | Register | FR-01 | Server errors do not expose technical details. | Review addition | **Failed** | The catch block renders err.response.data.error directly; a simulated 500 produced “SQLITE_ERROR: no such column: name”. | [CHK-55-register-raw-error.png](screenshots/CHK-55-register-raw-error.png) |
| CHK-56 | Register | FR-01 | The submit button shows a loading/disabled state while registering. | AI initial | **Failed** | During a delayed /api/register the button stays enabled and keeps the label “Đăng Ký”. | [CHK-56-register-loading.png](screenshots/CHK-56-register-loading.png) |
| CHK-57 | Forgot Password | FR-03 | A successful OTP request is shown clearly. | AI initial | Passed | A green box and step 2 are shown after the request. | Playwright forgot-password flow |
| CHK-58 | Forgot Password | FR-03 | The OTP is not exposed in the UI. | Review addition | **Failed** | Step 2 shows “Mã OTP của bạn là: 2129” in a green success box. | [CHK-58-forgot-otp-exposed.png](screenshots/CHK-58-forgot-otp-exposed.png) |
| CHK-59 | Forgot Password | FR-03 | The invalid-email error is inline and non-blocking. | AI initial | **Failed** | Uses alert(“Lỗi: User not found”); no inline message, field highlight or live region. | [CHK-59-forgot-alert.png](screenshots/CHK-59-forgot-alert.png) |
| CHK-60 | Forgot Password | FR-03 | Reset success and failure feedback is clear. | AI initial | Passed | The success and failure outcomes are distinguishable (success alert + redirect to /login; failure alert). The blocking alert modality itself is reported in CHK-59 and CHK-61. | Playwright forgot-password flow |
| CHK-61 | Profile | FR-04 | Profile update success is shown inline and announced. | AI initial | **Failed** | Uses alert(“Cập nhật thành công!”); no inline message, aria-live region or focus/state update. | [CHK-61-profile-update-alert.png](screenshots/CHK-61-profile-update-alert.png) |
| CHK-62 | Profile | FR-04 | Order history shows a loading state. | AI initial | **Failed** | During a delayed /api/orders/my-orders the empty state “Bạn chưa có đơn hàng nào.” is already visible; no spinner/skeleton/aria-busy. | [CHK-62-profile-orders-loading.png](screenshots/CHK-62-profile-orders-loading.png) |
| CHK-63 | Profile | FR-04 | Order-history errors are distinguished from an empty list. | Review addition | **Failed** | A 500 response sets orders=[] and the UI says “Bạn chưa có đơn hàng nào.”; no error or retry. | [CHK-63-profile-orders-error.png](screenshots/CHK-63-profile-orders-error.png) |
| CHK-64 | Profile | FR-04 | The cancel-order action asks for confirmation before executing. | Review addition | **Failed** | “Hủy đơn” calls the API immediately; no “Bạn có chắc?” confirmation. It is also offered for a “Đang giao” order. | [CHK-64-profile-cancel.png](screenshots/CHK-64-profile-cancel.png) |
| CHK-68 | Profile | FR-04 | Order status is conveyed by text, not colour alone. | AI initial | Passed | statusLabel() maps each status to Vietnamese text next to the coloured badge. | DOM inspection |

## Execution notes

- The SUT was run locally: backend on `http://localhost:3000`, web frontend on `http://localhost:5173`.
- Functional behaviour was exercised with Playwright 1.65 (Chromium 158); DOM/ARIA facts were collected in the same run.
- Automated accessibility evidence was produced with axe-core 4.x. Contrast ratios are axe-core computed ratios, not eyeballed.
- Mobile checks used a 360×800 viewport; the 200% zoom check used a 640×800 viewport (equivalent CSS width).
- Screenshots contain a red annotation banner with the checklist ID and the observed defect. They are evidence, not a redesign proposal.
- A failed item is not automatically a bug: missing confirm-password fields and step indicators are design gaps; the bug list only includes reproducible defects.

## Evidence index

| Screenshot | Checklist IDs | What it shows |
| --- | --- | --- |
| [CHK-01-login-heading.png](screenshots/CHK-01-login-heading.png) | CHK-01 | Observed <h2>Đăng Ký</h2> on /login; expected a Login heading such as “Đăng nhập”. |
| [CHK-02-login-title.png](screenshots/CHK-02-login-title.png) | CHK-02 | document.title = "frontend-web" on /login; no page-specific title. |
| [CHK-06-register-title.png](screenshots/CHK-06-register-title.png) | CHK-06 | document.title = "frontend-web" on /register. |
| [CHK-07-register-contrast.png](screenshots/CHK-07-register-contrast.png) | CHK-07 | axe-core: helper text #9ca3af on #ffffff = 2.53:1; white on #ef4444 = 3.76:1. |
| [CHK-10-forgot-title.png](screenshots/CHK-10-forgot-title.png) | CHK-10 | document.title = "frontend-web" on /forgot-password. |
| [CHK-11-forgot-buttons.png](screenshots/CHK-11-forgot-buttons.png) | CHK-11 | “Đặt lại mật khẩu” and “← Quay lại” are both full-width green buttons with identical styling. |
| [CHK-13-14-profile-headings-title.png](screenshots/CHK-13-14-profile-headings-title.png) | CHK-13, CHK-14 | 0 <h1> and two <h2> elements (“Hồ sơ của bạn”, “Lịch sử đơn hàng”). |
| [CHK-15-profile-mobile-table.png](screenshots/CHK-15-profile-mobile-table.png) | CHK-15 | Page scrollWidth 399px vs clientWidth 360px (39px overflow); the 5-column table keeps its desktop width. |
| [CHK-16-profile-contrast.png](screenshots/CHK-16-profile-contrast.png) | CHK-16 | axe-core: #fde047 on #2563eb = 3.92:1; white on #ef4444 = 3.76:1. |
| [CHK-65-login-rtl.png](screenshots/CHK-65-login-rtl.png) | CHK-65 | With dir="rtl", physical Tailwind utilities keep the “Quên mật khẩu?” link right-aligned and the header unchanged; the layout is not mirrored. |
| [CHK-17-18-19-login-fields.png](screenshots/CHK-17-18-19-login-fields.png) | CHK-17, CHK-18, CHK-19 | type="text" and the label says “Username”, although the backend expects an email. |
| [CHK-21-register-invalid-email.png](screenshots/CHK-21-register-invalid-email.png) | CHK-21 | type="text"; “not-an-email-<timestamp>” was accepted and the app redirected to /login. |
| [CHK-23-register-password-rule.png](screenshots/CHK-23-register-password-rule.png) | CHK-23 | Text promises “ký tự đặc biệt”, but the regex requires whitespace and rejects special characters; “Abcd1234!” is rejected. |
| [CHK-24-register-no-confirm.png](screenshots/CHK-24-register-no-confirm.png) | CHK-24 | Only one password input is present. |
| [CHK-25-forgot-email-type.png](screenshots/CHK-25-forgot-email-type.png) | CHK-25 | type="text"; malformed addresses are only rejected by the backend after submission. |
| [CHK-26-forgot-otp-input.png](screenshots/CHK-26-forgot-otp-input.png) | CHK-26 | type="text", maxlength=-1, no inputmode or pattern; arbitrary text is accepted. |
| [CHK-28-forgot-no-confirm.png](screenshots/CHK-28-forgot-no-confirm.png) | CHK-28 | Step 2 has only one “Mật khẩu mới” input. |
| [CHK-30-profile-phone-inputmode.png](screenshots/CHK-30-profile-phone-inputmode.png) | CHK-30 | type="text"; no inputmode="tel", pattern, minlength or maxlength. |
| [CHK-31-profile-phone-alert.png](screenshots/CHK-31-profile-phone-alert.png) | CHK-31 | Uses alert(); the regex /^[1-9][0-9]{8,9}$/ rejects every 0-prefixed Vietnamese number, including the placeholder 0912345678; no inline error. |
| [CHK-32-profile-labels.png](screenshots/CHK-32-profile-labels.png) | CHK-32 | All four labels lack for/id; axe-core reports critical label violations. |
| [CHK-34-forgot-link-reload.png](screenshots/CHK-34-forgot-link-reload.png) | CHK-34 | Raw <a href="/forgot-password">; a window marker was lost after the click, proving a full reload. |
| [CHK-36-login-tab-order.png](screenshots/CHK-36-login-tab-order.png) | CHK-36 | The Sign In button has tabindex="1", so the first Tab from the page focuses it before email/password. |
| [CHK-43-forgot-focus.png](screenshots/CHK-43-forgot-focus.png) | CHK-43 | After “Lấy mã OTP”, document.activeElement is BODY; focus is not moved to the OTP field or heading. |
| [CHK-44-forgot-step-indicator.png](screenshots/CHK-44-forgot-step-indicator.png) | CHK-44 | No progress indicator or step count is shown. |
| [CHK-45-profile-unauth.png](screenshots/CHK-45-profile-unauth.png) | CHK-45 | URL stays /profile and only “Vui lòng đăng nhập” is rendered; no redirect or return path. |
| [CHK-47-profile-logout.png](screenshots/CHK-47-profile-logout.png) | CHK-47 | After “Thoát”, the URL remains /profile and the page shows “Vui lòng đăng nhập”. |
| [CHK-48-profile-active-nav.png](screenshots/CHK-48-profile-active-nav.png) | CHK-48 | No aria-current, active class or visual state identifies the current page. |
| [CHK-69-login-while-authenticated.png](screenshots/CHK-69-login-while-authenticated.png) | CHK-69 | A logged-in user still sees the Login form; the header shows the authenticated state at the same time. |
| [CHK-49-login-loading.png](screenshots/CHK-49-login-loading.png) | CHK-49 | During a delayed /api/login the button stays enabled with the label “Sign In”; no spinner or aria-busy. |
| [CHK-50-51-login-error.png](screenshots/CHK-50-51-login-error.png) | CHK-50, CHK-51 | Error div has no role="alert" or aria-live; no field association. |
| [CHK-53-register-silent-success.png](screenshots/CHK-53-register-silent-success.png) | CHK-53 | Redirects silently to /login; no success message. |
| [CHK-54-register-duplicate-email.png](screenshots/CHK-54-register-duplicate-email.png) | CHK-54 | Registering the same email twice both redirected to /login; no error (backend has no unique constraint). |
| [CHK-55-register-raw-error.png](screenshots/CHK-55-register-raw-error.png) | CHK-55 | The catch block renders err.response.data.error directly; a simulated 500 produced “SQLITE_ERROR: no such column: name”. |
| [CHK-56-register-loading.png](screenshots/CHK-56-register-loading.png) | CHK-56 | During a delayed /api/register the button stays enabled and keeps the label “Đăng Ký”. |
| [CHK-58-forgot-otp-exposed.png](screenshots/CHK-58-forgot-otp-exposed.png) | CHK-58 | Step 2 shows “Mã OTP của bạn là: 2129” in a green success box. |
| [CHK-59-forgot-alert.png](screenshots/CHK-59-forgot-alert.png) | CHK-59 | Uses alert(“Lỗi: User not found”); no inline message, field highlight or live region. |
| [CHK-61-profile-update-alert.png](screenshots/CHK-61-profile-update-alert.png) | CHK-61 | Uses alert(“Cập nhật thành công!”); no inline message, aria-live region or focus/state update. |
| [CHK-62-profile-orders-loading.png](screenshots/CHK-62-profile-orders-loading.png) | CHK-62 | During a delayed /api/orders/my-orders the empty state “Bạn chưa có đơn hàng nào.” is already visible; no spinner/skeleton/aria-busy. |
| [CHK-63-profile-orders-error.png](screenshots/CHK-63-profile-orders-error.png) | CHK-63 | A 500 response sets orders=[] and the UI says “Bạn chưa có đơn hàng nào.”; no error or retry. |
| [CHK-64-profile-cancel.png](screenshots/CHK-64-profile-cancel.png) | CHK-64 | “Hủy đơn” calls the API immediately; no “Bạn có chắc?” confirmation. It is also offered for a “Đang giao” order. |
