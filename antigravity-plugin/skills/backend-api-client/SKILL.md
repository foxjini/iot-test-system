---
name: backend-api-client
description: 라즈베리파이 코드에서 테스트 백엔드(REST/JSON)와 통신하는 클라이언트를 작성하거나 수정할 때 사용한다. "백엔드 연동", "REST", "API 호출", "텔레메트리", "명령 폴링", "device_id", "api_key"가 언급되면 이 스킬을 불러온다.
---

# 백엔드 REST 클라이언트

정확한 엔드포인트/인증/페이로드 계약은 `rules/03-api-contract.md`가 기준이다.
이 스킬은 그 계약을 실제로 구현한 클라이언트 코드를 새로 만들 때 쓰는 템플릿을 제공한다.

- `templates/client.py` — `iot-test-system/mock_pi/client.py`와 동일한 계약을 구현한
  `BackendClient`. 그대로 복사해서 시작해도 되고, 필요한 부분만 참고해도 된다.
- `references/api.md` — 엔드포인트 요약 (상세 계약은 `rules/03-api-contract.md`)

## 사용 방법

1. `templates/client.py`를 프로젝트의 `client.py`로 복사한다.
2. `.env`에 `BACKEND_URL`, `DEVICE_ID`, `API_KEY`를 채운다 (대시보드에서 디바이스
   등록 후 발급받은 값).
3. `run.py`(진입점)에서 `list_components()`로 등록된 컴포넌트를 동기화하고,
   센서는 주기적으로 `push_telemetry()`, 액추에이터는 주기적으로
   `pending_commands()` → 실행 → `ack_command()` 순서로 호출한다.
4. 연결 확인은 `workflows/connect-and-test.md` 절차를 따른다.

이 클라이언트는 REST 통신만 전담한다 — GPIO/카메라 관련 로직을 여기 섞지 않는다
(관심사 분리, `rules/04-project-conventions.md`의 파일 구조 참고).
