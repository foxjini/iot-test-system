import random

# TODO(실기기 연동): 매트릭스 키패드 GPIO 스캔 라이브러리로 실제 키 입력 감지

_KEYS = list("0123456789*#")


def generate() -> dict | None:
    """실제 키패드처럼 눌렸을 때만 값을 보낸다 (대부분의 주기엔 입력 없음)."""
    if random.random() < 0.9:
        return None
    return {"key": random.choice(_KEYS), "event": "press"}
