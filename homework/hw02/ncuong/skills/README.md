# Bộ skill kiểm thử theo miền dữ liệu

Thư mục này chứa **15 skill** hỗ trợ phân tích yêu cầu, thiết kế và thực thi test, đánh giá coverage, rồi viết báo cáo kiểm thử bằng tiếng Việt. Bài HW02 dùng **Domain Testing với Equivalence Partitioning (EP)** và **Boundary Value Analysis (BVA)**. Decision table hoặc state model chỉ hỗ trợ phân tích rule khi cần; không tự tạo thêm bộ test UI.

README này dành cho người đọc trong nhóm. Bộ skill riêng của sinh viên nằm ở `homework/hw02/<tên viết tắt>/skills/`; yêu cầu bài ở `homework/hw02/docs/`. Báo cáo chung nằm ở `reports/` (`main-report.md`, `ai-audit.md`, `ai-critique.md` và bản PDF tương ứng khi nộp); báo cáo từng feature nằm ở `features/<FEATURE_CODE>/`. HW02 còn yêu cầu `git-commit-log.txt` và chọn bốn feature, mỗi pool một feature. Mỗi thư mục con có `SKILL.md` mô tả cách một AI agent thực hiện công việc; các file trong `assets/` là mẫu đầu ra. Skill không tự biến nội dung báo cáo thành sự thật: kết quả PASS/FAIL vẫn cần chạy trên hệ thống và có bằng chứng.

## Đọc nhanh: dùng skill nào?

| Việc cần làm | Bắt đầu từ |
| --- | --- |
| Kiểm thử trọn một feature từ đặc tả đến báo cáo | [`domain-testing-workflow`](domain-testing-workflow/SKILL.md) |
| Phân tích input, ràng buộc và vùng hợp lệ/không hợp lệ | [`input-domain-partitioner`](input-domain-partitioner/SKILL.md) |
| Chọn lớp tương đương và giá trị đại diện | [`equivalence-partitioning-generator`](equivalence-partitioning-generator/SKILL.md) |
| Thiết kế ca ở sát ngưỡng, giới hạn, thời điểm | [`boundary-value-generator`](boundary-value-generator/SKILL.md) |
| Nhiều điều kiện cùng quyết định kết quả | [`decision-table-builder`](decision-table-builder/SKILL.md) |
| Kết quả phụ thuộc trạng thái hoặc thứ tự sự kiện | [`state-transition-test-designer`](state-transition-test-designer/SKILL.md) |
| Chưa rõ Expected hoặc cách quan sát kết quả | [`test-oracle-writer`](test-oracle-writer/SKILL.md) |
| Gộp case từ nhiều kỹ thuật, giữ ID và số liệu nhất quán | [`test-case-catalog`](test-case-catalog/SKILL.md) |
| Đặt mục tiêu và tính coverage | [`coverage-goal-planner`](coverage-goal-planner/SKILL.md) |
| Viết báo cáo cho một hoặc nhiều feature | [`feature-testing-report-writer`](feature-testing-report-writer/SKILL.md), [`testing-report-assembler`](testing-report-assembler/SKILL.md) |
| Ghi bug và lịch sử sử dụng AI | [`test-findings-report-writer`](test-findings-report-writer/SKILL.md), [`ai-audit-logger`](ai-audit-logger/SKILL.md) |

Có thể dùng riêng một skill cho một việc nhỏ. Với bài kiểm thử đầy đủ, dùng `domain-testing-workflow` làm điểm điều phối để các phần dùng chung ID, catalog và evidence.

## Bộ skill được chia thành 5 nhóm

### 1. Điều phối quy trình

**[`domain-testing-workflow`](domain-testing-workflow/SKILL.md)** nối các bước: đọc đặc tả → dựng mô hình miền → thiết kế case → lập catalog → đặt coverage → thực thi an toàn → đánh giá kết quả → viết báo cáo. Nó yêu cầu chỉ dùng kỹ thuật phù hợp với feature; decision table và state transition không phải thủ tục bắt buộc cho mọi màn hình hoặc API.

Đây là skill nên đọc đầu tiên nếu team muốn hiểu quan hệ giữa các skill còn lại. Nó cũng đặt các nguyên tắc thực thi: dùng môi trường test phù hợp, tách dữ liệu test khỏi dữ liệu đang làm việc, ghi nhận trạng thái trước và sau, không tự nhận đã chạy nếu mới đọc code, và chỉ cleanup tài nguyên do phiên test sở hữu.

### 2. Mô hình hóa và thiết kế test

