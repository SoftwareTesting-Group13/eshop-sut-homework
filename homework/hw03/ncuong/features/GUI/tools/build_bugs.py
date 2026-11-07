#!/usr/bin/env python3
"""Build bug reports and GitHub issue drafts for the HW03 GUI checklist."""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(BASE)
BUGS_DIR = os.path.join(OUT, "bugs")
ISSUES_DIR = os.path.join(OUT, "issues")
os.makedirs(BUGS_DIR, exist_ok=True)
os.makedirs(ISSUES_DIR, exist_ok=True)

REPO = "SoftwareTesting-Group13/eshop-sut-homework"
BRANCH = "ncuong"
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/homework/hw03/ncuong/features/GUI"

B = [
    dict(id="BUG-GUI-01", severity="Minor", fr="FR-02", ia="IA-01", screen="Login",
         title="Login page heading says “Đăng Ký” instead of “Đăng nhập”",
         checks=["CHK-01"], shots=["CHK-01-login-heading.png"],
         steps=["Open http://localhost:5173/login.", "Read the card heading above the form."],
         expected="The heading identifies the Login screen (for example “Đăng nhập”).",
         actual="The heading is “Đăng Ký” (Register), so users can believe they are on the registration screen.",
         root="frontend-web/src/pages/Login.jsx:24 — hard-coded <h2>Đăng Ký</h2>.",
         fix="Change the heading to “Đăng nhập” and add a page-title test to the auth-screen suite."),
    dict(id="BUG-GUI-02", severity="Minor", fr="FR-01..04", ia="IA-01", screen="All auth screens",
         title="All pages share the browser tab title “frontend-web”",
         checks=["CHK-02", "CHK-06", "CHK-10", "CHK-14"], shots=["CHK-02-login-title.png", "CHK-06-register-title.png", "CHK-10-forgot-title.png", "CHK-13-14-profile-headings-title.png"],
         steps=["Open /login, /register, /forgot-password and /profile in separate tabs.", "Compare the browser tab titles."],
         expected="Each tab has a unique, descriptive title (for example “Đăng nhập — EShop”).",
         actual="Every tab is titled “frontend-web”; users with several tabs cannot tell them apart and bookmarks are indistinguishable.",
         root="frontend-web/index.html:7 static <title>; no per-route document.title update.",
         fix="Set document.title in each page (or use react-helmet / a route-title hook)."),
    dict(id="BUG-GUI-03", severity="Major", fr="FR-01, FR-04", ia="IA-01", screen="Register, Profile",
         title="Text and button contrast fails WCAG 2.2 AA in several places",
         checks=["CHK-07", "CHK-16"], shots=["CHK-07-register-contrast.png", "CHK-16-profile-contrast.png"],
         steps=["Open /register and /profile.", "Run axe-core or compute the contrast of the helper text, red CTA, yellow username and red logout button."],
         expected="Normal text has at least 4.5:1 contrast against its background.",
         actual="axe-core reports 2.53:1 for the register helper text, 3.76:1 for white on the red button, 3.92:1 for the yellow username on blue, and 3.76:1 for the red logout button.",
         root="frontend-web/src/pages/Register.jsx:64-66, 72; frontend-web/src/App.jsx:26-29.",
         fix="Darken the grey helper text and the red surfaces, or use dark text on light backgrounds; re-run axe-core after the change."),
    dict(id="BUG-GUI-04", severity="Minor", fr="FR-03", ia="IA-01", screen="Forgot Password",
         title="Forgot-password step 2 primary and back buttons look identical",
         checks=["CHK-11"], shots=["CHK-11-forgot-buttons.png"],
         steps=["Open /forgot-password, enter a valid email and request the OTP.", "Compare “Đặt lại mật khẩu” and “← Quay lại”."],
         expected="The primary action is visually dominant and the secondary/back action is clearly subordinate.",
         actual="Both are full-width green buttons with identical bg-green-600 styling; users can click the wrong one.",
         root="frontend-web/src/pages/ForgotPassword.jsx:90-95.",
         fix="Render the back action as a text/outline button and keep the primary action filled."),
    dict(id="BUG-GUI-05", severity="Minor", fr="FR-04", ia="IA-01", screen="Profile",
         title="Profile page has no h1 and two h2 headings",
         checks=["CHK-13"], shots=["CHK-13-14-profile-headings-title.png"],
         steps=["Open /profile while logged in.", "Inspect the heading outline or run axe-core."],
         expected="One h1 for the page and h2 for the two sections.",
         actual="0 h1 and two h2 elements (“Hồ sơ của bạn”, “Lịch sử đơn hàng”); axe-core reports “page-has-heading-one”.",
         root="frontend-web/src/pages/Profile.jsx:113, 167.",
         fix="Use an h1 for the page title and h2 for the section titles."),
    dict(id="BUG-GUI-06", severity="Major", fr="FR-04", ia="IA-01", screen="Profile",
         title="Order-history table forces horizontal page scrolling on mobile",
         checks=["CHK-15"], shots=["CHK-15-profile-mobile-table.png"],
         steps=["Open /profile at a 360px viewport with at least one order.", "Measure document.documentElement.scrollWidth."],
         expected="The table adapts (scroll container or card layout) and the page has no horizontal scroll.",
         actual="Page scrollWidth is 399px vs clientWidth 360px (39px overflow); the 5-column table keeps its desktop width and is clipped.",
         root="frontend-web/src/pages/Profile.jsx:171-212 — no responsive wrapper or card layout.",
         fix="Wrap the table in overflow-x-auto with a min-width, or render order cards below the md breakpoint."),
    dict(id="BUG-GUI-07", severity="Minor", fr="FR-01..04", ia="IA-01", screen="All auth screens",
         title="RTL direction does not mirror the auth layout",
         checks=["CHK-65"], shots=["CHK-65-login-rtl.png"],
         steps=["Open /login.", "Set document.documentElement.dir = 'rtl'."],
         expected="Alignment, ordering and spacing mirror for RTL readers.",
         actual="Physical Tailwind utilities keep “Quên mật khẩu?” right-aligned and the header order unchanged; the layout is not mirrored.",
         root="Physical utilities (text-right, ml/mr) in Login.jsx:49-50 and App.jsx:20-38.",
         fix="Use logical utilities (text-start/text-end, ms/me) and add an RTL smoke test."),
    dict(id="BUG-GUI-08", severity="Major", fr="FR-02", ia="IA-02", screen="Login",
         title="Login password is visible and the email field has no email semantics",
         checks=["CHK-17", "CHK-18"], shots=["CHK-17-18-19-login-fields.png"],
         steps=["Open /login.", "Type into both fields and inspect the input types."],
         expected="The email field is type=email and the password field is type=password.",
         actual="Both fields are type=text; the password is visible on screen and the label says “Username” although the backend expects an email.",
         root="frontend-web/src/pages/Login.jsx:29-45.",
         fix="Use type=email, type=password and label the first field “Email”."),
    dict(id="BUG-GUI-09", severity="Major", fr="FR-01..04", ia="IA-02", screen="Login, Register, Forgot Password, Profile",
         title="Form inputs lack programmatic label associations",
         checks=["CHK-19", "CHK-32"], shots=["CHK-17-18-19-login-fields.png", "CHK-32-profile-labels.png"],
         steps=["Open each auth screen.", "Run axe-core or inspect label htmlFor / input id / aria-label."],
         expected="Every input has an accessible name from a label, aria-label or aria-labelledby.",
         actual="All labels are plain text without htmlFor and all inputs lack id/aria-label; axe-core reports critical “label” violations on every screen.",
         root="Login.jsx:28-45, Register.jsx:36-66, ForgotPassword.jsx:48-86, Profile.jsx:116-155.",
         fix="Add id to each input and htmlFor to its label (or aria-label for icon-only controls)."),
    dict(id="BUG-GUI-10", severity="Major", fr="FR-01, FR-03", ia="IA-02, IA-04", screen="Register, Forgot Password",
         title="Email format and duplicate-email checks are missing",
         checks=["CHK-21", "CHK-25", "CHK-54"], shots=["CHK-21-register-invalid-email.png", "CHK-25-forgot-email-type.png", "CHK-54-register-duplicate-email.png"],
         steps=["Register with “not-an-email-<timestamp>”.", "Register the same valid email twice.", "Request an OTP for a malformed email."],
         expected="Malformed addresses are rejected inline and duplicate emails return a clear conflict message.",
         actual="Malformed emails are accepted; registering the same email twice also succeeds and redirects to /login with no error. The backend has no unique constraint on email.",
         root="Register.jsx:47-53 (type=text); backend/server.js:20-30 (plain INSERT, no validation); database.js users.email is not UNIQUE.",
         fix="Use type=email plus a format check; add UNIQUE(email) and return HTTP 409 with a human-readable message."),
    dict(id="BUG-GUI-11", severity="Major", fr="FR-01, FR-03", ia="IA-02", screen="Register, Forgot Password",
         title="Password rule text contradicts the implemented regex",
         checks=["CHK-23"], shots=["CHK-23-register-password-rule.png"],
         steps=["Open /register.", "Enter “Abcd1234!” (upper, lower, digit, special character, 9 chars) and submit."],
         expected="The password is accepted because the helper text says a special character is required.",
         actual="It is rejected. The regex requires a whitespace character ((?=.*\\s)) and its character class [A-Za-z\\d\\s] forbids special characters. The same regex is used on the reset screen.",
         root="Register.jsx:15-18; ForgotPassword.jsx:26-29.",
         fix="Replace the regex with a correct strong-password rule (for example /^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[^A-Za-z0-9])\\S{8,}$/) and keep the copy in sync."),
    dict(id="BUG-GUI-12", severity="Minor", fr="FR-01, FR-03", ia="IA-02", screen="Register, Forgot Password",
         title="Registration and password reset have no confirm-password field",
         checks=["CHK-24", "CHK-28"], shots=["CHK-24-register-no-confirm.png", "CHK-28-forgot-no-confirm.png"],
         steps=["Open /register and the OTP step of /forgot-password.", "Count the password inputs."],
         expected="A confirm-password field with a match check.",
         actual="Only one password input on each form; a typo creates an unusable account or locks the user out of the new password.",
         root="Register.jsx:55-67; ForgotPassword.jsx:78-87.",
         fix="Add a confirm-password input and a match validation before submit."),
    dict(id="BUG-GUI-13", severity="Minor", fr="FR-03", ia="IA-02, IA-03", screen="Forgot Password",
         title="OTP input is unconstrained and step 2 has no step indicator",
         checks=["CHK-26", "CHK-44"], shots=["CHK-26-forgot-otp-input.png", "CHK-44-forgot-step-indicator.png"],
         steps=["Request an OTP.", "Inspect the OTP input and the step-2 layout."],
         expected="A 4-digit numeric input (inputmode=numeric, maxlength=4) and a step indicator such as “Bước 2/2”.",
         actual="The OTP input is type=text with maxlength=-1 and no inputmode/pattern; there is no step indicator.",
         root="ForgotPassword.jsx:68-87.",
         fix="Use inputmode=numeric, maxLength=4, pattern=\"[0-9]{4}\" and add a 1/2–2/2 indicator."),
    dict(id="BUG-GUI-14", severity="Blocker", fr="FR-04", ia="IA-02", screen="Profile",
         title="Phone validation rejects valid Vietnamese numbers and uses a blocking alert",
         checks=["CHK-30", "CHK-31"], shots=["CHK-30-profile-phone-inputmode.png", "CHK-31-profile-phone-alert.png"],
         steps=["Log in and open /profile.", "Enter the placeholder value 0912345678 and click “Cập nhật”."],
         expected="The phone number is accepted and the profile is saved.",
         actual="An alert says “Số điện thoại không hợp lệ. Vui lòng nhập đúng 9-10 chữ số.” The regex /^[1-9][0-9]{8,9}$/ rejects every number starting with 0, which is the normal Vietnamese mobile prefix.",
         root="Profile.jsx:43-46.",
         fix="Use a Vietnamese phone rule such as /^0\\d{9,10}$/ (or a library), add inputmode=tel, and show an inline error instead of alert()."),
    dict(id="BUG-GUI-15", severity="Minor", fr="FR-02", ia="IA-03", screen="Login",
         title="Forgot-password link performs a full page reload",
         checks=["CHK-34"], shots=["CHK-34-forgot-link-reload.png"],
         steps=["Open /login.", "Set window.__spaMarker = 'kept', click “Quên mật khẩu?” and inspect the marker."],
         expected="React Router navigation without a document reload.",
         actual="The marker is lost; the link is a raw <a href=\"/forgot-password\"> and the whole SPA reloads.",
         root="Login.jsx:50.",
         fix="Use <Link to=\"/forgot-password\"> from react-router-dom."),
    dict(id="BUG-GUI-16", severity="Major", fr="FR-02", ia="IA-03", screen="Login",
         title="Login tab order starts at the submit button because of tabindex=1",
         checks=["CHK-36"], shots=["CHK-36-login-tab-order.png"],
         steps=["Open /login.", "Focus the document body and press Tab once."],
         expected="The first Tab focuses the email field, then password, forgot link, submit, register link.",
         actual="The first Tab focuses the Sign In button because it has tabindex=\"1\"; keyboard users skip the fields and the visual order is violated.",
         root="Login.jsx:53-59 (tabIndex={1}).",
         fix="Remove tabIndex; rely on DOM order."),
    dict(id="BUG-GUI-17", severity="Minor", fr="FR-03", ia="IA-03", screen="Forgot Password",
         title="Focus is lost after switching to the OTP step",
         checks=["CHK-43"], shots=["CHK-43-forgot-focus.png"],
         steps=["Request an OTP.", "Inspect document.activeElement after step 2 renders."],
         expected="Focus moves to the OTP field or the step-2 heading and the change is announced.",
         actual="document.activeElement is BODY; screen-reader and keyboard users are not told that the step changed.",
         root="ForgotPassword.jsx:13-22 (setStep without focus management).",
         fix="Focus the step-2 heading or first input in an effect and use aria-live for the status message."),
    dict(id="BUG-GUI-18", severity="Major", fr="FR-02, FR-04", ia="IA-03", screen="Login, Profile",
         title="Auth route guards are missing (profile, login, logout)",
         checks=["CHK-45", "CHK-47", "CHK-69"], shots=["CHK-45-profile-unauth.png", "CHK-47-profile-logout.png", "CHK-69-login-while-authenticated.png"],
         steps=["Open /profile in a private window.", "Log in, then open /login.", "Log out and observe the URL."],
         expected="Unauthenticated /profile redirects to /login?next=/profile; authenticated /login redirects home; logout navigates to a public page.",
         actual="Unauthenticated /profile stays on /profile with “Vui lòng đăng nhập”; authenticated /login still renders the login form; after logout the URL remains /profile.",
         root="App.jsx:50-59 (no guards), Profile.jsx:108, AuthContext.jsx:37-41 (logout does not navigate).",
         fix="Add ProtectedRoute/PublicRoute wrappers and navigate('/') or navigate('/login') on logout."),
    dict(id="BUG-GUI-19", severity="Minor", fr="FR-04", ia="IA-03", screen="Profile",
         title="Navigation has no current-page indication",
         checks=["CHK-48"], shots=["CHK-48-profile-active-nav.png"],
         steps=["Open /profile while logged in.", "Inspect the header links for aria-current or an active class."],
         expected="The current page is visually and programmatically indicated.",
         actual="Only hover styles exist; no aria-current, active class or underline identifies /profile.",
         root="App.jsx:20-38.",
         fix="Use NavLink and aria-current=\"page\" plus an active style."),
    dict(id="BUG-GUI-20", severity="Minor", fr="FR-01, FR-02", ia="IA-04", screen="Login, Register",
         title="Login and Register buttons have no loading or disabled state",
         checks=["CHK-49", "CHK-56"], shots=["CHK-49-login-loading.png", "CHK-56-register-loading.png"],
         steps=["Delay /api/login or /api/register by 2 seconds.", "Click the submit button and inspect it during the request."],
         expected="The button is disabled, shows a spinner/label change and exposes aria-busy.",
         actual="The button stays enabled with the same label; double submits are possible.",
         root="Login.jsx:12-20; Register.jsx:12-28.",
         fix="Add a submitting state, disable the button and show a spinner or “Đang xử lý…” label."),
    dict(id="BUG-GUI-21", severity="Major", fr="FR-01..04", ia="IA-04", screen="Login, Forgot Password, Profile",
         title="Form feedback uses blocking alert() or unannounced divs",
         checks=["CHK-50", "CHK-51", "CHK-59", "CHK-61"], shots=["CHK-50-51-login-error.png", "CHK-59-forgot-alert.png", "CHK-61-profile-update-alert.png"],
         steps=["Submit a wrong password on /login.", "Request an OTP for an unknown email.", "Save the profile with an invalid phone."],
         expected="Inline, field-associated messages announced through role=alert/aria-live; no blocking dialogs.",
         actual="Login shows a generic div without role/aria-live; Forgot Password and Profile use native alert(); errors are not associated with fields and do not distinguish causes.",
         root="Login.jsx:66; ForgotPassword.jsx:20, 37; Profile.jsx:44, 60-62, 75-78.",
         fix="Add an inline error/success region with role=status or role=alert, aria-describedby/aria-invalid on the field, and map server errors to specific messages."),
    dict(id="BUG-GUI-22", severity="Minor", fr="FR-01", ia="IA-04", screen="Register",
         title="Successful registration redirects silently",
         checks=["CHK-53"], shots=["CHK-53-register-silent-success.png"],
         steps=["Register a new valid account.", "Observe the transition to /login."],
         expected="A success message confirms the account was created before the redirect.",
         actual="The app navigates to /login with no success feedback; users cannot tell whether registration succeeded.",
         root="Register.jsx:23-24.",
         fix="Show a success toast/inline message and then navigate (or pass state to Login)."),
    dict(id="BUG-GUI-23", severity="Major", fr="FR-01", ia="IA-04", screen="Register",
         title="Server error text is rendered verbatim",
         checks=["CHK-55"], shots=["CHK-55-register-raw-error.png"],
         steps=["Simulate POST /api/register returning 500 with a SQLite error.", "Submit the form."],
         expected="A generic, human-readable error; technical details stay in server logs.",
         actual="The UI renders “SQLITE_ERROR: no such column: name” because the catch block uses err.response.data.error directly.",
         root="Register.jsx:26.",
         fix="Map known errors to friendly messages and log the raw error server-side; never render database messages."),
    dict(id="BUG-GUI-24", severity="Blocker", fr="FR-03", ia="IA-04", screen="Forgot Password",
         title="Password-reset OTP is displayed on screen",
         checks=["CHK-58"], shots=["CHK-58-forgot-otp-exposed.png"],
         steps=["Open /forgot-password.", "Enter a registered email and request the OTP."],
         expected="The OTP is sent out-of-band (email/SMS) and never shown in the UI.",
         actual="Step 2 shows “Mã OTP của bạn là: 2129” in a green box; anyone with the email address can reset the password.",
         root="ForgotPassword.jsx:16-18; backend/server.js:68-85 returns resetToken in the response.",
         fix="Remove resetToken from the API response and UI; send it through a real out-of-band channel with expiry and rate limiting."),
    dict(id="BUG-GUI-25", severity="Major", fr="FR-04", ia="IA-04", screen="Profile",
         title="Order-history loading and error states are shown as an empty list",
         checks=["CHK-62", "CHK-63"], shots=["CHK-62-profile-orders-loading.png", "CHK-63-profile-orders-error.png"],
         steps=["Delay /api/orders/my-orders and open /profile.", "Repeat with a 500 response."],
         expected="A loading state while fetching and a distinct error state with retry on failure.",
         actual="“Bạn chưa có đơn hàng nào.” is shown during loading and after a 500 response; users cannot tell “no orders” from “request failed”.",
         root="Profile.jsx:14-29 (catch sets []), 168-169 (single empty state).",
         fix="Add loading/error state variables and render three distinct branches; add a retry button."),
    dict(id="BUG-GUI-26", severity="Major", fr="FR-04", ia="IA-04", screen="Profile",
         title="Cancel-order has no confirmation and is offered for shipping orders",
         checks=["CHK-64"], shots=["CHK-64-profile-cancel.png"],
         steps=["Open /profile with an order whose status is “Đang giao”.", "Click “Hủy đơn”."],
         expected="A confirmation dialog before cancelling, and the action only for statuses that may be cancelled.",
         actual="The button is rendered for shipping orders and calls PUT /api/orders/:id/cancel immediately; the only dialog is the API error. No “Bạn có chắc?” confirmation.",
         root="Profile.jsx:199-207 (condition allows shipping; no confirm).",
         fix="Show the button only for pending/confirmed, and require an explicit confirmation dialog before the API call."),
]

