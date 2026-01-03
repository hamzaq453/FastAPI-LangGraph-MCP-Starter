"""Tests for API endpoints."""

import pytest
from unittest.mock import AsyncMock, patch


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


@pytest.mark.asyncio
async def test_chat_endpoint_success(client):
    """Test successful chat interaction."""
    # Mock the agent graph to avoid actual LLM calls
    mock_result = {
        "messages": [
            type('MockMessage', (), {
                'content': 'Hello! How can I help you today?',
                'tool_calls': []
            })()
        ]
    }
    
    with patch('app.api.routes.create_agent_graph') as mock_graph:
        mock_graph.return_value.ainvoke = AsyncMock(return_value=mock_result)
        
        response = client.post(
            "/chat",
            json={"message": "Hello"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["response"] == "Hello! How can I help you today?"


def test_chat_endpoint_validation(client):
    """Test chat endpoint input validation."""
    # Empty message should fail
    response = client.post(
        "/chat",
        json={"message": ""}
    )
    
    assert response.status_code == 422  # Validation error


def test_chat_endpoint_missing_message(client):
    """Test chat endpoint with missing message field."""
    response = client.post(
        "/chat",
        json={}
    )
    
    assert response.status_code == 422  # Validation error
