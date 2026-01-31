import { test, expect } from '@playwright/test';

/**
 * API Field Validation E2E Tests
 *
 * Tests for validating backend API response fields including:
 * - GET /api/v1/recipes returns correct fields
 * - GET /api/v1/recipes/{id} returns complete detail
 * - Field types validation (difficulty enum, JSON arrays)
 * - Filter validation results
 * - Combined filter validation
 */

test.describe('Recipe API Field Validation', () => {
  const API_BASE_URL = 'http://localhost:8000/api/v1/recipes';

  test.beforeEach(async ({ request }) => {
    // Verify backend API is accessible - check for valid response format
    // Note: API may return empty results if no data is seeded
    const response = await request.get(`${API_BASE_URL}?page_size=1`);
    expect([200, 404]).toContain(response.status());

    // For 404, we skip the test (no recipes in database)
    if (response.status() === 404) {
      test.skip();
    }
  });

  test('GET /api/v1/recipes returns correct fields', async ({ request }) => {
    const response = await request.get(`${API_BASE_URL}?page_size=5`);
    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data).toHaveProperty('code', 0);
    expect(data).toHaveProperty('data');

    const { data: recipeData } = data;
    expect(recipeData).toHaveProperty('total');
    expect(recipeData).toHaveProperty('page');
    expect(recipeData).toHaveProperty('page_size');
    expect(recipeData).toHaveProperty('items');

    // Verify items is an array
    expect(Array.isArray(recipeData.items)).toBeTruthy();

    // If items exist, verify structure
    if (recipeData.items.length > 0) {
      const firstRecipe = recipeData.items[0];

      // Required fields from PRD
      expect(firstRecipe).toHaveProperty('id');
      expect(firstRecipe).toHaveProperty('name');
      expect(firstRecipe).toHaveProperty('cooking_time');
      expect(firstRecipe).toHaveProperty('cover_image');
      expect(firstRecipe).toHaveProperty('difficulty');

      // Verify field types
      expect(typeof firstRecipe.id).toBe('string');
      expect(typeof firstRecipe.name).toBe('string');
      expect(typeof firstRecipe.cooking_time).toBe('number');
      expect(typeof firstRecipe.difficulty).toBe('string');

      // Verify difficulty enum value
      expect(['easy', 'medium', 'hard', '简单', '中等', '困难']).toContain(firstRecipe.difficulty);

      // Verify efficacy_tags is JSON array (optional field)
      if (firstRecipe.efficacy_tags !== null && firstRecipe.efficacy_tags !== undefined) {
        expect(Array.isArray(firstRecipe.efficacy_tags)).toBeTruthy();
      }

      // Verify suitable_constitutions is JSON array (optional field)
      if (firstRecipe.suitable_constitutions !== null && firstRecipe.suitable_constitutions !== undefined) {
        expect(Array.isArray(firstRecipe.suitable_constitutions)).toBeTruthy();
      }
    }
  });

  test('GET /api/v1/recipes/{id} returns complete detail', async ({ request }) => {
    // First get a recipe ID from the list
    const listResponse = await request.get(`${API_BASE_URL}?page_size=1`);
    const listData = await listResponse.json();

    if (listData.data.items.length === 0) {
      test.skip();
      return;
    }

    const recipeId = listData.data.items[0].id;

    // Get recipe detail
    const response = await request.get(`${API_BASE_URL}/${recipeId}`);
    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data).toHaveProperty('code', 0);
    expect(data).toHaveProperty('data');

    const recipe = data.data;

    // Required fields
    expect(recipe).toHaveProperty('id');
    expect(recipe).toHaveProperty('name');

    // PRD required fields: desc, tip, ingredients, steps, calories
    expect(recipe).toHaveProperty('desc');
    expect(recipe).toHaveProperty('tip');
    expect(recipe).toHaveProperty('ingredients');
    expect(recipe).toHaveProperty('steps');
    expect(recipe).toHaveProperty('calories');

    // Verify ingredients is an array with nature/taste
    expect(Array.isArray(recipe.ingredients)).toBeTruthy();

    if (recipe.ingredients.length > 0) {
      const firstIngredient = recipe.ingredients[0];
      expect(firstIngredient).toHaveProperty('name');
      // nature and taste are optional (from Ingredient relation)
      if (firstIngredient.nature !== undefined && firstIngredient.nature !== null) {
        expect(typeof firstIngredient.nature).toBe('string');
      }
      if (firstIngredient.taste !== undefined && firstIngredient.taste !== null) {
        expect(typeof firstIngredient.taste).toBe('string');
      }
    }

    // Verify steps is an array
    expect(Array.isArray(recipe.steps)).toBeTruthy();

    if (recipe.steps.length > 0) {
      const firstStep = recipe.steps[0];
      expect(firstStep).toHaveProperty('step_number');
      expect(firstStep).toHaveProperty('description');
      expect(typeof firstStep.step_number).toBe('number');
      expect(typeof firstStep.description).toBe('string');
    }

    // Verify calories is a number (optional field)
    if (recipe.calories !== null && recipe.calories !== undefined) {
      expect(typeof recipe.calories).toBe('number');
    }
  });

  test('GET /api/v1/recipes/{id} returns 404 for non-existent recipe', async ({ request }) => {
    const response = await request.get(`${API_BASE_URL}/non-existent-id-12345`);
    expect(response.status()).toBe(404);

    const data = await response.json();
    expect(data).toHaveProperty('detail');
    expect(data.detail).toContain('菜谱不存在');
  });

  test('should verify field types (difficulty enum, JSON arrays)', async ({ request }) => {
    const response = await request.get(`${API_BASE_URL}?page_size=10`);
    expect(response.status()).toBe(200);

    const data = await response.json();
    const items = data.data.items;

    if (items.length === 0) {
      test.skip();
      return;
    }

    // Check difficulty enum values across all items
    const validDifficulties = ['easy', 'medium', 'hard', '简单', '中等', '困难'];

    for (const recipe of items) {
      // Verify difficulty type and value
      expect(typeof recipe.difficulty).toBe('string');
      expect(validDifficulties).toContain(recipe.difficulty);

      // Verify cooking_time is number
      expect(typeof recipe.cooking_time).toBe('number');
      expect(recipe.cooking_time).toBeGreaterThanOrEqual(0);

      // Verify efficacy_tags is JSON array if present
      if (recipe.efficacy_tags !== null && recipe.efficacy_tags !== undefined) {
        expect(Array.isArray(recipe.efficacy_tags)).toBeTruthy();
        // All items should be strings
        recipe.efficacy_tags.forEach((tag: unknown) => {
          expect(typeof tag).toBe('string');
        });
      }

      // Verify suitable_constitutions is JSON array if present
      if (recipe.suitable_constitutions !== null && recipe.suitable_constitutions !== undefined) {
        expect(Array.isArray(recipe.suitable_constitutions)).toBeTruthy();
        // All items should be strings
        recipe.suitable_constitutions.forEach((constitution: unknown) => {
          expect(typeof constitution).toBe('string');
        });
      }

      // Verify solar_terms is JSON array if present
      if (recipe.solar_terms !== null && recipe.solar_terms !== undefined) {
        expect(Array.isArray(recipe.solar_terms)).toBeTruthy();
        recipe.solar_terms.forEach((term: unknown) => {
          expect(typeof term).toBe('string');
        });
      }
    }
  });

  test('should verify constitution filter returns results containing that constitution', async ({ request }) => {
    // Test with qi_deficiency constitution
    const response = await request.get(`${API_BASE_URL}?constitution=qi_deficiency&page_size=10`);
    expect(response.status()).toBe(200);

    const data = await response.json();
    const items = data.data.items;

    if (items.length === 0) {
      test.skip();
      return;
    }

    // Verify each result has qi_deficiency in suitable_constitutions
    for (const recipe of items) {
      if (recipe.suitable_constitutions !== null && recipe.suitable_constitutions !== undefined) {
        expect(recipe.suitable_constitutions).toContain('qi_deficiency');
      }
    }
  });

  test('should verify solar_term filter returns results containing that solar term', async ({ request }) => {
    // Test with '春季' (Spring) solar term
    const response = await request.get(`${API_BASE_URL}?solar_term=春季&page_size=10`);
    expect(response.status()).toBe(200);

    const data = await response.json();
    const items = data.data.items;

    if (items.length === 0) {
      test.skip();
      return;
    }

    // Verify each result has '春季' in solar_terms
    for (const recipe of items) {
      if (recipe.solar_terms !== null && recipe.solar_terms !== undefined) {
        // Check for both Chinese and unicode-escaped formats
        const hasSolarTerm = recipe.solar_terms.includes('春季') ||
                            recipe.solar_terms.includes('\\u6625\\u5b63') ||
                            recipe.solar_terms.includes('\\\\u6625\\\\u5b63');
        expect(hasSolarTerm).toBeTruthy();
      }
    }
  });

  test('should verify keyword search returns results containing keyword', async ({ request }) => {
    // Search for '山药' (common ingredient)
    const response = await request.get(`${API_BASE_URL}/search?keyword=山药&page_size=10`);
    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data).toHaveProperty('code', 0);
    expect(data).toHaveProperty('data');

    const { data: searchData } = data;
    expect(searchData).toHaveProperty('items');
    expect(Array.isArray(searchData.items)).toBeTruthy();

    if (searchData.items.length > 0) {
      // At least one result should contain the keyword in name or ingredients
      const hasKeyword = searchData.items.some((recipe: { name: string; efficacy_tags?: string[] }) =>
        recipe.name.includes('山药') ||
        (recipe.efficacy_tags && recipe.efficacy_tags.some((tag: string) => tag.includes('山药')))
      );
      expect(hasKeyword).toBeTruthy();
    }
  });

  test('should verify combined filters work together', async ({ request }) => {
    // Combine constitution and difficulty filters
    const response = await request.get(`${API_BASE_URL}?constitution=qi_deficiency&difficulty=easy&page_size=10`);
    expect(response.status()).toBe(200);

    const data = await response.json();
    const items = data.data.items;

    if (items.length === 0) {
      test.skip();
      return;
    }

    // Verify each result matches BOTH filters
    for (const recipe of items) {
      // Check difficulty filter
      expect(['easy', '简单']).toContain(recipe.difficulty);

      // Check constitution filter
      if (recipe.suitable_constitutions !== null && recipe.suitable_constitutions !== undefined) {
        expect(recipe.suitable_constitutions).toContain('qi_deficiency');
      }
    }
  });

  test('should verify efficacy filter works correctly', async ({ request }) => {
    // Test with '健脾' efficacy tag
    const response = await request.get(`${API_BASE_URL}?efficacy=健脾&page_size=10`);
    expect(response.status()).toBe(200);

    const data = await response.json();
    const items = data.data.items;

    if (items.length === 0) {
      test.skip();
      return;
    }

    // Verify each result has '健脾' in efficacy_tags
    for (const recipe of items) {
      if (recipe.efficacy_tags !== null && recipe.efficacy_tags !== undefined) {
        // Check for both Chinese and unicode-escaped formats
        const hasEfficacy = recipe.efficacy_tags.includes('健脾') ||
                           recipe.efficacy_tags.includes('\\u5065\\u813e') ||
                           recipe.efficacy_tags.includes('\\\\u5065\\\\u813e');
        expect(hasEfficacy).toBeTruthy();
      }
    }
  });

  test('should verify max_cooking_time filter works correctly', async ({ request }) => {
    // Test with max_cooking_time=30
    const response = await request.get(`${API_BASE_URL}?max_cooking_time=30&page_size=10`);
    expect(response.status()).toBe(200);

    const data = await response.json();
    const items = data.data.items;

    if (items.length === 0) {
      test.skip();
      return;
    }

    // Verify each result has cooking_time <= 30
    for (const recipe of items) {
      expect(recipe.cooking_time).toBeLessThanOrEqual(30);
    }
  });

  test('should verify difficulty filter works correctly', async ({ request }) => {
    // Test with 'medium' difficulty
    const response = await request.get(`${API_BASE_URL}?difficulty=medium&page_size=10`);
    expect(response.status()).toBe(200);

    const data = await response.json();
    const items = data.data.items;

    if (items.length === 0) {
      test.skip();
      return;
    }

    // Verify each result has difficulty='medium' or '中等'
    for (const recipe of items) {
      expect(['medium', '中等']).toContain(recipe.difficulty);
    }
  });

  test('should verify search API with empty keyword returns 422', async ({ request }) => {
    // Empty keyword should return 422 (validation error)
    const response = await request.get(`${API_BASE_URL}/search?keyword=`);
    expect(response.status()).toBe(422);

    const data = await response.json();
    expect(data).toHaveProperty('detail');
    expect(Array.isArray(data.detail)).toBeTruthy();
  });

  test('should verify recommendation API with constitution type', async ({ request }) => {
    const response = await request.get(`${API_BASE_URL}/recommend?recommend_type=constitution&constitution=qi_deficiency&limit=5`);
    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data).toHaveProperty('code', 0);
    expect(data).toHaveProperty('data');

    const { data: recData } = data;
    expect(recData).toHaveProperty('type', 'constitution');
    expect(recData).toHaveProperty('recommendation_reason');
    expect(recData).toHaveProperty('items');
    expect(Array.isArray(recData.items)).toBeTruthy();

    if (recData.items.length > 0) {
      // Verify items contain qi_deficiency constitution
      for (const recipe of recData.items) {
        if (recipe.suitable_constitutions !== null && recipe.suitable_constitutions !== undefined) {
          expect(recipe.suitable_constitutions).toContain('qi_deficiency');
        }
      }
    }
  });

  test('should verify recommendation API with invalid type returns 400', async ({ request }) => {
    const response = await request.get(`${API_BASE_URL}/recommend?recommend_type=invalid&limit=5`);
    expect(response.status()).toBe(400);

    const data = await response.json();
    expect(data).toHaveProperty('detail');
    expect(data.detail).toContain('Invalid recommend_type');
  });

  test('should verify recommendation API missing required parameter returns 400', async ({ request }) => {
    // Missing constitution parameter for constitution type
    const response = await request.get(`${API_BASE_URL}/recommend?recommend_type=constitution&limit=5`);
    expect(response.status()).toBe(400);

    const data = await response.json();
    expect(data).toHaveProperty('detail');
    expect(data.detail).toContain('constitution');
  });
});
