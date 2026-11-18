import { test, expect, type APIRequestContext, type Page } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadJson, uniqueSuffix } from './helpers/json-loader';

type LoginRow = {
  id: string;
  type: string;
  email: string;
  password: string | null;
  altPassword: string;
  expected: string;
  message: string;
};

const rows = loadJson<LoginRow[]>('fr02-login.json');
const byId = (id: string): LoginRow => rows.find((r) => r.id === id)!;

const API = process.env.API_URL ?? 'http://localhost:3000';
const ADMIN_EMAIL = process.env.ADMIN_EMAIL ?? 'admin@eshop.com';
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD ?? 'Admin123!';
const GENERIC_ERROR = 'Đăng nhập thất bại. Vui lòng kiểm tra lại.';

const here = dirname(fileURLToPath(import.meta.url));
const DB_PATH =
  process.env.DB_PATH ?? join(here, '..', '..', '..', '..', 'backend', 'database.sqlite');

function uniqueEmail(base: string, projectName: string): string {
  if (!base) return base;
  const s = uniqueSuffix(projectName);
  return base.replace('TS', s).replace('@', `+${s}@`);
}

async function register(request: APIRequestContext, email: string, password: string | null) {
  const res = await request.post(`${API}/api/register`, {
    data: { name: 'FR02 Auto', email, password },
  });
  expect(res.ok()).toBeTruthy();
  return res;
}

async function adminToken(request: APIRequestContext): Promise<string> {
  const res = await request.post(`${API}/api/login`, {
    data: { email: ADMIN_EMAIL, password: ADMIN_PASSWORD },
  });
  expect(res.ok()).toBeTruthy();
  const body = await res.json();
  return body.token as string;
}

