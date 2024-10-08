from flask import Flask, render_template, request
import requests
import os
import sys
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import OPENWEATHER_API_KEY

app = Flask(__name__)

# Date format filter
@app.template_filter('dateformat')
def dateformat(value):
    return datetime.fromtimestamp(value, tz=timezone.utc).strftime('%Y-%m-%d %H:%M')

# Function to get weather data from OpenWeather 5 Day / 3 Hour Forecast API
def get_weather_data(city_name):
    base_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Function to predict fishing success
def predict_fishing_success(weather_data):
    temp = weather_data['main']['temp']
    wind_speed = weather_data['wind']['speed']

    if 15 <= temp <= 25 and wind_speed < 10:
        return {
            "text": "Loistavat olosuhteet kalastukseen! Lämpötila ja tuuli ovat ihanteelliset.",
            "icon": "happy.png"
        }
    elif (10 <= temp < 15 or 25 < temp <= 30) and wind_speed < 15:
        return {
            "text": "Hyvät olosuhteet kalastukseen, mutta seuraa lämpötilaa ja tuulta.",
            "icon": "happy.png"
        }
    elif temp < 10 or temp > 30 or wind_speed > 15:
        return {
            "text": "Huonot olosuhteet kalastukselle äärimmäisten lämpötilojen tai kovan tuulen takia.",
            "icon": "sad.png"
        }
    else:
        return {
            "text": "Olosuhteet ovat keskinkertaiset. Voit silti saada kalaa, mutta ei ole ihanteellista.",
            "icon": "neutral.png"
        }

# Process forecast data from API response
def process_forecast_data(forecast_data):
    forecast = []
    for day_data in forecast_data['list']:
        date = day_data['dt']
        temp = day_data['main']['temp']
        wind_speed = day_data['wind']['speed']
        
        prediction_data = predict_fishing_success(day_data)
        forecast.append({
            "prediction": prediction_data["text"],
            "fisherman_icon": prediction_data["icon"],
            "temp": temp,
            "wind_speed": wind_speed,
            "date": date
        })
    return forecast

@app.route("/", methods=["GET", "POST"])
def index():
    forecast = []
    city = ""

    if request.method == "POST":
        city = request.form.get("city")
        weather_data = get_weather_data(city)

        if weather_data:
            forecast = process_forecast_data(weather_data)
        else:
            forecast = [{"prediction": "Kaupunkia ei löytynyt. Yritä uudelleen.", "fisherman_icon": "sad.png"}]

    return render_template("index.html", forecast=forecast, location=city)

if __name__ == "__main__":
    app.run(debug=True)
