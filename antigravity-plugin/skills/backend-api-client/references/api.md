# 엔드포인트 요약

라즈베리파이 쪽에서 실제로 부르는 5개 엔드포인트만 요약한다. 상세 계약(요청/응답
필드, 오류 형식)은 `rules/03-api-contract.md`와 `iot-test-system/docs/부록B-REST-API-스펙.md`를 본다.

| 메서드 | 경로 | 인증 | 용도 |
|---|---|---|---|
| GET | `/api/devices/{device_id}/components` | - | 컴포넌트 목록 동기화 |
| POST | `/api/devices/{device_id}/telemetry` | O | 센서값 push |
| GET | `/api/devices/{device_id}/commands/pending` | O | 명령 poll |
| POST | `/api/devices/{device_id}/commands/{command_id}/ack` | O | 실행결과 보고 |
| POST | `/api/devices/{device_id}/heartbeat` | O | 생존 신고 |

인증(O)은 `X-Device-Key: <api_key>` 헤더가 필요하다는 뜻이다.
