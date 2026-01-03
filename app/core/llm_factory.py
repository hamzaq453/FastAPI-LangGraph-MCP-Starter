"""LLM Factory for creating language model instances.

This module provides a centralized way to create and configure LLM instances,
supporting OpenRouter API with easy switching between models.
"""

from langchain_openai import ChatOpenAI

from app.config import settings


class LLMFactory:
    """Factory for creating LLM instances with consistent configuration."""
    
    @staticmethod
    def create_chat_model(
        model_name: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> ChatOpenAI:
        """
        Create a ChatOpenAI instance configured for OpenRouter.
        
        Args:
            model_name: Model identifier (e.g., "openai/gpt-4o"). Uses config default if None.
            temperature: Sampling temperature (0-2). Uses config default if None.
            max_tokens: Maximum tokens in response. Uses config default if None.
            
        Returns:
            Configured ChatOpenAI instance.
        """
        return ChatOpenAI(
            model=model_name or settings.model_name,
            temperature=temperature or settings.model_temperature,
            max_tokens=max_tokens or settings.model_max_tokens,
            openai_api_key=settings.openrouter_api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "https://github.com/yourusername/fastapi-langgraph-mcp-starter",
                "X-Title": "FastAPI LangGraph MCP Starter",
            },
        )


# Convenience function for quick access
def get_llm() -> ChatOpenAI:
    """Get default LLM instance with settings from config."""
    return LLMFactory.create_chat_model()
