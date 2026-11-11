# HW03 — GUI Usability Testing and Evaluation Report

**Student:** Nguyễn Ngọc Minh Tuấn  
**Student ID:** 23120102  
**Email:** 23120102@student.hcmus.edu.vn  
**Course:** Software Testing (CSC13003)  
**System Under Test:** EShop  
**Selected Requirements:** FR-09 Coupons, FR-10 Order State Machine, FR-11 User Order History, FR-13 Admin Dashboard

---

# 1. Introduction

## 1.1. Background

Usability is an important quality attribute of an e-commerce application because users must be able to understand product prices, apply discounts, complete purchases, and track their orders without unnecessary difficulty or uncertainty.

This assignment evaluates selected GUI features of the EShop application, focusing on four functional requirements:

- **FR-09 — Coupons:** Users can apply discount codes and receive appropriate eligibility and discount feedback.
- **FR-10 — Order State Machine:** Orders follow valid state transitions, including cancellation and delivery-related operations.
- **FR-11 — User Order History:** Users can view their previous orders and understand their current statuses.
- **FR-13 — Admin Dashboard:** Administrators can monitor order information and revenue statistics.

The evaluation combines two complementary activities:

1. **Task 1 — GUI Usability Checklist Evaluation:** A structured checklist is used to inspect the application interface, identify usability problems, and document failures with supporting evidence.
2. **Task 2 — Usability Evaluation:** A task-based evaluation is designed to explore how different hypothetical shoppers interact with the coupon and checkout workflow, interpret feedback, recover from errors, and judge the reliability of the final payable amount.

The assignment also includes cross-platform testing to examine whether the interface behaves consistently across different browsers and devices.

## 1.2. Evaluation Objectives

The overall objectives are:

1. Evaluate the usability and consistency of the selected EShop features.
2. Identify interface problems that may prevent users from completing essential shopping tasks.
3. Examine whether coupon eligibility and discount information are communicated clearly.
4. Evaluate users' ability to understand order information and status changes.
5. Investigate whether the displayed checkout amount creates sufficient confidence before purchase.
6. Document defects systematically and maintain traceability between test cases, screenshots, and GitHub Issues.
7. Prepare a repeatable usability evaluation procedure and analyze the results transparently.

## 1.3. Scope

The evaluation covers the following areas:

| Feature | Requirement | Main evaluation focus |
|---|---|---|
| Coupon application | FR-09 | Coupon input, eligibility, validation, discount calculation, and feedback |
| Checkout and order creation | FR-09 / FR-10 | Final amount, order submission, and checkout consistency |
| Order management | FR-10 | Valid state transitions and cancellation behavior |
| Order history | FR-11 | Order visibility, details, and status comprehension |
| Admin Dashboard | FR-13 | Order counts, revenue calculations, and responsive layout |

The evaluation also considers four general usability inspection areas:

| Inspection area | Focus |
|---|---|
| IA-01 — General UI | Visual consistency, readability, and interface conventions |
| IA-02 — Forms | Labels, input validation, keyboard interaction, and error prevention |
| IA-03 — Navigation | Navigation structure, discoverability, and responsive behavior |
| IA-04 — Feedback and State | Loading indicators, success/error messages, and state visibility |

# 2. Task 1 — GUI Usability Checklist Evaluation

## 2.1. Objective

Task 1 aims to systematically inspect the EShop GUI against predefined usability criteria and determine whether the selected features provide a consistent and understandable user experience.

Unlike task-based usability evaluation, which focuses on how users complete activities, checklist evaluation examines specific interface behaviors and usability requirements.

The main objectives are:

- Identify usability problems in forms, navigation, visual presentation, and feedback.
- Verify whether the application handles normal, invalid, and boundary inputs correctly.
- Evaluate keyboard accessibility and responsive layouts.
- Examine loading, empty, error, and recovery states.
- Identify potential trust issues in checkout and order-related operations.
- Collect reproducible evidence to support bug reports.

## 2.2. Test Methodology

A manual GUI inspection approach was used.

The initial checklist was developed with AI assistance and subsequently reviewed and expanded through manual analysis. Additional checks were introduced to cover cases that might not be captured by an initial AI-generated checklist.

The final checklist contains **80 distinct test items**, each including:

- Test case ID and description.
- Related requirement or usability criterion.
- Preconditions and test procedure.
- Expected result.
- Actual result.
- Execution status.
- Supporting evidence.
- Additional observations or notes.

The checklist was executed through student-run sessions using the Opera browser and the local EShop application.

For each test case, the observed interface behavior was compared with the expected result. Screenshots were collected for failed checks and organized under `evidence/screenshots/`.

Unobserved checks were intended to remain Not Run rather than being marked as passed based on assumptions.

## 2.3. Test Coverage

The 80 checklist items cover several dimensions of GUI usability.

