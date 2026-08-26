# 워크플로우: 액추에이터 새로 연동하기

1. `rules/02-catalog-contract.md`에서 추가할 액추에이터의 `type_key`와 필드 계약을 확인한다.
2. 대시보드에서 해당 디바이스에 이 `type_key`로 컴포넌트를 등록하고 이름을 붙인다.
3. `skills/gpiozero-wiring/references/actuators.md`에서 이 타입의 권장 gpiozero
   클래스와 최소 코드를 확인한다.
4. `actuators/<type_key>.py`를 만든다. `apply(desired: dict) -> dict` 하나만
   구현한다 — `desired`를 받아 실제 GPIO를 그 상태로 바꾸고, **반영된 실제 상태**를
   그대로 dict로 반환한다 (실패했으면 실제로 반영된 값만 반환하거나 예외를 던져서
   호출부가 `status="failed"`로 ack하게 한다).
5. 전체 루프에 연결하기 전에 `apply()`를 단독으로 먼저 테스트한다 (예:
   `python -c "import actuators.servo as a; print(a.apply({'angle_deg': 90.0}))"`).
   반환된 dict가 `desired_state`와 같은 형태(키/타입)인지 여기서 확인한다.
6. `run.py`(또는 동일 구조)의 명령 poll 루프에서: `pending_commands()` → 해당
   컴포넌트면 이 `apply()` 호출 → `ack_command(command_id, 반환된_dict)`로 연결한다.
7. 대시보드의 "적용" 버튼으로 실제 하드웨어가 반응하는지, "현재" 상태 표시가
   반영된 값과 일치하는지 확인한다.
