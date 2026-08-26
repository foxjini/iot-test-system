# 라즈베리파이팀을 위한 사용 가이드

## 이 시스템은 왜 필요한가

우리 팀의 진짜 백엔드/프론트엔드가 아직 개발 중이더라도, 라즈베리파이 5의 센서/액추에이터
코드와 REST API 통신 부분을 미리 만들고 테스트할 수 있도록, 17종 센서/액추에이터를 모두
지원하는 **범용 테스트 백엔드+프론트엔드**를 제공한다. 진짜 백엔드가 완성되면 이 시스템과
**같은 API 계약**(`docs/API.md`)을 따르므로, 지금 만든 라즈베리파이 쪽 코드를 거의 그대로
옮겨 쓸 수 있다.

구성 요소:

- `backend/` — FastAPI + MySQL. 팀의 센서값/액추에이터 상태를 저장하고 REST API로 제공.
- `frontend/` — Next.js 대시보드. 팀 구성 관리 + 센서 모니터링 + 액추에이터 제어 화면.
- `mock_pi/` — 진짜 라즈베리파이가 준비되기 전, 그 자리를 대신하는 Python 프로그램.

**`backend` + `frontend` + `MySQL`은 같은 Windows PC 한 대에 설치**하고, 그 PC와 같은
네트워크(공유기/핫스팟)에 연결된 라즈베리파이가 REST API로 접속하는 구조다.

`backend`, `frontend`, `mock_pi` 각 폴더에는 실행용 스크립트가 `.bat`(cmd)와
`.ps1`(PowerShell) 두 버전으로 들어있다. 아래 안내는 전부 `.bat` 기준으로 적었으니,
PowerShell을 쓴다면 같은 이름의 `.ps1`로 바꿔서 실행하면 된다 (예: `setup.bat` → `setup.ps1`).

## 0. PowerShell 사용자를 위한 안내

cmd 대신 PowerShell에서 작업한다면 아래 두 가지만 알아두면 된다.

**`.bat` 파일 실행** — PowerShell은 cmd와 달리 현재 폴더를 명령 검색 경로에 포함하지
않는다. 그냥 `setup.bat`이라고 치면 "인식할 수 없는 명령입니다" 오류가 난다. 반드시 앞에
`.\`을 붙여 `.\setup.bat`처럼 실행한다.

**`.ps1` 파일 실행** — 기본 보안 정책상 처음에는 스크립트 실행 자체가 막혀 있다. PowerShell을
열고 (관리자 권한 불필요) 최초 1회만 아래 명령을 실행한다.

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

그 다음부터는 `.\setup.ps1`처럼 실행하면 된다. (계정 설정을 바꾸고 싶지 않다면 매번
`powershell -ExecutionPolicy Bypass -File .\setup.ps1`로 실행해도 된다.)

## 1. Windows PC 준비물 설치

1. **Python 3.11 이상** — [python.org](https://www.python.org/downloads/) 설치 시
   "Add python.exe to PATH" 체크.
2. **Node.js 20 이상(LTS)** — [nodejs.org](https://nodejs.org/)
3. **MySQL 8.0** (MySQL Community Server) — [MySQL Installer](https://dev.mysql.com/downloads/installer/)로
   설치. 이미 설치되어 있다면 새로 깔 필요 없다. 설치 중 지정한 **root 비밀번호를 기억해
   둘 것** — 이 시스템은 별도 앱 계정을 만들지 않고 root 계정을 그대로 사용한다.

## 2. MySQL 데이터베이스 만들기

"MySQL Command Line Client"를 열고 root 비밀번호로 로그인한 뒤:

```sql
source C:/경로/iot-test-system/scripts/mysql_setup.sql
```

또는 명령 프롬프트/PowerShell에서:

```bat
mysql -u root -p < scripts\mysql_setup.sql
```

`iot_test` 데이터베이스가 생성된다. (아직 비밀번호나 `.env` 파일은 건드리지 않는다 —
다음 단계에서 스크립트가 자동으로 만들어 준다.)

> **root 계정으로 접속이 안 될 때(Access denied for user 'root'@'127.0.0.1')**:
> root 계정이 `localhost` 전용으로만 등록되어 있고 127.0.0.1(TCP) 접속용 등록이 없는
> 경우다. `scripts/mysql_setup.sql` 안의 주석 처리된 `CREATE USER 'root'@'127.0.0.1'...`
> 부분을 실제 비밀번호로 채워 넣고 다시 실행하면 해결된다.

## 3. 백엔드 설정 및 실행

항상 **① setup 실행(파일 생성) → ② 그 파일 열어서 값 채우기 → ③ run 실행** 순서다.

```bat
cd backend
.\setup.bat
```

`setup.bat`이 venv 생성, 라이브러리 설치에 이어 `backend\.env` 파일을 자동으로 만든다
(`.env.example`을 복사). **이제 `backend\.env`를 열어** `DATABASE_URL`의
`여기에_root_비밀번호` 부분을 2번에서 사용한 실제 MySQL root 비밀번호로 바꾼다.

저장했으면 실행한다:

```bat
.\run.bat
```

`http://0.0.0.0:8000`에서 뜬다 (종료는 Ctrl+C). `http://localhost:8000/docs`에 접속하면
모든 API를 Swagger UI로 바로 테스트해 볼 수 있다.

## 4. 프론트엔드(대시보드) 설정 및 실행

```bat
cd frontend
.\setup.bat
```

