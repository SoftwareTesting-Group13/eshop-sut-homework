# BUG-GUI-23 — UI render nguyên văn lỗi kỹ thuật từ server

**GitHub Issue:** chưa publish — draft tại [`issues/BUG-GUI-23.md`](../issues/BUG-GUI-23.md)

## Tóm tắt

UI render nguyên văn lỗi kỹ thuật từ server. Bug được phát hiện khi thực thi checklist GUI Task 1 trên màn hình `/register`.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-01 — Đăng ký; FR-24 — Feedback |
| Checklist | CHK-55 |
| Màn hình | `/register` |
| Môi trường | Chromium 158 / Playwright 1.65; backend `http://localhost:3000`; web `http://localhost:5173`; viewport 1280×900 (mobile 360×800 khi có kiểm tra responsive). |
| Severity / Priority | **Major** / High |
| Lặp lại | 1/1 trên build hiện tại |

## Các bước tái hiện

1. Giả lập `POST /api/register` trả 500 với body chứa lỗi SQLite.
2. Submit form đăng ký.

| Mốc | Expected | Actual |
| --- | --- | --- |
| Sau thao tác | Thông báo lỗi thân thiện, generic; chi tiết kỹ thuật chỉ nằm trong log server. | UI hiển thị “SQLITE_ERROR: no such column: name” vì catch block dùng trực tiếp `err.response.data.error`. |

## Bằng chứng

![BUG-GUI-23 — CHK-55-register-raw-error.png](../screenshots/CHK-55-register-raw-error.png)

## Nguyên nhân đối chiếu mã nguồn

**[`frontend-web/src/pages/Register.jsx:25`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Register.jsx#L25)–[L27](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Register.jsx#L27)**

```jsx
    } catch (err) {
      setError(err.response?.data?.error || 'Đăng ký thất bại.');
    }
```

Render `err.response?.data?.error` trực tiếp ra UI.

## Đề xuất sửa

Map lỗi đã biết sang message thân thiện; log raw error ở server; không render database message.

## Ghi chú

Screenshot được chụp trên SUT đang chạy tại `http://localhost:5173`; code block lấy trực tiếp từ source tại commit [`85af3ba`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9).
