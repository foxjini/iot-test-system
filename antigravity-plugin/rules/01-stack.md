# 스택/개발 환경 규칙

## 하드웨어

- 대상 보드: **Raspberry Pi 5**, OS: Raspberry Pi OS **Trixie** (Debian 13 기반).
- GPIO 라이브러리는 **gpiozero**를 우선 사용한다. 반드시 다음을 전제로 코드를 작성한다:
  - `gpiozero>=2.0.1.post3` (그 이전 버전은 Pi 5 설치 관련 버그가 있었다).
  - 핀팩토리는 **lgpio** (`pip install lgpio`, 또는 `gpiozero[lgpio]`). Pi 5의 GPIO는
    RP1이라는 별도 칩을 통하는데, 구형 `RPi.GPIO`/기본 핀팩토리는 이를 지원하지
    않는다. `.env` 또는 코드 상단에서 `GPIOZERO_PIN_FACTORY=lgpio`를 명시하거나,
    `from gpiozero.pins.lgpio import LGPIOFactory` + `Device.pin_factory = LGPIOFactory()`로
    명시적으로 지정하는 것을 기본값으로 한다.
  - gpiozero가 지원하지 않는 장치(DHT11 같은 1-wire 타이밍 센서, WS2812 네오픽셀 같은
    정밀 비트 타이밍 LED)는 무리하게 gpiozero로 구현하지 말고 전용 라이브러리를 쓴다.
    자세한 항목별 선택은 `skills/gpiozero-wiring/`을 따른다.

## 개발 워크플로우 (윈도우 PC ↔ 라즈베리파이 5)

- 코드 편집: Windows PC의 **Antigravity 2.0 IDE**. 실행/검증은 라즈베리파이에서 한다.
- **코드 전달: WinSCP**(무료 SFTP GUI 클라이언트, winscp.net). SSH(SFTP) 위에서
  동작하므로 라즈베리파이에 별도 서버를 깔 필요 없이 SSH만 켜져 있으면 된다.
  듀얼 패널 드래그 앤 드롭 복사, "Synchronize" 기능으로 바뀐 파일만 반영할 수
  있다. 정확한 절차는 `workflows/deploy-to-pi.md`.
- 라즈베리파이에서 SSH 활성화: `sudo raspi-config` → `Interface Options` → `SSH` → `Yes`
  (헤드리스 초기 설정 시에는 부팅 파티션에 빈 `ssh` 파일을 두는 방법도 가능).
- **화면이 필요한 디버깅**(카메라 미리보기, GUI 확인 등)에는 **TightVNC**를 쓴다.
  - Trixie는 기본 데스크톱이 **Wayland**인데, TightVNC(고전 Xvnc 기반)는 **X11**이
    있어야 동작한다. `raspi-config` → Advanced Options에서 Wayland → X11로 전환하고
    재부팅한 뒤 `sudo apt install tightvncserver`로 설치한다.
  - 이전에 RealVNC를 설치해 뒀다면 TightVNC 설치 중 충돌해서 제거될 수 있다 —
    이제 TightVNC만 쓸 거라면 문제 없다.
  - 설치 후 라즈베리파이에서 `vncserver :1`로 세션을 직접 띄운다(최초 실행 시
    비밀번호를 설정한다). 재부팅하면 다시 실행해야 한다.
  - Windows에는 **TightVNC Viewer**(tightvnc.com, 무료)를 설치하고
    `<라즈베리파이IP>:1`(포트로는 `:5901`)로 접속한다.

## 최신 라이브러리 문서 (Context7 MCP)

`mcp_config.json`으로 Context7(https://context7.com) MCP를 연결해 뒀다. gpiozero,
adafruit-circuitpython-*, ultralytics, mediapipe처럼 버전이 자주 바뀌는 라이브러리를
쓸 때는 이 스킬 문서의 고정된 예시 코드만 믿지 말고, Context7로 해당 라이브러리의
**그 시점 최신 문서**를 직접 조회해서 API가 안 바뀌었는지 확인하는 것을 권장한다
(예: "gpiozero의 DistanceSensor 최신 사용법을 Context7로 확인해줘"). 별도 설치
없이 원격 MCP로 연결되어 있어 바로 쓸 수 있다.

## 참고 자료

- gpiozero 설치/핀팩토리: https://gpiozero.readthedocs.io/en/stable/installing.html
- Pi 5 lgpio 이슈 이력: https://github.com/gpiozero/gpiozero/issues/1166
- WinSCP: https://winscp.net/
- Raspberry Pi에 TightVNC 설치(Wayland/X11 전환 포함): https://www.penguintutor.com/raspberrypi/tightvnc
