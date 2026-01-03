"""LangGraph workflow definition.

Creates the agent graph with nodes and edges for the ReAct pattern.
"""

from typing import Optional

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, StateGraph

from app.agent.nodes import call_model, create_tool_node, should_continue
from app.agent.state import AgentState


def create_agent_graph(checkpointer: Optional[BaseCheckpointSaver] = None):
    """
    Create the LangGraph agent workflow.
    
    The graph follows a ReAct (Reasoning + Acting) pattern:
    1. LLM decides what to do (call_model)
    2. If tools needed, execute them (tools)
    3. Return to LLM with tool results
    4. Repeat until task is complete
    
    Args:
        checkpointer: Optional checkpointer for conversation memory
    
    Returns:
        Compiled StateGraph ready for execution.
    """
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", create_tool_node())
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END,
        },
    )
    
    # Add edge from tools back to agent
    workflow.add_edge("tools", "agent")
    
    # Compile the graph with optional checkpointer
    return workflow.compile(checkpointer=checkpointer)
