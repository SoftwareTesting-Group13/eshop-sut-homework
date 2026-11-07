# BUG-GUI-04 — Forgot-password step 2 primary and back buttons look identical

| Field | Value |
| --- | --- |
| Severity | **Minor** |
| FR | FR-03 |
| Interface aspect | IA-01 |
| Screen | Forgot Password |
| Checklist IDs | CHK-11 |
| Environment | Chromium 158 (Playwright 1.65), 1280×900; backend http://localhost:3000, web http://localhost:5173 |
| Status | Draft — student review and GitHub publication pending |

## Steps to reproduce

1. Open /forgot-password, enter a valid email and request the OTP.
2. Compare “Đặt lại mật khẩu” and “← Quay lại”.

## Expected result

The primary action is visually dominant and the secondary/back action is clearly subordinate.

## Actual result

Both are full-width green buttons with identical bg-green-600 styling; users can click the wrong one.

## Evidence

![BUG-GUI-04 evidence](../screenshots/CHK-11-forgot-buttons.png)

## Root cause

frontend-web/src/pages/ForgotPassword.jsx:90-95.

## Suggested fix

Render the back action as a text/outline button and keep the primary action filled.

## GitHub issue

- Title: `[BUG-GUI-04] Forgot-password step 2 primary and back buttons look identical`
- Labels: `bug`, `minor`, `ia-01`, `fr-03`
- Publishing is blocked in this environment because the GitHub CLI/token is not configured; the ready-to-publish body is in `issues/`.
