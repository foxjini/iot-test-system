from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

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
    last_seen_at: datetime | None


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
    recorded_at: datetime

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
    created_at: datetime
    acked_at: datetime | None

    model_config = {"from_attributes": True}


class HeartbeatOut(BaseModel):
    ok: bool = True
    server_time: datetime
