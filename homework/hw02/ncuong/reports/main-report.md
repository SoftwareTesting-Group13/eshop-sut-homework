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
| A | FR-02 — Login and account lockout | **Đã kiểm thử** (15 ca; 2 bug đã xác nhận và mở Issue #23, #24) | [`features/FR02/`](../features/FR02/) |
| B | FR-10 — Order state machine | Chờ làm lại | — |
| C | FR-17 — Coupon management (CRUD) | Chưa thực hiện | — |
| D | FR-06 — Product detail view (Mobile) | Chưa thực hiện | — |

Mỗi feature có `domain-analysis.md`, `boundary-analysis.md`, `test-cases.md`, `test-results.md` và `evidence/` trong `../features/<FEATURE_CODE>/`.

## 2. Tổng hợp test case và kết quả

**Run được chọn:** `run-20261020-fr02`; SUT commit `f3162660d5c4f9005cbb15910290adb4b58ef2c7`.

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

FR-10, FR-17 và FR-06 chưa có kết quả; không gán số 0 cho các feature chưa thực hiện.

## 3. Tổng hợp bug

| Bug ID | Feature | Tóm tắt | Severity | Test case | Trạng thái | Chi tiết |
| --- | --- | --- | --- | --- | --- | --- |
| BUG-FR02-01 | FR02 | Bộ đếm đăng nhập sai tăng 2 thay vì 1 → khóa sau 2 lần sai | High | DT-02, BVA-02, BVA-03 | Đã xác nhận; Issue [#23](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/23) (kèm screenshot) | [`test-results.md`](../features/FR02/test-results.md) |
| BUG-FR02-02 | FR02 | Thời lượng khóa 180 giây thay vì 30 giây | Medium | BVA-02, BVA-06 | Đã xác nhận; Issue [#24](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/24) (kèm screenshot) | [`test-results.md`](../features/FR02/test-results.md) |

**Thống kê severity FR02:** Critical 0 · High 1 · Medium 1 · Low 0 · **Tổng 2**.

Cả hai bug đã được người kiểm thử xác nhận; screenshot (`screenshots/BUG-FR02-01.png`, `screenshots/BUG-FR02-02.png`) đã được đính kèm trong GitHub Issue tương ứng.

## 4. Tài liệu kèm theo

- Domain/BVA/evidence của FR02: [`features/FR02/`](../features/FR02/); evidence log: [`FR02-evidence.md`](../features/FR02/evidence/FR02-evidence.md).
- Bug + screenshot + GitHub Issue: [#23](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/23), [#24](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/24); nội dung issue: [`features/FR02/issues/`](../features/FR02/issues/).
- Quan sát ngoài EP/BVA: [`supporting-materials/fr02-observations.md`](../supporting-materials/fr02-observations.md) (không cộng vào coverage).
- AI Audit Report: [`ai-audit.md`](ai-audit.md).
- AI Critique: [`ai-critique.md`](ai-critique.md) — sinh viên tự viết.
