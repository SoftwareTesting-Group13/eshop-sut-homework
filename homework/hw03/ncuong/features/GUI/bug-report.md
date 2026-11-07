# Bug report — HW03 GUI checklist

**SUT:** EShop web frontend · **Executed:** 2026-11-07 · **Browser:** Chromium 158 (Playwright 1.65)

**Total bugs:** 26 · **Blocker:** 2 · **Major:** 12 · **Minor:** 12

Every bug below is reproducible from the steps in its linked report and has at least one screenshot. The GitHub issue body for each bug is in `issues/`; publication is pending GitHub authentication in this environment.

| ID | Severity | FR | Screen | Title | Checklist IDs | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| [BUG-GUI-01](bugs/BUG-GUI-01.md) | Minor | FR-02 | Login | Login page heading says “Đăng Ký” instead of “Đăng nhập” | CHK-01 | CHK-01-login-heading.png |
| [BUG-GUI-02](bugs/BUG-GUI-02.md) | Minor | FR-01..04 | All auth screens | All pages share the browser tab title “frontend-web” | CHK-02, CHK-06, CHK-10, CHK-14 | CHK-02-login-title.png, CHK-06-register-title.png, CHK-10-forgot-title.png, CHK-13-14-profile-headings-title.png |
| [BUG-GUI-03](bugs/BUG-GUI-03.md) | Major | FR-01, FR-04 | Register, Profile | Text and button contrast fails WCAG 2.2 AA in several places | CHK-07, CHK-16 | CHK-07-register-contrast.png, CHK-16-profile-contrast.png |
| [BUG-GUI-04](bugs/BUG-GUI-04.md) | Minor | FR-03 | Forgot Password | Forgot-password step 2 primary and back buttons look identical | CHK-11 | CHK-11-forgot-buttons.png |
| [BUG-GUI-05](bugs/BUG-GUI-05.md) | Minor | FR-04 | Profile | Profile page has no h1 and two h2 headings | CHK-13 | CHK-13-14-profile-headings-title.png |
| [BUG-GUI-06](bugs/BUG-GUI-06.md) | Major | FR-04 | Profile | Order-history table forces horizontal page scrolling on mobile | CHK-15 | CHK-15-profile-mobile-table.png |
| [BUG-GUI-07](bugs/BUG-GUI-07.md) | Minor | FR-01..04 | All auth screens | RTL direction does not mirror the auth layout | CHK-65 | CHK-65-login-rtl.png |
| [BUG-GUI-08](bugs/BUG-GUI-08.md) | Major | FR-02 | Login | Login password is visible and the email field has no email semantics | CHK-17, CHK-18 | CHK-17-18-19-login-fields.png |
| [BUG-GUI-09](bugs/BUG-GUI-09.md) | Major | FR-01..04 | Login, Register, Forgot Password, Profile | Form inputs lack programmatic label associations | CHK-19, CHK-32 | CHK-17-18-19-login-fields.png, CHK-32-profile-labels.png |
| [BUG-GUI-10](bugs/BUG-GUI-10.md) | Major | FR-01, FR-03 | Register, Forgot Password | Email format and duplicate-email checks are missing | CHK-21, CHK-25, CHK-54 | CHK-21-register-invalid-email.png, CHK-25-forgot-email-type.png, CHK-54-register-duplicate-email.png |
| [BUG-GUI-11](bugs/BUG-GUI-11.md) | Major | FR-01, FR-03 | Register, Forgot Password | Password rule text contradicts the implemented regex | CHK-23 | CHK-23-register-password-rule.png |
| [BUG-GUI-12](bugs/BUG-GUI-12.md) | Minor | FR-01, FR-03 | Register, Forgot Password | Registration and password reset have no confirm-password field | CHK-24, CHK-28 | CHK-24-register-no-confirm.png, CHK-28-forgot-no-confirm.png |
| [BUG-GUI-13](bugs/BUG-GUI-13.md) | Minor | FR-03 | Forgot Password | OTP input is unconstrained and step 2 has no step indicator | CHK-26, CHK-44 | CHK-26-forgot-otp-input.png, CHK-44-forgot-step-indicator.png |
| [BUG-GUI-14](bugs/BUG-GUI-14.md) | Blocker | FR-04 | Profile | Phone validation rejects valid Vietnamese numbers and uses a blocking alert | CHK-30, CHK-31 | CHK-30-profile-phone-inputmode.png, CHK-31-profile-phone-alert.png |
| [BUG-GUI-15](bugs/BUG-GUI-15.md) | Minor | FR-02 | Login | Forgot-password link performs a full page reload | CHK-34 | CHK-34-forgot-link-reload.png |
| [BUG-GUI-16](bugs/BUG-GUI-16.md) | Major | FR-02 | Login | Login tab order starts at the submit button because of tabindex=1 | CHK-36 | CHK-36-login-tab-order.png |
| [BUG-GUI-17](bugs/BUG-GUI-17.md) | Minor | FR-03 | Forgot Password | Focus is lost after switching to the OTP step | CHK-43 | CHK-43-forgot-focus.png |
| [BUG-GUI-18](bugs/BUG-GUI-18.md) | Major | FR-02, FR-04 | Login, Profile | Auth route guards are missing (profile, login, logout) | CHK-45, CHK-47, CHK-69 | CHK-45-profile-unauth.png, CHK-47-profile-logout.png, CHK-69-login-while-authenticated.png |
| [BUG-GUI-19](bugs/BUG-GUI-19.md) | Minor | FR-04 | Profile | Navigation has no current-page indication | CHK-48 | CHK-48-profile-active-nav.png |
| [BUG-GUI-20](bugs/BUG-GUI-20.md) | Minor | FR-01, FR-02 | Login, Register | Login and Register buttons have no loading or disabled state | CHK-49, CHK-56 | CHK-49-login-loading.png, CHK-56-register-loading.png |
| [BUG-GUI-21](bugs/BUG-GUI-21.md) | Major | FR-01..04 | Login, Forgot Password, Profile | Form feedback uses blocking alert() or unannounced divs | CHK-50, CHK-51, CHK-59, CHK-61 | CHK-50-51-login-error.png, CHK-59-forgot-alert.png, CHK-61-profile-update-alert.png |
| [BUG-GUI-22](bugs/BUG-GUI-22.md) | Minor | FR-01 | Register | Successful registration redirects silently | CHK-53 | CHK-53-register-silent-success.png |
| [BUG-GUI-23](bugs/BUG-GUI-23.md) | Major | FR-01 | Register | Server error text is rendered verbatim | CHK-55 | CHK-55-register-raw-error.png |
| [BUG-GUI-24](bugs/BUG-GUI-24.md) | Blocker | FR-03 | Forgot Password | Password-reset OTP is displayed on screen | CHK-58 | CHK-58-forgot-otp-exposed.png |
| [BUG-GUI-25](bugs/BUG-GUI-25.md) | Major | FR-04 | Profile | Order-history loading and error states are shown as an empty list | CHK-62, CHK-63 | CHK-62-profile-orders-loading.png, CHK-63-profile-orders-error.png |
| [BUG-GUI-26](bugs/BUG-GUI-26.md) | Major | FR-04 | Profile | Cancel-order has no confirmation and is offered for shipping orders | CHK-64 | CHK-64-profile-cancel.png |

## Severity model

- **Blocker:** prevents the user from completing the flow or exposes the account (BUG-GUI-14, BUG-GUI-24).
- **Major:** causes task failure, data loss/confusion, a WCAG failure with real impact, or a security/privacy leak.
- **Minor:** visible defect or friction with a workaround; does not block the task.
