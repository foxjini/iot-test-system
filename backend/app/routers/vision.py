"""선택 기능: 비전 인식 오프로드.

라즈베리파이 대신 백엔드(Windows PC)에서 QR 인식을 수행하고 싶은 팀만 쓰는
엔드포인트다. 결과를 자동으로 텔레메트리에 기록하지 않는다 — 호출한 쪽(라즈베리파이
코드)이 필요하면 평소처럼 POST /api/devices/{device_id}/telemetry로 직접 올린다.

opencv-python은 기본 requirements.txt에 포함하지 않는다(설치 용량, 비전 기능을
쓰지 않는 팀에게 불필요한 의존성이라). backend/requirements-vision.txt로 별도 설치한다.
"""

import base64
import binascii

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.auth import get_device_by_any_key
from app.models import Device

router = APIRouter(prefix="/api/vision", tags=["vision"])


class QrDetectIn(BaseModel):
    image_base64: str


class QrDetectOut(BaseModel):
    detected: bool
    payload: str = ""


@router.post("/qr", response_model=QrDetectOut)
def detect_qr(
    body: QrDetectIn, device: Device = Depends(get_device_by_any_key)
) -> QrDetectOut:
    try:
        import cv2
        import numpy as np
    except ImportError as exc:
        raise ValueError(
            "이 백엔드에는 비전 기능이 설치되어 있지 않습니다. "
            "backend/requirements-vision.txt를 설치한 뒤 다시 실행하세요."
        ) from exc

    try:
        raw = base64.b64decode(body.image_base64, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError("image_base64 값을 디코딩할 수 없습니다.") from exc

    frame = cv2.imdecode(np.frombuffer(raw, dtype=np.uint8), cv2.IMREAD_COLOR)
    if frame is None:
        raise ValueError("이미지를 디코딩할 수 없습니다 (JPEG/PNG 형식인지 확인하세요).")

    payload, _points, _straight_qr = cv2.QRCodeDetector().detectAndDecode(frame)
    return QrDetectOut(detected=bool(payload), payload=payload or "")
