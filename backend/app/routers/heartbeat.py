from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_device_by_key
from app.database import get_db
from app.models import Device, utcnow
from app.schemas import HeartbeatOut

router = APIRouter(prefix="/api/devices/{device_id}", tags=["heartbeat"])


@router.post("/heartbeat", response_model=HeartbeatOut)
def heartbeat(
    device_id: int,
    device: Device = Depends(get_device_by_key),
    db: Session = Depends(get_db),
):
    device.last_seen_at = utcnow()
    db.commit()
    return HeartbeatOut(server_time=utcnow())
