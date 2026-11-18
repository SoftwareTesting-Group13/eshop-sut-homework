import type { APIRequestContext } from '@playwright/test';

// Shared API login helpers (env-overridable credentials, no test data here).
export const API = process.env.API_URL ?? 'http://localhost:3000';
export const ADMIN_EMAIL = process.env.ADMIN_EMAIL ?? 'admin@eshop.com';
export const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD ?? 'Admin123!';
export const USER_EMAIL = process.env.USER_EMAIL ?? 'test@eshop.com';
export const USER_PASSWORD = process.env.USER_PASSWORD ?? 'Test1234!';

export async function apiLogin(
  request: APIRequestContext,
  email: string,
  password: string,
): Promise<string> {
  const res = await request.post(`${API}/api/login`, { data: { email, password } });
  if (!res.ok()) throw new Error(`apiLogin failed for ${email}: ${res.status()}`);
  return (await res.json()).token as string;
}

export async function adminToken(request: APIRequestContext): Promise<string> {
  return apiLogin(request, ADMIN_EMAIL, ADMIN_PASSWORD);
}

export async function userToken(request: APIRequestContext): Promise<string> {
  return apiLogin(request, USER_EMAIL, USER_PASSWORD);
}

export async function authHeaders(request: APIRequestContext) {
  return { Authorization: `Bearer ${await adminToken(request)}` };
}
