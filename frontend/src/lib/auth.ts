import { writable } from 'svelte/store';

export const authStore = writable<{
	isAuthenticated: boolean;
	token: string | null;
	user: { name: string; email: string } | null;
}>({
	isAuthenticated: false,
	token: null,
	user: null
});

const AUTH_KEY = 'personai_auth';

export function initAuth() {
	if (typeof window !== 'undefined') {
		const stored = localStorage.getItem(AUTH_KEY);
		if (stored) {
			try {
				const auth = JSON.parse(stored);
				authStore.set(auth);
			} catch (e) {
				console.error('Failed to parse auth data', e);
			}
		}
	}
}

export function login(token: string, user: { name: string; email: string }) {
	const auth = {
		isAuthenticated: true,
		token,
		user
	};
	authStore.set(auth);
	if (typeof window !== 'undefined') {
		localStorage.setItem(AUTH_KEY, JSON.stringify(auth));
	}
}

export function logout() {
	authStore.set({
		isAuthenticated: false,
		token: null,
		user: null
	});
	if (typeof window !== 'undefined') {
		localStorage.removeItem(AUTH_KEY);
		localStorage.removeItem('github_token');
		localStorage.removeItem('github_repo');
	}
}

export function getAuthToken(): string | null {
	let token: string | null = null;
	authStore.subscribe((auth) => {
		token = auth.token;
	})();
	return token;
}
