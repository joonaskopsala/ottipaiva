from datetime import datetime, timedelta

def predict_fishing_success(weather_data):
    temp = weather_data['main']['temp']
    wind_speed = weather_data['wind']['speed']

    if 15 <= temp <= 25 and wind_speed < 10:
        return {"text": "Loistavat olosuhteet kalastukseen!", "icon": "happy.png"}
    elif (10 <= temp < 15 or 25 < temp <= 30) and wind_speed < 15:
        return {"text": "Hyvät olosuhteet kalastukseen.", "icon": "happy.png"}
    elif temp < 10 or temp > 30 or wind_speed > 15:
        return {"text": "Huonot olosuhteet kalastukselle.", "icon": "sad.png"}
    return {"text": "Olosuhteet ovat keskinkertaiset.", "icon": "neutral.png"}

def process_forecast_data(weather_data):
    return [
        {
            "prediction": predict_fishing_success(day_data)["text"],
            "fisherman_icon": predict_fishing_success(day_data)["icon"],
            "temp": day_data['main']['temp'],
            "wind_speed": day_data['wind']['speed'],
            "date": day_data['dt']
        }
        for day_data in weather_data['list']
    ]

def filter_forecast_data(forecast):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    day_ranges = [(today + timedelta(days=i), today + timedelta(days=i+1) - timedelta(seconds=1)) for i in range(6)]
    
    day_lists = [[] for _ in range(6)]
    for obj in forecast:
        obj_date = datetime.fromtimestamp(obj['date'])
        for i, (start_day, end_day) in enumerate(day_ranges):
            if start_day <= obj_date <= end_day:
                day_lists[i].append(obj)
                break

    return [day_list for day_list in day_lists if day_list]
