import { test, expect } from '@playwright/test';

/**
 * Navigation Entry E2E Tests
 *
 * Tests for navigation from home page to recipes list page.
 * Tests the feature navigation card on the home page.
 */

test.describe('Home Page Navigation', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to home page before each test
    await page.goto('/');
  });

  test('should display feature navigation section', async ({ page }) => {
    // Verify the features section exists
    const featuresSection = page.locator('.features-section');
    await expect(featuresSection).toBeVisible();

    // Verify section header
    const sectionTitle = page.locator('.section-title');
    await expect(sectionTitle).toBeVisible();
    await expect(sectionTitle).toHaveText('功能导航');

    const sectionDesc = page.locator('.section-desc');
    await expect(sectionDesc).toBeVisible();
    await expect(sectionDesc).toHaveText('核心功能 - 一键直达');
  });

  test('should display recipe library card with correct content', async ({ page }) => {
    // Find the recipe library card - it should have the 🍲 icon
    const recipeCard = page.locator('.feature-card').filter({
      hasText: '食谱库'
    });

    // Verify card is visible
    await expect(recipeCard).toBeVisible();

    // Verify icon
    const icon = recipeCard.locator('.feature-icon');
    await expect(icon).toBeVisible();
    await expect(icon).toHaveText('🍲');

    // Verify title
    const title = recipeCard.locator('.feature-title');
    await expect(title).toBeVisible();
    await expect(title).toHaveText('食谱库');

    // Verify description
    const desc = recipeCard.locator('.feature-desc');
    await expect(desc).toBeVisible();
    await expect(desc).toHaveText('根据体质推荐的养生食谱和食疗方案');

    // Verify action button text
    const actionText = recipeCard.locator('.action-text');
    await expect(actionText).toBeVisible();
    await expect(actionText).toHaveText('查看食谱');

    // Verify arrow icon
    const actionArrow = recipeCard.locator('.action-arrow');
    await expect(actionArrow).toBeVisible();
    await expect(actionArrow).toHaveText('→');
  });

  test('should navigate to recipes list page when card is clicked', async ({ page }) => {
    // Find and click the recipe library card
    const recipeCard = page.locator('.feature-card').filter({
      hasText: '食谱库'
    });

    // Click the card
    await recipeCard.click();

    // Wait for navigation - URL should contain /pages/recipes/list
    await page.waitForURL(/\/pages\/recipes\/list/);

    // Verify the URL
    expect(page.url()).toContain('/pages/recipes/list');

    // Verify we're on the recipes list page by checking for recipe items
    // The page might have recipe cards or a loading state
    const pageContainer = page.locator('.page-container, .recipes-list');
    await expect(pageContainer.first()).toBeVisible({ timeout: 10000 });
  });

  test('should display correct page title on recipes list page', async ({ page }) => {
    // Navigate to recipes list
    const recipeCard = page.locator('.feature-card').filter({
      hasText: '食谱库'
    });
    await recipeCard.click();

    // Wait for navigation
    await page.waitForURL(/\/pages\/recipes\/list/);

    // Check for page title - could be in uni-app navigation bar or page content
    // In H5 mode, the page title is typically in the document title
    const pageTitle = await page.title();
    expect(pageTitle).toMatch(/食谱|菜谱/);
  });
});
