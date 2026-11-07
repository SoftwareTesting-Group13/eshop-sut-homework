# BUG-GUI-19 — Navbar không chỉ ra trang hiện tại

**GitHub Issue:** chưa publish — draft tại [`issues/BUG-GUI-19.md`](../issues/BUG-GUI-19.md)

## Tóm tắt

Navbar không chỉ ra trang hiện tại. Bug được phát hiện khi thực thi checklist GUI Task 1 trên màn hình `/profile`.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-23 — Navigation |
| Checklist | CHK-48 |
| Màn hình | `/profile` |
| Môi trường | Chromium 158 / Playwright 1.65; backend `http://localhost:3000`; web `http://localhost:5173`; viewport 1280×900 (mobile 360×800 khi có kiểm tra responsive). |
| Severity / Priority | **Minor** / Medium |
| Lặp lại | 1/1 trên build hiện tại |

## Các bước tái hiện

1. Đăng nhập và mở `/profile`.
2. Kiểm tra `aria-current`, class active hoặc underline trên các link header.

| Mốc | Expected | Actual |
| --- | --- | --- |
| Sau thao tác | Trang hiện tại được chỉ ra bằng visual state và `aria-current="page"` (FR-23). | Chỉ có hover style; không có `aria-current`, active class hay underline cho `/profile`. |

## Bằng chứng

![BUG-GUI-19 — CHK-48-profile-active-nav.png](../screenshots/CHK-48-profile-active-nav.png)

## Nguyên nhân đối chiếu mã nguồn

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

## Ghi chú

Screenshot được chụp trên SUT đang chạy tại `http://localhost:5173`; code block lấy trực tiếp từ source tại commit [`85af3ba`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9).
