// Evidence capture for FR02 bug reports (helper, not a test).
// Run: node capture-evidence.mjs   (SUT must be up: API 3000, WEB 5173)
import { chromium } from '@playwright/test';

const API = process.env.API_URL ?? 'http://localhost:3000';
const WEB = process.env.WEB_URL ?? 'http://localhost:5173';
const TS = Date.now();
const OUT = new URL('./screenshots/', import.meta.url);

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });

// 1. Inputs are type=text: fill password, it stays visible.
await page.goto(`${WEB}/login`);
await page.getByRole('textbox').first().fill('evidence@eshop.com');
await page.getByRole('textbox').nth(1).fill('Passw0rd!');
await page.screenshot({ path: new URL('bug-fr02-input-types.png', OUT).pathname });

// helper: render JSON in page and screenshot it
async function shotJSON(name, obj) {
  await page.goto('about:blank');
  await page.evaluate((o) => {
    document.body.style.fontFamily = 'monospace';
    document.body.style.whiteSpace = 'pre';
    document.body.textContent = JSON.stringify(o, null, 2);
  }, obj);
  await page.screenshot({ path: new URL(name, OUT).pathname });
}

// 2. Counter +2 per fail: 2 wrong logins -> attempts should be 2, actual 4 + locked.
{
  const email = `fr02.ev.counter+${TS}@eshop.com`;
  await page.request.post(`${API}/api/register`, { data: { name: 'FR02 EV', email, password: 'Passw0rd!' } });
  for (let i = 0; i < 2; i++) {
    await page.request.post(`${API}/api/login`, { data: { email, password: 'WrongPass1!' } });
  }
  const admin = await page.request.post(`${API}/api/login`, {
    data: { email: 'admin@eshop.com', password: 'Admin123!' },
  });
  const users = await (await page.request.get(`${API}/api/admin/users`, {
    headers: { Authorization: `Bearer ${(await admin.json()).token}` },
  })).json();
  const u = users.find((x) => x.email === email);
  await shotJSON('bug-fr02-counter.png', {
    note: 'after 2 wrong logins, spec expects login_attempts=2 and locked_until=null',
    email: u.email, login_attempts: u.login_attempts, locked_until: u.locked_until,
  });
}

// 3. Null-password bypass: register with password null, login with null -> JWT issued.
{
  const email = `fr02.ev.null+${TS}@eshop.com`;
  await page.request.post(`${API}/api/register`, { data: { name: 'FR02 EV', email, password: null } });
  const res = await page.request.post(`${API}/api/login`, { data: { email, password: null } });
  const body = await res.json();
  await shotJSON('bug-fr02-null-bypass.png', {
    note: 'login with password:null must NOT issue a token',
    status: res.status(), token_issued: Boolean(body.token), token: body.token ?? null,
  });
}

await browser.close();
console.log('evidence captured');
