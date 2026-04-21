from prometheus_client import start_http_server, Counter
import time
import random

from logger import LOGGER  # bruger din lærers logger

REQUEST_COUNT = Counter('app_requests_total', 'Total requests')

def run_app():
    while True:
        REQUEST_COUNT.inc()
        LOGGER.info("Request handled", extra={"status": "ok"})
        time.sleep(random.randint(1, 3))

if __name__ == "__main__":
    start_http_server(8000)
    LOGGER.info("App started")
    run_app()