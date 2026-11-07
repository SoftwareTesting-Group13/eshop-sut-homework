#!/usr/bin/env python3
"""Sinh báo cáo bug và GitHub issue draft cho HW03 Task 1.

Mỗi bug có:
- bối cảnh / checklist / môi trường,
- bước tái hiện, Expected vs Actual,
- screenshot,
- root cause kèm code block lấy trực tiếp từ source và link GitHub tới đúng dòng.

Chạy:
    python tools/build_bugs.py
"""
import glob
import json
import os
import textwrap

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(BASE)
BUGS_DIR = os.path.join(OUT, "bugs")
ISSUES_DIR = os.path.join(OUT, "issues")
SHOTS_DIR = os.path.join(OUT, "screenshots")
os.makedirs(BUGS_DIR, exist_ok=True)
os.makedirs(ISSUES_DIR, exist_ok=True)

REPO = "SoftwareTesting-Group13/eshop-sut-homework"
BRANCH = "ncuong"
COMMIT = "85af3ba875c88283615e22cb108f13e2fccaf0e9"
ROOT = os.path.abspath(os.path.join(BASE, "../../../../../.."))
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/homework/hw03/ncuong/features/GUI"
BLOB = f"https://github.com/{REPO}/blob/{COMMIT}"

ENV = (
    "Chromium 158 / Playwright 1.65; backend `http://localhost:3000`; "
    "web `http://localhost:5173`; viewport 1280×900 (mobile 360×800 khi có kiểm tra responsive)."
)


def code_link(path, line):
    return f"[`{path}:{line}`]({BLOB}/{path}#L{line})"


def snippet(path, start, end):
    full = os.path.join(ROOT, path)
    with open(full, encoding="utf-8") as f:
        lines = f.readlines()
    return "".join(lines[start - 1:end]).rstrip("\n")


def root_section(entries):
    """entries: list of dict(path, start, end, lang, note)."""
    chunks = []
    for e in entries:
        lang = e.get("lang", "jsx")
        link = code_link(e["path"], e["start"])
        if e["end"] != e["start"]:
            link += f"–[L{e['end']}]({BLOB}/{e['path']}#L{e['end']})"
        block = snippet(e["path"], e["start"], e["end"])
        chunk = [f"**{link}**\n", f"```{lang}\n{block}\n```"]
        if e.get("note"):
            chunk.append(f"\n{e['note']}")
        chunks.append("\n".join(chunk))
    return "\n\n".join(chunks)


