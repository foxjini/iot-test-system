# 워크플로우: 영상/QR 트리거 추가하기

1. 이 기능이 정말 필요한지, 필요하다면 QR인지 객체 인식인지 먼저 확인한다
   (`skills/vision-trigger/SKILL.md`).
2. 처리 위치(라즈베리파이 로컬 vs 백엔드 오프로드)를 정한다
   (`skills/vision-trigger/references/options.md`의 비교표 참고).
3. 대시보드에서 `qr_scanner` 또는 `object_detector` 컴포넌트를 등록한다
   (`rules/02-catalog-contract.md`).
4. 선택한 방식에 맞는 템플릿을 `sensors/qr_scanner.py` 또는
   `sensors/object_detector.py`로 복사해서 시작한다:
   - 로컬 QR: `skills/vision-trigger/templates/qr_local.py`
   - 오프로드 QR: `skills/vision-trigger/templates/qr_offload_client.py`
     (백엔드에 `pip install -r backend/requirements-vision.txt` 먼저 설치되어 있어야 함)
   - 로컬 객체 인식: `skills/vision-trigger/templates/object_detector_local.py`
5. 카메라가 실제로 열리는지, `generate()`가 계약대로 dict를 반환하는지 단독으로
   먼저 테스트한다 (`python -c "import sensors.qr_scanner as s; print(s.generate())"` 등).
6. `new-sensor.md`와 동일하게 push 루프에 연결해 대시보드에 값이 올라오는지 확인한다.
7. 트리거가 필요하면(인식 시 액추에이터 반응), 인식 결과를 받는 지점에서 바로
   해당 `actuators/<type_key>.py`의 `apply()`를 호출하는 일반 코드를 추가한다 —
   백엔드를 거치지 않고 라즈베리파이 안에서 바로 반응하게 하는 것을 권장한다
   (반응 속도, 네트워크 의존성 최소화).
