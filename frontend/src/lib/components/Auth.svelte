<script lang="ts">
	import { authStore, login } from '$lib/auth';
	import { createEventDispatcher, onMount } from 'svelte';

	const dispatch = createEventDispatcher();

	let error = $state('');
	let isLoading = $state(false);
	let deviceCode = $state('');
	let userCode = $state('');
	let verificationUri = $state('');
	let isPolling = $state(false);
	
	// Auto-detect API URL (Codespace or local)
	const API_URL = import.meta.env.VITE_API_URL || 
		(typeof window !== 'undefined' && window.location.hostname.includes('github.dev')
			? window.location.origin.replace('-5173', '-8080')
			: 'http://localhost:8080');

	async function handleGitHubLogin() {
		isLoading = true;
		error = '';

		try {
			// Start device flow
			const response = await fetch(`${API_URL}/auth/github/device/start`);
			const data = await response.json();

			if (data.device_code) {
				deviceCode = data.device_code;
				userCode = data.user_code;
				verificationUri = data.verification_uri;
				
				// Open GitHub authorization page
				window.open(verificationUri, '_blank');
				
				// Start polling
				isPolling = true;
				pollForToken();
			} else {
				error = 'Failed to start GitHub authentication';
			}
		} catch (err) {
			error = 'GitHub OAuth is not configured. Please set GITHUB_CLIENT_ID.';
			console.error(err);
		} finally {
			isLoading = false;
		}
	}

	async function pollForToken() {
		const maxAttempts = 60; // 5 minutes with 5 second intervals
		let attempts = 0;

		const poll = async () => {
			if (attempts >= maxAttempts) {
				error = 'Authentication timeout. Please try again.';
				isPolling = false;
				return;
			}

			try {
				const response = await fetch(`${API_URL}/auth/github/device/poll`, {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({ device_code: deviceCode })
				});

				const data = await response.json();

				if (data.access_token) {
					// Success!
					const user = data.user;
					login(data.access_token, {
						name: user.name || user.login,
						email: user.email || `${user.login}@github.com`
					});
					
					isPolling = false;
					dispatch('authenticated');
				} else if (data.error === 'authorization_pending') {
					// Still waiting, poll again
					attempts++;
					setTimeout(poll, 5000);
				} else if (data.error === 'slow_down') {
					// Rate limited, wait longer
					attempts++;
					setTimeout(poll, 10000);
				} else if (data.error) {
					// Other error
					error = `Authentication failed: ${data.error_description || data.error}`;
					isPolling = false;
				}
			} catch (err) {
				error = 'Failed to check authentication status';
				console.error(err);
				isPolling = false;
			}
		};

		poll();
	}

	function copyUserCode() {
		navigator.clipboard.writeText(userCode);
	}
</script>

<div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-purple-600 p-4">
	<div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8 max-w-md w-full">
		<div class="text-center mb-8">
			<div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-br from-primary-500 to-purple-600 text-white text-2xl font-bold mb-4">
				AI
			</div>
			<h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">PersonAI</h1>
			<p class="text-gray-600 dark:text-gray-400">Your Personal AI Assistant</p>
		</div>

		<div class="space-y-4">
			{#if error}
				<div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg text-sm">
					{error}
				</div>
			{/if}

			{#if isPolling && userCode}
				<div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
					<p class="text-sm text-blue-900 dark:text-blue-100 mb-3">
						Enter this code on GitHub:
					</p>
					<div class="flex items-center gap-2 mb-3">
						<code class="flex-1 text-2xl font-mono font-bold text-center bg-white dark:bg-gray-900 px-4 py-3 rounded border-2 border-blue-300 dark:border-blue-700 text-blue-600 dark:text-blue-400">
							{userCode}
						</code>
						<button
							onclick={copyUserCode}
							class="px-3 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
							title="Copy code"
						>
							<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
							</svg>
						</button>
					</div>
					<div class="flex items-center justify-center gap-2 text-sm text-blue-700 dark:text-blue-300">
						<svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
							<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
							<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
						</svg>
						Waiting for authorization...
					</div>
				</div>
			{/if}

			<button
				onclick={handleGitHubLogin}
				disabled={isLoading || isPolling}
				class="w-full px-6 py-3 bg-gray-900 hover:bg-gray-800 disabled:bg-gray-400 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-all transform hover:scale-[1.02] disabled:scale-100 flex items-center justify-center gap-3"
			>
				{#if isLoading}
					<svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
						<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
						<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
					</svg>
					Starting...
				{:else if isPolling}
					<svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
						<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
						<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
					</svg>
					Waiting for GitHub...
				{:else}
					<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
						<path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
					</svg>
					Continue with GitHub
				{/if}
			</button>

			<div class="text-center text-sm text-gray-600 dark:text-gray-400 mt-6">
				<p>🔒 Secure device flow authentication</p>
				<p class="mt-2">No callback URLs or redirects needed</p>
			</div>
		</div>
	</div>
</div>
