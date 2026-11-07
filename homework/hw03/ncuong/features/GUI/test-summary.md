# Test summary — HW03 Task 1 (GUI checklist)

**Sinh viên:** Dương Nhật Cường · **MSSV:** 23120223 · **Nhóm:** 13
**SUT:** EShop web frontend · **Ngày:** 2026-11-07
**Phạm vi:** FR-01 Đăng ký, FR-02 Đăng nhập, FR-03 Quên/đặt lại mật khẩu, FR-04 Hồ sơ
**Màn hình:** Login, Register, Forgot Password, Profile
**Interface aspects:** IA-01 General UI standards, IA-02 Forms, IA-03 Navigation, IA-04 Feedback / state

## Số liệu chính

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

## Kết quả theo interface aspect

| Interface aspect | Items | Passed | Failed |
| --- | ---: | ---: | ---: |
| IA-01 General UI standards | 18 | 7 | 11 |
| IA-02 Forms | 17 | 4 | 13 |
| IA-03 Navigation | 15 | 9 | 6 |
| IA-04 Feedback / state | 16 | 7 | 9 |
| **Tổng** | **66** | **27** | **39** |

## Phân nguồn

| Nguồn | Items |
| --- | ---: |
| AI sinh ban đầu (`ui-checklist-generator`) | 44 item được sinh, 41 item được giữ |
| Bổ sung/sửa sau review | 25 |
| **Checklist cuối** | **66** |

25 item bổ sung/sửa, lý do AI bỏ sót và bộ AI ban đầu nằm trong
[`ai-checklist-and-review.md`](ai-checklist-and-review.md).

## Môi trường thực thi

| Item | Value |
| --- | --- |
| Backend | `http://localhost:3000` (`backend/server.js`, SQLite seed) |
| Web frontend | `http://localhost:5173` (`frontend-web`, Vite) |
| Browser | Chromium 158 / Playwright 1.65 |
| Desktop viewport | 1280×900 |
| Mobile viewport | 360×800 |
| 200% zoom equivalent | 640×800 |
| Accessibility engine | axe-core 4.x |
| Test data | Seed user `test@eshop.com`; user đăng ký qua UI/API; order inject bằng Playwright route interception |

## Artifact

| Artifact | Path |
| --- | --- |
| Full checklist (Markdown) | [`checklist.md`](checklist.md) |
| Full checklist (Excel) | [`checklist.xlsx`](checklist.xlsx) |
| Machine-readable results | [`checklist.json`](checklist.json) |
| AI initial checklist + review additions | [`ai-checklist-and-review.md`](ai-checklist-and-review.md) |
| Bug report | [`bug-report.md`](bug-report.md) |
| Individual bug reports | [`bugs/`](bugs/) |
| GitHub issues (đã publish) | [`issues/`](issues/), [`published.json`](issues/published.json) |
| Screenshots (Failed items only) | [`screenshots/`](screenshots/) |

## Ghi chú và hạn chế

- Tất cả 66 item đã được thực thi. Một item Failed không tự động là bug: thiếu confirm-password và step indicator là design gap; 26 bug là defect tái hiện được.
- Screenshot có banner đỏ tiếng Việt ghi checklist ID, mô tả lỗi và quan sát; ảnh chụp SUT tại `localhost:5173`, không phải mock.
- 26 GitHub Issues đã publish (#80–#105) và screenshot dùng raw URL trên nhánh `ncuong` đã push.
- Task 1 chỉ chạy trên Chromium; Firefox/Safari/Expo Go thuộc Task 3.
