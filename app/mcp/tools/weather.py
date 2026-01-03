"""Weather tool for MCP.

Provides weather information using OpenWeatherMap API.
"""

import httpx
from typing import Any


async def get_weather(city: str, api_key: str) -> dict[str, Any]:
    """
    Get current weather for a city.
    
    Args:
        city: City name (e.g., "London", "New York")
        api_key: OpenWeatherMap API key
        
    Returns:
        Weather information including temperature, condition, humidity
        
    Raises:
        ValueError: If API request fails or city not found
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",  # Celsius
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url, params=params, timeout=10.0)
            
            if response.status_code == 404:
                raise ValueError(f"City '{city}' not found")
            elif response.status_code == 401:
                raise ValueError("Invalid API key")
            elif response.status_code != 200:
                raise ValueError(f"Weather API error: {response.status_code}")
            
            data = response.json()
            
            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "condition": data["weather"][0]["main"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
            }
    
    except httpx.TimeoutException:
        raise ValueError("Weather API request timed out")
    except httpx.RequestError as e:
        raise ValueError(f"Weather API request failed: {str(e)}")
    except (KeyError, IndexError) as e:
        raise ValueError(f"Unexpected weather API response format: {str(e)}")
