import os
import requests
from datetime import date, timedelta

NASA_API_KEY = os.getenv("NASA_API_KEY")

def fetch_neos():
    today = date.today()
    tomorrow = today + timedelta(days=1)

    url = "https://api.nasa.gov/neo/rest/v1/feed"
    params = {
        "start_date": today.isoformat(),
        "end_date": tomorrow.isoformat(),
        "api_key": NASA_API_KEY
    }

    res = requests.get(url, params=params)
    data = res.json()

    neos = []

    for neo_date in data["near_earth_objects"]:
        for obj in data["near_earth_objects"][neo_date]:
            name = obj["name"]
            diameter = obj["estimated_diameter"]["meters"]["estimated_diameter_max"]
            speed = obj["close_approach_data"][0]["relative_velocity"]["kilometers_per_second"]
            miss_distance = obj["close_approach_data"][0]["miss_distance"]["lunar"]
            approach_date = obj["close_approach_data"][0]["close_approach_date"]

            neos.append({
                "name": name,
                "diameter": round(float(diameter)),
                "speed": round(float(speed), 2),
                "miss_distance": round(float(miss_distance), 1),
                "date": approach_date
            })

    return neos
