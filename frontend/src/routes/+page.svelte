<script lang="ts">
	import { onMount } from 'svelte';
	import ChatInterface from '$lib/components/ChatInterface.svelte';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import MonacoEditor from '$lib/components/MonacoEditor.svelte';
	import Auth from '$lib/components/Auth.svelte';
	import { authStore, initAuth, logout } from '$lib/auth';

	let isSidebarOpen = $state(true);
	let isEditorOpen = $state(false);
	let currentFile = $state<{ path: string; content: string } | null>(null);
	let githubRepo = $state<string>('');
	let isAuthenticated = $state(false);

	// Subscribe to auth store
	$effect(() => {
		const unsubscribe = authStore.subscribe((auth) => {
			isAuthenticated = auth.isAuthenticated;
		});
		return unsubscribe;
	});

	onMount(() => {
		initAuth();
	});

	function toggleSidebar() {
		isSidebarOpen = !isSidebarOpen;
	}

	function openFile(path: string, content: string) {
		currentFile = { path, content };
		isEditorOpen = true;
	}

	function closeEditor() {
		isEditorOpen = false;
		currentFile = null;
	}

	function handleLogout() {
		if (confirm('Are you sure you want to logout?')) {
			logout();
		}
	}
</script>

{#if !isAuthenticated}
	<Auth on:authenticated={() => {}} />
{:else}
	<div class="flex h-screen bg-gray-50 dark:bg-gray-900">
		<!-- Sidebar -->
		<Sidebar bind:isOpen={isSidebarOpen} bind:githubRepo on:openFile={(e) => openFile(e.detail.path, e.detail.content)} />

		<!-- Main Content Area -->
		<div class="flex-1 flex flex-col overflow-hidden">
			<!-- Header -->
			<header class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 py-3 flex items-center justify-between">
				<div class="flex items-center gap-4">
					<button onclick={toggleSidebar} class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
						<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
						</svg>
					</button>
					<h1 class="text-xl font-bold text-gray-900 dark:text-white">PersonAI</h1>
				</div>
				<div class="flex items-center gap-4">
					{#if githubRepo}
						<span class="text-sm text-gray-600 dark:text-gray-400 hidden md:flex items-center">
							<svg class="w-4 h-4 inline-block mr-1" fill="currentColor" viewBox="0 0 24 24">
								<path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
							</svg>
							{githubRepo}
						</span>
					{/if}
					<button
						onclick={handleLogout}
						class="px-3 py-1 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
					>
						Logout
					</button>
				</div>
			</header>

			<!-- Main Content -->
			<div class="flex-1 flex overflow-hidden">
				<!-- Chat Area -->
				<div class={isEditorOpen ? 'w-1/2' : 'flex-1'}>
					<ChatInterface {githubRepo} />
				</div>

				<!-- Editor Area -->
				{#if isEditorOpen && currentFile}
					<div class="w-1/2 border-l border-gray-200 dark:border-gray-700">
						<MonacoEditor file={currentFile} onClose={closeEditor} />
					</div>
				{/if}
			</div>
		</div>
	</div>
{/if}
