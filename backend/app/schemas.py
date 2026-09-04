from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, PlainSerializer

# 모든 시각 컬럼은 타임존 없는 UTC로 저장된다(app.models.utcnow). 응답에 'Z'를 붙여
# UTC임을 명시하지 않으면 브라우저의 new Date()가 '로컬 시각'으로 해석해서,
# 방금 도착한 센서값이 한국에서 "9시간 전"으로 표시된다.
UtcDatetime = Annotated[
    datetime,
    PlainSerializer(lambda v: v.replace(microsecond=0).isoformat() + "Z", return_type=str),
]

# ---------------- Catalog ----------------


class CatalogFieldOut(BaseModel):
    key: str
    label_ko: str
    type: str
    unit: str | None = None
    min: float | None = None
    max: float | None = None
    step: float | None = None
    options: list[str] | None = None


class CatalogComponentOut(BaseModel):
    type_key: str
    category: str
    label_ko: str
    note_ko: str = ""
    fields: list[CatalogFieldOut]


# ---------------- Device ----------------


class DeviceCreate(BaseModel):
    team_name: str = Field(min_length=1, max_length=100)


class DeviceOut(BaseModel):
    id: int
    team_name: str
    api_key: str
    is_online: bool
    last_seen_at: UtcDatetime | None


# ---------------- Component ----------------


class ComponentCreate(BaseModel):
    type_key: str
    label: str = Field(min_length=1, max_length=100)
    gpio_pin: str | None = None


class ComponentOut(BaseModel):
    id: int
    device_id: int
    type_key: str
    category: str
    label: str
    gpio_pin: str | None


# ---------------- Telemetry ----------------


class TelemetryItemIn(BaseModel):
    component_id: int
    value: dict[str, Any]


class TelemetryBatchIn(BaseModel):
    items: list[TelemetryItemIn]


class ReadingOut(BaseModel):
    id: int
    component_id: int
    value: dict[str, Any]
    recorded_at: UtcDatetime

    model_config = {"from_attributes": True}


# ---------------- Actuator commands ----------------


class CommandCreateIn(BaseModel):
    desired_state: dict[str, Any]


class CommandAckIn(BaseModel):
    actual_state: dict[str, Any]
    status: Literal["acked", "failed"] = "acked"


class CommandOut(BaseModel):
    id: int
    component_id: int
    desired_state: dict[str, Any]
    actual_state: dict[str, Any] | None
    status: str
    created_at: UtcDatetime
    acked_at: UtcDatetime | None

    model_config = {"from_attributes": True}


class HeartbeatOut(BaseModel):
    ok: bool = True
    server_time: UtcDatetime
