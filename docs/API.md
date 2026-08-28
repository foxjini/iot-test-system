# IoT 테스트 시스템 — REST API 스펙

이 문서는 라즈베리파이(Mock 또는 실제 기기)와 백엔드, 그리고 프론트엔드 대시보드 간의
REST API 계약을 정의한다. **실제 백엔드를 개발하는 학생팀도 이 계약을 그대로 따르면**,
라즈베리파이팀이 미리 만들어 둔 통신 코드를 거의 수정 없이 재사용할 수 있다.

백엔드 실행 중에는 `http://<백엔드 PC IP>:8000/docs` 에서 Swagger UI로 모든 엔드포인트를
직접 테스트해 볼 수 있다 (FastAPI 자동 생성).

## 개념

- **Device** — 팀의 라즈베리파이 5 한 대. 등록 시 `id`(device_id)와 `api_key`가 발급된다.
- **Component** — 디바이스가 실제로 사용하는 센서/액추에이터 1개. 17종 카탈로그 중에서
  선택해 등록한다 (같은 종류를 여러 개 등록해도 된다, 예: LED 2개).
- **인증** — 라즈베리파이(Mock/실제)가 호출하는 엔드포인트는 `X-Device-Key` 헤더에
  등록 시 발급받은 `api_key`를 담아야 한다. 프론트엔드 대시보드가 호출하는 엔드포인트는
  **이 테스트 시스템이 교내망 내부 전용 도구라는 전제로** 별도 인증을 넣지 않은
  것이다 — 실제 팀 프로젝트 시스템이 이보다 완성도 있는 결과물을 목표로 한다면
  이 선택을 그대로 가져갈지, 대시보드 쪽에도 인증을 추가할지는 백엔드팀이 별도로
  판단해야 한다.

## 17종 센서/액추에이터 카탈로그

`GET /api/catalog/components` 로 아래 내용을 언제든 최신 스펙으로 조회할 수 있다
(필드의 label/unit/min/max 등은 프론트엔드가 폼을 자동으로 그리는 데 쓰인다).

| type_key | 구분 | 이름 | payload 필드 |
|---|---|---|---|
| `pressure` | 센서 | 압력센서 | `value`(float, kPa) |
| `keypad` | 센서 | 숫자 키패드 | `key`(string), `event`(string) |
| `reed_switch` | 센서 | 리드 스위치 | `closed`(bool) |
| `flame` | 센서 | 불꽃센서 | `detected`(bool), `intensity`(float, %) |
| `dht11` | 센서 | 온습도센서(DHT11) | `temperature_c`(float), `humidity_pct`(float) |
| `hcsr04` | 센서 | 초음파센서(HC-SR04) | `distance_cm`(float) |
| `push_button` | 센서 | 푸시버튼 | `pressed`(bool) |
| `illuminance` | 센서 | 조도센서 | `lux`(float, lx) |
| `qr_scanner` | 센서 | QR/바코드 인식 | `detected`(bool), `payload`(string) |
| `object_detector` | 센서 | 영상 객체 인식 | `label`(string), `confidence`(float), `count`(int) |
| `led` | 액추에이터 | LED | `on`(bool), `brightness_pct`(float) |
| `dc_motor` | 액추에이터 | DC모터 | `speed_pct`(float, -100~100) |
| `solenoid` | 액추에이터 | 솔레노이드 | `on`(bool) |
| `neopixel` | 액추에이터 | 네오픽셀 LED | `color`([r,g,b] 0-255), `brightness_pct`(float) |
| `buzzer` | 액추에이터 | 부저 | `on`(bool), `freq_hz`(int) |
| `servo` | 액추에이터 | 서보모터(SG-90) | `angle_deg`(float, 0~180) |
| `relay` | 액추에이터 | 릴레이 | `on`(bool) |

범위(0~100, 2~400 등)는 프론트엔드가 입력 폼을 그릴 때 쓰는 힌트일 뿐이다 —
**백엔드는 이 범위를 하드 검증하지 않는다.** 실제 센서는 일시적으로 범위를 벗어난
값을 보낼 수 있고, 그 자체가 확인해야 할 신호이지 거부할 이유가 아니기 때문이다.
백엔드를 새로 구현하는 팀도 이 필드들에 엄격한 범위 검증을 넣지 않는 것을 권장한다
(타입 불일치나 정의되지 않은 필드는 여전히 400으로 거부해야 한다).

## 엔드포인트

아래 "성공 코드" 이외의 모든 실패는 오류 응답 표(맨 아래)를 따른다. 204는 응답
본문이 없다.

### 카탈로그

| Method | Path | 인증 | 성공 코드 | 설명 |
|---|---|---|---|---|
| GET | `/api/catalog/components` | - | 200 | 17종 스펙 전체 조회 |

### 디바이스

| Method | Path | 인증 | 성공 코드 | 설명 |
|---|---|---|---|---|
| GET | `/api/devices` | - | 200 | 디바이스 목록 |
| POST | `/api/devices` | - | 201 | 디바이스 등록 `{team_name}` → `api_key` 발급 |
| GET | `/api/devices/{device_id}` | - | 200 | 디바이스 조회 (온라인 상태 포함) |
| DELETE | `/api/devices/{device_id}` | - | 204 | 디바이스 삭제 |

