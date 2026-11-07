# BUG-GUI-06 — Bảng lịch sử đơn hàng gây horizontal scroll ở viewport 360px

**GitHub Issue:** chưa publish — draft tại [`issues/BUG-GUI-06.md`](../issues/BUG-GUI-06.md)

## Tóm tắt

Bảng lịch sử đơn hàng gây horizontal scroll ở viewport 360px. Bug được phát hiện khi thực thi checklist GUI Task 1 trên màn hình `/profile`.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-04 — Hồ sơ cá nhân |
| Checklist | CHK-15 |
| Màn hình | `/profile` |
| Môi trường | Chromium 158 / Playwright 1.65; backend `http://localhost:3000`; web `http://localhost:5173`; viewport 1280×900 (mobile 360×800 khi có kiểm tra responsive). |
| Severity / Priority | **Major** / High |
| Lặp lại | 1/1 trên build hiện tại |

## Các bước tái hiện

1. Đăng nhập, mở `/profile` ở viewport 360×800 với ít nhất một đơn hàng.
2. Đo `document.documentElement.scrollWidth` và `clientWidth`.

| Mốc | Expected | Actual |
| --- | --- | --- |
| Sau thao tác | Bảng co giãn hoặc nằm trong vùng scroll riêng; cả trang không có horizontal scroll. | `scrollWidth` = 399px, `clientWidth` = 360px (tràn 39px); bảng 5 cột giữ nguyên width desktop và bị cắt. |

## Bằng chứng

![BUG-GUI-06 — CHK-15-profile-mobile-table.png](../screenshots/CHK-15-profile-mobile-table.png)

## Nguyên nhân đối chiếu mã nguồn

**[`frontend-web/src/pages/Profile.jsx:171`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Profile.jsx#L171)–[L179](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Profile.jsx#L179)**

```jsx
          <table className="w-full text-left">
            <thead>
              <tr className="border-b bg-gray-50">
                <th className="p-2">Mã ĐH</th>
                <th className="p-2">Ngày đặt</th>
                <th className="p-2">Tổng tiền</th>
                <th className="p-2">Trạng thái</th>
                <th className="p-2">Thao tác</th>
              </tr>
```

`<table className="w-full text-left">` không có wrapper `overflow-x-auto` hay layout card cho mobile.

## Đề xuất sửa

Bọc bảng trong `overflow-x-auto` với `min-width`, hoặc render card đơn hàng dưới breakpoint `md`.

## Ghi chú

Screenshot được chụp trên SUT đang chạy tại `http://localhost:5173`; code block lấy trực tiếp từ source tại commit [`85af3ba`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9).
