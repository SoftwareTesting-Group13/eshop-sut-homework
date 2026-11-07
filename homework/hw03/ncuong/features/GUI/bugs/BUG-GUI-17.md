# BUG-GUI-17 — Focus bị mất sau khi chuyển sang bước OTP

**GitHub Issue:** [#95](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/95)

## Tóm tắt

Focus bị mất sau khi chuyển sang bước OTP. Bug được phát hiện khi thực thi checklist GUI Task 1 trên màn hình `/forgot-password`.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-03 — Quên mật khẩu |
| Checklist | CHK-43 |
| Màn hình | `/forgot-password` |
| Môi trường | Chromium 158 / Playwright 1.65; backend `http://localhost:3000`; web `http://localhost:5173`; viewport 1280×900 (mobile 360×800 khi có kiểm tra responsive). |
| Severity / Priority | **Minor** / Medium |
| Lặp lại | 1/1 trên build hiện tại |

## Các bước tái hiện

1. Yêu cầu OTP thành công.
2. Kiểm tra `document.activeElement` sau khi bước 2 render.

| Mốc | Expected | Actual |
| --- | --- | --- |
| Sau thao tác | Focus chuyển tới ô OTP hoặc heading bước 2 và thay đổi được announce. | `document.activeElement` là `BODY`; người dùng screen-reader/bàn phím không biết bước đã đổi. |

## Bằng chứng

![BUG-GUI-17 — CHK-43-forgot-focus.png](../screenshots/CHK-43-forgot-focus.png)

## Nguyên nhân đối chiếu mã nguồn

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

## Ghi chú

Screenshot được chụp trên SUT đang chạy tại `http://localhost:5173`; code block lấy trực tiếp từ source tại commit [`85af3ba`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9).
