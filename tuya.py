import logging
import time
from tuya_iot import TuyaOpenAPI, TUYA_LOGGER
from config import PROJECT_PATH, ENDPOINT, ACCESS_ID, ACCESS_KEY, USERNAME, PASSWORD, DEVICE_ID

# Initialization of tuya openapi
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect(USERNAME, PASSWORD, "86", 'smartlife')

TUYA_LOGGER.setLevel(logging.WARNING)
TUYA_LOGGER.addHandler(logging.FileHandler(f"{PROJECT_PATH}/logs/tuya.log"))


class TuyaException(Exception):
    pass


def get_status(retry=5, delay=0.2):
    result = openapi.get(f"/v1.0/iot-03/devices/{DEVICE_ID}/status")
    TUYA_LOGGER.debug(result)
    attempts = 0
    while True:
        try:
            status = result["result"][0]["value"]
        except KeyError:
            if attempts >= retry:
                raise TuyaException
            else:
                attempts += 1
                time.sleep(delay)
        else:
            return status


def set_status(new_status, retry=5, delay=0.2):
    command = {"commands": [
        {
            "code": "switch_1",
            "value": new_status
        }
    ]}
    attempts = 0
    while True:
        result = openapi.post(f"/v1.0/devices/{DEVICE_ID}/commands", command)
        if result["success"]:
            return
        else:
            if attempts >= retry:
                raise TuyaException
            else:
                attempts += 1
                time.sleep(delay)