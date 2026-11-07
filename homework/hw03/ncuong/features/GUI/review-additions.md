# Review additions — items the AI missed

The initial AI set had **44 items**. During the critical review, **25 items** were added. Each row states why the initial AI pass missed it.

| ID | IA | Screen | Added item | Why the AI missed it |
| --- | --- | --- | --- | --- |
| CHK-02 | IA-01 | Login | The browser tab title is unique and describes the Login page. | The AI checklist focused on the visible page and ignored browser chrome (tab title). |
| CHK-06 | IA-01 | Register | The browser tab title is unique and describes the Register page. | Same blind spot as CHK-02: document.title is outside the rendered body. |
| CHK-07 | IA-01 | Register | Helper text and the primary button meet WCAG 2.2 AA contrast (4.5:1 normal text). | The AI item said “sufficient contrast” but did not compute ratios; axe-core found two failures. |
| CHK-10 | IA-01 | Forgot Password | The browser tab title is unique and describes the Forgot Password page. | Same blind spot as CHK-02: document.title is outside the rendered body. |
| CHK-13 | IA-01 | Profile | The Profile page has exactly one h1 and a logical heading hierarchy. | The AI item treated headings as typography, not as a semantic outline; it did not check h1/h2 structure. |
| CHK-14 | IA-01 | Profile | The browser tab title is unique and describes the Profile page. | Same blind spot as CHK-02: document.title is outside the rendered body. |
| CHK-15 | IA-01 | Profile | The order-history table remains usable at 360px without page-level horizontal scrolling. | The AI responsiveness item was generic (“mobile usable”) and did not test a data table with real columns. |
| CHK-16 | IA-01 | Profile | Profile text and order-status badges meet WCAG 2.2 AA contrast. | Same as CHK-07: the AI did not compute contrast for status badges and header text. |
| CHK-65 | IA-01 | All auth screens | The layout remains usable when the document direction is RTL. | The AI checklist had no RTL item; the model defaulted to LTR assumptions. |
| CHK-66 | IA-01 | All auth screens | Text remains legible when the operating system uses dark mode. | The AI checklist had no dark-mode item; the model assumed the light theme is the only theme. |
| CHK-67 | IA-01 | All auth screens | Content reflows at 200% zoom (640 CSS px) without horizontal scrolling. | The AI checklist had no 200% zoom/reflow item (WCAG 1.4.10). |
| CHK-19 | IA-02 | Login | Every input has a programmatically associated label. | The AI checked that labels are visible, not that they are programmatically associated (for/id or aria-label). |
| CHK-23 | IA-02 | Register | The password rule text matches the implemented validation. | The AI did not compare the displayed password rule with the actual regex; the contradiction only appears when both are read together. |
| CHK-26 | IA-02 | Forgot Password | The OTP field restricts input to four digits (inputmode/maxlength/pattern). | The AI missed the domain-specific OTP constraints (4 digits, numeric keypad, maxlength). |
| CHK-31 | IA-02 | Profile | Phone validation feedback is inline and associated with the field. | The AI checked that a phone error exists, not where/how it is shown or whether the regex accepts real Vietnamese numbers. |
| CHK-32 | IA-02 | Profile | All Profile labels are programmatically associated with their inputs. | Same as CHK-19: visible labels were counted as sufficient. |
| CHK-34 | IA-03 | Login | The Forgot Password link uses client-side routing and does not reload the document. | The AI did not distinguish a raw <a href> reload from React Router navigation. |
| CHK-36 | IA-03 | Login | Keyboard tab order follows the visual order. | The AI did not execute a keyboard-only tab-order test; tabindex="1" is invisible in a screenshot. |
| CHK-43 | IA-03 | Forgot Password | Focus moves to the new step's first field after a step transition. | The AI missed dynamic focus management after a client-side step transition. |
| CHK-45 | IA-03 | Profile | Unauthenticated access to /profile redirects to Login with a return path. | The AI did not test the unauthenticated route guard or the return path. |
| CHK-48 | IA-03 | Profile | The current page is indicated in navigation. | The AI did not check current-page indication (aria-current/active state). |
| CHK-55 | IA-04 | Register | Server errors do not expose technical details. | The AI did not test a server-error path and therefore missed raw error leakage. |
| CHK-58 | IA-04 | Forgot Password | The OTP is not exposed in the UI. | The AI treated the OTP message as helpful feedback and did not flag it as a security/privacy defect. |
| CHK-63 | IA-04 | Profile | Order-history errors are distinguished from an empty list. | The AI checked the empty state but not whether an error is distinguishable from an empty list. |
| CHK-64 | IA-04 | Profile | The cancel-order action asks for confirmation before executing. | The AI missed destructive-action confirmation and the shipping-order edge case. |
