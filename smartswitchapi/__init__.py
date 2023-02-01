from flask import Flask, request
from config import PROJECT_PATH, MODES
import tuya
import mode

from update_economy import update_economy

app = Flask(__name__)

@app.get("/get_mode")
def get_mode():
    mode.sync_mode()
    return {"mode": mode.get_mode()}


@app.post("/set_mode")
def set_mode():
    # type: ignore , request is a global variable changed by Flask
    mode_input = request.get_json()["mode"]
    if mode_input in MODES:
        mode.set_mode(mode_input)
        if mode_input == "ON":
            tuya.set_status(True)
        elif mode_input == "OFF":
            tuya.set_status(False)
        elif mode_input == "ECONOMY":
            update_economy.update_economy()
        return f"Updated mode to \"{mode_input}\"", 201
    else:
        return f"\"mode\" must be in {MODES}", 400
