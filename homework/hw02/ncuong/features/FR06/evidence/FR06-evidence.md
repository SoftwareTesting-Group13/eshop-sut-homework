# FR-06 — Evidence log

**Run API trước:** `run-20261021-fr06-api`; build `46a2d87e6e27b222dc857819be35a2268bf8bb45`; 2026-10-21 03:01:18–03:01:19 +0700 (theo HTTP Date). Backend test là bản sao source ở `/private/tmp/fr06-run.ozqOVe`, chỉ bản sao đổi cổng 3106. DB test seed 5 sản phẩm ID 1–5 và ba danh mục. DB làm việc trước run có SHA-256 `c63f00544180ba1fbb1427a9b9dd3f1784842698809972f33ce90482e7420ba6`. API GET không có side effect. Lệnh thật là `curl -sS -i` tương ứng dưới đây; response bỏ header không liên quan nhưng giữ HTTP status, Date và body. Các verdict API ở EV-001…007 là verdict tại thời điểm run API; verdict toàn ca mới nhất ở [test-results](../test-results.md).

### EV-FR06-001 — T01

```zsh
curl -sS -i http://127.0.0.1:3106/api/products/1
```
```text
HTTP/1.1 200 OK
Date: Tue, 20 Oct 2026 20:01:18 GMT
```
```json
{
  "id": 1,
  "name": "iPhone 15 Pro Max",
  "price": 30000000,
  "description": "Điện thoại cao cấp của Apple",
  "imageUrl": "https://placehold.co/300x300/png?text=iPhone+15",
  "category_id": 1
}
```
Actual: API có dữ liệu fixture; chưa thấy render mobile. Verdict toàn T01: **INCONCLUSIVE**.

---

### EV-FR06-002 — T02

```zsh
curl -sS -i http://127.0.0.1:3106/api/products/2
```
```text
HTTP/1.1 200 OK
Date: Tue, 20 Oct 2026 20:01:19 GMT
```
```json
{
  "id": 2,
  "name": "Samsung Galaxy S24 Ultra",
  "price": "28000000",
  "description": "Màn hình hiển thị xuất sắc, camera siêu zoom",
  "imageUrl": "https://placehold.co/300x300/png?text=Samsung+S24",
  "category_id": 1
}
```
Actual: API trả giá dạng chuỗi số; chưa thấy giá render mobile. Verdict: **INCONCLUSIVE**.

---

### EV-FR06-003 — T03

```zsh
curl -sS -i http://127.0.0.1:3106/api/products/5
```
```text
HTTP/1.1 200 OK
Date: Tue, 20 Oct 2026 20:01:19 GMT
```
```json
{
  "id": 5,
  "name": "Bàn phím cơ Keychron Q1",
  "price": 4000000,
  "description": "Gõ cực sướng, thiết kế kim loại",
  "imageUrl": "https://placehold.co/300x300/png?text=Keychron+Q1",
  "category_id": 3
}
```
Actual: API trả `category_id=3`; chưa thấy tên danh mục mobile. Verdict: **INCONCLUSIVE**.

---

### EV-FR06-004 — T04

```zsh
curl -sS -i http://127.0.0.1:3106/api/products/0
```
```text
HTTP/1.1 200 OK
Date: Tue, 20 Oct 2026 20:01:19 GMT
```
```json
{}
```
Actual: HTTP 200, object rỗng. Verdict: **INCONCLUSIVE** vì spec không quy định status/body của ID vắng.

---

### EV-FR06-005 — T05

```zsh
curl -sS -i http://127.0.0.1:3106/api/products/6
```
```text
HTTP/1.1 200 OK
Date: Tue, 20 Oct 2026 20:01:19 GMT
```
```json
{}
```
Actual: HTTP 200, object rỗng. Verdict: **INCONCLUSIVE** vì oracle unresolved.

---

### EV-FR06-006 — T06

