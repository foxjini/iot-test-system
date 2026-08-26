import random

from util import maybe_flip

# TODO(실기기 연동): 카메라 + QR 인식 라이브러리로 실제 인식 (antigravity-plugin/skills/vision-trigger 참고)

_SAMPLE_PAYLOADS = ["TEAM-DOOR-OPEN", "TEAM-CHECKIN-01", "TEAM-ITEM-42"]
_state = {"detected": False, "payload": ""}


def generate() -> dict:
    was_detected = _state["detected"]
    _state["detected"] = maybe_flip(was_detected, flip_prob=0.05)
    if _state["detected"] and not was_detected:
        _state["payload"] = random.choice(_SAMPLE_PAYLOADS)
    elif not _state["detected"]:
        _state["payload"] = ""
    return {"detected": _state["detected"], "payload": _state["payload"]}
