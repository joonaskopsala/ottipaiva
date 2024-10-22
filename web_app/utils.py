from datetime import datetime, timedelta


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

def process_forecast_data(weather_data):
    forecast = []
    for day_data in weather_data['list']:
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

def filter_forecast_data(forecast):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    day_ranges = [(today + timedelta(days=i), today + timedelta(days=i+1) - timedelta(seconds=1)) for i in range(6)]

    day_lists = [[] for _ in range(6)]  # One array for each day

    for obj in forecast:
        obj_date = datetime.fromtimestamp(obj['date'])

        for i in range(6):
            start_day, end_day = day_ranges[i]
            if start_day <= obj_date <= end_day:
                day_lists[i].append(obj)
                break

    # Remove empty arrays
    day_lists = [day_list for day_list in day_lists if day_list]

    return day_lists