def rel_shot(name):
    return f"../screenshots/{name}"

def bug_md(b):
    lines = []
    lines.append(f"# {b['id']} — {b['title']}\n")
    lines.append("| Field | Value |")
    lines.append("| --- | --- |")
    lines.append(f"| Severity | **{b['severity']}** |")
    lines.append(f"| FR | {b['fr']} |")
    lines.append(f"| Interface aspect | {b['ia']} |")
    lines.append(f"| Screen | {b['screen']} |")
    lines.append(f"| Checklist IDs | {', '.join(b['checks'])} |")
    lines.append(f"| Environment | Chromium 158 (Playwright 1.65), 1280×900; backend http://localhost:3000, web http://localhost:5173 |")
    lines.append(f"| Status | Draft — student review and GitHub publication pending |")
    lines.append("\n## Steps to reproduce\n")
    for n, s in enumerate(b["steps"], 1):
        lines.append(f"{n}. {s}")
    lines.append("\n## Expected result\n")
    lines.append(b["expected"])
    lines.append("\n## Actual result\n")
    lines.append(b["actual"])
    lines.append("\n## Evidence\n")
    for s in b["shots"]:
        lines.append(f"![{b['id']} evidence]({rel_shot(s)})\n")
    lines.append("## Root cause\n")
    lines.append(b["root"])
    lines.append("\n## Suggested fix\n")
    lines.append(b["fix"])
    lines.append("\n## GitHub issue\n")
    lines.append(f"- Title: `[{b['id']}] {b['title']}`")
    lines.append(f"- Labels: `bug`, `{b['severity'].lower()}`, `{b['ia'].lower()}`, `{b['fr'].split(',')[0].strip().lower()}`")
    lines.append("- Publishing is blocked in this environment because the GitHub CLI/token is not configured; the ready-to-publish body is in `issues/`.")
    return "\n".join(lines) + "\n"