| Coverage area | Examples of inspected behaviors |
|---|---|
| Visual consistency | Currency formatting, text presentation, and layout consistency |
| Form usability | Input labels, placeholders, validation, and keyboard interaction |
| Coupon functionality | Valid codes, invalid codes, minimum-spend thresholds, and discount feedback |
| Checkout confidence | Final payable amount, editable fields, and post-checkout behavior |
| Order management | State transitions, cancellation, and terminal states |
| Order history | Order visibility, details, and status information |
| Dashboard | Revenue calculations and responsive presentation |
| Accessibility | Keyboard navigation and screen-reader-related checks |
| Feedback and recovery | Loading indicators, error messages, and empty states |
| Responsive design | Layout behavior across different viewport sizes |

The checklist was designed to cover both functional correctness and usability characteristics. This distinction is important because an interface may technically accept an operation while still providing confusing or insufficient feedback to the user.

## 2.4. Execution Results

**All 80 checks executed.** The following table summarizes the checklist execution.

| Measure | Result |
|---|---:|
| Total test items designed | 80 |
| Test items executed in live UI | 80 |
| Passed | 61 |
| Failed | 19 |
| Not Run | 0 |
| GitHub Issues created | 12 |
| Source-review candidates | 3 |

The overall pass rate is:

`Pass Rate = 61 / 80 × 100 = 76.25%`

The failure rate is:

`Failure Rate = 19 / 80 × 100 = 23.75%`

**Execution distribution**

| Status | Count | Percentage |
|---|---:|---:|
| Passed | 61 | 76.25% |
| Failed | 19 | 23.75% |
| Not Run | 0 | 0% |
| **Total** | **80** | **100%** |

The results indicate that most inspected interface behaviors met their expected outcomes. However, 19 failed checks reveal several areas that require attention, particularly coupon validation, checkout reliability, order management, and dashboard presentation.

The 12 GitHub Issues represent documented findings selected for issue tracking. They should not be interpreted as a one-to-one count of failed checklist items because multiple checks may relate to the same underlying problem, and some observations may be intentionally excluded from issue reporting.

## 2.5. Detailed Analysis of Failed Checks

The failed checks reveal several recurring usability and interface reliability concerns.

### 2.5.1. Coupon Application and Validation

Several failures relate to how the coupon interface handles user input and eligibility conditions.

Examples include:

| GUI ID | Observed problem | Potential user impact |
|---|---|---|
| GUI-002 | Inconsistent currency formatting | Users may find it harder to compare prices and understand the final amount. |
| GUI-006 | Input accessible name relies only on its placeholder | Assistive technology users may have difficulty identifying the field. |
| GUI-009 | Pressing Enter does not apply the coupon | Keyboard users cannot use an expected interaction method. |
| GUI-017 / GUI-018 / GUI-020 | Coupon rejection at exact threshold conditions | Users may receive unexpected eligibility results even when the cart appears to satisfy the requirement. |

These issues affect both the functional interaction and the user's understanding of the discount process.

In particular, coupon validation should communicate why a code is rejected and what the user needs to change. When threshold conditions are handled inconsistently, users may repeatedly modify their cart without understanding the actual eligibility rule.

The Enter-key issue also demonstrates that usability is not limited to visual presentation. Users may expect familiar keyboard interactions to work consistently.

### 2.5.2. Checkout and Payment Confidence

Two important findings concern the checkout process.

| GUI ID | Observed problem | Potential user impact |
|---|---|---|
| GUI-026 | Checkout total is editable | Users may question whether the displayed payment amount is calculated correctly. |
| GUI-027 | Cart does not clear after successful checkout | Users may mistakenly believe that the order was not completed or may encounter inconsistent cart state. |

GUI-026 is particularly important because the payable amount is one of the most sensitive pieces of information in an e-commerce workflow.

The final total should be derived from trusted order data and validated by the backend. Allowing users to edit the total directly can create uncertainty about whether the displayed amount accurately reflects the products, discounts, and other applicable charges.

GUI-027 may also negatively affect the post-purchase experience. After successfully creating an order, users generally expect the cart to reflect the completed transaction.

These problems suggest that checkout should be evaluated not only for successful order submission but also for the consistency of the information presented before and after purchase.

### 2.5.3. Order Management and State Transitions

Several failures relate to order state management.

| GUI ID | Observed problem | Potential user impact |
|---|---|---|
| GUI-036 / GUI-039 / GUI-045 / GUI-046 / GUI-049 | Invalid or inconsistent order-state transitions and cancellation behavior, such as an action being offered in a state where it should not be allowed | Users or administrators may see order states and available actions that contradict the expected workflow, making order management confusing or unreliable. |
| GUI-060 | Order details are absent | Users have insufficient information to understand an order. |

Order management requires a clearly defined state machine. Each state should permit only valid transitions, while terminal states should not expose operations that contradict the business rules.

