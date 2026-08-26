---
name: gpiozero-wiring
description: 카탈로그 센서/액추에이터를 라즈베리파이 5의 GPIO에 배선하고 코드로 제어할 때 사용한다. "배선", "핀", "GPIO", "gpiozero", 또는 센서/액추에이터 이름(DHT11, HC-SR04, 서보, 네오픽셀 등)이 언급되면 이 스킬을 불러온다.
---

# gpiozero 배선/코드 레퍼런스

카탈로그 항목 중 상당수는 `gpiozero`로 바로 되지만, 일부(DHT11, 네오픽셀 등)는
타이밍이 정밀해서 gpiozero가 지원하지 않는다 — 이런 항목은 무리하게 gpiozero로
구현하지 말고 전용 라이브러리를 쓴다. 항목별 정확한 선택은 아래 레퍼런스를 따른다.

- `references/sensors.md` — 센서 8종 + 비전 센서 2종
- `references/actuators.md` — 액추에이터 7종

## 공통 규칙

- 핀팩토리는 항상 lgpio다: 코드 시작 전에 `GPIOZERO_PIN_FACTORY=lgpio` 환경변수를
  쓰거나, `Device.pin_factory = LGPIOFactory()`를 명시한다 (`rules/01-stack.md` 참고).
  이걸 빼먹으면 Pi 5에서 RP1 칩 미지원으로 아예 동작하지 않는다.
- BCM 핀 번호(GPIOxx) 기준으로 코드를 작성한다. 실제 사용 핀은 팀의 회로 설계에
  맞춰 바꾸되, 이미 다른 컴포넌트가 쓰는 핀과 겹치지 않는지 확인한다.
  (`hooks/hooks.json`의 핀 중복 점검 훅이 이를 보조한다.)
  I2C(BH1750 등)를 쓰려면 `sudo raspi-config` → Interface Options → I2C를 먼저
  켜야 한다. SPI(MCP3008)도 마찬가지로 Interface Options → SPI를 켜야 한다.
- 카탈로그 필드 계약(`rules/02-catalog-contract.md`)에 맞는 타입/범위로 값을
  변환해서 반환한다 (예: gpiozero의 0~1 스케일 값을 카탈로그의 실제 단위로 환산).
