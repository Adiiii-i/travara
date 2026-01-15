"""
AI-Powered Travel Planner - Main Streamlit Application
"""

import streamlit as st
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from services.openai_service import OpenAIService
from services.ollama_service import OllamaService
from services.places_service import PlacesService
from services.weather_service import WeatherService
from utils.helpers import (
    calculate_trip_duration,
    format_date,
    validate_dates,
    format_interests
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stExpander {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_services():
    """Initialize API services with error handling."""
    services = {}
    errors = []
    
    # Initialize OpenAI service
    try:
        services['openai'] = OpenAIService()
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg or "your_openai_api_key_here" in error_msg:
            errors.append("OpenAI: API key not configured. Please add your OPENAI_API_KEY to the .env file.")
        else:
            errors.append(f"OpenAI: {error_msg}")
        services['openai'] = None
    except Exception as e:
        errors.append(f"OpenAI: {str(e)}")
        services['openai'] = None
    
    # Initialize Ollama service
    try:
        services['ollama'] = OllamaService()
    except ValueError as e:
        error_msg = str(e)
        if "Cannot connect" in error_msg or "not responding" in error_msg:
            errors.append(f"Ollama: {error_msg}")
        else:
            errors.append(f"Ollama: {error_msg}")
        services['ollama'] = None
    except Exception as e:
        errors.append(f"Ollama: {str(e)}")
        services['ollama'] = None
    
    # Initialize Google Places service
    try:
        services['places'] = PlacesService()
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg or "your_google_places_api_key_here" in error_msg:
            errors.append("Google Places: API key not configured. Please add your GOOGLE_PLACES_API_KEY to the .env file.")
        else:
            errors.append(f"Google Places: {error_msg}")
        services['places'] = None
    except Exception as e:
        errors.append(f"Google Places: {str(e)}")
        services['places'] = None
    
    # Initialize Weather service (optional)
    try:
        services['weather'] = WeatherService()
    except Exception as e:
        services['weather'] = None
    
    return services, errors


def main():
    """Main application function."""
    
    # Header
    st.markdown('<p class="main-header">✈️ AI Travel Planner</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Generate personalized travel itineraries powered by AI</p>', unsafe_allow_html=True)
    
    # Initialize services
    services, service_errors = initialize_services()
    
    if service_errors:
        st.warning("⚠️ Some services are unavailable. Please check your API keys in the .env file.")
        for error in service_errors:
            st.error(error)
    
    # Sidebar for user inputs
    with st.sidebar:
        st.header("📝 Trip Details")
        
        source = st.text_input("Source City", placeholder="e.g., New York")
        destination = st.text_input("Destination City/Country", placeholder="e.g., Paris, France")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                min_value=datetime.now().date(),
                value=datetime.now().date() + timedelta(days=7)
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                min_value=datetime.now().date(),
                value=datetime.now().date() + timedelta(days=14)
            )
        
        budget = st.selectbox(
            "Budget Level",
            ["low", "medium", "high"],
            index=1
        )
        
        interests = st.multiselect(
            "Interests",
            ["nature", "food", "culture", "nightlife", "adventure", "shopping", "history", "beaches"],
            default=["culture", "food"]
        )
        
        travel_type = st.selectbox(
            "Travel Type",
            ["solo", "couple", "friends", "family"],
            index=0
        )
        
        # AI Service Selection
        st.markdown("---")
        st.subheader("🤖 AI Service")
        ai_service_options = []
        if services.get('ollama'):
            ai_service_options.append("Ollama (Local)")
        if services.get('openai'):
            ai_service_options.append("OpenAI")
        
        if not ai_service_options:
            st.warning("No AI service available. Please configure OpenAI or start Ollama.")
            ai_service = None
        else:
            default_index = 0
            if "Ollama (Local)" in ai_service_options:
                default_index = 0  # Prefer Ollama if available
            ai_service = st.radio(
                "Choose AI Service:",
                ai_service_options,
                index=default_index if ai_service_options else None
            )
        
        generate_button = st.button("🚀 Generate Itinerary", type="primary", use_container_width=True)
    
    # Main content area
    if generate_button:
        # Validate inputs
        if not source or not destination:
            st.error("❌ Please fill in both source and destination cities.")
            return
        
        # Validate dates
        start_dt = datetime.combine(start_date, datetime.min.time())
        end_dt = datetime.combine(end_date, datetime.min.time())
        
        is_valid, error_msg = validate_dates(start_dt, end_dt)
        if not is_valid:
            st.error(f"❌ {error_msg}")
            return
        
        # Check if AI service is available
        if not ai_service:
            st.error("❌ No AI service available. Please configure OpenAI or start Ollama.")
            return
        
        # Determine which service to use
        if ai_service == "Ollama (Local)":
            ai_service_obj = services.get('ollama')
            service_name = "Ollama"
        else:
            ai_service_obj = services.get('openai')
            service_name = "OpenAI"
        
        if not ai_service_obj:
            st.error(f"❌ {service_name} service is not available. Please check your configuration.")
            return
        
        # Calculate trip duration
        duration = calculate_trip_duration(start_dt, end_dt)
        
        # Display trip summary
        st.success(f"✅ Planning a {duration}-day trip from {source} to {destination} using {service_name}")
        
        # Generate itinerary
        with st.spinner(f"🤖 {service_name} is generating your personalized itinerary..."):
            try:
                itinerary = ai_service_obj.generate_itinerary(
                    source=source,
                    destination=destination,
                    start_date=format_date(start_dt),
                    end_date=format_date(end_dt),
                    duration=duration,
                    budget=budget,
                    interests=interests,
                    travel_type=travel_type
                )
                
                st.session_state['itinerary'] = itinerary
                st.session_state['destination'] = destination
                st.session_state['start_date'] = start_dt
                st.session_state['end_date'] = end_dt
                
            except Exception as e:
                st.error(f"❌ Error generating itinerary: {str(e)}")
                return
        
        # Display itinerary
        if 'itinerary' in st.session_state:
            st.markdown("---")
            st.header("📅 Your Travel Itinerary")
            
            # Display itinerary - try to split by days, otherwise show as single block
            itinerary_text = st.session_state['itinerary']
            lines = itinerary_text.split('\n')
            
            # Check if itinerary has day markers
            has_day_markers = any(
                line.lower().strip().startswith(('day ', '**day ', '# day '))
                for line in lines
            )
            
            if has_day_markers:
                # Split itinerary by days and display in expandable sections
                current_day = None
                current_content = []
                
                for line in lines:
                    line_lower = line.lower().strip()
                    # Check for various day marker formats
                    if (line_lower.startswith('day ') or 
                        line_lower.startswith('**day ') or 
                        line_lower.startswith('# day ') or
                        (line.strip().startswith('#') and 'day' in line_lower)):
                        # Save previous day if exists
                        if current_day is not None:
                            with st.expander(current_day, expanded=True):
                                st.markdown('\n'.join(current_content))
                        
                        # Start new day
                        current_day = line.strip().replace('#', '').replace('**', '').strip()
                        current_content = []
                    else:
                        if current_day is None:
                            # Content before first day
                            current_day = "Overview"
                            current_content.append(line)
                        else:
                            current_content.append(line)
                
                # Display last day
                if current_day:
                    with st.expander(current_day, expanded=True):
                        st.markdown('\n'.join(current_content))
            else:
                # No day markers found, display as single formatted text
                st.markdown(itinerary_text)
            
            # Weather information (optional)
            if services.get('weather') and services['weather'].api_key:
                st.markdown("---")
                st.header("🌤️ Weather Information")
                with st.spinner("Fetching weather data..."):
                    weather_data = services['weather'].get_weather_summary(
                        st.session_state['destination'],
                        st.session_state['start_date'],
                        st.session_state['end_date']
                    )
                    if weather_data:
                        weather_summary = services['weather'].format_weather_summary(weather_data)
                        st.markdown(weather_summary)
            
            # Places recommendations
            if services.get('places'):
                st.markdown("---")
                st.header("📍 Recommended Places")
                
                with st.spinner("Fetching places recommendations..."):
                    # Get attractions
                    attractions = services['places'].get_attractions(destination, limit=5)
                    if attractions:
                        st.subheader("🏛️ Top Attractions")
                        for attr in attractions:
                            rating = attr.get('rating', 'N/A')
                            rating_str = f"⭐ {rating}" if rating != 'N/A' else ""
                            st.markdown(f"**{attr['name']}** {rating_str}")
                            st.caption(f"📍 {attr['address']}")
                    
                    # Get restaurants
                    restaurants = services['places'].get_restaurants(destination, limit=5)
                    if restaurants:
                        st.subheader("🍽️ Top Restaurants")
                        for rest in restaurants:
                            rating = rest.get('rating', 'N/A')
                            rating_str = f"⭐ {rating}" if rating != 'N/A' else ""
                            price_level = rest.get('price_level', '')
                            price_str = "💰" * price_level if isinstance(price_level, int) else ""
                            st.markdown(f"**{rest['name']}** {rating_str} {price_str}")
                            st.caption(f"📍 {rest['address']}")
                    
                    # Get cafes
                    cafes = services['places'].get_cafes(destination, limit=5)
                    if cafes:
                        st.subheader("☕ Top Cafes")
                        for cafe in cafes:
                            rating = cafe.get('rating', 'N/A')
                            rating_str = f"⭐ {rating}" if rating != 'N/A' else ""
                            st.markdown(f"**{cafe['name']}** {rating_str}")
                            st.caption(f"📍 {cafe['address']}")
    
    else:
        # Welcome message
        st.info("👈 Fill in the trip details in the sidebar and click 'Generate Itinerary' to get started!")
        
        # Display example
        with st.expander("📖 How it works"):
            st.markdown("""
            **AI Travel Planner** helps you create personalized travel itineraries:
            
            1. **Enter your trip details** in the sidebar:
               - Source and destination cities
               - Travel dates
               - Budget level
               - Your interests
               - Travel type
            
            2. **Click "Generate Itinerary"** to create your personalized plan
            
            3. **Get comprehensive recommendations**:
               - Day-wise detailed schedule
               - Estimated expenses
               - Food suggestions
               - Top attractions, restaurants, and cafes
               - Weather information
               - Local tips and safety advice
            
            The AI considers your preferences, budget, and travel style to create the perfect itinerary for you!
            """)


if __name__ == "__main__":
    main()

