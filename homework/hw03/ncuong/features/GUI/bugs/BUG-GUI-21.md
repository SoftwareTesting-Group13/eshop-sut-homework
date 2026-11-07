# BUG-GUI-21 — Form feedback uses blocking alert() or unannounced divs

| Field | Value |
| --- | --- |
| Severity | **Major** |
| FR | FR-01..04 |
| Interface aspect | IA-04 |
| Screen | Login, Forgot Password, Profile |
| Checklist IDs | CHK-50, CHK-51, CHK-59, CHK-61 |
| Environment | Chromium 158 (Playwright 1.65), 1280×900; backend http://localhost:3000, web http://localhost:5173 |
| Status | Draft — student review and GitHub publication pending |

## Steps to reproduce

1. Submit a wrong password on /login.
2. Request an OTP for an unknown email.
3. Save the profile with an invalid phone.

## Expected result

Inline, field-associated messages announced through role=alert/aria-live; no blocking dialogs.

## Actual result

Login shows a generic div without role/aria-live; Forgot Password and Profile use native alert(); errors are not associated with fields and do not distinguish causes.

## Evidence

![BUG-GUI-21 evidence](../screenshots/CHK-50-51-login-error.png)

![BUG-GUI-21 evidence](../screenshots/CHK-59-forgot-alert.png)

![BUG-GUI-21 evidence](../screenshots/CHK-61-profile-update-alert.png)

## Root cause

Login.jsx:66; ForgotPassword.jsx:20, 37; Profile.jsx:44, 60-62, 75-78.

## Suggested fix

Add an inline error/success region with role=status or role=alert, aria-describedby/aria-invalid on the field, and map server errors to specific messages.

## GitHub issue

- Title: `[BUG-GUI-21] Form feedback uses blocking alert() or unannounced divs`
- Labels: `bug`, `major`, `ia-04`, `fr-01..04`
- Publishing is blocked in this environment because the GitHub CLI/token is not configured; the ready-to-publish body is in `issues/`.
