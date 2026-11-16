import { test, expect } from '@playwright/test';
import cases from '../data/fr04-profile.json' with { type: 'json' };

test.beforeEach(({}, testInfo) => testInfo.annotations.push({ type: `Run by: ${process.env.STUDENT_ID || '23120102'}`, description: new Date().toISOString() }));

async function openProfile(page) {
  await page.addInitScript(() => localStorage.setItem('token', 'hw04-test-token'));
  await page.route('**/api/users/me', async route => route.request().method() === 'GET'
    ? route.fulfill({ json: { id: 501, name: 'Test User', email: 'test@example.test', phone: '0911111111', shipping_address: 'Old address' } })
    : route.fulfill({ json: { message: 'Profile updated' } }));
  await page.route('**/api/orders/my-orders', route => route.fulfill({ json: [] }));
  page.dialogMessage = '';
  page.on('dialog', dialog => { page.dialogMessage = dialog.message(); dialog.accept(); });
  await page.goto('/profile');
  await expect(page.getByRole('heading', { name: 'Hồ sơ của bạn' })).toBeVisible();
}

for (const row of cases) {
  test(`${row.id}: profile data ${row.valid ? 'accepted' : 'rejected'}`, async ({ page }) => {
    await openProfile(page);
    const fields = page.locator('form input, form textarea');
    const name = fields.nth(1);
    const phone = fields.nth(2);
    const address = fields.nth(3);
    if (row.name) await name.fill(row.name);
    else await name.fill('');
    await phone.fill(row.phone);
    await address.fill(row.address);
    const email = page.locator('input[disabled]');
    await expect(email).toHaveValue('test@example.test');
    await expect(email).toBeDisabled();

    let submittedBody;
    page.on('request', request => {
      if (request.url().includes('/api/users/me') && request.method() === 'PUT') {
        submittedBody = request.postDataJSON();
      }
    });
    await page.getByRole('button', { name: 'Cập nhật' }).click();
    const validAccordingToSpec = row.valid && row.phone.startsWith('0') && /^0\d{9,10}$/.test(row.phone);
    if (validAccordingToSpec) {
      await expect.poll(() => submittedBody, { timeout: 1000 }).toBeTruthy();
      expect(submittedBody).toMatchObject({ name: row.name, phone: row.phone, shipping_address: row.address });
      expect(submittedBody).not.toHaveProperty('email');
      await expect(page.getByRole('heading', { name: 'Lịch sử đơn hàng' })).toBeVisible();
    } else if (!row.name) {
      await expect(name).toBeFocused();
    } else {
      await expect.poll(() => page.dialogMessage, { timeout: 1000 }).toMatch(/Số điện thoại không hợp lệ/);
      expect(submittedBody).toBeUndefined();
    }
  });
}

test('FR04-13: unauthenticated user is asked to sign in', async ({ page }) => {
  await page.goto('/profile');
  await expect(page.getByText('Vui lòng đăng nhập')).toBeVisible();
});