B = [
    dict(
        id="BUG-GUI-01", severity="Minor", priority="Medium",
        fr="FR-02 — Đăng nhập", ia="IA-01", screen="/login",
        title="Tiêu đề trang Đăng nhập ghi “Đăng Ký” thay vì “Đăng nhập”",
        checks=["CHK-01"], shots=["CHK-01-login-heading.png"],
        steps=[
            "Mở `http://localhost:5173/login` trong cửa sổ chưa đăng nhập.",
            "Đọc tiêu đề trên card đăng nhập, ngay phía trên hai ô nhập.",
        ],
        expected="Tiêu đề mô tả đúng màn hình Đăng nhập (ví dụ “Đăng nhập”) và là một thẻ `<h1>`.",
        actual="Tiêu đề là `<h2>Đăng Ký</h2>`; trang không có `<h1>`. Người dùng có thể tưởng đang ở màn hình đăng ký.",
        root=[
            dict(path="frontend-web/src/pages/Login.jsx", start=24, end=24,
                 note="Chuỗi tiêu đề bị copy từ màn hình Register và không được sửa lại."),
        ],
        fix="Đổi tiêu đề thành “Đăng nhập” và dùng `<h1>` cho tiêu đề trang; thêm kiểm tra heading vào test auth.",
    ),
    dict(
        id="BUG-GUI-03", severity="Major", priority="High",
        fr="FR-21 — Tiêu chuẩn giao diện chung", ia="IA-01", screen="/register, /profile",
        title="Text phụ và nút đỏ không đạt WCAG 2.2 AA về contrast",
        checks=["CHK-07", "CHK-16"],
        shots=["CHK-07-register-contrast.png", "CHK-16-profile-contrast.png"],
        steps=[
            "Mở `/register` và `/profile` (đã đăng nhập).",
            "Chạy axe-core hoặc tính contrast của helper text, nút đỏ, username vàng và nút đăng xuất.",
        ],
        expected="Text thường đạt tối thiểu 4.5:1 so với nền; text lớn đạt 3:1.",
        actual="axe-core báo helper text `#9ca3af` trên `#ffffff` = 2.53:1; trắng trên `#ef4444` = 3.76:1; vàng `#fde047` trên xanh `#2563eb` = 3.92:1; nút đăng xuất đỏ/trắng = 3.76:1.",
        root=[
            dict(path="frontend-web/src/pages/Register.jsx", start=64, end=65,
                 note="Helper text dùng `text-gray-400` trên nền trắng."),
            dict(path="frontend-web/src/pages/Register.jsx", start=70, end=75,
                 note="Nút tích cực dùng `bg-red-500` với chữ trắng."),
            dict(path="frontend-web/src/App.jsx", start=26, end=29,
                 note="Username dùng `text-yellow-300` trên nền xanh; nút đăng xuất dùng `bg-red-500` với chữ trắng."),
        ],
        fix="Dùng màu đậm hơn cho helper text và nút đỏ, hoặc đổi sang nền sáng/chữ tối; chạy lại axe-core sau khi sửa.",
    ),
    dict(
        id="BUG-GUI-04", severity="Minor", priority="Medium",
        fr="FR-03 — Quên mật khẩu", ia="IA-01", screen="/forgot-password",
        title="Hai nút ở bước 2 Quên mật khẩu trông giống hệt nhau",
        checks=["CHK-11"], shots=["CHK-11-forgot-buttons.png"],
        steps=[
            "Mở `/forgot-password`, nhập email đã đăng ký và bấm “Lấy mã OTP”.",
            "So sánh nút “Đặt lại mật khẩu” và nút “← Quay lại”.",
        ],
        expected="Primary action nổi bật, dùng màu xanh dương theo FR-21; secondary/back rõ ràng là hành động phụ.",
        actual="Cả hai đều là nút xanh lá full-width (`bg-green-600`), cùng kích thước và kiểu chữ; người dùng dễ bấm nhầm.",
        root=[
            dict(path="frontend-web/src/pages/ForgotPassword.jsx", start=89, end=95,
                 note="Hai button dùng cùng class `w-full bg-green-600 text-white`."),
        ],
        fix="Render nút quay lại dạng text/outline và giữ primary action là nút filled màu xanh dương.",
    ),
    dict(
        id="BUG-GUI-05", severity="Minor", priority="Medium",
        fr="FR-21 — Tiêu chuẩn giao diện chung", ia="IA-01", screen="/register, /forgot-password, /profile",
        title="Ba màn hình Register, Forgot Password và Profile không có thẻ `<h1>`",
        checks=["CHK-05", "CHK-09", "CHK-13"],
        shots=["CHK-05-register-h1.png", "CHK-09-forgot-h1.png", "CHK-13-profile-h1.png"],
        steps=[
            "Mở lần lượt `/register`, `/forgot-password`, `/profile`.",
            "Đếm số thẻ `<h1>` trong DOM hoặc chạy axe-core.",
        ],
        expected="Mỗi trang có đúng một `<h1>` mô tả nội dung trang (FR-21).",
        actual="Cả ba trang có 0 `<h1>`; tiêu đề được render bằng `<h2>` (Profile có hai `<h2>` cho hai section).",
        root=[
            dict(path="frontend-web/src/pages/Register.jsx", start=31, end=33,
                 note="Tiêu đề Register là `<h2>`."),
            dict(path="frontend-web/src/pages/ForgotPassword.jsx", start=42, end=44,
                 note="Tiêu đề Forgot Password là `<h2>`."),
            dict(path="frontend-web/src/pages/Profile.jsx", start=112, end=114,
                 note="Section hồ sơ dùng `<h2>`; section lịch sử đơn hàng cũng dùng `<h2>` tại dòng 167."),
        ],
        fix="Dùng `<h1>` cho tiêu đề trang và `<h2>` cho các section; thêm kiểm tra heading outline.",
    ),
    dict(
        id="BUG-GUI-06", severity="Major", priority="High",
        fr="FR-04 — Hồ sơ cá nhân", ia="IA-01", screen="/profile",
        title="Bảng lịch sử đơn hàng gây horizontal scroll ở viewport 360px",
        checks=["CHK-15"], shots=["CHK-15-profile-mobile-table.png"],
        steps=[
            "Đăng nhập, mở `/profile` ở viewport 360×800 với ít nhất một đơn hàng.",
            "Đo `document.documentElement.scrollWidth` và `clientWidth`.",
        ],
        expected="Bảng co giãn hoặc nằm trong vùng scroll riêng; cả trang không có horizontal scroll.",
        actual="`scrollWidth` = 399px, `clientWidth` = 360px (tràn 39px); bảng 5 cột giữ nguyên width desktop và bị cắt.",
        root=[
            dict(path="frontend-web/src/pages/Profile.jsx", start=171, end=179,
                 note="`<table className=\"w-full text-left\">` không có wrapper `overflow-x-auto` hay layout card cho mobile."),
        ],
        fix="Bọc bảng trong `overflow-x-auto` với `min-width`, hoặc render card đơn hàng dưới breakpoint `md`.",
    ),
    dict(
        id="BUG-GUI-07", severity="Minor", priority="Low",
        fr="FR-21 — Tiêu chuẩn giao diện chung", ia="IA-01", screen="/login, /register, /forgot-password, /profile",
        title="Layout không mirror khi document direction là RTL",
        checks=["CHK-65"], shots=["CHK-65-login-rtl.png"],
        steps=[
            "Mở `/login`.",
            "Đặt `document.documentElement.dir = 'rtl'` và quan sát header, link “Quên mật khẩu?” và thứ tự các phần tử.",
        ],
        expected="Alignment, thứ tự và spacing được mirror cho người đọc RTL.",
        actual="Utility vật lý giữ link “Quên mật khẩu?” ở bên phải và header không đảo; layout không mirror.",
        root=[
            dict(path="frontend-web/src/pages/Login.jsx", start=48, end=51,
                 note="Dùng `text-right` thay vì `text-end`."),
            dict(path="frontend-web/src/App.jsx", start=20, end=29,
                 note="Header dùng `justify-between`, `gap-4` và thứ tự vật lý; không có logical property."),
        ],
        fix="Dùng logical utilities (`text-start`/`text-end`, `ms`/`me`) và thêm RTL smoke test.",
    ),
    dict(
        id="BUG-GUI-08", severity="Major", priority="High",
        fr="FR-02 — Đăng nhập; FR-22 — Form", ia="IA-02", screen="/login",
        title="Ô email dùng `type=text` và ô mật khẩu hiển thị rõ ký tự",
        checks=["CHK-17", "CHK-18"], shots=["CHK-17-18-19-login-fields.png"],
        steps=[
            "Mở `/login`.",
            "Nhập email và mật khẩu; kiểm tra `type` của hai input.",
        ],
        expected="Ô email dùng `type=\"email\"`; ô mật khẩu dùng `type=\"password\"` (FR-02, FR-22).",
        actual="Cả hai input đều là `type=\"text\"`; mật khẩu hiển thị rõ và nhãn thứ nhất là “Username” dù backend xác thực bằng email.",
        root=[
            dict(path="frontend-web/src/pages/Login.jsx", start=28, end=45,
                 note="Hai input đều khai báo `type=\"text\"`; label không phải “Email”."),
        ],
        fix="Đổi input email sang `type=\"email\"`, input mật khẩu sang `type=\"password\"` và đổi nhãn thành “Email”.",
    ),
    dict(
        id="BUG-GUI-09", severity="Major", priority="High",
        fr="FR-22 — Form", ia="IA-02", screen="/login, /register, /forgot-password, /profile",
        title="Input không có label liên kết bằng chương trình",
        checks=["CHK-19", "CHK-32"],
        shots=["CHK-17-18-19-login-fields.png", "CHK-32-profile-labels.png"],
        steps=[
            "Mở từng màn hình auth.",
            "Kiểm tra `label[for]`, `input#id` và `aria-label`; hoặc chạy axe-core.",
        ],
        expected="Mọi input có accessible name từ `label[for]`, `aria-label` hoặc `aria-labelledby`.",
        actual="Không label nào có `for`, không input nào có `id`/`aria-label`; axe-core báo critical “label” violation trên cả bốn màn hình.",
        root=[
            dict(path="frontend-web/src/pages/Login.jsx", start=28, end=45,
                 note="Label là text thuần, không có `htmlFor`; input không có `id`."),
            dict(path="frontend-web/src/pages/Register.jsx", start=36, end=66,
                 note="Cùng pattern ở cả ba trường Register."),
            dict(path="frontend-web/src/pages/ForgotPassword.jsx", start=48, end=86,
                 note="Cùng pattern ở bước 1 và bước 2."),
            dict(path="frontend-web/src/pages/Profile.jsx", start=116, end=155,
                 note="Bốn label của Profile đều thiếu `htmlFor`/`id`."),
        ],
        fix="Thêm `id` cho từng input và `htmlFor` cho label tương ứng; dùng `aria-label` cho control icon-only.",
    ),
    dict(
        id="BUG-GUI-10", severity="Major", priority="High",
        fr="FR-01 — Đăng ký; FR-03 — Quên mật khẩu", ia="IA-02, IA-04", screen="/register, /forgot-password",
        title="Không kiểm tra định dạng email và không chặn email trùng",
        checks=["CHK-21", "CHK-25", "CHK-54"],
        shots=["CHK-21-register-invalid-email.png", "CHK-25-forgot-email-type.png", "CHK-54-register-duplicate-email.png"],
        steps=[
            "Đăng ký với email `not-an-email-<timestamp>`.",
            "Đăng ký cùng một email hợp lệ hai lần.",
            "Yêu cầu OTP với email sai định dạng.",
        ],
        expected="Email sai định dạng bị chặn ngay trên form; email trùng trả về thông báo conflict dễ hiểu (FR-01).",
        actual="Email sai định dạng được chấp nhận và chuyển về `/login`; đăng ký trùng email cũng thành công, không báo lỗi. Backend không có unique constraint trên `email`.",
        root=[
            dict(path="frontend-web/src/pages/Register.jsx", start=47, end=53,
                 note="Input email dùng `type=\"text\"`; không có kiểm tra format trước khi POST."),
            dict(path="frontend-web/src/pages/ForgotPassword.jsx", start=49, end=55,
                 note="Input email dùng `type=\"text\"`; lỗi format chỉ lộ ra từ backend sau submit."),
            dict(path="backend/server.js", start=20, end=30,
                 note="`/api/register` INSERT thẳng, không validate email và không bắt lỗi unique."),
            dict(path="backend/database.js", start=50, end=61,
                 note="Cột `email` không có ràng buộc `UNIQUE`."),
        ],
        fix="Dùng `type=\"email\"` và kiểm tra format; thêm `UNIQUE(email)` và trả HTTP 409 với thông báo thân thiện.",
    ),
    dict(
        id="BUG-GUI-11", severity="Major", priority="High",
        fr="FR-01 — Đăng ký; FR-03 — Đặt lại mật khẩu", ia="IA-02", screen="/register, /forgot-password",
        title="Nội dung mô tả password rule mâu thuẫn với regex thực tế",
        checks=["CHK-23"], shots=["CHK-23-register-password-rule.png"],
        steps=[
            "Mở `/register`.",
            "Nhập `Abcd1234!` (chữ hoa, chữ thường, số, ký tự đặc biệt, 9 ký tự) và submit.",
        ],
        expected="Mật khẩu được chấp nhận vì copy nói cần ký tự đặc biệt (FR-01).",
        actual="Mật khẩu bị từ chối. Regex yêu cầu whitespace `(?=.*\\s)` và character class `[A-Za-z\\d\\s]` chặn ký tự đặc biệt. Cùng regex được dùng ở màn hình reset.",
        root=[
            dict(path="frontend-web/src/pages/Register.jsx", start=15, end=18,
                 note="Regex yêu cầu `\\s` và chỉ cho phép chữ, số, whitespace."),
            dict(path="frontend-web/src/pages/ForgotPassword.jsx", start=26, end=29,
                 note="Copy regex y nguyên sang màn hình đặt lại mật khẩu."),
        ],
        fix="Thay bằng regex đúng (ví dụ `/^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[^A-Za-z0-9])\\S{8,}$/`) và giữ copy đồng bộ.",
    ),
    dict(
        id="BUG-GUI-12", severity="Minor", priority="Medium",
        fr="FR-01 — Đăng ký; FR-03 — Đặt lại mật khẩu", ia="IA-02", screen="/register, /forgot-password",
        title="Form đăng ký và đặt lại mật khẩu thiếu trường xác nhận mật khẩu",
        checks=["CHK-24", "CHK-28"], shots=["CHK-24-register-no-confirm.png", "CHK-28-forgot-no-confirm.png"],
        steps=[
            "Mở `/register` và bước 2 của `/forgot-password`.",
            "Đếm số input mật khẩu trên mỗi form.",
        ],
        expected="Có trường xác nhận mật khẩu và chặn khi hai trường không khớp (FR-01, FR-03).",
        actual="Mỗi form chỉ có một input mật khẩu; lỗi gõ nhầm không được phát hiện trước khi tạo tài khoản hoặc đổi mật khẩu.",
        root=[
            dict(path="frontend-web/src/pages/Register.jsx", start=55, end=67,
                 note="Chỉ có một input `Mật khẩu`."),
            dict(path="frontend-web/src/pages/ForgotPassword.jsx", start=78, end=87,
                 note="Chỉ có một input `Mật khẩu mới`."),
        ],
        fix="Thêm input xác nhận mật khẩu và kiểm tra khớp trước khi submit.",
    ),
    dict(
        id="BUG-GUI-13", severity="Major", priority="High",
        fr="FR-03 — Quên mật khẩu; FR-22 — Form", ia="IA-02, IA-03", screen="/forgot-password",
        title="OTP chỉ có 4 chữ số, input không giới hạn và bước 2 thiếu step indicator",
        checks=["CHK-26", "CHK-44"], shots=["CHK-26-forgot-otp-input.png", "CHK-44-forgot-step-indicator.png"],
        steps=[
            "Mở `/forgot-password`, nhập email đã đăng ký và lấy OTP.",
            "Đọc độ dài OTP, kiểm tra `maxlength`/`inputmode`/`pattern` của input và tìm step indicator.",
        ],
        expected="OTP 6 chữ số (FR-03, SEC-07); input giới hạn đúng 6 chữ số; có chỉ báo “Bước 1/2”, “Bước 2/2” (FR-03, FR-22).",
        actual="Backend sinh OTP 4 chữ số (`1000`–`9999`); label ghi “Mã OTP (4 số)”; input là `type=\"text\"`, không `maxlength`, `inputmode` hay `pattern`; không có step indicator.",
        root=[
            dict(path="backend/server.js", start=72, end=72,
                 note="`Math.floor(1000 + Math.random() * 9000)` chỉ sinh 4 chữ số."),
            dict(path="frontend-web/src/pages/ForgotPassword.jsx", start=63, end=96,
                 note="Label ghi “4 số”; input không có ràng buộc; không render step indicator."),
        ],
        fix="Sinh OTP 6 chữ số, dùng `inputmode=\"numeric\"`, `maxLength=6`, `pattern=\"[0-9]{6}\"` và thêm indicator “Bước 1/2”/“Bước 2/2”.",
    ),
    dict(
        id="BUG-GUI-14", severity="Blocker", priority="High",
        fr="FR-04 — Hồ sơ cá nhân", ia="IA-02", screen="/profile",
        title="Regex số điện thoại từ chối số Việt Nam hợp lệ và dùng alert chặn",
        checks=["CHK-31"], shots=["CHK-31-profile-phone-alert.png"],
        steps=[
            "Đăng nhập và mở `/profile`.",
            "Nhập số `0912345678` (đúng placeholder) và bấm “Cập nhật”.",
        ],
        expected="Số bắt đầu bằng `0`, dài 10–11 chữ số được chấp nhận và lưu hồ sơ (FR-04).",
        actual="Alert “Số điện thoại không hợp lệ...” hiện ra. Regex `/^[1-9][0-9]{8,9}$/` từ chối mọi số bắt đầu bằng `0`, gồm cả placeholder `0912345678`; lỗi dùng `alert()` thay vì inline.",
        root=[
            dict(path="frontend-web/src/pages/Profile.jsx", start=40, end=46,
                 note="Regex bắt đầu bằng `[1-9]` và dùng `alert()`."),
        ],
        fix="Dùng `/^0\\d{9,10}$/` (hoặc thư viện validate), thêm `inputmode=\"tel\"` và hiển thị lỗi inline.",
    ),
    dict(
        id="BUG-GUI-16", severity="Major", priority="High",
        fr="FR-21 — Tiêu chuẩn giao diện chung", ia="IA-03", screen="/login",
        title="Tab order bắt đầu ở nút Sign In vì `tabIndex=1`",
        checks=["CHK-36"], shots=["CHK-36-login-tab-order.png"],
        steps=[
            "Mở `/login`.",
            "Focus vào body và bấm Tab một lần; ghi lại phần tử được focus.",
        ],
        expected="Tab đầu tiên vào ô email, sau đó mật khẩu, link quên mật khẩu, nút submit, link đăng ký.",
        actual="Tab đầu tiên focus vào nút “Sign In” vì nút có `tabIndex={1}`; người dùng bàn phím bỏ qua hai ô nhập và thứ tự thị giác bị đảo.",
        root=[
            dict(path="frontend-web/src/pages/Login.jsx", start=53, end=59,
                 note="`tabIndex={1}` trên button submit."),
        ],
        fix="Bỏ `tabIndex`; để DOM order quyết định tab order.",
    ),
    dict(
        id="BUG-GUI-17", severity="Minor", priority="Medium",
        fr="FR-03 — Quên mật khẩu", ia="IA-03", screen="/forgot-password",
        title="Focus bị mất sau khi chuyển sang bước OTP",
        checks=["CHK-43"], shots=["CHK-43-forgot-focus.png"],
        steps=[
            "Yêu cầu OTP thành công.",
            "Kiểm tra `document.activeElement` sau khi bước 2 render.",
        ],
        expected="Focus chuyển tới ô OTP hoặc heading bước 2 và thay đổi được announce.",
        actual="`document.activeElement` là `BODY`; người dùng screen-reader/bàn phím không biết bước đã đổi.",
        root=[
            dict(path="frontend-web/src/pages/ForgotPassword.jsx", start=13, end=22,
                 note="`setStep(2)` không kèm focus management."),
        ],
        fix="Dùng `useEffect` để focus heading/input bước 2 và thêm `aria-live` cho status message.",
    ),
    dict(
        id="BUG-GUI-19", severity="Minor", priority="Medium",
        fr="FR-23 — Navigation", ia="IA-03", screen="/profile",
        title="Navbar không chỉ ra trang hiện tại",
        checks=["CHK-48"], shots=["CHK-48-profile-active-nav.png"],
        steps=[
            "Đăng nhập và mở `/profile`.",
            "Kiểm tra `aria-current`, class active hoặc underline trên các link header.",
        ],
        expected="Trang hiện tại được chỉ ra bằng visual state và `aria-current=\"page\"` (FR-23).",
        actual="Chỉ có hover style; không có `aria-current`, active class hay underline cho `/profile`.",
        root=[
            dict(path="frontend-web/src/App.jsx", start=20, end=38,
                 note="Header dùng `<Link>` thường, không dùng `<NavLink>` và không có active style."),
        ],
        fix="Dùng `<NavLink>` với `aria-current=\"page\"` và class active.",
    ),
    dict(
        id="BUG-GUI-20", severity="Minor", priority="Medium",
        fr="FR-01 — Đăng ký; FR-02 — Đăng nhập", ia="IA-04", screen="/login, /register",
        title="Nút Login và Register không có loading/disabled state",
        checks=["CHK-49", "CHK-56"], shots=["CHK-49-login-loading.png", "CHK-56-register-loading.png"],
        steps=[
            "Delay `/api/login` hoặc `/api/register` khoảng 2 giây.",
            "Bấm submit và quan sát nút trong lúc request đang chạy.",
        ],
        expected="Nút bị disable, có spinner hoặc đổi label và expose `aria-busy`.",
        actual="Nút vẫn enabled và giữ nguyên label; người dùng có thể submit lặp và không biết request đang chạy.",
        root=[
            dict(path="frontend-web/src/pages/Login.jsx", start=12, end=20,
                 note="Không có state `submitting`; button không bị disable."),
            dict(path="frontend-web/src/pages/Register.jsx", start=12, end=28,
                 note="Cùng pattern ở Register."),
        ],
        fix="Thêm state `submitting`, disable button và hiển thị spinner/“Đang xử lý…”, kèm `aria-busy`.",
    ),
    dict(
        id="BUG-GUI-21", severity="Major", priority="High",
        fr="FR-22 — Form; FR-24 — Feedback", ia="IA-04", screen="/login, /forgot-password",
        title="Thông báo lỗi nằm dưới nút submit hoặc dùng alert chặn",
        checks=["CHK-50", "CHK-59", "CHK-75"],
        shots=["CHK-50-login-error.png", "CHK-59-forgot-alert.png", "CHK-75-error-position.png"],
        steps=[
            "Nhập sai mật khẩu trên `/login` và submit.",
            "Yêu cầu OTP cho email không tồn tại trên `/forgot-password`.",
        ],
        expected="Lỗi hiển thị inline, nằm trên nút submit, gắn với field và được announce qua `role=\"alert\"`/`aria-live` (FR-22).",
        actual="Login render error div sau `</form>`, bên dưới nút “Sign In”, không có `role`/`aria-live`; Forgot Password dùng `alert(\"Lỗi: User not found\")`, không có inline message hay field highlight.",
        root=[
            dict(path="frontend-web/src/pages/Login.jsx", start=61, end=66,
                 note="Error div nằm ngoài `<form>`, sau nút submit."),
            dict(path="frontend-web/src/pages/ForgotPassword.jsx", start=19, end=21,
                 note="Dùng `alert()` cho lỗi request OTP."),
            dict(path="frontend-web/src/pages/ForgotPassword.jsx", start=36, end=38,
                 note="Dùng `alert()` cho lỗi reset."),
        ],
        fix="Tạo inline error region phía trên nút submit, dùng `role=\"alert\"`/`aria-live`, `aria-invalid` và `aria-describedby` trên field.",
    ),
    dict(
        id="BUG-GUI-23", severity="Major", priority="High",
        fr="FR-01 — Đăng ký; FR-24 — Feedback", ia="IA-04", screen="/register",
        title="UI render nguyên văn lỗi kỹ thuật từ server",
        checks=["CHK-55"], shots=["CHK-55-register-raw-error.png"],
        steps=[
            "Giả lập `POST /api/register` trả 500 với body chứa lỗi SQLite.",
            "Submit form đăng ký.",
        ],
        expected="Thông báo lỗi thân thiện, generic; chi tiết kỹ thuật chỉ nằm trong log server.",
        actual="UI hiển thị “SQLITE_ERROR: no such column: name” vì catch block dùng trực tiếp `err.response.data.error`.",
        root=[
            dict(path="frontend-web/src/pages/Register.jsx", start=25, end=27,
                 note="Render `err.response?.data?.error` trực tiếp ra UI."),
        ],
        fix="Map lỗi đã biết sang message thân thiện; log raw error ở server; không render database message.",
    ),
    dict(
        id="BUG-GUI-25", severity="Major", priority="High",
        fr="FR-04 — Hồ sơ cá nhân; FR-24 — Feedback", ia="IA-04", screen="/profile",
        title="Loading và lỗi tải đơn hàng đều hiển thị thành “chưa có đơn hàng”",
        checks=["CHK-62", "CHK-63"], shots=["CHK-62-profile-orders-loading.png", "CHK-63-profile-orders-error.png"],
        steps=[
            "Delay `/api/orders/my-orders` rồi mở `/profile`.",
            "Lặp lại với response 500.",
        ],
        expected="Có loading state khi đang fetch và error state riêng (kèm retry) khi request thất bại.",
        actual="“Bạn chưa có đơn hàng nào.” hiện ngay trong lúc loading và sau response 500; người dùng không phân biệt được “chưa có đơn” với “tải thất bại”.",
        root=[
            dict(path="frontend-web/src/pages/Profile.jsx", start=14, end=29,
                 note="`catch` đặt `orders=[]`; không có state loading/error."),
            dict(path="frontend-web/src/pages/Profile.jsx", start=168, end=169,
                 note="Chỉ có một nhánh empty state cho mọi trường hợp."),
        ],
        fix="Thêm state `loading`/`error`, render ba nhánh riêng và nút retry.",
    ),
    dict(
        id="BUG-GUI-27", severity="Minor", priority="Medium",
        fr="FR-22 — Form", ia="IA-02", screen="/login, /register, /forgot-password, /profile",
        title="Không có ký hiệu `*` cạnh nhãn trường bắt buộc",
        checks=["CHK-70"], shots=["CHK-70-required-asterisk.png"],
        steps=[
            "Mở các màn hình auth.",
            "So sánh nhãn với thuộc tính `required` của từng input.",
        ],
        expected="Mọi trường bắt buộc có ký hiệu `*` bên cạnh nhãn (FR-22).",
        actual="Không nhãn nào có `*` dù tất cả input đều `required`.",
        root=[
            dict(path="frontend-web/src/pages/Register.jsx", start=36, end=56,
                 note="Label “Họ Tên”, “Email”, “Mật khẩu” không có `*`; input đều `required`."),
            dict(path="frontend-web/src/pages/Login.jsx", start=28, end=38,
                 note="Label “Username”, “Mật khẩu” không có `*`."),
        ],
        fix="Thêm `*` (kèm text ẩn “bắt buộc” cho screen-reader) vào mọi label của trường required.",
    ),
    dict(
        id="BUG-GUI-28", severity="Minor", priority="Medium",
        fr="FR-21 — Tiêu chuẩn giao diện chung", ia="IA-01", screen="/login",
        title="Login dùng “Username” và “Sign In” giữa giao diện tiếng Việt",
        checks=["CHK-71"], shots=["CHK-71-login-language.png"],
        steps=[
            "Mở `/login`.",
            "Đọc nhãn trường và nút submit; so sánh với các màn hình còn lại.",
        ],
        expected="Toàn bộ giao diện dùng tiếng Việt, trừ thuật ngữ kỹ thuật chuẩn (FR-21).",
        actual="Nhãn “Username” và nút “Sign In” là tiếng Anh không cần thiết; các màn hình khác dùng tiếng Việt.",
        root=[
            dict(path="frontend-web/src/pages/Login.jsx", start=28, end=28,
                 note="Label “Username”."),
            dict(path="frontend-web/src/pages/Login.jsx", start=58, end=58,
                 note="Nút “Sign In”."),
        ],
        fix="Đổi thành “Email” và “Đăng nhập”.",
    ),
    dict(
        id="BUG-GUI-29", severity="Minor", priority="Medium",
        fr="FR-23 — Navigation", ia="IA-03", screen="/profile",
        title="Nút đăng xuất có nhãn “Thoát” thay vì “Đăng xuất”",
        checks=["CHK-47"], shots=["CHK-47-logout-label.png"],
        steps=[
            "Đăng nhập và quan sát header.",
            "Đọc nhãn nút đăng xuất.",
        ],
        expected="Nhãn là “Đăng xuất” (FR-23).",
        actual="Nhãn là “Thoát”.",
        root=[
            dict(path="frontend-web/src/App.jsx", start=29, end=29,
                 note="Button logout hard-code “Thoát”."),
        ],
        fix="Đổi nhãn thành “Đăng xuất”.",
    ),
    dict(
        id="BUG-GUI-30", severity="Minor", priority="Low",
        fr="FR-24 — Feedback & State", ia="IA-04", screen="/profile",
        title="Empty state lịch sử đơn hàng không có icon/hình minh họa",
        checks=["CHK-73"], shots=["CHK-73-empty-state.png"],
        steps=[
            "Đăng nhập bằng tài khoản chưa có đơn hàng.",
            "Mở `/profile` và quan sát section “Lịch sử đơn hàng”.",
        ],
        expected="Empty state có icon/hình minh họa và message thân thiện (FR-24).",
        actual="Chỉ có `<p>Bạn chưa có đơn hàng nào.</p>`; không icon, hình minh họa hay hướng dẫn tiếp theo.",
        root=[
            dict(path="frontend-web/src/pages/Profile.jsx", start=168, end=169,
                 note="Nhánh empty state chỉ render một đoạn text."),
        ],
        fix="Thêm icon/illustration và message thân thiện, ví dụ “Bạn chưa có đơn hàng nào. Hãy bắt đầu mua sắm!”.",
    ),
    dict(
        id="BUG-GUI-31", severity="Minor", priority="Medium",
        fr="FR-21 — Tiêu chuẩn giao diện chung", ia="IA-01", screen="/register, /forgot-password",
        title="Nút hành động tích cực dùng màu đỏ/xanh lá thay vì xanh dương",
        checks=["CHK-74"], shots=["CHK-74-button-color.png", "CHK-74-forgot-button-color.png"],
        steps=[
            "Mở `/register` và quan sát nút “Đăng Ký”.",
            "Lấy OTP trên `/forgot-password` và quan sát hai nút ở bước 2.",
        ],
        expected="Nút hành động tích cực dùng màu xanh dương (FR-21).",
        actual="Register dùng `bg-red-500` (#ef4444); bước 2 Forgot dùng `bg-green-600` cho cả “Đặt lại mật khẩu” và “← Quay lại”; Login, Forgot bước 1 và Profile dùng xanh dương.",
        root=[
            dict(path="frontend-web/src/pages/Register.jsx", start=70, end=75,
                 note="Nút submit dùng `bg-red-500`."),
            dict(path="frontend-web/src/pages/ForgotPassword.jsx", start=90, end=95,
                 note="Hai nút dùng `bg-green-600`."),
        ],
        fix="Đổi primary action sang `bg-blue-600`; dùng đỏ chỉ cho hành động nguy hiểm/hủy.",
    ),
    dict(
        id="BUG-GUI-32", severity="Minor", priority="Medium",
        fr="FR-23 — Navigation", ia="IA-03", screen="/login, /register, /forgot-password, /profile",
        title="Link “Giỏ hàng” trên header không có badge số lượng",
        checks=["CHK-80"], shots=["CHK-80-cart-badge.png"],
        steps=[
            "Mở bất kỳ màn hình auth nào.",
            "Quan sát link “Giỏ hàng” trên header.",
        ],
        expected="Link “Giỏ hàng” hiển thị badge số lượng sản phẩm (FR-23).",
        actual="Header chỉ có text “Giỏ hàng”; không có badge hay số lượng cạnh link.",
        root=[
            dict(path="frontend-web/src/App.jsx", start=22, end=23,
                 note="Link cart chỉ render text, không dùng `cart.length` để hiển thị badge."),
        ],
        fix="Đọc `cart` từ `useCart()` và render badge số lượng cạnh link “Giỏ hàng”.",
    ),
]