`setup.bat`이 `npm install`에 이어 `frontend\.env.local`을 자동으로 만든다. 백엔드와
프론트를 같은 PC에서 실행하는 기본 구성이면 **이 파일은 열어볼 필요 없이 기본값
(`NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000`) 그대로 두면 된다.**

```bat
.\run.bat
```

브라우저로 `http://localhost:3000` 접속.

## 5. 대시보드에서 팀 디바이스 등록 및 구성

1. 홈 화면에서 "새 디바이스(팀) 등록"에 팀 이름 입력 → 등록.
2. 발급된 **device_id / API Key**를 적어 둔다 (화면에 계속 표시되고, 상세 화면에서
   "복사" 버튼으로도 복사할 수 있다).
3. 디바이스 카드를 클릭해 상세 화면으로 이동, "구성 관리"에서 우리 팀이 실제로 쓰는
   센서/액추에이터를 17종 중 골라 이름을 붙여 추가한다 (예: DHT11 → "거실 온습도").

## 6. Mock 라즈베리파이 설정 및 실행

```bat
cd mock_pi
.\setup.bat
```

`setup.bat`이 venv 생성, 라이브러리 설치에 이어 `mock_pi\.env`를 자동으로 만든다.
**이제 `mock_pi\.env`를 열어** 5번에서 발급받은 `DEVICE_ID`, `API_KEY`를 입력한다.

저장했으면 실행한다:

```bat
.\run.bat
```

대시보드로 돌아가면 방금 추가한 센서 카드에 값이 들어오기 시작하고, 액추에이터 카드에서
"적용"을 누르면 콘솔에 `[명령 실행]` 로그가 찍히며 "실행 완료"로 바뀌는 것을 볼 수 있다.

> Mock은 대시보드의 "구성 관리"에서 선택한 항목을 자동으로 읽어 동작한다. 항목을
> 추가/삭제해도 Mock을 재시작할 필요 없이 (기본 15초 주기로) 자동 반영된다.

## 7. 진짜 라즈베리파이 5로 전환하기

라즈베리파이 5(Trixie OS)에서:

1. 같은 공유기/네트워크에 연결한다.
2. Windows PC의 LAN IP를 확인한다 (Windows에서 `ipconfig` → IPv4 주소, 예: `192.168.0.10`).
3. 라즈베리파이에서 `curl http://192.168.0.10:8000/api/health` 로 접속이 되는지 먼저 확인한다.
   - 안 되면 **Windows Defender 방화벽에서 8000번 포트 인바운드 허용**이 필요할 수 있다.
4. `mock_pi/` 폴더 전체를 라즈베리파이로 복사해도 되고, 직접 gpiozero로 새로 작성해도 된다.
   어느 쪽이든 `mock_pi/client.py`의 `BackendClient`는 그대로 재사용 가능하다 —
   REST 통신 코드이지 Mock 전용 코드가 아니다.
5. `mock_pi/sensors/*.py`, `mock_pi/actuators/*.py` 안의 `# TODO(실기기 연동)` 주석이 달린
   부분만 실제 gpiozero 코드로 바꾸면 된다. 함수 시그니처(`generate() -> dict`,
   `apply(desired: dict) -> dict`)는 그대로 유지해야 `run.py`가 그대로 동작한다.
6. `.env`의 `BACKEND_URL`을 Windows PC의 LAN IP로 바꾼다
   (예: `BACKEND_URL=http://192.168.0.10:8000`).
7. Windows PC에서 **Antigravity 2.0 IDE**로 이 코드를 작성한다면
   [`antigravity-plugin/README.md`](../antigravity-plugin/README.md)를 먼저 읽는다.
   같은 카탈로그/API 계약과 gpiozero 배선 정보를 AI 에이전트가 항상 참고하도록
   만드는 플러그인이다 (SSH/RealVNC로 라즈베리파이에 배포하는 절차 포함).

## 문제 해결

| 증상 | 확인할 것 |
|---|---|
| PowerShell에서 `setup.bat`을 쳤는데 "인식할 수 없는 명령"이라고 나옴 | `.\setup.bat`처럼 앞에 `.\`을 붙였는지 (위 0번 항목) |
| PowerShell에서 `.ps1` 실행이 막힘(스크립트 실행을 사용할 수 없으므로...) | 위 0번 항목의 `Set-ExecutionPolicy` 명령을 최초 1회 실행했는지 |
| 프론트엔드에서 "백엔드에 연결할 수 없습니다" | 백엔드(`run.bat`)가 실행 중인지, `frontend/.env.local`의 주소가 맞는지 |
| 백엔드 실행 시 MySQL 연결 오류 | MySQL 서비스가 켜져 있는지, `backend/.env`의 `DATABASE_URL` root 비밀번호가 맞는지 |
| `Access denied for user 'root'@'127.0.0.1'` | root 계정이 `localhost` 전용으로만 등록된 경우다. 위 2번 항목의 안내대로 `root`@`127.0.0.1` 계정을 추가로 등록한다 |
| Mock 실행 시 401 오류 | `mock_pi/.env`의 `DEVICE_ID`/`API_KEY`가 대시보드에서 발급받은 값과 정확히 일치하는지 |
| 라즈베리파이(또는 다른 PC)에서 백엔드 접속 안 됨 | Windows 방화벽 인바운드 규칙(8000번 포트), 같은 네트워크 대역인지, `run.bat`이 `--host 0.0.0.0`로 켜져 있는지 |
| 대시보드에 값은 오는데 갱신이 느림 | 정상 동작(1~2초 폴링 방식). 더 빠르게 하려면 `mock_pi` 실행 시 `--push-interval`, `--poll-interval` 값을 줄인다 |
