# [BUG-GUI-25] Loading và lỗi tải đơn hàng đều hiển thị thành “chưa có đơn hàng”

**Severity:** Major · **Priority:** High · **FR:** FR-04 — Hồ sơ cá nhân; FR-24 — Feedback · **Screen:** `/profile`

## Mô tả

“Bạn chưa có đơn hàng nào.” hiện ngay trong lúc loading và sau response 500; người dùng không phân biệt được “chưa có đơn” với “tải thất bại”.

## Các bước tái hiện

1. Delay `/api/orders/my-orders` rồi mở `/profile`.
2. Lặp lại với response 500.

## Expected

Có loading state khi đang fetch và error state riêng (kèm retry) khi request thất bại.

## Actual

“Bạn chưa có đơn hàng nào.” hiện ngay trong lúc loading và sau response 500; người dùng không phân biệt được “chưa có đơn” với “tải thất bại”.

## Checklist IDs

CHK-62, CHK-63

## Nguyên nhân

**[`frontend-web/src/pages/Profile.jsx:14`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Profile.jsx#L14)–[L29](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Profile.jsx#L29)**

```jsx
  const fetchOrders = () => {
    if (!token) return;

    axios
      .get("http://localhost:3000/api/orders/my-orders", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        const data = Array.isArray(res.data) ? res.data : res.data.orders || [];
        setOrders(data);
      })
      .catch((err) => {
        console.error("Lỗi lấy đơn hàng:", err);
        setOrders([]);
      });
  };
```

`catch` đặt `orders=[]`; không có state loading/error.

**[`frontend-web/src/pages/Profile.jsx:168`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Profile.jsx#L168)–[L169](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9/frontend-web/src/pages/Profile.jsx#L169)**

```jsx
        {orders.length === 0 ? (
          <p>Bạn chưa có đơn hàng nào.</p>
```

Chỉ có một nhánh empty state cho mọi trường hợp.

## Đề xuất sửa

Thêm state `loading`/`error`, render ba nhánh riêng và nút retry.

## Screenshots

![BUG-GUI-25](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-62-profile-orders-loading.png)

![BUG-GUI-25](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw03/ncuong/features/GUI/screenshots/CHK-63-profile-orders-error.png)


> Screenshot dùng raw URL trên nhánh `ncuong`; cần push nhánh này trước khi publish issue.
