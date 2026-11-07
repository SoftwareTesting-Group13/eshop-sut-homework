## Summary

Login page heading says “Đăng Ký” instead of “Đăng nhập”.

## Environment

- SUT: EShop (`frontend-web`)
- URL: http://localhost:5173
- Browser: Chromium 158 (Playwright 1.65)
- Viewport: 1280×900 desktop; 360×800 mobile for responsive checks
- FR: FR-02 · IA-01 · Login
- Checklist IDs: CHK-01

## Steps to reproduce

1. Open http://localhost:5173/login.
2. Read the card heading above the form.

## Expected

The heading identifies the Login screen (for example “Đăng nhập”).

## Actual

The heading is “Đăng Ký” (Register), so users can believe they are on the registration screen.

## Evidence

![BUG-GUI-01](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-01-login-heading.png)

## Root cause

frontend-web/src/pages/Login.jsx:24 — hard-coded <h2>Đăng Ký</h2>.

## Suggested fix

Change the heading to “Đăng nhập” and add a page-title test to the auth-screen suite.
