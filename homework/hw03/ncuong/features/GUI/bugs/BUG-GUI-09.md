# BUG-GUI-09 — Form inputs lack programmatic label associations

| Field | Value |
| --- | --- |
| Severity | **Major** |
| FR | FR-01..04 |
| Interface aspect | IA-02 |
| Screen | Login, Register, Forgot Password, Profile |
| Checklist IDs | CHK-19, CHK-32 |
| Environment | Chromium 158 (Playwright 1.65), 1280×900; backend http://localhost:3000, web http://localhost:5173 |
| Status | Draft — student review and GitHub publication pending |

## Steps to reproduce

1. Open each auth screen.
2. Run axe-core or inspect label htmlFor / input id / aria-label.

## Expected result

Every input has an accessible name from a label, aria-label or aria-labelledby.

## Actual result

All labels are plain text without htmlFor and all inputs lack id/aria-label; axe-core reports critical “label” violations on every screen.

## Evidence

![BUG-GUI-09 evidence](../screenshots/CHK-17-18-19-login-fields.png)

![BUG-GUI-09 evidence](../screenshots/CHK-32-profile-labels.png)

## Root cause

Login.jsx:28-45, Register.jsx:36-66, ForgotPassword.jsx:48-86, Profile.jsx:116-155.

## Suggested fix

Add id to each input and htmlFor to its label (or aria-label for icon-only controls).

## GitHub issue

- Title: `[BUG-GUI-09] Form inputs lack programmatic label associations`
- Labels: `bug`, `major`, `ia-02`, `fr-01..04`
- Publishing is blocked in this environment because the GitHub CLI/token is not configured; the ready-to-publish body is in `issues/`.
