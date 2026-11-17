# Demo video outline (student-recorded)

Target duration: 5–6 minutes. Narrate in Vietnamese and show the real desktop/browser. At the start, show face-cam or run `whoami` and `hostname` in the terminal.

1. **0:00–0:40** Introduce the SUT, selected FRs, and the test structure/data files.
2. **0:40–1:30** Explain one FR-04 case and the spec rule for phone numbers; show the JSON row and spec assertion.
3. **1:30–2:15** Narrate a real review fix: exact matching for the coupon discount amount (the page renders the final amount in multiple places). Show the changed locator and why it prevents ambiguous matches.
4. **2:15–3:35** Run the matrix command and show Chromium, Firefox, and WebKit execution. State that current frontend tests mock API calls and explain the limitation honestly.
5. **3:35–4:30** Open one genuine HTML report. Point out the run annotation and ISO timestamp, then explain one failed assertion as a candidate requiring human triage.
6. **4:30–5:20** Show the FR-15 edit-isolation case and explain the observed behavior without changing or hiding the test result.
7. **5:20–5:45** Summarize automated case counts, report paths, and what still needs live-backend confirmation.

Do not synthesize narration, impersonate authorship evidence, or alter a report after execution. Upload as unlisted and paste the actual YouTube URL into the report/README.
