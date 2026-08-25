import random


def random_walk(current: float, step: float, lo: float, hi: float) -> float:
    """이전 값에서 조금씩 움직이는 값 생성 — 매번 완전 랜덤보다 실제 센서와 비슷하다."""
    nxt = current + random.uniform(-step, step)
    return max(lo, min(hi, nxt))


def maybe_flip(current: bool, flip_prob: float) -> bool:
    """대부분 유지되다가 가끔 상태가 바뀌는 스위치/버튼류 흉내."""
    return (not current) if random.random() < flip_prob else current
