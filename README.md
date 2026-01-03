# FastAPI + LangGraph + MCP Starter Template

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![MCP](https://img.shields.io/badge/MCP-FastMCP_2.0-purple.svg)](https://github.com/jlowin/fastmcp)

Production-ready starter template for building AI agents with **FastAPI** (API layer), **LangGraph** (agent orchestration), and **MCP** (Model Context Protocol for tools).

## 🚀 Features

### Core Features
- **FastAPI Backend**: High-performance async API with automatic OpenAPI docs
- **LangGraph Agent**: Stateful ReAct-pattern agent with tool calling
- **MCP Tools**: Standardized tool protocol with TODO, calculator, and weather
- **OpenRouter Integration**: Easy LLM provider switching (GPT-4o default)
- **Streaming Responses**: Real-time SSE streaming of agent thoughts and actions

### Phase III: Production Features ✨
- **PostgreSQL Database**: Persistent storage with SQLModel ORM
- **Conversation Memory**: LangGraph checkpointing for multi-turn conversations
- **API Key Authentication**: Secure your endpoints (optional)
- **Rate Limiting**: Prevent API abuse (100 req/min default)
- **Multi-MCP Server Support**: Connect to multiple MCP servers dynamically
- **LangSmith Tracing**: Full observability for agent workflows
- **Structured Logging**: JSON logs for production monitoring

### Additional Features
- **Docker Ready**: One-command setup with Docker Compose
- **Database Migrations**: Alembic for schema versioning
- **Fully Tested**: Comprehensive unit tests with pytest
- **Type Safe**: Full type hints with Pydantic validation

## 📋 What's Included

### API Endpoints
- `GET /health` - Health check
- `POST /chat` - Chat with AI agent (supports session memory)
- `GET /chat/stream` - Stream agent responses via SSE

### MCP Tools
- **TODO Management**: Add, list, complete, delete tasks
- **Calculator**: Safe mathematical expression evaluation
- **Weather**: Get current weather for any city

### Agent Capabilities
The LangGraph agent can:
- Remember conversations across requests (session-based memory)
- Manage your TODO list via natural language
- Perform calculations
- Get weather information for cities worldwide
- Combine multiple tools to complete complex tasks

## 🏃 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (recommended)
- PostgreSQL (included in Docker Compose)

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/fastapi-langgraph-mcp-starter
cd fastapi-langgraph-mcp-starter
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` and add your API keys:

```env
# Required
OPENROUTER_API_KEY=your_openrouter_key_here

# Database (default works with Docker Compose)
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/mcp-agent

# Optional: Weather API
WEATHER_API_KEY=your_openweather_key_here

# Optional: LangSmith Tracing
LANGSMITH_API_KEY=your_langsmith_key_here
LANGSMITH_PROJECT=my-project
LANGSMITH_ENABLED=true

# Optional: Authentication
AUTH_ENABLED=false
API_KEYS=key1,key2,key3
```

**Get API Keys:**
- OpenRouter: https://openrouter.ai/
- OpenWeather: https://openweathermap.org/api
- LangSmith: https://smith.langchain.com/

### 3. Run with Docker (Recommended)

```bash
# Start PostgreSQL and API
docker-compose up

# In another terminal, run migrations
docker-compose exec api alembic upgrade head
```

The API will be available at `http://localhost:8000`.

### 4. Run Locally (Alternative)

```bash
# Start PostgreSQL (if not using Docker)
# Make sure PostgreSQL is running on localhost:5432

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Run migrations
alembic upgrade head

# Run the application
python -m app.main
```

## 🧪 Usage Examples

### Health Check

```bash
curl http://localhost:8000/health
```

### Chat with Agent (Basic)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a TODO: Buy groceries"
  }'
```

### Chat with Conversation Memory

```bash
# First message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hi, my name is Alice",
    "session_id": "user-123"
  }'

# Follow-up message - agent remembers!
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is my name?",
    "session_id": "user-123"
  }'
```

### Stream Agent Response

```bash
curl -N "http://localhost:8000/chat/stream?message=Calculate%2025%20*%204&session_id=calc-session"
```

### With Authentication (if enabled)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "message": "List my TODOs"
  }'
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key | Yes | - |
| `DATABASE_URL` | PostgreSQL connection string | Yes | `postgresql+asyncpg://...` |
| `MODEL_NAME` | LLM model to use | No | `openai/gpt-4o` |
| `MODEL_TEMPERATURE` | LLM temperature | No | `0.7` |
| `MODEL_MAX_TOKENS` | Max tokens in response | No | `2000` |
| `API_HOST` | API server host | No | `0.0.0.0` |
| `API_PORT` | API server port | No | `8000` |
| `AUTH_ENABLED` | Enable API key auth | No | `false` |
| `API_KEYS` | Comma-separated API keys | No | `` |
| `RATE_LIMIT_PER_MINUTE` | Rate limit per key/IP | No | `100` |
| `WEATHER_API_KEY` | OpenWeather API key | No | `` |
| `LANGSMITH_API_KEY` | LangSmith API key | No | `` |
| `LANGSMITH_PROJECT` | LangSmith project name | No | `fastapi-langgraph-mcp-starter` |
| `LANGSMITH_ENABLED` | Enable LangSmith tracing | No | `false` |
| `LOG_LEVEL` | Logging level | No | `INFO` |
| `JSON_LOGS` | Use JSON log format | No | `false` |

