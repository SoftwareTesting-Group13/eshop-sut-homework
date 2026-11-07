# BUG-GUI-07 — RTL direction does not mirror the auth layout

| Field | Value |
| --- | --- |
| Severity | **Minor** |
| FR | FR-01..04 |
| Interface aspect | IA-01 |
| Screen | All auth screens |
| Checklist IDs | CHK-65 |
| Environment | Chromium 158 (Playwright 1.65), 1280×900; backend http://localhost:3000, web http://localhost:5173 |
| Status | Draft — student review and GitHub publication pending |

## Steps to reproduce

1. Open /login.
2. Set document.documentElement.dir = 'rtl'.

## Expected result

Alignment, ordering and spacing mirror for RTL readers.

## Actual result

Physical Tailwind utilities keep “Quên mật khẩu?” right-aligned and the header order unchanged; the layout is not mirrored.

## Evidence

![BUG-GUI-07 evidence](../screenshots/CHK-65-login-rtl.png)

## Root cause

Physical utilities (text-right, ml/mr) in Login.jsx:49-50 and App.jsx:20-38.

## Suggested fix

Use logical utilities (text-start/text-end, ms/me) and add an RTL smoke test.

## GitHub issue

- Title: `[BUG-GUI-07] RTL direction does not mirror the auth layout`
- Labels: `bug`, `minor`, `ia-01`, `fr-01..04`
- Publishing is blocked in this environment because the GitHub CLI/token is not configured; the ready-to-publish body is in `issues/`.
