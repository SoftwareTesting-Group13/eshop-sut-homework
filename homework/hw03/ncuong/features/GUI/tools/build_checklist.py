#!/usr/bin/env python3
"""Build the HW03 GUI checklist artifacts (Markdown + Excel) from one source of truth."""
import json
import os
from collections import Counter, OrderedDict

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(BASE)

ITEMS = [
    # ---------------- IA-01 General UI standards ----------------
    dict(id="CHK-01", ia="IA-01", fr="FR-02", screen="Login",
         item="The page heading names the Login screen and matches the action.",
         source="AI initial", result="Failed",
         notes="Observed <h2>Đăng Ký</h2> on /login; expected a Login heading such as “Đăng nhập”.",
         evidence="screenshots/CHK-01-login-heading.png", bug="BUG-GUI-01"),
    dict(id="CHK-02", ia="IA-01", fr="FR-02", screen="Login",
         item="The browser tab title is unique and describes the Login page.",
         source="Review addition", result="Failed",
         notes="document.title = \"frontend-web\" on /login; no page-specific title.",
         evidence="screenshots/CHK-02-login-title.png", bug="BUG-GUI-02"),
    dict(id="CHK-03", ia="IA-01", fr="FR-02", screen="Login",
         item="The auth card uses the same alignment, spacing and typography as Register and Forgot Password.",
         source="AI initial", result="Passed",
         notes="All three auth screens use max-w-md mx-auto mt-10 bg-white p-8 border rounded shadow-sm.",
         evidence="DOM inspection", bug=""),
    dict(id="CHK-04", ia="IA-01", fr="FR-02", screen="Login",
         item="The Login page has no horizontal scrolling at a 360px viewport.",
         source="AI initial", result="Passed",
         notes="scrollWidth = clientWidth = 360.",
         evidence="Playwright viewport 360px", bug=""),
    dict(id="CHK-05", ia="IA-01", fr="FR-01", screen="Register",
         item="The page heading names the Register screen.",
         source="AI initial", result="Passed",
         notes="Observed <h2>Đăng Ký Tài Khoản</h2>.",
         evidence="DOM inspection", bug=""),
    dict(id="CHK-06", ia="IA-01", fr="FR-01", screen="Register",
         item="The browser tab title is unique and describes the Register page.",
         source="Review addition", result="Failed",
         notes="document.title = \"frontend-web\" on /register.",
         evidence="screenshots/CHK-06-register-title.png", bug="BUG-GUI-02"),
    dict(id="CHK-07", ia="IA-01", fr="FR-01", screen="Register",
         item="Helper text and the primary button meet WCAG 2.2 AA contrast (4.5:1 normal text).",
         source="Review addition", result="Failed",
         notes="axe-core: helper text #9ca3af on #ffffff = 2.53:1; white on #ef4444 = 3.76:1.",
         evidence="screenshots/CHK-07-register-contrast.png", bug="BUG-GUI-03"),
    dict(id="CHK-08", ia="IA-01", fr="FR-01", screen="Register",
         item="The Register page has no horizontal scrolling at a 360px viewport.",
         source="AI initial", result="Passed",
         notes="scrollWidth = clientWidth = 360.",
         evidence="Playwright viewport 360px", bug=""),
    dict(id="CHK-09", ia="IA-01", fr="FR-03", screen="Forgot Password",
         item="The page heading names the Forgot Password screen.",
         source="AI initial", result="Passed",
         notes="Observed <h2>Quên Mật Khẩu</h2>.",
         evidence="DOM inspection", bug=""),
    dict(id="CHK-10", ia="IA-01", fr="FR-03", screen="Forgot Password",
         item="The browser tab title is unique and describes the Forgot Password page.",
         source="Review addition", result="Failed",
         notes="document.title = \"frontend-web\" on /forgot-password.",
         evidence="screenshots/CHK-10-forgot-title.png", bug="BUG-GUI-02"),
    dict(id="CHK-11", ia="IA-01", fr="FR-03", screen="Forgot Password",
         item="Step 2 primary and secondary actions are visually distinguishable.",
         source="AI initial", result="Failed",
         notes="“Đặt lại mật khẩu” and “← Quay lại” are both full-width green buttons with identical styling.",
         evidence="screenshots/CHK-11-forgot-buttons.png", bug="BUG-GUI-04"),
    dict(id="CHK-12", ia="IA-01", fr="FR-03", screen="Forgot Password",
         item="The Forgot Password page has no horizontal scrolling at a 360px viewport.",
         source="AI initial", result="Passed",
         notes="scrollWidth = clientWidth = 360.",
         evidence="Playwright viewport 360px", bug=""),
    dict(id="CHK-13", ia="IA-01", fr="FR-04", screen="Profile",
         item="The Profile page has exactly one h1 and a logical heading hierarchy.",
         source="Review addition", result="Failed",
         notes="0 <h1> and two <h2> elements (“Hồ sơ của bạn”, “Lịch sử đơn hàng”).",
         evidence="screenshots/CHK-13-14-profile-headings-title.png", bug="BUG-GUI-05"),
    dict(id="CHK-14", ia="IA-01", fr="FR-04", screen="Profile",
         item="The browser tab title is unique and describes the Profile page.",
         source="Review addition", result="Failed",
         notes="document.title = \"frontend-web\" on /profile.",
         evidence="screenshots/CHK-13-14-profile-headings-title.png", bug="BUG-GUI-02"),
    dict(id="CHK-15", ia="IA-01", fr="FR-04", screen="Profile",
         item="The order-history table remains usable at 360px without page-level horizontal scrolling.",
         source="Review addition", result="Failed",
         notes="Page scrollWidth 399px vs clientWidth 360px (39px overflow); the 5-column table keeps its desktop width.",
         evidence="screenshots/CHK-15-profile-mobile-table.png", bug="BUG-GUI-06"),
    dict(id="CHK-16", ia="IA-01", fr="FR-04", screen="Profile",
         item="Profile text and order-status badges meet WCAG 2.2 AA contrast.",
         source="Review addition", result="Failed",
         notes="axe-core: #fde047 on #2563eb = 3.92:1; white on #ef4444 = 3.76:1.",
         evidence="screenshots/CHK-16-profile-contrast.png", bug="BUG-GUI-03"),
    dict(id="CHK-65", ia="IA-01", fr="FR-01..04", screen="All auth screens",
         item="The layout remains usable when the document direction is RTL.",
         source="Review addition", result="Failed",
         notes="With dir=\"rtl\", physical Tailwind utilities keep the “Quên mật khẩu?” link right-aligned and the header unchanged; the layout is not mirrored.",
         evidence="screenshots/CHK-65-login-rtl.png", bug="BUG-GUI-07"),
    dict(id="CHK-66", ia="IA-01", fr="FR-01..04", screen="All auth screens",
         item="Text remains legible when the operating system uses dark mode.",
         source="Review addition", result="Passed",
         notes="No dark theme is implemented, but the explicit white card and black text stay legible under colorScheme=dark.",
         evidence="Playwright colorScheme=dark", bug=""),
    dict(id="CHK-67", ia="IA-01", fr="FR-01..04", screen="All auth screens",
         item="Content reflows at 200% zoom (640 CSS px) without horizontal scrolling.",
         source="Review addition", result="Passed",
         notes="Login, Register and Forgot Password all report scrollWidth = clientWidth = 640.",
         evidence="Playwright 640px viewport", bug=""),

    # ---------------- IA-02 Forms ----------------
    dict(id="CHK-17", ia="IA-02", fr="FR-02", screen="Login",
         item="The email/username field uses an input type appropriate for email.",
         source="AI initial", result="Failed",
         notes="type=\"text\" and the label says “Username”, although the backend expects an email.",
         evidence="screenshots/CHK-17-18-19-login-fields.png", bug="BUG-GUI-08"),
    dict(id="CHK-18", ia="IA-02", fr="FR-02", screen="Login",
         item="The password field masks entered characters.",
         source="AI initial", result="Failed",
         notes="type=\"text\" — the password is visible on screen.",
         evidence="screenshots/CHK-17-18-19-login-fields.png", bug="BUG-GUI-08"),
    dict(id="CHK-19", ia="IA-02", fr="FR-02", screen="Login",
         item="Every input has a programmatically associated label.",
         source="Review addition", result="Failed",
         notes="Labels have no for/id; axe-core reports 2 critical “label” violations.",
         evidence="screenshots/CHK-17-18-19-login-fields.png", bug="BUG-GUI-09"),
    dict(id="CHK-20", ia="IA-02", fr="FR-02", screen="Login",
         item="Required fields are enforced with native validation on empty submit.",
         source="AI initial", result="Passed",
         notes="Both inputs have required; browser reports “Please fill out this field.” and focuses the first empty field.",
         evidence="Playwright native validation", bug=""),
    dict(id="CHK-21", ia="IA-02", fr="FR-01", screen="Register",
         item="The email field uses type=email and rejects malformed addresses.",
         source="AI initial", result="Failed",
         notes="type=\"text\"; “not-an-email-<timestamp>” was accepted and the app redirected to /login.",
         evidence="screenshots/CHK-21-register-invalid-email.png", bug="BUG-GUI-10"),
    dict(id="CHK-22", ia="IA-02", fr="FR-01", screen="Register",
         item="The password field masks entered characters.",
         source="AI initial", result="Passed",
         notes="type=\"password\".",
         evidence="DOM inspection", bug=""),
    dict(id="CHK-23", ia="IA-02", fr="FR-01", screen="Register",
         item="The password rule text matches the implemented validation.",
         source="Review addition", result="Failed",
         notes="Text promises “ký tự đặc biệt”, but the regex requires whitespace and rejects special characters; “Abcd1234!” is rejected.",
         evidence="screenshots/CHK-23-register-password-rule.png", bug="BUG-GUI-11"),
    dict(id="CHK-24", ia="IA-02", fr="FR-01", screen="Register",
         item="A confirm-password field prevents mistyped passwords.",
         source="AI initial", result="Failed",
         notes="Only one password input is present.",
         evidence="screenshots/CHK-24-register-no-confirm.png", bug="BUG-GUI-12"),
    dict(id="CHK-25", ia="IA-02", fr="FR-03", screen="Forgot Password",
         item="The email field uses type=email and validates the address format.",
         source="AI initial", result="Failed",
         notes="type=\"text\"; malformed addresses are only rejected by the backend after submission.",
         evidence="screenshots/CHK-25-forgot-email-type.png", bug="BUG-GUI-10"),
    dict(id="CHK-26", ia="IA-02", fr="FR-03", screen="Forgot Password",
         item="The OTP field restricts input to four digits (inputmode/maxlength/pattern).",
         source="Review addition", result="Failed",
         notes="type=\"text\", maxlength=-1, no inputmode or pattern; arbitrary text is accepted.",
         evidence="screenshots/CHK-26-forgot-otp-input.png", bug="BUG-GUI-13"),
    dict(id="CHK-27", ia="IA-02", fr="FR-03", screen="Forgot Password",
         item="The new-password field masks entered characters.",
         source="AI initial", result="Passed",
         notes="type=\"password\".",
         evidence="DOM inspection", bug=""),
    dict(id="CHK-28", ia="IA-02", fr="FR-03", screen="Forgot Password",
         item="The reset form requires password confirmation.",
         source="AI initial", result="Failed",
         notes="Step 2 has only one “Mật khẩu mới” input.",
         evidence="screenshots/CHK-28-forgot-no-confirm.png", bug="BUG-GUI-12"),
    dict(id="CHK-29", ia="IA-02", fr="FR-04", screen="Profile",
         item="The email field is read-only and clearly marked as non-editable.",
         source="AI initial", result="Passed",
         notes="disabled + label “Email (Không đổi)”.",
         evidence="DOM inspection", bug=""),
    dict(id="CHK-30", ia="IA-02", fr="FR-04", screen="Profile",
         item="The phone field uses tel inputmode and constrains its format.",
         source="AI initial", result="Failed",
         notes="type=\"text\"; no inputmode=\"tel\", pattern, minlength or maxlength.",
         evidence="screenshots/CHK-30-profile-phone-inputmode.png", bug="BUG-GUI-14"),
    dict(id="CHK-31", ia="IA-02", fr="FR-04", screen="Profile",
         item="Phone validation feedback is inline and associated with the field.",
         source="Review addition", result="Failed",
         notes="Uses alert(); the regex /^[1-9][0-9]{8,9}$/ rejects every 0-prefixed Vietnamese number, including the placeholder 0912345678; no inline error.",
         evidence="screenshots/CHK-31-profile-phone-alert.png", bug="BUG-GUI-14"),
    dict(id="CHK-32", ia="IA-02", fr="FR-04", screen="Profile",
         item="All Profile labels are programmatically associated with their inputs.",
         source="Review addition", result="Failed",
         notes="All four labels lack for/id; axe-core reports critical label violations.",
         evidence="screenshots/CHK-32-profile-labels.png", bug="BUG-GUI-09"),

    # ---------------- IA-03 Navigation ----------------
    dict(id="CHK-33", ia="IA-03", fr="FR-02", screen="Login",
         item="The global header is present and its links work on the Login page.",
         source="AI initial", result="Passed",
         notes="Header contains EShop, Giỏ hàng, Đăng nhập, Đăng ký; all navigate correctly.",
         evidence="Playwright navigation", bug=""),
    dict(id="CHK-34", ia="IA-03", fr="FR-02", screen="Login",
         item="The Forgot Password link uses client-side routing and does not reload the document.",
         source="Review addition", result="Failed",
         notes="Raw <a href=\"/forgot-password\">; a window marker was lost after the click, proving a full reload.",
         evidence="screenshots/CHK-34-forgot-link-reload.png", bug="BUG-GUI-15"),
    dict(id="CHK-35", ia="IA-03", fr="FR-02", screen="Login",
         item="The “Đăng ký ngay” link navigates to /register.",
         source="AI initial", result="Passed",
         notes="Navigates to the Register screen.",
         evidence="Playwright navigation", bug=""),
    dict(id="CHK-36", ia="IA-03", fr="FR-02", screen="Login",
         item="Keyboard tab order follows the visual order.",
         source="Review addition", result="Failed",
         notes="The Sign In button has tabindex=\"1\", so the first Tab from the page focuses it before email/password.",
         evidence="screenshots/CHK-36-login-tab-order.png", bug="BUG-GUI-16"),
    dict(id="CHK-37", ia="IA-03", fr="FR-01", screen="Register",
         item="Header navigation is present and consistent with Login.",
         source="AI initial", result="Passed",
         notes="Same header links and styling.",
         evidence="DOM inspection", bug=""),
    dict(id="CHK-38", ia="IA-03", fr="FR-01", screen="Register",
         item="The “Đăng nhập” link navigates to /login.",
         source="AI initial", result="Passed",
         notes="Navigates to Login.",
         evidence="Playwright navigation", bug=""),
    dict(id="CHK-39", ia="IA-03", fr="FR-01", screen="Register",
         item="Keyboard tab order follows the visual order.",
         source="AI initial", result="Passed",
         notes="Header → name → email → password → Đăng Ký → login link.",
         evidence="Playwright keyboard test", bug=""),
    dict(id="CHK-40", ia="IA-03", fr="FR-01", screen="Register",
         item="Successful registration returns the user to Login.",
         source="AI initial", result="Passed",
         notes="navigate('/login') after a successful POST.",
         evidence="Playwright registration flow", bug=""),
    dict(id="CHK-41", ia="IA-03", fr="FR-03", screen="Forgot Password",
         item="Going back to step 1 preserves the entered email.",
         source="AI initial", result="Passed",
         notes="Email state is retained after “← Quay lại”.",
         evidence="Playwright step-back test", bug=""),
    dict(id="CHK-42", ia="IA-03", fr="FR-03", screen="Forgot Password",
         item="There is a way back to Login from Forgot Password.",
         source="AI initial", result="Passed",
         notes="Header “Đăng nhập” link is available.",
         evidence="DOM inspection", bug=""),
    dict(id="CHK-43", ia="IA-03", fr="FR-03", screen="Forgot Password",
         item="Focus moves to the new step's first field after a step transition.",
         source="Review addition", result="Failed",
         notes="After “Lấy mã OTP”, document.activeElement is BODY; focus is not moved to the OTP field or heading.",
         evidence="screenshots/CHK-43-forgot-focus.png", bug="BUG-GUI-17"),
    dict(id="CHK-44", ia="IA-03", fr="FR-03", screen="Forgot Password",
         item="Step 2 shows a step indicator (for example 2/2).",
         source="AI initial", result="Failed",
         notes="No progress indicator or step count is shown.",
         evidence="screenshots/CHK-44-forgot-step-indicator.png", bug="BUG-GUI-13"),
    dict(id="CHK-45", ia="IA-03", fr="FR-04", screen="Profile",
         item="Unauthenticated access to /profile redirects to Login with a return path.",
         source="Review addition", result="Failed",
         notes="URL stays /profile and only “Vui lòng đăng nhập” is rendered; no redirect or return path.",
         evidence="screenshots/CHK-45-profile-unauth.png", bug="BUG-GUI-18"),
    dict(id="CHK-46", ia="IA-03", fr="FR-04", screen="Profile",
         item="The header shows the authenticated state and a working Profile link.",
         source="AI initial", result="Passed",
         notes="“Chào, <name>” links to /profile; “Thoát” is present.",
         evidence="DOM inspection", bug=""),
    dict(id="CHK-47", ia="IA-03", fr="FR-04", screen="Profile",
         item="Logout returns the user to a public page.",
         source="AI initial", result="Failed",
         notes="After “Thoát”, the URL remains /profile and the page shows “Vui lòng đăng nhập”.",
         evidence="screenshots/CHK-47-profile-logout.png", bug="BUG-GUI-18"),
    dict(id="CHK-48", ia="IA-03", fr="FR-04", screen="Profile",
         item="The current page is indicated in navigation.",
         source="Review addition", result="Failed",
         notes="No aria-current, active class or visual state identifies the current page.",
         evidence="screenshots/CHK-48-profile-active-nav.png", bug="BUG-GUI-19"),
    dict(id="CHK-69", ia="IA-03", fr="FR-02", screen="Login",
         item="Authenticated users are redirected away from /login.",
         source="AI initial", result="Failed",
         notes="A logged-in user still sees the Login form; the header shows the authenticated state at the same time.",
         evidence="screenshots/CHK-69-login-while-authenticated.png", bug="BUG-GUI-18"),

    # ---------------- IA-04 Feedback / state ----------------
    dict(id="CHK-49", ia="IA-04", fr="FR-02", screen="Login",
         item="The submit button shows a loading/disabled state while authenticating.",
         source="AI initial", result="Failed",
         notes="During a delayed /api/login the button stays enabled with the label “Sign In”; no spinner or aria-busy.",
         evidence="screenshots/CHK-49-login-loading.png", bug="BUG-GUI-20"),
    dict(id="CHK-50", ia="IA-04", fr="FR-02", screen="Login",
         item="The login error is inline and announced to assistive technology.",
         source="AI initial", result="Failed",
         notes="Error div has no role=\"alert\" or aria-live; no field association.",
         evidence="screenshots/CHK-50-51-login-error.png", bug="BUG-GUI-21"),
    dict(id="CHK-51", ia="IA-04", fr="FR-02", screen="Login",
         item="The login error text distinguishes wrong credentials, account lockout and network failure.",
         source="AI initial", result="Failed",
         notes="Only “Đăng nhập thất bại. Vui lòng kiểm tra lại.” is shown for every failure.",
         evidence="screenshots/CHK-50-51-login-error.png", bug="BUG-GUI-21"),
    dict(id="CHK-52", ia="IA-04", fr="FR-02", screen="Login",
         item="Successful login gives clear feedback and redirects.",
         source="AI initial", result="Passed",
         notes="Redirects to / and the header changes to “Chào, <name>”.",
         evidence="Playwright login flow", bug=""),
    dict(id="CHK-53", ia="IA-04", fr="FR-01", screen="Register",
         item="Successful registration gives success feedback before redirecting.",
         source="AI initial", result="Failed",
         notes="Redirects silently to /login; no success message.",
         evidence="screenshots/CHK-53-register-silent-success.png", bug="BUG-GUI-22"),
    dict(id="CHK-54", ia="IA-04", fr="FR-01", screen="Register",
         item="Duplicate-email registration is rejected with a human-readable message.",
         source="AI initial", result="Failed",
         notes="Registering the same email twice both redirected to /login; no error (backend has no unique constraint).",
         evidence="screenshots/CHK-54-register-duplicate-email.png", bug="BUG-GUI-10"),
    dict(id="CHK-55", ia="IA-04", fr="FR-01", screen="Register",
         item="Server errors do not expose technical details.",
         source="Review addition", result="Failed",
         notes="The catch block renders err.response.data.error directly; a simulated 500 produced “SQLITE_ERROR: no such column: name”.",
         evidence="screenshots/CHK-55-register-raw-error.png", bug="BUG-GUI-23"),
    dict(id="CHK-56", ia="IA-04", fr="FR-01", screen="Register",
         item="The submit button shows a loading/disabled state while registering.",
         source="AI initial", result="Failed",
         notes="During a delayed /api/register the button stays enabled and keeps the label “Đăng Ký”.",
         evidence="screenshots/CHK-56-register-loading.png", bug="BUG-GUI-20"),
    dict(id="CHK-57", ia="IA-04", fr="FR-03", screen="Forgot Password",
         item="A successful OTP request is shown clearly.",
         source="AI initial", result="Passed",
         notes="A green box and step 2 are shown after the request.",
         evidence="Playwright forgot-password flow", bug=""),
    dict(id="CHK-58", ia="IA-04", fr="FR-03", screen="Forgot Password",
         item="The OTP is not exposed in the UI.",
         source="Review addition", result="Failed",
         notes="Step 2 shows “Mã OTP của bạn là: 2129” in a green success box.",
         evidence="screenshots/CHK-58-forgot-otp-exposed.png", bug="BUG-GUI-24"),
    dict(id="CHK-59", ia="IA-04", fr="FR-03", screen="Forgot Password",
         item="The invalid-email error is inline and non-blocking.",
         source="AI initial", result="Failed",
         notes="Uses alert(“Lỗi: User not found”); no inline message, field highlight or live region.",
         evidence="screenshots/CHK-59-forgot-alert.png", bug="BUG-GUI-21"),
    dict(id="CHK-60", ia="IA-04", fr="FR-03", screen="Forgot Password",
         item="Reset success and failure feedback is clear.",
         source="AI initial", result="Passed",
         notes="The success and failure outcomes are distinguishable (success alert + redirect to /login; failure alert). The blocking alert modality itself is reported in CHK-59 and CHK-61.",
         evidence="Playwright forgot-password flow", bug=""),
    dict(id="CHK-61", ia="IA-04", fr="FR-04", screen="Profile",
         item="Profile update success is shown inline and announced.",
         source="AI initial", result="Failed",
         notes="Uses alert(“Cập nhật thành công!”); no inline message, aria-live region or focus/state update.",
         evidence="screenshots/CHK-61-profile-update-alert.png", bug="BUG-GUI-21"),
    dict(id="CHK-62", ia="IA-04", fr="FR-04", screen="Profile",
         item="Order history shows a loading state.",
         source="AI initial", result="Failed",
         notes="During a delayed /api/orders/my-orders the empty state “Bạn chưa có đơn hàng nào.” is already visible; no spinner/skeleton/aria-busy.",
         evidence="screenshots/CHK-62-profile-orders-loading.png", bug="BUG-GUI-25"),
    dict(id="CHK-63", ia="IA-04", fr="FR-04", screen="Profile",
         item="Order-history errors are distinguished from an empty list.",
         source="Review addition", result="Failed",
         notes="A 500 response sets orders=[] and the UI says “Bạn chưa có đơn hàng nào.”; no error or retry.",
         evidence="screenshots/CHK-63-profile-orders-error.png", bug="BUG-GUI-25"),
    dict(id="CHK-64", ia="IA-04", fr="FR-04", screen="Profile",
         item="The cancel-order action asks for confirmation before executing.",
         source="Review addition", result="Failed",
         notes="“Hủy đơn” calls the API immediately; no “Bạn có chắc?” confirmation. It is also offered for a “Đang giao” order.",
         evidence="screenshots/CHK-64-profile-cancel.png", bug="BUG-GUI-26"),
    dict(id="CHK-68", ia="IA-04", fr="FR-04", screen="Profile",
         item="Order status is conveyed by text, not colour alone.",
         source="AI initial", result="Passed",
         notes="statusLabel() maps each status to Vietnamese text next to the coloured badge.",
         evidence="DOM inspection", bug=""),
]

