# ottipaiva
Python project to check weather conditions and predict if its good day to fish or not

# HOW TO RUN
Install required packages:
pip install -r requirements.txt

From project root, run:
1. env\Scripts\activate
2. set FLASK_APP=app.py (this is to configure development settings for Flask)
3. set FLASK_ENV=development (this is to configure development settings for Flask)
4. python -m web_app.app

# REQUIREMENTS
In project root, create file named config.py and get Openweatherapp api key from https://openweathermap.org, set it as OPENWEATHER_API_KEY = "your_key"
