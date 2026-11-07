# BUG-GUI-01 — Tiêu đề trang Đăng nhập ghi “Đăng Ký” thay vì “Đăng nhập”

**GitHub Issue:** [#90](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/90)

## Tóm tắt

Tiêu đề trang Đăng nhập ghi “Đăng Ký” thay vì “Đăng nhập”. Bug được phát hiện khi thực thi checklist GUI Task 1 trên màn hình `/login`.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-02 — Đăng nhập |
| Checklist | CHK-01 |
| Màn hình | `/login` |
| Môi trường | Chromium 158 / Playwright 1.65; backend `http://localhost:3000`; web `http://localhost:5173`; viewport 1280×900 (mobile 360×800 khi có kiểm tra responsive). |
| Severity / Priority | **Minor** / Medium |
| Lặp lại | 1/1 trên build hiện tại |

## Các bước tái hiện

1. Mở `http://localhost:5173/login` trong cửa sổ chưa đăng nhập.
2. Đọc tiêu đề trên card đăng nhập, ngay phía trên hai ô nhập.

| Mốc | Expected | Actual |
| --- | --- | --- |
| Sau thao tác | Tiêu đề mô tả đúng màn hình Đăng nhập (ví dụ “Đăng nhập”) và là một thẻ `<h1>`. | Tiêu đề là `<h2>Đăng Ký</h2>`; trang không có `<h1>`. Người dùng có thể tưởng đang ở màn hình đăng ký. |

## Bằng chứng

![BUG-GUI-01 — CHK-01-login-heading.png](../screenshots/CHK-01-login-heading.png)

## Nguyên nhân đối chiếu mã nguồn

**[`frontend-web/src/pages/Login.jsx:24`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Login.jsx#L24)**

```jsx
      <h2 className="text-2xl font-bold mb-6 text-center">Đăng Ký</h2>
```

Chuỗi tiêu đề bị copy từ màn hình Register và không được sửa lại.

## Đề xuất sửa

Đổi tiêu đề thành “Đăng nhập” và dùng `<h1>` cho tiêu đề trang; thêm kiểm tra heading vào test auth.

## Ghi chú

Screenshot được chụp trên SUT đang chạy tại `http://localhost:5173`; code block lấy trực tiếp từ source tại commit [`85af3ba`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9).
