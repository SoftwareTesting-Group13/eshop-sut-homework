# [BUG-GUI-08] Ô email dùng `type=text` và ô mật khẩu hiển thị rõ ký tự

**Severity:** Major · **Priority:** High · **FR:** FR-02 — Đăng nhập; FR-22 — Form · **Screen:** `/login`

## Mô tả

Cả hai input đều là `type="text"`; mật khẩu hiển thị rõ và nhãn thứ nhất là “Username” dù backend xác thực bằng email.

## Các bước tái hiện

1. Mở `/login`.
2. Nhập email và mật khẩu; kiểm tra `type` của hai input.

## Expected

Ô email dùng `type="email"`; ô mật khẩu dùng `type="password"` (FR-02, FR-22).

## Actual

Cả hai input đều là `type="text"`; mật khẩu hiển thị rõ và nhãn thứ nhất là “Username” dù backend xác thực bằng email.

## Checklist IDs

CHK-17, CHK-18

## Nguyên nhân

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

## Screenshots

![BUG-GUI-08](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-17-18-19-login-fields.png)


> Screenshot dùng raw URL trên nhánh `ncuong`; cần push nhánh này trước khi publish issue.