```zsh
curl -sS -i http://127.0.0.1:3106/api/products/abc
```
```text
HTTP/1.1 200 OK
Date: Tue, 20 Oct 2026 20:01:19 GMT
```
```json
{}
```
Actual: HTTP 200, object rỗng. Verdict: **INCONCLUSIVE** vì oracle unresolved.

---

### EV-FR06-007 — T07

```zsh
curl -sS -i http://127.0.0.1:3106/api/products/1.5
```
```text
HTTP/1.1 200 OK
Date: Tue, 20 Oct 2026 20:01:19 GMT
```
```json
{}
```
Actual: HTTP 200, object rỗng. Verdict: **INCONCLUSIVE** vì oracle unresolved.

---

**Kết thúc run API:** 7 EV-ID/7 T-ID API, 7 INCONCLUSIVE khi chưa có UI. Backend test cổng 3106 đã dừng bằng Ctrl-C (exit 130). DB làm việc sau run có cùng SHA-256 `c63f00544180ba1fbb1427a9b9dd3f1784842698809972f33ce90482e7420ba6`. Thư mục `/private/tmp/fr06-run.ozqOVe` đã xóa, cổng 3106 không còn listener.

## Run mobile — `run-20261021-fr06-mobile`

**Môi trường:** Android emulator preexisting `Pixel_10_Pro`, Expo Go SDK 54 cài tạm; Metro phục vụ app React Native ở `localhost:8081`; app dùng endpoint Android mặc định `http://10.0.2.2:3000/api`. Backend test chạy từ bản sao `server.js`/`database.js` trong `/private/tmp/fr06-mobile.ErhauX`, DB SQLite riêng seed 5 sản phẩm; không động đến `backend/database.sqlite` làm việc. Android Chrome trên emulator nhận JSON từ `http://10.0.2.2:3000/api/products/1`; Expo app tải danh sách và chi tiết. Bản test có thay đổi local ở cấu hình API_URL, còn renderer/logic quantity giống commit gốc. Screenshot chụp bằng `adb exec-out screencap -p`, không chỉnh sửa ảnh. Các `adb input` tương tác với UI thật; `adb input text` có thể vượt giới hạn bàn phím mềm nên riêng T14/T16 chưa có bằng chứng gõ/dán thường.

**Reset và thao tác chung:** `adb shell am force-stop host.exp.exponent` → mở `exp://127.0.0.1:8081` → đợi Danh sách sản phẩm, `Giỏ (0)` → tap card ID 1/2/5 → chờ chi tiết. Với ca quantity, tap ô số lượng, xóa mặc định `1` bằng `keyevent 123` rồi `67`, nhập giá trị với `adb shell input text` (T10 để rỗng), đóng keyboard `keyevent 4`, chụp input, tap nút Thêm, chụp alert. Đóng alert, dùng `Tab` đến accessibility node “Giỏ (1)” rồi `Enter` để mở màn Giỏ và chụp quantity. Navbar nằm dưới Android status bar nên tap trực tiếp bị hệ thống chặn; keyboard focus chỉ là cách tiếp cận màn Giỏ, không thay đổi state app. Reset app/giỏ giữa các T-ID. T15 bấm hai lần từ giỏ rỗng.

