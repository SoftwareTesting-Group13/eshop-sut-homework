# BUG-GUI-05 — Profile page has no h1 and two h2 headings

| Field | Value |
| --- | --- |
| Severity | **Minor** |
| FR | FR-04 |
| Interface aspect | IA-01 |
| Screen | Profile |
| Checklist IDs | CHK-13 |
| Environment | Chromium 158 (Playwright 1.65), 1280×900; backend http://localhost:3000, web http://localhost:5173 |
| Status | Draft — student review and GitHub publication pending |

## Steps to reproduce

1. Open /profile while logged in.
2. Inspect the heading outline or run axe-core.

## Expected result

One h1 for the page and h2 for the two sections.

## Actual result

0 h1 and two h2 elements (“Hồ sơ của bạn”, “Lịch sử đơn hàng”); axe-core reports “page-has-heading-one”.

## Evidence

![BUG-GUI-05 evidence](../screenshots/CHK-13-14-profile-headings-title.png)

## Root cause

frontend-web/src/pages/Profile.jsx:113, 167.

## Suggested fix

Use an h1 for the page title and h2 for the section titles.

## GitHub issue

- Title: `[BUG-GUI-05] Profile page has no h1 and two h2 headings`
- Labels: `bug`, `minor`, `ia-01`, `fr-04`
- Publishing is blocked in this environment because the GitHub CLI/token is not configured; the ready-to-publish body is in `issues/`.
