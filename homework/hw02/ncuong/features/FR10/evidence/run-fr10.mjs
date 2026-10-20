// FR-10 Order state machine — isolated execution driver.
// Writes per-case raw evidence logs and a combined summary to this directory.
import fs from "node:fs";
import path from "node:path";

const BASE = "http://localhost:3000";
const RUN_ID = "run-20261020-fr10";
const OUT = path.dirname(new URL(import.meta.url).pathname);
const LI = (s) => `\n--- ${s} ---\n`;

const ADMIN = { email: "admin@eshop.com", password: "Admin123!" };
const USER = { email: "test@eshop.com", password: "Test1234!" };

let ADMIN_TOKEN = "";
let USER_TOKEN = "";

async function req(method, p, { token, body } = {}) {
  const headers = {};
  if (body !== undefined) headers["Content-Type"] = "application/json";
  if (token) headers["Authorization"] = "Bearer " + token;
  const res = await fetch(BASE + p, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await res.text();
  let json = null;
  try {
    json = JSON.parse(text);
  } catch {}
  return { status: res.status, text, json };
}

async function login(creds) {
  const r = await req("POST", "/api/login", { body: creds });
  return r.json?.token || "";
}

async function checkout(amount = 200000) {
  const r = await req("POST", "/api/checkout", {
    token: USER_TOKEN,
    body: { total_amount: amount, shipping_address: "FR10 test 123 Le Loi" },
  });
  return r.json?.orderId;
}

async function readStatus(id) {
  const r = await req("GET", `/api/orders/${id}`);
  return r.json?.status;
}

async function adminSet(id, status) {
  return req("PUT", `/api/admin/orders/${id}/status`, {
    token: ADMIN_TOKEN,
    body: { status },
  });
}

async function userCancel(id, token = USER_TOKEN) {
  return req("PUT", `/api/orders/${id}/cancel`, { token });
}

async function driveTo(id, target) {
  if (target === "pending") return;
  if (target === "confirmed") return void (await adminSet(id, "confirmed"));
  if (target === "shipping") {
    await adminSet(id, "confirmed");
    return void (await adminSet(id, "shipping"));
  }
  if (target === "delivered") {
    await adminSet(id, "confirmed");
    await adminSet(id, "shipping");
    return void (await adminSet(id, "delivered"));
  }
  if (target === "canceled") return void (await adminSet(id, "canceled"));
  throw new Error("bad target " + target);
}

const results = [];

function verdictFor(kind, httpStatus, before, after, target) {
  const okSuccess = httpStatus >= 200 && httpStatus < 300;
  if (kind === "allow") {
    const pass = okSuccess && after === target;
    return { verdict: pass ? "PASS" : "FAIL", kind };
  } else {
    // forbidden / not-accessible: must be an error AND state must not change
    const pass = !okSuccess && after === before;
    return { verdict: pass ? "PASS" : "FAIL", kind };
  }
}

async function runCase({
  id,
  tech,
  obligations,
  src,
  actor,
  action, // "admin" | "user" | "admin-missing" | "user-missing" | "user-other"
  target,
  kind, // allow | forbid
  note,
}) {
  let orderId;
  if (action === "admin-missing") {
    orderId = 999999;
  } else if (action === "user-missing") {
    orderId = 999999;
  } else {
    orderId = await checkout();
    await driveTo(orderId, src);
  }

  const before = orderId === 999999 ? "N/A (không tồn tại)" : await readStatus(orderId);
  if (orderId !== 999999 && before !== src) {
    throw new Error(`setup mismatch ${id}: wanted ${src} got ${before}`);
  }

  let call;
  if (action === "admin" || action === "admin-missing") {
    call = await adminSet(orderId, target);
  } else if (action === "user" || action === "user-missing") {
    call = await userCancel(orderId);
  } else if (action === "user-other") {
    // admin token (user_id 1) cancels test user's order (user_id 2)
    call = await userCancel(orderId, ADMIN_TOKEN);
  }

  const after = orderId === 999999 ? "N/A" : await readStatus(orderId);
  const v =
    orderId === 999999
      ? { verdict: call.status >= 400 ? "PASS" : "FAIL", kind: "forbid" }
      : verdictFor(kind, call.status, before, after, target);

  let reqDesc, path;
  if (action.startsWith("admin")) path = `/api/admin/orders/${orderId}/status`;
  else path = `/api/orders/${orderId}/cancel`;

  const ev = {
    id,
    tech,
    obligations,
    run: RUN_ID,
    time: new Date().toISOString(),
    orderId,
    actor,
    method: action.startsWith("admin") ? "PUT" : "PUT",
    path,
    requestBody: action.startsWith("admin") ? JSON.stringify({ status: target }) : "(không body)",
    before,
    httpStatus: call.status,
    responseBody: call.text,
    after,
    expected: kind === "allow"
      ? `Thành công (2xx) và status = "${target}"`
      : `Lỗi (không 2xx), status giữ nguyên "${before}"`,
    verdict: v.verdict,
    note: note || "",
  };
  results.push(ev);
  writeCase(ev);
  return ev;
}

function writeCase(ev) {
  const lines = [];
  lines.push(`# ${ev.id} — raw evidence`);
  lines.push("");
  lines.push(`| Trường | Giá trị |`);
  lines.push(`| --- | --- |`);
  lines.push(`| T-ID | ${ev.id} |`);
  lines.push(`| Kỹ thuật / obligation | ${ev.tech}; ${ev.obligations} |`);
  lines.push(`| Run ID | ${ev.run} |`);
  lines.push(`| Thời điểm (UTC) | ${ev.time} |`);
  lines.push(`| Actor | ${ev.actor} |`);
  lines.push(`| Order id | ${ev.orderId} |`);
  lines.push(`| Tiền điều kiện (status trước) | ${ev.before} |`);
  lines.push("");
  lines.push("**Request:**");
  lines.push("```text");
  lines.push(`${ev.method} ${BASE}${ev.path}`);
  if (ev.requestBody !== "(không body)") lines.push(`Body: ${ev.requestBody}`);
  lines.push("```");
  lines.push("");
  lines.push("**Response thô:**");
  lines.push("```text");
  lines.push(`HTTP ${ev.httpStatus}`);
  lines.push(ev.responseBody);
  lines.push("```");
  lines.push("");
  lines.push(`| | |`);
  lines.push(`| --- | --- |`);
  lines.push(`| Expected (đặc tả) | ${ev.expected} |`);
  lines.push(`| Actual | HTTP ${ev.httpStatus}; status sau = ${ev.after} |`);
  lines.push(`| Verdict | ${ev.verdict} |`);
  if (ev.note) lines.push(`| Ghi chú | ${ev.note} |`);
  lines.push("");
  fs.writeFileSync(path.join(OUT, `${ev.id}.log`), lines.join("\n"));
}

async function main() {
  ADMIN_TOKEN = await login(ADMIN);
  USER_TOKEN = await login(USER);
  const hdr = [];
  hdr.push("# FR10 — session header");
  hdr.push("");
  hdr.push(`Run ID: ${RUN_ID}`);
  hdr.push(`Started (UTC): ${new Date().toISOString()}`);
  hdr.push(`Admin token obtained: ${ADMIN_TOKEN ? "yes" : "NO"}`);
  hdr.push(`User token obtained: ${USER_TOKEN ? "yes" : "NO"}`);
  fs.writeFileSync(path.join(OUT, "session-header.log"), hdr.join("\n"));

  const C = [
    { id: "DT-01", tech: "EP", obligations: "P1", src: "pending", actor: "admin", action: "admin", target: "confirmed", kind: "allow" },
    { id: "DT-02", tech: "EP", obligations: "P2", src: "confirmed", actor: "admin", action: "admin", target: "shipping", kind: "allow" },
    { id: "DT-03", tech: "EP + BVA", obligations: "P3, B2 tiến vào terminal", src: "shipping", actor: "admin", action: "admin", target: "delivered", kind: "allow" },
    { id: "DT-04", tech: "EP + BVA", obligations: "P4, B3 tiến vào terminal", src: "pending", actor: "admin", action: "admin", target: "canceled", kind: "allow" },
    { id: "DT-05", tech: "EP + BVA", obligations: "P5, B3 tiến vào terminal", src: "confirmed", actor: "admin", action: "admin", target: "canceled", kind: "allow" },
    { id: "DT-06", tech: "EP + BVA", obligations: "P6, B1 ngay dưới biên", src: "pending", actor: "user", action: "user", target: "canceled", kind: "allow" },
    { id: "DT-07", tech: "EP + BVA", obligations: "P7, B1 tại biên (cuối vùng hủy được)", src: "confirmed", actor: "user", action: "user", target: "canceled", kind: "allow" },
    { id: "DT-08", tech: "EP", obligations: "P8 (skip pending→shipping)", src: "pending", actor: "admin", action: "admin", target: "shipping", kind: "forbid" },
    { id: "DT-09", tech: "EP", obligations: "P9 (skip confirmed→delivered)", src: "confirmed", actor: "admin", action: "admin", target: "delivered", kind: "forbid" },
    { id: "DT-10", tech: "EP", obligations: "P10 (lùi confirmed→pending)", src: "confirmed", actor: "admin", action: "admin", target: "pending", kind: "forbid" },
    { id: "DT-11", tech: "EP", obligations: "P11 (lùi shipping→confirmed)", src: "shipping", actor: "admin", action: "admin", target: "confirmed", kind: "forbid" },
    { id: "DT-12", tech: "EP", obligations: "P12 (trùng trạng thái pending→pending)", src: "pending", actor: "admin", action: "admin", target: "pending", kind: "forbid" },
    { id: "DT-13", tech: "EP + BVA", obligations: "P13, B2 rời terminal delivered", src: "delivered", actor: "admin", action: "admin", target: "shipping", kind: "forbid" },
    { id: "DT-14", tech: "EP + BVA", obligations: "P14, B3 rời terminal canceled", src: "canceled", actor: "admin", action: "admin", target: "delivered", kind: "forbid", note: "Bug ứng viên BUG-FR10-01 (canceled là trạng thái kết thúc)" },
    { id: "DT-15", tech: "EP", obligations: "P15 (status đích không hợp lệ)", src: "pending", actor: "admin", action: "admin", target: "shipped", kind: "forbid" },
    { id: "DT-16", tech: "EP + BVA", obligations: "P16, B1 ngay trên biên (shipping)", src: "shipping", actor: "user", action: "user", target: "canceled", kind: "forbid", note: "Bug ứng viên BUG-FR10-02 (User tự hủy khi shipping)" },
    { id: "DT-17", tech: "EP + BVA", obligations: "P17, B1 xa trên biên (delivered)", src: "delivered", actor: "user", action: "user", target: "canceled", kind: "forbid" },
    { id: "DT-18", tech: "EP", obligations: "P18 (hủy khi đã canceled)", src: "canceled", actor: "user", action: "user", target: "canceled", kind: "forbid" },
    { id: "DT-19", tech: "EP", obligations: "P19 (đơn không tồn tại / không sở hữu)", src: "n/a", actor: "admin-missing", action: "admin-missing", target: "confirmed", kind: "forbid", note: "Đơn id 999999 không tồn tại (admin)" },
    { id: "DT-20", tech: "EP", obligations: "P20 (shipping→canceled, biên nhập nhằng)", src: "shipping", actor: "admin", action: "admin", target: "canceled", kind: "forbid", note: "ASSUMED theo sơ đồ FR-10 (không có cung shipping→canceled)" },
  ];
  for (const c of C) {
    try {
      await runCase(c);
    } catch (e) {
      results.push({ id: c.id, error: String(e) });
      fs.writeFileSync(path.join(OUT, `${c.id}.log`), `# ${c.id} — ERROR\n\n${e}\n`);
    }
  }

  // rerun for the two candidate bugs
  const reruns = [
    { id: "DT-14-rerun", tech: "EP", obligations: "P14 rerun", src: "canceled", actor: "admin", action: "admin", target: "delivered", kind: "forbid", note: "Rerun độ lặp lại BUG-FR10-01" },
    { id: "DT-16-rerun", tech: "EP", obligations: "P16 rerun", src: "shipping", actor: "user", action: "user", target: "canceled", kind: "forbid", note: "Rerun độ lặp lại BUG-FR10-02" },
  ];
  for (const c of reruns) await runCase(c);

  // DT-19 second variant: user cancel non-existent + non-owned order, captured separately
  const nc1 = await userCancel(999999);
  const no1 = await userCancel(999999);
  const otherOrder = await checkout();
  await driveTo(otherOrder, "pending");
  const cOther = await userCancel(otherOrder, ADMIN_TOKEN); // admin (id 1) tries test user's order (id 2)
  const otherAfter = await readStatus(otherOrder);
  const dt19 = {
    id: "DT-19-variants",
    run: RUN_ID,
    time: new Date().toISOString(),
    variants: [
      { name: "user cancel non-existent 999999", httpStatus: nc1.status, body: nc1.text },
      { name: "user cancel non-owned order (admin token)", orderId: otherOrder, httpStatus: cOther.status, body: cOther.text, statusAfter: otherAfter },
    ],
  };
  fs.writeFileSync(path.join(OUT, "DT-19-variants.log"), JSON.stringify(dt19, null, 2));

  // combined summary
  const summary = {
    run: RUN_ID,
    finished: new Date().toISOString(),
    cases: results,
    dt19variants: dt19,
  };
  fs.writeFileSync(path.join(OUT, "run-summary.json"), JSON.stringify(summary, null, 2));

  console.log("CASE\tHTTP\tBEFORE\tAFTER\tVERDICT");
  for (const r of results) {
    if (r.error) console.log(`${r.id}\tERROR\t${r.error}`);
    else console.log(`${r.id}\t${r.httpStatus}\t${r.before}\t${r.after}\t${r.verdict}`);
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
