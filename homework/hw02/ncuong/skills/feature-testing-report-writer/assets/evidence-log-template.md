# `<FEATURE_CODE>` — Evidence log (nhật ký bằng chứng thực thi)

> File mẫu trống cho **evidence log**. Mỗi lần thử thực thi một test case có một mục `EV-ID`; cùng `T-ID` có thể xuất hiện nhiều lần khi rerun.
> Ghi kết quả **thô** quan sát được, không chép Expected vào Actual. Lưu file thô (`*.log`,
> `*.json`, `*.png`) trong thư mục `evidence/` và link ở đây. Với ca phát hiện bug,
> **người kiểm thử review rồi mới chụp screenshot và mở GitHub Issue kèm ảnh** theo yêu cầu HW02.
> Trước bước review, ghi `Chờ người kiểm thử xác nhận`.

## Thông tin phiên chạy

| Mục | Giá trị |
| --- | --- |
| Feature | `<FEATURE_CODE> — <tên feature>` |
| Interface | `<interface dùng để chạy EP/BVA>` |
| SUT / build | `<repo><commit> / phiên bản>` |
| Môi trường | `<OS, runtime, DB; browser nếu đã dùng>` |
| Thời điểm chạy | `<YYYY-MM-DD HH:MM:SS ±hhmm>` (mỗi mục có timestamp riêng) |
| Người/agent thực thi | AI agent (theo skill); screenshot Issue: người kiểm thử chụp sau khi xác nhận bug |
| Thư mục evidence | `evidence/` |
| Cách reset state | `<lệnh/kịch bản chuẩn bị state trước mỗi ca>` |
| Database làm việc trước khi chạy | `<đường dẫn, checksum/trạng thái; nêu sẵn thay đổi nếu có>` |
| Database test | `<đường dẫn bản sao hoặc snapshot để restore>` |

## Quy ước ghi

- **EV-ID** đánh số tăng dần theo **thứ tự thực thi**; mỗi mục chỉ liên kết một `T-ID`, nhưng một `T-ID` có thể có nhiều `EV-ID` khi chạy lại. Ghi `Run ID` và số lần thử để không ghi đè lịch sử.
- Mỗi mục nêu: interface, cách chuẩn bị state, **lệnh/thao tác thật**, kết quả thô, Expected (tham chiếu oracle), Actual, Status.
- **Lệnh thật, đầy đủ, nằm trong khối mã shell.** Mọi lệnh phải ở trong fenced code block có gắn ngôn ngữ (`zsh` hoặc `bash`) và ghi **đủ tham số** — **không** viết tắt kiểu `curl …` và **không** nhét lệnh vào giữa dòng văn. Ghi cả hành vi side-effect (DB row, header) khi có.
- **JSON phải pretty-print (mỗi field một dòng) trong khối mã `json`.** Tuyệt đối **không** viết cả object trên một dòng, và **không** gộp `request`/`response`/`pre-state`/`post-state` vào một dòng. Chỉ được rút gọn một chuỗi dài (token, mật khẩu) bằng `…` **bên trong dòng giá trị**, không rút gọn cả object.
- Chỉ kèm script chạy test khi đó là deliverable được yêu cầu; nếu dùng script tạm, ghi cách tái hiện trong log và giữ script tạm ngoài bài nộp.
- Không đánh dấu PASS/FAIL cho ca mà đặc tả không định nghĩa Expected — dùng `Quan sát`/`Inconclusive` và nêu rõ.
- Kết thúc mỗi mục bằng dòng `---` để log dài vẫn dễ quét.

### Định dạng bắt buộc (một dòng = lỗi)

> ❌ **Sai** — viết tắt và dồn một dòng:
> `Lệnh: curl … -d '{"email":"nobody@eshop.com",...}' Kết quả thô: HTTP 401; {"error":"Invalid email or password"}; POST-STATE login_attempts=0 locked_until=NULL`
>
> ✅ **Đúng** — lệnh đầy đủ trong khối mã `zsh`, JSON xuống dòng trong khối mã `json`, trạng thái trong khối mã `text`:

**Thao tác / lệnh:**
```zsh
curl -s -X POST http://localhost:3000/api/login \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"nobody@eshop.com","password":"Whatever1!"}'
```

