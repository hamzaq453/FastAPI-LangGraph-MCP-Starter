"""MCP Client Manager for connecting to multiple MCP servers.

Manages connections to multiple MCP servers and aggregates their tools.
"""

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger(__name__)


class MCPServerConfig:
    """Configuration for a single MCP server."""
    
    def __init__(self, name: str, config: dict[str, Any]):
        self.name = name
        self.type = config.get("type", "stdio")
        self.enabled = config.get("enabled", True)
        self.description = config.get("description", "")
        self.command = config.get("command")
        self.args = config.get("args", [])
        self.env = config.get("env", {})
    
    def __repr__(self) -> str:
        return f"MCPServerConfig(name={self.name}, type={self.type}, enabled={self.enabled})"


class MCPClientManager:
    """Manages connections to multiple MCP servers."""
    
    def __init__(self, config_path: str = "mcp_servers.json"):
        """
        Initialize MCP client manager.
        
        Args:
            config_path: Path to MCP servers configuration file
        """
        self.config_path = config_path
        self.servers: dict[str, MCPServerConfig] = {}
        self.sessions: dict[str, ClientSession] = {}
        self.tools: dict[str, list[Any]] = {}  # server_name -> tools
        
        self._load_config()
    
    def _load_config(self) -> None:
        """Load server configurations from JSON file."""
        config_file = Path(self.config_path)
        
        if not config_file.exists():
            logger.warning(f"MCP config file not found: {self.config_path}, using built-in only")
            self.servers = {
                "local": MCPServerConfig("local", {"type": "builtin", "enabled": True})
            }
            return
        
        try:
            with open(config_file) as f:
                config_data = json.load(f)
            
            for name, server_config in config_data.get("servers", {}).items():
                self.servers[name] = MCPServerConfig(name, server_config)
                logger.info(f"Loaded MCP server config: {name} ({server_config.get('description', 'No description')})")
        
        except Exception as e:
            logger.error(f"Failed to load MCP config: {e}")
            # Fallback to built-in only
            self.servers = {
                "local": MCPServerConfig("local", {"type": "builtin", "enabled": True})
            }
    
    async def __aenter__(self):
        """Connect to all enabled MCP servers."""
        await self.connect_all()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Disconnect from all MCP servers."""
        await self.disconnect_all()
    
    async def connect_all(self) -> None:
        """Connect to all enabled servers concurrently."""
        tasks = []
        
        for name, config in self.servers.items():
            if not config.enabled:
                logger.info(f"Skipping disabled server: {name}")
                continue
            
            if config.type == "builtin":
                # Built-in server doesn't need connection
                logger.info(f"✓ Built-in server '{name}' ready")
                self.tools[name] = []  # Will be populated by agent nodes
                continue
            
            # Connect to external servers
            tasks.append(self._connect_server(name, config))
        
        # Connect concurrently with timeout
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Log results
            for name, result in zip([n for n, c in self.servers.items() if c.enabled and c.type != "builtin"], results):
                if isinstance(result, Exception):
                    logger.error(f"Failed to connect to {name}: {result}")
                else:
                    logger.info(f"✓ Connected to MCP server '{name}'")
    
    async def _connect_server(self, name: str, config: MCPServerConfig) -> None:
        """
        Connect to a single MCP server.
        
        Args:
            name: Server name
            config: Server configuration
        """
        try:
            # Prepare environment variables
            env = os.environ.copy()
            for key, value in config.env.items():
                # Support ${VAR} substitution
                if value.startswith("${") and value.endswith("}"):
                    env_var = value[2:-1]
                    env[key] = os.environ.get(env_var, "")
                else:
                    env[key] = value
            
            # Create server parameters
            server_params = StdioServerParameters(
                command=config.command,
                args=config.args,
                env=env
            )
            
            # Connect with timeout
            async with asyncio.timeout(30):
                # Create stdio client
                stdio_transport = await stdio_client(server_params)
                
                # Create session
                read, write = stdio_transport
                session = ClientSession(read, write)
                
                # Initialize session
                await session.initialize()
                
                # List available tools
                tools_result = await session.list_tools()
                
                # Store session and tools
                self.sessions[name] = session
                self.tools[name] = tools_result.tools if hasattr(tools_result, 'tools') else []
                
                logger.info(f"Server '{name}' has {len(self.tools[name])} tools")
        
        except asyncio.TimeoutError:
            logger.warning(f"Timeout connecting to server '{name}'")
            raise
        except Exception as e:
            logger.error(f"Error connecting to server '{name}': {e}")
            raise
    
    async def disconnect_all(self) -> None:
        """Disconnect from all connected servers."""
        for name, session in self.sessions.items():
            try:
                # MCP sessions don't have explicit close, just let them cleanup
                logger.info(f"Disconnected from server '{name}'")
            except Exception as e:
                logger.error(f"Error disconnecting from '{name}': {e}")
        
        self.sessions.clear()
        self.tools.clear()
    
    def get_all_tools(self) -> dict[str, list[Any]]:
        """
        Get all tools from all connected servers.
        
        Returns:
            Dictionary mapping server names to their tools
        """
        return self.tools.copy()
    
    def get_enabled_servers(self) -> list[str]:
        """
        Get list of enabled server names.
        
        Returns:
            List of server names that are enabled
        """
        return [name for name, config in self.servers.items() if config.enabled]
    
    async def call_tool(
        self,
        server_name: str,
        tool_name: str,
        arguments: dict[str, Any]
    ) -> Any:
        """
        Call a tool on a specific server.
        
        Args:
            server_name: Name of the server
            tool_name: Name of the tool
            arguments: Tool arguments
            
        Returns:
            Tool execution result
            
        Raises:
            ValueError: If server not found or not connected
        """
        if server_name not in self.sessions:
            raise ValueError(f"Server '{server_name}' not connected")
        
        session = self.sessions[server_name]
        
        try:
            result = await session.call_tool(tool_name, arguments)
            return result
        except Exception as e:
            logger.error(f"Error calling tool '{tool_name}' on '{server_name}': {e}")
            raise
