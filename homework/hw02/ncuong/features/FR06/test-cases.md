# FR-06 — Test case catalog (EP + BVA, Mobile)

Một T-ID là một ca, dù liên kết cả EP/BVA. **Fixture API run trước:** backend test cách ly cổng `3106`, seed 5 sản phẩm ID 1…5 và danh mục 1 “Điện thoại”, 2 “Laptop”, 3 “Phụ kiện”. **Fixture UI run mới:** cùng source/seed trong backend bản sao cổng `3000`, Expo Android emulator dùng `10.0.2.2:3000/api`; không dùng `backend/database.sqlite` làm việc để reset. Hướng dẫn dưới đây đã được chạy trên Android emulator trừ T04–T07 API-only; chi tiết cách nhập và giới hạn T14/T16 ở [test-results.md](test-results.md).

| T-ID | Obligation | Setup, stimulus | Expected / oracle |
| --- | --- | --- | --- |
| T01 | P01 | Chọn chi tiết ID 1 | Ảnh lớn, tên iPhone 15 Pro Max, 30.000.000 ₫, mô tả, danh mục Điện thoại |
| T02 | P02 | Chọn chi tiết ID 2 | Đủ 5 trường; giá 28.000.000 ₫ dù response API giá có dạng chuỗi số |
| T03 | P03 | Chọn chi tiết ID 5 | Đủ 5 trường; danh mục Phụ kiện |
| T04 | P04 | `GET /api/products/0` | UNRESOLVED: API spec không quy định status/body ID vắng |
| T05 | P05 | `GET /api/products/6` | UNRESOLVED như T04 |
| T06 | P06 | `GET /api/products/abc` | UNRESOLVED: API spec không quy định ID sai cú pháp |
| T07 | P07 | `GET /api/products/1.5` | UNRESOLVED như T06 |
| T08 | P08, B1-on, B2-int | ID 1, giỏ rỗng, nhập `1`, bấm Thêm vào giỏ hàng | Nhận 1, phản hồi trực quan, giỏ có quantity 1 |
| T09 | P09, B1-in, B2-int | ID 1, giỏ rỗng, nhập `2`, bấm thêm | Nhận 2, phản hồi, giỏ có quantity 2 |
| T10 | P10 | ID 1, giỏ rỗng, xóa hết ô quantity rồi bấm thêm | Không chấp nhận chuỗi rỗng làm số lượng; không thêm từ input invalid |
| T11 | P11, B1-out | ID 1, giỏ rỗng, nhập `0`, bấm thêm | Không chấp nhận 0; giỏ không tăng vì input invalid |
| T12 | P12 | ID 1, giỏ rỗng, nhập `-1`, bấm thêm | Không chấp nhận âm; giỏ không tăng |
| T13 | P13, B2-frac | ID 1, giỏ rỗng, nhập/dán `1.5`, bấm thêm | Không chấp nhận phân số; giỏ không tăng |
| T14 | P14 | ID 1, giỏ rỗng, nhập/dán `abc`, bấm thêm | Không chấp nhận chữ; giỏ không tăng |
| T15 | P15 | ID 1, giỏ rỗng: thêm `1`, ở lại chi tiết và thêm `1` lần nữa | Mỗi lần bấm có phản hồi; tổng quantity giỏ = 2 |
| T16 | P16 | ID 1, giỏ rỗng, nhập/dán `2abc`, bấm thêm | Không chấp nhận chuỗi hỗn hợp; giỏ không tăng |

## Đường API và thao tác mobile

**T01–T03:** API trực tiếp lần lượt `GET http://127.0.0.1:3106/api/products/1`, `/2`, `/5`; không token. Manual: (1) Mở Expo app EShop Mobile, ở “Danh sách sản phẩm”, không cần đăng nhập. (2) Tìm card đúng tên ở bảng dưới, bấm **Xem chi tiết**. (3) Đợi màn chi tiết tải; đọc ảnh, tên, giá, mô tả và tên danh mục. (4) Chụp toàn màn chi tiết từ ảnh đến nút thêm giỏ, cuộn hết card nếu cần. (5) Về Danh sách sản phẩm để chọn ca tiếp; trên Android emulator run này header đè status bar nên dùng keyboard focus đến “EShop Mobile” rồi Enter hoặc đóng/mở app. API trả `category_id`; verdict đủ trường lấy từ UI riêng.

**T04–T07:** API trực tiếp như bảng. Không có manual UI cùng input: card “Xem chi tiết” chỉ truyền `item.id` từ `GET /api/products`, không có ô nhập ID hoặc deep link công khai. Không chấm lỗi vì oracle response cho ID không tồn tại/sai cú pháp chưa được đặc tả. Nếu thử trực tiếp qua API, ghi request/response và hỏi chủ yêu cầu về status/message mong đợi.

**T08–T14, T16:** Không có API tương đương của màn chi tiết: số lượng và nút thêm giỏ do mobile xử lý cục bộ; `POST /api/cart` trong spec là giao diện khác, có token và body sản phẩm, không nhận chính chuỗi từ TextInput. Manual cho **từng T-ID riêng**: (1) Đóng/mở app để giỏ rỗng, kiểm tra navbar `Giỏ (0)`; không cần login. (2) Ở “Danh sách sản phẩm”, card **iPhone 15 Pro Max** → **Xem chi tiết**; đợi thông tin hiện. (3) Chạm ô **Số lượng**, select all rồi nhập chính giá trị ở bảng; T10 xóa trống, T13/T14/T16 dùng thao tác dán thông thường nếu bàn phím không có ký tự cần thiết. (4) Chụp ô ngay trước khi bấm; nếu bàn phím chặn giá trị, ghi gate và không coi như đã gửi input ấy. (5) Bấm **Thêm vào giỏ hàng**, ghi alert/nhãn/badge thực tế; vào **Giỏ**, ghi quantity của iPhone và chụp màn giỏ. Trên emulator run này, header bị status bar che nên sau khi đóng alert dùng keyboard focus Tab đến node “Giỏ” rồi Enter. (6) Reset bằng đóng app hoàn toàn/mở lại, xác nhận `Giỏ (0)` trước ca kế. Expected nhìn thấy là cột Expected của đúng T-ID; với invalid, không được có item mới do giá trị invalid. Không tự đặt wording thông báo lỗi.

**T15:** Không có API tương đương vì giỏ mobile cục bộ. Manual: reset app → Giỏ (0) → card iPhone ID 1 → Xem chi tiết → giữ quantity `1` → bấm **Thêm vào giỏ hàng**, ghi phản hồi → sau khi nhãn nút trở lại, bấm thêm lần hai → ghi phản hồi lần hai → Giỏ, kiểm tra iPhone có quantity `2`. Trên emulator bị status bar che, dùng Tab/Enter để vào Giỏ như trên. Chụp hai trạng thái phản hồi và màn giỏ. Nếu cần reset, đóng/mở app.

Các bước manual là cách chạy lại; Actual/verdict chỉ lấy từ [evidence](evidence/FR06-evidence.md). T14/T16 đã đưa chuỗi vào TextInput bằng `adb input text`, chưa xác nhận bàn phím mềm/dán thông thường. App đã được cấu hình endpoint Android emulator trong lượt sửa API được người dùng yêu cầu; logic FR-06 không sửa.
