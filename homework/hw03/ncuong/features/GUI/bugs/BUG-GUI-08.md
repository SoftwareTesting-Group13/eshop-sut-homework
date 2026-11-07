# BUG-GUI-08 — Ô email dùng `type=text` và ô mật khẩu hiển thị rõ ký tự

**GitHub Issue:** [#83](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/83)

## Tóm tắt

Ô email dùng `type=text` và ô mật khẩu hiển thị rõ ký tự. Bug được phát hiện khi thực thi checklist GUI Task 1 trên màn hình `/login`.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-02 — Đăng nhập; FR-22 — Form |
| Checklist | CHK-17, CHK-18 |
| Màn hình | `/login` |
| Môi trường | Chromium 158 / Playwright 1.65; backend `http://localhost:3000`; web `http://localhost:5173`; viewport 1280×900 (mobile 360×800 khi có kiểm tra responsive). |
| Severity / Priority | **Major** / High |
| Lặp lại | 1/1 trên build hiện tại |

## Các bước tái hiện

1. Mở `/login`.
2. Nhập email và mật khẩu; kiểm tra `type` của hai input.

| Mốc | Expected | Actual |
| --- | --- | --- |
| Sau thao tác | Ô email dùng `type="email"`; ô mật khẩu dùng `type="password"` (FR-02, FR-22). | Cả hai input đều là `type="text"`; mật khẩu hiển thị rõ và nhãn thứ nhất là “Username” dù backend xác thực bằng email. |

## Bằng chứng

![BUG-GUI-08 — CHK-17-18-19-login-fields.png](../screenshots/CHK-17-18-19-login-fields.png)

## Nguyên nhân đối chiếu mã nguồn

**[`frontend-web/src/pages/Login.jsx:28`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Login.jsx#L28)–[L45](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Login.jsx#L45)**

```jsx
          <label className="block text-gray-700 mb-2">Username</label>
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border p-2 rounded"
            required
          />
        </div>
        <div>
          <label className="block text-gray-700 mb-2">Mật khẩu</label>
          <input
            type="text"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border p-2 rounded"
            required
          />
```

Hai input đều khai báo `type="text"`; label không phải “Email”.

## Đề xuất sửa

Đổi input email sang `type="email"`, input mật khẩu sang `type="password"` và đổi nhãn thành “Email”.

## Ghi chú

Screenshot được chụp trên SUT đang chạy tại `http://localhost:5173`; code block lấy trực tiếp từ source tại commit [`85af3ba`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9).
