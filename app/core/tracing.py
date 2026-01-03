"""LangSmith tracing integration.

Provides observability for LangGraph agent workflows.
"""

import os
from typing import Optional


def setup_langsmith(
    api_key: Optional[str] = None,
    project: Optional[str] = None,
    enabled: bool = True,
) -> None:
    """
    Configure LangSmith tracing.
    
    Args:
        api_key: LangSmith API key (optional, can use env var)
        project: LangSmith project name (optional, defaults to "default")
        enabled: Whether to enable tracing
    """
    if not enabled:
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
        return
    
    # Enable tracing
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    
    # Set API key if provided
    if api_key:
        os.environ["LANGCHAIN_API_KEY"] = api_key
    
    # Set project if provided
    if project:
        os.environ["LANGCHAIN_PROJECT"] = project
    else:
        os.environ["LANGCHAIN_PROJECT"] = "fastapi-langgraph-mcp-starter"


def is_langsmith_enabled() -> bool:
    """
    Check if LangSmith tracing is enabled.
    
    Returns:
        True if tracing is enabled, False otherwise
    """
    return os.environ.get("LANGCHAIN_TRACING_V2", "false").lower() == "true"
