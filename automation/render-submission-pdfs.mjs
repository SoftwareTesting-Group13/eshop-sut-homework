import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const root = path.dirname(new URL(import.meta.url).pathname).replace(/^\/[A-Za-z]:/, match => match.slice(1));
const outputDir = path.join(root, 'output', 'pdf');
fs.mkdirSync(outputDir, { recursive: true });
const tempDir = path.join(root, '.pdf-tmp');
fs.mkdirSync(tempDir, { recursive: true });
process.env.TEMP = tempDir;
process.env.TMP = tempDir;

function escapeHtml(value) {
  return value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
}

function inline(value) {
  return escapeHtml(value)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
}

function renderMarkdown(markdown) {
  const lines = markdown.replaceAll('\r\n', '\n').split('\n');
  const html = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i].trim();
    if (!line) { i++; continue; }
    if (line.startsWith('```')) {
      const code = [];
      i++;
      while (i < lines.length && !lines[i].trim().startsWith('```')) code.push(lines[i++]);
      i++;
      html.push(`<pre><code>${escapeHtml(code.join('\n'))}</code></pre>`);
      continue;
    }
    if (line.startsWith('|')) {
      const rows = [];
      while (i < lines.length && lines[i].trim().startsWith('|')) {
        const cells = lines[i].trim().replace(/^\||\|$/g, '').split('|').map(cell => cell.trim());
        if (!cells.every(cell => /^:?-{3,}:?$/.test(cell))) rows.push(cells);
        i++;
      }
      if (rows.length) {
        const [head, ...body] = rows;
        html.push(`<table><thead><tr>${head.map(cell => `<th>${inline(cell)}</th>`).join('')}</tr></thead><tbody>${body.map(row => `<tr>${head.map((_, n) => `<td>${inline(row[n] || '')}</td>`).join('')}</tr>`).join('')}</tbody></table>`);
      }
      continue;
    }
    const heading = /^(#{1,3})\s+(.+)$/.exec(line);
    if (heading) { const level = heading[1].length; html.push(`<h${level}>${inline(heading[2])}</h${level}>`); i++; continue; }
    if (line.startsWith('> ')) {
      const quote = [];
      while (i < lines.length && lines[i].trim().startsWith('> ')) quote.push(inline(lines[i++].trim().slice(2)));
      html.push(`<blockquote>${quote.join('<br>')}</blockquote>`);
      continue;
    }
    if (line.startsWith('- ')) {
      const items = [];
      while (i < lines.length && lines[i].trim().startsWith('- ')) items.push(`<li>${inline(lines[i++].trim().slice(2))}</li>`);
      html.push(`<ul>${items.join('')}</ul>`);
      continue;
    }
    const paragraph = [line];
    i++;
    while (i < lines.length && lines[i].trim() && !/^(#{1,3})\s|^```|^\|/.test(lines[i].trim()) && !lines[i].trim().startsWith('- ') && !lines[i].trim().startsWith('> ')) paragraph.push(lines[i++].trim());
    html.push(`<p>${paragraph.map(inline).join(' ')}</p>`);
  }
  return html.join('\n');
}

const documents = [
  ['main-report.md', 'HW04 Automation Testing Report'],
  ['ai-audit.md', 'AI Audit Report'],
  ['ai-critique.md', 'AI Critique'],
];
const systemBrowsers = [
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
];
const executablePath = process.env.PDF_BROWSER_EXECUTABLE || systemBrowsers.find(candidate => fs.existsSync(candidate));
const browser = await chromium.launch({ headless: true, ...(executablePath ? { executablePath } : {}) });
try {
  for (const [source, title] of documents) {
    const markdown = fs.readFileSync(path.join(root, source), 'utf8');
    const body = renderMarkdown(markdown);
    const html = `<!doctype html><html><head><meta charset="utf-8"><title>${escapeHtml(title)}</title><style>
      @page { size: A4; margin: 18mm 17mm 18mm; }
      * { box-sizing: border-box; }
      body { font-family: Arial, 'Microsoft YaHei', sans-serif; color: #172033; font-size: 10.5pt; line-height: 1.55; }
      h1 { color: #123b63; font-size: 23pt; line-height: 1.2; margin: 0 0 19pt; padding-bottom: 8pt; border-bottom: 2px solid #1d78a8; }
      h2 { color: #155b82; font-size: 15pt; margin: 20pt 0 7pt; break-after: avoid; }
      h3 { color: #155b82; font-size: 11.5pt; margin: 15pt 0 5pt; break-after: avoid; }
      p { margin: 0 0 9pt; orphans: 3; widows: 3; }
      ul { margin: 0 0 11pt; padding-left: 20pt; }
      li { margin: 0 0 4pt; }
      table { width: 100%; border-collapse: collapse; margin: 10pt 0 14pt; font-size: 9pt; break-inside: avoid; }
      th { text-align: left; background: #e9f2f7; color: #123b63; }
      th, td { border: 1px solid #b8cbd7; padding: 6pt 7pt; vertical-align: top; }
      blockquote { border-left: 3px solid #2490b5; margin: 10pt 0 12pt; padding: 5pt 10pt; color: #38566a; background: #f4f8fa; }
      code { font-family: Consolas, monospace; font-size: 9pt; background: #f0f3f6; padding: 1pt 3pt; }
      pre { background: #f0f3f6; border: 1px solid #d6e0e7; border-radius: 4pt; padding: 8pt; white-space: pre-wrap; break-inside: avoid; }
      a { color: #075e9b; overflow-wrap: anywhere; }
      strong { color: #111d31; }
      </style></head><body>${body}</body></html>`;
    const page = await browser.newPage();
    await page.setContent(html, { waitUntil: 'load' });
    const output = path.join(outputDir, source.replace('.md', '.pdf'));
    await page.pdf({ path: output, format: 'A4', printBackground: true, displayHeaderFooter: true,
      headerTemplate: '<div></div>',
      footerTemplate: '<div style="width:100%;margin:0 17mm;color:#657487;font:8px Arial;display:flex;justify-content:space-between"><span>HW04 Automation Testing · 23120102</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
      margin: { top: '18mm', right: '17mm', bottom: '20mm', left: '17mm' } });
    const previewPath = path.join(tempDir, source.replace('.md', '-preview.png'));
    await page.screenshot({ path: previewPath, fullPage: true });
    await page.close();
    console.log(`${source} -> ${output}`);
  }
} finally {
  await browser.close();
}
