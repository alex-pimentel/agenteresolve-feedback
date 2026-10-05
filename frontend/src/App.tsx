import { Route, Routes } from 'react-router-dom';
import { installSessionAuth } from './lib/session';
import { AuthCallback } from './pages/AuthCallback';

import { NotFoundPage } from './pages/NotFoundPage';
import { ToolPage } from './pages/ToolPage';

installSessionAuth();

export function App() {
  return (
    <Routes>
      <Route path="/" element={<ToolPage slug="feedback" />} />
      <Route path="/auth/callback" element={<AuthCallback />} />
      <Route path="/:slug" element={<ToolPage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
