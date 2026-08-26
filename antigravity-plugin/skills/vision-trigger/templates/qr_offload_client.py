"""라즈베리파이는 프레임만 캡처해서 백엔드(Windows PC)로 보내고, 인식은
백엔드가 대신 하는 예시 (sensors/qr_scanner.py로 사용).

필요 설치(라즈베리파이): pip install opencv-python requests
필요 설치(백엔드): backend/requirements-vision.txt (skills/vision-trigger/references/options.md 참고)

client는 skills/backend-api-client/templates/client.py의 BackendClient를
그대로 재사용한다 — 이 함수는 그 base_url/api_key를 그대로 물려받아 쓴다고 가정한다.
"""

import base64

import cv2
import requests

_cap = cv2.VideoCapture(0)


def generate(base_url: str, api_key: str, timeout: float = 5.0) -> dict | None:
    ok, frame = _cap.read()
    if not ok:
        return None

    ok, buf = cv2.imencode(".jpg", frame)
    if not ok:
        return None
    image_base64 = base64.b64encode(buf.tobytes()).decode("ascii")

    resp = requests.post(
        f"{base_url.rstrip('/')}/api/vision/qr",
        json={"image_base64": image_base64},
        headers={"X-Device-Key": api_key},
        timeout=timeout,
    )
    resp.raise_for_status()
    result = resp.json()
    return {"detected": result["detected"], "payload": result.get("payload") or ""}