| Skill | Nó giải quyết gì? | Đầu ra chính |
| --- | --- | --- |
| [`input-domain-partitioner`](input-domain-partitioner/SKILL.md) | Liệt kê input, kiểu/đơn vị/độ chính xác, state liên quan; chuyển rule thành predicate và ràng buộc. Tách **hợp lệ**, **không hợp lệ**, **chưa rõ**, đồng thời xét khả năng tạo dữ liệu test. | Danh sách dimension, constraint, vùng miền ứng viên và câu hỏi còn mở. **Chưa chọn giá trị test cụ thể.** |
| [`equivalence-partitioning-generator`](equivalence-partitioning-generator/SKILL.md) | Chia miền thành các lớp có hành vi kỳ vọng tương đương, chọn giá trị đại diện và xử lý tương tác giữa các input. | `P-ID`, điều kiện của từng lớp, giá trị đại diện, case và lỗ hổng coverage. |
| [`boundary-value-generator`](boundary-value-generator/SKILL.md) | Tìm biên từ predicate: min/max, độ dài, số lượng, thời gian hoặc quan hệ giữa hai giá trị. Chọn điểm ngay dưới/tại/ngay trên biên; chỉ dùng `ON/IN/OUT` khi đã xác định rõ phía `IN` và `OUT`. | `B-ID`, điểm biên, Expected mỗi phía, baseline, case và lý do chọn giá trị. |
| [`decision-table-builder`](decision-table-builder/SKILL.md) | Dùng khi nhiều điều kiện cùng quyết định một kết quả, ví dụ quyền người dùng × trạng thái đơn hàng × điều kiện thanh toán. Phân biệt tổ hợp đã có rule, chưa được định nghĩa, xung đột hoặc không thể xảy ra. | Điều kiện `DC-ID`, hành động và decision rule `DR-ID`, case theo rule. |
| [`state-transition-test-designer`](state-transition-test-designer/SKILL.md) | Dùng khi hành vi phụ thuộc trạng thái trước đó hoặc thứ tự sự kiện, ví dụ khóa tài khoản, đơn hàng, retry, hết hạn. Xét guard, sự kiện bị từ chối, side effect và invariant. | State `S-ID`, transition `TR-ID`, chuỗi setup và case theo transition. |

**Domain Testing** là cách nhìn tổng thể vào miền input và các rule. **Equivalence Partitioning** chọn đại diện cho những vùng được kỳ vọng hành xử giống nhau. **BVA** tập trung vào nơi hành vi có thể đổi tại biên. Một case có thể phục vụ cả hai kỹ thuật và chỉ cần tồn tại **một lần** trong catalog.

Các skill thiết kế đều lấy Expected từ yêu cầu hoặc nguồn được chấp nhận. Hành vi đang có trong code/SUT có thể giúp điều tra lỗi, nhưng không tự trở thành đặc tả. Nếu rule thiếu hoặc mâu thuẫn, ghi là chưa rõ thay vì tự đặt ngưỡng, mã lỗi hay kết quả mong đợi.

### 3. Oracle, catalog và coverage

**[`test-oracle-writer`](test-oracle-writer/SKILL.md)** trả lời: *chạy case này thì cần quan sát điều gì để biết đúng hay sai?* Oracle có thể gồm HTTP response, thông báo UI, dữ liệu lưu, trạng thái mới, event/notification hoặc invariant. Một case có thể có nhiều assertion bắt buộc. Expected được xác định trước; Actual chỉ được ghi sau khi chạy.

**[`test-case-catalog`](test-case-catalog/SKILL.md)** là danh sách case có thẩm quyền cho một feature. Mỗi `T-ID` chỉ định nghĩa một case; hai phần Domain/BVA chỉ dẫn về ID đó. Hai đề xuất case được gộp nếu **cùng setup, cùng thao tác/input và một lần quan sát đủ kiểm tra các oracle cần thiết**. Khi gộp, giữ tất cả obligation mà case phủ. Nếu setup, thao tác hoặc phép quan sát cần thiết khác nhau đáng kể, giữ case riêng. Tiền tố `DT-`, `BVA-` có thể cho biết case xuất phát từ đâu, không giới hạn kỹ thuật mà case được tính coverage.

**[`coverage-goal-planner`](coverage-goal-planner/SKILL.md)** đếm **nghĩa vụ kiểm thử** thay vì chỉ đếm số case. Với HW02, mẫu số chính là lớp tương đương và điểm biên khả thi; decision rule hoặc transition chỉ là mô hình hỗ trợ trừ khi phạm vi bài thay đổi. Nó tách ba câu hỏi:

