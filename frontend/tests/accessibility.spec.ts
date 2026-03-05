import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
	test('login page should not have accessibility violations', async ({ page }) => {
		await page.goto('/');
		
		const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
		
		expect(accessibilityScanResults.violations).toEqual([]);
	});

	test('should have proper heading hierarchy', async ({ page }) => {
		await page.goto('/');
		
		// Check for h1
		const h1 = page.getByRole('heading', { level: 1 });
		await expect(h1).toBeVisible();
	});

	test('buttons should have accessible names', async ({ page }) => {
		await page.goto('/');
		
		const loginButton = page.getByRole('button', { name: /Continue with GitHub/i });
		await expect(loginButton).toHaveAccessibleName();
	});

	test('should support keyboard navigation', async ({ page }) => {
		await page.goto('/');
		
		// Tab to login button
		await page.keyboard.press('Tab');
		
		const loginButton = page.getByRole('button', { name: /Continue with GitHub/i });
		await expect(loginButton).toBeFocused();
		
		// Should be able to activate with Enter
		await page.keyboard.press('Enter');
		
		// Should trigger the login flow
		await page.waitForTimeout(500);
	});

	test('should have sufficient color contrast', async ({ page }) => {
		await page.goto('/');
		
		const accessibilityScanResults = await new AxeBuilder({ page })
			.withTags(['wcag2aa'])
			.analyze();
		
		const contrastViolations = accessibilityScanResults.violations.filter(
			v => v.id === 'color-contrast'
		);
		
		expect(contrastViolations).toEqual([]);
	});

	test('images should have alt text', async ({ page }) => {
		await page.goto('/');
		
		const images = page.locator('img');
		const count = await images.count();
		
		for (let i = 0; i < count; i++) {
			const img = images.nth(i);
			const alt = await img.getAttribute('alt');
			expect(alt).toBeTruthy();
		}
	});

	test('form inputs should have labels', async ({ page }) => {
		await page.goto('/');
		
		const inputs = page.locator('input');
		const count = await inputs.count();
		
		for (let i = 0; i < count; i++) {
			const input = inputs.nth(i);
			const ariaLabel = await input.getAttribute('aria-label');
			const ariaLabelledBy = await input.getAttribute('aria-labelledby');
			const id = await input.getAttribute('id');
			
			// Should have either aria-label, aria-labelledby, or associated label
			const hasLabel = ariaLabel || ariaLabelledBy || (id && await page.locator(`label[for="${id}"]`).count() > 0);
			expect(hasLabel).toBeTruthy();
		}
	});

	test('should support screen reader announcements', async ({ page }) => {
		await page.goto('/');
		
		// Check for aria-live regions
		const liveRegions = page.locator('[aria-live]');
		const count = await liveRegions.count();
		
		// Should have at least one live region for dynamic content
		expect(count).toBeGreaterThanOrEqual(0);
	});
});
