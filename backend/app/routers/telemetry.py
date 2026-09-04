from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import get_device_by_key
from app.catalog import get_component_type, validate_payload
from app.database import get_db
from app.models import Component, Device, SensorReading, utcnow
from app.schemas import ReadingOut, TelemetryBatchIn

router = APIRouter(prefix="/api/devices/{device_id}", tags=["telemetry"])


@router.post("/telemetry", status_code=204)
def push_telemetry(
    device_id: int,
    body: TelemetryBatchIn,
    device: Device = Depends(get_device_by_key),
    db: Session = Depends(get_db),
):
    """Mock/실제 라즈베리파이가 센서값을 일괄 업로드한다. (X-Device-Key 인증 필요)"""
    components = {
        c.id: c for c in db.query(Component).filter(Component.device_id == device_id).all()
    }
    for item in body.items:
        component = components.get(item.component_id)
        if component is None:
            raise HTTPException(400, f"등록되지 않은 component_id입니다: {item.component_id}")
        ctype = get_component_type(component.type_key)
        if ctype is None or ctype.category.value != "sensor":
            raise HTTPException(400, f"센서 타입이 아닙니다: {component.type_key}")
        validate_payload(component.type_key, item.value)
        db.add(SensorReading(component_id=component.id, value=item.value))
    device.last_seen_at = utcnow()
    db.commit()


@router.get("/components/{component_id}/readings", response_model=list[ReadingOut])
def list_readings(
    device_id: int,
    component_id: int,
    limit: int = Query(default=50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    component = db.get(Component, component_id)
    if component is None or component.device_id != device_id:
        raise HTTPException(404, "컴포넌트를 찾을 수 없습니다.")
    rows = (
        db.query(SensorReading)
        .filter(SensorReading.component_id == component_id)
        # recorded_at은 초 단위라 1~2초 폴링에서 값이 자주 겹친다.
        # id를 함께 정렬하지 않으면 같은 초에 들어온 값들의 순서가 보장되지 않는다.
        .order_by(SensorReading.recorded_at.desc(), SensorReading.id.desc())
        .limit(limit)
        .all()
    )
    return list(reversed(rows))
