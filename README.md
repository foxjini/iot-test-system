# IoT 테스트 시스템

라즈베리파이 5 담당 학생팀(6개 팀)이, 진짜 백엔드/프론트엔드가 완성되기 전까지 사용할
**범용 테스트 백엔드 + 프론트엔드 + Mock 라즈베리파이**. 17종 센서/액추에이터를 모두
지원하며, 팀마다 실제 작품에서 쓰는 항목만 골라 구성하고 테스트할 수 있다.

- 센서 10종: 압력센서, 숫자 키패드, 리드 스위치, 불꽃센서, 온습도센서(DHT11),
  초음파센서(HC-SR04), 푸시버튼, 조도센서, QR/바코드 인식, 영상 객체 인식
- 액추에이터 7종: LED, DC모터, 솔레노이드, 네오픽셀 LED, 부저, 서보모터(SG-90), 릴레이

## 구성

| 폴더 | 역할 | 스택 |
|---|---|---|
| `backend/` | REST API 서버 | FastAPI + SQLAlchemy + MySQL (Python venv) |
| `frontend/` | 팀별 구성/모니터링/제어 대시보드 | Next.js (TypeScript) |
| `mock_pi/` | 라즈베리파이 5를 대신하는 테스트 클라이언트 | Python venv |
| `docs/` | API 스펙, 학생 가이드 | - |
| `scripts/` | MySQL 초기 설정 스크립트 | - |
| `antigravity-plugin/` | 실기기(라즈베리파이 5) 프로젝트 개발용 Antigravity 2.0 플러그인 | AGENTS.md/agents/rules/workflows/skills/hooks |

`backend` + `frontend` + `MySQL`은 한 Windows PC에 함께 설치해서 실행하고, 라즈베리파이
(또는 그 자리를 대신하는 `mock_pi`)가 REST API로 접속하는 구조다. DB 계정은 팀마다 독립
설치되는 테스트 도구라는 점을 감안해 root를 그대로 사용한다.

## 빠른 시작 (Windows)

각 폴더의 스크립트는 `.bat`(cmd)와 `.ps1`(PowerShell) 두 버전으로 있다. PowerShell에서는
`.\setup.bat`처럼 `.\`을 붙이거나 같은 이름의 `.ps1`을 쓴다 (`.ps1` 최초 1회 실행 정책 설정은
`docs/STUDENT_GUIDE.md` 0번 항목 참고). 항상 **setup 실행 → 방금 생성된 .env 파일 편집 →
run 실행** 순서다.

```bat
REM 1) DB에 iot_test 데이터베이스 생성 (최초 1회, root 계정 사용)
mysql -u root -p < scripts\mysql_setup.sql

REM 2) 백엔드
cd backend
.\setup.bat
REM -> backend\.env 생성됨. 열어서 DATABASE_URL의 root 비밀번호를 채운다
.\run.bat

REM 3) 프론트엔드 (새 터미널)
cd frontend
.\setup.bat
.\run.bat

REM 4) 대시보드(http://localhost:3000)에서 디바이스 등록 후 device_id/API Key 확인

REM 5) Mock 라즈베리파이 (새 터미널)
cd mock_pi
.\setup.bat
REM -> mock_pi\.env 생성됨. 열어서 DEVICE_ID/API_KEY를 4번 값으로 채운다
.\run.bat
```

자세한 설치/실행/문제해결은 [`docs/STUDENT_GUIDE.md`](docs/STUDENT_GUIDE.md),
REST API 전체 스펙은 [`docs/API.md`](docs/API.md) 참고.

## 설계 메모

- **팀마다 센서/액추에이터 구성이 다르다는 점**을 반영해, 17종을 하드코딩하지 않고
  카탈로그(`backend/app/catalog.py`) + 디바이스별 컴포넌트 등록 방식으로 처리한다.
  대시보드의 "구성 관리"에서 팀이 직접 필요한 항목만 추가한다.
- API 경로에는 `device_id`를 유지해, 6개 팀이 테스트 기간 동안 **하나의 테스트
  백엔드 인스턴스를 함께 쓸 수 있도록** 설계했다 (`docs/API.md`). 각 팀의 진짜
  백엔드(`agent-vibe-coding-starter-kit2`로 별도 개발)는 팀당 독립 배포·단일
  디바이스를 전제로 한 다른 계약을 쓰므로, 이 다중 디바이스 계약을 그대로
  이어받지는 않는다 — 진짜 시스템 연동 방법은 `antigravity-plugin/README.md`의
  "이 플러그인의 역할" 참고.
- `mock_pi`는 백엔드에 등록된 컴포넌트 목록을 그대로 읽어와 동작하므로, 대시보드에서
  구성을 바꾸면 자동으로 맞춰진다. 실제 라즈베리파이로 전환할 때도 `mock_pi/sensors`,
  `mock_pi/actuators` 안의 함수만 gpiozero 코드로 교체하면 되도록 구조를 맞췄다
  (`docs/STUDENT_GUIDE.md` 7번 항목).
- 통신은 REST(JSON) polling만 사용한다 (WebSocket/MQTT 없음): 센서는 라즈베리파이가
  주기적으로 push, 액추에이터 명령은 라즈베리파이가 주기적으로 poll한다.
