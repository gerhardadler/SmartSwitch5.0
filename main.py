import logging
from env import ENDPOINT, ACCESS_ID, ACCESS_KEY, USERNAME, PASSWORD, DEVICE_ID

from tuya_iot import TuyaOpenAPI, TUYA_LOGGER

# Initialization of tuya openapi
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect(USERNAME, PASSWORD, "86", 'smartlife')

# # Uncomment the following lines to see logs.

TUYA_LOGGER.setLevel(logging.INFO)
TUYA_LOGGER.addHandler(logging.FileHandler('logs.log'))

result = openapi.get(f"/v1.0/iot-03/devices/{DEVICE_ID}/status")

status = result["result"][0]["value"]

commands = {'commands': [
    {
        "code": "switch_1",
        "value": not status
    }
]}
openapi.post(f'/v1.0/devices/{DEVICE_ID}/commands', commands)
