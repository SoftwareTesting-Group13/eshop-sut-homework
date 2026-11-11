# Task 3 – Cross-Browser / Cross-Platform Testing

## 1. Objective

The objective of this task is to evaluate the consistency and compatibility of the EShop user interface across different web browsers.

The testing focuses on identifying potential differences in layout, visual presentation, navigation, form behavior, and user feedback across browsers.

The testing scope covers the four functional requirements selected in Task 1:

- **FR-09:** Discount Coupons
- **FR-10:** Order State Machine
- **FR-11:** Order History View (User)
- **FR-13:** Dashboard (Admin)

## 2. Testing Environment

The same EShop application and GUI checklist developed in Task 1 were used throughout the cross-browser testing process.

The following browsers were used:

| Platform | Browser | Operating System |
|---|---|---|
| Platform 1 | Google Chrome | Windows 11 |
| Platform 2 | Mozilla Firefox | Windows 11 |
| Platform 3 | Opera GX | Windows 11 |

The application was tested using the same functional scope and test conditions to ensure consistency when comparing results across browsers.

## 3. Testing Approach

The GUI checklist from Task 1 was reused without changing its original testing objectives or expected results.

The testing covered the following interface aspects:

- **IA-01 – General UI Standards:** Layout consistency, text readability, alignment, spacing, and visual presentation.
- **IA-02 – Forms:** Input fields, buttons, validation messages, and form interactions.
- **IA-03 – Navigation:** Navigation links, page transitions, and accessibility of interface elements.
- **IA-04 – Feedback / State:** Success and error messages, loading indicators, and order status presentation.

The same checklist items were executed on Google Chrome and Mozilla Firefox.

The results from both browsers were compared with the baseline results recorded in Task 1 to identify browser-specific inconsistencies.

## 4. Test Results and Observations

### 4.1 Google Chrome

The GUI checklist was executed on Google Chrome across the selected functional requirements (FR-09, FR-10, FR-11, and FR-13).

The observed results were generally consistent with those recorded during Task 1. No significant browser-specific differences were identified in the tested interface elements.

### 4.2 Mozilla Firefox

The same GUI checklist was executed on Mozilla Firefox using the same testing scope.

The observed results were similar to those obtained in Task 1 and on Google Chrome. The tested interface elements generally maintained consistent visual presentation and interaction behavior.

### 4.3 Cross-Browser Comparison

Based on the executed tests, Google Chrome and Mozilla Firefox produced generally consistent results across the selected functional requirements.

No significant differences were observed in the tested GUI checklist items. The comparison did not reveal any additional browser-specific issues during these test sessions.

This finding is limited to the tested screens, interactions, and environments.

## 5. Conclusion

The cross-browser testing demonstrated that the selected EShop interfaces behaved consistently across Google Chrome and Mozilla Firefox within the tested scope.

Reusing the GUI checklist from Task 1 allowed the same interface criteria to be evaluated across multiple browsers, making the comparison more systematic and consistent.

The testing results provide evidence of the application's interface consistency across the two tested browser environments.