# Example instantiation: EShop HW04 (FR-02 / FR-10 / FR-17)

This is one proven instantiation of the skill — not part of the skill itself.

## Context

- App: EShop demo shop. Web `http://localhost:5173`, admin `http://localhost:5174`, API `http://localhost:3000/api`. Playwright 1.65, `fullyParallel: false`.
- Catalogs: per-feature confirmed tables with `DT-*`/`BVA-*` IDs.
- Real-DOM facts found by reading source (never assumed): login labels not wired to inputs (use ordered textboxes); admin order rows expose per-status buttons; coupon form uses placeholders with an auto-uppercase code field.
- Backend facts found by reading source: wrong-password counter `+2` (spec: `+1`); lockout 180 s (spec: 30 s); `password: null` passes an `===` check and issues a JWT; order transitions `canceled→delivered` and user-cancel-while-`shipping` allowed; admin APIs never check `role`; coupon `POST` validates nothing.

## Results

| Feature | Cases | Pass / fail per browser | Browsers |
| --- | --- | --- | --- |
| Login + lockout | 16 (2 P / 7 N / 7 E) | 11 / 5 | chromium, firefox, webkit |
| Order state machine | 16 (7 P / 7 N / 2 E) | 13 / 3 | chromium, firefox, webkit |
| Coupon CRUD | 18 (9 P / 8 N / 1 E) | 10 / 8 | chromium, firefox, webkit |

Totals: 50 cases, 150 runs, 102 passed / 48 failed, 9 browser runs, 9 root-cause bug reports with screenshots and tracker issues.

## How the skill was applied

1. Test plans first (`test-plan-automation.md` per feature, ≥12 rows each, UI-automatable column).
2. One skeleton + one sample test, verified on chromium before expanding.
3. JSON data files (`fr02-login.json`, `fr10-orders.json`, `fr17-coupons.json`); specs read rows only.
4. Batches of 1–2 cases with an immediate chromium run; fixes: label-free locators, `waitForEvent('dialog')`, await-PUT-before-assert, deterministic actual-then-spec asserts, per-run unique data with `try/finally` cleanup.
5. Three browsers per feature with per-run report folders + sidecar metadata; signatures identical across browsers.
6. Gap table, 9 bug reports + evidence, one issue per root cause, per-concern commits (8 spec-touching commits).
