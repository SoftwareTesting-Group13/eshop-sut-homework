# BUG-GUI-03 — Text and button contrast fails WCAG 2.2 AA in several places

| Field | Value |
| --- | --- |
| Severity | **Major** |
| FR | FR-01, FR-04 |
| Interface aspect | IA-01 |
| Screen | Register, Profile |
| Checklist IDs | CHK-07, CHK-16 |
| Environment | Chromium 158 (Playwright 1.65), 1280×900; backend http://localhost:3000, web http://localhost:5173 |
| Status | Draft — student review and GitHub publication pending |

## Steps to reproduce

1. Open /register and /profile.
2. Run axe-core or compute the contrast of the helper text, red CTA, yellow username and red logout button.

## Expected result

Normal text has at least 4.5:1 contrast against its background.

## Actual result

axe-core reports 2.53:1 for the register helper text, 3.76:1 for white on the red button, 3.92:1 for the yellow username on blue, and 3.76:1 for the red logout button.

## Evidence

![BUG-GUI-03 evidence](../screenshots/CHK-07-register-contrast.png)

![BUG-GUI-03 evidence](../screenshots/CHK-16-profile-contrast.png)

## Root cause

frontend-web/src/pages/Register.jsx:64-66, 72; frontend-web/src/App.jsx:26-29.

## Suggested fix

Darken the grey helper text and the red surfaces, or use dark text on light backgrounds; re-run axe-core after the change.

## GitHub issue

- Title: `[BUG-GUI-03] Text and button contrast fails WCAG 2.2 AA in several places`
- Labels: `bug`, `major`, `ia-01`, `fr-01`
- Publishing is blocked in this environment because the GitHub CLI/token is not configured; the ready-to-publish body is in `issues/`.