def rel_shot(name):
    return f"../screenshots/{name}"


def raw_shot(name):
    return f"{RAW}/screenshots/{name}"


def bug_md(b):
    lines = []
    lines.append(f"# {b['id']} — {b['title']}\n")
    lines.append(f"**GitHub Issue:** chưa publish — draft tại [`issues/{b['id']}.md`](../issues/{b['id']}.md)\n")
    lines.append("## Tóm tắt\n")
    lines.append(
        f"{b['title']}. Bug được phát hiện khi thực thi checklist GUI Task 1 trên màn hình `{b['screen']}`."
    )
    lines.append("\n| Mục | Giá trị |")
    lines.append("| --- | --- |")
    lines.append(f"| Feature / rule | {b['fr']} |")
    lines.append(f"| Checklist | {', '.join(b['checks'])} |")
    lines.append(f"| Màn hình | `{b['screen']}` |")
    lines.append(f"| Môi trường | {ENV} |")
    lines.append(f"| Severity / Priority | **{b['severity']}** / {b['priority']} |")
    lines.append("| Lặp lại | 1/1 trên build hiện tại |")
    lines.append("\n## Các bước tái hiện\n")
    for n, s in enumerate(b["steps"], 1):
        lines.append(f"{n}. {s}")
    lines.append("\n| Mốc | Expected | Actual |")
    lines.append("| --- | --- | --- |")
    lines.append(f"| Sau thao tác | {b['expected']} | {b['actual']} |")
    lines.append("\n## Bằng chứng\n")
    for s in b["shots"]:
        lines.append(f"![{b['id']} — {s}]({rel_shot(s)})\n")
    lines.append("## Nguyên nhân đối chiếu mã nguồn\n")
    lines.append(root_section(b["root"]))
    lines.append("\n## Đề xuất sửa\n")
    lines.append(b["fix"])
    lines.append("\n## Ghi chú\n")
    lines.append(
        "Screenshot được chụp trên SUT đang chạy tại `http://localhost:5173`; "
        "code block lấy trực tiếp từ source tại commit "
        f"[`{COMMIT[:7]}`]({BLOB})."
    )
    return "\n".join(lines) + "\n"


