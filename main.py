from prefect import task, flow
from prefect.artifacts import create_markdown_artifact
import httpx

@flow
def main():
    print("Hello, world!")
    

    httpx.get()

if __name__ == "__main__":
    main.serve("prefect-deployment-1")