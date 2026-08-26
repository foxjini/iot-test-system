# antigravity-plugin — 라즈베리파이 5 IoT 캡스톤 팀용 Antigravity 플러그인

각 팀의 라즈베리파이 5 담당 학생이, Windows PC의 **Antigravity 2.0 IDE**로 실제
작품 코드를 바이브 코딩할 때 쓰는 플러그인이다. `iot-test-system`(범용 테스트
백엔드+프론트엔드)과 같은 REST API 계약, 같은 센서/액추에이터 카탈로그를 AI
에이전트가 항상 알고 있도록 만든다.

**이 폴더 자체가 실행되는 프로그램은 아니다** — 각 팀의 실제 프로젝트 폴더에
설치해서 Antigravity가 그 컨텍스트를 읽게 만드는 설정 묶음이다.

## 설치 방법

Antigravity는 플러그인을 워크스페이스(팀이 Antigravity로 여는 프로젝트 폴더)
루트의 `.agents/plugins/<플러그인이름>/`에서 찾는다. `AGENTS.md`는 플러그인
폴더가 아니라 **워크스페이스 루트**에서 세션 시작 시 읽힌다. 따라서 팀의 실제
프로젝트 폴더가 예를 들어 `D:\team3-pi-project`라면:

1. 이 폴더(`antigravity-plugin/`) 전체를 복사한다.
2. `AGENTS.md`는 워크스페이스 루트로: `D:\team3-pi-project\AGENTS.md`
   (이미 그 프로젝트에 다른 `AGENTS.md`가 있다면 내용을 이어 붙인다).
3. 나머지(`plugin.json`, `agents/`, `rules/`, `workflows/`, `skills/`, `hooks/`)는
   `D:\team3-pi-project\.agents\plugins\iot-pi5-vibe-coding\` 아래에 그대로 넣는다.
4. Antigravity에서 그 프로젝트 폴더를 워크스페이스로 열면 자동으로 인식된다.

> 위 경로/구조는 2026년 8월 기준 공개된 Antigravity 문서를 참고해 작성했다.
> IDE 버전에 따라 세부 사항이 바뀔 수 있으니, 플러그인이 인식되지 않으면
> Antigravity의 Plugins 설정 화면에서 실제 스캔 경로를 확인한다.

## 이 프로젝트가 필요로 하는 것들 (최초 1회 확인)

- 라즈베리파이 5, Raspberry Pi OS **Trixie**.
- SSH 활성화 (`sudo raspi-config` → Interface Options → SSH) — WinSCP로 파일을
  올리려면 필요하다.
- (코드 전달용) **WinSCP** — Windows에 설치하는 무료 SFTP GUI 클라이언트(winscp.net).
- (화면 디버깅용) **TightVNC** — Trixie는 기본이 Wayland라, X11로 전환한 뒤
  `sudo apt install tightvncserver`로 설치해야 한다.
- `iot-test-system/backend`가 Windows PC에서 실행 중이어야 실제 연동 테스트가 된다
  (`docs/STUDENT_GUIDE.md` 참고).

자세한 내용은 `rules/01-stack.md`, 배포 절차는 `workflows/deploy-to-pi.md`.

## 구성

| 폴더/파일 | 역할 |
|---|---|
| `AGENTS.md` | 워크스페이스 루트에 두는 표준 컨텍스트 (요약) |
| `rules/` | 항상 적용: 스택, 카탈로그 계약, API 계약, 코드 관례 |
| `agents/` | 서브에이전트: gpio-agent, api-agent, vision-agent |
| `workflows/` | 반복 절차: 센서/액추에이터/비전 트리거 추가, 연결 테스트, 배포 |
| `skills/` | 필요할 때만 로드: gpiozero 배선, 백엔드 클라이언트, 비전 트리거 |
| `hooks/` | 사전 점검·자동 포맷·핀 중복 경고 (스키마는 `hooks/README.md` 참고) |

## 이 플러그인이 다루지 않는 것

- 팀의 회로 설계/기구 설계 자체 (하드웨어 담당 학생의 영역).
- `iot-test-system` 백엔드/프론트엔드 자체의 수정 — 그건 저장소 루트의
  `backend/`, `frontend/`를 직접 고친다 (이 플러그인은 그걸 "쓰는" 쪽이다).