For example, once an order has been cancelled, the interface should not offer an action that marks it as delivered.

The absence of order details also reduces transparency because users cannot easily verify what was purchased or understand the information associated with a particular order.

### 2.5.4. Dashboard and Responsive Layout

The evaluation also identified issues affecting the administrator interface.

| GUI ID | Observed problem | Potential user impact |
|---|---|---|
| GUI-031 | Admin layout does not adapt properly to smaller viewport sizes | Administrators may have difficulty accessing dashboard information at smaller viewport sizes. |
| GUI-068 | Dashboard layout is inconsistent across screen sizes | Dashboard content may not be presented consistently across screen sizes. |
| GUI-075 / GUI-077 | Doubled delivered-order revenue observed in the UI | Administrators may receive inaccurate financial information. |

The dashboard is important because administrators rely on its information to monitor business performance.

Incorrect revenue calculations can reduce confidence in the application and may lead to incorrect business decisions.

Responsive layout problems also matter because administrative interfaces should remain usable across supported screen sizes.

**Note:** GUI-068 remains marked as Failed in the checklist but was intentionally excluded from the GitHub bug reports by the author's decision.

### 2.5.5. Feedback and Loading Behavior

GUI-070 identified missing loading feedback.

When an operation requires time to complete, users should receive a visible indication that the system is processing their request.

Without such feedback, users may interpret a delayed response as a failure and attempt the same action repeatedly.

This is particularly important for operations such as checkout, order submission, and administrative state updates.

## 2.6. Source Code Review Candidates

In addition to live UI inspection, source code review identified three implementation-level candidates. They correspond to behaviors also observed in the live UI: the editable checkout total (GUI-026), the doubled delivered-order revenue (GUI-075 / GUI-077), and the invalid order-state transition (Section 2.5.3).

The live UI observations are the runtime evidence for these problems. The source-review findings suggest their likely causes but are not treated as confirmed root causes on their own.

| Candidate | Location | Potential problem | Verification required |
|---|---|---|---|
| Checkout amount is editable | `frontend-web/src/pages/Checkout.jsx` | `editableTotal` is bound to a numeric input and submitted as `total_amount`, although the SRS specifies a derived amount. | Verify the UI and backend handling using controlled order data. |
| Revenue may be doubled | `frontend-admin/src/App.jsx` | Delivered-order revenue calculation multiplies `o.total_amount` by 2. | Verify against known order fixtures and the expected dashboard total. |
| Invalid transition from cancelled to delivered | `frontend-admin/src/App.jsx` | The interface renders a delivery action for cancelled orders, despite cancellation being terminal. | Verify both the UI action and backend state-transition validation. |

These findings are important because source code inspection can reveal implementation risks that are not always immediately visible during manual testing.

However, source code evidence alone does not establish that a defect is reproducible in the running application.

Therefore, the likely causes identified in the source code remain separate from the confirmed runtime findings, and should be verified with controlled order data before being reported as confirmed root causes.

## 2.7. GitHub Issue Tracking and Evidence Management

A total of 12 GitHub Issues were created for the reported findings.

The issue-tracking process helps maintain traceability between:

1. The original checklist observation.
2. The related GUI test case.
3. The screenshot demonstrating the failure.
4. The GitHub Issue describing the problem.

Screenshots for failed checklist checks are stored under:

`evidence/screenshots/`

Screenshots associated with GitHub Issues are stored under:

`evidence/github_issues/`

This separation makes it easier to review the original test evidence and the corresponding bug reports.

The issue-tracking approach also helps prevent duplicate reports for multiple observations that may originate from the same underlying defect.

## 2.8. Task 1 Discussion

The checklist evaluation demonstrates that the EShop application has several usability weaknesses despite passing most of the inspected checks.

The most important concerns are concentrated in three areas:

- **Financial transparency:** Inconsistent currency presentation, coupon eligibility feedback, and an editable checkout total may reduce confidence in the amount users are expected to pay.
- **Workflow consistency:** Invalid order-state transitions and incomplete order information can make the purchase lifecycle difficult to understand.
- **Interface feedback:** Missing loading indicators and responsive layout issues may increase interaction effort and reduce predictability.

The findings also show that usability and functional correctness are closely related.

For example, a coupon may be technically implemented but still be difficult to use if its eligibility rules are not communicated clearly. Similarly, an order may be successfully created but still produce a poor user experience if the cart does not update or the order history does not provide sufficient information.

The checklist therefore provides a useful foundation for investigating the same problems through task-based evaluation in Task 2.

## 2.9. Task 1 Limitations

Several limitations should be considered when interpreting the results:

