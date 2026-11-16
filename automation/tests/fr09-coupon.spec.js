import { test, expect } from '@playwright/test';
import cases from '../data/fr09-coupon.json' with { type: 'json' };

test.beforeEach(({}, testInfo) => {
  testInfo.annotations.push({ type: 'Feature', description: 'FR-09 Coupons' });
  testInfo.annotations.push({ type: `Run by: ${process.env.STUDENT_ID || '23120102'}`, description: new Date().toISOString() });
});

async function openCheckout(page, row) {
  if (row.error !== 'Vui lòng đăng nhập') await page.addInitScript(() => localStorage.setItem('token', 'hw04-test-token'));
  await page.route('**/api/users/me', route => route.fulfill({ json: { id: 501, name: 'Test User', email: 'test@example.test' } }));
  await page.route('**/api/apply-coupon', async route => {
    const body = route.request().postDataJSON();
    if (row.error === 'empty') return route.fulfill({ status: 400, json: { error: 'empty' } });
    if (!row.ok) return route.fulfill({ status: 400, json: { error: row.error } });
    return route.fulfill({ json: { message: 'Áp dụng mã thành công', coupon_id: 1, discount_amount: row.discount, final_amount: row.final, receivedCode: body.code } });
  });
  await page.goto('/checkout');
  await expect(page.getByRole('heading', { name: 'Xác Nhận Đơn Hàng' })).toBeVisible();
  await page.locator('input[type="number"]').fill(String(row.total));
}

for (const row of cases) {
  test(`${row.id}: coupon ${row.code || '(blank)'}`, async ({ page }) => {
    await openCheckout(page, row);
    let submittedCode;
    page.on('request', request => {
      if (request.url().includes('/api/apply-coupon')) {
        submittedCode = request.postDataJSON().code;
      }
    });
    if (!row.code) {
      await expect(page.getByRole('button', { name: 'Áp dụng' })).toBeDisabled();
      return;
    }
    await page.getByPlaceholder('Nhập mã giảm giá...').fill(row.code);
    await page.getByRole('button', { name: 'Áp dụng' }).click();
    await expect.poll(() => submittedCode, { timeout: 1000 }).toBe(row.code.toUpperCase());
    if (row.ok) {
      expect(row.total - row.discount).toBe(row.final);
      await expect(page.getByText('Tiết kiệm:')).toBeVisible();
      await expect(page.getByText(`${row.discount.toLocaleString()} ₫`, { exact: true })).toBeVisible();
      await expect(page.getByText(`${row.final.toLocaleString()} ₫`, { exact: true }).last()).toBeVisible();
      if (row.code.toLowerCase() === 'save10') await expect(page.getByText('SAVE10', { exact: true })).toHaveCount(0);
    } else {
      await expect(page.getByText(row.error)).toBeVisible();
    }
  });
}