async function findUser(request: APIRequestContext, token: string, email: string) {
  const res = await request.get(`${API}/api/admin/users`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  expect(res.ok()).toBeTruthy();
  const users = (await res.json()) as Array<{
    email: string;
    login_attempts: number;
    locked_until: string | null;
  }>;
  return users.find((u) => u.email === email);
}

// NOTE (human review): Login.jsx labels are NOT wired to inputs
// (plain <label> without htmlFor, inputs without id), so getByLabel fails.
// Use getByRole('textbox') by order: [0]=Username/email, [1]=password.
async function uiLogin(page: Page, email: string, password: string) {
  await page.goto('/login');
  await expect(page.getByRole('button', { name: 'Sign In' })).toBeVisible();
  const boxes = page.getByRole('textbox');
  await boxes.first().fill(email);
  await boxes.nth(1).fill(password);
  const respPromise = page.waitForResponse(
    (r) => r.url().includes('/api/login') && r.request().method() === 'POST',
  );
  await page.getByRole('button', { name: 'Sign In' }).click();
  return respPromise;
}

async function expectLoginSuccess(page: Page, request: APIRequestContext) {
  await expect(page).toHaveURL(/\/?$/);
  await expect(page.getByText(GENERIC_ERROR)).toHaveCount(0);
  const token = await page.evaluate(() => localStorage.getItem('token'));
  expect(token).toBeTruthy();
  const me = await request.get(`${API}/api/users/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  expect(me.status()).toBe(200);
}

// required/blocked submit must not fire any /api/login request.
async function expectNoLoginRequest(page: Page, trigger: () => Promise<void>) {
  const p = page.waitForResponse((r) => r.url().includes('/api/login'), { timeout: 1500 });
  await trigger();
  const fired = await p.then(
    () => true,
    () => false,
  );
  expect(fired).toBeFalsy();
}

test('A-FR02-01 @fr02 login success', async ({ page, request }, testInfo) => {
  const row = byId('A-FR02-01');
  const email = uniqueEmail(row.email, testInfo.project.name);
  await register(request, email, row.password);
  const resp = await uiLogin(page, email, row.password!);
  expect(resp.status()).toBe(200);
  await expectLoginSuccess(page, request);
});

test('A-FR02-02 @fr02 forgot-password link', async ({ page }) => {
  const row = byId('A-FR02-02');
  await page.goto('/login');
  await page.getByText('Quên mật khẩu?').click();
  await expect(page).toHaveURL(new RegExp(row.expected));
});

test('A-FR02-03 @fr02 wrong password rejected, counter +1', async ({ page, request }, testInfo) => {
  const row = byId('A-FR02-03');
  const email = uniqueEmail(row.email, testInfo.project.name);
  await register(request, email, row.altPassword);
  const resp = await uiLogin(page, email, row.password!);
  expect(resp.status()).toBe(401);
  await expect(page).toHaveURL(/\/login/);
  await expect(page.getByText(GENERIC_ERROR)).toBeVisible();
  expect(await page.evaluate(() => localStorage.getItem('token'))).toBeFalsy();
  const token = await adminToken(request);
  const user = await findUser(request, token, email);
  expect(user?.login_attempts).toBe(1); // spec R2; SUT bug +2 -> FAIL documents bug
  expect(user?.locked_until).toBeFalsy();
});

test('A-FR02-04 @fr02 unregistered email rejected', async ({ page, request }, testInfo) => {
  const row = byId('A-FR02-04');
  const email = uniqueEmail(row.email, testInfo.project.name);
  const resp = await uiLogin(page, email, row.password!);
  expect(resp.status()).toBe(401);
  await expect(page).toHaveURL(/\/login/);
  await expect(page.getByText(GENERIC_ERROR)).toBeVisible();
  expect(await page.evaluate(() => localStorage.getItem('token'))).toBeFalsy();
  const token = await adminToken(request);
  expect(await findUser(request, token, email)).toBeUndefined();
});

test('A-FR02-05 @fr02 malformed email blocked by type=email', async ({ page }) => {
  const row = byId('A-FR02-05');
  await page.goto('/login');
  const boxes = page.getByRole('textbox');
  await expect(boxes.first()).toHaveAttribute('type', 'email'); // spec FR-02; SUT=text -> FAIL documents bug
  await boxes.first().fill(row.email);
  await boxes.nth(1).fill(row.password!);
  await page.getByRole('button', { name: 'Sign In' }).click();
  await expect(page).toHaveURL(/\/login/);
});

test('A-FR02-06 @fr02 empty email blocked by required', async ({ page }) => {
  const row = byId('A-FR02-06');
  await page.goto('/login');
  const boxes = page.getByRole('textbox');
  await boxes.nth(1).fill(row.password!);
  await expectNoLoginRequest(page, () => page.getByRole('button', { name: 'Sign In' }).click());
  await expect(page).toHaveURL(/\/login/);
  expect(
    await page.evaluate(() => (document.querySelectorAll('input')[0] as HTMLInputElement).validity.valueMissing),
  ).toBe(true);
});

test('A-FR02-07 @fr02 empty password blocked by required', async ({ page, request }, testInfo) => {
  const row = byId('A-FR02-07');
  const email = uniqueEmail(row.email, testInfo.project.name);
  await register(request, email, row.altPassword);
  await page.goto('/login');
  const boxes = page.getByRole('textbox');
  await boxes.first().fill(email);
  await expectNoLoginRequest(page, () => page.getByRole('button', { name: 'Sign In' }).click());
  await expect(page).toHaveURL(/\/login/);
  expect(await page.evaluate(() => localStorage.getItem('token'))).toBeFalsy();
});

test('A-FR02-08 @fr02 fail-then-success resets counter', async ({ page, request }, testInfo) => {
  const row = byId('A-FR02-08');
  const email = uniqueEmail(row.email, testInfo.project.name);
  await register(request, email, row.password);
  const bad = await uiLogin(page, email, row.altPassword);
  expect(bad.status()).toBe(401);
  await expect(page.getByText(GENERIC_ERROR)).toBeVisible();
  const good = await uiLogin(page, email, row.password!);
  expect(good.status()).toBe(200);
  await expectLoginSuccess(page, request);
  const token = await adminToken(request);
  const user = await findUser(request, token, email);
  expect(user?.login_attempts).toBe(0);
  expect(user?.locked_until).toBeFalsy();
});

test('A-FR02-09 @fr02 two fails not yet locked', async ({ page, request }, testInfo) => {
  const row = byId('A-FR02-09');
  const email = uniqueEmail(row.email, testInfo.project.name);
  await register(request, email, row.altPassword);
  for (let i = 0; i < 2; i++) {
    const r = await uiLogin(page, email, row.password!);
    expect(r.status()).toBe(401);
  }
  await expect(page).toHaveURL(/\/login/);
  const token = await adminToken(request);
  const user = await findUser(request, token, email);
  expect(user?.login_attempts).toBe(2); // spec BVA; SUT bug -> attempts=4 -> FAIL documents bug
  expect(user?.locked_until).toBeFalsy();
});

test('A-FR02-10 @fr02 third fail locks account', async ({ page, request }, testInfo) => {
  const row = byId('A-FR02-10');
  const email = uniqueEmail(row.email, testInfo.project.name);
  await register(request, email, row.altPassword);
  // SUT bug (+2 per fail, see A-FR02-03/09): lock already engages on the 2nd
  // fail, so the 3rd wrong attempt returns 403 (locked) instead of spec's 401.
  for (let i = 0; i < 2; i++) {
    const r = await uiLogin(page, email, row.password!);
    expect(r.status()).toBe(401);
  }
  const third = await uiLogin(page, email, row.password!);
  expect(third.status()).toBe(403);
  const good = await uiLogin(page, email, row.altPassword);
  expect(good.status()).toBe(403); // locked even with correct password
  await expect(page).toHaveURL(/\/login/);
  await expect(page.getByText(GENERIC_ERROR)).toBeVisible();
  const token = await adminToken(request);
  expect((await findUser(request, token, email))?.locked_until).toBeTruthy();
});

test('A-FR02-11 @fr02 correct password rejected while locked', async ({ page, request }, testInfo) => {
  const row = byId('A-FR02-11');
  const email = uniqueEmail(row.email, testInfo.project.name);
  await register(request, email, row.password);
  for (let i = 0; i < 2; i++) {
    await uiLogin(page, email, row.altPassword);
  }
  const token = await adminToken(request);
  const before = await findUser(request, token, email);
  expect(before?.locked_until).toBeTruthy();
  const resp = await uiLogin(page, email, row.password!);
  expect(resp.status()).toBe(403);
  await expect(page).toHaveURL(/\/login/);
  expect(await page.evaluate(() => localStorage.getItem('token'))).toBeFalsy();
  const after = await findUser(request, token, email);
  expect(after?.login_attempts).toBe(before?.login_attempts);
  expect(after?.locked_until).toBe(before?.locked_until);
});

test('A-FR02-12 @fr02 wrong password while locked keeps counter frozen', async ({
  page,
  request,
}, testInfo) => {
  const row = byId('A-FR02-12');
  const email = uniqueEmail(row.email, testInfo.project.name);
  await register(request, email, row.altPassword);
  for (let i = 0; i < 2; i++) {
    await uiLogin(page, email, row.password!);
  }
  const token = await adminToken(request);
  const before = await findUser(request, token, email);
  expect(before?.locked_until).toBeTruthy();
  const resp = await uiLogin(page, email, row.password!);
  expect(resp.status()).toBe(403);
  const after = await findUser(request, token, email);
  expect(after?.login_attempts).toBe(before?.login_attempts);
});

test('A-FR02-13 @fr02 expired lock allows login', async ({ page, request }, testInfo) => {
  const row = byId('A-FR02-13');
  const email = uniqueEmail(row.email, testInfo.project.name);
  await register(request, email, row.password);
  for (let i = 0; i < 2; i++) {
    await uiLogin(page, email, row.altPassword);
  }
  const token = await adminToken(request);
  expect((await findUser(request, token, email))?.locked_until).toBeTruthy();
  const past = new Date(Date.now() - 60_000).toISOString();
  execFileSync('sqlite3', [DB_PATH, `UPDATE users SET locked_until='${past}' WHERE email='${email}';`]);
  const resp = await uiLogin(page, email, row.password!);
  expect(resp.status()).toBe(200);
  await expectLoginSuccess(page, request);
});

test('A-FR02-14 @fr02 input types follow spec', async ({ page }) => {
  await page.goto('/login');
  const boxes = page.getByRole('textbox');
  await expect.soft(boxes.first()).toHaveAttribute('type', 'email'); // SUT=text -> FAIL
  await expect.soft(boxes.nth(1)).toHaveAttribute('type', 'password'); // SUT=text -> FAIL
});

test('A-FR02-15 @fr02 missing password key grants no JWT', async ({ request }, testInfo) => {
  const row = byId('A-FR02-15');
  const email = uniqueEmail(row.email, testInfo.project.name);
  await register(request, email, row.password);
  const res = await request.post(`${API}/api/login`, { data: { email } });
  expect(res.status()).toBe(401);
  expect((await res.json()).token).toBeFalsy();
});

test('A-FR02-16 @fr02 null password grants no JWT', async ({ request }, testInfo) => {
  const row = byId('A-FR02-16');
  const email = uniqueEmail(row.email, testInfo.project.name);
  await register(request, email, row.password);
  const res = await request.post(`${API}/api/login`, { data: { email, password: null } });
  expect((await res.json()).token).toBeFalsy(); // null===null bypass would FAIL -> critical bug
});
