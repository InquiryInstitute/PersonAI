<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';

	let { children } = $props();

	onMount(() => {
		// Register service worker for PWA
		if ('serviceWorker' in navigator) {
			navigator.serviceWorker
				.register('/PersonAI/service-worker.js')
				.then((registration) => {
					console.log('Service Worker registered:', registration);
				})
				.catch((error) => {
					console.log('Service Worker registration failed:', error);
				});
		}
	});
</script>

<svelte:head>
	<title>PersonAI - Your Personal AI Assistant</title>
	<meta name="description" content="A personal AI assistant for students" />
	<meta name="theme-color" content="#0ea5e9" />
	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
	<meta name="mobile-web-app-capable" content="yes" />
	<meta name="apple-mobile-web-app-capable" content="yes" />
	<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
	<meta name="apple-mobile-web-app-title" content="PersonAI" />
	<link rel="manifest" href="/PersonAI/manifest.json" />
	<link rel="icon" type="image/png" sizes="192x192" href="/PersonAI/icon-192.png" />
	<link rel="apple-touch-icon" href="/PersonAI/icon-192.png" />
</svelte:head>

{@render children()}