# Sanity checks
ids = [i["id"] for i in ITEMS]
assert len(ids) == len(set(ids)), "duplicate IDs"
assert len(ITEMS) > 40, len(ITEMS)

# Derived summary
summary = OrderedDict()
for ia in ["IA-01", "IA-02", "IA-03", "IA-04"]:
    rows = [i for i in ITEMS if i["ia"] == ia]
    summary[ia] = {
        "total": len(rows),
        "passed": sum(1 for i in rows if i["result"] == "Passed"),
        "failed": sum(1 for i in rows if i["result"] == "Failed"),
        "screens": sorted({i["screen"] for i in rows}),
    }

source_counts = Counter(i["source"] for i in ITEMS)
result_counts = Counter(i["result"] for i in ITEMS)
bug_ids = sorted({i["bug"] for i in ITEMS if i["bug"]})

# Write JSON source
with open(os.path.join(OUT, "checklist.json"), "w", encoding="utf-8") as f:
    json.dump({"items": ITEMS, "summary": summary,
               "source_counts": source_counts, "result_counts": result_counts,
               "bugs": bug_ids}, f, ensure_ascii=False, indent=2)

# ---------------- Markdown: full checklist ----------------
lines = []
lines.append("# GUI Checklist — Login, Register, Forgot Password, Profile\n")
lines.append("**SUT:** EShop (http://localhost:5173) · **FRs:** FR-01, FR-02, FR-03, FR-04 · **Interface aspects:** IA-01…IA-04\n")
lines.append("**Execution date:** 2026-11-07 · **Browser:** Chromium 158 (Playwright 1.65) · **Viewport:** 1280×900; mobile checks at 360×800 and 640×800.\n")
lines.append("\n## Summary\n")
lines.append("| Interface aspect | Items | Passed | Failed |")
lines.append("| --- | ---: | ---: | ---: |")
for ia, s in summary.items():
    lines.append(f"| {ia} | {s['total']} | {s['passed']} | {s['failed']} |")
