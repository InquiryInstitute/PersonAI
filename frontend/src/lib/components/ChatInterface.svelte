<script lang="ts">
	import { onMount } from 'svelte';
	import ChatMessage from './ChatMessage.svelte';

	interface Message {
		id: string;
		role: 'user' | 'assistant';
		content: string;
		timestamp: Date;
	}

	interface Props {
		githubRepo?: string;
	}

	let { githubRepo = '' }: Props = $props();

	let messages = $state<Message[]>([
		{
			id: '1',
			role: 'assistant',
			content: "Hello! I'm PersonAI, your personal AI assistant. I can help you work with your GitHub repositories, edit files, and answer questions about your code. How can I help you today?",
			timestamp: new Date()
		}
	]);
	let inputMessage = $state('');
	let isLoading = $state(false);
	let messagesContainer: HTMLDivElement;

	async function sendMessage() {
		if (!inputMessage.trim() || isLoading) return;

		const userMessage: Message = {
			id: Date.now().toString(),
			role: 'user',
			content: inputMessage,
			timestamp: new Date()
		};

		messages = [...messages, userMessage];
		const currentInput = inputMessage;
		inputMessage = '';
		isLoading = true;

		try {
			// Call the FastAPI backend
			const response = await fetch('http://localhost:8080/query', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					question: currentInput,
					sources: ['github', 'drive', 'web']
				})
			});

			if (!response.ok) {
				throw new Error('Failed to get response');
			}

			const data = await response.json();

			const assistantMessage: Message = {
				id: (Date.now() + 1).toString(),
				role: 'assistant',
				content: data.answer,
				timestamp: new Date()
			};

			messages = [...messages, assistantMessage];
		} catch (error) {
			console.error('Error sending message:', error);
			const errorMessage: Message = {
				id: (Date.now() + 1).toString(),
				role: 'assistant',
				content: "I'm sorry, I encountered an error processing your request. Please make sure the backend server is running.",
				timestamp: new Date()
			};
			messages = [...messages, errorMessage];
		} finally {
			isLoading = false;
		}
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			sendMessage();
		}
	}

	$effect(() => {
		if (messagesContainer) {
			messagesContainer.scrollTop = messagesContainer.scrollHeight;
		}
	});
</script>

<div class="flex flex-col h-full">
	<!-- Messages Area -->
	<div bind:this={messagesContainer} class="flex-1 overflow-y-auto p-4 space-y-4">
		{#each messages as message (message.id)}
			<ChatMessage {message} />
		{/each}

		{#if isLoading}
			<div class="flex items-center gap-2 text-gray-500 dark:text-gray-400">
				<div class="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
				<span>Thinking...</span>
			</div>
		{/if}
	</div>

	<!-- Input Area -->
	<div class="border-t border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-800">
		<form onsubmit={(e) => { e.preventDefault(); sendMessage(); }} class="flex gap-2">
			<textarea
				bind:value={inputMessage}
				onkeydown={handleKeydown}
				placeholder="Type your message... (Enter to send, Shift+Enter for new line)"
				class="flex-1 resize-none rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 px-4 py-2 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
				rows="3"
			></textarea>
			<button
				type="submit"
				disabled={isLoading || !inputMessage.trim()}
				class="px-6 py-2 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
			>
				Send
			</button>
		</form>
		<p class="text-xs text-gray-500 dark:text-gray-400 mt-2">
			Connected to: {githubRepo || 'No repository selected'}
		</p>
	</div>
</div>
