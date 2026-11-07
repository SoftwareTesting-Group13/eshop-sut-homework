## Summary

RTL direction does not mirror the auth layout.

## Environment

- SUT: EShop (`frontend-web`)
- URL: http://localhost:5173
- Browser: Chromium 158 (Playwright 1.65)
- Viewport: 1280×900 desktop; 360×800 mobile for responsive checks
- FR: FR-01..04 · IA-01 · All auth screens
- Checklist IDs: CHK-65

## Steps to reproduce

1. Open /login.
2. Set document.documentElement.dir = 'rtl'.

## Expected

Alignment, ordering and spacing mirror for RTL readers.

## Actual

Physical Tailwind utilities keep “Quên mật khẩu?” right-aligned and the header order unchanged; the layout is not mirrored.

## Evidence

![BUG-GUI-07](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-65-login-rtl.png)

## Root cause

Physical utilities (text-right, ml/mr) in Login.jsx:49-50 and App.jsx:20-38.

## Suggested fix

Use logical utilities (text-start/text-end, ms/me) and add an RTL smoke test.
