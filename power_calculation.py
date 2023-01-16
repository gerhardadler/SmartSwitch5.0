import requests
from datetime import datetime


def get_hvakosterstrommen(power_datetime, area):
    response = requests.get(
        f"https://www.hvakosterstrommen.no/api/v1/prices/{power_datetime:%Y}/{power_datetime:%m}-{power_datetime:%d}_{area}.json")
    return response.json()


get_hvakosterstrommen(datetime.now(), "NO1")