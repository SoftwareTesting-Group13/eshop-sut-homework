# HW03 — GUI & Usability

**Sinh viên:** Dương Nhật Cường · **MSSV:** 23120223 · **Nhóm:** Group 13
**SUT:** EShop · **Đề bài:** [HW03 GUI & Usability](../docs/2026.HW03.GUI_Usability_En.md)
**Trạng thái:** Task 1 đã triển khai; Task 2 và Task 3 chưa bắt đầu.

## Hồ sơ báo cáo

- [Main report](reports/main-report.md)
- [AI Audit Report](reports/ai-audit.md)
- [AI Critique (draft)](reports/ai-critique.md)
- [GUI checklist — Markdown](features/GUI/checklist.md)
- [GUI checklist — Excel, 69 items](features/GUI/checklist.xlsx)
- [Test summary](features/GUI/test-summary.md)
- [AI initial checklist](features/GUI/ai-initial-checklist.md)
- [Review additions + why AI missed them](features/GUI/review-additions.md)
- [Bug report — 26 bugs](features/GUI/bug-report.md)
- [Individual bug reports](features/GUI/bugs/)
- [GitHub issue drafts](features/GUI/issues/)
- [Screenshots — failed items only](features/GUI/screenshots/)
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
| End-to-end flows tested | 0 (Task 2 not started) |
| Checklist items designed | 69 |
| Checklist items executed | 69 |
| Passed | 25 |
| Failed | 44 |
| Bugs reported | 26 |
| Blockers | 2 |
| Major | 12 |
| Minor | 12 |
| Participants | 0 (Task 2 not started) |
| Demo videos | 0 (to be recorded) |

| Interface aspect | Items | Passed | Failed |
| --- | ---: | ---: | ---: |
| IA-01 General UI standards | 19 | 8 | 11 |
| IA-02 Forms | 16 | 4 | 12 |
| IA-03 Navigation | 17 | 9 | 8 |
| IA-04 Feedback / state | 17 | 4 | 13 |
| **Total** | **69** | **25** | **44** |

**Source split:** 44 AI-initial items + 25 review additions. The review additions and the reason the AI missed each one are in [`features/GUI/review-additions.md`](features/GUI/review-additions.md).

**Execution environment:** backend `http://localhost:3000`, web frontend `http://localhost:5173`, Chromium 158 / Playwright 1.65, axe-core 4.x, 1280×900 desktop, 360×800 mobile, 640×800 (200% zoom equivalent).

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

- [ ] Sinh viên review 69 checklist item và 26 bug; xác nhận bug nào là thật.
- [ ] Cấu hình `gh auth login` rồi chạy `bash features/GUI/issues/publish.sh` để publish 26 GitHub Issues (kèm screenshot). Hiện môi trường chưa có `gh`/token nên issue mới ở dạng draft.
- [ ] Chạy Task 2: chọn flow, viết task scenario, tuyển 7 participant, pilot, 7 session, SUS/UEQ-S, phân tích severity.
- [ ] Chạy Task 3: Chrome, Firefox, Safari (hoặc Android Chrome / Expo Go), screenshot có overlay MSSV + họ tên.
- [ ] Quay video demo Agent Skills và điền link YouTube.
- [ ] Điền điểm tự đánh giá; PDF main report + AI audit + AI critique đã xuất, cần xuất lại nếu sửa Markdown.
- [ ] Tạo git commit cho từng bước và cập nhật `git-commit-log.txt`.

## Ghi chú về GitHub Issues

26 issue draft nằm trong [`features/GUI/issues/`](features/GUI/issues/), mỗi file có:
- tiêu đề,
- môi trường,
- steps to reproduce,
- expected/actual,
- screenshot (raw URL trỏ về nhánh `ncuong`),
- root cause và suggested fix.

Script publish: [`features/GUI/issues/publish.sh`](features/GUI/issues/publish.sh). Script yêu cầu `gh auth login` và screenshot đã được push lên nhánh `ncuong`.