| EV-ID | T-ID | Input / Actual UI | Ảnh gốc từ emulator trong repo | Verdict |
| --- | --- | --- | --- | --- |
| EV-FR06-008 | T01 | ID 1 có ảnh/tên/giá/mô tả; không có “Điện thoại” đến cuối card | [chi tiết ID 1](../screenshots/T01-detail-ID1.png) | FAIL |
| EV-FR06-009 | T02 | ID 2 render giá `28,000,000 đ`, không có “Điện thoại” | [chi tiết ID 2](../screenshots/T02-detail-ID2.png) | FAIL |
| EV-FR06-010 | T03 | ID 5 render giá `4,000,000 đ`, không có “Phụ kiện” | [chi tiết ID 5](../screenshots/T03-detail-ID5.png) | FAIL |
| EV-FR06-011 | T08 | Input `1`, alert thành công; giỏ `1`, tổng `30,000,000 đ` | [input](../screenshots/T08-input-1.png), [giỏ](../screenshots/T08-cart-1.png) | PASS |
| EV-FR06-012 | T09 | Input `2`, alert thành công; giỏ `2`, tổng `60,000,000 đ` | [input](../screenshots/T09-input-2.png), [giỏ](../screenshots/T09-cart-2.png) | PASS |
| EV-FR06-013 | T10 | Input rỗng, alert thành công; giỏ `1`, tổng `30,000,000 đ`; rerun từ Giỏ (0) | [input](../screenshots/T10-input-empty.png), [alert](../screenshots/T10-success-empty.png), [giỏ](../screenshots/T10-cart-1.png) | FAIL |
| EV-FR06-014 | T11 | Input `0`, alert thành công; giỏ `1`, tổng `30,000,000 đ`; rerun từ Giỏ (0) | [input](../screenshots/T11-input-0.png), [alert](../screenshots/T11-success-0.png), [giỏ](../screenshots/T11-cart-1.png) | FAIL |
| EV-FR06-015 | T12 | Input `-1`, alert thành công; giỏ `1`, tổng `30,000,000 đ` | [input](../screenshots/T12-input-minus1.png), [giỏ](../screenshots/T12-cart-1.png) | FAIL |
| EV-FR06-016 | T13 | Input `1.5`, alert thành công; giỏ `1`, tổng `30,000,000 đ` | [input](../screenshots/T13-input-1point5.png), [giỏ](../screenshots/T13-cart-1.png) | FAIL |
| EV-FR06-017 | T14 | Input `abc` giữ nguyên trên TextInput qua ADB, alert thành công; giỏ `1` | [input](../screenshots/T14-input-abc.png), [giỏ](../screenshots/T14-cart-1.png) | FAIL; manual reachability mở |
| EV-FR06-018 | T15 | Hai lần thêm input `1`, cả hai lần alert thành công; giỏ `2`, tổng `60,000,000 đ` | [alert 1](../screenshots/T15-success-first.png), [alert 2](../screenshots/T15-success-second.png), [giỏ](../screenshots/T15-cart-2.png) | PASS |
| EV-FR06-019 | T16 | Input `2abc` giữ nguyên trên TextInput qua ADB, alert thành công; giỏ `2`, tổng `60,000,000 đ` | [input](../screenshots/T16-input-2abc.png), [giỏ](../screenshots/T16-cart-2.png) | FAIL; manual reachability mở |

T10/T11 ban đầu cũng có alert thành công; rerun sạch được dùng làm EV-013/014. Một lần chạy T16 sau nhiều lần force-stop bị Expo Go bật về Android home trước khi nhập, không có Actual của ca nên bỏ khỏi coverage; EV-019 là lần chạy lại thành công. Mỗi ca có ảnh input/giỏ cùng một lần chạy, trừ T01–03 chỉ cần một ảnh card. Status bar che navbar là [quan sát ngoài phạm vi](../../../supporting-materials/fr06-observations.md).

**Cleanup sau run mobile:** Đã dừng Metro cổng 8081, backend bản sao cổng 3000 và emulator do run này mở; kiểm tra `lsof` không còn listener ở 3000/8081. Đã `adb uninstall host.exp.exponent` với kết quả `Success` cho Expo Go APK cài tạm. Đã xóa chính xác `frontend-mobile/node_modules`, `.expo`, `dist` (đều tạo trong lượt này), hai APK tải tạm, `/private/tmp/fr06-mobile.ErhauX`, driver `/private/tmp/fr06-ui-run.zsh` và các ảnh `fr06-*.png` trong `/private/tmp` sau khi sao 24 ảnh cần nộp vào `screenshots/`. Android SDK/AVD/Android Studio có sẵn được giữ nguyên. Hash `backend/database.sqlite` sau cleanup vẫn `c63f00544180ba1fbb1427a9b9dd3f1784842698809972f33ce90482e7420ba6`, trùng trước run. File `homework/hw02/ncuong/prompt.txt` là thay đổi có sẵn của người dùng, không đụng tới.
