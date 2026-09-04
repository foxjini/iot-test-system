from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_device_by_key
from app.catalog import get_component_type, validate_payload
from app.database import get_db
from app.models import ActuatorCommand, Component, Device, utcnow
from app.schemas import CommandAckIn, CommandCreateIn, CommandOut

router = APIRouter(prefix="/api/devices/{device_id}", tags=["commands"])


def _get_component_or_404(device_id: int, component_id: int, db: Session) -> Component:
    component = db.get(Component, component_id)
    if component is None or component.device_id != device_id:
        raise HTTPException(404, "컴포넌트를 찾을 수 없습니다.")
    return component


@router.post("/components/{component_id}/command", response_model=CommandOut, status_code=201)
def create_command(
    device_id: int, component_id: int, body: CommandCreateIn, db: Session = Depends(get_db)
):
    """프론트엔드 대시보드가 액추에이터 제어 명령을 등록한다. (인증 불필요, 교내망 전용)"""
    component = _get_component_or_404(device_id, component_id, db)
    ctype = get_component_type(component.type_key)
    if ctype is None or ctype.category.value != "actuator":
        raise HTTPException(400, f"액추에이터 타입이 아닙니다: {component.type_key}")
    validate_payload(component.type_key, body.desired_state)
    command = ActuatorCommand(component_id=component_id, desired_state=body.desired_state)
    db.add(command)
    db.commit()
    db.refresh(command)
    return command


@router.get("/components/{component_id}/command/latest", response_model=CommandOut | None)
def latest_command(device_id: int, component_id: int, db: Session = Depends(get_db)):
    """대시보드가 액추에이터의 현재 명령(원하는 상태/실제 상태)을 보여주기 위해 조회."""
    _get_component_or_404(device_id, component_id, db)
    return (
        db.query(ActuatorCommand)
        .filter(ActuatorCommand.component_id == component_id)
        # created_at은 초 단위다. 슬라이더처럼 1초 안에 여러 번 조작하면
        # id 없이는 가장 최근 명령이 아닌 엉뚱한 명령이 반환된다.
        .order_by(ActuatorCommand.created_at.desc(), ActuatorCommand.id.desc())
        .first()
    )


@router.get("/commands/pending", response_model=list[CommandOut])
def list_pending_commands(
    device_id: int, device: Device = Depends(get_device_by_key), db: Session = Depends(get_db)
):
    """Mock/실제 라즈베리파이가 실행할 명령을 폴링한다. (X-Device-Key 인증 필요)"""
    return (
        db.query(ActuatorCommand)
        .join(Component)
        .filter(Component.device_id == device_id, ActuatorCommand.status == "pending")
        .order_by(ActuatorCommand.created_at, ActuatorCommand.id)
        .all()
    )


@router.post("/commands/{command_id}/ack", response_model=CommandOut)
def ack_command(
    device_id: int,
    command_id: int,
    body: CommandAckIn,
    device: Device = Depends(get_device_by_key),
    db: Session = Depends(get_db),
):
    """Mock/실제 라즈베리파이가 명령 실행 결과를 보고한다. (X-Device-Key 인증 필요)"""
    command = db.get(ActuatorCommand, command_id)
    if command is None or command.component.device_id != device_id:
        raise HTTPException(404, "명령을 찾을 수 없습니다.")
    command.actual_state = body.actual_state
    command.status = body.status
    command.acked_at = utcnow()
    db.commit()
    db.refresh(command)
    return command
