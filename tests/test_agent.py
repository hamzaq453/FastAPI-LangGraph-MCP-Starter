"""Tests for LangGraph agent."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.agent.graph import create_agent_graph
from app.agent.nodes import should_continue


class TestAgentGraph:
    """Tests for agent graph creation and execution."""
    
    def test_create_agent_graph(self):
        """Test that agent graph is created successfully."""
        graph = create_agent_graph()
        
        assert graph is not None
        # Graph should be compiled and ready to use
    
    @pytest.mark.asyncio
    async def test_agent_graph_execution(self):
        """Test agent graph execution with mocked LLM."""
        # Mock the LLM response
        mock_llm_response = MagicMock()
        mock_llm_response.content = "I can help you with that!"
        mock_llm_response.tool_calls = []
        
        with patch('app.agent.nodes.get_llm') as mock_get_llm:
            mock_llm = MagicMock()
            mock_llm.bind_tools.return_value.ainvoke = AsyncMock(
                return_value=mock_llm_response
            )
            mock_get_llm.return_value = mock_llm
            
            graph = create_agent_graph()
            result = await graph.ainvoke({
                "messages": [("user", "Hello")]
            })
            
            assert "messages" in result
            assert len(result["messages"]) > 0


class TestAgentNodes:
    """Tests for individual agent nodes."""
    
    def test_should_continue_with_tool_calls(self):
        """Test routing when LLM wants to call tools."""
        mock_message = MagicMock()
        mock_message.tool_calls = [{"name": "add_todo", "args": {"task": "Test"}}]
        
        state = {"messages": [mock_message]}
        
        assert should_continue(state) == "continue"
    
    def test_should_continue_without_tool_calls(self):
        """Test routing when LLM is done."""
        mock_message = MagicMock()
        mock_message.tool_calls = []
        
        state = {"messages": [mock_message]}
        
        assert should_continue(state) == "end"
