# [BUG-GUI-17] Focus bị mất sau khi chuyển sang bước OTP

**Severity:** Minor · **Priority:** Medium · **FR:** FR-03 — Quên mật khẩu · **Screen:** `/forgot-password`

## Mô tả

`document.activeElement` là `BODY`; người dùng screen-reader/bàn phím không biết bước đã đổi.

## Các bước tái hiện

1. Yêu cầu OTP thành công.
2. Kiểm tra `document.activeElement` sau khi bước 2 render.

## Expected

Focus chuyển tới ô OTP hoặc heading bước 2 và thay đổi được announce.

## Actual

`document.activeElement` là `BODY`; người dùng screen-reader/bàn phím không biết bước đã đổi.

## Checklist IDs

CHK-43

## Nguyên nhân

**[`frontend-web/src/pages/ForgotPassword.jsx:13`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/ForgotPassword.jsx#L13)–[L22](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/ForgotPassword.jsx#L22)**

```jsx
  const handleRequest = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:3000/api/forgot-password', { email });
      setMessage(`Mã OTP của bạn là: ${res.data.resetToken}`);
      setStep(2);
    } catch (err) {
      alert("Lỗi: " + (err.response?.data?.error || err.message));
    }
  };
```

`setStep(2)` không kèm focus management.

## Đề xuất sửa

Dùng `useEffect` để focus heading/input bước 2 và thêm `aria-live` cho status message.

## Screenshots

![BUG-GUI-17](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-43-forgot-focus.png)


> Screenshot dùng raw URL trên nhánh `ncuong`; cần push nhánh này trước khi publish issue.
