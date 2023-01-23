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


# class PowerHourList:


def get_hvakosterstrommen(power_datetime: datetime, area) -> list[PowerHour]:
    response = requests.get(
        f"https://www.hvakosterstrommen.no/api/v1/prices/{power_datetime:%Y}/{power_datetime:%m}-{power_datetime:%d}_{area}.json")
    output: list = []
    for hour in response.json():
        output.append(PowerHour(
            hour["NOK_per_kWh"],
            datetime.fromisoformat(hour["time_start"]),
            datetime.fromisoformat(hour["time_end"]),
        ))
    return output


def add_use_power(powerhours: list[PowerHour]) -> list[PowerHour]:
    use_power_count: int = int(len(powerhours) * config.USE_POWER_PERCENTAGE)
    price_sorted_hours: list[PowerHour] = sorted(
        copy.deepcopy(powerhours), key=lambda powerhour: powerhour.nok_kwh)

    for hour in price_sorted_hours[:use_power_count]:
        hour.use_power = True

    time_sorted_hours: list[PowerHour] = sorted(
        price_sorted_hours, key=lambda powerhour: powerhour.time_start)
    return time_sorted_hours


powerhours = get_hvakosterstrommen(datetime.now(), "NO1")
powerhours = add_use_power(powerhours)
print(powerhours)
