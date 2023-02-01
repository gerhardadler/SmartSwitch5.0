import os
from datetime import datetime
import pytz
import tuya
from config import USE_POWER_COUNT
from power_calculation import PowerHourList
import mode

def update_economy():
    oslo_tz = pytz.timezone("Europe/Oslo") 
    now = datetime.now(oslo_tz)
    now_string = now.strftime("%Y-%m-%d")
    now_string_file = f"{now_string}.pickle"

    if not f"{now_string}.pickle" in os.listdir("powerdays"):
        powerhours = PowerHourList.from_time_and_area(now, "NO1")
        powerhours.save_to_file(f"powerdays/{now_string_file}")

    current_mode = mode.get_mode()

    if current_mode == "ECONOMY":
        if powerhours.get_powerhour_from_time(now).power_order < USE_POWER_COUNT:
            tuya.set_status(True)
        else:
            tuya.set_status(False)