1. **Browser coverage:** The 80 checklist items were executed using student-run Opera sessions. Cross-browser checks on Chrome and Firefox are described in Section 4, but equivalent behavior on Safari or Android Chrome has not been established.
2. **Human participant coverage:** Checklist execution was performed by the student and does not represent a diverse sample of end-user behavior.
3. **Source review:** The likely causes identified through source review require verification with controlled order data before being treated as confirmed root causes.
4. **Evidence scope:** The report relies on student-supplied execution outcomes and screenshots. Findings should be interpreted within that evidence scope.
5. **Issue selection:** GUI-068 was intentionally excluded from bug reporting even though it remains Failed in the checklist.

These limitations motivate the additional task-based evaluation and cross-platform work described in the following section.

# 3. Task 2 — Usability Evaluation

## 3.1. Objective

Task 2 investigates how different types of online shoppers might interact with the EShop coupon and checkout workflow.

The evaluation focuses on user understanding and confidence rather than only whether the application accepts a valid coupon.

The main research questions are:

1. Can users locate and apply the SAVE10 coupon?
2. Do users understand coupon eligibility and validation feedback?
3. Can users recover when a coupon is rejected?
4. Can users correctly interpret the final payable amount?
5. Does the checkout interface provide sufficient confidence before purchase?
6. Can users find their orders and understand order status changes?

These questions complement Task 1 by examining the potential impact of interface problems from a user-centered perspective.

## 3.2. Evaluation Scenario

The primary task scenario is:

> "You are shopping for household items and have a SAVE10 discount code. Please buy what you need and complete checkout if you can. Think aloud as you go, and tell me what you expect the final amount to be."

The scenario intentionally avoids giving step-by-step navigation instructions.

Participants are expected to decide how to interact with the shopping cart, locate the coupon control, evaluate the displayed discount, and determine whether they are confident enough to proceed.

For the main pilot flow, the planned cart subtotal is 400,000 VND, which is above the SAVE10 minimum-spend requirement of 300,000 VND.

A separate boundary-condition scenario can be used to investigate eligibility feedback at the minimum-spend threshold. This is important because Task 1 identified issues involving exact coupon thresholds.

The primary scenario and boundary-condition scenario should be interpreted separately to avoid mixing different test conditions.

## 3.3. Evaluation Protocol

The planned usability evaluation uses a task-based approach with think-aloud observation.

The moderator provides the scenario and allows the participant to interact with the application independently.

The main procedure is:

1. Introduce the evaluation and explain that the system, not the participant, is being tested.
2. Present the task scenario without explaining where to click.
3. Observe how the participant reviews the cart and applies SAVE10.
4. Record the participant's interpretation of coupon feedback and expected final amount.
5. Observe checkout completion or abandonment.
6. Ask the participant to locate the order and interpret its status.
7. Administer the System Usability Scale (SUS).
8. Ask follow-up questions about clarity, error recovery, speed, and trust.

The moderator should avoid providing hints unless the participant is completely stuck for more than two minutes.

Any hint given should be recorded separately because assisted completion is different from unaided task completion.

## 3.4. Evaluation Instruments

Four instruments are prepared for the usability evaluation.

### 3.4.1. Observation Sheet

The observation sheet records:

- Time and task progression.
- Participant actions and comments.
- Hesitation and frustration.
- Errors and recovery attempts.
- Hints provided by the moderator.
- Related functional requirements or GUI issue IDs.

This instrument helps identify problems that may not be visible from task completion alone.

### 3.4.2. System Usability Scale (SUS)

The SUS questionnaire contains ten statements rated on a five-point Likert scale:

1 = Strongly disagree<br>
2 = Disagree<br>
3 = Neutral<br>
4 = Agree<br>
5 = Strongly agree

The standard SUS calculation is:

- Odd-numbered items: response − 1.
- Even-numbered items: 5 − response.
- Sum the adjusted scores and multiply by 2.5.

The resulting score ranges from 0 to 100.

### 3.4.3. Follow-up Questions

The probe questions cover five dimensions:

| Dimension | Evaluation focus |
|---|---|
| Clarity | Whether the scenario, coupon feedback, and order status are understandable |
| Error recovery | How users respond when something does not work as expected |
| Speed | Whether the interaction feels efficient |
| Trust | Whether users believe the displayed discount and final amount |
| Open feedback | Which interface improvement users would prioritize |

### 3.4.4. Task Results

The task-results sheet records:

- Checkout completion.
- Successful coupon application.
- Understanding of coupon feedback.
- Expected and displayed payable amounts.
- Order-history navigation.
- Order-status comprehension.
- Confidence in the final amount.
- Task completion time.

These measures provide a more detailed view of usability than a single questionnaire score.

## 3.5. Pilot Session

The pilot uses a hypothetical occasional online shopper with moderate digital confidence.

Its purpose is to review:

- Whether the scenario is understandable.
- Whether the coupon and checkout workflow is adequately covered.
- Whether the observation sheet captures important interaction problems.
- Whether the SUS questionnaire and probes are ready for use.
- Whether the task procedure is sufficiently concise.

