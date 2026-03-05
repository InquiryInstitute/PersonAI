# Testing PersonAI

PersonAI uses Playwright for end-to-end testing, ensuring the application works correctly across different browsers and devices.

## Running Tests

### Local Development

```bash
cd frontend

# Run all tests
npm run test

# Run tests in UI mode (interactive)
npm run test:ui

# Run tests in headed mode (see browser)
npm run test:headed

# Debug tests
npm run test:debug

# View test report
npm run test:report
```

### Specific Tests

```bash
# Run only auth tests
npx playwright test auth

# Run only chat tests
npx playwright test chat

# Run only accessibility tests
npx playwright test accessibility

# Run specific test file
npx playwright test tests/auth.spec.ts
```

### Browser Selection

```bash
# Run on specific browser
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit

# Run on mobile
npx playwright test --project="Mobile Chrome"
npx playwright test --project="Mobile Safari"
```

## Test Structure

### Test Files

- `tests/auth.spec.ts` - Authentication flow tests
  - Login page display
  - Device code flow
  - Clipboard functionality
  - Error handling
  - Mobile responsiveness

- `tests/chat.spec.ts` - Chat interface tests
  - Chat UI display
  - Message input
  - Sidebar functionality
  - User info display
  - Logout functionality

- `tests/accessibility.spec.ts` - Accessibility tests
  - WCAG 2.0 AA compliance
  - Keyboard navigation
  - Screen reader support
  - Color contrast
  - Semantic HTML

### Test Configuration

`playwright.config.ts` configures:
- Test directory
- Browser projects (Chrome, Firefox, Safari, Mobile)
- Base URL
- Screenshots on failure
- Trace on retry
- Web server auto-start

## Writing Tests

### Basic Test Structure

```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
	test('should do something', async ({ page }) => {
		await page.goto('/');
		
		// Interact with page
		await page.getByRole('button', { name: 'Click me' }).click();
		
		// Assert expectations
		await expect(page.getByText('Success')).toBeVisible();
	});
});
```

### Mocking API Calls

```typescript
test('should handle API response', async ({ page }) => {
	// Mock backend API
	await page.route('**/api/endpoint', async (route) => {
		await route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify({ data: 'test' })
		});
	});
	
	await page.goto('/');
	// Test continues...
});
```

### Testing Authentication

```typescript
test.beforeEach(async ({ page }) => {
	// Mock authenticated state
	await page.addInitScript(() => {
		localStorage.setItem('personai_auth', JSON.stringify({
			isAuthenticated: true,
			token: 'test_token',
			user: { name: 'Test User', email: 'test@example.com' }
		}));
	});
});
```

### Accessibility Testing

```typescript
import AxeBuilder from '@axe-core/playwright';

test('should not have accessibility violations', async ({ page }) => {
	await page.goto('/');
	
	const results = await new AxeBuilder({ page }).analyze();
	expect(results.violations).toEqual([]);
});
```

## CI/CD Integration

Tests run automatically on:
- Push to main branch
- Pull requests
- Manual workflow dispatch

### GitHub Actions

The `.github/workflows/test.yml` workflow:
1. Checks out code
2. Installs dependencies
3. Installs Playwright browsers
4. Runs tests
5. Uploads test reports and screenshots

### Viewing Results

- Test reports: Available as artifacts in GitHub Actions
- Screenshots: Uploaded on test failures
- Traces: Available for debugging failed tests

## Test Coverage

### Current Coverage

- ✅ Authentication flow
- ✅ Device code display and copy
- ✅ Error handling
- ✅ Mobile responsiveness
- ✅ Accessibility compliance
- ✅ Keyboard navigation
- ✅ Chat interface basics

### TODO

- [ ] GitHub repository connection
- [ ] File browsing
- [ ] Monaco editor integration
- [ ] Message sending and receiving
- [ ] Code syntax highlighting
- [ ] Dark mode toggle
- [ ] Settings management

## Best Practices

### 1. Use Semantic Selectors

```typescript
// Good - semantic and stable
await page.getByRole('button', { name: 'Login' });
await page.getByLabel('Email');
await page.getByText('Welcome');

// Avoid - brittle and non-semantic
await page.locator('.btn-primary');
await page.locator('#email-input');
```

### 2. Wait for Elements

```typescript
// Good - explicit wait
await expect(page.getByText('Success')).toBeVisible();

// Avoid - implicit wait
await page.waitForTimeout(1000);
```

### 3. Mock External Dependencies

```typescript
// Mock API calls to avoid flaky tests
await page.route('**/api/**', async (route) => {
	await route.fulfill({ body: '{"status": "ok"}' });
});
```

### 4. Test User Flows, Not Implementation

```typescript
// Good - tests user behavior
test('user can login', async ({ page }) => {
	await page.goto('/');
	await page.getByRole('button', { name: 'Login' }).click();
	await expect(page.getByText('Welcome')).toBeVisible();
});

// Avoid - tests implementation details
test('login button calls handleLogin', async ({ page }) => {
	// Don't test internal functions
});
```

### 5. Keep Tests Independent

```typescript
// Good - each test is independent
test('test 1', async ({ page }) => {
	await page.goto('/');
	// Test logic
});

test('test 2', async ({ page }) => {
	await page.goto('/');
	// Test logic
});

// Avoid - tests depend on each other
```

## Debugging Tests

### Visual Debugging

```bash
# Run with UI mode
npm run test:ui

# Run in headed mode
npm run test:headed

# Debug specific test
npm run test:debug tests/auth.spec.ts
```

### Trace Viewer

```bash
# Generate trace
npx playwright test --trace on

# View trace
npx playwright show-trace trace.zip
```

### Screenshots

Screenshots are automatically captured on failure and saved to `test-results/`.

### Console Logs

```typescript
test('debug test', async ({ page }) => {
	page.on('console', msg => console.log(msg.text()));
	await page.goto('/');
});
```

## Performance Testing

### Lighthouse Integration

```typescript
import { playAudit } from 'playwright-lighthouse';

test('should pass lighthouse audit', async ({ page }) => {
	await page.goto('/');
	
	await playAudit({
		page,
		thresholds: {
			performance: 90,
			accessibility: 90,
			'best-practices': 90,
			seo: 90,
		},
	});
});
```

## Resources

- [Playwright Documentation](https://playwright.dev/)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Axe Accessibility Testing](https://www.deque.com/axe/)
- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
