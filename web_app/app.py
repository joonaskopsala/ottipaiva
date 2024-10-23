from flask import Flask, jsonify, render_template, request
import requests
import os
import sys
from web_app.utils import process_forecast_data, filter_forecast_data
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import OPENWEATHER_API_KEY

app = Flask(__name__)

def get_weather_data(city_name):
    base_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    forecast = []
    filteredforecast = []
    city = ""

    if request.method == "POST":
        city = request.form.get("city").capitalize()
        weather_data = get_weather_data(city)

        if weather_data:
            forecast = process_forecast_data(weather_data)
            filteredforecast = filter_forecast_data(forecast)
        else:
            forecast = [{"prediction": "Kaupunkia ei löytynyt. Yritä uudelleen.", "fisherman_icon": "sad.png"}]

    return render_template("index.html", forecast=forecast, location=city, filteredData=filteredforecast)

if __name__ == "__main__":
    app.run(debug=True)
