from __future__ import annotations

import datetime
import secrets

from sqlalchemy import JSON, DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _new_api_key() -> str:
    return secrets.token_hex(16)


class Device(Base):
    """팀의 라즈베리파이 5 한 대를 나타낸다.

    이 테스트 시스템은 팀마다 독립된 PC에 설치되므로 보통 인스턴스당 device가
    1개뿐이지만, 실제 다중팀 운영 백엔드와 API 계약(경로에 device_id 포함)을
    동일하게 유지하기 위해 테이블/경로 구조는 그대로 둔다.
    """

    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(100))
    api_key: Mapped[str] = mapped_column(String(64), unique=True, default=_new_api_key)
    last_seen_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    components: Mapped[list["Component"]] = relationship(
        back_populates="device", cascade="all, delete-orphan"
    )


class Component(Base):
    """디바이스(팀)가 실제로 사용하는 센서/액추에이터 1개.

    15종 카탈로그(app.catalog) 중 팀이 선택한 항목만 여기 등록되고,
    Mock/실제 라즈베리파이와 프론트엔드 대시보드 모두 이 목록을 기준으로 동작한다.
    """

    __tablename__ = "components"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"))
    type_key: Mapped[str] = mapped_column(String(50))
    label: Mapped[str] = mapped_column(String(100))
    gpio_pin: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    device: Mapped["Device"] = relationship(back_populates="components")
    readings: Mapped[list["SensorReading"]] = relationship(
        back_populates="component", cascade="all, delete-orphan"
    )
    commands: Mapped[list["ActuatorCommand"]] = relationship(
        back_populates="component", cascade="all, delete-orphan"
    )


class SensorReading(Base):
    __tablename__ = "sensor_readings"
    __table_args__ = (Index("ix_sensor_readings_component_recorded", "component_id", "recorded_at"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    component_id: Mapped[int] = mapped_column(ForeignKey("components.id"))
    value: Mapped[dict] = mapped_column(JSON)
    recorded_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    component: Mapped["Component"] = relationship(back_populates="readings")


class ActuatorCommand(Base):
    __tablename__ = "actuator_commands"
    __table_args__ = (Index("ix_actuator_commands_component_status", "component_id", "status"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    component_id: Mapped[int] = mapped_column(ForeignKey("components.id"))
    desired_state: Mapped[dict] = mapped_column(JSON)
    actual_state: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending / acked / failed
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    acked_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    component: Mapped["Component"] = relationship(back_populates="commands")
