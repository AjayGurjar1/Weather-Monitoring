import requests 
from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)


API_KEY = 'ADD_YOUR_API_KEY'     #add your OpenWeatherMap api key  here 
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

# Database initialization 
def init_db():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            datetime TEXT,
            avg_temp REAL,
            max_temp REAL,
            min_temp REAL,
            dominant_condition TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to fetch weather data from OpenWeatherMap API
def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

  
    if response.status_code != 200:
        print(f"Error fetching weather data: {data.get('message', 'Unknown error')}")
        return None

    return data

# Function to store daily weather summary
def store_daily_summary(city, weather_data):
    avg_temp = sum([w['main']['temp'] for w in weather_data]) / len(weather_data)
    max_temp = max([w['main']['temp_max'] for w in weather_data])
    min_temp = min([w['main']['temp_min'] for w in weather_data])
    
    # Dominant weather condition logic (you can customize this further)
    condition_counts = {}
    for w in weather_data:
        condition = w['weather'][0]['description']
        condition_counts[condition] = condition_counts.get(condition, 0) + 1

    dominant_condition = max(condition_counts, key=condition_counts.get)

    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save summary to database
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO daily_summary (city, datetime, avg_temp, max_temp, min_temp, dominant_condition)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (city, datetime_now, avg_temp, max_temp, min_temp, dominant_condition))
    conn.commit()
    conn.close()

# Function to check for alert thresholds
def check_alert(city, temperature):
    threshold = 35.0  # Example threshold
    alert_msg = None

    if temperature > threshold:
        alert_msg = f"ALERT: Temperature in {city} exceeded {threshold}°C!"

    
    if alert_msg:
        print(alert_msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_city = request.form.get('city', 'Delhi')
    
    weather = fetch_weather(selected_city)
    
    if weather is None:
        return render_template('index.html', cities=CITIES, selected_city=selected_city, weather=None)

    # Store weather data and check for alerts
    store_daily_summary(selected_city, [weather])  # Store the current weather
    check_alert(selected_city, weather['main']['temp'])

    weather_info = {
        "temperature": weather['main']['temp'],
        "feels_like": weather['main']['feels_like'],
        "humidity": weather['main']['humidity'],
        "wind_speed": weather['wind']['speed'],
        "condition": weather['weather'][0]['description'],
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    }
    
    return render_template('index.html', cities=CITIES, selected_city=selected_city, weather=weather_info)


@app.route('/trends', methods=['GET'])
def view_trends():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('SELECT city, datetime, avg_temp, max_temp, min_temp, dominant_condition FROM daily_summary')
    trends_data = cursor.fetchall()
    conn.close()

    # Prepare data for display
    trends = [
        {
            "city": row[0],
            "datetime": row[1],
            "avg_temp": row[2],
            "max_temp": row[3],
            "min_temp": row[4],
            "dominant_condition": row[5]
        } for row in trends_data
    ]

    return render_template('trends.html', trends=trends)

if __name__ == '__main__':
    init_db()  
    app.run(debug=True)
