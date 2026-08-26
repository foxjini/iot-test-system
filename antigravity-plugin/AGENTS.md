# 프로젝트 컨텍스트: 라즈베리파이 5 IoT 캡스톤 프로젝트

이 프로젝트는 **라즈베리파이 5(Trixie)** 에서 동작하는 팀별 IoT 작품의 실제 코드다.
같은 저장소의 `iot-test-system`(범용 테스트 백엔드+프론트엔드)이 이미 정해둔 REST API
계약을 그대로 따르므로, 그 계약을 벗어나는 코드를 생성하지 않는다.

## 하드웨어/개발 환경

- 대상: 라즈베리파이 5, OS는 Raspberry Pi OS **Trixie**(Debian 13 기반).
- GPIO 제어는 **gpiozero를 우선 사용**한다 (`gpiozero>=2.0.1.post3`, 핀팩토리는 **lgpio**).
  Pi 5의 RP1 칩은 구형 `RPi.GPIO` 백엔드를 지원하지 않으므로 다른 핀팩토리를 쓰지 않는다.
- 개발은 Windows PC의 **Antigravity 2.0 IDE**에서 코드를 작성하고, **SSH**(`scp`/`rsync`,
  Windows 10/11 내장 OpenSSH 클라이언트)로 라즈베리파이에 코드를 올려 실행한다.
  화면이 필요한 디버깅(카메라 미리보기 등)은 **RealVNC**로 라즈베리파이에 원격 접속한다.
  자세한 절차는 `workflows/deploy-to-pi.md` 참고.
- 이 두 원격 도구는 서로 무관하다: SSH는 Raspberry Pi OS 자체 기능(라즈베리파이용
  RealVNC 요금제와 무관하게 항상 무료)이고, RealVNC는 같은 공유기 LAN 안에서
  "Direct" 연결로 쓰는 한 라즈베리파이에서 계정 가입 없이 무료다.

## 백엔드 연동 (범용 테스트 시스템)

- 백엔드는 Windows PC에서 실행 중인 FastAPI 서버(`iot-test-system/backend`)이며,
  REST(JSON)만 사용한다. WebSocket/MQTT는 쓰지 않는다.
- 센서는 주기적으로 `POST /api/devices/{device_id}/telemetry`로 값을 push하고,
  액추에이터 명령은 `GET /api/devices/{device_id}/commands/pending`을 주기적으로
  poll해서 실행한 뒤 `POST .../commands/{command_id}/ack`로 결과를 보고한다.
- 정확한 엔드포인트/인증/페이로드 형식은 `rules/api-contract.md`와
  `skills/backend-api-client/`를 따른다 — 필드명을 임의로 바꾸거나 새로 만들지 않는다.

## 센서/액추에이터 카탈로그

이 팀이 실제로 쓰는 항목은 전체 카탈로그(센서 8종 + 액추에이터 7종 + 선택적 비전
센서 2종) 중 프로젝트 주제에 맞게 고른 일부뿐이다. 카탈로그에 없는 필드명을
새로 만들지 말고, 새 종류가 필요하면 먼저 `rules/catalog-contract.md`에 추가할지
사용자에게 확인한다. 정확한 필드/타입은 `rules/catalog-contract.md` 참고.

## 영상/QR 트리거 (선택 기능)

프로젝트 주제에 영상 인식(예: 객체 인식, QR코드 인식)이 필요한 팀만 사용한다.
연산을 **라즈베리파이에서 직접** 할지, 연산량이 큰 경우 **백엔드(Windows PC)로
오프로드**할지는 팀이 정한다. 두 방식 모두 결과는 결국 기존 텔레메트리/명령
엔드포인트로 보고·실행되므로 새로운 통신 경로를 만들 필요는 없다.
자세한 내용은 `skills/vision-trigger/`와 `workflows/add-vision-trigger.md` 참고.

## 코드 스타일

- 불필요한 추상화·설정 옵션을 만들지 않는다. 이 프로젝트에 필요한 만큼만 구현한다.
- 비밀값(API Key 등)은 항상 `.env`에서 읽고 코드에 하드코딩하지 않는다.
- 실기기로 넘어가는 부분은 `# TODO(실기기 연동)` 주석 관례를 따르는
  `iot-test-system/mock_pi`의 구조(각 센서/액추에이터가 독립 파일, `client.py`가
  REST 통신 전담)를 참고해도 좋다 — 그대로 베낄 필요는 없지만 같은 계약을 지킨다.

## 더 자세한 내용

- `rules/` — 항상 적용되는 표준 컨텍스트(스택, 카탈로그 계약, API 계약, 코드 관례).
- `skills/` — 필요할 때만 불러오는 전문 지식(gpiozero 배선, 백엔드 클라이언트, 비전 트리거).
- `agents/` — 하드웨어/API/비전 각각을 담당하는 서브에이전트.
- `workflows/` — 센서·액추에이터 추가, 비전 트리거 추가, 연결 테스트, 배포의 반복 절차.
