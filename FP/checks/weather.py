import requests
from datetime import datetime

def get_weather_data(lat, lon):
    """
    Fetch weather data from Open-Meteo (No API key required).
    Returns a dict with current weather and a short farming advice.
    """
    if not lat or not lon:
        return None

    try:
        # Open-Meteo API URL
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,is_day,precipitation,weather_code,wind_speed_10m&timezone=auto"
        
        response = requests.get(url, timeout=10)
        if not response.ok:
            return None
            
        data = response.json()
        current = data.get('current', {})
        
        temp = current.get('temperature_2m')
        humidity = current.get('relative_humidity_2m')
        precip = current.get('precipitation', 0)
        code = current.get('weather_code', 0)
        
        # Determine advice based on weather code (WMO codes)
        # 0: Clear, 1-3: Partly Cloudy, 51-67: Rain, 71-77: Snow, 80-82: Showers
        advice = "Good conditions for general farming activities."
        icon = "☀️"
        
        if precip > 0 or code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            advice = "Rain expected. Avoid spraying pesticides or fertilizers today."
            icon = "🌧️"
        elif temp > 35:
            advice = "High heat detected. Ensure adequate irrigation for sensitive crops."
            icon = "🔥"
        elif temp < 10:
            advice = "Low temperatures. Protect frost-sensitive plants if necessary."
            icon = "❄️"
        elif humidity > 85:
            advice = "High humidity. Check for fungal growth and pests."
            icon = "🌫️"
            
        return {
            'temp': temp,
            'humidity': humidity,
            'advice': advice,
            'icon': icon,
            'description': _get_weather_description(code),
            'timestamp': datetime.now().strftime("%I:%M %p")
        }
    except Exception as e:
        print(f"Weather Fetch Error: {e}")
        return None

def _get_weather_description(code):
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers"
    }
    return descriptions.get(code, "Cloudy")
