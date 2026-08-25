from util import random_walk

# TODO(실기기 연동): gpiozero.DistanceSensor(echo=, trigger=).distance * 100

_state = {"distance_cm": 100.0}


def generate() -> dict:
    _state["distance_cm"] = random_walk(_state["distance_cm"], step=20, lo=2, hi=400)
    return {"distance_cm": round(_state["distance_cm"], 1)}
