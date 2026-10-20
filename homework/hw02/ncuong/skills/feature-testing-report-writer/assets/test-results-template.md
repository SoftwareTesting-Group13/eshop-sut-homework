# <FEATURE_CODE> — Test results

## Kết quả theo run

| T-ID | Run ID | Actual | Status | EV-ID / evidence | Bug ID |
| --- | --- | --- | --- | --- | --- |
| `<T-ID>` | `<run hoặc Chưa chạy>` | `<quan sát thực hoặc —>` | `PASS/FAIL/INCONCLUSIVE/BLOCKED/CHƯA CHẠY` | `<EV-ID nếu đã thử>` | `<nếu có>` |

## Tổng hợp case duy nhất

| Phạm vi | Thiết kế | Đã chạy | PASS | FAIL | Quan sát | BLOCKED | Chưa chạy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Tất cả T-ID duy nhất** | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |

Đã chạy = PASS + FAIL + Quan sát; Thiết kế = Đã chạy + BLOCKED + Chưa chạy cho run được nêu. Thống kê theo kỹ thuật, nếu thêm, có thể chồng lấp và không cộng thành tổng.

- Môi trường: `<...>`
- Reset trạng thái: `<cách chuẩn bị state trước mỗi ca>`
- `<ca observation/inconclusive nếu có>`
- Bằng chứng: `<danh sách file log>` + evidence log `evidence/<feature>-evidence.md`

---

## Bug report

### Bảng tổng hợp

| Bug ID | Feature | Title | Severity | Priority | Related TC | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BUG-<FEATURE>-01 | <FEATURE> | `<title>` | `<sev>` | `<priority>` | `<TC>` | Đã tái hiện; chờ SV xác nhận | `<log>` |

### Thống kê severity

| Critical | High | Medium | Low | Tổng |
| ---: | ---: | ---: | ---: | ---: |
| `<n>` | `<n>` | `<n>` | `<n>` | **`<n>`** |

### Tiêu chí phân loại

| Severity | Tiêu chí |
| --- | --- |
| **Critical** | Lộ/mất dữ liệu nhạy cảm hoặc lỗi bảo mật nghiêm trọng. |
| **High** | Luồng cốt lõi hoặc business rule quan trọng sai, ảnh hưởng lớn tới người dùng. |
| **Medium** | Quy tắc/validation sai với ảnh hưởng giới hạn hơn High. |
| **Low** | Sai lệch hiển thị/nội dung nhỏ, ít ảnh hưởng đến việc hoàn thành tác vụ. |

Priority là mức ưu tiên xử lý, đánh giá riêng theo mức ảnh hưởng và tính cấp bách.

### Chi tiết (manual reproduction)

> **Môi trường chung:** `<...>`. **Cách tái hiện:** ưu tiên các bước người dùng thực hiện trên UI khi bug đã được xác nhận qua UI; nếu chỉ chạy API thì ghi bước API và chưa nhận là đã tái hiện trên UI. API/DB có thể bổ sung để xác nhận trạng thái ẩn. **Sau khi xác nhận bug, người kiểm thử chụp screenshot và gắn vào GitHub Issue theo yêu cầu HW02.**

#### BUG-<FEATURE>-01 — <title>

| Trường | Giá trị |
| --- | --- |
| Feature | <FEATURE_CODE> — <tên> |
| Test case liên quan | `<DT/BVA-ID>` |
| Requirement | `<R#/mục đặc tả>` |
| Severity / Priority | `<sev>` / `<priority>` |
| Trạng thái | Đã tái hiện; chờ người kiểm thử xác nhận |
| Evidence | `<đường dẫn log>` |

**Tiền điều kiện:** `<tài khoản cụ thể + state cụ thể>`

**Các bước tái hiện:**
1. `<UI đã kiểm chứng: Người dùng mở trang ... / API đã kiểm chứng: Người kiểm thử gửi request ...>`
2. `<Người dùng nhập/bấm/chờ và thấy gì; hoặc người kiểm thử đọc response/DB. Giữ giá trị cụ thể.>`

| Bước | Input / hành động | Quan sát |
| --- | --- | --- |
| 1 | `<giá trị thật>` | `<...>` |

**Expected:** `<theo đặc tả + rule>`. **Actual:** `<kết quả quan sát>`.
**Độ lặp lại:** `<1/1 hoặc n/m>`. **Root cause:** `<file:dòng, chỉ khi có bằng chứng>`.
**Đối chiếu API/DB (nếu cần):** `<lệnh quan sát trạng thái ẩn; bỏ mục này nếu UI đã đủ bằng chứng>`.
**GitHub Issue:** Chờ người kiểm thử xác nhận bug. **Screenshot:** Chờ xác nhận rồi chụp và gắn vào Issue.

---

#### BUG-<FEATURE>-02 — <title>

`<lặp lại khối trên cho mỗi bug; luôn kết thúc bằng dòng '---'>`

---

## Coverage & gaps

| Tiêu chí coverage | Nghĩa vụ đủ điều kiện | Thiết kế | Đã chạy | PASS | Chưa phủ |
| --- | ---: | ---: | ---: | ---: | ---: |
| `<lớp tương đương / điểm biên>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |

- **Chưa bao phủ:** `<Q#/rule>`
- **Infeasible/khó:** `<...>`
- **Ca BLOCKED:** `<... hoặc 'không có'>`

## AI Gap Analysis

> Phần này do **người kiểm thử tự rà soát và viết** (không điền thay). Trạng thái: `Chờ người kiểm thử rà soát và viết`.

| Gap ID | AI output/source | Test case/bug tôi phát hiện thêm | Cách tôi phát hiện | Vì sao AI bỏ sót (nhận định của tôi) | Bổ sung/sửa chữa |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Việc còn lại

1. `<...>`
2. `<...>`
