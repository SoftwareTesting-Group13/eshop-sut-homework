# HW02 — Dương Nhật Cường (23120223)

- Yêu cầu bài: [`../docs/2026.HW02.Domain Testing_En.md`](../docs/2026.HW02.Domain%20Testing_En.md)
- Báo cáo chung: [`reports/main-report.md`](reports/main-report.md); [`reports/ai-audit.md`](reports/ai-audit.md) ghi các tương tác AI của các lượt FR02, FR10 và FR17; [`reports/ai-critique.md`](reports/ai-critique.md) dành cho sinh viên tự viết.
- Bộ skill cá nhân: [`skills/`](skills/).

## Thứ tự bắt đầu bài HW02

Trước khi đọc bộ skill hoặc đi sâu vào source code, đọc **cả ba** tài liệu từ gốc repo theo thứ tự: [`README.md`](../../../README.md) (rule nghiệp vụ và Expected) → [`api_specification.md`](../../../api_specification.md) (hợp đồng API) → [`homework/hw02/docs/2026.HW02.Domain Testing_En.md`](../docs/2026.HW02.Domain%20Testing_En.md) (phạm vi, EP/BVA và đầu ra).

Sau đó quét cấu trúc repo để tìm ứng dụng, feature, interface và artifact hiện có. Lúc này mới đọc [`README` của bộ skill](skills/README.md), [`domain-testing-workflow/SKILL.md`](skills/domain-testing-workflow/SKILL.md), các skill chuyên biệt và source liên quan. Đọc API spec kể cả khi feature chạy qua UI/mobile; nếu nguồn mâu thuẫn, ghi điểm chưa rõ thay vì suy Expected từ code.

## Trạng thái feature

| Nhóm | Feature | Trạng thái |
| --- | --- | --- |
| A | FR-02 — Login and account lockout | Đã kiểm thử — 15 ca (11 PASS, 3 FAIL, 1 Quan sát); 2 bug đã xác nhận, Issue [#25](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/25) & [#26](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/26) kèm screenshot |
| B | FR-10 — Order state machine | Đã kiểm thử — 20 ca (18 PASS, 2 FAIL); 2 bug đã xác nhận qua UI, Issue [#33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33) & [#34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34) kèm screenshot |
| C | FR-17 — Coupon management (CRUD) | Đã kiểm thử — 32 ca (11 PASS, 20 FAIL, 1 Quan sát); 8 bug đã xác nhận API, Issue #47…#54; 39 ảnh Postman + 1 ảnh UI bổ sung cho BUG-08, phủ 19/20 FAIL; bằng chứng chính là API |
| D | FR-06 — Product detail view (Mobile) | Chưa thực hiện |

## Tổng hợp test summary hiện hành

| Feature | Thiết kế | Đã chạy | PASS | FAIL | Quan sát | BLOCKED | Chưa chạy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| FR-02 | 15 | 15 | 11 | 3 | 1 | 0 | 0 |
| FR-10 | 20 | 20 | 18 | 2 | 0 | 0 | 0 |
| FR-17 | 32 | 32 | 11 | 20 | 1 | 0 | 0 |
| **Tổng** | **67** | **67** | **40** | **25** | **2** | **0** | **0** |

- Bug hiện hành: FR-02 và FR-10 đều có 2 bug đã xác nhận qua UI và mở Issue kèm ảnh (FR-02: #25, #26; FR-10: #33, #34). FR-17 có 8 bug đã xác nhận API (3 High, 5 Medium); 39 ảnh Postman + 1 ảnh UI bổ sung tại [`features/FR17/screenshots/`](features/FR17/screenshots/) phủ 19/20 FAIL (chỉ còn `DT-06` chưa có ảnh API). 8 bug đã mở Issue [#47](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/47)…#[54](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54); 2 bug mới `BUG-FR17-07/08` có Issue [#53](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/53)/[#54](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54) ([BUG-FR17-07](features/FR17/issues/BUG-FR17-07.md), [BUG-FR17-08](features/FR17/issues/BUG-FR17-08.md)). Bằng chứng chính là Postman/API; ảnh UI chỉ bổ sung hệ quả `BUG-FR17-08`.
- Feature đã có kết quả hiện hành: 3/4 (Pool A FR-02, Pool B FR-10, Pool C FR-17); Pool D FR-06 chưa thực hiện.

## Demo video

- *(chưa có — bổ sung link YouTube demo skill khi nộp)*

## Việc còn lại trước khi nộp

1. ~~Xác nhận 2 bug FR-10 và mở GitHub Issue kèm ảnh~~ — **đã xong** (Issue #33, #34).
2. ~~Xác nhận 8 bug FR-17 qua Postman và mở GitHub Issue kèm ảnh~~ — **đã xong** (Issue #47…#54; bằng chứng chính là ảnh Postman; 1 ảnh UI bổ sung hệ quả `BUG-FR17-08`). 2 bug mới `BUG-FR17-07/08` đã publish tại [#53](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/53)/[#54](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54); `DT-06` vẫn là ca FAIL duy nhất chưa có ảnh API.
3. Hoàn thành FR-06 (Mobile) theo Domain/EP + BVA; không gán số 0 cho feature chưa làm.
4. Sinh viên viết AI Gap Analysis cho FR02/FR10/FR17 và `reports/ai-critique.md`; rà soát lại `reports/ai-audit.md` và bổ sung nếu còn tương tác AI khác.
5. Xuất PDF (`main-report`, `ai-audit`, `ai-critique`), tạo `git-commit-log.txt`, đóng gói bài nộp theo yêu cầu HW02; bổ sung bảng tự đánh giá trong README.
