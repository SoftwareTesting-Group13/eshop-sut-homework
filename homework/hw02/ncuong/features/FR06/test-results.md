# FR-06 — Kết quả Domain/EP + BVA (Mobile)

**Build:** commit `46a2d87e6e27b222dc857819be35a2268bf8bb45` cộng thay đổi local chỉ ở cấu hình `API_URL` của `frontend-mobile/App.js`; logic chi tiết sản phẩm/giỏ giữ nguyên. **Run được chọn:** `run-20261021-fr06-mobile`, Android emulator `Pixel_10_Pro`, Expo Go SDK 54, Metro `localhost:8081`, backend/SQLite bản sao cách ly cổng `3000`; app gọi `10.0.2.2:3000/api`. Giỏ reset bằng force-stop/mở lại app, xác nhận `Giỏ (0)` ở mỗi ca số lượng. Ảnh chụp từ emulator là Actual UI, lưu tại [screenshots/](screenshots/); thao tác và kết quả trong [evidence/FR06-evidence.md](evidence/FR06-evidence.md). API-only T04–T07 lấy từ run trước `run-20261021-fr06-api`, cùng source/fixture; không suy ra verdict UI từ API.

| T-ID | EV-ID / interface | Actual quan sát | Verdict toàn ca |
| --- | --- | --- | --- |
| T01 | EV-FR06-001 API; EV-FR06-008 UI | ID 1: ảnh lớn, tên, `30,000,000 đ`, mô tả; không có “Điện thoại” | **FAIL** — BUG-FR06-01 |
| T02 | EV-FR06-002 API; EV-FR06-009 UI | ID 2: giá API chuỗi số render thành `28,000,000 đ`; ảnh/tên/mô tả có, thiếu danh mục | **FAIL** — BUG-FR06-01 |
| T03 | EV-FR06-003 API; EV-FR06-010 UI | ID 5: ảnh/tên/`4,000,000 đ`/mô tả có, thiếu “Phụ kiện” | **FAIL** — BUG-FR06-01 |
| T04 | EV-FR06-004 API only | `GET /api/products/0` → HTTP 200 `{}`; UI không chọn được ID này | **INCONCLUSIVE** — spec không quy định status/body |
| T05 | EV-FR06-005 API only | `GET /api/products/6` → HTTP 200 `{}`; không có card ID 6 | **INCONCLUSIVE** — như T04 |
| T06 | EV-FR06-006 API only | `GET /api/products/abc` → HTTP 200 `{}`; UI không có ô nhập ID | **INCONCLUSIVE** — thiếu oracle ID sai cú pháp |
| T07 | EV-FR06-007 API only | `GET /api/products/1.5` → HTTP 200 `{}`; UI không có ô nhập ID | **INCONCLUSIVE** — như T06 |
| T08 | EV-FR06-011 UI | Ô `1`, alert “Thành công”, Giỏ quantity `1`, thành tiền `30,000,000 đ` | **PASS** |
| T09 | EV-FR06-012 UI | Ô `2`, alert “Thành công”, Giỏ quantity `2`, thành tiền `60,000,000 đ` | **PASS** |
| T10 | EV-FR06-013 UI | Ô rỗng vẫn alert “Thành công”, Giỏ quantity `1` | **FAIL** — BUG-FR06-02 |
| T11 | EV-FR06-014 UI | Ô `0` vẫn alert “Thành công”, Giỏ quantity `1`; lặp lại từ giỏ rỗng | **FAIL** — BUG-FR06-02 |
| T12 | EV-FR06-015 UI | Ô `-1` vẫn thành công, Giỏ quantity `1` | **FAIL** — BUG-FR06-02 |
| T13 | EV-FR06-016 UI | Ô `1.5` vẫn thành công, Giỏ quantity `1` (lấy phần nguyên) | **FAIL** — BUG-FR06-02 |
| T14 | EV-FR06-017 UI | Ô `abc` qua Android `adb input text` vẫn thành công, Giỏ quantity `1` | **FAIL** — BUG-FR06-02; đường gõ/dán thường chưa đối chiếu |
| T15 | EV-FR06-018 UI | Bấm hai lần quantity `1`: mỗi lần có alert; Giỏ quantity `2` | **PASS** |
| T16 | EV-FR06-019 UI | Ô `2abc` qua Android `adb input text` vẫn thành công, Giỏ quantity `2` (lấy tiền tố) | **FAIL** — BUG-FR06-02; đường gõ/dán thường chưa đối chiếu |

