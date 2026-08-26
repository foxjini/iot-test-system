# 백엔드 REST API 계약

전체 계약은 `iot-test-system/docs/API.md`가 원본이다. 여기서는 라즈베리파이
쪽 코드를 작성할 때 실제로 필요한 부분만 요약한다. 백엔드가 켜져 있으면
`http://<백엔드 PC IP>:8000/docs`에서 Swagger UI로 직접 확인할 수 있다.

## 인증

라즈베리파이가 호출하는 엔드포인트는 모두 `X-Device-Key` 헤더에 디바이스 등록 시
발급받은 `api_key`를 담아야 한다 (`.env`에서 읽어온다, 코드에 하드코딩 금지).

## 라즈베리파이가 실제로 호출하는 엔드포인트

| Method | Path | 용도 |
|---|---|---|
| GET | `/api/devices/{device_id}/components` | 이 디바이스에 등록된 컴포넌트 목록 동기화 |
| POST | `/api/devices/{device_id}/telemetry` | 센서값 일괄 push |
| GET | `/api/devices/{device_id}/commands/pending` | 대기 중인 액추에이터 명령 poll |
| POST | `/api/devices/{device_id}/commands/{command_id}/ack` | 명령 실행 결과 보고 |
| POST | `/api/devices/{device_id}/heartbeat` | 생존 신고 |

`telemetry` 요청 본문:

```json
{ "items": [ { "component_id": 1, "value": { "temperature_c": 24.5, "humidity_pct": 55.0 } } ] }
```

`ack` 요청 본문:

```json
{ "actual_state": { "on": true, "brightness_pct": 80.0 }, "status": "acked" }
```

`status`는 정상 실행 시 `"acked"`, 실행 실패 시 `"failed"`.

## 동작 방식

- 센서는 **push**(주기적으로 telemetry를 보낸다), 액추에이터 명령은 **poll**(주기적으로
  pending을 확인한다) — 서버가 라즈베리파이로 먼저 연결을 열지 않는다.
- WebSocket/MQTT는 쓰지 않는다. 폴링 주기는 보통 1~2초 (필요에 맞게 조정 가능).
- `is_online`은 서버가 최근 heartbeat 시각으로 계산한다 — 라즈베리파이가 직접 관리하지 않는다.

## 오류 응답

모든 오류는 `{"detail": "메시지"}` JSON. 401은 `X-Device-Key` 누락/불일치, 400은
카탈로그에 없는 type_key/필드, 404는 device_id/component_id/command_id 없음.

## 선택 기능: 비전 인식 오프로드

라즈베리파이 대신 백엔드(Windows PC)에서 QR 인식을 수행하고 싶을 때만 쓰는
엔드포인트다. 일반 센서/액추에이터 흐름과는 별도이고, 이것을 쓰지 않아도
`qr_scanner`/`object_detector` 값을 직접 인식해 텔레메트리로 올리는 데는 아무 문제 없다.

| Method | Path | 인증 | 설명 |
|---|---|---|---|
| POST | `/api/vision/qr` | `X-Device-Key` | 이미지(base64 JPEG/PNG)를 보내면 OpenCV로 QR을 디코딩해 결과만 반환 (센서 값으로 자동 기록되지 않음) |

요청/응답 형식과 백엔드에 필요한 추가 설치(`opencv-python`)는
`skills/vision-trigger/references/options.md` 참고.