### Database Setup

The application uses PostgreSQL for:
- **Conversation Memory**: LangGraph checkpointing stores conversation state
- **Future**: Persistent TODO storage (currently in-memory for agent)

**Migrations:**
```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

### Authentication

Enable API key authentication:

```env
AUTH_ENABLED=true
API_KEYS=secret-key-1,secret-key-2,another-key
```

Then include the key in requests:
```bash
curl -H "X-API-Key: secret-key-1" ...
```

### Rate Limiting

Configured per API key (or IP if no key provided):

```env
RATE_LIMIT_PER_MINUTE=100
```

Returns `429 Too Many Requests` when limit exceeded.

### Multi-MCP Server Support

Connect to multiple MCP servers to extend your agent's capabilities:

**Configuration File:** `mcp_servers.json`

```json
{
  "servers": {
    "local": {
      "type": "builtin",
      "enabled": true,
      "description": "Built-in tools"
    },
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./workspace"],
      "enabled": true,
      "description": "File operations"
    }
  }
}
```

**Features:**
- Dynamic tool loading from multiple servers
- Enable/disable servers via configuration
- Graceful error handling (continues with available servers)
- Tool namespacing to avoid conflicts

**Available MCP Servers:**
- `@modelcontextprotocol/server-filesystem` - File operations
- `@modelcontextprotocol/server-github` - GitHub API
- `@modelcontextprotocol/server-postgres` - Database queries
- Custom servers - Build your own!

**Environment Variables:**
```env
MCP_SERVERS_CONFIG=mcp_servers.json
MCP_TIMEOUT=30
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py
```

### Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI with interactive API testing.

## 📁 Project Structure

```
fastapi-langgraph-mcp-starter/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── api/
│   │   ├── routes.py           # API endpoints
│   │   ├── schemas.py          # Pydantic models
│   │   └── streaming.py        # SSE streaming utilities
│   ├── agent/
│   │   ├── state.py            # Agent state definition
│   │   ├── nodes.py            # Agent node functions
│   │   ├── graph.py            # LangGraph workflow
│   │   └── checkpointer.py     # Conversation memory
│   ├── core/
│   │   ├── llm_factory.py      # LLM initialization
│   │   ├── logging.py          # Structured logging
│   │   ├── tracing.py          # LangSmith integration
│   │   ├── auth.py             # API key authentication
│   │   └── rate_limit.py       # Rate limiting
│   ├── db/
│   │   ├── models.py           # Database models
│   │   └── session.py          # Database session management
│   └── mcp/
│       ├── server.py           # MCP server definition
│       └── tools/
│           ├── todo.py         # TODO tool (database-backed)
│           ├── todo_simple.py  # TODO tool (in-memory for agent)
│           ├── calculator.py   # Calculator tool
│           └── weather.py      # Weather tool
├── tests/
│   ├── conftest.py             # Test fixtures
│   ├── test_api.py             # API endpoint tests
│   ├── test_agent.py           # Agent workflow tests
│   └── test_mcp.py             # MCP tool tests
├── alembic/                    # Database migrations
├── .env.example                # Environment template
├── docker-compose.yml          # Docker services
├── Dockerfile                  # Container definition
├── pyproject.toml              # Project dependencies
└── README.md                   # This file
```

## 🔍 How It Works

### Request Flow

1. **Client** sends request to FastAPI endpoint
2. **Authentication** validates API key (if enabled)
3. **Rate Limiter** checks request quota
4. **Agent** processes request using LangGraph workflow:
   - LLM decides what to do
   - Calls MCP tools if needed
   - Returns final response
5. **Checkpointer** saves conversation state to PostgreSQL
6. **Response** sent back to client

### Agent Workflow (ReAct Pattern)

```
User Input → LLM Decision → Tool Call? → Execute Tool → LLM Decision → ... → Final Answer
                ↑                                          ↓
                └──────────── Tool Results ────────────────┘
```

### Conversation Memory

Each session has a unique `session_id`. The checkpointer:
- Stores all messages and tool calls in PostgreSQL
- Retrieves conversation history on subsequent requests
- Enables multi-turn conversations with context

## 🚀 Deployment

### Docker Production Build

```bash
# Build production image
docker build -t fastapi-langgraph-mcp:latest .

# Run with external PostgreSQL
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db \
  -e OPENROUTER_API_KEY=your_key \
  fastapi-langgraph-mcp:latest
```

### Environment Best Practices

- Use environment-specific `.env` files
- Never commit `.env` to version control
- Use secrets management in production (AWS Secrets Manager, etc.)
- Enable `JSON_LOGS=true` for production logging
- Set `API_RELOAD=false` in production

## 📚 Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [OpenRouter API](https://openrouter.ai/docs)
- [LangSmith Tracing](https://docs.smith.langchain.com/)

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) by Sebastián Ramírez
- [LangGraph](https://github.com/langchain-ai/langgraph) by LangChain
- [FastMCP](https://github.com/jlowin/fastmcp) by Marvin Team
- [OpenRouter](https://openrouter.ai/) for LLM access

---

**Ready to build your AI agent?** Start with this template and customize it for your needs! 🚀