lines.append(f"| **Total** | **{len(ITEMS)}** | **{result_counts['Passed']}** | **{result_counts['Failed']}** |")
lines.append(f"\nSource split: **{source_counts['AI initial']} AI-initial items** + **{source_counts['Review addition']} review additions**. Bug IDs: {', '.join(bug_ids)}.\n")

for ia in ["IA-01", "IA-02", "IA-03", "IA-04"]:
    titles = {"IA-01": "IA-01 — General UI standards", "IA-02": "IA-02 — Forms",
              "IA-03": "IA-03 — Navigation", "IA-04": "IA-04 — Feedback / state"}
    lines.append(f"\n## {titles[ia]}\n")
    lines.append("| ID | Screen | FR | Checklist item | Source | Result | Notes / failure reason | Evidence |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for i in ITEMS:
        if i["ia"] != ia:
            continue
        res = "**Failed**" if i["result"] == "Failed" else "Passed"
        notes = i["notes"].replace("|", "\\|")
        ev = f"[{os.path.basename(i['evidence'])}]({i['evidence']})" if i["evidence"].startswith("screenshots/") else i["evidence"]
        lines.append(f"| {i['id']} | {i['screen']} | {i['fr']} | {i['item']} | {i['source']} | {res} | {notes} | {ev} |")

lines.append("\n## Execution notes\n")
lines.append("- The SUT was run locally: backend on `http://localhost:3000`, web frontend on `http://localhost:5173`.")
lines.append("- Functional behaviour was exercised with Playwright 1.65 (Chromium 158); DOM/ARIA facts were collected in the same run.")
lines.append("- Automated accessibility evidence was produced with axe-core 4.x. Contrast ratios are axe-core computed ratios, not eyeballed.")
lines.append("- Mobile checks used a 360×800 viewport; the 200% zoom check used a 640×800 viewport (equivalent CSS width).")
lines.append("- Screenshots contain a red annotation banner with the checklist ID and the observed defect. They are evidence, not a redesign proposal.")
lines.append("- A failed item is not automatically a bug: missing confirm-password fields and step indicators are design gaps; the bug list only includes reproducible defects.")
lines.append("\n## Evidence index\n")
lines.append("| Screenshot | Checklist IDs | What it shows |")
lines.append("| --- | --- | --- |")
seen = set()
for i in ITEMS:
    if not i["evidence"].startswith("screenshots/"):
        continue
    if i["evidence"] in seen:
        continue
    seen.add(i["evidence"])
    related = [x["id"] for x in ITEMS if x["evidence"] == i["evidence"]]
    lines.append(f"| [{os.path.basename(i['evidence'])}]({i['evidence']}) | {', '.join(related)} | {i['notes'].replace('|', '\\|')} |")

with open(os.path.join(OUT, "checklist.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

# ---------------- Markdown: AI initial set ----------------
init = [i for i in ITEMS if i["source"] == "AI initial"]
lines = ["# AI-generated initial checklist (before human review)\n",
         f"Generated with the `ui-checklist-generator` skill (8 categories: layout, typography, colour, interaction, responsiveness, accessibility, product states, polish) expanded across four screens. **{len(init)} items.**\n",
         "This is the raw initial set kept for the audit trail. It was reviewed afterwards; the review additions and their rationale are in `review-additions.md`.\n",
         "| ID | IA | Screen | FR | Item |", "| --- | --- | --- | --- | --- |"]
for i in init:
    lines.append(f"| {i['id']} | {i['ia']} | {i['screen']} | {i['fr']} | {i['item']} |")
with open(os.path.join(OUT, "ai-initial-checklist.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

# ---------------- Markdown: review additions ----------------
add = [i for i in ITEMS if i["source"] == "Review addition"]
rationale = {
    "CHK-02": "The AI checklist focused on the visible page and ignored browser chrome (tab title).",
    "CHK-06": "Same blind spot as CHK-02: document.title is outside the rendered body.",
    "CHK-10": "Same blind spot as CHK-02: document.title is outside the rendered body.",
    "CHK-14": "Same blind spot as CHK-02: document.title is outside the rendered body.",
    "CHK-07": "The AI item said “sufficient contrast” but did not compute ratios; axe-core found two failures.",
    "CHK-13": "The AI item treated headings as typography, not as a semantic outline; it did not check h1/h2 structure.",
    "CHK-15": "The AI responsiveness item was generic (“mobile usable”) and did not test a data table with real columns.",
    "CHK-16": "Same as CHK-07: the AI did not compute contrast for status badges and header text.",
    "CHK-19": "The AI checked that labels are visible, not that they are programmatically associated (for/id or aria-label).",
    "CHK-21": "The AI forms checklist mentioned “email validation” but not the HTML input type or a malformed-email test.",
    "CHK-23": "The AI did not compare the displayed password rule with the actual regex; the contradiction only appears when both are read together.",
    "CHK-26": "The AI missed the domain-specific OTP constraints (4 digits, numeric keypad, maxlength).",
    "CHK-31": "The AI checked that a phone error exists, not where/how it is shown or whether the regex accepts real Vietnamese numbers.",
    "CHK-32": "Same as CHK-19: visible labels were counted as sufficient.",
    "CHK-34": "The AI did not distinguish a raw <a href> reload from React Router navigation.",
    "CHK-36": "The AI did not execute a keyboard-only tab-order test; tabindex=\"1\" is invisible in a screenshot.",
    "CHK-43": "The AI missed dynamic focus management after a client-side step transition.",
    "CHK-45": "The AI did not test the unauthenticated route guard or the return path.",
    "CHK-48": "The AI did not check current-page indication (aria-current/active state).",
    "CHK-55": "The AI did not test a server-error path and therefore missed raw error leakage.",
    "CHK-58": "The AI treated the OTP message as helpful feedback and did not flag it as a security/privacy defect.",
    "CHK-63": "The AI checked the empty state but not whether an error is distinguishable from an empty list.",
    "CHK-64": "The AI missed destructive-action confirmation and the shipping-order edge case.",
    "CHK-65": "The AI checklist had no RTL item; the model defaulted to LTR assumptions.",
    "CHK-66": "The AI checklist had no dark-mode item; the model assumed the light theme is the only theme.",
    "CHK-67": "The AI checklist had no 200% zoom/reflow item (WCAG 1.4.10).",
}
lines = ["# Review additions — items the AI missed\n",
         f"The initial AI set had **{len(init)} items**. During the critical review, **{len(add)} items** were added. Each row states why the initial AI pass missed it.\n",
         "| ID | IA | Screen | Added item | Why the AI missed it |", "| --- | --- | --- | --- | --- |"]
for i in add:
    lines.append(f"| {i['id']} | {i['ia']} | {i['screen']} | {i['item']} | {rationale.get(i['id'], 'See report.')} |")
with open(os.path.join(OUT, "review-additions.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

# ---------------- Excel ----------------
try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    ws.title = "Checklist"
    headers = ["ID", "IA", "FR", "Screen", "Checklist item", "Source", "Result", "Notes / failure reason", "Evidence", "Bug ID"]
    ws.append(headers)
    header_fill = PatternFill("solid", fgColor="1F4E78")
    header_font = Font(bold=True, color="FFFFFF")
    thin = Side(style="thin", color="BFBFBF")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border
    pass_fill = PatternFill("solid", fgColor="E2EFDA")
    fail_fill = PatternFill("solid", fgColor="FCE4D6")
    for i in ITEMS:
        ws.append([i["id"], i["ia"], i["fr"], i["screen"], i["item"], i["source"], i["result"], i["notes"], i["evidence"], i["bug"]])
        r = ws.max_row
        for c in range(1, len(headers) + 1):
            cell = ws.cell(row=r, column=c)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = border
        ws.cell(row=r, column=7).fill = pass_fill if i["result"] == "Passed" else fail_fill
        ws.cell(row=r, column=7).font = Font(bold=True)
    widths = [9, 8, 9, 18, 58, 15, 10, 55, 46, 14]
    for idx, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(idx)].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:J{ws.max_row}"
    ws.row_dimensions[1].height = 28

    ws2 = wb.create_sheet("Summary")
    ws2.append(["Interface aspect", "Items", "Passed", "Failed"])
    for c in range(1, 5):
        cell = ws2.cell(row=1, column=c)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = border
        cell.alignment = Alignment(horizontal="center")
    for ia, s in summary.items():
        ws2.append([ia, s["total"], s["passed"], s["failed"]])
    ws2.append(["Total", len(ITEMS), result_counts["Passed"], result_counts["Failed"]])
    for row in ws2.iter_rows(min_row=1, max_row=ws2.max_row, max_col=4):
        for cell in row:
            cell.border = border
            cell.alignment = Alignment(horizontal="center", vertical="center")
    ws2.cell(row=ws2.max_row, column=1).font = Font(bold=True)
    for idx, w in enumerate([22, 10, 10, 10], start=1):
        ws2.column_dimensions[get_column_letter(idx)].width = w

    ws3 = wb.create_sheet("Execution")
    ws3.append(["Field", "Value"])
    for k, v in [
        ("SUT", "EShop — frontend-web"),
        ("URL", "http://localhost:5173"),
        ("FRs", "FR-01, FR-02, FR-03, FR-04"),
        ("Screens", "Login, Register, Forgot Password, Profile"),
        ("Interface aspects", "IA-01, IA-02, IA-03, IA-04"),
        ("Browser", "Chromium 158 (Playwright 1.65)"),
        ("Viewports", "1280×900 desktop; 360×800 mobile; 640×800 (200% zoom equivalent)"),
        ("Date", "2026-11-07"),
        ("Total items", len(ITEMS)),
        ("Passed", result_counts["Passed"]),
        ("Failed", result_counts["Failed"]),
        ("AI initial items", source_counts["AI initial"]),
        ("Review additions", source_counts["Review addition"]),
        ("Bugs", len(bug_ids)),
    ]:
        ws3.append([k, v])
    ws3.column_dimensions["A"].width = 24
    ws3.column_dimensions["B"].width = 80

    wb.save(os.path.join(OUT, "checklist.xlsx"))
    print("wrote checklist.xlsx")
except ImportError as e:
    print("openpyxl not available:", e)

print(f"items={len(ITEMS)} passed={result_counts['Passed']} failed={result_counts['Failed']}")
print("sources:", dict(source_counts))
print("bugs:", len(bug_ids))
