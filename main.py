import requests
from config import OPENWEATHER_API_KEY

def get_weather_data(city_name, api_key):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def predict_fishing_success(weather_data):
    temp = weather_data['main']['temp']
    wind_speed = weather_data['wind']['speed']
    pressure = weather_data['main']['pressure']
    humidity = weather_data['main']['humidity']

    if 15 <= temp <= 25 and wind_speed < 10 and pressure > 1010 and humidity < 80:
        return "Great conditions for fishing! Temperature, wind, and pressure are all ideal."
    elif 10 <= temp < 15 or 25 < temp <= 30 and wind_speed < 15 and pressure > 1005:
        return "Good conditions for fishing, but keep an eye on temperature and wind."
    elif temp < 10 or temp > 30 or wind_speed > 15:
        return "Poor conditions for fishing due to extreme temperatures or high winds."
    else:
        return "Conditions are average. You might still catch some fish, but it's not ideal."

if __name__ == "__main__":
    city = input("Enter the city name: ")
    api_key = OPENWEATHER_API_KEY
    weather_data = get_weather_data(city, api_key)
    
    if weather_data:
        result = predict_fishing_success(weather_data)
        print(f"Fishing forecast for {city}: {result}")
