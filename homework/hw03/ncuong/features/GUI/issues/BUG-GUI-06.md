# [BUG-GUI-06] Bảng lịch sử đơn hàng gây horizontal scroll ở viewport 360px

**Severity:** Major · **Priority:** High · **FR:** FR-04 — Hồ sơ cá nhân · **Screen:** `/profile`

## Mô tả

`scrollWidth` = 399px, `clientWidth` = 360px (tràn 39px); bảng 5 cột giữ nguyên width desktop và bị cắt.

## Các bước tái hiện

1. Đăng nhập, mở `/profile` ở viewport 360×800 với ít nhất một đơn hàng.
2. Đo `document.documentElement.scrollWidth` và `clientWidth`.

## Expected

Bảng co giãn hoặc nằm trong vùng scroll riêng; cả trang không có horizontal scroll.

## Actual

`scrollWidth` = 399px, `clientWidth` = 360px (tràn 39px); bảng 5 cột giữ nguyên width desktop và bị cắt.

## Checklist IDs

CHK-15

## Nguyên nhân

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

## Screenshots

![BUG-GUI-06](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-15-profile-mobile-table.png)


> Screenshot dùng raw URL trên nhánh `ncuong`; cần push nhánh này trước khi publish issue.
