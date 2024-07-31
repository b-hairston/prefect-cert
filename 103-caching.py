from prefect import task, flow
from prefect.tasks import task_input_hash
from datetime import timedelta
import httpx


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def get_weather(lat: float, lon: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "wind_speed_10m",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch"
    }
    with httpx.Client() as client:
        response = client.get(url, params=params)
        response.raise_for_status() 

    return response.json()
@flow(name="weather_flow",log_prints=True)
def main():
    weather_data = get_weather(52.52, 13.41)
    print(weather_data)


if __name__ == "__main__":
    main.serve("caching-deployment")