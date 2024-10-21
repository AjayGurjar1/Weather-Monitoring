**Project Overview**

This Weather Monitoring System is a real-time web application that allows users to check weather information for various cities. It fetches data from the OpenWeatherMap API and stores daily weather summaries in a SQLite database. Users can view the current weather as well as historical trends.

**Technologies Used**

Frontend: HTML, CSS (with Bootstrap) 

Backend: Python (Flask) 

Database: SQLite

APIs: OpenWeatherMap API

Setup Instructions

**Prerequisites**

Python 3.x

Flask

SQLite

**Clone the Repository**

git clone https://github.com/AjayGurjar1/Weather-Monitoring

cd weather-monitoring

Add your OpenWeatherMap API key in app.py at line-9

**Install Dependencies**

pip install -r requirements.txt

python app.py 

Access the application at http://127.0.0.1:5000/.

Usage
Select a city from the dropdown menu and click "Get Weather" to retrieve the current weather information.
Navigate to the "View Weather Trends" link to see historical weather data.