`is_online`은 최근 하트비트가 `HEARTBEAT_TIMEOUT_SEC`(기본 15초) 이내인지로 서버가 계산한다.

### 컴포넌트(팀별 센서/액추에이터 구성)

| Method | Path | 인증 | 성공 코드 | 설명 |
|---|---|---|---|---|
| GET | `/api/devices/{device_id}/components` | - | 200 | 등록된 컴포넌트 목록 |
| POST | `/api/devices/{device_id}/components` | - | 201 | 컴포넌트 추가 `{type_key, label, gpio_pin?}` |
| DELETE | `/api/devices/{device_id}/components/{component_id}` | - | 204 | 컴포넌트 삭제 |

### 센서 텔레메트리

| Method | Path | 인증 | 성공 코드 | 설명 |
|---|---|---|---|---|
| POST | `/api/devices/{device_id}/telemetry` | `X-Device-Key` | 204 | 센서값 일괄 업로드 |
| GET | `/api/devices/{device_id}/components/{component_id}/readings?limit=50` | - | 200 | 최근 이력 조회 |

`POST .../telemetry` 요청 본문:

```json
{
  "items": [
    { "component_id": 1, "value": { "temperature_c": 24.5, "humidity_pct": 55.0 } },
    { "component_id": 5, "value": { "detected": false, "intensity": 2.1 } }
  ]
}
```

### 액추에이터 명령

| Method | Path | 인증 | 성공 코드 | 설명 |
|---|---|---|---|---|
| POST | `/api/devices/{device_id}/components/{component_id}/command` | - | 201 | 명령 등록(대시보드→백엔드) `{desired_state}` |
| GET | `/api/devices/{device_id}/components/{component_id}/command/latest` | - | 200 | 최신 명령/실행결과 조회(대시보드 표시용) |
| GET | `/api/devices/{device_id}/commands/pending` | `X-Device-Key` | 200 | 대기 중인 명령 조회(라즈베리파이 폴링) |
| POST | `/api/devices/{device_id}/commands/{command_id}/ack` | `X-Device-Key` | 200 | 실행결과 보고 `{actual_state, status}` |

명령 상태(`status`)는 `pending` → `acked`(정상 실행) 또는 `failed`(실행 실패)로 전이한다.

### 하트비트

| Method | Path | 인증 | 성공 코드 | 설명 |
|---|---|---|---|---|
| POST | `/api/devices/{device_id}/heartbeat` | `X-Device-Key` | 200 | 생존 신고 |

### 비전 인식 오프로드 (선택 기능)

라즈베리파이 5는 GPU가 없어 무거운 영상 인식(YOLO 등)이 느릴 수 있다. QR 인식만큼은
백엔드(Windows PC)로 오프로드할 수 있도록 별도 엔드포인트를 둔다. 일반 텔레메트리/명령
흐름과 무관한 독립 기능이라 `device_id`가 경로에 없고, 등록된 디바이스 중 하나의
유효한 API Key이기만 하면 된다(특정 device_id에 종속되지 않음).

| Method | Path | 인증 | 성공 코드 | 설명 |
|---|---|---|---|---|
| POST | `/api/vision/qr` | `X-Device-Key` | 200 | 이미지(base64)를 받아 QR을 디코딩해 결과만 반환 |

```json
// 요청
{ "image_base64": "<JPEG/PNG를 base64로 인코딩한 문자열>" }
```

```json
// 200 응답
{ "detected": true, "payload": "TEAM3-DOOR-OPEN" }
```

결과는 자동으로 저장되지 않는다 — 호출한 쪽이 필요하면 `qr_scanner` 컴포넌트에 대해
평소처럼 `POST .../telemetry`로 직접 기록한다. 이 엔드포인트를 쓰려면 백엔드에
`backend/requirements-vision.txt`(`opencv-python`)를 추가 설치해야 하며, 설치하지
않으면 400과 함께 설치 안내 메시지를 반환한다.

## 동작 방식 요약

- 센서: 라즈베리파이가 **주기적으로 push**(`/telemetry`)한다. 서버가 먼저 요청하지 않는다.
- 액추에이터: 대시보드가 명령을 등록하면, 라즈베리파이가 **주기적으로 poll**(`/commands/pending`)해서
  가져가 실행하고 `/ack`로 결과를 보고한다.
- 실시간 push(WebSocket/MQTT 등)는 쓰지 않는다 — REST(JSON) polling만으로 구성된다.

## 오류 응답

모든 오류는 `{"detail": "메시지"}` 형태의 JSON으로 반환된다.

| 상태코드 | 상황 |
|---|---|
| 400 | 잘못된 요청 (알 수 없는 type_key, 카탈로그에 없는 필드, 센서/액추에이터 카테고리 불일치 등) |
| 401 | `X-Device-Key`가 없거나 device_id와 일치하지 않음 |
| 404 | device_id/component_id/command_id가 존재하지 않음 |
