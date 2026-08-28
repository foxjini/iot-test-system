# antigravity-plugin — 라즈베리파이 5 IoT 캡스톤 팀용 Antigravity 플러그인

각 팀의 라즈베리파이 5 담당 학생이, Windows PC의 **Antigravity 2.0 IDE**로 실제
작품 코드를 바이브 코딩할 때 쓰는 플러그인이다. `iot-test-system`(범용 테스트
백엔드+프론트엔드)과 같은 REST API 계약, 같은 센서/액추에이터 카탈로그를 AI
에이전트가 항상 알고 있도록 만든다.

**이 폴더 자체가 실행되는 프로그램은 아니다** — 각 팀의 실제 프로젝트 폴더에
설치해서 Antigravity가 그 컨텍스트를 읽게 만드는 설정 묶음이다.

## 이 플러그인의 역할 (중요 — 꼭 읽기)

이 플러그인은 **팀의 진짜 백엔드가 준비되기 전, 임시 테스트 시스템
(`iot-test-system`)에 연동해서 라즈베리파이 코드를 미리 연습·개발**하는 용도다.
팀의 진짜 백엔드/프론트엔드는 백엔드/프론트엔드 담당 학생이
`agent-vibe-coding-starter-kit2`로 별도 개발하는데, 그 시스템은 이 플러그인이
따르는 계약(`docs/API.md`)과 **경로·인증 헤더·응답 형식이 전부 달라서** 그대로
이어 붙지 않는다.

- **진짜 백엔드가 준비되면**: 이 플러그인으로 만든 `client.py`/`run.py`를 그대로
  갖다 쓰지 말고, `agent-vibe-coding-starter-kit2`의 `hardware-agent`와
  `.agents/workflows/hardware-swap.md` 경로를 따라 `pi/main.py`를 새로 만든다.
  그 시스템은 이미 자체적으로 실기기 연동 경로(`DeviceProvider`, desired-state
  폴링, 공유 `DEVICE_API_KEY`)를 갖추고 있다 — 이 플러그인이 만든 계약과 다리를
  놓을 필요 없이, 그 경로를 그대로 따르면 된다.
- **그대로 옮겨 쓰는 것**: gpiozero 클래스 선택(`DistanceSensor`, `AngularServo`,
  `PWMLED` 등), lgpio 핀팩토리 필요성, 센서/액추에이터 배선과 로직 자체 —
  `docs/SENSOR_ACTUATOR_PROMPTS.md`에서 연습한 내용이 그대로 유효하다.
- **새로 만들어야 하는 것**: REST 클라이언트(`client.py`) 전체 — 경로/헤더/필드명이
  달라서 재사용할 수 없다.

## 설치 방법

Antigravity는 플러그인을 워크스페이스(팀이 Antigravity로 여는 프로젝트 폴더)
루트의 `.agents/plugins/<플러그인이름>/`에서 찾는다. `AGENTS.md`는 플러그인
폴더가 아니라 **워크스페이스 루트**에서 세션 시작 시 읽힌다. 따라서 팀의 실제
프로젝트 폴더가 예를 들어 `D:\team3-pi-project`라면:

1. 이 폴더(`antigravity-plugin/`) 전체를 복사한다.
2. `AGENTS.md`는 워크스페이스 루트로: `D:\team3-pi-project\AGENTS.md`
   (이미 그 프로젝트에 다른 `AGENTS.md`가 있다면 내용을 이어 붙인다).
