# 워크플로우: 센서 새로 연동하기

1. `rules/02-catalog-contract.md`에서 추가할 센서의 `type_key`와 필드 계약을 확인한다.
2. 대시보드(`http://localhost:3000`, 또는 팀 백엔드 PC의 IP)에서 해당 디바이스에
   이 `type_key`로 컴포넌트를 등록하고 이름을 붙인다 (예: `dht11` → "거실 온습도").
3. `skills/gpiozero-wiring/references/sensors.md`에서 이 타입의 권장 라이브러리와
   최소 코드를 확인한다.
4. `sensors/<type_key>.py`를 만든다. `generate() -> dict | None` 하나만 구현한다 —
   값을 못 읽었으면 `None`을 반환한다 (예외로 전체 루프를 죽이지 않는다).
5. 반환하는 dict의 키/타입이 2번 계약과 정확히 일치하는지 다시 확인한다.
6. `run.py`(또는 동일 구조)의 센서 push 루프에서 이 함수를 호출해
   `push_telemetry()`로 올리도록 연결한다.
7. `workflows/connect-and-test.md`로 실제 값이 대시보드에 올라오는지 확인한다.
