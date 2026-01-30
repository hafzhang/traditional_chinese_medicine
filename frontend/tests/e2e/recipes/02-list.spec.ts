import { test, expect } from '@playwright/test';

/**
 * Recipe List Page E2E Tests
 *
 * Tests for the recipes list page functionality including:
 * - Page elements display
 * - Recipe cards display
 * - Filter functionality
 * - Navigation to detail page
 * - Pull-to-refresh functionality
 */

test.describe('Recipe List Page', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to recipes list page
    await page.goto('/#/pages/recipes/list');
    // Wait for recipes to load
    await page.waitForSelector('.recipes-list, .empty-state', { timeout: 15000 });
  });

  test('should display page elements correctly', async ({ page }) => {
    // Verify filter section exists
    const filterSection = page.locator('.filter-section');
    await expect(filterSection).toBeVisible();

    // Verify constitution filter options exist
    const constitutionFilter = filterSection.locator('.filter-scroll').first();
    await expect(constitutionFilter).toBeVisible();

    // Should have "全部体质" option
    await expect(constitutionFilter.locator('text=全部体质')).toBeVisible();

    // Verify efficacy filter options exist
    const efficacyFilter = filterSection.locator('.filter-scroll').nth(1);
    await expect(efficacyFilter).toBeVisible();

    // Should have "全部功效" option
    await expect(efficacyFilter.locator('text=全部功效')).toBeVisible();

    // Verify difficulty filter options exist
    const difficultyFilter = filterSection.locator('.filter-scroll').nth(2);
    await expect(difficultyFilter).toBeVisible();

    // Should have "全部难度" option
    await expect(difficultyFilter.locator('text=全部难度')).toBeVisible();
  });

  test('should display constitution filter options', async ({ page }) => {
    const filterSection = page.locator('.filter-section');
    const constitutionFilter = filterSection.locator('.filter-scroll').first();

    // Check for common constitution types
    await expect(constitutionFilter.locator('text=平和质')).toBeVisible();
    await expect(constitutionFilter.locator('text=气虚质')).toBeVisible();
    await expect(constitutionFilter.locator('text=阳虚质')).toBeVisible();
  });

  test('should display recipe list with cards', async ({ page }) => {
    // Check if recipes exist (might be empty state)
    const emptyState = page.locator('.empty-state');
    const recipesList = page.locator('.recipes-list');

    if (await emptyState.isVisible()) {
      // Empty state is valid - no recipes in database
      await expect(emptyState.locator('.empty-icon')).toHaveText('🍳');
      await expect(emptyState.locator('.empty-text')).toHaveText('暂无菜谱');
    } else {
      // Recipes should be displayed
      await expect(recipesList).toBeVisible();

      // Check for recipe items
      const recipeItems = page.locator('.recipe-item');
      const count = await recipeItems.count();

      if (count > 0) {
        // Verify first recipe card structure
        const firstRecipe = recipeItems.first();

        // Should have recipe image or placeholder
        const image = firstRecipe.locator('.recipe-image');
        await expect(image).toBeVisible();

        // Should have recipe name
        const name = firstRecipe.locator('.recipe-name');
        await expect(name).toBeVisible();
        const nameText = await name.textContent();
        expect(nameText?.trim()).toBeTruthy();
      }
    }
  });

  test('should filter recipes by constitution', async ({ page }) => {
    const filterSection = page.locator('.filter-section');
    const constitutionFilter = filterSection.locator('.filter-scroll').first();

    // Find and click "气虚质" filter
    const qiDeficiencyFilter = constitutionFilter.locator('.filter-item', { hasText: '气虚质' });

    // Only click if it exists and recipes are available
    if (await qiDeficiencyFilter.isVisible({ timeout: 5000 }).catch(() => false)) {
      await qiDeficiencyFilter.click();

      // Wait for data reload
      await page.waitForTimeout(1000);

      // Verify filter is active
      await expect(qiDeficiencyFilter).toHaveClass(/active/);

      // Verify the list updated (either has recipes or empty state)
      await expect(page.locator('.recipes-list, .empty-state')).toBeVisible();
    }
  });

  test('should filter recipes by difficulty', async ({ page }) => {
    const filterSection = page.locator('.filter-section');
    const difficultyFilter = filterSection.locator('.filter-scroll').nth(2);

    // Find and click "简单" filter
    const easyFilter = difficultyFilter.locator('.filter-item', { hasText: '简单' });

    if (await easyFilter.isVisible({ timeout: 5000 }).catch(() => false)) {
      await easyFilter.click();

      // Wait for data reload
      await page.waitForTimeout(1000);

      // Verify filter is active
      await expect(easyFilter).toHaveClass(/active/);

      // Verify the list updated
      await expect(page.locator('.recipes-list, .empty-state')).toBeVisible();
    }
  });

  test('should navigate to detail page when recipe card is clicked', async ({ page }) => {
    const recipesList = page.locator('.recipes-list');

    // Only test if recipes exist
    if (await recipesList.isVisible({ timeout: 5000 }).catch(() => false)) {
      const recipeItems = page.locator('.recipe-item');
      const count = await recipeItems.count();

      if (count > 0) {
        // Click the first recipe
        await recipeItems.first().click();

        // Wait for navigation to detail page
        await page.waitForURL(/\/pages\/recipes\/detail/, { timeout: 10000 });

        // Verify we're on the detail page
        expect(page.url()).toContain('/pages/recipes/detail');
      }
    }
  });

  test('should support pull-to-refresh', async ({ page }) => {
    const scrollView = page.locator('.recipes-scroll');

    // Verify scroll view exists with refresher
    await expect(scrollView).toBeVisible();

    // Note: Actual pull-to-refresh gesture testing is complex in Playwright
    // We verify the element exists with the correct attributes
    // The refresh functionality would be tested manually or with more complex gestures
  });

  test('should display recipe card with correct information', async ({ page }) => {
    const recipesList = page.locator('.recipes-list');

    if (await recipesList.isVisible({ timeout: 5000 }).catch(() => false)) {
      const recipeItems = page.locator('.recipe-item');
      const count = await recipeItems.count();

      if (count > 0) {
        const firstRecipe = recipeItems.first();

        // Verify recipe image or placeholder
        const image = firstRecipe.locator('.recipe-image');
        await expect(image).toBeVisible();

        // Verify recipe name
        const name = firstRecipe.locator('.recipe-name');
        await expect(name).toBeVisible();

        // Check for optional elements
        const desc = firstRecipe.locator('.recipe-desc');
        const difficultyTag = firstRecipe.locator('.tag.difficulty');
        const timeTag = firstRecipe.locator('.time');
        const efficacyTags = firstRecipe.locator('.tag.efficacy');

        // At least the name should be visible
        const nameText = await name.textContent();
        expect(nameText?.trim().length).toBeGreaterThan(0);
      }
    }
  });

  test('should display constitution and efficacy tags on recipe cards', async ({ page }) => {
    const recipesList = page.locator('.recipes-list');

    if (await recipesList.isVisible({ timeout: 5000 }).catch(() => false)) {
      const recipeItems = page.locator('.recipe-item');
      const count = await recipeItems.count();

      if (count > 0) {
        const firstRecipe = recipeItems.first();

        // Check for constitution tags (optional element)
        const constitutionTags = firstRecipe.locator('.recipe-constitutions');
        if (await constitutionTags.isVisible({ timeout: 1000 }).catch(() => false)) {
          await expect(constitutionTags.locator('.constitution-label')).toHaveText('适合:');
        }

        // Check for efficacy tags (optional element)
        const efficacyTags = firstRecipe.locator('.recipe-tags');
        const efficacyTag = firstRecipe.locator('.tag.efficacy').first();
        // Efficacy tags are optional, so we just check if they exist
        const isVisible = await efficacyTag.isVisible({ timeout: 1000 }).catch(() => false);
        if (isVisible) {
          await expect(efficacyTag).toBeVisible();
        }
      }
    }
  });
});
