# FR-06 — Product detail view (Mobile): Domain/EP

**Nguồn oracle:** `README.md` §3 FR-06; `api_specification.md` §3.2 và §4.2; `README.md` §7 FR-20 xác nhận phạm vi mobile. **Build:** `46a2d87e6e27b222dc857819be35a2268bf8bb45`. FR-07 chỉ dùng để nhìn số lượng đã thêm, không mở rộng kiểm thử giỏ hàng.

## Rule và miền

| Rule | Trạng thái | Điều kiện / Expected | Nguồn |
| --- | --- | --- | --- |
| R1 | CONFIRMED | Chi tiết sản phẩm hiển thị ảnh lớn, tên, giá, mô tả, danh mục. | README FR-06 |
| R2 | CONFIRMED | Ô số lượng chỉ nhận số nguyên dương, nhỏ nhất 1. | README FR-06 |
| R3 | CONFIRMED | Bấm Thêm vào giỏ có phản hồi trực quan (toast hoặc badge). | README FR-06 |
| R4 | CONFIRMED | API có `GET /api/products/:id`; không quy định schema response, status cho ID không tồn tại/sai kiểu. | api_specification §3.2 |
| R5 | CONFIRMED | API `POST /api/cart` cần token và có `quantity`; mobile dùng giỏ cục bộ theo source. Không dùng response API cart làm oracle cho thao tác mobile. | api_specification §4.2; source chỉ để xác định đường chạy |

**D1 — sản phẩm được chọn:** ID từ danh sách hiện có; fixture test có 1…5. ID ngoài danh sách hoặc sai cú pháp chỉ gửi được trực tiếp qua API, vì app chỉ truyền `item.id` từ danh sách. Không có rule quy định lỗi/HTTP status cho trường hợp đó: oracle `UNRESOLVED`, không tự chấm FAIL chỉ vì HTTP 200. **D2 — dữ liệu trả về:** ảnh/tên/giá/mô tả/danh mục của sản phẩm hiện có. Giá API có thể là number hoặc chuỗi số; đặc tả không quy định kiểu JSON nên chỉ đánh giá giá trị hiển thị sau khi chạy UI. **D3 — số lượng:** chuỗi nhập ở TextInput; miền hợp lệ là số nguyên dương `1, 2, …`; rỗng, 0, âm, phân số và chữ là miền không hợp lệ. Không có giới hạn trên hoặc quy tắc overflow trong đặc tả. **D4 — trạng thái giỏ:** chưa có sản phẩm / đã có sản phẩm; dùng trạng thái giỏ sau thao tác làm quan sát phụ cho số lượng, không xét các rule CRUD FR-07.

## Lớp tương đương

Baseline: app mở ở màn hình Danh sách sản phẩm, fixture sản phẩm ID 1 “iPhone 15 Pro Max” có ảnh URL, giá 30.000.000 ₫, mô tả và `category_id=1` (danh mục “Điện thoại”); giỏ rỗng; không cần đăng nhập cho luồng mobile cục bộ. Mỗi ca quantity mở lại chi tiết để reset ô về `1`, giỏ được reset bằng khởi động lại app.

| Lớp | Điều kiện và giá trị đem test | Expected theo rule | Case | Rule |
| --- | --- | --- | --- | --- |
| P01 | Sản phẩm đầu fixture, ID `1` | Màn chi tiết hiển thị đủ 5 thành phần, đúng dữ liệu fixture | T01 | R1 |
| P02 | Sản phẩm giữa fixture, ID `2`; API có thể trả giá chuỗi số | Giá mobile vẫn hiển thị giá trị đúng, đủ 5 thành phần | T02 | R1 |
| P03 | Sản phẩm cuối fixture, ID `5`, danh mục khác ID 1 | Hiển thị danh mục “Phụ kiện” cùng dữ liệu sản phẩm | T03 | R1 |
| P04 | ID không tồn tại `0` | API outcome chưa được quy định; quan sát, UI không chọn được | T04 | R4 |
| P05 | ID không tồn tại `6` | Như P04 | T05 | R4 |
| P06 | ID sai cú pháp `abc` | API outcome chưa được quy định; quan sát, UI không chọn được | T06 | R4 |
| P07 | ID phân số `1.5` | API outcome chưa được quy định; quan sát, UI không chọn được | T07 | R4 |
| P08 | Số lượng `1`, giỏ rỗng | Nhận 1; bấm thêm có phản hồi trực quan; giỏ có 1 | T08 | R2,R3 |
| P09 | Số lượng `2`, giỏ rỗng | Nhận 2; phản hồi; giỏ có 2 | T09 | R2,R3 |
| P10 | Ô quantity bị xóa thành rỗng | Không được nhận giá trị rỗng làm số lượng hợp lệ hoặc âm thầm thêm hàng | T10 | R2 |
| P11 | Số lượng `0` | Từ chối/không chấp nhận `0`; không thêm hàng từ input không hợp lệ | T11 | R2 |
| P12 | Số lượng `-1` | Từ chối/không chấp nhận số âm | T12 | R2 |
| P13 | Số lượng `1.5` | Từ chối/không chấp nhận phân số | T13 | R2 |
| P14 | Số lượng chữ `abc` | Từ chối/không chấp nhận chuỗi không phải số | T14 | R2 |
| P15 | Cùng sản phẩm, giỏ đã có 1, thêm tiếp quantity `1` | Có phản hồi sau lần bấm; số lượng giỏ tăng thành 2 (kiểm tra phụ theo FR-07) | T15 | R3 |
| P16 | Chuỗi có tiền tố số nhưng chứa chữ `2abc` | Không chấp nhận chuỗi hỗn hợp không phải số nguyên | T16 | R2 |

Với P10–P14, đặc tả không ấn định thông báo lỗi, thời điểm validate hay tự sửa input; oracle là **không chấp nhận chính giá trị không hợp lệ** và không tạo thêm item do input ấy. Nếu app biến đổi input trước khi người dùng bấm, ghi rõ hành vi UI rồi đối chiếu rule, không coi input đã biến đổi là ca hợp lệ ban đầu.

**Coverage EP sau run mobile:** 16/16 lớp có case và đã chạy; P01–P03 cùng P08–P16 có 12 Actual UI, P04–P07 chỉ có API vì không thể chọn những ID ấy trên màn hình. Verdict duy nhất: 3 PASS (P08/P09/P15), 9 FAIL (P01–P03, P10–P14, P16), 4 INCONCLUSIVE do API spec thiếu oracle (P04–P07). Với P14/P16, Android ADB đưa chuỗi vào TextInput rồi app nhận khi bấm; khả năng gõ/dán bằng bàn phím mềm cần kiểm chứng thêm. Xem [kết quả](test-results.md) và [ảnh UI](screenshots/). API một mình không chứng minh R1 trên màn hình.
