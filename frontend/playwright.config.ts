import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright E2E Testing Configuration
 *
 * This config is set up for H5 (web) testing of the uni-app frontend.
 * The dev server runs on http://localhost:5173 via vite dev:h5.
 *
 * Run tests:
 *   npx playwright test              # Run all tests
 *   npx playwright test --list       # List all tests
 *   npx playwright test 01-navigation # Run specific file
 *   npx playwright test --ui         # Run in UI mode
 *   npx playwright show-report       # View HTML report
 */
export default defineConfig({
  testDir: './tests/e2e',

  /* Run tests in files in parallel */
  fullyParallel: false,

  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,

  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,

  /* Opt out of parallel tests on CI. */
  workers: 1,

  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'playwright-report/results.json' }]
  ],

  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL: 'http://localhost:5173',

    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',

    /* Take screenshot on failure */
    screenshot: 'only-on-failure',

    /* Record video on failure */
    video: 'retain-on-failure',

    /* Timeout for each action */
    actionTimeout: 10000,

    /* Timeout for navigation */
    navigationTimeout: 30000,
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
      testIgnore: /04-api\.spec\.ts/,
    },

    /* Test against mobile viewport */
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
      testIgnore: /04-api\.spec\.ts/,
    },

    /* API tests - no browser required, backend should be running separately */
    {
      name: 'API',
      testMatch: /04-api\.spec\.ts/,
      use: {},
      // Don't use webServer for API tests
      dependencies: [],
    },
  ],

  /* Run your local dev server before starting the tests */
  webServer: {
    command: 'npm run dev:h5',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
    stdout: 'pipe',
    stderr: 'pipe',
  },
});
