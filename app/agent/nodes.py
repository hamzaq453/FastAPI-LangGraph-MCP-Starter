"""Agent node functions for LangGraph workflow.

Each node represents a step in the agent's reasoning process.
"""

import logging

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.prebuilt import ToolNode

from app.agent.state import AgentState
from app.config import settings
from app.core.llm_factory import get_llm
from app.mcp.tools import calculator, weather
from app.mcp.tools import todo_simple as todo  # Use simple in-memory TODO for agent

logger = logging.getLogger(__name__)


def create_tool_node() -> ToolNode:
    """
    Create a ToolNode with all available MCP tools.
    
    Returns:
        Configured ToolNode instance.
    """
    # Import LangChain tool wrapper
    from langchain_core.tools import tool
    
    # Wrap MCP tools as LangChain tools
    @tool
    def add_todo_tool(task: str) -> dict:
        """Add a new TODO item to the list."""
        return todo.add_todo(task)
    
    @tool
    def list_todos_tool() -> list:
        """Get all TODO items."""
        return todo.list_todos()
    
    @tool
    def complete_todo_tool(todo_id: int) -> dict:
        """Mark a TODO item as completed."""
        return todo.complete_todo(todo_id)
    
    @tool
    def delete_todo_tool(todo_id: int) -> dict:
        """Delete a TODO item."""
        return todo.delete_todo(todo_id)
    
    @tool
    def calculate_tool(expression: str) -> dict:
        """
        Safely evaluate a mathematical expression.
        Supports: +, -, *, /, ^ (power)
        Example: "2 + 2" or "10 * 5 - 3"
        """
        return calculator.calculate(expression)
    
    @tool
    async def get_weather_tool(city: str) -> dict:
        """
        Get current weather for a city.
        Example: "London", "New York", "Tokyo"
        """
        if not settings.weather_api_key:
            return {"error": "Weather API key not configured"}
        return await weather.get_weather(city, settings.weather_api_key)
    
    # Create list of tools
    tools = [
        add_todo_tool,
        list_todos_tool,
        complete_todo_tool,
        delete_todo_tool,
        calculate_tool,
        get_weather_tool,
    ]
    
    return ToolNode(tools)


async def call_model(state: AgentState) -> dict:
    """
    Call the LLM to decide the next action.
    
    Args:
        state: Current agent state with conversation history.
        
    Returns:
        Updated state with LLM response.
    """
    # Get LLM with tools bound
    from langchain_core.tools import tool
    
    # Wrap tools for binding
    @tool
    def add_todo_tool(task: str) -> dict:
        """Add a new TODO item to the list."""
        return todo.add_todo(task)
    
    @tool
    def list_todos_tool() -> list:
        """Get all TODO items."""
        return todo.list_todos()
    
    @tool
    def complete_todo_tool(todo_id: int) -> dict:
        """Mark a TODO item as completed."""
        return todo.complete_todo(todo_id)
    
    @tool
    def delete_todo_tool(todo_id: int) -> dict:
        """Delete a TODO item."""
        return todo.delete_todo(todo_id)
    
    @tool
    def calculate_tool(expression: str) -> dict:
        """
        Safely evaluate a mathematical expression.
        Supports: +, -, *, /, ^ (power)
        Example: "2 + 2" or "10 * 5 - 3"
        """
        return calculator.calculate(expression)
    
    @tool
    async def get_weather_tool(city: str) -> dict:
        """
        Get current weather for a city.
        Example: "London", "New York", "Tokyo"
        """
        if not settings.weather_api_key:
            return {"error": "Weather API key not configured"}
        return await weather.get_weather(city, settings.weather_api_key)
    
    tools = [
        add_todo_tool,
        list_todos_tool,
        complete_todo_tool,
        delete_todo_tool,
        calculate_tool,
        get_weather_tool,
    ]
    
    try:
        llm = get_llm()
        llm_with_tools = llm.bind_tools(tools)
        
        # Log the input messages
        logger.info(f"Calling LLM with {len(state['messages'])} messages")
        logger.debug(f"Messages: {state['messages']}")
        
        # Call LLM
        response = await llm_with_tools.ainvoke(state["messages"])
        
        # Log the response
        logger.info(f"LLM response type: {type(response)}")
        logger.info(f"LLM response content: {response.content if hasattr(response, 'content') else 'No content'}")
        logger.info(f"LLM response tool_calls: {response.tool_calls if hasattr(response, 'tool_calls') else 'No tool_calls'}")
        
        # Check if response is empty
        if not response.content and (not hasattr(response, 'tool_calls') or not response.tool_calls):
            logger.error("LLM returned empty response!")
            # Return a default response to avoid the error
            from langchain_core.messages import AIMessage
            return {"messages": [AIMessage(content="I apologize, but I encountered an issue processing your request. Please try again.")]}
        
        return {"messages": [response]}
    
    except Exception as e:
        logger.error(f"Error in call_model: {e}", exc_info=True)
        from langchain_core.messages import AIMessage
        return {"messages": [AIMessage(content=f"Error: {str(e)}")]}


def should_continue(state: AgentState) -> str:
    """
    Determine if the agent should continue or finish.
    
    Args:
        state: Current agent state.
        
    Returns:
        "continue" if tools should be called, "end" otherwise.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    # If the last message has tool calls, continue to tools
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "continue"
    
    # Otherwise, end the workflow
    return "end"
