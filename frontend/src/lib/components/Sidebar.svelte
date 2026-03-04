<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { Octokit } from '@octokit/rest';

	interface Props {
		isOpen?: boolean;
		githubRepo?: string;
	}

	let { isOpen = true, githubRepo = $bindable('') }: Props = $props();

	const dispatch = createEventDispatcher();

	let repoInput = $state('');
	let files = $state<Array<{ path: string; type: string }>>([]);
	let isLoadingFiles = $state(false);
	let error = $state('');
	let githubToken = $state('');

	async function connectToRepo() {
		if (!repoInput.trim() || !githubToken.trim()) {
			error = 'Please enter both repository and GitHub token';
			return;
		}

		error = '';
		isLoadingFiles = true;
		githubRepo = repoInput;

		try {
			const octokit = new Octokit({ auth: githubToken });
			const [owner, repo] = repoInput.split('/');

			if (!owner || !repo) {
				throw new Error('Invalid repository format. Use: owner/repo');
			}

			// Get repository tree
			const { data: repoData } = await octokit.repos.get({ owner, repo });
			const { data: treeData } = await octokit.git.getTree({
				owner,
				repo,
				tree_sha: repoData.default_branch,
				recursive: 'true'
			});

			files = treeData.tree
				.filter((item: any) => item.type === 'blob')
				.map((item: any) => ({
					path: item.path,
					type: item.type
				}));

			// Save token to localStorage
			if (typeof window !== 'undefined') {
				localStorage.setItem('github_token', githubToken);
				localStorage.setItem('github_repo', repoInput);
			}
		} catch (err: any) {
			error = err.message || 'Failed to connect to repository';
			files = [];
		} finally {
			isLoadingFiles = false;
		}
	}

	async function loadFile(filePath: string) {
		if (!githubRepo || !githubToken) return;

		try {
			const octokit = new Octokit({ auth: githubToken });
			const [owner, repo] = githubRepo.split('/');

			const { data } = await octokit.repos.getContent({
				owner,
				repo,
				path: filePath
			});

			if ('content' in data && data.encoding === 'base64') {
				const content = atob(data.content);
				dispatch('openFile', { path: filePath, content });
			}
		} catch (err) {
			console.error('Failed to load file:', err);
		}
	}

	// Load saved credentials on mount
	$effect(() => {
		if (typeof window !== 'undefined') {
			const savedToken = localStorage.getItem('github_token');
			const savedRepo = localStorage.getItem('github_repo');
			
			if (savedToken) githubToken = savedToken;
			if (savedRepo) {
				repoInput = savedRepo;
				githubRepo = savedRepo;
			}
		}
	});
</script>

<aside
	class="w-80 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col transition-all duration-300 {isOpen ? '' : '-ml-80'}"
>
	<div class="p-4 border-b border-gray-200 dark:border-gray-700">
		<h2 class="text-lg font-semibold mb-4">GitHub Repository</h2>
		
		<div class="space-y-3">
			<div>
				<label class="block text-sm font-medium mb-1" for="github-token">
					GitHub Token
				</label>
				<input
					id="github-token"
					type="password"
					bind:value={githubToken}
					placeholder="ghp_..."
					class="input text-sm"
				/>
			</div>

			<div>
				<label class="block text-sm font-medium mb-1" for="repo-input">
					Repository
				</label>
				<input
					id="repo-input"
					type="text"
					bind:value={repoInput}
					placeholder="owner/repository"
					class="input text-sm"
				/>
			</div>

			<button
				onclick={connectToRepo}
				disabled={isLoadingFiles}
				class="btn btn-primary w-full"
			>
				{isLoadingFiles ? 'Connecting...' : 'Connect'}
			</button>

			{#if error}
				<p class="text-sm text-red-600 dark:text-red-400">{error}</p>
			{/if}
		</div>
	</div>

	{#if githubRepo}
		<div class="flex-1 overflow-y-auto p-4">
			<h3 class="text-sm font-semibold mb-2 text-gray-700 dark:text-gray-300">
				Files ({files.length})
			</h3>

			{#if files.length === 0}
				<p class="text-sm text-gray-500">No files loaded</p>
			{:else}
				<ul class="space-y-1">
					{#each files as file}
						<li>
							<button
								onclick={() => loadFile(file.path)}
								class="w-full text-left text-sm px-2 py-1.5 rounded hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
							>
								<div class="flex items-center gap-2">
									<svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
									</svg>
									<span class="truncate">{file.path}</span>
								</div>
							</button>
						</li>
					{/each}
				</ul>
			{/if}
		</div>
	{/if}

	<div class="p-4 border-t border-gray-200 dark:border-gray-700">
		<p class="text-xs text-gray-500 dark:text-gray-400">
			PersonAI v0.2.0
		</p>
		<p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
			<a href="https://github.com/InquiryInstitute/personAI" target="_blank" class="hover:text-primary-600">
				GitHub
			</a>
		</p>
	</div>
</aside>
