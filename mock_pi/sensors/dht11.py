from util import random_walk

# TODO(실기기 연동): adafruit_dht 등 DHT11 전용 라이브러리로 온습도 읽기 (gpiozero 미지원)

_state = {"temperature_c": 24.0, "humidity_pct": 55.0}


def generate() -> dict:
    _state["temperature_c"] = random_walk(_state["temperature_c"], step=0.3, lo=15, hi=35)
    _state["humidity_pct"] = random_walk(_state["humidity_pct"], step=1.0, lo=30, hi=80)
    return {
        "temperature_c": round(_state["temperature_c"], 1),
        "humidity_pct": round(_state["humidity_pct"], 1),
    }
