# BUG-<FEATURE_CODE>-<NN> — <hành vi sai + hệ quả chính>

## Tóm tắt

<1–2 câu: thao tác nào làm lộ lỗi, hệ thống thực tế làm gì, đặc tả yêu cầu gì.>

| Mục | Giá trị |
| --- | --- |
| Feature / rule | `<FEATURE_CODE>` — `<tên>`; `<R-ID và link tới đúng đoạn yêu cầu>` |
| Test case | `<T-ID; nêu vai trò của từng case nếu nhiều case>` |
| Build / môi trường | `<commit>`; `<runtime, DB, base URL, endpoint>` |
| Severity / Priority | `<mức>` / `<mức>` — `<lý do ngắn dựa trên ảnh hưởng>` |
| Trạng thái / lặp lại | `<đã xác nhận hay còn chờ>`; `<n/m lần thử độc lập>` |

## Chuẩn bị để tái hiện

- `<Tài khoản hoặc fixture cụ thể; dữ liệu đăng nhập cần dùng.>`
- `<Trạng thái ban đầu của những cột/giá trị ảnh hưởng tới lỗi.>`
- `<Cách khởi động SUT và đường dẫn DB đang được server sử dụng, hoặc link tới hướng dẫn setup chính xác. Nếu dùng DB tạm, nói rõ đây là lần tái hiện thủ công.>`
- `<Lệnh tạo/reset dữ liệu, nếu cần. Nêu tác động của việc reset; chỉ dùng DB test được phép sửa.>`

```bash
# <Các lệnh setup thực sự cần cho lần tái hiện này, theo đúng thứ tự.>
# <Nếu dùng biến đường dẫn DB, gán biến ở đây; không giả định người đọc đã export từ trước.>
```

## Các bước tái hiện và kết quả

1. `<Thao tác/input cụ thể để kích hoạt lỗi; ghi đầy đủ request hoặc hành động UI.>`
2. `<Lệnh hoặc thao tác đọc trạng thái ngay sau đó.>`
3. `<Nếu kiểm tra biên thời gian: mốc bắt đầu t0, thời gian chờ thực tế, thao tác retry và cách đọc thời điểm retry.>`

```bash
# <Chuỗi lệnh chạy được từ trạng thái đã chuẩn bị; gồm cả trigger, phép đo, retry nếu có.>
```

| Mốc / bước | Expected theo rule | Actual quan sát được |
| --- | --- | --- |
| `<bước/mốc có ý nghĩa>` | `<giá trị, trạng thái hoặc HTTP response cụ thể>` | `<giá trị, trạng thái hoặc HTTP response thực tế>` |

**Kết luận:** `<Nêu chính xác điểm vi phạm rule; giải thích hệ quả đối với người dùng.>`

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
