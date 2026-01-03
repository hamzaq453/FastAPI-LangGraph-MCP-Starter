"""API routes for the FastAPI application."""

import logging
import uuid
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, Query
from langchain_core.messages import HumanMessage
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from app.agent.checkpointer import create_checkpointer
from app.agent.graph import create_agent_graph
from app.api.schemas import ChatRequest, ChatResponse, HealthResponse
from app.api.streaming import stream_agent_response
from app.core.auth import verify_api_key
from app.core.rate_limit import limiter
from app.db.session import get_session

logger = logging.getLogger(__name__)

router = APIRouter()

# Create agent graph with checkpointer for conversation memory
checkpointer = create_checkpointer()
agent_graph = create_agent_graph(checkpointer=checkpointer)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="0.1.0")


@router.post("/chat", response_model=ChatResponse)
@limiter.limit("100/minute")
async def chat(
    request: ChatRequest,
    session: AsyncSession = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    """
    Chat with the AI agent.
    
    Requires authentication if AUTH_ENABLED=true in config.
    Rate limited to prevent abuse.
    """
    try:
        # Generate or use provided session ID for conversation memory
        session_id = request.session_id or str(uuid.uuid4())
        
        # Prepare initial state
        initial_state = {
            "messages": [HumanMessage(content=request.message)],
            "session_id": session_id,
        }
        
        # Run the agent with checkpointing
        config = {"configurable": {"thread_id": session_id}}
        result = await agent_graph.ainvoke(initial_state, config=config)
        
        # Extract response
        messages = result.get("messages", [])
        if not messages:
            raise HTTPException(status_code=500, detail="No response from agent")
        
        final_message = messages[-1]
        response_text = final_message.content
        
        # Extract tool calls for debugging
        tool_calls = []
        for msg in messages:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    tool_calls.append({
                        "name": tool_call.get("name"),
                        "args": tool_call.get("args"),
                    })
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            tool_calls=tool_calls if tool_calls else None,
        )
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/stream")
@limiter.limit("100/minute")
async def chat_stream(
    message: str = Query(..., description="User message"),
    session_id: str = Query(None, description="Session ID for conversation memory"),
    api_key: str = Depends(verify_api_key),
) -> EventSourceResponse:
    """
    Stream chat responses via Server-Sent Events.
    
    Requires authentication if AUTH_ENABLED=true in config.
    Rate limited to prevent abuse.
    """
    async def event_generator() -> AsyncGenerator[str, None]:
        try:
            # Generate or use provided session ID
            sid = session_id or str(uuid.uuid4())
            
            # Prepare initial state
            initial_state = {
                "messages": [HumanMessage(content=message)],
                "session_id": sid,
            }
            
            # Stream agent execution
            config = {"configurable": {"thread_id": sid}}
            async for event in stream_agent_response(agent_graph, initial_state, config):
                yield event
        
        except Exception as e:
            logger.error(f"Error in streaming endpoint: {e}", exc_info=True)
            yield f"event: error\ndata: {str(e)}\n\n"
    
    return EventSourceResponse(event_generator())
