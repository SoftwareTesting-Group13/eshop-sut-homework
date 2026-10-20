# BUG-FR06-02 — Số lượng không hợp lệ vẫn được thêm vào giỏ

## Tóm tắt

Ở màn chi tiết, để ô Số lượng rỗng hoặc nhập `0`, `-1`, `1.5`, `abc`, `2abc` rồi bấm thêm. App luôn báo thành công và tạo dòng giỏ quantity `1` hoặc `2`, dù FR-06 chỉ cho phép số nguyên dương tối thiểu 1.

| Mục | Giá trị |
| --- | --- |
| Feature / rule | FR-06 — Xem chi tiết sản phẩm; R2 trong [README FR-06](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/46a2d87e6e27b222dc857819be35a2268bf8bb45/README.md#L83-L89) |
| Test case | T10 rỗng; T11 `0` (BVA ngay dưới biên); T12 `-1`; T13 `1.5`; T14 `abc`; T16 `2abc` |
| Build / môi trường | Commit `46a2d87e6e27b222dc857819be35a2268bf8bb45` + thay đổi local `API_URL`; Android emulator Pixel_10_Pro, Expo Go SDK 54; giỏ cục bộ, backend test cách ly |
| Severity / Priority | Medium / High — giá trị invalid âm thầm biến thành số lượng mua thực, ảnh hưởng ý định mua hàng và tổng tiền |
| Trạng thái / lặp lại | Đã xác nhận UI: 6 lớp input, T10/T11 còn lặp lại từ giỏ rỗng; đã mở [Issue #56](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/56) kèm 7 ảnh UI |

## Chuẩn bị để tái hiện

- Mở app ở Danh sách sản phẩm, chưa đăng nhập; backend test có sản phẩm ID 1 “iPhone 15 Pro Max”, giá 30.000.000 ₫. Force-stop/mở lại Expo app để Giỏ `(0)` trước từng giá trị.
- Chọn card iPhone ID 1 → **Xem chi tiết**. Ô Số lượng mặc định `1`.

## Các bước tái hiện và kết quả

**Đường tái hiện đã kiểm chứng:** UI Android Expo Go; thay giá trị TextInput bằng `adb shell input text` hoặc xóa bằng keyevent. `abc`/`2abc` được đưa vào control qua ADB, vì vậy đường gõ/dán bằng bàn phím mềm chưa xác nhận; rỗng/`0`/`-1`/`1.5` độc lập xác nhận bug.

1. Chạm ô **Số lượng**, xóa `1`, để trống hoặc nhập chính xác `0`.
2. Bấm **Thêm vào giỏ hàng**. App hiện alert “Thành công — Đã thêm vào giỏ hàng”.
3. Vào **Giỏ** (trên emulator dùng keyboard focus `Tab` đến “Giỏ (1)” rồi `Enter`, do thanh điều hướng bị status bar che), thấy iPhone quantity `1` và thành tiền `30,000,000 ₫`.
4. Reset app/giỏ về `(0)`, lặp lại độc lập với `-1`, `1.5`, `abc`, `2abc`. Với `2abc`, quantity thực là `2`, thành tiền `60,000,000 ₫`.

| Input | Expected theo FR-06 | Actual UI/Giỏ |
| --- | --- | --- |
| Rỗng, `0`, `-1` | Không nhận làm quantity hợp lệ, không thêm hàng | Alert thành công; giỏ quantity `1` |
| `1.5` | Không nhận số phân số | Alert thành công; giỏ quantity `1` |
| `abc` | Không nhận chữ | Alert thành công; giỏ quantity `1` |
| `2abc` | Không nhận chuỗi hỗn hợp | Alert thành công; giỏ quantity `2` |

**Kết luận:** Giá trị đang hiển thị ở TextInput không được validate trước khi thêm. Không tự đặt câu chữ hay thời điểm báo lỗi làm oracle; yêu cầu cốt lõi là không nhận chính input invalid này.

## Cách kiểm tra thủ công trên UI

**Trạng thái:** Đã tái hiện UI cho mọi giá trị bằng Android input injection; nhập/xóa bằng bàn phím thông thường đã khả thi với rỗng/`0`. Từ màn chi tiết ID 1, reset giỏ giữa mỗi giá trị, xóa `1`, nhập giá trị, chụp ô trước bấm, bấm thêm, chụp alert và màn Giỏ. Nếu bàn phím mềm chặn `abc`/`2abc`, thử dán thông thường; nếu vẫn chặn, ghi gate và dùng bốn giá trị còn lại để xác nhận bug.

## Bằng chứng

- [Evidence run và Actual](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/ncuong/homework/hw02/ncuong/features/FR06/evidence/FR06-evidence.md) — EV-FR06-013…017, 019.
- T11/BVA: [ô `0`](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T11-input-0.png), [alert thành công](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T11-success-0.png), [giỏ quantity `1`](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T11-cart-1.png).
- Các lớp khác: [rỗng](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T10-input-empty.png) · [giỏ](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T10-cart-1.png); [`-1`](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T12-input-minus1.png) · [giỏ](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T12-cart-1.png); [`1.5`](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T13-input-1point5.png) · [giỏ](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T13-cart-1.png); [`abc`](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T14-input-abc.png) · [giỏ](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T14-cart-1.png); [`2abc`](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T16-input-2abc.png) · [giỏ](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T16-cart-2.png).
- Lặp lại: T10 và T11 được chạy lại từ giỏ rỗng; 6 lớp input riêng, không coi ảnh trước/sau cùng lần là các lần tái hiện độc lập.

### Ảnh xác nhận UI

![T11-input-0](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T11-input-0.png)

![T11-success-0](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T11-success-0.png)

![T11-cart-1](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T11-cart-1.png)

![T13-input-1point5](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T13-input-1point5.png)

![T13-cart-1](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T13-cart-1.png)

![T16-input-2abc](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T16-input-2abc.png)

![T16-cart-2](https://raw.githubusercontent.com/SoftwareTesting-Group13/eshop-sut-homework/ncuong/homework/hw02/ncuong/features/FR06/screenshots/T16-cart-2.png)

## Điều tra nguyên nhân

**Vị trí:** [`frontend-mobile/App.js`](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/46a2d87e6e27b222dc857819be35a2268bf8bb45/frontend-mobile/App.js#L129-L135) dòng 129–135, cùng đường gọi ở [dòng 565–575](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/blob/46a2d87e6e27b222dc857819be35a2268bf8bb45/frontend-mobile/App.js#L565-L575).

```js
  const normalizeQuantity = (value) => {
    const parsed = parseInt(value, 10);
    return Number.isFinite(parsed) && parsed > 0 ? parsed : 1;
  };

  const addToCart = (selectedProduct, selectedQuantity = 1) => {
    const safeQuantity = normalizeQuantity(selectedQuantity);
```

**Cơ chế:** `parseInt` lấy tiền tố nguyên của `1.5` và `2abc`; với rỗng/`0`/âm/chữ, hàm trả mặc định `1`. `addToCart` dùng giá trị đã đổi và luôn báo thành công; TextInput không có bước từ chối trước khi gọi. Expected/Actual lấy từ rule và screenshot, mã chỉ giải thích kết quả.
