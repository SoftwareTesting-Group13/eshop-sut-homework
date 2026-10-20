#!/usr/bin/env node
/**
 * FR17 — Coupon management (CRUD)
 * Domain/EP + BVA execution driver.
 *
 * Design oracle: README.md §5 FR-17 + api_specification.md §5/§6.4.
 * The driver only records observed behavior; it never edits the SUT.
 *
 * Run from the repository root:
 *   node homework/hw02/ncuong/features/FR17/evidence/run-fr17.mjs
 *
 * The SUT is expected on http://localhost:3000 and must use an isolated
 * copy of backend/database.sqlite (FR17_SUT_DIR).
 */

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const EVIDENCE_DIR = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = process.env.FR17_REPO_ROOT || process.cwd();
const SUT_DIR =
  process.env.FR17_SUT_DIR ||
  "/private/var/folders/2f/64j8q4t10vz15mrnyzk48_j80000gn/T/opencode/fr17-sut";
const BASE = "http://localhost:3000";
const RUN_ID = "run-20261020-fr17";
const ADMIN_EMAIL = "admin@eshop.com";
const ADMIN_PASSWORD = "Admin123!";
const USER_EMAIL = "test@eshop.com";
const USER_PASSWORD = "Test1234!";

const results = [];
const outOfScope = [];
let evSeq = 0;
let startedAt;
let finishAt;

