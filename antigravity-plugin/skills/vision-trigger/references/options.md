# 비전 처리 옵션 비교

| 방식 | 처리 위치 | 필요 설치 | 장점 | 단점 |
|---|---|---|---|---|
| QR (OpenCV) | 라즈베리파이 or 백엔드 | `opencv-python` | 가볍다, GPU 불필요, 의존성 최소 | QR 전용 (다중 클래스 인식 불가) |
| QR (pyzbar) | 라즈베리파이 or 백엔드 | `pyzbar`, `opencv-python` | 인식률이 opencv 기본 디코더보다 나은 경우가 있음 | 시스템 라이브러리(`libzbar0`) 별도 설치 필요 |
| YOLO(nano) | 백엔드 권장(무거우면), 가속기 있으면 Pi | `ultralytics` (+ torch) | 다중 클래스, 범용 객체 인식 | 설치 용량 크고, Pi 5 CPU 단독으론 느릴 수 있음 |
| mediapipe Tasks | 백엔드 또는 Pi | `mediapipe` | YOLO보다 가볍고 CPU 친화적(사람/손/얼굴 등 특화 태스크) | 범용 다중 클래스 인식엔 YOLO보다 제한적 |

라즈베리파이 5에 GPU 가속이 없다는 점이 기준이다. 학교에 Raspberry Pi AI
Kit/HAT(Hailo 등) 같은 가속기가 있다면 로컬 처리도 실시간으로 충분히 가능하다 —
없다면 무거운 모델은 백엔드로 오프로드하는 쪽이 안정적이다.

## 백엔드 오프로드 엔드포인트 (`POST /api/vision/qr`)

백엔드 쪽에 `opencv-python`을 추가 설치해야 동작한다
(`backend/requirements-vision.txt`, 기본 설치에는 포함되지 않는다):

```bash
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements-vision.txt
```

요청/응답 예시:

```json
// POST /api/vision/qr  (헤더: X-Device-Key)
{ "image_base64": "<JPEG/PNG를 base64로 인코딩한 문자열>" }
```

```json
// 200 응답
{ "detected": true, "payload": "TEAM3-DOOR-OPEN" }
```

YOLO/mediapipe는 백엔드에 전용 엔드포인트를 만들어두지 않았다 — 설치 용량이 크고
팀마다 쓰는 모델/클래스가 다르기 때문이다. 백엔드에서 처리하고 싶다면
`templates/object_detector_local.py`의 추론 부분을 백엔드 PC에서 별도 스크립트로
돌리고, 그 스크립트가 직접 `push_telemetry()`를 호출하도록 구성한다(백엔드 PC에서
실행되지만 이 REST 계약상으로는 "이 디바이스의 텔레메트리를 올리는 클라이언트"일
뿐이라 새로운 개념이 필요 없다).
