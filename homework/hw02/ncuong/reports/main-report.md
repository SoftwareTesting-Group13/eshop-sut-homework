# Báo cáo tổng hợp — Domain Testing và Boundary Value Analysis

## 0. Thông tin sinh viên

| Trường | Giá trị |
| --- | --- |
| Họ và tên | Dương Nhật Cường |
| MSSV | 23120223 |
| Lớp / Nhóm | Kiểm thử phần mềm — CQ2023/3 / Group13 |
| Assignment | HW02 — Domain Testing & BVA |
| GitHub repo (nhóm) | https://github.com/SoftwareTesting-Group13/eshop-sut-homework |

## 1. Feature đã chọn

| Nhóm | Feature | Tình trạng | Báo cáo chi tiết |
| --- | --- | --- | --- |
| A | FR-02 — Login and account lockout | **Đã kiểm thử** (15 ca; 2 bug đã xác nhận, Issue [#25](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/25) & [#26](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/26)) | [`features/FR02/`](../features/FR02/) |
| B | FR-10 — Order state machine | **Đã kiểm thử** (20 ca; 18 PASS, 2 FAIL; 2 bug `BUG-FR10-01/02` đã xác nhận qua UI và mở Issue kèm screenshot) | [`features/FR10/`](../features/FR10/) |
| C | FR-17 — Coupon management (CRUD) | **Đã kiểm thử** (32 ca; 11 PASS, 18 FAIL, 3 Quan sát; 6 bug đã xác nhận qua API bằng ảnh Postman; Issue #47…#52; UI không dùng làm bằng chứng) | [`features/FR17/`](../features/FR17/) |
| D | FR-06 — Product detail view (Mobile) | Chưa thực hiện | — |

Mỗi feature có `domain-analysis.md`, `boundary-analysis.md`, `test-cases.md`, `test-results.md` và `evidence/` trong `../features/<FEATURE_CODE>/`.

## 2. Tổng hợp test case và kết quả

**Run được chọn:** FR-02 `run-20261020-fr02` tại commit `f3162660d5c4f9005cbb15910290adb4b58ef2c7`; FR-10 `run-20261020-fr10` tại commit `09a950cf451428bd8f54542b3f11a0e4b6fdaa91`; FR-17 `run-20261020-fr17` tại commit `f389502cdb308b133fe9044e34505f19202dd887`.

### FR-02 — Login and account lockout

| Chỉ số | Giá trị |
| --- | ---: |
| Test case thiết kế (T-ID duy nhất) | 15 |
| Đã chạy | 15 |
| PASS | 11 |
| FAIL | 3 |
| Quan sát / INCONCLUSIVE | 1 |
| BLOCKED | 0 |
| Chưa chạy | 0 |

Coverage theo nghĩa vụ: EP 9 lớp — thiết kế 9/9, đã chạy 9/9, đạt oracle 7/9; BVA 8 điểm biên — thiết kế 8/8, đã chạy 8/8, đạt oracle 5/8. Chi tiết: [`domain-analysis.md`](../features/FR02/domain-analysis.md), [`boundary-analysis.md`](../features/FR02/boundary-analysis.md), [`test-cases.md`](../features/FR02/test-cases.md), [`test-results.md`](../features/FR02/test-results.md).

### FR-10 — Order state machine

| Chỉ số | Giá trị |
| --- | ---: |
| Test case thiết kế (T-ID duy nhất) | 20 |
| Đã chạy | 20 |
| PASS | 18 |
| FAIL | 2 |
| Quan sát / INCONCLUSIVE | 0 |
| BLOCKED | 0 |
| Chưa chạy | 0 |

Coverage theo nghĩa vụ: EP 20 lớp — thiết kế 20/20, đã chạy 20/20, đạt oracle 18/20; BVA 9 điểm biên (B1 5, B2 2, B3 2) — thiết kế 9/9, đã chạy 9/9, đạt oracle 7/9. Interface: API admin `PUT /api/admin/orders/:id/status` và API user `PUT /api/orders/:id/cancel`. Chi tiết: [`domain-analysis.md`](../features/FR10/domain-analysis.md), [`boundary-analysis.md`](../features/FR10/boundary-analysis.md), [`test-cases.md`](../features/FR10/test-cases.md), [`test-results.md`](../features/FR10/test-results.md).

### FR-17 — Coupon management (CRUD)

| Chỉ số | Giá trị |
| --- | ---: |
| Test case thiết kế (T-ID duy nhất) | 32 |
| Đã chạy | 32 |
| PASS | 11 |
| FAIL | 18 |
| Quan sát / INCONCLUSIVE | 3 |
| BLOCKED | 0 |
| Chưa chạy | 0 |

Coverage theo nghĩa vụ: EP 32 lớp — thiết kế 32/32, đã chạy 32/32, có oracle 29/32 (11 PASS, 18 FAIL), 3 lớp UNRESOLVED/Quan sát; BVA 9 điểm biên (B1 3, B2 3, B3 3) — thiết kế 9/9, đã chạy 9/9, đạt oracle 5/9, dùng lại 9 T-ID EP (0 T-ID BVA-only). Interface: API admin `POST/GET/DELETE` coupon; UI admin mới có hướng dẫn manual; **chỉ dùng bằng chứng Postman/API, không dùng ảnh UI**. Chi tiết: [`domain-analysis.md`](../features/FR17/domain-analysis.md), [`boundary-analysis.md`](../features/FR17/boundary-analysis.md), [`test-cases.md`](../features/FR17/test-cases.md), [`test-results.md`](../features/FR17/test-results.md).

FR-06 chưa có kết quả. Không gán số 0 cho feature chưa thực hiện.

### Tổng hợp case đã thực hiện

| Feature | Thiết kế | Đã chạy | PASS | FAIL | Quan sát | BLOCKED | Chưa chạy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| FR-02 | 15 | 15 | 11 | 3 | 1 | 0 | 0 |
| FR-10 | 20 | 20 | 18 | 2 | 0 | 0 | 0 |
| FR-17 | 32 | 32 | 11 | 18 | 3 | 0 | 0 |
| **Tổng (T-ID duy nhất)** | **67** | **67** | **40** | **23** | **4** | **0** | **0** |

Đã chạy = PASS + FAIL + Quan sát; chỉ cộng T-ID duy nhất của từng feature, không cộng chéo EP/BVA.

## 3. Tổng hợp bug

| Bug ID | Feature | Tóm tắt | Severity | Test case | Trạng thái | Chi tiết |
| --- | --- | --- | --- | --- | --- | --- |
| BUG-FR02-01 | FR02 | Bộ đếm đăng nhập sai tăng 2 thay vì 1 → khóa sau 2 lần sai | High | DT-02, BVA-02, BVA-03 | Đã xác nhận; Issue [#25](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/25) (kèm screenshot) | [`test-results.md`](../features/FR02/test-results.md) |
| BUG-FR02-02 | FR02 | Thời lượng khóa 180 giây thay vì 30 giây | Medium | BVA-02, BVA-06 | Đã xác nhận; Issue [#26](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/26) (kèm screenshot) | [`test-results.md`](../features/FR02/test-results.md) |
| BUG-FR10-01 | FR10 | Admin chuyển được đơn `canceled` sang `delivered` (xuyên trạng thái kết thúc) | Medium | DT-14 | Đã xác nhận qua UI; Issue [#33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33) (kèm screenshot) | [`test-results.md`](../features/FR10/test-results.md) |
| BUG-FR10-02 | FR10 | User tự hủy được đơn đang `shipping` | High | DT-16 | Đã xác nhận qua UI; Issue [#34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34) (kèm screenshot) | [`test-results.md`](../features/FR10/test-results.md) |
| BUG-FR17-01 | FR17 | Backend nhận `code` rỗng/thiếu/chỉ khoảng trắng | Medium | DT-04, DT-05, DT-06 | Đã xác nhận API; Issue [#47](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/47); ảnh Postman | [`test-results.md`](../features/FR17/test-results.md) |
| BUG-FR17-02 | FR17 | Backend nhận `type` ngoài `percent/fixed` hoặc thiếu | Medium | DT-08, DT-09 | Đã xác nhận API; Issue [#48](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/48); ảnh Postman | [`test-results.md`](../features/FR17/test-results.md) |
| BUG-FR17-03 | FR17 | Backend nhận `discount_value <= 0`, không phải số hoặc thiếu | High | DT-10…DT-13 | Đã xác nhận API; Issue [#49](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/49); ảnh Postman | [`test-results.md`](../features/FR17/test-results.md) |
| BUG-FR17-04 | FR17 | Backend nhận `expired_at` thiếu/rỗng/sai định dạng | High | DT-15, DT-16, DT-17 | Đã xác nhận API; Issue [#50](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/50); ảnh Postman | [`test-results.md`](../features/FR17/test-results.md) |
| BUG-FR17-05 | FR17 | Backend nhận `min_order_amount` âm/không phải số/thiếu | Medium | DT-21, DT-22, DT-23 | Đã xác nhận API; Issue [#51](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/51); ảnh Postman | [`test-results.md`](../features/FR17/test-results.md) |
| BUG-FR17-06 | FR17 | Backend nhận `max_uses_per_user < 1` hoặc thiếu; number `0` thành `1` | Medium | DT-26, DT-27, DT-28 | Đã xác nhận API; Issue [#52](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/52); ảnh Postman | [`test-results.md`](../features/FR17/test-results.md) |

**Thống kê severity FR02:** Critical 0 · High 1 · Medium 1 · Low 0 · **Tổng 2**.

**Thống kê severity FR10:** Critical 0 · High 1 · Medium 1 · Low 0 · **Tổng 2** (đã mở Issue #33, #34).

**Thống kê severity FR17:** Critical 0 · High 2 · Medium 4 · Low 0 · **Tổng 6** (6 bug đã xác nhận qua API bằng ảnh Postman; đã mở Issue [#47](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/47)…[#52](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/52); không dùng ảnh UI).

Ảnh xác nhận API: [`features/FR17/screenshots/`](../features/FR17/screenshots/) (34 ảnh Postman, người kiểm thử cung cấp). 6 GitHub Issue đã mở: [#47](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/47), [#48](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/48), [#49](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/49), [#50](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/50), [#51](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/51), [#52](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/52); nội dung draft tại [`features/FR17/issues/`](../features/FR17/issues/).

Hai bug FR-02 và FR-10 đã được người kiểm thử xác nhận qua UI; screenshot đã được đính kèm trong GitHub Issue tương ứng (FR-02: `screenshots/BUG-FR02-01.png`, `BUG-FR02-02.png`; FR-10: `screenshots/BUG-FR10-01-*.png`, `BUG-FR10-02-*.png`). Sáu bug FR-17 đã xác nhận qua **API** bằng ảnh Postman và đã mở Issue #47…#52; chỉ dùng bằng chứng Postman/API, không dùng ảnh UI.

## 4. Tài liệu kèm theo

- Domain/BVA/evidence của FR02: [`features/FR02/`](../features/FR02/); evidence log: [`FR02-evidence.md`](../features/FR02/evidence/FR02-evidence.md).
- Bug + screenshot + GitHub Issue FR02: [#25](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/25), [#26](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/26); nội dung issue: [`features/FR02/issues/`](../features/FR02/issues/).
- Domain/BVA/evidence của FR10: [`features/FR10/`](../features/FR10/); evidence log: [`FR10-evidence.md`](../features/FR10/evidence/FR10-evidence.md).
- Bug + screenshot + GitHub Issue FR10: [#33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33), [#34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34); nội dung issue: [`features/FR10/issues/`](../features/FR10/issues/).
- Domain/BVA/evidence của FR17: [`features/FR17/`](../features/FR17/); evidence log: [`FR17-evidence.md`](../features/FR17/evidence/FR17-evidence.md); driver: [`run-fr17.mjs`](../features/FR17/evidence/run-fr17.mjs). Bug FR17 đã xác nhận API; ảnh tại [`features/FR17/screenshots/`](../features/FR17/screenshots/); **Issue**: [#47](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/47), [#48](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/48), [#49](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/49), [#50](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/50), [#51](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/51), [#52](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/52).
- Quan sát ngoài EP/BVA: [`supporting-materials/fr02-observations.md`](../supporting-materials/fr02-observations.md), [`supporting-materials/fr10-observations.md`](../supporting-materials/fr10-observations.md), [`supporting-materials/fr17-observations.md`](../supporting-materials/fr17-observations.md) (không cộng vào coverage).
- AI Audit Report: [`ai-audit.md`](ai-audit.md).
- AI Critique: [`ai-critique.md`](ai-critique.md) — sinh viên tự viết.
