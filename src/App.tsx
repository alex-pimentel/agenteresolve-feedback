import { Route, Routes } from 'react-router-dom';

import { NotFoundPage } from './pages/NotFoundPage';
import { ToolPage } from './pages/ToolPage';

export function App() {
  return (
    <Routes>
      <Route path="/" element={<ToolPage slug="feedback" />} />
      <Route path="/:slug" element={<ToolPage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
