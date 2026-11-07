## Summary

Login tab order starts at the submit button because of tabindex=1.

## Environment

- SUT: EShop (`frontend-web`)
- URL: http://localhost:5173
- Browser: Chromium 158 (Playwright 1.65)
- Viewport: 1280×900 desktop; 360×800 mobile for responsive checks
- FR: FR-02 · IA-03 · Login
- Checklist IDs: CHK-36

## Steps to reproduce

1. Open /login.
2. Focus the document body and press Tab once.

## Expected

The first Tab focuses the email field, then password, forgot link, submit, register link.

## Actual

The first Tab focuses the Sign In button because it has tabindex="1"; keyboard users skip the fields and the visual order is violated.

## Evidence

![BUG-GUI-16](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-36-login-tab-order.png)

## Root cause

Login.jsx:53-59 (tabIndex={1}).

## Suggested fix

Remove tabIndex; rely on DOM order.
