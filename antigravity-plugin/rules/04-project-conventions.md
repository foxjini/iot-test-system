# 프로젝트 구조/코드 관례

## 권장 파일 구조

`iot-test-system/mock_pi`와 같은 구조를 권장한다 (그대로 베낄 필요는 없지만, 이미
검증된 구조라 이유 없이 다르게 만들지 않는다):

```
project/
  .env                  # BACKEND_URL, DEVICE_ID, API_KEY (커밋 금지)
  .env.example
  client.py             # BackendClient — REST 통신 전담 (skills/backend-api-client 참고)
  run.py                # 진입점: 스레드/루프로 센서 push + 명령 poll + heartbeat
  sensors/
    <type_key>.py        # 센서 1종 = 파일 1개, generate() -> dict | None
  actuators/
    <type_key>.py         # 액추에이터 1종 = 파일 1개, apply(desired: dict) -> dict
  vision/                 # 비전 트리거를 쓰는 팀만 (skills/vision-trigger 참고)
```

## 하드웨어 코드 관례

- `sensors/<type_key>.py`, `actuators/<type_key>.py` 각각의 함수 시그니처
  (`generate() -> dict | None`, `apply(desired: dict) -> dict`)를 지킨다 — `mock_pi/run.py`와
  동일한 스레드 루프 구조를 쓴다면 이 시그니처를 그대로 기대한다.
- gpiozero로 처리하기 어려운 장치(타이밍 민감 센서, 카메라)는 무리하게 gpiozero로
  구현하지 않는다. `skills/gpiozero-wiring/`이 항목별 권장 라이브러리를 정리해 둔다.
- 실기기 특성상 한 번에 완벽히 동작하지 않을 수 있다 — 배선/전원 문제와 코드 문제를
  구분할 수 있도록 print/log를 충분히 남긴다.

## 비밀값/설정

- `BACKEND_URL`, `DEVICE_ID`, `API_KEY`는 항상 `.env`에서 읽는다. 코드에 직접 쓰지 않는다.
- `.env`는 `.gitignore`에 반드시 포함한다 (`.env.example`만 커밋).

## 하지 말 것

- 카탈로그에 없는 필드명을 임의로 추가하거나 타입을 바꾸는 것.
- 텔레메트리/명령 엔드포인트 외에 백엔드와 새로운 통신 경로(WebSocket 등)를 만드는 것.
- 당장 필요하지 않은 설정 옵션·추상화 레이어를 미리 만들어 두는 것 — 이 프로젝트에
  필요한 만큼만 구현한다.
