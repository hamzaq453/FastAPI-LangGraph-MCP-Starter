# FastAPI + LangGraph + MCP Starter Template

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![MCP](https://img.shields.io/badge/MCP-FastMCP_2.0-purple.svg)](https://github.com/jlowin/fastmcp)

Production-ready starter template for building AI agents with **FastAPI** (API layer), **LangGraph** (agent orchestration), and **MCP** (Model Context Protocol for tools).

## 🚀 Features

- **FastAPI Backend**: High-performance async API with automatic OpenAPI docs
- **LangGraph Agent**: Stateful ReAct-pattern agent with tool calling
- **MCP Tools**: Standardized tool protocol with TODO, calculator, and weather
- **OpenRouter Integration**: Easy LLM provider switching (GPT-4o default)
- **Streaming Responses**: Real-time SSE streaming of agent thoughts and actions
- **LangSmith Observability**: Optional tracing and debugging (Phase II)
- **Structured Logging**: JSON logs for production monitoring
- **Docker Ready**: One-command setup with Docker Compose
- **Fully Tested**: Comprehensive unit tests with pytest
- **Type Safe**: Full type hints with Pydantic validation

## 📋 What's Included

### API Endpoints
- `GET /health` - Health check
- `POST /chat` - Chat with AI agent
- `GET /chat/stream` - Stream agent responses via SSE (Phase II)

### MCP Tools
- **TODO Management**: Add, list, complete, delete tasks
- **Calculator**: Safe mathematical expression evaluation
- **Weather**: Get current weather for any city (Phase II)

### Agent Capabilities
The LangGraph agent can:
- Manage your TODO list via natural language
- Perform calculations
- Get weather information for cities worldwide
- Combine multiple tools to complete complex tasks

## 🏃 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (optional but recommended)

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/fastapi-langgraph-mcp-starter
cd fastapi-langgraph-mcp-starter
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Get your API key from [OpenRouter](https://openrouter.ai/).

### 3. Run with Docker (Recommended)

```bash
docker-compose up
```

The API will be available at `http://localhost:8000`.

### 4. Run Locally (Alternative)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Run the application
python -m app.main
```

## 🧪 Testing

### Health Check

```bash
curl http://localhost:8000/health
```

### Chat with Agent

**Add a TODO:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a todo: Buy groceries"}'
```

**List TODOs:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me all my todos"}'
```

**Calculate:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Calculate 25 * 4 + 10"}'
```

**Complex Task:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add 3 todos: buy milk, call mom, finish report. Then calculate 100 / 5"}'
```

## 🧪 Run Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Project Structure

```
fastapi-langgraph-mcp-starter/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── api/
│   │   ├── routes.py        # API endpoints
│   │   └── schemas.py       # Request/Response models
│   ├── core/
│   │   └── llm_factory.py   # LLM provider abstraction
│   ├── agent/
│   │   ├── state.py         # Agent state schema
│   │   ├── nodes.py         # Graph node functions
│   │   └── graph.py         # LangGraph workflow
│   └── mcp/
│       ├── server.py        # MCP server
│       └── tools/
│           ├── todo.py      # TODO tool
│           └── calculator.py # Calculator tool
├── tests/                   # Unit tests
├── .env.example             # Environment template
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
└── pyproject.toml           # Dependencies
```

## 🔧 Configuration

All configuration is managed via environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key | Required |
| `MODEL_NAME` | LLM model identifier | `openai/gpt-4o` |
| `MODEL_TEMPERATURE` | Sampling temperature | `0.7` |
| `MODEL_MAX_TOKENS` | Max response tokens | `2000` |
| `API_PORT` | API server port | `8000` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000,http://localhost:8000` |
| `WEATHER_API_KEY` | OpenWeatherMap API key (optional) | `` |
| `LANGSMITH_API_KEY` | LangSmith API key (optional) | `` |
| `LANGSMITH_ENABLED` | Enable LangSmith tracing | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `JSON_LOGS` | Use JSON log format | `false` |

## 🎯 Customization

### Add a New Tool

1. Create tool function in `app/mcp/tools/`:

```python
# app/mcp/tools/weather.py
def get_weather(city: str) -> dict:
    """Get weather for a city."""
    # Your implementation
    return {"city": city, "temp": 72}
```

2. Register in MCP server (`app/mcp/server.py`):

```python
from app.mcp.tools import weather

@mcp.tool()
def get_weather(city: str) -> dict:
    """Get current weather for a city."""
    return weather.get_weather(city)
```

3. Add to agent tools (`app/agent/nodes.py`):

```python
@tool
def get_weather_tool(city: str) -> dict:
    """Get current weather for a city."""
    return weather.get_weather(city)

# Add to tools list
tools = [..., get_weather_tool]
```

### Change LLM Provider

Edit `.env`:

```env
MODEL_NAME=anthropic/claude-3.5-sonnet
```

OpenRouter supports 100+ models. See [OpenRouter Models](https://openrouter.ai/models).

## 🗺️ Roadmap

### Phase I ✅
- Core FastAPI + LangGraph + MCP integration
- TODO and calculator tools
- Docker setup
- Unit tests

### Phase II (Current) ✅
- Streaming responses (SSE)
- Weather tool integration
- LangSmith observability
- Structured logging

### Phase III (Planned)
- PostgreSQL persistence
- Conversation memory
- OAuth 2.0 authentication
- Multi-MCP server support
- Rate limiting

### Phase IV (Future)
- Multi-agent workflows
- RAG integration
- Web UI
- Advanced monitoring

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [LangGraph](https://langchain-ai.github.io/langgraph/) - Agent orchestration
- [FastMCP](https://github.com/jlowin/fastmcp) - Model Context Protocol
- [OpenRouter](https://openrouter.ai/) - Unified LLM API

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/fastapi-langgraph-mcp-starter/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/fastapi-langgraph-mcp-starter/discussions)

---

**Star ⭐ this repo if you find it useful!**
"# LangGrapgh-MCP-" 
