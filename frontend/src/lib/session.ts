import { setAuthTokenGetter } from './api';
import { API_BASE, LOGIN_BASE } from './env';

const TOKEN_KEY = 'ar_session_token';
const EXPIRY_KEY = 'ar_session_expires_at';

/** Gateway session token stored by the central login (null when signed out/expired). */
export function getServiceToken(): string | null {
  try {
    const token = localStorage.getItem(TOKEN_KEY);
    if (!token) {
      return null;
    }
    const expiresAt = Number(localStorage.getItem(EXPIRY_KEY) ?? '0');
    if (expiresAt > 0 && Date.now() / 1000 > expiresAt - 60) {
      clearServiceToken();
      return null;
    }
    return token;
  } catch {
    return null;
  }
}

export function storeServiceToken(token: string, expiresAt: number): void {
  try {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(EXPIRY_KEY, String(expiresAt));
  } catch {
    // Storage unavailable (private mode); calls go out unauthenticated.
  }
}

export function clearServiceToken(): void {
  try {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(EXPIRY_KEY);
  } catch {
    // Ignore storage errors on logout.
  }
}

export function isSignedIn(): boolean {
  return getServiceToken() !== null;
}

/** Central login URL; after sign-in the login app returns to `/auth/callback`. */
export function loginUrl(returnPath = '/'): string {
  const callback = `${window.location.origin}/auth/callback?next=${encodeURIComponent(returnPath)}`;
  return `${LOGIN_BASE}/?redirect=${encodeURIComponent(callback)}`;
}

/** Wire the gateway client to the browser session (call once at startup). */
export function installSessionAuth(): void {
  setAuthTokenGetter(() => Promise.resolve(getServiceToken()));
}

/** Sign out: revoke server-side (best-effort), clear local state, go home. */
export async function logout(homePath = '/'): Promise<void> {
  const token = getServiceToken();
  clearServiceToken();
  if (token) {
    try {
      await fetch(`${API_BASE}/api/auth/logout`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
      });
    } catch {
      // Logout stays best-effort; the local session is already gone.
    }
  }
  window.location.assign(homePath);
}
