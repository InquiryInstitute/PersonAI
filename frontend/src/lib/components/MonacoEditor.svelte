<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import * as monaco from 'monaco-editor';

	interface Props {
		file: { path: string; content: string };
		onClose: () => void;
	}

	let { file, onClose }: Props = $props();

	let editorContainer: HTMLDivElement;
	let editor: monaco.editor.IStandaloneCodeEditor | null = null;

	const getLanguage = (filename: string): string => {
		const ext = filename.split('.').pop()?.toLowerCase();
		const languageMap: Record<string, string> = {
			js: 'javascript',
			ts: 'typescript',
			tsx: 'typescript',
			jsx: 'javascript',
			py: 'python',
			java: 'java',
			cpp: 'cpp',
			c: 'c',
			cs: 'csharp',
			rb: 'ruby',
			go: 'go',
			rs: 'rust',
			php: 'php',
			html: 'html',
			css: 'css',
			scss: 'scss',
			json: 'json',
			xml: 'xml',
			md: 'markdown',
			sql: 'sql',
			sh: 'shell',
			yaml: 'yaml',
			yml: 'yaml'
		};
		return languageMap[ext || ''] || 'plaintext';
	};

	onMount(() => {
		if (editorContainer) {
			// Configure Monaco Editor
			editor = monaco.editor.create(editorContainer, {
				value: file.content,
				language: getLanguage(file.path),
				theme: 'vs-dark',
				automaticLayout: true,
				minimap: { enabled: true },
				fontSize: 14,
				lineNumbers: 'on',
				scrollBeyondLastLine: false,
				wordWrap: 'on',
				readOnly: false
			});
		}
	});

	onDestroy(() => {
		if (editor) {
			editor.dispose();
		}
	});

	function handleSave() {
		if (editor) {
			const content = editor.getValue();
			console.log('Saving file:', file.path, content);
			// TODO: Implement save functionality with GitHub API
			alert('Save functionality coming soon!');
		}
	}
</script>

<div class="flex flex-col h-full bg-gray-900">
	<!-- Editor Header -->
	<div class="bg-gray-800 border-b border-gray-700 px-4 py-2 flex items-center justify-between">
		<div class="flex items-center gap-3">
			<span class="text-sm text-gray-300 font-mono">{file.path}</span>
		</div>
		<div class="flex items-center gap-2">
			<button
				onclick={handleSave}
				class="px-3 py-1 text-sm bg-primary-600 hover:bg-primary-700 text-white rounded transition-colors"
			>
				Save
			</button>
			<button
				onclick={onClose}
				class="p-1 hover:bg-gray-700 rounded transition-colors"
			>
				<svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
				</svg>
			</button>
		</div>
	</div>

	<!-- Editor Container -->
	<div bind:this={editorContainer} class="flex-1"></div>
</div>
