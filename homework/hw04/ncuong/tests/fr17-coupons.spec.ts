import { test, expect, type APIRequestContext, type Page } from '@playwright/test';
import { loadJson, uniqueSuffix } from './helpers/json-loader';
import { API, adminToken, authHeaders } from './helpers/eshop-api';

type CouponRow = {
  id: string;
  type: string;
  code: string;
  discountType: string;
  discountValue: number | string;
  minOrderAmount: number;
  expiredAt: string;
  maxUsesPerUser: number;
  expected: string;
};

const rows = loadJson<CouponRow[]>('fr17-coupons.json');
const byId = (id: string): CouponRow => rows.find((r) => r.id === id)!;

const ADMIN_URL = process.env.ADMIN_URL ?? 'http://localhost:5174';

function uniqueCode(base: string, projectName: string): string {
  if (!base || !base.trim() || base === '__OMITTED__') return base;
  return `${base}-${uniqueSuffix(projectName)}`.toUpperCase();
}

async function openCoupons(page: Page, request: APIRequestContext) {
  const token = await adminToken(request);
  await page.addInitScript(
    (t: string) => localStorage.setItem('adminToken', t),
    token,
  );
  await page.goto(ADMIN_URL);
  await page.getByText('Mã Giảm Giá', { exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Quản lý Mã Giảm Giá' })).toBeVisible();
}

function couponRow(page: Page, code: string) {
  return page.locator('table tbody tr', { has: page.getByText(code, { exact: true }) });
}

async function rowCount(page: Page): Promise<number> {
  return page.locator('table tbody tr').count();
}

async function fillCouponForm(
  page: Page,
  f: { code: string; type: string; discount: number | string; min: number; expired: string; max: number },
) {
  await page.getByPlaceholder('Mã coupon (VD: SAVE10)').fill(f.code);
  await page.getByRole('combobox').selectOption(f.type);
  const discountPlaceholder = f.type === 'percent' ? 'Giá trị % (VD: 10)' : 'Số tiền (VD: 50000)';
  await page.getByPlaceholder(discountPlaceholder).fill(String(f.discount));
  await page.getByPlaceholder('Đơn tối thiểu (₫)').fill(String(f.min));
  await page.getByPlaceholder('Ngày hết hạn').fill(f.expired);
  await page.getByPlaceholder('Số lần dùng tối đa/người').fill(String(f.max));
}

async function submitCoupon(page: Page) {
  const respPromise = page.waitForResponse(
    (r) => r.url().includes('/api/admin/coupons') && r.request().method() === 'POST',
  );
  await page.getByRole('button', { name: 'Tạo mã' }).click();
  return respPromise;
}

async function deleteByCode(request: APIRequestContext, code: string | null) {
  const headers = await authHeaders(request);
  const list = (await (
    await request.get(`${API}/api/coupons`, { headers })
  ).json()) as Array<{ id: number; code: string | null }>;
  for (const c of list.filter((x) => x.code === code)) {
    await request.delete(`${API}/api/admin/coupons/${c.id}`, { headers });
  }
}

test('A-FR17-01 @fr17 tao percent hop le', async ({ page, request }, testInfo) => {
  const row = byId('A-FR17-01');
  const code = uniqueCode(row.code, testInfo.project.name);
  try {
    await openCoupons(page, request);
    await fillCouponForm(page, {
      code, type: row.discountType, discount: row.discountValue,
      min: row.minOrderAmount, expired: row.expiredAt, max: row.maxUsesPerUser,
    });
    const resp = await submitCoupon(page);
    expect(resp.status()).toBe(200);
    const r = couponRow(page, code);
    await expect(r.getByText(code, { exact: true })).toBeVisible();
    await expect(r.getByText('Phần trăm')).toBeVisible();
    await expect(r.getByText('10%')).toBeVisible();
    await expect(r.getByText('100,000 ₫')).toBeVisible();
    await expect(r.getByText('2099-12-31')).toBeVisible();
    await expect(r.getByText('1 lần')).toBeVisible();
  } finally {
    await deleteByCode(request, code);
  }
});

test('A-FR17-02 @fr17 tao fixed hop le', async ({ page, request }, testInfo) => {
  const row = byId('A-FR17-02');
  const code = uniqueCode(row.code, testInfo.project.name);
  try {
    await openCoupons(page, request);
    await fillCouponForm(page, {
      code, type: row.discountType, discount: row.discountValue,
      min: row.minOrderAmount, expired: row.expiredAt, max: row.maxUsesPerUser,
    });
    const resp = await submitCoupon(page);
    expect(resp.status()).toBe(200);
    const r = couponRow(page, code);
    await expect(r.getByText('Cố định')).toBeVisible();
    await expect(r.getByText('50,000 ₫')).toBeVisible();
  } finally {
    await deleteByCode(request, code);
  }
});

test('A-FR17-03 @fr17 trung ma SAVE10 bi tu choi', async ({ page, request }) => {
  const row = byId('A-FR17-03');
  await openCoupons(page, request);
  const before = await rowCount(page);
  await fillCouponForm(page, {
    code: row.code, type: row.discountType, discount: row.discountValue,
    min: row.minOrderAmount, expired: row.expiredAt, max: row.maxUsesPerUser,
  });
  const dialogPromise = page.waitForEvent('dialog');
  await page.getByRole('button', { name: 'Tạo mã' }).click();
  const dialog = await dialogPromise;
  expect(dialog.message()).toContain('Lỗi');
  await dialog.dismiss();
  expect(await rowCount(page)).toBe(before);
});

test('A-FR17-04 @fr17 ma toan khoang trang bi tu choi', async ({ page, request }) => {
  const row = byId('A-FR17-04');
  await openCoupons(page, request);
  const before = await rowCount(page);
  try {
    await fillCouponForm(page, {
      code: row.code, type: row.discountType, discount: row.discountValue,
      min: row.minOrderAmount, expired: row.expiredAt, max: row.maxUsesPerUser,
    });
    const resp = await submitCoupon(page);
    // Spec ASSUMED: blank code rejected. Actual SUT inserts it -> FAIL documents bug.
    expect(resp.status()).toBeGreaterThanOrEqual(400);
    expect(await rowCount(page)).toBe(before);
  } finally {
    await deleteByCode(request, row.code);
  }
});

test('A-FR17-05 @fr17 discount_value 0 bi tu choi', async ({ page, request }, testInfo) => {
  const row = byId('A-FR17-05');
  const code = uniqueCode(row.code, testInfo.project.name);
  try {
    await openCoupons(page, request);
    const before = await rowCount(page);
    await fillCouponForm(page, {
      code, type: row.discountType, discount: row.discountValue,
      min: row.minOrderAmount, expired: row.expiredAt, max: row.maxUsesPerUser,
    });
    const resp = await submitCoupon(page);
    expect(resp.status()).toBeGreaterThanOrEqual(400); // actual 200 -> FAIL documents bug
    expect(await rowCount(page)).toBe(before);
  } finally {
    await deleteByCode(request, code);
  }
});

test('A-FR17-06 @fr17 discount_value -1 bi tu choi', async ({ page, request }, testInfo) => {
  const row = byId('A-FR17-06');
  const code = uniqueCode(row.code, testInfo.project.name);
  try {
    await openCoupons(page, request);
    const before = await rowCount(page);
    await fillCouponForm(page, {
      code, type: row.discountType, discount: row.discountValue,
      min: row.minOrderAmount, expired: row.expiredAt, max: row.maxUsesPerUser,
    });
    const resp = await submitCoupon(page);
    expect(resp.status()).toBeGreaterThanOrEqual(400); // actual 200 -> FAIL documents bug
    expect(await rowCount(page)).toBe(before);
  } finally {
    await deleteByCode(request, code);
  }
});

test('A-FR17-07 @fr17 discount_value 1 tao duoc', async ({ page, request }, testInfo) => {
  const row = byId('A-FR17-07');
  const code = uniqueCode(row.code, testInfo.project.name);
  try {
    await openCoupons(page, request);
    await fillCouponForm(page, {
      code, type: row.discountType, discount: row.discountValue,
      min: row.minOrderAmount, expired: row.expiredAt, max: row.maxUsesPerUser,
    });
    const resp = await submitCoupon(page);
    expect(resp.status()).toBe(200);
    await expect(couponRow(page, code).getByText('1%')).toBeVisible();
  } finally {
    await deleteByCode(request, code);
  }
});

test('A-FR17-08 @fr17 percent 150 bi tu choi', async ({ page, request }, testInfo) => {
  const row = byId('A-FR17-08');
  const code = uniqueCode(row.code, testInfo.project.name);
  try {
    await openCoupons(page, request);
    const before = await rowCount(page);
    await fillCouponForm(page, {
      code, type: row.discountType, discount: row.discountValue,
      min: row.minOrderAmount, expired: row.expiredAt, max: row.maxUsesPerUser,
    });
    const resp = await submitCoupon(page);
    // Spec: percent max 100. Actual SUT inserts 150% -> FAIL documents bug.
    expect(resp.status()).toBeGreaterThanOrEqual(400);
    expect(await rowCount(page)).toBe(before);
  } finally {
    await deleteByCode(request, code);
  }
});

test('A-FR17-09 @fr17 het han qua khu van tao duoc', async ({ page, request }, testInfo) => {
  const row = byId('A-FR17-09');
  const code = uniqueCode(row.code, testInfo.project.name);
  try {
    await openCoupons(page, request);
    await fillCouponForm(page, {
      code, type: row.discountType, discount: row.discountValue,
      min: row.minOrderAmount, expired: row.expiredAt, max: row.maxUsesPerUser,
    });
    const resp = await submitCoupon(page);
    expect(resp.status()).toBe(200);
    const r = couponRow(page, code);
    await expect(r.getByText('Hết hạn')).toBeVisible();
  } finally {
    await deleteByCode(request, code);
  }
});

test('A-FR17-10 @fr17 min_order 0 tao duoc', async ({ page, request }, testInfo) => {
  const row = byId('A-FR17-10');
  const code = uniqueCode(row.code, testInfo.project.name);
  try {
    await openCoupons(page, request);
    await fillCouponForm(page, {
      code, type: row.discountType, discount: row.discountValue,
      min: row.minOrderAmount, expired: row.expiredAt, max: row.maxUsesPerUser,
    });
    const resp = await submitCoupon(page);
    expect(resp.status()).toBe(200);
    await expect(couponRow(page, code).getByText('0 ₫')).toBeVisible();
  } finally {
    await deleteByCode(request, code);
  }
});

test('A-FR17-11 @fr17 min_order 1 tao duoc', async ({ page, request }, testInfo) => {
  const row = byId('A-FR17-11');
  const code = uniqueCode(row.code, testInfo.project.name);
  try {
    await openCoupons(page, request);
    await fillCouponForm(page, {
      code, type: row.discountType, discount: row.discountValue,
      min: row.minOrderAmount, expired: row.expiredAt, max: row.maxUsesPerUser,
    });
    const resp = await submitCoupon(page);
    expect(resp.status()).toBe(200);
    await expect(couponRow(page, code).getByText('1 ₫')).toBeVisible();
  } finally {
    await deleteByCode(request, code);
  }
});

test('A-FR17-12 @fr17 min_order -1 bi tu choi', async ({ page, request }, testInfo) => {
  const row = byId('A-FR17-12');
  const code = uniqueCode(row.code, testInfo.project.name);
  try {
    await openCoupons(page, request);
    const before = await rowCount(page);
    await fillCouponForm(page, {
      code, type: row.discountType, discount: row.discountValue,
      min: row.minOrderAmount, expired: row.expiredAt, max: row.maxUsesPerUser,
    });
    const resp = await submitCoupon(page);
    expect(resp.status()).toBeGreaterThanOrEqual(400); // actual 200 -> FAIL documents bug
    expect(await rowCount(page)).toBe(before);
  } finally {
    await deleteByCode(request, code);
  }
});

test('A-FR17-13 @fr17 max_uses 2 tao duoc', async ({ page, request }, testInfo) => {
  const row = byId('A-FR17-13');
  const code = uniqueCode(row.code, testInfo.project.name);
  try {
    await openCoupons(page, request);
    await fillCouponForm(page, {
      code, type: row.discountType, discount: row.discountValue,
      min: row.minOrderAmount, expired: row.expiredAt, max: row.maxUsesPerUser,
    });
    const resp = await submitCoupon(page);
    expect(resp.status()).toBe(200);
    await expect(couponRow(page, code).getByText('2 lần')).toBeVisible();
  } finally {
    await deleteByCode(request, code);
  }
});

test('A-FR17-14 @fr17 danh sach hien seed + moi', async ({ page, request }, testInfo) => {
  const row = byId('A-FR17-14');
  const code = uniqueCode(row.code, testInfo.project.name);
  try {
    await openCoupons(page, request);
    await fillCouponForm(page, {
      code, type: row.discountType, discount: row.discountValue,
      min: row.minOrderAmount, expired: row.expiredAt, max: row.maxUsesPerUser,
    });
    const resp = await submitCoupon(page);
    expect(resp.status()).toBe(200);
    for (const seed of ['SAVE10', 'BIGBUY', 'VIP100', 'EXPIRED']) {
      await expect(page.getByText(seed, { exact: true }).first()).toBeVisible();
    }
    await expect(page.getByText(code, { exact: true })).toBeVisible();
  } finally {
    await deleteByCode(request, code);
  }
});

test('A-FR17-15 @fr17 xoa coupon', async ({ page, request }, testInfo) => {
  const row = byId('A-FR17-15');
  const code = uniqueCode(row.code, testInfo.project.name);
  await openCoupons(page, request);
  await fillCouponForm(page, {
    code, type: row.discountType, discount: row.discountValue,
    min: row.minOrderAmount, expired: row.expiredAt, max: row.maxUsesPerUser,
  });
  const created = await submitCoupon(page);
  expect(created.status()).toBe(200);
  await expect(page.getByText(code, { exact: true })).toBeVisible();
  const delPromise = page.waitForResponse(
    (r) => r.url().includes('/api/admin/coupons/') && r.request().method() === 'DELETE',
  );
  await couponRow(page, code).getByRole('button', { name: 'Xóa' }).click();
  expect((await delPromise).status()).toBe(200);
  await expect(page.getByText(code, { exact: true })).toHaveCount(0);
});

test('A-FR17-16 @fr17 thieu key code bi tu choi (API)', async ({ request }) => {
  const headers = await authHeaders(request);
  try {
    const res = await request.post(`${API}/api/admin/coupons`, {
      data: {
        type: 'percent', discount_value: 10, min_order_amount: 100000,
        expired_at: '2099-12-31', max_uses_per_user: 1,
      },
      headers,
    });
    // Spec: code is required. Actual SUT inserts NULL -> FAIL documents bug.
    expect(res.status()).toBeGreaterThanOrEqual(400);
  } finally {
    await deleteByCode(request, null);
  }
});

test('A-FR17-17 @fr17 save10 thuong bi tu choi (API)', async ({ request }) => {
  const row = byId('A-FR17-17');
  const headers = await authHeaders(request);
  try {
    const res = await request.post(`${API}/api/admin/coupons`, {
      data: {
        code: row.code, type: row.discountType, discount_value: row.discountValue,
        min_order_amount: row.minOrderAmount, expired_at: row.expiredAt,
        max_uses_per_user: row.maxUsesPerUser,
      },
      headers,
    });
    // Spec HW02: uniqueness case-insensitive. Actual SQLite UNIQUE is
    // case-sensitive -> 200 creates save10 beside SAVE10 -> FAIL documents bug.
    expect(res.status()).toBeGreaterThanOrEqual(400);
  } finally {
    await deleteByCode(request, row.code);
  }
});

test('A-FR17-18 @fr17 gia tri khong hop le bi tu choi (API)', async ({ request }, testInfo) => {
  const headers = await authHeaders(request);
  const sfx = uniqueSuffix(testInfo.project.name).toUpperCase();
  const mk = (code: string, body: Record<string, unknown>) =>
    request.post(`${API}/api/admin/coupons`, { data: { code, ...body }, headers });
  const base = { min_order_amount: 100000, expired_at: '2099-12-31', max_uses_per_user: 1 };
  const c1 = `FR17-18A-${sfx}`;
  const r1 = await mk(c1, { ...base, type: 'percentage', discount_value: 10 });
  expect.soft(r1.status(), "type='percentage'").toBeGreaterThanOrEqual(400);
  const c2 = `FR17-18B-${sfx}`;
  const r2 = await mk(c2, { ...base, type: 'percent', discount_value: 'abc' });
  expect.soft(r2.status(), "discount='abc'").toBeGreaterThanOrEqual(400);
  const c3 = `FR17-18C-${sfx}`;
  const r3 = await mk(c3, { ...base, type: 'percent', discount_value: 10, expired_at: 'not-a-date' });
  expect.soft(r3.status(), "expired='not-a-date'").toBeGreaterThanOrEqual(400);
  const c4 = `FR17-18D-${sfx}`;
  const r4 = await mk(c4, { ...base, type: 'percent', discount_value: 10, max_uses_per_user: 0 });
  expect.soft(r4.status(), 'max_uses=0').toBeGreaterThanOrEqual(400);
  for (const c of [c1, c2, c3, c4]) await deleteByCode(request, c);
});
