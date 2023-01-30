from collections import UserList
import pickle
import requests
from dataclasses import dataclass
from datetime import datetime


@dataclass()
class PowerHour:
    nok_kwh: float
    start_time: datetime
    end_time: datetime
    power_order: int = 0

    def __repr__(self):
        return repr(self.__dict__)


class PowerHourList(UserList):
    def __init__(self, data: list[PowerHour]):
        self.data: list[PowerHour] = data
        self.add_power_order()
    
    def __repr__(self):
        output = ""
        for index, powerhour in enumerate(self.data):
            output += f"{index}:\n{powerhour}\n"
        return output

    @classmethod
    def from_time_and_area(cls, dt: datetime, area):
        response = requests.get(
            f"https://www.hvakosterstrommen.no/api/v1/prices/{dt:%Y}/{dt:%m}-{dt:%d}_{area}.json")

        data: list = []  # this is the list data that can be accessed like a list
        for hour in response.json():
            data.append(PowerHour(
                hour["NOK_per_kWh"],
                datetime.fromisoformat(hour["time_start"]),
                datetime.fromisoformat(hour["time_end"]),
            ))
        return cls(data)

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'rb') as f:  # Overwrites any existing file.
            return cls(pickle.load(f))

    def save_to_file(self, filename):
        with open(filename, 'wb') as f:  # Overwrites any existing file.
            pickle.dump(self, f)

    def add_power_order(self):
        self.data.sort(key=lambda powerhour: powerhour.nok_kwh)

        for index, hour in enumerate(self.data):
            hour.power_order = index

        self.data.sort(key=lambda powerhour: powerhour.start_time)
    
    def get_powerhour_from_time(self, dt: datetime):
        for powerhour in self.data:
            if powerhour.start_time <= dt < powerhour.end_time:
                return powerhour 
        else:
            raise IndexError("Datetime outside range")
