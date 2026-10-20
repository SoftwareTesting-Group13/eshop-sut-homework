# <FEATURE_CODE> — Test cases (EP + BVA)

Thiết kế ca từ lớp tương đương trong `domain-analysis.md` và điểm biên trong `boundary-analysis.md`. Mỗi `T-ID` chỉ có một dòng; một ca có thể phủ cả hai phương pháp.

| T-ID | Phương pháp & obligation IDs | Setup + input + thao tác | Expected / oracle |
| --- | --- | --- | --- |
| `<DT/BVA-ID>` | `<EP/BVA; P-ID/B-ID>` | `<giá trị và bước cụ thể>` | `<theo rule>` |

Ghi rõ ca gộp và các lớp/điểm biên mà nó phủ. Kết quả quan sát và `EV-ID` nằm trong `test-results.md`.

## Đường chạy API và thao tác UI thủ công

Với mỗi T-ID có cả API và UI, giữ **cùng ID** và ghi hai đường dưới đây. Gộp các bước mở app/đăng nhập chung nếu nhiều ca dùng cùng fixture, nhưng từng ca vẫn phải đủ giá trị và nút thao tác để tester chạy riêng.

### `<T-ID>`

- **API:** `<method, endpoint, body/header chính xác; hoặc Không có API>`.
- **UI thông thường:** `<Khả thi / Không cùng input-state vì control/gate cụ thể>`.
- **Các bước manual UI:** `<URL/trang → tài khoản/role + fixture → điền các giá trị → bấm/chọn theo thứ tự → quan sát vị trí kết quả; không cần browser automation>`.
- **Expected nhìn thấy:** `<theo rule; nếu kết quả chỉ ẩn ở server, nêu đối chiếu API/DB riêng>`.
- **Screenshot nên chụp:** `<trạng thái trước/sau và vùng kết quả/alert cần thấy>`.
- **Trạng thái kiểm chứng UI:** `Dự kiến từ luồng/source; chưa chạy` / `<EV-ID của lần UI đã chạy>`.

Nếu UI không thể gửi đúng input API, nêu lý do cụ thể và không viết bước UI giả tương đương. Có thể thiết kế một ca UI khác khi stimulus/oracle thật sự khác; không cộng thêm case chỉ vì đổi interface.
