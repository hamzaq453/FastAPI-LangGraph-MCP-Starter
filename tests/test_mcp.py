"""Tests for MCP tools."""

import pytest

from app.mcp.tools import calculator, todo


class TestTodoTool:
    """Tests for TODO tool."""
    
    def setup_method(self):
        """Clear todos before each test."""
        todo.clear_todos()
    
    def test_add_todo(self):
        """Test adding a TODO item."""
        result = todo.add_todo("Buy groceries")
        
        assert result["id"] == 1
        assert result["task"] == "Buy groceries"
        assert result["completed"] is False
    
    def test_list_todos(self):
        """Test listing TODO items."""
        todo.add_todo("Task 1")
        todo.add_todo("Task 2")
        
        todos = todo.list_todos()
        
        assert len(todos) == 2
        assert todos[0]["task"] == "Task 1"
        assert todos[1]["task"] == "Task 2"
    
    def test_complete_todo(self):
        """Test completing a TODO item."""
        result = todo.add_todo("Task to complete")
        todo_id = result["id"]
        
        completed = todo.complete_todo(todo_id)
        
        assert completed["completed"] is True
        assert completed["id"] == todo_id
    
    def test_complete_nonexistent_todo(self):
        """Test completing a non-existent TODO."""
        with pytest.raises(ValueError, match="not found"):
            todo.complete_todo(999)
    
    def test_delete_todo(self):
        """Test deleting a TODO item."""
        result = todo.add_todo("Task to delete")
        todo_id = result["id"]
        
        delete_result = todo.delete_todo(todo_id)
        
        assert "deleted successfully" in delete_result["message"]
        assert len(todo.list_todos()) == 0
    
    def test_delete_nonexistent_todo(self):
        """Test deleting a non-existent TODO."""
        with pytest.raises(ValueError, match="not found"):
            todo.delete_todo(999)


class TestCalculatorTool:
    """Tests for calculator tool."""
    
    def test_simple_addition(self):
        """Test simple addition."""
        result = calculator.calculate("2 + 2")
        
        assert result["expression"] == "2 + 2"
        assert result["result"] == 4.0
    
    def test_complex_expression(self):
        """Test complex mathematical expression."""
        result = calculator.calculate("10 * 5 - 3")
        
        assert result["result"] == 47.0
    
    def test_division(self):
        """Test division."""
        result = calculator.calculate("10 / 2")
        
        assert result["result"] == 5.0
    
    def test_power(self):
        """Test power operation."""
        result = calculator.calculate("2 ** 3")
        
        assert result["result"] == 8.0
    
    def test_division_by_zero(self):
        """Test division by zero error."""
        with pytest.raises(ValueError, match="Division by zero"):
            calculator.calculate("5 / 0")
    
    def test_invalid_expression(self):
        """Test invalid expression."""
        with pytest.raises(ValueError):
            calculator.calculate("2 +")


class TestWeatherTool:
    """Tests for weather tool."""
    
    @pytest.mark.asyncio
    async def test_get_weather_success(self):
        """Test successful weather API call."""
        from app.mcp.tools import weather
        import httpx
        from unittest.mock import AsyncMock, patch
        
        mock_response = {
            "name": "London",
            "sys": {"country": "GB"},
            "main": {
                "temp": 15.5,
                "feels_like": 14.0,
                "humidity": 72
            },
            "weather": [
                {"main": "Clouds", "description": "overcast clouds"}
            ],
            "wind": {"speed": 5.5}
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_get = AsyncMock()
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            mock_client.return_value.__aenter__.return_value.get = mock_get
            
            result = await weather.get_weather("London", "test_api_key")
            
            assert result["city"] == "London"
            assert result["country"] == "GB"
            assert result["temperature"] == 15.5
            assert result["condition"] == "Clouds"
    
    @pytest.mark.asyncio
    async def test_get_weather_city_not_found(self):
        """Test weather API with invalid city."""
        from app.mcp.tools import weather
        from unittest.mock import AsyncMock, patch
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_get = AsyncMock()
            mock_get.return_value.status_code = 404
            mock_client.return_value.__aenter__.return_value.get = mock_get
            
            with pytest.raises(ValueError, match="not found"):
                await weather.get_weather("InvalidCity123", "test_api_key")
    
    @pytest.mark.asyncio
    async def test_get_weather_invalid_api_key(self):
        """Test weather API with invalid API key."""
        from app.mcp.tools import weather
        from unittest.mock import AsyncMock, patch
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_get = AsyncMock()
            mock_get.return_value.status_code = 401
            mock_client.return_value.__aenter__.return_value.get = mock_get
            
            with pytest.raises(ValueError, match="Invalid API key"):
                await weather.get_weather("London", "invalid_key")