def issue_md(b):
    lines = []
    lines.append(f"## Summary\n")
    lines.append(b["title"] + ".\n")
    lines.append("## Environment\n")
    lines.append("- SUT: EShop (`frontend-web`)")
    lines.append("- URL: http://localhost:5173")
    lines.append("- Browser: Chromium 158 (Playwright 1.65)")
    lines.append("- Viewport: 1280×900 desktop; 360×800 mobile for responsive checks")
    lines.append(f"- FR: {b['fr']} · {b['ia']} · {b['screen']}")
    lines.append(f"- Checklist IDs: {', '.join(b['checks'])}")
    lines.append("\n## Steps to reproduce\n")
    for n, s in enumerate(b["steps"], 1):
        lines.append(f"{n}. {s}")
    lines.append("\n## Expected\n")
    lines.append(b["expected"])
    lines.append("\n## Actual\n")
    lines.append(b["actual"])
    lines.append("\n## Evidence\n")
    for s in b["shots"]:
        lines.append(f"![{b['id']}]({RAW}/screenshots/{s})\n")
    lines.append("## Root cause\n")
    lines.append(b["root"])
    lines.append("\n## Suggested fix\n")
    lines.append(b["fix"])
    return "\n".join(lines) + "\n"

for b in B:
    with open(os.path.join(BUGS_DIR, b["id"] + ".md"), "w", encoding="utf-8") as f:
        f.write(bug_md(b))
    with open(os.path.join(ISSUES_DIR, b["id"] + ".md"), "w", encoding="utf-8") as f:
        f.write(issue_md(b))

