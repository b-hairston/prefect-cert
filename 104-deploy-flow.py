from prefect import task, flow
from prefect.tasks import task_input_hash
from datetime import timedelta
import httpx

@task(name="get_max_wind_task",cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def get_max_wind_speed(lat: float, lon: float) -> dict:
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

@flow(name="deploy_flow",log_prints=True)
def main():
    max_wind_speed = get_max_wind_speed(52.52, 13.41)

if __name__ == "__main__":
    # flow.from_source(
    #     "https://github.com/b-hairston/prefect-cert.git",
    #     entrypoint="104-deploy-flow.py:main",).deploy(name="max-wind-speed-deployment",
    # work_pool_name="status-work-pool", build=False)

    main.deploy(name="wind-speed-docker-deployment", 
        work_pool_name="status-docker-pool", 
        image="bhairston/personal-repo:latest")




