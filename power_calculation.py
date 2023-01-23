from collections import UserList
import copy
import requests
from dataclasses import dataclass
from datetime import datetime
import config



@dataclass()
class PowerHour:
    nok_kwh: float
    time_start: datetime
    time_end: datetime
    use_power: bool = False

    def __repr__(self):
        return f"{self.nok_kwh} {self.use_power}"


class PowerHourList(UserList):
    def __init__(self, power_datetime: datetime, area):
        response = requests.get(
            f"https://www.hvakosterstrommen.no/api/v1/prices/{power_datetime:%Y}/{power_datetime:%m}-{power_datetime:%d}_{area}.json")
        
        self.data: list = [] # this is the list data that can be accessed like a list
        for hour in response.json():
            self.data.append(PowerHour(
                hour["NOK_per_kWh"],
                datetime.fromisoformat(hour["time_start"]),
                datetime.fromisoformat(hour["time_end"]),
            ))


    def add_use_power(self):
        use_power_count: int = int(len(self.data) * config.USE_POWER_PERCENTAGE)
        self.data.sort(key=lambda powerhour: powerhour.nok_kwh)

        for hour in self.data[:use_power_count]:
            hour.use_power = True

        self.data.sort(key=lambda powerhour: powerhour.time_start)


powerhours = PowerHourList(datetime.now(), "NO1")
powerhours.add_use_power()
print(powerhours)
