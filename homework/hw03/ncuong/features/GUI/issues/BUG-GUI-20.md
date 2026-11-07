# [BUG-GUI-20] Nút Login và Register không có loading/disabled state

**Severity:** Minor · **Priority:** Medium · **FR:** FR-01 — Đăng ký; FR-02 — Đăng nhập · **Screen:** `/login, /register`

## Mô tả

Nút vẫn enabled và giữ nguyên label; người dùng có thể submit lặp và không biết request đang chạy.

## Các bước tái hiện

1. Delay `/api/login` hoặc `/api/register` khoảng 2 giây.
2. Bấm submit và quan sát nút trong lúc request đang chạy.

## Expected

Nút bị disable, có spinner hoặc đổi label và expose `aria-busy`.

## Actual

Nút vẫn enabled và giữ nguyên label; người dùng có thể submit lặp và không biết request đang chạy.

## Checklist IDs

CHK-49, CHK-56

## Nguyên nhân

**[`frontend-web/src/pages/Login.jsx:12`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Login.jsx#L12)–[L20](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Login.jsx#L20)**

```jsx
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(email, password);
      navigate('/');
    } catch (err) {
      setError('Đăng nhập thất bại. Vui lòng kiểm tra lại.');
    }
  };
```

Không có state `submitting`; button không bị disable.

**[`frontend-web/src/pages/Register.jsx:12`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Register.jsx#L12)–[L28](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Register.jsx#L28)**

```jsx
  const handleSubmit = async (e) => {
    e.preventDefault();

    const flawedStrongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\s)[A-Za-z\d\s]{8,}$/;

    if (!flawedStrongPasswordRegex.test(password)) {
      setError('Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT.');
      return;
    }

    try {
      await axios.post('http://localhost:3000/api/register', { name, email, password });
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.error || 'Đăng ký thất bại.');
    }
  };
```

Cùng pattern ở Register.

## Đề xuất sửa

Thêm state `submitting`, disable button và hiển thị spinner/“Đang xử lý…”, kèm `aria-busy`.

## Screenshots

![BUG-GUI-20](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-49-login-loading.png)

![BUG-GUI-20](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-56-register-loading.png)


> Screenshot dùng raw URL trên nhánh `ncuong`; cần push nhánh này trước khi publish issue.
