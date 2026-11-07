# BUG-GUI-14 — Regex số điện thoại từ chối số Việt Nam hợp lệ và dùng alert chặn

**GitHub Issue:** [#80](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/80)

## Tóm tắt

Regex số điện thoại từ chối số Việt Nam hợp lệ và dùng alert chặn. Bug được phát hiện khi thực thi checklist GUI Task 1 trên màn hình `/profile`.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-04 — Hồ sơ cá nhân |
| Checklist | CHK-31 |
| Màn hình | `/profile` |
| Môi trường | Chromium 158 / Playwright 1.65; backend `http://localhost:3000`; web `http://localhost:5173`; viewport 1280×900 (mobile 360×800 khi có kiểm tra responsive). |
| Severity / Priority | **Blocker** / High |
| Lặp lại | 1/1 trên build hiện tại |

## Các bước tái hiện

1. Đăng nhập và mở `/profile`.
2. Nhập số `0912345678` (đúng placeholder) và bấm “Cập nhật”.

| Mốc | Expected | Actual |
| --- | --- | --- |
| Sau thao tác | Số bắt đầu bằng `0`, dài 10–11 chữ số được chấp nhận và lưu hồ sơ (FR-04). | Alert “Số điện thoại không hợp lệ...” hiện ra. Regex `/^[1-9][0-9]{8,9}$/` từ chối mọi số bắt đầu bằng `0`, gồm cả placeholder `0912345678`; lỗi dùng `alert()` thay vì inline. |

## Bằng chứng

![BUG-GUI-14 — CHK-31-profile-phone-alert.png](../screenshots/CHK-31-profile-phone-alert.png)

## Nguyên nhân đối chiếu mã nguồn

**[`frontend-web/src/pages/Profile.jsx:40`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Profile.jsx#L40)–[L46](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Profile.jsx#L46)**

```jsx
  const handleUpdate = async (e) => {
    e.preventDefault();

    if (!/^[1-9][0-9]{8,9}$/.test(phone)) {
      alert("Số điện thoại không hợp lệ. Vui lòng nhập đúng 9-10 chữ số.");
      return;
    }
```

Regex bắt đầu bằng `[1-9]` và dùng `alert()`.

## Đề xuất sửa

Dùng `/^0\d{9,10}$/` (hoặc thư viện validate), thêm `inputmode="tel"` và hiển thị lỗi inline.

## Ghi chú

Screenshot được chụp trên SUT đang chạy tại `http://localhost:5173`; code block lấy trực tiếp từ source tại commit [`85af3ba`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9).
