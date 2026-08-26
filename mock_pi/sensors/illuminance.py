from util import random_walk

# TODO(실기기 연동): CDS 등 아날로그 모듈은 gpiozero.MCP3008 등 ADC로 읽어 lux로 환산,
# BH1750 등 I2C 모듈은 smbus2 등 전용 라이브러리로 lux를 직접 읽는다 (gpiozero 미지원)

_state = {"lux": 300.0}


def generate() -> dict:
    _state["lux"] = random_walk(_state["lux"], step=60, lo=0, hi=1500)
    return {"lux": round(_state["lux"], 1)}
