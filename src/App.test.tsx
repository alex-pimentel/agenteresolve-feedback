import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it } from 'vitest';

import { App } from './App';

function renderAt(path: string) {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <App />
    </MemoryRouter>,
  );
}

describe('App', () => {
  it('renders the FeedbackClassifier tool shell at /', () => {
    renderAt('/');
    expect(document.querySelector('[data-slot="service-shell"]')).toBeTruthy();
    expect(screen.getByRole('heading', { name: 'FeedbackClassifier' })).toBeInTheDocument();
  });

  it('renders the not-found page for unknown routes', () => {
    renderAt('/a/b/c');
    expect(screen.getByRole('heading', { name: 'Ferramenta não encontrada' })).toBeInTheDocument();
  });
});
