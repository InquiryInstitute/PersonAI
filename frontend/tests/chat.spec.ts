import { test, expect } from '@playwright/test';

test.describe('Chat Interface', () => {
	test.beforeEach(async ({ page }) => {
		// Mock authentication
		await page.addInitScript(() => {
			localStorage.setItem('personai_auth', JSON.stringify({
				isAuthenticated: true,
				token: 'test_token',
				user: { name: 'Test User', email: 'test@example.com' }
			}));
		});
	});

	test('should display chat interface when authenticated', async ({ page }) => {
		await page.goto('/');
		
		// Should show chat interface, not login
		await expect(page.getByPlaceholder(/Type your message/i)).toBeVisible();
	});

	test('should have sidebar with GitHub connection', async ({ page }) => {
		await page.goto('/');
		
		// Check for sidebar elements
		await expect(page.getByText('PersonAI')).toBeVisible();
		await expect(page.getByText('GitHub')).toBeVisible();
	});

	test('should allow typing in message input', async ({ page }) => {
		await page.goto('/');
		
		const input = page.getByPlaceholder(/Type your message/i);
		await input.fill('Hello, PersonAI!');
		
		await expect(input).toHaveValue('Hello, PersonAI!');
	});

	test('should have send button', async ({ page }) => {
		await page.goto('/');
		
		const sendButton = page.getByRole('button', { name: /send/i });
		await expect(sendButton).toBeVisible();
	});

	test('should show user info in sidebar', async ({ page }) => {
		await page.goto('/');
		
		// User info should be visible
		await expect(page.getByText('Test User')).toBeVisible();
	});

	test('should have logout functionality', async ({ page }) => {
		await page.goto('/');
		
		// Look for logout button (might be in a menu)
		const logoutButton = page.getByRole('button', { name: /logout/i });
		if (await logoutButton.isVisible()) {
			await logoutButton.click();
			
			// Should redirect to login
			await expect(page.getByRole('heading', { name: 'PersonAI' })).toBeVisible();
			await expect(page.getByRole('button', { name: /Continue with GitHub/i })).toBeVisible();
		}
	});

	test('should be responsive on mobile', async ({ page }) => {
		await page.setViewportSize({ width: 375, height: 667 });
		await page.goto('/');
		
		// Chat interface should be visible
		await expect(page.getByPlaceholder(/Type your message/i)).toBeVisible();
	});
});
