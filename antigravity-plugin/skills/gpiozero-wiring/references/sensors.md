# 센서 배선/코드 레퍼런스

| type_key | 권장 클래스/라이브러리 | 최소 코드 | 비고 |
|---|---|---|---|
| `pressure` | `gpiozero.MCP3008` (SPI ADC) | `mcp = MCP3008(channel=0); value = mcp.value * 1000` | 아날로그 출력 → ADC 필수. 실제 센서 스펙에 맞게 스케일 보정 |
| `keypad` | gpiozero 기본 미지원 → row/col 스캔 | 행: `DigitalOutputDevice`, 열: `DigitalInputDevice(pull_up=True)`로 직접 스캔하거나 `adafruit-circuitpython-matrixkeypad` 사용 | 4x4면 핀 8개 필요 |
| `reed_switch` | `gpiozero.Button(pin, pull_up=True)` | `closed = button.is_pressed` | 리드 스위치는 버튼과 동일하게 취급 가능 |
| `flame` | 디지털: `gpiozero.Button` / 아날로그: `MCP3008` | `detected = not button.is_pressed`(모듈에 따라 active-low) | 모듈 데이터시트로 active-high/low 확인 |
| `dht11` | gpiozero 미지원(1-wire 정밀 타이밍) → `adafruit-circuitpython-dht` | `dht = adafruit_dht.DHT11(board.D4); t = dht.temperature; h = dht.humidity` | 읽기 실패가 잦은 센서 — `RuntimeError` 재시도 로직 필요 |
| `hcsr04` | `gpiozero.DistanceSensor(echo=, trigger=)` | `distance_cm = sensor.distance * 100` | `.distance`는 0~1(m) 스케일 |
| `push_button` | `gpiozero.Button(pin)` | `pressed = button.is_pressed` | |
| `illuminance` | CDS(아날로그): `MCP3008` / BH1750(I2C): `smbus2` 또는 `adafruit-circuitpython-bh1750` | `lux = bh1750.lux` | I2C 모듈이 배선/보정 면에서 더 간단 |
| `qr_scanner` | 카메라 필요 — GPIO 아님 | 해당 없음 | `skills/vision-trigger/` 참고 |
| `object_detector` | 카메라 필요 — GPIO 아님 | 해당 없음 | `skills/vision-trigger/` 참고 |

`adafruit-circuitpython-*` 계열 라이브러리는 `pip install adafruit-blinka <패키지명>`으로
설치한다 (Blinka가 라즈베리파이 GPIO를 CircuitPython API로 감싸준다).
