import { LogIn } from 'lucide-react';
import { Button } from '@agenteresolve/ui';

import { loginUrl } from '../lib/session';

/** "Entrar" button pointing at the central login app (no Clerk JS needed here). */
export function LoginButton({ returnPath }: { returnPath?: string }) {
  const href = loginUrl(returnPath ?? window.location.pathname + window.location.search);

  return (
    <Button asChild variant="outline" size="sm">
      <a href={href}>
        <LogIn />
        Entrar
      </a>
    </Button>
  );
}
