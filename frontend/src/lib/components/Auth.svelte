<script lang="ts">
	import { authStore, login } from '$lib/auth';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	let passphrase = $state('');
	let error = $state('');
	let isLoading = $state(false);

	async function handleLogin() {
		if (!passphrase.trim()) {
			error = 'Please enter a passphrase';
			return;
		}

		isLoading = true;
		error = '';

		try {
			// For demo purposes, we'll use a simple passphrase-based auth
			// In production, this should integrate with GitHub OAuth or similar
			
			// Generate a simple token from the passphrase
			const encoder = new TextEncoder();
			const data = encoder.encode(passphrase);
			const hashBuffer = await crypto.subtle.digest('SHA-256', data);
			const hashArray = Array.from(new Uint8Array(hashBuffer));
			const token = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

			// Store authentication
			login(token, {
				name: 'Student',
				email: 'student@example.com'
			});

			dispatch('authenticated');
		} catch (err) {
			error = 'Authentication failed';
			console.error(err);
		} finally {
			isLoading = false;
		}
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			handleLogin();
		}
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
			<div>
				<label for="passphrase" class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
					Passphrase
				</label>
				<input
					id="passphrase"
					type="password"
					bind:value={passphrase}
					onkeydown={handleKeydown}
					placeholder="Enter your passphrase"
					class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
					disabled={isLoading}
				/>
			</div>

			{#if error}
				<div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg text-sm">
					{error}
				</div>
			{/if}

			<button
				onclick={handleLogin}
				disabled={isLoading || !passphrase.trim()}
				class="w-full px-6 py-3 bg-gradient-to-r from-primary-600 to-purple-600 hover:from-primary-700 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-all transform hover:scale-[1.02] disabled:scale-100"
			>
				{isLoading ? 'Authenticating...' : 'Login'}
			</button>

			<div class="text-center text-sm text-gray-600 dark:text-gray-400 mt-6">
				<p>🔒 Your data is encrypted and stored locally</p>
				<p class="mt-2">For mobile use, save this page to your home screen</p>
			</div>
		</div>
	</div>
</div>
