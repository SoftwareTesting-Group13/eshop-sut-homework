# BUG-<FEATURE_CODE>-<NN> — <hành vi sai + hệ quả chính>

## Tóm tắt

<1–2 câu: thao tác nào làm lộ lỗi, hệ thống thực tế làm gì, đặc tả yêu cầu gì.>

| Mục | Giá trị |
| --- | --- |
| Feature / rule | `<FEATURE_CODE>` — `<tên>`; `<R-ID và link tới đúng đoạn yêu cầu>` |
| Test case | `<T-ID; nêu vai trò của từng case nếu nhiều case>` |
| Build / môi trường | `<commit>`; `<trình duyệt/thiết bị và URL trang nếu tái hiện qua UI; runtime, DB, endpoint nếu cần>` |
| Severity / Priority | `<mức>` / `<mức>` — `<lý do ngắn dựa trên ảnh hưởng>` |
| Trạng thái / lặp lại | `<đã xác nhận hay còn chờ>`; `<n/m lần thử độc lập>` |

## Chuẩn bị để tái hiện

- `<Tài khoản hoặc fixture cụ thể; dữ liệu đăng nhập cần dùng.>`
- `<Trạng thái ban đầu của những cột/giá trị ảnh hưởng tới lỗi.>`
- `<URL/trang cần mở và trạng thái đăng nhập nếu tái hiện qua UI; hoặc endpoint nếu chỉ tái hiện qua API.>`
- `<Cách tạo/reset fixture khi thật sự cần; nêu đúng DB server đang dùng nếu phải can thiệp DB test.>`

<Nếu cần lệnh setup: thêm một khối lệnh chạy được, đặt biến DB trong cùng khối. Nếu chuẩn bị hoàn toàn bằng UI thì ghi thao tác UI, bỏ khối lệnh.>

## Các bước tái hiện và kết quả

**Đường tái hiện đã kiểm chứng:** `<UI hoặc API; ghi rõ nếu bước UI mới là đề xuất, chưa chạy>`.

1. `<UI: Người dùng mở URL/trang cụ thể và đăng nhập bằng tài khoản cụ thể. API: Người kiểm thử gửi method/endpoint với body cụ thể. Chỉ giữ đường thực sự đã kiểm chứng.>`
2. `<UI: Người dùng nhập/bấm/chờ gì tiếp theo. API: Người kiểm thử gửi request tiếp theo hoặc đọc response/DB nào.>`
3. `<UI: Người dùng quan sát lỗi ở đâu và thấy gì. API: Người kiểm thử đọc status/body/trạng thái nào. Nếu có biên thời gian, ghi rõ t0 và thời điểm thử lại.>`

<Nếu đường chính là API, thêm khối request chạy được ngay dưới các bước. Với đường UI, chỉ thêm lệnh API/DB ở mục đối chiếu bên dưới khi giao diện không bộc lộ đủ trạng thái. Không viết bước UI như đã chạy khi evidence hiện có chỉ là API hoặc đọc source.>

| Mốc / bước | Expected theo rule | Actual quan sát được |
| --- | --- | --- |
| `<bước/mốc có ý nghĩa>` | `<giá trị, trạng thái hoặc HTTP response cụ thể>` | `<giá trị, trạng thái hoặc HTTP response thực tế>` |

**Kết luận:** `<Nêu chính xác điểm vi phạm rule; giải thích hệ quả đối với người dùng.>`

## Đối chiếu kỹ thuật (chỉ khi cần)

`<Lệnh đọc trạng thái API/DB, kết quả tương ứng và lý do cần đối chiếu. Bỏ hẳn mục này nếu Expected/Actual đã quan sát đủ trên UI.>`

## Bằng chứng

- Log/run: `<link tới evidence có output thô và Run ID nếu có>`.
- Screenshot: `<ảnh đã chụp và gắn vào Issue; ảnh phải thấy input/mốc thời gian và Actual đủ để hiểu lỗi, hoặc kết hợp với log được dẫn>`.
- Lặp lại: `<n/m; các lần thử/fixture độc lập và link nếu có. Không gọi hai phép quan sát trong cùng một run là 2 lần tái hiện.>`

## Điều tra nguyên nhân (chỉ khi đã kiểm chứng)

**Vị trí:** [`<đường/dẫn/file>`](<link tới đúng commit và dòng trên GitHub>) dòng `<số dòng>`.

```<ngôn ngữ>
<Trích nguyên văn vài dòng mã quanh lệnh/điều kiện gây lỗi, đủ ngữ cảnh để hiểu luồng xử lý.>
```

**Cơ chế:** `<Giải thích lệnh hoặc điều kiện trên dẫn tới Actual như thế nào; đối chiếu rõ với rule/Expected. Nếu đoạn trích chỉ là điểm nghi vấn, ghi là giả thuyết thay vì kết luận.>`

Đây là nhận định từ mã nguồn; Expected và Actual ở trên dựa trên đặc tả và lần chạy thực tế. Trích đúng phiên bản commit đã kiểm thử, giữ nguyên nội dung mã và không chép cả hàm nếu chỉ vài dòng liên quan.

<!-- Bỏ hẳn mục nguyên nhân nếu chưa đủ bằng chứng. Không để placeholder trong Issue đã đăng. -->
