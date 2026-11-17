# Task 2 — Usability Evaluation Runbook

## Study status

Preparation only. No pilot or participant session has been conducted yet. Do not enter names, contact details, SUS answers, observations, scores, or findings until collected from real people.

## Study objective

Evaluate whether a shopper can complete the selected end-to-end coupon checkout flow, find and apply a discount, understand feedback or errors, recover without moderator coaching, and trust the final payable amount.

### Questions to answer

1. Can participants find the cart and reach checkout without help?
2. Can they locate and apply the supplied coupon, and do they understand the eligibility/result feedback?
3. Do they notice and trust the payable amount? What makes them confident or uncertain?
4. Where do hesitation, errors, or recovery attempts occur?

## Participants

- Run one pilot with one real person first. The pilot is for refining the scenario and procedure; exclude the pilot from the seven scored sessions.
- Recruit seven different real participants for seven moderated sessions.
- Participants must not be enrolled in this HW03 class. Prefer people who shop online and are not IT/test professionals.
- For each scored participant, keep their real name and a verifiable contact method in `evidence/participants.csv`; mask the middle four digits in phone numbers as required by the assignment. Record whether they are outside the class and their target profile.
- Ask separately for consent to screen recording and audio. Do not record audio without consent. Use participant IDs in notes and filenames; avoid placing names/contact details in recordings or screenshots.

## Task scenario for participants

> You are shopping for household items and have a SAVE10 discount code. Please buy what you need and complete checkout if you can. Think aloud as you go, and tell me what you expect the final amount to be.

Moderator setup: use a resettable test account and prepare a cart with a subtotal of at least 300,000 VND. Do not tell participants where the cart, coupon field, or Apply button is, or explain the coupon's minimum spend. Reset cart/order state before each session so participants start from equivalent conditions.

## Session procedure

1. Confirm eligibility and obtain recording consent. Assign an ID (Pilot, then P01–P07).
2. Read the opening script in `evidence/sessions/session-template.md`. Explain that the product is being tested, not the participant, and ask them to think aloud.
3. Present only the scenario above. Observe neutrally; do not point out controls or explain expected behavior. If they are completely stuck, ask “What would you try next?” and record that intervention.
4. Record task outcome (complete / partial / unable), elapsed time, errors, hesitations, recovery actions, and any help given. Record participant quotes only with consent.
5. Immediately after the task, have the participant answer all 10 SUS items in `evidence/sessions/SUS-form.md` (1–5), then ask the open-ended probes listed below.
6. Thank the participant and save notes using their ID. Keep pilot notes separate from scored P01–P07 data.

### Moderator opening script

“Thanks for helping. We are evaluating the website, not you. There are no right or wrong actions. Please think aloud and tell me what you expect as you use it. I will stay quiet unless you are completely stuck. With your permission, I will record the screen [and audio]. You can stop at any time.”

### Post-task probes

- **Clarity:** What was clear or unclear while completing the task?
- **Error recovery:** Did anything go wrong or surprise you? How did you recover?
- **Speed:** Which part felt slow or required extra effort?
- **Trust:** How confident are you that the final amount and discount are correct? Why?
- What would you change first?

## Measures and analysis

For each session record completion, time, number of errors/hesitations, moderator interventions, coupon outcome, and participant confidence/concerns. Score SUS with the standard rule in `SUS-form.md`: odd items response minus 1; even items 5 minus response; sum times 2.5. Preserve raw item answers. Report the seven individual scores and mean; report the pilot separately and do not include it in the seven-session mean.

After all seven sessions, group repeated observations into themes and distinguish isolated functional bugs from broader usability issues. Rank findings by severity using:

- **Critical:** blocks completion or creates a serious payment/trust risk.
- **High:** major confusion or recovery failure; task is possible only with difficulty.
- **Medium:** repeated friction that slows or misleads but does not block completion.
- **Low:** minor clarity or visual issue with little effect on completion.

Only report observations that occurred in real sessions. Link genuine software bugs to the existing GitHub issue or create a new issue with a genuine screenshot. Do not convert a participant preference into a bug without verifying expected behavior.

## Evidence files to complete

- `evidence/participants.csv`: seven eligible, real participants with contact details masked as specified.
- `evidence/sessions/session-template.md`: copy once for Pilot and once per P01–P07; fill during/after each session.
- `evidence/sessions/SUS-responses.csv`: raw responses for P01–P07, plus completion/time summary.
- Screen recordings where consented, stored by participant ID; keep them private and include only as allowed by the assignment.
- `main-report.md`: final seven-session SUS summary, themes, severity-ranked findings, and limitations.

## Recruitment message (adapt before sending)

Hi! I’m doing a short usability study for a university assignment about an online shop checkout. It takes about 10–15 minutes. You’ll try a shopping task on a local test site and answer a short usability questionnaire. There are no right or wrong answers. I’m looking for someone not enrolled in my HW03 class. Screen recording is for study notes; audio is optional and only recorded with your permission. Are you available, and would you be comfortable participating?