### 3.5.1. Pilot Results

| Metric | Illustrative result |
|---|---|
| Participant ID | P-00 |
| Profile | Occasional online shopper; moderate digital confidence |
| Coupon application | Successful |
| Understanding of coupon feedback | Partial |
| Expected final amount | 360,000 VND |
| Displayed final amount | 360,000 VND |
| Checkout completion | Completed in the scenario |
| Order history | Order located successfully |
| Order-status understanding | Partial |
| Confidence in final amount | 3/5 |
| SUS score | 50.0 |

The hypothetical participant completes the main purchase flow but shows uncertainty about the discount calculation and order status.

### 3.5.2. Pilot Improvements

Two potential improvements were identified during the rehearsal:

| Potential issue | Planned improvement |
|---|---|
| Coupon feedback may not clearly explain the discount. | Include an observation point for coupon feedback and the participant's expected payable amount. |
| Order status may not be immediately understandable. | Ask participants to explain the meaning of the displayed order status. |

Additional preparation decisions include:

1. Preload the shopping cart to avoid unnecessary browsing.
2. Use a subtotal above the minimum coupon threshold for the primary scenario.
3. Avoid explaining where the coupon control is located.
4. Record hints separately from unaided task completion.

The pilot SUS score of 50.0 is illustrative and must not be included in the seven-session SUS calculation.

## 3.6. Seven Synthetic Usability Sessions

### 3.6.1. Simulation Rationale

The instructor-approved time accommodation is documented as a simulation of seven hypothetical usability sessions.

The sessions represent different shopping habits, digital confidence levels, and attitudes toward payment information.

They are intended to explore possible user interaction patterns and support analysis practice.

The sessions are not real participant studies, and their outcomes must not be interpreted as actual user observations.

### 3.6.2. Hypothetical Participant Profiles and Outcomes

| ID | Hypothetical profile | Path and outcome | SUS |
|---|---|---|---:|
| SIM-01 | Infrequent online shopper; low confidence with checkout forms | Reaches checkout after pausing to locate the cart. Applies the coupon and completes checkout but hesitates over whether the final amount includes the discount. | 40.0 |
| SIM-02 | Frequent online shopper; high digital confidence | Quickly locates the cart and coupon control, understands success feedback, and completes checkout. Prefers a read-only order total. | 75.0 |
| SIM-03 | Occasional shopper; careful about discounts | Encounters a minimum-spend error at the stated threshold, rechecks the total, remains uncertain about eligibility, and stops before checkout. | 50.0 |
| SIM-04 | Mobile-first shopper; moderate confidence | Completes the scenario but expects more prominent coupon feedback and checks the total twice. | 62.5 |
| SIM-05 | Cautious shopper; low tolerance for unclear amounts | Completes most of the flow but hesitates at the editable total and does not feel confident proceeding with payment. | 27.5 |
| SIM-06 | Price-conscious shopper; experienced with coupon codes | Applies the coupon successfully when eligible and completes checkout. Understands the savings but expects clearer minimum-spend information. | 70.0 |
| SIM-07 | Occasional shopper; moderate digital confidence | Completes checkout after manually verifying the arithmetic. The editable total reduces confidence in the final amount. | 47.5 |

The sessions cover a range of hypothetical user characteristics.

SIM-01 and SIM-05 represent users who may require more reassurance when interacting with checkout information.

SIM-02 and SIM-06 represent more experienced shoppers who complete the task more efficiently but still identify opportunities for improvement.

SIM-03 explores the coupon eligibility boundary, while SIM-04 emphasizes the mobile shopping experience.

SIM-07 highlights the relationship between calculation transparency and payment confidence.

### 3.6.3. Task Outcomes

The seven scenarios suggest three broad outcome patterns:

| Outcome pattern | Sessions | Interpretation |
|---|---|---|
| Successful checkout with some usability concerns | SIM-01, SIM-02, SIM-04, SIM-06, SIM-07 | Users can complete the main workflow but may still question the discount or final amount. |
| Checkout interrupted by coupon eligibility uncertainty | SIM-03 | Unclear threshold feedback may prevent users from proceeding. |
| Checkout interrupted by payment confidence concerns | SIM-05 | An editable amount may reduce trust sufficiently to stop the purchase. |

These patterns are illustrative classifications based on the synthetic session descriptions.

They do not represent measured completion rates or observed differences between actual user groups.

## 3.7. SUS Results and Analysis

### 3.7.1. Individual SUS Scores

The seven synthetic sessions produced the following illustrative scores:

| Session | SUS score |
|---|---:|
| SIM-01 | 40.0 |
| SIM-02 | 75.0 |
| SIM-03 | 50.0 |
| SIM-04 | 62.5 |
| SIM-05 | 27.5 |
| SIM-06 | 70.0 |
| SIM-07 | 47.5 |
| **Mean** | **53.2** |

