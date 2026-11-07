## Summary

OTP input is unconstrained and step 2 has no step indicator.

## Environment

- SUT: EShop (`frontend-web`)
- URL: http://localhost:5173
- Browser: Chromium 158 (Playwright 1.65)
- Viewport: 1280×900 desktop; 360×800 mobile for responsive checks
- FR: FR-03 · IA-02, IA-03 · Forgot Password
- Checklist IDs: CHK-26, CHK-44

## Steps to reproduce

1. Request an OTP.
2. Inspect the OTP input and the step-2 layout.

## Expected

A 4-digit numeric input (inputmode=numeric, maxlength=4) and a step indicator such as “Bước 2/2”.

## Actual

The OTP input is type=text with maxlength=-1 and no inputmode/pattern; there is no step indicator.

## Evidence

![BUG-GUI-13](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-26-forgot-otp-input.png)

![BUG-GUI-13](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-44-forgot-step-indicator.png)

## Root cause

ForgotPassword.jsx:68-87.

## Suggested fix

Use inputmode=numeric, maxLength=4, pattern="[0-9]{4}" and add a 1/2–2/2 indicator.