def issue_md(b):
    lines = []
    lines.append(f"# [{b['id']}] {b['title']}\n")
    lines.append(f"**Severity:** {b['severity']} · **Priority:** {b['priority']} · **FR:** {b['fr']} · **Screen:** `{b['screen']}`\n")
    lines.append("## Mô tả\n")
    lines.append(b["actual"])
    lines.append("\n## Các bước tái hiện\n")
    for n, s in enumerate(b["steps"], 1):
        lines.append(f"{n}. {s}")
    lines.append("\n## Expected\n")
    lines.append(b["expected"])
    lines.append("\n## Actual\n")
    lines.append(b["actual"])
    lines.append("\n## Checklist IDs\n")
    lines.append(", ".join(b["checks"]))
    lines.append("\n## Nguyên nhân\n")
    lines.append(root_section(b["root"]))
    lines.append("\n## Đề xuất sửa\n")
    lines.append(b["fix"])
    lines.append("\n## Screenshots\n")
    for s in b["shots"]:
        lines.append(f"![{b['id']}]({raw_shot(s)})\n")
    lines.append(
        f"\n> Screenshot dùng raw URL trên nhánh `{BRANCH}`; cần push nhánh này trước khi publish issue."
    )
    return "\n".join(lines) + "\n"


# ---- dọn file cũ để không còn bug/issue ngoài bộ hiện tại ----
for f in glob.glob(os.path.join(BUGS_DIR, "BUG-GUI-*.md")):
    os.remove(f)
