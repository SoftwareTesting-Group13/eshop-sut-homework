# AI-generated initial checklist (before human review)

Generated with the `ui-checklist-generator` skill (8 categories: layout, typography, colour, interaction, responsiveness, accessibility, product states, polish) expanded across four screens. **44 items.**

This is the raw initial set kept for the audit trail. It was reviewed afterwards; the review additions and their rationale are in `review-additions.md`.

| ID | IA | Screen | FR | Item |
| --- | --- | --- | --- | --- |
| CHK-01 | IA-01 | Login | FR-02 | The page heading names the Login screen and matches the action. |
| CHK-03 | IA-01 | Login | FR-02 | The auth card uses the same alignment, spacing and typography as Register and Forgot Password. |
| CHK-04 | IA-01 | Login | FR-02 | The Login page has no horizontal scrolling at a 360px viewport. |
| CHK-05 | IA-01 | Register | FR-01 | The page heading names the Register screen. |
| CHK-08 | IA-01 | Register | FR-01 | The Register page has no horizontal scrolling at a 360px viewport. |
| CHK-09 | IA-01 | Forgot Password | FR-03 | The page heading names the Forgot Password screen. |
| CHK-11 | IA-01 | Forgot Password | FR-03 | Step 2 primary and secondary actions are visually distinguishable. |
| CHK-12 | IA-01 | Forgot Password | FR-03 | The Forgot Password page has no horizontal scrolling at a 360px viewport. |
| CHK-17 | IA-02 | Login | FR-02 | The email/username field uses an input type appropriate for email. |
| CHK-18 | IA-02 | Login | FR-02 | The password field masks entered characters. |
| CHK-20 | IA-02 | Login | FR-02 | Required fields are enforced with native validation on empty submit. |
| CHK-21 | IA-02 | Register | FR-01 | The email field uses type=email and rejects malformed addresses. |
| CHK-22 | IA-02 | Register | FR-01 | The password field masks entered characters. |
| CHK-24 | IA-02 | Register | FR-01 | A confirm-password field prevents mistyped passwords. |
| CHK-25 | IA-02 | Forgot Password | FR-03 | The email field uses type=email and validates the address format. |
| CHK-27 | IA-02 | Forgot Password | FR-03 | The new-password field masks entered characters. |
| CHK-28 | IA-02 | Forgot Password | FR-03 | The reset form requires password confirmation. |
| CHK-29 | IA-02 | Profile | FR-04 | The email field is read-only and clearly marked as non-editable. |
| CHK-30 | IA-02 | Profile | FR-04 | The phone field uses tel inputmode and constrains its format. |
| CHK-33 | IA-03 | Login | FR-02 | The global header is present and its links work on the Login page. |
| CHK-35 | IA-03 | Login | FR-02 | The “Đăng ký ngay” link navigates to /register. |
| CHK-37 | IA-03 | Register | FR-01 | Header navigation is present and consistent with Login. |
| CHK-38 | IA-03 | Register | FR-01 | The “Đăng nhập” link navigates to /login. |
| CHK-39 | IA-03 | Register | FR-01 | Keyboard tab order follows the visual order. |
| CHK-40 | IA-03 | Register | FR-01 | Successful registration returns the user to Login. |
| CHK-41 | IA-03 | Forgot Password | FR-03 | Going back to step 1 preserves the entered email. |
| CHK-42 | IA-03 | Forgot Password | FR-03 | There is a way back to Login from Forgot Password. |
| CHK-44 | IA-03 | Forgot Password | FR-03 | Step 2 shows a step indicator (for example 2/2). |
| CHK-46 | IA-03 | Profile | FR-04 | The header shows the authenticated state and a working Profile link. |
| CHK-47 | IA-03 | Profile | FR-04 | Logout returns the user to a public page. |
| CHK-69 | IA-03 | Login | FR-02 | Authenticated users are redirected away from /login. |
| CHK-49 | IA-04 | Login | FR-02 | The submit button shows a loading/disabled state while authenticating. |
| CHK-50 | IA-04 | Login | FR-02 | The login error is inline and announced to assistive technology. |
| CHK-51 | IA-04 | Login | FR-02 | The login error text distinguishes wrong credentials, account lockout and network failure. |
| CHK-52 | IA-04 | Login | FR-02 | Successful login gives clear feedback and redirects. |
| CHK-53 | IA-04 | Register | FR-01 | Successful registration gives success feedback before redirecting. |
| CHK-54 | IA-04 | Register | FR-01 | Duplicate-email registration is rejected with a human-readable message. |
| CHK-56 | IA-04 | Register | FR-01 | The submit button shows a loading/disabled state while registering. |
| CHK-57 | IA-04 | Forgot Password | FR-03 | A successful OTP request is shown clearly. |
| CHK-59 | IA-04 | Forgot Password | FR-03 | The invalid-email error is inline and non-blocking. |
| CHK-60 | IA-04 | Forgot Password | FR-03 | Reset success and failure feedback is clear. |
| CHK-61 | IA-04 | Profile | FR-04 | Profile update success is shown inline and announced. |
| CHK-62 | IA-04 | Profile | FR-04 | Order history shows a loading state. |
| CHK-68 | IA-04 | Profile | FR-04 | Order status is conveyed by text, not colour alone. |
