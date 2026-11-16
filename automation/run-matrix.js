import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';

const cli = fileURLToPath(new URL('./node_modules/@playwright/test/cli.js', import.meta.url));
const cases = [
  ['FR-04 Profile', 'tests/fr04-profile.spec.js', 'fr04-profile'],
  ['FR-09 Coupons', 'tests/fr09-coupon.spec.js', 'fr09-coupon'],
  ['FR-15 Product CRUD', 'tests/fr15-products.spec.js', 'fr15-products'],
];
const browsers = ['chromium', 'firefox', 'webkit'];
const results = [];

for (const [feature, file, slug] of cases) {
  for (const browser of browsers) {
    const reportName = `${slug}-${browser}`;
    console.log(`\n=== ${feature} / ${browser} ===`);
    const result = spawnSync(process.execPath, [cli, 'test', file, `--project=${browser}`, '--workers=1'], {
      cwd: path.dirname(fileURLToPath(import.meta.url)),
      stdio: 'inherit',
      env: { ...process.env, REPORT_NAME: reportName },
    });
    let counts = null;
    const jsonPath = new URL(`./reports/${reportName}/results.json`, import.meta.url);
    if (fs.existsSync(jsonPath)) {
      const report = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
      counts = { passed: report.stats.expected, failed: report.stats.unexpected, skipped: report.stats.skipped, flaky: report.stats.flaky };
    }
    results.push({ feature, browser, report: `reports/${reportName}/index.html`, counts, exitCode: result.status ?? 1 });
  }
}

fs.writeFileSync(new URL('./matrix-results.json', import.meta.url), JSON.stringify({ generatedAt: new Date().toISOString(), studentId: process.env.STUDENT_ID || '23120102', results }, null, 2));
console.log('\nMatrix finished. See matrix-results.json and each reports/<feature>-<browser>/index.html.');
if (results.some(result => result.exitCode !== 0)) process.exitCode = 1;