for f in glob.glob(os.path.join(ISSUES_DIR, "BUG-GUI-*.md")):
    os.remove(f)

for b in B:
    with open(os.path.join(BUGS_DIR, f"{b['id']}.md"), "w", encoding="utf-8") as f:
        f.write(bug_md(b))
    with open(os.path.join(ISSUES_DIR, f"{b['id']}.md"), "w", encoding="utf-8") as f:
        f.write(issue_md(b))

# ---- bug-report.md ----
sev_order = {"Blocker": 0, "Major": 1, "Minor": 2}
bugs = sorted(B, key=lambda b: (sev_order[b["severity"]], b["id"]))
counts = {s: sum(1 for b in B if b["severity"] == s) for s in ["Blocker", "Major", "Minor"]}
lines = ["# Bug report — HW03 Task 1 (GUI checklist)\n",
         f"**Tổng số bug:** {len(B)} · **Blocker:** {counts['Blocker']} · **Major:** {counts['Major']} · **Minor:** {counts['Minor']}\n",
         "Mỗi bug có báo cáo riêng trong [`bugs/`](bugs/) với bước tái hiện, Expected/Actual, screenshot và root cause kèm code block + link tới đúng dòng source.\n",
         "| ID | Severity | FR | Màn hình | Checklist | Tiêu đề | Bug report |",
         "| --- | --- | --- | --- | --- | --- | --- |"]
