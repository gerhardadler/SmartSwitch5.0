from flask import Flask, request
from config import PROJECT_PATH, MODES
import tuya
import os.path

from update_economy import update_economy

app = Flask(__name__)

@app.get("/get_mode")
def get_mode():
    with open(f"{PROJECT_PATH}/mode.txt", "r") as f:
        mode = f.read()
        return {"mode": mode}


@app.post("/set_mode")
def set_mode():
    # type: ignore , request is a global variable changed by Flask
    mode = request.get_json()["mode"]
    if mode in MODES:
        with open(f"{PROJECT_PATH}/mode.txt", "w") as f:
            f.write(mode)
        if mode == "ON":
            tuya.set_status(True)
        elif mode == "OFF":
            tuya.set_status(False)
        elif mode == "ECONOMY":
            update_economy.update_economy()
        return f"Updated mode to \"{mode}\"", 201
    else:
        return f"\"mode\" must be in {MODES}", 400
