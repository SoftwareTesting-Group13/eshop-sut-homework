# [BUG-GUI-23] UI render nguyên văn lỗi kỹ thuật từ server

**Severity:** Major · **Priority:** High · **FR:** FR-01 — Đăng ký; FR-24 — Feedback · **Screen:** `/register`

## Mô tả

UI hiển thị “SQLITE_ERROR: no such column: name” vì catch block dùng trực tiếp `err.response.data.error`.

## Các bước tái hiện

1. Giả lập `POST /api/register` trả 500 với body chứa lỗi SQLite.
2. Submit form đăng ký.

## Expected

Thông báo lỗi thân thiện, generic; chi tiết kỹ thuật chỉ nằm trong log server.

## Actual

UI hiển thị “SQLITE_ERROR: no such column: name” vì catch block dùng trực tiếp `err.response.data.error`.

## Checklist IDs

CHK-55

## Nguyên nhân

**[`frontend-web/src/pages/Register.jsx:25`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Register.jsx#L25)–[L27](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Register.jsx#L27)**

```jsx
    } catch (err) {
      setError(err.response?.data?.error || 'Đăng ký thất bại.');
    }
```

Render `err.response?.data?.error` trực tiếp ra UI.

## Đề xuất sửa

Map lỗi đã biết sang message thân thiện; log raw error ở server; không render database message.

## Screenshots

![BUG-GUI-23](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-55-register-raw-error.png)


> Screenshot dùng raw URL trên nhánh `ncuong`; cần push nhánh này trước khi publish issue.
