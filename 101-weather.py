from prefect import flow
import httpx
import json
@flow(name="weather_flow",log_prints=True)
def main():

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        "hourly": "wind_speed_10m",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch"
    }
    with httpx.Client() as client:
        response = client.get(url, params=params)
        response.raise_for_status()

    print(response.json())  
    response = response.json()
    max_wind_speed = max(response['hourly']['wind_speed_10m'])

    print(f"Max wind speed was {max_wind_speed} mph")

    return max_wind_speed

if __name__ == "__main__":
    main.serve("weather-deployment")