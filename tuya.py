import logging
from config import ENDPOINT, ACCESS_ID, ACCESS_KEY, USERNAME, PASSWORD, DEVICE_ID

from tuya_iot import TuyaOpenAPI, TUYA_LOGGER

# Initialization of tuya openapi
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect(USERNAME, PASSWORD, "86", 'smartlife')

TUYA_LOGGER.setLevel(logging.INFO)
TUYA_LOGGER.addHandler(logging.FileHandler('logs.log'))

def get_state():
    result = openapi.get(f"/v1.0/iot-03/devices/{DEVICE_ID}/state")
    state = result["result"][0]["value"]
    return state

def set_state(new_state):
    command = {'commands': [
        {
            "code": "switch_1",
            "value": new_state
        }
    ]}
    openapi.post(f'/v1.0/devices/{DEVICE_ID}/commands', command)