The arithmetic mean is:

`Mean SUS = (40 + 75 + 50 + 62.5 + 27.5 + 70 + 47.5) / 7 = 372.5 / 7 ≈ 53.2`

**Synthetic SUS distribution**

| Score range | Sessions |
|---|---|
| Below 40 | SIM-05 |
| 40–49.9 | SIM-01, SIM-07 |
| 50–59.9 | SIM-03 |
| 60–69.9 | SIM-04 |
| 70 and above | SIM-02, SIM-06 |

The scores range from 27.5 to 75.0, indicating considerable variation across the hypothetical scenarios.

### 3.7.2. Interpretation

The synthetic mean SUS score of 53.2 is used only for analysis practice.

It suggests that the hypothetical users' experiences are mixed rather than consistently positive.

The lower scores in SIM-05, SIM-01, and SIM-07 are consistent with scenarios involving uncertainty about checkout amounts and payment confidence.

The higher scores in SIM-02 and SIM-06 are consistent with hypothetical users who are more comfortable with online shopping and coupon interactions.

However, the scores should not be interpreted as a measured usability rating of the EShop application.

SUS scores are subjective and cannot independently explain the cause of usability problems. They should be considered together with task outcomes, observations, and qualitative feedback.

Furthermore, the synthetic responses were generated for analysis practice and must not be entered into the real `SUS-responses.csv` dataset.

## 3.8. Exploratory Usability Themes

The sessions and Task 1 checklist observations suggest several hypotheses worth investigating.

### Theme 1 — Payment Amount Transparency

The editable checkout total is a potentially significant usability concern.

Users may expect the final amount to be calculated automatically from the product subtotal, discount, and other applicable charges.

If the amount can be edited, users may question whether the system is displaying the correct value.

This concern appears in the hypothetical scenarios of SIM-02, SIM-05, and SIM-07.

The most important implication is that users need to understand not only the final amount but also how that amount was calculated.

**Suggested investigation:**

- Display the original subtotal.
- Show the discount amount separately.
- Clearly identify the final payable amount.
- Prevent unauthorized modification of calculated totals.
- Ensure the backend independently validates the amount.

### Theme 2 — Coupon Eligibility and Error Feedback

Coupon validation should communicate both the result and the reason behind it.

A message indicating that a coupon is invalid or ineligible may not be sufficient if the user cannot determine what needs to change.

SIM-03 illustrates a hypothetical situation where uncertainty about the minimum-spend requirement prevents checkout.

SIM-06 illustrates the expectations of a more experienced coupon user who still wants clearer eligibility information.

**Suggested investigation:**

- Clearly communicate minimum-spend requirements.
- Display understandable validation messages.
- Explain why a coupon was rejected.
- Update the displayed discount and total immediately after successful application.
- Ensure boundary values are handled consistently.

### Theme 3 — Interaction Effort and Repeated Verification

Several hypothetical users repeatedly check the cart and final amount before proceeding.

Although reviewing an order is normal user behavior, repeated verification may indicate that the interface does not communicate the necessary information clearly enough.

This can increase task duration and make checkout feel more complicated.

**Suggested investigation:**

- Improve the visibility of coupon success feedback.
- Keep price information consistent across cart and checkout.
- Reduce unnecessary navigation between screens.
- Provide a clear order summary before confirmation.

### Theme 4 — Differences in Digital Confidence

The hypothetical sessions suggest that shopping experience may influence how users approach the same interface.

Frequent online shoppers may locate familiar controls more quickly, while occasional shoppers may require clearer explanations.

However, this relationship remains an exploratory hypothesis.

The synthetic sessions cannot establish that shopping frequency or digital confidence causes differences in usability outcomes.

## 3.9. Relationship Between Task 1 and Task 2

Task 1 and Task 2 provide complementary perspectives on the selected EShop features.

| Task 1 checklist observation | Related Task 2 exploration |
|---|---|
| GUI-002: Inconsistent currency formatting | Whether users can understand and compare payable amounts |
| GUI-006: Coupon input accessible name | Whether users can identify and interact with the coupon field |
| GUI-009: Enter does not apply coupon | Whether users can use expected keyboard interactions |
| GUI-017 / GUI-018 / GUI-020: Coupon threshold rejection | Whether users understand coupon eligibility and recover from rejection |
| GUI-026: Editable checkout total | Whether users trust the final amount |
| GUI-027: Cart does not clear | Whether users understand whether their purchase was completed |
| GUI-036 / GUI-039 / GUI-045 / GUI-046 / GUI-049: Order-state issues | Whether order operations and statuses are understandable |
| GUI-060: Missing order details | Whether users can obtain sufficient order information |
| GUI-070: Missing loading feedback | Whether users understand that an operation is processing |
| GUI-075 / GUI-077: Doubled delivered revenue | Whether dashboard information is reliable for administrators |

