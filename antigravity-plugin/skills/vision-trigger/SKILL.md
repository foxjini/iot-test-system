---
name: vision-trigger
description: 프로젝트 주제에 영상 인식(QR코드, 객체 인식 등)을 트리거로 추가할 때 사용한다. "카메라", "영상 인식", "QR", "YOLO", "mediapipe", "트리거"가 언급되면 이 스킬을 불러온다. 모든 팀에 필요한 기능이 아니므로 요청받았을 때만 적용한다.
---

# 영상/QR 트리거

이 기능은 **선택 사항**이다 — 프로젝트 주제가 영상 인식을 필요로 하는 팀만 쓴다.
카탈로그의 `qr_scanner`/`object_detector`(`rules/02-catalog-contract.md`)를 통해
결과를 보고한다는 점은 항상 같지만, **인식 연산을 어디서 하는지**는 두 가지로 나뉜다.

## 1. 처리 위치부터 정한다: 라즈베리파이 vs 백엔드(Windows PC)

`references/options.md`의 비교표를 보고 아래 기준으로 정한다.

- **QR코드 인식만 필요** → 연산이 가볍다(OpenCV만으로 충분). 라즈베리파이에서 직접
  처리해도 되고, 이미 백엔드 오프로드 엔드포인트가 있으니 편의상 그쪽을 써도 된다.
- **YOLO 등 다중 클래스 객체 인식** → 라즈베리파이 5는 GPU 가속이 없어 CPU만으로는
  무겁다. 실시간성이 꼭 필요하지 않다면 **백엔드(Windows PC)로 오프로드**하는 쪽을
  기본으로 권장한다. Windows PC에 GPU가 있거나, 라즈베리파이에 AI 가속 HAT(Hailo 등)이
  있다면 로컬 처리도 가능하다.
- 어느 쪽이든, 인식 결과가 **즉시 하드웨어 반응(트리거)**으로 이어져야 한다면 최종
  판단·액추에이터 구동은 라즈베리파이 쪽 코드가 맡는 것을 권장한다 (백엔드 왕복
  지연에 좌우되지 않는 "로컬 반사" 방식 — 대시보드에는 결과만 별도로 보고).

## 2. 템플릿

- `templates/qr_local.py` — 라즈베리파이에서 OpenCV로 직접 QR 인식
- `templates/qr_offload_client.py` — 프레임을 백엔드 `/api/vision/qr`로 보내 인식
- `templates/object_detector_local.py` — 라즈베리파이에서 경량 YOLO(nano) 모델로 객체 인식

## 3. 결과 보고 + 트리거 연결

인식 결과는 `qr_scanner`(`detected`, `payload`) 또는 `object_detector`(`label`,
`confidence`, `count`) 컴포넌트에 대해 평소 센서와 똑같이
`push_telemetry()`(`skills/backend-api-client/`)로 올린다. 트리거 로직(예: 특정
QR 값이 감지되면 서보를 90도로) 자체는 이 프로젝트의 일반 코드이지, 백엔드가
대신 판단해주지 않는다 — 백엔드는 어디까지나 텔레메트리를 저장/표시하는 역할이다.

자세한 절차는 `workflows/add-vision-trigger.md`.
