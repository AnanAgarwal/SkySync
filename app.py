from flask import Flask, render_template, request
import requests
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None

    if request.method == "POST":
        city = request.form.get("city")

        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo = requests.get(geo_url).json()

        if "results" in geo and len(geo["results"]) > 0:
            lat = geo["results"][0]["latitude"]
            lon = geo["results"][0]["longitude"]

            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&current_weather=true"
            data = requests.get(url).json()

            temps = data["hourly"]["temperature_2m"][:6]

            # 🤖 AI MODEL
            X = np.array([[i] for i in range(len(temps))])
            y = np.array(temps)

            model = LinearRegression()
            model.fit(X, y)

            next_temp = model.predict([[len(temps)]])[0]

            weather = {
                "city": city.upper(),
                "temp": data["current_weather"]["temperature"],
                "wind": data["current_weather"]["windspeed"],
                "code": data["current_weather"]["weathercode"],
                "hourly": temps,
                "prediction": round(next_temp, 2)
            }

    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)