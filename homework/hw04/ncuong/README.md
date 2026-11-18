# HW04 — AI Automation Testing
**Sinh viên:** Dương Nhật Cường · **MSSV:** 23120223

- Repo: https://github.com/SoftwareTesting-Group13/eshop-sut-homework (nhánh `ncuong`, thư mục `homework/hw04/ncuong`)
- Demo video: <link YouTube unlisted — bổ sung sau khi quay>
- Main report: [reports/main-report.md](reports/main-report.md)
- AI Audit Report: [reports/ai-audit.md](reports/ai-audit.md)
- AI Critique: [reports/ai-critique.md](reports/ai-critique.md)
- Agent Skill: `skills/` (đang xây dựng) + video demo (link bổ sung sau)

## Test summary

| Feature | Pool | TC automated | TC executed | PASS | FAIL | Browser runs | Bugs |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| FR-02 Login and account lockout | A | 16 | 48 | 33 | 15 | 3 | 3 |
| FR-10 Order state machine | B | 16 | 48 | 39 | 9 | 3 | 3 |
| FR-17 Coupon management (CRUD) | C | 18 | 54 | 30 | 24 | 3 | 3 |
| **Tổng** | | **50** | **150** | **102** | **48** | **9** | **9** |

Mọi ca FAIL đều là bug SUT đã xác nhận (16 fail-instance gộp theo root cause thành 9 GitHub Issues #128–#136, mỗi issue có screenshot). Không có test case nào không tự động hóa được (các ca API-only của HW02 chạy bằng request assertion trong cùng spec).

## Cấu trúc

- `tests/` — `fr02-login.spec.ts`, `fr10-orders.spec.ts`, `fr17-coupons.spec.ts`, `helpers/` (JSON loader, eshop-api)
- `data/` — `fr02-login.json`, `fr10-orders.json`, `fr17-coupons.json`
- `playwright.config.ts` — 3 projects, metadata `Run by: 23120223` + ISO timestamp
- `reports/html/<feature>-<browser>/` — 9 HTML report + `report-meta.txt`
- `features/FR*/` — test plan, bug reports + screenshots, `issues/publish.sh`
- `reports/` — main report, AI audit, AI critique (+ PDF khi xuất)

## Bảng tự đánh giá

| No. | Criteria | Điểm tối đa | Điểm tự đánh giá |
| ---: | --- | ---: | --- |
| 1 | Task 1 - Feature A (FR-02) | 25 | |
| 1 | Task 1 - Feature B (FR-10) | 25 | |
| 1 | Task 1 - Feature C (FR-17) | 25 | |
| 2 | Task 2 — Demo video | 15 | |
| 3 | Agent Skills | 10 | |
| **Tổng** | | **100** | |
