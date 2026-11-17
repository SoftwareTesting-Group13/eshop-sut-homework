import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
// tests/helpers -> ncuong root -> data/
const ROOT = join(here, '..', '..');

export function loadJson<T>(name: string): T {
  const raw = readFileSync(join(ROOT, 'data', name), 'utf-8');
  return JSON.parse(raw) as T;
}

export function uniqueSuffix(projectName: string): string {
  return `${Date.now()}-${projectName}`;
}
