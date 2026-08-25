from util import maybe_flip

# TODO(실기기 연동): gpiozero.Button(pin)

_state = {"pressed": False}


def generate() -> dict:
    _state["pressed"] = maybe_flip(_state["pressed"], flip_prob=0.05)
    return {"pressed": _state["pressed"]}
