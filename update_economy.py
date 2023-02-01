import os
from datetime import datetime
import pytz
import tuya
from config import USE_POWER_COUNT, PROJECT_PATH
from power_calculation import PowerHourList
import instance.mode as mode
import instance.area as area


def update_economy():
    if mode.get_mode() != "ECONOMY":
        return

    current_area = area.get_area()
    oslo_tz = pytz.timezone("Europe/Oslo") 
    now = datetime.now(oslo_tz)
    now_string = now.strftime("%Y-%m-%d")
    powerhours_file = f"{current_area}-{now_string}.pickle"

    if not powerhours_file in os.listdir(f"{PROJECT_PATH}/powerdays"):
        powerhours = PowerHourList.from_time_and_area(now, current_area)
        powerhours.save_to_file(f"{PROJECT_PATH}/powerdays/{powerhours_file}")
    else:
        powerhours = PowerHourList.load_from_file(f"{PROJECT_PATH}/powerdays/{powerhours_file}")
    
    if powerhours.get_powerhour_from_time(now).power_order < USE_POWER_COUNT:
        tuya.set_status(True)
    else:
        tuya.set_status(False)