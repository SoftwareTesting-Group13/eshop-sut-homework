# Báo cáo tổng hợp — Domain Testing và Boundary Value Analysis

> File mẫu trống cho **master report**. Thay `<...>` bằng nội dung thật. Master chỉ
> tổng hợp + dẫn link; không lặp lại phân tích đặc tả / partition / BVA của feature report.

## 0. Thông tin sinh viên

| Trường | Giá trị |
| --- | --- |
| Họ và tên | `<...>` |
| MSSV | `<...>` |
| Lớp / Nhóm | `<...>` |
| Assignment | `<...>` |
| GitHub repo (nhóm) | `<url>` |

## 1. Feature đã chọn

| Nhóm | Feature | Báo cáo feature | Tình trạng |
| --- | --- | --- | --- |
| A | `<mã + tên feature>` | [Domain](../features/<FEATURE_CODE>/domain-analysis.md) · [BVA](../features/<FEATURE_CODE>/boundary-analysis.md) · [Test cases](../features/<FEATURE_CODE>/test-cases.md) · [Results](../features/<FEATURE_CODE>/test-results.md) | `<trạng thái>` |

## 2. Tổng hợp test case và kết quả

Đếm theo `T-ID` duy nhất của Domain/EP và BVA trong run được nêu. Một case có thể phủ cả hai phương pháp; không cộng các subtotal kỹ thuật. Rerun tạo EV-ID mới nhưng không tạo test case mới. `Đã chạy = PASS + FAIL + Quan sát`; `Thiết kế = Đã chạy + BLOCKED + Chưa chạy`.

| Feature / Run ID | Thiết kế | Đã chạy | PASS | FAIL | Quan sát | BLOCKED | Chưa chạy | Báo cáo chi tiết |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `<mã / run>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` | [Results](../features/<FEATURE_CODE>/test-results.md) |
| **Tổng** | **`<n>`** | **`<n>`** | **`<n>`** | **`<n>`** | **`<n>`** | **`<n>`** | **`<n>`** | |

`<ghi chú: các lớp case được cộng, số ca quan sát/inconclusive không tính PASS/FAIL, ca BLOCKED nếu có>`

## 3. Tổng hợp bug

Mỗi bug độc lập có một dòng trong bảng và một mục chi tiết bên dưới. Bug ID mang mã feature (`BUG-<FEATURE>-NN`) để tra cứu khi tổng hợp nhiều feature.

### 3.1. Bảng tổng hợp bug

| Bug ID | Feature | Title | Severity | Priority | Related TC | Status | Evidence | GitHub Issue |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BUG-<FEATURE>-01 | `<mã>` | `<title>` | `<sev>` | `<priority>` | `<TC>` | Đã tái hiện; chờ SV xác nhận | `<log>` | Chờ SV xác nhận |

### 3.2. Thống kê bug theo severity

| Feature | Critical | High | Medium | Low | Tổng |
| --- | ---: | ---: | ---: | ---: | ---: |
| `<mã + tên>` | `<n>` | `<n>` | `<n>` | `<n>` | `<n>` |
| **Tổng** | **`<n>`** | **`<n>`** | **`<n>`** | **`<n>`** | **`<n>`** |

### 3.3. Tiêu chí phân loại severity

| Severity | Tiêu chí |
| --- | --- |
| **Critical** | Lộ/mất dữ liệu nhạy cảm, lỗi bảo mật nghiêm trọng hoặc hệ thống ngừng hoạt động trên luồng chính. |
| **High** | Chức năng cốt lõi hoặc business rule quan trọng sai, gây chặn người dùng hoặc xử lý sai đáng kể. |
| **Medium** | Quy tắc chức năng hoặc validation sai với ảnh hưởng giới hạn hơn High. |
| **Low** | Sai lệch hiển thị/nội dung nhỏ, ít ảnh hưởng đến việc hoàn thành tác vụ. |

Priority là mức ưu tiên xử lý; đánh giá riêng theo mức ảnh hưởng, tần suất và tính cấp bách.

### 3.4. Chi tiết từng bug (manual reproduction)

Mỗi mục ghi rõ cách tái hiện bằng tay, giá trị cụ thể và kết quả mong đợi. **Sau khi xác nhận bug, người kiểm thử chụp screenshot và gắn vào GitHub Issue bắt buộc của HW02.** Kết thúc mỗi mục bằng dòng `---` để tách.

#### BUG-<FEATURE>-01 — <title>

**Feature:** `<mã>` | **Severity:** `<sev>` | **Priority:** `<priority>` | **Test case:** `<TC>` | **Evidence:** `<log>`

**Tiền điều kiện:** `<tài khoản cụ thể + state cụ thể>`

1. `<bước với giá trị cụ thể>`
2. `<...>`

**Expected:** `<theo đặc tả + rule>`. **Actual:** `<kết quả quan sát>`.
**Root cause:** `<file:dòng, chỉ khi có bằng chứng>`.
**Chi tiết đầy đủ:** [`<link feature report §7.4>`](<...>). **GitHub Issue / Screenshot:** Chờ người kiểm thử xác nhận bug rồi tạo Issue và gắn ảnh.

---

#### BUG-<FEATURE>-02 — <title>

`<lặp lại khối trên cho mỗi bug; luôn kết thúc bằng dòng '---'>`

---
