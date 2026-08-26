"""경량 YOLO(nano) 모델로 객체를 인식하는 예시 (sensors/object_detector.py로 사용).

필요 설치: pip install ultralytics opencv-python
라즈베리파이 5는 GPU가 없어 CPU로만 추론한다 — yolo11n(nano)처럼 가장 가벼운
모델을 쓰고, 그래도 느리면 skills/vision-trigger/references/options.md의
백엔드 오프로드 방식(이 스크립트를 백엔드 PC에서 돌리고 push_telemetry만 원격에서
호출)을 검토한다.
"""

import cv2
from ultralytics import YOLO

_model = YOLO("yolo11n.pt")
_cap = cv2.VideoCapture(0)


def generate() -> dict | None:
    ok, frame = _cap.read()
    if not ok:
        return None

    results = _model(frame, verbose=False)[0]
    if len(results.boxes) == 0:
        return {"label": "", "confidence": 0.0, "count": 0}

    best = results.boxes[results.boxes.conf.argmax()]
    label = results.names[int(best.cls[0])]
    return {
        "label": label,
        "confidence": round(float(best.conf[0]), 2),
        "count": len(results.boxes),
    }
