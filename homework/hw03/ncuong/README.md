# HW03 — GUI & Usability

**Sinh viên:** Dương Nhật Cường · **MSSV:** 23120223 · **Nhóm:** Group 13
**SUT:** EShop · **Đề bài:** [HW03 GUI & Usability](../docs/2026.HW03.GUI_Usability_En.md)
**Trạng thái:** Task 1 đã hoàn thiện; Task 2 và Task 3 chưa bắt đầu.

## Hồ sơ báo cáo

- [Báo cáo chính](reports/main-report.md)
- [AI Audit Report](reports/ai-audit.md)
- [AI Critique](reports/ai-critique.md)
- [GUI checklist — Markdown, 66 item](features/GUI/checklist.md)
- [GUI checklist — Excel, 66 item](features/GUI/checklist.xlsx)
- [Test summary](features/GUI/test-summary.md)
- [Checklist AI sinh ban đầu + 25 item bổ sung/sửa sau review](features/GUI/ai-checklist-and-review.md)
- [Bug report — 26 bug](features/GUI/bug-report.md)
- [Báo cáo bug riêng lẻ](features/GUI/bugs/)
- [GitHub Issues (đã publish #80–#105)](features/GUI/issues/)
- [Screenshot — chỉ item Failed](features/GUI/screenshots/)
- [Agent Skills](skills/)

## Phạm vi Task 1

| FR | Màn hình | Interface aspects |
| --- | --- | --- |
| FR-01 Account registration | `/register` | IA-01…IA-04 |
| FR-02 Login and account lockout | `/login` | IA-01…IA-04 |
| FR-03 Forgot password and reset | `/forgot-password` | IA-01…IA-04 |
| FR-04 Profile management | `/profile` | IA-01…IA-04 |

## Test summary

| Metric | Value |
| --- | ---: |
| Screens tested | 4 |
| End-to-end flows tested | 0 (Task 2 chưa bắt đầu) |
| Checklist items designed | 66 |
| Checklist items executed | 66 |
| Passed | 27 |
| Failed | 39 |
| Bugs reported | 26 |
| Blockers | 1 |
| Major | 11 |
| Minor | 14 |
| Screenshots | 38 PNG cho 39 item Failed (một số ảnh dùng chung) |
| Participants | 0 (Task 2 chưa bắt đầu) |
| Demo videos | 0 (sẽ quay khi hoàn thiện Agent Skill) |

| Interface aspect | Items | Passed | Failed |
| --- | ---: | ---: | ---: |
| IA-01 General UI standards | 18 | 7 | 11 |
| IA-02 Forms | 17 | 4 | 13 |
| IA-03 Navigation | 15 | 9 | 6 |
| IA-04 Feedback / state | 16 | 7 | 9 |
| **Total** | **66** | **27** | **39** |

**Phân nguồn:** 41 item AI sinh ban đầu được giữ + 25 item bổ sung/sửa sau review. Danh sách 25 item, lý do AI bỏ sót và bộ AI ban đầu nằm ở [`features/GUI/ai-checklist-and-review.md`](features/GUI/ai-checklist-and-review.md).

**Môi trường thực thi:** backend `http://localhost:3000`, web frontend `http://localhost:5173`, Chromium 158 / Playwright 1.65, axe-core 4.x, desktop 1280×900, mobile 360×800, 640×800 (tương đương zoom 200%).

## Bảng tự đánh giá

Theo thang điểm trong đề HW03. Cột tự đánh giá để sinh viên điền sau khi rà bản nộp; chưa tự chấm điểm thay sinh viên.

| STT | Tiêu chí | Điểm tối đa | Điểm tự đánh giá |
| ---: | --- | ---: | ---: |
| 1 | Task 1 — GUI checklist (design + execution + bug report) | 30 | — |
| 2 | Task 2 — Usability evaluation (task scenario + 7 sessions + analysis) | 40 | — |
| 3 | Task 3 — Cross-browser / cross-platform (≥ 3 platforms) | 20 | — |
| 4 | Agent Skills | 10 | — |
| **Tổng** | | **100** | **—** |

## Cần bổ sung trước khi nộp

- [ ] Sinh viên review 66 checklist item và 26 bug; xác nhận bug nào là thật.
- [x] Đã publish 26 GitHub Issues (#80–#105) kèm screenshot; danh sách ở [`features/GUI/issues/published.json`](features/GUI/issues/published.json).
- [ ] Chạy Task 2: chọn flow, viết task scenario, tuyển 7 participant, pilot, 7 session, SUS/UEQ-S, phân tích severity.
- [ ] Chạy Task 3: Chrome, Firefox, Safari (hoặc Android Chrome / Expo Go), screenshot có overlay MSSV + họ tên.
- [ ] Quay video demo Agent Skills và điền link YouTube.
- [ ] Điền điểm tự đánh giá; PDF main report + AI audit + AI critique đã xuất, cần xuất lại nếu sửa Markdown.
- [ ] Tạo git commit cho từng bước và cập nhật `git-commit-log.txt`.

## Ghi chú về GitHub Issues

26 issue đã publish (#80–#105); danh sách máy đọc ở [`features/GUI/issues/published.json`](features/GUI/issues/published.json). Mỗi issue có:
- tiêu đề,
- môi trường,
- steps to reproduce,
- expected/actual,
- screenshot (raw URL trỏ về nhánh `ncuong`),
- root cause và suggested fix.

Các file draft và [`features/GUI/issues/publish.sh`](features/GUI/issues/publish.sh) được giữ lại để tái tạo issue nếu cần.
