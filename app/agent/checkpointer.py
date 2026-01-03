"""LangGraph checkpointer using PostgreSQL.

Provides conversation memory across requests using database persistence.
"""

from langgraph.checkpoint.postgres import PostgresSaver

from app.config import settings


def create_checkpointer() -> PostgresSaver:
    """
    Create PostgreSQL checkpointer for LangGraph.
    
    Returns:
        PostgresSaver instance configured with database URL
    """
    # PostgresSaver will create necessary tables automatically
    return PostgresSaver.from_conn_string(settings.database_url)