- **Designed:** đã có case cụ thể để kiểm tra nghĩa vụ này chưa?
- **Executed:** đã thực sự chạy và có kết quả quan sát chưa?
- **Passed:** kết quả có thỏa oracle không?

Một case FAIL vẫn đóng góp cho **executed coverage**, nhưng không cho **passed coverage**. Mỗi tỷ lệ cần mẫu số rõ ràng; nghĩa vụ chưa giải quyết hoặc bị chặn không được âm thầm loại khỏi phép tính. Coverage cao cũng không chứng minh phần mềm không còn lỗi.

### 4. Viết báo cáo

| Skill | Phạm vi |
| --- | --- |
| [`domain-testing-report-writer`](domain-testing-report-writer/SKILL.md) | Viết `features/<FEATURE_CODE>/domain-analysis.md`: input, constraint, equivalence class, lựa chọn representative case, tương tác và coverage. Dẫn `T-ID` thay vì chép lại toàn bộ case. |
| [`boundary-value-report-writer`](boundary-value-report-writer/SKILL.md) | Viết `features/<FEATURE_CODE>/boundary-analysis.md`: predicate tạo biên, tính bao gồm/loại trừ, kiểu/đơn vị/độ chính xác, ON/IN/OUT và case liên quan. |
| [`feature-testing-report-writer`](feature-testing-report-writer/SKILL.md) | Ghép **bốn file cho mỗi feature**: `domain-analysis.md`, `boundary-analysis.md`, `test-cases.md`, `test-results.md`; giữ evidence trong cùng thư mục feature. |
| [`testing-report-assembler`](testing-report-assembler/SKILL.md) | Tạo **master report** cho nhiều feature: đường dẫn tới từng báo cáo chi tiết, tổng case theo run, bug và thống kê severity. Không lặp lại toàn bộ suy luận và case của từng feature. |

Template đi kèm:

- Bốn mẫu trong [`feature-testing-report-writer/assets/`](feature-testing-report-writer/assets/): `domain-analysis-template.md`, `boundary-analysis-template.md`, `test-cases-template.md`, `test-results-template.md`. Các file cùng dùng một catalog `T-ID` và evidence `EV-ID`.
- [`evidence-log-template.md`](feature-testing-report-writer/assets/evidence-log-template.md): nhật ký những lần thử thực thi, gồm lệnh/thao tác, kết quả thô, Actual, verdict và tài nguyên đã cleanup.
- [`master-report-template.md`](testing-report-assembler/assets/master-report-template.md): bố cục báo cáo tổng cho nhiều feature.
- [`github-issue-template.md`](test-findings-report-writer/assets/github-issue-template.md): mẫu Issue độc lập với phần chuẩn bị, lệnh kích hoạt/đo kết quả, Expected/Actual và bằng chứng; không lấy nguyên khối “Reproduce nhanh” trong báo cáo làm toàn bộ Issue.

Hai template phân tích đặt thông tin cần review ngay trong nội dung chính: lớp EP có điều kiện, giá trị đại diện, Expected, rule và `T-ID`; mỗi biên BVA có ngưỡng, setup, giá trị từng điểm, Expected và `T-ID`. Chọn bảng hoặc đoạn ngắn theo tính chất feature; không bắt buộc mục “Đọc nhanh”, không dùng khuôn bug report cho mọi phần, và không tạo bảng ánh xạ lặp. ON/IN/OUT chỉ dùng khi đã nói rõ phía nào là IN. Chỉ chú thích rule khó, setup, điểm không khả thi hoặc đặc tả chưa rõ. Actual và bug chi tiết ở `test-results.md`.

Skill báo cáo không mặc định có quyền chạy SUT. Nếu yêu cầu **chỉ thiết kế test hoặc chỉ biên tập báo cáo**, ghi rõ phần chưa chạy. Nếu yêu cầu **kiểm thử thực tế** và có môi trường phù hợp, chạy case trong phạm vi, lưu evidence rồi mới ghi PASS/FAIL. Kiểm tra mã nguồn có thể giúp lập case hoặc tìm nguyên nhân, nhưng không được ghi như một lần chạy API/UI.

### 5. Bug và minh bạch khi dùng AI