for b in bugs:
    lines.append(
        f"| {b['id']} | **{b['severity']}** | {b['fr'].split(' — ')[0]} | `{b['screen']}` | "
        f"{', '.join(b['checks'])} | {b['title']} | [chi tiết](bugs/{b['id']}.md) |"
    )
lines.append("\n## Ghi chú\n")
lines.append("- Screenshot chỉ tồn tại cho các item Failed; mỗi ảnh có banner đỏ ghi checklist ID và lỗi quan sát.")
lines.append("- GitHub Issues chưa publish vì môi trường không có `gh` CLI/token; 26 issue draft nằm trong [`issues/`](issues/).")
lines.append("- Severity: **Blocker** = không thể hoàn thành tác vụ chính; **Major** = sai requirement rõ ràng hoặc cản trở đáng kể; **Minor** = lỗi hiển thị/nhất quán.")
with open(os.path.join(OUT, "bug-report.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

# ---- issues.json + publish.sh ----
issues = []
for b in bugs:
    issues.append({
        "id": b["id"], "title": f"[{b['id']}] {b['title']}",
        "severity": b["severity"], "priority": b["priority"],
        "fr": b["fr"], "screen": b["screen"], "checks": b["checks"],
        "labels": ["bug", b["severity"].lower(), b["ia"].lower()],
        "body_file": f"{b['id']}.md",
    })
with open(os.path.join(ISSUES_DIR, "issues.json"), "w", encoding="utf-8") as f:
    json.dump(issues, f, ensure_ascii=False, indent=2)

publish = ["#!/usr/bin/env bash",
           "set -euo pipefail",
           "# Publish 26 issue drafts. Yêu cầu: gh auth login và đã push nhánh ncuong (để raw screenshot URL hoạt động).",
           'cd "$(dirname "$0")"',
           'command -v gh >/dev/null || { echo "gh CLI chưa cài; cài gh rồi chạy lại."; exit 1; }',
           "gh auth status >/dev/null || { echo \"Chưa đăng nhập gh; chạy 'gh auth login'.\"; exit 1; }",
           ""]
for i in issues:
    publish.append(
        f'gh issue create --title {json.dumps(i["title"], ensure_ascii=False)} '
        f'--body-file {i["body_file"]} --label bug'
        + "".join(f' --label {l}' for l in i["labels"][1:])
    )
with open(os.path.join(ISSUES_DIR, "publish.sh"), "w", encoding="utf-8") as f:
    f.write("\n".join(publish) + "\n")

print(f"bugs={len(B)} blocker={counts['Blocker']} major={counts['Major']} minor={counts['Minor']}")
print("wrote", len(B), "bug reports and", len(B), "issue drafts")
