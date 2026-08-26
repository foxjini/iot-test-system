import random

from util import maybe_flip

# TODO(실기기 연동): 카메라 + YOLO/mediapipe 등으로 실제 객체 인식 (antigravity-plugin/skills/vision-trigger 참고)

_SAMPLE_LABELS = ["person", "bottle", "chair"]
_state = {"detected": False, "label": "", "confidence": 0.0, "count": 0}


def generate() -> dict:
    was_detected = _state["detected"]
    _state["detected"] = maybe_flip(was_detected, flip_prob=0.05)
    if _state["detected"] and not was_detected:
        _state["label"] = random.choice(_SAMPLE_LABELS)
        _state["confidence"] = round(random.uniform(0.5, 0.99), 2)
        _state["count"] = random.randint(1, 3)
    elif not _state["detected"]:
        _state["label"] = ""
        _state["confidence"] = 0.0
        _state["count"] = 0
    return {"label": _state["label"], "confidence": _state["confidence"], "count": _state["count"]}
