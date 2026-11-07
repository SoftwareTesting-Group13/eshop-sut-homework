# AI Critique

**Draft — student review required before submission.**

The AI was useful for breadth but unreliable as an oracle. In this assignment it expanded the `ui-checklist-generator` skill's eight categories into 44 plausible checklist items very quickly, and it wrote consistent Markdown, Excel and bug-report artifacts. However, it was wrong or incomplete in exactly the places that matter for a GUI review. It treated visible `<label>` text as an accessible label and missed the missing `for`/`id` associations; it said “check contrast” without computing a ratio, while axe-core found 2.53:1 and 3.76:1 failures. It assumed LTR, light mode and 100% zoom, so RTL, dark mode and 200% reflow only appeared after I added them. It also read “Mã OTP của bạn là: …” as helpful feedback rather than a password-reset takeover vector, and it did not test keyboard tab order, SPA reloads, route guards, loading-versus-error states, or destructive-action confirmation.

Three causes explain these misses. First, my prompt asked for a checklist, not for an executable oracle per item, so the AI produced broad statements that could not be marked pass/fail. Second, the model cannot execute the SUT: it cannot press Tab, delay a request, intercept a 500 response, or inspect `document.activeElement`. Third, the model defaults to the visual happy path and to the developer's assumptions (LTR, light theme, visible labels, “feedback exists” equals “feedback is good”).

The principle I learned is that AI is a candidate generator, not evidence. The human must define the oracle, run the edge cases, and challenge accessibility and security assumptions. AI output becomes trustworthy only after execution and review.

<!-- Word count target: 200–300 words. -->
