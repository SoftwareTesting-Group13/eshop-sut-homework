# AI Audit Report

I use AI tools for the following tasks,

- Đọc đặc tả FR-02 và bộ skill Domain/EP + BVA, lập mô hình miền, thiết kế test case.
- Thiết lập instance SUT cách ly, thực thi các ca qua API, ghi evidence và đánh giá coverage.
- Soạn báo cáo feature FR02 (domain, boundary, catalog, results) và cập nhật master report/README.
- Tạo GitHub Issue cho 2 bug đã được sinh viên xác nhận, đính screenshot vào báo cáo và issue.
- Xóa 2 issue cũ và tạo lại theo template mới của skill `test-findings-report-writer` sau khi template được bổ sung.
- Đọc đặc tả FR-17, thiết kế EP/BVA cho Coupon CRUD, rà soát source coupon (backend + admin UI) để tìm bug và lập artifact FR17.
- Thiết lập instance SUT cách ly, chạy 32 ca API cho FR-17, ghi evidence, đánh giá coverage và cập nhật master report/README.
- Soạn 6 GitHub Issue draft cho FR-17 theo template `test-findings-report-writer`; sau đó đính 34 ảnh Postman do người kiểm thử cung cấp vào draft và các báo cáo liên quan, giữ UI chưa kiểm chứng, không publish/không commit.
- Tạo 6 GitHub Issue FR-17 (#47…#52) kèm ảnh Postman, commit/push artifact FR-17 và cập nhật link Issue trong báo cáo; không dùng ảnh UI.
- Bổ sung 5 ảnh Postman cho `BUG-FR17-07/08`, publish Issue #53/#54, cập nhật báo cáo và ghi AI Audit.
- Bổ sung 1 ảnh UI áp dụng coupon `150%` cho `BUG-FR17-08`, cập nhật Issue #54 và báo cáo; ảnh UI chỉ minh họa hệ quả, không thay bằng chứng API.
- Đọc rule FR-06 và API spec, thiết kế Domain/EP + BVA cho Product detail view trên mobile, chạy API cách ly, ghi giới hạn môi trường mobile và cập nhật báo cáo.
- Sửa cấu hình API endpoint cho Expo mobile theo Android emulator/iOS Simulator/thiết bị thật và kiểm tra bản export Android.
- Cài tạm Expo Go và dependency, chạy FR-06 trên Android emulator/backend cách ly, chụp screenshot, phân tích bug, cập nhật báo cáo và dọn tài nguyên do lượt test tạo.
- Rà báo cáo FR-06, commit/push artifact và ảnh, tạo GitHub Issue #55/#56 kèm ảnh UI, cập nhật liên kết vào báo cáo.
- Biên tập lại main report HW02 thành bản tổng hợp nhất quán cho bốn feature, giữ số liệu gốc và bổ sung tái hiện ngắn cho từng bug.
- Mở rộng AI Gap FR-02 thành ba ca Domain/EP thực chạy, tạo fixture qua FR-01, kiểm tra UI Firefox và API/DB cách ly, chụp ảnh, mở Issue #58/#59, cập nhật báo cáo và dọn môi trường test.
- Chạy Domain/EP cho AI-GAP-FR10-01 trên miền quyền API Admin với DB cách ly, ghi evidence và bug report nháp, cập nhật số liệu FR-10/master report, dọn môi trường test.
- Chụp ảnh bản trình bày raw API log cho BUG-FR10-03, gắn vào GitHub Issue #60, cập nhật báo cáo/evidence và dọn profile trình duyệt tạm.
- Rà số liệu bốn FR, biên tập README cho mục nộp bài và bổ sung phần Domain Testing/BVA vào main report Markdown; kiểm tra link, phép cộng và ghi audit.
- Soạn AI Audit Report này.

> **Phạm vi lập báo cáo (capture notes):**
> - Bằng chứng khả dụng: phiên hội thoại hiện tại (prompt của người dùng + các artifact do agent tạo trong repo); không có file export transcript riêng. Hai screenshot (`features/FR02/screenshots/BUG-FR02-01.png`, `BUG-FR02-02.png`) và 39 ảnh Postman + 1 ảnh UI FR17 trong `features/FR17/screenshots/` do **người dùng** cung cấp. 24 screenshot FR-06 trong `features/FR06/screenshots/` do agent chụp trực tiếp từ Android emulator trong AI-016.
> - Số interaction đã ghi: **22** (AI-001…AI-022; các tool call nội bộ không phải prompt của người dùng nên không liệt kê). AI-022 ghi lượt chỉnh README và main report để chuẩn bị nộp bài.
> - Giới hạn nguồn: giữa AI-018 và AI-019 có các trao đổi ngắn về AI Gap FR-02/FR-17/FR-10/FR-06. Trong nguồn còn giữ của lượt này chỉ có nguyên văn prompt, không có đủ nguyên văn output tương ứng; chưa chép các trao đổi đó thành bản ghi đầy đủ hoặc tự dựng lại output. Cần transcript export để hoàn chỉnh khoảng này.
> - Công cụ AI đã dùng (theo bằng chứng): OpenCode agent, model `DeepSeek V4.1 Flash Free` (provider `opencode`); Codex (OpenAI, GPT-6) cho AI-014…AI-022.
> - Công cụ/phiên được nhắc tới nhưng không kiểm tra được: không.

---

## Interaction AI-001

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time: 2026-10-20 00:25 +0700**.
- **Source:** Phiên hội thoại hiện tại (không có transcript export).
- **Task:** Triển khai toàn bộ quy trình Domain Testing + BVA cho FR-02 (Login and account lockout) theo `homework/hw02/ncuong/prompt.txt` và đề HW02.

### Your prompt

```text
Tiến hành đọc @homework/hw02/ncuong/prompt.txt để triển khai test domain tesing cho feature 02: Login and account lockout nhé.
```

Phần đính kèm của prompt là toàn văn file `homework/hw02/ncuong/prompt.txt` (nội dung người dùng cung cấp trong cùng lượt gửi; file còn trong repo để đối chiếu nguyên văn), bắt đầu bằng:

```text
# Prompt kiểm thử Domain/EP + BVA cho một feature HW02

## Cấu hình duy nhất cần đổi

TARGET_FEATURE_ID: FR02
```

### The AI output

Output của agent là bộ artifact tạo/cập nhật trong repo (nội dung đầy đủ, kiểm tra được):

| Artifact | Đường dẫn |
| --- | --- |
| Domain analysis (EP) | `homework/hw02/ncuong/features/FR02/domain-analysis.md` |
| Boundary analysis (BVA) | `homework/hw02/ncuong/features/FR02/boundary-analysis.md` |
| Test case catalog | `homework/hw02/ncuong/features/FR02/test-cases.md` |
| Test results + bug + coverage | `homework/hw02/ncuong/features/FR02/test-results.md` |
| Evidence log + log thô | `homework/hw02/ncuong/features/FR02/evidence/` |
| Quan sát ngoài EP/BVA | `homework/hw02/ncuong/supporting-materials/fr02-observations.md` |
| Master report cập nhật | `homework/hw02/ncuong/reports/main-report.md` |
| README cập nhật | `homework/hw02/ncuong/README.md` |

Tóm tắt kết quả agent đã tạo (số liệu nằm trong các file trên): 15 T-ID; 15 đã chạy; 11 PASS, 3 FAIL, 1 Quan sát, 0 BLOCKED, 0 chưa chạy; 2 bug ứng viên `BUG-FR02-01` và `BUG-FR02-02` đang chờ sinh viên xác nhận. Agent không tự mở GitHub Issue, không tự chụp screenshot, không điền AI Gap Analysis hay AI Critique.

> Phản hồi cuối của agent cho người dùng là bản tóm tắt bàn giao (số ca, coverage, bug, câu hỏi mở, trạng thái AI Audit); toàn bộ nội dung kỹ thuật chi tiết nằm trong các artifact liên kết ở trên. Các thông điệp tool nội bộ (đọc file, chạy lệnh) không phải output người dùng thấy nên không chép vào đây.

---

## Interaction AI-002

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time: 2026-10-20 01:02 +0700**
- **Source:** Phiên hội thoại hiện tại; screenshot người dùng cung cấp tại `homework/hw02/ncuong/features/FR02/screenshots/`.
- **Task:** Cập nhật báo cáo với 2 screenshot đã được sinh viên xác nhận và tạo GitHub Issue (kèm ảnh) cho từng bug theo `features/FR02/test-results.md`; ghi lại kết quả vào file và cập nhật AI Audit.

### Your prompt

```text
T vừa thêm 2 bức ảnh screenshot xác nhận 2 bug mà m đã phát hiện. Và t xác nhận 2 bug này. Thêm vào báo cáo 2 bức ảnh đó và tạo issue cho mỗi bug dựa trên @homework/hw02/ncuong/features/FR02/test-results.md. Sau đó ghi lại vào file nhé (Issue phải đầy đủ tương tự test-result, có đủ thông tin report bug kèm ảnh đã đính). Xong nhớ ai audit log @homework/hw02/ncuong/skills/ai-audit-logger/SKILL.md
```

### The AI output

Agent đã (nội dung kiểm tra được trong repo và trên GitHub):

- Push screenshot do người dùng cung cấp lên nhánh `ncuong` (commit `test(FR02): add bug confirmation screenshots for BUG-FR02-01/02`).
- Tạo 2 GitHub Issue kèm ảnh nhúng:
    - [#23 [BUG-FR02-01] Bộ đếm đăng nhập sai tăng 2 thay vì 1 → khóa tài khoản sau 2 lần sai](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/23)
    - [#24 [BUG-FR02-02] Thời lượng khóa tài khoản là 180 giây thay vì 30 giây](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/24)
- Lưu toàn văn nội dung issue tại `homework/hw02/ncuong/features/FR02/issues/BUG-FR02-01.md` và `BUG-FR02-02.md`.
- Cập nhật trạng thái bug/Issue và ảnh vào `features/FR02/test-results.md`, `features/FR02/evidence/FR02-evidence.md`, `reports/main-report.md`, `README.md`.

---

## Interaction AI-003

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time: 2026-10-20 01:30 +0700**
- **Source:** Phiên hội thoại hiện tại; template do người dùng bổ sung tại `homework/hw02/ncuong/skills/test-findings-report-writer/assets/github-issue-template.md`.
- **Task:** Xóa 2 GitHub Issue đã tạo ở AI-002 (#23, #24) và tạo lại cho từng bug theo template issue mới; ghi lại vào file và cập nhật AI Audit.

### Your prompt

```text
Xóa 2 issues vừa làm, tạo lại 2 issue đó nha. Vì t vừa bổ sung thêm bộ skills template issue @homework/hw02/ncuong/skills/test-findings-report-writer/assets/github-issue-template.md nên tôi cần bỏ 2 issue cũ và làm lại với template mới này. AI Audit report sau khi xong nhé
```

### The AI output

Agent đã (nội dung kiểm tra được trong repo và trên GitHub):

- Xóa 2 Issue cũ #23 và #24 bằng GraphQL `deleteIssue` (đã kiểm tra danh sách issue không còn FR-02 nào ngoài 2 issue mới).
- Viết lại hoàn toàn `features/FR02/issues/BUG-FR02-01.md` và `BUG-FR02-02.md` theo đúng 5 mục của template (Tóm tắt + bảng Metadata, Chuẩn bị để tái hiện, Các bước tái hiện và kết quả, Bằng chứng, Điều tra nguyên nhân), không để lại placeholder.
- Tạo lại 2 GitHub Issue kèm ảnh nhúng:
    - [#25 BUG-FR02-01 — Bộ đếm đăng nhập sai tăng 2 thay vì 1 khiến tài khoản bị khóa sớm sau 2 lần sai](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/25)
    - [#26 BUG-FR02-02 — Thời lượng khóa tài khoản là 180 giây thay vì 30 giây](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/26)
- Cập nhật lại link Issue (#25/#26) và lệnh tái hiện trong `features/FR02/test-results.md`, `features/FR02/evidence/FR02-evidence.md`, `reports/main-report.md`, `README.md`.

---

## Interaction AI-004

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time:** 2026-10-20 02:06 +0700
- **Source:** Phiên hội thoại hiện tại (không có transcript export).
- **Task:** Triển khai toàn bộ quy trình Domain Testing + BVA cho FR-10 (Order state machine) theo `homework/hw02/ncuong/prompt.txt` và đề HW02; viết AI Audit Log.

### Your prompt

```text
@homework/hw02/ncuong/prompt.txt Triển khai Domain Testing cho Feature 10 nhé. Đọc kỹ file @homework/hw02/ncuong/prompt.txt. Làm xong nhớ viết AI Audit Log @homework/hw02/ncuong/skills/ai-audit-logger/SKILL.md .
```

Phần đính kèm của prompt là toàn văn file `homework/hw02/ncuong/prompt.txt` (nội dung người dùng cung cấp trong cùng lượt gửi; file còn trong repo để đối chiếu nguyên văn), bắt đầu bằng:

```text
# Prompt kiểm thử Domain/EP + BVA cho một feature HW02

## Cấu hình duy nhất cần đổi

TARGET_FEATURE_ID: FR10
```

### The AI output

Output của agent là bộ artifact tạo/cập nhật trong repo (nội dung đầy đủ, kiểm tra được):

| Artifact | Đường dẫn |
| --- | --- |
| Domain analysis (EP) | `homework/hw02/ncuong/features/FR10/domain-analysis.md` |
| Boundary analysis (BVA) | `homework/hw02/ncuong/features/FR10/boundary-analysis.md` |
| Test case catalog | `homework/hw02/ncuong/features/FR10/test-cases.md` |
| Test results + bug + coverage | `homework/hw02/ncuong/features/FR10/test-results.md` |
| Evidence log + log thô | `homework/hw02/ncuong/features/FR10/evidence/` (`FR10-evidence.md`, `DT-*.log`, `run-summary.json`, `run-fr10.mjs`) |
| Nháp GitHub Issue cho 2 bug | `homework/hw02/ncuong/features/FR10/issues/BUG-FR10-01.md`, `BUG-FR10-02.md` |
| Quan sát ngoài EP/BVA | `homework/hw02/ncuong/supporting-materials/fr10-observations.md` |
| Master report cập nhật | `homework/hw02/ncuong/reports/main-report.md` |
| README cập nhật | `homework/hw02/ncuong/README.md` |

Tóm tắt kết quả agent đã tạo (số liệu nằm trong các file trên): 20 T-ID; 20 đã chạy; 18 PASS, 2 FAIL, 0 Quan sát, 0 BLOCKED, 0 chưa chạy; 2 bug ứng viên `BUG-FR10-01` (admin `canceled→delivered`) và `BUG-FR10-02` (user hủy đơn `shipping`) đã tái hiện 2/2, đang chờ sinh viên xác nhận. Agent không tự mở GitHub Issue, không tự chụp screenshot, không điền AI Gap Analysis hay AI Critique. Thực thi trên instance SUT cách ly trong thư mục tạm (commit `09a950cf…`), Database làm việc giữ nguyên.

> Phản hồi cuối của agent cho người dùng là bản tóm tắt bàn giao (số ca, coverage, bug, câu hỏi mở, trạng thái AI Audit); toàn bộ nội dung kỹ thuật chi tiết nằm trong các artifact liên kết ở trên. Các thông điệp tool nội bộ (đọc file, chạy lệnh) không phải output người dùng thấy nên không chép vào đây.

---

## Interaction AI-005

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time:** 2026-10-20 11:30 +0700.
- **Source:** Phiên hội thoại hiện tại (không có transcript export); 7 file screenshot do người dùng bổ sung tại `features/FR10/screenshots/`.
- **Task:** Ghi nhận việc người kiểm thử đã xác nhận 2 bug FR-10 qua UI và bổ sung screenshot; tạo GitHub Issue tương ứng và cập nhật tài liệu.

### Your prompt

```text
t vừa thêm ảnh cũng như confirm 2 bug + add screenshots trên UI rồi ấy. Tạo issue tương ứng nhé.
```

### The AI output

Output của agent là các thay đổi trong repo và trên GitHub (kiểm tra được):

- Đọc 7 screenshot mới, đối chiếu chuỗi thao tác UI: `BUG-FR10-01-Cancelled-Admin.png`, `BUG-FR10-01-Delivered-Admin.png`, `BUG-FR10-01-Delivered-User.png`, `BUG-FR10-02-Delivering-Admin.png`, `BUG-FR10-02-Delivering-User.png`, `BUG-FR10-02-Noti-Cancelled-User.png`, `BUG-FR10-02-Status-Cancelled-User.png`.
- Viết lại 2 bản nháp Issue theo template hiện hành, chuyển trọng tâm sang **đường UI đã kiểm chứng** + nhúng screenshot.
- Commit + push riêng phần screenshot lên nhánh `ncuong` (commit `f49ac90`) để ảnh có URL nhúng trong Issue.
- Tạo 2 GitHub Issue (qua GitHub REST API; `gh` CLI không có trên máy):
    - [#33 BUG-FR10-01 — Admin chuyển được đơn "Đã hủy" sang "Đã giao" (xuyên trạng thái kết thúc)](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33) — labels `bug`, `backend`, `business-logic`.
    - [#34 BUG-FR10-02 — User tự hủy được đơn "Đang giao" (hủy sai trạng thái)](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34) — labels `bug`, `backend`, `frontend`, `business-logic`; ghi chú liên quan Issue #13 (cùng defect, góc nhìn FR-11).
- Cập nhật trạng thái bug thành **đã xác nhận qua UI** và thêm link Issue/screenshot vào `features/FR10/test-results.md`, `features/FR10/issues/*.md`, `features/FR10/evidence/FR10-evidence.md` (thêm EV-FR10-024/025), `supporting-materials/fr10-observations.md`, `reports/main-report.md`, `README.md`.

> Agent không tự chạy lại UI (người kiểm thử đã làm), không sửa source SUT, không điền AI Gap Analysis hay AI Critique. Các thông điệp tool nội bộ không phải output người dùng thấy nên không chép vào đây.

---

## Interaction AI-006

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time:** 2026-10-20 11:55 +0700.
- **Source:** Phiên hội thoại hiện tại (không có transcript export).
- **Task:** Sửa 2 Issue FR-10 vì GitHub tự nhận diện `#1`/`#2` (mã đơn trong nội dung) thành số Issue; ghi AI Audit.

### Your prompt

```text
Quan sát: đơn [FR-01] Từ chối mật khẩu hợp lệ Aa1!bbbb có đúng 8 ký tự #2 "Đang giao"

Sửa lại dùm t 2 cái issue này. Vì m sài #2 nên issue nó nhận diện là issue số 2 chứ ko phải là mã đơn là 2 ấy. Sửa dùm t 2 cái issue phần này, nhớ AI Audit log
```

### The AI output

Output của agent là các thay đổi trong repo và trên GitHub (kiểm tra được):

- Rà soát toàn bộ nội dung Issue FR-10: các cụm `đơn #1`, `đơn #2` (kể cả alt text ảnh) bị GitHub auto-link thành Issue #1/#2.
- Đổi cách diễn đạt thành **"đơn hàng số 1"**, **"đơn hàng số 2"** trong:
    - nội dung đã publish của Issue [#33](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/33) và [#34](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/34);
    - bản lưu tại `features/FR10/issues/BUG-FR10-01.md`, `BUG-FR10-02.md`;
    - `features/FR10/test-results.md`, `features/FR10/evidence/FR10-evidence.md`.
- Kiểm tra lại: Issue #33 không còn tham chiếu `#N` ngoài ý muốn; Issue #34 chỉ còn tham chiếu có chủ đích tới Issue #13. Không tạo Issue mới, không đổi nội dung kỹ thuật/Expected/Actual.

---

## Interaction AI-007

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time:** 2026-10-20 22:31 +0700 (theo thời gian người dùng cung cấp trong prompt).
- **Source:** Phiên hội thoại hiện tại (không có transcript export); artifact và evidence do agent tạo trong repo.
- **Task:** Triển khai toàn bộ quy trình Domain Testing + BVA cho FR-17 (Coupon management — CRUD) theo `homework/hw02/ncuong/prompt.txt`; rà soát source coupon để tìm bug; ghi AI Audit.

### Your prompt

```text
Triển khai Domain Testing cho Feature 17 - Coupon, đọc kỹ @homework/hw02/ncuong/prompt.txt, làm kỹ lưỡng các test case và rà soát tất cả các bug có thể xảy ra trong source nhé. Xong hết thì nhớ AI Audit Log. Thời gian hiện tại là: 20/10/2026 22:31
```

Phần đính kèm của prompt là toàn văn file `homework/hw02/ncuong/prompt.txt` (nội dung người dùng cung cấp trong cùng lượt gửi; file còn trong repo để đối chiếu nguyên văn), bắt đầu bằng:

```text
# Prompt kiểm thử Domain/EP + BVA cho một feature HW02

## Cấu hình duy nhất cần đổi

TARGET_FEATURE_ID: FR17
```

### The AI output

Output của agent là bộ artifact tạo/cập nhật trong repo (nội dung đầy đủ, kiểm tra được):

| Artifact | Đường dẫn |
| --- | --- |
| Domain analysis (EP) | `homework/hw02/ncuong/features/FR17/domain-analysis.md` |
| Boundary analysis (BVA) | `homework/hw02/ncuong/features/FR17/boundary-analysis.md` |
| Test case catalog | `homework/hw02/ncuong/features/FR17/test-cases.md` |
| Test results + bug + coverage | `homework/hw02/ncuong/features/FR17/test-results.md` |
| Evidence log + log thô | `homework/hw02/ncuong/features/FR17/evidence/` (`FR17-evidence.md`, `DT-01.log`…`DT-32.log`, `run-summary.json`, `session-header.log`, `cleanup.log`, `run-fr17.mjs`, `OBS-fr17-user-token.log`, `OBS-fr09-apply-coupon.log`) |
| Quan sát ngoài EP/BVA | `homework/hw02/ncuong/supporting-materials/fr17-observations.md` |
| Master report cập nhật | `homework/hw02/ncuong/reports/main-report.md` |
| README cập nhật | `homework/hw02/ncuong/README.md` |
| AI Audit cập nhật | `homework/hw02/ncuong/reports/ai-audit.md` |

Tóm tắt kết quả agent đã tạo (số liệu nằm trong các file trên): 32 T-ID duy nhất; 32 đã chạy; 11 PASS, 18 FAIL, 3 Quan sát/INCONCLUSIVE, 0 BLOCKED, 0 chưa chạy; EP 32 lớp, BVA 9 điểm biên dùng lại 9 T-ID (0 T-ID BVA-only). 6 bug ứng viên `BUG-FR17-01…06` (2 High, 4 Medium) đang **Chờ người kiểm thử xác nhận**; agent không tự mở GitHub Issue, không tự chụp screenshot, không điền AI Gap Analysis hay AI Critique. Thực thi trên instance SUT cách ly trong thư mục tạm (commit `f389502cdb308b133fe9044e34505f19202dd887`); Database làm việc giữ nguyên SHA-256 `c63f0054…`. UI admin mới có hướng dẫn manual, **chưa chạy UI**; 16 T-ID UI-reachable, 16 T-ID API-only. Quan sát ngoài phạm vi FR-17 (FR-09/FR-12) được lưu riêng, không cộng coverage.

> **Ghi chú lịch sử:** số liệu trong AI-007 là tại thời điểm 2026-10-20. Sau xác nhận của người kiểm thử ở AI-011, FR-17 có **11 PASS, 20 FAIL, 1 Quan sát**; tổng 3 feature là **40 PASS, 25 FAIL, 2 Quan sát**.

> Phản hồi cuối của agent cho người dùng là bản tóm tắt bàn giao (số ca, coverage, bug, câu hỏi mở, trạng thái AI Audit); toàn bộ nội dung kỹ thuật chi tiết nằm trong các artifact liên kết ở trên. Các thông điệp tool nội bộ (đọc file, chạy lệnh) không phải output người dùng thấy nên không chép vào đây.

---

## Interaction AI-008

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time:** 2026-10-20 (prompt không cung cấp giờ; không tự tạo timestamp).
- **Source:** Phiên hội thoại hiện tại (không có transcript export); artifact do agent tạo trong repo.
- **Task:** Soạn 6 GitHub Issue draft cho FR-17 theo template có sẵn của skill `test-findings-report-writer`; không commit, không publish Issue, không chụp screenshot.

### Your prompt

```text
Viết issue template luôn m, chưa commit nhma có template rồi mà @homework/hw02/ncuong/skills/test-findings-report-writer/assets/github-issue-template.md
```

Phần đính kèm của prompt là toàn văn file `homework/hw02/ncuong/skills/test-findings-report-writer/assets/github-issue-template.md` (nội dung người dùng cung cấp trong cùng lượt gửi; file còn trong repo để đối chiếu nguyên văn).

### The AI output

Output của agent là 6 draft Issue mới trong repo (nội dung đầy đủ, kiểm tra được):

| Draft Issue | Đường dẫn |
| --- | --- |
| `BUG-FR17-01` — `code` rỗng/thiếu/chỉ khoảng trắng | `homework/hw02/ncuong/features/FR17/issues/BUG-FR17-01.md` |
| `BUG-FR17-02` — `type` ngoài `percent/fixed` hoặc thiếu | `homework/hw02/ncuong/features/FR17/issues/BUG-FR17-02.md` |
| `BUG-FR17-03` — `discount_value <= 0`, không phải số hoặc thiếu | `homework/hw02/ncuong/features/FR17/issues/BUG-FR17-03.md` |
| `BUG-FR17-04` — `expired_at` thiếu/rỗng/sai định dạng | `homework/hw02/ncuong/features/FR17/issues/BUG-FR17-04.md` |
| `BUG-FR17-05` — `min_order_amount` âm/không phải số/thiếu | `homework/hw02/ncuong/features/FR17/issues/BUG-FR17-05.md` |
| `BUG-FR17-06` — `max_uses_per_user < 1` hoặc thiếu; `0` thành `1` | `homework/hw02/ncuong/features/FR17/issues/BUG-FR17-06.md` |

Mỗi draft dùng đúng các mục của template: trạng thái, tóm tắt, bảng Feature/rule + Test case + Build/môi trường + Severity/Priority + Trạng thái/lặp lại, chuẩn bị, đường tái hiện API đã kiểm chứng, bảng Expected/Actual, phần UI thủ công, đối chiếu kỹ thuật, bằng chứng, điều tra nguyên nhân. Với 4 input có thể đi qua form UI (`DT-06`, `DT-10`, `DT-11`, `DT-21`), phần UI ghi rõ **“Hướng dẫn dự kiến — chưa kiểm chứng UI”**; các input còn lại là **API-only** kèm control/gate chặn tương ứng, không mô phỏng UI.

Các draft giữ trạng thái **Chờ người kiểm thử xác nhận**, không có screenshot, không có URL Issue publish, không có Actual UI giả; evidence link dùng nhánh `ncuong` và sẽ sống sau khi commit/push. Agent cũng cập nhật link draft trong `features/FR17/test-results.md`, `reports/main-report.md` và `README.md`, đồng thời giữ nguyên source, template, DB làm việc và không commit.

> Phản hồi cuối của agent cho người dùng là bản tóm tắt các draft đã soạn, vị trí file và việc còn lại (xác nhận UI, chụp screenshot, publish Issue); không có thay đổi source hay commit.

---

## Interaction AI-009

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time:** 2026-10-21 (prompt không cung cấp giờ; không tự tạo timestamp).
- **Source:** Phiên hội thoại hiện tại (không có transcript export); 34 ảnh do **người dùng** đính kèm trong `features/FR17/screenshots/`; artifact do agent cập nhật trong repo.
- **Task:** Đính 34 ảnh Postman vào 6 Issue draft và các báo cáo liên quan của FR-17; cập nhật trạng thái “đã xác nhận qua API, UI chưa chạy”; ghi AI Audit.

### Your prompt

```text
T có đính kèm ảnh trong screenshot r đó, đính kèm vào các báo cáo liên quan với issue đi m. Nhớ AI Audit
```

### The AI output

Output của agent là các thay đổi trong repo (nội dung kiểm tra được):

| Artifact | Thay đổi |
| --- | --- |
| 6 Issue draft FR-17 | `homework/hw02/ncuong/features/FR17/issues/BUG-FR17-01.md`…`BUG-FR17-06.md`: thêm mục **Ảnh xác nhận API**, nhúng 34 ảnh Postman bằng raw GitHub URL (nhánh `ncuong`); cập nhật trạng thái sang **Đã xác nhận qua API; UI chưa kiểm chứng**; vẫn **chưa publish** |
| Test results | `homework/hw02/ncuong/features/FR17/test-results.md`: thêm ghi chú 34 ảnh API, link ảnh theo từng bug, cập nhật trạng thái 6 bug; nêu rõ `DT-06` chưa có ảnh UI |
| Evidence log | `homework/hw02/ncuong/features/FR17/evidence/FR17-evidence.md`: thêm bảng ánh xạ 34 ảnh theo bug/test case và ghi chú ảnh API không phải ảnh UI |
| Master report / README | `homework/hw02/ncuong/reports/main-report.md`, `homework/hw02/ncuong/README.md`: cập nhật trạng thái FR-17, link thư mục ảnh, số lượng 34 ảnh và việc chưa publish Issue |
| AI Audit | `homework/hw02/ncuong/reports/ai-audit.md`: thêm AI-009, tăng số interaction lên 9 |

- Đã phân loại 34 ảnh theo tên file và kiểm tra mẫu nội dung: `BUG-FR17-01` 4 ảnh, `02` 4, `03` 8, `04` 6, `05` 6, `06` 6; 17/18 ca FAIL có ảnh, `DT-06` không có ảnh vì UI chưa chạy.
- Ảnh là **Postman request/response API**, không phải ảnh UI; báo cáo giữ phân biệt “đã xác nhận API” và “UI chưa kiểm chứng”, không tạo Actual UI giả.
- Link raw GitHub sẽ sống sau khi commit/push nhánh `ncuong`; trước đó ảnh vẫn xem được cục bộ trong repo.
- Không publish GitHub Issue, không commit/push, không sửa source, template, skill hay `backend/database.sqlite`. Working DB hiện đang modified so với HEAD nhưng không phải do AI-009 sửa.

> **Ghi chú lịch sử:** `17/18 ca FAIL` và `6 bug` là số liệu tại thời điểm AI-009. Sau AI-011, FR-17 có **20 FAIL** và **8 bug**; xem tổng hợp hiện hành ở AI-011.

> Phản hồi cuối của agent cho người dùng là bản tóm tắt ảnh đã đính vào đâu, số ảnh/độ phủ, trạng thái Issue và các việc còn lại (UI nếu muốn, commit/push, publish Issue); không có thao tác publish hay commit.

---

## Interaction AI-010

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time:** 2026-10-21 (prompt không cung cấp giờ; không tự tạo timestamp).
- **Source:** Phiên hội thoại hiện tại (không có transcript export); Issue được tạo qua GitHub API bằng credential có sẵn; ảnh do người dùng cung cấp trong `features/FR17/screenshots/`.
- **Task:** Chỉ dùng ảnh Postman, không dùng ảnh UI; publish 6 GitHub Issue FR-17 và cập nhật link Issue trong các báo cáo.

### Your prompt

```text
Không sài ảnh UI nha, sài ảnh postman thôi, tạo issue luôn cho t đi
```

### The AI output

Output của agent là các thay đổi trong repo, commit/push và 6 Issue đã publish (kiểm tra được):

| Issue | URL |
| --- | --- |
| `BUG-FR17-01` | https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/47 |
| `BUG-FR17-02` | https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/48 |
| `BUG-FR17-03` | https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/49 |
| `BUG-FR17-04` | https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/50 |
| `BUG-FR17-05` | https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/51 |
| `BUG-FR17-06` | https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/52 |

- Đã commit artifact FR-17 và ảnh Postman tại commit `4dae771`, sau đó cập nhật link Issue/báo cáo tại commit `0b32a5a`; push lên nhánh `ncuong` để raw URL của ảnh sống.
- Đã tạo 6 Issue, sau đó cập nhật lại body Issue bằng link Issue tương ứng; tất cả Issue đang `open`.
- Đã đổi raw URL ảnh sang dạng `raw.githubusercontent.com/.../refs/heads/ncuong/...` để tránh 404 khi branch mới được push; kiểm tra mẫu ảnh trả HTTP 200.
- Cập nhật `test-results.md`, `FR17-evidence.md`, `main-report.md`, `README.md` và 6 draft Issue với link #47…#52; bỏ trạng thái “chưa publish”.
- **Chỉ dùng ảnh Postman/API**, không dùng ảnh UI; không sửa source hay `backend/database.sqlite`. Working DB vẫn đang modified so với HEAD từ phiên kiểm thử của người dùng.

> Phản hồi cuối của agent cho người dùng là danh sách 6 Issue đã tạo kèm link, xác nhận ảnh Postman đã render và ghi chú không dùng ảnh UI.

---

## Interaction AI-011

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time:** 2026-10-21 (prompt không cung cấp giờ; không tự tạo timestamp).
- **Source:** Phiên hội thoại hiện tại; evidence log `DT-07.log`/`DT-32.log` của run `run-20261020-fr17`; không có ảnh mới trong lượt này.
- **Task:** Xác nhận `OBS-FR17-03` (`save10` bên cạnh `SAVE10`) và `OBS-FR17-04` (`percent` với `discount_value=150`) là bug; thêm vào FR-17, chạy lại bộ skill và cập nhật báo cáo đầy đủ; ghi AI Audit.

### Your prompt

```text
OBS-FR17-03 — save10 được tạo bên cạnh SAVE10
OBS-FR17-04 — percent với discount_value=150 được chấp nhận
T xác nhận đây là 2 bug. FR1703 vì trường trong db là text unique --> có phân biệt hoa thường rồi.
FR1704 --> 150% là 1 mức discount không hợp lệ kể cả khi ko có rule, vì giảm giá thực tế ko ai giảm tới mức này cả.
Thêm 2 bug này vào fr17 hiện tại, chạy lại @homework/hw02/ncuong/skills/ và thêm vào report báo cáo đầy đủ. Ghi xong nhớ AI Audit log @homework/hw02/ncuong/skills/ai-audit-logger/.
```

### The AI output

Output của agent là các thay đổi trong repo (kiểm tra được):

| Artifact | Thay đổi |
| --- | --- |
| Domain / BVA | `features/FR17/domain-analysis.md`, `boundary-analysis.md`: thêm quy tắc uniqueness không phân biệt hoa/thường và upper bound `100` cho percent; P7/P32 có oracle non-2xx; ghi rõ đây là xác nhận của người kiểm thử ngày 2026-10-21, không phải suy từ hành vi SUT |
| Test cases | `features/FR17/test-cases.md`: DT-07 và DT-32 đổi Expected sang từ chối, không tạo row |
| Test results | `features/FR17/test-results.md`: DT-07/DT-32 chuyển `Quan sát` → `FAIL`; thêm `BUG-FR17-07` (Medium) và `BUG-FR17-08` (High); counts FR-17 thành `11 PASS / 20 FAIL / 1 Quan sát`; tổng thành `67/67/40/25/2`; thêm reproduction, root cause, trạng thái ảnh/Issue |
| Evidence | `features/FR17/evidence/FR17-evidence.md`, `DT-07.log`, `DT-32.log`, `run-summary.json`: cập nhật oracle/status/bug ID/counts; giữ nguyên Actual của lần chạy và thêm metadata reclassification |
| Bug drafts | `features/FR17/issues/BUG-FR17-07.md`, `BUG-FR17-08.md`: tạo draft đầy đủ; **chưa publish** vì chưa có ảnh Postman cho DT-07/DT-32 |
| Reports | `reports/main-report.md`, `README.md`, `supporting-materials/fr17-observations.md`: cập nhật 8 bug FR-17 (`High 3 / Medium 5`), counts, liên kết evidence và trạng thái 2 Issue draft |
| AI Audit | `reports/ai-audit.md`: thêm AI-011, tăng số interaction lên 11 |

- Hai bug dùng ID mới `BUG-FR17-07` và `BUG-FR17-08`, không tái sử dụng ID của bug khác; DT-07/DT-32 vẫn giữ nguyên T-ID nên tổng thiết kế/đã chạy không đổi (`32`).
- `BUG-FR17-07` là lỗi API-only vì UI tự uppercase `code`; `BUG-FR17-08` có đường UI tiềm năng nhưng bằng chứng mới là API.
- **Giới hạn:** không có ảnh Postman mới cho `DT-07`/`DT-32`, nên 2 Issue chỉ ở dạng draft; không tạo ảnh giả, không dùng ảnh UI.
- Không sửa source `backend/`/`frontend-admin/`, không sửa `backend/database.sqlite`, không sửa bộ skill; không commit/push trong lượt này.
- Các thay đổi của người dùng trong `prompt.txt` và `skills/` vẫn giữ nguyên.

> Phản hồi cuối của agent cho người dùng là tóm tắt 2 bug mới, counts đã đổi, các file báo cáo đã cập nhật, và việc 2 GitHub Issue còn draft chờ ảnh Postman.

---

## Interaction AI-012

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time:** 2026-10-21 (prompt không cung cấp giờ; không tự tạo timestamp).
- **Source:** Phiên hội thoại hiện tại; 5 ảnh Postman mới trong `features/FR17/screenshots/`; evidence log `DT-07.log`/`DT-32.log`; GitHub Issue tạo qua API.
- **Task:** Bổ sung 5 ảnh Postman cho `BUG-FR17-07/08`, cập nhật báo cáo, publish 2 Issue và ghi AI Audit.

### Your prompt

```text
T vừa thêm các ảnh cho 2 issue mới, bổ sung vào báo cáo và tạo issue dùm t nhé. Nhớ AI Audit
```

### The AI output

Output của agent là các thay đổi trong repo và 2 Issue đã publish (kiểm tra được):

| Issue | URL |
| --- | --- |
| `BUG-FR17-07` | https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/53 |
| `BUG-FR17-08` | https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/54 |

| Artifact | Thay đổi |
| --- | --- |
| Ảnh Postman | Thêm `BUG-FR17-07-CouponUppercase.png`, `BUG-FR17-07-CreateCouponLowercase.png`, `BUG-FR17-07-GetCouponLowercase.png`, `BUG-FR17-08-Discount150.png`, `BUG-FR17-08-GetDiscount150.png`; tổng FR-17 thành **39 ảnh**, **19/20 FAIL** có ảnh, chỉ còn `DT-06` chưa có |
| Bug drafts | `features/FR17/issues/BUG-FR17-07.md`, `BUG-FR17-08.md`: thêm mục **Ảnh xác nhận API**, nhúng 3 + 2 ảnh bằng raw GitHub URL, cập nhật Issue #53/#54 |
| Test results | `features/FR17/test-results.md`: thêm link ảnh cho BUG-07/08, cập nhật 39 ảnh, 19/20 FAIL, 8 Issue #47…#54 |
| Evidence | `features/FR17/evidence/FR17-evidence.md`: thêm 3 dòng ảnh cho DT-07/DT-32, cập nhật 39 ảnh và Issue #53/#54 |
| Reports | `reports/main-report.md`, `README.md`, `supporting-materials/fr17-observations.md`: cập nhật 39 ảnh, 8 Issue #47…#54, trạng thái bug mới |
| AI Audit | `reports/ai-audit.md`: thêm AI-012, tăng số interaction lên 12 |

- Ảnh chụp lần chạy lại có id `5`/`6`, trong khi log `DT-07`/`DT-32` giữ id `10`/`34`; báo cáo ghi rõ khác biệt, không sửa Actual của log run gốc.
- Đã commit/push artifact và ảnh tại commit `80abf1a` trước khi tạo Issue; kiểm tra 5 raw URL ảnh trả HTTP 200.
- Đã tạo Issue #53/#54 rồi PATCH body bằng bản draft cuối có link Issue và ảnh Postman.
- **Chỉ dùng ảnh Postman/API**, không dùng ảnh UI; không stage `prompt.txt`, `skills/**` hoặc `backend/database.sqlite` (các thay đổi có sẵn ngoài phạm vi).

> Phản hồi cuối của agent cho người dùng là tóm tắt 5 ảnh đã bổ sung, 39 ảnh/19-of-20 FAIL, Issue #53/#54, các báo cáo đã cập nhật và ghi chú `DT-06` vẫn thiếu ảnh.

---

## Interaction AI-013

- **AI tool:** OpenCode agent — model `DeepSeek V4.1 Flash Free` (provider `opencode`).
- **Date and time:** 2026-10-21 (prompt không cung cấp giờ; không tự tạo timestamp).
- **Source:** Phiên hội thoại hiện tại; ảnh UI mới `features/FR17/screenshots/BUG-FR17-08-AppliedDiscount150.png`; Issue #54; commit `2a8c77c`.
- **Task:** Bổ sung 1 ảnh UI áp dụng coupon `150%` vào `BUG-FR17-08`/Issue #54 và cập nhật báo cáo; giữ ảnh Postman/API là bằng chứng chính.

### Your prompt

```text
T mới thêm 1 ảnh applied coupon 150% ấy, sửa issue tí cho cái ảnh t mới thêm nha m
```

### The AI output

Output của agent là các thay đổi trong repo và Issue #54 đã cập nhật (kiểm tra được):

| Artifact | Thay đổi |
| --- | --- |
| Ảnh UI bổ sung | `features/FR17/screenshots/BUG-FR17-08-AppliedDiscount150.png`: coupon `FR17-DT-32` được áp dụng thành công với mức giảm `150%`; UI hiển thị tiết kiệm `-4,470,000,000 đ`, thành tiền `4,500,000,000 đ` |
| Issue #54 | Body được PATCH bằng bản draft cuối, thêm ảnh UI; Issue hiện có 2 ảnh Postman + 1 ảnh UI |
| Bug draft / test results | `features/FR17/issues/BUG-FR17-08.md`, `features/FR17/test-results.md`: thêm link ảnh UI, ghi rõ đây là bằng chứng bổ sung hệ quả FR-09, không thay bằng chứng API |
| Evidence / reports | `features/FR17/evidence/FR17-evidence.md`, `reports/main-report.md`, `README.md`, `supporting-materials/fr17-observations.md`: cập nhật thành **39 ảnh Postman + 1 ảnh UI**, 19/20 FAIL có ảnh API, `DT-06` vẫn là ca duy nhất chưa có ảnh API |
| AI Audit | `reports/ai-audit.md`: thêm AI-013, tăng số interaction lên 13 |

- Đã commit/push ảnh và báo cáo tại `2a8c77c`; raw URL của ảnh mới trả HTTP 200.
- Đã kiểm tra Issue #54 có đúng 3 ảnh raw GitHub, gồm `BUG-FR17-08-AppliedDiscount150.png`.
- **Không đổi** counts FR-17 (`11 PASS / 20 FAIL / 1 Quan sát`) và severity (`High 3 / Medium 5`); ảnh UI chỉ bổ sung hệ quả FR-09.
- Không stage `prompt.txt`, `skills/**` hoặc `backend/database.sqlite`.

> Phản hồi cuối của agent cho người dùng là xác nhận đã thêm ảnh applied coupon `150%` vào `BUG-FR17-08`/Issue #54, ảnh render được, và ghi chú ảnh UI chỉ là bằng chứng bổ sung.

---

## Interaction AI-014

- **AI tool:** Codex (OpenAI, GPT-6).
- **Date and time:** Time not available in source.
- **Source:** Yêu cầu của người dùng trong phiên hội thoại này; ngày client context 2026-10-21, không có giờ gửi.
- **Task:** Domain/EP + BVA cho FR-06 Mobile và cập nhật AI Audit.

### Your prompt

```text
Tiến hành thực hiện test domain testing cho FR-06 — Product detail view (Mobile). Đọc kỹ [prompt.txt](homework/hw02/ncuong/prompt.txt) , requirement và api spec.&#x20;

Tham khảo các folder khác cách tổ chức và làm việc, kết hợp với [skills](homework/hw02/ncuong/skills/) . Test kỹ lưỡng domain testing, ko để sót.

Sau khi làm xong, nhớ AI Audit Log lại [ai-audit-report-template.md](homework/hw02/ncuong/skills/ai-audit-logger/assets/ai-audit-report-template.md) 
```

### The AI output

Đã thiết kế 16 ca FR-06 Mobile (EP và BVA), chạy 7 ca API trên backend/DB cách ly và lưu evidence tại [FR06](/Users/cuong/Documents/Code/eshop-sut-homework/homework/hw02/ncuong/features/FR06/test-results.md). Kết quả: 7 INCONCLUSIVE, 9 BLOCKED vì chưa có môi trường chạy mobile; chưa có bug được xác nhận. Đã cập nhật [báo cáo tổng hợp](/Users/cuong/Documents/Code/eshop-sut-homework/homework/hw02/ncuong/reports/main-report.md), [README](/Users/cuong/Documents/Code/eshop-sut-homework/homework/hw02/ncuong/README.md) và AI Audit. Cần chạy các bước manual trên thiết bị để xác nhận hiển thị, số lượng và phản hồi thêm giỏ.

---

## Interaction AI-015

- **AI tool:** Codex (OpenAI, GPT-6).
- **Date and time:** Time not available in source (client context date 2026-10-21, không có giờ gửi prompt).
- **Source:** Prompt người dùng trong phiên này; thay đổi local `frontend-mobile/App.js`, `setup_guide.md`.
- **Task:** Làm rõ React Native/Expo mobile và sửa endpoint API để Android emulator/iOS Simulator/thiết bị thật truy cập được backend.

### Your prompt

```text
Ủa mobile dc build dưới dạng react native mà sao lại truy cập không dc nhỉ, với sửa api endpoint cho mobile để chạy đúng đi
```

### The AI output

Output là thay đổi có thể kiểm tra tại `frontend-mobile/App.js` (Android emulator mặc định `http://10.0.2.2:3000/api`, iOS Simulator `http://localhost:3000/api`, cho phép override `EXPO_PUBLIC_API_URL`, bỏ dấu `/` cuối) và `setup_guide.md` (hướng dẫn `.env.local` cho thiết bị thật, `npm ci`). Đã xuất bundle Android bằng Expo và xác nhận bundle có endpoint `10.0.2.2:3000/api`; sau đó chạy app thật trong AI-016. Không sửa logic FR-06 ở interaction này.

---

## Interaction AI-016

- **AI tool:** Codex (OpenAI, GPT-6).
- **Date and time:** Time not available in source (client context date 2026-10-21, không có giờ gửi prompt).
- **Source:** Prompt người dùng trong phiên này; run `run-20261021-fr06-mobile`, 24 ảnh tại `features/FR06/screenshots/`, report/evidence/issue draft trong repo.
- **Task:** Cài tạm môi trường cần thiết, tự chạy lại Domain/EP+BVA FR-06 trên mobile, tìm/phân tích bug, chụp ảnh, cập nhật AI Audit và dọn tài nguyên cài tạm.

### Your prompt

```text
cài xong tự test, tự tìm và phân tích bug lại từ đầu nhé. Xong tự cap màn hình đính dô luôn. Nhớ AI Audit log và xóa những thứ m đã cài (ko xóa nhầm nhé)
```

### The AI output

Output là bộ artifact FR-06 tại `features/FR06/`: 16 T-ID đã chạy (3 PASS, 9 FAIL, 4 INCONCLUSIVE), 2 bug xác nhận trên Android emulator, 24 screenshot gắn EV-ID/ca và 2 nháp Issue có ảnh. Cập nhật `domain-analysis.md`, `boundary-analysis.md`, `test-cases.md`, `test-results.md`, `evidence/FR06-evidence.md`, `reports/main-report.md`, `README.md`, `supporting-materials/fr06-observations.md` và AI Audit này. Đã dừng backend/Metro/emulator do phiên mở, gỡ Expo Go APK cài tạm và xóa dependency/build/temp do phiên tạo; giữ nguyên SDK/AVD và `backend/database.sqlite` (SHA-256 trước/sau giống nhau). Hai nháp Issue chờ sinh viên review theo `prompt.txt`, chưa publish.

---

## Interaction AI-017

- **AI tool:** Codex (OpenAI, GPT-6).
- **Date and time:** Time not available in source (client context date 2026-10-21, không có giờ gửi prompt).
- **Source:** Prompt người dùng trong phiên này; commit `4e4f0ee3aac82aed2e526929bfa6dab41601e5c8`, GitHub Issue [#55](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/55) và [#56](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/56).
- **Task:** Rà report FR-06, commit/push ảnh và artifact, tạo hai GitHub Issue sau khi người dùng chốt, cập nhật link vào báo cáo.

### Your prompt

```text
OK chốt hết nhé, check report + commit + tạo issue cho 2 bug dùm t.
```

### The AI output

Rà lại 16 ca FR-06 (3 PASS, 9 FAIL, 4 INCONCLUSIVE), 24 screenshot, link và nội dung hai bug. Commit/push `4e4f0ee3aac82aed2e526929bfa6dab41601e5c8` đúng các file FR-06, endpoint mobile, setup guide và report; không stage `prompt.txt` thay đổi có sẵn. Kiểm tra 10 ảnh UI nhúng trên GitHub đều HTTP 200; tạo [Issue #55 — BUG-FR06-01](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/55) và [Issue #56 — BUG-FR06-02](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/56). Cập nhật bản lưu Issue, test results, evidence, main report, README và AI Audit; commit/push tiếp các link và trạng thái Issue.

---

## Interaction AI-018

- **AI tool:** Codex (OpenAI, GPT-6).
- **Date and time:** Time not available in source (client context date 2026-10-21, không có giờ gửi prompt).
- **Source:** Prompt người dùng trong phiên này; thay đổi tại `reports/main-report.md`.
- **Task:** Biên tập lại master report để bỏ lặp, đối chiếu số liệu/link và giữ mỗi bug một đường tái hiện ngắn.

### Your prompt

```text
Clean lại dùm t cái main report đi m
```

### The AI output

Đã viết lại `reports/main-report.md` thành bản tổng hợp cho FR-02/FR-10/FR-17/FR-06: một bảng 83 T-ID (43 PASS, 34 FAIL, 6 Quan sát), bảng coverage EP/BVA, 14 bug và severity tổng 5 High/9 Medium, cùng 14 mục tái hiện ngắn theo đúng bug ID. Giữ kết quả và trạng thái Issue #25/#26, #33/#34, #47…#56; liên kết tới báo cáo/evidence từng feature. Đã kiểm tra 14 hàng bug khớp 14 mục chi tiết, không có link nội bộ hỏng và `git diff --check` không báo lỗi.

---

## Interaction AI-019

- **AI tool:** Codex (OpenAI, GPT-6).
- **Date and time:** Time not available in source (client context date 2026-10-21, không có giờ gửi prompt).
- **Source:** Prompt người dùng trong phiên này; `run-20261021-fr02-gap-api`, `run-20261021-fr02-gap-ui`; commit `933d77e`; GitHub Issue [#58](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/58) và [#59](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/59).
- **Task:** Chạy lại Domain/EP cho hai AI Gap FR-02, chụp bằng chứng, publish Issue, cập nhật report và dọn môi trường.

### Your prompt

```text
Bổ sung cho t thêm 2 bug ở phần AI-GAP-FR02-01 (liên hệ FR Đăng ký, tạo 1 tài khoản định dạng sai email và login vào) và AI-GAP-FR02-03.

[skills](homework/hw02/ncuong/skills/) Triển khai lại domain testing cho 2 case này. [prompt.txt](homework/hw02/ncuong/prompt.txt) đọc kỹ. Cap màn hình và tạo lại issue dùm t.
Viết lại report + clean. Làm xong nhớ AI Audit Log.
```

### The AI output

Đã triển khai lại FR-02 và cập nhật [test results](/Users/cuong/Documents/Code/eshop-sut-homework/homework/hw02/ncuong/features/FR02/test-results.md) cùng [main report](/Users/cuong/Documents/Code/eshop-sut-homework/homework/hw02/ncuong/reports/main-report.md). Ba ca bổ sung DT-09–DT-11 đã chạy; tổng FR-02 là **18 ca: 11 PASS, 6 FAIL, 1 Quan sát**.

- **AI-GAP-FR02-01:** Đăng ký `not-an-email` qua API rồi đăng nhập được trên web. Form dùng `type="text"`; đã mở [Issue #58](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/58) kèm ảnh UI trước/sau.
- **AI-GAP-FR02-03:** Thiếu hẳn key `password` bị từ chối 401, nhưng bộ đếm tăng 2 (bug #25 đã có). Với tài khoản có mật khẩu DB `NULL`, gửi `password:null` lại nhận JWT; đã mở [Issue #59](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/59) kèm ảnh log API. Ảnh này là bản trình bày log API, không phải ảnh giao diện app.

Đã ghi [AI Audit Log](/Users/cuong/Documents/Code/eshop-sut-homework/homework/hw02/ncuong/reports/ai-audit.md), xóa đúng thư mục test tạm và dừng các dịch vụ test; checksum DB làm việc giữ nguyên. Các chỉnh sửa có sẵn ở FR-06, FR-10, FR-17 và `prompt.txt` được giữ nguyên.

---

## Interaction AI-020

- **AI tool:** Codex (OpenAI, GPT-6).
- **Date and time:** Time not available in source (client context date 2026-10-21, không có giờ gửi prompt).
- **Source:** Prompt người dùng trong phiên này; `run-20261021-fr10-gap-access`, raw API log ở `features/FR10/evidence/ev-gap-access-*.json`.
- **Task:** Triển khai Domain Testing cho miền quyền trong AI-GAP-FR10-01, chạy API/DB cách ly, cập nhật báo cáo và ghi bug nháp.

### Your prompt

```text
[skills](homework/hw02/ncuong/skills/) Triển khai Domain Testing cho AI-GAP-FR10-01.
```

### The AI output

Đã chạy Domain Testing cho **AI-GAP-FR10-01** trên DB cách ly. JWT user thường đổi được đơn `pending → confirmed` qua API Admin: **2/2 với đơn của mình, 1/1 với đơn người khác**. Đối chứng: JWT admin đổi được đơn; không token bị 401 và đơn giữ nguyên.

Đã thêm DT-21–DT-23 và [BUG-FR10-03](/Users/cuong/Documents/Code/eshop-sut-homework/homework/hw02/ncuong/features/FR10/issues/BUG-FR10-03.md) vào [báo cáo FR-10](/Users/cuong/Documents/Code/eshop-sut-homework/homework/hw02/ncuong/features/FR10/test-results.md). Tổng FR-10 hiện là **23 ca: 19 PASS, 4 FAIL**; coverage EP/BVA trạng thái cũ giữ nguyên, miền quyền có coverage riêng. [Main report](/Users/cuong/Documents/Code/eshop-sut-homework/homework/hw02/ncuong/reports/main-report.md) và [AI Audit](/Users/cuong/Documents/Code/eshop-sut-homework/homework/hw02/ncuong/reports/ai-audit.md) đã cập nhật.

BUG-FR10-03 mới có bằng chứng API và nháp Issue; **chưa có screenshot hay GitHub Issue**, đang chờ sinh viên review theo `prompt.txt`. Đã xóa thư mục test tạm, dừng dịch vụ test; checksum DB làm việc không đổi.

---

## Interaction AI-021

- **AI tool:** Codex (OpenAI, GPT-6).
- **Date and time:** Time not available in source (client context date 2026-10-21, không có giờ gửi prompt).
- **Source:** Prompt người dùng trong phiên này; screenshot `features/FR10/screenshots/BUG-FR10-03-api-evidence.png`; GitHub Issue [#60](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/60).
- **Task:** Chụp màn hình bằng chứng API cho BUG-FR10-03 và đăng GitHub Issue kèm ảnh.

### Your prompt

```text
Screenshot case vừa rồi và tạo issue cho t luôn đi.
```

### The AI output

Đã chụp [ảnh bằng chứng API](/Users/cuong/Documents/Code/eshop-sut-homework/homework/hw02/ncuong/features/FR10/screenshots/BUG-FR10-03-api-evidence.png) cho DT-21/DT-22 và tạo [GitHub Issue #60 — BUG-FR10-03](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/60). Ảnh là bản trình bày raw log đã chạy, ghi rõ nguồn; đây là ca API-only, không phải screenshot giao diện app hay Postman.

Đã gắn ảnh vào Issue, kiểm tra URL ảnh trả HTTP 200, cập nhật [báo cáo FR-10](/Users/cuong/Documents/Code/eshop-sut-homework/homework/hw02/ncuong/features/FR10/test-results.md), [main report](/Users/cuong/Documents/Code/eshop-sut-homework/homework/hw02/ncuong/reports/main-report.md) và AI Audit Log. Đã xóa profile Firefox/thư mục dựng ảnh tạm; các chỉnh sửa sẵn có ở FR-06, FR-17 và `prompt.txt` được giữ nguyên.

---

## Interaction AI-022

- **AI tool:** Codex (OpenAI, GPT-6).
- **Date and time:** Time not available in source (client context date 2026-10-21, không có giờ gửi prompt).
- **Source:** Prompt người dùng trong phiên này; `README.md`, `reports/main-report.md`, `reports/ai-audit.md`.
- **Task:** Chỉnh README và main report Markdown để chuẩn bị nộp HW02; bổ sung tóm tắt Domain Testing/BVA và bảng tự đánh giá; ghi AI Audit.

### Your prompt

```text
A README.md  containing the self-assessment table (below) and a testsummary report: number of features; number of test cases designed,
executed, passed, failed, and not yet executed; number of bugs; anddemo videos.

Main report Markdown + PDF, including the Domain Testing report andthe Boundary Value Analysis report

Fix README và Main Report lại để t chuẩn bị nộp bài nha (ko cần xuất PDF, viết markdown xong t review lại rồi nộp nha, giữ nguyên các FR nhé). Nhớ AI Audit
```

### The AI output

Đã chỉnh README với bảng tự đánh giá theo thang 100 điểm, test summary 4 feature/89 ca/17 bug và mục video demo ghi rõ chưa có link. Main report Markdown hiện có phần Domain Testing và BVA cho cả bốn FR, giữ nguyên bảng bug và link evidence. Đã cập nhật AI Audit; kiểm tra số liệu, link nội bộ và `git diff --check`. Không sửa file FR, không xuất PDF hay commit. Còn cần bạn điền điểm, link video và viết AI Critique trước khi nộp.

---

## Optional audit table (theo mẫu `[AI-02]` — bổ sung, không thay thế 4 trường bắt buộc)

| (1) Prompt + Công cụ | (2) Output AI | (3) Verdict | (4) Lý do | (5) Bản SV sửa |
| --- | --- | --- | --- | --- |
| OpenCode · DeepSeek V4.1 Flash Free · Time not available in source · “Tiến hành đọc @homework/hw02/ncuong/prompt.txt để triển khai test domain tesing cho feature 02: Login and account lockout nhé.” | Bộ artifact FR02 tại `features/FR02/` + cập nhật `reports/main-report.md`, `README.md` | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| OpenCode · DeepSeek V4.1 Flash Free · Time not available in source · “T vừa thêm 2 bức ảnh screenshot xác nhận 2 bug … Xong nhớ ai audit log …” | Issue #23, #24 kèm screenshot; cập nhật `test-results.md`, `FR02-evidence.md`, `main-report.md`, `README.md`; lưu issue tại `features/FR02/issues/` | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| OpenCode · DeepSeek V4.1 Flash Free · Time not available in source · “Xóa 2 issues vừa làm, tạo lại 2 issue đó nha … làm lại với template mới này …” | Xóa #23/#24; viết lại `issues/*.md` theo template mới; tạo Issue #25, #26 kèm screenshot; cập nhật link trong `test-results.md`, `FR02-evidence.md`, `main-report.md`, `README.md` | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| OpenCode · DeepSeek V4.1 Flash Free · Time not available in source · “@homework/hw02/ncuong/prompt.txt Triển khai Domain Testing cho Feature 10 nhé. … Làm xong nhớ viết AI Audit Log …” | Bộ artifact FR10 tại `features/FR10/` (4 file + evidence + 2 nháp Issue) + `supporting-materials/fr10-observations.md` + cập nhật `reports/main-report.md`, `reports/ai-audit.md`, `README.md` | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| OpenCode · DeepSeek V4.1 Flash Free · Time not available in source · “t vừa thêm ảnh cũng như confirm 2 bug + add screenshots trên UI rồi ấy. Tạo issue tương ứng nhé.” | Issue #33, #34 kèm 7 screenshot; commit/push ảnh `f49ac90`; cập nhật `test-results.md`, `FR10-evidence.md` (EV-024/025), `issues/*.md`, `fr10-observations.md`, `main-report.md`, `README.md` | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| OpenCode · DeepSeek V4.1 Flash Free · Time not available in source · “Quan sát: đơn … #2 "Đang giao" … Sửa lại dùm t 2 cái issue này. Vì m sài #2 nên issue nó nhận diện là issue số 2 … nhớ AI Audit log” | Sửa `đơn #1/#2` → `đơn hàng số 1/2` trong Issue #33, #34 (published) và `issues/*.md`, `test-results.md`, `FR10-evidence.md`; xác nhận chỉ còn tham chiếu #13 có chủ đích | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| OpenCode · DeepSeek V4.1 Flash Free · 2026-10-20 22:31 +0700 · “Triển khai Domain Testing cho Feature 17 - Coupon, đọc kỹ @homework/hw02/ncuong/prompt.txt, làm kỹ lưỡng các test case và rà soát tất cả các bug có thể xảy ra trong source nhé. Xong hết thì nhớ AI Audit Log. Thời gian hiện tại là: 20/10/2026 22:31” | Bộ artifact FR17 tại `features/FR17/` (4 file + evidence 32 log + driver) + `supporting-materials/fr17-observations.md` + cập nhật `reports/main-report.md`, `reports/ai-audit.md`, `README.md` | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| OpenCode · DeepSeek V4.1 Flash Free · 2026-10-20 · Time not available in source · “Viết issue template luôn m, chưa commit nhma có template rồi mà @homework/hw02/ncuong/skills/test-findings-report-writer/assets/github-issue-template.md” | 6 draft Issue FR17 tại `features/FR17/issues/BUG-FR17-01.md`…`BUG-FR17-06.md`; cập nhật link draft trong `test-results.md`, `main-report.md`, `README.md`; không publish/không commit | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| OpenCode · DeepSeek V4.1 Flash Free · 2026-10-21 · Time not available in source · “T có đính kèm ảnh trong screenshot r đó, đính kèm vào các báo cáo liên quan với issue đi m. Nhớ AI Audit” | 34 ảnh Postman được nhúng vào 6 Issue draft FR17 và liên kết trong `test-results.md`, `FR17-evidence.md`, `main-report.md`, `README.md`; trạng thái chuyển thành “đã xác nhận API; UI chưa chạy”; không publish/không commit | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| OpenCode · DeepSeek V4.1 Flash Free · 2026-10-21 · Time not available in source · “Không sài ảnh UI nha, sài ảnh postman thôi, tạo issue luôn cho t đi” | Commit/push `4dae771` (artifact + ảnh) và `0b32a5a` (link Issue/báo cáo); tạo Issue FR17 #47…#52 kèm ảnh Postman; cập nhật draft Issue và `test-results.md`, `FR17-evidence.md`, `main-report.md`, `README.md`; chỉ dùng ảnh Postman, không dùng ảnh UI | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| OpenCode · DeepSeek V4.1 Flash Free · 2026-10-21 · Time not available in source · “OBS-FR17-03 … OBS-FR17-04 … T xác nhận đây là 2 bug … Thêm 2 bug này vào fr17 hiện tại … Ghi xong nhớ AI Audit log …” | Chuyển DT-07/DT-32 sang FAIL; thêm `BUG-FR17-07`/`BUG-FR17-08`; cập nhật domain/BVA/test-cases/test-results/evidence/observations/master report/README; counts FR-17 `11/20/1`, tổng `40/25/2`; tạo 2 Issue draft chờ ảnh Postman; thêm AI-011 | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| OpenCode · DeepSeek V4.1 Flash Free · 2026-10-21 · Time not available in source · “T vừa thêm các ảnh cho 2 issue mới, bổ sung vào báo cáo và tạo issue dùm t nhé. Nhớ AI Audit” | Thêm 5 ảnh Postman cho BUG-FR17-07/08; cập nhật 39 ảnh/19-of-20 FAIL/8 Issue; publish Issue #53/#54; commit/push `80abf1a`; cập nhật draft, test-results, evidence, main-report, README, observations; thêm AI-012 | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| OpenCode · DeepSeek V4.1 Flash Free · 2026-10-21 · Time not available in source · “T mới thêm 1 ảnh applied coupon 150% ấy, sửa issue tí cho cái ảnh t mới thêm nha m” | Thêm ảnh UI `BUG-FR17-08-AppliedDiscount150.png` vào BUG-FR17-08/Issue #54; cập nhật draft, test-results, evidence, main-report, README, observations; commit/push `2a8c77c`; thêm AI-013 | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| Codex · GPT-6 · Time not available in source · “Tiến hành thực hiện test domain testing cho FR-06 — Product detail view (Mobile)…” | 16 ca EP/BVA, 7 ca API INCONCLUSIVE, 9 ca BLOCKED mobile; artifact FR06, master report, README, AI-014 | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| Codex · GPT-6 · Time not available in source · “Ủa mobile dc build dưới dạng react native…” | Sửa endpoint Expo mobile trong `frontend-mobile/App.js`, cập nhật `setup_guide.md`, xác nhận Android bundle; AI-015 | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| Codex · GPT-6 · Time not available in source · “cài xong tự test, tự tìm và phân tích bug lại từ đầu nhé…” | Run FR-06 Android 16 ca (3 PASS, 9 FAIL, 4 INCONCLUSIVE), 2 bug, 24 screenshot, 2 draft Issue; cập nhật report/evidence/AI Audit; cleanup tài nguyên cài tạm; AI-016 | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| Codex · GPT-6 · Time not available in source · “OK chốt hết nhé, check report + commit + tạo issue cho 2 bug dùm t.” | Commit/push artifact FR-06 + 24 ảnh; Issue #55/#56 có 10 ảnh UI nhúng; cập nhật report/evidence/README/AI Audit và commit link; AI-017 | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| Codex · GPT-6 · Time not available in source · “Clean lại dùm t cái main report đi m” | Biên tập lại `reports/main-report.md`: 83 case, 14 bug có 14 mục tái hiện ngắn, severity 5 High/9 Medium, link hợp lệ; AI-018 | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| Codex · GPT-6 · Time not available in source · “Bổ sung cho t thêm 2 bug ở phần AI-GAP-FR02-01…” | Chạy DT-09–DT-11, 2 bug mới; ảnh UI/API; Issue #58/#59; cập nhật FR02, master report, README và AI Audit; dọn test temp; AI-019 | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| Codex · GPT-6 · Time not available in source · “Triển khai Domain Testing cho AI-GAP-FR10-01” | Chạy DT-21–DT-23 trên DB cách ly; xác nhận BUG-FR10-03 qua API, tạo nháp Issue, cập nhật report/evidence/README/AI Audit; AI-020 | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| Codex · GPT-6 · Time not available in source · “Screenshot case vừa rồi và tạo issue cho t luôn đi.” | Chụp ảnh từ raw API log, gắn vào Issue #60, cập nhật report/evidence/README/AI Audit và dọn Firefox profile tạm; AI-021 | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |
| Codex · GPT-6 · Time not available in source · “Fix README và Main Report lại để t chuẩn bị nộp bài nha … Nhớ AI Audit” | README có bảng tự đánh giá/test summary/video demo; main report có phần Domain/BVA của bốn FR; kiểm tra link và số liệu; thêm AI-022 | *(SV tự điền)* | *(SV tự điền theo ISTQB)* | *(SV tự điền)* |

> Cột (3)–(5) do **sinh viên** tự đánh giá/điền; báo cáo không tự suy diễn verdict hay bản sửa của sinh viên.
