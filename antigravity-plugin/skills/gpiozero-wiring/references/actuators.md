# 액추에이터 배선/코드 레퍼런스

| type_key | 권장 클래스 | 최소 코드 | 비고 |
|---|---|---|---|
| `led` | `gpiozero.PWMLED(pin)` | `led.value = (brightness_pct / 100) if on else 0` | 밝기 제어가 필요 없으면 `gpiozero.LED`로도 충분 |
| `dc_motor` | `gpiozero.Motor(forward=, backward=)` | `speed = speed_pct / 100; motor.forward(speed) if speed >= 0 else motor.backward(-speed)` | 모터드라이버(L298N 등) 필요 |
| `solenoid` | `gpiozero.OutputDevice(pin)` | `sol.on() if on else sol.off()` | 릴레이/트랜지스터로 구동 (직접 GPIO로 큰 전류를 흘리지 않는다) |
| `neopixel` | gpiozero 미지원(정밀 비트타이밍) → `adafruit-circuitpython-neopixel` | `pixels.fill((r, g, b)); pixels.brightness = brightness_pct / 100; pixels.show()` | 데이터 핀 1개, 별도 전원 권장(개수 많을 때) |
| `buzzer` | `gpiozero.PWMOutputDevice(pin)` | `buzzer.frequency = freq_hz; buzzer.on() if on else buzzer.off()` | 수동 부저는 주파수를 무시하고 on/off만 반응할 수 있음 |
| `servo` | `gpiozero.AngularServo(pin, min_angle=0, max_angle=180)` | `servo.angle = angle_deg` | SG-90은 별도 5V 전원 권장(라즈베리파이 5V 핀 부하 주의) |
| `relay` | `gpiozero.OutputDevice(pin)` | `relay.on() if on else relay.off()` | 모듈에 따라 active-low(신호 반전) — 배선 후 실제 동작으로 확인 |

`apply(desired: dict) -> dict` 함수는 위 코드로 실제 상태를 바꾼 뒤, 반영된 실제
상태를 그대로 `dict`로 반환한다 (`mock_pi/actuators/*.py`와 같은 패턴).
