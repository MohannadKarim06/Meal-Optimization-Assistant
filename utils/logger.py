import logging 
from datetime import datetime


logging.basicConfig(
    filename="/app/data/logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_event(event_type: str, details: str):

    message = f"{event_type}: {details}"
    logging.info(message)
    print(message)
