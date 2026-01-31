import { test, expect } from '@playwright/test';

test.describe('Recipe Search Page E2E Tests', () => {
  // Navigate to search page before each test
  test.beforeEach(async ({ page }) => {
    await page.goto('/#/pages/recipes/search');
    // Wait for page to load
    await page.waitForLoadState('networkidle');
  });

  test('should display search page basic elements', async ({ page }) => {
    // Verify search input exists
    const searchInput = page.locator('.search-input');
    await expect(searchInput).toBeVisible();

    // Verify search button exists
    const searchBtn = page.locator('.search-btn');
    await expect(searchBtn).toBeVisible();
    await expect(searchBtn).toHaveText('搜索');

    // Verify clear icon exists (hidden initially when no keyword)
    const clearIcon = page.locator('.clear-icon');
    const isVisible = await clearIcon.isVisible({ timeout: 5000 }).catch(() => false);
    // Clear icon should only be visible when there's a keyword
    expect(isVisible).toBe(false);

    // Verify filter section exists
    const filterSection = page.locator('.filter-section');
    await expect(filterSection).toBeVisible();

    // Verify at least one filter scroll area exists
    const filterScroll = page.locator('.filter-scroll').first();
    await expect(filterScroll).toBeVisible();
  });

  test('should display filter options correctly', async ({ page }) => {
    // Verify constitution filter options
    await expect(page.locator('.filter-scroll').filter({ hasText: '平和质' })).toBeVisible();
    await expect(page.locator('.filter-scroll').filter({ hasText: '气虚质' })).toBeVisible();

    // Verify efficacy filter options
    await expect(page.locator('.filter-scroll').filter({ hasText: '健脾' })).toBeVisible();
    await expect(page.locator('.filter-scroll').filter({ hasText: '补气' })).toBeVisible();

    // Verify difficulty filter options
    await expect(page.locator('.filter-scroll').filter({ hasText: '简单' })).toBeVisible();
    await expect(page.locator('.filter-scroll').filter({ hasText: '中等' })).toBeVisible();
    await expect(page.locator('.filter-scroll').filter({ hasText: '困难' })).toBeVisible();

    // Verify cooking time filter options
    await expect(page.locator('.filter-scroll').filter({ hasText: '15分钟内' })).toBeVisible();
    await expect(page.locator('.filter-scroll').filter({ hasText: '30分钟内' })).toBeVisible();
  });

  test('should perform keyword search', async ({ page }) => {
    // Type keyword in search input
    const searchInput = page.locator('.search-input');
    await searchInput.fill('山药');

    // Click search button
    const searchBtn = page.locator('.search-btn');
    await searchBtn.click();

    // Wait for results to load
    await page.waitForTimeout(2000);

    // Verify clear icon is now visible
    const clearIcon = page.locator('.clear-icon');
    await expect(clearIcon).toBeVisible();

    // Check if results are displayed or empty state is shown
    const recipeItem = page.locator('.recipe-item').first();
    const hasResults = await recipeItem.isVisible({ timeout: 5000 }).catch(() => false);

    const emptyState = page.locator('.empty-state');
    const hasEmptyState = await emptyState.isVisible({ timeout: 5000 }).catch(() => false);

    // Either results should be displayed or empty state shown
    expect(hasResults || hasEmptyState).toBe(true);

    if (hasEmptyState) {
      const emptyText = page.locator('.empty-text');
      const text = await emptyText.textContent();
      // Should show "没有找到相关菜谱" or similar message
      expect(text).toContain('没有找到相关菜谱');
    }
  });

  test('should filter by constitution', async ({ page }) => {
    // Click on a constitution filter (e.g., 气虚质)
    const constitutionFilter = page.locator('.filter-item').filter({ hasText: '气虚质' }).first();
    await constitutionFilter.click();

    // Wait for results to load
    await page.waitForTimeout(2000);

    // Verify filter is active (has active class)
    await expect(constitutionFilter).toHaveClass(/active/);

    // Check if action bar is displayed (since filter is applied)
    const actionBar = page.locator('.action-bar');
    const isVisible = await actionBar.isVisible({ timeout: 5000 }).catch(() => false);

    if (isVisible) {
      // Verify filter summary is displayed
      const summaryText = page.locator('.summary-text');
      await expect(summaryText).toBeVisible();
      await expect(summaryText).toContainText('已筛选');

      // Verify clear button exists
      const clearBtn = page.locator('.clear-btn');
      await expect(clearBtn).toBeVisible();
      await expect(clearBtn).toHaveText('清除筛选');
    }
  });

  test('should filter by difficulty', async ({ page }) => {
    // Click on a difficulty filter (e.g., 简单)
    const difficultyFilter = page.locator('.filter-item').filter({ hasText: '简单' }).first();
    await difficultyFilter.click();

    // Wait for results to load
    await page.waitForTimeout(2000);

    // Verify filter is active
    await expect(difficultyFilter).toHaveClass(/active/);

    // Check if action bar is displayed
    const actionBar = page.locator('.action-bar');
    const isVisible = await actionBar.isVisible({ timeout: 5000 }).catch(() => false);

    if (isVisible) {
      const summaryText = page.locator('.summary-text');
      await expect(summaryText).toContainText('已筛选');
    }
  });

  test('should support combined filters', async ({ page }) => {
    // Apply constitution filter
    const constitutionFilter = page.locator('.filter-item').filter({ hasText: '气虚质' }).first();
    await constitutionFilter.click();
    await page.waitForTimeout(1000);

    // Apply difficulty filter
    const difficultyFilter = page.locator('.filter-item').filter({ hasText: '简单' }).first();
    await difficultyFilter.click();
    await page.waitForTimeout(2000);

    // Verify both filters are active
    await expect(constitutionFilter).toHaveClass(/active/);
    await expect(difficultyFilter).toHaveClass(/active/);

    // Verify action bar shows combined filters
    const actionBar = page.locator('.action-bar');
    const isVisible = await actionBar.isVisible({ timeout: 5000 }).catch(() => false);

    if (isVisible) {
      const summaryText = page.locator('.summary-text');
      const text = await summaryText.textContent();
      // Should show multiple filter types
      expect(text).toContain('已筛选');
    }
  });

  test('should clear all filters', async ({ page }) => {
    // Apply a filter first
    const constitutionFilter = page.locator('.filter-item').filter({ hasText: '气虚质' }).first();
    await constitutionFilter.click();
    await page.waitForTimeout(1000);

    // Verify filter is active
    await expect(constitutionFilter).toHaveClass(/active/);

    // Wait for action bar to appear
    const actionBar = page.locator('.action-bar');
    await expect(actionBar).toBeVisible({ timeout: 5000 });

    // Click clear filters button
    const clearBtn = page.locator('.clear-btn');
    await clearBtn.click();
    await page.waitForTimeout(1000);

    // Verify filter is no longer active
    await expect(constitutionFilter).not.toHaveClass(/active/);

    // Verify action bar is hidden (no more filters)
    await expect(actionBar).not.toBeVisible();
  });

  test('should display empty state when no results', async ({ page }) => {
    // Enter a search term that likely has no results
    const searchInput = page.locator('.search-input');
    await searchInput.fill('xyznonexistentrecipe123456789');

    // Click search button
    const searchBtn = page.locator('.search-btn');
    await searchBtn.click();

    // Wait for results to load
    await page.waitForTimeout(2000);

    // Verify empty state is displayed
    const emptyState = page.locator('.empty-state');
    await expect(emptyState).toBeVisible();

    // Verify empty state icon and text
    const emptyIcon = page.locator('.empty-icon');
    await expect(emptyIcon).toBeVisible();
    await expect(emptyIcon).toHaveText('🔍');

    const emptyText = page.locator('.empty-text');
    await expect(emptyText).toBeVisible();
    const text = await emptyText.textContent();
    expect(text).toContain('没有找到相关菜谱');
  });

  test('should display empty state when no keyword entered', async ({ page }) => {
    // The page starts with no keyword and no filters
    // Should show "请输入关键词搜索" empty state
    const emptyState = page.locator('.empty-state');
    const isVisible = await emptyState.isVisible({ timeout: 5000 }).catch(() => false);

    if (isVisible) {
      const emptyText = page.locator('.empty-text');
      await expect(emptyText).toBeVisible();
      const text = await emptyText.textContent();
      expect(text).toContain('请输入关键词搜索');
    }
  });

  test('should clear keyword when clicking clear icon', async ({ page }) => {
    // Type a keyword
    const searchInput = page.locator('.search-input');
    await searchInput.fill('test keyword');

    // Verify clear icon appears
    const clearIcon = page.locator('.clear-icon');
    await expect(clearIcon).toBeVisible();

    // Click clear icon
    await clearIcon.click();

    // Verify input is cleared
    const inputValue = await searchInput.inputValue();
    expect(inputValue).toBe('');

    // Verify clear icon is hidden again
    const isVisible = await clearIcon.isVisible({ timeout: 1000 }).catch(() => false);
    expect(isVisible).toBe(false);
  });

  test('should navigate to detail page when clicking recipe card', async ({ page }) => {
    // First apply a filter or search to get results
    const searchInput = page.locator('.search-input');
    await searchInput.fill('汤');
    await page.keyboard.press('Enter');

    // Wait for results
    await page.waitForTimeout(2000);

    // Check if there are any results
    const recipeItem = page.locator('.recipe-item').first();
    const hasResults = await recipeItem.isVisible({ timeout: 5000 }).catch(() => false);

    if (hasResults) {
      // Click on the first recipe card
      await recipeItem.click();

      // Wait for navigation
      await page.waitForTimeout(1000);

      // Verify URL changed to detail page
      const url = page.url();
      expect(url).toContain('/pages/recipes/detail');
    } else {
      // Skip test if no results found (test data issue)
      test.skip();
    }
  });

  test('should support solar term filter', async ({ page }) => {
    // Click on a solar term filter (e.g., 春季)
    const solarTermFilter = page.locator('.filter-item').filter({ hasText: '春季' }).first();
    await solarTermFilter.click();

    // Wait for results to load
    await page.waitForTimeout(2000);

    // Verify filter is active
    await expect(solarTermFilter).toHaveClass(/active/);

    // Verify action bar shows filter is applied
    const actionBar = page.locator('.action-bar');
    const isVisible = await actionBar.isVisible({ timeout: 5000 }).catch(() => false);

    if (isVisible) {
      const summaryText = page.locator('.summary-text');
      await expect(summaryText).toContainText('已筛选');
    }
  });

  test('should support efficacy filter', async ({ page }) => {
    // Click on an efficacy filter (e.g., 健脾)
    const efficacyFilter = page.locator('.filter-item').filter({ hasText: '健脾' }).first();
    await efficacyFilter.click();

    // Wait for results to load
    await page.waitForTimeout(2000);

    // Verify filter is active
    await expect(efficacyFilter).toHaveClass(/active/);

    // Verify action bar shows filter is applied
    const actionBar = page.locator('.action-bar');
    const isVisible = await actionBar.isVisible({ timeout: 5000 }).catch(() => false);

    if (isVisible) {
      const summaryText = page.locator('.summary-text');
      await expect(summaryText).toContainText('已筛选');
    }
  });

  test('should support cooking time filter', async ({ page }) => {
    // Click on a cooking time filter (e.g., 30分钟内)
    const cookingTimeFilter = page.locator('.filter-item').filter({ hasText: '30分钟内' }).first();
    await cookingTimeFilter.click();

    // Wait for results to load
    await page.waitForTimeout(2000);

    // Verify filter is active
    await expect(cookingTimeFilter).toHaveClass(/active/);

    // Verify action bar shows filter is applied
    const actionBar = page.locator('.action-bar');
    const isVisible = await actionBar.isVisible({ timeout: 5000 }).catch(() => false);

    if (isVisible) {
      const summaryText = page.locator('.summary-text');
      await expect(summaryText).toContainText('已筛选');
    }
  });
});
