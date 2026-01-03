"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenRouter API Configuration
    openrouter_api_key: str
    
    # LLM Configuration
    model_name: str = "openai/gpt-4o"
    model_temperature: float = 0.7
    model_max_tokens: int = 2000
    
    # MCP Configuration
    mcp_transport: str = "stdio"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # CORS Configuration
    cors_origins: str = "http://localhost:3000,http://localhost:8000"
    
    # Database Configuration
    database_url: str = "postgresql+asyncpg://agent:agent_password@localhost:5432/agent_db"
    database_echo: bool = False
    
    # Authentication Configuration
    api_keys: str = ""
    auth_enabled: bool = False
    
    # Rate Limiting Configuration
    rate_limit_per_minute: int = 100
    
    # Weather API Configuration
    weather_api_key: str = ""
    
    # LangSmith Configuration (Optional)
    langsmith_api_key: str = ""
    langsmith_project: str = "fastapi-langgraph-mcp-starter"
    langsmith_enabled: bool = False
    
    # Logging Configuration
    log_level: str = "INFO"
    json_logs: bool = False
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        protected_namespaces=('settings_',),  # Fix Pydantic warning
    )
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def api_keys_list(self) -> list[str]:
        """Parse API keys from comma-separated string."""
        if not self.api_keys:
            return []
        return [key.strip() for key in self.api_keys.split(",")]


# Global settings instance
settings = Settings()
