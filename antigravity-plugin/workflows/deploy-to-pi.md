# 워크플로우: 윈도우(Antigravity) → 라즈베리파이 배포/실행

## 최초 1회 준비

1. 라즈베리파이에서 SSH 활성화: `sudo raspi-config` → `Interface Options` → `SSH` → `Yes`
   (헤드리스라면 SD카드 boot 파티션에 빈 `ssh` 파일을 두는 방법도 가능).
2. 라즈베리파이의 LAN IP 확인: `hostname -I` (라즈베리파이에서) 또는 공유기 관리 페이지.
3. Windows PowerShell에서 접속 테스트: `ssh pi@<라즈베리파이IP>` (Windows 10/11은
   OpenSSH 클라이언트가 기본 내장되어 있어 추가 설치가 필요 없다).
4. 화면이 필요한 디버깅(카메라 미리보기 등)을 위해 RealVNC Viewer로도 한 번 접속해
   둔다 — 같은 LAN 안에서는 Direct 연결이 무료다 (`rules/01-stack.md` 참고). Trixie에서
   `realvnc-vnc-server`가 없다면 `sudo apt install realvnc-vnc-server` 후
   `raspi-config`에서 X11로 전환 → 재부팅 → VNC 활성화 순서로 진행한다.

## 코드를 올릴 때마다

1. Windows PowerShell에서 프로젝트 폴더로 이동한다.
2. 전체 복사(최초 1회 또는 구조가 크게 바뀌었을 때):
   ```powershell
   scp -r .\project pi@<라즈베리파이IP>:/home/pi/project
   ```
3. 이후에는 바뀐 파일만 다시 올리거나(작은 프로젝트라 전체 재복사도 무방하다),
   Git Bash/WSL이 있다면 `rsync -avz --delete ./project/ pi@<IP>:/home/pi/project/`로
   더 빠르게 동기화할 수 있다 (선택 사항, 필수 아님).
4. 라즈베리파이에서 실행:
   ```bash
   ssh pi@<라즈베리파이IP>
   cd project
   source .venv/bin/activate
   python run.py
   ```
5. 로그/출력은 SSH 터미널에서 바로 보고, 카메라 미리보기 등 화면 확인이 필요하면
   RealVNC로 별도 접속해 확인한다.
6. 종료는 SSH 세션에서 Ctrl+C.

## 참고

`.env`는 `scp`로 함께 올리지 않는다(각 기기에서 직접 만든다) — 실수로 API Key가
Windows 쪽 저장소에만 있는 값과 라즈베리파이 쪽 값이 서로 다르게 남는 것을 막기 위해,
라즈베리파이 쪽 `.env`는 최초 1회만 만들어두고 이후 배포에서는 건드리지 않는다.
