# BUG-GUI-25 — Loading và lỗi tải đơn hàng đều hiển thị thành “chưa có đơn hàng”

**GitHub Issue:** [#89](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/89)

## Tóm tắt

Loading và lỗi tải đơn hàng đều hiển thị thành “chưa có đơn hàng”. Bug được phát hiện khi thực thi checklist GUI Task 1 trên màn hình `/profile`.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-04 — Hồ sơ cá nhân; FR-24 — Feedback |
| Checklist | CHK-62, CHK-63 |
| Màn hình | `/profile` |
| Môi trường | Chromium 158 / Playwright 1.65; backend `http://localhost:3000`; web `http://localhost:5173`; viewport 1280×900 (mobile 360×800 khi có kiểm tra responsive). |
| Severity / Priority | **Major** / High |
| Lặp lại | 1/1 trên build hiện tại |

## Các bước tái hiện

1. Delay `/api/orders/my-orders` rồi mở `/profile`.
2. Lặp lại với response 500.

| Mốc | Expected | Actual |
| --- | --- | --- |
| Sau thao tác | Có loading state khi đang fetch và error state riêng (kèm retry) khi request thất bại. | “Bạn chưa có đơn hàng nào.” hiện ngay trong lúc loading và sau response 500; người dùng không phân biệt được “chưa có đơn” với “tải thất bại”. |

## Bằng chứng

![BUG-GUI-25 — CHK-62-profile-orders-loading.png](../screenshots/CHK-62-profile-orders-loading.png)

![BUG-GUI-25 — CHK-63-profile-orders-error.png](../screenshots/CHK-63-profile-orders-error.png)

## Nguyên nhân đối chiếu mã nguồn

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

## Ghi chú

Screenshot được chụp trên SUT đang chạy tại `http://localhost:5173`; code block lấy trực tiếp từ source tại commit [`85af3ba`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/85af3ba875c88283615e22cb108f13e2fccaf0e9).
