# ✈️ AI-Powered Travel Planner

An intelligent web application that generates personalized travel itineraries using AI and real-time data from multiple APIs. Built with Python and Streamlit.

## 🌟 Features

- **AI-Powered Itinerary Generation**: Uses OpenAI GPT or Ollama (local LLM) to create detailed, personalized day-wise travel plans
- **Smart Recommendations**: Integrates with Google Places API to suggest top attractions, restaurants, and cafes
- **Weather Integration**: Optional weather forecasts for your travel dates via OpenWeather API
- **Budget-Aware Planning**: Considers your budget level (low/medium/high) when generating recommendations
- **Personalized Experience**: Tailors suggestions based on your interests (nature, food, culture, nightlife, adventure, etc.)
- **Travel Type Optimization**: Adapts recommendations for solo travelers, couples, friends, or families
- **Clean & Intuitive UI**: Simple Streamlit interface with expandable sections for easy navigation

## 🛠️ Tech Stack

- **Python 3.8+**: Core programming language
- **Streamlit**: Web framework for the frontend UI
- **OpenAI API** or **Ollama**: For AI itinerary generation
  - OpenAI: Cloud-based (requires API key, may have quotas)
  - Ollama: Local LLM (free, no quotas, perfect for 8GB RAM)
- **Google Places API**: For attractions, restaurants, and cafes
- **OpenWeather API**: For weather information (optional)
- **python-dotenv**: For secure API key management

## 📋 Prerequisites

- Python 3.8 or higher
- AI Service (choose one):
  - **OpenAI API key** (cloud-based, may have quotas)
  - **Ollama** (local, free, no quotas - recommended for 8GB RAM)
- API keys for:
  - Google Places API (optional, for places recommendations)
  - OpenWeather API (optional, for weather info)

## 🚀 Setup Instructions

### 1. Clone or Download the Project

```bash
cd Travel-planner
```

### 2. Install Dependencies

Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

Install required packages:

```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_PLACES_API_KEY=your_google_places_api_key_here
   OPENWEATHER_API_KEY=your_openweather_api_key_here
   ```

### 4. Get API Keys

#### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new secret key
5. Copy and paste it into your `.env` file

#### Google Places API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the "Places API" and "Geocoding API"
4. Go to "Credentials" and create an API key
5. Restrict the key to Places API and Geocoding API for security
6. Copy and paste it into your `.env` file




#### OpenWeather API Key (Optional)
1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to API keys section
4. Copy your default API key
5. Paste it into your `.env` file

#### Ollama Setup (Alternative to OpenAI - Free & Local)
**Ollama allows you to use local LLMs without API costs or quotas!**

1. **Install Ollama:**
   ```bash
   # macOS: Download from https://ollama.com/download
   # Or use Homebrew:
   brew install ollama
   ```

2. **Start Ollama service:**
   ```bash
   ollama serve
   ```
   (Keep this running in a terminal)

3. **Pull a lightweight model (recommended for 8GB RAM):**
   ```bash
   ollama pull phi3:mini    # ~2GB, fast and efficient
   # or
   ollama pull llama3.2     # Alternative option
   ```

4. **Configure in `.env` (already added):**
   ```env
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=phi3:mini
   ```

5. **In the app:** Select "Ollama (Local)" from the AI Service dropdown in the sidebar

**Benefits:**
- ✅ No API costs
- ✅ No quota limits
- ✅ Works offline
- ✅ Privacy (runs locally)
- ✅ Perfect for 8GB RAM machines

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 How to Use

1. **Enter Trip Details** (in the sidebar):
   - Source city (where you're traveling from)
   - Destination city/country
   - Start and end dates
   - Budget level (low/medium/high)
   - Select your interests
   - Choose travel type (solo/couple/friends/family)

2. **Generate Itinerary**:
   - Click the "🚀 Generate Itinerary" button
   - Wait for the AI to generate your personalized plan

3. **Review Your Itinerary**:
   - View day-wise schedule in expandable sections
   - Check estimated expenses
   - See food recommendations
   - Browse top attractions, restaurants, and cafes
   - Review weather information (if available)

## 📁 Project Structure

```
Travel-planner/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Template for environment variables
├── .env                  # Your API keys (not in git)
├── README.md             # This file
├── services/
│   ├── openai_service.py    # OpenAI API integration
│   ├── places_service.py    # Google Places API integration
│   └── weather_service.py   # OpenWeather API integration
└── utils/
    └── helpers.py           # Utility functions
```

## ⚙️ Configuration

### Budget Levels
- **Low**: $30-70 per day
- **Medium**: $70-150 per day
- **High**: $150-500 per day

### Supported Interests
- Nature
- Food
- Culture
- Nightlife
- Adventure
- Shopping
- History
- Beaches

### Travel Types
- Solo
- Couple
- Friends
- Family

## 🔒 Security Notes

- **Never commit your `.env` file** to version control
- The `.env` file is already in `.gitignore` (if using git)
- Keep your API keys secure and don't share them
- Consider restricting API keys in their respective platforms

## 🐛 Troubleshooting

### "API key not found" error
- Make sure your `.env` file exists in the project root
- Verify that API keys are correctly formatted (no extra spaces)
- Restart the Streamlit app after updating `.env`

### "Service unavailable" warning
- Check if your API keys are valid
- Verify that you have enabled the required APIs in Google Cloud Console
- Ensure you have sufficient API credits/quota

### Slow response times
- The app makes multiple API calls which can take a few seconds
- Check your internet connection
- Some APIs have rate limits on free tiers

## 📝 Example Usage

**Input:**
- Source: New York
- Destination: Paris, France
- Dates: 7 days
- Budget: Medium
- Interests: Culture, Food, History
- Travel Type: Couple

**Output:**
- Detailed 7-day itinerary with daily schedules
- Restaurant recommendations for each day
- Top attractions in Paris
- Weather forecast
- Local tips and safety advice

## 🎯 Performance

- Optimized for systems with 8GB RAM
- No heavy ML models (uses API-based AI)
- Efficient API calls with limits
- Lightweight and fast UI

## 📄 License

This project is open source and available for personal and educational use.

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 📧 Support

For issues or questions, please open an issue on the project repository.

---

**Happy Traveling! ✈️🌍**

