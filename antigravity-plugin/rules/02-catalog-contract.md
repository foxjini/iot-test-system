# 센서/액추에이터 카탈로그 계약

백엔드(`iot-test-system/backend/app/catalog.py`)가 정의한 카탈로그가 유일한 기준이다.
여기 없는 필드명을 새로 만들거나 타입을 바꾸지 않는다. 우리 팀은 이 중 프로젝트
주제에 맞는 **일부만** 골라서 쓴다 — 전부 구현할 필요 없다.

`GET /api/catalog/components`로 백엔드가 켜져 있을 때 언제든 최신 스펙을 확인할 수 있다.

## 센서 (8종 + 선택적 비전 센서 2종)

| type_key | 이름 | payload 필드 | 비고 |
|---|---|---|---|
| `pressure` | 압력센서 | `value`(float, kPa, 0~1000) | 아날로그 → ADC(MCP3008) 필요 |
| `keypad` | 숫자 키패드 | `key`(string, "0"~"9"/"*"/"#"), `event`(string, "press") | 3x4/4x4 매트릭스 |
| `reed_switch` | 리드 스위치 | `closed`(bool) | |
| `flame` | 불꽃센서 | `detected`(bool), `intensity`(float, %, 0~100) | 모듈별 디지털/아날로그 상이 |
| `dht11` | 온습도센서(DHT11) | `temperature_c`(float, °C), `humidity_pct`(float, %) | |
| `hcsr04` | 초음파센서(HC-SR04) | `distance_cm`(float, cm, 2~400) | trig/echo 2핀 |
| `push_button` | 푸시버튼 | `pressed`(bool) | |
| `illuminance` | 조도센서 | `lux`(float, lx, 0~2000) | CDS는 ADC, BH1750은 I2C |
| `qr_scanner` | QR/바코드 인식 *(선택)* | `detected`(bool), `payload`(string) | 미인식 시 `payload`는 빈 문자열 |
| `object_detector` | 영상 객체 인식 *(선택)* | `label`(string), `confidence`(float, 0~1), `count`(int) | YOLO 등 다중 클래스는 label 하나로 대표하거나 컴포넌트를 여러 개 등록 |

## 액추에이터 (7종)

| type_key | 이름 | payload 필드 | 비고 |
|---|---|---|---|
| `led` | LED | `on`(bool), `brightness_pct`(float, %, 0~100) | |
| `dc_motor` | DC모터 | `speed_pct`(float, -100~100) | 모터드라이버(L298N 등), 부호=방향 |
| `solenoid` | 솔레노이드 | `on`(bool) | 릴레이/트랜지스터로 구동 |
| `neopixel` | 네오픽셀 LED | `color`([r,g,b] 0~255), `brightness_pct`(float, %, 0~100) | WS2812, 데이터 1핀 |
| `buzzer` | 부저 | `on`(bool), `freq_hz`(int, Hz, 100~5000) | 수동 부저는 freq_hz 무시될 수 있음 |
| `servo` | 서보모터(SG-90) | `angle_deg`(float, deg, 0~180) | |
| `relay` | 릴레이 | `on`(bool) | |

## `qr_scanner`/`object_detector`에 대한 참고

이 두 타입은 **어디서 인식 연산을 하든** 결과를 텔레메트리로 보고할 때 쓰는
"센서"일 뿐이다. 라즈베리파이에서 직접 인식하든, 백엔드(Windows PC)로 프레임을
보내 인식하든 상관없이 최종적으로 `POST /api/devices/{device_id}/telemetry`로
같은 형태의 값을 올린다. 어느 쪽에서 연산할지는 `skills/vision-trigger/`와
`workflows/add-vision-trigger.md`를 참고해 팀이 정한다.

min/max 등 범위는 UI 힌트일 뿐 하드 검증되지 않는다 — 실제 값이 잠시 범위를
벗어나도 오류가 아니다.
