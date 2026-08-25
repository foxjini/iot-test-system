from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.catalog import get_component_type
from app.database import get_db
from app.models import Component, Device
from app.schemas import ComponentCreate, ComponentOut

router = APIRouter(prefix="/api/devices/{device_id}/components", tags=["components"])


def _to_out(c: Component) -> ComponentOut:
    ctype = get_component_type(c.type_key)
    return ComponentOut(
        id=c.id,
        device_id=c.device_id,
        type_key=c.type_key,
        category=ctype.category.value if ctype else "unknown",
        label=c.label,
        gpio_pin=c.gpio_pin,
    )


def _get_device_or_404(device_id: int, db: Session) -> Device:
    device = db.get(Device, device_id)
    if device is None:
        raise HTTPException(404, "디바이스를 찾을 수 없습니다.")
    return device


@router.get("", response_model=list[ComponentOut])
def list_components(device_id: int, db: Session = Depends(get_db)):
    _get_device_or_404(device_id, db)
    rows = (
        db.query(Component)
        .filter(Component.device_id == device_id)
        .order_by(Component.id)
        .all()
    )
    return [_to_out(c) for c in rows]


@router.post("", response_model=ComponentOut, status_code=201)
def create_component(device_id: int, body: ComponentCreate, db: Session = Depends(get_db)):
    _get_device_or_404(device_id, db)
    if get_component_type(body.type_key) is None:
        raise HTTPException(400, f"알 수 없는 컴포넌트 타입입니다: {body.type_key}")
    component = Component(
        device_id=device_id, type_key=body.type_key, label=body.label, gpio_pin=body.gpio_pin
    )
    db.add(component)
    db.commit()
    db.refresh(component)
    return _to_out(component)


@router.delete("/{component_id}", status_code=204)
def delete_component(device_id: int, component_id: int, db: Session = Depends(get_db)):
    component = db.get(Component, component_id)
    if component is None or component.device_id != device_id:
        raise HTTPException(404, "컴포넌트를 찾을 수 없습니다.")
    db.delete(component)
    db.commit()
