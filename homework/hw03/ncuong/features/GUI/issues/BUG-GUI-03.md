# [BUG-GUI-03] Text phụ và nút đỏ không đạt WCAG 2.2 AA về contrast

**Severity:** Major · **Priority:** High · **FR:** FR-21 — Tiêu chuẩn giao diện chung · **Screen:** `/register, /profile`

## Mô tả

axe-core báo helper text `#9ca3af` trên `#ffffff` = 2.53:1; trắng trên `#ef4444` = 3.76:1; vàng `#fde047` trên xanh `#2563eb` = 3.92:1; nút đăng xuất đỏ/trắng = 3.76:1.

## Các bước tái hiện

1. Mở `/register` và `/profile` (đã đăng nhập).
2. Chạy axe-core hoặc tính contrast của helper text, nút đỏ, username vàng và nút đăng xuất.

## Expected

Text thường đạt tối thiểu 4.5:1 so với nền; text lớn đạt 3:1.

## Actual

axe-core báo helper text `#9ca3af` trên `#ffffff` = 2.53:1; trắng trên `#ef4444` = 3.76:1; vàng `#fde047` trên xanh `#2563eb` = 3.92:1; nút đăng xuất đỏ/trắng = 3.76:1.

## Checklist IDs

CHK-07, CHK-16

## Nguyên nhân

**[`frontend-web/src/pages/Register.jsx:64`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Register.jsx#L64)–[L65](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Register.jsx#L65)**

```jsx
          <p className="text-xs text-gray-400 mt-1">
            Yêu cầu: Tối thiểu 8 ký tự, có chữ hoa, chữ thường, số và ký tự đặc biệt.
```

Helper text dùng `text-gray-400` trên nền trắng.

**[`frontend-web/src/pages/Register.jsx:70`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Register.jsx#L70)–[L75](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Register.jsx#L75)**

```jsx
        <button
          type="submit"
          className="w-full bg-red-500 text-white py-2 rounded hover:bg-red-600"
        >
          Đăng Ký
        </button>
```

Nút tích cực dùng `bg-red-500` với chữ trắng.

**[`frontend-web/src/App.jsx:26`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/App.jsx#L26)–[L29](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/App.jsx#L29)**

```jsx
            <Link to="/profile" className="hover:underline text-yellow-300">
              <span dangerouslySetInnerHTML={{ __html: `Chào, ${user.name}` }} />
            </Link>
            <button onClick={logout} className="bg-red-500 px-3 py-1 rounded">Thoát</button>
```

Username dùng `text-yellow-300` trên nền xanh; nút đăng xuất dùng `bg-red-500` với chữ trắng.

## Đề xuất sửa

Dùng màu đậm hơn cho helper text và nút đỏ, hoặc đổi sang nền sáng/chữ tối; chạy lại axe-core sau khi sửa.

## Screenshots

![BUG-GUI-03](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-07-register-contrast.png)

![BUG-GUI-03](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-16-profile-contrast.png)


> Screenshot dùng raw URL trên nhánh `ncuong`; cần push nhánh này trước khi publish issue.
