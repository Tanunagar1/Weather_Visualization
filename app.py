import requests
import matplotlib.pyplot as plt
import numpy as np
from flask import render_template, Flask, request, redirect, url_for
from datetime import datetime


app =Flask(__name__)

@app.route("/")
def weather():
    return render_template("weather.html")

@app.route("/submit_city", methods=['POST'])
def submit_city():
    city = request.form.get('city')
    if city:

        return redirect(url_for('read_file', city=city))
    else:
        return "Please enter a city name."


@app.route("/api/v1/weather/<city>")
def read_file(city):
    api_key="0738d931fa0e1dc34c73580cf55e3244"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    responce = requests.get(url)
    i = responce.json()

    temperature =i["main"]["temp"]-273.15
    wind = i["wind"]["speed"]
    clouds = i["clouds"]["all"]
    date_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    x = np.array([date_timestamp])
    y_temperature = np.array([temperature])
    y_wind = np.array([wind])
    y_clouds = np.array([clouds])

    plt.plot(x, y_temperature, label='Temperature (Celsius)')
    plt.plot(x, y_wind, label='Wind Speed')
    plt.plot(x, y_clouds, label='Cloudiness')

    plt.xlabel('Date and Time')
    plt.ylabel('Values')
    plt.title(f'Weather Parameters in {city}')

    plt.savefig('weather_graph.png')
    plt.show()

    return {
         "city name":city,
         "Temperature": temperature,
         "Wind ": wind,
         "Cloudiness": clouds,
         "date":date_timestamp
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)


