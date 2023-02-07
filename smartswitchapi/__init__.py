from flask import Flask, request
from flask_cors import CORS
from config import AREAS, PROJECT_PATH, MODES
import tuya
import instance.mode as mode
import instance.area as area

from update_economy import update_economy

app = Flask(__name__)
CORS(app)


@app.get("/get_mode")
def get_mode():
    try:
        mode.sync_mode()
    except tuya.TuyaException as e:
        return "Tuya exception", 504
    return {"mode": mode.get_mode()}


@app.post("/set_mode")
def set_mode():
    # type: ignore , request is a global variable changed by Flask
    mode_input = request.get_json()["mode"]
    if mode_input in MODES:
        try:
            if mode_input == "ON":
                tuya.set_status(True)
            elif mode_input == "OFF":
                tuya.set_status(False)
            elif mode_input == "ECONOMY":
                update_economy()
        except tuya.TuyaException as e:
            return "Tuya exception", 504
        else:
            mode.set_mode(mode_input)
        return f"Updated mode to \"{mode_input}\"", 201
    else:
        return f"\"mode\" must be in {MODES}", 400


@app.get("/get_area")
def get_area():
    return {"area": area.get_area()}


@app.post("/set_area")
def set_area():
    # type: ignore , request is a global variable changed by Flask
    area_input = request.get_json()["area"]
    if area_input in AREAS:
        area.set_area(area_input)
        update_economy()
        return f"Updated area to \"{area_input}\"", 201
    else:
        return f"\"area\" must be in {AREAS}", 400