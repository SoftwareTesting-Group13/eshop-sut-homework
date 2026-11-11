# Task 2 — Usability Evaluation

## Objective and scenario

Objective: explore how different hypothetical online shoppers might approach finding/applying SAVE10, interpret eligibility feedback, recover from errors, and judge the final payable amount.

Scenario: “You are shopping for household items and have a SAVE10 discount code. Please buy what you need and complete checkout if you can. Think aloud as you go, and tell me what you expect the final amount to be.”

## Synthetic session summaries

| ID | Hypothetical profile | Simulated path and outcome | Illustrative SUS |
|---|---|---|---:|
| SIM-01 | Infrequent online shopper; low confidence with checkout forms | Reaches checkout after pausing to locate the cart. Finds the coupon field, applies the code, and completes the flow. Hesitates over whether the displayed final amount includes the discount. | 40.0 |
| SIM-02 | Frequent online shopper; high digital confidence | Quickly locates the cart and coupon control, understands success feedback, and completes checkout. Wants the order total to be read-only for payment confidence. | 75.0 |
| SIM-03 | Occasional shopper; careful about discounts | Applies SAVE10 at the stated minimum and sees a minimum-spend error. Rechecks the total, remains uncertain about eligibility, and stops before completing checkout. | 50.0 |
| SIM-04 | Mobile-first shopper; moderate confidence | Completes the scenario, but expects the coupon result and savings to be more prominent. Checks the total twice before proceeding. | 62.5 |
| SIM-05 | Cautious shopper; low tolerance for unclear amounts | Completes most of the flow but pauses at the editable total and does not feel confident proceeding with payment. | 27.5 |
| SIM-06 | Price-conscious shopper; experienced with coupon codes | Applies the coupon successfully when the cart is eligible and completes checkout. Understands the savings but expects a clearer explanation of minimum-spend rules. | 70.0 |
| SIM-07 | Occasional shopper; moderate digital confidence | Completes checkout after trying to verify the arithmetic manually. The editable total makes the final amount feel less trustworthy. | 47.5 |

## SUS responses

| ID | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 | Score |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SIM-01 | 3 | 4 | 3 | 3 | 3 | 4 | 3 | 4 | 2 | 4 | 40.0 |
| SIM-02 | 4 | 2 | 4 | 2 | 4 | 2 | 4 | 2 | 4 | 2 | 75.0 |
| SIM-03 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 50.0 |
| SIM-04 | 4 | 3 | 4 | 2 | 4 | 3 | 4 | 3 | 4 | 3 | 62.5 |
| SIM-05 | 2 | 4 | 2 | 4 | 3 | 4 | 2 | 4 | 2 | 4 | 27.5 |
| SIM-06 | 4 | 2 | 3 | 2 | 3 | 2 | 4 | 2 | 4 | 2 | 70.0 |
| SIM-07 | 3 | 3 | 4 | 3 | 3 | 4 | 3 | 4 | 3 | 3 | 47.5 |
| **Mean (synthetic only)** | | | | | | | | | | | **53.2** |

SUS was scored using the standard method: for odd-numbered items subtract 1 from the response; for even-numbered items subtract the response from 5; sum adjusted responses and multiply by 2.5. The mean is arithmetic and applies only to this synthetic dataset. It is not a real usability score for the SUT.

## Exploratory themes and severity hypotheses

These are hypotheses suggested by the simulation and Task 1 observations, not findings from participant sessions.

| Hypothesis | Possible impact | Suggested priority to investigate |
|---|---|---|
| An editable checkout total can undermine confidence in payment arithmetic. | Users may hesitate or distrust the amount. | High |
| Coupon minimum-spend feedback may leave users unsure how to qualify. | Users may retry, abandon, or misunderstand the discount. | Medium |
| Repeatedly checking totals adds effort and slows checkout. | Longer task time and reduced confidence. | Medium |
| Frequent online shoppers may recover more easily than occasional shoppers. | Usability may vary by experience. | Exploratory; validate with actual participants if permitted/required. |

Do not report these as observed participant issues or create new GitHub bugs from the synthetic sessions. Existing confirmed GUI checklist issues remain documented separately.