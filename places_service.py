"""
Google Places API service for fetching attractions, restaurants, and cafes.
"""

import os
from typing import List, Dict, Optional
import googlemaps
from dotenv import load_dotenv

load_dotenv()


class PlacesService:
    """Service class for interacting with Google Places API."""
    
    def __init__(self):
        """Initialize Google Maps client with API key from environment variables."""
        api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        if not api_key or api_key == "your_google_places_api_key_here":
            raise ValueError("GOOGLE_PLACES_API_KEY not found in environment variables")
        try:
            self.client = googlemaps.Client(key=api_key)
        except Exception as e:
            raise ValueError(f"Failed to initialize Google Places client: {str(e)}")
    
    def get_attractions(self, destination: str, limit: int = 5) -> List[Dict]:
        """
        Get top attractions for a destination.
        
        Args:
            destination: Destination city/country
            limit: Maximum number of results to return
        
        Returns:
            List of attraction dictionaries with name, rating, and address
        """
        try:
            # Geocode the destination to get coordinates
            geocode_result = self.client.geocode(destination)
            if not geocode_result:
                return []
            
            location = geocode_result[0]['geometry']['location']
            
            # Search for tourist attractions
            places_result = self.client.places_nearby(
                location=(location['lat'], location['lng']),
                radius=5000,  # 5km radius
                type='tourist_attraction',
                rank_by='prominence'
            )
            
            attractions = []
            for place in places_result.get('results', [])[:limit]:
                attractions.append({
                    'name': place.get('name', 'Unknown'),
                    'rating': place.get('rating', 'N/A'),
                    'address': place.get('vicinity', 'Address not available'),
                    'place_id': place.get('place_id', '')
                })
            
            return attractions
        
        except Exception as e:
            print(f"Error fetching attractions: {str(e)}")
            return []
    
    def get_restaurants(self, destination: str, limit: int = 5) -> List[Dict]:
        """
        Get top restaurants for a destination.
        
        Args:
            destination: Destination city/country
            limit: Maximum number of results to return
        
        Returns:
            List of restaurant dictionaries with name, rating, and address
        """
        try:
            # Geocode the destination
            geocode_result = self.client.geocode(destination)
            if not geocode_result:
                return []
            
            location = geocode_result[0]['geometry']['location']
            
            # Search for restaurants
            places_result = self.client.places_nearby(
                location=(location['lat'], location['lng']),
                radius=5000,
                type='restaurant',
                rank_by='prominence'
            )
            
            restaurants = []
            for place in places_result.get('results', [])[:limit]:
                restaurants.append({
                    'name': place.get('name', 'Unknown'),
                    'rating': place.get('rating', 'N/A'),
                    'address': place.get('vicinity', 'Address not available'),
                    'price_level': place.get('price_level', 'N/A'),
                    'place_id': place.get('place_id', '')
                })
            
            return restaurants
        
        except Exception as e:
            print(f"Error fetching restaurants: {str(e)}")
            return []
    
    def get_cafes(self, destination: str, limit: int = 5) -> List[Dict]:
        """
        Get top cafes for a destination.
        
        Args:
            destination: Destination city/country
            limit: Maximum number of results to return
        
        Returns:
            List of cafe dictionaries with name, rating, and address
        """
        try:
            # Geocode the destination
            geocode_result = self.client.geocode(destination)
            if not geocode_result:
                return []
            
            location = geocode_result[0]['geometry']['location']
            
            # Search for cafes
            places_result = self.client.places_nearby(
                location=(location['lat'], location['lng']),
                radius=5000,
                type='cafe',
                rank_by='prominence'
            )
            
            cafes = []
            for place in places_result.get('results', [])[:limit]:
                cafes.append({
                    'name': place.get('name', 'Unknown'),
                    'rating': place.get('rating', 'N/A'),
                    'address': place.get('vicinity', 'Address not available'),
                    'place_id': place.get('place_id', '')
                })
            
            return cafes
        
        except Exception as e:
            print(f"Error fetching cafes: {str(e)}")
            return []

