# BUG-FR06-01 — Màn chi tiết sản phẩm không hiển thị danh mục

## Tóm tắt

Chọn bất kỳ sản phẩm fixture ID 1, 2 hoặc 5 từ danh sách và mở chi tiết. Màn hình có ảnh, tên, giá, mô tả nhưng không có tên danh mục, trái với FR-06.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-06 — Xem chi tiết sản phẩm; R1 trong [README FR-06](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/46a2d87e6e27b222dc857819be35a2268bf8bb45/README.md#L83-L89) |
| Test case | T01 (Điện thoại, ID 1), T02 (giá API dạng chuỗi, ID 2), T03 (Phụ kiện, ID 5) |
| Build / môi trường | Commit `46a2d87e6e27b222dc857819be35a2268bf8bb45` + thay đổi local `API_URL` để kết nối; Android emulator Pixel_10_Pro, Expo Go SDK 54, backend/SQLite test cách ly tại `10.0.2.2:3000/api` |
| Severity / Priority | Medium / Medium — người dùng không thấy một trong năm thông tin bắt buộc, ảnh hưởng mọi sản phẩm đã thử |
| Trạng thái / lặp lại | Đã xác nhận UI; 3/3 sản phẩm khác nhau trong ba lần mở chi tiết độc lập; đã mở [Issue #55](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/55) kèm 3 ảnh UI |

## Chuẩn bị để tái hiện

- Backend test có sản phẩm ID 1 “iPhone 15 Pro Max” thuộc danh mục 1 “Điện thoại”, ID 2 “Samsung Galaxy S24 Ultra” thuộc danh mục 1, ID 5 “Bàn phím cơ Keychron Q1” thuộc danh mục 3 “Phụ kiện”. API `GET /api/products/:id` trả `category_id` nhưng không trả tên danh mục.
- Mở Expo app “EShop Mobile” trên Android emulator với backend truy cập được; không cần đăng nhập. Trang bắt đầu là “Danh sách sản phẩm”.

## Các bước tái hiện và kết quả

**Đường tái hiện đã kiểm chứng:** UI Android Expo Go.

1. Ở Danh sách sản phẩm, chọn card iPhone 15 Pro Max và bấm **Xem chi tiết**.
2. Chờ màn chi tiết hiện đầy đủ; quan sát từ ảnh lớn đến nút **Thêm vào giỏ hàng**. Không có vùng nào ghi “Điện thoại” hoặc tên danh mục.
3. Quay lại danh sách, làm tương tự với Samsung Galaxy S24 Ultra và Bàn phím cơ Keychron Q1. Cả hai thiếu tên danh mục tương ứng.

| Mốc | Expected theo FR-06 | Actual UI |
| --- | --- | --- |
| ID 1 và 2 | Ảnh lớn, tên, giá, mô tả, “Điện thoại” | Bốn trường đầu có; không thấy “Điện thoại” |
| ID 5 | Ảnh lớn, tên, giá, mô tả, “Phụ kiện” | Bốn trường đầu có; không thấy “Phụ kiện” |

**Kết luận:** Cả ba màn chi tiết không hiển thị trường danh mục bắt buộc. Giá chuỗi của ID 2 vẫn render đúng, nên T02 chỉ FAIL ở danh mục.

## Cách kiểm tra thủ công trên UI

**Trạng thái:** Đã tái hiện qua UI, EV-FR06-008/009/010. Từ Danh sách sản phẩm, bấm **Xem chi tiết** lần lượt ở ba card trên; ảnh nên chụp toàn bộ card từ ảnh đến nút thêm giỏ, đối chiếu tên danh mục theo fixture. Đóng/mở app nếu cần quay về danh sách trên emulator.

## Bằng chứng

- [Evidence run và Actual](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR06/evidence/FR06-evidence.md) — EV-FR06-008, 009, 010.
- Screenshot: [ID 1](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T01-detail-ID1.png), [ID 2](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T02-detail-ID2.png), [ID 5](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T03-detail-ID5.png). Mỗi ảnh thấy toàn card chi tiết kết thúc ở nút thêm giỏ.
- Lặp lại: 3/3 lần trên ba sản phẩm khác nhau cùng fixture, không cộng ba lần đọc một màn.

### Ảnh xác nhận UI

![T01-detail-ID1](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T01-detail-ID1.png)

![T02-detail-ID2](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T02-detail-ID2.png)

![T03-detail-ID5](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T03-detail-ID5.png)

## Điều tra nguyên nhân

**Vị trí:** [`frontend-mobile/App.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/46a2d87e6e27b222dc857819be35a2268bf8bb45/frontend-mobile/App.js#L555-L564) dòng 555–564 của commit đã kiểm thử; thay đổi local API_URL chỉ ở đầu file, không tác động vùng này.

```jsx
          <Image
            source={{ uri: product.imageUrl }}
            style={styles.detailImage}
            resizeMode="stretch"
          />
          <Text style={styles.detailName}>{product.name}</Text>
          <Text style={styles.detailPrice}>{formatMoney(product.price)}</Text>
          <Text style={styles.description}>{product.description}</Text>

          <Text style={styles.label}>Số lượng:</Text>
```

**Cơ chế:** Renderer đi thẳng từ mô tả sang số lượng, không render danh mục. API chi tiết chỉ có `category_id`; app cần ánh xạ ID sang tên hoặc backend cung cấp tên. Expected/Actual dựa trên rule và screenshot; mã chỉ giải thích cơ chế.
