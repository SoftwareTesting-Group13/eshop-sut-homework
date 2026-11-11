# Task 2 — Pilot Session (Plan + Record)

## 1. Objectives

1. Check whether the scenario is clear and goal-oriented.
2. Rehearse the cart → coupon → checkout → order history flow.
3. Check whether the testing procedure and instruments are practical.
4. Identify potential improvements before the 7 usability evaluation sessions.

## 2. Scope: flow and FR mapping

| Step | Who | Action | FR |
|---|---|---|---|
| 1 | Participant | Reviews cart and applies SAVE10 | FR-09 |
| 2 | Participant | Completes checkout and places order | FR-08 / FR-10 |
| 3 | Participant | Finds the order and checks its status | FR-10 / FR-11 |
| 4 | Moderator | Changes order status and asks participant to check again | FR-10 |
| 5 | Moderator | Checks Admin Dashboard consistency | FR-13 |

> FR-13 is checked by the moderator because it is an admin feature, not a target-user task.

## 3. Task scenario

> "You have selected the household items you want, and they are in your shopping cart. You have a SAVE10 discount code. Please review your purchase and complete checkout if the total looks right. Afterwards, check what has happened to your order. Think aloud as you go, and tell me what you expect to pay."

## 4. Test setup checklist

- [ ] Local shop and test account are ready.
- [ ] Cart contains household items with a subtotal of **400,000 VND**, above the SAVE10 minimum of 300,000 VND.
- [ ] SAVE10 is active and not expired.
- [ ] Admin account is available in a separate window.
- [ ] Stopwatch and observation sheet are ready.
- [ ] SUS questionnaire and probe questions are prepared.
- [ ] Known Task 1 issues (e.g., GUI-026) are documented separately.

> These are planned setup requirements, not verified execution evidence.

## 5. Moderator script

1. Explain: "We are testing the shop, not you. There are no right or wrong actions. Please think aloud."
2. Ask for recording consent if conducting a real session.
3. Read the scenario once without giving navigation hints.
4. Intervene only if the participant is completely stuck for more than 2 minutes.
5. After the task, administer SUS and ask the probe questions.

## 6. Observation log

| Time | Action / observation | Friction or hesitation | Hint? | Related FR |
|---|---|---|---|---|
| 00:00–02:00 | Reviews the cart and checks the subtotal. | No significant difficulty. | No | FR-09 |
| 02:00–04:00 | Finds the coupon field and applies SAVE10. | Briefly hesitates about whether the discount was applied. | No | FR-09 |
| 04:00–06:00 | Reviews the final amount and completes checkout. | Not completely confident about the discount calculation. | No | FR-08 / FR-10 |
| 06:00–08:00 | Opens order history and locates the order. | Needs some time to understand the order status. | No | FR-10 / FR-11 |
| 08:00–09:00 | Moderator changes order status; participant checks again. | Needs to refresh the page to see the updated status. | No | FR-10 |

## 7. Task results

| Metric | Value |
|---|---|
| Completed checkout without help? | Yes |
| Applied SAVE10 successfully? | Yes |
| Understood coupon feedback? | Partially |
| Expected final amount | 360,000 VND |
| Amount displayed | 360,000 VND (simulated) |
| Found order history? | Yes |
| Understood updated order status? | Partially |
| Confidence in final amount (1–5) | 3 |
| Total task time | 09:00 (simulated task flow; SUS and probes excluded) |
| Admin Dashboard check | Not verified; no actual order was created |

## 8. SUS

Scale: 1 = Strongly disagree; 5 = Strongly agree.

| # | Statement | Response |
|---|---|---:|
| Q1 | I think that I would like to use this system frequently. | 3 |
| Q2 | I found the system unnecessarily complex. | 3 |
| Q3 | I thought the system was easy to use. | 3 |
| Q4 | I think that I would need the support of a technical person to be able to use this system. | 3 |
| Q5 | I found the various functions in this system were well integrated. | 3 |
| Q6 | I thought there was too much inconsistency in this system. | 3 |
| Q7 | I would imagine that most people would learn to use this system very quickly. | 3 |
| Q8 | I found the system very cumbersome to use. | 3 |
| Q9 | I felt very confident using the system. | 3 |
| Q10 | I needed to learn a lot of things before I could get going with this system. | 3 |

**SUS scoring:**

- Odd items: (3−1) × 5 = 10
- Even items: (5−3) × 5 = 10
- SUS = (10 + 10) × 2.5 = **50.0**

> This is a simulated score only. It is excluded from the 7-session SUS mean.

## 9. Probe questions

| Dimension | Answer |
|---|---|
| Clarity | "The overall task was clear, but I was not completely sure whether the coupon had been applied correctly." |
| Error recovery | "I reviewed the cart again to verify the discount and refreshed order history to see the updated status." |
| Speed | "The process was acceptable, although finding the coupon field and checking the order status took some time." |
| Trust | "I wanted a clearer explanation of the discount and a more descriptive order status before fully trusting the result." |
| Open | "I would improve the coupon feedback and make the final payable amount easier to verify." |

## 10. Pilot findings and changes

| # | Potential issue identified | Evidence | Change before subsequent sessions | Done |
|---|---|---|---|---|
| 1 | Coupon feedback may not clearly communicate the discount. | Simulated observation at 02:00–04:00. | Keep a specific observation point for coupon feedback and expected amount. | ☑ |
| 2 | Order status may not be immediately understandable. | Simulated observation at 06:00–09:00. | Ask participants to explain the meaning of the displayed status. | ☑ |

**Planning decisions:**

1. Preload the cart to avoid unnecessary product browsing.
2. Use a subtotal above the SAVE10 minimum for the primary scenario.
3. Do not tell participants where the coupon control is.
4. Record hints separately from unaided task completion.

> Findings above are simulation-based hypotheses, not observed real-user problems.

## 11. Genuine bugs found

| Observation | Systemic or isolated | Severity | GitHub issue link + screenshot |
|---|---|---|---|
| GUI-026: Editable checkout total (previously identified in Task 1). | Previously identified; requires separate verification. | Refer to Task 1 classification. | Reference existing Task 1 issue; do not duplicate. |
| No new genuine bugs confirmed. | N/A | N/A | N/A |

> Simulated observations are not sufficient evidence for creating new GitHub bug reports.