import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
	test('should display login page', async ({ page }) => {
		await page.goto('/');
		
		// Check for PersonAI branding
		await expect(page.getByRole('heading', { name: 'PersonAI' })).toBeVisible();
		await expect(page.getByText('Your Personal AI Assistant')).toBeVisible();
		
		// Check for GitHub login button
		const loginButton = page.getByRole('button', { name: /Continue with GitHub/i });
		await expect(loginButton).toBeVisible();
		await expect(loginButton).toBeEnabled();
	});

	test('should show device code flow UI', async ({ page }) => {
		// Mock the backend API
		await page.route('**/auth/github/device/start', async (route) => {
			await route.fulfill({
				status: 200,
				contentType: 'application/json',
				body: JSON.stringify({
					device_code: 'test_device_code_123',
					user_code: 'ABCD-1234',
					verification_uri: 'https://github.com/login/device',
					expires_in: 900,
					interval: 5
				})
			});
		});

		await page.goto('/');
		
		// Click login button
		await page.getByRole('button', { name: /Continue with GitHub/i }).click();
		
		// Wait for device code to appear
		await expect(page.getByText('Enter this code on GitHub:')).toBeVisible();
		await expect(page.getByText('ABCD-1234')).toBeVisible();
		
		// Check for copy button
		const copyButton = page.getByRole('button', { title: 'Copy code' });
		await expect(copyButton).toBeVisible();
		
		// Check for waiting message
		await expect(page.getByText('Waiting for authorization...')).toBeVisible();
	});

	test('should copy device code to clipboard', async ({ page, context }) => {
		// Grant clipboard permissions
		await context.grantPermissions(['clipboard-read', 'clipboard-write']);
		
		// Mock the backend API
		await page.route('**/auth/github/device/start', async (route) => {
			await route.fulfill({
				status: 200,
				contentType: 'application/json',
				body: JSON.stringify({
					device_code: 'test_device_code_123',
					user_code: 'WXYZ-5678',
					verification_uri: 'https://github.com/login/device',
					expires_in: 900,
					interval: 5
				})
			});
		});

		await page.goto('/');
		await page.getByRole('button', { name: /Continue with GitHub/i }).click();
		
		// Wait for device code
		await expect(page.getByText('WXYZ-5678')).toBeVisible();
		
		// Click copy button
		await page.getByRole('button', { title: 'Copy code' }).click();
		
		// Verify clipboard content
		const clipboardText = await page.evaluate(() => navigator.clipboard.readText());
		expect(clipboardText).toBe('WXYZ-5678');
	});

	test('should handle authentication success', async ({ page }) => {
		// Mock device flow start
		await page.route('**/auth/github/device/start', async (route) => {
			await route.fulfill({
				status: 200,
				contentType: 'application/json',
				body: JSON.stringify({
					device_code: 'test_device_code_123',
					user_code: 'TEST-CODE',
					verification_uri: 'https://github.com/login/device',
					expires_in: 900,
					interval: 5
				})
			});
		});

		// Mock successful polling
		await page.route('**/auth/github/device/poll', async (route) => {
			await route.fulfill({
				status: 200,
				contentType: 'application/json',
				body: JSON.stringify({
					access_token: 'gho_test_token_123',
					token_type: 'bearer',
					scope: 'repo,read:user,user:email',
					user: {
						login: 'testuser',
						name: 'Test User',
						email: 'test@example.com',
						avatar_url: 'https://github.com/testuser.png'
					}
				})
			});
		});

		await page.goto('/');
		await page.getByRole('button', { name: /Continue with GitHub/i }).click();
		
		// Wait for authentication to complete
		// Should redirect to main app (not login page)
		await page.waitForTimeout(6000); // Wait for polling
		
		// Check that we're no longer on login page
		await expect(page.getByRole('heading', { name: 'PersonAI' })).not.toBeVisible();
	});

	test('should handle authentication error', async ({ page }) => {
		// Mock failed API call
		await page.route('**/auth/github/device/start', async (route) => {
			await route.fulfill({
				status: 500,
				contentType: 'application/json',
				body: JSON.stringify({
					detail: 'GitHub OAuth not configured'
				})
			});
		});

		await page.goto('/');
		await page.getByRole('button', { name: /Continue with GitHub/i }).click();
		
		// Should show error message
		await expect(page.getByText(/GitHub OAuth is not configured/i)).toBeVisible();
	});

	test('should be responsive on mobile', async ({ page }) => {
		await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
		await page.goto('/');
		
		// Check that elements are visible and properly sized
		await expect(page.getByRole('heading', { name: 'PersonAI' })).toBeVisible();
		const loginButton = page.getByRole('button', { name: /Continue with GitHub/i });
		await expect(loginButton).toBeVisible();
		
		// Check button is full width on mobile
		const buttonBox = await loginButton.boundingBox();
		expect(buttonBox?.width).toBeGreaterThan(300); // Should be nearly full width
	});
});
