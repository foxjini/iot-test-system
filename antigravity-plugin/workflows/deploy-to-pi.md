# 워크플로우: 윈도우(Antigravity) → 라즈베리파이 배포/실행

## 최초 1회 준비

1. 라즈베리파이에서 SSH 활성화: `sudo raspi-config` → `Interface Options` → `SSH` → `Yes`
   (헤드리스라면 SD카드 boot 파티션에 빈 `ssh` 파일을 두는 방법도 가능).
2. 라즈베리파이의 LAN IP 확인: `hostname -I` (라즈베리파이에서) 또는 공유기 관리 페이지.
3. Windows에 **WinSCP**(winscp.net, 무료)를 설치하고 새 사이트를 만든다: 파일
   프로토콜 SFTP, 호스트에 라즈베리파이 IP, 사용자명/비밀번호는 라즈베리파이
   로그인 계정. 접속하면 왼쪽(Windows)/오른쪽(라즈베리파이) 듀얼 패널이 보인다.
4. 화면이 필요한 디버깅(카메라 미리보기 등)을 위해 **TightVNC**도 준비한다
   (`rules/01-stack.md` 참고 — Trixie는 Wayland가 기본이라 X11 전환이 먼저
   필요하다). 설치 후 라즈베리파이에서 `vncserver :1`로 세션을 띄우고, Windows의
   TightVNC Viewer로 `<라즈베리파이IP>:1`에 접속해 한 번 확인해 둔다.

## 코드를 올릴 때마다

1. WinSCP 왼쪽(Windows) 패널을 프로젝트 폴더로, 오른쪽(라즈베리파이) 패널을
   실행 위치(예: `/home/pi/project`)로 맞춘다.
2. 최초 1회 또는 폴더 구조가 크게 바뀌었을 때는 왼쪽 폴더 전체를 오른쪽으로
   드래그 앤 드롭해서 복사한다.
3. 이후에는 툴바의 **Synchronize**(`Commands` → `Synchronize`)로 바뀐 파일만
   반영한다 — 매번 전체를 다시 옮기지 않아도 된다. `.env`는 동기화 대상에서
   제외한다(아래 참고).
4. 라즈베리파이에서 실행 — WinSCP의 `Commands` → `Open Terminal`(또는 별도로
   PowerShell에서 `ssh pi@<IP>`)로 접속해:
   ```bash
   cd project
   source .venv/bin/activate
   python run.py
   ```
5. 로그/출력은 그 터미널에서 바로 보고, 카메라 미리보기 등 화면 확인이 필요하면
   TightVNC Viewer로 별도 접속해 확인한다.
6. 종료는 터미널 세션에서 Ctrl+C.

## 참고

`.env`는 WinSCP로 함께 올리지 않는다(각 기기에서 직접 만든다) — 실수로 API Key가
Windows 쪽 값과 라즈베리파이 쪽 값이 서로 다르게 남는 것을 막기 위해, 라즈베리파이
쪽 `.env`는 최초 1회만 만들어두고 이후 배포에서는 건드리지 않는다. WinSCP의
Synchronize 설정에서 `.env`를 제외 규칙에 추가해 두면 실수로 덮어쓸 일이 없다.