# Consolidated bug report
lines = ["# Bug report — HW03 GUI checklist\n",
         f"**SUT:** EShop web frontend · **Executed:** 2026-11-07 · **Browser:** Chromium 158 (Playwright 1.65)\n",
         f"**Total bugs:** {len(B)} · **Blocker:** {sum(1 for b in B if b['severity']=='Blocker')} · **Major:** {sum(1 for b in B if b['severity']=='Major')} · **Minor:** {sum(1 for b in B if b['severity']=='Minor')}\n",
         "Every bug below is reproducible from the steps in its linked report and has at least one screenshot. The GitHub issue body for each bug is in `issues/`; publication is pending GitHub authentication in this environment.\n",
         "| ID | Severity | FR | Screen | Title | Checklist IDs | Evidence |",
         "| --- | --- | --- | --- | --- | --- | --- |"]
for b in B:
    lines.append(f"| [{b['id']}](bugs/{b['id']}.md) | {b['severity']} | {b['fr']} | {b['screen']} | {b['title']} | {', '.join(b['checks'])} | {', '.join(b['shots'])} |")
lines.append("\n## Severity model\n")
lines.append("- **Blocker:** prevents the user from completing the flow or exposes the account (BUG-GUI-14, BUG-GUI-24).")
lines.append("- **Major:** causes task failure, data loss/confusion, a WCAG failure with real impact, or a security/privacy leak.")
lines.append("- **Minor:** visible defect or friction with a workaround; does not block the task.")
with open(os.path.join(OUT, "bug-report.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

# Issues JSON + publish script
issues = [{"id": b["id"], "title": f"[{b['id']}] {b['title']}",
           "body_file": f"issues/{b['id']}.md",
           "labels": ["bug", b["severity"].lower(), b["ia"].lower()],
           "screenshots": b["shots"]} for b in B]
with open(os.path.join(ISSUES_DIR, "issues.json"), "w", encoding="utf-8") as f:
    json.dump(issues, f, ensure_ascii=False, indent=2)

publish = """#!/usr/bin/env bash
set -euo pipefail
# Publish the drafted HW03 GUI issues with the GitHub CLI.
# Prerequisites:
#   1. gh auth login (or GH_TOKEN with repo scope)
#   2. The screenshots are pushed to the branch used in the raw URLs.
# Run from homework/hw03/ncuong/features/GUI:
#   bash issues/publish.sh
cd "$(dirname "$0")/.."
if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not found. Install it and run: gh auth login" >&2
  exit 1
fi
if ! gh auth status >/dev/null 2>&1; then
  echo "Not authenticated. Run: gh auth login" >&2
  exit 1
fi
python3 - <<'PY'
import json, subprocess, sys
issues = json.load(open('issues/issues.json'))
for it in issues:
    body = open(it['body_file'], encoding='utf-8').read()
    cmd = ['gh', 'issue', 'create', '--title', it['title'], '--body', body]
    for label in it['labels']:
        cmd += ['--label', label]
    print('Creating', it['title'])
    subprocess.run(cmd, check=True)
PY
"""
with open(os.path.join(ISSUES_DIR, "publish.sh"), "w", encoding="utf-8") as f:
    f.write(publish)
os.chmod(os.path.join(ISSUES_DIR, "publish.sh"), 0o755)

print(f"wrote {len(B)} bug reports and issue drafts")
