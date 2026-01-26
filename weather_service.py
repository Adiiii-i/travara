"""
OpenWeather API service for fetching weather information.
"""

import os
from typing import Dict, Optional
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class WeatherService:
    """Service class for interacting with OpenWeather API."""
    
    def __init__(self):
        """Initialize weather service with API key from environment variables."""
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def get_weather_summary(self, destination: str, start_date: datetime, end_date: datetime) -> Optional[Dict]:
        """
        Get weather summary for a destination during travel dates.
        
        Args:
            destination: Destination city/country
            start_date: Trip start date
            end_date: Trip end date
        
        Returns:
            Dictionary with weather summary or None if unavailable
        """
        if not self.api_key:
            return None
        
        try:
            # Get current weather for the destination
            # Note: Free tier of OpenWeather API provides current weather and 5-day forecast
            # For simplicity, we'll get current weather and a forecast if available
            geocode_url = f"http://api.openweathermap.org/geo/1.0/direct"
            geocode_params = {
                "q": destination,
                "limit": 1,
                "appid": self.api_key
            }
            
            geocode_response = requests.get(geocode_url, params=geocode_params, timeout=5)
            if geocode_response.status_code != 200:
                return None
            
            geocode_data = geocode_response.json()
            if not geocode_data:
                return None
            
            lat = geocode_data[0]['lat']
            lon = geocode_data[0]['lon']
            
            # Get current weather
            weather_url = f"{self.base_url}/weather"
            weather_params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            
            weather_response = requests.get(weather_url, params=weather_params, timeout=5)
            if weather_response.status_code != 200:
                return None
            
            weather_data = weather_response.json()
            
            # Get 5-day forecast
            forecast_url = f"{self.base_url}/forecast"
            forecast_response = requests.get(forecast_url, params=weather_params, timeout=5)
            
            forecast_data = None
            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()
            
            return {
                "current": {
                    "temperature": weather_data['main']['temp'],
                    "description": weather_data['weather'][0]['description'],
                    "humidity": weather_data['main']['humidity'],
                    "wind_speed": weather_data.get('wind', {}).get('speed', 0)
                },
                "forecast": forecast_data,
                "location": destination
            }
        
        except Exception as e:
            print(f"Error fetching weather: {str(e)}")
            return None
    
    def format_weather_summary(self, weather_data: Dict) -> str:
        """
        Format weather data into a readable string.
        
        Args:
            weather_data: Weather data dictionary
        
        Returns:
            Formatted weather summary string
        """
        if not weather_data:
            return "Weather information unavailable."
        
        current = weather_data.get('current', {})
        location = weather_data.get('location', 'Unknown')
        
        summary = f"**Weather in {location}:**\n\n"
        summary += f"🌡️ Temperature: {current.get('temperature', 'N/A')}°C\n"
        summary += f"☁️ Conditions: {current.get('description', 'N/A').title()}\n"
        summary += f"💧 Humidity: {current.get('humidity', 'N/A')}%\n"
        summary += f"💨 Wind Speed: {current.get('wind_speed', 'N/A')} m/s\n"
        
        return summary

