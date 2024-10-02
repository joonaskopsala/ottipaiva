from flask import Flask, jsonify, render_template, request
import requests
from config import OPENWEATHER_API_KEY

app = Flask(__name__)

def get_weather_data(city_name):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def predict_fishing_success(weather_data):
    temp = weather_data['main']['temp']
    wind_speed = weather_data['wind']['speed']
    pressure = weather_data['main']['pressure']
    humidity = weather_data['main']['humidity']

    if 15 <= temp <= 25 and wind_speed < 10 and pressure > 1010 and humidity < 80:
        return {
            "text": "Great conditions for fishing! Temperature, wind, and pressure are all ideal.",
            "icon": "happy.png"
        }
    elif (10 <= temp < 15 or 25 < temp <= 30) and wind_speed < 15 and pressure > 1005:
        return {
            "text": "Good conditions for fishing, but keep an eye on temperature and wind.",
            "icon": "happy.png"
        }
    elif temp < 10 or temp > 30 or wind_speed > 15:
        return {
            "text": "Poor conditions for fishing due to extreme temperatures or high winds.",
            "icon": "sad.png"
        }
    else:
        return {
            "text": "Conditions are average. You might still catch some fish, but it's not ideal.",
            "icon": "neutral.png"
        }

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = ""
    fisherman_icon = "neutral.png"

    if request.method == "POST":
        city = request.form.get("city")
        weather_data = get_weather_data(city)

        if weather_data:
            prediction_data = predict_fishing_success(weather_data)
            prediction = prediction_data["text"]
            fisherman_icon = prediction_data["icon"]
        else:
            prediction = "City not found. Please try again."
            fisherman_icon = "sad.png"

    return render_template("index.html", prediction=prediction, fisherman_icon=fisherman_icon)

if __name__ == "__main__":
    app.run(debug=True)
