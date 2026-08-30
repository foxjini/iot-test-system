from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Device, utcnow
from app.schemas import DeviceCreate, DeviceOut

router = APIRouter(prefix="/api/devices", tags=["devices"])


def _to_out(d: Device) -> DeviceOut:
    online = d.last_seen_at is not None and (
        utcnow() - d.last_seen_at < timedelta(seconds=settings.heartbeat_timeout_sec)
    )
    return DeviceOut(
        id=d.id,
        team_name=d.team_name,
        api_key=d.api_key,
        is_online=online,
        last_seen_at=d.last_seen_at,
    )


@router.get("", response_model=list[DeviceOut])
def list_devices(db: Session = Depends(get_db)):
    rows = db.query(Device).order_by(Device.id).all()
    return [_to_out(d) for d in rows]


@router.post("", response_model=DeviceOut, status_code=201)
def create_device(body: DeviceCreate, db: Session = Depends(get_db)):
    device = Device(team_name=body.team_name)
    db.add(device)
    db.commit()
    db.refresh(device)
    return _to_out(device)


@router.get("/{device_id}", response_model=DeviceOut)
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = db.get(Device, device_id)
    if device is None:
        raise HTTPException(404, "디바이스를 찾을 수 없습니다.")
    return _to_out(device)


@router.delete("/{device_id}", status_code=204)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    device = db.get(Device, device_id)
    if device is None:
        raise HTTPException(404, "디바이스를 찾을 수 없습니다.")
    db.delete(device)
    db.commit()
