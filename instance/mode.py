from config import PROJECT_PATH, MODES
import tuya


def get_mode() -> str:
    with open(f"{PROJECT_PATH}/instance/mode.txt", "r") as f:
        return f.read()


def set_mode(mode: str) -> None:
    if mode in MODES:
        with open(f"{PROJECT_PATH}/instance/mode.txt", "w") as f:
            f.write(mode)
    else:
        raise KeyError(f"\"mode\" must be in {MODES}")


def sync_mode():
    mode = get_mode()
    if mode == "ECONOMY":
        return
    
    if tuya.get_status() and mode != "ON":
        set_mode("ON")
    elif not tuya.get_status() and mode != "OFF":
        set_mode("OFF")