This relationship helps establish traceability between checklist findings and the usability questions explored in Task 2.

Task 1 identifies specific interface problems, while Task 2 examines the possible consequences of those problems for users.

For example, GUI-026 identifies the editable checkout amount as an interface issue. The synthetic scenarios then explore how such behavior might influence users' confidence when deciding whether to complete a purchase.

Similarly, the coupon threshold failures in Task 1 provide a basis for exploring eligibility comprehension and error recovery in SIM-03.

The two tasks therefore complement each other, but the synthetic results do not independently confirm the behavioral impact of the checklist defects.

## 3.10. Task 2 Limitations

The main limitation is that all seven usability sessions are synthetic rather than actual participant sessions.

Consequently:

1. The hypothetical profiles do not represent recruited users.
2. The task outcomes are generated examples rather than observed application interactions.
3. The SUS responses are synthetic and cannot be treated as measured usability data.
4. The mean SUS score of 53.2 is not a valid empirical usability score for the SUT.
5. The exploratory themes are hypotheses that require further validation.
6. No actual screen recordings, participant consent records, or participant quotations were collected.

# 4. Cross-Platform Testing

## 4.1. Objective

Cross-platform testing examines whether the EShop user interface and its interactions remain consistent across different web browsers.

The testing focuses on the four selected functional requirements:

- **FR-09 — Coupons:** Coupon input, application, validation, discount calculation, and feedback.
- **FR-10 — Order State Machine:** Order status presentation and available state-transition actions.
- **FR-11 — User Order History:** Order list, order information, and status visibility.
- **FR-13 — Admin Dashboard:** Dashboard layout, statistic cards, and information presentation.

The GUI checklist developed and executed in Task 1 was reused as the basis for cross-browser testing. This keeps the evaluation criteria consistent and makes it possible to compare browser results with the original checklist baseline.

## 4.2. Testing Environments

The following browser environments were selected:

| Platform | Browser | Operating system |
|---|---|---|
| Platform 1 | Google Chrome | Windows |
| Platform 2 | Mozilla Firefox | Windows |
| Platform 3 | Safari or Android Chrome | Not yet tested |

The same EShop version and selected functional scope were used for the Chrome and Firefox test runs. The checklist criteria and expected results were kept consistent with Task 1.

**Note:** Chrome and Firefox have been tested. The third required environment (Safari or Android Chrome) remains to be completed.

## 4.3. Testing Method

The cross-browser testing followed these steps:

1. Open the EShop application in Google Chrome and verify that the selected screens are accessible.
2. Execute the relevant GUI checklist items for FR-09, FR-10, FR-11, and FR-13.
3. Repeat the same checklist-based inspection in Mozilla Firefox.
4. Compare the observed results with the Task 1 baseline and with the results from the other browser.
5. Record any browser-specific differences in rendering, layout, navigation, form interaction, or feedback.
6. Capture genuine screenshots of the tested application and record the corresponding environment information.
7. Repeat the procedure on Safari or Android Chrome to complete the required third platform.

The checklist was reused rather than redesigned. This approach avoids changing the test criteria between browsers and supports a more meaningful comparison.

## 4.4. Execution Results

### 4.4.1. Google Chrome

The GUI checklist was executed in Google Chrome for the selected requirements FR-09, FR-10, FR-11, and FR-13.

The observed checklist results were generally consistent with the Task 1 baseline. No significant browser-specific differences were identified during the completed checks.

### 4.4.2. Mozilla Firefox

The same GUI checklist criteria were executed in Mozilla Firefox for FR-09, FR-10, FR-11, and FR-13.

The observed results were also generally consistent with the Task 1 baseline and with the Chrome test run. No significant browser-specific differences were identified during the completed checks.

### 4.4.3. Cross-Browser Comparison

Based on the Chrome and Firefox test runs, the selected EShop screens showed generally consistent behavior across the two browsers within the tested scope.

The comparison did not identify significant differences in the inspected interface elements. This does not prove that the application is fully compatible with all browsers or devices; the conclusion is limited to the selected requirements, checklist items, and environments actually tested.

The third platform has not yet been executed, so a complete three-platform conclusion cannot be made at this stage.

## 4.5. Cross-Platform Evidence Register

The following register records the execution status and evidence for each platform.

| Platform | Browser / OS | FR / screen | Result |
|---|---|---|---|
| 1 | Google Chrome / Windows | FR-09, FR-10, FR-11, FR-13 | Executed; results generally consistent with Task 1 |
| 2 | Mozilla Firefox / Windows | FR-09, FR-10, FR-11, FR-13 | Executed; results generally consistent with Task 1 |
| 3 | Safari or Android Chrome | FR-09, FR-10, FR-11, FR-13 | Not Run |

