// Evidence capture for FR17 bug reports (helper, not a test).
// Run: node capture-evidence.mjs   (SUT must be up: API 3000, ADMIN 5174)
import { chromium } from '@playwright/test';

const API = process.env.API_URL ?? 'http://localhost:3000';
const ADMIN = process.env.ADMIN_URL ?? 'http://localhost:5174';
const TS = Date.now();
const OUT = new URL('./screenshots/', import.meta.url);

const browser = await chromium.launch();
const page = await browser.newPage({ width: 1280, height: 800 });

const admin = await page.request.post(`${API}/api/login`, {
  data: { email: 'admin@eshop.com', password: 'Admin123!' },
});
const at = (await admin.json()).token;
const auth = { Authorization: `Bearer ${at}` };

async function shotJSON(name, obj) {
  await page.goto('about:blank');
  await page.evaluate((o) => {
    document.body.style.fontFamily = 'monospace';
    document.body.style.whiteSpace = 'pre';
    document.textContent = '';
    document.body.textContent = JSON.stringify(o, null, 2);
  }, obj);
  await page.screenshot({ path: new URL(name, OUT).pathname });
}

async function create(body) {
  const r = await page.request.post(`${API}/api/admin/coupons`, { data: body, headers: auth });
  return { status: r.status(), body: await r.json() };
}
async function cleanup(codes) {
  const list = await (await page.request.get(`${API}/api/coupons`, { headers: auth })).json();
  for (const c of list.filter((x) => codes.includes(x.code) || (x.code === null && codes.includes(null)))) {
    await page.request.delete(`${API}/api/admin/coupons/${c.id}`, { headers: auth });
  }
}

// 1. UI: invalid numerics accepted -> table shows -1% / 150% rows.
await page.addInitScript((t) => localStorage.setItem('adminToken', t), at);
await page.goto(ADMIN);
await page.getByText('Mã Giảm Giá', { exact: true }).click();
await expect_table_visible();
async function expect_table_visible() {
  await page.getByRole('heading', { name: 'Quản lý Mã Giảm Giá' }).waitFor();
}
const ev1 = `FR17EVN1-${TS}`;
await page.getByPlaceholder('Mã coupon (VD: SAVE10)').fill(ev1);
await page.getByRole('combobox').selectOption('percent');
await page.getByPlaceholder('Giá trị % (VD: 10)').fill('-1');
await page.getByPlaceholder('Đơn tối thiểu (₫)').fill('100000');
await page.getByPlaceholder('Ngày hết hạn').fill('2099-12-31');
await page.getByPlaceholder('Số lần dùng tối đa/người').fill('1');
await page.getByRole('button', { name: 'Tạo mã' }).click();
await page.getByText(ev1, { exact: true }).waitFor();
await page.locator('table').screenshot({ path: new URL('bug-fr17-numeric-bounds.png', OUT).pathname });

// 2. Case-sensitive duplicate: SAVE10 seed + save10 both listed.
const rSave = await create({ code: 'save10', type: 'percent', discount_value: 10, min_order_amount: 100000, expired_at: '2099-12-31', max_uses_per_user: 1 });
await page.goto(ADMIN);
await page.getByText('Mã Giảm Giá', { exact: true }).click();
await expect_table_visible();
await page.getByText('save10', { exact: true }).waitFor();
await page.locator('table').screenshot({ path: new URL('bug-fr17-code-case.png', OUT).pathname });
await shotJSON('bug-fr17-code-case-api.png', {
  note: 'uniqueness should be case-insensitive; save10 must be rejected',
  put_save10_status: rSave.status, save10_id: rSave.body.id ?? null,
});

// 3. Grab-bag: bad type, abc discount, bad date, max 0.
const evT = `FR17EVT-${TS}`;
const rT = await create({ code: evT, type: 'percentage', discount_value: 10, min_order_amount: 100000, expired_at: '2099-12-31', max_uses_per_user: 1 });
const evD = `FR17EVD-${TS}`;
const rD = await create({ code: evD, type: 'percent', discount_value: 'abc', min_order_amount: 100000, expired_at: '2099-12-31', max_uses_per_user: 1 });
const evE = `FR17EVE-${TS}`;
const rE = await create({ code: evE, type: 'percent', discount_value: 10, min_order_amount: 100000, expired_at: 'not-a-date', max_uses_per_user: 1 });
const evM = `FR17EVM-${TS}`;
const rM = await create({ code: evM, type: 'percent', discount_value: 10, min_order_amount: 100000, expired_at: '2099-12-31', max_uses_per_user: 0 });
const list = await (await page.request.get(`${API}/api/coupons`, { headers: auth })).json();
const rowOf = (c) => list.find((x) => x.code === c);
await shotJSON('bug-fr17-other-fields-api.png', {
  note: 'all four invalid inputs must be rejected (>=400); none was',
  type_percentage: { status: rT.status, stored_type: rowOf(evT)?.type },
  discount_abc: { status: rD.status, stored_value: rowOf(evD)?.discount_value },
  expired_garbage: { status: rE.status, stored_expiry: rowOf(evE)?.expired_at },
  max_uses_0: { status: rM.status, stored_max: rowOf(evM)?.max_uses_per_user, remark: '0 became 1 via || 1' },
});
await cleanup([ev1, 'save10', evT, evD, evE, evM]);

await browser.close();
console.log('evidence captured');
