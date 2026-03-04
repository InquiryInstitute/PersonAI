/**
 * MCP (Model Context Protocol) Client for PersonAI
 * 
 * This module provides integration with Continue-style MCP servers
 * allowing PersonAI to use the same tools available in Continue/Cursor
 */

export interface MCPTool {
	name: string;
	description: string;
	inputSchema: Record<string, any>;
	server: string;
}

export interface MCPResource {
	uri: string;
	name: string;
	description?: string;
	mimeType?: string;
}

export interface MCPServer {
	name: string;
	command: string;
	args?: string[];
	env?: Record<string, string>;
}

export class MCPClient {
	private servers: Map<string, MCPServer> = new Map();
	private tools: Map<string, MCPTool[]> = new Map();

	constructor(private backendUrl: string = 'http://localhost:8080') {}

	/**
	 * Register an MCP server
	 */
	registerServer(name: string, server: MCPServer) {
		this.servers.set(name, server);
	}

	/**
	 * List all available tools from all registered servers
	 */
	async listTools(): Promise<MCPTool[]> {
		const allTools: MCPTool[] = [];
		
		for (const [serverName, _] of this.servers) {
			try {
				const response = await fetch(`${this.backendUrl}/mcp/${serverName}/tools`);
				if (response.ok) {
					const tools: MCPTool[] = await response.json();
					allTools.push(...tools.map(t => ({ ...t, server: serverName })));
					this.tools.set(serverName, tools);
				}
			} catch (error) {
				console.error(`Failed to list tools from ${serverName}:`, error);
			}
		}

		return allTools;
	}

	/**
	 * Call an MCP tool
	 */
	async callTool(serverName: string, toolName: string, args: Record<string, any>): Promise<any> {
		try {
			const response = await fetch(`${this.backendUrl}/mcp/${serverName}/call`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					tool: toolName,
					arguments: args
				})
			});

			if (!response.ok) {
				throw new Error(`Tool call failed: ${response.statusText}`);
			}

			return await response.json();
		} catch (error) {
			console.error(`Failed to call tool ${toolName} on ${serverName}:`, error);
			throw error;
		}
	}

	/**
	 * List resources from an MCP server
	 */
	async listResources(serverName: string): Promise<MCPResource[]> {
		try {
			const response = await fetch(`${this.backendUrl}/mcp/${serverName}/resources`);
			if (response.ok) {
				return await response.json();
			}
		} catch (error) {
			console.error(`Failed to list resources from ${serverName}:`, error);
		}
		return [];
	}

	/**
	 * Fetch a resource from an MCP server
	 */
	async fetchResource(serverName: string, uri: string): Promise<any> {
		try {
			const response = await fetch(`${this.backendUrl}/mcp/${serverName}/resource`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ uri })
			});

			if (!response.ok) {
				throw new Error(`Resource fetch failed: ${response.statusText}`);
			}

			return await response.json();
		} catch (error) {
			console.error(`Failed to fetch resource ${uri} from ${serverName}:`, error);
			throw error;
		}
	}
}

/**
 * Create default MCP client with common servers
 */
export function createDefaultMCPClient(): MCPClient {
	const client = new MCPClient();

	// Register common MCP servers (matching Continue's configuration)
	client.registerServer('filesystem', {
		name: 'filesystem',
		command: 'npx',
		args: ['-y', '@modelcontextprotocol/server-filesystem']
	});

	client.registerServer('github', {
		name: 'github',
		command: 'npx',
		args: ['-y', '@modelcontextprotocol/server-github']
	});

	client.registerServer('git', {
		name: 'git',
		command: 'npx',
		args: ['-y', '@modelcontextprotocol/server-git']
	});

	return client;
}
