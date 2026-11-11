# Bug Report — Live UI Findings

Execution environment: student-run Opera session on the local EShop SUT. Findings are based on checklist outcomes and screenshots supplied by the student. Twelve GitHub Issues have been created; GUI-068 is intentionally excluded from this bug report at the student’s request. Issue-page captures are stored in `evidence/github_issues/`.

## Confirmed findings

| Candidate | Checklist | Observation | Evidence |
|---|---|---|---|
| BUG-CANDIDATE-01 — Coupon accessible name uses placeholder | GUI-006 | Accessibility pane reports the placeholder as computed name; no explicit label/ARIA name is exposed. | `evidence/screenshots/GUI-006_coupon-accessible-name.png` |
| BUG-CANDIDATE-02 — Enter does not apply coupon | GUI-009 | Enter in coupon input has no effect; Apply button works. | User report |
| BUG-CANDIDATE-03 — Exact minimum coupon threshold rejected | GUI-017/018/020 | SAVE10 at 300,000 and BIGBUY at 500,000 VND are rejected although equal to the configured minimum. | `GUI-017-018_save10-boundary.png`; `GUI-020_bigbuy-boundary.png` |
| BUG-CANDIDATE-04 — Checkout amount formatting inconsistent | GUI-002 | Raw integer total lacks grouping and currency formatting used elsewhere. | `GUI-002_currency-format.png` |
| BUG-CANDIDATE-05 — Checkout total is user-editable | GUI-026 | A 28,000,000 VND item was paired with a manually altered, extremely large total. | `GUI-026_editable-checkout-total.png` |
| BUG-CANDIDATE-06 — Cart persists after successful order | GUI-027 | Order succeeded but cart was not cleared. | User report |
| BUG-CANDIDATE-07 — Admin orders responsive layout clips | GUI-031 | At 360px, table columns and actions do not fit/reflow. | `GUI-031_orders-responsive-overflow.png` |
| BUG-CANDIDATE-08 — Canceled orders can be marked delivered | GUI-036/045/049 | Canceled rows still show the delivery action; activating it changes canceled status to delivered. | `GUI-036-049_canceled-row-action.png`; `GUI-045_canceled-before.png`; `GUI-045_canceled-to-delivered-after.png` |
| BUG-CANDIDATE-09 — Customer can cancel while order is shipping | GUI-039/046 | Customer cancellation succeeded while the order was in shipping. | `GUI-039-046_shipping-before.png`; `GUI-039-046_cancel-success.png` |
| BUG-CANDIDATE-10 — Order history lacks details view | GUI-060 | No order details action/view was available from history. | `GUI-060_history-no-detail.png` |
| BUG-CANDIDATE-12 — No loading indicator | GUI-070 | No progress/loading indicator appeared during the checked operation. | User report |
| BUG-CANDIDATE-13 — Delivered revenue doubled | GUI-075/077 | Dashboard showed 88,000,000 VND for delivered orders totaling 44,000,000 VND. GUI-077 used different fixture values from its checklist procedure. | `GUI-075-077_revenue-double-count.png` |

## GitHub issue evidence

Screenshots of the 12 created GitHub issues are stored in `evidence/github_issues/`: `GUI-002.png`, `GUI-006.png`, `GUI-009.png`, `GUI-017-018-020.png`, `GUI-026.png`, `GUI-027.png`, `GUI-031.png`, `GUI-036-045-049.png`, `GUI-039-046.png`, `GUI-060.png`, `GUI-070.png`, and `GUI-075-077.png`.

## Consolidation notes

GUI-036, GUI-045 and GUI-049 are evidence of one terminal-state defect. GUI-039 and GUI-046 describe the same cancellation rule defect. GUI-075 and GUI-077 concern the same revenue calculation. Consider filing consolidated issues to avoid duplicates.
