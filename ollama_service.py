"""
Ollama service for generating AI-powered travel itineraries using local LLM.
"""

import os
from typing import List
import requests
from dotenv import load_dotenv

load_dotenv()


class OllamaService:
    """Service class for interacting with Ollama API to generate travel itineraries."""
    
    def __init__(self):
        """Initialize Ollama service with base URL from environment variables."""
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2")  # Default to llama3.2, can be changed
        
        # Test connection to Ollama
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                raise ValueError(f"Ollama server not responding at {self.base_url}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Cannot connect to Ollama at {self.base_url}. Make sure Ollama is running: {str(e)}")
    
    def generate_itinerary(
        self,
        source: str,
        destination: str,
        start_date: str,
        end_date: str,
        duration: int,
        budget: str,
        interests: List[str],
        travel_type: str
    ) -> str:
        """
        Generate a personalized travel itinerary using Ollama API.
        
        Args:
            source: Source city
            destination: Destination city/country
            start_date: Trip start date (formatted string)
            end_date: Trip end date (formatted string)
            duration: Number of days
            budget: Budget level (low/medium/high)
            interests: List of interests
            travel_type: Type of travel (solo/couple/friends/family)
        
        Returns:
            Generated itinerary as a formatted string
        """
        interests_str = ", ".join(interests) if interests else "general travel"
        
        prompt = f"""You are an expert travel planner. Create a detailed {duration}-day travel itinerary for a trip from {source} to {destination}.

Travel Details:
- Travel Dates: {start_date} to {end_date}
- Budget Level: {budget}
- Interests: {interests_str}
- Travel Type: {travel_type}

Please provide a day-wise itinerary that includes:
1. Daily schedule with time slots (morning, afternoon, evening)
2. Specific activities and attractions to visit
3. Estimated daily expenses in USD (based on {budget} budget)
4. Food recommendations (breakfast, lunch, dinner) with local specialties
5. Local travel tips
6. Safety tips specific to {destination}

Format the response clearly with:
- Day 1, Day 2, etc. as headers
- Use bullet points for activities
- Keep it concise but informative
- Make it practical and actionable

Focus on authentic experiences that match the traveler's interests and budget level."""

        system_prompt = "You are a professional travel planner with expertise in creating detailed, practical, and budget-conscious itineraries."

        try:
            # Ollama API format
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 2000  # Similar to max_tokens
                    }
                },
                timeout=120  # Ollama can take longer for local processing
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama API error: {response.status_code} - {response.text}")
            
            result = response.json()
            return result.get("message", {}).get("content", "").strip()
        
        except requests.exceptions.Timeout:
            raise Exception("Ollama request timed out. The model might be too slow or not responding.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error connecting to Ollama: {str(e)}")
        except Exception as e:
            raise Exception(f"Error generating itinerary: {str(e)}")

