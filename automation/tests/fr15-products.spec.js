import { test, expect } from '@playwright/test';
import cases from '../data/fr15-products.json' with { type: 'json' };

test.beforeEach(({}, testInfo) => testInfo.annotations.push({ type: `Run by: ${process.env.STUDENT_ID || '23120102'}`, description: new Date().toISOString() }));

const initialProducts = [
  { id: 11, name: 'Existing Alpha', price: 10000, description: 'alpha', imageUrl: '', category_id: 1 },
  { id: 12, name: 'Existing Beta', price: 20000, description: 'beta', imageUrl: '', category_id: 1 },
];

async function openAdmin(page, noCategories = false) {
  await page.route('**/api/login', route => route.fulfill({ json: { token: 'admin-token', user: { id: 1, role: 'admin' } } }));
  await page.route('**/api/admin/**', route => route.fulfill({ json: [] }));
  await page.route('**/api/products', route => route.request().method() === 'GET' ? route.fulfill({ json: initialProducts }) : route.fulfill({ json: { id: 90 } }));
  await page.route('**/api/categories', route => route.fulfill({ json: noCategories ? [] : [{ id: 1, name: 'Điện tử' }] }));
  await page.route('**/api/products/*', route => route.fulfill({ json: { message: 'ok' } }));
  await page.goto('http://127.0.0.1:5174');
  await page.getByPlaceholder('Email').fill('admin@eshop.com');
  await page.getByPlaceholder('Password').fill('admin123');
  await page.getByRole('button', { name: 'Login' }).click();
  await page.getByText('Sản phẩm', { exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Quản lý Sản phẩm' })).toBeVisible();
}

for (const row of cases) {
  test(`${row.id}: product CRUD input ${row.valid ? 'accepted' : 'rejected'}`, async ({ page }) => {
    await openAdmin(page, Boolean(row.noCategory));
    const nameValue = row.nameLength ? 'N'.repeat(row.nameLength) : row.name;
    await page.getByPlaceholder('Tên sản phẩm').fill(nameValue);
    await page.getByPlaceholder('Giá tiền').fill(row.price);
    if (row.noCategory) await expect(page.locator('select option')).toHaveCount(0);
    let created = false;
    page.on('request', request => { if (request.url().endsWith('/api/products') && request.method() === 'POST') created = true; });
    await page.getByRole('button', { name: 'Lưu sản phẩm' }).click();
    if (row.valid) {
      await expect.poll(() => created, { timeout: 1000 }).toBe(true);
    } else if (!row.name) {
      await expect(page.getByPlaceholder('Tên sản phẩm')).toBeFocused();
    } else if (!row.price || Number(row.price) <= 0 || Number.isNaN(Number(row.price))) {
      await expect.poll(() => created, { timeout: 1000 }).toBe(false);
    } else {
      await expect.poll(() => created, { timeout: 1000 }).toBe(false);
    }
  });
}

test('FR15-13: editing one product does not rename other products in the table', async ({ page }) => {
  await openAdmin(page);
  const alpha = page.getByRole('row').filter({ hasText: 'Existing Alpha' });
  await alpha.getByRole('button', { name: 'Sửa' }).click();
  await page.getByPlaceholder('Tên sản phẩm').fill('Updated Alpha');
  await page.getByRole('button', { name: 'Lưu sản phẩm' }).click();
  await expect(page.getByRole('row').filter({ hasText: 'Existing Beta' })).toContainText('Existing Beta', { timeout: 1000 });
});
