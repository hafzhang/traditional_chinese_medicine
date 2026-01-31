import { test, expect } from '@playwright/test';

/**
 * Recipe Detail Page E2E Tests
 *
 * Tests for the recipe detail page functionality including:
 * - Page basic elements display
 * - Desc area blue background
 * - Tip area yellow background
 * - Constitution tags Chinese mapping
 * - Efficacy and solar terms tags display
 */

test.describe('Recipe Detail Page', () => {
  test.beforeEach(async ({ page }) => {
    // Start from the list page and navigate to detail
    await page.goto('/#/pages/recipes/list');
    await page.waitForSelector('.recipes-list, .empty-state', { timeout: 15000 });

    // Try to navigate to detail page if recipes exist
    const recipesList = page.locator('.recipes-list');
    if (await recipesList.isVisible({ timeout: 5000 }).catch(() => false)) {
      const recipeItems = page.locator('.recipe-item');
      const count = await recipeItems.count();

      if (count > 0) {
        // Click first recipe to navigate to detail
        await recipeItems.first().click();
        await page.waitForURL(/\/pages\/recipes\/detail/, { timeout: 10000 });
        return;
      }
    }

    // If no recipes in list, navigate directly to detail with a test ID
    // This will show error state or load from backend if data exists
    await page.goto('/#/pages/recipes/detail?id=test-recipe-id');
  });

  test('should display detail page basic elements', async ({ page }) => {
    // Wait for page to load (either loading, content, or error state)
    await page.waitForSelector('.loading-state, .recipe-detail-page .image-section, .error-state', { timeout: 15000 });

    // Check if we have content (not loading or error)
    const loadingState = page.locator('.loading-state');
    const errorState = page.locator('.error-state');
    const contentArea = page.locator('.image-section');

    if (await loadingState.isVisible({ timeout: 5000 }).catch(() => false)) {
      // Content is still loading - verify loading state exists
      await expect(loadingState).toBeVisible();
    } else if (await errorState.isVisible({ timeout: 5000 }).catch(() => false)) {
      // Recipe not found - verify error state
      await expect(errorState).toBeVisible();
      await expect(errorState.locator('.error-icon')).toHaveText('😕');
      await expect(errorState.locator('.error-text')).toHaveText('菜谱不存在');
    } else {
      // Content loaded - verify basic elements
      // Image section
      await expect(contentArea).toBeVisible();

      // Recipe image or placeholder
      const recipeImage = page.locator('.recipe-image');
      await expect(recipeImage).toBeVisible();

      // Info card with name and metadata
      const infoCard = page.locator('.info-card').first();
      await expect(infoCard).toBeVisible();

      // Recipe name
      const recipeName = page.locator('.recipe-name');
      const nameVisible = await recipeName.isVisible({ timeout: 3000 }).catch(() => false);
      if (nameVisible) {
        const nameText = await recipeName.textContent();
        expect(nameText?.trim().length).toBeGreaterThan(0);
      }
    }
  });

  test('should display recipe cover image or placeholder', async ({ page }) => {
    await page.waitForSelector('.image-section, .error-state', { timeout: 15000 });

    const errorState = page.locator('.error-state');
    if (await errorState.isVisible({ timeout: 5000 }).catch(() => false)) {
      // Skip test if recipe not found
      test.skip();
      return;
    }

    const imageSection = page.locator('.image-section');
    await expect(imageSection).toBeVisible();

    const recipeImage = page.locator('.recipe-image');
    await expect(recipeImage).toBeVisible();

    // Check if it's a placeholder (has placeholder class) or actual image
    const hasPlaceholder = await recipeImage.locator('.placeholder-icon').isVisible({ timeout: 3000 }).catch(() => false);
    const hasImage = await recipeImage.locator('img[src]').isVisible({ timeout: 3000 }).catch(() => false);

    // Should have either placeholder or actual image
    expect(hasPlaceholder || hasImage).toBeTruthy();

    if (hasPlaceholder) {
      await expect(recipeImage.locator('.placeholder-icon')).toHaveText('🍲');
    }
  });

  test('should display recipe metadata (difficulty, time, calories)', async ({ page }) => {
    await page.waitForSelector('.image-section, .error-state', { timeout: 15000 });

    const errorState = page.locator('.error-state');
    if (await errorState.isVisible({ timeout: 5000 }).catch(() => false)) {
      test.skip();
      return;
    }

    // Check for recipe metadata section
    const recipeMeta = page.locator('.recipe-meta');
    const metaVisible = await recipeMeta.isVisible({ timeout: 5000 }).catch(() => false);

    if (metaVisible) {
      // Check for difficulty tag
      const difficultyTag = recipeMeta.locator('.tag.difficulty');
      const difficultyVisible = await difficultyTag.isVisible({ timeout: 3000 }).catch(() => false);

      if (difficultyVisible) {
        const difficultyText = await difficultyTag.textContent();
        expect(['简单', '中等', '困难', 'easy', 'medium', 'hard']).toContain(difficultyText?.trim().toLowerCase());
      }

      // Check for cooking time
      const timeTag = recipeMeta.locator('.time');
      const timeVisible = await timeTag.isVisible({ timeout: 3000 }).catch(() => false);

      if (timeVisible) {
        await expect(timeTag).toContainText('分钟');
      }
    }
  });

  test('should display desc section with blue gradient background', async ({ page }) => {
    await page.waitForSelector('.image-section, .error-state', { timeout: 15000 });

    const errorState = page.locator('.error-state');
    if (await errorState.isVisible({ timeout: 5000 }).catch(() => false)) {
      test.skip();
      return;
    }

    // Look for desc section
    const descSection = page.locator('.info-card.desc-section');
    const descVisible = await descSection.isVisible({ timeout: 5000 }).catch(() => false);

    if (descVisible) {
      // Verify section title
      await expect(descSection.locator('.card-title')).toContainText('个人体验');

      // Verify content
      const content = descSection.locator('.card-content');
      await expect(content).toBeVisible();

      // Verify blue gradient background using computed style
      const backgroundColor = await descSection.evaluate((el) => {
        return window.getComputedStyle(el).backgroundColor;
      });

      // The blue gradient background should have a bluish color
      // Check if background contains blue tones (rgb values where blue is dominant)
      const rgbMatch = backgroundColor.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
      if (rgbMatch) {
        const [, r, g, b] = rgbMatch.map(Number);
        // Blue background means B component should be relatively high
        // For the gradient #e6f7ff to #f0f5ff, blue values are around 255
        expect(b).toBeGreaterThan(200);
      }

      // Also check for the blue left border
      const borderLeftColor = await descSection.evaluate((el) => {
        return window.getComputedStyle(el).borderLeftColor;
      });
      expect(borderLeftColor).toContain('rgb'); // Should have a border color
    } else {
      // Desc section is optional, skip if not present
      test.skip();
    }
  });

  test('should display tip section with yellow gradient background', async ({ page }) => {
    await page.waitForSelector('.image-section, .error-state', { timeout: 15000 });

    const errorState = page.locator('.error-state');
    if (await errorState.isVisible({ timeout: 5000 }).catch(() => false)) {
      test.skip();
      return;
    }

    // Look for tip section
    const tipSection = page.locator('.info-card.tip-section');
    const tipVisible = await tipSection.isVisible({ timeout: 5000 }).catch(() => false);

    if (tipVisible) {
      // Verify section title
      await expect(tipSection.locator('.card-title')).toContainText('烹饪贴士');

      // Verify content
      const content = tipSection.locator('.card-content');
      await expect(content).toBeVisible();

      // Verify yellow gradient background using computed style
      const backgroundColor = await tipSection.evaluate((el) => {
        return window.getComputedStyle(el).backgroundColor;
      });

      // The yellow gradient background should have yellowish tones
      const rgbMatch = backgroundColor.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
      if (rgbMatch) {
        const [, r, g, b] = rgbMatch.map(Number);
        // Yellow background means R and G components should be relatively high and close to each other
        expect(r).toBeGreaterThan(200);
        expect(g).toBeGreaterThan(200);
      }

      // Also check for the yellow left border
      const borderLeftColor = await tipSection.evaluate((el) => {
        return window.getComputedStyle(el).borderLeftColor;
      });
      expect(borderLeftColor).toContain('rgb');
    } else {
      // Tip section is optional, skip if not present
      test.skip();
    }
  });

  test('should display constitution tags with Chinese names (not codes)', async ({ page }) => {
    await page.waitForSelector('.image-section, .error-state', { timeout: 15000 });

    const errorState = page.locator('.error-state');
    if (await errorState.isVisible({ timeout: 5000 }).catch(() => false)) {
      test.skip();
      return;
    }

    // Look for suitable constitutions section
    const suitableSection = page.locator('.info-card').filter({ hasText: '适合体质' });
    const suitableVisible = await suitableSection.isVisible({ timeout: 5000 }).catch(() => false);

    if (suitableVisible) {
      // Check constitution tags
      const constitutionTags = suitableSection.locator('.constitution-tag.suitable');
      const count = await constitutionTags.count();

      if (count > 0) {
        // Verify Chinese names are displayed, not codes
        for (let i = 0; i < count; i++) {
          const tag = constitutionTags.nth(i);
          const tagText = await tag.textContent();

          // Should be Chinese names like '平和质', '气虚质', etc.
          // NOT codes like 'peace', 'qi_deficiency', etc.
          expect(tagText).toMatch(/[质]/); // Should contain '质' character

          // Verify it's a known Chinese constitution name
          const knownConstitutions = ['平和质', '气虚质', '阳虚质', '阴虚质', '痰湿质', '湿热质', '血瘀质', '气郁质', '特禀质'];
          expect(knownConstitutions).toContain(tagText?.trim());
        }
      }
    } else {
      // Constitution section might not be present
      test.skip();
    }
  });

  test('should display efficacy tags and solar terms tags', async ({ page }) => {
    await page.waitForSelector('.image-section, .error-state', { timeout: 15000 });

    const errorState = page.locator('.error-state');
    if (await errorState.isVisible({ timeout: 5000 }).catch(() => false)) {
      test.skip();
      return;
    }

    // Check for efficacy tags section
    const efficacySection = page.locator('.info-card').filter({ hasText: '功效标签' });
    const efficacyVisible = await efficacySection.isVisible({ timeout: 5000 }).catch(() => false);

    if (efficacyVisible) {
      // Verify efficacy tags
      const efficacyTags = efficacySection.locator('.tag-item.efficacy');
      const efficacyCount = await efficacyTags.count();

      if (efficacyCount > 0) {
        // Check first efficacy tag
        const firstTag = efficacyTags.first();
        await expect(firstTag).toBeVisible();

        // Efficacy tags should be Chinese text
        const tagText = await firstTag.textContent();
        expect(tagText?.trim().length).toBeGreaterThan(0);
      }
    }

    // Check for solar terms section
    const solarSection = page.locator('.info-card').filter({ hasText: '适用节气' });
    const solarVisible = await solarSection.isVisible({ timeout: 5000 }).catch(() => false);

    if (solarVisible) {
      // Verify solar term tags
      const solarTags = solarSection.locator('.tag-item.season');
      const solarCount = await solarTags.count();

      if (solarCount > 0) {
        // Check first solar term tag
        const firstTag = solarTags.first();
        await expect(firstTag).toBeVisible();

        // Solar term tags should be Chinese text
        const tagText = await firstTag.textContent();
        expect(tagText?.trim().length).toBeGreaterThan(0);
      }
    }

    // If neither section is present, skip the test
    if (!efficacyVisible && !solarVisible) {
      test.skip();
    }
  });

  test('should display ingredients list with main ingredient highlighting', async ({ page }) => {
    await page.waitForSelector('.image-section, .error-state', { timeout: 15000 });

    const errorState = page.locator('.error-state');
    if (await errorState.isVisible({ timeout: 5000 }).catch(() => false)) {
      test.skip();
      return;
    }

    // Look for ingredients section
    const ingredientsSection = page.locator('.info-card').filter({ hasText: '食材清单' });
    const ingredientsVisible = await ingredientsSection.isVisible({ timeout: 5000 }).catch(() => false);

    if (ingredientsVisible) {
      // Check for ingredient rows
      const ingredientRows = ingredientsSection.locator('.ingredient-row');
      const count = await ingredientRows.count();

      if (count > 0) {
        // Check for main ingredient highlighting
        const mainIngredient = ingredientsSection.locator('.ingredient-row.main');
        const hasMain = await mainIngredient.isVisible({ timeout: 3000 }).catch(() => false);

        if (hasMain) {
          // Main ingredient should have yellow background
          const backgroundColor = await mainIngredient.evaluate((el) => {
            return window.getComputedStyle(el).backgroundColor;
          });

          // Yellow background means R and G are high
          const rgbMatch = backgroundColor.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
          if (rgbMatch) {
            const [, r, g] = rgbMatch.map(Number);
            expect(r + g).toBeGreaterThan(400); // Should be yellowish
          }

          // Should have main badge
          await expect(mainIngredient.locator('.main-badge')).toBeVisible();
          await expect(mainIngredient.locator('.main-badge')).toHaveText('主料');
        }

        // Check ingredient info display
        const firstRow = ingredientRows.first();
        await expect(firstRow.locator('.ingredient-name')).toBeVisible();
      }
    } else {
      // Ingredients section might not be present
      test.skip();
    }
  });

  test('should display cooking steps with numbered circles', async ({ page }) => {
    await page.waitForSelector('.image-section, .error-state', { timeout: 15000 });

    const errorState = page.locator('.error-state');
    if (await errorState.isVisible({ timeout: 5000 }).catch(() => false)) {
      test.skip();
      return;
    }

    // Look for steps section
    const stepsSection = page.locator('.info-card').filter({ hasText: '制作步骤' });
    const stepsVisible = await stepsSection.isVisible({ timeout: 5000 }).catch(() => false);

    if (stepsVisible) {
      // Check for step items
      const stepItems = stepsSection.locator('.step-item');
      const count = await stepItems.count();

      expect(count).toBeGreaterThan(0);

      // Verify step structure
      const firstStep = stepItems.first();

      // Should have step number circle
      const stepNumber = firstStep.locator('.step-number');
      await expect(stepNumber).toBeVisible();

      // Step number should be numeric
      const numberText = await stepNumber.textContent();
      expect(numberText).toMatch(/\d+/);

      // Should have step description
      const stepDescription = firstStep.locator('.step-description');
      await expect(stepDescription).toBeVisible();
      const descText = await stepDescription.textContent();
      expect(descText?.trim().length).toBeGreaterThan(0);

      // Check for optional step duration
      const stepDuration = firstStep.locator('.step-duration');
      const hasDuration = await stepDuration.isVisible({ timeout: 3000 }).catch(() => false);
      if (hasDuration) {
        await expect(stepDuration).toContainText('分钟');
      }
    } else {
      // Steps section might not be present
      test.skip();
    }
  });
});
