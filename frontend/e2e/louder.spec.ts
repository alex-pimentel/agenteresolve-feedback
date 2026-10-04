import { expect, test } from '@playwright/test';

test('client-side Louder route surfaces the standalone app link', async ({ page }) => {
  await page.goto('/louder');
  await expect(page.getByRole('link', { name: /abrir louder/i })).toBeVisible();
});
