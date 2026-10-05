import * as React from 'react';
import { useNavigate } from 'react-router-dom';

import { storeServiceToken } from '../lib/session';
import { StateMessage } from '../components/StateMessage';

interface CallbackResult {
  error: string | null;
  next: string;
}

function processCallback(): CallbackResult {
  const hash = new URLSearchParams(window.location.hash.replace(/^#/, ''));
  const token = hash.get('access_token');
  const expiresAt = Number(hash.get('expires_at') ?? '0');
  const next = new URLSearchParams(window.location.search).get('next') ?? '/';
  const safeNext = next.startsWith('/') && !next.startsWith('//') ? next : '/';

  if (!token) {
    return { error: 'Login não concluído: token ausente. Tente entrar novamente.', next: safeNext };
  }
  storeServiceToken(token, expiresAt);
  window.location.hash = '';
  return { error: null, next: safeNext };
}

/** Landing for the central login return: stores the token fragment, then continues. */
export function AuthCallback() {
  const navigate = useNavigate();
  const [result] = React.useState<CallbackResult>(processCallback);

  React.useEffect(() => {
    if (!result.error) {
      navigate(result.next, { replace: true });
    }
  }, [navigate, result]);

  if (!result.error) {
    return null;
  }

  return (
    <div className="mx-auto max-w-md p-8">
      <StateMessage tone="error" title="Erro">
        {result.error}
      </StateMessage>
    </div>
  );
}
