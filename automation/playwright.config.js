import { defineConfig } from '@playwright/test';

const runBy = process.env.STUDENT_ID || '23120102';
const timestamp = new Date().toISOString();

export default defineConfig({
  testDir: './tests',
  fullyParallel: false,
  retries: 0,
  reporter: [
    ['html', { outputFolder: `reports/${process.env.REPORT_NAME || 'all'}`, open: 'never' }],
    ['json', { outputFile: `reports/${process.env.REPORT_NAME || 'all'}/results.json` }],
  ],
  use: {
    baseURL: 'http://127.0.0.1:5173',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    browserName: undefined,
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'firefox', use: { browserName: 'firefox' } },
    { name: 'webkit', use: { browserName: 'webkit' } },
  ],
  metadata: { runBy: `Run by: ${runBy}`, generatedAt: timestamp },
  webServer: [
    { command: 'npm run dev -- --host 127.0.0.1 --port 5173 --strictPort', cwd: '../frontend-web', url: 'http://127.0.0.1:5173', reuseExistingServer: false },
    { command: 'npm run dev -- --host 127.0.0.1 --port 5174 --strictPort', cwd: '../frontend-admin', url: 'http://127.0.0.1:5174', reuseExistingServer: false },
  ],
});
