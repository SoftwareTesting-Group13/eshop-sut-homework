# BUG-GUI-16 — Login tab order starts at the submit button because of tabindex=1

| Field | Value |
| --- | --- |
| Severity | **Major** |
| FR | FR-02 |
| Interface aspect | IA-03 |
| Screen | Login |
| Checklist IDs | CHK-36 |
| Environment | Chromium 158 (Playwright 1.65), 1280×900; backend http://localhost:3000, web http://localhost:5173 |
| Status | Draft — student review and GitHub publication pending |

## Steps to reproduce

1. Open /login.
2. Focus the document body and press Tab once.

## Expected result

The first Tab focuses the email field, then password, forgot link, submit, register link.

## Actual result

The first Tab focuses the Sign In button because it has tabindex="1"; keyboard users skip the fields and the visual order is violated.

## Evidence

![BUG-GUI-16 evidence](../screenshots/CHK-36-login-tab-order.png)

## Root cause

Login.jsx:53-59 (tabIndex={1}).

## Suggested fix

Remove tabIndex; rely on DOM order.

## GitHub issue

- Title: `[BUG-GUI-16] Login tab order starts at the submit button because of tabindex=1`
- Labels: `bug`, `major`, `ia-03`, `fr-02`
- Publishing is blocked in this environment because the GitHub CLI/token is not configured; the ready-to-publish body is in `issues/`.
