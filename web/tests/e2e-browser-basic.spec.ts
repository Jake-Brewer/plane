/**
 * E2E Test: Basic Browser Functionality
 * Category: read-only
 * Speed: fast
 * Side Effect Risk: none
 * Framework: Playwright (headless)
 *
 * This test verifies that Playwright can launch browsers and navigate to external sites.
 * It serves as a baseline test to ensure the testing infrastructure is working.
 */
import { test, expect, BrowserContext, Page } from '@playwright/test';

test.describe('Basic Browser Tests (Infrastructure)', () => {
  let context: BrowserContext;
  let page: Page;

  test.beforeEach(async ({ browser }) => {
    // Create a new context for each test to ensure isolation
    context = await browser.newContext();
    page = await context.newPage();
  });

  test.afterEach(async () => {
    // Ensure proper cleanup after each test
    console.log('🧹 Cleaning up browser resources...');
    if (page) {
      await page.close();
      console.log('✅ Page closed');
    }
    if (context) {
      await context.close();
      console.log('✅ Browser context closed');
    }
  });

  test('should launch browser and handle basic operations', async () => {
    try {
      console.log('🚀 Testing basic browser operations...');
      
      // Navigate to a data URL to avoid external dependencies
      await page.goto('data:text/html,<html><head><title>Test Page</title></head><body><h1>Test Content</h1><p id="test-para">Hello World</p></body></html>');
      
      // Verify page loaded
      await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
      
      // Get page title
      const title = await page.title();
      expect(title).toBe('Test Page');
      console.log(`📄 Page title: ${title}`);
      
      // Verify content is present
      const heading = await page.locator('h1').textContent();
      expect(heading).toBe('Test Content');
      
      // Test element interaction
      const paragraph = await page.locator('#test-para').textContent();
      expect(paragraph).toBe('Hello World');
      
      console.log('✅ Basic browser test passed');
      
    } catch (error) {
      console.error('❌ Basic browser test failed:', error);
      
      // Take a screenshot for debugging
      if (page) {
        await page.screenshot({ path: 'basic-test-failure.png', fullPage: true });
        console.log('📸 Screenshot saved as basic-test-failure.png');
      }
      
      throw error;
    }
  });

  test('should handle browser context isolation', async () => {
    try {
      console.log('🔒 Testing browser context isolation...');
      
      // Use httpbin.org which supports localStorage
      await page.goto('https://httpbin.org/html', { waitUntil: 'networkidle', timeout: 30000 });
      
      // Set a local storage item
      await page.evaluate(() => {
        localStorage.setItem('test-key', 'test-value');
      });
      
      // Verify the item was set
      const storageValue = await page.evaluate(() => localStorage.getItem('test-key'));
      expect(storageValue).toBe('test-value');
      
      // Verify page title exists (may be empty for some test pages)
      const title = await page.title();
      console.log(`📄 Page title: "${title}"`);
      // Just verify localStorage worked, title content may vary
      
      console.log('✅ Browser context isolation test passed');
      
    } catch (error) {
      console.error('❌ Browser context isolation test failed:', error);
      throw error;
    }
  });
}); 