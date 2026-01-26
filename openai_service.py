"""
OpenAI service for generating AI-powered travel itineraries.
"""

import os
from typing import Dict, List
import openai
from dotenv import load_dotenv

load_dotenv()


class OpenAIService:
    """Service class for interacting with OpenAI API to generate travel itineraries."""
    
    def __init__(self):
        """Initialize OpenAI client with API key from environment variables."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        try:
            # Clear any proxy-related env vars that might interfere
            # Initialize OpenAI client with only the api_key parameter
            # Store original env vars temporarily
            original_env = {}
            proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']
            for var in proxy_vars:
                if var in os.environ:
                    original_env[var] = os.environ[var]
                    del os.environ[var]
            
            try:
                # Initialize OpenAI client
                self.client = openai.OpenAI(api_key=api_key)
                self.model = "gpt-3.5-turbo"  # Using GPT-3.5 for cost efficiency
            finally:
                # Restore original environment variables
                for var, value in original_env.items():
                    os.environ[var] = value
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI client: {str(e)}")
    
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
        Generate a personalized travel itinerary using OpenAI API.
        
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

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional travel planner with expertise in creating detailed, practical, and budget-conscious itineraries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise Exception(f"Error generating itinerary: {str(e)}")

