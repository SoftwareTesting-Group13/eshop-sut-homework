import { defineConfig, devices } from '@playwright/test';

const STUDENT_ID = process.env.STUDENT_ID ?? '23120223';
const ISO = new Date().toISOString();
const FEATURE = process.env.FEATURE ?? 'suite';
const BROWSER = process.env.BROWSER ?? 'chromium';

export default defineConfig({
  testDir: './tests',
  fullyParallel: false,
  retries: 0,
  // Top-level metadata IS embedded into report.json and shown in the
  // HTML report's Metadata tab (reporter-level title/metadata are ignored).
  metadata: {
    'Run by': STUDENT_ID,
    'ISO timestamp': ISO,
    Feature: FEATURE,
    Browser: BROWSER,
  },
  reporter: [
    ['list'],
    [
      'html',
      {
        outputFolder: `reports/html/${FEATURE}-${BROWSER}`,
        title: `Run by: ${STUDENT_ID}`,
        open: 'never',
      },
    ],
  ],
  use: {
    baseURL: process.env.WEB_URL ?? 'http://localhost:5173',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
});
