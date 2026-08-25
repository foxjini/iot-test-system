from util import random_walk

# TODO(실기기 연동): 압력센서는 아날로그 출력 → gpiozero.MCP3008 등 ADC로 읽은 뒤 환산

_state = {"value": 50.0}


def generate() -> dict:
    _state["value"] = random_walk(_state["value"], step=15, lo=0, hi=500)
    return {"value": round(_state["value"], 1)}
