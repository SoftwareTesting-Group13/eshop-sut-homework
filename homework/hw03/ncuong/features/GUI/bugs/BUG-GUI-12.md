# BUG-GUI-12 — Form đăng ký và đặt lại mật khẩu thiếu trường xác nhận mật khẩu

**GitHub Issue:** [#94](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/94)

## Tóm tắt

Form đăng ký và đặt lại mật khẩu thiếu trường xác nhận mật khẩu. Bug được phát hiện khi thực thi checklist GUI Task 1 trên màn hình `/register, /forgot-password`.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-01 — Đăng ký; FR-03 — Đặt lại mật khẩu |
| Checklist | CHK-24, CHK-28 |
| Màn hình | `/register, /forgot-password` |
| Môi trường | Chromium 158 / Playwright 1.65; backend `http://localhost:3000`; web `http://localhost:5173`; viewport 1280×900 (mobile 360×800 khi có kiểm tra responsive). |
| Severity / Priority | **Minor** / Medium |
| Lặp lại | 1/1 trên build hiện tại |

## Các bước tái hiện

1. Mở `/register` và bước 2 của `/forgot-password`.
2. Đếm số input mật khẩu trên mỗi form.

| Mốc | Expected | Actual |
| --- | --- | --- |
| Sau thao tác | Có trường xác nhận mật khẩu và chặn khi hai trường không khớp (FR-01, FR-03). | Mỗi form chỉ có một input mật khẩu; lỗi gõ nhầm không được phát hiện trước khi tạo tài khoản hoặc đổi mật khẩu. |

## Bằng chứng

![BUG-GUI-12 — CHK-24-register-no-confirm.png](../screenshots/CHK-24-register-no-confirm.png)

![BUG-GUI-12 — CHK-28-forgot-no-confirm.png](../screenshots/CHK-28-forgot-no-confirm.png)

## Nguyên nhân đối chiếu mã nguồn

**[`frontend-web/src/pages/Register.jsx:55`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Register.jsx#L55)–[L67](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Register.jsx#L67)**

```jsx
        <div>
          <label className="block text-gray-700 mb-2">Mật khẩu</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border p-2 rounded"
            required
          />
          <p className="text-xs text-gray-400 mt-1">
            Yêu cầu: Tối thiểu 8 ký tự, có chữ hoa, chữ thường, số và ký tự đặc biệt.
          </p>
        </div>
```

Chỉ có một input `Mật khẩu`.

**[`frontend-web/src/pages/ForgotPassword.jsx:78`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/ForgotPassword.jsx#L78)–[L87](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/ForgotPassword.jsx#L87)**

```jsx
          <div>
            <label className="block text-gray-700 mb-2">Mật khẩu mới</label>
            <input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              className="w-full border p-2 rounded"
              required
            />
          </div>
```

Chỉ có một input `Mật khẩu mới`.

## Đề xuất sửa

Thêm input xác nhận mật khẩu và kiểm tra khớp trước khi submit.

## Ghi chú

Screenshot được chụp trên SUT đang chạy tại `http://localhost:5173`; code block lấy trực tiếp từ source tại commit [`85af3ba`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9).
