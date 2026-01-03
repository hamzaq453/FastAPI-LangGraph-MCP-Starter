"""Main FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.routes import router
from app.config import settings
from app.core.logging import setup_logging
from app.core.rate_limit import limiter
from app.core.tracing import setup_langsmith
from app.db.session import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events.
    """
    # Startup
    setup_logging()
    setup_langsmith()
    
    # Create database tables if they don't exist
    await create_db_and_tables()
    
    yield
    
    # Shutdown (if needed)
    pass


# Create FastAPI app
app = FastAPI(
    title="FastAPI + LangGraph + MCP Starter",
    description="Production-ready AI agent with FastAPI, LangGraph, and MCP",
    version="0.1.0",
    lifespan=lifespan,
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


@app.middleware("http")
async def add_request_to_limiter(request: Request, call_next):
    """Add request to rate limiter context."""
    request.state.limiter = limiter
    response = await call_next(request)
    return response


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )
