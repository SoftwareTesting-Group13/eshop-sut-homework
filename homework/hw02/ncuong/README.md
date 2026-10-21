# HW02 — Domain Testing và Boundary Value Analysis

**Sinh viên:** Dương Nhật Cường · **MSSV:** 23120223 · **Nhóm:** Group13

**SUT:** EShop · **Đề bài:** [HW02 Domain Testing](../docs/2026.HW02.Domain%20Testing_En.md)

## Hồ sơ báo cáo

- [Main report — Domain Testing và BVA](reports/main-report.md)
- [AI Audit Report](reports/ai-audit.md) · [AI Critique](reports/ai-critique.md)
- [Agent Skills](skills/)
- [Git commit log](git-commit-log.txt)

| Nhóm | Feature | Phân tích miền | Phân tích biên | Test case | Kết quả |
| --- | --- | --- | --- | --- | --- |
| A | FR-02 — Login and account lockout | [Domain](features/FR02/domain-analysis.md) | [BVA](features/FR02/boundary-analysis.md) | [Catalog](features/FR02/test-cases.md) | [Results](features/FR02/test-results.md) |
| B | FR-10 — Order state machine | [Domain](features/FR10/domain-analysis.md) | [BVA](features/FR10/boundary-analysis.md) | [Catalog](features/FR10/test-cases.md) | [Results](features/FR10/test-results.md) |
| C | FR-17 — Coupon management (CRUD) | [Domain](features/FR17/domain-analysis.md) | [BVA](features/FR17/boundary-analysis.md) | [Catalog](features/FR17/test-cases.md) | [Results](features/FR17/test-results.md) |
| D | FR-06 — Product detail view (Mobile) | [Domain](features/FR06/domain-analysis.md) | [BVA](features/FR06/boundary-analysis.md) | [Catalog](features/FR06/test-cases.md) | [Results](features/FR06/test-results.md) |

## Test summary

**Số feature: 4.** Đếm theo test case ID duy nhất; ca dùng cho cả Domain và BVA chỉ tính một lần. “Đã chạy” gồm PASS, FAIL và Quan sát/INCONCLUSIVE; ca Quan sát đã thực thi nhưng chưa đủ oracle để kết luận. “Chưa chạy” không gồm Quan sát.

| Feature | Thiết kế | Đã chạy | PASS | FAIL | Quan sát | BLOCKED | Chưa chạy | Bug |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| FR-02 | 18 | 18 | 11 | 6 | 1 | 0 | 0 | 4 |
| FR-10 | 23 | 23 | 19 | 4 | 0 | 0 | 0 | 3 |
| FR-17 | 32 | 32 | 11 | 20 | 1 | 0 | 0 | 8 |
| FR-06 | 16 | 16 | 3 | 9 | 4 | 0 | 0 | 2 |
| **Tổng: 4 feature** | **89** | **89** | **44** | **39** | **6** | **0** | **0** | **17** |

**Số bug: 17** (FR-02: 4; FR-10: 3; FR-17: 8; FR-06: 2). Mỗi bug có một GitHub Issue; ID, mức độ, ca liên quan và link Issue nằm trong [bảng bug của main report](reports/main-report.md#51-bug-đã-xác-nhận). Evidence và screenshot được dẫn từ kết quả của từng feature.

## Bảng tự đánh giá

Theo thang điểm trong đề HW02. Cột tự đánh giá để sinh viên điền sau khi rà bản nộp; chưa tự chấm điểm thay sinh viên.

| STT | Tiêu chí | Điểm tối đa | Điểm tự đánh giá |
| ---: | --- | ---: | ---: |
| 1 | Feature A — FR-02 (Domain + Boundary) | 25 | — |
| 2 | Feature B — FR-10 (Domain + Boundary) | 25 | — |
| 3 | Feature C — FR-17 (Domain + Boundary) | 25 | — |
| 4 | Feature D — FR-06 Mobile (Domain + Boundary) | 15 | — |
| 5 | Agent Skills | 10 | — |
| **Tổng** | | **100** | **—** |

## Demo videos

| Nội dung | Link YouTube | Trạng thái |
| --- | --- | --- |
| Demo sử dụng Agent Skills từ đầu đến cuối trên một feature | [Xem video](https://youtu.be/Grs61GfzvQA) | Đã bổ sung link |

## Cần bổ sung trước khi nộp

- Điền điểm tự đánh giá.
- Sinh viên rà soát và chỉnh sửa [AI Critique](reports/ai-critique.md) trước khi nộp.
- Sau khi duyệt Markdown, xuất các PDF theo yêu cầu đề bài.