**Thao tác UI:** chọn card ID tương ứng ở Danh sách sản phẩm; mỗi ca số lượng thay ô quantity trên màn chi tiết, bấm **Thêm vào giỏ hàng**, đóng alert, vào **Giỏ** bằng focus keyboard `Tab` rồi `Enter` vì navbar nằm dưới status bar trên emulator. ADB `input text` nhập trực tiếp vào control React Native, không sửa source/state. Với T14/T16, cách này bỏ qua giới hạn bàn phím mềm; screenshot xác nhận TextInput giữ nguyên chuỗi trước khi bấm, nhưng chưa chứng minh người dùng gõ/dán thông thường tạo được chuỗi ấy. T10/T11 có rerun từ giỏ rỗng; bảng dùng rerun. Một lần rerun T16 không mở được Expo Go và bị bỏ; EV-FR06-019 là lần chạy lại hợp lệ, có ảnh input/giỏ.

## Tổng hợp và coverage

| Thiết kế | Đã chạy T-ID | PASS | FAIL | INCONCLUSIVE | BLOCKED | Chưa chạy |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 16 | 3 | 9 | 4 | 0 | 0 |

| Nghĩa vụ | Thiết kế | Đã chạy | PASS | FAIL | INCONCLUSIVE |
| --- | ---: | ---: | ---: | ---: | ---: |
| EP P01–P16 | 16/16 | 16/16 (12 UI, 4 API-only) | 3 | 9 | 4 |
| BVA B1: `0,1,2` | 3/3 | 3/3 UI | 2 | 1 | 0 |
| BVA B2: `1,1.5,2` | 3/3 | 3/3 UI | 2 | 1 | 0 |

T08/T09 dùng lại ở hai nhóm BVA; tổng BVA là 6 nghĩa vụ điểm nhưng chỉ 4 T-ID duy nhất. 4 API-only có Actual nhưng thiếu oracle; không chấm bug HTTP 200. Không suy ra code coverage.

## Bug và giới hạn

- **BUG-FR06-01 (Medium):** Thiếu tên danh mục ở ID 1, 2 và 5; [Issue #55](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/55) (3 ảnh UI), [bản lưu](issues/BUG-FR06-01.md), [ảnh ID 1](screenshots/T01-detail-ID1.png), [ID 2](screenshots/T02-detail-ID2.png), [ID 5](screenshots/T03-detail-ID5.png).
- **BUG-FR06-02 (Medium):** Chấp nhận quantity không hợp lệ, đổi thành `1` hoặc lấy tiền tố số; [Issue #56](https://github.com/SoftwareTesting-Group13/eshop-sut-homework/issues/56) (7 ảnh UI nhúng), [bản lưu](issues/BUG-FR06-02.md), [ảnh `0` trước bấm](screenshots/T11-input-0.png), [alert](screenshots/T11-success-0.png), [giỏ](screenshots/T11-cart-1.png), các lớp còn lại trong evidence. Người dùng đã chốt hai bug; cả hai Issue đã publish.
- **Ngoài phạm vi FR-06:** Navbar đè lên status bar Android nên không tap được mục Giỏ tại vị trí hiển thị; [ghi chú](../../supporting-materials/fr06-observations.md). Không cộng thành T-ID/bug FR-06.
- **UNRESOLVED:** API spec không quy định status/body cho ID vắng/sai cú pháp; không có upper bound quantity. Đường dán chữ bằng UI thường và iOS/thiết bị vật lý chưa chạy; kết luận chính BUG-FR06-02 đã được xác nhận độc lập bởi rỗng/`0`/`-1`/`1.5` trên TextInput.

AI Gap Analysis và AI Critique là phần sinh viên tự viết. Cleanup và hash DB làm việc được ghi ở evidence.
