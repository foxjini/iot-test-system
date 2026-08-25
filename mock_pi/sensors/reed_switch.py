from util import maybe_flip

# TODO(실기기 연동): gpiozero.Button(pin, pull_up=True) - 자석 근접 시 closed=True

_state = {"closed": False}


def generate() -> dict:
    _state["closed"] = maybe_flip(_state["closed"], flip_prob=0.05)
    return {"closed": _state["closed"]}
