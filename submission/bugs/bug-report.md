# Source-review candidates — runtime verification pending

1. **Checkout total editable (FR-08/09):** `frontend-web/src/pages/Checkout.jsx` binds `editableTotal` to a number input and submits that amount. Expected derived/read-only total and backend recalculation. Potential high integrity impact; verify backend/runtime. Screenshot and issue URL pending.
2. **Delivered revenue doubled (FR-13):** `frontend-admin/src/App.jsx` reducer adds `o.total_amount * 2`. Expected each delivered total once. High metric accuracy impact; verify known fixtures. Screenshot and issue URL pending.
3. **Canceled order offers delivered transition (FR-10):** admin renders “Đánh dấu Đã giao” for canceled status, though canceled is terminal. High state integrity impact; verify backend/runtime. Screenshot and issue URL pending.

Do not publish as confirmed UI bugs until reproduced.