**[`test-findings-report-writer`](test-findings-report-writer/SKILL.md)** viết bug report từ lỗi có bằng chứng để sinh viên xác nhận trước khi mở Issue. Một test FAIL chưa tự động là bug: cần kiểm tra oracle, dữ liệu setup và khả năng tái hiện. Mỗi bug có ID theo feature (`BUG-<FEATURE_CODE>-NN`), các bước tái hiện thủ công với giá trị cụ thể, Expected theo đặc tả, Actual và evidence. Phần **AI Gap Analysis** là phần sinh viên/người kiểm thử tự đánh giá; skill chỉ để khung trống và giữ nội dung họ cung cấp. Với bug, agent chuẩn bị evidence và bước tái hiện để sinh viên review; sau khi xác nhận, sinh viên chụp screenshot và mở GitHub Issue. Cả Issue và ảnh gắn kèm đều bắt buộc khi nộp HW02, nhưng trước bước review phải ghi `Chờ người kiểm thử xác nhận`, không coi là bị quên.

Issue cần tự đủ thông tin để người khác chạy lại mà không phải đọc báo cáo trước: mô tả fixture và trạng thái DB, cách kích hoạt, lệnh quan sát, mốc thời gian nếu có, Expected/Actual tại từng bước quyết định, ảnh/log và ảnh hưởng của bug. Báo cáo feature có thể giữ phần tái hiện ngắn hơn; mẫu Issue riêng nằm trong `test-findings-report-writer/assets/`.

Quan sát phát sinh ngoài các ca EP/BVA được lưu ở `supporting-materials/` và dẫn link từ báo cáo tổng, không cộng vào coverage hoặc số ca của hai kỹ thuật. Nếu sinh viên xác nhận đó là bug, vẫn phải báo cáo và mở GitHub Issue kèm screenshot theo §6 của đề.

**[`ai-audit-logger`](ai-audit-logger/SKILL.md)** ghi lại việc dùng AI từ hội thoại hoặc transcript có thể kiểm chứng. Mỗi lần tương tác cần tên công cụ, ngày giờ, prompt và output tương ứng; thiếu dữ liệu thì đánh dấu thiếu, không dựng lại từ trí nhớ. Mẫu nằm ở [`ai-audit-report-template.md`](ai-audit-logger/assets/ai-audit-report-template.md). AI audit ghi **AI đã tạo gì**; nhận xét và bản sửa của con người là nội dung khác.

## Cách các artifact nối với nhau

```text
Đặc tả / acceptance criteria
  → Requirement (R-ID)
  → Dimension, constraint, region (D-ID, C-ID, RG-ID)
  → Lớp / biên / decision rule / transition (P-ID, B-ID, DR-ID, TR-ID)
  → Test case duy nhất (T-ID) + Expected/oracle
  → Lần thử thực thi (Run ID, EV-ID) + Actual/verdict
  → Coverage, bug hoặc điểm chưa xác định
  → Báo cáo feature → master report
```

| ID | Nghĩa | Lưu ý |
| --- | --- | --- |
| `R-ID` | Requirement hoặc business rule | Lấy từ nguồn yêu cầu; ví dụ `R1`. |
| `D-ID` | Input/state dimension | Kiểu, miền giá trị, đơn vị, null/omitted, nguồn rule. |
| `C-ID` | Constraint/predicate của miền | Ví dụ `quantity >= 1`. |
| `RG-ID` | Vùng miền ứng viên | Tách khỏi `R-ID` để không đụng requirement. |
| `P-ID` | Equivalence class | Template hoặc artifact cũ có thể dùng `EC-ID`; giữ ID cũ và ghi ánh xạ khi cần. |
| `B-ID` | Boundary | Một biên có thể tạo các nghĩa vụ ON/IN/OUT khác nhau. |
| `DC-ID` / `DR-ID` | Điều kiện / rule trong decision table | `DC-ID` tách khỏi `C-ID` của domain constraint. |
| `S-ID` / `TR-ID` | State / transition | Dùng cho feature có hành vi phụ thuộc trạng thái. |
| `T-ID` | Test case | Mỗi case có một ID ổn định trong catalog; có thể phủ nhiều obligation. |
| `EV-ID` | Một lần thử thực thi | Một `T-ID` có thể có nhiều `EV-ID` khi rerun. Ghi kèm `Run ID`. |

Nếu tài liệu đang làm dùng ID cũ theo quy ước khác, **không đổi ID âm thầm**. Ghi rõ đối tượng mà ID đại diện và bảng ánh xạ sang namespace chung.

### Ví dụ nhỏ: một case phục vụ hai kỹ thuật

Giả sử **đặc tả ví dụ** quy định số lượng đặt hàng là số nguyên `1 ≤ quantity ≤ stock`, và fixture có `stock = 5`:

