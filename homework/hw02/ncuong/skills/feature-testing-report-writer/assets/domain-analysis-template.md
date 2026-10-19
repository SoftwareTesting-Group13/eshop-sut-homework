# <FEATURE_CODE> — Domain analysis (EP)

**Feature / interface:** `<tên feature; API hoặc UI thực sự được kiểm thử>`  
**Phạm vi:** `<hành vi được kiểm thử; phần loại trừ nếu cần>`  
**Nguồn yêu cầu:** `<file §mục>`

## Quy tắc dùng để chia miền

| Rule | Hệ thống phải làm gì? | Điều kiện ảnh hưởng | Nguồn |
| --- | --- | --- | --- |
| R1 | `<hành vi kiểm thử được, ghi trực tiếp>` | `<input/trạng thái>` | `<file §mục>` |

`<Chỉ nêu giả định hoặc điểm chưa rõ nếu nó ảnh hưởng đến việc chia lớp hoặc Expected. Không chép lại luồng nghiệp vụ khi bảng rule đã đủ.>`

## Các lớp tương đương và ca đại diện

`<Nhóm hàng theo email, password, trạng thái... khi cần. P-ID là lớp tương đương; T-ID là ca trong test-cases.md. Ghi một baseline chung ở đầu nhóm nếu nhiều hàng dùng lại.>`

**<Đầu vào hoặc trạng thái>:** `<baseline chung nếu có>`

| Lớp | Điều kiện của nhóm | Giá trị/trạng thái đem test | Expected theo đặc tả | Test case | Rule |
| --- | --- | --- | --- | --- | --- |
| P1 | `<điều kiện cụ thể; hợp lệ/không hợp lệ/chưa rõ>` | `<giá trị + trạng thái cần tạo>` | `<kết quả quan sát được hoặc Chưa xác định>` | `<T-ID hoặc Chưa có>` | `<R-ID>` |

**Tương tác cần kiểm tra:** `<chỉ những cặp input/trạng thái làm đổi hành vi; nêu case kiểm tra. Nếu cần mô hình trạng thái/bảng quyết định, đặt cạnh quyết định kiểm thử mà nó làm rõ.>`

**Lớp gộp, không khả thi hoặc chưa rõ:** `<chỉ nêu ngoại lệ thực tế; không cần mục này nếu không có>`

## Coverage EP

| Nghĩa vụ | Khả thi | Có case | Đã chạy có evidence | Đạt oracle | Còn thiếu / chưa rõ |
| --- | ---: | ---: | ---: | ---: | --- |
| Lớp `P-ID` | `<n>` | `<n>` | `<n hoặc Chưa chạy>` | `<n hoặc Chưa chạy>` | `<P-ID + lý do>` |

`<Ghi rõ lớp nào ở mẫu số và lý do loại trừ; FAIL vẫn tính đã chạy. Kết quả chi tiết, Actual và bug nằm ở test-results.md, không chép lại ở đây.>`
