import { expect, test } from '@playwright/test';

test('loads the FeedbackClassifier tool directly at the root', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByRole('heading', { name: 'FeedbackClassifier' }).first()).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Entrada' })).toBeVisible();
  await expect(page.getByRole('button', { name: /processar/i })).toBeDisabled();
});

test('shows the expected input control', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByLabel('Texto')).toBeVisible();
});

test('unknown route shows not found', async ({ page }) => {
  await page.goto('/rota-inexistente-xyz');
  await expect(page.getByText(/n[ãa]o encontrad/i).first()).toBeVisible();
});