3. 나머지(`plugin.json`, `mcp_config.json`, `agents/`, `rules/`, `workflows/`,
   `skills/`, `hooks/`)는 `D:\team3-pi-project\.agents\plugins\iot-pi5-vibe-coding\`
   아래에 그대로 넣는다.
4. Antigravity에서 그 프로젝트 폴더를 워크스페이스로 열면 자동으로 인식된다.

> 위 경로/구조는 2026년 8월 기준 공개된 Antigravity 문서를 참고해 작성했다.
> IDE 버전에 따라 세부 사항이 바뀔 수 있으니, 플러그인이 인식되지 않으면
> Antigravity의 Plugins 설정 화면에서 실제 스캔 경로를 확인한다.

## 이 프로젝트가 필요로 하는 것들 (최초 1회 확인)

- 라즈베리파이 5, Raspberry Pi OS **Trixie**.
- SSH 활성화 (`sudo raspi-config` → Interface Options → SSH) — WinSCP로 파일을
  올리려면 필요하다.
- (코드 전달용) **WinSCP** — Windows에 설치하는 무료 SFTP GUI 클라이언트(winscp.net).
- (화면 디버깅용) **RealVNC** — 같은 LAN에서 Direct 연결은 무료. Trixie는
  `sudo apt install realvnc-vnc-server` + X11 전환이 필요할 수 있다.
- `iot-test-system/backend`가 Windows PC에서 실행 중이어야 실제 연동 테스트가 된다
  (`docs/STUDENT_GUIDE.md` 참고).

자세한 내용은 `rules/01-stack.md`, 배포 절차는 `workflows/deploy-to-pi.md`.

## 사용 방법 (실습 흐름)

이 플러그인은 외워서 치는 명령어가 없다. Antigravity 채팅창에 우리 팀 프로젝트에
대해 하고 싶은 말을 그냥 한국어로 하면, 에이전트가 `rules/`·`skills/`·`workflows/`
내용을 알아서 참고해서 답한다. 처음 써본다면 아래 순서를 그대로 한 번 따라 해보는
것을 추천한다. 각 단계는 채팅창에 그대로 복사해서 부품/핀 번호만 바꿔 써도 된다.
(혹시 에이전트가 엉뚱한 방향으로 가면 "`workflows/new-sensor.md` 절차대로 진행해줘"
처럼 파일 이름을 직접 말해줘도 된다.)

### 0단계 — 플러그인이 잘 로드됐는지 확인

워크스페이스를 처음 열면 채팅창에 이렇게 물어본다.

```
너 지금 이 프로젝트에 대해 뭘 알고 있어? 우리가 쓰는 하드웨어랑 통신 방식을 설명해줘.
```

라즈베리파이 5, Trixie, gpiozero/lgpio, 테스트 백엔드와 REST로 통신한다는 이야기가
나오면 잘 로드된 것이다. "그런 정보는 없다"는 식으로 답하면 설치 경로가 잘못됐을
가능성이 크다 — 위 "설치 방법"을 다시 확인한다.

### 1단계 — 센서 하나 연동해보기

우리 팀이 실제로 쓸 센서를 하나 정해서 요청한다 (예시: 초음파 센서).

```
초음파 센서(HC-SR04)로 거리를 측정하는 코드를 만들어줘.
트리거 핀은 GPIO23, 에코 핀은 GPIO24를 쓸 거야.
```

`sensors/hcsr04.py` 같은 파일이 만들어진다. 확인할 점은 아래 "결과물 확인하기" 참고.
잘 모르겠으면 이렇게 되물어도 된다: `이 코드가 카탈로그 계약이랑 맞는지 확인해줘.`

### 2단계 — 액추에이터 하나 연동해보기

```
서보모터(SG-90)를 GPIO18에 연결해서 각도를 제어하는 코드를 만들어줘.
```

### 3단계 — 테스트 백엔드에 실제로 연결해보기

먼저 Windows PC에서 범용 테스트 시스템의 backend/frontend가 실행 중이어야 한다
(`docs/STUDENT_GUIDE.md` 1~5번을 먼저 끝낸다). 대시보드에서 디바이스를 등록해
device_id/API Key를 받은 다음 채팅창에 요청한다.

```
mock_pi/client.py 같은 방식으로 우리 프로젝트용 client.py를 만들고,
.env에서 BACKEND_URL/DEVICE_ID/API_KEY를 읽어오게 해줘.
그리고 방금 만든 센서/액추에이터 코드를 여기에 연결해줘.
```

실행해서 대시보드에 센서 값이 올라오는지, 대시보드에서 액추에이터를 조작했을 때
실제로 반응하는지 확인한다(순서는 `workflows/connect-and-test.md`와 같다).

### 4단계 — 라즈베리파이에 올려서 실제로 돌려보기

```
이 프로젝트를 라즈베리파이에 배포하고 실행하는 절차를 알려줘.
```

라고 물으면 `workflows/deploy-to-pi.md`의 WinSCP/RealVNC 절차를 안내해 준다. 처음엔
아래 요약만 기억해도 된다: ① WinSCP로 프로젝트 폴더를 라즈베리파이에 복사 →
② WinSCP의 "Open Terminal"(또는 별도 SSH)로 접속해 `python run.py` 실행 →
③ 화면 확인이 필요하면 RealVNC Viewer로 접속.

### (선택) 영상/QR 트리거가 필요하면

```
우리 프로젝트에 QR코드를 인식해서 문이 열리는 기능을 추가하고 싶어.
라즈베리파이에서 직접 처리할지 백엔드로 넘길지도 같이 정해줘.
```

## 결과물 확인하기 (AI가 만든 코드를 그대로 믿지 않기)

바이브 코딩은 편하지만 에이전트가 만든 코드가 항상 맞는 것은 아니다. 아래 3가지는
매번 눈으로 확인하는 습관을 들인다.

1. **필드 이름이 카탈로그와 정확히 같은가** — `rules/02-catalog-contract.md`를 열어
   우리가 쓰는 타입의 필드 이름(예: `distance_cm`)과 생성된 코드가 반환하는 값의
   키가 글자까지 정확히 같은지 비교한다. 하나라도 다르면 대시보드에 값이 안 뜬다.
2. **`GPIOZERO_PIN_FACTORY=lgpio`가 지정되어 있는가** — 없으면 라즈베리파이 5에서
   아예 실행되지 않는다.
3. **핀 번호가 다른 센서/액추에이터와 겹치지 않는가** — 같은 GPIO 핀을 두 부품이
   같이 쓰면 둘 다 오작동한다.

모르는 용어가 나오면 "이 코드에서 OO가 뭐 하는 부분이야?"처럼 에이전트에게 바로
되물어봐도 된다 — 그것도 정상적인 사용법이다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 에이전트가 우리 하드웨어/API 계약을 전혀 모르는 것 같음 | "설치 방법"대로 파일 위치가 맞는지 다시 확인 |
| 생성된 코드를 실행했는데 대시보드에 값이 안 올라옴 | 필드 이름이 `rules/02-catalog-contract.md`와 정확히 같은지, `.env`의 DEVICE_ID/API_KEY가 맞는지 |
| 라즈베리파이 실행 시 GPIO 관련 오류 | `GPIOZERO_PIN_FACTORY=lgpio` 지정 여부, 핀 번호 중복 여부 (`rules/01-stack.md`) |
| WinSCP 접속 안 됨 | 라즈베리파이 SSH 활성화 여부 (`sudo raspi-config`) |
| RealVNC 접속 안 됨 | `realvnc-vnc-server` 설치 여부, Trixie가 X11로 전환되어 있는지 (`rules/01-stack.md`) |
| 어떤 문장으로 물어봐야 할지 모르겠음 | 위 "사용 방법"의 예시 문장을 그대로 복사해서 부품 이름/핀 번호만 우리 팀 것으로 바꿔 써본다 |

## 구성

| 폴더/파일 | 역할 |
|---|---|
| `AGENTS.md` | 워크스페이스 루트에 두는 표준 컨텍스트 (요약) |
| `mcp_config.json` | Context7 MCP 연결 (라이브러리 최신 문서 조회, 설치 불필요) |
| `rules/` | 항상 적용: 스택, 카탈로그 계약, API 계약, 코드 관례 |
| `agents/` | 서브에이전트: gpio-agent, api-agent, vision-agent |
| `workflows/` | 반복 절차: 센서/액추에이터/비전 트리거 추가, 연결 테스트, 배포 |
| `skills/` | 필요할 때만 로드: gpiozero 배선, 백엔드 클라이언트, 비전 트리거 |
| `hooks/` | 사전 점검·자동 포맷·핀 중복 경고 (스키마는 `hooks/README.md` 참고) |

## 이 플러그인이 다루지 않는 것

- 팀의 회로 설계/기구 설계 자체 (하드웨어 담당 학생의 영역).
- `iot-test-system` 백엔드/프론트엔드 자체의 수정 — 그건 저장소 루트의
  `backend/`, `frontend/`를 직접 고친다 (이 플러그인은 그걸 "쓰는" 쪽이다).
