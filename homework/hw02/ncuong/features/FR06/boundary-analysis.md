# FR-06 — Boundary Value Analysis (Mobile)

**Nguồn:** `README.md` FR-06, `api_specification.md` §3.2. Số lượng là số nguyên theo rule; bước nhỏ nhất giữa các giá trị hợp lệ là 1. Fixture ID 1…5 chỉ là dữ liệu chạy, không phải ngưỡng nghiệp vụ của ID.

## B1 — số lượng tối thiểu `q ≥ 1`

Setup: giỏ rỗng, mở chi tiết sản phẩm ID 1. Dấu bằng thuộc miền hợp lệ. Giá trị nhập là chuỗi mà UI đưa vào ô Số lượng.

| Điểm | Giá trị | Expected | Case | Khả thi |
| --- | --- | --- | --- | --- |
| Ngay dưới | `0` | Không nhận `0`, không thêm item với quantity từ input này | T11 | Đã chạy UI: FAIL, giỏ quantity 1 |
| Tại biên | `1` | Nhận 1; bấm thêm có phản hồi, giỏ tăng 1 | T08 | Đã chạy UI: PASS |
| Ngay trên | `2` | Nhận 2; bấm thêm có phản hồi, giỏ tăng 2 | T09 | Đã chạy UI: PASS |

## B2 — ranh giới số nguyên và số không nguyên

Với `1.5`, có thể biểu diễn bằng chuỗi trong ô nếu bàn phím/thiết bị cho phép nhập hoặc dán. Đây là một lớp invalid, không phải bước `+1` của miền số nguyên. Nếu mobile không cho tạo giá trị `1.5` bằng thao tác thường, ghi gate thực tế và đổi T13 thành không khả thi trên thiết bị đó; không dùng devtools.

| Điểm | Giá trị | Expected | Case | Khả thi |
| --- | --- | --- | --- | --- |
| Số nguyên hợp lệ | `1` | Chấp nhận | T08 | Đã chạy UI: PASS |
| Giữa hai số nguyên | `1.5` | Không chấp nhận phân số | T13 | Đã chạy UI bằng ADB input: FAIL, giỏ quantity 1 |
| Số nguyên tiếp theo | `2` | Chấp nhận | T09 | Đã chạy UI: PASS |

ID sản phẩm `0/1` và `5/6` được thử để khảo sát hai phía của fixture, **không** tính vào BVA vì đặc tả không đặt khoảng ID 1…5. Không có giới hạn số lượng trên được xác định; không tạo biên cực đại giả. Số âm `-1`, rỗng và chữ thuộc EP invalid, không cần nhân thêm các điểm BVA không có ngưỡng riêng.

**Coverage BVA:** B1 thiết kế/chạy 3/3 điểm UI (2 PASS, 1 FAIL); B2 thiết kế/chạy 3/3 điểm UI (2 PASS, 1 FAIL). Mẫu số 6 nghĩa vụ điểm theo hai quyết định kiểm thử; 4 T-ID duy nhất vì T08/T09 dùng lại. T13 được đưa vào TextInput bằng ADB và thấy nguyên chuỗi trước bấm; đường bàn phím mềm/dán thông thường vẫn cần đối chiếu. [Evidence](evidence/FR06-evidence.md).
