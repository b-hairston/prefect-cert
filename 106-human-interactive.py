from prefect import task, flow, pause_flow_run
from prefect.tasks import task_input_hash
from datetime import timedelta
import httpx

@task(name="get-weather-data", log_prints=True)
def get_weather_data(lat: float, lon: float) -> dict:
    

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

    weather_data = response.json()
    return weather_data

@flow(name="main-flow", log_prints=True)
def main():
    weather_data = get_weather_data(52.52, 13.41)
    pause_flow_run(wait_for_input=string_input)
    print(f"Continuing flow, thank you {string_input}")


if __name__ == "__main__":
    main.serve("human-interactive-deployment")

