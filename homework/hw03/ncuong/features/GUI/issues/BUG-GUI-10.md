## Summary

Email format and duplicate-email checks are missing.

## Environment

- SUT: EShop (`frontend-web`)
- URL: http://localhost:5173
- Browser: Chromium 158 (Playwright 1.65)
- Viewport: 1280×900 desktop; 360×800 mobile for responsive checks
- FR: FR-01, FR-03 · IA-02, IA-04 · Register, Forgot Password
- Checklist IDs: CHK-21, CHK-25, CHK-54

## Steps to reproduce

1. Register with “not-an-email-<timestamp>”.
2. Register the same valid email twice.
3. Request an OTP for a malformed email.

## Expected

Malformed addresses are rejected inline and duplicate emails return a clear conflict message.

## Actual

Malformed emails are accepted; registering the same email twice also succeeds and redirects to /login with no error. The backend has no unique constraint on email.

## Evidence

![BUG-GUI-10](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-21-register-invalid-email.png)

![BUG-GUI-10](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-25-forgot-email-type.png)

![BUG-GUI-10](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-54-register-duplicate-email.png)

## Root cause

Register.jsx:47-53 (type=text); backend/server.js:20-30 (plain INSERT, no validation); database.js users.email is not UNIQUE.

## Suggested fix

Use type=email plus a format check; add UNIQUE(email) and return HTTP 409 with a human-readable message.
