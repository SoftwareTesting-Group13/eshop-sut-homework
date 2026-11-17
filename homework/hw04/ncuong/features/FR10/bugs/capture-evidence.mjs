// Evidence capture for FR10 bug reports (helper, not a test).
// Run: node capture-evidence.mjs   (SUT must be up: API 3000, WEB 5173, ADMIN 5174)
import { chromium } from '@playwright/test';

const API = process.env.API_URL ?? 'http://localhost:3000';
const WEB = process.env.WEB_URL ?? 'http://localhost:5173';
const ADMIN = process.env.ADMIN_URL ?? 'http://localhost:5174';
const TS = Date.now();
const OUT = new URL('./screenshots/', import.meta.url);

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });

async function loginAs(email, password) {
  const r = await page.request.post(`${API}/api/login`, { data: { email, password } });
  return (await r.json()).token;
}
async function shotJSON(name, obj) {
  await page.goto('about:blank');
  await page.evaluate((o) => {
    document.body.style.fontFamily = 'monospace';
    document.body.style.whiteSpace = 'pre';
    document.body.textContent = JSON.stringify(o, null, 2);
  }, obj);
  await page.screenshot({ path: new URL(name, OUT).pathname });
}

const ut = await loginAs('test@eshop.com', 'Test1234!');
const at = await loginAs('admin@eshop.com', 'Admin123!');
const authU = { Authorization: `Bearer ${ut}` };
const authA = { Authorization: `Bearer ${at}` };
async function mkOrder() {
  const r = await page.request.post(`${API}/api/checkout`, {
    data: { total_amount: 100000, shipping_address: `FR10 EV ${TS}` },
    headers: authU,
  });
  return (await r.json()).orderId;
}
async function setStatus(id, status, headers = authA) {
  return page.request.put(`${API}/api/admin/orders/${id}/status`, {
    data: { status },
    headers,
  });
}

// 1. canceled -> delivered allowed: UI shows the invalid button on a canceled order.
{
  const id = await mkOrder();
  await setStatus(id, 'canceled');
  await page.addInitScript((t) => localStorage.setItem('adminToken', t), at);
  await page.goto(ADMIN);
  await page.getByText('Đơn hàng', { exact: true }).click();
  await page.locator('table tbody tr', { has: page.getByText(`#${id}`, { exact: true }) })
    .screenshot({ path: new URL('bug-fr10-cancelled-delivered.png', OUT).pathname });
  const r = await setStatus(id, 'delivered');
  const o = await (await page.request.get(`${API}/api/orders/${id}`)).json();
  await shotJSON('bug-fr10-cancelled-delivered-api.png', {
    note: 'canceled is final per spec; PUT canceled->delivered must be 400',
    put_status: r.status(), final_status: o.status,
  });
}

// 2. user cancels a shipping order (spec: only admin, and only before shipping).
{
  const id = await mkOrder();
  await setStatus(id, 'confirmed');
  await setStatus(id, 'shipping');
  await page.addInitScript((t) => localStorage.setItem('token', t), ut);
  await page.goto(`${WEB}/profile`);
  await page.locator('table tbody tr', { has: page.getByText(`#${id}`, { exact: true }) })
    .screenshot({ path: new URL('bug-fr10-shipping-cancel.png', OUT).pathname });
  const r = await page.request.put(`${API}/api/orders/${id}/cancel`, { headers: authU });
  const o = await (await page.request.get(`${API}/api/orders/${id}`)).json();
  await shotJSON('bug-fr10-shipping-cancel-api.png', {
    note: 'user cancel while shipping must be 400 and keep shipping',
    put_status: r.status(), final_status: o.status,
  });
}

// 3. no role check: plain user drives the admin status endpoint.
{
  const id = await mkOrder();
  const r = await setStatus(id, 'confirmed', authU);
  const o = await (await page.request.get(`${API}/api/orders/${id}`)).json();
  await shotJSON('bug-fr10-no-authz.png', {
    note: 'FR-12 requires role=admin; user JWT must be rejected with 403',
    put_status_by_user: r.status(), final_status: o.status,
  });
}

await browser.close();
console.log('evidence captured');
