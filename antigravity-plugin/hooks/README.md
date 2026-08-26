# hooks 사용 참고

`hooks.json`의 이벤트 이름/필드(`event`, `match`, `run` 등)는 2026년 8월 기준
공개된 Antigravity 문서 요약을 참고해 작성했다. 정확한 스키마는 IDE 버전에 따라
달라질 수 있으니, 실제로 훅이 발동하지 않으면 Antigravity 자체 문서(Hooks 항목)를
설치된 버전 기준으로 확인해 이벤트 이름만 맞춰 조정한다 — 아래 스크립트들
(`scripts/*.py`) 자체는 독립적으로도 그냥 실행 가능하므로, JSON 연결부만 손보면 된다.

## 훅 목록

| 이름 | 시점 | 하는 일 |
|---|---|---|
| `check-env-before-run` | `python run.py` 실행 전 | `.env` 파일 존재 여부 확인, 없으면 경고 |
| `format-after-write` | `.py` 파일 저장 후 | `black`으로 자동 포맷 (설치 안 되어 있으면 조용히 건너뜀) |
| `check-pin-conflicts` | `sensors/`, `actuators/` 파일 저장 후 | 같은 GPIO 핀이 여러 파일에서 쓰였는지 휴리스틱 경고 |

`check-pin-conflicts`는 정규식 기반 휴리스틱이라 오탐/누락이 있을 수 있다 —
참고용이며, 실제 배선 확인을 대체하지 않는다.
