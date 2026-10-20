# HW02 — Dương Nhật Cường (23120223)

- Yêu cầu bài: [`../docs/2026.HW02.Domain Testing_En.md`](../docs/2026.HW02.Domain%20Testing_En.md)
- Báo cáo chung: [`reports/main-report.md`](reports/main-report.md); [`reports/ai-audit.md`](reports/ai-audit.md) ghi các tương tác AI của các lượt FR02 và FR10; [`reports/ai-critique.md`](reports/ai-critique.md) dành cho sinh viên tự viết.
- Bộ skill cá nhân: [`skills/`](skills/).

## Thứ tự bắt đầu bài HW02

Trước khi đọc bộ skill hoặc đi sâu vào source code, đọc **cả ba** tài liệu từ gốc repo theo thứ tự: [`README.md`](../../../README.md) (rule nghiệp vụ và Expected) → [`api_specification.md`](../../../api_specification.md) (hợp đồng API) → [`homework/hw02/docs/2026.HW02.Domain Testing_En.md`](../docs/2026.HW02.Domain%20Testing_En.md) (phạm vi, EP/BVA và đầu ra).

Sau đó quét cấu trúc repo để tìm ứng dụng, feature, interface và artifact hiện có. Lúc này mới đọc [`README` của bộ skill](skills/README.md), [`domain-testing-workflow/SKILL.md`](skills/domain-testing-workflow/SKILL.md), các skill chuyên biệt và source liên quan. Đọc API spec kể cả khi feature chạy qua UI/mobile; nếu nguồn mâu thuẫn, ghi điểm chưa rõ thay vì suy Expected từ code.

## Trạng thái feature

| Nhóm | Feature | Trạng thái |
| --- | --- | --- |
| A | FR-02 — Login and account lockout | Đã kiểm thử — 15 ca (11 PASS, 3 FAIL, 1 Quan sát); 2 bug đã xác nhận, Issue [#25](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/25) & [#26](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/26) kèm screenshot |
| B | FR-10 — Order state machine | Đã kiểm thử — 20 ca (18 PASS, 2 FAIL); 2 bug đã xác nhận qua UI, Issue [#33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33) & [#34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34) kèm screenshot |
| C | FR-17 — Coupon management (CRUD) | Chưa thực hiện |
| D | FR-06 — Product detail view (Mobile) | Chưa thực hiện |

## Tổng hợp test summary hiện hành

| Feature | Thiết kế | Đã chạy | PASS | FAIL | Quan sát | BLOCKED | Chưa chạy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| FR-02 | 15 | 15 | 11 | 3 | 1 | 0 | 0 |
| FR-10 | 20 | 20 | 18 | 2 | 0 | 0 | 0 |
| **Tổng** | **35** | **35** | **29** | **5** | **1** | **0** | **0** |

- Bug hiện hành: FR-02 và FR-10 đều có 2 bug đã xác nhận qua UI và mở Issue kèm ảnh (FR-02: #25, #26; FR-10: #33, #34).
- Feature đã có kết quả hiện hành: 2/4 (Pool A FR-02, Pool B FR-10); Pool C FR-17 và Pool D FR-06 chưa thực hiện.

## Demo video

- *(chưa có — bổ sung link YouTube demo skill khi nộp)*

## Việc còn lại trước khi nộp

1. ~~Xác nhận 2 bug FR-10 và mở GitHub Issue kèm ảnh~~ — **đã xong** (Issue #33, #34).
2. Hoàn thành FR-17 và FR-06 (Mobile) theo Domain/EP + BVA; không gán số 0 cho feature chưa làm.
3. Sinh viên viết AI Gap Analysis cho FR02/FR10 và `reports/ai-critique.md`; rà soát lại `reports/ai-audit.md` và bổ sung nếu còn tương tác AI khác.
4. Xuất PDF (`main-report`, `ai-audit`, `ai-critique`), tạo `git-commit-log.txt`, đóng gói bài nộp theo yêu cầu HW02; bổ sung bảng tự đánh giá trong README.
