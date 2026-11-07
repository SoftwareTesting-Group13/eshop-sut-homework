## Summary

Password rule text contradicts the implemented regex.

## Environment

- SUT: EShop (`frontend-web`)
- URL: http://localhost:5173
- Browser: Chromium 158 (Playwright 1.65)
- Viewport: 1280×900 desktop; 360×800 mobile for responsive checks
- FR: FR-01, FR-03 · IA-02 · Register, Forgot Password
- Checklist IDs: CHK-23

## Steps to reproduce

1. Open /register.
2. Enter “Abcd1234!” (upper, lower, digit, special character, 9 chars) and submit.

## Expected

The password is accepted because the helper text says a special character is required.

## Actual

It is rejected. The regex requires a whitespace character ((?=.*\s)) and its character class [A-Za-z\d\s] forbids special characters. The same regex is used on the reset screen.

## Evidence

![BUG-GUI-11](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-23-register-password-rule.png)

## Root cause

Register.jsx:15-18; ForgotPassword.jsx:26-29.

## Suggested fix

Replace the regex with a correct strong-password rule (for example /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9])\S{8,}$/) and keep the copy in sync.
