# BUG-GUI-11 — Password rule text contradicts the implemented regex

| Field | Value |
| --- | --- |
| Severity | **Major** |
| FR | FR-01, FR-03 |
| Interface aspect | IA-02 |
| Screen | Register, Forgot Password |
| Checklist IDs | CHK-23 |
| Environment | Chromium 158 (Playwright 1.65), 1280×900; backend http://localhost:3000, web http://localhost:5173 |
| Status | Draft — student review and GitHub publication pending |

## Steps to reproduce

1. Open /register.
2. Enter “Abcd1234!” (upper, lower, digit, special character, 9 chars) and submit.

## Expected result

The password is accepted because the helper text says a special character is required.

## Actual result

It is rejected. The regex requires a whitespace character ((?=.*\s)) and its character class [A-Za-z\d\s] forbids special characters. The same regex is used on the reset screen.

## Evidence

![BUG-GUI-11 evidence](../screenshots/CHK-23-register-password-rule.png)

## Root cause

Register.jsx:15-18; ForgotPassword.jsx:26-29.

## Suggested fix

Replace the regex with a correct strong-password rule (for example /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9])\S{8,}$/) and keep the copy in sync.

## GitHub issue

- Title: `[BUG-GUI-11] Password rule text contradicts the implemented regex`
- Labels: `bug`, `major`, `ia-02`, `fr-01`
- Publishing is blocked in this environment because the GitHub CLI/token is not configured; the ready-to-publish body is in `issues/`.