**Kết quả thô:**
```json
{
  "error": "Invalid email or password"
}
```
```text
HTTP 401 · pre-state login_attempts=0 locked_until=NULL · post-state login_attempts=0 locked_until=NULL
```

> **Ngoại lệ hợp lệ:** body không phải JSON (HTML/text, DOM snippet, output DB, output Playwright) đặt trong khối mã `text`/`html` tương ứng, nhưng vẫn phải **xuống dòng theo cấu trúc** — không dồn toàn bộ kết quả vào một dòng.


## Evidence items

### EV-`<FEATURE>`-001 — `<T-ID>` `<mô tả ngắn>`

| Trường | Giá trị |
| --- | --- |
| Test case | `<DT/BVA-ID>` |
| Run ID / lần thử | `<run-YYYYMMDD hoặc mã run> / <1, 2, ...>` |
| Kỹ thuật | `Domain/EP / BVA` |
| Thời điểm | `<YYYY-MM-DD HH:MM:SS ±hhmm>` |
| Interface | `API <METHOD endpoint>` / `UI <url> (<browser>)` |
| Tiền điều kiện / reset state | `<state cụ thể, tài khoản, prior data>` |

**Thao tác / lệnh:**
```zsh
<lệnh thật, ĐẦY ĐỦ tham số — ví dụ: curl -s -X POST http://localhost:3000/api/login -H 'Content-Type: application/json' --data-raw '{"email":"nobody@eshop.com","password":"Whatever1!"}'>
```

**Kết quả thô:**
```json
{
  "<field>": "<giá trị thật — mỗi field một dòng>"
}
```
```text
HTTP <status> · pre-state <...> · post-state <...>
```

- **Expected (oracle ref):** `<theo đặc tả + rule>`
- **Actual:** `<kết quả quan sát thật>`
- **Status:** `PASS / FAIL / BLOCKED / Quan sát`
- **Artifact:** `evidence/<tên-file>.log|json|png`
- **Bug liên quan:** `<BUG-FEATURE-NN hoặc 'không'>`
- **Screenshot / Issue:** nếu ca phát hiện bug, ghi `Chờ người kiểm thử xác nhận`; sau khi xác nhận, người kiểm thử chụp ảnh và mở Issue kèm ảnh. Nếu không có bug, ghi `Không áp dụng`.
- **Ghi chú:** `<độ lặp lại, giới hạn, điều kiện bất thường>`

---

### EV-`<FEATURE>`-002 — `<T-ID>` `<mô tả ngắn>`

`<lặp lại khối trên cho mỗi lần thử thực thi; luôn kết thúc bằng dòng '---'>`

---

## Tổng hợp evidence

| Chỉ số | Số lượng |
| --- | ---: |
| Ca thiết kế | `<n>` |
| Ca đã chạy duy nhất trong run được chọn | `<n>` |
| Tổng lần thử thực thi (EV-ID) | `<n>` |
| PASS | `<n>` |
| FAIL | `<n>` |
| Quan sát / Inconclusive | `<n>` |
| BLOCKED (nêu lý do) | `<n>` |

- **Artifact thô:** `<danh sách file trong evidence/>`
- **Đối chiếu catalog:** mọi `T-ID` được tính là đã chạy trong run được chọn có ít nhất một EV-ID của run đó; mỗi EV-ID trỏ đến đúng một T-ID, không có EV-ID mồ côi. Nếu một case được thử nhiều lần trong cùng run, nêu rõ lần thử nào dùng cho verdict tổng hợp và giữ các lần trước.

## Xác nhận cleanup sau khi hoàn tất

| Mục | Kết quả thực tế |
| --- | --- |
| Test services đã dừng | `<process/port và lệnh kiểm tra>` |
| Database test/file tạm đã xóa | `<đường dẫn và lệnh kiểm tra>` |
| Database làm việc đã trở về trạng thái trước khi chạy | `<checksum/trạng thái trước và sau; hoặc cách restore snapshot>` |

Không điền “đã reset” nếu chưa kiểm tra. Nếu cleanup thất bại, ghi rõ đường dẫn, trạng thái còn lại và bước khôi phục cần làm trước ca kiểm thử tiếp theo.
