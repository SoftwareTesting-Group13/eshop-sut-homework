# [BUG-GUI-19] Navbar không chỉ ra trang hiện tại

**Severity:** Minor · **Priority:** Medium · **FR:** FR-23 — Navigation · **Screen:** `/profile`

## Mô tả

Chỉ có hover style; không có `aria-current`, active class hay underline cho `/profile`.

## Các bước tái hiện

1. Đăng nhập và mở `/profile`.
2. Kiểm tra `aria-current`, class active hoặc underline trên các link header.

## Expected

Trang hiện tại được chỉ ra bằng visual state và `aria-current="page"` (FR-23).

## Actual

Chỉ có hover style; không có `aria-current`, active class hay underline cho `/profile`.

## Checklist IDs

CHK-48

## Nguyên nhân

**[`frontend-web/src/App.jsx:20`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/App.jsx#L20)–[L38](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/App.jsx#L38)**

```jsx
    <header className="bg-blue-600 text-white p-4 flex justify-between items-center">
      <Link to="/" className="text-2xl font-bold">EShop</Link>
      <nav className="flex gap-4 items-center">
        <Link to="/cart" className="hover:underline">Giỏ hàng</Link>
        {user ? (
          <div className="flex gap-4 items-center">
            <Link to="/profile" className="hover:underline text-yellow-300">
              <span dangerouslySetInnerHTML={{ __html: `Chào, ${user.name}` }} />
            </Link>
            <button onClick={logout} className="bg-red-500 px-3 py-1 rounded">Thoát</button>
          </div>
        ) : (
          <>
            <Link to="/login" className="hover:underline">Đăng nhập</Link>
            <Link to="/register" className="hover:underline">Đăng ký</Link>
          </>
        )}
      </nav>
    </header>
```

Header dùng `<Link>` thường, không dùng `<NavLink>` và không có active style.

## Đề xuất sửa

Dùng `<NavLink>` với `aria-current="page"` và class active.

## Screenshots

![BUG-GUI-19](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-48-profile-active-nav.png)


> Screenshot dùng raw URL trên nhánh `ncuong`; cần push nhánh này trước khi publish issue.
