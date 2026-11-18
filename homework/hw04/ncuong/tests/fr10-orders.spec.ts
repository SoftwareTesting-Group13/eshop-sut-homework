import { test, expect, type APIRequestContext, type Page } from '@playwright/test';
import { loadJson, uniqueSuffix } from './helpers/json-loader';
import { API, adminToken as adminLogin, userToken } from './helpers/eshop-api';

type OrderRow = {
  id: string;
  type: string;
  sourceStatus: string;
  action: string;
  expectedStatus: string;
  actor: string;
  total: number;
  address: string;
};

const rows = loadJson<OrderRow[]>('fr10-orders.json');
const byId = (id: string): OrderRow => rows.find((r) => r.id === id)!;

const ADMIN_URL = process.env.ADMIN_URL ?? 'http://localhost:5174';

async function createOrder(
  request: APIRequestContext,
  token: string,
  total: number,
  address: string,
): Promise<number> {
  const res = await request.post(`${API}/api/checkout`, {
    data: { total_amount: total, shipping_address: address },
    headers: { Authorization: `Bearer ${token}` },
  });
  expect(res.ok()).toBeTruthy();
  return (await res.json()).orderId as number;
}

async function setStatus(
  request: APIRequestContext,
  token: string,
  id: number,
  status: string,
) {
  const res = await request.put(`${API}/api/admin/orders/${id}/status`, {
    data: { status },
    headers: { Authorization: `Bearer ${token}` },
  });
  expect(res.ok()).toBeTruthy();
  return res;
}

async function getOrder(request: APIRequestContext, id: number) {
  const res = await request.get(`${API}/api/orders/${id}`);
  expect(res.ok()).toBeTruthy();
  return (await res.json()) as { status: string };
}

