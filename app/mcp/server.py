"""FastMCP server exposing TODO and calculator tools.

This server runs in stdio mode and provides tools that can be called
by the LangGraph agent.
"""

import os
from fastmcp import FastMCP

from app.mcp.tools import calculator, todo, weather

# Create MCP server instance
mcp = FastMCP("Agent Tools")


# Register TODO tools
@mcp.tool()
def add_todo(task: str) -> dict:
    """Add a new TODO item to the list."""
    return todo.add_todo(task)


@mcp.tool()
def list_todos() -> list:
    """Get all TODO items."""
    return todo.list_todos()


@mcp.tool()
def complete_todo(todo_id: int) -> dict:
    """Mark a TODO item as completed."""
    return todo.complete_todo(todo_id)


@mcp.tool()
def delete_todo(todo_id: int) -> dict:
    """Delete a TODO item."""
    return todo.delete_todo(todo_id)


# Register calculator tool
@mcp.tool()
def calculate(expression: str) -> dict:
    """
    Safely evaluate a mathematical expression.
    
    Supports: +, -, *, /, ^ (power)
    Example: "2 + 2" or "10 * 5 - 3"
    """
    return calculator.calculate(expression)


# Register weather tool
@mcp.tool()
async def get_weather(city: str) -> dict:
    """
    Get current weather for a city.
    
    Example: "London", "New York", "Tokyo"
    """
    api_key = os.getenv("WEATHER_API_KEY", "")
    if not api_key:
        return {"error": "Weather API key not configured"}
    
    return await weather.get_weather(city, api_key)


# Entry point for running the MCP server
if __name__ == "__main__":
    mcp.run()
