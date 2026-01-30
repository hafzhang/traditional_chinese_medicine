import { test, expect } from '@playwright/test';

/**
 * Example E2E Test
 *
 * This is a placeholder test to verify Playwright configuration.
 * Remove this file once real E2E tests are implemented.
 */
test('example test - homepage loads', async ({ page }) => {
  // Navigate to the home page
  await page.goto('/');

  // Check that the page title contains the app name
  await expect(page).toHaveTitle(/中医/);

  // Verify the hero section is visible
  const heroTitle = page.locator('.hero-title');
  await expect(heroTitle).toBeVisible();
  await expect(heroTitle).toHaveText('中医体质识别');
});
