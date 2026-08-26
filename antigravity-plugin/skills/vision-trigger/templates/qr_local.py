"""라즈베리파이에서 직접 QR 코드를 인식하는 예시 (sensors/qr_scanner.py로 사용).

필요 설치: pip install opencv-python
카메라: USB 웹캠은 보통 바로 인식된다. Pi Camera Module(CSI)은 라즈베리파이 OS
설정에 따라 cv2.VideoCapture(0)으로 안 열리면 picamera2로 프레임을 받아
numpy 배열로 넘기는 방식으로 바꾼다.
"""

import cv2

_detector = cv2.QRCodeDetector()
_cap = cv2.VideoCapture(0)


def generate() -> dict | None:
    ok, frame = _cap.read()
    if not ok:
        return None
    payload, _points, _straight_qr = _detector.detectAndDecode(frame)
    return {"detected": bool(payload), "payload": payload}
