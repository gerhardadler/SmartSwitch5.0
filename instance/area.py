from config import PROJECT_PATH, AREAS


def get_area() -> str:
    with open(f"{PROJECT_PATH}/instance/area.txt", "r") as f:
        return f.read()


def set_area(area: str) -> None:
    if area in AREAS:
        with open(f"{PROJECT_PATH}/instance/area.txt", "w") as f:
            f.write(area)
    else:
        raise KeyError(f"\"area\" must be in {AREAS}")