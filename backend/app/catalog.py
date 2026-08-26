"""15종 센서/액추에이터 타입 카탈로그.

백엔드 검증(app.routers), 프론트엔드 동적 UI(/api/catalog/components 응답),
Mock 라즈베리파이 클라이언트(mock_pi)가 모두 이 정의를 기준으로 삼는 단일 소스다.
새 센서/액추에이터 종류가 추가되면 이 파일에만 항목을 추가하면 된다.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Category(str, Enum):
    SENSOR = "sensor"
    ACTUATOR = "actuator"


class FieldType(str, Enum):
    BOOL = "bool"
    FLOAT = "float"
    INT = "int"
    STRING = "string"
    COLOR = "color"  # [r, g, b], 각 0-255


@dataclass(frozen=True)
class FieldSpec:
    key: str
    label_ko: str
    type: FieldType
    unit: str | None = None
    min: float | None = None
    max: float | None = None
    step: float | None = None
    options: list[str] | None = None  # STRING 타입의 선택지 (없으면 자유 입력)


@dataclass(frozen=True)
class ComponentType:
    type_key: str
    category: Category
    label_ko: str
    fields: list[FieldSpec] = field(default_factory=list)
    note_ko: str = ""


CATALOG: list[ComponentType] = [
    # ---------------- 센서 ----------------
    ComponentType(
        type_key="pressure",
        category=Category.SENSOR,
        label_ko="압력센서",
        fields=[FieldSpec("value", "압력값", FieldType.FLOAT, unit="kPa", min=0, max=1000)],
        note_ko="아날로그 출력 → 실제 라즈베리파이에서는 ADC(MCP3008 등) 필요",
    ),
    ComponentType(
        type_key="keypad",
        category=Category.SENSOR,
        label_ko="숫자 키패드",
        fields=[
            FieldSpec("key", "입력 키", FieldType.STRING, options=list("0123456789*#")),
            FieldSpec("event", "이벤트", FieldType.STRING, options=["press"]),
        ],
        note_ko="3x4/4x4 매트릭스 키패드",
    ),
    ComponentType(
        type_key="reed_switch",
        category=Category.SENSOR,
        label_ko="리드 스위치",
        fields=[FieldSpec("closed", "닫힘 여부", FieldType.BOOL)],
    ),
    ComponentType(
        type_key="flame",
        category=Category.SENSOR,
        label_ko="불꽃센서",
        fields=[
            FieldSpec("detected", "감지 여부", FieldType.BOOL),
            FieldSpec("intensity", "강도", FieldType.FLOAT, unit="%", min=0, max=100),
        ],
        note_ko="모듈에 따라 디지털/아날로그 출력 상이",
    ),
    ComponentType(
        type_key="dht11",
        category=Category.SENSOR,
        label_ko="온습도센서(DHT11)",
        fields=[
            FieldSpec("temperature_c", "온도", FieldType.FLOAT, unit="°C", min=-10, max=50),
            FieldSpec("humidity_pct", "습도", FieldType.FLOAT, unit="%", min=0, max=100),
        ],
    ),
    ComponentType(
        type_key="hcsr04",
        category=Category.SENSOR,
        label_ko="초음파센서(HC-SR04)",
        fields=[FieldSpec("distance_cm", "거리", FieldType.FLOAT, unit="cm", min=2, max=400)],
        note_ko="trig/echo 2핀 사용",
    ),
    ComponentType(
        type_key="push_button",
        category=Category.SENSOR,
        label_ko="푸시버튼",
        fields=[FieldSpec("pressed", "눌림 여부", FieldType.BOOL)],
    ),
    ComponentType(
        type_key="illuminance",
        category=Category.SENSOR,
        label_ko="조도센서",
        fields=[FieldSpec("lux", "조도", FieldType.FLOAT, unit="lx", min=0, max=2000)],
        note_ko="CDS 등 아날로그 모듈은 ADC(MCP3008 등) 필요, BH1750 등 I2C 모듈은 전용 라이브러리로 lux 직접 획득",
    ),
    # ---------------- 액추에이터 ----------------
    ComponentType(
        type_key="led",
        category=Category.ACTUATOR,
        label_ko="LED",
        fields=[
            FieldSpec("on", "on/off", FieldType.BOOL),
            FieldSpec("brightness_pct", "밝기", FieldType.FLOAT, unit="%", min=0, max=100),
        ],
    ),
    ComponentType(
        type_key="dc_motor",
        category=Category.ACTUATOR,
        label_ko="DC모터",
        fields=[FieldSpec("speed_pct", "속도", FieldType.FLOAT, unit="%", min=-100, max=100)],
        note_ko="모터드라이버(L298N 등) 필요, 부호로 정/역방향 표현",
    ),
    ComponentType(
        type_key="solenoid",
        category=Category.ACTUATOR,
        label_ko="솔레노이드",
        fields=[FieldSpec("on", "on/off", FieldType.BOOL)],
        note_ko="릴레이/트랜지스터로 구동",
    ),
    ComponentType(
        type_key="neopixel",
        category=Category.ACTUATOR,
        label_ko="네오픽셀 LED",
        fields=[
            FieldSpec("color", "색상(RGB)", FieldType.COLOR),
            FieldSpec("brightness_pct", "밝기", FieldType.FLOAT, unit="%", min=0, max=100),
        ],
        note_ko="WS2812, 데이터 1핀",
    ),
    ComponentType(
        type_key="buzzer",
        category=Category.ACTUATOR,
        label_ko="부저",
        fields=[
            FieldSpec("on", "on/off", FieldType.BOOL),
            FieldSpec("freq_hz", "주파수", FieldType.INT, unit="Hz", min=100, max=5000),
        ],
        note_ko="능동/수동 부저에 따라 freq_hz 무시될 수 있음",
    ),
    ComponentType(
        type_key="servo",
        category=Category.ACTUATOR,
        label_ko="서보모터(SG-90)",
        fields=[FieldSpec("angle_deg", "각도", FieldType.FLOAT, unit="deg", min=0, max=180)],
    ),
    ComponentType(
        type_key="relay",
        category=Category.ACTUATOR,
        label_ko="릴레이",
        fields=[FieldSpec("on", "on/off", FieldType.BOOL)],
    ),
]

CATALOG_BY_KEY: dict[str, ComponentType] = {c.type_key: c for c in CATALOG}


def get_component_type(type_key: str) -> ComponentType | None:
    return CATALOG_BY_KEY.get(type_key)


def _matches_type(field_type: FieldType, val: Any) -> bool:
    if field_type == FieldType.BOOL:
        return isinstance(val, bool)
    if field_type in (FieldType.FLOAT, FieldType.INT):
        return isinstance(val, (int, float)) and not isinstance(val, bool)
    if field_type == FieldType.STRING:
        return isinstance(val, str)
    if field_type == FieldType.COLOR:
        return (
            isinstance(val, list)
            and len(val) == 3
            and all(isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= 255 for v in val)
        )
    return True


def validate_payload(type_key: str, payload: dict[str, Any]) -> None:
    """payload의 키가 카탈로그에 정의된 필드인지, 값 타입이 맞는지 검사한다.

    범위(min/max)는 UI 힌트로만 쓰고 하드 검증하지 않는다 — 실제 센서는
    일시적으로 범위를 벗어난 값을 낼 수 있고, 그 자체가 디버깅 대상이 되어야 하기 때문.
    """
    ctype = get_component_type(type_key)
    if ctype is None:
        raise ValueError(f"알 수 없는 컴포넌트 타입입니다: {type_key}")
    field_by_key = {f.key: f for f in ctype.fields}
    for key, val in payload.items():
        spec = field_by_key.get(key)
        if spec is None:
            raise ValueError(f"'{type_key}'에 정의되지 않은 필드입니다: {key}")
        if not _matches_type(spec.type, val):
            raise ValueError(f"필드 '{key}'의 값 타입이 올바르지 않습니다: {val!r}")
