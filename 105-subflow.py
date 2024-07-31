from prefect import task, flow
from prefect.tasks import task_input_hash
from datetime import timedelta
import httpx


@flow(name="get-weather-data", log_prints=True)
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


@flow(name="get-max-stats", log_prints=True)
def get_max_stats(data: dict) -> str:
    run_deployment("max-wind-speed-deployment/deploy_flow")
    


@flow(name="main-flow", log_prints=True)
def main():
    weather_data = get_weather_data(52.52, 13.41)
    max_stats = get_max_stats(weather_data)

if __name__ == "__main__":
    flow.from_source(
        "https://github.com/b-hairston/prefect-cert.git",
        entrypoint="105-subflow.py:main",).deploy(name="subflow-deployment",
    work_pool_name="status-work-pool", build=False)
        

