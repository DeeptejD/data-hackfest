import os
import requests
from datetime import date, timedelta

NASA_API_KEY = os.getenv("NASA_API_KEY")

def fetch_neos(start_date=None, end_date=None):
    if start_date is None:
        start_date = date.today()
    if end_date is None:
        end_date = start_date + timedelta(days=1)
    
    # Convert string dates to date objects if needed
    if isinstance(start_date, str):
        start_date = date.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = date.fromisoformat(end_date)

    url = "https://api.nasa.gov/neo/rest/v1/feed"
    params = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "api_key": NASA_API_KEY
    }

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()  # Raise an exception for bad status codes
        data = res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching NEO data: {e}")
        return []
    except KeyError as e:
        print(f"Error parsing NEO data: {e}")
        return []

    neos = []

    for neo_date in data.get("near_earth_objects", {}):
        for obj in data["near_earth_objects"][neo_date]:
            try:
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
            except (KeyError, IndexError, ValueError) as e:
                print(f"Error processing NEO object: {e}")
                continue

    return neos
