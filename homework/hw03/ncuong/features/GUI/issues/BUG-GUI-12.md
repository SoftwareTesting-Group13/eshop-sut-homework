## Summary

Registration and password reset have no confirm-password field.

## Environment

- SUT: EShop (`frontend-web`)
- URL: http://localhost:5173
- Browser: Chromium 158 (Playwright 1.65)
- Viewport: 1280×900 desktop; 360×800 mobile for responsive checks
- FR: FR-01, FR-03 · IA-02 · Register, Forgot Password
- Checklist IDs: CHK-24, CHK-28

## Steps to reproduce

1. Open /register and the OTP step of /forgot-password.
2. Count the password inputs.

## Expected

A confirm-password field with a match check.

## Actual

Only one password input on each form; a typo creates an unusable account or locks the user out of the new password.

## Evidence

![BUG-GUI-12](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-24-register-no-confirm.png)

![BUG-GUI-12](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-28-forgot-no-confirm.png)

## Root cause

Register.jsx:55-67; ForgotPassword.jsx:78-87.

## Suggested fix

Add a confirm-password input and a match validation before submit.
