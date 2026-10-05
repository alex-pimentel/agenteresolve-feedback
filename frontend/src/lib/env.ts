const DEFAULT_API_BASE = '';
const DEFAULT_LOUDER_URL = 'https://louder.agenteresolve.com.br';

/** Base URL of the AI services gateway (no trailing slash). */
export const API_BASE: string = (import.meta.env.VITE_API_BASE?.trim() || DEFAULT_API_BASE).replace(
  /\/+$/,
  '',
);

/** Standalone client-side Louder app surfaced by `/louder`. */
export const LOUDER_URL: string = import.meta.env.VITE_LOUDER_URL?.trim() || DEFAULT_LOUDER_URL;

/** Central login app (the only Clerk frontend). */
export const LOGIN_BASE: string = (
  import.meta.env.VITE_LOGIN_BASE?.trim() || 'https://login.agenteresolve.com.br'
).replace(/\/+$/, '');

/** Optional Clerk publishable key; when absent the UI degrades gracefully. */
export const CLERK_PUBLISHABLE_KEY: string | undefined =
  import.meta.env.VITE_CLERK_PUBLISHABLE_KEY?.trim() || undefined;
