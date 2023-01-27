from flask import Flask, request
from config import MODES
import tuya

app = Flask(__name__)

with open("mode.txt", "r") as f:
    var = f.read()


@app.get("/get_mode")
def get_mode():
    with open("mode.txt", "r") as f:
        mode = f.read()
        return {"mode": mode}


@app.post("/set_mode")
def set_mode():
    # type: ignore , request is a global variable changed by Flask
    mode = request.get_json()["mode"]
    if mode in MODES:
        with open("mode.txt", "w") as f:
            f.write(mode)
        return f"Updated mode to \"{mode}\"", 201
    else:
        return f"\"mode\" must be in {MODES}", 400


@app.get("/get_switch_status")
def get_switch_status():
    return {"status": tuya.get_status()}


@app.post("/set_switch_status")
def set_switch_status():
    # type: ignore , request is a global variable changed by Flask
    status = request.get_json()["status"]
    if type(status) == bool:
        tuya.set_status(status)
        return f"Updated status to \"{status}\"", 201
    else:
        return f"\"status\" must be bool", 400