// Admin UI: token via API, inject adminToken, open tab Don hang.
async function openAdminOrders(page: Page, request: APIRequestContext) {
  const token = await adminLogin(request);
  await page.addInitScript(
    (t: string) => localStorage.setItem('adminToken', t),
    token,
  );
  await page.goto(ADMIN_URL);
  await page.getByText('Đơn hàng', { exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Quản lý Đơn hàng' })).toBeVisible();
}

// Unique row by exact order-code cell (avoids #1 matching #10).
function adminRow(page: Page, id: number) {
  return page.locator('table tbody tr', { has: page.getByText(`#${id}`, { exact: true }) });
}

function profileRow(page: Page, id: number) {
  return page.locator('table tbody tr', { has: page.getByText(`#${id}`, { exact: true }) });
}

async function adminDo(page: Page, id: number, action: string, expectedBadge: string) {
  const respPromise = page.waitForResponse(
    (r) => r.url().includes('/api/admin/orders') && r.request().method() === 'PUT',
  );
  await adminRow(page, id).getByRole('button', { name: action }).click();
  const resp = await respPromise;
  expect(resp.status()).toBe(200);
  await expect(adminRow(page, id).getByText(expectedBadge)).toBeVisible();
}

async function openProfile(page: Page, token: string) {
  await page.addInitScript((t: string) => localStorage.setItem('token', t), token);
  await page.goto('/profile');
  await expect(page.getByRole('heading', { name: 'Lịch sử đơn hàng' })).toBeVisible();
}

test('A-FR10-01 @fr10 pending -> Xac nhan', async ({ page, request }) => {
  const row = byId('A-FR10-01');
  const ut = await userToken(request);
  const at = await adminLogin(request);
  const id = await createOrder(request, ut, row.total, `${row.address} ${uniqueSuffix('c')}`);
  await openAdminOrders(page, request);
  await adminDo(page, id, row.action, row.expectedStatus);
  expect((await getOrder(request, id)).status).toBe('confirmed');
});

test('A-FR10-02 @fr10 confirmed -> Giao hang', async ({ page, request }) => {
  const row = byId('A-FR10-02');
  const ut = await userToken(request);
  const at = await adminLogin(request);
  const id = await createOrder(request, ut, row.total, row.address);
  await setStatus(request, at, id, 'confirmed');
  await openAdminOrders(page, request);
  await adminDo(page, id, row.action, row.expectedStatus);
  expect((await getOrder(request, id)).status).toBe('shipping');
});

test('A-FR10-03 @fr10 shipping -> Hoan thanh', async ({ page, request }) => {
  const row = byId('A-FR10-03');
  const ut = await userToken(request);
  const at = await adminLogin(request);
  const id = await createOrder(request, ut, row.total, row.address);
  await setStatus(request, at, id, 'confirmed');
  await setStatus(request, at, id, 'shipping');
  await openAdminOrders(page, request);
  await adminDo(page, id, row.action, row.expectedStatus);
  expect((await getOrder(request, id)).status).toBe('delivered');
});

test('A-FR10-04 @fr10 pending -> Huy (admin)', async ({ page, request }) => {
  const row = byId('A-FR10-04');
  const ut = await userToken(request);
  const id = await createOrder(request, ut, row.total, row.address);
  await openAdminOrders(page, request);
  await adminDo(page, id, row.action, row.expectedStatus);
  expect((await getOrder(request, id)).status).toBe('canceled');
});

test('A-FR10-05 @fr10 confirmed -> Huy (admin)', async ({ page, request }) => {
  const row = byId('A-FR10-05');
  const ut = await userToken(request);
  const at = await adminLogin(request);
  const id = await createOrder(request, ut, row.total, row.address);
  await setStatus(request, at, id, 'confirmed');
  await openAdminOrders(page, request);
  await adminDo(page, id, row.action, row.expectedStatus);
  expect((await getOrder(request, id)).status).toBe('canceled');
});

test('A-FR10-06 @fr10 user huy don pending', async ({ page, request }) => {
  const row = byId('A-FR10-06');
  const ut = await userToken(request);
  const id = await createOrder(request, ut, row.total, row.address);
  await openProfile(page, ut);
  const dialogPromise = page.waitForEvent('dialog');
  const respPromise = page.waitForResponse(
    (r) => r.url().includes(`/api/orders/${id}/cancel`) && r.request().method() === 'PUT',
  );
  await profileRow(page, id).getByRole('button', { name: row.action }).click();
  expect((await respPromise).status()).toBe(200);
  const dialog = await dialogPromise;
  expect(dialog.message()).toContain('Hủy đơn thành công');
  await dialog.dismiss();
  await expect(profileRow(page, id).getByText(row.expectedStatus)).toBeVisible();
});

test('A-FR10-07 @fr10 user huy don confirmed', async ({ page, request }) => {
  const row = byId('A-FR10-07');
  const ut = await userToken(request);
  const at = await adminLogin(request);
  const id = await createOrder(request, ut, row.total, row.address);
  await setStatus(request, at, id, 'confirmed');
  await openProfile(page, ut);
  page.on('dialog', async (d) => d.dismiss());
  const respPromise = page.waitForResponse(
    (r) => r.url().includes(`/api/orders/${id}/cancel`) && r.request().method() === 'PUT',
  );
  await profileRow(page, id).getByRole('button', { name: row.action }).click();
  expect((await respPromise).status()).toBe(200);
  await expect(profileRow(page, id).getByText(row.expectedStatus)).toBeVisible();
});

test('A-FR10-08 @fr10 canceled -> Danh dau Da giao (transition sai)', async ({
  page,
  request,
}) => {
  const row = byId('A-FR10-08');
  const ut = await userToken(request);
  const at = await adminLogin(request);
  const id = await createOrder(request, ut, row.total, row.address);
  await setStatus(request, at, id, 'canceled');
  await openAdminOrders(page, request);
  // Spec FR-10: canceled is final, must be rejected and stay canceled.
  // Actual SUT allows it (PUT 200 -> badge becomes Da giao). Assert the
  // ACTUAL UI change first (deterministic, proves the click took effect),
  // then assert the SPEC oracle -> FAIL documents the bug (HW02 DT-14).
  const respPromise = page.waitForResponse(
    (r) => r.url().includes('/api/admin/orders') && r.request().method() === 'PUT',
  );
  await adminRow(page, id).getByRole('button', { name: row.action }).click();
  expect((await respPromise).status()).toBe(200);
  await expect(adminRow(page, id).getByText('Đã giao')).toBeVisible();
  expect((await getOrder(request, id)).status).toBe('canceled');
});

test('A-FR10-09 @fr10 shipping khong co nut Huy', async ({ page, request }) => {
  const row = byId('A-FR10-09');
  const ut = await userToken(request);
  const at = await adminLogin(request);
  const id = await createOrder(request, ut, row.total, row.address);
  await setStatus(request, at, id, 'confirmed');
  await setStatus(request, at, id, 'shipping');
  await openAdminOrders(page, request);
  const r = adminRow(page, id);
  await expect(r.getByRole('button', { name: 'Hoàn thành' })).toBeVisible();
  await expect(r.getByRole('button', { name: 'Hủy' })).toHaveCount(0);
  await expect(r.getByText(row.expectedStatus)).toBeVisible();
});

test('A-FR10-10 @fr10 delivered khong co nut hanh dong', async ({ page, request }) => {
  const row = byId('A-FR10-10');
  const ut = await userToken(request);
  const at = await adminLogin(request);
  const id = await createOrder(request, ut, row.total, row.address);
  await setStatus(request, at, id, 'confirmed');
  await setStatus(request, at, id, 'shipping');
  await setStatus(request, at, id, 'delivered');
  await openAdminOrders(page, request);
  const r = adminRow(page, id);
  await expect(r.getByText(row.expectedStatus)).toBeVisible();
  await expect(r.getByRole('button')).toHaveCount(0);
  await openProfile(page, ut);
  await expect(profileRow(page, id).getByRole('button', { name: 'Hủy đơn' })).toHaveCount(0);
});

test('A-FR10-11 @fr10 dia chi trong hien placeholder', async ({ page, request }) => {
  const row = byId('A-FR10-11');
  const ut = await userToken(request);
  const id = await createOrder(request, ut, row.total, row.address);
  await openAdminOrders(page, request);
  await expect(adminRow(page, id).getByText('Chưa cập nhật')).toBeVisible();
});

test('A-FR10-12 @fr10 tong tien 0 format khong crash', async ({ page, request }) => {
  const row = byId('A-FR10-12');
  const ut = await userToken(request);
  const id = await createOrder(request, ut, row.total, row.address);
  await openAdminOrders(page, request);
  await expect(adminRow(page, id).getByText('0 ₫')).toBeVisible();
});

test('A-FR10-13 @fr10 pending->shipping bi tu choi (API)', async ({ request }) => {
  const row = byId('A-FR10-13');
  const ut = await userToken(request);
  const at = await adminLogin(request);
  const id = await createOrder(request, ut, row.total, row.address);
  const res = await request.put(`${API}/api/admin/orders/${id}/status`, {
    data: { status: 'shipping' },
    headers: { Authorization: `Bearer ${at}` },
  });
  expect(res.status()).toBe(400);
  expect(await res.text()).toContain('Invalid state transition');
  expect((await getOrder(request, id)).status).toBe('pending');
});

test('A-FR10-14 @fr10 invalid jumps bi tu choi (API)', async ({ request }) => {
  const row = byId('A-FR10-14');
  const ut = await userToken(request);
  const at = await adminLogin(request);
  const auth = { Authorization: `Bearer ${at}` };
  const idC = await createOrder(request, ut, row.total, row.address);
  await setStatus(request, at, idC, 'confirmed');
  const r1 = await request.put(`${API}/api/admin/orders/${idC}/status`, {
    data: { status: 'delivered' },
    headers: auth,
  });
  expect(r1.status(), 'confirmed->delivered').toBe(400);
  expect((await getOrder(request, idC)).status).toBe('confirmed');
  const r2 = await request.put(`${API}/api/admin/orders/${idC}/status`, {
    data: { status: 'pending' },
    headers: auth,
  });
  expect(r2.status(), 'confirmed->pending').toBe(400);
  const idP = await createOrder(request, ut, row.total, row.address);
  const r3 = await request.put(`${API}/api/admin/orders/${idP}/status`, {
    data: { status: 'pending' },
    headers: auth,
  });
  expect(r3.status(), 'pending->pending').toBe(400);
  const r4 = await request.put(`${API}/api/admin/orders/${idP}/status`, {
    data: { status: 'shipped' },
    headers: auth,
  });
  expect(r4.status(), 'pending->shipped').toBe(400);
  expect((await getOrder(request, idP)).status).toBe('pending');
});

test('A-FR10-15 @fr10 user cancel sai trang thai (API)', async ({ request }) => {
  const row = byId('A-FR10-15');
  const ut = await userToken(request);
  const at = await adminLogin(request);
  const authU = { Authorization: `Bearer ${ut}` };
  // Soft asserts: record every sub-case outcome (spec expects 400 for all).
  const idS = await createOrder(request, ut, row.total, row.address);
  await setStatus(request, at, idS, 'confirmed');
  await setStatus(request, at, idS, 'shipping');
  const rS = await request.put(`${API}/api/orders/${idS}/cancel`, { headers: authU });
  expect.soft(rS.status(), 'user cancel shipping (spec: 400)').toBe(400); // actual 200 -> FAIL documents bug
  const idD = await createOrder(request, ut, row.total, row.address);
  await setStatus(request, at, idD, 'confirmed');
  await setStatus(request, at, idD, 'shipping');
  await setStatus(request, at, idD, 'delivered');
  const rD = await request.put(`${API}/api/orders/${idD}/cancel`, { headers: authU });
  expect.soft(rD.status(), 'user cancel delivered').toBe(400);
  const idC = await createOrder(request, ut, row.total, row.address);
  await setStatus(request, at, idC, 'canceled');
  const rC = await request.put(`${API}/api/orders/${idC}/cancel`, { headers: authU });
  expect.soft(rC.status(), 'user cancel canceled').toBe(400);
});

test('A-FR10-16 @fr10 actor gates (API)', async ({ request }) => {
  const ut = await userToken(request);
  const at = await adminLogin(request);
  const id = await createOrder(request, ut, 100000, 'HW04 FR10 actor');
  // Spec FR-12: admin API requires role=admin -> non-admin must be rejected.
  // Actual SUT never checks role -> 200 -> FAIL documents missing-authz bug.
  const r1 = await request.put(`${API}/api/admin/orders/${id}/status`, {
    data: { status: 'confirmed' },
    headers: { Authorization: `Bearer ${ut}` },
  });
  expect.soft(r1.status(), 'user calls admin endpoint (spec: 403)').toBe(403);
  const id2 = await createOrder(request, at, 100000, 'HW04 FR10 actor2');
  const r2 = await request.put(`${API}/api/admin/orders/${id2}/status`, {
    data: { status: 'confirmed' },
    headers: { Authorization: `Bearer ${ut}` },
  });
  expect.soft(r2.status(), "user touches another user's order (spec: 403)").toBe(403);
  const r3 = await request.put(`${API}/api/admin/orders/${id}/status`, {
    data: { status: 'confirmed' },
  });
  expect.soft(r3.status(), 'no token (spec: 401)').toBe(401);
});
