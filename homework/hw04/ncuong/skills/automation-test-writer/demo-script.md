# Skill demo video — outline (5–7 phút, tiếng Việt, unlisted)

Mục tiêu: chứng minh skill `automation-test-writer` dùng được end-to-end trên 1 feature hoàn chỉnh (đề §7 — video này khác video Task 2).

## Kịch bản (dùng FR-01 Registration làm ví dụ mới, hoặc FR-02 có sẵn)

| Thời gian | Nội dung | Lệnh / thao tác |
| --- | --- | --- |
| 0:00–0:30 | Giới thiệu: tên, MSSV, skill gì, input/output của skill | face-cam + `whoami` + `hostname` |
| 0:30–1:00 | Mở `skills/automation-test-writer/SKILL.md` — đọc lướt 6 bước + hard rules | editor |
| 1:00–2:00 | Chạy `bash skills/automation-test-writer/scripts/new-feature.sh FR01 fr01` — show 2 file sinh ra | terminal |
| 2:00–3:30 | Điền test plan HW02 FR-01 (2–3 ca) vào `data/fr01.json`, mở rộng spec mẫu từ `templates/` | editor |
| 3:30–5:00 | Chạy `FEATURE=fr01 BROWSER=chromium npx playwright test --project=chromium --grep "@fr01"` | terminal, log xanh |
| 5:00–6:00 | Mở HTML report có `Run by: 23120223` + ISO timestamp | browser |
| 6:00–6:30 | Kết: skill tái dùng được, link repo | terminal |

## Checklist video

unlisted · giọng Việt thật · face-cam hoặc `whoami`+`hostname` · thấy rõ SKILL.md → script chạy → spec chạy → report.