function sha256File(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

function exists(file) {
  try {
    return fs.existsSync(file);
  } catch {
    return false;
  }
}

function localTime(date = new Date()) {
  const iso = date.toISOString();
  const local = new Intl.DateTimeFormat("sv-SE", {
    timeZone: "Asia/Ho_Chi_Minh",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(date);
  return `${iso} (${local} +0700)`;
}

function redactAuth(token) {
  return token ? "Authorization: Bearer <redacted-test-token>" : "Authorization: (none)";
}

async function api(method, endpoint, body, token) {
  const headers = {};
  if (token) headers.Authorization = `Bearer ${token}`;
  let payload;
  if (body !== undefined) {
    headers["Content-Type"] = "application/json";
    payload = JSON.stringify(body);
  }
  const started = Date.now();
  const response = await fetch(BASE + endpoint, { method, headers, body: payload });
  const text = await response.text();
  let json = null;
  try {
    json = JSON.parse(text);
  } catch {
    json = null;
  }
  return {
    method,
    endpoint,
    status: response.status,
    ok: response.ok,
    body: json,
    text,
    ms: Date.now() - started,
    requestBody: body,
  };
}

async function login(email, password) {
  const response = await api("POST", "/api/login", { email, password });
  if (response.status !== 200 || !response.body || !response.body.token) {
    throw new Error(
      `Login failed for ${email}: HTTP ${response.status} ${response.text}`,
    );
  }
  return {
    token: response.body.token,
    user: response.body.user,
    response,
  };
}

async function listCoupons(token) {
  const response = await api("GET", "/api/coupons", undefined, token);
  if (response.status !== 200 || !Array.isArray(response.body)) {
    throw new Error(
      `GET /api/coupons failed: HTTP ${response.status} ${response.text}`,
    );
  }
  return { rows: response.body, response };
}

async function deleteCoupon(id, token) {
  return api("DELETE", `/api/admin/coupons/${id}`, undefined, token);
}

function rowMatches(row, expected) {
  const checks = [];
  for (const [field, expectedValue] of Object.entries(expected)) {
    const actualValue = row ? row[field] : undefined;
    let pass;
    if (typeof expectedValue === "number") {
      pass = Number(actualValue) === expectedValue;
    } else {
      pass = String(actualValue) === String(expectedValue);
    }
    checks.push({ field, expected: expectedValue, actual: actualValue, pass });
  }
  return { pass: checks.every((check) => check.pass), checks };
}

function summarizeRows(rows) {
  return rows.map((row) => ({
    id: row.id,
    code: row.code,
    type: row.type,
    discount_value: row.discount_value,
    min_order_amount: row.min_order_amount,
    expired_at: row.expired_at,
    max_uses_per_user: row.max_uses_per_user,
    is_active: row.is_active,
  }));
}

function nextEvId() {
  evSeq += 1;
  return `EV-FR17-${String(evSeq).padStart(3, "0")}`;
}

function writeCaseLog(item) {
  const lines = [];
  lines.push(`# ${item.evId} — ${item.id} (${item.interface})`);
  lines.push("");
  lines.push("| Trường | Giá trị |");
  lines.push("| --- | --- |");
  lines.push(`| Test case | ${item.id} |`);
  lines.push(`| Run ID / lần thử | ${RUN_ID} / 1 |`);
  lines.push(`| Kỹ thuật | ${item.technique} |`);
  lines.push(`| Obligation IDs | ${item.obligations.join(", ")} |`);
  lines.push(`| Thời điểm | ${item.timestamp} |`);
  lines.push(`| Interface | ${item.interface} |`);
  lines.push(`| Setup / trạng thái trước | ${item.setup} |`);
  lines.push("");
  lines.push("## Thao tác / request thật");
  lines.push("");
  lines.push("```http");
  lines.push(`${item.request.method} ${item.request.endpoint}`);
  lines.push(redactAuth(true));
  lines.push("Content-Type: application/json");
  lines.push("");
  lines.push(
    item.request.requestBody === undefined
      ? "(no body)"
      : JSON.stringify(item.request.requestBody, null, 2),
  );
  lines.push("```");
  lines.push("");
  lines.push("## Kết quả thô");
  lines.push("");
  lines.push("```json");
  lines.push(`HTTP ${item.request.status}`);
  lines.push(JSON.stringify(item.request.body, null, 2));
  lines.push("```");
  lines.push("");
  lines.push("### Kiểm tra trạng thái qua GET /api/coupons");
  lines.push("");
  lines.push("```json");
  lines.push(
    JSON.stringify(
      {
        before_count: item.verification.before_count,
        after_count: item.verification.after_count,
        new_rows: item.verification.new_rows,
        target_row: item.verification.target_row,
        field_checks: item.verification.field_checks,
        seeds_present: item.verification.seeds_present,
        absent_after_delete: item.verification.absent_after_delete,
      },
      null,
      2,
    ),
  );
  lines.push("```");
  lines.push("");
  lines.push(`- **Expected (oracle ref):** ${item.oracle}`);
  lines.push(`- **Actual:** ${item.actual}`);
  lines.push(`- **Status:** \`${item.verdict}\``);
  lines.push(`- **Artifact:** \`evidence/${item.id}.log\``);
  lines.push(`- **Cleanup:** ${item.cleanup}`);
  lines.push(`- **Bug liên quan:** ${item.bugId || "không"}`);
  if (item.notes) lines.push(`- **Ghi chú:** ${item.notes}`);
  lines.push("");
  return lines.join("\n");
}

function record(item) {
  item.evId = nextEvId();
  item.timestamp = localTime();
  item.logFile = `${item.id}.log`;
  results.push(item);
  fs.writeFileSync(path.join(EVIDENCE_DIR, item.logFile), writeCaseLog(item));
  console.log(
    `${item.id} ${item.verdict.padEnd(12)} HTTP ${item.request.status} | ${item.actual}`,
  );
}

const bugMap = {
  "DT-04": "BUG-FR17-01",
  "DT-05": "BUG-FR17-01",
  "DT-06": "BUG-FR17-01",
  "DT-08": "BUG-FR17-02",
  "DT-09": "BUG-FR17-02",
  "DT-10": "BUG-FR17-03",
  "DT-11": "BUG-FR17-03",
  "DT-12": "BUG-FR17-03",
  "DT-13": "BUG-FR17-03",
  "DT-15": "BUG-FR17-04",
  "DT-16": "BUG-FR17-04",
  "DT-17": "BUG-FR17-04",
  "DT-21": "BUG-FR17-05",
  "DT-22": "BUG-FR17-05",
  "DT-23": "BUG-FR17-05",
  "DT-26": "BUG-FR17-06",
  "DT-27": "BUG-FR17-06",
  "DT-28": "BUG-FR17-06",
};

const validBase = {
  code: "FR17-DT-01",
  type: "percent",
  discount_value: 10,
  min_order_amount: 100000,
  expired_at: "2099-12-31",
  max_uses_per_user: 1,
};

function withCode(code, overrides = {}) {
  return { ...validBase, code, ...overrides };
}

function without(body, field) {
  const copy = { ...body };
  delete copy[field];
  return copy;
}

const createCases = [
  {
    id: "DT-01",
    technique: "EP",
    obligations: ["P1", "R1", "R2", "R3", "R4", "R5", "R6", "R7"],
    expected: "created",
    body: withCode("FR17-DT-01"),
    expectedFields: {
      code: "FR17-DT-01",
      type: "percent",
      discount_value: 10,
      min_order_amount: 100000,
      expired_at: "2099-12-31",
      max_uses_per_user: 1,
    },
    oracle:
      "Tạo thành công (2xx); coupon xuất hiện trong GET /api/coupons với đủ 6 trường đúng giá trị. Nguồn: README.md §5 FR-17; api_specification.md §6.4.",
    setup:
      "DB test mới seed 4 coupon (SAVE10, BIGBUY, VIP100, EXPIRED); đăng nhập admin@eshop.com; các trường khác giữ baseline hợp lệ.",
    notes: "Baseline percent; đồng thời kiểm tra persistence qua GET danh sách.",
  },
  {
    id: "DT-02",
    technique: "EP",
    obligations: ["P2", "R1", "R2", "R3", "R4", "R5", "R6", "R7"],
    expected: "created",
    body: withCode("FR17-DT-02", {
      type: "fixed",
      discount_value: 50000,
      min_order_amount: 200000,
    }),
    expectedFields: {
      code: "FR17-DT-02",
      type: "fixed",
      discount_value: 50000,
      min_order_amount: 200000,
      expired_at: "2099-12-31",
      max_uses_per_user: 1,
    },
    oracle:
      "Tạo thành công (2xx); coupon type=fixed xuất hiện trong GET /api/coupons với đủ 6 trường đúng giá trị. Nguồn: README.md §5 FR-17; api_specification.md §6.4.",
    setup:
      "DB test mới seed 4 coupon; đăng nhập admin; type=fixed, discount_value=50000, min_order_amount=200000.",
    notes: "Lớp hợp lệ của type=fixed.",
  },
  {
    id: "DT-03",
    technique: "EP",
    obligations: ["P3", "R2"],
    expected: "rejected",
    body: withCode("SAVE10"),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; code phải duy nhất. Nguồn: README.md §5 FR-17.",
    setup:
      "DB test có seed SAVE10; đăng nhập admin; gửi code trùng SAVE10 với các trường còn lại hợp lệ.",
    notes:
      "Đặc tả không quy định status/message cho trùng code; verdict chỉ dựa trên việc coupon không được tạo. Quan sát mã lỗi thô trong log.",
  },
  {
    id: "DT-04",
    technique: "EP",
    obligations: ["P4", "R2"],
    expected: "rejected",
    body: withCode(""),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; code là trường bắt buộc. Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; code = chuỗi rỗng; các trường còn lại hợp lệ.",
    notes: "UI có thuộc tính required nên không gửi được chuỗi rỗng qua form thông thường.",
  },
  {
    id: "DT-05",
    technique: "EP",
    obligations: ["P5", "R2"],
    expected: "rejected",
    body: without(withCode("FR17-DT-05"), "code"),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; code là trường bắt buộc. Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; bỏ hẳn key code khỏi JSON; các trường còn lại hợp lệ.",
    notes:
      "Khác với code rỗng: request không có key code. UI luôn gửi key code nên ca này API-only.",
  },
  {
    id: "DT-06",
    technique: "EP",
    obligations: ["P6", "R2"],
    expected: "rejected",
    body: withCode("   "),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; code chỉ gồm khoảng trắng không phải code hợp lệ (ASSUMED: cần trim trước khi kiểm tra bắt buộc). Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; code = ba khoảng trắng; các trường còn lại hợp lệ.",
    notes:
      "ASSUMED: đặc tả không nói rõ trim, nhưng code chỉ có khoảng trắng không thể là mã duy nhất có nghĩa. UI required không chặn chuỗi khoảng trắng.",
  },
  {
    id: "DT-07",
    technique: "EP",
    obligations: ["P7", "R2"],
    expected: "observation",
    body: withCode("save10"),
    oracle:
      "Chưa xác định — đặc tả chỉ nói code duy nhất, không nói uniqueness phân biệt hoa/thường. Đây là quan sát, không chấm PASS/FAIL.",
    setup:
      "DB test có seed SAVE10; đăng nhập admin; gửi code viết thường save10.",
    notes:
      "UI tự uppercase code nên không gửi được save10 qua form thông thường; ca này API-only. Nếu tạo được, ghi nhận hai mã cùng nghĩa khác hoa/thường.",
  },
  {
    id: "DT-08",
    technique: "EP",
    obligations: ["P8", "R3"],
    expected: "rejected",
    body: withCode("FR17-DT-08", { type: "percentage" }),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; type chỉ nhận percent/fixed. Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; type = percentage; các trường còn lại hợp lệ.",
    notes: "UI là select percent/fixed nên không gửi được type ngoài enum; ca này API-only.",
  },
  {
    id: "DT-09",
    technique: "EP",
    obligations: ["P9", "R3"],
    expected: "rejected",
    body: without(withCode("FR17-DT-09"), "type"),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; type là trường bắt buộc và chỉ nhận percent/fixed. Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; bỏ hẳn key type; các trường còn lại hợp lệ.",
    notes: "UI select luôn có giá trị nên ca này API-only.",
  },
  {
    id: "DT-10",
    technique: "EP + BVA",
    obligations: ["P10", "B3-ON", "R4"],
    expected: "rejected",
    body: withCode("FR17-DT-10", { discount_value: 0 }),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; discount_value phải dương (> 0). 0 là điểm biên ON phía invalid. Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; discount_value=0; các trường còn lại hợp lệ.",
    notes: "UI type=number không có min nên người dùng có thể nhập 0 và submit.",
  },
  {
    id: "DT-11",
    technique: "EP + BVA",
    obligations: ["P11", "B3-below", "R4"],
    expected: "rejected",
    body: withCode("FR17-DT-11", { discount_value: -1 }),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; discount_value phải dương. -1 là điểm ngay dưới biên 0. Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; discount_value=-1; các trường còn lại hợp lệ.",
    notes: "UI type=number không có min nên nhập được -1.",
  },
  {
    id: "DT-12",
    technique: "EP",
    obligations: ["P12", "R4"],
    expected: "rejected",
    body: without(withCode("FR17-DT-12"), "discount_value"),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; discount_value là trường bắt buộc. Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; bỏ hẳn key discount_value; các trường còn lại hợp lệ.",
    notes: "UI có required nên ca bỏ hẳn key là API-only.",
  },
  {
    id: "DT-13",
    technique: "EP",
    obligations: ["P13", "R4"],
    expected: "rejected",
    body: withCode("FR17-DT-13", { discount_value: "abc" }),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; discount_value phải là số dương. Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; discount_value='abc'; các trường còn lại hợp lệ.",
    notes: "UI type=number không gửi được abc; ca này API-only.",
  },
  {
    id: "DT-14",
    technique: "EP + BVA",
    obligations: ["P14", "B3-above", "R4"],
    expected: "created",
    body: withCode("FR17-DT-14", { discount_value: 1 }),
    expectedFields: {
      code: "FR17-DT-14",
      type: "percent",
      discount_value: 1,
      min_order_amount: 100000,
      expired_at: "2099-12-31",
      max_uses_per_user: 1,
    },
    oracle:
      "Tạo thành công (2xx); discount_value=1 là giá trị dương nhỏ nhất, coupon xuất hiện với discount_value=1. Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; discount_value=1; các trường còn lại hợp lệ.",
    notes: "Điểm ngay trên biên 0 của B3.",
  },
  {
    id: "DT-15",
    technique: "EP",
    obligations: ["P15", "R5"],
    expected: "rejected",
    body: without(withCode("FR17-DT-15"), "expired_at"),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; expired_at là trường bắt buộc. Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; bỏ hẳn key expired_at; các trường còn lại hợp lệ.",
    notes: "UI có required nên ca bỏ hẳn key là API-only.",
  },
  {
    id: "DT-16",
    technique: "EP",
    obligations: ["P16", "R5"],
    expected: "rejected",
    body: withCode("FR17-DT-16", { expired_at: "" }),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; expired_at là trường bắt buộc. Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; expired_at=chuỗi rỗng; các trường còn lại hợp lệ.",
    notes: "UI required chặn chuỗi rỗng; ca này API-only.",
  },
  {
    id: "DT-17",
    technique: "EP",
    obligations: ["P17", "R5"],
    expected: "rejected",
    body: withCode("FR17-DT-17", { expired_at: "not-a-date" }),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; expired_at phải là ngày hợp lệ (ASSUMED: API example dùng YYYY-MM-DD, UI dùng input type=date). Nguồn: README.md §5 FR-17; api_specification.md §6.4.",
    setup:
      "Đăng nhập admin; expired_at='not-a-date'; các trường còn lại hợp lệ.",
    notes: "ASSUMED về định dạng ngày; UI date input không gửi được chuỗi này nên ca API-only.",
  },
  {
    id: "DT-18",
    technique: "EP",
    obligations: ["P18", "R5"],
    expected: "created",
    body: withCode("FR17-DT-18", { expired_at: "2020-01-01" }),
    expectedFields: {
      code: "FR17-DT-18",
      type: "percent",
      discount_value: 10,
      min_order_amount: 100000,
      expired_at: "2020-01-01",
      max_uses_per_user: 1,
    },
    oracle:
      "Tạo thành công (2xx); FR-17 chỉ yêu cầu expired_at, không cấm ngày quá khứ; seed có coupon EXPIRED. (ASSUMED từ seed + phạm vi FR-17.)",
    setup:
      "Đăng nhập admin; expired_at='2020-01-01'; các trường còn lại hợp lệ.",
    notes:
      "ASSUMED: đặc tả không nói expired_at phải ở tương lai. UI date cho phép chọn ngày quá khứ.",
  },
  {
    id: "DT-19",
    technique: "EP + BVA",
    obligations: ["P19", "B1-ON", "R6"],
    expected: "created",
    body: withCode("FR17-DT-19", { min_order_amount: 0 }),
    expectedFields: {
      code: "FR17-DT-19",
      type: "percent",
      discount_value: 10,
      min_order_amount: 0,
      expired_at: "2099-12-31",
      max_uses_per_user: 1,
    },
    oracle:
      "Tạo thành công (2xx); min_order_amount=0 thỏa >= 0 (điểm biên ON hợp lệ). Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; min_order_amount=0; các trường còn lại hợp lệ.",
    notes: "UI cho phép 0 (không có min).",
  },
  {
    id: "DT-20",
    technique: "EP + BVA",
    obligations: ["P20", "B1-above", "R6"],
    expected: "created",
    body: withCode("FR17-DT-20", { min_order_amount: 1 }),
    expectedFields: {
      code: "FR17-DT-20",
      type: "percent",
      discount_value: 10,
      min_order_amount: 1,
      expired_at: "2099-12-31",
      max_uses_per_user: 1,
    },
    oracle:
      "Tạo thành công (2xx); min_order_amount=1 thỏa >= 0 (điểm ngay trên biên 0). Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; min_order_amount=1; các trường còn lại hợp lệ.",
    notes: "UI cho phép 1.",
  },
  {
    id: "DT-21",
    technique: "EP + BVA",
    obligations: ["P21", "B1-below", "R6"],
    expected: "rejected",
    body: withCode("FR17-DT-21", { min_order_amount: -1 }),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; min_order_amount phải >= 0. -1 là điểm ngay dưới biên 0. Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; min_order_amount=-1; các trường còn lại hợp lệ.",
    notes: "UI type=number không có min nên nhập được -1.",
  },
  {
    id: "DT-22",
    technique: "EP",
    obligations: ["P22", "R6"],
    expected: "rejected",
    body: without(withCode("FR17-DT-22"), "min_order_amount"),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; min_order_amount là trường bắt buộc. Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; bỏ hẳn key min_order_amount; các trường còn lại hợp lệ.",
    notes:
      "UI luôn gửi key min_order_amount (có thể là chuỗi rỗng), nên ca bỏ hẳn key là API-only.",
  },
  {
    id: "DT-23",
    technique: "EP",
    obligations: ["P23", "R6"],
    expected: "rejected",
    body: withCode("FR17-DT-23", { min_order_amount: "abc" }),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; min_order_amount phải là số >= 0. Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; min_order_amount='abc'; các trường còn lại hợp lệ.",
    notes: "UI type=number không gửi được abc; ca này API-only.",
  },
  {
    id: "DT-24",
    technique: "EP + BVA",
    obligations: ["P24", "B2-ON", "R6"],
    expected: "created",
    body: withCode("FR17-DT-24", { max_uses_per_user: 1 }),
    expectedFields: {
      code: "FR17-DT-24",
      type: "percent",
      discount_value: 10,
      min_order_amount: 100000,
      expired_at: "2099-12-31",
      max_uses_per_user: 1,
    },
    oracle:
      "Tạo thành công (2xx); max_uses_per_user=1 thỏa >= 1 (điểm biên ON hợp lệ). Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; max_uses_per_user=1; các trường còn lại hợp lệ.",
    notes: "UI min=1 cho phép 1.",
  },
  {
    id: "DT-25",
    technique: "EP + BVA",
    obligations: ["P25", "B2-above", "R6"],
    expected: "created",
    body: withCode("FR17-DT-25", { max_uses_per_user: 2 }),
    expectedFields: {
      code: "FR17-DT-25",
      type: "percent",
      discount_value: 10,
      min_order_amount: 100000,
      expired_at: "2099-12-31",
      max_uses_per_user: 2,
    },
    oracle:
      "Tạo thành công (2xx); max_uses_per_user=2 thỏa >= 1 (điểm ngay trên biên 1). Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; max_uses_per_user=2; các trường còn lại hợp lệ.",
    notes: "UI min=1 cho phép 2.",
  },
  {
    id: "DT-26",
    technique: "EP + BVA",
    obligations: ["P26", "B2-below", "R6"],
    expected: "rejected",
    body: withCode("FR17-DT-26", { max_uses_per_user: 0 }),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; max_uses_per_user phải >= 1. 0 là điểm ngay dưới biên 1. Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; max_uses_per_user=0; các trường còn lại hợp lệ.",
    notes:
      "UI min=1 chặn submit 0; ca này API-only. Backend dùng max_uses_per_user || 1 nên cần kiểm tra giá trị lưu thực tế.",
  },
  {
    id: "DT-27",
    technique: "EP",
    obligations: ["P27", "R6"],
    expected: "rejected",
    body: withCode("FR17-DT-27", { max_uses_per_user: -1 }),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; max_uses_per_user phải >= 1. Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; max_uses_per_user=-1; các trường còn lại hợp lệ.",
    notes: "UI min=1 chặn submit -1; ca này API-only.",
  },
  {
    id: "DT-28",
    technique: "EP",
    obligations: ["P28", "R6"],
    expected: "rejected",
    body: without(withCode("FR17-DT-28"), "max_uses_per_user"),
    oracle:
      "Bị từ chối (non-2xx) và không tạo coupon mới; max_uses_per_user là trường bắt buộc. Nguồn: README.md §5 FR-17.",
    setup:
      "Đăng nhập admin; bỏ hẳn key max_uses_per_user; các trường còn lại hợp lệ.",
    notes:
      "UI luôn gửi key max_uses_per_user (có thể là chuỗi rỗng), nên ca bỏ hẳn key là API-only.",
  },
];

const observationPercentAbove100 = {
  id: "DT-32",
  technique: "EP",
  obligations: ["P32", "R4"],
  expected: "observation",
  body: withCode("FR17-DT-32", { discount_value: 150 }),
  oracle:
    "Chưa xác định — FR-17 chỉ nói discount_value dương, không đặt upper bound cho percent. Đây là quan sát, không chấm PASS/FAIL; ảnh hưởng cách FR-09 tính giảm giá nếu >100%.",
  setup:
    "Đăng nhập admin; type=percent, discount_value=150; các trường còn lại hợp lệ.",
  notes:
    "UI không có max nên người dùng nhập được 150. Quan sát giá trị lưu và ghi nhận khoảng trống đặc tả.",
};

async function runCreateCase(testCase, token) {
  const before = await listCoupons(token);
  const request = await api(
    "POST",
    "/api/admin/coupons",
    testCase.body,
    token,
  );
  const after = await listCoupons(token);
  const beforeIds = new Set(before.rows.map((row) => row.id));
  const newRows = after.rows.filter((row) => !beforeIds.has(row.id));
  const expectedCode = testCase.body.code;
  const targetRow =
    expectedCode !== undefined && expectedCode !== null && String(expectedCode) !== ""
      ? newRows.find((row) => String(row.code) === String(expectedCode)) || null
      : null;

  let verdict;
  let actual;
  let fieldChecks = null;
  if (testCase.expected === "created") {
    const match = targetRow
      ? rowMatches(targetRow, testCase.expectedFields)
      : { pass: false, checks: [] };
    fieldChecks = match.checks;
    const statusOk = request.status >= 200 && request.status < 300;
    verdict =
      statusOk && newRows.length === 1 && targetRow && match.pass
        ? "PASS"
        : "FAIL";
    actual =
      `HTTP ${request.status}; new_rows=${newRows.length}; ` +
      `target=${targetRow ? JSON.stringify(targetRow) : "null"}; ` +
      `field_checks=${JSON.stringify(match.checks)}`;
  } else if (testCase.expected === "rejected") {
    const statusRejected = request.status < 200 || request.status >= 300;
    verdict = statusRejected && newRows.length === 0 ? "PASS" : "FAIL";
    actual =
      `HTTP ${request.status}; new_rows=${newRows.length}; ` +
      `body=${JSON.stringify(request.body)}`;
    if (newRows.length > 0) {
      actual += `; unexpected_rows=${JSON.stringify(summarizeRows(newRows))}`;
    }
  } else {
    verdict = "INCONCLUSIVE";
    actual =
      `HTTP ${request.status}; new_rows=${newRows.length}; ` +
      `body=${JSON.stringify(request.body)}; ` +
      `new_rows_data=${JSON.stringify(summarizeRows(newRows))}`;
  }

  const cleanupParts = [];
  for (const row of newRows) {
    const cleanup = await deleteCoupon(row.id, token);
    cleanupParts.push(`DELETE /api/admin/coupons/${row.id} -> HTTP ${cleanup.status}`);
  }

  record({
    id: testCase.id,
    technique: testCase.technique,
    obligations: testCase.obligations,
    interface: "API POST /api/admin/coupons",
    setup: testCase.setup,
    request,
    verification: {
      before_count: before.rows.length,
      after_count: after.rows.length,
      new_rows: summarizeRows(newRows),
      target_row: targetRow,
      field_checks: fieldChecks,
      seeds_present: null,
      absent_after_delete: null,
    },
    oracle: testCase.oracle,
    actual,
    verdict,
    cleanup: cleanupParts.length ? cleanupParts.join("; ") : "không tạo row nào",
    bugId: bugMap[testCase.id] || null,
    notes: testCase.notes,
  });
}

async function runListCase(token) {
  const code = "FR17-DT-29";
  const body = withCode(code);
  const before = await listCoupons(token);
  const create = await api("POST", "/api/admin/coupons", body, token);
  const after = await listCoupons(token);
  const targetRow = after.rows.find((row) => String(row.code) === code) || null;
  const seedCodes = ["SAVE10", "BIGBUY", "VIP100", "EXPIRED"];
  const seedsPresentBefore = seedCodes.every((seed) =>
    before.rows.some((row) => String(row.code) === seed),
  );
  const seedsPresentAfter = seedCodes.every((seed) =>
    after.rows.some((row) => String(row.code) === seed),
  );
  const expectedFields = {
    code,
    type: "percent",
    discount_value: 10,
    min_order_amount: 100000,
    expired_at: "2099-12-31",
    max_uses_per_user: 1,
  };
  const match = targetRow
    ? rowMatches(targetRow, expectedFields)
    : { pass: false, checks: [] };

  const statusOk = create.status >= 200 && create.status < 300;
  const verdict =
    statusOk &&
    targetRow &&
    match.pass &&
    seedsPresentBefore &&
    seedsPresentAfter &&
    after.rows.length === before.rows.length + 1
      ? "PASS"
      : "FAIL";
  const actual =
    `POST HTTP ${create.status}; before_count=${before.rows.length}; ` +
    `after_count=${after.rows.length}; seeds_before=${seedsPresentBefore}; ` +
    `seeds_after=${seedsPresentAfter}; target=${targetRow ? JSON.stringify(targetRow) : "null"}; ` +
    `field_checks=${JSON.stringify(match.checks)}`;

  const cleanup = targetRow
    ? await deleteCoupon(targetRow.id, token)
    : null;

  record({
    id: "DT-29",
    technique: "EP",
    obligations: ["P29", "R1", "R7"],
    interface: "API GET /api/coupons (sau khi POST tạo coupon)",
    setup:
      "Đăng nhập admin; DB test có 4 seed coupon; tạo coupon FR17-DT-29 rồi gọi GET /api/coupons.",
    request: create,
    verification: {
      before_count: before.rows.length,
      after_count: after.rows.length,
      new_rows: summarizeRows(
        after.rows.filter((row) => !before.rows.some((old) => old.id === row.id)),
      ),
      target_row: targetRow,
      field_checks: match.checks,
      seeds_present: { before: seedsPresentBefore, after: seedsPresentAfter },
      absent_after_delete: null,
    },
    oracle:
      "GET /api/coupons trả danh sách nhìn thấy được, gồm 4 seed coupon và coupon vừa tạo với đủ trường đúng giá trị. Nguồn: README.md §5 FR-17 (Xem); api_specification.md §5.2.",
    actual,
    verdict,
    cleanup: cleanup
      ? `DELETE /api/admin/coupons/${targetRow.id} -> HTTP ${cleanup.status}`
      : "không có row để cleanup",
    bugId: null,
    notes:
      "Ca này kiểm tra yêu cầu Xem danh sách; không kiểm tra thứ tự hiển thị vì đặc tả không quy định.",
  });
}

async function runDeleteExistingCase(token) {
  const code = "FR17-DT-30";
  const body = withCode(code);
  const before = await listCoupons(token);
  const create = await api("POST", "/api/admin/coupons", body, token);
  const afterCreate = await listCoupons(token);
  const targetRow = afterCreate.rows.find((row) => String(row.code) === code) || null;

  if (!targetRow) {
    record({
      id: "DT-30",
      technique: "EP",
      obligations: ["P30", "R8"],
      interface: "API DELETE /api/admin/coupons/:id",
      setup:
        "Đăng nhập admin; tạo coupon FR17-DT-30 rồi xóa theo id.",
      request: create,
      verification: {
        before_count: before.rows.length,
        after_count: afterCreate.rows.length,
        new_rows: [],
        target_row: null,
        field_checks: null,
        seeds_present: null,
        absent_after_delete: null,
      },
      oracle:
        "Xóa coupon đang tồn tại thành công (2xx) và coupon biến mất khỏi GET /api/coupons. Nguồn: README.md §5 FR-17 (Xóa); api_specification.md §6.4.",
      actual: `Setup create failed: HTTP ${create.status} ${JSON.stringify(create.body)}`,
      verdict: "BLOCKED",
      cleanup: "không có row",
      bugId: null,
      notes: "Không thể chạy ca xóa vì bước tạo fixture thất bại.",
    });
    return;
  }

  const request = await deleteCoupon(targetRow.id, token);
  const afterDelete = await listCoupons(token);
  const stillPresent = afterDelete.rows.some(
    (row) => row.id === targetRow.id || String(row.code) === code,
  );
  const verdict =
    request.status >= 200 && request.status < 300 && !stillPresent
      ? "PASS"
      : "FAIL";
  const actual =
    `POST create HTTP ${create.status}; DELETE HTTP ${request.status}; ` +
    `body=${JSON.stringify(request.body)}; still_present=${stillPresent}; ` +
    `after_delete_count=${afterDelete.rows.length}`;

  record({
    id: "DT-30",
    technique: "EP",
    obligations: ["P30", "R8"],
    interface: "API DELETE /api/admin/coupons/:id + GET /api/coupons",
    setup:
      "Đăng nhập admin; tạo coupon FR17-DT-30 rồi xóa theo id.",
    request,
    verification: {
      before_count: before.rows.length,
      after_count: afterDelete.rows.length,
      new_rows: summarizeRows(
        afterCreate.rows.filter(
          (row) => !before.rows.some((old) => old.id === row.id),
        ),
      ),
      target_row: targetRow,
      field_checks: null,
      seeds_present: null,
      absent_after_delete: !stillPresent,
    },
    oracle:
      "Xóa coupon đang tồn tại thành công (2xx) và coupon biến mất khỏi GET /api/coupons. Nguồn: README.md §5 FR-17 (Xóa); api_specification.md §6.4.",
    actual,
    verdict,
    cleanup: "row đã bị xóa bởi chính ca test",
    bugId: null,
    notes: "Không kiểm tra confirm dialog vì đặc tả FR-17 không yêu cầu.",
  });
}

async function runDeleteMissingCase(token) {
  const before = await listCoupons(token);
  const request = await deleteCoupon(999999, token);
  const after = await listCoupons(token);
  const verdict = "INCONCLUSIVE";
  const actual =
    `HTTP ${request.status}; body=${JSON.stringify(request.body)}; ` +
    `before_count=${before.rows.length}; after_count=${after.rows.length}`;

  record({
    id: "DT-31",
    technique: "EP",
    obligations: ["P31"],
    interface: "API DELETE /api/admin/coupons/:id",
    setup:
      "Đăng nhập admin; DB test không có coupon id 999999; gọi DELETE /api/admin/coupons/999999.",
    request,
    verification: {
      before_count: before.rows.length,
      after_count: after.rows.length,
      new_rows: [],
      target_row: null,
      field_checks: null,
      seeds_present: null,
      absent_after_delete: after.rows.length === before.rows.length,
    },
    oracle:
      "Chưa xác định — FR-17 yêu cầu Admin có thể Xóa mã giảm giá nhưng không quy định hành vi khi id không tồn tại. Đây là Quan sát/INCONCLUSIVE.",
    actual,
    verdict,
    cleanup: "không tạo tài nguyên",
    bugId: null,
    notes:
      "Quan sát status/body thực tế; không chấm PASS/FAIL vì thiếu oracle. Nếu thấy 2xx thì ghi nhận như một điểm cần người kiểm thử quyết định.",
  });
}

async function runOutOfScopeAuthObservation(adminToken) {
  const timestamp = localTime();
  const userLogin = await login(USER_EMAIL, USER_PASSWORD);
  const listBefore = await api("GET", "/api/coupons", undefined, userLogin.token);
  const code = "FR17-OBS-USER";
  const body = withCode(code);
  const create = await api("POST", "/api/admin/coupons", body, userLogin.token);
  const listAfter = await api("GET", "/api/coupons", undefined, userLogin.token);
  const rows = Array.isArray(listAfter.body) ? listAfter.body : [];
  const row = rows.find((item) => String(item.code) === code) || null;
  let cleanup = "không tạo row";
  if (row) {
    const del = await deleteCoupon(row.id, adminToken);
    cleanup = `DELETE /api/admin/coupons/${row.id} bằng admin -> HTTP ${del.status}`;
  }
  const item = {
    timestamp,
    user: userLogin.user
      ? {
          id: userLogin.user.id,
          email: userLogin.user.email,
          role: userLogin.user.role,
        }
      : null,
    getStatus: listBefore.status,
    getCount: Array.isArray(listBefore.body) ? listBefore.body.length : null,
    createStatus: create.status,
    createBody: create.body,
    created: Boolean(row),
    createdRow: row,
    cleanup,
  };
  outOfScope.push(item);
  fs.writeFileSync(
    path.join(EVIDENCE_DIR, "OBS-fr17-user-token.log"),
    JSON.stringify(item, null, 2) + "\n",
  );
  console.log(
    `OBS-FR17-06 HTTP ${create.status} | created=${Boolean(row)} | user role=${userLogin.user?.role}`,
  );
}

function sessionInfo() {
  const commit = execSync("git rev-parse HEAD", { cwd: REPO_ROOT })
    .toString()
    .trim();
  const branch = execSync("git rev-parse --abbrev-ref HEAD", { cwd: REPO_ROOT })
    .toString()
    .trim();
  const workingDb = path.join(REPO_ROOT, "backend", "database.sqlite");
  const testDb = path.join(SUT_DIR, "database.sqlite");
  return {
    run_id: RUN_ID,
    started_at: startedAt,
    finished_at: finishAt,
    repo: REPO_ROOT,
    sut_commit: commit,
    branch,
    source: {
      "backend/server.js": sha256File(path.join(REPO_ROOT, "backend", "server.js")),
      "backend/database.js": sha256File(
        path.join(REPO_ROOT, "backend", "database.js"),
      ),
    },
    environment: {
      platform: process.platform,
      node: process.version,
      port: 3000,
      base_url: BASE,
      sut_dir: SUT_DIR,
      isolation:
        "Bản sao server.js/database.js/package.json trong thư mục tạm; database.sqlite riêng; node_modules symlink; không dùng DB làm việc.",
    },
    working_db: {
      path: workingDb,
      sha256_before: sha256File(workingDb),
      sha256_after: sha256File(workingDb),
    },
    test_db: {
      path: testDb,
      sha256_before: sha256File(testDb),
      sha256_after: sha256File(testDb),
    },
    seed_coupons: ["SAVE10", "BIGBUY", "VIP100", "EXPIRED"],
  };
}

function writeSessionHeader(info) {
  const lines = [
    "# FR17 — Session header",
    "",
    "| Mục | Giá trị |",
    "| --- | --- |",
    `| Run ID | ${info.run_id} |`,
    `| Bắt đầu | ${info.started_at} |`,
    `| Kết thúc | ${info.finished_at} |`,
    `| Repo | ${info.repo} |`,
    `| Commit | ${info.sut_commit} |`,
    `| Branch | ${info.branch} |`,
    `| Backend server.js SHA-256 | ${info.source["backend/server.js"]} |`,
    `| Backend database.js SHA-256 | ${info.source["backend/database.js"]} |`,
    `| OS / Node | ${info.environment.platform} / ${info.environment.node} |`,
    `| Base URL | ${info.environment.base_url} |`,
    `| SUT dir | ${info.environment.sut_dir} |`,
    `| Cách ly | ${info.environment.isolation} |`,
    `| Working DB | ${info.working_db.path} |`,
    `| Working DB SHA-256 before | ${info.working_db.sha256_before} |`,
    `| Working DB SHA-256 after | ${info.working_db.sha256_after} |`,
    `| Test DB | ${info.test_db.path} |`,
    `| Test DB SHA-256 before | ${info.test_db.sha256_before} |`,
    `| Test DB SHA-256 after | ${info.test_db.sha256_after} |`,
    `| Seed coupons | ${info.seed_coupons.join(", ")} |`,
    "",
  ];
  fs.writeFileSync(path.join(EVIDENCE_DIR, "session-header.log"), lines.join("\n"));
}

function writeEvidenceMarkdown(info, counts) {
  const lines = [];
  lines.push("# FR17 — Evidence log (nhật ký bằng chứng thực thi)");
  lines.push("");
  lines.push(
    "> Mỗi lần thử một test case có một mục `EV-ID`; kết quả thô quan sát được, không chép Expected vào Actual. Log chi tiết từng ca nằm trong `evidence/<T-ID>.log`; dữ liệu có cấu trúc trong `run-summary.json`.",
  );
  lines.push("");
  lines.push("## Thông tin phiên chạy");
  lines.push("");
  lines.push("| Mục | Giá trị |");
  lines.push("| --- | --- |");
  lines.push("| Feature | FR-17 — Quản lý Mã Giảm Giá (Coupon CRUD) |");
  lines.push("| Interface | API `POST/GET/DELETE` coupon (admin token); UI admin dự kiến cho manual |");
  lines.push(`| SUT / build | \`eshop-sut-homework\` commit \`${info.sut_commit}\` |`);
  lines.push(
    "| Môi trường | macOS; Node " +
      info.environment.node +
      "; backend Node/Express + SQLite; instance cách ly (bản sao `server.js`/`database.js`, `database.sqlite` riêng, `node_modules` symlink) |",
  );
  lines.push(`| Thời điểm chạy | ${info.started_at} → ${info.finished_at} |`);
  lines.push(
    "| Người/agent thực thi | AI agent (theo skill `domain-testing-workflow`); screenshot Issue: người kiểm thử chụp sau khi xác nhận bug |",
  );
  lines.push("| Thư mục evidence | `evidence/` |");
  lines.push(
    "| Database làm việc | `backend/database.sqlite`, SHA-256 trước/sau: `" +
      info.working_db.sha256_before +
      "` / `" +
      info.working_db.sha256_after +
      "` |",
  );
  lines.push(
    `| Database test | \`${info.test_db.path}\`, SHA-256 sau run: \`${info.test_db.sha256_after}\` |`,
  );
  lines.push("");
  lines.push(
    "**Fixture:** seed coupons `SAVE10`, `BIGBUY`, `VIP100`, `EXPIRED`; tài khoản seed `admin@eshop.com` / `Admin123!` (admin) và `test@eshop.com` / `Test1234!` (user, chỉ dùng cho quan sát ngoài phạm vi).",
  );
  lines.push("");
  lines.push(
    "**Trình điều khiển (driver):** `evidence/run-fr17.mjs` (chạy các ca, ghi log và `run-summary.json`).",
  );
  lines.push("");
  lines.push("## Tổng hợp");
  lines.push("");
  lines.push("| Chỉ số | Giá trị |");
  lines.push("| --- | ---: |");
  lines.push(`| T-ID thiết kế | ${counts.designed} |`);
  lines.push(`| Đã chạy | ${counts.executed} |`);
  lines.push(`| PASS | ${counts.pass} |`);
  lines.push(`| FAIL | ${counts.fail} |`);
  lines.push(`| Quan sát / INCONCLUSIVE | ${counts.inconclusive} |`);
  lines.push(`| BLOCKED | ${counts.blocked} |`);
  lines.push(`| Chưa chạy | ${counts.not_run} |`);
  lines.push("");
  lines.push("## Evidence items");
  lines.push("");
  for (const item of results) {
    lines.push(`### ${item.evId} — ${item.id} (${item.interface})`);
    lines.push("");
    lines.push("| Trường | Giá trị |");
    lines.push("| --- | --- |");
    lines.push(`| Test case | ${item.id} |`);
    lines.push(`| Run ID / lần thử | ${RUN_ID} / 1 |`);
    lines.push(`| Kỹ thuật | ${item.technique} |`);
    lines.push(`| Obligation IDs | ${item.obligations.join(", ")} |`);
    lines.push(`| Thời điểm | ${item.timestamp} |`);
    lines.push(`| Interface | ${item.interface} |`);
    lines.push(`| Setup / trạng thái trước | ${item.setup} |`);
    lines.push("");
    lines.push("**Request thật:**");
    lines.push("");
    lines.push("```http");
    lines.push(`${item.request.method} ${item.request.endpoint}`);
    lines.push(redactAuth(true));
    lines.push("Content-Type: application/json");
    lines.push("");
    lines.push(
      item.request.requestBody === undefined
        ? "(no body)"
        : JSON.stringify(item.request.requestBody, null, 2),
    );
    lines.push("```");
    lines.push("");
    lines.push("**Kết quả thô:**");
    lines.push("");
    lines.push("```json");
    lines.push(`HTTP ${item.request.status}`);
    lines.push(JSON.stringify(item.request.body, null, 2));
    lines.push("```");
    lines.push("");
    lines.push("**Kiểm tra qua `GET /api/coupons`:**");
    lines.push("");
    lines.push("```json");
    lines.push(
      JSON.stringify(
        {
          before_count: item.verification.before_count,
          after_count: item.verification.after_count,
          new_rows: item.verification.new_rows,
          target_row: item.verification.target_row,
          field_checks: item.verification.field_checks,
          seeds_present: item.verification.seeds_present,
          absent_after_delete: item.verification.absent_after_delete,
        },
        null,
        2,
      ),
    );
    lines.push("```");
    lines.push("");
    lines.push(`- **Expected (oracle ref):** ${item.oracle}`);
    lines.push(`- **Actual:** ${item.actual}`);
    lines.push(`- **Status:** \`${item.verdict}\``);
    lines.push(`- **Artifact:** \`evidence/${item.id}.log\``);
    lines.push(`- **Cleanup:** ${item.cleanup}`);
    lines.push(`- **Bug liên quan:** ${item.bugId || "không"}`);
    if (item.notes) lines.push(`- **Ghi chú:** ${item.notes}`);
    lines.push("");
  }
  fs.writeFileSync(path.join(EVIDENCE_DIR, "FR17-evidence.md"), lines.join("\n"));
}

async function waitForServer() {
  for (let attempt = 0; attempt < 40; attempt += 1) {
    try {
      const response = await fetch(BASE + "/api/products");
      if (response.status === 200) return;
    } catch {
      // server not ready yet
    }
    await new Promise((resolve) => setTimeout(resolve, 250));
  }
  throw new Error(`Server not ready at ${BASE}`);
}

async function main() {
  startedAt = localTime();
  const workingDb = path.join(REPO_ROOT, "backend", "database.sqlite");
  const testDb = path.join(SUT_DIR, "database.sqlite");
  if (!exists(workingDb)) throw new Error(`Working DB not found: ${workingDb}`);
  if (!exists(testDb)) throw new Error(`Test DB not found: ${testDb}`);
  const workingBefore = sha256File(workingDb);
  const testBefore = sha256File(testDb);

  await waitForServer();
  const admin = await login(ADMIN_EMAIL, ADMIN_PASSWORD);
  if (admin.user?.role !== "admin") {
    throw new Error(`Expected admin role, got ${JSON.stringify(admin.user)}`);
  }

  for (const testCase of createCases) {
    await runCreateCase(testCase, admin.token);
  }
  await runListCase(admin.token);
  await runDeleteExistingCase(admin.token);
  await runDeleteMissingCase(admin.token);
  await runCreateCase(observationPercentAbove100, admin.token);
  await runOutOfScopeAuthObservation(admin.token);

  finishAt = localTime();
  const counts = {
    designed: results.length,
    executed: results.filter((item) => item.verdict !== "CHƯA CHẠY").length,
    pass: results.filter((item) => item.verdict === "PASS").length,
    fail: results.filter((item) => item.verdict === "FAIL").length,
    inconclusive: results.filter((item) => item.verdict === "INCONCLUSIVE")
      .length,
    blocked: results.filter((item) => item.verdict === "BLOCKED").length,
    not_run: results.filter((item) => item.verdict === "CHƯA CHẠY").length,
  };

  const info = {
    run_id: RUN_ID,
    started_at: startedAt,
    finished_at: finishAt,
    repo: REPO_ROOT,
    sut_commit: execSync("git rev-parse HEAD", { cwd: REPO_ROOT })
      .toString()
      .trim(),
    branch: execSync("git rev-parse --abbrev-ref HEAD", { cwd: REPO_ROOT })
      .toString()
      .trim(),
    source: {
      "backend/server.js": sha256File(path.join(REPO_ROOT, "backend", "server.js")),
      "backend/database.js": sha256File(
        path.join(REPO_ROOT, "backend", "database.js"),
      ),
    },
    environment: {
      platform: process.platform,
      node: process.version,
      port: 3000,
      base_url: BASE,
      sut_dir: SUT_DIR,
      isolation:
        "Bản sao server.js/database.js/package.json trong thư mục tạm; database.sqlite riêng; node_modules symlink; không dùng DB làm việc.",
    },
    working_db: {
      path: workingDb,
      sha256_before: workingBefore,
      sha256_after: sha256File(workingDb),
    },
    test_db: {
      path: testDb,
      sha256_before: testBefore,
      sha256_after: sha256File(testDb),
    },
    seed_coupons: ["SAVE10", "BIGBUY", "VIP100", "EXPIRED"],
    counts,
    cases: results,
    out_of_scope_observations: outOfScope,
  };

  fs.writeFileSync(
    path.join(EVIDENCE_DIR, "run-summary.json"),
    JSON.stringify(info, null, 2) + "\n",
  );
  writeSessionHeader(info);
  writeEvidenceMarkdown(info, counts);

  console.log("");
  console.log("Counts:", JSON.stringify(counts));
  console.log(`Evidence: ${EVIDENCE_DIR}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
