<script lang="ts">
	import { marked } from 'marked';
	import DOMPurify from 'dompurify';

	interface Message {
		id: string;
		role: 'user' | 'assistant';
		content: string;
		timestamp: Date;
	}

	interface Props {
		message: Message;
	}

	let { message }: Props = $props();

	const renderedContent = $derived(() => {
		if (message.role === 'assistant') {
			const rawHtml = marked.parse(message.content) as string;
			return DOMPurify.sanitize(rawHtml);
		}
		return message.content;
	});

	const timeString = $derived(() => {
		return message.timestamp.toLocaleTimeString('en-US', {
			hour: '2-digit',
			minute: '2-digit'
		});
	});
</script>

<div class="chat-message {message.role}">
	<div class="flex items-start gap-3">
		<div class="flex-shrink-0">
			{#if message.role === 'user'}
				<div class="w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center text-white font-medium">
					U
				</div>
			{:else}
				<div class="w-8 h-8 rounded-full bg-gradient-to-br from-primary-500 to-purple-600 flex items-center justify-center text-white font-medium">
					AI
				</div>
			{/if}
		</div>

		<div class="flex-1 min-w-0">
			<div class="flex items-center gap-2 mb-1">
				<span class="font-medium text-sm">
					{message.role === 'user' ? 'You' : 'PersonAI'}
				</span>
				<span class="text-xs text-gray-500 dark:text-gray-400">
					{timeString()}
				</span>
			</div>

			{#if message.role === 'assistant'}
				<div class="prose prose-sm dark:prose-invert max-w-none">
					{@html renderedContent()}
				</div>
			{:else}
				<div class="whitespace-pre-wrap text-sm">
					{message.content}
				</div>
			{/if}
		</div>
	</div>
</div>