The cross-platform procedure is documented in `cross-platform/README.md`.

## 4.6. Current Status and Remaining Work

| Platform | Execution status |
|---|---|
| Google Chrome | Completed |
| Mozilla Firefox | Completed |
| Safari or Android Chrome | Pending |
| **Total required platforms** | **2/3 completed** |

# 5. Overall Discussion

## 5.1. Main Findings

The combined evaluation identifies several areas that deserve priority.

First, payment transparency is a significant concern. The editable checkout total and unclear coupon feedback may make users uncertain about the amount they are expected to pay.

Second, coupon eligibility needs consistent handling. Threshold conditions should be validated correctly, and error messages should explain how users can resolve the problem.

Third, order management should enforce valid state transitions and provide sufficient information about each order.

Finally, the dashboard should present accurate financial information and remain usable across different screen sizes.

These concerns are supported by different forms of evidence, including live UI checklist results, source-review hypotheses, and synthetic usability scenarios. Their evidence status must remain distinguishable.

## 5.2. Recommended Improvement Priorities

| Priority | Area | Recommended improvement |
|---|---|---|
| High | Checkout amount | Make calculated totals read-only and validate them on the backend. |
| High | Coupon validation | Correct threshold handling and provide clear eligibility feedback. |
| High | Order state machine | Prevent invalid transitions and enforce terminal-state rules. |
| High | Dashboard revenue | Verify revenue calculations against known order fixtures. |
| Medium | Order history | Provide complete order details and understandable status information. |
| Medium | Form accessibility | Provide persistent labels and support keyboard interaction. |
| Medium | Loading feedback | Add clear processing indicators for important operations. |
| Medium | Responsive design | Improve admin layout behavior at smaller screen sizes. |
| Low–Medium | Visual consistency | Standardize currency formatting and interface presentation. |

These priorities are recommendations based on the potential impact of the identified issues. They do not represent a formally measured risk score.

## 5.3. Testing Process Reflection

The assignment demonstrates the importance of combining structured testing techniques.

AI assistance helped generate initial testing ideas and organize the evaluation process. However, the initial suggestions required manual review and expansion to cover additional usability dimensions.

Manual checklist execution provided concrete evidence of interface behavior and helped identify issues that might not be captured by reviewing requirements alone.

Source code inspection provided additional implementation-level hypotheses, but these still require runtime verification.

The synthetic usability sessions allowed the evaluation procedure, questionnaire scoring, and qualitative analysis to be rehearsed under the instructor-approved time accommodation.

The main lesson is that passing functional checks does not automatically guarantee a good user experience. Users also need understandable feedback, predictable interactions, and confidence in the information presented by the application.

# 6. Conclusion

This assignment evaluated the EShop application's selected coupon, checkout, order management, order history, and dashboard features through GUI checklist inspection and a prepared usability evaluation.

Task 1 completed 80 live UI checklist checks, with 61 passing and 19 failing. The findings identified several issues affecting coupon validation, checkout confidence, order-state consistency, responsive presentation, and dashboard reliability. Twelve GitHub Issues were created to document selected findings with supporting screenshots.

Task 2 developed a task-based usability evaluation procedure and used the instructor-approved simulation of seven hypothetical sessions. The synthetic sessions produced an illustrative mean SUS score of 53.2, while the separate pilot produced a score of 50.0.

The analysis highlighted payment transparency, coupon eligibility feedback, interaction effort, and differences in hypothetical digital confidence as areas for further investigation.

These SUS results and usability themes are not empirical findings from real participants and must not be reported as measured user experience.

Cross-platform execution is partially complete: Google Chrome and Mozilla Firefox have been tested, while the third required platform (Safari or Android Chrome) remains pending. The completed Chrome and Firefox runs produced results generally consistent with the Task 1 checklist baseline. The final cross-platform conclusion must be updated after the third platform is tested.

Overall, the assignment provides a structured view of the current EShop GUI quality, documents observed interface failures, and identifies improvements that could make the shopping and administration workflows more understandable, consistent, and trustworthy.

# 7. References

1. HW03 Software Testing assignment specification, supplied by the student.
2. EShop project `README.md`.
3. EShop project `api_specification.md`.
4. Brooke, J. (1996). *SUS: A Quick and Dirty Usability Scale*. In P. W. Jordan, B. Thomas, B. A. Weerdmeester, and A. L. McClelland (Eds.), *Usability Evaluation in Industry*. Taylor & Francis.
5. Student-maintained GUI Usability Checklist workbook and associated execution evidence.
6. Student-maintained GitHub Issues and screenshots under `evidence/github_issues/`.
7. `evidence/sessions/participant_session.md` — synthetic usability session scenarios and illustrative SUS responses.
8. `evidence/sessions/pilot_session.md` — pilot preparation and rehearsal record.
9. `cross-platform/README.md` — cross-platform testing procedure.