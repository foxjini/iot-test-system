from fastapi import Depends, Header, HTTPException, Path
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Device


def get_device_by_key(
    device_id: int = Path(...),
    x_device_key: str = Header(..., alias="X-Device-Key"),
    db: Session = Depends(get_db),
) -> Device:
    """라즈베리파이(Mock 또는 실제)가 자기 device_id와 API Key로 인증하는 의존성.

    프론트엔드 대시보드가 호출하는 엔드포인트(디바이스/컴포넌트 관리, 명령 등록,
    이력 조회)는 교내망 내부용 도구라 별도 인증을 요구하지 않는다.
    """
    device = db.get(Device, device_id)
    if device is None or device.api_key != x_device_key:
        raise HTTPException(status_code=401, detail="유효하지 않은 device_id 또는 API Key입니다.")
    return device


def get_device_by_any_key(
    x_device_key: str = Header(..., alias="X-Device-Key"),
    db: Session = Depends(get_db),
) -> Device:
    """URL에 device_id가 없는 엔드포인트(비전 오프로드 등)용 인증 의존성.

    특정 device_id에 묶이지 않고, 등록된 디바이스 중 하나의 유효한 API Key인지만 확인한다.
    """
    device = db.query(Device).filter(Device.api_key == x_device_key).first()
    if device is None:
        raise HTTPException(status_code=401, detail="유효하지 않은 API Key입니다.")
    return device
