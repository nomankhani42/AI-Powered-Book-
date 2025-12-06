import { test, expect } from '@playwright/test';

test.describe('Learning Path Navigation', () => {
  test('should navigate to the learning path and display week 1 content', async ({ page }) => {
    await page.goto('/'); // Navigate to the Docusaurus homepage

    // Assuming there's a link to the learning path or it's directly on the homepage
    // This part might need adjustment based on the actual implementation of T009
    // For now, let's assume it's a custom page at '/learning-path' for now.

    // Check for a link to the learning path and click it if it exists
    const learningPathLink = page.locator('a', { hasText: 'Learning Path' });
    if (await learningPathLink.isVisible()) {
      await learningPathLink.click();
      await page.waitForURL('/learning-path'); // Wait for the URL to change to the learning path page
    } else {
      // If no explicit link, assume learning path content is on the homepage or another default route
      // For now, we'll proceed assuming we are on a page where learning path content should be
      console.warn("No 'Learning Path' link found. Proceeding to check for content on current page.");
    }

    // Expect to see a heading or section related to 'Week 1'
    await expect(page.locator('text=Week 1')).toBeVisible();
    await expect(page.locator('text=chapter1')).toBeVisible();
    await expect(page.locator('text=chapter2')).toBeVisible();
  });
});
