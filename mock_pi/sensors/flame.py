import random

from util import maybe_flip

# TODO(실기기 연동): 디지털 모듈은 gpiozero.DigitalInputDevice, 아날로그는 ADC 필요

_state = {"detected": False}


def generate() -> dict:
    _state["detected"] = maybe_flip(_state["detected"], flip_prob=0.03)
    intensity = (
        round(random.uniform(60, 100), 1) if _state["detected"] else round(random.uniform(0, 5), 1)
    )
    return {"detected": _state["detected"], "intensity": intensity}
