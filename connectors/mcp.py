"""
MCP (Model Context Protocol) Server Integration for PersonAI
Provides compatibility with Continue/Cursor MCP tools
"""
import subprocess
import json
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import os


@dataclass
class MCPServer:
    name: str
    command: str
    args: List[str]
    env: Optional[Dict[str, str]] = None


class MCPServerManager:
    """Manages MCP server processes and tool calls"""
    
    def __init__(self):
        self.servers: Dict[str, MCPServer] = {}
        self.processes: Dict[str, subprocess.Popen] = {}
        
    def register_server(self, server: MCPServer):
        """Register an MCP server configuration"""
        self.servers[server.name] = server
        
    async def start_server(self, server_name: str) -> bool:
        """Start an MCP server process"""
        if server_name not in self.servers:
            return False
            
        if server_name in self.processes:
            return True  # Already running
            
        server = self.servers[server_name]
        env = os.environ.copy()
        if server.env:
            env.update(server.env)
            
        try:
            process = subprocess.Popen(
                [server.command] + server.args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                text=True
            )
            self.processes[server_name] = process
            return True
        except Exception as e:
            print(f"Failed to start MCP server {server_name}: {e}")
            return False
            
    async def call_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a tool on an MCP server"""
        if server_name not in self.processes:
            if not await self.start_server(server_name):
                raise RuntimeError(f"Failed to start server {server_name}")
                
        process = self.processes[server_name]
        
        # Send JSON-RPC request
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        try:
            process.stdin.write(json.dumps(request) + "\n")
            process.stdin.flush()
            
            # Read response
            response_line = process.stdout.readline()
            response = json.loads(response_line)
            
            if "error" in response:
                raise RuntimeError(f"Tool call error: {response['error']}")
                
            return response.get("result")
        except Exception as e:
            print(f"Error calling tool {tool_name} on {server_name}: {e}")
            raise
            
    async def list_tools(self, server_name: str) -> List[Dict[str, Any]]:
        """List available tools from an MCP server"""
        if server_name not in self.processes:
            if not await self.start_server(server_name):
                return []
                
        process = self.processes[server_name]
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        }
        
        try:
            process.stdin.write(json.dumps(request) + "\n")
            process.stdin.flush()
            
            response_line = process.stdout.readline()
            response = json.loads(response_line)
            
            return response.get("result", {}).get("tools", [])
        except Exception as e:
            print(f"Error listing tools from {server_name}: {e}")
            return []
            
    def shutdown(self):
        """Shutdown all MCP server processes"""
        for name, process in self.processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                process.kill()
        self.processes.clear()


def create_default_mcp_manager() -> MCPServerManager:
    """Create MCP manager with default Continue-compatible servers"""
    manager = MCPServerManager()
    
    # Register standard MCP servers
    manager.register_server(MCPServer(
        name="filesystem",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "."]
    ))
    
    manager.register_server(MCPServer(
        name="github",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN", "")}
    ))
    
    manager.register_server(MCPServer(
        name="git",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-git"]
    ))
    
    return manager