1. `input-domain-partitioner` tạo `C1: quantity >= 1`, `C2: quantity <= stock` và ghi kiểu số nguyên.
2. `equivalence-partitioning-generator` tạo lớp hợp lệ, lớp `quantity < 1`, lớp `quantity > stock`.
3. `boundary-value-generator` xét biên dưới `1` và biên quan hệ `quantity = stock`; với biên dưới, `ON = 1`, `IN = 2`, `OUT = 0` (vì miền là số nguyên).
4. Case nhập `quantity = 1` có thể vừa đại diện cho lớp hợp lệ, vừa kiểm tra điểm `ON` của biên dưới. Catalog giữ **một `T-ID`**, liên kết cả `P-ID` và `B-ID`.
5. Nếu thực thi, evidence log ghi `EV-ID` với request/thao tác thật, response và thay đổi dữ liệu cần quan sát. Nếu chạy lại cùng case sau khi sửa bug, thêm `EV-ID` mới; không tạo `T-ID` mới chỉ vì rerun.

Ví dụ này chỉ minh họa cách phối hợp skill, không phải rule của SUT trong repo. Khi làm bài thật, lấy ngưỡng, kiểu dữ liệu và Expected từ đặc tả của feature đang kiểm thử.

## Quy ước khi thực thi và đọc kết quả

Trong **một run được chọn**: `Đã chạy = PASS + FAIL + INCONCLUSIVE`; `Thiết kế = Đã chạy + BLOCKED + Chưa chạy`. Các bảng tổng đếm `T-ID` duy nhất, không cộng số EV-ID hoặc cộng subtotal Domain/BVA vì một case có thể nằm trong nhiều kỹ thuật. Lần thử cũ vẫn ở evidence log; báo cáo phải nói rõ run/lần thử nào dùng cho verdict tổng hợp.

- `PASS`: đã chạy, các assertion bắt buộc của oracle có bằng chứng thỏa mãn.
- `FAIL`: đã chạy, bằng chứng mâu thuẫn với một assertion bắt buộc; cần điều tra trước khi xác nhận bug.
- `INCONCLUSIVE` / `Quan sát`: đã có quan sát nhưng chưa thể kết luận đúng/sai, chẳng hạn đặc tả chưa định nghĩa Expected.
- `BLOCKED`: execution nằm trong phạm vi nhưng có trở ngại cụ thể khiến case không thể chạy hoặc hoàn tất.
- `Chưa chạy`: chưa thực thi; dùng được cho báo cáo chỉ thiết kế test.

Khi thực thi có dữ liệu trạng thái, ưu tiên môi trường và database test riêng. Ghi setup, cách reset, các side effect và bước cleanup. Không tự xóa database người dùng, ghi đè thay đổi có sẵn hoặc tuyên bố đã khôi phục nếu chưa kiểm tra. Nếu EP/BVA phải chạy qua browser, ghi kết quả thật; đọc component source chưa đủ để kết luận đã chạy.

## Lộ trình sử dụng gợi ý

1. **Chốt phạm vi và nguồn yêu cầu:** feature, interface chạy test, rule nào trong phạm vi, môi trường có chạy được không, đầu ra cần là thiết kế hay cả kết quả thực thi.
2. **Dựng mô hình:** dùng `input-domain-partitioner`, rồi chọn `equivalence-partitioning-generator` và `boundary-value-generator`. Chỉ thêm decision table/state transition khi behavior thật sự cần.
3. **Chốt case:** dùng `test-oracle-writer` và `test-case-catalog`; mỗi case có rule nguồn, obligation, setup, input/thao tác và Expected quan sát được.
4. **Đặt coverage:** dùng `coverage-goal-planner` để xác định nghĩa vụ đủ điều kiện, mẫu số, mục tiêu và lỗ hổng.
5. **Nếu có thực thi:** chạy trên môi trường phù hợp, lưu một `EV-ID` cho mỗi lần thử và ghi PASS/FAIL/INCONCLUSIVE/BLOCKED dựa trên Actual. Giữ lịch sử rerun.
6. **Viết báo cáo:** tạo phần Domain và BVA, báo cáo feature, bug có evidence; nếu nhiều feature, tạo master report. Phần AI audit và AI Gap Analysis thực hiện theo yêu cầu bài nộp.

Không cần dùng đủ 15 skill cho mọi feature. Điều quan trọng là **rule → nghĩa vụ kiểm thử → case → oracle → evidence → kết luận** truy lại được, và mọi phần chưa rõ hoặc chưa chạy đều được nói rõ.
